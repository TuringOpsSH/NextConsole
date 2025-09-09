from app.services.user_center.user_role import *
from app.services.user_center.users import *
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash


def is_valid_datetime_ts(datetime_str):
    """
    判断日期时间格式是否正确yyyy-MM-dd HH:mm:ss
    """
    try:
        datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


def lookup_user_details_twadmin(params):
    """
    NextConsole管理员查询用户详细信息
    可根据params中的参数进行查询,增加账号类型，公司过滤条件
    """

    user_id = int(params.get("user_id"))
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 20)

    # 注册时间
    register_start_date = params.get("register_start_date")
    if register_start_date is not None:
        if not is_valid_datetime_ts(register_start_date):
            return next_console_response(error_status=True, error_code=1004, error_message="开始日期格式错误！")
    register_end_date = params.get("register_end_date")
    if register_end_date is not None:
        if not is_valid_datetime_ts(register_end_date):
            return next_console_response(error_status=True, error_code=1004, error_message="结束日期格式错误！")
            # 是否归档, 1-归档 0-未归档
    is_archive = params.get("is_archive")
    if is_archive is not None:
        if not isinstance(is_archive, int):
            return next_console_response(error_status=True, error_code=1004, error_message="is_archive格式错误！")
        elif is_archive not in [0, 1]:
            return next_console_response(error_status=True, error_code=1004, error_message="is_archive取值范围错误！")
    # 账号类型
    user_account_type = params.get("user_account_type", [])
    # 公司
    user_company_id = params.get("user_company_id", [])
    # 部门
    user_department_id = params.get("user_department_id", [])
    # 角色
    role_desc = params.get("role_desc", [])
    # 搜索
    search_text = params.get("search_text")
    try:
        search_text_int = int(search_text)
    except (ValueError, TypeError):
        search_text_int = 0
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="账号异常！")
    all_conditions = [
    ]
    if register_start_date:
        all_conditions.append(
            UserInfo.create_time >= datetime.strptime(register_start_date, '%Y-%m-%d %H:%M:%S')
        )
    if register_end_date:
        all_conditions.append(
            UserInfo.create_time <= datetime.strptime(register_end_date, '%Y-%m-%d %H:%M:%S')
        )
    if user_department_id:
        all_conditions.append(
            UserInfo.user_department_id.in_(user_department_id)
        )
    if search_text:
        all_conditions.append(
            or_(
                UserInfo.user_id == search_text_int,
                UserInfo.user_name.like(f"%{search_text}%"),
                UserInfo.user_nick_name.like(f"%{search_text}%"),
                UserInfo.user_nick_name_py.like(f"%{search_text}%"),
                UserInfo.user_email.like(f"%{search_text}%"),
                UserInfo.user_phone.like(f"%{search_text}%"),
            )
        )
    if is_archive == 0:
        all_conditions.append(
            UserInfo.user_status == 1
        )
    else:
        all_conditions.append(
            UserInfo.user_status < 0
        )
    if user_account_type:
        all_conditions.append(
            UserInfo.user_account_type.in_(user_account_type)
        )
    if user_company_id:
        all_conditions.append(
            UserInfo.user_company_id.in_(user_company_id)
        )

    all_colleagues = UserInfo.query.filter(
        *all_conditions
    )
    total = all_colleagues.count()
    all_colleagues = all_colleagues.paginate(page=page_num, per_page=page_size, error_out=False)
    all_colleagues_ids = [user.user_id for user in all_colleagues]
    role_condition = []
    if role_desc:
        role_condition.append(
            RoleInfo.role_desc.in_(role_desc)
        )
    role_desc_res = UserInfo.query.filter(
        UserInfo.user_id.in_(all_colleagues_ids)
    ).join(
        UserRoleInfo,
        UserRoleInfo.user_id == UserInfo.user_id
    ).filter(
        UserRoleInfo.rel_status == 1
    ).with_entities(
        UserInfo,
        UserRoleInfo.role_id
    ).join(
        RoleInfo,
        RoleInfo.role_id == UserRoleInfo.role_id
    ).filter(
        RoleInfo.status == 1,
        *role_condition
    ).with_entities(
        UserInfo,
        RoleInfo
    ).all()
    role_desc_map = {}
    for user, role in role_desc_res:
        if user.user_id not in role_desc_map:
            role_desc_map[user.user_id] = role.role_desc
        else:
            role_desc_map[user.user_id] += f",{role.role_desc}"
    # 公司信息
    all_user_companies = CompanyInfo.query.filter(
        CompanyInfo.company_status == "正常"
    ).all()
    all_user_companies_maps = {
        company.id: company.company_name
        for company in all_user_companies
    }
    # 部门信息
    all_user_departments = DepartmentInfo.query.filter(
        DepartmentInfo.department_status == "正常"
    ).all()
    all_user_departments_maps = {
        department.id: department.department_name
        for department in all_user_departments
    }
    all_role_desc = RoleInfo.query.filter(
        RoleInfo.status == 1
    ).all()
    data = []
    for colleague in all_colleagues:
        sub_data = colleague.to_dict()
        if role_desc and not role_desc_map.get(colleague.user_id):
            total += -1
            continue
        sub_data["role_desc"] = role_desc_map.get(colleague.user_id)
        sub_data["is_archive"] = False if colleague.user_status == 1 else True
        sub_data["user_company"] = all_user_companies_maps.get(colleague.user_company_id)
        sub_data["user_department"] = all_user_departments_maps.get(colleague.user_department_id)
        data.append(sub_data)
    return next_console_response(result={
        "total": total,
        "data": data,
        "user_companies": [company.to_dict() for company in all_user_companies],
        "user_departments": [department.to_dict() for department in all_user_departments],
        "role_desc": [role.role_desc for role in all_role_desc],
        "user_account_type": ["企业账号", "个人账号"]
    })


