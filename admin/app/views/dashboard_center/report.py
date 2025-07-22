from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import app
from app.services.user_center.users import *
import datetime
from app.services.user_center.roles import roles_required
from app.models.user_center.user_info import UserInfo
from app.models.user_center.user_role_info import UserRoleInfo
from app.models.user_center.role_info import RoleInfo


@app.route('/dashboard/report', methods=['POST'])
@roles_required(["admin", "super_admin", "app", "next_console_reader_admin"])
@jwt_required()
def report_get():
    report_name = request.json.get('report_name')
    begin_time = request.json.get('begin_time')
    end_time = request.json.get('end_time')
    company = request.json.get('company')
    user_id = get_jwt_identity()
    if report_name not in ('user_activity', '1', '2'):
        return next_console_response(error_status=True, error_message="参数错误！")
    if company:
        target_roles = UserRoleInfo.query.filter(
            UserRoleInfo.user_id == user_id,
            UserRoleInfo.rel_status == 1
        ).all()
        target_role_ids = [role.role_id for role in target_roles]
        target_roles = RoleInfo.query.filter(
            RoleInfo.role_id.in_(target_role_ids)
        ).all()
        target_roles = [role.role_name for role in target_roles]
        if "app" not in target_roles and "next_console_reader_admin" not in target_roles:
            return next_console_response(error_status=True, error_message="权限不足！")
    else:
        target_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
        company = target_user.user_company
        if not company:
            return next_console_response(error_status=True, error_message="公司信息为空！")
    if begin_time is None:
        try:
            begin_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return next_console_response(error_status=True, error_message="时间格式错误！")
    if end_time is None:
        try:
            end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return next_console_response(error_status=True, error_message="时间格式错误！")

    else:
        return next_console_response(error_status=True, error_message="暂不支持此类指标！")
