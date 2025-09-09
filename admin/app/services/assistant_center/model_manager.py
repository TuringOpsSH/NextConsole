from app.app import app, db
import uuid
from sqlalchemy import or_
from app.models.configure_center.llm_kernel import LLMInstance
from app.services.configure_center.response_utils import next_console_response


def model_instance_get(params):
    """
    获取模型实例
    :return:
    """
    llm_code = params.get("llm_code")
    user_id = int(params.get("user_id"))
    llm_instance = LLMInstance.query.filter_by(llm_code=llm_code).first()
    if not llm_instance:
        return next_console_response(error_status=True, error_message="模型不存在")
    if llm_instance.user_id != user_id:
        return next_console_response(error_status=True, error_message="无权限查看")
    return next_console_response(result=llm_instance.to_dict())


def model_instance_add(params):
    """
    添加模型实例
    :return:
    """
    llm_name = params.get("llm_name", "")
    llm_type = params.get("llm_type", "")
    llm_api_secret_key = params.get("llm_api_secret_key", "")
    llm_api_access_key = params.get("llm_api_access_key", "")
    llm_desc = params.get("llm_desc", "")
    llm_tags = params.get("llm_tags", "")
    llm_company = params.get("llm_company", "")
    llm_is_proxy = params.get("llm_is_proxy", False)
    llm_base_url = params.get("llm_base_url", "")
    llm_proxy_url = params.get("llm_proxy_url", app.config['openai_url'])
    llm_is_public = params.get("llm_is_public", False)
    if llm_is_public not in (True, False):
        return next_console_response(error_status=True, error_message="代理参数错误")
    llm_source = params.get("llm_source", "")
    user_id = int(params.get("user_id"))
    llm_status = "正常"
    frequency_penalty = params.get("frequency_penalty", 0)
    max_tokens = params.get("max_tokens", 100000)
    n = params.get("n", 1)
    presence_penalty = params.get("presence_penalty", 0)
    response_format = params.get("response_format", {
        "type": "text",
    })
    stop = params.get("stop", [])
    stream = params.get("stream", True)
    temperature = params.get("temperature", 1)
    top_p = params.get("top_p", 1)
    # 检查模型是否存在
    old_llm_instance = LLMInstance.query.filter_by(
        llm_name=llm_name,
        llm_api_secret_key=llm_api_secret_key,
        user_id=user_id
    ).first()
    if old_llm_instance:
        return next_console_response(error_status=True, error_message="模型已存在")
    llm_code = str(uuid.uuid4())[:20]
    llm_instance = LLMInstance(
        llm_code=llm_code, llm_name=llm_name, user_id=user_id,
        llm_api_secret_key=llm_api_secret_key, llm_api_access_key=llm_api_access_key,
        llm_type=llm_type, llm_desc=llm_desc, llm_tags=llm_tags, llm_company=llm_company,llm_is_proxy=llm_is_proxy,
        llm_base_url=llm_base_url, llm_proxy_url=llm_proxy_url,
        llm_status=llm_status, llm_source=llm_source, llm_is_public=llm_is_public,
        frequency_penalty=frequency_penalty, max_tokens=max_tokens, n=n, presence_penalty=presence_penalty,
        response_format=response_format, stop=stop, stream=stream, temperature=temperature, top_p=top_p
    )
    db.session.add(llm_instance)
    db.session.commit()
    return next_console_response(result=llm_instance.to_dict())


def model_instance_delete(params):
    """
    删除模型实例
    :param params:
    :return:
    """
    llm_codes = params.get("llm_codes", [])
    user_id = int(params.get("user_id"))
    llm_instances = LLMInstance.query.filter(
        LLMInstance.llm_code.in_(llm_codes),
        LLMInstance.user_id == user_id
    ).all()
    if llm_instances:
        for llm_instance in llm_instances:
            db.session.delete(llm_instance)
        db.session.commit()
        return next_console_response(result="删除成功")
    else:
        return next_console_response(error_status=True, error_message="模型不存在")


