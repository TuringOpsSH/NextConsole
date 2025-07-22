import re

from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import jwt, app
from app.services.user_center.system_notice_service import *


@app.route("/next_console_admin/get_system_notices", methods=["GET", "POST"])
@jwt_required()
def get_system_notices():
    """
    获取系统通知
    :return:
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params["user_id"] = user_id
    return get_system_notice_service(params)


@app.route("/next_console_admin/add_system_notices", methods=["GET", "POST"])
@jwt_required()
def add_system_notices():
    """
    获取系统通知
    :return:
    """
    # user_id = get_jwt_identity()
    params = request.get_json()
    # params["user_id"] = user_id
    return add_system_notice_service(params)


@app.route("/next_console_admin/set_system_notices_read", methods=["GET", "POST"])
@jwt_required()
def set_system_notices_read():
    """
    获取系统通知
    :return:
    """
    user_id = get_jwt_identity()
    params = request.get_json()
    params["user_id"] = user_id
    return set_system_notices_read_service(params)



