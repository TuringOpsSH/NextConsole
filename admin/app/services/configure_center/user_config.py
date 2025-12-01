import json

from app.app import db, app
from app.models.configure_center.user_config import UserConfig
from app.services.configure_center.response_utils import next_console_response


def init_user_config(user_id):
    """
    初始化用户配置
    """
    default_config = {
        "workbench": {
            "model_list": [],
            "message_layout": "",
            "search_engine_language": "en",
            "search_engine_resource": "search",
            "session_resources_list": [
              {
                "resource_id": -1,
                "resource_icon": 'all_resource.svg',
                "resource_name": '全部资源'
              }
            ]
        },
        "contact": {
            "allow_search": True,
        },
        "system": {
            "theme": "light",
            "language": "中文",
        }
    }
    for key in default_config:
        new_sub_config = UserConfig(
            user_id=user_id,
            config_key=key,
            config_value=default_config[key],
            config_status='正常'
        )
        db.session.add(new_sub_config)
    db.session.commit()
    return next_console_response(result=default_config)


def get_user_config(user_id):
    """
    获取用户配置
    """
    user_config = UserConfig.query.filter_by(
        user_id=user_id,
        config_status='正常'
    ).all()
    if user_config:
        user_config = {config.config_key: config.config_value for config in user_config}
        return next_console_response(result=user_config)
    else:
        return init_user_config(user_id)


def update_user_config(params):
    """
    更新用户配置
    """
    user_id = int(params.get("user_id"))
    config_key = params.get("config_key")
    config_value = params.get("config_value")
    target_config = UserConfig.query.filter_by(
        user_id=user_id,
        config_key=config_key,
        config_status='正常'
    ).first()
    if not target_config:
        return next_console_response(error_status=True, error_message="用户配置不存在")
    target_config.config_value = config_value
    db.session.add(target_config)
    try:
        db.session.commit()
        # 根据配置情况更新rag_model
        return next_console_response(result=target_config.to_dict())
    except Exception as e:
        app.logger.error("更新用户配置失败:{}".format(e.args))
        db.session.rollback()
        return next_console_response(error_status=True, error_message="更新用户配置失败")
