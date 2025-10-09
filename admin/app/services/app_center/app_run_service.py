import queue
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from flask import stream_with_context, Response
from flask_jwt_extended import (
    create_access_token
)
from gevent import Timeout
from sqlalchemy.orm.attributes import flag_modified
from app.models.app_center.app_info_model import *
from app.services.app_center.expermental_features import parallel_llm_node_execute
from app.services.app_center.file_reader import file_reader_node_execute, file_splitter_node_execute
from app.services.app_center.llm_node_service import llm_node_execute
from app.services.app_center.node_params_service import *
from app.services.app_center.workflow_service import check_workflow_permission
from app.services.next_console.workflow import *
from app.services.task_center.workflow import auto_naming_session
from app.services.next_console.base import *
import requests
from app.models.configure_center.system_config import SystemConfig
from app.models.knowledge_center.rag_ref_model import *


def check_user_access(user_code, app_code):
    """
    检查用户是否有权限访问应用
    """
    target_access = AppAccessInfo.query.filter(
        AppAccessInfo.app_code == app_code,
        AppAccessInfo.access_status == "正常",
        AppAccessInfo.user_code == user_code
    ).first()
    if not target_access:
        return False
    return True


def get_app_session_service(params):
    """
    检查用户权限，通过后，
        如果session—code 不存在，创建一个session，
        如果session-code 存在，返回target session
            如果session-status 不是正常，返回错误
        补充是否结束节点请求方式
    """
    user_id = int(params.get("user_id"))
    app_code = params.get("app_code")
    session_code = params.get("session_code")
    session_test = params.get("session_test", False)
    workflow_code = params.get("workflow_code", None)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1002)
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '开发'
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if session_code:
        target_session = NextConsoleSession.query.filter(
            NextConsoleSession.session_code == session_code,
            NextConsoleSession.user_id == user_id
        ).first()
        if not target_session:
            return next_console_response(error_status=True, error_message="会话不存在！", error_code=1002)
        if target_session.session_task_id != workflow_code and workflow_code:
            target_session.session_task_id = workflow_code
        db.session.add(target_session)
        db.session.flush()
        result = target_session.to_dict()
        db.session.commit()
    else:
        if target_app.app_status != "正常" and not session_test:
            return next_console_response(error_status=True, error_message="应用状态不正确！", error_code=1002)
        if check_workflow_permission(user_id, app_code) is not True and not check_user_access(
                target_user.user_code, app_code):
            return next_console_response(error_status=True, error_message="用户无权访问！", error_code=1002)
        target_start_node = WorkFlowMetaInfo.query.filter(
            WorkFlowMetaInfo.workflow_code == workflow_code,
            WorkFlowMetaInfo.workflow_status == "正常",
            WorkFlowMetaInfo.environment == '开发'
        ).join(
            AppWorkFlowRelation,
            AppWorkFlowRelation.workflow_code == WorkFlowMetaInfo.workflow_code
        ).filter(
            AppWorkFlowRelation.app_code == target_app.app_code,
            AppWorkFlowRelation.environment == '开发',
            AppWorkFlowRelation.rel_status == '正常'
        ).join(
            WorkflowNodeInfo,
            WorkflowNodeInfo.workflow_id == WorkFlowMetaInfo.id
        ).filter(
            WorkflowNodeInfo.node_type == 'start',
            WorkflowNodeInfo.node_status == '正常'
        ).with_entities(
            WorkflowNodeInfo
        ).first()
        session_task_params_schema = {}
        if target_start_node:
            session_task_params_schema = target_start_node.node_input_params_json_schema or {}
        result = add_session({
            "user_id": user_id,
            "session_topic": f"{target_app.app_name} 会话",
            "session_status": "正常" if not session_test else "测试",
            "session_source": target_app.app_code,
            "session_task_id": workflow_code,
            "session_task_params_schema": session_task_params_schema,
        }).json.get("result")
    return next_console_response(result=result)