def update_user_role_twadmin(params):
    """
    NextConsole管理员直接修改用户角色
    """
    user_id = int(params.get("user_id"))
    update_user_id = params.get("update_user_id")
    dest_role_desc = params.get("dest_role_desc")
    # 同时需要判断 user_id 和 update_user_id 的企业是否一致
    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="账号异常！")
    update_user = UserInfo.query.filter(
        UserInfo.user_id == update_user_id,
        UserInfo.user_status == 1,
    ).first()
    if not update_user:
        return next_console_response(error_status=True, error_message="账号异常！")

    dest_role = RoleInfo.query.filter(
        RoleInfo.role_desc.in_(dest_role_desc),
        RoleInfo.status == 1
    ).all()
    all_dest_role_id = [role.role_id for role in dest_role]
    if not all_dest_role_id:
        return next_console_response(error_status=True, error_message="角色异常！")
    # 获取 update_user_id 的当前所有角色，形成list
    all_role_rels = UserRoleInfo.query.filter(
        UserRoleInfo.user_id == update_user_id,
        UserRoleInfo.rel_status == 1
    ).all()
    all_current_role_id = [role.role_id for role in all_role_rels]
    new_roles_ids = list(set(all_dest_role_id) - set(all_current_role_id))
    del_roles_ids = list(set(all_current_role_id) - set(all_dest_role_id))
    for new_role_id in new_roles_ids:
        new_role_rel = UserRoleInfo(
            user_id=update_user_id,
            role_id=new_role_id,
            rel_status=1
        )
        db.session.add(new_role_rel)
    for del_role_id in del_roles_ids:
        del_role_rel = UserRoleInfo.query.filter(
            UserRoleInfo.user_id == update_user_id,
            UserRoleInfo.role_id == del_role_id
        ).first()
        db.session.delete(del_role_rel)
    db.session.commit()
    return next_console_response(result=dest_role_desc)


def check_df_data_corp(df):
    """
    检查df数据是否合法
    """
    # df = pd.read_excel(excel_file, sheet_name="用户数据", engine='openpyxl')
    # 如果df是空的或仅有表头
    if df.empty:
        return next_console_response(error_status=True, error_code=1004, error_message="文件内容为空！")
    else:
        # 检查是否改过表头 邮箱、昵称、手机号、密码、性别、部门、角色
        # 如果df是空的或仅有表头
        if df.empty:
            return next_console_response(error_status=True, error_code=1004, error_message="文件内容为空！")
        else:
            # 检查是否改过表头
            if df.columns[0] != "用户名称（必填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第一列异常")
            elif df.columns[1] != "密码（选填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第二列异常")
            elif df.columns[2] != "用户昵称（选填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第三列异常")
            elif df.columns[3] != "邮箱（选填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第四列异常")
            elif df.columns[4] != "手机号（选填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第五列异常")
            elif df.columns[5] != "性别（选填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第六列异常")
            elif df.columns[6] != "年龄（选填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第七列异常")
            elif df.columns[7] != "职位（选填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第八列异常")
            elif df.columns[8] != "部门ID（选填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第九列异常")
            elif df.columns[9] != "资源库空间上限，以mb为单位（选填）":
                return next_console_response(error_status=True, error_code=1004, error_message="第十列异常")
            else:
                return True


