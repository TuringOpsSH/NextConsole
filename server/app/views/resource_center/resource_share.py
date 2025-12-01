from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app import app
from app.services.resource_center.resource_share_service import *


@app.route('/next_console/resources/share_object/get_access_list', methods=['GET', 'POST'])
@jwt_required()
def resource_get_access_list():
    """
    更新共享资源访问列表
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get('resource_id')
    if not resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return get_share_resource_access_list(params)


@app.route('/next_console/resources/share_object/update_access_list', methods=['GET', 'POST'])
@jwt_required()
def resource_update_access_list():
    """
    更新共享资源访问列表
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get('resource_id')
    if not resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return update_share_resource_access_list(params)


@app.route('/next_console/resources/share_object/get_list', methods=['GET', 'POST'])
@jwt_required()
def resource_get_list():
    """
    更新共享资源访问列表
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return get_share_resource_list(params)


@app.route('/next_console/resources/share_object/get_meta', methods=['GET', 'POST'])
@jwt_required()
def resource_get_detail():
    """
    更新共享资源访问列表
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = int(params.get('resource_id'))
    if not resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return get_share_resource_meta(params)


@app.route('/next_console/resources/share_object/check_access', methods=['GET', 'POST'])
@jwt_required()
def resource_check_access():
    """
    检查用户是否有权限访问资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get('resource_id')
    target_access = params.get('access_type')
    if not resource_id or not target_access:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_user or not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在或用户不存在！")
    new_params = {
        "user": target_user,
        "resource": target_resource,
        "access_type": target_access
    }

    return next_console_response(result=check_user_manage_access_to_resource(new_params))


@app.route('/next_console/resources/share_object/search_by_keyword', methods=['GET', 'POST'])
@jwt_required()
def resource_search_by_keyword():
    """
    获取用户标签的资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_keyword = params.get("resource_keyword")
    if not resource_keyword:
        return next_console_response(error_status=True, error_message="关键字不能为空！")
    return search_share_resource_by_keyword(params)


@app.route('/next_console/resources/share_object/search_by_keyword_in_resource', methods=['GET', 'POST'])
@jwt_required()
def resource_search_by_keyword_in_resource():
    """
    指定资源路径下的关键词搜索
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_keyword = params.get("resource_keyword")
    auth_type = params.get("auth_type")
    allowed_auth_types = ['read', 'download', 'edit', 'manage']
    if not resource_keyword:
        return next_console_response(error_status=True, error_message="关键字不能为空！")
    if auth_type and auth_type not in allowed_auth_types:
        return next_console_response(error_status=True,
                                     error_message="无效的权限类型！仅支持: read, download, edit, manage")
    return search_share_resource_by_keyword_in_resource(params)


@app.route('/next_console/resources/cooling_record_detail', methods=['GET', 'POST'])
@jwt_required()
def resource_cooling_record_detail():
    """
    获取资源下载冷却记录
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    cooling_id = params.get("cooling_id")
    if not cooling_id:
        return next_console_response(error_status=True, error_message="记录id不能为空！")
    return get_resource_download_cooling_record(params)


@app.route('/next_console/resources/cooling_record_update', methods=['GET', 'POST'])
@jwt_required()
def cooling_record_update():
    """
    获取资源下载冷却记录
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    cooling_id = params.get("cooling_id")
    cooling_limit = params.get("cooling_limit")
    if not cooling_id or not cooling_limit:
        return next_console_response(error_status=True, error_message="记录id不能为空！")
    return update_resource_download_cooling_record(params)