def save_user_question(params):
    """
    保存用户问题
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    session = params.get("session")
    message = params.get("message")
    attachments = params.get("attachments")
    if not isinstance(attachments, list):
        attachments = []
    valid_attachments = []
    for resource_id in attachments:
        try:
            valid_attachments.append(int(resource_id))
        except ValueError:
            continue
    # 新增qa
    new_qa = NextConsoleQa(
        user_id=user_id,
        session_id=session.get("id"),
        qa_topic=message,
        qa_status="正常",
    )
    db.session.add(new_qa)
    db.session.flush()
    # 新增消息
    new_message = NextConsoleMessage(
        user_id=user_id,
        session_id=session.get("id"),
        qa_id=new_qa.qa_id,
        msg_role="user",
        msg_content=message,
    )
    db.session.add(new_message)
    db.session.flush()
    result = new_message.to_dict()
    if valid_attachments:
        new_rels = SessionAttachmentRelation.query.filter(
            SessionAttachmentRelation.resource_id.in_(valid_attachments),
            SessionAttachmentRelation.rel_status == "正常"
        ).all()
        for rel in new_rels:
            rel.msg_id = new_message.msg_id
            db.session.add(rel)
            db.session.flush()
    db.session.commit()
    return next_console_response(result=result)


def agent_add_message(params):
    """
    以工作流的形式运行
        初始化会话状态，保存问题,
            应用提供的工作流：推荐问题
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    app_code = params.get("app_code")
    session_code = params.get("session_code")
    message = params.get("message")
    question_id = params.get("msg_id")
    attachments = params.get("attachments")
    is_stream = params.get("stream", True)
    task_code = params.get("task_code", None)
    workflow_params = params.get("workflow_params", {})
    current_session_result = get_app_session_service({
        "user_id": user_id,
        "app_code": app_code,
        "session_code": session_code,
    })
    current_session = current_session_result.json.get("result")
    if not current_session:
        return next_console_response(error_status=True, error_message="会话不存在！", error_code=1002)
    # 读取应用配置
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '开发'
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    # 保存问题
    if not question_id:
        question = save_user_question({
            "user_id": user_id,
            "session": current_session,
            "message": message,
            "attachments": attachments
        }).json.get("result")
    else:
        question = NextConsoleMessage.query.filter(
            NextConsoleMessage.msg_id == question_id,
            NextConsoleMessage.user_id == user_id
        ).first()
        if question:
            question = question.to_dict()
            message = question.get("msg_content")
    history_list = NextConsoleQa.query.filter(
        NextConsoleQa.session_id == current_session.get("id"),
        NextConsoleQa.qa_status == "正常",
        NextConsoleQa.user_id == user_id
    ).order_by(NextConsoleQa.create_time.desc()).all()
    if len(history_list) >= 2 and "会话" in current_session.get("session_topic"):
        auto_naming_session.delay({
            "user_id": user_id,
            "session_id": current_session.get("id"),
            "assistant_id": '-12345',
            "msg_parent_id": question.get("msg_id"),
            "question_content": message
        })
    # 解析工作流并初始化
    workflow_result = analysis_workflow_schema({
        "target_app": target_app,
        "question": question,
        "session": current_session,
        "task_code": task_code,
    })
    if workflow_result.json.get("error_status"):
        return next_console_response(error_status=True, error_message="工作流解析异常！", error_code=1002,
                                     result=workflow_result.json.get("error_message"))
    workflow_result = workflow_result.json.get("result")
    # 初始化工作流消息队列
    message_queue = queue.Queue()
    # 初始化工作流任务队列
    task_queue = queue.Queue()
    executor = ThreadPoolExecutor(max_workers=20)
    global_params = {
        "app_code": app_code,
        "session_code": session_code,
        "message_queue": message_queue,
        "task_queue": task_queue,
        "executor": executor,
        "futures": [],
        "stream": is_stream,
        "qa_id": question.get("qa_id"),
    }
    # 运行开始工作流
    future = executor.submit(agent_run_workflow, {
        "user_id": user_id,
        "session": current_session,
        "qa_id": question.get("qa_id"),
        "msg_id": question.get("msg_id"),
        "message": message,
        "workflow_id": workflow_result.get("workflow_id"),
        "global_params": global_params,
        "workflow_params": workflow_params,
    })
    future.add_done_callback(
        lambda f: print(f"🎯 Child result: {f.result()}") if f.exception() is None
        else print(f"❌ Child error: {f.exception()}")
    )
    global_params["futures"].append(future)
    # 消费消息
    if is_stream:
        return Response(
            stream_with_context(workflow_messages_stream_generate(
                message_queue, global_params
            )), mimetype="text/event-stream")
    else:
        all_messages = []
        while True:
            try:
                message = message_queue.get(timeout=1)
                # 处理消息
                if message == "stop":
                    break
                all_messages.append(message)
                message_queue.task_done()
            except Exception as e:
                print(e)
                pass
            # 检查所有线程是否完成：全部为最终状态则退出
                # 检查所有线程是否完成：全部为最终状态则退出
                all_done = True
                # print("检查所有线程是否完成：", all_done, global_params["futures"])
                for future in global_params["futures"]:
                    if not future.done():
                        all_done = False
                        break
                if all_done:
                    # 退出循环
                    end_node = global_params.get("end_node_instance")
                    end_node_instance = WorkFlowNodeInstance.query.filter(
                        WorkFlowNodeInstance.id == end_node.id
                    ).first()
                    if end_node_instance.task_status == "初始化":
                        # 异常处理结束节点
                        handle_node_failed(
                            task_record=end_node_instance,
                            global_params=global_params,
                            error='工作流异常中断，请检查中间节点的启动条件'
                        )
                    else:
                        break
        # 处理消息
        all_messages.sort(key=lambda x: x.get("msg_id") or 0)
        return {
            "id": question.get("qa_id"),
            "session_id": question.get("session_id"),
            "qa_id": question.get("qa_id"),
            "msg_parent_id": question.get("msg_id"),
            "created": question.get("create_time"),
            "model": '',
            "object": "chat.completion",
            "usage": '',
            "choices": all_messages
        }


def workflow_messages_stream_generate(message_queue, global_params):
    try:
        while True:
            try:
                message = message_queue.get(timeout=1)
                if message == "stop":
                    yield "data: [DONE]\n\n"
                    message_queue.task_done()
                    break
                yield "data: " + json.dumps(message) + "\n\n"
                message_queue.task_done()
            except Exception as e:
                print(e)
                pass
            # 检查所有线程是否完成：全部为最终状态则退出
            all_done = True
            for future in global_params["futures"]:
                if not future.done():
                    all_done = False
                    break
            if all_done:
                # 退出循环
                end_node = global_params.get("end_node_instance")
                end_node_instance = WorkFlowNodeInstance.query.filter(
                    WorkFlowNodeInstance.id == end_node.id
                ).first()
                db.session.add(end_node_instance)
                if end_node_instance.task_status == "初始化":
                    # 异常处理结束节点
                    handle_node_failed(
                        task_record=end_node_instance,
                        global_params=global_params,
                        error='工作流异常中断，请检查中间节点的启动条件'
                    )
                else:
                    yield "data: [DONE]\n\n"
                    break
    except GeneratorExit:
        # 关闭线程池
        global_params["stop_flag"] = True
        for future in global_params["futures"]:
            future.cancel()
        global_params["executor"].shutdown(wait=False)
        # 更新qa
        target_qa = NextConsoleQa.query.filter(
            NextConsoleQa.qa_id == global_params.get("qa_id"),
            NextConsoleQa.user_id == global_params.get("user_id")
        ).first()
        if target_qa:
            target_qa.qa_is_cut_off = True
            db.session.add(target_qa)
            db.session.commit()
        return


