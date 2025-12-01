import asyncio
import json
from contextlib import AsyncExitStack
from datetime import datetime
from datetime import timedelta
from typing import Optional, Any

import requests
from flask_jwt_extended import (
    create_access_token
)
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.types import CallToolResult

from app.app import db
from app.services.app_center.node_params_service import load_properties


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
    # methods will go here

    async def connect_to_server(self, server_url: str, headers: dict = None):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        """Connect to an MCP server running with SSE transport"""
        # 创建 SSE 客户端连接上下文管理器
        self._streams_context = sse_client(url=server_url, headers=headers)
        # 异步初始化 SSE 连接，获取数据流对象
        streams = await self._streams_context.__aenter__()

        # 使用数据流创建 MCP 客户端会话上下文
        self._session_context = ClientSession(*streams)
        # 初始化客户端会话对象
        self.session: ClientSession = await self._session_context.__aenter__()

        # 执行 MCP 协议初始化握手
        await self.session.initialize()

    async def list_tools(self) -> list[Any]:
        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]
        return available_tools

    async def call_tool(self, name, params) -> CallToolResult:
        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]
        # Execute tool call
        return await self.session.call_tool(name, params)

    async def cleanup(self):
        """Clean up resources"""
        try:
            # 先清理 session
            if self._session_context:
                await self._session_context.__aexit__(None, None, None)
                self._session_context = None

            # 再清理 streams
            if self._streams_context:
                await self._streams_context.__aexit__(None, None, None)
                self._streams_context = None

            self.session = None
            self._is_connected = False
            print("Resources cleaned up successfully")

        except Exception as e:
            print(f"Error during cleanup: {e}")


def tool_node_execute(task_params, task_record, global_params):
    """
    工具节点执行器
        1. 读取节点信息
        2. 组装工具参数
        3. 发起请求
        4. 处理返回结果
        5. 更新任务状态

    :param task_params:
    :param task_record:
    :param global_params:
    :return:
    """
    # 解析 header 参数
    headers_schema = task_record.workflow_node_tool_http_header.get("properties", {})
    headers = load_properties(headers_schema, global_params)
    if task_record.workflow_node_tool_configs.get("protocol") == "https":
        return https_node_execute(headers, task_record, global_params)
    elif task_record.workflow_node_tool_configs.get("protocol") == "mcp":
        return mcp_node_execute(headers, task_record, global_params)
    else:
        return None


def https_node_execute(headers, task_record, global_params):
    """
    HTTP节点执行器
    :param headers:
    :param task_params:
    :param task_record:
    :param global_params:
    :return:
    """
    if "Authorization" not in headers:
        access_token = create_access_token(identity=str(task_record.user_id),
                                           expires_delta=timedelta(days=30)
                                           )
        headers["Authorization"] = f"Bearer {access_token}"
    # 解析 query 参数
    query_schema = task_record.workflow_node_tool_http_params.get("properties", {})
    query = load_properties(query_schema, global_params)
    # 解析 body 参数
    body_schema = task_record.workflow_node_tool_http_body.get("properties", {})
    data = load_properties(body_schema, global_params)
    task_record.task_params = {
        "Headers": headers,
        "Query": query,
        "Body": data
    }
    try:
        if task_record.workflow_node_tool_http_body_type == "form-data":
            res = requests.request(
                method=task_record.workflow_node_tool_http_method,
                url=task_record.workflow_node_tool_api_url,
                headers=headers,
                files=None,
                data=data,
                params=query,
                timeout=task_record.workflow_node_timeout,
                verify=task_record.workflow_node_tool_configs.get("https", {}).get("verify", True)
            )
        else:
            res = requests.request(
                method=task_record.workflow_node_tool_http_method,
                url=task_record.workflow_node_tool_api_url,
                headers=headers,
                json=data,
                params=query,
                timeout=task_record.workflow_node_timeout,
                verify=task_record.workflow_node_tool_configs.get("https", {}).get("verify", True)
            )
        task_record.task_result = res.text
        task_record.task_status = "已完成"
        task_record.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(task_record)
        db.session.commit()
        return task_record.task_result
    except Exception as e:
        task_record.task_status = "异常"
        task_record.task_trace_log = str(e)
        db.session.add(task_record)
        db.session.commit()
        return


def mcp_node_execute(headers, task_record, global_params):
    task_params = load_properties(task_record.workflow_node_tool_configs.get(
        "mcp", {}).get("call_data_schema", {}).get("properties", {}), global_params)
    task_record.task_params = {
        "Headers": headers,
        "MCP Call Params": task_params
    }
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            mcp_call(task_record.workflow_node_tool_api_url, headers, task_params)
        )
        loop.close()
        task_record.task_result = json.dumps(result)
        task_record.task_status = "已完成"
        task_record.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(task_record)
        db.session.commit()
        return task_record.task_result
    except Exception as e:
        task_record.task_status = "异常"
        task_record.task_trace_log = str(e)
        db.session.add(task_record)
        db.session.commit()


async def mcp_call(url, headers, params):
    """
    mcp 节点执行器
    :param url:
    :param headers:
    :param params:
    :return:
    """
    mcp_client = MCPClient()
    try:
        await mcp_client.connect_to_server(url, headers=headers)
        res = await mcp_client.call_tool(params.get("tool_name"), params.get("tool_params"))
    finally:
        await mcp_client.cleanup()
    return res.dict()
