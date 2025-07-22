from app.app import app, db
import uuid
from sqlalchemy import or_
from app.models.configure_center.llm_kernel import LLMInstance
from app.services.configure_center.response_utils import next_console_response
from sqlalchemy import distinct
from app.models.user_center.user_info import UserInfo
from app.utils.oss.oss_client import generate_new_path, generate_download_url
from app.models.user_center.user_role_info import UserRoleInfo
from app.models.user_center.role_info import RoleInfo


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
    if llm_instance.user_id != user_id and not llm_instance.llm_is_public:
        return next_console_response(error_status=True, error_message="无权限查看")
    result = llm_instance.to_dict()
    # 补充作者信息
    author_info = UserInfo.query.filter(
        UserInfo.user_id == llm_instance.user_id,
        UserInfo.user_status == 1
    ).first()
    result["author"] = {
        "user_id": author_info.user_id,
        "user_nick_name": author_info.user_nick_name,
        "user_avatar": author_info.user_avatar,
        "user_nick_name_py": author_info.user_nick_name_py,
    }
    if user_id == author_info.user_id or check_has_role(user_id, "next_console_admin"):
        result["is_editable"] = True
    else:
        result["is_editable"] = False
        result["llm_api_access_key"] = "****************"
        result["llm_api_secret_key"] = "****************"
    return next_console_response(result=result)


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
    llm_icon = params.get("llm_icon", "")
    llm_tags = params.get("llm_tags", "")
    llm_company = params.get("llm_company", "")
    llm_is_proxy = params.get("llm_is_proxy", False)
    llm_base_url = params.get("llm_base_url", "")
    llm_proxy_url = params.get("llm_proxy_url", '')
    llm_is_public = params.get("llm_is_public", False)
    llm_source = params.get("llm_source", "admin")
    user_id = int(params.get("user_id"))
    support_vis = params.get("support_vis", False)
    support_file = params.get("support_file", False)
    is_std_openai = params.get("is_std_openai", False)
    llm_status = "正常"
    frequency_penalty = params.get("frequency_penalty", 0)
    max_tokens = params.get("max_tokens", 8192)
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
        llm_code=llm_code,
        llm_name=llm_name,
        user_id=user_id,
        llm_api_secret_key=llm_api_secret_key,
        llm_api_access_key=llm_api_access_key,
        llm_type=llm_type,
        llm_desc=llm_desc,
        llm_tags=llm_tags,
        llm_icon=llm_icon,
        llm_company=llm_company,
        llm_is_proxy=llm_is_proxy,
        llm_base_url=llm_base_url,
        llm_proxy_url=llm_proxy_url,
        llm_status=llm_status,
        llm_source=llm_source,
        llm_is_public=llm_is_public,
        frequency_penalty=frequency_penalty, max_tokens=max_tokens, n=n, presence_penalty=presence_penalty,
        response_format=response_format, stop=stop, stream=stream, temperature=temperature, top_p=top_p,
        support_vis=support_vis, support_file=support_file, is_std_openai=is_std_openai
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
            llm_instance.llm_status = "已删除"
            db.session.add(llm_instance)
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
    target_llm_instance = LLMInstance.query.filter(
        LLMInstance.llm_code == llm_code,
        or_(
            LLMInstance.user_id == user_id,
            LLMInstance.llm_is_public == True
        ),
        LLMInstance.llm_status != "已删除"
    ).first()
    if not target_llm_instance:
        return next_console_response(error_status=True, error_message="模型不存在")
    if target_llm_instance.user_id != user_id and check_has_role(user_id, "next_console_admin") is False:
        return next_console_response(error_status=True, error_message="无权限修改")
    llm_name = params.get("llm_name")
    llm_type = params.get("llm_type")
    llm_desc = params.get("llm_desc")
    llm_api_secret_key = params.get("llm_api_secret_key")
    llm_api_access_key = params.get("llm_api_access_key")
    llm_tags = params.get("llm_tags")
    llm_company = params.get("llm_company")
    llm_is_proxy = params.get("llm_is_proxy")
    llm_is_public = params.get("llm_is_public")
    llm_icon = params.get("llm_icon")
    llm_base_url = params.get("llm_base_url")
    llm_proxy_url = params.get("llm_proxy_url")
    is_std_openai = params.get("is_std_openai")
    support_vis = params.get("support_vis")
    support_file = params.get("support_file")
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
    if llm_icon is not None and llm_icon != target_llm_instance.llm_icon:
        target_llm_instance.llm_icon = llm_icon
    if llm_base_url is not None and llm_base_url != target_llm_instance.llm_base_url:
        target_llm_instance.llm_base_url = llm_base_url
    if llm_proxy_url is not None and llm_proxy_url != target_llm_instance.llm_proxy_url:
        target_llm_instance.llm_proxy_url = llm_proxy_url
    if is_std_openai is not None and is_std_openai != target_llm_instance.is_std_openai:
        target_llm_instance.is_std_openai = is_std_openai
    if support_vis is not None and support_vis != target_llm_instance.support_vis:
        target_llm_instance.support_vis = support_vis
    if support_file is not None and support_file != target_llm_instance.support_file:
        target_llm_instance.support_file = support_file
    db.session.add(target_llm_instance)
    db.session.commit()
    return next_console_response(result=target_llm_instance.to_dict())