def analysis_workflow_schema(params):
    """
    解析工作流,并进行初步校验
        ## 找出开始节层级的节点
        ## 解析出每个节点的下游节点
    实例数据初始化
    :param params:
    :return:
    """
    target_app = params.get("target_app")
    question = params.get("question")
    session_task_id = params.get("session").get("session_task_id")
    task_code = params.get("task_code")
    if task_code:
        main_workflow = WorkFlowMetaInfo.query.filter(
            WorkFlowMetaInfo.workflow_code == task_code,
            WorkFlowMetaInfo.workflow_status == "正常",
            WorkFlowMetaInfo.environment == '开发'
        ).first()
    elif session_task_id:
        main_workflow = WorkFlowMetaInfo.query.filter(
            WorkFlowMetaInfo.workflow_code == session_task_id,
            WorkFlowMetaInfo.workflow_status == "正常",
            WorkFlowMetaInfo.environment == '开发'
        ).first()
    else:
        main_workflow = AppWorkFlowRelation.query.filter(
            AppWorkFlowRelation.app_code == target_app.app_code,
            AppWorkFlowRelation.environment == "开发",
            AppWorkFlowRelation.rel_status == "正常",
        ).join(
            WorkFlowMetaInfo,
            WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
        ).filter(
            WorkFlowMetaInfo.workflow_status == "正常",
            AppWorkFlowRelation.rel_status == "正常",
            WorkFlowMetaInfo.workflow_is_main == True,
            WorkFlowMetaInfo.environment == '开发'
        ).with_entities(
            WorkFlowMetaInfo
        ).first()
    if not main_workflow or not main_workflow.workflow_edit_schema:
        return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)
    workflow_schema = main_workflow.workflow_edit_schema
    cells = workflow_schema.get("cells")
    start_node = None
    end_node = None
    all_node_code = []
    for cell in cells:
        if cell.get("shape") != 'edge':
            all_node_code.append(cell.get("id"))
            if cell.get("data").get("nodeType") == "start":
                start_node = cell.get("id")
            elif cell.get("data").get("nodeType") == "end":
                end_node = cell.get("id")
    if not start_node:
        return next_console_response(error_status=True, error_message="工作流开始节点不存在！", error_code=1002)
    if not end_node:
        return next_console_response(error_status=True, error_message="工作流结束节点不存在！", error_code=1002)
    # 生成所有实例数据
    all_instance_map = {}
    for node_code in all_node_code:
        # 读取节点信息
        node_info = WorkflowNodeInfo.query.filter(
            WorkflowNodeInfo.node_code == node_code,
            WorkflowNodeInfo.environment == '开发',
            WorkflowNodeInfo.node_status == '正常',
        ).first()
        # 生成任务记录
        task_record = WorkFlowNodeInstance(
            user_id=question.get("user_id"),
            workflow_id=node_info.workflow_id,
            workflow_node_id=node_info.id,
            workflow_node_code=node_info.node_code,
            workflow_node_type=node_info.node_type,
            workflow_node_icon=node_info.node_icon,
            workflow_node_name=node_info.node_name,
            workflow_node_desc=node_info.node_desc,
            workflow_node_run_model_config=node_info.node_run_model_config,
            workflow_node_llm_code=node_info.node_llm_code,
            workflow_node_llm_params=node_info.node_llm_params,
            workflow_node_ipjs=node_info.node_input_params_json_schema,
            workflow_node_llm_spt=node_info.node_llm_system_prompt_template,
            workflow_node_llm_upt=node_info.node_llm_user_prompt_template,
            workflow_node_result_format=node_info.node_result_format,
            workflow_node_rpjs=node_info.node_result_params_json_schema,
            workflow_node_result_template=node_info.node_result_template,
            workflow_node_timeout=node_info.node_timeout,
            workflow_node_retry_max=node_info.node_retry_max,
            workflow_node_retry_duration=node_info.node_retry_duration,
            workflow_node_retry_model=node_info.node_retry_model,
            workflow_node_failed_solution=node_info.node_failed_solution,
            workflow_node_failed_template=node_info.node_failed_template,
            node_session_memory_size=node_info.node_session_memory_size,
            node_deep_memory=node_info.node_deep_memory,
            node_agent_tools=node_info.node_agent_tools,
            workflow_node_tool_api_url=node_info.node_tool_api_url,
            workflow_node_tool_http_method=node_info.node_tool_http_method,
            workflow_node_tool_http_header=node_info.node_tool_http_header,
            workflow_node_tool_http_body=node_info.node_tool_http_body,
            workflow_node_tool_http_params=node_info.node_tool_http_params,
            workflow_node_tool_http_body_type=node_info.node_tool_http_body_type,
            workflow_node_rag_resources=node_info.node_rag_resources,
            workflow_node_rag_ref_show=node_info.node_rag_ref_show,
            workflow_node_rag_query_template=node_info.node_rag_query_template,
            workflow_node_rag_recall_config=node_info.node_rag_recall_config,
            workflow_node_rag_rerank_config=node_info.node_rag_rerank_config,
            workflow_node_rag_web_search_config=node_info.node_rag_web_search_config,
            workflow_node_enable_message=node_info.node_enable_message,
            workflow_node_message_schema_type=node_info.node_message_schema_type,
            workflow_node_message_schema=node_info.node_message_schema,
            workflow_node_file_reader_config=node_info.node_file_reader_config,
            workflow_node_file_splitter_config=node_info.node_file_splitter_config,
            workflow_node_sub_workflow_config=node_info.node_sub_workflow_config,
            session_id=question.get("session_id"),
            qa_id=question.get("qa_id"),
            msg_id=question.get("msg_id"),
            task_status="初始化",
        )
        db.session.add(task_record)
        all_instance_map[node_code] = task_record
    db.session.commit()

    # 更新上下游条件
    for cell in cells:
        if cell.get("shape") != 'edge':
            continue
        source_code = cell.get("source").get("cell")
        target_code = cell.get("target").get("cell")
        data = cell.get("data")
        source_task_record = all_instance_map.get(source_code)
        target_task_record = all_instance_map.get(target_code)
        if not source_task_record or not target_task_record:
            continue
        # 更新前置条件
        edge_type = data.get("edge_type", "充分")
        edge_condition_type = data.get("edge_condition_type", "or")
        edge_conditions = data.get("edge_conditions", [])
        try:
            task_precondition = target_task_record.task_precondition
        except Exception as e:
            db.session.refresh(target_task_record)
            task_precondition = target_task_record.task_precondition or []
        task_precondition.append({
            "id": source_task_record.id,
            "type": edge_type,
            "status": '初始化'
        })
        target_task_record.task_precondition = task_precondition
        # 更新后置条件
        task_downstream = source_task_record.task_downstream
        task_downstream.append({
            "id": target_task_record.id,
            "type": edge_type,
            "condition_type": edge_condition_type,
            "conditions": edge_conditions,
            "status": '初始化'
        })
        source_task_record.task_downstream = task_downstream
        # 标记字段已修改
        flag_modified(target_task_record, "task_precondition")
        flag_modified(source_task_record, "task_downstream")
        db.session.add(source_task_record)
        db.session.add(target_task_record)
    db.session.commit()
    return next_console_response(
        result={
            "workflow_id": main_workflow.id,
        }
    )


def agent_run_workflow(params):
    """
    运行工作流
        初始化全局变量
        启动 工作流
    :param params:
    :return:
    """
    with app.app_context():
        current_session = params.get("session")
        msg_id = params.get("msg_id")
        message = params.get("message")
        workflow_id = params.get("workflow_id")
        global_params = params.get("global_params", {})
        session_task_params = params.get("workflow_params")
        # 读取开始节点
        start_node_instance = WorkFlowNodeInstance.query.filter(
            WorkFlowNodeInstance.workflow_id == workflow_id,
            WorkFlowNodeInstance.msg_id == msg_id,
            WorkFlowNodeInstance.workflow_node_type == "start",
        ).first()
        # 读取结束节点
        end_node_instance = WorkFlowNodeInstance.query.filter(
            WorkFlowNodeInstance.workflow_id == workflow_id,
            WorkFlowNodeInstance.msg_id == msg_id,
            WorkFlowNodeInstance.workflow_node_type == "end",
        ).first()
        # 设置系统全局变量
        global_params["user_id"] = params.get("user_id")
        global_params["session_id"] = current_session.get("id")
        global_params["session_topic"] = current_session.get("session_topic")
        global_params["msg_id"] = msg_id
        global_params["qa_id"] = params.get("qa_id")
        global_params["session_task_params"] = session_task_params or current_session.get("session_task_params")
        global_params["SessionId"] = current_session.get("id")
        global_params["UserInput"] = message
        global_params["end_node_instance"] = end_node_instance
        SessionAttachments = SessionAttachmentRelation.query.filter(
            SessionAttachmentRelation.session_id == current_session.get("id"),
            SessionAttachmentRelation.rel_status == "正常"
        ).join(
            ResourceObjectMeta,
            ResourceObjectMeta.id == SessionAttachmentRelation.resource_id
        ).filter(
            ResourceObjectMeta.resource_status == "正常"
        ).with_entities(
            ResourceObjectMeta, SessionAttachmentRelation.msg_id
        ).all()
        global_params["SessionAttachmentList"] = [SessionAttachment
                                                  for SessionAttachment, msg_id in SessionAttachments]
        global_params["MessageAttachmentList"] = [
            SessionAttachment for SessionAttachment, item_msg_id in SessionAttachments
            if item_msg_id == msg_id
        ]
        future = global_params["executor"].submit(agent_run_node, start_node_instance.id, global_params)
        # 添加回调确保子任务完成（可选）
        future.add_done_callback(
            lambda f: print(f"🎯agent_run_workflow:result: {f.result()}") if f.exception() is None
            else print(f"agent_run_workflow:❌error: {f.exception()}"))
        global_params["futures"].append(future)
        return


