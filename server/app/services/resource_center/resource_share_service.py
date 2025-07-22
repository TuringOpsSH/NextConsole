import time
from sqlalchemy import or_, distinct
from app.models.resource_center.share_resource_model import *
from app.models.user_center.user_info import UserInfo
from app.models.contacts.company_model import *
from app.models.contacts.department_model import *
from pathlib import Path
from app.models.knowledge_center.rag_ref_model import *
from app.app import app
from app.services.user_center.users import validate_user
from app.services.resource_center.resource import *
from app.services.knowledge_center.rag_service_v3 import rag_query_v3
# 共享资源访问权限值
# - 阅读（只读）
#     - 可以在线查看文件夹，预览文件，评论文件
# - 下载（包含阅读）
#     - 可以下载文件 / 文件夹
#     - 可以将单个文件转存至我的资源
# - 编辑（包含下载）
#     - 可以在线编辑文件 / 文件夹信息
#     - 可以在线编辑文件
#     - 可以新建文件 / 文件夹
#     - 可以上传文件 / 文件夹
#     - 可以移动文件 / 文件夹
#     - 可以分享文件 / 文件夹，但分享权限为只读，不能管理
# - 管理（包含编辑）
#     - 可以分享文件 / 文件夹，同时可以管理分享权限（分享管理）
#     - 可以删除文件 / 文件夹
access_value_map = {
        '无权访问': 0,
        'read': 1,
        'download': 2,
        'edit': 3,
        'manage': 4,
}


