from app.app import app
from flask import request
from app.services.configure_center.response_utils import next_console_response
from app.services.contacts_service.visitor_service import *


@app.route('/next_console_admin/user_center/visitor/subscribe', methods=['POST'])
def add_subscribe():
    """
    订阅公司邮件
    """
    data = request.get_json()
    email = data.get("email")
    if not email:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return add_subscribe_service(data)


@app.route('/next_console_admin/user_center/visitor/unsubscribe', methods=['POST'])
def cancel_subscribe():
    """
    取消订阅公司邮件
    """
    data = request.get_json()
    email = data.get("email")
    if not email:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return cancel_subscribe_service(data)


@app.route('/next_console_admin/user_center/visitor/valid_invite', methods=['POST'])
def valid_invite():
    """
    验证邀请id合法性
    """
    data = request.get_json()
    invite_id = data.get("invite_id")
    if not invite_id:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return valid_invite_service(data)