def agent_run_node(task_record_id, global_params=None):
    """
    并发完成

        1. 判断前置条件是否满足
        2. 加载本次调用的全部参数
        4. 通过不同执行器来运行工作流节点，保存异步结果
        5. 运行完成后，更新task状态
        6. 运行完成后，启动下游节点
    :param task_record_id:
    :param global_params
    :return:
    """
    with app.app_context():
        # 判断前置条件是否满足
        task_record = WorkFlowNodeInstance.query.filter(
            WorkFlowNodeInstance.id == task_record_id
        ).first()
        if not check_task_precondition(task_record):
            return
        try:
            # 加载入参
            task_params = load_task_params(task_record, global_params,
                                           isStart=task_record.workflow_node_type == "start")
            task_record.task_params = task_params
            task_record.task_status = "执行中"
            task_record.begin_time = datetime.now()
            flag_modified(task_record, "task_params")
            db.session.add(task_record)
            db.session.commit()
            # 执行节点
            with Timeout(task_record.workflow_node_timeout):
                # 路由到对应的执行器
                if task_record.workflow_node_type == "start":
                    start_node_execute(task_params, task_record, global_params)
                elif task_record.workflow_node_type == "llm":
                    if task_record.workflow_node_run_model_config.get("node_run_model") == "parallel":
                        # 并发执行
                        parallel_llm_node_execute(task_params, task_record, global_params)
                    else:
                        # 单线程执行
                        llm_node_execute(task_params, task_record, global_params)
                elif task_record.workflow_node_type == "tool":
                    tool_node_execute(task_params, task_record, global_params)
                elif task_record.workflow_node_type == "rag":
                    rag_node_execute(task_params, task_record, global_params)
                elif task_record.workflow_node_type == "end":
                    end_node_execute(task_params, task_record, global_params)
                elif task_record.workflow_node_type == "file_reader":
                    file_reader_node_execute(task_params, task_record, global_params)
                elif task_record.workflow_node_type == "file_splitter":
                    file_splitter_node_execute(task_params, task_record, global_params)
                elif task_record.workflow_node_type == "workflow":
                    workflow_node_execute(task_params, task_record, global_params)
            # 解析结果
            exec_result = load_task_result(task_record)
            task_record.task_result = json.dumps(exec_result)
            task_record.task_status = "已完成"
            task_record.end_time = datetime.now()
            db.session.add(task_record)
            db.session.commit()
            # 更新全局参数
            global_params[task_record.workflow_node_code] = exec_result
            # 消息输出
            if task_record.workflow_node_enable_message:
                transform_to_message(task_record, global_params)
            if task_record.task_status == "已完成":
                return invoke_next_task(task_record, global_params)
            else:
                handle_node_failed(task_record, global_params, "任务执行异常")
            return
        except Exception as e:
            handle_node_failed(task_record, global_params, str(e))


def invoke_next_task(task_record, global_params):
    """
    启动下游节点
        根据条件表达式，判断边是否可以通过，通过则启动下游节点，不通过则不启动
    """
    if task_record.workflow_node_type == "end":
        global_params["message_queue"].put("stop")
    # 更新下游节点的前置条件并提交任务
    node_downstream_ids = [instance.get("id") for instance in task_record.task_downstream]
    node_downstream_id_map = {instance.get("id"): instance for instance in task_record.task_downstream}
    node_downstream = WorkFlowNodeInstance.query.filter(
        WorkFlowNodeInstance.id.in_(node_downstream_ids),
        WorkFlowNodeInstance.task_status == '初始化',
    ).all()
    task_list = []
    # 逐一更新下游节点的前置条件
    for instance in node_downstream:
        new_task_precondition = instance.task_precondition
        edge_config_result = check_edge_conditions(node_downstream_id_map.get(instance.id), global_params)
        # 找到对应的前置条件并更新结果
        for new_instance in new_task_precondition:
            if int(new_instance.get("id")) == int(task_record.id):
                if edge_config_result:
                    new_instance["status"] = "已完成"
                else:
                    new_instance["status"] = "未满足"
                break
        instance.task_precondition = new_task_precondition
        flag_modified(instance, "task_precondition")
        db.session.add(instance)
        # 条件满足则启动下游节点
        if edge_config_result:
            task_list.append((agent_run_node, instance.id, global_params))
    db.session.commit()
    for sub_task in task_list:
        _func, instance, global_params = sub_task
        future = global_params["executor"].submit(_func, instance, global_params)
        future.add_done_callback(
            lambda f: print(f"🎯 result: {f.result()}")
            if f.exception() is None else None
        )
        global_params["futures"].append(future)


