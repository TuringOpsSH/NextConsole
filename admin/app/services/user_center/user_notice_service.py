from app.models.user_center.user_info import *
from app.services.configure_center.response_utils import next_console_response
from sqlalchemy import or_, func, case
from datetime import datetime
from app.models.contacts.company_model import *
from app.models.contacts.department_model import *
from app.services.task_center.user_notice import *
from app.app import celery


def list_task_info(params):
    """
    列出通知任务清单
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 10)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)

    all_history_data = NoticeTaskInfo.query.filter(
        NoticeTaskInfo.task_status != "已删除"
    ).order_by(
        NoticeTaskInfo.create_time.desc()
    )
    total = all_history_data.count()
    data = all_history_data.paginate(page=page_num, per_page=page_size, error_out=False)
    all_page_task_id = [i.id for i in data.items]
    all_task_instance_count = NoticeTaskInstance.query.filter(
        NoticeTaskInstance.task_id.in_(all_page_task_id)
    ).with_entities(
        NoticeTaskInstance.task_id,
        func.count(NoticeTaskInstance.id).label("instance_count")
    ).group_by(
        NoticeTaskInstance.task_id
    ).all()
    instance_count_dict = {i.task_id: i.instance_count for i in all_task_instance_count}
    result = {
        "page_num": page_num,
        "page_size": page_size,
        "total": total,
        "data": []
    }
    for i in data:
        sub_i = i.to_dict()
        if i.task_instance_total:
            sub_i["task_progress"] = round(
                i.task_instance_success/i.task_instance_total * 100, 2
            )
        else:
            sub_i["task_progress"] = 0.00
        sub_i["instance_count"] = instance_count_dict.get(i.id, 0)
        result["data"].append(sub_i)
    return next_console_response(result=result)


def search_task_info(params):
    """
    搜索通知任务
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 10)
    fetch_all = params.get("fetch_all", False)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    keyword = params.get("keyword")
    task_status = params.get("task_status", [])
    notice_type = params.get("notice_type", [])
    all_condition = [
        NoticeTaskInfo.task_status != "已删除"
    ]
    if keyword:
        all_condition.append(
            or_(
                NoticeTaskInfo.task_name.like(f"%{keyword}%"),
                NoticeTaskInfo.task_desc.like(f"%{keyword}%")
            )
        )
    if task_status:
        all_condition.append(
            NoticeTaskInfo.task_status.in_(task_status)
        )
    if notice_type:
        all_condition.append(
            NoticeTaskInfo.notice_type.in_(notice_type)
        )
    all_history_data = NoticeTaskInfo.query.filter(
        *all_condition
    ).order_by(
        NoticeTaskInfo.create_time.desc()
    )
    total = all_history_data.count()
    if not fetch_all:
        data = all_history_data.paginate(page=page_num, per_page=page_size, error_out=False)
    else:
        data = all_history_data.all()
    result = {
        "page_num": page_num,
        "page_size": page_size,
        "total": total,
        "data": [i.to_dict() for i in data]
    }
    return next_console_response(result=result)


def add_task_info(params):
    """
    添加通知任务
    :param params:
    :return:
    """
    return next_console_response()


def del_task_info(params):
    """
    删除通知任务, 逻辑删除, 实例数据不动
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    task_id = params.get("task_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    target_task = NoticeTaskInfo.query.filter(
        NoticeTaskInfo.id == task_id
    ).first()
    if target_task.task_status == "执行中":
        return next_console_response(error_status=True, error_message="任务状态不允许删除！", error_code=1001)
    target_task.task_status = "已删除"
    db.session.add(target_task)
    db.session.commit()
    return next_console_response()


def init_task_info(params):
    """
    初始化通知任务
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    new_task = NoticeTaskInfo(
        user_id=user_id,
        task_name="",
        task_desc="",
        notice_type="",
        notice_template="",
        notice_params={},
        task_status="新建中",
    )
    db.session.add(new_task)
    db.session.commit()
    return next_console_response(result=new_task.to_dict())