def check_df_data_twadmin(df):
    """
    检查df数据是否合法
    """
    # 如果df是空的或仅有表头
    if df.empty:
        return next_console_response(error_status=True, error_code=1004, error_message="文件内容为空！")
    else:
        # 检查是否改过表头
        if df.columns[0] != "用户名称（必填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第一列异常")
        elif df.columns[1] != "密码（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第二列异常")
        elif df.columns[2] != "用户昵称（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第三列异常")
        elif df.columns[3] != "邮箱（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第四列异常")
        elif df.columns[4] != "手机号（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第五列异常")
        elif df.columns[5] != "性别（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第六列异常")
        elif df.columns[6] != "年龄（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第七列异常")
        elif df.columns[7] != "公司（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第八列异常")
        elif df.columns[8] != "部门（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第九列异常")
        elif df.columns[9] != "职位（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第十列异常")
        elif df.columns[10] != "公司ID（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第十一列异常")
        elif df.columns[11] != "部门ID（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第十二列异常")
        elif df.columns[12] != "资源库空间上限，以mb为单位（选填）":
            return next_console_response(error_status=True, error_code=1004, error_message="第十三列异常")
        else:
            return True


# 管理员仅能看本企业的用户情况
def lookup_user_details_admin(params):
    """
    管理员查询用户详细信息
    可根据params中的参数进行查询
    """
    user_id = int(params.get("user_id"))
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 20)
    
    # 注册时间
    register_start_date = params.get("register_start_date")
    if register_start_date is not None:
        if not is_valid_datetime_ts(register_start_date):
            return next_console_response(error_status=True, error_code=1004, error_message="开始日期格式错误！")
    register_end_date = params.get("register_end_date")
    if register_end_date is not None:
        if not is_valid_datetime_ts(register_end_date):
            return next_console_response(error_status=True, error_code=1004, error_message="结束日期格式错误！")    
    # 是否归档, 1-归档 0-未归档
    is_archive = params.get("is_archive")
    if is_archive is not None:
        if not isinstance(is_archive, int):
            return next_console_response(error_status=True, error_code=1004, error_message="is_archive格式错误！")
        elif is_archive not in [0, 1]:
            return next_console_response(error_status=True, error_code=1004, error_message="is_archive取值范围错误！")
    # 部门
    user_department_id = params.get("user_department_id", [])
    # 角色
    role_desc = params.get("role_desc", [])
    # 搜索
    search_text = params.get("search_text")
    try:
        search_text_int = int(search_text)
    except (ValueError, TypeError):
        search_text_int = 0
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not target_user:
        return next_console_response(error_status=True,error_message="账号异常！")
    all_conditions = [
        UserInfo.user_company_id == target_user.user_company_id
    ]
    if register_start_date:
        all_conditions.append(
            UserInfo.create_time >= datetime.strptime(register_start_date, '%Y-%m-%d %H:%M:%S')
        )
    if register_end_date:
        all_conditions.append(
            UserInfo.create_time <= datetime.strptime(register_end_date, '%Y-%m-%d %H:%M:%S')
        )
    if user_department_id:
        all_conditions.append(
            UserInfo.user_department_id.in_(user_department_id)
        )
    if search_text:
        all_conditions.append(
            or_(
                UserInfo.user_id == search_text_int,
                UserInfo.user_name.like(f"%{search_text}%"),
                UserInfo.user_nick_name_py.like(f"%{search_text}%"),
                UserInfo.user_email.like(f"%{search_text}%"),
            )
        )
    if is_archive == 0:
        all_conditions.append(
            UserInfo.user_status == 1
        )
    else:
        all_conditions.append(
            UserInfo.user_status < 0
        )

    all_colleagues = UserInfo.query.filter(
        *all_conditions
    )
    total = all_colleagues.count()
    all_colleagues = all_colleagues.paginate(page=page_num, per_page=page_size, error_out=False)
    all_colleagues_ids = [user.user_id for user in all_colleagues]
    role_condition = []
    if role_desc:
        role_condition.append(
            RoleInfo.role_desc.in_(role_desc)
        )
    role_desc_res = UserInfo.query.filter(
        UserInfo.user_id.in_(all_colleagues_ids)
    ).join(
        UserRoleInfo,
        UserRoleInfo.user_id == UserInfo.user_id
    ).filter(
        UserRoleInfo.rel_status == 1
    ).with_entities(
        UserInfo,
        UserRoleInfo.role_id
    ).join(
        RoleInfo,
        RoleInfo.role_id == UserRoleInfo.role_id
    ).filter(
        RoleInfo.status == 1,
        *role_condition
    ).with_entities(
        UserInfo,
        RoleInfo
    ).all()
    role_desc_map = {}
    for user, role in role_desc_res:
        if user.user_id not in role_desc_map:
            role_desc_map[user.user_id] = role.role_desc
        else:
            role_desc_map[user.user_id] += f",{role.role_desc}"

    all_user_departments = DepartmentInfo.query.filter(
        DepartmentInfo.company_id == target_user.user_company_id,
        DepartmentInfo.department_status == "正常"
    ).all()
    all_user_departments_maps = {
        department.id: department.department_name
        for department in all_user_departments
    }
    all_role_desc = RoleInfo.query.filter(
        RoleInfo.status == 1
    ).all()
    data = []
    for colleague in all_colleagues:
        sub_data = colleague.to_dict()
        if role_desc and not role_desc_map.get(colleague.user_id):
            total += -1
            continue
        sub_data["role_desc"] = role_desc_map.get(colleague.user_id)
        sub_data["is_archive"] = False if colleague.user_status == 1 else True
        sub_data["user_department"] = all_user_departments_maps.get(colleague.user_department_id)
        data.append(sub_data)
    return next_console_response(result={
        "total": total,
        "data": data,
        "user_departments": [department.to_dict() for department in all_user_departments],
        "role_desc": [role.role_desc for role in all_role_desc],
                    })


