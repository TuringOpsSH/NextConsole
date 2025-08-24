from app.services.user_center.users import *

def lookup_company_twadmin(params):
    """
    平台管理员查询企业信息
    """
    user_id = int(params.get("user_id"))
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 20)
    search_text = params.get("search_text")
    company_status = params.get("company_status")
    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="当前请求账号异常！")
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
    # 搜索条件构造
    all_conditions = []
    if search_text:
        all_conditions.append(or_(
            CompanyInfo.id == search_text,
            CompanyInfo.company_code.like(f"%{search_text}%"),
            CompanyInfo.company_name.like(f"%{search_text}%"),
            CompanyInfo.company_country.like(f"%{search_text}%"),
            CompanyInfo.company_area.like(f"%{search_text}%")
        ))
    if company_status:
        all_conditions.append(CompanyInfo.company_status == company_status)
    # 查询数据
    all_companies = CompanyInfo.query.filter(
        *all_conditions
    )
    total = all_companies.count()
    companies = all_companies.paginate(page=page_num, per_page=page_size, error_out=False)
    return next_console_response(result={
        "total": total,
        "data": [company.to_dict() for company in companies.items]
    })



def add_company_twadmin(params):
    """
    平台管理员新增公司信息
    """
    user_id = int(params.get("user_id"))
    parent_company_id = params.get("parent_company_id")
    company_code = params.get("company_code")
    company_name = params.get("company_name")
    company_country = params.get("company_country", "")
    company_area = params.get("company_area", "")
    company_industry = params.get("company_industry", "")
    company_scale = params.get("company_scale", "")
    company_desc = params.get("company_desc", "")
    company_address = params.get("company_address", "")
    company_phone = params.get("company_phone", "")
    company_email = params.get("company_email", "")
    company_website = params.get("company_website", "")
    company_logo = params.get("company_logo", "")
    company_type = params.get("company_type", "")

    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="当前请求账号异常！")
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
    if not company_code:
        return next_console_response(error_status=True, error_message="公司编码不能为空！")
    if not company_name:
        return next_console_response(error_status=True, error_message="公司名称不能为空！")
    company_code_exist = CompanyInfo.query.filter(
        CompanyInfo.company_code == company_code
    ).first()
    if company_code_exist:
        return next_console_response(error_status=True, error_message="公司编码已存在！")
    company_name_exist = CompanyInfo.query.filter(
        CompanyInfo.company_name == company_name,
        CompanyInfo.company_status == '正常'
    ).first()
    if company_name_exist:
        return next_console_response(error_status=True, error_message="公司名称已存在！")
    if parent_company_id:
        dest_company = CompanyInfo.query.filter(
            CompanyInfo.id == parent_company_id,
            CompanyInfo.company_status == "正常"
        ).first()
        if not dest_company:
            return next_console_response(error_status=True, error_message="父公司不存在或非正常状态！")
    # 先创建公司，然后创建默认公司部门
    try:
        new_company = CompanyInfo(
            parent_company_id=parent_company_id,
            company_code=company_code, company_name=company_name,
            company_country=company_country, company_area=company_area,
            company_industry=company_industry, company_scale=company_scale,
            company_desc=company_desc, company_address=company_address,
            company_phone=company_phone, company_email=company_email,
            company_website=company_website, company_logo=company_logo,
            company_type=company_type,
            company_status="正常"
        )
        db.session.add(new_company)
        db.session.flush()  # 提交但不commit，获取新创建公司的ID

        # 创建默认根部门，与公司同名
        default_department = DepartmentInfo(
            company_id=new_company.id,
            department_name=company_name,  # 部门名称与公司名称一致
            parent_department_id=None,  # 根部门没有父部门
            department_code=f"{company_code}-ROOT",  # 根部门编码
            department_desc=f"{company_name}的根部门",
            department_logo = company_logo,  # 使用公司logo
            department_status = "正常"
        )
        db.session.add(default_department)
        db.session.commit()
        app.logger.info(f'用户({user_id})成功创建公司({new_company.id})及其默认根部门({default_department.id})')
        # 返回公司信息，包含新创建的默认部门ID
        company_result = new_company.to_dict()
        company_result["default_department_id"] = default_department.id
        return next_console_response(result=company_result)
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'用户({user_id})添加公司及默认部门失败！错误: {e}')
        return next_console_response(error_status=True, error_message=f"添加公司及默认部门失败！{e}")


