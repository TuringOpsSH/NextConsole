from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import app
from app.services.contacts_service.company_service import *


@app.route('/next_console/contacts/get_company_info', methods=['POST'])
@jwt_required()
def get_company():
    """
    获取公司信息
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params['user_id'] = user_id
    return get_company_info(params)