def update_user_role_admin(params):
    """
    管理员直接修改用户角色
    """
    user_id = int(params.get("user_id"))
    update_user_id = params.get("update_user_id")
    dest_role_desc = params.get("dest_role_desc")
    # 同时需要判断 user_id 和 update_user_id 的企业是否一致
    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="账号异常！")
    request_user_roles = UserRoleInfo.query.filter(
        UserRoleInfo.user_id == user_id,
        UserRoleInfo.rel_status == 1
    ).join(
        RoleInfo, RoleInfo.role_id == UserRoleInfo.role_id
    ).filter(
        RoleInfo.status == 1
    ).with_entities(
        RoleInfo
    ).all()
    request_user_role_name = [role.role_name for role in request_user_roles]
    if "super_admin" not in request_user_role_name and "next_console_admin" not in request_user_role_name:
        return next_console_response(error_status=True, error_message="权限不足！")

    update_user = UserInfo.query.filter(
        UserInfo.user_id == update_user_id,
        UserInfo.user_status == 1,
        UserInfo.user_company_id == request_user.user_company_id
    ).first()
    if not update_user:
        return next_console_response(error_status=True, error_message="账号异常！")

    dest_role = RoleInfo.query.filter(
        RoleInfo.role_desc.in_(dest_role_desc),
        RoleInfo.status == 1
    ).all()
    all_dest_role_id = [role.role_id for role in dest_role]
    if not all_dest_role_id:
        return next_console_response(error_status=True, error_message="角色异常！")
    all_desc_role_names = [role.role_name for role in dest_role]
    if "next_console_admin" not in request_user_role_name and (
        "next_console_admin" in all_desc_role_names or "super_admin" in all_desc_role_names
    ):
        return next_console_response(error_status=True, error_message="权限不足！")
    # 获取 update_user_id 的当前所有角色，形成list
    all_role_rels = UserRoleInfo.query.filter(
        UserRoleInfo.user_id == update_user_id,
        UserRoleInfo.rel_status == 1
    ).all()
    all_current_role_id = [role.role_id for role in all_role_rels]
    new_roles_ids = list(set(all_dest_role_id) - set(all_current_role_id))
    del_roles_ids = list(set(all_current_role_id) - set(all_dest_role_id))
    for new_role_id in new_roles_ids:
        new_role_rel = UserRoleInfo(
            user_id=update_user_id,
            role_id=new_role_id,
            rel_status=1
        )
        db.session.add(new_role_rel)
    for del_role_id in del_roles_ids:
        del_role_rel = UserRoleInfo.query.filter(
            UserRoleInfo.user_id == update_user_id,
            UserRoleInfo.role_id == del_role_id
        ).first()
        db.session.delete(del_role_rel)
    db.session.commit()
    return next_console_response(result=dest_role_desc)


