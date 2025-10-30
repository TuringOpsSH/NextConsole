from app.app import app, db
import uuid
from sqlalchemy import or_, and_
from app.models.configure_center.llm_kernel import LLMInstance, LLMInstanceAuthorizeInfo
from app.services.configure_center.response_utils import next_console_response
from sqlalchemy import distinct
from app.models.user_center.user_info import UserInfo
from app.utils.oss.oss_client import generate_new_path, generate_download_url
from app.models.user_center.user_role_info import UserRoleInfo
from app.models.user_center.role_info import RoleInfo
from sqlalchemy.orm.attributes import flag_modified


def model_instance_get(params):
    """
    获取模型实例
    :return:
    """
    llm_code = params.get("llm_code")
    user_id = int(params.get("user_id"))
    required_access = 'use'
    llm_instance = LLMInstance.query.filter_by(llm_code=llm_code).first()
    if not llm_instance:
        return next_console_response(error_status=True, error_message="模型不存在")
    _, access_info = check_model_authorize(
        user_id, [llm_instance], required_access=required_access, show_access=True)
    if not access_info:
        return next_console_response(error_status=True, error_message="无权限查看")
    access_info = access_info[llm_instance.id]
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
    result["access"] = access_info
    if 'edit' in access_info:
        result["is_editable"] = True
        result["llm_api_access_key"] = llm_instance.llm_api_access_key
        result["llm_api_secret_key"] = llm_instance.llm_api_secret_key
    else:
        result["is_editable"] = False
        result["llm_api_access_key"] = "****************"
        result["llm_api_secret_key"] = "****************"
    if 'manage' in access_info:
        from app.models.contacts.company_model import CompanyInfo
        from app.models.contacts.department_model import DepartmentInfo
        result['llm_authors'] = []
        # 添加所有者
        llm_owner = UserInfo.query.filter(
            UserInfo.user_id == llm_instance.user_id,
            UserInfo.user_status == 1
        ).first()
        result['llm_authors'].insert(0, {
            "structure_type": "friend",
            "company_id": llm_owner.user_company_id,
            "company_name": None,
            "department_id": llm_owner.user_department_id,
            "department_name": None,
            "user_id": llm_owner.user_id,
            "user_nick_name": llm_owner.user_nick_name,
            "user_avatar": llm_owner.user_avatar,
            "access": "own"
        })
        llm_authors = LLMInstanceAuthorizeInfo.query.filter(
            LLMInstanceAuthorizeInfo.model_id == llm_instance.id,
            LLMInstanceAuthorizeInfo.auth_status == '正常'
        ).all()
        # 公司，当前仅支持一个公司授权，
        company_ids = [author.auth_company_id for author in llm_authors
                       if author.auth_company_id and author.auth_department_id == 0]
        company_access_map = {author.auth_company_id: author for author in llm_authors
                              if author.auth_company_id}
        if company_ids:
            companies = CompanyInfo.query.filter(
                CompanyInfo.id.in_(company_ids),
                CompanyInfo.company_status == '正常'
            ).all()
            for company in companies:
                result['llm_authors'].append({
                    "structure_type": "company",
                    "company_id": company.id,
                    "company_name": company.company_name,
                    "company_logo": company.company_logo,
                    "department_id": None,
                    "department_name": None,
                    "user_id": None,
                    "user_nick_name": None,
                    "access": company_access_map.get(company.id).auth_type,
                    "access_id": company_access_map.get(company.id).id
                })
        department_ids = [author.auth_department_id for author in llm_authors if author.auth_department_id]
        department_access_map = {author.auth_department_id: author for author in llm_authors
                                 if author.auth_department_id}
        if department_ids:
            departments = DepartmentInfo.query.filter(
                DepartmentInfo.id.in_(department_ids),
                DepartmentInfo.department_status == '正常'
            ).all()
            for department in departments:
                result['llm_authors'].append({
                    "structure_type": "department",
                    "company_id": department.company_id,
                    "company_name": None,
                    "department_id": department.id,
                    "department_name": department.department_name,
                    "parent_department_id": department.parent_department_id,
                    "user_id": None,
                    "user_nick_name": None,
                    "access": department_access_map.get(department.id).auth_type,
                    "access_id": department_access_map.get(department.id).id
                })
        colleague_ids = [author.auth_colleague_id for author in llm_authors if author.auth_colleague_id]
        colleague_access_map = {author.auth_colleague_id: author for author in llm_authors
                                if author.auth_colleague_id}
        if colleague_ids:
            users = UserInfo.query.filter(
                UserInfo.user_id.in_(colleague_ids),
                UserInfo.user_status == 1
            ).all()
            for user in users:
                result['llm_authors'].append({
                    "structure_type": "colleague",
                    "company_id": user.user_company_id,
                    "company_name": None,
                    "department_id": user.user_department_id,
                    "user_department_id": user.user_department_id,
                    "department_name": None,
                    "user_id": user.user_id,
                    "user_nick_name": user.user_nick_name,
                    "user_name": user.user_name,
                    "user_avatar": user.user_avatar,
                    "user_nick_name_py": user.user_nick_name_py,
                    "access": colleague_access_map.get(user.user_id).auth_type,
                    "access_id": colleague_access_map.get(user.user_id).id
                })

        friend_ids = [author.auth_friend_id for author in llm_authors if
                      author.auth_friend_id and author.auth_friend_id != 0]
        friend_access_map = {author.auth_friend_id: author for author in llm_authors
                             if author.auth_friend_id and author.auth_friend_id != 0}
        if friend_ids:
            users = UserInfo.query.filter(
                UserInfo.user_id.in_(friend_ids),
                UserInfo.user_status == 1
            ).all()
            for user in users:
                result['llm_authors'].append({
                    "structure_type": "friend",
                    "company_id": None,
                    "company_name": None,
                    "department_id": None,
                    "department_name": None,
                    "user_id": user.user_id,
                    "user_nick_name": user.user_nick_name,
                    "user_avatar": user.user_avatar,
                    "user_nick_name_py": user.user_nick_name_py,
                    "access": friend_access_map.get(user.user_id).auth_type,
                    "access_id": friend_access_map.get(user.user_id).id
                })
        # 处理所有联系人
        for author in llm_authors:
            if author.auth_friend_id == 0:
                result['llm_authors'].append({
                    "structure_type": "friend",
                    "company_id": None,
                    "company_name": None,
                    "department_id": None,
                    "department_name": None,
                    "user_id": 0,
                    "user_nick_name": "所有好友",
                    "access": "read",
                    "access_id": author.id
                })
            # 处理全平台用户
            if author.auth_user_id == 0:
                result['llm_authors'].append({
                    "structure_type": "user",
                    "company_id": None,
                    "company_name": None,
                    "department_id": None,
                    "department_name": None,
                    "user_id": 0,
                    "user_nick_name": "全平台用户",
                    "access": "read",
                    "access_id": author.id
                })
    return next_console_response(result=result)


