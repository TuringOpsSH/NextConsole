from flask import request

from app.services.configure_center.model_manager import *
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)


@app.route('/next_console/config_center/llm_instance/search', methods=['POST'])
@jwt_required(optional=True)
def models_search():
    """
    搜索助手
    """
    params = request.json
    try:
        user_id = int(get_jwt_identity() or 0)
    except Exception as e:
        user_id = 0
    params["user_id"] = int(user_id)
    return model_instance_search(params)


# @app.route('/next_console/config_center/llm_instance/add', methods=['POST'])
# @jwt_required()
# def models_add():
#     """
#     搜索助手
#     """
#     params = request.json
#     user_id = get_jwt_identity()
#     params["user_id"] = int(user_id)
#     return model_instance_add(params)
#
#
# @app.route('/next_console/config_center/llm_instance/del', methods=['POST'])
# @jwt_required()
# def models_del():
#     """
#     搜索助手
#     """
#     params = request.json
#     user_id = get_jwt_identity()
#     params["user_id"] = int(user_id)
#     return model_instance_delete(params)


@app.route('/next_console/config_center/llm_instance/get', methods=['POST'])
@jwt_required()
def models_get():
    """
    搜索助手
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return model_instance_get(params)


# @app.route('/next_console/config_center/llm_instance/update', methods=['POST'])
# @jwt_required()
# def models_update():
#     """
#     搜索助手
#     """
#     params = request.json
#     user_id = get_jwt_identity()
#     params["user_id"] = int(user_id)
#     return model_instance_update(params)



