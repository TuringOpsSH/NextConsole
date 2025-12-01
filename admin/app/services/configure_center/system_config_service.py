from app.models.configure_center.system_config import SupportArea
from app.services.configure_center.response_utils import next_console_response
from app.models.configure_center.system_config import SystemConfig
from app.app import db, app


def get_support_area_data():
    """
    获取支持区域数据，并组装成前端需要的数据格式
    data.continent
        data.region
            data.name+(data.iso_code_3)
                data.area
    [
        {
            value: 'guide',  +
            label: 'Guide',
            children: []
        },
    ]
    """
    support_area = SupportArea.query.filter(
        SupportArea.area_status == "正常"
    ).order_by(
        SupportArea.continent,
        SupportArea.country,
        SupportArea.province,
        SupportArea.city
    ).all()
    support_area_list = []
    continent_index_dict = {}
    country_index_dict = {}
    province_index_dict = {}
    for data in support_area:
        if data.continent not in continent_index_dict:
            continent_index_dict[data.continent] = len(support_area_list)
            support_area_list.append({
                "value": data.continent,
                "label": data.continent,
                "children": []
            })
        continent_index = continent_index_dict[data.continent]
        if data.country not in country_index_dict:
            country_index_dict[data.country] = len(support_area_list[continent_index]["children"])
            support_area_list[continent_index]["children"].append({
                "value": data.country,
                "label": data.country,
                "children": []
            })
        country_index = country_index_dict[data.country]
        if data.province not in province_index_dict:
            province_index_dict[data.province] = len(support_area_list[continent_index]["children"][country_index]["children"])
            support_area_list[continent_index]["children"][country_index]["children"].append({
                "value": data.province,
                "label": f"{data.province}",
                "children": []
            })
        province_index = province_index_dict[data.province]
        support_area_list[continent_index]["children"][country_index]["children"][province_index]["children"].append({
            "value": data.city,
            "label": data.city
        })
    return next_console_response(result=support_area_list)


