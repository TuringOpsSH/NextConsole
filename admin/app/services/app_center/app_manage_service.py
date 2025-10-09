import json
from datetime import timedelta, timezone
from app.models.user_center.user_info import UserInfo
from app.models.app_center.app_info_model import *
from app.models.app_center.publish_info_model import AppPublishRecord
from app.models.contacts.company_model import CompanyInfo
from app.models.contacts.department_model import DepartmentInfo
from app.models.user_center.role_info import RoleInfo
from app.models.user_center.user_role_info import UserRoleInfo
from app.services.next_console.base import *
from app.utils.oss.oss_client import *


def search_all_apps(params):
    """
    搜索所有应用列表
        平台管理员可以看到所有的
        管理员能看到同一公司的
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    app_keyword = params.get("app_keyword")
    app_type = params.get("app_type", [])
    app_status = params.get("app_status", [])
    page_size = params.get("page_size", 20)
    page_num = params.get("page_num", 1)
    environment = params.get("environment", "开发")
    admin_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    all_condition = [
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == environment,
    ]
    if app_keyword:
        all_condition.append(
            or_(
                AppMetaInfo.app_name.like("%" + app_keyword + "%"),
                AppMetaInfo.app_desc.like("%" + app_keyword + "%")
            )
        )
    if app_type:
        all_condition.append(AppMetaInfo.app_type.in_(app_type))
    if app_status:
        all_condition.append(AppMetaInfo.app_status.in_(app_status))
    target_apps = AppMetaInfo.query.filter(
        *all_condition
    ).join(
        UserInfo,
        UserInfo.user_id == AppMetaInfo.user_id
    ).with_entities(
        AppMetaInfo,
        UserInfo.user_nick_name,
        UserInfo.user_avatar,
        UserInfo.user_company_id
    )
    if not check_has_role(admin_user.user_id, "next_console_admin"):
        # 非平台管理员
        target_apps = target_apps.filter(
            UserInfo.user_company_id == admin_user.user_company_id,
        )
    target_apps = target_apps.order_by(
        AppMetaInfo.create_time.desc()
    )
    total = target_apps.count()
    page_res = target_apps.paginate(page=page_num, per_page=page_size, error_out=False)
    data = []
    for sub_app, user_nick_name, user_avatar, user_company_id in page_res:
        data.append({
            "app_code": sub_app.app_code,
            "app_name": sub_app.app_name,
            "app_desc": sub_app.app_desc,
            "app_icon": sub_app.app_icon,
            "app_type": sub_app.app_type,
            "app_status": sub_app.app_status,
            "create_time": sub_app.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": sub_app.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "user_nick_name": user_nick_name,
            "user_avatar": user_avatar,
            "version": sub_app.version,
        })
    result = {
        "total": total,
        "page_num": page_num,
        "page_size": page_size,
        "data": data
    }
    return next_console_response(result=result)


def upload_app_icon(user_id, app_icon_data):
    """
    上传应用图标
    :param params:
    :return:
    """
    suffix = app_icon_data.filename.split(".")[-1]
    avatar_path = generate_new_path("app_center",
                                    user_id=user_id, file_type="file", suffix=suffix
                                    ).json.get("result")
    app_icon_data.save(avatar_path)
    app_icon = generate_download_url(
        "app_center",
        avatar_path, suffix=suffix ).json.get("result")
    return next_console_response(result={
        "app_icon": app_icon,
    })


def add_app(data):
    """
    添加应用
    :param data:
    :return:
    """
    user_id = int(data.get("user_id"))
    app_name = data.get("app_name")
    app_desc = data.get("app_desc", '')
    app_icon = data.get("app_icon")
    app_type = data.get("app_type", '个人应用')
    app_status = data.get("app_status", '创建中')
    app_code = str(uuid.uuid4())
    app_info = AppMetaInfo(
        app_code=app_code,
        user_id=user_id,
        app_name=app_name,
        app_desc=app_desc,
        app_icon=app_icon,
        app_type=app_type,
        app_status=app_status,
        app_config={
            "welcome": {
              "description": "这是一个配置示例",
              "image": "/images/welcome.svg",
              "keep": False,
              "prefixQuestions": [],
              "title": "欢迎使用"
            }
        },
        environment='开发',
    )
    db.session.add(app_info)
    db.session.commit()
    return next_console_response(result=app_info.to_dict())


def delete_app(data):
    """
    删除应用
        平台管理员和应用创建者可以删除应用
    :param data:
    :return:
    """
    app_code = data.get("app_code")
    user_id = int(data.get("user_id"))
    app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.environment == '开发',
        AppMetaInfo.app_status != '已删除'
    ).first()
    if not app_info:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if app_info.app_type != '个人应用':
        return next_console_response(error_status=True, error_message="无法删除非个人应用！", error_code=1002)
    if app_info.user_id != user_id:
        if not check_has_role(user_id, "next_console_admin"):
            return next_console_response(error_status=True, error_message="没有权限删除该应用！", error_code=1002)
    app_info.app_status = '已删除'
    db.session.add(app_info)
    db.session.commit()
    return next_console_response()


def get_app_detail(params):
    """
    获取应用详情,包括元数据，工作流列表，插件列表，数据列表，应用变量列表
        agent_code: '1',
        agent_name: 'agent1',
        agent_type: 'assistant',
        agent_icon: '/images/assistant.svg',
        id: 1
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '开发'
    ).first()
    if not app_info:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and app_info.user_id != user_id:
        app_user = UserInfo.query.filter(
            UserInfo.user_id == app_info.user_id
        ).first()
        current_user = UserInfo.query.filter(
            UserInfo.user_id == user_id
        ).first()
        if not app_user or not current_user:
            return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
        if app_user.user_company_id != current_user.user_company_id:
            return next_console_response(error_status=True, error_message="没有权限查看该应用！", error_code=1002)
    # 获取agent 列表
    all_workflows = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.app_code == app_code,
        AppWorkFlowRelation.rel_status == '正常',
        AppWorkFlowRelation.environment == '开发',
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        WorkFlowMetaInfo.workflow_status == '正常',
        WorkFlowMetaInfo.environment == '开发'
    ).with_entities(
        WorkFlowMetaInfo
    ).all()
    all_agents = []
    for workflow in all_workflows:
        all_agents.append({
            "id": workflow.id,
            "workflow_code": workflow.workflow_code,
            "workflow_name": workflow.workflow_name,
            "workflow_type": 'workflow',
            "workflow_icon": workflow.workflow_icon,
            "workflow_desc": workflow.workflow_desc,
            "workflow_is_main": workflow.workflow_is_main,
            "create_time": workflow.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        })
    result = {
        "meta": app_info.to_dict(),
        "flows": all_agents,
    }
    return next_console_response(result=result)


