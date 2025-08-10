import os
from app.services.configure_center.response_utils import next_console_response
from app.app import app
import json


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
        return next_console_response(result={"version": "0.2.4"})
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