def get_share_resource_access_list(params):
    """
    获取目标共享资源的访问列表，包括非本身设定的访问列表，
    来源为真实的设置操作
    access { id, type, auth_type, meta}
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_id = params.get('resource_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == '正常',
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    # 所有上级资源文件夹
    all_parent_resources = get_all_parent_resources(target_resource)
    all_resource_id = [resource.id for resource in all_parent_resources]
    all_resource_id.append(resource_id)
    access_list = []
    # 关联公司权限取最高
    access_list.extend(get_resources_company_access(all_resource_id))
    # 关联部门权限取最高
    access_list.extend(get_resources_department_access(all_resource_id))
    # 关联同事权限取最高
    access_list.extend(get_resources_colleague_access(all_resource_id))
    # 关联好友权限取最高
    access_list.extend(get_resources_friend_access(all_resource_id))
    # 全部好友公开
    if target_resource.resource_is_public:
        access_list.append({
            'type': 'friend',
            'auth_type': target_resource.resource_public_access,
            'id': None,
        })
    # 公开访问权限
    access_list.extend(get_resources_open_access(all_resource_id))
    return next_console_response(result={
        'access_list': access_list,
        'resource_id': resource_id,
    })


def get_all_parent_resources(target_resource):
    """
    获取资源的所有上级分享资源
    :param target_resource:
    :return:
    """
    all_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.resource_status == '正常',
        ResourceObjectMeta.resource_type == 'folder',
        ResourceObjectMeta.user_id == target_resource.user_id,
        ResourceObjectMeta.id != target_resource.id,
        ResourceObjectMeta.resource_source == "resource_center"

    ).all()
    if not all_resources:
        return []

    all_parent_resources = []
    all_parent_id = target_resource.resource_parent_id
    if not all_parent_id:
        return all_parent_resources
    add_cnt = 1
    while add_cnt > 0:
        add_cnt = 0
        # 找到上级资源，并推送到all_parent_resources
        for resource in all_resources:
            if resource.id == all_parent_id:
                all_parent_resources.append(resource)
                if resource.resource_parent_id:
                    all_parent_id = resource.resource_parent_id
                    add_cnt += 1
                    break
    return all_parent_resources


def get_resources_company_access(resource_list):
    """
    获取资源的公司访问权限
    :param resource_list:
    :return:
    """
    company_list = ShareResourceAuthorizeCompanyInfo.query.filter(
        ShareResourceAuthorizeCompanyInfo.resource_id.in_(resource_list),
        ShareResourceAuthorizeCompanyInfo.auth_status == '正常',
    ).join(
        CompanyInfo,
        ShareResourceAuthorizeCompanyInfo.company_id == CompanyInfo.id
    ).with_entities(
        ShareResourceAuthorizeCompanyInfo.resource_id,
        CompanyInfo,
        ShareResourceAuthorizeCompanyInfo.auth_type.label('auth_type'),
    ).all()
    # 当不同资源的公司授权类型不同时，以最大权限为准
    company_access_map = {}
    for resource_id, company, auth_type in company_list:
        if company.id not in company_access_map:
            company_access_map[company.id] = auth_type
        else:
            if access_value_map[auth_type] > access_value_map[company_access_map[company.id]]:
                company_access_map[company.id] = auth_type
    access_list = []
    for resource_id, company, auth_type in company_list:
        access_list.append({
            'type': 'company',
            'id': company.id,
            'auth_type': company_access_map[company.id],
            'meta': company.to_dict(),
            'resource_id': resource_id,
        })
    return access_list


def get_resources_department_access(resource_list):
    """
    获取资源的部门访问权限
    :param resource_list:
    :return:
    """
    department_list = ShareResourceAuthorizeDepartmentInfo.query.filter(
        ShareResourceAuthorizeDepartmentInfo.resource_id.in_(resource_list),
        ShareResourceAuthorizeDepartmentInfo.auth_status == '正常',
    ).join(
        DepartmentInfo,
        ShareResourceAuthorizeDepartmentInfo.department_id == DepartmentInfo.id
    ).with_entities(
        ShareResourceAuthorizeDepartmentInfo.resource_id,
        DepartmentInfo,
        ShareResourceAuthorizeDepartmentInfo.auth_type.label('auth_type'),
    ).all()
    # 当不同资源的公司授权类型不同时，以最大权限为准
    department_access_map = {}
    for resource_id, department, auth_type in department_list:
        if department.id not in department_access_map:
            department_access_map[department.id] = auth_type
        else:
            if access_value_map[auth_type] > access_value_map[department_access_map[department.id]]:
                department_access_map[department.id] = auth_type
    access_list = []
    for resource_id, department, auth_type in department_list:
        access_list.append({
            'type': 'department',
            'id': department.id,
            'auth_type': department_access_map[department.id],
            'meta': department.to_dict(),
            'resource_id': resource_id,
        })
    return access_list


def get_resources_colleague_access(resource_list):
    """
    获取资源的同事访问权限
    :param resource_list:
    :return:
    """
    colleague_list = ShareResourceAuthorizeColleagueInfo.query.filter(
        ShareResourceAuthorizeColleagueInfo.resource_id.in_(resource_list),
        ShareResourceAuthorizeColleagueInfo.auth_status == '正常',
    ).join(
        UserInfo,
        ShareResourceAuthorizeColleagueInfo.auth_user_id == UserInfo.user_id
    ).with_entities(
        ShareResourceAuthorizeColleagueInfo.resource_id,
        UserInfo,
        ShareResourceAuthorizeColleagueInfo.auth_type.label('auth_type'),
    ).all()
    # 当不同资源的公司授权类型不同时，以最大权限为准
    colleague_access_map = {}
    for resource_id, colleague, auth_type in colleague_list:
        if colleague.user_id not in colleague_access_map:
            colleague_access_map[colleague.user_id] = auth_type
        else:
            if access_value_map[auth_type] > access_value_map[colleague_access_map[colleague.user_id]]:
                colleague_access_map[colleague.user_id] = auth_type
    access_list = []
    for resource_id, colleague, auth_type in colleague_list:
        access_list.append({
            'type': 'colleague',
            'id': colleague.user_id,
            'auth_type': colleague_access_map[colleague.user_id],
            'meta': colleague.show_info(),
            'resource_id': resource_id,
        })
    return access_list


def get_resources_friend_access(resource_list):
    """
    获取资源的好友访问权限
    :param resource_list:
    :return:
    """
    friend_list = ShareResourceAuthorizeFriendInfo.query.filter(
        ShareResourceAuthorizeFriendInfo.resource_id.in_(resource_list),
        ShareResourceAuthorizeFriendInfo.auth_status == '正常',
    ).join(
        UserInfo,
        ShareResourceAuthorizeFriendInfo.auth_user_id == UserInfo.user_id
    ).with_entities(
        ShareResourceAuthorizeFriendInfo.resource_id,
        UserInfo,
        ShareResourceAuthorizeFriendInfo.auth_type.label('auth_type'),
    ).all()
    # 当不同资源的公司授权类型不同时，以最大权限为准
    friend_access_map = {}
    for resource_id, friend, auth_type in friend_list:
        if friend.user_id not in friend_access_map:
            friend_access_map[friend.user_id] = auth_type
        else:
            if access_value_map[auth_type] > access_value_map[friend_access_map[friend.user_id]]:
                friend_access_map[friend.user_id] = auth_type
    access_list = []
    for resource_id, friend, auth_type in friend_list:
        access_list.append({
            'type': 'friend',
            'id': friend.user_id,
            'auth_type': friend_access_map[friend.user_id],
            'meta': friend.show_info(),
            'resource_id': resource_id,
        })
    return access_list


def get_resources_open_access(resource_list):
    """
    获取资源的公开访问权限
    :param resource_list:
    :return:
    """
    open_access_list = []
    target_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(resource_list),
        ResourceObjectMeta.resource_status == '正常',
        ResourceObjectMeta.resource_is_open == True,
    ).all()
    for resource in target_resources:
        open_access_list.append({
            'type': 'open',
            'auth_type': resource.resource_open_access,
            'id': None,
            'meta': resource.to_dict(),
            'resource_id': resource.id,
        })
    return open_access_list


def update_share_resource_access_list(params):
    """
    更新共享资源访问列表
    :param params:
    :return:
    """

    user_id = int(params.get("user_id"))
    resource_id = params.get('resource_id')
    access_list = params.get('access_list')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == '正常',
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    # 检查资源是否为我的资源根目录
    if not target_resource.resource_parent_id:
        return next_console_response(error_status=True, error_message="不能直接分享根目录！")
    # 检查用户是否有权限去变更资源的访问列表
    manage_access = False
    if check_user_manage_access_to_resource(
            {'user': target_user, 'resource': target_resource, 'access_type': 'manage'}):
        manage_access = True
    if not manage_access:
        return next_console_response(error_status=True, error_message="无权操作！")
    # 无需给资源所有者分享资源
    for access in access_list:
        if access.get('id') == target_resource.user_id:
            return next_console_response(error_status=True, error_message="无需给资源所有者授权资源权限！")
    # 更新资源的访问列表
    target_resource.resource_is_share = True
    db.session.add(target_resource)
    db.session.commit()
    # 分类处理
    all_company_access = [access for access in access_list if access.get('type') == 'company']
    all_update_company_access = update_company_access_list(all_company_access, resource_id, user_id)
    all_department_access = [access for access in access_list if access.get('type') == 'department']
    all_update_department_access = update_department_access_list(all_department_access, resource_id, user_id)
    all_colleague_access = [access for access in access_list if access.get('type') == 'colleague']
    all_update_colleague_access = update_colleague_access_list(all_colleague_access, resource_id, user_id)
    all_friend_access = [access for access in access_list if access.get('type') == 'friend' and access.get('id')]
    all_update_friend_access = update_friend_access_list(all_friend_access, resource_id, user_id)
    # 分享给全部好友
    all_friend_access = [access for access in access_list if access.get('type') == 'friend' and not access.get('id')]
    if all_friend_access:
        if not all_friend_access[0].get('auth_type'):
            target_resource.resource_is_public = False
        target_resource.resource_public_access = all_friend_access[0].get('auth_type')
        db.session.add(target_resource)
        db.session.commit()
    res = []
    # 组装返回结果
    res.extend(all_update_company_access)
    res.extend(all_update_department_access)
    res.extend(all_update_colleague_access)
    res.extend(all_update_friend_access)
    res = [item.to_dict() for item in res]
    if not res:
        target_resource.resource_is_share = False
        db.session.add(target_resource)
        db.session.commit()
    try:
        return next_console_response(result=res)
    except Exception as e:
        return next_console_response(error_status=True, error_message=str(e))


def check_user_manage_access_to_resource(params):
    """
    检查用户是否有权限访问资源
        首先查看资源及其上级资源的管理权限清单
        然后比对用户的公司，部门，自身是否在权限清单中
    :param params:
    :return:
    """
    user = params.get('user')
    resource = params.get('resource')
    access_type = params.get('access_type', 'read')
    # 如果是资源的拥有者，直接返回True
    if user.user_id == resource.user_id:
        return True
    # 获取资源的所有权限
    all_access_list_res = get_share_resource_access_list({
        'user_id': user.user_id,
        'resource_id': resource.id,
    })
    if all_access_list_res.json.get('error_status'):
        return False
    all_access_list = all_access_list_res.json.get('result').get('access_list')
    all_department_list = get_user_department_list(user)
    all_department_ids = [department.id for department in all_department_list]
    target_access_value = access_value_map.get(access_type, -1)
    # 检查用户是否在权限清单中
    for access in all_access_list:
        # print(access)
        if access_value_map.get(access.get('auth_type'), 0) < target_access_value:
            continue
        # 检查好友权限
        if access.get('type') == 'friend' and (
                (access.get('id') and access.get('id') == user.user_id) or not access.get('id')):
            return True
        # 检查同事权限
        if access.get('type') == 'colleague' and access.get('id') and access.get('id') == user.user_id:
            return True
        # 检查部门权限
        if access.get('type') == 'department' and access.get('id') and access.get('id') in all_department_ids:
            return True
        # 检查公司权限
        if access.get('type') == 'company' and access.get('id') and access.get('id') == user.user_company_id:
            return True
        # 检查公开访问权限
        if access.get('type') == 'open':
            return True
    return False


def get_user_department_list(user):
    """
    获取用户所有上级部门
    :param user:
    :return:
    """
    if user.user_account_type != '企业账号':
        return []

    user_department = DepartmentInfo.query.filter(
        DepartmentInfo.id == user.user_department_id,
        DepartmentInfo.department_status == '正常',
    ).first()
    if not user_department:
        return []
    if not user_department.parent_department_id:
        return [user_department]
    all_department_list = [user_department]
    all_parent_department_id = user_department.parent_department_id
    all_department = DepartmentInfo.query.filter(
        DepartmentInfo.company_id == user.user_company_id,
        DepartmentInfo.department_status == '正常',
        DepartmentInfo.parent_department_id.isnot(None),
    ).all()
    add_cnt = 1
    while add_cnt > 0:
        add_cnt = 0
        for department in all_department:
            if department.id == all_parent_department_id:
                all_department_list.append(department)
                if department.parent_department_id:
                    all_parent_department_id = department.parent_department_id
                    add_cnt += 1
                    break

    return all_department_list


def update_company_access_list(all_company_access, resource_id, user_id):
    """
    更新公司访问权限，删除原有的，不存在则新增，存在则更新权限值
    :param all_company_access:
    :param resource_id:
    :param user_id:
    :return:
    """
    all_company_access_id = [access.get('id') for access in all_company_access]
    exist_company_access = ShareResourceAuthorizeCompanyInfo.query.filter(
        ShareResourceAuthorizeCompanyInfo.user_id == user_id,
        ShareResourceAuthorizeCompanyInfo.resource_id == resource_id,
        ShareResourceAuthorizeCompanyInfo.auth_status == '正常',
    ).all()
    exist_company_access_map = {access.company_id: access for access in exist_company_access}
    res = []
    for access in all_company_access:
        # 新增
        if access.get('id') not in exist_company_access_map:
            new_company_access = ShareResourceAuthorizeCompanyInfo(
                resource_id=resource_id,
                user_id=user_id,
                company_id=access.get('id'),
                auth_type=access.get('auth_type'),
                auth_status='正常',
            )
            db.session.add(new_company_access)
            res.append(new_company_access)
        else:
            # 更新
            exist_access = exist_company_access_map[access.get('id')]
            exist_access.auth_type = access.get('auth_type')
            db.session.add(exist_access)
            res.append(exist_access)
    # 删除不存在的
    for access in exist_company_access:
        if access.company_id not in all_company_access_id or not all_company_access_id:
            db.session.delete(access)
    db.session.commit()
    return res


def update_department_access_list(all_department_access, resource_id, user_id):
    """
    更新部门访问权限，不存在则新增，存在则更新权限值
    :param all_department_access:
    :param resource_id:
    :param user_id:
    :return:
    """
    all_department_access_id = [access.get('id') for access in all_department_access]
    exist_department_access = ShareResourceAuthorizeDepartmentInfo.query.filter(
        ShareResourceAuthorizeDepartmentInfo.user_id == user_id,
        ShareResourceAuthorizeDepartmentInfo.resource_id == resource_id,
        ShareResourceAuthorizeDepartmentInfo.auth_status == '正常',
    ).all()
    exist_department_access_map = {access.department_id: access for access in exist_department_access}
    res = []
    for access in all_department_access:
        # 新增
        if access.get('id') not in exist_department_access_map:
            new_department_access = ShareResourceAuthorizeDepartmentInfo(
                resource_id=resource_id,
                user_id=user_id,
                department_id=access.get('id'),
                auth_type=access.get('auth_type'),
                auth_status='正常',
            )
            db.session.add(new_department_access)
            res.append(new_department_access)
        else:
            # 更新
            exist_access = exist_department_access_map[access.get('id')]
            exist_access.auth_type = access.get('auth_type')
            db.session.add(exist_access)
            res.append(exist_access)
    # 删除不存在的
    for access in exist_department_access:
        if access.department_id not in all_department_access_id or not all_department_access_id:
            db.session.delete(access)
    db.session.commit()
    return res


def update_colleague_access_list(all_colleague_access, resource_id, user_id):
    """
    更新同事访问权限，不存在则新增，存在则更新权限值
    :param all_colleague_access:
    :param resource_id:
    :param user_id:
    :return:
    """
    all_colleague_access_id = [access.get('id') for access in all_colleague_access]
    exist_colleague_access = ShareResourceAuthorizeColleagueInfo.query.filter(
        ShareResourceAuthorizeColleagueInfo.user_id == user_id,
        ShareResourceAuthorizeColleagueInfo.resource_id == resource_id,
        ShareResourceAuthorizeColleagueInfo.auth_status == '正常',
    ).all()
    exist_colleague_access_map = {access.auth_user_id: access for access in exist_colleague_access}
    res = []
    for access in all_colleague_access:
        # 新增
        if access.get('id') not in exist_colleague_access_map:
            new_colleague_access = ShareResourceAuthorizeColleagueInfo(
                resource_id=resource_id,
                user_id=user_id,
                auth_user_id=access.get('id'),
                auth_type=access.get('auth_type'),
                auth_status='正常',
            )
            db.session.add(new_colleague_access)
            res.append(new_colleague_access)
        else:
            # 更新
            exist_access = exist_colleague_access_map[access.get('id')]
            exist_access.auth_type = access.get('auth_type')
            db.session.add(exist_access)
            res.append(exist_access)

    for access in exist_colleague_access:
        if access.auth_user_id not in all_colleague_access_id or not all_colleague_access_id:
            db.session.delete(access)
    db.session.commit()
    return res


def update_friend_access_list(all_friend_access, resource_id, user_id):
    """
    更新好友访问权限，不存在则新增，存在则更新权限值
    :param all_friend_access:
    :param resource_id:
    :param user_id:
    :return:
    """
    all_friend_access_id = [access.get('id') for access in all_friend_access]
    exist_friend_access = ShareResourceAuthorizeFriendInfo.query.filter(
        ShareResourceAuthorizeFriendInfo.user_id == user_id,
        ShareResourceAuthorizeFriendInfo.resource_id == resource_id,
        ShareResourceAuthorizeFriendInfo.auth_status == '正常',
    ).all()
    exist_friend_access_map = {access.auth_user_id: access for access in exist_friend_access}
    res = []
    for access in all_friend_access:
        # 新增
        if access.get('id') not in exist_friend_access_map:
            new_friend_access = ShareResourceAuthorizeFriendInfo(
                resource_id=resource_id,
                user_id=user_id,
                auth_user_id=access.get('id'),
                auth_type=access.get('auth_type'),
                auth_status='正常',
            )
            db.session.add(new_friend_access)
            res.append(new_friend_access)
        else:
            # 更新
            exist_access = exist_friend_access_map[access.get('id')]
            exist_access.auth_type = access.get('auth_type')
            db.session.add(exist_access)
            res.append(exist_access)

    for access in exist_friend_access:
        if access.auth_user_id not in all_friend_access_id or not all_friend_access_id:
            db.session.delete(access)
    db.session.commit()
    return res


@validate_user
@validate_resource
def update_open_access_to_resource(params):
    """
    更新资源的公开访问权限
    :param params:
    resource_id: 资源ID
    resource_is_open: 是否公开访问
    resource_open_access: 公开访问权限类型
    :return:
    """
    target_user = params.get('target_user')
    target_resource = params.get('target_resource')
    resource_is_open = params.get('resource_is_open', False)
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    # 检查用户是否有权限去变更资源的访问列表
    manage_access = False
    if check_user_manage_access_to_resource(
            {'user': target_user, 'resource': target_resource, 'access_type': 'manage'}):
        manage_access = True
    if not manage_access:
        return next_console_response(error_status=True, error_message="无权操作！")
    # 更新资源的公开访问权限
    if resource_is_open:
        resource_open_access = params.get('resource_open_access', 'read')
        if resource_open_access not in ['read', 'download']:
            return next_console_response(error_status=True, error_message="公开访问权限类型错误！")
        target_resource.resource_is_open = True
        target_resource.resource_open_access = resource_open_access
    else:
        # 取消公开访问
        target_resource.resource_is_open = False
        target_resource.resource_open_access = ''
    db.session.add(target_resource)
    db.session.commit()
    return next_console_response(result=target_resource.to_dict())


def get_share_resource_list(params):
    """
    获取用户的共享资源列表,公司，部门，同事，好友，自己共享的资源
    所有资源（文件夹，文件） 取最顶层共享资源展示，即向上找到最顶层的共享资源
    添加分页功能
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    parent_resource_id = params.get('resource_parent_id')
    page_num = params.get('page_num', 1)
    page_size = params.get('page_size', 50)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    # 存在目标上级资源
    if parent_resource_id:
        target_parent_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == parent_resource_id,
            ResourceObjectMeta.resource_status == '正常',
            ResourceObjectMeta.resource_source == "resource_center"
        ).first()
        if not target_parent_resource:
            return next_console_response(error_status=True, error_message="资源不存在！")
        # 检查用户是否有权限访问资源
        if not check_user_manage_access_to_resource(
                {'user': target_user,
                 'resource': target_parent_resource,
                 'access_type': 'read'}):
            return next_console_response(error_status=True, error_message="无权操作！")
        # 获取目标资源的所有子资源
        all_child_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.resource_status == '正常',
            ResourceObjectMeta.resource_parent_id == parent_resource_id,
            ResourceObjectMeta.resource_source == "resource_center"
        ).order_by(
            ResourceObjectMeta.resource_type.asc(),
            ResourceObjectMeta.resource_name.asc(),
        )
        total = all_child_resources.count()
        data = []
        all_child_resources = all_child_resources.paginate(page=page_num, per_page=page_size, error_out=False)
        for resource in all_child_resources:
            data.append({
                'resource': resource.show_info(),
                'auth_type': 'read',
            })
        # 作者信息
        all_author_id = [resource.user_id for resource in all_child_resources]
        all_author = UserInfo.query.filter(
            UserInfo.user_id.in_(all_author_id),
            UserInfo.user_status == 1
        ).all()
        author_map = {author.user_id: author.show_info() for author in all_author}
        for resource in data:
            resource['resource']["author_info"] = author_map.get(resource.get("resource").get("user_id"))

        return next_console_response(result={
            'data': data,
            'total': total,
        })
    # 不存在目标上级资源，获取用户的所有共享资源
    res = []
    if target_user.user_account_type == '企业账号':
        # 1. 获取用户的所有公司共享资源
        res.extend(get_all_company_share_resource(target_user))
        # 2. 获取用户的所有部门共享资源
        res.extend(get_all_department_share_resource(target_user))
        # 3. 获取用户的所有同事共享资源
        res.extend(get_all_colleague_share_resource(target_user))
    # 4. 获取用户的所有好友共享资源
    res.extend(get_all_friend_share_resource(target_user))
    # 5. 获取自己共享的资源
    self_share_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == '正常',
        ResourceObjectMeta.resource_is_share == True,
    ).all()
    for resource in self_share_resources:
        res.append({
            'resource': resource,
            'auth_type': 'manage',
        })
    # 6. 取最大权限
    new_res = []
    resource_access_value_map = {}
    for resource in res:
        if resource.get("resource").id not in resource_access_value_map:
            resource_access_value_map[resource.get("resource").id] = access_value_map.get(resource.get("auth_type"), 0)
        else:
            if (access_value_map.get(resource.get("auth_type"), 0) >
                    resource_access_value_map[resource.get("resource").id]):
                resource_access_value_map[resource.get("resource").id] = access_value_map.get(
                    resource.get("auth_type"), 0)
    # 汇总去重
    tmp_add_id = []
    for resource in res:
        if (access_value_map.get(resource.get("auth_type"), 0) == resource_access_value_map[resource.get("resource").id]
                and resource.get("resource").id in resource_access_value_map
                and resource.get("resource").id not in tmp_add_id):
            new_res.append(resource)
            tmp_add_id.append(resource.get("resource").id)
    # 7. 提取最顶层资源: 如果上级资源存在于资源列表中，则去除本资源
    all_path_list = [resource.get("resource").resource_path for resource in new_res]
    new_res2 = []
    for resource in new_res:
        if not resource.get("resource").resource_parent_id:
            new_res2.append(resource)
        else:
            target_path = Path(resource.get("resource").resource_path).resolve()
            has_parent = False
            for check_path in all_path_list:
                if check_path == resource.get("resource").resource_path:
                    continue
                base_path = Path(check_path).resolve()
                if target_path.is_relative_to(base_path):
                    has_parent = True
                    break
            if not has_parent:
                new_res2.append(resource)
    final_res = [
        {
            'resource': resource.get("resource").show_info(),
            'auth_type': resource.get("auth_type"),
        } for resource in new_res2
    ]
    # 8. 新增作者信息
    all_author_id = [resource.get("resource").user_id for resource in new_res2]
    all_author = UserInfo.query.filter(
        UserInfo.user_id.in_(all_author_id),
        UserInfo.user_status == 1
    ).all()

    author_map = {author.user_id: author.show_info() for author in all_author}
    for resource in final_res:
        resource['resource']["author_info"] = author_map.get(resource.get("resource").get("user_id"))
    return next_console_response(result={
        'data': final_res,
        'total': len(final_res),
    })