def update_app_detail(params):
    """
    更新应用详情
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '开发'
    ).first()
    if not app_info:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and app_info.user_id != user_id:
        app_user = UserInfo.query.filter(
            UserInfo.user_id == app_info.user_id
        ).first()
        current_user = UserInfo.query.filter(
            UserInfo.user_id == user_id
        ).first()
        if not app_user or not current_user:
            return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
        if app_user.user_company_id != current_user.user_company_id:
            return next_console_response(error_status=True, error_message="没有权限查看该应用！", error_code=1002)
    app_name = params.get("app_name")
    app_desc = params.get("app_desc")
    app_icon = params.get("app_icon")
    app_config = params.get("app_config", {})
    if app_name:
        app_info.app_name = app_name
    if app_desc is not None:
        app_info.app_desc = app_desc
    if app_icon:
        app_info.app_icon = app_icon
    if app_config:
        app_info.app_config = app_config
    db.session.add(app_info)
    db.session.commit()
    return next_console_response(result={
        "app_code": app_code,
        "app_name": app_name,
        "app_desc": app_desc,
        "app_icon": app_icon,
        "app_config": app_config,
    })


def create_app_publish(data):
    """
    创建应用发布
    :return:
    """
    user_id = int(data.get("user_id"))
    app_code = data.get("app_code")
    publish_name = data.get("publish_name")
    publish_desc = data.get("publish_desc")
    publish_config = data.get("publish_config")
    dev_app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '开发'
    ).first()
    if not dev_app_info:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and dev_app_info.user_id != user_id:
        return next_console_response(error_status=True, error_message="没有权限发布该应用！", error_code=1002)
    publish_code = str(uuid.uuid4()),
    new_publish_record = AppPublishRecord(
        app_code=app_code,
        publish_code=publish_code,
        user_id=user_id,
        publish_name=publish_name,
        publish_desc=publish_desc,
        publish_config=publish_config,
        publish_status='创建中',
    )
    db.session.add(new_publish_record)
    db.session.commit()
    # 发布配置校验
    ...
    # 应用合法性校验
    ...
    # 更加配置创建应用发布
    connectors = publish_config.get("connectors", [])
    # 覆写workflow的schema
    all_target_workflows = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.app_code == app_code,
        AppWorkFlowRelation.rel_status == '正常',
        AppWorkFlowRelation.environment == '开发',
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        WorkFlowMetaInfo.workflow_status == '正常',
        WorkFlowMetaInfo.environment == '开发'
    ).with_entities(
        WorkFlowMetaInfo
    ).all()
    for workflow in all_target_workflows:
        workflow.workflow_schema = workflow.workflow_edit_schema
        db.session.add(workflow)
    db.session.commit()
    publish_status = "成功"
    # for connector in connectors:
    #     if "NC" in connector.get("name"):
    res = publish_nextconsole({
        "app": dev_app_info,
        # "connector": connector,
        "user_id": user_id
    })
    if not res:
        publish_status = "异常"
        # break
    new_publish_record.publish_status = publish_status
    new_publish_record.publish_version = res.version
    db.session.add(new_publish_record)
    db.session.commit()
    return next_console_response(result=new_publish_record.to_dict())


def publish_nextconsole(params):
    """
    发布应用至NC平台
        失效旧版本，
        创建或者新增应用记录
        创建或者新增关系与工作流记录
            新增工作节点记录
    :param params:
    :return:
    """
    dev_app_info = params.get("app")
    connector = params.get("connector")
    exist_version = -1
    exist_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == dev_app_info.app_code,
        AppMetaInfo.environment == '生产',
        AppMetaInfo.app_status == '正常'
    ).first()
    if exist_app:
        exist_version = exist_app.version
        invalid_exist_data(dev_app_info, exist_app)
    new_app = AppMetaInfo(
        app_code=dev_app_info.app_code,
        user_id=dev_app_info.user_id,
        app_name=dev_app_info.app_name,
        app_desc=dev_app_info.app_desc,
        app_icon=dev_app_info.app_icon,
        app_type=dev_app_info.app_type,
        app_default_assistant=dev_app_info.app_default_assistant,
        app_status="升级中",
        app_config=dev_app_info.app_config,
        environment="生产",
        version=exist_version + 1,
    )
    db.session.add(new_app)
    db.session.commit()
    # 新增工作流与工作流关系
    all_dev_workflows = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.app_code == dev_app_info.app_code,
        AppWorkFlowRelation.rel_status == "正常",
        AppWorkFlowRelation.environment == "开发",
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        AppWorkFlowRelation.rel_status == "正常",
        WorkFlowMetaInfo.environment == "开发",
        WorkFlowMetaInfo.workflow_status == "正常"
    ).with_entities(
        WorkFlowMetaInfo
    ).all()
    res = merge_workflow_data(new_app, all_dev_workflows)
    if not res:
        return False
    new_app.app_status = "正常"
    db.session.add(new_app)
    db.session.commit()
    dev_app_info.app_status = '已发布'
    db.session.add(dev_app_info)
    db.session.commit()
    # 给自己新增授权
    author_app_publish({
        "app_code": dev_app_info.app_code,
        "user_id": dev_app_info.user_id,
        "user_list": [dev_app_info.user_id]
    })
    return new_app


def invalid_exist_data(dev_app_info, exist_app):
    """
    失效已有数据
    :return:
    """
    exist_app.app_status = '失效'
    db.session.add(exist_app)
    db.session.commit()
    exist_items = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.app_code == dev_app_info.app_code,
        AppWorkFlowRelation.rel_status == "正常",
        AppWorkFlowRelation.environment == "生产",
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        AppWorkFlowRelation.rel_status == "正常",
        WorkFlowMetaInfo.environment == "生产",
        WorkFlowMetaInfo.workflow_status == "正常"
    ).with_entities(
        AppWorkFlowRelation, WorkFlowMetaInfo
    ).all()
    exist_workflow_ids = []
    for exist_rel, exist_workflow in exist_items:
        exist_rel.rel_status = "失效"
        db.session.add(exist_rel)
        exist_workflow.workflow_status = "失效"
        db.session.add(exist_workflow)
        exist_workflow_ids.append(exist_workflow.id)
    db.session.commit()
    # 失效所有node
    exist_nodes = WorkflowNodeInfo.query.filter(
        WorkflowNodeInfo.workflow_id.in_(exist_workflow_ids)
    ).all()
    for node in exist_nodes:
        node.node_status = "失效"
        db.session.add(node)
    db.session.commit()


def merge_workflow_data(new_app, all_dev_workflows):
    """
    迁移融合工作流数据
    :return:
    """
    try:
        for dev_workflow in all_dev_workflows:
            new_prd_workflow = WorkFlowMetaInfo(
                user_id=dev_workflow.user_id,
                workflow_code=dev_workflow.workflow_code,
                workflow_name=dev_workflow.workflow_name,
                workflow_desc=dev_workflow.workflow_desc,
                workflow_icon=dev_workflow.workflow_icon,
                workflow_schema=dev_workflow.workflow_schema,
                workflow_edit_schema=dev_workflow.workflow_edit_schema,
                workflow_is_main=dev_workflow.workflow_is_main,
                workflow_status="正常",
                environment="生产",
                version=new_app.version
            )
            db.session.add(new_prd_workflow)
            db.session.commit()
            new_prd_rel = AppWorkFlowRelation(
                app_code=new_app.app_code,
                workflow_code=dev_workflow.workflow_code,
                rel_type="使用",
                environment="生产",
            )
            db.session.add(new_prd_rel)
            db.session.commit()
            dev_nodes = WorkflowNodeInfo.query.filter(
                WorkflowNodeInfo.workflow_id == dev_workflow.id,
                WorkflowNodeInfo.node_status == "正常",
                WorkflowNodeInfo.environment == "开发",
            ).all()
            for dev_node in dev_nodes:
                new_prod_node = WorkflowNodeInfo(
                    user_id=dev_node.user_id,
                    workflow_id=new_prd_workflow.id,
                    node_code=dev_node.node_code,
                    node_type=dev_node.node_type,
                    node_icon=dev_node.node_icon,
                    node_name=dev_node.node_name,
                    node_desc=dev_node.node_desc,
                    node_run_model_config=dev_node.node_run_model_config,
                    node_llm_code=dev_node.node_llm_code,
                    node_llm_params=dev_node.node_llm_params,
                    node_llm_system_prompt_template=dev_node.node_llm_system_prompt_template,
                    node_llm_user_prompt_template=dev_node.node_llm_user_prompt_template,
                    node_result_format=dev_node.node_result_format,
                    node_result_params_json_schema=dev_node.node_result_params_json_schema,
                    node_result_extract_separator=dev_node.node_result_extract_separator,
                    node_result_extract_quote=dev_node.node_result_extract_quote,
                    node_result_extract_columns=dev_node.node_result_extract_columns,
                    node_result_template=dev_node.node_result_template,
                    node_timeout=dev_node.node_timeout,
                    node_retry_max=dev_node.node_retry_max,
                    node_retry_duration=dev_node.node_retry_duration,
                    node_failed_solution=dev_node.node_failed_solution,
                    node_failed_template=dev_node.node_failed_template,
                    node_session_memory_size=dev_node.node_session_memory_size,
                    node_deep_memory=dev_node.node_deep_memory,
                    node_agent_nickname=dev_node.node_agent_nickname,
                    node_agent_desc=dev_node.node_agent_desc,
                    node_agent_avatar=dev_node.node_agent_avatar,
                    node_agent_prologue=dev_node.node_agent_prologue,
                    node_agent_preset_question=dev_node.node_agent_preset_question,
                    node_agent_tools=dev_node.node_agent_tools,
                    node_input_params_json_schema=dev_node.node_input_params_json_schema,
                    node_tool_api_url=dev_node.node_tool_api_url,
                    node_tool_http_method=dev_node.node_tool_http_method,
                    node_tool_http_header=dev_node.node_tool_http_header,
                    node_tool_http_params=dev_node.node_tool_http_params,
                    node_tool_http_body=dev_node.node_tool_http_body,
                    node_tool_http_body_type=dev_node.node_tool_http_body_type,
                    node_rag_resources=dev_node.node_rag_resources,
                    node_rag_ref_show=dev_node.node_rag_ref_show,
                    node_rag_query_template=dev_node.node_rag_query_template,
                    node_rag_recall_config=dev_node.node_rag_recall_config,
                    node_rag_rerank_config=dev_node.node_rag_rerank_config,
                    node_rag_web_search_config=dev_node.node_rag_web_search_config,
                    node_enable_message=dev_node.node_enable_message,
                    node_message_schema_type=dev_node.node_message_schema_type,
                    node_message_schema=dev_node.node_message_schema,
                    node_file_reader_config=dev_node.node_file_reader_config,
                    node_file_splitter_config=dev_node.node_file_splitter_config,
                    node_sub_workflow_config=dev_node.node_sub_workflow_config,
                    environment="生产",
                    version=new_app.version
                )
                db.session.add(new_prod_node)
            db.session.commit()
    except Exception as e:
        app.logger.error(f"迁移融合工作流数据:{e}")
        return False
    return True


def search_app_publish(data):
    """
    获取指定应用的发布记录
    :param data:
    :return:
    """
    user_id = int(data.get("user_id"))
    app_code = data.get("app_code")
    page_num = data.get("page_num", 1)
    page_size = data.get("page_size", 50)
    target_publish_records = AppPublishRecord.query.filter(
        AppPublishRecord.app_code == app_code
    )
    admin_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    if not check_has_role(user_id, "next_console_admin"):
        # 非平台管理员
        target_publish_records = target_publish_records.join(
            UserInfo,
            UserInfo.user_id == AppPublishRecord.user_id
        ).filter(
            UserInfo.user_company_id == admin_user.user_company_id
        ).with_entities(
            AppPublishRecord
        )
    target_publish_records = target_publish_records.order_by(
        AppPublishRecord.create_time.desc()
    )
    total = target_publish_records.count()
    data = target_publish_records.paginate(page=page_num, per_page=page_size, error_out=False)
    prod_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.environment == '生产',
        AppMetaInfo.app_status == '正常'
    ).first()
    res = []
    for publish_record in data:
        record_dict = publish_record.to_dict()
        if publish_record.publish_version == prod_app.version:
            record_dict["publish_is_prod"] = True
        res.append(record_dict)
    result = {
        "total": total,
        "page_num": page_num,
        "page_size": page_size,
        "data": res
    }
    return next_console_response(result=result)


def author_app_publish(data):
    """
    授权应用发布
    :param data:
    :return:
    """
    user_id = int(data.get("user_id"))
    app_code = data.get("app_code")
    user_list = data.get("user_list")
    department_list = data.get("department_list")
    company_list = data.get("company_list")
    is_nc_admin = check_has_role(user_id, "next_console_admin")
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status == '正常',
        AppMetaInfo.environment == '生产'
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not is_nc_admin and target_app.user_id != user_id:
        return next_console_response(error_status=True, error_message="没有权限授权该应用！", error_code=1002)
    admin_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    res = []
    if user_list:
        if -1 in user_list and is_nc_admin:
            new_access_info = AppAccessInfo(
                app_code=app_code,
                user_id=-1,
                access_type='使用',
                access_name='使用',
                access_status='正常',
            )
            db.session.add(new_access_info)
            db.session.commit()
            return next_console_response(result=[new_access_info.to_dict()])
        res.extend(author_app_publish_user({
            "user_list": user_list,
            "app_code": app_code,
            "is_nc_admin": is_nc_admin,
            "admin_user": admin_user
        }))
    if department_list:
        res.extend(author_app_publish_department({
            "department_list": department_list,
            "app_code": app_code,
            "is_nc_admin": is_nc_admin,
            "admin_user": admin_user
        }))
    if company_list and is_nc_admin:
        res.extend(author_app_publish_company({
            "company_list": company_list,
            "app_code": app_code,
        }))
    res = [access.to_dict() for access in res]
    return next_console_response(result=res)


def author_app_publish_user(data):
    """
    为用户授权应用发布
    :param data:
    :return:
    """
    user_list = data.get("user_list")
    app_code = data.get("app_code")
    is_nc_admin = data.get("is_nc_admin", False)
    admin_user = data.get("admin_user")
    all_conditions = [
        UserInfo.user_id.in_(user_list),
        UserInfo.user_status == 1,
    ]
    if not is_nc_admin:
        all_conditions.append(UserInfo.user_company_id == admin_user.user_company_id)
    target_uses = UserInfo.query.filter(*all_conditions).all()
    if not target_uses:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1002)
    all_user_ids = [user.user_id for user in target_uses]
    exist_user_access = AppAccessInfo.query.filter(
        AppAccessInfo.app_code == app_code,
        AppAccessInfo.user_id.in_(all_user_ids),
        AppAccessInfo.access_status == '正常',
    ).all()
    exist_user_access = [user.user_id for user in exist_user_access]
    res = []
    for user in target_uses:
        if user.user_id in exist_user_access:
            continue
        new_access_info = AppAccessInfo(
            app_code=app_code,
            user_id=user.user_id,
            user_code=user.user_code,
            access_type='使用',
            access_name='使用',
            access_status='正常',
        )
        db.session.add(new_access_info)
        res.append(new_access_info)
    db.session.commit()
    return res


def author_app_publish_department(data):
    """
    为部门授权应用发布
    :param data:
    :return:
    """
    department_list = data.get("department_list")
    app_code = data.get("app_code")
    is_nc_admin = data.get("is_nc_admin", False)
    admin_user = data.get("admin_user")
    all_conditions = [
        DepartmentInfo.id.in_(department_list),
        DepartmentInfo.department_status == "正常",
    ]
    if not is_nc_admin:
        all_conditions.append(DepartmentInfo.company_id == admin_user.user_company_id)
    target_departments = DepartmentInfo.query.filter(*all_conditions).all()
    if not target_departments:
        return []
    all_department_ids = [department.id for department in target_departments]
    exist_department_access = AppAccessInfo.query.filter(
        AppAccessInfo.app_code == app_code,
        AppAccessInfo.department_id.in_(all_department_ids),
        AppAccessInfo.access_status == '正常',
    ).all()
    exist_department_access = [department.department_id for department in exist_department_access]
    res = []
    for department in target_departments:
        if department.id in exist_department_access:
            continue
        new_access_info = AppAccessInfo(
            app_code=app_code,
            department_id=department.id,
            access_type='使用',
            access_name='使用',
            access_status='正常',
        )
        db.session.add(new_access_info)
        res.append(new_access_info)
    db.session.commit()
    return res


def author_app_publish_company(data):
    """
    为公司授权应用发布
    :param data:
    :return:
    """
    company_list = data.get("company_list")
    app_code = data.get("app_code")
    target_companies = CompanyInfo.query.filter(
        CompanyInfo.id.in_(company_list),
        CompanyInfo.company_status == "正常"
    ).all()
    if not target_companies:
        return []
    all_company_ids = [company.id for company in target_companies]
    exist_company_access = AppAccessInfo.query.filter(
        AppAccessInfo.app_code == app_code,
        AppAccessInfo.company_id.in_(all_company_ids),
        AppAccessInfo.access_status == '正常',
    ).all()
    exist_company_access = [company.company_id for company in exist_company_access]
    res = []
    for company in target_companies:
        if company.id in exist_company_access:
            continue
        new_access_info = AppAccessInfo(
            app_code=app_code,
            company_id=company.id,
            access_type='使用',
            access_name='使用',
            access_status='正常',
        )
        db.session.add(new_access_info)
        res.append(new_access_info)
    db.session.commit()
    return res


def cancel_author_app_publish(data):
    """
    取消用户授权
    :param data:
    :return:
    """
    user_id = int(data.get("user_id"))
    app_code = data.get("app_code")
    user_list = data.get("user_list")
    department_list = data.get("department_list")
    company_list = data.get("company_list")
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status == '正常',
        AppMetaInfo.environment == '生产'
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    is_nc_admin = check_has_role(user_id, "next_console_admin")
    admin_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    if not is_nc_admin and target_app.user_id != user_id:
        return next_console_response(error_status=True, error_message="没有权限操作该应用！", error_code=1002)
    if user_list and -1 in user_list and is_nc_admin:
        target_all_access = AppAccessInfo.query.filter(
            AppAccessInfo.app_code == app_code,
            AppAccessInfo.user_id == -1,
            AppAccessInfo.access_type == '使用',
            AppAccessInfo.access_status == '正常',
        ).first()
        target_all_access.access_status = '失效'
        db.session.add(target_all_access)
        db.session.commit()
        return next_console_response(result=[target_all_access.to_dict()])
    res = []
    if user_list:
        all_conditions = [
            UserInfo.user_id.in_(user_list),
            UserInfo.user_status == 1,
        ]
        if not is_nc_admin:
            all_conditions.append(UserInfo.user_company_id == admin_user.user_company_id)
        target_uses = UserInfo.query.filter(
            *all_conditions
        ).all()
        if not target_uses:
            return next_console_response(error_status=True, error_message="用户不存在！", error_code=1002)
        # 去除权限
        all_user_ids = [user.user_id for user in target_uses]
        exist_user_access = AppAccessInfo.query.filter(
            AppAccessInfo.app_code == app_code,
            AppAccessInfo.user_id.in_(all_user_ids),
            AppAccessInfo.access_status == '正常',
        ).all()
        for access in exist_user_access:
            access.access_status = '失效'
            db.session.add(access)
            res.append(access)
        db.session.commit()
    if department_list:
        all_conditions = [
            DepartmentInfo.id.in_(department_list),
            DepartmentInfo.department_status == "正常",
        ]
        if not is_nc_admin:
            all_conditions.append(DepartmentInfo.company_id == admin_user.user_company_id)
        target_departments = DepartmentInfo.query.filter(*all_conditions).all()
        if not target_departments:
            return []
        all_department_ids = [department.id for department in target_departments]
        exist_department_access = AppAccessInfo.query.filter(
            AppAccessInfo.app_code == app_code,
            AppAccessInfo.department_id.in_(all_department_ids),
            AppAccessInfo.access_status == '正常',
        ).all()
        for access in exist_department_access:
            access.access_status = '失效'
            db.session.add(access)
            res.append(access)
        db.session.commit()
    if company_list and is_nc_admin:
        all_conditions = [
            CompanyInfo.id.in_(company_list),
            CompanyInfo.company_status == "正常",
        ]
        target_companies = CompanyInfo.query.filter(*all_conditions).all()
        if not target_companies:
            return []
        all_company_ids = [company.id for company in target_companies]
        exist_company_access = AppAccessInfo.query.filter(
            AppAccessInfo.app_code == app_code,
            AppAccessInfo.company_id.in_(all_company_ids),
            AppAccessInfo.access_status == '正常',
        ).all()
        for access in exist_company_access:
            access.access_status = '失效'
            db.session.add(access)
            res.append(access)
        db.session.commit()
    res = [access.to_dict() for access in res]
    return next_console_response(result=res)


def search_app_access(data):
    """
    获取应用当前的授权用户列表
    :param data:
    :return:
    """
    user_id = int(data.get("user_id"))
    app_code = data.get("app_code")
    access_object = data.get("access_object", 'user')
    access_keyword = data.get("access_keyword", '')
    page_num = data.get("page_num", 1)
    page_size = data.get("page_size", 50)
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status == '正常',
        AppMetaInfo.environment == '生产'
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and target_app.user_id != user_id:
        return next_console_response(error_status=True, error_message="没有权限授权该应用！", error_code=1002)
    if access_object == "user":
        all_access_flag = AppAccessInfo.query.filter(
            AppAccessInfo.app_code == app_code,
            AppAccessInfo.access_status == '正常',
            AppAccessInfo.user_id == -1
        ).first()
        if all_access_flag:
            result = {
                "total": 1,
                "page_num": page_num,
                "page_size": page_size,
                "data": [{
                    "id": all_access_flag.id,
                    "user_id": -1,
                    "user_code": all_access_flag.user_code,
                    "access_type": all_access_flag.access_type,
                    "access_name": all_access_flag.access_name,
                    "access_status": all_access_flag.access_status,
                    "create_time": all_access_flag.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "update_time": all_access_flag.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                }]
            }
            return next_console_response(result=result)
        user_conditions = [
            UserInfo.user_status == 1
        ]
        if access_keyword:
            user_conditions.append(
                or_(
                    UserInfo.user_nick_name.like("%" + access_keyword + "%"),
                    UserInfo.user_name.like("%" + access_keyword + "%"),
                    UserInfo.user_email.like("%" + access_keyword + "%"),
                    UserInfo.user_phone.like("%" + access_keyword + "%"),
                    UserInfo.user_code.like("%" + access_keyword + "%")
                )
            )
        target_access_users = AppAccessInfo.query.filter(
            AppAccessInfo.app_code == app_code,
            AppAccessInfo.access_status == '正常',
            AppAccessInfo.user_id.isnot(None)
        ).join(
            UserInfo,
            UserInfo.user_id == AppAccessInfo.user_id
        ).filter(
            *user_conditions
        ).with_entities(
            AppAccessInfo,
            UserInfo.user_id,
            UserInfo.user_nick_name,
            UserInfo.user_avatar
        ).order_by(
            AppAccessInfo.create_time.desc()
        )
        total = target_access_users.count()
        data = target_access_users.paginate(page=page_num, per_page=page_size, error_out=False)
        result = {
            "total": total,
            "page_num": page_num,
            "page_size": page_size,
            "data": []
        }
        for access_info, user_id, user_nick_name, user_avatar in data:
            result["data"].append({
                "id": access_info.id,
                "user_id": user_id,
                "user_code": access_info.user_code,
                "user_nick_name": user_nick_name,
                "user_avatar": user_avatar,
                "access_type": access_info.access_type,
                "access_name": access_info.access_name,
                "access_status": access_info.access_status,
                "create_time": access_info.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                "update_time": access_info.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return next_console_response(result=result)
    elif access_object == "department":
        department_conditions = [
            DepartmentInfo.department_status == '正常'
        ]
        if access_keyword:
            department_conditions.append(
                or_(
                    DepartmentInfo.department_code.like("%" + access_keyword + "%"),
                    DepartmentInfo.department_name.like("%" + access_keyword + "%"),
                    DepartmentInfo.department_desc.like("%" + access_keyword + "%"),
                )
            )

        target_access_users = AppAccessInfo.query.filter(
            AppAccessInfo.app_code == app_code,
            AppAccessInfo.access_status == '正常',
            AppAccessInfo.department_id.isnot(None)
        ).join(
            DepartmentInfo,
            DepartmentInfo.id == AppAccessInfo.department_id
        ).with_entities(
            AppAccessInfo,
            DepartmentInfo.id,
            DepartmentInfo.department_code,
            DepartmentInfo.department_name,
            DepartmentInfo.department_logo
        ).filter(
            *department_conditions
        ).order_by(
            AppAccessInfo.create_time.desc()
        )
        total = target_access_users.count()
        data = target_access_users.paginate(page=page_num, per_page=page_size, error_out=False)
        result = {
            "total": total,
            "page_num": page_num,
            "page_size": page_size,
            "data": []
        }
        for access_info, department_id, department_code, department_name, department_logo in data:
            result["data"].append({
                "id": access_info.id,
                "department_id": department_id,
                "department_code": department_code,
                "department_name": department_name,
                "department_logo": department_logo,
                "access_type": access_info.access_type,
                "access_name": access_info.access_name,
                "access_status": access_info.access_status,
                "create_time": access_info.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                "update_time": access_info.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return next_console_response(result=result)
    elif access_object == "company":
        company_conditions = [
            CompanyInfo.company_status == '正常'
        ]
        if access_keyword:
            company_conditions.append(
                or_(
                    CompanyInfo.company_code.like("%" + access_keyword + "%"),
                    CompanyInfo.company_name.like("%" + access_keyword + "%"),
                    CompanyInfo.company_desc.like("%" + access_keyword + "%"),
                )
            )
        target_access_users = AppAccessInfo.query.filter(
            AppAccessInfo.app_code == app_code,
            AppAccessInfo.access_status == '正常',
            AppAccessInfo.company_id.isnot(None)
        ).join(
            CompanyInfo,
            CompanyInfo.id == AppAccessInfo.company_id
        ).with_entities(
            AppAccessInfo,
            CompanyInfo.id,
            CompanyInfo.company_code,
            CompanyInfo.company_name,
            CompanyInfo.company_logo
        ).filter(
            *company_conditions
        ).order_by(
            AppAccessInfo.create_time.desc()
        )
        total = target_access_users.count()
        data = target_access_users.paginate(page=page_num, per_page=page_size, error_out=False)
        result = {
            "total": total,
            "page_num": page_num,
            "page_size": page_size,
            "data": []
        }
        for access_info, company_id, company_code, company_name, company_logo in data:
            result["data"].append({
                "id": access_info.id,
                "company_id": company_id,
                "company_code": company_code,
                "company_name": company_name,
                "company_logo": company_logo,
                "access_type": access_info.access_type,
                "access_name": access_info.access_name,
                "access_status": access_info.access_status,
                "create_time": access_info.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                "update_time": access_info.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return next_console_response(result=result)
    else:
        return next_console_response(error_status=True, error_message="不支持的授权对象")


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


def get_app_running_status(params):
    """
    获取应用运行状态
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    index_type = params.get("index_type")
    time_range = params.get("time_range", 60 * 24)
    # 检查权限
    app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '生产'
    ).first()
    if not app_info:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and app_info.user_id != user_id:
        return next_console_response(error_status=True, error_message="没有权限查看该应用！", error_code=1002)
    start_time = datetime.now(timezone.utc) - timedelta(minutes=time_range)
    if index_type == 'user_count':
        # 获取用户数
        user_count = NextConsoleSession.query.filter(
            NextConsoleSession.session_source == app_code,
            NextConsoleSession.create_time >= start_time,
            NextConsoleSession.session_status != "测试"
        ).with_entities(
            NextConsoleSession.user_id
        ).distinct().count()
        return next_console_response(result={
            "data": user_count
        })
    elif index_type == 'session_count':
        # 获取会话数
        session_count = NextConsoleSession.query.filter(
            NextConsoleSession.session_source == app_code,
            NextConsoleSession.create_time >= start_time,
            NextConsoleSession.session_status != "测试"
        ).count()
        return next_console_response(result={
            "data": session_count
        })
    elif index_type == 'qa_count':
        # 获取问答数
        qa_count = NextConsoleSession.query.filter(
            NextConsoleSession.session_source == app_code,
            NextConsoleSession.create_time >= start_time,
            NextConsoleSession.session_status != "测试"
        ).join(
            NextConsoleQa,
            NextConsoleQa.session_id == NextConsoleSession.id
        ).count()
        return next_console_response(result={
            "data": qa_count
        })
    elif index_type == 'attachment_count':
        # 获取问答数
        attachment_count = NextConsoleSession.query.filter(
            NextConsoleSession.session_source == app_code,
            NextConsoleSession.create_time >= start_time,
            NextConsoleSession.session_status != "测试"
        ).join(
            SessionAttachmentRelation,
            SessionAttachmentRelation.session_id == NextConsoleSession.id
        ).count()
        return next_console_response(result={
            "data": attachment_count
        })
    else:
        return next_console_response(error_status=True, error_message="不支持的指标类型！", error_code=1002)