def update_company_twadmin(params):
    """
    平台管理员更新公司信息
    """
    user_id = int(params.get("user_id"))
    company_id = params.get("company_id")
    parent_company_id = params.get("parent_company_id")
    company_code = params.get("company_code")
    company_name = params.get("company_name")

    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="当前请求账号异常！")
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
    if not company_id:
        return next_console_response(error_status=True, error_message="公司ID不能为空！")
    dest_company = CompanyInfo.query.filter(
        CompanyInfo.id == company_id,
        CompanyInfo.company_status == "正常"
    ).first()
    if not dest_company:
        return next_console_response(error_status=True, error_message="目标公司不存在或非正常状态！")
    if parent_company_id:
        dest_company = CompanyInfo.query.filter(
            CompanyInfo.id == parent_company_id,
            CompanyInfo.company_status == "正常"
        ).first()
        if not dest_company:
            return next_console_response(error_status=True, error_message="母公司不存在或非正常状态！")
    # 企业编号 企业名称不可重复
    company_code_exist = CompanyInfo.query.filter(
        CompanyInfo.company_code == company_code,
        CompanyInfo.id != company_id
    ).first()
    if company_code_exist:
        return next_console_response(error_status=True, error_message="不可修改为已存在的公司编码！")
    company_name_exist = CompanyInfo.query.filter(
        CompanyInfo.company_name == company_name,
        CompanyInfo.id != company_id
    ).first()
    if company_name_exist:
        return next_console_response(error_status=True, error_message="不可修改为已存在的公司名称！")
    # 只更新非空字段
    try:
        update_fields = {}
        # 定义公司模型可更新的字段列表
        company_fields = [
            "parent_company_id", "company_code", "company_name", "company_country",
            "company_area", "company_industry", "company_scale", "company_desc",
            "company_address", "company_phone", "company_email", "company_website",
            "company_logo", "company_type", "company_status"
        ]
        # 从params中提取非空字段
        for field in company_fields:
            if field in params and params[field] is not None:
                update_fields[field] = params[field]
        # 更新公司信息
        company = CompanyInfo.query.get(company_id)
        for field, value in update_fields.items():
            # 如果是_id字段，空字符串转为None
            if field.endswith("_id"):
                value = value if value else None
            setattr(company, field, value)
        db.session.commit()
        app.logger.info(f'用户({user_id})成功更新公司({company_id})信息')
        return next_console_response(result=company.to_dict())
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'用户({user_id})更新公司({company_id})信息失败！错误: {e}')
        return next_console_response(error_status=True, error_message=f"更新公司信息失败！{e}")


def delete_company_twadmin(params):
    """
    todo 平台管理员删除公司信息,需注意子公司的迁移，企业用户的清理，企业部门的清理
    """
    pass


def lookup_department_twadmin(params):
    """
    平台管理员查询部门信息
    """
    user_id = int(params.get("user_id"))
    search_text = params.get("search_text")
    department_status = params.get("department_status")
    company_id = params.get("company_id")
    parent_department_id = params.get("parent_department_id")
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 100)
    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="当前请求账号异常！")
    plus_require_role_rel = RoleInfo.query.filter(
        RoleInfo.role_name == "next_console_admin",
        RoleInfo.status == 1
    ).join(
        UserRoleInfo, UserRoleInfo.role_id == RoleInfo.role_id
    ).filter(
        UserRoleInfo.user_id == user_id,
        UserRoleInfo.rel_status == 1
    ).first()
    # 搜索条件构造
    all_conditions = []
    if search_text:
        all_conditions.append(or_(
            DepartmentInfo.id == search_text,
            DepartmentInfo.department_code.like(f"%{search_text}%"),
            DepartmentInfo.department_name.like(f"%{search_text}%"),
            DepartmentInfo.department_desc.like(f"%{search_text}%")
        ))
    if department_status:
        all_conditions.append(DepartmentInfo.department_status == department_status)
    if plus_require_role_rel:
        if company_id:
            all_conditions.append(DepartmentInfo.company_id == company_id)
    else:
        all_conditions.append(DepartmentInfo.company_id == request_user.user_company_id)
    if parent_department_id:
        all_conditions.append(DepartmentInfo.parent_department_id == parent_department_id)
    # 查询数据
    all_departments = DepartmentInfo.query.filter(
        *all_conditions
    )
    total = all_departments.count()
    all_departments = all_departments.paginate(page=page_num, per_page=page_size, error_out=False)
    return next_console_response(result={
        "total": total,
        "data": [department.to_dict() for department in all_departments]
    })