def get_all_company_share_resource(user):
    """
    获取用户从公司共享的资源
    :param user:
    :return:
    """
    company_share_resources = ShareResourceAuthorizeCompanyInfo.query.filter(
        ShareResourceAuthorizeCompanyInfo.company_id == user.user_company_id,
        ShareResourceAuthorizeCompanyInfo.auth_status == '正常',
    ).join(
        ResourceObjectMeta,
        ShareResourceAuthorizeCompanyInfo.resource_id == ResourceObjectMeta.id
    ).with_entities(
        ResourceObjectMeta,
        ShareResourceAuthorizeCompanyInfo.auth_type.label('auth_type'),
    ).filter(
        ResourceObjectMeta.resource_status == '正常',
    ).all()
    res = []
    for resource, auth_type in company_share_resources:
        res.append({
            'resource': resource,
            'auth_type': auth_type,
        })
    return res


def get_all_department_share_resource(user):
    """
    获取用户从部门共享的资源
    """
    all_departments = get_user_department_list(user)
    all_department_ids = [department.id for department in all_departments]
    department_share_resources = ShareResourceAuthorizeDepartmentInfo.query.filter(
        ShareResourceAuthorizeDepartmentInfo.auth_status == '正常',
        ShareResourceAuthorizeDepartmentInfo.department_id.in_(all_department_ids),
    ).join(
        ResourceObjectMeta,
        ShareResourceAuthorizeDepartmentInfo.resource_id == ResourceObjectMeta.id
    ).with_entities(
        ResourceObjectMeta,
        ShareResourceAuthorizeDepartmentInfo.auth_type.label('auth_type'),
    ).filter(
        ResourceObjectMeta.resource_status == '正常',
    ).all()
    res = []
    for resource, auth_type in department_share_resources:
        res.append({
            'resource': resource,
            'auth_type': auth_type,
        })
    return res


