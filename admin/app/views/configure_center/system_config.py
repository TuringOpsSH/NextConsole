import os
from app.services.configure_center.response_utils import next_console_response
from app.app import app
import json
from flask_jwt_extended import (
    jwt_required
)
from flask import request
from app.services.configure_center.system_config_service import *
from app.services.user_center.roles import roles_required


@app.route('/next_console_admin/version', methods=['POST'])
def get_version():
    """
    获取版本号并返回
    :return:
    """
    version_path = app.config.get("public_dir")
    version_json = os.path.join(version_path, "version.json")
    try:
        with open(version_json, "r") as f:
            version = f.read()
        version = json.loads(version)
    except Exception as e:
        return next_console_response(result={"version": "0.2.7"})
    return next_console_response(result=version)


@app.route('/next_console_admin/domain', methods=['POST'])
def get_domain():
    """
    获取版本号并返回
    :return:
    """
    server_domain = app.config.get("domain", "https://www.turingops.com")
    result = {
        "server_domain": server_domain,
    }
    return next_console_response(result=result)


@app.route('/next_console_admin/config_center/system_config/get', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def get_system_configs():
    """
    获取系统配置
    :return:
    """

    return get_system_configs_service()


@app.route('/next_console_admin/config_center/system_config/update', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def update_system_config():
    """
    更新系统配置
    :return:
    """
    from flask import request
    params = request.get_json()
    from app.services.configure_center.system_config_service import update_system_config_service
    return update_system_config_service(params)


@app.route("/next_console_admin/config_center/system_config/get_wx_config", methods=["POST"])
def get_wx_config():
    data = request.get_json()
    domain = data.get("domain")
    if not domain:
        return next_console_response(error_message="参数错误！", error_code=1002)
    return get_wx_config_service(data)


@app.route('/next_console_admin/config_center/system_config/load', methods=['POST'])
def load_system_configs():
    """
    加载必要的系统配置
    :return:
    """

    return load_system_configs_service()