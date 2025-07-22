from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app import app
from app.services.configure_center.response_utils import next_console_response
from app.services.resource_center.resource_shortcut_service import *


@app.route('/next_console/resources/shortcut/add', methods=['GET', 'POST'])
@jwt_required()
def resource_shortcut_add():
    """
        新增资源快捷方式
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return add_resource_shortcut(params)


@app.route('/next_console/resources/shortcut/search', methods=['GET', 'POST'])
@jwt_required()
def resource_shortcut_search():
    """
        获取资源快捷方式
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_resource_shortcut(params)


@app.route('/next_console/resources/shortcut/delete', methods=['GET', 'POST'])
@jwt_required()
def resource_shortcut_delete():
    """
        删除资源快捷方式
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return delete_resource_shortcut(params)


