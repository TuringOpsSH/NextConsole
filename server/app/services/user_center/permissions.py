from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from app.models.user_center.user_role_info import *
from app.models.user_center.permission_info import *
from app.models.user_center.role_permission_info import *
from app.services.configure_center.response_utils import next_console_response
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def add_permission(params):
    """
    新增权限
    :return:
    """
    # 获取入参
    permission_name = params.get("permission_name")
    permission_desc = params.get("permission_desc")
    permission_url = params.get("permission_url")
    permission_condition = params.get("permission_condition")
    permission_status = 1
    if permission_url == "":
        return next_console_response(error_status=True, error_code=1001,
                                     error_message="权限URL不能为空！")
    new_permission = PermissionInfo(
        permission_name=permission_name,
        permission_desc=permission_desc,
        permission_status=permission_status,
        permission_url=permission_url,
        permission_condition=permission_condition
    )
    res = db.session.add(new_permission)
    try:
        db.session.commit()
        return next_console_response(result=res)
    except IntegrityError as e:
        error_info = e.orig.args[1].split(" ")[2].strip("'")
        return next_console_response(error_status=True, error_code=1001,
                                     error_message=" {} 已经被占用！".format(error_info))


def search_permissions(params):
    filters = []
    page_size = params.get("page_size", 100)
    page_num = params.get("page_num", 1)
    permission_id = params.get("permission_id", [])
    if permission_id:
        filters.append(PermissionInfo.permission_id == permission_id)

    permission_name = params.get("permission_name", [])
    if permission_name:
        filters.append(PermissionInfo.permission_name.in_(permission_name))

    permission_desc = params.get("permission_desc", [])
    if permission_desc:
        filters.append(PermissionInfo.permission_desc.in_(permission_desc))

    permission_create_time = params.get("permission_create_time", [])
    if permission_create_time:
        filters.append(
            PermissionInfo.permission_create_time.between(
                permission_create_time[0], permission_create_time[1]))

    permission_status = params.get("permission_status", [])
    if permission_status:
        filters.append(PermissionInfo.permission_status.in_(permission_status))
    else:
        filters.append(PermissionInfo.permission_status != -1)

    # 查询
    permission_info = PermissionInfo.query.filter(
        and_(*filters)).order_by(desc(PermissionInfo.permission_create_time)).paginate(
        page=page_num, per_page=page_size, error_out=False)
    permission_list = []
    for permission in permission_info.items:
        permission_list.append(permission.to_dict())
    return next_console_response(result={"cnt": permission_info.total, "data": permission_list})


def delete_permissions(params):
    permission_ids = params.get("permission_ids")
    res = PermissionInfo.query.filter(
        PermissionInfo.permission_id.in_(permission_ids)).delete(synchronize_session=False)
    db.session.commit()
    return next_console_response(result=res)


def update_permission(params):
    permission_id = params.get("permission_id")
    if permission_id is None:
        return next_console_response(error_status=True, error_code=1001,
                                     error_message="权限ID不能为空！")
    del params["permission_id"]
    try:
        res = PermissionInfo.query.filter(
            PermissionInfo.permission_id == permission_id).update(params, synchronize_session=False)
        db.session.commit()
        return next_console_response(result=res)
    except IntegrityError as e:
        error_info = e.orig.args[1].split(" ")[2].strip("'")
        return next_console_response(error_status=True, error_code=1001,
                                     error_message=" {} 已经被占用！".format(error_info))


def get_permission_detail(params):
    permission_id = params.get("permission_id")
    permission_info = PermissionInfo.query.filter(PermissionInfo.permission_id == permission_id).first()
    return next_console_response(result=permission_info.to_dict())


def permission_required(permission_url):
    """
    权限验证
        根据用户，查询角色，再查询权限，是否有该对象的权限，
        如果有，则返回，否则返回403

    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            permission_info = UserRoleInfo.query.join(
                RolePermissionInfo, UserRoleInfo.role_id == RolePermissionInfo.role_id).join(
                PermissionInfo, RolePermissionInfo.permission_id == PermissionInfo.permission_id
            ).filter(
              UserRoleInfo.user_id == user_id,
              PermissionInfo.permission_status == 1,
              PermissionInfo.permission_url == permission_url,
              PermissionInfo.permission_name == "all"
            ).all()
            if not permission_info:
                return next_console_response(error_status=True, error_code=403, error_message="没有权限！请联系管理员！")
            else:
                return fn(*args, **kwargs)
        return wrapper
    return decorator


