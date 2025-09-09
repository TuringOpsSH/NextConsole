from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import app
from app.services.assistant_center.assistant_instruction import *


@app.route('/next_console/assistant_center/assistant_instruction/add', methods=['POST'])
@jwt_required()
def assistant_instruction_add():
    """
    添加助手指令
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    assistant_id = params.get("assistant_id")
    instruction_name = params.get("instruction_name")
    if not assistant_id or not instruction_name:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)

    return add_assistant_instruction(params)


@app.route('/next_console/assistant_center/assistant_instruction/del', methods=['POST'])
@jwt_required()
def assistant_instruction_del():
    """
    删除助手指令
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    instructions = params.get("instruction_ids", [])
    if not instructions:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return del_assistant_instruction(params)


@app.route('/next_console/assistant_center/assistant_instruction/update', methods=['POST'])
@jwt_required()
def assistant_instruction_update():
    """
    更新助手指令
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    instruction_id = params.get("id")
    if not instruction_id:
        return next_console_response(error_status=True, error_message=f"参数错误！instruction_id:{instruction_id}",
                                     error_code=1002)
    return update_assistant_instruction(params)


@app.route('/next_console/assistant_center/assistant_instruction/search', methods=['POST'])
@jwt_required()
def assistant_instruction_search():
    """
    查询助手指令
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return search_assistant_instruction(params)


@app.route('/next_console/assistant_center/assistant_instruction/get', methods=['POST'])
@jwt_required()
def assistant_instruction_get():
    """
    查询助手指令详情
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    instruction_id = params.get("id")
    if not instruction_id:
        return next_console_response(error_status=True, error_message=f"参数错误！instruction_id:{instruction_id}",
                                     error_code=1002)
    return get_assistant_instruction(params)


@app.route('/next_console/assistant_center/assistant_instruction/render', methods=['POST'])
@jwt_required()
def assistant_instruction_render():
    """
    查询助手指令详情
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    instruction_id = params.get("id")
    if not instruction_id:
        return next_console_response(error_status=True, error_message=f"参数错误！instruction_id:{instruction_id}",
                                     error_code=1002)
    return render_assistant_instruction(params)


@app.route('/next_console/assistant_center/assistant_instruction/run', methods=['POST'])
@jwt_required()
def assistant_instruction_run():
    """
    查询助手指令详情
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    instruction_id = params.get("instruction_id")
    if not instruction_id or not isinstance(instruction_id, int):
        return next_console_response(error_status=True, error_message=f"参数错误！instruction_id:{instruction_id}",
                                     error_code=1002)
    msg_id = params.get("msg_id")
    if not msg_id or not isinstance(msg_id, int):
        return next_console_response(error_status=True, error_message=f"参数错误！msg_id:{msg_id}",
                                     error_code=1002)
    dry_run = params.get("dry_run", False)
    if dry_run not in (True, False):
        return next_console_response(error_status=True, error_message=f"参数错误！dry_run:{dry_run}",
                                     error_code=1002)
    return run_assistant_instruction(params)

