from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.app import app
from app.services.next_console.workflow import *


@app.route('/next_console/reference/search', methods=['GET', 'POST'])
@jwt_required()
def reference_search():
    """
    新增会话
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    msg_id_list = params.get("msg_id_list")
    if msg_id_list is None:
        return next_console_response(error_status=True, error_message="参数异常！")
    return search_reference(params)

