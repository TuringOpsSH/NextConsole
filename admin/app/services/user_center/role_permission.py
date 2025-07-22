from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from app.models.user_center.role_permission_info import *
from app.models.user_center.permission_info import *
from app.services.configure_center.response_utils import next_console_response


def add_role_permission(params):
    """
    新增角色权限
    """
    role_id = params.get("role_id")
    permission_ids = params.get("permission_ids")
    rel_status = params.get("rel_status", 1)
    if not role_id:
        return next_console_response(error_status=True, error_code=1000, error_message="角色ID不能为空！")
    if not permission_ids:
        return next_console_response(error_status=True, error_code=1000, error_message="权限ID不能为空！")
    new_role_permissions = [RolePermissionInfo(
        role_id=role_id,
        permission_id=permission_id,
        rel_status=rel_status
    ) for permission_id in permission_ids]
    try:
        res = db.session.add_all(new_role_permissions)
        db.session.commit()
        db.session.close()
        return next_console_response(result=res)
    except IntegrityError as e:
        error_info = e.orig.args[1].split(" ")[2].strip("'")
        return next_console_response(error_status=True, error_code=1001,
                                     error_message=" {} 已经被占用！".format(error_info))


def search_role_permissions(params):
    """
    查询角色权限
    """
    role_ids = params.get("role_ids")
    if not role_ids:
        return next_console_response(error_status=True, error_code=1000, error_message="角色ID不能为空！")
    role_permission = PermissionInfo.query.join(
        RolePermissionInfo, RolePermissionInfo.permission_id == PermissionInfo.permission_id).filter(
        RolePermissionInfo.role_id.in_(role_ids)).all()
    if role_permission:
        return next_console_response(result=[permission.to_dict() for permission in role_permission])
    else:
        return next_console_response(error_status=True, error_code=1002, error_message="角色权限不存在！")


def delete_role_permissions(params):
    """
    删除角色权限
    """
    role_id = params.get("role_id")
    permission_ids = params.get("permission_ids", [])
    if not role_id:
        return next_console_response(error_status=True, error_code=1000, error_message="角色ID不能为空！")
    if not permission_ids:
        return next_console_response(error_status=True, error_code=1000, error_message="权限ID不能为空！")
    res = RolePermissionInfo.query.filter(
        and_(RolePermissionInfo.role_id == role_id, RolePermissionInfo.permission_id.in_(permission_ids))).delete(
        synchronize_session=False)
    db.session.commit()
    db.session.close()
    return next_console_response(result=res)



