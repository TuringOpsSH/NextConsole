import os
from app.services.configure_center.response_utils import next_console_response
from app.app import app
import json


@app.route('/next_console/version', methods=['POST'])
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
        return next_console_response(result={"version": "2.1.0"})
    return next_console_response(result=version)


@app.route('/next_console/reinit_user_resource_path', methods=['POST'])
def reinit_user():
    """
    重新初始化用户
    :return:
    """
    from app.app import db
    from app.models.user_center.user_info import UserInfo
    from app.models.resource_center.resource_model import ResourceObjectMeta
    target_reinit_user = UserInfo.query.filter(
        UserInfo.user_status == 1,
        UserInfo.user_resource_base_path.is_(None)
    ).all()
    init_cnt = 0
    for user in target_reinit_user:
        # 初始化用户资源地址
        user.user_resource_base_path = os.path.join(app.config["UPLOAD_FOLDER"], 'user_resources', str(user.user_code))
        if not os.path.exists(user.user_resource_base_path):
            os.makedirs(user.user_resource_base_path, exist_ok=True)
        db.session.add(user)
        db.session.commit()
        # 初始化用户资源库
        user_resource = ResourceObjectMeta(
            user_id=user.user_id,
            resource_name="我的资源",
            resource_type="folder",
            resource_desc="用户资源库",
            resource_status="正常",
            resource_path=user.user_resource_base_path,
            resource_icon="folder.svg",
        )
        db.session.add(user_resource)
        db.session.commit()
        init_cnt += 1
    return next_console_response(result={"init_cnt": init_cnt})