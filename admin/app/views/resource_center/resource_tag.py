from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import app
from app.services.resource_center.resource_tag_service import *


@app.route('/next_console_admin/resources/tag/add', methods=['GET', 'POST'])
@jwt_required()
def resource_tag_add():
    """
    资源标签添加
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    tag_name = params.get("tag_name")
    if not tag_name:
        return next_console_response(error_status=True, error_code=1001, error_message="标签名称不能为空")
    return add_resource_tag(params)


@app.route('/next_console_admin/resources/tag/delete', methods=['GET', 'POST'])
@jwt_required()
def resource_tag_delete():
    """
    资源标签删除
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    tag_list = params.get("tag_list")
    if not tag_list:
        return next_console_response(error_status=True, error_code=1001, error_message="标签不能为空")
    return delete_resource_tag(params)


@app.route('/next_console_admin/resources/tag/get', methods=['GET', 'POST'])
@jwt_required()
def resource_tag_get():
    """
    资源标签获取
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    tag_id = params.get("tag_id")
    if not tag_id:
        return next_console_response(error_status=True, error_code=1001, error_message="标签不能为空")
    return get_resource_tag(params)


@app.route('/next_console_admin/resources/tag/search', methods=['GET', 'POST'])
@jwt_required()
def resource_tag_search():
    """
    资源标签搜索
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_resource_tag(params)


@app.route('/next_console_admin/resources/tag/update', methods=['GET', 'POST'])
@jwt_required()
def resource_tag_update():
    """
    资源标签更新
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    tag_id = params.get("tag_id")
    if not tag_id:
        return next_console_response(error_status=True, error_code=1001, error_message="标签不能为空")
    return update_resource_tag(params)


@app.route('/next_console_admin/resources/tag/add_resources', methods=['GET', 'POST'])
@jwt_required()
def resource_tag_add_resources():
    """
    资源标签新增资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    tag_id = params.get("tag_id")
    resource_list = params.get("resource_list")
    if not tag_id or not resource_list:
        return next_console_response(error_status=True, error_code=1001, error_message="标签不能为空")
    return add_resource_tag_for_resource(params)


@app.route('/next_console_admin/resources/tag/remove_resources', methods=['GET', 'POST'])
@jwt_required()
def resource_tag_remove_resources():
    """
    资源标签移除资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    tag_id = params.get("tag_id")
    if not tag_id:
        return next_console_response(error_status=True, error_code=1001, error_message="标签不能为空")
    return remove_resource_tag_for_resource(params)


@app.route('/next_console_admin/resources/tag/list_resources', methods=['GET', 'POST'])
@jwt_required()
def resource_tag_list_resources():
    """
    资源标签移除资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    tag_id = params.get("tag_id")
    if not tag_id:
        return next_console_response(error_status=True, error_code=1001, error_message="标签不能为空")
    return list_resource_tag_for_resource(params)