def update_user_status_admin(params):
    """
    管理员直接修改用户归档状态
    """
    user_id = int(params.get("user_id"))
    update_user_id = params.get("update_user_id")
    dest_is_archive = params.get("dest_is_archive")
    # 同时需要判断 user_id 和 update_user_id 的企业是否一致
    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="账号异常！")
    update_user = UserInfo.query.filter(
        UserInfo.user_id == update_user_id,
    ).first()
    if not update_user:
        return next_console_response(error_status=True, error_message="账号异常！")
    plus_require_role_rel = RoleInfo.query.filter(
        RoleInfo.role_name == "next_console_admin",
        RoleInfo.status == 1
    ).join(
        UserRoleInfo, UserRoleInfo.role_id == RoleInfo.role_id
    ).filter(
        UserRoleInfo.user_id == user_id,
        UserRoleInfo.rel_status == 1
    ).first()
    if not plus_require_role_rel:
        return next_console_response(error_status=True, error_message="权限不足！")
    try:
        if dest_is_archive == 0:
            update_user.user_status = 1
        else:
            update_user.user_status = -1
        db.session.add(update_user)
        db.session.commit()
        return next_console_response(result=update_user.to_dict())
    except Exception as e:
        db.session.rollback()
        return next_console_response(error_status=True, error_code=2001, error_message=f"更新用户归档状态失败！{e}")


def update_user_company_admin(params):
    """
    管理员直接修改用户公司
    """
    user_id = int(params.get("user_id"))
    update_user_id = params.get("update_user_id")
    dest_company_id = params.get("dest_company_id")
    dest_department_id = params.get("dest_department_id")
    user_account_type = params.get("user_account_type")

    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="当前请求账号异常！")
    update_user = UserInfo.query.filter(
        UserInfo.user_id == update_user_id,
    ).first()
    if not update_user:
        return next_console_response(error_status=True, error_message="待更新账号异常！")
    plus_require_role_rel = RoleInfo.query.filter(
        RoleInfo.role_name == "next_console_admin",
        RoleInfo.status == 1
    ).join(
        UserRoleInfo, UserRoleInfo.role_id == RoleInfo.role_id
    ).filter(
        UserRoleInfo.user_id == user_id,
        UserRoleInfo.rel_status == 1
    ).first()
    if not plus_require_role_rel:
        return next_console_response(error_status=True, error_message="权限不足！")
    if not user_account_type:
        return next_console_response(error_status=True, error_message="账号类型不能为空！")
    if user_account_type == "企业账号":
        # 判断公司是否存在
        dest_company = CompanyInfo.query.filter(
            CompanyInfo.id == dest_company_id,
            CompanyInfo.company_status == "正常"
        ).first()
        if not dest_company:
            return next_console_response(error_status=True, error_message="目标公司不存在或非正常状态！")
        # 判断公司的部门是否存在
        dest_department = DepartmentInfo.query.filter(
            DepartmentInfo.id == dest_department_id,
            DepartmentInfo.company_id == dest_company_id,
            DepartmentInfo.department_status == "正常"
        ).first()
        if not dest_department:
            return next_console_response(error_status=True, error_message="目标公司的目标部门不存在或非正常状态！")
        try:
            update_user.user_account_type = user_account_type
            update_user.user_company = dest_company.company_name
            update_user.user_company_id = dest_company_id
            update_user.user_department = dest_department.department_name
            update_user.user_department_id = dest_department_id
            db.session.add(update_user)
            db.session.commit()
            return next_console_response(result=update_user.to_dict())
        except Exception as e:
            db.session.rollback()
            return next_console_response(error_status=True, error_code=2001, error_message=f"更新用户所属公司部门失败！{e}")
    else:
        return next_console_response(error_status=True, error_message= f"不支持修改为当前账号类型：{user_account_type}！")
    