def model_instance_update(params):
    """
    更新模型实例
    :param params:
    :return:
    """
    llm_code = params.get("llm_code")
    user_id = int(params.get("user_id"))
    target_llm_instance = LLMInstance.query.filter_by(llm_code=llm_code).first()
    if not target_llm_instance:
        return next_console_response(error_status=True, error_message="模型不存在")
    if target_llm_instance.user_id != user_id:
        return next_console_response(error_status=True, error_message="无权限修改")
    llm_name = params.get("llm_name")
    llm_type = params.get("llm_type")
    llm_api_secret_key = params.get("llm_api_secret_key")
    llm_api_access_key = params.get("llm_api_access_key")
    llm_desc = params.get("llm_desc")
    llm_tags = params.get("llm_tags")
    llm_company = params.get("llm_company")
    llm_is_proxy = params.get("llm_is_proxy", False)
    llm_is_public = params.get("llm_is_public", False)
    llm_source = params.get("llm_source")
    llm_base_url = params.get("llm_base_url")
    llm_proxy_url = params.get("llm_proxy_url", app.config['openai_url'])
    if llm_is_proxy not in (True, False):
        return next_console_response(error_status=True, error_message="代理参数错误")
    if llm_name and llm_name != target_llm_instance.llm_name:
        target_llm_instance.llm_name = llm_name
    if llm_type is not None and llm_type != target_llm_instance.llm_type:
        target_llm_instance.llm_type = llm_type
    if llm_api_secret_key is not None and llm_api_secret_key != target_llm_instance.llm_api_secret_key:
        target_llm_instance.llm_api_secret_key = llm_api_secret_key
    if llm_api_access_key is not None and llm_api_access_key != target_llm_instance.llm_api_access_key:
        target_llm_instance.llm_api_access_key = llm_api_access_key
    if llm_desc is not None and llm_desc != target_llm_instance.llm_desc:
        target_llm_instance.llm_desc = llm_desc
    if llm_tags is not None and llm_tags != target_llm_instance.llm_tags:
        target_llm_instance.llm_tags = llm_tags
    if llm_company is not None and llm_company != target_llm_instance.llm_company:
        target_llm_instance.llm_company = llm_company
    if llm_is_proxy is not None and llm_is_proxy != target_llm_instance.llm_is_proxy:
        target_llm_instance.llm_is_proxy = llm_is_proxy
    if llm_is_public is not None and llm_is_public != target_llm_instance.llm_is_public:
        target_llm_instance.llm_is_public = llm_is_public
    if llm_source is not None and llm_source != target_llm_instance.llm_source:
        target_llm_instance.llm_source = llm_source
    if llm_base_url is not None and llm_base_url != target_llm_instance.llm_base_url:
        target_llm_instance.llm_base_url = llm_base_url
    if llm_proxy_url is not None and llm_proxy_url != target_llm_instance.llm_proxy_url:
        target_llm_instance.llm_proxy_url = llm_proxy_url

    db.session.add(target_llm_instance)
    db.session.commit()
    return next_console_response(result=target_llm_instance.to_dict())


def model_instance_search(params):
    """
    搜索模型实例
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    llm_code = params.get("llm_code")
    llm_name = params.get("llm_name")
    llm_type = params.get("llm_type")
    llm_status = params.get("llm_status", [])
    llm_is_proxy = params.get("llm_is_proxy", [])
    llm_company = params.get("llm_company")
    llm_desc = params.get("llm_desc")
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 20)
    fetch_all = params.get("fetch_all", False)
    filter_list = [
        or_(
            LLMInstance.user_id == user_id,
            LLMInstance.llm_is_public == True
        )
    ]
    if llm_code:
        filter_list.append(LLMInstance.llm_code == llm_code)
    if llm_name:
        filter_list.append(LLMInstance.llm_name.like(f"%{llm_name}%"))
    if llm_type:
        filter_list.append(LLMInstance.llm_type == llm_type)
    if llm_status:
        filter_list.append(LLMInstance.llm_status.in_(llm_status))
    if llm_is_proxy:
        filter_list.append(LLMInstance.llm_is_proxy.in_(llm_is_proxy))
    if llm_company:
        filter_list.append(LLMInstance.llm_company.like(f"%{llm_company}%"))
    if llm_desc:
        filter_list.append(LLMInstance.llm_desc.like(f"%{llm_desc}%"))
    total = LLMInstance.query.filter(*filter_list).count()
    if fetch_all:
        llm_instances = LLMInstance.query.filter(*filter_list).all()
    else:
        llm_instances = LLMInstance.query.filter(*filter_list).paginate(page=page_num, per_page=page_size)
    data = []
    for llm_instance in llm_instances:
        sub_instance = {
            "llm_code": llm_instance.llm_code,
            "llm_name": llm_instance.llm_name,
            "llm_type": llm_instance.llm_type,
            "llm_status": llm_instance.llm_status,
            "llm_is_proxy": llm_instance.llm_is_proxy,
            "llm_company": llm_instance.llm_company,
            "llm_desc": llm_instance.llm_desc,
            "llm_tags": llm_instance.llm_tags,
            "create_time": llm_instance.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": llm_instance.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        data.append(sub_instance)
    return next_console_response(result={
        "total": total,
        "data": data
    })