def model_instance_search(params):
    """
    搜索模型实例，只可以获取有权限的模型
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    llm_type = params.get("llm_type", [])
    llm_status = params.get("llm_status", ['正常'])
    llm_is_proxy = params.get("llm_is_proxy", [])
    llm_keyword = params.get("keyword")
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 20)
    fetch_all = params.get("fetch_all", False)
    filter_list = [
        or_(
            LLMInstance.user_id == user_id,
            LLMInstance.llm_is_public
        )
    ]
    if llm_keyword:
        filter_list.append(
            or_(
                LLMInstance.llm_code.like(f"%{llm_keyword}%"),
                LLMInstance.llm_name.like(f"%{llm_keyword}%"),
                LLMInstance.llm_desc.like(f"%{llm_keyword}%"),
                LLMInstance.llm_tags.like(f"%{llm_keyword}%"),
                LLMInstance.llm_company.like(f"%{llm_keyword}%")
            )
        )
    if llm_type:
        filter_list.append(LLMInstance.llm_type.in_(llm_type))
    if llm_status:
        filter_list.append(LLMInstance.llm_status.in_(llm_status))
    if llm_is_proxy:
        filter_list.append(LLMInstance.llm_is_proxy.in_(llm_is_proxy))
    total = LLMInstance.query.filter(*filter_list).count()
    if fetch_all:
        llm_instances = LLMInstance.query.filter(*filter_list).order_by(
            LLMInstance.llm_desc.desc()
        ).all()
    else:
        llm_instances = LLMInstance.query.filter(*filter_list).order_by(
            LLMInstance.llm_desc.desc()
        ).paginate(page=page_num, per_page=page_size)
    data = [llm_instance.show_info() for llm_instance in llm_instances]
    llm_type_options = LLMInstance.query.filter(
        or_(
            LLMInstance.user_id == user_id,
            LLMInstance.llm_is_public
        ),
        LLMInstance.llm_status != "已删除"
    ).with_entities(
        distinct(LLMInstance.llm_type).label("llm_type"),
    ).all()
    llm_status_options = LLMInstance.query.filter(
        or_(
            LLMInstance.user_id == user_id,
            LLMInstance.llm_is_public
        ),
        LLMInstance.llm_status != "已删除"
    ).with_entities(
        distinct(LLMInstance.llm_status).label("llm_status"),
    ).all()
    options = {
        "llm_type": [item.llm_type for item in llm_type_options],
        "llm_status": [item.llm_status for item in llm_status_options],
    }
    # 补充作者信息
    all_authors_id = [llm_instance.user_id for llm_instance in llm_instances]
    all_authors_id = list(set(all_authors_id))
    all_authors = UserInfo.query.filter(
        UserInfo.user_id.in_(all_authors_id),
        UserInfo.user_status == 1
    ).all()
    author_map = {author.user_id: author.to_dict() for author in all_authors}
    for llm_instance in data:
        author_info = author_map.get(llm_instance.get("user_id"), {})
        llm_instance["author"] = {
            "user_id": author_info.get("user_id"),
            "user_nick_name": author_info.get("user_nick_name"),
            "user_avatar": author_info.get("user_avatar"),
            "user_nick_name_py": author_info.get("user_nick_name_py"),
        }

    return next_console_response(result={
        "total": total,
        "data": data,
        "options": options
    })


def model_icon_upload_service(user_id, icon_data):
    """

    """
    suffix = icon_data.filename.split(".")[-1]
    avatar_path = generate_new_path("configure_center",
                                    user_id=user_id, file_type="file", suffix=suffix
                                    ).json.get("result")
    icon_data.save(avatar_path)
    app_icon = generate_download_url(
        ""
        "configure_center",
        avatar_path,
        suffix=suffix
    ).json.get("result")
    return next_console_response(result={
        "llm_icon": app_icon,
    })


def check_has_role(user_id, role_name):
    """
    检查用户是否有指定角色
    :param user_id:
    :param role_name:
    :return:
    """
    user_roles = UserRoleInfo.query.filter(UserRoleInfo.user_id == user_id).all()
    all_role_ids = [role.role_id for role in user_roles]
    all_roles = RoleInfo.query.filter(RoleInfo.role_id.in_(all_role_ids)).all()
    user_roles = [role.role_name for role in all_roles]
    if role_name in user_roles:
        return True
    return False
