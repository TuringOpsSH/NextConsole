from app.app import app
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask import request
from app.services.feedback_center.trace import *
from app.services.configure_center.response_utils import next_console_response
from app.services.user_center.roles import roles_required


@app.route('/feedback_center/trace/rag/get', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def get_rag_trace():
    """
    获取rag追溯
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    msg_id = params.get("msg_id")
    if not msg_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    return rag_trace(params)


@app.route('/feedback_center/trace/workflow/get', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def get_workflow_query_agent_trace():
    """
    获取query_agent追溯
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    msg_id = params.get("msg_id")
    if not msg_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    return query_agent_trace(params)