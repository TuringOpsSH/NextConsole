import json

from app.app import db, app
from app.models.configure_center.user_config import UserConfig
from app.services.configure_center.response_utils import next_console_response


def init_user_config(user_id):
    """
    初始化用户配置
    """
    resource_shortcut_types = [
        {
            "icon": 'images/recent.svg',
            "title": '最近',
            "type": 'recent',
            "show": True
        },
        {
            "icon": 'images/support_search.svg',
            "title": '索引',
            "type": 'rag',
            "show": True
        },
        {
            "icon": 'images/document.svg',
            "title": '文档',
            "type": 'document',
            "show": True
        },
        {
            "icon": 'images/image.svg',
            "title": '图片',
            "type": 'image',
            "show": False
        },
        {
            "icon": 'images/video.svg',
            "title": '视频',
            "type": 'video',
            "show": False
        },
        {
            "icon": 'images/audio.svg',
            "title": '音频',
            "type": 'audio',
            "show": False
        },
        {
            "icon": 'images/code.svg',
            "title": '代码',
            "type": 'code',
            "show": True
        },
        {
            "icon": 'images/folder.svg',
            "title": '文件夹',
            "type": 'folder',
            "show": True
        },
        {
            "icon": 'images/webpage.svg',
            "title": '网页',
            "type": 'webpage',
            "show": True
        },
        {
            "icon": 'images/archive.svg',
            "title": '压缩包',
            "type": 'archive',
            "show": True
        },
        {
            "icon": 'images/binary.svg',
            "title": '程序',
            "type": 'binary',
            "show": True
        },
        {
            "icon": 'images/other.svg',
            "title": '其他',
            "type": 'other',
            "show": True
        }
    ]
    user_config = UserConfig(
        user_id=user_id,
        open_query_agent=0,
        config_status='正常',
        resource_shortcut_types=resource_shortcut_types

    )
    db.session.add(user_config)
    db.session.commit()
    return next_console_response(result=user_config.to_dict())


def get_user_config(user_id):
    """
    获取用户配置
    """
    user_config = UserConfig.query.filter_by(
        user_id=user_id).first()
    if user_config:
        if user_config.config_status != '正常':
            return next_console_response(error_status=True, error_message="用户配置异常")
        return next_console_response(result=user_config.to_dict())
    else:
        return init_user_config(user_id)


def update_user_config(params):
    """
    更新用户配置
    """
    user_id = int(params.get("user_id"))
    open_query_agent = params.get("open_query_agent")
    resource_shortcut_types = params.get("resource_shortcut_types")
    search_engine_language_type = params.get("search_engine_language_type")
    search_engine_resource_type = params.get("search_engine_resource_type")
    target_config = UserConfig.query.filter_by(
        user_id=user_id
    ).first()
    if not target_config:
        return next_console_response(error_status=True, error_message="用户配置不存在")
    if (open_query_agent is not None and isinstance(open_query_agent, int)
            and target_config.open_query_agent != open_query_agent):
        target_config.open_query_agent = open_query_agent
    if resource_shortcut_types is not None and isinstance(resource_shortcut_types, list):
        target_config.resource_shortcut_types = resource_shortcut_types
    if search_engine_language_type is not None:
        try:
            search_engine_language_type = json.loads(search_engine_language_type)
        except Exception as e:
            app.logger.error("搜索引擎语言类型转换失败:{}".format(e.args))
            return next_console_response(error_status=True, error_message="搜索引擎语言类型转换失败")
        target_config.search_engine_language_type = search_engine_language_type
    if search_engine_resource_type is not None and search_engine_resource_type in ("news", "search", "scholar"):
        target_config.search_engine_resource_type = search_engine_resource_type
    db.session.add(target_config)
    try:
        db.session.commit()
        # 根据配置情况更新rag_model
        return next_console_response(result=target_config.to_dict())
    except Exception as e:
        app.logger.error("更新用户配置失败:{}".format(e.args))
        db.session.rollback()
        return next_console_response(error_status=True, error_message="更新用户配置失败")
