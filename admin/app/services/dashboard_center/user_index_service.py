import datetime
from datetime import timedelta
from sqlalchemy import func, distinct, or_, text, case
from app.app import db
from app.models.user_center.user_info import UserInfo, UserInviteCodeViewRecord, UserFriendsRelation
from app.models.next_console.next_console_model import NextConsoleMessage
from app.models.next_console.next_console_model import NextConsoleQa
from app.models.next_console.next_console_model import NextConsoleSession
from app.services.configure_center.response_utils import next_console_response
from app.models.resource_center.resource_model import ResourceObjectMeta, ResourceObjectUpload
from app.models.resource_center.resource_model import ResourceDownloadRecord, ResourceViewRecord


def get_uv(params):
    """
    获取UV，请求者公司的指定时间内的UV，通过产生消息的用户数来计算
        (用户更新，消息问答，资源库，工单，客服，通讯录，）
    默认查询24小时内的数据
    """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    uv_update = UserInfo.query.filter(
        UserInfo.update_time.between(begin_time, end_time),
        UserInfo.user_id.in_(all_company_staff_id),
        UserInfo.user_status == 1
    ).with_entities(UserInfo.user_id).all()
    uv_msg = NextConsoleMessage.query.with_entities(NextConsoleMessage.user_id).filter(
        NextConsoleMessage.create_time.between(begin_time, end_time),
        NextConsoleMessage.user_id.in_(all_company_staff_id)
    ).distinct()
    uv_resource_upload = ResourceObjectUpload.query.with_entities(ResourceObjectUpload.user_id).filter(
        ResourceObjectUpload.create_time.between(begin_time, end_time),
        ResourceObjectUpload.user_id.in_(all_company_staff_id)
    ).distinct()
    uv_resource_download = ResourceDownloadRecord.query.with_entities(ResourceDownloadRecord.user_id).filter(
        ResourceDownloadRecord.create_time.between(begin_time, end_time),
        ResourceDownloadRecord.user_id.in_(all_company_staff_id)
    ).distinct()
    uv_resource_view = ResourceViewRecord.query.with_entities(ResourceViewRecord.user_id).filter(
        ResourceViewRecord.create_time.between(begin_time, end_time),
        ResourceViewRecord.user_id.in_(all_company_staff_id)
    ).distinct()
    uv_resource_update = ResourceObjectMeta.query.with_entities(ResourceObjectMeta.user_id).filter(
        ResourceObjectMeta.update_time.between(begin_time, end_time),
        ResourceObjectMeta.user_id.in_(all_company_staff_id)
    ).distinct()
    uv = set(
        set(uv_update) | set(uv_msg) | set(uv_resource_upload) | set(uv_resource_download) | set(uv_resource_view)
        | set(uv_resource_update))
    return next_console_response(result={"uv": len(uv), "begin_time": begin_time, "end_time": end_time})


def get_uv_accum_day(params):
    """
        获取UV，请求者公司的指定时间内的UV，通过产生消息的用户数来计算
        默认查询24小时内的数据
        按照天汇总返回时间序列
        """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    uv_day = db.session.query(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(NextConsoleMessage.user_id)).label('unique_user_count')
    ).filter(
        NextConsoleMessage.create_time.between(begin_time, end_time),
        NextConsoleMessage.user_id.in_(all_company_staff_id)
    ).group_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).order_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).all()
    unique_user_count_accum = 0
    uv_day_accum = []

    for item in uv_day:
        unique_user_count_accum += item.unique_user_count
        uv_day_accum.append({"day": item.day, "unique_user_count": unique_user_count_accum})

    return next_console_response(result={"uv_accum_day": uv_day_accum, "begin_time": begin_time, "end_time": end_time})


def get_qa_accum_day(params):
    """
    获取UV，请求者公司的指定时间内的UV，通过产生消息的用户数来计算
    默认查询24小时内的数据
    按照小时汇总返回时间序列
    """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    qa_day = db.session.query(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(NextConsoleMessage.qa_id)).label('unique_qa_count')
        ).filter(
            NextConsoleMessage.create_time.between(begin_time, end_time),
            NextConsoleMessage.user_id.in_(all_company_staff_id)
        ).group_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).order_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).all()
    unique_qa_count_accum = 0
    qa_accum_day = []

    for item in qa_day:
        unique_qa_count_accum += item.unique_qa_count
        qa_accum_day.append({"day": item.day, "unique_qa_count": unique_qa_count_accum})

    return next_console_response(result={"qa_accum_day": qa_accum_day, "begin_time": begin_time, "end_time": end_time})