def get_all_colleague_share_resource(user):
    """
    获取用户从同事共享的资源
    """
    colleague_share_resources = ShareResourceAuthorizeColleagueInfo.query.filter(
        ShareResourceAuthorizeColleagueInfo.auth_user_id == user.user_id,
        ShareResourceAuthorizeColleagueInfo.auth_status == '正常',
    ).join(
        ResourceObjectMeta,
        ShareResourceAuthorizeColleagueInfo.resource_id == ResourceObjectMeta.id
    ).with_entities(
        ResourceObjectMeta,
        ShareResourceAuthorizeColleagueInfo.auth_type.label('auth_type'),
    ).filter(
        ResourceObjectMeta.resource_status == '正常',
    ).all()
    res = []
    for resource, auth_type in colleague_share_resources:
        res.append({
            'resource': resource,
            'auth_type': auth_type,
        })
    return res


def get_all_friend_share_resource(user):
    """
    获取用户从好友共享的资源
    :param user:
    :return:
    """
    friend_share_resources = ShareResourceAuthorizeFriendInfo.query.filter(
        ShareResourceAuthorizeFriendInfo.auth_user_id == user.user_id,
        ShareResourceAuthorizeFriendInfo.auth_status == '正常',
    ).join(
        ResourceObjectMeta,
        ShareResourceAuthorizeFriendInfo.resource_id == ResourceObjectMeta.id
    ).with_entities(
        ResourceObjectMeta,
        ShareResourceAuthorizeFriendInfo.auth_type.label('auth_type'),
    ).filter(
        ResourceObjectMeta.resource_status == '正常',
    ).all()
    res = []
    for resource, auth_type in friend_share_resources:
        res.append({
            'resource': resource,
            'auth_type': auth_type,
        })
    return res


