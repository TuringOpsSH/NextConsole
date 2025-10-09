from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import app
from app.services.contacts_service.colleague_service import *


@app.route('/next_console_admin/contacts/get_colleague_list', methods=['POST'])
@jwt_required()
def get_colleague():
    """
    获取同事列表
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params['user_id'] = user_id
    department_id = params.get('department_id')
    is_root = params.get('is_root', False)

    if not department_id and not is_root:
        return next_console_response(error_status=True, error_message='部门id不能为空')
    return get_colleague_list(params)


@app.route('/next_console_admin/contacts/search_colleague', methods=['POST'])
@jwt_required()
def search_department_colleague():
    """
    搜索获取同事列表
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params['user_id'] = user_id
    keyword = params.get('keyword')
    if not keyword:
        return next_console_response(error_status=True, error_message='关键词不能为空')
    return search_colleague_service(params)

