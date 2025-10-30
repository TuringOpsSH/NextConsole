from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask_cors import cross_origin
from app.services.app_center.app_run_service import *
from app.app import app


@app.route("/next_console/app_center/app_run/init_session", methods=["POST"])
@app.route("/next_console/app_center/app/init_session", methods=["POST"])
@jwt_required()
def get_app_session():
    """
    获取应用详情
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    data["user_id"] = user_id
    return get_app_session_service(data)


@app.route('/next_console/app_center/app_run/v2/chat/completions', methods=["GET", "POST", "OPTIONS"])
@app.route('/next_console/app_center/app_run/v2/chat/completions', methods=["GET", "POST", "OPTIONS"])
@jwt_required()
@cross_origin()  # 允许跨域访问
def app_add_message():
    # 处理请求
    if request.content_type == 'application/json':
        params = request.get_json()
    elif request.content_type.startswith('text/plain'):
        try:
            params = json.loads(request.data)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON in text/plain body"}), 400
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    # 检验参数
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)

    return agent_add_message(data)