def get_share_resource_meta(params):
    """
    获取资源对象元信息，
    :param params:
    :return:
    """
    t1 = time.time()
    user_id = int(params.get("user_id"))
    resource_id = params.get("resource_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center"
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    # 检查用户是否有权限访问资源
    if not check_user_manage_access_to_resource(
            {'user': target_user,
             'resource': target_resource,
             'access_type': 'read'}):
        return next_console_response(error_status=True, error_message="无权操作！")
    result = target_resource.show_info()
    t2 = time.time()
    # 如果是folder，增加资源大小与子资源数量统计
    if target_resource.resource_type == "folder":
        all_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == target_resource.user_id,
            ResourceObjectMeta.resource_status == "正常"
        ).all()
        all_sub_resource_ids = [target_resource.id]
        add_cnt = 1
        while add_cnt > 0:
            add_cnt = 0
            for resource_item in all_resources:
                if (resource_item.resource_parent_id in all_sub_resource_ids
                        and resource_item.id not in all_sub_resource_ids):
                    all_sub_resource_ids.append(resource_item.id)
                    add_cnt += 1
        sub_resource_list = [resource_item for resource_item in all_resources
                             if resource_item.id in all_sub_resource_ids]
        sub_dir = [resource_item for resource_item in sub_resource_list if resource_item.resource_type == "folder"]
        all_size = sum([resource_item.resource_size_in_MB for resource_item in sub_resource_list])
        result["resource_size_in_MB"] = all_size
        result["sub_resource_dir_cnt"] = len(sub_dir)
        result["sub_resource_file_cnt"] = len(sub_resource_list) - len(sub_dir)
        # rag资源数量
        all_rag_ref = RagRefInfo.query.filter(
            RagRefInfo.resource_id.in_(all_sub_resource_ids),
            RagRefInfo.ref_status == "成功"
        ).all()
        result["sub_rag_file_cnt"] = len(all_rag_ref)
    t3 = time.time()
    # 新增路径信息
    try:
        from app.services.resource_center.resource_object_service import get_resource_object_path
        resource_path_res = get_resource_object_path({
            "user_id": user_id,
            "resource_id": target_resource.id
        }).json
        resource_path = resource_path_res.get("result").get("data")
        if not resource_path:
            return next_console_response(result=[])
        resource_path = [resource_item.get("resource_name") for resource_item in resource_path]
    except Exception as e:
        app.logger.warning(f"获取资源路径异常：{e.args}")
        resource_path = []
    result["resource_path"] = "/".join(resource_path)
    t4 = time.time()
    # 返回资源ref状态
    ref = RagRefInfo.query.filter(
        RagRefInfo.resource_id == resource_id,
        RagRefInfo.ref_status != "已删除"
    ).order_by(
        RagRefInfo.id.desc()
    ).first()
    if ref:
        result["rag_status"] = ref.ref_status
    t5 = time.time()
    # 新增Tag信息
    all_tags = ResourceTagRelation.query.filter(
        ResourceTagRelation.resource_id == resource_id,
        ResourceTagRelation.rel_status == "正常"
    ).join(
        ResourceTag,
        ResourceTagRelation.tag_id == ResourceTag.id
    ).with_entities(
        ResourceTag
    ).all()
    result["resource_tags"] = [tag.show_info() for tag in all_tags]
    # 新增作者信息
    author_info = UserInfo.query.filter(
        UserInfo.user_id == target_resource.user_id
    ).first()
    if author_info:
        result["author_info"] = author_info.show_info()
    t6 = time.time()
    # 新增权限信息
    access_list = get_user_access_to_resource({
        "user": target_user,
        "resource": target_resource
    })
    t7 = time.time()
    # 定义权限优先级
    permission_priority = {'阅读': 1, '下载': 2, '编辑': 3, '管理': 4}
    highest_access = max(
        access_list,
        key=lambda x: permission_priority.get(x, 0),
        default=None
    ) if access_list else None
    result["access_list"] = [highest_access] if highest_access else []
    return next_console_response(result=result)


