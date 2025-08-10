from sqlalchemy import or_
from app.services.next_console.base import *
from app.models.app_center.app_info_model import *
from app.models.user_center.user_info import UserInfo
from app.utils.oss.oss_client import *
from app.models.contacts.department_model import DepartmentInfo
from app.models.contacts.company_model import CompanyInfo


def search_all_apps(params):
    """
    搜索所有可见应用列表
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    app_keyword = params.get("app_keyword")
    app_type = params.get("app_type", [])
    page_size = params.get("page_size", 20)
    page_num = params.get("page_num", 1)
    environment = "生产"
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1002)
    all_condition = [
        AppMetaInfo.app_status == '正常',
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
    # 找到所有父部门id
    department_id_list = []
    if target_user.user_department_id:
        target_department_id = target_user.user_department_id
        while target_department_id:
            department_id_list.append(target_department_id)
            target_department = DepartmentInfo.query.filter(
                DepartmentInfo.id == target_department_id
            ).first()
            if target_department:
                target_department_id = target_department.parent_department_id
            else:
                break
    # 找到所有父公司id
    company_id_list = []
    if target_user.user_company_id:
        target_company_id = target_user.user_company_id
        while target_company_id:
            company_id_list.append(target_company_id)
            target_company = CompanyInfo.query.filter(
                CompanyInfo.id == target_company_id
            ).first()
            if target_company:
                target_company_id = target_company.parent_company_id
            else:
                break
    target_apps = AppAccessInfo.query.filter(
        or_(
            AppAccessInfo.user_id == target_user.user_id,
            AppAccessInfo.user_id == -1,
            AppAccessInfo.user_code == target_user.user_code,
            AppAccessInfo.department_id.in_(department_id_list),
            AppAccessInfo.company_id.in_(company_id_list),
        ),
        AppAccessInfo.access_status == '正常',
    ).join(
        AppMetaInfo,
        AppMetaInfo.app_code == AppAccessInfo.app_code
    ).filter(
        *all_condition
    ).join(
        UserInfo,
        UserInfo.user_id == AppMetaInfo.user_id
    ).with_entities(
        AppMetaInfo,
        UserInfo.user_nick_name,
        UserInfo.user_avatar
    ).order_by(
        AppMetaInfo.create_time.desc()
    )
    total = target_apps.count()
    all_data = target_apps.all()
    data = []
    for item in all_data:
        data.append({
            "app_code": item.AppMetaInfo.app_code,
            "app_name": item.AppMetaInfo.app_name,
            "app_desc": item.AppMetaInfo.app_desc,
            "app_icon": item.AppMetaInfo.app_icon,
            "app_type": item.AppMetaInfo.app_type,
            "app_status": item.AppMetaInfo.app_status,
            "create_time": item.AppMetaInfo.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": item.AppMetaInfo.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "user_nick_name": item.user_nick_name,
            "user_avatar": item.user_avatar
        })
    result = {
        "total": total,
        "page_num": page_num,
        "page_size": page_size,
        "data": data
    }
    return next_console_response(result=result)


def get_app_detail(params):
    """
    获取应用详情,包括元数据，工作流列表，插件列表，数据列表，应用变量列表
        agent_code: '1',
        agent_name: 'agent1',
        agent_type: 'assistant',
        agent_icon: 'images/assistant.svg',
        id: 1
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '生产'
    ).first()
    if not app_info:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    # 获取agent 列表
    all_workflows = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.app_code == app_code,
        AppWorkFlowRelation.rel_status == '正常',
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        WorkFlowMetaInfo.workflow_status == '正常',
        WorkFlowMetaInfo.environment == '生产'
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
        })
    result = {
        "meta": app_info.to_dict(),
        "flows": all_agents,
    }
    return next_console_response(result=result)
