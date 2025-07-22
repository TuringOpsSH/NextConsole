from app.models.contacts.company_model import *
from app.models.contacts.department_model import *
from app.models.user_center.user_info import *
from app.models.user_center.user_role_info import UserRoleInfo
from app.models.user_center.role_info import RoleInfo
from app.services.configure_center.response_utils import *
from sqlalchemy import or_


def get_colleague_list(params):
    """
    获取同事列表
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    department_id = params.get('department_id')
    is_root = params.get('is_root', False)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1001, error_message='用户不存在')
    if target_user.user_account_type != '企业账号':
        return next_console_response(error_message='用户未认证')
    if not target_user.user_company_id:
        return next_console_response(error_message='用户未加入公司')
    target_company = CompanyInfo.query.filter(
        CompanyInfo.id == target_user.user_company_id,
        CompanyInfo.company_status == '正常'
    ).first()
    if not target_company:
        return next_console_response(error_message='公司不存在')
    if is_root:
        root_department = DepartmentInfo.query.filter(
            DepartmentInfo.company_id == target_user.user_company_id,
            DepartmentInfo.parent_department_id.is_(None),
            DepartmentInfo.department_status == '正常'
        ).first()
        if not root_department:
            return next_console_response(error_message='公司未设置部门')
        department_id = root_department.id
    target_department = DepartmentInfo.query.filter(
        DepartmentInfo.id == department_id,
        DepartmentInfo.company_id == target_user.user_company_id,
        DepartmentInfo.department_status == '正常'
    ).first()
    if not target_department:
        return next_console_response(error_status=True, error_message='部门不存在')
    colleague_list = UserInfo.query.filter(
        UserInfo.user_department_id == target_department.id,
        UserInfo.user_status == 1
    ).all()
    colleague_info_list = []
    for colleague in colleague_list:
        colleague_info = colleague.show_info()
        colleague_info['user_company'] = target_company.company_name
        colleague_info['user_company_id'] = target_company.id
        colleague_info['user_department'] = target_department.department_name
        colleague_info['user_department_id'] = target_department.id
        colleague_info_list.append(colleague_info)
    # 补充角色信息
    role_res = {}
    if colleague_list:
        role_info = UserInfo.query.filter(
            UserInfo.user_department_id == target_department.id,
            UserInfo.user_status == 1
        ).join(
            UserRoleInfo,
            UserRoleInfo.user_id == UserInfo.user_id,
        ).filter(
            UserRoleInfo.rel_status == 1
        ).with_entities(
            UserInfo.user_id,
            UserRoleInfo.role_id
        ).join(
            RoleInfo,
            RoleInfo.role_id == UserRoleInfo.role_id
        ).filter(
            RoleInfo.status == 1,
            RoleInfo.role_name.in_(['admin', "super_admin"])
        ).with_entities(
            UserInfo.user_id,
            RoleInfo.role_name,
            RoleInfo.role_desc
        ).all()
        for user_id, role_name, role_desc in role_info:
            if user_id not in role_res:
                role_res[user_id] = [{
                    "role_name": role_name,
                    "role_desc": role_desc
                }]
            else:
                role_res[user_id].append(
                    {
                        "role_name": role_name,
                        "role_desc": role_desc
                    }
                )
        for colleague in colleague_info_list:
            colleague["roles"] = role_res.get(colleague["user_id"], [])
    return next_console_response(result=colleague_info_list)


def search_colleague_service(params):
    """
    获取同事列表
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    if target_user.user_account_type != '企业账号':
        return next_console_response(error_message='用户未认证')
    if not target_user.user_company_id:
        return next_console_response(error_message='用户未加入公司')
    target_company = CompanyInfo.query.filter(
        CompanyInfo.id == target_user.user_company_id,
        CompanyInfo.company_status == '正常'
    ).first()
    if not target_company:
        return next_console_response(error_message='公司不存在')
    keyword = params.get('keyword')
    colleague_list = UserInfo.query.filter(
        UserInfo.user_company_id == target_user.user_company_id,
        or_(
            UserInfo.user_nick_name.like('%' + keyword + '%'),
            UserInfo.user_email.like('%' + keyword + '%'),
            UserInfo.user_name.like('%' + keyword + '%')
        ),
        UserInfo.user_status == 1
    ).all()
    colleague_info_list = []
    for colleague in colleague_list:
        colleague_info = colleague.show_info()
        colleague_info['user_company'] = target_company.company_name
        colleague_info_list.append(colleague_info)
    return next_console_response(result=colleague_info_list)