def init_system_configs(config_key=None):
    """
    初始化系统配置
        在第一次使用系统时，初始化系统配置
        后续可以根据key重置具体配置
    Returns
    -------

    """
    default_system_config = {
        'ai': {
            "xiaoyi": {
                "llm_code": "",
                "name": "小亦助手",
                "avatar_url": "/images/logo.svg"
            },
            "stt": {
                "provider": "讯飞",
                "xf_api": "wss://ws-api.xfyun.cn/v2/iat",
                "xf_api_id": "",
                "xf_api_key": "",
                "xf_api_secret": ""
            }
        },
        'resources': {
            'auto_rag': True,
            'viewer': {

            },
            'download': {
              "max_count": 100,
              "cool_time": 7200,
            },
            'parser': {
                'pdf': {
                    'engine': 'pymupdf',
                    'options': [],
                    'config': {

                    }
                },
                'pptx': {
                    'engine': 'pymupdf',
                    'engine_options': [],
                },
                'xlsx': {
                    'engine': 'openpyxl',
                    'options': [],
                    'config': {}
                },
                'xls': {
                    'engine': 'openpyxl',
                    'options': [],
                    'config': {}
                },
                'html': {
                    'engine': 'html2text',
                    'engine_options': [],
                    'config': {}
                },
                'shtml': {
                    'engine': 'html2text',
                    'engine_options': [],
                    'config': {}
                },
                'phtml': {
                    'engine': 'html2text',
                    'engine_options': [],
                    'config': {}
                },
                'htm': {
                    'engine': 'html2text',
                    'engine_options': [],
                    'config': {}
                },
                'others': {
                    'engine': 'text',
                    'engine_options': [],
                    'config': {}
                }
            },
            'splitter': {

            },
            'abstractor': {

            },
            "embedding": {
                "llm_code": "",
                "enable": False,
                "threshold": 0.5,
                "topK": 10
            },
            "rerank": {
                "enable": False,
                "llm_code": "",
                "threshold": 0.2,
                "topK": 10
            },
        },
        'connectors': {
            "qywx": [{
                'domain': '',
                "sToken": "",
                "sEncodingAESKey": "",
                "sCorpID": "",
                "corpsecret": "",
                "agent_id": ""
            }],
            "weixin": [
                {
                    'domain': '',
                    "wx_app_id": "",
                    "wx_app_secret": ""
                }
            ]
        },
        'tools': {
            "search_engine": {
                "endpoint": "",
                "key": "",
            },
            "sms": {
                "provider": "阿里云",
                "key_id": "",
                "key_secret": "",
                "endpoint": "dysmsapi.aliyuncs.com",
                "sign_name": "",
                "template_code": ""
            },
            "email": {
                "smtp_server": "",
                "smtp_ssl": False,
                "smtp_port": 465,
                "smtp_user": "",
                "smtp_password": "",
            },
            "wps": {
                "enabled": False,
                "app_id": "",
            }
        },
        "ops": {
            "brand": {
                "enable": False,
                "logo_url": "",
                "logo_full_url": "",
                "brand_name": "NextConsole",
            }
        },
    }
    pandoc_input_formats = [
        "biblatex", "bibtex", "bits",
        "commonmark", "commonmark_x", "creole", "csljson", "csv",
        "djot", "docbook", "docx", "dokuwiki",
        "endnotexml", "epub",
        "fb2",
        "gfm",
        "haddock", "html",
        "ipynb",
        "jats", "jira",
        "latex",
        "man", "markdown", "markdown_github", "markdown_mmd", "markdown_phpextra", "markdown_strict", "mdoc",
        "mediawiki", "muse",
        "native",
        "odt", "opml", "org",
        "pod",
        "ris", "rst", "rtf",
        "t2t", "textile", "tikiwiki", "tsv", "twiki", "typst",
        "vimwiki",
    ]
    for resource_format in pandoc_input_formats:
        if resource_format not in default_system_config["resources"]["parser"]:
            default_system_config["resources"]["parser"][resource_format] = {
                'engine': 'pandoc',
                'options': ['pandoc'],
                'config': {
                    "to_format": "markdown",
                    "preserve-tabs": True,
                    "wrap": "none",
                    "mathml": True,
                },
            }
    if config_key:
        target_config = SystemConfig.query.filter(
            SystemConfig.config_key == config_key,
            SystemConfig.config_status == 1
        ).first()
        if config_key not in default_system_config:
            return next_console_response(error_status=True, error_message="无法初始化该系统配置")
        if not target_config:
            target_config = SystemConfig(
                config_key=config_key,
                config_desc=f"{config_key}配置",
                config_default_value=default_system_config[config_key],
                config_value=default_system_config[config_key],
                config_status=1
            )
            db.session.add(target_config)
            db.session.commit()
        else:
            target_config.config_value = default_system_config[config_key]
            db.session.add(target_config)
            db.session.commit()
        return next_console_response(result={
            config_key: default_system_config[config_key],
        })

    exist_system_configs = SystemConfig.query.filter(
        SystemConfig.config_status == 1
    ).with_entities(
        SystemConfig.config_key
    ).all()
    exist_keys = [config.config_key for config in exist_system_configs]

    for key in default_system_config:
        if key in exist_keys:
            continue
        new_config = SystemConfig(
            config_key=key,
            config_desc=f"{key}配置",
            config_default_value=default_system_config[key],
            config_value=default_system_config[key],
            config_status=1
        )
        db.session.add(new_config)
    db.session.commit()
    return next_console_response(result=default_system_config)


