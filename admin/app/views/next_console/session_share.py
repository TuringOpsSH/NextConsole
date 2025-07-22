from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.services.next_console.share import *
from app.services.next_console.workflow import *


@app.route('/next_console_admin/session_share/create', methods=['GET', 'POST'])
@jwt_required()
def session_share_create():
    """
    创建会话分享
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    session_id = params.get("session_id")
    if not session_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id,
        NextConsoleSession.user_id == user_id
    ).first()
    if not target_session:
        return next_console_response(error_status=True, error_message="会话不存在！")
    return create_session_share(params)


@app.route('/next_console_admin/session_share/get', methods=['GET', 'POST'])
def session_share_get():
    """
    获取分享会话
    """
    params = request.get_json()
    share_token = params.get("share_token")
    if not share_token:
        return next_console_response(error_status=True, error_message="参数异常！")
    return get_session_share(params)


@app.route('/next_console_admin/session_share/get_qa', methods=['GET', 'POST'])
def session_share_get_qa():
    """
    获取分享会话
    """
    params = request.get_json()
    share_token = params.get("share_token")
    if not share_token:
        return next_console_response(error_status=True, error_message="参数异常！")
    return get_session_share_qa(params)


@app.route('/next_console_admin/session_share/get_message', methods=['GET', 'POST'])
def session_share_get_message():
    """
    获取分享会话
    """
    params = request.get_json()
    share_token = params.get("share_token")
    if not share_token:
        return next_console_response(error_status=True, error_message="参数异常！")
    return get_session_share_message(params)


@app.route('/next_console_admin/session_share/get_reference', methods=['GET', 'POST'])
def session_share_get_reference():
    """
    获取分享会话
    """
    params = request.get_json()
    share_token = params.get("share_token")
    if not share_token:
        return next_console_response(error_status=True, error_message="参数异常！")
    return get_session_share_reference(params)

