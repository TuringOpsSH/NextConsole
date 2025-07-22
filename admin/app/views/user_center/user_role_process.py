from flask import request
from flask_jwt_extended import (
    jwt_required,
)

from app.app import app
from app.services.user_center.permissions import permission_required
from app.services.user_center.user_role import *


@app.route('/next_console_admin/user_center/user_roles/add', methods=['POST'])
# @permission_required("/next_console_admin/user_center/user_roles/add")
@jwt_required()
def user_role_add():
    """
    新增用户角色
    :return:
    """
    # 获取入参
    params = request.get_json()
    res = add_user_role(params)
    return res


@app.route('/next_console_admin/user_center/user_roles/search', methods=['POST'])
@jwt_required()
def user_roles_search():
    params = request.get_json()
    return search_user_roles(params)


@app.route('/next_console_admin/user_center/user_roles/delete', methods=['POST'])
@jwt_required()
def user_roles_delete():
    params = request.get_json()
    return delete_user_roles(params)

