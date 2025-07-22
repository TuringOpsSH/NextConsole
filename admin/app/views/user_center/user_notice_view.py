from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.app import app
from app.services.user_center.roles import roles_required
from app.services.configure_center.response_utils import next_console_response
from app.services.user_center.user_notice_service import *


@app.route('/next_console_admin/user_center/user_notice_service/list', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_list():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return list_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/search', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_search():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return search_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/add', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_add():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return add_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/del', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_del():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    task_id = data.get("task_id")
    if not task_id:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return del_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/init', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_init():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return init_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/detail', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_detail():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("task_id"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return get_task_detail_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/update', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_update():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("task_id"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return update_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/start', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_start():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("task_id"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return start_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/pause', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_pause():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("task_id"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return pause_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/resume', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_resume():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("task_id"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return resume_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/stop', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_stop():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("task_id"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return stop_task_info(data)


@app.route('/next_console_admin/user_center/user_notice_service/search_notice_company', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def search_notice_company():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("keyword"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return search_company(data)


@app.route('/next_console_admin/user_center/user_notice_service/search_notice_department', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def search_notice_department():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("keyword"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return search_department(data)


@app.route('/next_console_admin/user_center/user_notice_service/search_notice_user', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def search_notice_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("keyword"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return search_user(data)


@app.route('/next_console_admin/user_center/user_notice_service/list_instance', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_instance_list():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("task_id"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return list_task_instances(data)


@app.route('/next_console_admin/user_center/user_notice_service/retry_instances', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def notice_task_instance_retry():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    if not data.get("task_instances"):
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return retry_task_instances(data)

