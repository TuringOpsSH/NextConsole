from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.app import app
from app.services.next_console.workflow import *


@app.route('/next_console/recommend_question/update', methods=['GET', 'POST'])
@jwt_required()
def recommend_question_update():
    """
    接受推荐问题的点击更新
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    recommend_question_id = params.get("recommend_question_id")
    if not recommend_question_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    return update_recommend_question(params)

