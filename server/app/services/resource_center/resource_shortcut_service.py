from app.models.resource_center.resource_model import ResourceObjectShortCut
from app.services.configure_center.response_utils import next_console_response
from app.models.user_center.user_info import UserInfo
from app.app import db
from app.models.resource_center.resource_model import ResourceObjectMeta


def add_resource_shortcut(params):
    """
    新增资源快捷方式
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_id = params.get("resource_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    if not target_resource.resource_type == "folder":
        return next_console_response(error_message="资源类型不正确！")
    resource_shortcut = ResourceObjectShortCut.query.filter(
        ResourceObjectShortCut.user_id == user_id,
        ResourceObjectShortCut.resource_id == resource_id
    ).first()
    if resource_shortcut:
        return next_console_response(error_message="资源快捷方式已存在！")
    new_shortcut = ResourceObjectShortCut(
        user_id=user_id,
        resource_id=resource_id
    )
    db.session.add(new_shortcut)
    db.session.commit()
    return next_console_response(result=new_shortcut.to_dict())


def search_resource_shortcut(params):
    """
    获取资源快捷方式
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    resource_shortcuts = ResourceObjectShortCut.query.filter(
        ResourceObjectShortCut.user_id == user_id
    ).order_by(ResourceObjectShortCut.create_time.asc()).all()
    all_resource_id = [resource_shortcut.resource_id for resource_shortcut in resource_shortcuts]
    all_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(all_resource_id),
        ResourceObjectMeta.resource_status == "正常"
    ).all()
    all_resource_map = {resource.id: resource for resource in all_resource}
    result = []
    for shortcut in resource_shortcuts:
        resource = all_resource_map.get(shortcut.resource_id)
        if resource:
            result.append({
                "id": shortcut.id,
                "resource_id": shortcut.resource_id,
                "resource_name": resource.resource_name,
                "resource_icon": resource.resource_icon,
                "create_time": shortcut.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            })
    return next_console_response(result={
        "total": len(result),
        "data": result
    })


def delete_resource_shortcut(params):
    """
    删除资源快捷方式
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    shortcut_id = params.get("shortcut_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    resource_shortcut = ResourceObjectShortCut.query.filter(
        ResourceObjectShortCut.user_id == user_id,
        ResourceObjectShortCut.id == shortcut_id
    ).first()
    if not resource_shortcut:
        return next_console_response(error_message="资源快捷方式已删除！")
    db.session.delete(resource_shortcut)
    db.session.commit()
    return next_console_response(result="删除成功！")