def model_instance_add(params):
    """
    添加模型实例
    :return:
    """
    llm_label = params.get("llm_label", "")
    llm_name = params.get("llm_name", "")
    llm_type = params.get("llm_type", "")
    llm_api_secret_key = params.get("llm_api_secret_key", "")
    llm_desc = params.get("llm_desc", "")
    llm_icon = params.get("llm_icon", "")
    llm_tags = params.get("llm_tags", "")
    llm_company = params.get("llm_company", "")
    llm_base_url = params.get("llm_base_url", "")
    llm_source = params.get("llm_source", "admin")
    user_id = int(params.get("user_id"))
    support_vis = params.get("support_vis", False)
    support_file = params.get("support_file", False)
    is_std_openai = params.get("is_std_openai", False)
    llm_status = "正常"
    frequency_penalty = params.get("frequency_penalty", 0)
    max_tokens = params.get("max_tokens", 819200)
    n = params.get("n", 1)
    presence_penalty = params.get("presence_penalty", 0)
    response_format = params.get("response_format", {
        "type": "text",
    })
    stop = params.get("stop", [])
    stream = params.get("stream", True)
    temperature = params.get("temperature", 1)
    top_p = params.get("top_p", 1)
    use_default = params.get("use_default", True)
    extra_headers_schema = params.get("extra_headers", {})
    extra_body_schema = params.get("extra_body", {})
    llm_authors = params.get("llm_authors", [])
    llm_code = str(uuid.uuid4())[:20]
    from app.services.app_center.node_params_service import load_properties
    try:
        extra_headers = load_properties(extra_headers_schema.get('properties', {}), {})
    except Exception as e:
        extra_headers = {}
    try:
        extra_body = load_properties(extra_body_schema.get('properties', {}), {})
    except Exception as e:
        extra_body = {}
    llm_instance = LLMInstance(
        llm_code=llm_code,
        llm_name=llm_name,
        llm_label=llm_label,
        user_id=user_id,
        llm_api_secret_key=llm_api_secret_key,
        llm_type=llm_type,
        llm_desc=llm_desc,
        llm_tags=llm_tags,
        llm_icon=llm_icon,
        llm_company=llm_company,
        llm_base_url=llm_base_url,
        llm_status=llm_status,
        llm_source=llm_source,
        frequency_penalty=frequency_penalty, max_tokens=max_tokens, n=n, presence_penalty=presence_penalty,
        response_format=response_format, stop=stop, stream=stream, temperature=temperature, top_p=top_p,
        support_vis=support_vis, support_file=support_file, is_std_openai=is_std_openai,
        extra_headers=extra_headers, extra_body=extra_body, use_default=use_default
    )
    db.session.add(llm_instance)
    db.session.commit()
    if llm_authors:
        for llm_author in llm_authors:
            new_author = LLMInstanceAuthorizeInfo(
                user_id=user_id,
                model_id=llm_instance.id,
                auth_type='use',
                auth_status='正常',
            )
            if llm_author.get('structure_type') == 'colleague':
                new_author.auth_colleague_id = llm_author.get('colleague_id')
            elif llm_author.get('structure_type') == 'department':
                new_author.auth_company_id = llm_author.get('company_id')
                new_author.auth_department_id = llm_author.get('department_id')
            elif llm_author.get('structure_type') == 'friend':
                new_author.auth_friend_id = llm_author.get('friend_id')
            elif llm_author.get('structure_type') == 'user':
                new_author.auth_user_id = llm_author.get('auth_user_id')
            if llm_author.get('access'):
                new_author.auth_type = llm_author.get('access')
            db.session.add(new_author)
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
    required_access = 'manage'
    llm_instances = LLMInstance.query.filter(
        LLMInstance.llm_code.in_(llm_codes),
        LLMInstance.user_id == user_id
    ).all()
    if llm_instances:
        llm_instances = check_model_authorize(user_id, llm_instances, required_access=required_access)
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
    required_access = 'edit'
    target_llm_instance = LLMInstance.query.filter(
        LLMInstance.llm_code == llm_code,
        LLMInstance.llm_status != "已删除"
    ).first()
    if not target_llm_instance:
        return next_console_response(error_status=True, error_message="模型不存在")
    _, access_info = check_model_authorize(
        user_id, [target_llm_instance], required_access=required_access, show_access=True)
    if not access_info:
        return next_console_response(error_status=True, error_message="无权限修改")
    llm_label = params.get("llm_label")
    llm_name = params.get("llm_name")
    llm_type = params.get("llm_type")
    llm_desc = params.get("llm_desc")
    llm_api_secret_key = params.get("llm_api_secret_key")
    llm_api_access_key = params.get("llm_api_access_key")
    llm_tags = params.get("llm_tags")
    llm_company = params.get("llm_company")
    llm_is_proxy = params.get("llm_is_proxy")
    llm_icon = params.get("llm_icon")
    llm_base_url = params.get("llm_base_url")
    llm_proxy_url = params.get("llm_proxy_url")
    is_std_openai = params.get("is_std_openai")
    support_vis = params.get("support_vis")
    support_file = params.get("support_file")
    llm_status = params.get("llm_status")
    max_tokens = params.get("max_tokens")
    steam = params.get("stream")
    use_default = params.get("use_default")
    temperature = params.get("temperature")
    frequency_penalty = params.get("frequency_penalty")
    presence_penalty = params.get("presence_penalty")
    top_p = params.get("top_p")
    extra_headers_schema = params.get("extra_headers")
    extra_body_schema = params.get("extra_body")
    from app.services.app_center.node_params_service import load_properties
    try:
        extra_headers = load_properties(extra_headers_schema.get('properties', {}), {})
    except Exception as e:
        extra_headers = {}
    try:
        extra_body = load_properties(extra_body_schema.get('properties', {}), {})
    except Exception as e:
        extra_body = {}
    if llm_is_proxy is not None and llm_is_proxy not in (True, False):
        return next_console_response(error_status=True, error_message="代理参数错误")
    if llm_label and llm_label != target_llm_instance.llm_label:
        target_llm_instance.llm_label = llm_label
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
    if llm_status is not None and llm_status != target_llm_instance.llm_status:
        target_llm_instance.llm_status = llm_status
    if max_tokens is not None and max_tokens != target_llm_instance.max_tokens:
        target_llm_instance.max_tokens = max_tokens
    if steam is not None and steam != target_llm_instance.stream:
        target_llm_instance.stream = steam
    if use_default is not None and use_default != target_llm_instance.use_default:
        target_llm_instance.use_default = use_default
    if temperature is not None and temperature != target_llm_instance.temperature:
        target_llm_instance.temperature = temperature
    if frequency_penalty is not None and frequency_penalty != target_llm_instance.frequency_penalty:
        target_llm_instance.frequency_penalty = frequency_penalty
    if top_p is not None and top_p != target_llm_instance.top_p:
        target_llm_instance.top_p = top_p
    if presence_penalty is not None and presence_penalty != target_llm_instance.presence_penalty:
        target_llm_instance.presence_penalty = presence_penalty
    if extra_headers is not None and extra_headers != target_llm_instance.extra_headers:
        target_llm_instance.extra_headers = extra_headers
        flag_modified(target_llm_instance, "extra_headers")
    if extra_body is not None and extra_body != target_llm_instance.extra_body:
        target_llm_instance.extra_body = extra_body
        flag_modified(target_llm_instance, "extra_body")
    db.session.add(target_llm_instance)
    db.session.commit()
    # 更新权限
    llm_authors = params.get("llm_authors", [])
    if llm_authors:
        if 'manage' not in access_info[target_llm_instance.id]:
            return next_console_response(error_status=True, error_message="无权限修改授权")
        # 先删除已有授权，再添加此次授权
        exist_authors = LLMInstanceAuthorizeInfo.query.filter(
            LLMInstanceAuthorizeInfo.model_id == target_llm_instance.id
        ).all()
        # 开启事务
        try:
            for exist_author in exist_authors:
                db.session.delete(exist_author)
            db.session.commit()
            for llm_author in llm_authors:
                if llm_author.get('user_id') == user_id:
                    continue
                new_author = LLMInstanceAuthorizeInfo(
                    user_id=user_id,
                    model_id=target_llm_instance.id,
                    auth_type='use',
                    auth_status='正常',
                )
                if llm_author.get('structure_type') == 'colleague':
                    new_author.auth_colleague_id = llm_author.get('colleague_id')
                elif llm_author.get('structure_type') == 'department':
                    new_author.auth_company_id = llm_author.get('company_id')
                    new_author.auth_department_id = llm_author.get('department_id')
                elif llm_author.get('structure_type') == 'friend':
                    new_author.auth_friend_id = llm_author.get('friend_id')
                elif llm_author.get('structure_type') == 'user':
                    new_author.auth_user_id = llm_author.get('auth_user_id')
                if llm_author.get('access'):
                    new_author.auth_type = llm_author.get('access')
                db.session.add(new_author)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return next_console_response(error_status=True, error_message="授权更新失败，请稍后再试")
    return next_console_response(result=target_llm_instance.to_dict())