def get_session_accum_day(params):
    """
        获取session，请求者公司的指定时间内的session，通过产生消息的用户数来计算
        默认查询24小时内的数据
        按照小时汇总返回时间序列
        """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    session_day = db.session.query(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(NextConsoleMessage.session_id)).label('unique_session_count')
    ).filter(
        NextConsoleMessage.create_time.between(begin_time, end_time),
        NextConsoleMessage.user_id.in_(all_company_staff_id)
    ).group_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).order_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).all()
    unique_session_count_accum = 0
    session_accum_day = []

    for item in session_day:
        unique_session_count_accum += item.unique_session_count
        session_accum_day.append({"day": item.day, "unique_session_count": unique_session_count_accum})

    return next_console_response(result={
        "session_accum_day": session_accum_day, "begin_time": begin_time, "end_time": end_time})


def get_dnu(params):
    """
    获取前一日新注册用户数量
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    dnu_result = db.session.query(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(UserInfo.user_id)).label('dnu')
    ).filter(
        UserInfo.create_time.between(begin_time, end_time),
        UserInfo.user_id.in_(all_company_staff_id)
    ).group_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).order_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).all()
    dnu_result = [{"day": item.day, "dnu": item.dnu} for item in dnu_result]
    return next_console_response(result={"dnu": dnu_result, "begin_time": begin_time, "end_time": end_time})


def get_d1_retention(params):
    """
    获取D1留存率，请求者公司的指定时间内的D1留存率，通过相隔一天的独立访客数来计算
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]

    # 计算每个数据的第二天对应的独立访客数
    next_uv_sub_query = UserInfo.query.filter(
        UserInfo.create_time.between(begin_time, end_time),
        UserInfo.user_id.in_(all_company_staff_id)
    ).with_entities(
        UserInfo.create_time,
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD').label('day'),
        (func.date(UserInfo.create_time) + text("INTERVAL '1 days'")).label('next_day'),  # 使用 INTERVAL
        (func.date(UserInfo.create_time) + text("INTERVAL '2 days'")).label('end_day'),  # 使用 INTERVAL
        UserInfo.user_id
    ).subquery()
    next_uv_msg = db.session.query(
        next_uv_sub_query.c.create_time,
        next_uv_sub_query.c.day,
        next_uv_sub_query.c.user_id,
        next_uv_sub_query.c.next_day,
        next_uv_sub_query.c.end_day
    ).join(
        NextConsoleMessage,
        NextConsoleMessage.user_id == next_uv_sub_query.c.user_id
    ).filter(
        NextConsoleMessage.create_time.between(
            next_uv_sub_query.c.next_day,
            next_uv_sub_query.c.end_day)
    ).with_entities(
        next_uv_sub_query.c.end_day,
        next_uv_sub_query.c.user_id
    ).distinct().all()
    next_uv_resource_upload = db.session.query(
        next_uv_sub_query.c.create_time,
        next_uv_sub_query.c.day,
        next_uv_sub_query.c.user_id,
        next_uv_sub_query.c.next_day,
        next_uv_sub_query.c.end_day
    ).join(
        ResourceObjectUpload,
        ResourceObjectUpload.user_id == next_uv_sub_query.c.user_id
    ).filter(
        ResourceObjectUpload.create_time.between(
            next_uv_sub_query.c.next_day,
            next_uv_sub_query.c.end_day)
    ).with_entities(
        next_uv_sub_query.c.end_day,
        next_uv_sub_query.c.user_id
    ).distinct().all()
    next_uv_resource_download = db.session.query(
        next_uv_sub_query.c.create_time,
        next_uv_sub_query.c.day,
        next_uv_sub_query.c.user_id,
        next_uv_sub_query.c.next_day,
        next_uv_sub_query.c.end_day
    ).join(
        ResourceDownloadRecord,
        ResourceDownloadRecord.user_id == next_uv_sub_query.c.user_id
    ).filter(
        ResourceDownloadRecord.create_time.between(
            next_uv_sub_query.c.next_day,
            next_uv_sub_query.c.end_day)
    ).with_entities(
        next_uv_sub_query.c.end_day,
        next_uv_sub_query.c.user_id
    ).distinct().all()
    next_uv_resource_view = db.session.query(
        next_uv_sub_query.c.create_time,
        next_uv_sub_query.c.day,
        next_uv_sub_query.c.user_id,
        next_uv_sub_query.c.next_day,
        next_uv_sub_query.c.end_day
    ).join(
        ResourceViewRecord,
        ResourceViewRecord.user_id == next_uv_sub_query.c.user_id
    ).filter(
        ResourceViewRecord.create_time.between(
            next_uv_sub_query.c.next_day,
            next_uv_sub_query.c.end_day)
    ).with_entities(
        next_uv_sub_query.c.end_day,
        next_uv_sub_query.c.user_id
    ).distinct().all()
    next_uv_resource_update = db.session.query(
        next_uv_sub_query.c.create_time,
        next_uv_sub_query.c.day,
        next_uv_sub_query.c.user_id,
        next_uv_sub_query.c.next_day,
        next_uv_sub_query.c.end_day
    ).join(
        ResourceObjectUpload,
        ResourceObjectUpload.user_id == next_uv_sub_query.c.user_id
    ).filter(
        ResourceObjectUpload.create_time.between(
            next_uv_sub_query.c.next_day,
            next_uv_sub_query.c.end_day)
    ).with_entities(
        next_uv_sub_query.c.end_day,
        next_uv_sub_query.c.user_id
    ).distinct().all()
    all_sub_res = (next_uv_msg + next_uv_resource_upload + next_uv_resource_download
                   + next_uv_resource_view + next_uv_resource_update)
    all_sub_res_dict = {}
    for item in all_sub_res:
        if item.end_day.strftime('%Y-%m-%d') not in all_sub_res_dict:
            all_sub_res_dict[item.end_day.strftime('%Y-%m-%d')] = set()
        all_sub_res_dict[item.end_day.strftime('%Y-%m-%d')].add(item.user_id)
    d1_retention = []
    next_uv_sub_query_res = db.session.query(
        func.to_char(next_uv_sub_query.c.end_day, 'YYYY-MM-DD').label('end_day'),
        func.count(next_uv_sub_query.c.user_id).label('user_cnt')
    ).group_by(
        func.to_char(next_uv_sub_query.c.end_day, 'YYYY-MM-DD'),
    ).all()
    for i in next_uv_sub_query_res:
        d1_retention.append({
            "day": i.end_day,
            "d1_retention": len(all_sub_res_dict.get(i.end_day, set())),
            'user_cnt': i.user_cnt
        })
    return next_console_response(result={"d1_retention": d1_retention, "begin_time": begin_time, "end_time": end_time})


