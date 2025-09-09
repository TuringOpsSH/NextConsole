from app.models.user_center.user_info import *
from app.models.app_center.app_info_model import *
from app.services.configure_center.response_utils import next_console_response
from app.models.next_console.next_console_model import *
from app.services.next_console.base import *
from app.app import app
from flask import request, current_app
from werkzeug.exceptions import NotFound
from app.models.contacts.department_model import DepartmentInfo
from app.models.contacts.company_model import CompanyInfo
GLOBAL_APP_blueprints = {}


def check_user_access(target_user, app_code):
    """
    检查用户是否有权限访问应用
    """
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
    target_access = AppAccessInfo.query.filter(
        AppAccessInfo.app_code == app_code,
        AppAccessInfo.access_status == "正常",
        or_(
            AppAccessInfo.user_code == target_user.user_code,
            AppAccessInfo.user_id == target_user.user_id,
            AppAccessInfo.user_id == -1,
            AppAccessInfo.department_id.in_(department_id_list),
            AppAccessInfo.company_id.in_(company_id_list),
        ),
    ).first()
    if not target_access:
        return False
    return True


def get_app_detail_service(params):
    """
    获取应用详情
    """
    user_id = int(params.get("user_id"))
    app_code = params.get("app_code")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1002)
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '生产'
    ).order_by(
        AppMetaInfo.id.desc()
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if target_app.app_status not in ("正常", "已发布"):
        return next_console_response(error_status=True, error_message="应用状态不正确！", error_code=1002)
    if not check_user_access(target_user, app_code):
        return next_console_response(error_status=True, error_message="用户无权访问！", error_code=1002)
    result = target_app.to_dict()
    if target_app.app_default_assistant:
        target_assistant = Assistant.query.filter(
            Assistant.id == target_app.app_default_assistant
        ).first()
    else:
        target_assistant = Assistant.query.filter(
            Assistant.id == -12345
        ).first()
    result["assistant_prologue"] = target_assistant.assistant_prologue
    result["assistant_preset_question"] = target_assistant.assistant_preset_question or []
    result['assistant_avatar'] = target_assistant.assistant_avatar or '/images/logo.svg'
    return next_console_response(result=result)


def router_app_messages(params):
    """
    新增应用消息,
        首先检查用户权限，应用权限，
        其次转发到对应项目蓝图中进行处理
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1002)
    session_id = params.get("session_id")
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id,
        NextConsoleSession.user_id == user_id
    ).first()
    if not target_session:
        return next_console_response(error_status=True, error_message="会话不存在！", error_code=1002)
    app_code = target_session.session_source
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status == "正常"
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_user_access(target_user, target_app.app_code):
        return next_console_response(error_status=True, error_message="用户无权访问！", error_code=1002)
    # 进行消息转发
    redirect_url = f"/next_console/app_center/{app_code}/messages/add"
    # 查找目标视图函数
    adapter = current_app.url_map.bind('')
    try:
        endpoint, args = adapter.match(redirect_url, method=request.method)
    except NotFound:
        return next_console_response(error_status=True, error_message="目标路由不存在", error_code=404)

    # 获取目标视图函数
    view_func = current_app.view_functions[endpoint]

    # 构造模拟请求参数
    request_args = {
        "path": request.path,
        "method": request.method,
        "headers": dict(request.headers),  # 转换为可修改的字典
        "query_string": request.query_string,
        "data": request.get_data(),  # 统一通过 data 传递请求体
    }
    request_args["headers"].pop("Content-Length", None)




