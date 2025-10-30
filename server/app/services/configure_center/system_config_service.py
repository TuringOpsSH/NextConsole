from app.models.configure_center.system_config import SupportArea
from app.services.configure_center.response_utils import next_console_response
from app.models.configure_center.system_config import SystemConfig
from app.app import db


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


def init_system_configs():
    """
    初始化系统配置
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
            "stt": {
                "provider": "讯飞",
                "xf_api": "wss://ws-api.xfyun.cn/v2/iat",
                "xf_api_id": "",
                "xf_api_key": "",
                "xf_api_secret": ""
            }
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
    for key in default_system_config:
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


def get_system_configs_service():
    """
    获取系统配置
    Returns
    -------

    """
    all_system_configs = SystemConfig.query.filter(
        SystemConfig.config_status == 1
    ).all()
    if not all_system_configs:
        return init_system_configs()
    system_configs = {config.config_key: config.config_value for config in all_system_configs}
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
ops
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
    if system_config.config_value.get("brand",{}).get("enable"):
        result["brand"] = system_config.config_value.get("brand",{})
    return next_console_response(result=result)
