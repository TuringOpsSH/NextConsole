from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app import app
from app.services.resource_center.resource_recycle_objcet_service import *


@app.route('/next_console_admin/resources/recycle_object/search_in_recycle_bin', methods=['GET', 'POST'])
@jwt_required()
def resource_search_in_recycle_bin():
    """
    获取用户删除的资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_in_recycle_bin(params)


@app.route('/next_console_admin/resources/recycle_object/delete', methods=['GET', 'POST'])
@jwt_required()
def resource_recycle_object_delete():
    """
    删除回收站 资源目录列表
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_list = params.get("resource_list")
    clean_all = params.get("clean_all")
    if not resource_list and not clean_all:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return delete_resource_recycle_object(params)


@app.route('/next_console_admin/resources/recycle_object/recover', methods=['GET', 'POST'])
@jwt_required()
def resource_recycle_object_recover():
    """
    删除回收站 资源目录列表
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_list = params.get("resource_list")
    if not resource_list:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return recover_resource_recycle_object(params)


@app.route('/next_console_admin/resources/recycle_object/get', methods=['GET', 'POST'])
@jwt_required()
def resource_recycle_object_get():
    """
    获取回收站资源对象
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return get_resource_recycle_object(params)

