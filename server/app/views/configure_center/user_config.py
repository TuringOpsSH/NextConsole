from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask import request
from app.services.configure_center.user_config import *


@app.route('/next_console/config_center/user_config/get', methods=['GET', 'POST'])
@jwt_required()
def user_config_get():
    """
    获取用户配置
    :return:
    """

    user_id = get_jwt_identity()

    return get_user_config(user_id)


@app.route('/next_console/config_center/user_config/update', methods=['GET', 'POST'])
@jwt_required()
def user_config_update():
    """
    更新用户配置
    :return:
    """

    params = request.get_json()
    if not params:
        return next_console_response(error_status=True, error_message="参数为空", error_code=1002)
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return update_user_config(params)