def start_node_execute(task_params, task_record, global_params):
    # 加载用户全局变量
    task_result = {
        "UserInput": global_params.get("UserInput"),
        "SessionId": global_params.get("SessionId"),
        "CurrentTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    MessageAttachmentList = []
    SessionAttachmentList = []
    for attachment in global_params.get("MessageAttachmentList", []):
        MessageAttachmentList.append({
            "id": attachment.id,
            "name": attachment.resource_name,
            "format": attachment.resource_format,
            "size": attachment.resource_size_in_MB,
            "icon": attachment.resource_icon,
            "content": "",
            "content_chunks": []
        })
    for attachment in global_params.get("SessionAttachmentList", []):
        SessionAttachmentList.append({
            "id": attachment.id,
            "name": attachment.resource_name,
            "format": attachment.resource_format,
            "size": attachment.resource_size_in_MB,
            "icon": attachment.resource_icon,
            "content": "",
            "content_chunks": []
        })
    task_result["MessageAttachmentList"] = MessageAttachmentList
    task_result["SessionAttachmentList"] = SessionAttachmentList
    task_result.update(task_params)
    task_record.task_result = json.dumps(task_result)
    task_record.task_status = "已完成"
    task_record.end_time = datetime.now()
    db.session.add(task_record)
    db.session.commit()


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
            )
        else:
            res = requests.request(
                method=task_record.workflow_node_tool_http_method,
                url=task_record.workflow_node_tool_api_url,
                headers=headers,
                json=data,
                params=query,
                timeout=task_record.workflow_node_timeout,
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


def rag_node_execute(params, task_record, global_params):
    """
    rag 节点执行器
        1. 组装query
        2. 获取知识ref
        3. 组装检索参数
        4. 调用api
        5. 存储检索结果
        6. 更新任务状态
    :param params:
    :param task_record:
    :param global_params:
    :return:
    """
    # 获取节点信息
    query = render_template_with_params(task_record.workflow_node_rag_query_template, params)
    if not query:
        task_record.task_status = "异常"
        task_record.task_trace_log = "检索query为空"
        db.session.add(task_record)
        db.session.commit()
        return
    # 获取知识ref
    all_resource_ids = []
    for resource in task_record.workflow_node_rag_resources:
        if resource.get("id") == "message_attachments" and global_params.get("MessageAttachmentList"):
            all_resource_ids.extend([attachment.id for attachment in global_params.get("MessageAttachmentList")])
        elif resource.get("id") == "session_attachments" and global_params.get("SessionAttachmentList"):
            all_resource_ids.extend([attachment.id for attachment in global_params.get("SessionAttachmentList")])
        else:
            all_resource_ids.append(resource.get("id"))
    all_resource_ids = list(set(all_resource_ids))
    all_ref_ids = get_all_resource_ref_ids(all_resource_ids)
    if not all_ref_ids and not task_record.workflow_node_rag_web_search_config.get("search_engine_enhanced"):
        task_record.task_status = "已完成"
        task_record.task_trace_log = "关联知识为空"
        db.session.add(task_record)
        db.session.commit()
        return
    system_tool_config = SystemConfig.query.filter(
        SystemConfig.config_key == "tools",
        SystemConfig.config_status == 1
    ).first()
    rag_params = {
        "user_id": task_record.user_id,
        "session_id": task_record.session_id,
        "msg_id": task_record.msg_id,
        "task_id": task_record.id,
        "query": query,
        "ref_ids": all_ref_ids,
        "config": {
            "recall_threshold": task_record.workflow_node_rag_recall_config.get("recall_threshold", 0.3),
            "recall_k": task_record.workflow_node_rag_recall_config.get("recall_k", 30),
            "recall_similarity": task_record.workflow_node_rag_recall_config.get("recall_similarity", "cosine"),
            "rerank_enabled": task_record.workflow_node_rag_rerank_config.get("rerank_enabled", True),
            "max_chunk_per_doc": task_record.workflow_node_rag_rerank_config.get("max_chunk_per_doc", 1024),
            "overlap_tokens": task_record.workflow_node_rag_rerank_config.get("overlap_tokens", 80),
            "rerank_threshold": task_record.workflow_node_rag_rerank_config.get("rerank_threshold", 0.3),
            "rerank_k": task_record.workflow_node_rag_rerank_config.get("rerank_k", 10),
            "search_engine_enhanced": task_record.workflow_node_rag_web_search_config.get(
                "search_engine_enhanced", False),
            "search_engine_config": {
                "api": system_tool_config.config_value.get("search_engine", {}).get("endpoint"),
                "key": system_tool_config.config_value.get("search_engine", {}).get("key"),
                "gl": "cn",
                "hl": "zh-cn",
                "location": "China",
                "num": task_record.workflow_node_rag_web_search_config.get("num", 20),
                "timeout": task_record.workflow_node_rag_web_search_config.get("timeout", 30),
            },
        }
    }
    from app.services.knowledge_center.rag_service_v3 import rag_query_v3
    rag_response = rag_query_v3(rag_params).json.get("result", {})
    details = rag_response.get("details", [])
    if not details:
        task_record.task_status = "异常"
        task_record.task_trace_log = rag_response.get("error_message", "检索结果为空")
        db.session.add(task_record)
        db.session.commit()
        return
    task_record.task_result = json.dumps(rag_response)
    task_record.task_status = "已完成"
    db.session.add(task_record)
    db.session.commit()
    return task_record.task_result


def end_node_execute(task_params, task_record, global_params):
    """
    此节点为工作流的结束节点，更新回答消息，返回服务器响应
    :param task_params:
    :param global_params:
    :param task_record:
    :return:
    """
    task_record.end_time = datetime.now()
    task_result = load_properties(task_record.workflow_node_rpjs.get("properties"), global_params)
    task_record.task_result = json.dumps(task_result)
    task_record.task_status = "已完成"
    db.session.add(task_record)
    db.session.commit()


def workflow_node_execute(task_params, task_record, global_params):
    """
    执行子workflow节点
        新建会话，因为工作流节点的入参是从会话参数中提取的？
    :param task_params:
    :param task_record:
    :param global_params:
    :return:
    """
    from app.services.configure_center.llm import NextConsoleLLMClient
    nc_client = NextConsoleLLMClient({
        "user_id": task_record.user_id,
        "is_nc": True
    })
    task_code = task_record.workflow_node_sub_workflow_config.get("target_workflow_code", "")
    main_workflow = WorkFlowMetaInfo.query.filter(
        WorkFlowMetaInfo.workflow_code == task_code,
        WorkFlowMetaInfo.workflow_status == "正常",
        WorkFlowMetaInfo.environment == '开发'
    ).first()
    if global_params.get("stream", False):
        try:
            completion = nc_client.chat({
                "messages": [
                    {
                        "role": "user",
                        "content": global_params.get("UserInput", ""),
                    }
                ],
                "stream": True,
                "extra_body": {
                    "user_id": task_record.user_id,
                    "app_code": global_params.get("app_code"),
                    "session_code": global_params.get("session_code"),
                    "is_stream": True,
                    "msg_id": task_record.msg_id,
                    "task_code": task_code,
                    "workflow_params": task_params,
                },
                "extra_headers": {
                    "Authorization": f"""Bearer {create_access_token(identity=str(task_record.user_id),
                                                           expires_delta=timedelta(days=30))}"""
                }
            })
            for chunk in completion:
                if global_params.get("stop_flag"):
                    raise GeneratorExit
                try:
                    chunk_res = chunk.model_dump_json()
                    chunk_res = json.loads(chunk_res)
                except Exception as e:
                    continue
                if global_params["stream"]:
                    global_params["message_queue"].put(chunk_res)
        except GeneratorExit:
            pass
        except Exception as e3:
            app.logger.error(f"调用基模型异常：{str(e3)}")
            error_msg = "\n\n **对不起，模型服务正忙，请稍等片刻后重试，或者可以试试切换其他模型~**"
            if task_record.workflow_node_enable_message and global_params["stream"]:
                if task_record.workflow_node_message_schema_type == "messageFlow":
                    except_result = {
                        "id": "",
                        "session_id": task_record.session_id,
                        "qa_id": task_record.qa_id,
                        "msg_parent_id": task_record.msg_id,
                        "created": 0,
                        "model": '',
                        "object": "chat.completion",
                        "choices": [
                            {
                                "finish_reason": "error",
                                "index": 0,
                                "delta": {
                                    "content": error_msg,
                                    "role": "assistant"
                                },

                            }
                        ]
                    }
                    global_params["message_queue"].put(except_result)
        finally:
            # 更新节点记录-子工作流的结束节点的结果
            result_node = WorkFlowNodeInstance.query.filter(
                WorkFlowNodeInstance.workflow_node_type == "end",
                WorkFlowNodeInstance.workflow_id == main_workflow.id,
                WorkFlowNodeInstance.msg_id == task_record.msg_id,
            ).order_by(
                WorkFlowNodeInstance.id.desc()
            ).first()
            task_record.task_result = result_node.task_result
            task_record.end_time = datetime.now()
            task_record.task_status = "已完成"
            db.session.add(task_record)
            db.session.commit()
        return True
    else:
        # 非流式执行
        try:
            nc_client.chat({
                "messages": [
                    {
                        "role": "user",
                        "content": '123',
                    }
                ],
                "stream": False,
                "extra_body": {
                    "user_id": task_record.user_id,
                    "app_code": global_params.get("app_code"),
                    "session_code": global_params.get("session_code"),
                    "is_stream": False,
                    "msg_id": task_record.msg_id,
                    "task_code": task_code,
                    "workflow_params": task_params,
                },
                "extra_headers": {
                        "Authorization": f""""Bearer {create_access_token(identity=str(task_record.user_id), 
                                                               expires_delta=timedelta(days=30))}"""""
                    }
            }).model_dump_json()
            task_record.task_status = "已完成"
        except Exception as e:
            task_record.task_status = "异常"
            app.logger.error(f"workflow_chat error: {e}")
            task_record.task_trace_log = str(e)
        result_node = WorkFlowNodeInstance.query.filter(
            WorkFlowNodeInstance.workflow_node_type == "end",
            WorkFlowNodeInstance.workflow_id == main_workflow.id,
            WorkFlowNodeInstance.msg_id == task_record.msg_id,
        ).order_by(
            WorkFlowNodeInstance.id.desc()
        ).first()
        task_record.task_result = result_node.task_result
        task_record.task_status = "已完成"
        task_record.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(task_record)
        db.session.commit()
        return True


def get_all_resource_ref_ids(all_resource_ids):
    """
    获取所有资源对应的索引列表
    :param all_resource_ids:
    :return:
    """
    res = all_resource_ids
    all_parent_id = [id for id in res]
    while all_parent_id:
        children_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.resource_status == '正常',
            ResourceObjectMeta.resource_parent_id.in_(all_parent_id),
        ).all()
        all_parent_id = []
        for resource in children_resource:
            all_parent_id.append(resource.id)
            res.append(resource.id)
    all_ref_ids = []
    file_refs = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(all_resource_ids),
        ResourceObjectMeta.resource_status == "正常"
    ).join(
        RagRefInfo,
        RagRefInfo.resource_id == ResourceObjectMeta.id,
    ).filter(
        RagRefInfo.ref_status == '成功'
    ).with_entities(
        RagRefInfo.id
    ).all()
    for ref_id in file_refs:
        all_ref_ids.append(ref_id.id)
    return all_ref_ids


