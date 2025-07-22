from flask import request
from app.services.configure_center.model_manager import *
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.services.user_center.roles import roles_required


@app.route('/next_console_admin/config_center/llm_instance/search', methods=['POST'])
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


@app.route('/next_console_admin/config_center/llm_instance/add', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def models_add():
    """
    搜索助手
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return model_instance_add(params)


@app.route('/next_console_admin/config_center/llm_instance/del', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def models_del():
    """
    搜索助手
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return model_instance_delete(params)


@app.route('/next_console_admin/config_center/llm_instance/get', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def models_get():
    """
    搜索助手
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return model_instance_get(params)


@app.route('/next_console_admin/config_center/llm_instance/update', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def models_update():
    """
    搜索助手
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return model_instance_update(params)


@app.route('/next_console_admin/config_center/llm_instance/icon/upload', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def models_icon_upload():
    """
    搜索助手
    """
    user_id = get_jwt_identity()
    llm_icon_data = request.files.get('llm_icon')
    if not llm_icon_data:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return model_icon_upload_service(user_id, llm_icon_data)