def lookup_department_admin(params):
    """
    平台管理员查询公司部门信息
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    search_text = params.get("search_text")
    department_status = params.get("department_status")
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 100)
    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="当前请求账号异常！")
    # 搜索条件构造
    all_conditions = [
        DepartmentInfo.company_id == request_user.user_company_id
    ]
    if search_text:
        all_conditions.append(or_(
            DepartmentInfo.id == search_text,
            DepartmentInfo.department_code.like(f"%{search_text}%"),
            DepartmentInfo.department_name.like(f"%{search_text}%"),
            DepartmentInfo.department_desc.like(f"%{search_text}%")
        ))
    if department_status:
        all_conditions.append(DepartmentInfo.department_status == department_status)
    # 查询数据
    all_departments = DepartmentInfo.query.filter(
        *all_conditions
    )
    total = all_departments.count()
    all_departments = all_departments.paginate(page=page_num, per_page=page_size, error_out=False)
    return next_console_response(result={
        "total": total,
        "data": [department.to_dict() for department in all_departments]
    })


def add_department_twadmin(params):
    """
    平台管理员添加公司部门信息
    """
    user_id = int(params.get("user_id"))
    company_id = params.get("company_id")
    parent_department_id = params.get("parent_department_id")
    department_code = params.get("department_code")
    department_name = params.get("department_name")
    department_desc = params.get("department_desc", "")
    department_logo = params.get("department_logo", "")
    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="当前请求账号异常！")
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
    if not department_code:
        return next_console_response(error_status=True, error_message="部门编码不能为空！")
    if not department_name:
        return next_console_response(error_status=True, error_message="部门名称不能为空！")
    if not company_id:
        return next_console_response(error_status=True, error_message="公司ID不能为空！")
    dest_company = CompanyInfo.query.filter(
        CompanyInfo.id == company_id,
        CompanyInfo.company_status == "正常"
    ).first()
    if not dest_company:
        return next_console_response(error_status=True, error_message="目标公司不存在或非正常状态！")
    department_code_exist = DepartmentInfo.query.filter(
        DepartmentInfo.department_code == department_code
    ).first()
    if department_code_exist:
        return next_console_response(error_status=True, error_message="部门编码已存在！")
    department_name_exist = DepartmentInfo.query.filter(
        DepartmentInfo.department_name == department_name,
        DepartmentInfo.company_id == company_id,
        DepartmentInfo.department_status == '正常'
    ).first()
    if department_name_exist:
        return next_console_response(error_status=True, error_message="部门名称已存在！")
    if parent_department_id:
        dest_department = DepartmentInfo.query.filter(
            DepartmentInfo.id == parent_department_id,
            DepartmentInfo.department_status == "正常"
        ).first()
        if not dest_department:
            return next_console_response(error_status=True, error_message="父部门不存在或非正常状态！")
    try:
        new_department = DepartmentInfo(
            company_id=company_id,
            department_name=department_name,
            parent_department_id=parent_department_id if parent_department_id else None,
            department_code=department_code,
            department_desc=department_desc,
            department_logo=department_logo,
            department_status="正常"
        )
        db.session.add(new_department)
        db.session.commit()
        return next_console_response(result=new_department.to_dict())
    except Exception as e:
        app.logger.error(f'用户({user_id})添加部门失败！{e}')
        return next_console_response(error_status=True, error_message="添加部门失败！")


def update_department_twadmin(params):
    """
    平台管理员更新公司部门信息
    """
    user_id = int(params.get("user_id"))
    department_id = params.get("department_id")
    company_id = params.get("company_id")
    parent_department_id = params.get("parent_department_id")
    department_code = params.get("department_code")
    department_name = params.get("department_name")

    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="当前请求账号异常！")
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
    if not department_id:
        return next_console_response(error_status=True, error_message="部门ID不能为空！")
    dest_department = DepartmentInfo.query.filter(
        DepartmentInfo.id == department_id,
        DepartmentInfo.department_status == "正常"
    ).first()
    if not dest_department:
        return next_console_response(error_status=True, error_message="目标部门不存在或非正常状态！")

    def check_department_loop(current_id, target_parent_id):
        """
        使用BFS检查是否形成部门循环引用，避免在已有闭环数据中陷入死循环

        Args:
            current_id: 当前部门ID
            target_parent_id: 目标父部门ID

        Returns:
            tuple: (bool, str) - (是否存在循环引用, 错误信息)
        """
        # 已访问的部门ID集合，用于检测现有数据中的循环
        visited = set()
        # 待访问的部门队列
        queue = [(current_id, [current_id])]
        # 设置最大迭代次数，防止因数据异常导致死循环
        max_iterations = 1000
        iteration_count = 0
        while queue and iteration_count < max_iterations:
            dept_id, current_path = queue.pop(0)
            iteration_count += 1
            # 如果找到目标父部门，说明形成循环引用
            if dept_id == target_parent_id:
                path_str = " -> ".join(map(str, current_path + [target_parent_id]))
                return True, f"检测到循环引用：{path_str}"
            # 如果当前部门已访问过，说明现有数据中存在循环
            if dept_id in visited:
                return True, "数据库中已存在部门循环引用，请联系管理员处理！"
            # 标记为已访问
            visited.add(dept_id)
            # 获取所有子部门
            children = DepartmentInfo.query.filter(
                DepartmentInfo.parent_department_id == dept_id,
                DepartmentInfo.department_status == "正常"
            ).all()
            # 将子部门加入队列，同时更新路径
            for child in children:
                if child.id not in visited:
                    new_path = current_path + [child.id]
                    queue.append((child.id, new_path))
        # 超过最大迭代次数
        if iteration_count >= max_iterations:
            return True, f"检测部门关系时超出最大迭代次数({max_iterations})，数据可能存在异常，请联系管理员处理！"
        # 未找到循环引用
        return False, ""
    if parent_department_id:
        if not isinstance(parent_department_id, int):
            try:
                parent_department_id = int(parent_department_id)
            except (TypeError, ValueError):
                return next_console_response(error_status=True, error_message="父部门ID格式不正确！")
        if dest_department.parent_department_id is None:
            return next_console_response(error_status=True, error_message="根部门不能设置父部门！")
        if dest_department.id == parent_department_id:
            return next_console_response(error_status=True, error_message="父部门不能设置为自己！")
        dest_parent_department = DepartmentInfo.query.filter(
            DepartmentInfo.id == parent_department_id,
            DepartmentInfo.department_status == "正常"
        ).first()
        if not dest_parent_department:
            return next_console_response(error_status=True, error_message="父部门不存在或非正常状态！")
        # 父部门不可以是部门的子部门以及其递归子部门
        has_loop, error_msg = check_department_loop(department_id, parent_department_id)
        if has_loop:
            return next_console_response(
                error_status=True,
                error_message=error_msg
            )
    else:
        # 非根部门不能设置父部门为None
        if dest_department.parent_department_id is not None:
            return next_console_response(error_status=True, error_message="非根部门必须设置父部门！")
    # 部门编号 部门名称不可重复
    department_code_exist = DepartmentInfo.query.filter(
        DepartmentInfo.department_code == department_code,
        DepartmentInfo.id != department_id
    ).first()
    if department_code_exist:
        return next_console_response(error_status=True, error_message="不可修改为已存在的部门编码！")
    department_name_exist = DepartmentInfo.query.filter(
        DepartmentInfo.department_name == department_name,
        DepartmentInfo.company_id == dest_department.company_id,
        DepartmentInfo.id != department_id
    ).first()
    if department_name_exist:
        return next_console_response(error_status=True, error_message="不可修改为已存在的部门名称！")
    # 只更新非空字段
    try:
        update_fields = {}
        # 定义部门模型可更新的字段列表
        department_fields = [
            "company_id", "parent_department_id", "department_code", "department_name",
            "department_desc", "department_logo", "department_status"
        ]
        # 从params中提取非空字段
        for field in department_fields:
            if field in params and params[field] is not None:
                update_fields[field] = params[field]
        # 更新部门信息
        department = DepartmentInfo.query.get(department_id)
        for field, value in update_fields.items():
            # 如果是_id字段，空字符串转为None
            if field.endswith("_id"):
                value = value if value else None
            setattr(department, field, value)
        db.session.commit()
        app.logger.info(f'用户({user_id})成功更新部门({department_id})信息')
        return next_console_response(result=department.to_dict())
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'用户({user_id})更新部门({department_id})信息失败！错误: {e}')
        return next_console_response(error_status=True, error_message=f"更新部门信息失败！{e}")


def delete_department_twadmin(params):
    """
    todo 平台管理员删除公司部门信息,需注意部门下的用户迁移，部门下的子部门迁移
    """
    pass