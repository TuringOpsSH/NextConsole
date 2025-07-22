from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from app.models.user_center.user_role_info import *
from app.models.user_center.role_info import *
from app.services.configure_center.response_utils import next_console_response


def add_user_role(params):
    """
    新增用户角色
    """
    user_id = int(params.get("user_id"))
    role_id = params.get("role_id")
    rel_status = params.get("rel_status", 1)
    if not user_id:
        return next_console_response(error_status=True, error_code=1000, error_message="用户ID不能为空！")
    if not role_id:
        return next_console_response(error_status=True, error_code=1000, error_message="角色ID不能为空！")

    new_user_role = UserRoleInfo(
        user_id=user_id,
        role_id=role_id,
        rel_status=rel_status
    )
    db.session.add(new_user_role)
    try:
        res = db.session.commit()
        return next_console_response(result=res)
    except IntegrityError as e:
        error_info = e.orig.args[1].split(" ")[2].strip("'")
        return next_console_response(error_status=True, error_code=1001,
                                     error_message=" {} 已经被占用！".format(error_info))


def search_user_roles(params):
    """
    查询用户角色
    """
    user_id = int(params.get("user_id"))
    if not user_id:
        return next_console_response(error_status=True, error_code=1000, error_message="用户ID不能为空！")
    user_role = RoleInfo.query.join(
        UserRoleInfo, UserRoleInfo.role_id == RoleInfo.role_id).filter(
        UserRoleInfo.user_id == user_id).all()
    if user_role:
        return next_console_response(result=[role.to_dict() for role in user_role])
    else:
        return next_console_response(error_status=True, error_code=1002, error_message="用户角色不存在！")


def delete_user_roles(params):
    """
    删除用户角色
    """
    user_id = int(params.get("user_id"))
    role_ids = params.get("role_ids", [])
    if not user_id:
        return next_console_response(error_status=True, error_code=1000, error_message="用户ID不能为空！")
    if not role_ids:
        return next_console_response(error_status=True, error_code=1000, error_message="角色ID不能为空！")
    res = UserRoleInfo.query.filter(
        and_(UserRoleInfo.user_id == user_id, UserRoleInfo.role_id.in_(role_ids))).delete(synchronize_session=False)
    db.session.commit()
    return next_console_response(result=res)