def export_app_schema(params):
    """
    导出指定版本的应用schema
        返回json数据
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    app_code = params.get("app_code")
    publish_id = params.get("publish_id")
    # 检查权限
    app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '生产'
    ).first()
    if not app_info:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and app_info.user_id != user_id:
        return next_console_response(error_status=True, error_message="没有权限查看该应用！", error_code=1002)
    target_publish_record = AppPublishRecord.query.filter(
        AppPublishRecord.app_code == app_code,
        AppPublishRecord.publish_status == '成功',
        AppPublishRecord.id == publish_id
    ).first()
    if not target_publish_record:
        return next_console_response(error_status=True, error_message="应用发布记录不存在！", error_code=1002)
    # 获取应用schema
    target_app_meta = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.environment == '生产',
        AppMetaInfo.version == target_publish_record.publish_version
    ).first()
    if not target_app_meta:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    target_workflows = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.app_code == app_code,
        AppWorkFlowRelation.environment == '生产'
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        WorkFlowMetaInfo.version == target_publish_record.publish_version,
        WorkFlowMetaInfo.environment == '生产'
    ).with_entities(
        WorkFlowMetaInfo
    ).all()
    if not target_workflows:
        return next_console_response(error_status=True, error_message="应用工作流不存在！", error_code=1002)
    target_workflow_nodes = WorkflowNodeInfo.query.filter(
        WorkflowNodeInfo.workflow_id.in_([workflow.id for workflow in target_workflows]),
        WorkflowNodeInfo.node_status == '正常',
        WorkflowNodeInfo.environment == '生产',
        WorkflowNodeInfo.version == target_publish_record.publish_version
    ).all()
    result = {
        "app": target_app_meta.to_dict(),
        "workflows": [workflow.to_dict() for workflow in target_workflows],
        "workflow_nodes": [workflow_node.to_dict() for workflow_node in target_workflow_nodes],
        "meta": {
            "version": target_publish_record.publish_version,
            "publish_code": target_publish_record.publish_code,
            "publish_name": target_publish_record.publish_name,
            "publish_desc": target_publish_record.publish_desc,
            "publish_config": target_publish_record.publish_config,
            "publish_status": target_publish_record.publish_status,
            "export_time": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
        }
    }
    return next_console_response(result=result)


def upload_app_schema(user_id, data):
    app_schema_path = generate_new_path(
        "app_center", user_id=user_id, file_type="file", suffix="json"
                                    ).json.get("result")
    data.save(app_schema_path)
    app_schema_download_url = generate_download_url(
        "app_center",
        app_schema_path, suffix="json").json.get("result")
    return next_console_response(result={
        "app_schema_url": app_schema_download_url,
    })


def upload_app_flow_schema(user_id, data):
    """
    上传应用工作流schema
    :param user_id:
    :param data:
    :return:
    """
    app_flow_schema_path = generate_new_path(
        "app_center", user_id=user_id, file_type="file", suffix="json"
    ).json.get("result")
    data.save(app_flow_schema_path)
    app_flow_schema_download_url = generate_download_url(
        "app_center",
        app_flow_schema_path, suffix="json").json.get("result")
    return next_console_response(result={
        "app_flow_schema_url": app_flow_schema_download_url,
    })


def import_workflow_schema(params):
    """
    根据工作流schema创建新工作流
    :param data:
    :return:
    """
    # 检查权限
    user_id = int(params.get("user_id"))
    app_code = params.get("app_code")
    workflow_schema_url = params.get("workflow_schema_url")
    app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '开发'
    ).first()
    if not app_info:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and app_info.user_id != user_id:
        return next_console_response(error_status=True, error_message="没有权限查看该应用！", error_code=1002)
    # 获取schema数据
    workflow_schema_path = get_download_url_path(workflow_schema_url)
    if not workflow_schema_path:
        return next_console_response(error_status=True, error_message="工作流schema文件不存在！", error_code=1002)
    with open(workflow_schema_path, 'r', encoding='utf-8') as f:
        try:
            workflow_schema = json.load(f)
        except json.JSONDecodeError:
            return next_console_response(error_status=True, error_message="工作流schema文件格式错误！", error_code=1002)
        # 创建工作流
    workflows = workflow_schema.get("workflows")
    workflow_nodes = workflow_schema.get("workflow_nodes")
    workflow_id_maps = {}
    new_workflows = []
    for workflow in workflows:
        workflow_code = workflow.get("workflow_code")
        if not workflow_code:
            return next_console_response(error_status=True, error_message="应用schema文件格式错误！",
                                         error_code=1002)
        exist_workflow = WorkFlowMetaInfo.query.filter(
            WorkFlowMetaInfo.workflow_code == workflow_code,
            WorkFlowMetaInfo.workflow_status != '删除'
        ).first()
        if exist_workflow:
            workflow_code = str(uuid.uuid4())
        new_workflow = WorkFlowMetaInfo(
            user_id=user_id,
            workflow_code=workflow_code,
            workflow_name=workflow.get("workflow_name"),
            workflow_desc=workflow.get("workflow_desc"),
            workflow_icon=workflow.get("workflow_icon"),
            workflow_schema=workflow.get("workflow_schema"),
            workflow_edit_schema=workflow.get("workflow_edit_schema"),
            workflow_is_main=workflow.get("workflow_is_main"),
            workflow_status="正常",
            environment="开发"
        )
        db.session.add(new_workflow)
        db.session.flush()
        new_workflows.append(new_workflow)
        workflow_id_maps[workflow.get("id")] = new_workflow
        db.session.commit()
        new_rel = AppWorkFlowRelation(
            app_code=app_info.app_code,
            workflow_code=new_workflow.workflow_code,
            rel_type="使用",
            environment="开发",
        )
        db.session.add(new_rel)
        db.session.commit()
    node_code_maps = {}

    new_workflow_nodes = []
    for workflow_node in workflow_nodes:
        workflow_item = workflow_id_maps.get(workflow_node.get("workflow_id"))
        old_node_code = workflow_node.get("node_code")
        new_node_code = str(uuid.uuid4())
        # 替换工作流节点中的schema
        old_workflow_schema = json.dumps(workflow_item.workflow_schema)
        old_workflow_edit_schema = json.dumps(workflow_item.workflow_edit_schema)
        new_workflow_schema = json.loads(old_workflow_schema.replace(old_node_code, new_node_code))
        new_workflow_edit_schema = json.loads(old_workflow_edit_schema.replace(old_node_code, new_node_code))
        workflow_item.workflow_schema = new_workflow_schema
        workflow_item.workflow_edit_schema = new_workflow_edit_schema
        db.session.add(workflow_item)
        db.session.commit()
        node_code_maps[new_node_code] = old_node_code
        new_workflow_node = WorkflowNodeInfo(
            user_id=user_id,
            workflow_id=workflow_item.id,
            node_code=new_node_code,
            node_type=workflow_node.get("node_type"),
            node_icon=workflow_node.get("node_icon"),
            node_name=workflow_node.get("node_name"),
            node_desc=workflow_node.get("node_desc"),
            node_run_model_config=workflow_node.get("node_run_model_config"),
            node_llm_code='',
            node_llm_params=workflow_node.get("node_llm_params"),
            node_llm_system_prompt_template=workflow_node.get("node_llm_system_prompt_template"),
            node_llm_user_prompt_template=workflow_node.get("node_llm_user_prompt_template"),
            node_result_format=workflow_node.get("node_result_format"),
            node_result_params_json_schema=workflow_node.get("node_result_params_json_schema"),
            node_result_extract_separator=workflow_node.get("node_result_extract_separator"),
            node_result_extract_quote=workflow_node.get("node_result_extract_quote"),
            node_result_extract_columns=workflow_node.get("node_result_extract_columns"),
            node_result_template=workflow_node.get("node_result_template"),
            node_timeout=workflow_node.get("node_timeout"),
            node_retry_max=workflow_node.get("node_retry_max"),
            node_retry_duration=workflow_node.get("node_retry_duration"),
            node_retry_model=workflow_node.get("node_retry_model"),
            node_failed_solution=workflow_node.get("node_failed_solution"),
            node_failed_template=workflow_node.get("node_failed_template"),
            node_session_memory_size=workflow_node.get("node_session_memory_size"),
            node_deep_memory=workflow_node.get("node_deep_memory"),
            node_agent_nickname=workflow_node.get("node_agent_nickname"),
            node_agent_desc=workflow_node.get("node_agent_desc"),
            node_agent_avatar=workflow_node.get("node_agent_avatar"),
            node_agent_prologue=workflow_node.get("node_agent_prologue"),
            node_agent_preset_question=workflow_node.get("node_agent_preset_question"),
            node_agent_tools=workflow_node.get("node_agent_tools"),
            node_input_params_json_schema=workflow_node.get("node_input_params_json_schema"),
            node_status="正常",
            environment="开发",
            version=workflow_node.get("version"),
            node_tool_api_url=workflow_node.get("node_tool_api_url"),
            node_tool_http_method=workflow_node.get("node_tool_http_method"),
            node_tool_http_header=workflow_node.get("node_tool_http_header"),
            node_tool_http_params=workflow_node.get("node_tool_http_params"),
            node_tool_http_body=workflow_node.get("node_tool_http_body"),
            node_tool_http_body_type=workflow_node.get("node_tool_http_body_type"),
            node_rag_resources=workflow_node.get("node_rag_resources"),
            node_rag_ref_show=workflow_node.get("node_rag_ref_show"),
            node_rag_query_template=workflow_node.get("node_rag_query_template"),
            node_rag_recall_config=workflow_node.get("node_rag_recall_config"),
            node_rag_rerank_config=workflow_node.get("node_rag_rerank_config"),
            node_rag_web_search_config=workflow_node.get("node_rag_web_search_config"),
            node_enable_message=workflow_node.get("node_enable_message"),
            node_message_schema_type=workflow_node.get("node_message_schema_type"),
            node_message_schema=workflow_node.get("node_message_schema"),
            node_file_reader_config=workflow_node.get("node_file_reader_config"),
            node_file_splitter_config=workflow_node.get("node_file_splitter_config"),
            node_sub_workflow_config=workflow_node.get("node_sub_workflow_config")
        )
        db.session.add(new_workflow_node)
        new_workflow_nodes.append(new_workflow_node)
        db.session.commit()
    # 处理ref变量
    has_ref_attrs = [
        'node_input_params_json_schema',
        'node_llm_system_prompt_template', 'node_llm_user_prompt_template',
        'node_tool_http_header', 'node_tool_http_params', 'node_tool_http_body',
        'node_rag_query_template',
        'node_result_params_json_schema', 'node_result_template',
        'node_message_schema',
        'node_failed_template',
        'node_llm_params'
    ]
    for new_node in new_workflow_nodes:
        # 针对导入节点的引入ref变量的属性，将ref变量中的旧的node_code替换为新的node_code
        for ref_attr in has_ref_attrs:
            # 将旧的node_code替换为新的node_code
            ref_attr_value = getattr(new_node, ref_attr, None)
            if not ref_attr_value:
                continue
            json_flag = False
            if not isinstance(ref_attr_value, str):
                json_flag = True
                ref_attr_value = json.dumps(ref_attr_value)
            # 遍历旧code 和新code的映射关系,进行替换
            for new_node_code in node_code_maps:
                if node_code_maps[new_node_code] in ref_attr_value:
                    ref_attr_value = ref_attr_value.replace(node_code_maps[new_node_code], new_node_code)
            if json_flag:
                ref_attr_value = json.loads(ref_attr_value)
            setattr(new_node, ref_attr, ref_attr_value)
        db.session.add(new_node)
        db.session.commit()
    # 处理workflow-schema
    has_ref_attrs = [
        "workflow_edit_schema", "workflow_schema"
    ]
    for workflow in new_workflows:
        for ref_attr in has_ref_attrs:
            ref_attr_value = getattr(workflow, ref_attr, None)
            if not ref_attr_value:
                continue
            json_flag = False
            if not isinstance(ref_attr_value, str):
                json_flag = True
                ref_attr_value = json.dumps(ref_attr_value)
            # 遍历旧code 和新code的映射关系,进行替换
            for new_node_code in node_code_maps:
                if node_code_maps[new_node_code] in ref_attr_value:
                    ref_attr_value = ref_attr_value.replace(node_code_maps[new_node_code], new_node_code)
            if json_flag:
                ref_attr_value = json.loads(ref_attr_value)
            setattr(workflow, ref_attr, ref_attr_value)
        db.session.add(workflow)
        db.session.commit()
    return next_console_response()


def import_app_schema(data):
    """
    根据schema创建新应用
    :param data:
    :return:
    """
    user_id = int(data.get("user_id"))
    app_schema_url = data.get("app_schema_url")
    # 获取schema数据
    app_schema_path = get_download_url_path(app_schema_url)
    if not app_schema_path:
        return next_console_response(error_status=True, error_message="应用schema文件不存在！", error_code=1002)
    with open(app_schema_path, 'r', encoding='utf-8') as f:
        try:
            app_schema = json.load(f)
        except json.JSONDecodeError:
            return next_console_response(error_status=True, error_message="应用schema文件格式错误！", error_code=1002)
    app_meta = app_schema.get("app")
    workflows = app_schema.get("workflows")
    workflow_nodes = app_schema.get("workflow_nodes")
    meta = app_schema.get("meta")
    if not app_meta or not workflows or not meta:
        return next_console_response(error_status=True, error_message="应用schema文件格式错误！", error_code=1002)
    # 创建应用
    app_code = app_meta.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="应用schema文件格式错误！", error_code=1002)
    exist_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '删除'
    ).first()
    if exist_app:
        app_code = str(uuid.uuid4())
    dev_app_info = AppMetaInfo(
        app_code=app_code,
        user_id=user_id,
        app_name=app_meta.get("app_name"),
        app_desc=app_meta.get("app_desc"),
        app_icon=app_meta.get("app_icon"),
        app_type="个人应用",
        app_default_assistant=app_meta.get("app_default_assistant"),
        app_source=app_meta.get("app_source"),
        app_agent_api_url=app_meta.get("app_agent_api_url"),
        app_agent_api_key=app_meta.get("app_agent_api_key"),
        app_config=app_meta.get("app_config", {}),
        app_status="创建中",
        environment="开发",
        version=meta.get("version"),
    )
    db.session.add(dev_app_info)
    db.session.commit()
    # 创建工作流
    workflow_id_maps = {}
    new_workflows = []
    for workflow in workflows:
        workflow_code = workflow.get("workflow_code")
        if not workflow_code:
            return next_console_response(error_status=True, error_message="应用schema文件格式错误！", error_code=1002)
        exist_workflow = WorkFlowMetaInfo.query.filter(
            WorkFlowMetaInfo.workflow_code == workflow_code,
            WorkFlowMetaInfo.workflow_status != '删除'
        ).first()
        if exist_workflow:
            workflow_code = str(uuid.uuid4())
        new_workflow = WorkFlowMetaInfo(
            user_id=user_id,
            workflow_code=workflow_code,
            workflow_name=workflow.get("workflow_name"),
            workflow_desc=workflow.get("workflow_desc"),
            workflow_icon=workflow.get("workflow_icon"),
            workflow_schema=workflow.get("workflow_schema"),
            workflow_edit_schema=workflow.get("workflow_edit_schema"),
            workflow_is_main=workflow.get("workflow_is_main"),
            workflow_status="正常",
            environment="开发",
            version=meta.get("version")
        )
        db.session.add(new_workflow)
        db.session.flush()
        new_workflows.append(new_workflow)
        workflow_id_maps[workflow.get("id")] = new_workflow
        db.session.commit()
        new_rel = AppWorkFlowRelation(
            app_code=dev_app_info.app_code,
            workflow_code=new_workflow.workflow_code,
            rel_type="使用",
            environment="开发",
        )
        db.session.add(new_rel)
        db.session.commit()
    node_code_maps = {}
    new_workflow_nodes = []
    for workflow_node in workflow_nodes:
        workflow_item = workflow_id_maps.get(workflow_node.get("workflow_id"))
        old_node_code = workflow_node.get("node_code")
        new_node_code = str(uuid.uuid4())
        # 替换工作流节点中的schema
        old_workflow_schema = json.dumps(workflow_item.workflow_schema)
        old_workflow_edit_schema = json.dumps(workflow_item.workflow_edit_schema)
        new_workflow_schema = json.loads(old_workflow_schema.replace(old_node_code, new_node_code))
        new_workflow_edit_schema = json.loads(old_workflow_edit_schema.replace(old_node_code, new_node_code))
        workflow_item.workflow_schema = new_workflow_schema
        workflow_item.workflow_edit_schema = new_workflow_edit_schema
        db.session.add(workflow_item)
        db.session.commit()
        node_code_maps[new_node_code] = old_node_code
        new_workflow_node = WorkflowNodeInfo(
            user_id=user_id,
            workflow_id=workflow_item.id,
            node_code=new_node_code,
            node_type=workflow_node.get("node_type"),
            node_icon=workflow_node.get("node_icon"),
            node_name=workflow_node.get("node_name"),
            node_desc=workflow_node.get("node_desc"),
            node_run_model_config=workflow_node.get("node_run_model_config"),
            node_llm_code='',
            node_llm_params=workflow_node.get("node_llm_params"),
            node_llm_system_prompt_template=workflow_node.get("node_llm_system_prompt_template"),
            node_llm_user_prompt_template=workflow_node.get("node_llm_user_prompt_template"),
            node_result_format=workflow_node.get("node_result_format"),
            node_result_params_json_schema=workflow_node.get("node_result_params_json_schema"),
            node_result_extract_separator=workflow_node.get("node_result_extract_separator"),
            node_result_extract_quote=workflow_node.get("node_result_extract_quote"),
            node_result_extract_columns=workflow_node.get("node_result_extract_columns"),
            node_result_template=workflow_node.get("node_result_template"),
            node_timeout=workflow_node.get("node_timeout"),
            node_retry_max=workflow_node.get("node_retry_max"),
            node_retry_duration=workflow_node.get("node_retry_duration"),
            node_retry_model=workflow_node.get("node_retry_model"),
            node_failed_solution=workflow_node.get("node_failed_solution"),
            node_failed_template=workflow_node.get("node_failed_template"),
            node_session_memory_size=workflow_node.get("node_session_memory_size"),
            node_deep_memory=workflow_node.get("node_deep_memory"),
            node_agent_nickname=workflow_node.get("node_agent_nickname"),
            node_agent_desc=workflow_node.get("node_agent_desc"),
            node_agent_avatar=workflow_node.get("node_agent_avatar"),
            node_agent_prologue=workflow_node.get("node_agent_prologue"),
            node_agent_preset_question=workflow_node.get("node_agent_preset_question"),
            node_agent_tools=workflow_node.get("node_agent_tools"),
            node_input_params_json_schema=workflow_node.get("node_input_params_json_schema"),
            node_status="正常",
            environment="开发",
            version=workflow_node.get("version"),
            node_tool_api_url=workflow_node.get("node_tool_api_url"),
            node_tool_http_method=workflow_node.get("node_tool_http_method"),
            node_tool_http_header=workflow_node.get("node_tool_http_header"),
            node_tool_http_params=workflow_node.get("node_tool_http_params"),
            node_tool_http_body=workflow_node.get("node_tool_http_body"),
            node_tool_http_body_type=workflow_node.get("node_tool_http_body_type"),
            node_rag_resources=workflow_node.get("node_rag_resources"),
            node_rag_ref_show=workflow_node.get("node_rag_ref_show"),
            node_rag_query_template=workflow_node.get("node_rag_query_template"),
            node_rag_recall_config=workflow_node.get("node_rag_recall_config"),
            node_rag_rerank_config=workflow_node.get("node_rag_rerank_config"),
            node_rag_web_search_config=workflow_node.get("node_rag_web_search_config"),
            node_enable_message=workflow_node.get("node_enable_message"),
            node_message_schema_type=workflow_node.get("node_message_schema_type"),
            node_message_schema=workflow_node.get("node_message_schema"),
            node_file_reader_config=workflow_node.get("node_file_reader_config"),
            node_file_splitter_config=workflow_node.get("node_file_splitter_config"),
            node_sub_workflow_config=workflow_node.get("node_sub_workflow_config"),
        )
        db.session.add(new_workflow_node)
        new_workflow_nodes.append(new_workflow_node)
        db.session.commit()
    # 处理ref变量
    has_ref_attrs = [
        'node_input_params_json_schema',
        'node_llm_system_prompt_template', 'node_llm_user_prompt_template',
        'node_tool_http_header', 'node_tool_http_params', 'node_tool_http_body',
        'node_rag_query_template',
        'node_result_params_json_schema', 'node_result_template',
        'node_message_schema',
        'node_failed_template',
        'node_llm_params'
    ]
    for new_node in new_workflow_nodes:
        # 针对导入节点的引入ref变量的属性，将ref变量中的旧的node_code替换为新的node_code
        for ref_attr in has_ref_attrs:
            # 将旧的node_code替换为新的node_code
            ref_attr_value = getattr(new_node, ref_attr, None)
            if not ref_attr_value:
                continue
            json_flag = False
            if not isinstance(ref_attr_value, str):
                json_flag = True
                ref_attr_value = json.dumps(ref_attr_value)
            # 遍历旧code 和新code的映射关系,进行替换
            for new_node_code in node_code_maps:
                if node_code_maps[new_node_code] in ref_attr_value:
                    ref_attr_value = ref_attr_value.replace(node_code_maps[new_node_code], new_node_code)
            if json_flag:
                ref_attr_value = json.loads(ref_attr_value)
            setattr(new_node, ref_attr, ref_attr_value)
        db.session.add(new_node)
        db.session.commit()
    # 处理workflow-schema
    has_ref_attrs = [
        "workflow_edit_schema", "workflow_schema"
    ]
    for workflow in new_workflows:
        for ref_attr in has_ref_attrs:
            ref_attr_value = getattr(workflow, ref_attr, None)
            if not ref_attr_value:
                continue
            json_flag = False
            if not isinstance(ref_attr_value, str):
                json_flag = True
                ref_attr_value = json.dumps(ref_attr_value)
            # 遍历旧code 和新code的映射关系,进行替换
            for new_node_code in node_code_maps:
                if node_code_maps[new_node_code] in ref_attr_value:
                    ref_attr_value = ref_attr_value.replace(node_code_maps[new_node_code], new_node_code)
            if json_flag:
                ref_attr_value = json.loads(ref_attr_value)
            setattr(workflow, ref_attr, ref_attr_value)
        db.session.add(workflow)
        db.session.commit()
    return next_console_response()


def delete_app_publish(data):
    """
    删除生产环境的应用发布记录，且删除关联授权，应用，工作流，工作流节点
    :param data:
    :return:
    """
    app_code = data.get("app_code")
    user_id = int(data.get("user_id"))
    prod_app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status == '正常',
        AppMetaInfo.environment == '生产'
    ).first()
    if not prod_app_info:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and prod_app_info.user_id != user_id:
        return next_console_response(error_status=True, error_message="没有权限发布该应用！", error_code=1002)
    # 获取应用发布记录
    target_publish_record = AppPublishRecord.query.filter(
        AppPublishRecord.app_code == app_code,
        AppPublishRecord.publish_status == '成功'
    ).order_by(
        AppPublishRecord.id.desc()
    ).first()
    # 获取应用工作流
    app_workflows = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.app_code == app_code,
        AppWorkFlowRelation.environment == '生产'
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        WorkFlowMetaInfo.version == target_publish_record.publish_version,
        WorkFlowMetaInfo.environment == '生产'
    ).with_entities(
        WorkFlowMetaInfo
    ).all()
    # 获取工作流节点
    workflow_nodes = WorkflowNodeInfo.query.filter(
        WorkflowNodeInfo.workflow_id.in_([workflow.id for workflow in app_workflows]),
        WorkflowNodeInfo.node_status == '正常',
        WorkflowNodeInfo.environment == '生产',
        WorkflowNodeInfo.version == target_publish_record.publish_version
    ).all()
    all_user_access = AppAccessInfo.query.filter(
        AppAccessInfo.app_code == app_code,
        AppAccessInfo.access_status == '正常'
    ).all()
    # 删除应用
    prod_app_info.app_status = '已删除'
    db.session.add(prod_app_info)
    db.session.commit()
    # 删除应用工作流
    for app_workflow in app_workflows:
        app_workflow.workflow_status = '删除'
        db.session.add(app_workflow)
        db.session.commit()
    # 删除工作流节点
    for workflow_node in workflow_nodes:
        workflow_node.node_status = '删除'
        db.session.add(workflow_node)
        db.session.commit()
    # 删除应用发布记录
    target_publish_record.publish_status = '已删除'
    db.session.add(target_publish_record)
    db.session.commit()
    # 删除应用授权
    for access_info in all_user_access:
        access_info.access_status = '已删除'
        db.session.add(access_info)
        db.session.commit()
    return next_console_response(result={"message": "应用发布记录删除成功！"})

