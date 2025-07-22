from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.app import app
from app.services.task_center.workflow import *


@app.route('/next_console/task_center/workflow/add', methods=['GET', 'POST'])
@jwt_required()
def workflow_add():
    """
    创建工作流对象
    """
    user_id = get_jwt_identity()
    params = request.json
    params["user_id"] = user_id

    return add_workflow(params)


@app.route('/next_console/task_center/workflow/delete', methods=['GET', 'POST'])
@jwt_required()
def workflow_del():
    """
    创建工作流对象
    """
    user_id = get_jwt_identity()
    params = request.json
    params["user_id"] = user_id
    workflow_id = params.get("workflow_id")
    if not workflow_id:
        return next_console_response(error_status=True, error_message="工作流id不能为空")
    return del_workflow(params)


@app.route('/next_console/task_center/workflow/update', methods=['GET', 'POST'])
@jwt_required()
def workflow_update():
    """
    更新工作流对象
    """
    user_id = get_jwt_identity()
    params = request.json
    params["user_id"] = user_id
    workflow_id = params.get("workflow_id")
    if not workflow_id:
        return next_console_response(error_status=True, error_message="工作流id不能为空")
    return update_workflow(params)


@app.route('/next_console/task_center/workflow/search', methods=['GET', 'POST'])
@jwt_required()
def workflow_search():
    """
    创建工作流对象
    """
    user_id = get_jwt_identity()
    params = request.json
    params["user_id"] = user_id
    return search_workflow(params)