def model_instance_search(params):
    """
    搜索模型实例，只可以获取有权限的模型
        由于有权限的模型实例一般较少，所以先获取所有可见模型，然后应用层分页
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    llm_type = params.get("llm_type", [])
    llm_code = params.get("llm_code", [])
    llm_status = params.get("llm_status", ['正常'])
    llm_keyword = params.get("keyword")
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 20)
    fetch_all = params.get("fetch_all", False)
    filter_list = [
        or_(
            LLMInstance.user_id == user_id,
            LLMInstance.id.in_(check_model_authorize(user_id))
        )
    ]
    if llm_code:
        filter_list.append(LLMInstance.llm_code.in_(llm_code))
    if llm_keyword:
        filter_list.append(
            or_(
                LLMInstance.llm_code.like(f"%{llm_keyword}%"),
                LLMInstance.llm_name.like(f"%{llm_keyword}%"),
                LLMInstance.llm_desc.like(f"%{llm_keyword}%"),
                LLMInstance.llm_company.like(f"%{llm_keyword}%")
            )
        )
    if llm_type:
        filter_list.append(LLMInstance.llm_type.in_(llm_type))
    if llm_status:
        filter_list.append(LLMInstance.llm_status.in_(llm_status))
    total = LLMInstance.query.filter(*filter_list).count()
    if fetch_all:
        llm_instances = LLMInstance.query.filter(*filter_list).order_by(
            LLMInstance.llm_type.asc(),
            LLMInstance.create_time.desc()
        ).all()
    else:
        llm_instances = LLMInstance.query.filter(*filter_list).order_by(
            LLMInstance.llm_type.asc(),
            LLMInstance.create_time.desc()
        ).paginate(page=page_num, per_page=page_size)
    # 检查有权限的模型
    llm_instances = check_model_authorize(user_id, llm_instances)
    data = [llm_instance.show_info() for llm_instance in llm_instances]
    llm_type_options = LLMInstance.query.filter(
        or_(
            LLMInstance.user_id == user_id
        ),
        LLMInstance.llm_status != "已删除"
    ).with_entities(
        distinct(LLMInstance.llm_type).label("llm_type"),
    ).all()
    llm_status_options = LLMInstance.query.filter(
        or_(
            LLMInstance.user_id == user_id
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


def check_model_authorize(user_id, model_list=None, required_access=None, show_access=False):
    """
    检查用户是否有模型使用权限,如果有权限，返回有权限的模型列表
    1. 用户自己创建的模型
    2. 全平台公开 （auth_user_id = 0），
    3. 用户被明确授权的模型（好友,同事,用户）
    4. 用户所在部门被授权的模型
    5. 用户所在公司的模型
    6. 用户好友的全部好友类型
    :param required_access:
    :param show_access:
    :param user_id:
    :param model_list:
    :return:
    """
    from app.models.contacts.company_model import CompanyInfo
    from app.models.contacts.department_model import DepartmentInfo
    results = []
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    all_company_ids = []
    all_department_ids = []
    all_access_type = ['read', 'use', 'edit', 'manage', 'own']
    if required_access and required_access not in all_access_type:
        return results
    elif required_access:
        required_access_idx = all_access_type.index(required_access)
        required_access = all_access_type[required_access_idx:]
    if target_user.user_company_id:
        all_company_ids.append(target_user.user_company_id)
        target_company = CompanyInfo.query.filter(
            CompanyInfo.id == target_user.user_company_id,
            CompanyInfo.company_status == '正常'
        ).first()
        while target_company and target_company.parent_company_id:
            target_company = CompanyInfo.query.filter(
                CompanyInfo.id == target_company.parent_company_id,
                CompanyInfo.company_status == '正常'
            ).first()
            if target_company:
                all_company_ids.append(target_company.id)
        all_department_ids.append(target_user.user_department_id)
        target_department = DepartmentInfo.query.filter(
            DepartmentInfo.id == target_user.user_department_id,
            DepartmentInfo.department_status == '正常'
        ).first()
        while target_department and target_department.parent_department_id:
            target_department = DepartmentInfo.query.filter(
                DepartmentInfo.id == target_department.parent_department_id,
                DepartmentInfo.department_status == '正常'
            ).first()
            if target_department:
                all_department_ids.append(target_department.id)
    # 泛授权类型（全部好友）
    from app.models.user_center.user_info import UserFriendsRelation
    friends_relations = UserFriendsRelation.query.filter(
        UserFriendsRelation.rel_status >= 1,
        or_(
            and_(
                UserFriendsRelation.user_id == user_id,
                UserFriendsRelation.rel_status.in_([1, 2])
            ),
            and_(
                UserFriendsRelation.friend_id == user_id,
                UserFriendsRelation.rel_status.in_([1, 3])
            )
        ),
    ).all()
    friend_ids = []
    for friends_relation in friends_relations:
        if friends_relation.user_id != user_id:
            friend_ids.append(friends_relation.friend_id)
        if friends_relation.friend_id != user_id:
            friend_ids.append(friends_relation.friend_id)
    friend_ids = list(set(friend_ids))
    filter_conditions = [
        LLMInstanceAuthorizeInfo.auth_status == '正常',
        or_(
            LLMInstanceAuthorizeInfo.user_id == user_id,
            LLMInstanceAuthorizeInfo.auth_user_id == 0,
            LLMInstanceAuthorizeInfo.auth_user_id == user_id,
            LLMInstanceAuthorizeInfo.auth_friend_id == user_id,
            and_(
                LLMInstanceAuthorizeInfo.user_id.in_(friend_ids),
                LLMInstanceAuthorizeInfo.auth_friend_id == 0
            ),
            LLMInstanceAuthorizeInfo.auth_colleague_id == user_id,
            LLMInstanceAuthorizeInfo.auth_department_id.in_(all_department_ids),
            and_(
                LLMInstanceAuthorizeInfo.auth_company_id.in_(all_company_ids),
                LLMInstanceAuthorizeInfo.auth_department_id == 0
            )
        )
    ]
    if model_list:
        all_llm_ids = [model.id for model in model_list if model.user_id != user_id]
        filter_conditions.append(LLMInstanceAuthorizeInfo.model_id.in_(all_llm_ids))
    if required_access:
        filter_conditions.append(LLMInstanceAuthorizeInfo.auth_type.in_(required_access))
    authorize_info = LLMInstanceAuthorizeInfo.query.filter(
        *filter_conditions
    ).all()
    all_authorize_model_ids = list(set([info.model_id for info in authorize_info]))
    if not model_list:
        return all_authorize_model_ids
    for model in model_list:
        if model.user_id == user_id or model.id in all_authorize_model_ids:
            results.append(model)
    if show_access:
        access_map = {}
        for info in authorize_info:
            if info.model_id not in access_map:
                access_map[info.model_id] = []
            if info.auth_type not in access_map[info.model_id]:
                access_map[info.model_id].append(info.auth_type)
        for model in model_list:
            if model.user_id == user_id:
                access_map[model.id] = all_access_type
        return results, access_map
    return results


def remove_access_service(params):
    """
    移除模型访问权限
    :return:
    """
    user_id = int(params.get("user_id"))
    llm_code = params.get("llm_code")
    access_id = params.get("access_id")
    target_llm_instance = LLMInstance.query.filter(
        LLMInstance.llm_code == llm_code,
        LLMInstance.llm_status != "已删除"
    ).first()
    if not target_llm_instance:
        return next_console_response(error_status=True, error_message="模型不存在")
    required_access = 'manage'
    _, access_info = check_model_authorize(
        user_id, [target_llm_instance], required_access=required_access, show_access=True)
    if not access_info:
        return next_console_response(error_status=True, error_message="无权限修改")
    target_access = LLMInstanceAuthorizeInfo.query.filter(
        LLMInstanceAuthorizeInfo.id == access_id,
        LLMInstanceAuthorizeInfo.model_id == target_llm_instance.id
    ).first()
    if not target_access:
        return next_console_response(error_status=True, error_message="授权信息不存在")
    target_access.auth_status = "已移除"
    db.session.add(target_access)
    db.session.commit()
    return next_console_response(result="移除成功")