def transform_to_message(task_record, global_params):
    """
    将任务结果转换为消息格式
    更新至消息表
    发送至消息队列
    :param task_record:
    :param global_params:
    :return:
    """
    for message_schema in task_record.workflow_node_message_schema:
        schema = message_schema.get("schema", {})
        schema_type = message_schema.get("schema_type")
        message_item = load_properties(schema.get("properties"), global_params)
        if schema_type == "messageFlow" and not (
                global_params['stream'] and task_record.workflow_node_llm_params.get("stream", False)):
            answer_msg = NextConsoleMessage(
                user_id=task_record.user_id,
                session_id=task_record.session_id,
                qa_id=task_record.qa_id,
                msg_parent_id=task_record.msg_id,
                task_id=task_record.id,
                msg_format=schema_type,
                msg_llm_type=task_record.workflow_node_llm_code,
                msg_role="assistant",
                msg_content=''
            )
            db.session.add(answer_msg)
            db.session.commit()
            data = {
                "reasoning_content": message_item.get("reasoning_content", ""),
                "content": message_item.get("content", ""),
                "role": "assistant"
            }
            if global_params["stream"]:
                finish_reason = "stop"
                if task_record.task_status != "已完成":
                    finish_reason = "error"
                result = {
                    "session_id": task_record.session_id,
                    "qa_id": task_record.qa_id,
                    "msg_parent_id": task_record.msg_id,
                    "msg_id": answer_msg.msg_id,
                    "id": answer_msg.msg_id,
                    "created": answer_msg.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "object": "chat.completion.chunk",
                    "model": "",
                    "choices": [
                        {
                            "finish_reason": finish_reason,
                            "index": 0,
                            "delta": data,
                        }
                    ]
                }
            else:
                result = data
            # 保存消息
            answer_msg.msg_content = message_item.get("content", "")
            answer_msg.reasoning_content = message_item.get("reasoning_content", "")
            db.session.add(answer_msg)
            db.session.commit()
            global_params["message_queue"].put(result)
        elif schema_type == "workflow":
            answer_msg = NextConsoleMessage(
                user_id=task_record.user_id,
                session_id=task_record.session_id,
                qa_id=task_record.qa_id,
                msg_parent_id=task_record.msg_id,
                task_id=task_record.id,
                msg_format=schema_type,
                msg_llm_type=task_record.workflow_node_llm_code,
                msg_role="assistant",
                msg_content=''
            )
            db.session.add(answer_msg)
            db.session.commit()
            data = {
                    "msg_format": schema_type,
                    "title": message_item.get("title", ""),
                    "description": message_item.get("description", ""),
                }
            if global_params["stream"]:
                finish_reason = "stop"
                if task_record.task_status != "已完成":
                    finish_reason = "error"
                result = {
                    "session_id": task_record.session_id,
                    "qa_id": task_record.qa_id,
                    "msg_parent_id": task_record.msg_id,
                    "msg_id": answer_msg.msg_id,
                    "id": answer_msg.msg_id,
                    "created": answer_msg.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "object": "chat.completion.chunk",
                    "model": "",
                    "choices": [
                        {
                            "finish_reason": finish_reason,
                            "index": 0,
                            "delta": data,
                        }
                    ]
                }
            else:
                result = data
            # 保存消息
            answer_msg.msg_content = json.dumps(data)
            answer_msg.msg_format = schema_type
            db.session.add(answer_msg)
            db.session.commit()
            global_params["message_queue"].put(result)
        elif schema_type == "recommendQ":
            answer_msg = NextConsoleMessage(
                user_id=task_record.user_id,
                session_id=task_record.session_id,
                qa_id=task_record.qa_id,
                msg_parent_id=task_record.msg_id,
                task_id=task_record.id,
                msg_format=schema_type,
                msg_llm_type=task_record.workflow_node_llm_code,
                msg_role="assistant",
                msg_content=''
            )
            db.session.add(answer_msg)
            db.session.commit()
            data = {
                "msg_format": schema_type,
                "questions": message_item.get("questions", [])
            }
            if global_params["stream"]:
                finish_reason = "stop"
                if task_record.task_status != "已完成":
                    finish_reason = "error"
                result = {
                    "session_id": task_record.session_id,
                    "qa_id": task_record.qa_id,
                    "msg_parent_id": task_record.msg_id,
                    "msg_id": answer_msg.msg_id,
                    "msg_format": schema_type,
                    "id": answer_msg.msg_id,
                    "created": answer_msg.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "object": "chat.completion.chunk",
                    "model": "",
                    "choices": [
                        {
                            "finish_reason": finish_reason,
                            "index": 0,
                            "delta": data,
                        }
                    ]
                }
            else:
                result = data
            # 保存消息
            answer_msg.msg_content = json.dumps(data)
            answer_msg.msg_format = schema_type
            db.session.add(answer_msg)
            db.session.commit()
            global_params["message_queue"].put(result)
        elif schema_type == "echarts":
            ...
        elif schema_type == "customize":
            answer_msg = NextConsoleMessage(
                user_id=task_record.user_id,
                session_id=task_record.session_id,
                qa_id=task_record.qa_id,
                msg_parent_id=task_record.msg_id,
                task_id=task_record.id,
                msg_format=schema_type,
                msg_llm_type=task_record.workflow_node_llm_code,
                msg_role="assistant",
                msg_content=''
            )
            db.session.add(answer_msg)
            db.session.commit()
            message_item['msg_format'] = schema_type
            if global_params["stream"]:
                finish_reason = "stop"
                if task_record.task_status != "已完成":
                    finish_reason = "error"
                result = {
                    "session_id": task_record.session_id,
                    "qa_id": task_record.qa_id,
                    "msg_parent_id": task_record.msg_id,
                    "msg_id": answer_msg.msg_id,
                    "id": answer_msg.msg_id,
                    "created": answer_msg.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "object": "chat.completion.chunk",
                    "model": "",
                    "choices": [
                        {
                            "finish_reason": finish_reason,
                            "index": 0,
                            "delta": message_item,
                        }
                    ]
                }
            else:
                result = message_item
            # 保存消息
            answer_msg.msg_content = json.dumps(message_item)
            answer_msg.msg_format = "customize"
            db.session.add(answer_msg)
            db.session.commit()
            global_params["message_queue"].put(result)
        else:
            continue