def get_task_detail_info(params):
    """
    获取通知任务详情
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    task_id = params.get("task_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    target_task = NoticeTaskInfo.query.filter(
        NoticeTaskInfo.id == task_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在！", error_code=1001)
    return next_console_response(result=target_task.to_dict())


def update_task_info(params):
    """
    更新通知任务详情
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    task_id = params.get("task_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    target_task = NoticeTaskInfo.query.filter(
        NoticeTaskInfo.id == task_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在！", error_code=1001)
    if target_task.task_status != "新建中":
        return next_console_response(error_status=True, error_message="任务状态不允许修改！", error_code=1001)
    task_name = params.get("task_name")
    task_desc = params.get("task_desc")
    notice_type = params.get("notice_type")
    notice_template = params.get("notice_template")
    notice_params = params.get("notice_params")
    plan_begin_time = params.get("plan_begin_time")
    plan_finish_time = params.get("plan_finish_time")
    run_now = params.get("run_now")
    batch_size = params.get("batch_size")
    target_task.task_name = task_name
    target_task.task_desc = task_desc
    target_task.notice_type = notice_type
    target_task.notice_template = notice_template
    target_task.notice_params = notice_params
    if plan_begin_time:
        try:
            plan_begin_time = datetime.fromisoformat(plan_begin_time.replace('Z', '+00:00'))
        except Exception as e:
            return next_console_response(error_status=True, error_message="计划开始时间格式错误！", error_code=1001)
        target_task.plan_begin_time = plan_begin_time
    if plan_finish_time:
        try:
            plan_finish_time = datetime.fromisoformat(plan_finish_time.replace('Z', '+00:00'))
        except Exception as e:
            return next_console_response(error_status=True, error_message="计划结束时间格式错误！", error_code=1001)
        target_task.plan_finish_time = plan_finish_time
    if run_now is not None:
        target_task.run_now = run_now
    try:
        batch_size = int(batch_size)
    except Exception as e:
        return next_console_response(error_status=True, error_message="批量大小格式错误！", error_code=1001)
    target_task.task_instance_batch_size = batch_size
    db.session.add(target_task)
    db.session.commit()
    return next_console_response(result=target_task.to_dict())


def search_company(params):
    """
    搜索公司
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)

    keyword = params.get("keyword")
    target_companies = CompanyInfo.query.filter(
        or_(
            CompanyInfo.company_name.like(f"%{keyword}%"),
            CompanyInfo.company_desc.like(f"%{keyword}%")
        ),
        CompanyInfo.company_status == '正常'
    ).order_by(
        CompanyInfo.create_time.desc()
    ).all()
    result = [i.to_dict() for i in target_companies]
    res = {
        "data": result,
        "total": len(result)
    }
    return next_console_response(result=res)


def search_department(params):
    """
    搜索部门
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)

    keyword = params.get("keyword")
    target_departments = DepartmentInfo.query.filter(
        or_(
            DepartmentInfo.department_name.like(f"%{keyword}%"),
            DepartmentInfo.department_desc.like(f"%{keyword}%")
        ),
        DepartmentInfo.department_status == '正常'
    ).order_by(
        DepartmentInfo.create_time.desc()
    ).all()
    result = [i.to_dict() for i in target_departments]
    res = {
        "data": result,
        "total": len(result)
    }
    return next_console_response(result=res)


