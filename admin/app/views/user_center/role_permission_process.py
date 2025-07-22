from flask import request
from flask_jwt_extended import (
    jwt_required,
)

from app.app import app
from app.services.user_center.permissions import permission_required
from app.services.user_center.role_permission import *


@app.route('/next_console_admin/user_center/role_permissions/add', methods=['POST'])
# @permission_required("/next_console_admin/user_center/role_permissions/add")
@jwt_required()
def role_permission_add():
    """
    新增角色权限
    :return:
    """
    # 获取入参
    params = request.get_json()
    res = add_role_permission(params)
    return res


@app.route('/next_console_admin/user_center/role_permissions/search', methods=['POST'])
@jwt_required()
def role_permissions_search():
    params = request.get_json()
    return search_role_permissions(params)


@app.route('/next_console_admin/user_center/role_permissions/delete', methods=['POST'])
@jwt_required()
def role_permissions_delete():
    params = request.get_json()
    return delete_role_permissions(params)