def handle_node_failed(task_record, global_params, error=''):
    """
    节点运行失败处理
    :param task_record:
    :param global_params:
    :param error:
    :return:
    """
    # 更新任务状态
    task_record.task_status = "异常"
    task_record.task_trace_log = error
    task_record.end_time = datetime.now()
    db.session.add(task_record)
    db.session.commit()
    # 根据失败解决方案处理
    retry_model = None
    if task_record.workflow_node_failed_solution == "retry":
        if task_record.task_retry_cnt < task_record.workflow_node_retry_max:
            time.sleep(task_record.workflow_node_retry_duration / 1000)
            # 重新提交任务
            new_task = WorkFlowNodeInstance(
                user_id=task_record.user_id,
                workflow_id=task_record.workflow_id,
                workflow_node_id=task_record.workflow_node_id,
                workflow_node_code=task_record.workflow_node_code,
                workflow_node_type=task_record.workflow_node_type,
                workflow_node_icon=task_record.workflow_node_icon,
                workflow_node_name=task_record.workflow_node_name,
                workflow_node_desc=task_record.workflow_node_desc,
                workflow_node_run_model_config=task_record.workflow_node_run_model_config,
                workflow_node_llm_code=task_record.workflow_node_llm_code,
                workflow_node_llm_params=task_record.workflow_node_llm_params,
                workflow_node_ipjs=task_record.workflow_node_ipjs,
                workflow_node_llm_spt=task_record.workflow_node_llm_spt,
                workflow_node_llm_upt=task_record.workflow_node_llm_upt,
                workflow_node_result_format=task_record.workflow_node_result_format,
                workflow_node_rpjs=task_record.workflow_node_rpjs,
                workflow_node_result_template=task_record.workflow_node_result_template,
                workflow_node_timeout=task_record.workflow_node_timeout,
                workflow_node_retry_max=task_record.workflow_node_retry_max,
                workflow_node_retry_duration=task_record.workflow_node_retry_duration,
                workflow_node_retry_model=task_record.workflow_node_retry_model,
                workflow_node_failed_solution=task_record.workflow_node_failed_solution,
                workflow_node_failed_template=task_record.workflow_node_failed_template,
                node_session_memory_size=task_record.node_session_memory_size,
                node_deep_memory=task_record.node_deep_memory,
                node_agent_tools=task_record.node_agent_tools,
                workflow_node_tool_api_url=task_record.workflow_node_tool_api_url,
                workflow_node_tool_http_method=task_record.workflow_node_tool_http_method,
                workflow_node_tool_http_header=task_record.workflow_node_tool_http_header,
                workflow_node_tool_http_body=task_record.workflow_node_tool_http_body,
                workflow_node_tool_http_params=task_record.workflow_node_tool_http_params,
                workflow_node_tool_http_body_type=task_record.workflow_node_tool_http_body_type,
                workflow_node_rag_resources=task_record.workflow_node_rag_resources,
                workflow_node_rag_query_template=task_record.workflow_node_rag_query_template,
                workflow_node_rag_ref_show=task_record.workflow_node_rag_ref_show,
                workflow_node_rag_recall_config=task_record.workflow_node_rag_recall_config,
                workflow_node_rag_rerank_config=task_record.workflow_node_rag_rerank_config,
                workflow_node_rag_web_search_config=task_record.workflow_node_rag_web_search_config,
                workflow_node_enable_message=task_record.workflow_node_enable_message,
                workflow_node_message_schema_type=task_record.workflow_node_message_schema_type,
                workflow_node_message_schema=task_record.workflow_node_message_schema,
                session_id=task_record.session_id,
                qa_id=task_record.qa_id,
                msg_id=task_record.msg_id,
                task_status="初始化",
                task_precondition=task_record.task_precondition,
                task_downstream=task_record.task_downstream,
                task_retry_cnt=task_record.task_retry_cnt + 1,
            )
            db.session.add(new_task)
            db.session.flush()
            new_task_id = new_task.id
            db.session.commit()
            # 替换全局参数中的任务实例
            if task_record.workflow_node_code in global_params:
                del global_params[task_record.workflow_node_code]
            # 启动新任务
            future = global_params["executor"].submit(agent_run_node, new_task_id, global_params)
            future.add_done_callback(
                lambda f: print(f"🎯 result: {f.result()}")
                if f.exception() is None else None
            )
            global_params["futures"].append(future)
            return

        retry_model = task_record.workflow_node_retry_model
    # 异常捕捉模式
    if task_record.workflow_node_failed_solution == 'catch' or retry_model == 2:
        catch_result = render_template_with_params(task_record.workflow_node_failed_template, task_record.task_params)
        task_record.task_result = catch_result
        db.session.add(task_record)
        db.session.commit()
        # 解析结果
        exec_result = load_task_result(task_record)
        task_record.end_time = datetime.now()
        if not exec_result:
            task_record.task_status = "异常"
            db.session.add(task_record)
            db.session.commit()
            return
        task_record.task_result = json.dumps(exec_result)
        task_record.task_status = "已完成"
        db.session.add(task_record)
        db.session.commit()
        global_params[task_record.workflow_node_code] = exec_result
        # 处理消息
        if task_record.workflow_node_enable_message:
            transform_to_message(task_record, global_params)
        return invoke_next_task(task_record, global_params)
    # 跳过模式
    if task_record.workflow_node_failed_solution == 'pass' or retry_model == 3:
        task_record.task_status = "已跳过"
        task_record.end_time = datetime.now()
        db.session.add(task_record)
        db.session.commit()
        global_params[task_record.workflow_node_code] = {}
        return invoke_next_task(task_record, global_params)
    # 直接退出模式
    end_node = global_params["end_node_instance"]
    end_node = WorkFlowNodeInstance.query.filter(
        WorkFlowNodeInstance.id == end_node.id
    ).first()
    if end_node:
        end_node.task_status = "异常"
        end_node.task_result = json.dumps({
            "error": error,
            "message": "任务执行异常，请检查日志"
        })
        end_node.end_time = datetime.now()
        db.session.add(end_node)
        db.session.commit()
    for future in global_params["futures"]:
        future.cancel()
    global_params["futures"] = [future for future in global_params["futures"] if future.done()]
    return


