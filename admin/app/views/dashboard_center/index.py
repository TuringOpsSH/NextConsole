
from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import app
from app.services.dashboard_center.index_service import *
from app.services.user_center.users import *
import datetime
from app.services.user_center.roles import roles_required
from app.models.user_center.user_role_info import UserRoleInfo
from app.models.user_center.role_info import RoleInfo


@app.route('/next_console_admin/dashboard/index', methods=['GET'])
@roles_required(["admin", "super_admin", "next_console_admin", "next_console_reader_admin"])
@jwt_required()
def index_get():
    """
    获取用户使用详情
        只有天问管理员可以查看全部公司的数据
        管理员和超级管理员可以查看自己公司的数据
    """
    user_id = get_jwt_identity()
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    index_name = request.args.get('index_name')
    if not index_name:
        return next_console_response(error_status=True, error_message="参数错误！")
    begin_time = request.args.get('begin_time')
    end_time = request.args.get('end_time')
    top = request.args.get('top')

    # 支持公司筛选
    company_id = request.args.get('company_id')
    target_roles = UserRoleInfo.query.filter(
        UserRoleInfo.user_id == user_id,
        UserRoleInfo.rel_status == 1
    ).all()
    target_role_ids = [role.role_id for role in target_roles]
    target_roles = RoleInfo.query.filter(
        RoleInfo.role_id.in_(target_role_ids)
    ).all()
    target_roles = [role.role_name for role in target_roles]
    if company_id:
        if "next_console_admin" not in target_roles and "next_console_reader_admin" not in target_roles:
            return next_console_response(error_status=True, error_message="权限不足！")
    else:
        if "next_console_admin" in target_roles or "next_console_reader_admin" in target_roles:
            company_id = "all"
        else:
            company_id = target_user.user_company_id
    if not top:
        top = 10
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

    if index_name == "uv":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_uv(new_params)
    elif index_name == "qa":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_qa(new_params)
    elif index_name == "session":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_session(new_params)
    elif index_name == "uv_hour":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_uv_hour(new_params)
    elif index_name == "qa_hour":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_qa_hour(new_params)
    elif index_name == "session_hour":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_session_hour(new_params)
    elif index_name == "uv_day":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_uv_day(new_params)
    elif index_name == "qa_day":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_qa_day(new_params)
    elif index_name == "session_day":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_session_day(new_params)
    elif index_name == "uv_accum_day":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_uv_accum_day(new_params)
    elif index_name == "qa_accum_day":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_qa_accum_day(new_params)
    elif index_name == "session_accum_day":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_session_accum_day(new_params)
    elif index_name == "doc_download_count":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_doc_download_count(new_params)
    elif index_name == "doc_download_top":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "top": top,
            "company_id": company_id
        }
        return get_doc_download_top(new_params)
    elif index_name == "user_download_top":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "top": top,
            "company_id": company_id
        }
        return get_user_download_top(new_params)
    elif index_name == "dnu":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_dnu(new_params)
    elif index_name == "dnu_sd":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_dnu_sd(new_params)
    elif index_name == "all_cvr":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_all_cvr(new_params)
    elif index_name == "new_cvr":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_new_cvr(new_params)
    elif index_name == "d1_retention":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_d1_retention(new_params)
    elif index_name == "all_retention":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_all_retention(new_params)
    elif index_name == "avg_qa_retention":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_avg_qa_retention(new_params)
    elif index_name == "avg_session_retention":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_avg_session_retention(new_params)
    elif index_name == "doc_read_count":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_doc_read_count(new_params)
    elif index_name == "doc_view_top":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "company_id": company_id
        }
        return get_doc_view_top(new_params)
    elif index_name == "user_view_resource_top":
        new_params = {
            "user_id": user_id,
            "begin_time": begin_time,
            "end_time": end_time,
            "top": top,
            "company_id": company_id
        }
        return get_user_view_resource_top(new_params)

    return next_console_response(error_status=True, error_message="暂不支持此类指标！")