def get_system_configs_service(data):
    """
    获取系统配置
    Returns
    -------

    """
    config_key = data.get("config_key")
    all_system_configs = SystemConfig.query.filter(
        SystemConfig.config_status == 1
    ).all()
    if not all_system_configs:
        return init_system_configs()
    system_configs = {config.config_key: config.config_value for config in all_system_configs}
    ops_server_config = {
        "domain": app.config.get("domain"),
        "admin_domain": app.config.get("admin_domain"),
        "base_dir": str(app.config.get("base_dir")),
        "bucket_size": app.config.get("bucket_size"),
        "data_dir": str(app.config.get("data_dir")),
        "download_dir": str(app.config.get("download_dir")),
        "jwt_access_token_expires": str(app.config.get("JWT_ACCESS_TOKEN_EXPIRES")),
        "timezone": app.config.get("timezone"),
        "log_dir": str(app.config.get("LOG_DIR")),
        "log_file": app.config.get("LOG_FILE"),
        "log_level": app.config.get("LOG_LEVEL"),
        "log_max_size": app.config.get("LOG_MAX_BYTES"),
        "log_backup_count": app.config.get("LOG_BACKUP_COUNT"),
        "db_type": app.config.get("db_type"),
        "db_user": app.config.get("db_user"),
        "db_host": app.config.get("db_host"),
        "db_port": app.config.get("db_port"),
        "redis_host": app.config.get("redis_host"),
        "redis_port": app.config.get("redis_port"),
        "redis_username": app.config.get("redis_username"),
        "next_console_channel": app.config.get("next_console_channel"),
        "websocket_channel": app.config.get("websocket_channel"),
        "celery_broker_channel": app.config.get("celery_broker_channel"),
        "celery_result_channel": app.config.get("celery_result_channel"),
        "worker_concurrency": app.config.get("worker_concurrency"),
        "task_timeout": app.config.get("task_timeout"),
    }
    system_configs["ops"]["server"] = ops_server_config
    if config_key:
        if config_key not in system_configs:
            return next_console_response(error_status=True, error_message="系统配置不存在")
        return next_console_response(result={config_key: system_configs[config_key]})
    return next_console_response(result=system_configs)


def update_system_config_service(params):
    """
    更新系统配置
    Returns
    -------

    """
    config_key = params.get("config_key")
    config_value = params.get("config_value")
    target_config = SystemConfig.query.filter(
        SystemConfig.config_key == config_key,
        SystemConfig.config_status == 1
    ).first()
    if not target_config:
        return next_console_response(error_status=True, error_message="系统配置不存在")
    target_config.config_value = config_value
    db.session.add(target_config)
    try:
        db.session.commit()
        # 小亦默认模型
        if config_key == 'ai':
            from app.models.assistant_center.assistant import Assistant
            xiaoyi_assistant = Assistant.query.filter_by(
                id=-12345
            ).first()
            if xiaoyi_assistant:
                xiaoyi_assistant.assistant_model_code = config_value.get("xiaoyi", {}).get("llm_code", "")
                db.session.add(xiaoyi_assistant)
                db.session.commit()
        return next_console_response(result=target_config.to_dict())
    except Exception as e:
        print(e)
        db.session.rollback()
        return next_console_response(error_status=True, error_message="更新系统配置失败")


def get_wx_config_service(data):
    """
    获取微信配置
        appid
        redirect_uri
    """
    domain = data.get("domain", "")
    from app.models.configure_center.system_config import SystemConfig
    system_connectors_config = SystemConfig.query.filter(
        SystemConfig.config_key == "connectors",
        SystemConfig.config_status == 1
    ).first()
    if not system_connectors_config:
        return next_console_response(error_message="未配置微信登录！", error_code=1001)
    config = None
    for wx in system_connectors_config.config_value.get("weixin"):
        if wx.get("domain") == domain:
            config = wx
            break
    if not config:
        return next_console_response(error_message="未配置微信登录！", error_code=1002)

    return next_console_response(result={
        "domain": domain,
        "wx_app_id": config.get("wx_app_id")
    })


def load_system_configs_service():
    """
    加载必要的系统配置
    Returns
    -------
    """
    system_config = SystemConfig.query.filter(
        SystemConfig.config_status == 1,
        SystemConfig.config_key == "ops"
    ).first()
    if not system_config:
        return next_console_response()
    result = {}
    # brand
    if system_config.config_value.get("brand", {}).get("enable"):
        result["brand"] = system_config.config_value.get("brand", {})
    return next_console_response(result=result)

