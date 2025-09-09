from app.app import app
from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from .edith_service import *


@app.route("/next_console/edith_web/edith_client/meta_create", methods=["POST"])
@jwt_required()
def create_client_meta_info():
    """
    通过表单创建客户端版本信息，包括上传客户端图标和客户端文件
    """
    user_id = get_jwt_identity()
    data = request.form.to_dict()
    data["user_id"] = user_id
    client_icon = request.files.get("client_icon")
    client_binary = request.files.get("client_binary")
    return create_client_meta_info_service(data, client_icon, client_binary)


@app.route("/next_console/edith_web/edith_client/meta", methods=["POST"])
def get_client_meta_info():
    """
    获取客户端版本信息
    """
    return get_client_meta_info_service()


@app.route("/next_console/edith_web/edith_task/create", methods=["POST"])
@jwt_required()
def create_edith_task():
    """
    创建巡检任务
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    task_name = data.get("task_name")
    task_type = data.get("task_type")
    if not task_name or not task_type:
        return next_console_response(error_status=True, error_message="任务名称或任务类型不能为空")
    return create_edith_task_service(data)


@app.route("/next_console/edith_web/edith_task/search", methods=["POST"])
@jwt_required()
def search_edith_task():
    """
    获取巡检任务列表
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return search_edith_task_service(data)


@app.route("/next_console/edith_web/edith_task/update", methods=["POST"])
@jwt_required()
def update_edith_task():
    """
    更新巡检任务信息
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return update_edith_task_service(data)


@app.route("/next_console/edith_web/edith_task/upload_data", methods=["POST"])
@jwt_required()
def upload_edith_task():
    """
    上传巡检数据, 暂时只支持上传zip文件
    """
    user_id = get_jwt_identity()
    data = request.form.to_dict()
    if not data:
        data = request.get_json()
    data["user_id"] = user_id
    task_code = data.get("task_code")
    task_data = request.files.getlist("task_data")
    task_data_resources = data.get("task_data_resources")
    task_data_url = data.get("task_data_url")
    if not task_code:
        return next_console_response(error_status=True, error_message="任务编号不能为空")
    if not task_data and not task_data_url and not task_data_resources:
        return next_console_response(error_status=True, error_message="上传数据不能为空")
    return upload_edith_task_data(data, task_data)


@app.route("/next_console/edith_web/edith_task/delete_data", methods=["POST"])
@jwt_required()
def delete_edith_task():
    """
    上传巡检数据, 暂时只支持上传zip文件
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    task_code = data.get("task_code")
    task_data_name = data.get("task_data_name")
    if not task_code:
        return next_console_response(error_status=True, error_message="任务编号不能为空")
    if not task_data_name:
        return next_console_response(error_status=True, error_message="目标数据不能为空")
    return delete_edith_task_data(data)


@app.route("/next_console/edith_web/edith_task/start_generate_report", methods=["POST"])
@jwt_required()
def start_edith_task_generate_report():
    """
    生成巡检报告
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    task_code = data.get("task_code")
    report_type = data.get("report_type", 'single')
    if not task_code:
        return next_console_response(error_status=True, error_message="任务编号不能为空")
    if not report_type:
        return next_console_response(error_status=True, error_message="报告类型不能为空")
    if report_type not in ('single', 'full', 'cluster', 'all'):
        return next_console_response(error_status=True, error_message="报告类型错误")
    return start_generate_report_service(data)
