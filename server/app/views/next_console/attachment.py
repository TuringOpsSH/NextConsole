"""
会话级附件管理
"""
from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.app import app
from app.services.next_console.attachment import *


@app.route('/next_console/attachment/base_init', methods=['GET', 'POST'])
@jwt_required()
def attachment_base_init():
    """
    初始化会话文件夹
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not params.get("session_id"):
        return next_console_response(error_status=True, error_message="参数异常！")
    return init_attachment_base(params)


@app.route('/next_console/attachment/add_into_session', methods=['GET', 'POST'])
@jwt_required()
def attachment_add_into_session():
    """
    添加附件到会话
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not params.get("session_id") or not params.get("resource_id") or not params.get("attachment_source"):
        return next_console_response(error_status=True, error_message="参数异常！")
    return add_attachment_into_session(params)


@app.route('/next_console/attachment/remove_from_session', methods=['GET', 'POST'])
@jwt_required()
def attachment_delete_from_session():
    """
    从会话中删除附件
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not params.get("session_id"):
        return next_console_response(error_status=True, error_message="参数异常！")
    return remove_from_session(params)


@app.route('/next_console/attachment/search_in_session', methods=['GET', 'POST'])
@jwt_required()
def attachment_search_in_session():
    """
    从会话中搜索附件
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not params.get("session_id") or params.get('attachment_sources') is None:
        return next_console_response(error_status=True, error_message="参数异常！")
    return search_in_session(params)


@app.route('/next_console/attachment/get_detail', methods=['GET', 'POST'])
@jwt_required()
def attachment_get_attachment_detail():
    """
    获取附件详情
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not params.get("session_id") or not params.get("attachment_source"):
        return next_console_response(error_status=True, error_message="参数异常！")
    return get_attachment_detail(params)


@app.route('/next_console/attachment/add_webpage_tasks', methods=['GET', 'POST'])
@jwt_required()
def attachment_add_webpage_tasks():
    """
    添加网页任务
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not params.get("session_id") or not params.get("urls"):
        return next_console_response(error_status=True, error_message="参数异常！")
    return add_webpage_tasks(params)


@app.route('/next_console/attachment/search_resources', methods=['GET', 'POST'])
@jwt_required()
def attachment_search_resources():
    """
    添加网页任务
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_resources(params)


@app.route('/next_console/attachment/search_resources_by_rag', methods=['GET', 'POST'])
@jwt_required()
def attachment_search_resources_by_rag():
    """
    添加网页任务
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_keyword = params.get("resource_keyword")
    if not resource_keyword:
        return next_console_response(error_status=True, error_message="参数异常！")
    return search_resources_by_rag(params)


@app.route('/next_console/attachment/search_share_resources', methods=['GET', 'POST'])
@jwt_required()
def attachment_search_share_resources():
    """
    添加网页任务
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_keyword = params.get("resource_keyword")
    if not resource_keyword:
        return next_console_response(error_status=True, error_message="参数异常！")
    return search_share_resources(params)


@app.route('/next_console/attachment/add_resources_into_session', methods=['GET', 'POST'])
@jwt_required()
def attachment_add_resources_into_session():
    """
    添加资源到会话
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not params.get("session_id") or not params.get("resource_list"):
        return next_console_response(error_status=True, error_message="参数异常！")
    return add_resources_into_session(params)


@app.route('/next_console/attachment/get_all_resource_formats', methods=['GET', 'POST'])
@jwt_required()
def attachment_get_all_resource_formats():
    """
    获取所有资源格式
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return get_all_resource_formats(params)