def search_all_company():
    """
    查询所有企业并去重
    """
    try:
        all_company = CompanyInfo.query.filter(
            CompanyInfo.company_status == "正常"
        ).all()
        all_company = [company.to_dict() for company in all_company]
        return next_console_response(result=all_company)
    except Exception as e:
        return next_console_response(error_status=True, error_code=2001, error_message=f"查询企业信息失败！{e}")


def create_user(params):
    """
    创建用户
    """
    user_id = int(params.get("user_id"))
    user_name = params.get("user_name")
    user_nickname = params.get("user_nickname", user_name)
    user_nick_name_py = get_initial_py(user_nickname)
    user_email = params.get("user_email", '')
    user_phone = params.get("user_phone", '')
    user_password = params.get("user_password", str(uuid.uuid4()))
    user_password = hashlib.sha256(user_password.encode()).hexdigest()
    user_password = generate_password_hash(user_password)
    user_gender = params.get("user_gender", '')
    user_resource_limit = params.get("user_resource_limit", 2048)
    user_position = params.get("user_position", '')
    user_company_id = params.get("user_company_id")
    user_department_id = params.get("user_department_id")
    user_account_type = "个人账号"
    user_age = 22
    exist_user = UserInfo.query.filter(
        UserInfo.user_name == user_name,
        UserInfo.user_status == 1
    ).first()
    if exist_user:
        return next_console_response(error_status=True, error_message="用户名已存在！")
    if user_email:
        exist_user = UserInfo.query.filter(UserInfo.user_email == user_email).first()
        if exist_user:
            return next_console_response(error_status=True, error_message="邮箱已存在！")
    if user_phone:
        exist_user = UserInfo.query.filter(UserInfo.user_phone == user_phone).first()
        if exist_user:
            return next_console_response(error_status=True, error_message="手机号已存在！")
    admin_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    user_roles = UserRoleInfo.query.filter(UserRoleInfo.user_id == user_id).all()
    all_role_ids = [role.role_id for role in user_roles]
    all_roles = RoleInfo.query.filter(RoleInfo.role_id.in_(all_role_ids)).all()
    user_roles = [role.role_name for role in all_roles]
    if user_company_id:
        user_account_type = "企业账号"
        if "next_console_admin" not in user_roles:
            user_company_id = admin_user.user_company_id
        else:
            dest_company = CompanyInfo.query.filter(
                CompanyInfo.id == user_company_id,
                CompanyInfo.company_status == "正常"
            ).first()
            if not dest_company:
                return next_console_response(error_status=True, error_message="目标公司不存在或非正常状态！")
        root_department = DepartmentInfo.query.filter(
            DepartmentInfo.company_id == user_company_id,
            DepartmentInfo.parent_department_id.is_(None)
        ).first()
        if not root_department:
            return next_console_response(error_status=True, error_message="企业不存在根部门！")
        if not user_department_id:
            user_department_id = root_department.id
        else:
            # 判断公司的部门是否存在
            dest_department = DepartmentInfo.query.filter(
                DepartmentInfo.id == user_department_id,
                DepartmentInfo.company_id == user_company_id,
                DepartmentInfo.department_status == "正常"
            ).first()
            if not dest_department:
                return next_console_response(error_status=True, error_message="目标公司的目标部门不存在或非正常状态！")
    new_user = UserInfo(
        user_name=user_name,
        user_password=user_password,
        user_nick_name=user_nickname,
        user_nick_name_py=user_nick_name_py,
        user_email=user_email,
        user_phone=user_phone,
        user_gender=user_gender,
        user_age=user_age,
        user_position=user_position,
        user_resource_limit=user_resource_limit,
        user_status=1,
        user_account_type=user_account_type,
        user_company_id=user_company_id,
        user_department_id=user_department_id,
        user_source='admin',
        user_code=str(uuid.uuid4()),
    )
    db.session.add(new_user)
    db.session.commit()
    init_user(new_user, False, False)
    admin_notice_new_user.delay([new_user.to_dict()])
    app.logger.warning(f"管理员：{admin_user.user_id} 角色：{user_roles} ，创建新用户:{new_user}")
    return next_console_response(result=new_user.to_dict())