def get_user_access_to_resource(params):
    """
    获取用户对资源的所有访问权限
    :param params:
    :return:
    """
    user = params.get('user')
    resource = params.get('resource')
    # 如果是资源的拥有者，直接返回True
    if user.user_id == resource.user_id:
        return ['阅读', '下载', '编辑', '管理']
    # 获取资源的所有权限
    all_access_list_res = get_share_resource_access_list({
        'user_id': user.user_id,
        'resource_id': resource.id,
    })
    if all_access_list_res.json.get('error_status'):
        return False
    all_access_list = all_access_list_res.json.get('result').get('access_list')
    all_department_list = get_user_department_list(user)
    all_department_ids = [department.id for department in all_department_list]
    # 获取所有权限
    all_access = set()
    for access in all_access_list:
        # 检查好友权限
        if access.get('type') == 'friend' and (
                (access.get('id') and access.get('id') == user.user_id) or not access.get('id')):
            all_access.add(access.get('auth_type'))
        # 检查同事权限
        if access.get('type') == 'colleague' and access.get('id') and access.get('id') == user.user_id:
            all_access.add(access.get('auth_type'))
        # 检查部门权限
        if access.get('type') == 'department' and access.get('id') and access.get('id') in all_department_ids:
            all_access.add(access.get('auth_type'))
        # 检查公司权限
        if access.get('type') == 'company' and access.get('id') and access.get('id') == user.user_company_id:
            all_access.add(access.get('auth_type'))
        # 检查公开访问权限
        if access.get('type') == 'open':
            all_access.add(access.get('auth_type'))
    access_translate = {
        "read": '阅读',
        "download": '下载',
        "edit": '编辑',
        "manage": '管理',
    }
    return [access_translate.get(access) for access in all_access]


