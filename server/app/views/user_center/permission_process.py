from flask import request
from flask_jwt_extended import (
    jwt_required
)

from app.app import app
from app.services.user_center.permissions import *


@app.route('/next_console/user_center/permission/add', methods=['POST'])
@jwt_required()
def permission_add():
    """
    新增权限
    :return:
    """
    # 获取入参
    params = request.get_json()
    return add_permission(params)


@app.route('/next_console/user_center/permission/search', methods=['POST'])
@jwt_required()
def permission_search():
    params = request.get_json()
    return search_permissions(params)


@app.route('/next_console/user_center/permission/delete', methods=['POST'])
@jwt_required()
def permission_delete():
    params = request.get_json()
    return delete_permissions(params)


@app.route('/next_console/user_center/permission/update', methods=['POST'])
@jwt_required()
def permission_update():
    params = request.get_json()
    return update_permission(params)


@app.route('/next_console/user_center/permission/get', methods=['POST'])
@jwt_required()
def permission_get():
    params = request.get_json()
    return get_permission_detail(params)


