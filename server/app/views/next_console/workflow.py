from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.app import app
from app.services.next_console.workflow import *


@app.route('/next_console/workflow/get_progress_batch', methods=['GET', 'POST'])
@jwt_required()
def workflow_get_progress_batch():
    """
    批量获取获取工作流进度

    """
    params = request.get_json()
    qa_ids = params.get("qa_ids")
    if not qa_ids:
        return next_console_response(error_message="参数异常！", result={})
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return get_workflow_progress_batch(params)

