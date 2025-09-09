from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import app
from app.services.contacts_service.department_service import *


@app.route('/next_console/contacts/get_department_list', methods=['POST'])
@jwt_required()
def get_department_list():
    """
    获取部门列表
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params['user_id'] = user_id
    return get_department_list_info(params)


@app.route('/next_console/contacts/get_department_info', methods=['POST'])
@jwt_required()
def get_department_info():
    """
    获取部门信息
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params['user_id'] = user_id
    department_id = params.get('department_id')
    if not department_id:
        return next_console_response(error_status=True, error_message='部门id不能为空')
    return get_department_detail(params)


@app.route('/next_console/contacts/search_department_info', methods=['POST'])
@jwt_required()
def search_department_info():
    """
    获取部门信息
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params['user_id'] = user_id
    keyword = params.get('keyword')
    if not keyword:
        return next_console_response(error_status=True, error_message='关键词不能为空')
    return search_department_detail(params)