def search_app_workflow_debug_info(data):
    """
    根据qa_id 获取工作流调试信息
    """
    user_id = int(data.get("user_id"))
    qa_list = data.get("qa_list", [])
    session_id = data.get("session_id", None)
    from app.services.next_console.base import search_qa
    target_qas = search_qa({
        "user_id": user_id,
        "qa_id": qa_list
    }).json.get("result", [])
    if target_qas:
        target_instances = WorkFlowNodeInstance.query.filter(
            WorkFlowNodeInstance.qa_id.in_(qa_list)
        ).all()
    else:
        max_qa_id = WorkFlowNodeInstance.query.filter(
            WorkFlowNodeInstance.user_id == user_id,
            WorkFlowNodeInstance.session_id == session_id
        ).with_entities(
            func.max(WorkFlowNodeInstance.qa_id)
        ).scalar()
        target_instances = WorkFlowNodeInstance.query.filter(
            WorkFlowNodeInstance.qa_id == max_qa_id
        ).all()
    result = []
    for instance in target_instances:
        duration = (instance.end_time - instance.begin_time).total_seconds() if instance.begin_time and instance.end_time else None,
        instance_data = {
            "id": instance.id,
            "workflow_id": instance.workflow_id,
            "workflow_node_id": instance.workflow_node_id,
            "workflow_node_name": instance.workflow_node_name,
            "workflow_node_type": instance.workflow_node_type,
            "workflow_node_icon": instance.workflow_node_icon,
            "workflow_node_desc": instance.workflow_node_desc,
            "session_id": instance.session_id,
            "qa_id": instance.qa_id,
            "user_id": instance.user_id,
            "msg_id": instance.msg_id,
            "task_params": instance.task_params,
            "task_prompt": instance.task_prompt,
            "task_result": instance.task_result[:1000],
            "task_status": instance.task_status,
            "task_retry_cnt": instance.task_retry_cnt,
            "begin_time": instance.begin_time.strftime('%Y-%m-%d %H:%M:%S') if instance.begin_time else None,
            "end_time": instance.end_time.strftime('%Y-%m-%d %H:%M:%S') if instance.end_time else None,
            "task_token_used": instance.task_token_used,
            "create_time": instance.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": instance.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "duration": duration,
            "task_trace_log": instance.task_trace_log,
        }
        result.append(instance_data)
    return next_console_response(result=result)


def get_app_workflow_debug_full_info(data):
    """
    # 新增管理员查看权限
    :param data:
    :return:
    """
    user_id = int(data.get("user_id"))
    workflow_instance_id = data.get("workflow_instance_id")
    target_instance = WorkFlowNodeInstance.query.filter(
        WorkFlowNodeInstance.id == workflow_instance_id
    ).first()
    if not target_instance:
        return next_console_response(error_status=True, error_message="工作流实例不存在", error_code=1002)
    if not (
            check_has_role(user_id, "next_console_admin")
            or check_has_role(user_id, "super_admin")
            or check_has_role(user_id, "admin")
    ) and target_instance.user_id != user_id:
        return next_console_response(error_status=True, error_message="没有权限查看该工作流实例", error_code=1003)
    if target_instance.begin_time and target_instance.end_time:
        duration = (target_instance.end_time - target_instance.begin_time).total_seconds()
    else:
        duration = None
    return next_console_response(result={
        "id": target_instance.id,
        "workflow_id": target_instance.workflow_id,
        "workflow_node_id": target_instance.workflow_node_id,
        "workflow_node_name": target_instance.workflow_node_name,
        "workflow_node_type": target_instance.workflow_node_type,
        "workflow_node_icon": target_instance.workflow_node_icon,
        "workflow_node_desc": target_instance.workflow_node_desc,
        "session_id": target_instance.session_id,
        "qa_id": target_instance.qa_id,
        "user_id": target_instance.user_id,
        "msg_id": target_instance.msg_id,
        "task_params": target_instance.task_params,
        "task_prompt": target_instance.task_prompt,
        "task_result": target_instance.task_result,
        "task_status": target_instance.task_status,
        "task_retry_cnt": target_instance.task_retry_cnt,
        "begin_time": target_instance.begin_time.strftime('%Y-%m-%d %H:%M:%S') if target_instance.begin_time else None,
        "end_time": target_instance.end_time.strftime('%Y-%m-%d %H:%M:%S') if target_instance.end_time else None,
        "task_token_used": target_instance.task_token_used,
        "create_time": target_instance.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        "update_time": target_instance.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        "duration": duration,
        "task_trace_log": target_instance.task_trace_log,
    })


def check_has_role(user_id, role_name):
    """
    检查用户是否有指定角色
    :param user_id:
    :param role_name:
    :return:
    """
    from app.models.user_center.role_info import RoleInfo
    from app.models.user_center.user_role_info import UserRoleInfo
    user_roles = UserRoleInfo.query.filter(UserRoleInfo.user_id == user_id).all()
    all_role_ids = [role.role_id for role in user_roles]
    all_roles = RoleInfo.query.filter(RoleInfo.role_id.in_(all_role_ids)).all()
    user_roles = [role.role_name for role in all_roles]
    if role_name in user_roles:
        return True
    return False
