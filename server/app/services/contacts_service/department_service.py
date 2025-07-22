from app.models.contacts.department_model import *
from app.models.user_center.user_info import *
from app.services.configure_center.response_utils import *
from sqlalchemy import or_


def get_department_list_info(params):
    """
    获取部门信息
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    parent_department_id = params.get('parent_department_id')
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

    if not parent_department_id:
        parent_department = DepartmentInfo.query.filter(
            DepartmentInfo.company_id == target_user.user_company_id,
            DepartmentInfo.parent_department_id.is_(None),
        ).first()
        if not parent_department:
            return next_console_response(error_message='公司未设置部门')
        parent_department_id = parent_department.id
    target_departments = DepartmentInfo.query.filter(
        DepartmentInfo.company_id == target_user.user_company_id,
        DepartmentInfo.parent_department_id == parent_department_id,
        DepartmentInfo.department_status == '正常'
    ).all()
    department_list = [department.to_dict() for department in target_departments]
    return next_console_response(result=department_list)


def get_department_detail(params):
    """
    获取部门详情
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    department_id = params.get('department_id')
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
    target_department = DepartmentInfo.query.filter(
        DepartmentInfo.id == department_id,
        DepartmentInfo.company_id == target_user.user_company_id,
        DepartmentInfo.department_status == '正常'
    ).first()
    if not target_department:
        return next_console_response(error_message='部门不存在')
    department_info = target_department.to_dict()
    user_cnt = UserInfo.query.filter(
        UserInfo.user_department_id == target_department.id,
        UserInfo.user_status == 1
    ).count()
    department_info['user_count'] = user_cnt
    return next_console_response(result=department_info)


def search_department_detail(params):
    """
    根据关键词搜索部门信息，子部门不显示
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    keyword = params.get('keyword')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message='用户不存在')
    if target_user.user_account_type != '企业账号':
        return next_console_response(error_message='用户未认证')
    if not target_user.user_company_id:
        return next_console_response(error_message='用户未加入公司')
    target_department = DepartmentInfo.query.filter(
        DepartmentInfo.company_id == target_user.user_company_id,
        or_(
            DepartmentInfo.department_name.like('%{}%'.format(keyword)),
            DepartmentInfo.department_code.like('%{}%'.format(keyword)),
            DepartmentInfo.department_desc.like('%{}%'.format(keyword))
        ),
        DepartmentInfo.department_status == '正常',
        DepartmentInfo.parent_department_id.isnot(None)
    ).all()
    department_list = [department.to_dict() for department in target_department]
    all_return_id = [department.id for department in target_department]
    # 检查返回结果中是否有子部门关系,有则去除子部门
    all_department = DepartmentInfo.query.filter(
        DepartmentInfo.company_id == target_user.user_company_id,
        DepartmentInfo.department_status == '正常',
        DepartmentInfo.parent_department_id.isnot(None)
    ).all()
    all_department_rel = {
        department.id: department.parent_department_id for department in all_department
    }
    hide_department_id = []
    for department in target_department:
        has_parent = False
        check_list = [department.id]
        while check_list:
            check_id = check_list.pop()
            parent_id = all_department_rel.get(check_id)
            if parent_id:
                if parent_id in all_return_id:
                    has_parent = True
                    break
                check_list.append(parent_id)
        if has_parent:
            hide_department_id.append(department.id)
    department_list = [department for department in department_list if department['id'] not in hide_department_id]
    return next_console_response(result=department_list)

