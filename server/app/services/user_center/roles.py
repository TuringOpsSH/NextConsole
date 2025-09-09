from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user_center.role_info import *
from app.models.user_center.user_role_info import *
from app.services.configure_center.response_utils import next_console_response


def add_role(params):
    """
    新增角色
    :return:
    """
    # 获取入参
    role_name = params.get("role_name")
    role_desc = params.get("role_desc")
    status = 1
    new_role = RoleInfo(
        role_name=role_name,
        role_desc=role_desc,
        status=status
    )
    db.session.add(new_role)
    try:
        db.session.commit()
        return next_console_response()
    except IntegrityError as e:
        error_info = e.orig.args[1].split(" ")[2].strip("'")
        return next_console_response(error_status=True, error_code=1001,
                                     error_message=" {} 已经被占用！".format(error_info))


def search_roles(params):
    filters = []
    page_size = params.get("page_size", 100)
    page_num = params.get("page_num", 1)
    role_id = params.get("role_id", [])
    if role_id:
        filters.append(RoleInfo.role_id == role_id)

    role_name = params.get("role_name", [])
    if role_name:
        filters.append(RoleInfo.role_name.in_(role_name))

    role_desc = params.get("role_desc", [])
    if role_desc:
        filters.append(RoleInfo.role_desc.in_(role_desc))

    role_create_time = params.get("role_create_time", [])
    if role_create_time:
        filters.append(
            RoleInfo.role_create_time.between(
                role_create_time[0], role_create_time[1]))

    status = params.get("status", [])
    if status:
        filters.append(RoleInfo.status.in_(status))
    else:
        filters.append(RoleInfo.status != -1)

    res = RoleInfo.query.filter(
        and_(
            *filters
        )
    )
    res_cnt = res.count()
    pagination = res.order_by(
        desc(RoleInfo.role_id)).paginate(
        page=page_num, per_page=page_size, error_out=False)
    response = [role.to_dict() for role in pagination.items]
    response = {"cnt": res_cnt, "data": response}
    return next_console_response(result=response)


def update_role(params):
    role_id = params.get("role_id")
    del params["role_id"]
    try:
        res = RoleInfo.query.filter(RoleInfo.role_id == role_id).update(params, synchronize_session=False)
        db.session.commit()
        return next_console_response(result=res)
    except IntegrityError as e:
        error_info = e.orig.args[1].split(" ")[2].strip("'")
        return next_console_response(error_status=True, error_code=1001,
                                     error_message=" {} 已经被占用！".format(error_info))


def delete_roles(params):
    role_ids = params.get("role_ids", [])
    res = RoleInfo.query.filter(RoleInfo.role_id.in_(role_ids)).delete(synchronize_session=False)
    db.session.commit()
    return next_console_response(result=res)


def get_role_detail(params):
    role_id = params.get("role_id")
    role_info = db.session.query(RoleInfo).filter(RoleInfo.role_id == role_id).first()
    role_info = role_info.to_dict()
    return next_console_response(result={"role_info": role_info})


def roles_required(role_names):
    """
    权限装饰器
    :param role_names:
    :return:
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user_roles = UserRoleInfo.query.filter(UserRoleInfo.user_id == user_id).all()
            all_role_ids = [role.role_id for role in user_roles]
            all_roles = RoleInfo.query.filter(RoleInfo.role_id.in_(all_role_ids)).all()
            user_roles = [role.role_name for role in all_roles]
            if not set(role_names) & set(user_roles):
                return next_console_response(error_status=True, error_message="权限不足！")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
