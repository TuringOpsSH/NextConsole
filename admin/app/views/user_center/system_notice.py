import re
from app.models.user_center.user_info import UserInfo

from app.services.configure_center.response_utils import next_console_response
from app.models.user_center.user_role_info import *
from app.models.user_center.role_info import *
from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import jwt, app
from app.services.user_center.system_notice_service import *


@app.route("/next_console_admin/get_system_notices", methods=["GET", "POST"])
@jwt_required()
def get_system_notices():
    """
    获取系统通知
    :return:
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params["user_id"] = user_id
    return get_system_notice_service(params)


@app.route("/next_console_admin/add_system_notices_by_admin", methods=["GET", "POST"])
def add_system_notices():
    """
    获取系统通知
    :return:
    """
    params = request.get_json()
    admin_id = params.get("admin_id")
    if not admin_id:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    admin_user = UserInfo.query.filter(
        UserInfo.user_id == admin_id,
        UserInfo.user_status == 1
    ).join(
        UserRoleInfo, UserInfo.user_id == UserRoleInfo.user_id
    ).join(
        RoleInfo, UserRoleInfo.role_id == RoleInfo.role_id
    ).filter(
        RoleInfo.role_name == "next_console_admin"
    ).first()
    if not admin_user:
        return next_console_response(error_status=True, error_message="管理员不存在！", error_code=1002)
    return add_system_notice_service(params)


@app.route("/next_console_admin/set_system_notices_read", methods=["GET", "POST"])
@jwt_required()
def set_system_notices_read():
    """
    获取系统通知
    :return:
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params["user_id"] = user_id
    return set_system_notices_read_service(params)