def get_all_retention(params):
    """
    7日留存率
    15日留存率
    30日留存率
    计算每天活跃用户数，然后挑选出对应的留存用户数
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    last_begin_time = (
            datetime.datetime.strptime(begin_time, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(days=30)
    ).strftime('%Y-%m-%d %H:%M:%S')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.filter(
                UserInfo.create_time.between(last_begin_time, end_time)
            ).all()
        else:
            all_company_staff = UserInfo.query.filter(
                UserInfo.create_time.between(last_begin_time, end_time),
                UserInfo.user_company_id == company_id
            ).all()
    else:
        all_company_staff = UserInfo.query.filter(
            UserInfo.create_time.between(last_begin_time, end_time),
            UserInfo.user_company_id == request_user.user_company_id
        ).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    # 消息活跃用户
    msg_active_user = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time.between(begin_time, end_time),
        NextConsoleMessage.user_id.in_(all_company_staff_id)
    ).with_entities(
        NextConsoleMessage.user_id.label('user_id'),
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD').label('day')
    ).distinct()
    # 资源活跃用户
    resource_upload_user = ResourceObjectUpload.query.filter(
        ResourceObjectUpload.create_time.between(begin_time, end_time),
        ResourceObjectUpload.user_id.in_(all_company_staff_id)
    ).with_entities(
        ResourceObjectUpload.user_id.label('user_id'),
        func.to_char(ResourceObjectUpload.create_time, 'YYYY-MM-DD').label('day')
    ).distinct()
    resource_update_user = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.update_time.between(begin_time, end_time),
        ResourceObjectMeta.user_id.in_(all_company_staff_id)
    ).with_entities(
        ResourceObjectMeta.user_id.label('user_id'),
        func.to_char(ResourceObjectMeta.update_time, 'YYYY-MM-DD').label('day')
    ).distinct()
    resource_view_user = ResourceViewRecord.query.filter(
        ResourceViewRecord.create_time.between(begin_time, end_time),
        ResourceViewRecord.user_id.in_(all_company_staff_id)
    ).with_entities(
        ResourceViewRecord.user_id.label('user_id'),
        func.to_char(ResourceViewRecord.create_time, 'YYYY-MM-DD').label('day')
    ).distinct()
    resource_download_user = ResourceDownloadRecord.query.filter(
        ResourceDownloadRecord.create_time.between(begin_time, end_time),
        ResourceDownloadRecord.user_id.in_(all_company_staff_id)
    ).with_entities(
        ResourceDownloadRecord.user_id.label('user_id'),
        func.to_char(ResourceViewRecord.create_time, 'YYYY-MM-DD').label('day')
    ).distinct()
    all_active_user_sub = msg_active_user.union(
        resource_upload_user, resource_update_user, resource_view_user, resource_download_user
    ).subquery()
    all_active_user = db.session.query(
        all_active_user_sub.c.day,
        all_active_user_sub.c.user_id
    ).join(
        UserInfo,
        UserInfo.user_id == all_active_user_sub.c.user_id
    ).with_entities(
        all_active_user_sub.c.day,
        all_active_user_sub.c.user_id,
        # 判断是否为7日留存用户：创建时间在7天前，则新建字段is_seven_day_retention
        case((
            func.date(UserInfo.create_time) + text("INTERVAL '7 days'") >= func.date(all_active_user_sub.c.day), 1),
            else_=0
        ).label(
            'is_seven_day_retention'),
        # 判断是否为15日留存用户：创建时间在15天前，则新建字段is_fifteen_day_retention
        case((
            func.date(UserInfo.create_time) + text("INTERVAL '15 days'") >= func.date(all_active_user_sub.c.day), 1),
            else_=0
        ).label(
            'is_fifteen_day_retention'),
        # 判断是否为30日留存用户：创建时间在30天前，则新建字段is_thirty_day_retention
        case((
            func.date(UserInfo.create_time) + text("INTERVAL '30 days'") >= func.date(all_active_user_sub.c.day), 1),
            else_=0
        ).label(
            'is_thirty_day_retention')
    ).order_by(
        all_active_user_sub.c.day
    ).all()
    all_active_user_dict = {}
    retention_7 = []
    retention_15 = []
    retention_30 = []
    all_active_day = []
    for item in all_active_user:
        if item.day not in all_active_user_dict:
            all_active_user_dict[item.day] = set()
        if item.day not in all_active_day:
            all_active_day.append(item.day)
        all_active_user_dict[item.day].add((
            item.user_id, item.is_seven_day_retention,
            item.is_fifteen_day_retention, item.is_thirty_day_retention))
    active_user_series = [
        {"day": item, "active_user_count": len(all_active_user_dict.get(item, set()))}
        for item in all_active_day]
    for day in all_active_day:
        retention_7_cnt = 0
        retention_15_cnt = 0
        retention_30_cnt = 0
        for active_user in all_active_user_dict.get(day, set()):
            if active_user[1]:
                retention_7_cnt += 1
            if active_user[2]:
                retention_15_cnt += 1
            if active_user[3]:
                retention_30_cnt += 1
        retention_7.append(retention_7_cnt)
        retention_15.append(retention_15_cnt)
        retention_30.append(retention_30_cnt)

    all_retention = {
        "active_user_series": active_user_series,
        "retention_7": retention_7,
        "retention_15": retention_15,
        "retention_30": retention_30
    }
    return next_console_response(result={
        "all_retention": all_retention, "begin_time": begin_time, "end_time": end_time})


def get_dnu_sd(params):
    """
    获取前一日新注册用户来源渠道
    :param params:
    :return:
        ['source_channel', '2012', '2013', '2014', '2015', '2016', '2017'],
        ['营销推荐', 56.5, 82.1, 88.7, 70.1, 53.4, 85.1],
        ['官网注册', 51.1, 51.4, 55.1, 53.3, 73.8, 68.7],
        ['用户推荐', 40.1, 62.2, 69.5, 36.4, 45.2, 32.5],
        ['未知渠道', 25.2, 37.1, 41.2, 18, 33.9, 49.1]
    """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    dnu_result = db.session.query(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(UserInfo.user_id)).label('dnu')
    ).filter(
        UserInfo.create_time.between(begin_time, end_time),
        UserInfo.user_id.in_(all_company_staff_id)
    ).group_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).order_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).all()
    source_channel = [item.day for item in dnu_result]
    source_channel.insert(0, "source_channel")
    # 营销推荐: 新建用户关联浏览表，且finish_register为true 且，marketing_code 不为空
    marketing_result = UserInfo.query.filter(
        UserInfo.create_time.between(begin_time, end_time),
        UserInfo.user_id.in_(all_company_staff_id)
    ).join(
        UserInviteCodeViewRecord,
        UserInviteCodeViewRecord.view_user_id == UserInfo.user_id
    ).filter(
        UserInviteCodeViewRecord.finish_register == True,
        UserInviteCodeViewRecord.marketing_code.isnot(None),
        UserInviteCodeViewRecord.marketing_code != ""
    ).with_entities(
        UserInfo
    ).group_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).with_entities(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(UserInfo.user_id)).label('dnu_sd_marketing')
    ).order_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).all()
    marketing_result_map = {item.day: item.dnu_sd_marketing for item in marketing_result}
    marketing_result_series = ["营销推荐"]
    for sub_day, user_total in dnu_result:
        user_cnt = marketing_result_map.get(sub_day, 0)
        marketing_result_series.append(round(user_cnt / user_total * 100, 1))

    # 官网注册: 新建用户关联浏览表，且finish_register为true 且，user_id 为1
    webpage_result = UserInfo.query.filter(
        UserInfo.create_time.between(begin_time, end_time),
        UserInfo.user_id.in_(all_company_staff_id)
    ).join(
        UserInviteCodeViewRecord,
        UserInviteCodeViewRecord.view_user_id == UserInfo.user_id
    ).filter(
        UserInviteCodeViewRecord.finish_register == True,
        UserInviteCodeViewRecord.user_id == 1
    ).with_entities(
        UserInfo
    ).group_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).with_entities(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(UserInfo.user_id)).label('dnu_sd_webpage')
    ).order_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).all()
    webpage_result_map = {item.day: item.dnu_sd_webpage for item in webpage_result}
    webpage_result_series = ["官网注册"]
    for sub_day, user_total in dnu_result:
        user_cnt = webpage_result_map.get(sub_day, 0)
        webpage_result_series.append(round(user_cnt / user_total * 100, 1))
    # 用户推荐: 新建用户关联浏览表，且finish_register为true 且，user_id 不为1, 且marketing_code 为空
    user_invite_result = UserInfo.query.filter(
        UserInfo.create_time.between(begin_time, end_time),
        UserInfo.user_id.in_(all_company_staff_id)
    ).join(
        UserInviteCodeViewRecord,
        UserInviteCodeViewRecord.view_user_id == UserInfo.user_id
    ).filter(
        UserInviteCodeViewRecord.finish_register == True,
        UserInviteCodeViewRecord.user_id != 1,
        or_(
            UserInviteCodeViewRecord.marketing_code.is_(None),
            UserInviteCodeViewRecord.marketing_code == ""
        )
    ).with_entities(
        UserInfo
    ).group_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).with_entities(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(UserInfo.user_id)).label('dnu_sd_user_invite')
    ).order_by(
        func.to_char(UserInfo.create_time, 'YYYY-MM-DD')
    ).all()
    user_invite_result_map = {item.day: item.dnu_sd_user_invite for item in user_invite_result}
    user_invite_result_series = ["用户推荐"]
    for sub_day, user_total in dnu_result:
        user_cnt = user_invite_result_map.get(sub_day, 0)
        user_invite_result_series.append(round(user_cnt / user_total * 100, 1))

    other_channel_series = ["未知渠道"]
    for sub_day, user_total in dnu_result:
        user_cnt = (user_total - marketing_result_map.get(sub_day, 0)
                    - webpage_result_map.get(sub_day, 0) - user_invite_result_map.get(sub_day, 0))
        other_channel_series.append(round(user_cnt / user_total * 100, 1))
    res = [
        source_channel,
        marketing_result_series,
        webpage_result_series,
        user_invite_result_series,
        other_channel_series
    ]

    return next_console_response(result={"dnu_sd": res, "begin_time": begin_time, "end_time": end_time})


def get_all_cvr(params):
    """
    获取所有用户的转化率
    [
                { value: 60, name: '所有注册用户' },
                { value: 40, name: 'AI工作台' },
                { value: 20, name: '帮助工单' },
                { value: 80, name: '在线支持' },
                { value: 100, name: '知识库' },
                { value: 100, name: '全部使用' },
            ]
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")

    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    all_cvr = []
    # 所有注册用户
    all_user = UserInfo.query.filter(
        UserInfo.user_id.in_(all_company_staff_id),
        UserInfo.user_status == 1
    ).all()
    all_user_cnt = len(all_user)
    all_cvr.append({"value": 100, "name": "所有注册用户"})
    # AI工作台
    ai_workbench_user = NextConsoleMessage.query.filter(
        NextConsoleSession.user_id.in_(all_company_staff_id),

    ).with_entities(
        NextConsoleSession.user_id
    ).distinct()
    ai_workbench_user_cnt = ai_workbench_user.count()
    all_cvr.append({"value": round(ai_workbench_user_cnt / all_user_cnt * 100, 1), "name": "AI工作台"})
    # 知识库
    resource_update_user = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id.in_(all_company_staff_id)
    ).with_entities(
        ResourceObjectMeta.user_id
    ).distinct()
    resource_upload_user = ResourceObjectUpload.query.filter(
        ResourceObjectUpload.user_id.in_(all_company_staff_id),
    ).with_entities(
        ResourceObjectUpload.user_id
    ).distinct()
    resource_download_user = ResourceDownloadRecord.query.filter(
        ResourceDownloadRecord.user_id.in_(all_company_staff_id),
    ).with_entities(
        ResourceDownloadRecord.user_id
    ).distinct()
    resource_view_user = ResourceViewRecord.query.filter(
        ResourceViewRecord.user_id.in_(all_company_staff_id),
    ).with_entities(
        ResourceViewRecord.user_id
    ).distinct()
    resource_user = resource_update_user.union(resource_upload_user, resource_download_user, resource_view_user)
    resource_user_cnt = resource_user.count()
    all_cvr.append({"value": round(resource_user_cnt / all_user_cnt * 100, 1), "name": "资源库"})

    # 全部使用
    ai_workbench_user = set(ai_workbench_user.all())
    resource_user = set(resource_user.all())
    all_use_user_cnt = len(ai_workbench_user.intersection(resource_user))
    all_cvr.append({"value": round(all_use_user_cnt / all_user_cnt * 100, 1), "name": "全部使用"})
    return next_console_response(result={"all_cvr": all_cvr})