def search_share_resource_by_keyword(params):
    """
    根据关键词搜索共享资源，支持按权限类型过滤
        先获取用户所有可读的共享资源，取最大权限
        然后根据关键词和条件（包括auth_types）过滤
        如果rag增强，则使用未过滤的资源对应索引来检索
        最后返回结果，确保每个资源包含auth_type
        搜索接口不分页
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_ids = params.get("resource_ids", [])
    resource_type = params.get("resource_type", [])
    resource_format = params.get("resource_format", [])
    resource_tags = params.get("resource_tags", [])
    resource_keyword = params.get("resource_keyword")
    auth_type = params.get("auth_type")  # 权限类型过滤参数
    rag_enhance = params.get("rag_enhance", False)
    # 验证用户是否存在
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    # 获取用户的所有共享资源及权限
    res_with_auth = []  # 存储资源和权限的列表
    if target_user.user_account_type == '企业账号':
        # 1. 获取用户的所有公司共享资源
        res_with_auth.extend(get_all_company_share_resource(target_user))
        app.logger.warning(f"获取用户的所有公司共享资源,{len(res_with_auth)}")
        # 2. 获取用户的所有部门共享资源
        res_with_auth.extend(get_all_department_share_resource(target_user))
        app.logger.warning(f"获取用户的所有部门共享资源,{len(res_with_auth)}")
        # 3. 获取用户的所有同事共享资源
        res_with_auth.extend(get_all_colleague_share_resource(target_user))
        app.logger.warning(f"获取用户的所有同事共享资源,{len(res_with_auth)}")
    # 4. 获取用户的所有好友共享资源
    res_with_auth.extend(get_all_friend_share_resource(target_user))
    app.logger.warning(f"获取用户的所有好友共享资源,{len(res_with_auth)}")
    # 5. 获取自己共享的资源
    self_share_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == '正常',
        ResourceObjectMeta.resource_is_share == True,
        ResourceObjectMeta.resource_source == "resource_center",
    ).all()
    for resource in self_share_resources:
        res_with_auth.append({
            'resource': resource,
            'auth_type': 'manage',
        })
    # 6. 取最大权限（与get_share_resource_list一致）
    resource_access_value_map = {}
    for resource in res_with_auth:
        rid = resource['resource'].id
        auth_value = access_value_map.get(resource['auth_type'], 0)
        if rid not in resource_access_value_map or auth_value > resource_access_value_map[rid]:
            resource_access_value_map[rid] = auth_value
    # 汇总去重，只保留最大权限的资源
    tmp_add_id = []
    new_res = []
    for resource in res_with_auth:
        rid = resource['resource'].id
        if (rid not in tmp_add_id and
            access_value_map.get(resource['auth_type'], 0) == resource_access_value_map[rid]):
            new_res.append(resource)
            tmp_add_id.append(rid)
    # 扩展至所有下级资源并添加过滤条件
    res = [item['resource'] for item in new_res]
    resource_auth_map = {item['resource'].id: item['auth_type'] for item in new_res}  # 保留权限映射
    all_parent_id = [resource.id for resource in res]
    app.logger.warning(f"扩展至所有下级资源并添加过滤条件,begin,{len(res)},{len(all_parent_id)}")
    while all_parent_id:
        children_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.resource_status == '正常',
            ResourceObjectMeta.resource_source == "resource_center",
            ResourceObjectMeta.resource_parent_id.in_(all_parent_id),
        ).all()
        all_parent_id = []
        for resource in children_resource:
            all_parent_id.append(resource.id)
            # 子资源继承父资源的权限
            parent_auth = resource_auth_map.get(resource.resource_parent_id, 'read')
            resource_auth_map[resource.id] = parent_auth
            res.append(resource)
        app.logger.warning(f"扩展至所有下级资源并添加过滤条件,middle,{len(res)},{len(all_parent_id)}")
    finally_resource_ids = [resource.id for resource in res]
    app.logger.warning(f"扩展至所有下级资源并添加过滤条件,final,{len(finally_resource_ids)}")
    # 构建查询条件
    all_conditions = [
        ResourceObjectMeta.resource_status == '正常',
        ResourceObjectMeta.resource_source == "resource_center",
        ResourceObjectMeta.id.in_(finally_resource_ids),
        or_(
            ResourceObjectMeta.resource_name.like(f"%{resource_keyword}%"),
            ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%"),
        )
    ]
    if resource_type:
        all_conditions.append(ResourceObjectMeta.resource_type.in_(resource_type))
    if resource_format:
        all_conditions.append(ResourceObjectMeta.resource_format.in_(resource_format))
    if resource_ids:
        all_conditions.append(ResourceObjectMeta.id.in_(resource_ids))
    # 查询资源
    all_resources = ResourceObjectMeta.query.filter(*all_conditions)
    if resource_tags:
        user_tags = ResourceTag.query.filter(
            ResourceTag.user_id == user_id,
            ResourceTag.tag_status == "正常",
            ResourceTag.id.in_(resource_tags)
        ).all()
        legal_tags = [tag.id for tag in user_tags]
        all_resources = all_resources.join(
            ResourceTagRelation,
            ResourceTagRelation.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceTagRelation.tag_id.in_(legal_tags)
        ).with_entities(
            ResourceObjectMeta
        )
    total = all_resources.count()
    res = all_resources.order_by(
        ResourceObjectMeta.create_time.desc()
    ).all()

    # 获取资源对应的所有用户标签
    all_resource_id = [resource.id for resource in res]
    all_resource_tag_rels = ResourceTagRelation.query.filter(
        ResourceTagRelation.resource_id.in_(all_resource_id),
        ResourceTagRelation.rel_status == "正常"
    ).all()
    resource_tag_map = {}
    for tag_rel in all_resource_tag_rels:
        if tag_rel.resource_id not in resource_tag_map:
            resource_tag_map[tag_rel.resource_id] = []
        resource_tag_map[tag_rel.resource_id].append(tag_rel.tag_id)
    all_tags_id = list(set([tag_rel.tag_id for tag_rel in all_resource_tag_rels]))
    all_tags = ResourceTag.query.filter(
        ResourceTag.id.in_(all_tags_id)
    ).all()
    tags = [tag.to_dict() for tag in all_tags]
    # app.logger.warning(f"获取资源对应的所有用户标签,{len(tags)}")
    # 获取资源对应的作者信息
    all_author_id = list(set([resource.user_id for resource in res]))
    all_author = UserInfo.query.filter(
        UserInfo.user_id.in_(all_author_id),
        UserInfo.user_status == 1
    ).all()
    author_info = [author.show_info() for author in all_author]
    app.logger.warning(f"获取资源对应的作者信息,{len(author_info)}")

    # 格式化结果，确保包含auth_type
    new_res = []
    for resource in res:
        resource_info = resource.show_info()
        resource_info["resource_tags"] = list(set(resource_tag_map.get(resource.id, [])))
        resource_info["auth_type"] = resource_auth_map[resource.id]  # 确保添加权限标识
        new_res.append(resource_info)

    # 如果启用RAG增强
    if rag_enhance:
        from app.services.resource_center.resource_object_service import search_rag_enhanced
        rag_res = search_rag_enhanced({
            "all_resource_id": all_resource_id,
            "resource_keyword": resource_keyword
        })
        for rag_item in rag_res:
            rag_id = rag_item.get("id")
            if rag_id not in all_resource_id:
                rag_item["auth_type"] = "read"
                new_res.append(rag_item)
                total += 1
            else:
                for item in new_res:
                    if item.get("id") == rag_id:
                        item["rerank_score"] = rag_item.get("rerank_score")
                        item["ref_text"] = rag_item.get("ref_text")
                        break
        new_res = sorted(new_res, key=lambda x: x.get("rerank_score", 0), reverse=True)
    if auth_type:
        required_level = access_value_map.get(auth_type, 0)
        new_res = [item for item in new_res if access_value_map.get(item.get("auth_type"), 0) >= required_level]
    # 返回结果，确保data中的每个条目包含auth_type
    return next_console_response(result={
        "data": new_res,  # 每个资源对象包含auth_type
        "total": total,
        "resource_tags": tags,
        "author_info": author_info
    })


def search_share_resource_by_keyword_in_resource(params):
    """
    在指定资源中使用关键词搜索
    :param params: 包含 user_id, resource_id（单个资源ID）, resource_keyword 等参数
    :return: 搜索结果
    """
    user_id = int(params.get("user_id"))
    resource_id = params.get("resource_id")  # 假设传入单个资源ID
    resource_keyword = params.get("resource_keyword")
    auth_type = params.get("auth_type")
    # 检查用户是否存在
    target_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")

    def get_all_subresource_ids(resource_parent_id, visited=None):
        # 递归获取所有子资源ID
        if visited is None:
            visited = set()
        resource_ids = []
        if resource_parent_id in visited:
            return resource_ids
        visited.add(resource_parent_id)
        sub_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.resource_parent_id == resource_parent_id,
            ResourceObjectMeta.resource_status == '正常',
            ResourceObjectMeta.resource_source == "resource_center"
        ).all()
        for sub_res in sub_resources:
            resource_ids.append(sub_res.id)
            resource_ids.extend(get_all_subresource_ids(sub_res.id, visited))
        return resource_ids

    search_params = {
        "user_id": user_id,
        "resource_keyword": resource_keyword,
        "resource_type": params.get("resource_type", []),
        "resource_format": params.get("resource_format", []),
        "resource_tags": params.get("resource_tags", []),
        "rag_enhance": params.get("rag_enhance", False),
        "auth_type": auth_type
    }
    if resource_id:
        # 先校验资源是否存在
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource_id,
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_source == "resource_center"
        ).first()
        if not target_resource:
            return next_console_response(error_status=True, error_message="当前资源不存在！")
        # 检查用户是否有权限访问资源
        if not check_user_manage_access_to_resource(
                {'user': target_user,
                 'resource': target_resource,
                 'access_type': 'read'}):
            return next_console_response(error_status=True, error_message="没有当前资源的访问权限！")
        # 检查资源是否为文件夹
        if target_resource.resource_type != "folder":
            return next_console_response(error_status=True, error_message="当前资源不是文件夹，无法搜索！")
        # 检查资源是否有子资源
        all_subresource_ids = get_all_subresource_ids(resource_id)
        if not all_subresource_ids:
            return next_console_response(error_status=True, error_message="当前资源没有子资源，无法搜索！")
        # 搜索参数中添加所有子资源ID
        search_params["resource_ids"] = all_subresource_ids
    # 调用现有搜索函数
    return search_share_resource_by_keyword(search_params)


def get_resource_download_cooling_record(params):
    """
    获取资源下载冷却记录
        下载信息，
        授权信息，
        拦截信息，
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    cooling_id = params.get("cooling_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_cooldown = ResourceDownloadCoolingRecord.query.filter(
        ResourceDownloadCoolingRecord.id == cooling_id,
        ResourceDownloadCoolingRecord.author_id == user_id,
    ).first()
    if not target_cooldown:
        return next_console_response(error_status=True, error_message="记录不存在！")
    cooling_user = UserInfo.query.filter(
        UserInfo.user_id == target_cooldown.user_id
    ).first()
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == target_cooldown.resource_id
    ).first()
    res = {
        "cooling_record": target_cooldown.to_dict(),
        "cooling_user": cooling_user.show_info(),
        "cooling_resource": target_resource.show_info()
    }
    return next_console_response(result=res)


def update_resource_download_cooling_record(params):
    """
    更新资源下载冷却记录
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    cooling_id = params.get("cooling_id")
    cooling_limit = params.get("cooling_limit")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_cooldown = ResourceDownloadCoolingRecord.query.filter(
        ResourceDownloadCoolingRecord.id == cooling_id,
        ResourceDownloadCoolingRecord.author_id == user_id,
    ).first()
    if not target_cooldown:
        return next_console_response(error_status=True, error_message="记录不存在！")
    target_cooldown.author_allow = True
    target_cooldown.author_allow_cnt = cooling_limit
    db.session.add(target_cooldown)
    db.session.commit()
    return next_console_response(result=target_cooldown.to_dict())
