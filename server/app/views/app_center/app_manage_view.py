from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.services.app_center.app_manage_service import *
from app.services.app_center.app_manage.app_manage_service import *


@app.route('/next_console/app_center/app_manage/search', methods=['POST'])
@jwt_required()
def search_ai_apps():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return search_all_apps(data)


@app.route('/next_console/app_center/app_manage/detail',  methods=['POST'])
@jwt_required()
def detail_ai_app():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return get_app_detail(data)


@app.route("/next_console/app_center/app/detail", methods=["POST"])
@jwt_required()
def get_app_detail():
    """
    获取应用详情
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    data["user_id"] = user_id
    return get_app_detail_service(data)


# @app.route("/next_console/app_center/app/init_session", methods=["POST"])
# @jwt_required()
# def get_app_session():
#     """
#     获取应用详情
#     """
#     user_id = get_jwt_identity()
#     data = request.get_json()
#     app_code = data.get("app_code")
#     if not app_code:
#         return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
#     data["user_id"] = user_id
#     return get_app_session_service(data)