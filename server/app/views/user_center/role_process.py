from flask import request
from flask_jwt_extended import (
    jwt_required
)

from app.app import app
from app.services.user_center.roles import *


@app.route('/next_console/user_center/role/add', methods=['POST'])
@jwt_required()
def role_add():
    """
    新增角色
    :return:
    """
    # 获取入参
    params = request.get_json()
    return add_role(params)


@app.route('/next_console/user_center/role/search', methods=['POST'])
@jwt_required()
def role_search():
    params = request.get_json()
    return search_roles(params)


@app.route('/next_console/user_center/role/delete', methods=['POST'])
@jwt_required()
def role_delete():
    params = request.get_json()
    return delete_roles(params)


@app.route('/next_console/user_center/role/update', methods=['POST'])
@jwt_required()
def role_update():
    params = request.get_json()
    return update_role(params)


@app.route('/next_console/user_center/role/get', methods=['POST'])
@jwt_required()
def role_get():
    params = request.get_json()
    return get_role_detail(params)