def get_new_cvr(params):
    """
    获取新注册用户的转化率
    [
                { value: 60, name: '所有注册用户' },
                { value: 40, name: 'AI工作台' },
                { value: 20, name: '帮助工单' },
                { value: 80, name: '在线支持' },
                { value: 100, name: '知识库' },
                { value: 100, name: '全部使用' },
            ]
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    all_cvr = []
    # 所有新增注册用户
    all_new_user = UserInfo.query.filter(
        UserInfo.user_id.in_(all_company_staff_id),
        UserInfo.create_time.between(begin_time, end_time),
        UserInfo.user_status == 1
    ).all()
    all_new_user_id = [user.user_id for user in all_new_user]
    all_new_user_cnt = len(all_new_user)
    all_cvr.append({"value": 100, "name": "所有注册用户"})
    if all_new_user_cnt == 0:
        all_cvr.append({"value": 0, "name": "AI工作台"})
        all_cvr.append({"value": 0, "name": "帮助工单"})
        all_cvr.append({"value": 0, "name": "在线支持"})
        all_cvr.append({"value": 0, "name": "资源库"})
        all_cvr.append({"value": 0, "name": "全部使用"})
        return next_console_response(result={"new_cvr": all_cvr, "begin_time": begin_time, "end_time": end_time})
    # AI工作台
    ai_workbench_user = NextConsoleMessage.query.filter(
        NextConsoleSession.user_id.in_(all_new_user_id),
        NextConsoleSession.create_time.between(begin_time, end_time)
    ).with_entities(
        NextConsoleSession.user_id
    ).distinct()
    ai_workbench_user_cnt = ai_workbench_user.count()
    all_cvr.append({"value": round(ai_workbench_user_cnt / all_new_user_cnt * 100, 1), "name": "AI工作台"})
    # 资源库
    resource_update_user = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id.in_(all_new_user_id),
        or_(
            ResourceObjectMeta.create_time.between(begin_time, end_time),
            ResourceObjectMeta.update_time.between(begin_time, end_time)
        )
    ).with_entities(
        ResourceObjectMeta.user_id
    ).distinct()
    resource_upload_user = ResourceObjectUpload.query.filter(
        ResourceObjectUpload.user_id.in_(all_new_user_id),
        ResourceObjectUpload.create_time.between(begin_time, end_time)
    ).with_entities(
        ResourceObjectUpload.user_id
    ).distinct()
    resource_download_user = ResourceDownloadRecord.query.filter(
        ResourceDownloadRecord.user_id.in_(all_new_user_id),
        ResourceDownloadRecord.create_time.between(begin_time, end_time)
    ).with_entities(
        ResourceDownloadRecord.user_id
    ).distinct()
    resource_view_user = ResourceViewRecord.query.filter(
        ResourceViewRecord.user_id.in_(all_new_user_id),
        ResourceViewRecord.create_time.between(begin_time, end_time)
    ).with_entities(
        ResourceViewRecord.user_id
    ).distinct()
    resource_user = resource_update_user.union(resource_upload_user, resource_download_user, resource_view_user)
    resource_user_cnt = resource_user.count()
    all_cvr.append({"value": round(resource_user_cnt / all_new_user_cnt * 100, 1), "name": "资源库"})

    # 全部使用，求交集
    ai_workbench_user = set(ai_workbench_user.all())
    resource_user = set(resource_user.all())
    all_use_user_cnt = len(ai_workbench_user.intersection(resource_user))
    all_cvr.append({"value": round(all_use_user_cnt / all_new_user_cnt * 100, 1), "name": "全部使用"})
    return next_console_response(result={"new_cvr": all_cvr, "begin_time": begin_time, "end_time": end_time})


def get_active_day_rank(params):
    """
    获取活跃用户排名-统计在一个周期内（如过去30天），用户有活动的总天数。
    """
    user_id = int(params.get("user_id"))
    top = int(params.get("top", 100))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    all_msgs_day = NextConsoleMessage.query.filter(
        NextConsoleMessage.user_id.in_(all_company_staff_id),
        NextConsoleMessage.create_time.between(begin_time, end_time),
        NextConsoleMessage.msg_role == "user"
    ).with_entities(
        NextConsoleMessage.user_id,
        func.count(distinct(func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD'))).label('days'),
    ).group_by(
        NextConsoleMessage.user_id
    ).order_by(
        func.count(distinct(func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD'))).desc()
    ).limit(
        top
    ).all()
    active_user_rank = [{"user_id": item.user_id, "active_days": item.days} for item in all_msgs_day]
    all_user_id = [item["user_id"] for item in active_user_rank]
    user_info = UserInfo.query.filter(UserInfo.user_id.in_(all_user_id)).all()
    user_info_dict = {item.user_id: {
        "user_avatar": item.user_avatar,
        "user_name": item.user_name,
        "user_nick_name": item.user_nick_name,
        "user_nick_name_py": item.user_nick_name_py,
        "user_company": item.user_company,
        "user_department": item.user_department,
        "user_id": item.user_id,
    } for item in user_info}

    result = []
    for item in active_user_rank:
        user_data = user_info_dict.get(item["user_id"], {})
        user_data.update({"active_days": item["active_days"]})
        result.append(user_data)
    return next_console_response(result={
        "active_day_rank": result,
        "begin_time": begin_time,
        "end_time": end_time}
    )


def get_user_qa_rank(params):
    """
    获取问答用户排名-统计在一个周期内（如过去30天），用户提问次数排名。
    """
    user_id = int(params.get("user_id"))
    top = int(params.get("top", 100))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    all_msgs_qas = NextConsoleMessage.query.filter(
        NextConsoleMessage.user_id.in_(all_company_staff_id),
        NextConsoleMessage.create_time.between(begin_time, end_time),
        NextConsoleMessage.msg_role == "user"
    ).with_entities(
        NextConsoleMessage.user_id,
        func.count(distinct(NextConsoleMessage.qa_id)).label('qa_count'),
    ).group_by(
        NextConsoleMessage.user_id
    ).order_by(
        func.count(distinct(NextConsoleMessage.qa_id)).desc()
    ).limit(
        top
    ).all()
    active_user_rank = [{"user_id": item.user_id, "qa_count": item.qa_count} for item in all_msgs_qas]
    all_user_id = [item["user_id"] for item in active_user_rank]
    user_info = UserInfo.query.filter(UserInfo.user_id.in_(all_user_id)).all()
    user_info_dict = {item.user_id: {
        "user_avatar": item.user_avatar,
        "user_name": item.user_name,
        "user_nick_name": item.user_nick_name,
        "user_nick_name_py": item.user_nick_name_py,
        "user_company": item.user_company,
        "user_department": item.user_department,
        "user_id": item.user_id,
    } for item in user_info}

    result = []
    for item in active_user_rank:
        user_data = user_info_dict.get(item["user_id"], {})
        user_data.update({"qa_count": item["qa_count"]})
        result.append(user_data)
    return next_console_response(result={
        "qa_rank": result,
        "begin_time": begin_time,
        "end_time": end_time}
    )


def get_user_token_rank(params):
    """
    获取用户使用token排名-统计在一个周期内（如过去30天），用户使用token数量排名。
    """
    user_id = int(params.get("user_id"))
    top = int(params.get("top", 100))
    request_user = UserInfo.query.filter_by(user_id=user_id).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    end_time = params.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    all_msgs_qas = NextConsoleMessage.query.filter(
        NextConsoleMessage.user_id.in_(all_company_staff_id),
        NextConsoleMessage.create_time.between(begin_time, end_time),
        NextConsoleMessage.msg_token_used > 0
    ).with_entities(
        NextConsoleMessage.user_id,
        func.sum(NextConsoleMessage.msg_token_used).label('token_count'),
    ).group_by(
        NextConsoleMessage.user_id
    ).order_by(
        func.sum(NextConsoleMessage.msg_token_used).desc()
    ).limit(
        top
    ).all()
    active_user_rank = [{"user_id": item.user_id, "token_count": item.token_count} for item in all_msgs_qas]
    all_user_id = [item["user_id"] for item in active_user_rank]
    user_info = UserInfo.query.filter(UserInfo.user_id.in_(all_user_id)).all()
    user_info_dict = {item.user_id: {
        "user_avatar": item.user_avatar,
        "user_name": item.user_name,
        "user_nick_name": item.user_nick_name,
        "user_nick_name_py": item.user_nick_name_py,
        "user_company": item.user_company,
        "user_department": item.user_department,
        "user_id": item.user_id,
    } for item in user_info}

    result = []
    for item in active_user_rank:
        user_data = user_info_dict.get(item["user_id"], {})
        user_data.update({"token_count": item["token_count"]})
        result.append(user_data)
    return next_console_response(result={
        "token_rank": result,
        "begin_time": begin_time,
        "end_time": end_time}
    )