def search_user(params):
    """
    搜索用户
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)

    keyword = params.get("keyword")
    target_users = UserInfo.query.filter(
        or_(
            UserInfo.user_nick_name.like(f"%{keyword}%"),
            UserInfo.user_email.like(f"%{keyword}%"),
            UserInfo.user_phone.like(f"%{keyword}%"),
        ),
        UserInfo.user_status == 1,
    ).order_by(
        UserInfo.create_time.desc()
    ).all()
    result = [i.to_dict() for i in target_users]
    res = {
        "data": result,
        "total": len(result)
    }
    return next_console_response(result=res)


def start_task_info(params):
    """
    开始通知任务
    """
    user_id = int(params.get("user_id"))
    task_id = params.get("task_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    target_task = NoticeTaskInfo.query.filter(
        NoticeTaskInfo.id == task_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在！", error_code=1001)
    if target_task.task_status != "新建中":
        return next_console_response(error_status=True, error_message="任务状态不允许执行！", error_code=1001)
    # 任务前检查
    if not target_task.run_now and not target_task.plan_begin_time:
        return next_console_response(error_status=True, error_message="任务未设置执行时间！", error_code=1001)
    if not target_task.notice_type:
        return next_console_response(error_status=True, error_message="任务未设置通知类型！", error_code=1001)
    if not target_task.notice_template:
        return next_console_response(error_status=True, error_message="任务未设置通知模板！", error_code=1001)

    # 筛选出通知对象
    target_users = filter_notice_users(target_task)
    # 创建任务实例数据
    task_list = []
    for i in target_users:
        try:
            receive_user_id = i.user_id
        except Exception as e:
            receive_user_id = -1
        if target_task.notice_type == "邮件" and not i.user_email:
            continue
        if target_task.notice_type == "短信" and not i.user_phone:
            continue
        if target_task.notice_type == "站内信" and not i.user_id:
            continue
        new_task = NoticeTaskInstance(
            task_id=task_id,
            receive_user_id=receive_user_id,
            notice_status="排队中",
            task_celery_id="",
            notice_params={
                "user_email": i.user_email,
                "user_phone": i.user_phone,
                "subject": target_task.task_name,
                "admin_id": user_id,
                "user_id": receive_user_id,
            },
            notice_content=target_task.notice_template,
            notice_type=target_task.notice_type,
        )
        db.session.add(new_task)
        task_list.append(new_task)
    db.session.commit()
    # 更新任务状态
    if target_task.run_now:
        target_task.task_status = "执行中"
    else:
        target_task.task_status = "待执行"
    target_task.task_instance_total = len(task_list)
    db.session.add(target_task)
    db.session.commit()
    # 提交任务实例
    app.logger.warning(f"通知任务开始执行，任务ID:{target_task.id}，共通知{len(task_list)}人")
    for i in range(0, len(task_list), target_task.task_instance_batch_size):
        batch_list = task_list[i:i + target_task.task_instance_batch_size]
        sub_params = [item.to_dict() for item in batch_list]
        app.logger.warning(f"通知任务批次提交，任务ID:{target_task.id}，本批次通知{len(sub_params)}人")
        if target_task.run_now:
            if target_task.notice_type == "邮件":
                result = notice_user_by_email.delay(sub_params)
            elif target_task.notice_type == "短信":
                result = notice_user_by_sms.delay(sub_params)
            else:
                result = notice_user_by_message.delay(sub_params)
        else:
            plan_begin_time = target_task.plan_begin_time
            if target_task.notice_type == "邮件":
                result = notice_user_by_email.apply_async(args=[sub_params], eta=plan_begin_time)
            elif target_task.notice_type == "短信":
                result = notice_user_by_sms.apply_async(args=[sub_params], eta=plan_begin_time)
            else:
                result = notice_user_by_message.apply_async(args=[sub_params], eta=plan_begin_time)
        for sub_task in batch_list:
            sub_task.task_celery_id = result.id
            db.session.add(sub_task)
        db.session.commit()
    # 返回结果
    return next_console_response(result=target_task.to_dict(),
                                 error_message=f"任务已开始，共通知{len(task_list)}人！")


def filter_notice_users(target_task):
    """
    过滤通知用户
    :return:
    """
    # 筛选出通知对象
    target_users = []
    send_all_user = target_task.notice_params.get("all_user", False)
    send_all_company_user = target_task.notice_params.get("all_company_user", False)
    send_all_person_user = target_task.notice_params.get("all_person_user", False)
    send_all_subscribe_email = target_task.notice_params.get("all_subscribe_email", False)
    target_company_items = target_task.notice_params.get("target_companies", [])
    target_department_items = target_task.notice_params.get("target_departments", [])
    target_user_items = target_task.notice_params.get("target_users", [])

    if send_all_user:
        all_user = UserInfo.query.filter(
            UserInfo.user_status == 1
        ).all()
        target_users.extend(all_user)
    if send_all_company_user:
        all_company_user = CompanyInfo.query.filter(
            CompanyInfo.company_status == "正常"
        ).join(
            UserInfo, CompanyInfo.id == UserInfo.user_company_id
        ).with_entities(
            UserInfo
        ).all()
        target_users.extend(all_company_user)
    if send_all_person_user:
        all_person_user = UserInfo.query.filter(
            UserInfo.user_status == 1,
            UserInfo.user_company_id.is_(None)
        ).all()
        target_users.extend(all_person_user)
    if target_company_items:
        all_company_ids = [i.get("id") for i in target_company_items]
        all_company_user = UserInfo.query.filter(
            UserInfo.user_status == 1,
            UserInfo.user_company_id.in_(all_company_ids)
        ).all()
        target_users.extend(all_company_user)
    if target_department_items:
        all_department_ids = [i.get("id") for i in target_department_items]
        all_department_user = UserInfo.query.filter(
            UserInfo.user_status == 1,
            UserInfo.user_department_id.in_(all_department_ids)
        ).all()
        target_users.extend(all_department_user)
    if target_user_items:
        all_user_ids = [int(i.get("user_id")) for i in target_user_items]
        all_user = UserInfo.query.filter(
            UserInfo.user_status == 1,
            UserInfo.user_id.in_(all_user_ids)
        ).all()
        target_users.extend(all_user)
    if send_all_subscribe_email:
        user_emails = [i.user_email for i in target_users]
        all_subscribe_email = SubscriptionInfo.query.filter(
            SubscriptionInfo.subscribe_status == "正常",
        ).with_entities(
            SubscriptionInfo.id,
            SubscriptionInfo.email.label("user_email")
        ).all()
        for i in all_subscribe_email:
            if i.user_email in user_emails:
                continue
            target_users.append(i)
    # 找出禁用订阅的邮箱
    all_forbidden_email = SubscriptionInfo.query.filter(
        SubscriptionInfo.subscribe_status == "禁用",
    ).with_entities(
        SubscriptionInfo.email.label("user_email")
    ).all()
    all_subscribe_emails = [i.user_email for i in all_forbidden_email]
    target_users = [i for i in target_users if i.user_email not in all_subscribe_emails]
    if not target_users:
        return next_console_response(error_status=True, error_message="未找到通知对象！", error_code=1001)
    # 去重
    unique_user_dict = {}
    for user in target_users:
        unique_user_dict[user.user_id] = user
    target_users = list(unique_user_dict.values())
    return target_users


def pause_task_info(params):
    """
    停止通知任务
    """
    user_id = int(params.get("user_id"))
    task_id = params.get("task_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    target_task = NoticeTaskInfo.query.filter(
        NoticeTaskInfo.id == task_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在！", error_code=1001)
    if target_task.task_status != "执行中":
        return next_console_response(error_status=True, error_message="任务状态不允许停止！", error_code=1001)
    # 停止任务
    task_instances = NoticeTaskInstance.query.filter(
        NoticeTaskInstance.task_id == task_id,
        NoticeTaskInstance.notice_status == "排队中",
        NoticeTaskInstance.task_celery_id != ""
    ).all()
    if not task_instances:
        target_task.task_status = "已完成"
        db.session.add(target_task)
        db.session.commit()
        return next_console_response(error_status=False, error_message="无可停止通知！",
                                     result=target_task.to_dict())
    for task_instance in task_instances:
        task_instance.notice_status = "已暂停"
        db.session.add(task_instance)
    target_task.task_status = "已暂停"
    db.session.add(target_task)
    db.session.commit()
    return next_console_response(result=target_task.to_dict())


def resume_task_info(params):
    """
    恢复通知任务
    """
    user_id = int(params.get("user_id"))
    task_id = params.get("task_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    target_task = NoticeTaskInfo.query.filter(
        NoticeTaskInfo.id == task_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在！", error_code=1001)
    if target_task.task_status != "已暂停":
        return next_console_response(error_status=True, error_message="任务状态不允许恢复！", error_code=1001)

    pause_task_instances = NoticeTaskInstance.query.filter(
        NoticeTaskInstance.task_id == task_id,
        NoticeTaskInstance.notice_status == "已暂停"
    ).all()
    for task_instance in pause_task_instances:
        task_instance.notice_status = "排队中"
        db.session.add(task_instance)
    db.session.commit()
    for task_instance in pause_task_instances:
        if target_task.notice_type == "邮件":
            result = notice_user_by_email.delay(task_instance.to_dict())
            task_instance.task_celery_id = result.id
            db.session.add(task_instance)
            db.session.commit()
        elif target_task.notice_type == "短信":
            notice_user_by_sms.delay(task_instance.to_dict())
        elif target_task.notice_type == "站内信":
            result = notice_user_by_message.delay(task_instance.to_dict())
            task_instance.task_celery_id = result.id
            db.session.add(task_instance)
            db.session.commit()
    target_task.task_status = "执行中"
    db.session.add(target_task)
    db.session.commit()
    return next_console_response(result=target_task.to_dict())


def stop_task_info(params):
    """
    终止通知任务
    """
    user_id = int(params.get("user_id"))
    task_id = params.get("task_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    target_task = NoticeTaskInfo.query.filter(
        NoticeTaskInfo.id == task_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在！", error_code=1001)
    if target_task.task_status not in ["执行中", "已暂停"]:
        return next_console_response(error_status=True, error_message="任务状态不允许终止！", error_code=1001)

    task_instances = NoticeTaskInstance.query.filter(
        NoticeTaskInstance.task_id == task_id,
        NoticeTaskInstance.notice_status == "排队中",
        NoticeTaskInstance.task_celery_id != ""
    ).all()
    if not task_instances:
        target_task.task_status = "已完成"
        db.session.add(target_task)
        db.session.commit()
        return next_console_response(error_status=False, error_message="无可停止通知！",
                                     result=target_task.to_dict())
    for task_instance in task_instances:
        task_instance.notice_status = "已终止"
        db.session.add(task_instance)
    target_task.task_status = "已终止"
    db.session.add(target_task)
    db.session.commit()
    return next_console_response(result=target_task.to_dict())


def list_task_instances(params):
    """
    列出通知任务实例
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    task_id = params.get("task_id")
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 10)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1001)
    target_task = NoticeTaskInfo.query.filter(
        NoticeTaskInfo.id == task_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在！", error_code=1001)
    all_history_data = NoticeTaskInstance.query.filter(
        NoticeTaskInstance.task_id == task_id
    ).order_by(
        NoticeTaskInstance.create_time.desc()
    )
    total = all_history_data.count()
    data = all_history_data.paginate(page=page_num, per_page=page_size, error_out=False)
    result = {
        "page_num": page_num,
        "page_size": page_size,
        "total": total,
        "data": [i.to_dict() for i in data.items]
    }
    return next_console_response(result=result)


def retry_task_instances(params):
    """
    重试通知任务实例
    :param params:
    :return:
    """
    return next_console_response()

