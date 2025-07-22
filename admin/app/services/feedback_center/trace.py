from app.services.configure_center.response_utils import next_console_response
from app.models.next_console.next_console_model import *
from app.app import app
import requests
from app.models.app_center.app_info_model import WorkFlowTaskInfo


def rag_trace(params):
    """
    获取msg的 rag追溯

    :param params:
    :return:
    """
    msg_id = params.get("msg_id")
    if not msg_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    target_msg = NextConsoleMessage.query.filter_by(msg_id=msg_id).first()
    if not target_msg:
        return next_console_response(error_status=True, error_message="msg_id不存在！")

    trace_id = f"{target_msg.user_id}:{target_msg.session_id}:{target_msg.msg_id}"
    trace_ids = [
                    f"{target_msg.user_id}:{target_msg.session_id}:{target_msg.msg_id}_{i}"
                    for i in range(10)
                ]
    trace_ids.append(trace_id)
    rag_endpoint = app.config["RAG_ENDPOINT"]
    url = f"{rag_endpoint}/fetch_struct_log"
    data = {
        "trace_ids": trace_ids,
        "index": "trace_id"
    }
    try:
        res = requests.post(url, json=data).json()

        return next_console_response(result=res)
    except Exception as e:

        return next_console_response(error_status=True, error_message="获取rag追溯失败！")


def query_agent_trace(params):
    """
    获取msg的 query_agent追溯
    """
    msg_id = params.get("msg_id")
    if not msg_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    target_msg = NextConsoleMessage.query.filter_by(msg_id=msg_id).first()
    if not target_msg:
        return next_console_response(error_status=True, error_message="msg_id不存在！")

    query_agent_workflow = WorkFlowTaskInfo.query.filter(
        WorkFlowTaskInfo.msg_id == target_msg.msg_id
    ).order_by(WorkFlowTaskInfo.id).all()

    result = [sub_task.to_dict() for sub_task in query_agent_workflow]
    return next_console_response(result=result)

