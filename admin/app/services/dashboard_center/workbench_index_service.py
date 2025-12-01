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
from app.models.app_center.app_info_model import AppMetaInfo


def get_uv_hour(params):
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
    session_source = params.get('session_source', 'next_search')
    uv_hour = NextConsoleSession.query.filter(
        # NextConsoleSession.session_source == session_source,
        NextConsoleSession.user_id.in_(all_company_staff_id)
    ).join(
        NextConsoleMessage,
        NextConsoleSession.id == NextConsoleMessage.session_id
    ).filter(
        NextConsoleMessage.create_time.between(begin_time, end_time)
    ).with_entities(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD HH').label('hour'),
        func.count(distinct(NextConsoleMessage.user_id)).label('unique_user_count')
    ).group_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD HH')
    ).order_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD HH')
    ).all()
    uv_hour = [{"hour": item.hour + ":00:00", "unique_user_count": item.unique_user_count} for item in uv_hour]
    return next_console_response(result={"uv_hour": uv_hour, "begin_time": begin_time, "end_time": end_time})


def get_uv_day(params):
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
    session_source = params.get('session_source', 'next_search')
    uv_day = NextConsoleSession.query.filter(
        # NextConsoleSession.session_source == session_source,
        NextConsoleSession.user_id.in_(all_company_staff_id)
    ).join(
        NextConsoleMessage,
        NextConsoleSession.id == NextConsoleMessage.session_id
    ).filter(
        NextConsoleMessage.create_time.between(begin_time, end_time)
    ).with_entities(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(NextConsoleMessage.user_id)).label('unique_user_count')
    ).group_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).order_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).all()
    uv_day = [{"day": item.day + " 00:00:00", "unique_user_count": item.unique_user_count} for item in uv_day]
    return next_console_response(result={"uv_day": uv_day, "begin_time": begin_time, "end_time": end_time})


def get_avg_qa_retention(params):
    """
    获取平均问答留存率
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
    session_source = params.get('session_source', 'next_search')
    subquery = NextConsoleSession.query.filter(
        NextConsoleSession.user_id.in_(all_company_staff_id),
        # NextConsoleSession.session_source == session_source
    ).join(
        NextConsoleQa,
        NextConsoleQa.session_id == NextConsoleSession.id
    ).filter(
        NextConsoleQa.create_time.between(begin_time, end_time)
    ).join(
        UserInfo,
        UserInfo.user_id == NextConsoleSession.user_id
    ).with_entities(
        NextConsoleQa.qa_id,
        NextConsoleQa.create_time,
        NextConsoleQa.user_id,
        case((func.date_part('day', NextConsoleQa.create_time - UserInfo.create_time) == 1, 1),
             else_=0).label('is_one_day_retention'),
        case((func.date_part('day', NextConsoleQa.create_time - UserInfo.create_time) == 7, 1),
             else_=0).label('is_seven_day_retention'),
        # 判断是否为15日留存用户：创建时间在15天前，则新建字段is_fifteen_day_retention
        case((func.date_part('day', NextConsoleQa.create_time - UserInfo.create_time) == 15, 1),
             else_=0).label('is_fifteen_day_retention'),
        # 判断是否为30日留存用户：创建时间在30天前，则新建字段is_thirty_day_retention
        case((func.date_part('day', NextConsoleQa.create_time - UserInfo.create_time) == 30, 1),
             else_=0).label('is_thirty_day_retention')
    ).subquery()
    avg_qa_retention_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.qa_id)).label('qa_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    avg_qa_retention_map = {
        item.day: round(item.qa_count / item.user_count, 1)
        for item in avg_qa_retention_series
    }
    avg_qa_retention_series = [
        {"day": item.day, "avg_qa_count": round(item.qa_count / item.user_count, 1)}
        for item in avg_qa_retention_series
    ]
    retention_1_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.qa_id)).label('qa_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).filter(
        subquery.c.is_one_day_retention == 1
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    retention_1_map = {
        item.day: round(item.qa_count / item.user_count, 1)
        for item in retention_1_series
    }
    retention_1 = [retention_1_map.get(item, 0) for item in avg_qa_retention_map]
    retention_7_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.qa_id)).label('qa_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).filter(
        subquery.c.is_seven_day_retention == 1
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    retention_7_map = {
        item.day: round(item.qa_count / item.user_count, 1)
        for item in retention_7_series
    }
    retention_7 = [retention_7_map.get(item, 0) for item in avg_qa_retention_map]
    retention_15_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.qa_id)).label('qa_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).filter(
        subquery.c.is_fifteen_day_retention == 1
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    retention_15_map = {
        item.day: round(item.qa_count / item.user_count, 1)
        for item in retention_15_series
    }
    retention_15 = [retention_15_map.get(item, 0) for item in avg_qa_retention_map]
    retention_30_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.qa_id)).label('qa_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).filter(
        subquery.c.is_thirty_day_retention == 1
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    retention_30_map = {
        item.day: round(item.qa_count / item.user_count, 1)
        for item in retention_30_series
    }
    retention_30 = [retention_30_map.get(item, 0) for item in avg_qa_retention_map]
    avg_qa_retention = {
        "avg_qa_retention_series": avg_qa_retention_series,
        "retention_1": retention_1,
        "retention_7": retention_7,
        "retention_15": retention_15,
        "retention_30": retention_30
    }
    return next_console_response(result={
        "avg_qa_retention": avg_qa_retention, "begin_time": begin_time, "end_time": end_time})


def get_qa_hour(params):
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
    session_source = params.get('session_source', 'next_search')
    qa_hour = NextConsoleSession.query.filter(
        # NextConsoleSession.session_source == session_source,
        NextConsoleSession.user_id.in_(all_company_staff_id)
    ).join(
        NextConsoleQa,
        NextConsoleSession.id == NextConsoleQa.session_id
    ).filter(
        NextConsoleQa.create_time.between(begin_time, end_time)
    ).with_entities(
        func.to_char(NextConsoleQa.create_time, 'YYYY-MM-DD HH').label('hour'),
        func.count(distinct(NextConsoleQa.qa_id)).label('unique_qa_count')
    ).group_by(
        func.to_char(NextConsoleQa.create_time, 'YYYY-MM-DD HH')
    ).order_by(
        func.to_char(NextConsoleQa.create_time, 'YYYY-MM-DD HH')
    ).all()
    qa_hour = [{"hour": item.hour + ":00:00", "unique_qa_count": item.unique_qa_count} for item in qa_hour]
    return next_console_response(result={"qa_hour": qa_hour, "begin_time": begin_time, "end_time": end_time})


def get_qa_day(params):
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
    session_source = params.get('session_source', 'next_search')
    qa_day = NextConsoleSession.query.filter(
        # NextConsoleSession.session_source == session_source,
        NextConsoleSession.user_id.in_(all_company_staff_id)
    ).join(
        NextConsoleQa,
        NextConsoleSession.id == NextConsoleQa.session_id
    ).filter(
        NextConsoleQa.create_time.between(begin_time, end_time)
    ).with_entities(
        func.to_char(NextConsoleQa.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(NextConsoleQa.qa_id)).label('unique_qa_count')
    ).group_by(
        func.to_char(NextConsoleQa.create_time, 'YYYY-MM-DD')
    ).order_by(
        func.to_char(NextConsoleQa.create_time, 'YYYY-MM-DD')
    ).all()

    qa_day = [{"day": item.day + " 00:00:00", "unique_qa_count": item.unique_qa_count} for item in qa_day]
    return next_console_response(result={"qa_day": qa_day, "begin_time": begin_time, "end_time": end_time})


def get_avg_session_retention(params):
    """
    获取平均会话留存率
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
    session_source = params.get('session_source', 'next_search')
    subquery = NextConsoleSession.query.filter(
        NextConsoleSession.user_id.in_(all_company_staff_id),
        # NextConsoleSession.session_source == session_source,
        NextConsoleSession.create_time.between(begin_time, end_time)
    ).join(
        UserInfo,
        UserInfo.user_id == NextConsoleSession.user_id
    ).with_entities(
        NextConsoleSession.id,
        NextConsoleSession.create_time,
        NextConsoleSession.user_id,
        case((func.date_part('day', NextConsoleSession.create_time - UserInfo.create_time) == 1, 1),
             else_=0).label('is_one_day_retention'),
        case((func.date_part('day', NextConsoleSession.create_time - UserInfo.create_time) == 7, 1),
             else_=0).label('is_seven_day_retention'),
        # 判断是否为15日留存用户：创建时间在15天前，则新建字段is_fifteen_day_retention
        case((func.date_part('day', NextConsoleSession.create_time - UserInfo.create_time) == 15, 1),
             else_=0).label('is_fifteen_day_retention'),
        # 判断是否为30日留存用户：创建时间在30天前，则新建字段is_thirty_day_retention
        case((func.date_part('day', NextConsoleSession.create_time - UserInfo.create_time) == 30, 1),
             else_=0).label('is_thirty_day_retention')
    ).subquery()
    avg_session_retention_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.id)).label('session_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    avg_session_retention_map = {
        item.day: round(item.session_count / item.user_count, 1)
        for item in avg_session_retention_series
    }
    avg_session_retention_series = [
        {"day": item.day, "avg_session_count": round(item.session_count / item.user_count, 1)}
        for item in avg_session_retention_series
    ]
    retention_1_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.id)).label('session_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).filter(
        subquery.c.is_one_day_retention == 1
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    retention_1_map = {
        item.day: round(item.session_count / item.user_count, 1)
        for item in retention_1_series
    }
    retention_1 = [retention_1_map.get(item, 0) for item in avg_session_retention_map]
    retention_7_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.id)).label('session_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).filter(
        subquery.c.is_seven_day_retention == 1
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    retention_7_map = {
        item.day: round(item.session_count / item.user_count, 1)
        for item in retention_7_series
    }
    retention_7 = [retention_7_map.get(item, 0) for item in avg_session_retention_map]
    retention_15_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.id)).label('session_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).filter(
        subquery.c.is_fifteen_day_retention == 1
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    retention_15_map = {
        item.day: round(item.session_count / item.user_count, 1)
        for item in retention_15_series
    }
    retention_15 = [retention_15_map.get(item, 0) for item in avg_session_retention_map]
    retention_30_series = db.session.query(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(subquery.c.id)).label('session_count'),
        func.count(distinct(subquery.c.user_id)).label('user_count'),
    ).filter(
        subquery.c.is_thirty_day_retention == 1
    ).group_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD').label('day')
    ).order_by(
        func.to_char(subquery.c.create_time, 'YYYY-MM-DD')
    ).all()
    retention_30_map = {
        item.day: round(item.session_count / item.user_count, 1)
        for item in retention_30_series
    }
    retention_30 = [retention_30_map.get(item, 0) for item in avg_session_retention_map]
    avg_session_retention = {
        "avg_session_retention_series": avg_session_retention_series,
        "retention_1": retention_1,
        "retention_7": retention_7,
        "retention_15": retention_15,
        "retention_30": retention_30
    }
    return next_console_response(result={
        "avg_session_retention": avg_session_retention, "begin_time": begin_time, "end_time": end_time})


def get_session_hour(params):
    """
    获取session，请求者公司的指定时间内的session，通过产生qa的数来计算
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
    session_source = params.get('session_source', 'next_search')
    session_hour = NextConsoleSession.query.filter(
        NextConsoleSession.create_time.between(begin_time, end_time),
        NextConsoleSession.user_id.in_(all_company_staff_id),
        # NextConsoleSession.session_source == session_source
    ).join(
        NextConsoleMessage,
        NextConsoleSession.id == NextConsoleMessage.session_id
    ).with_entities(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD HH').label('hour'),
        func.count(distinct(NextConsoleMessage.session_id)).label('unique_session_count')
    ).group_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD HH')
    ).order_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD HH')
    ).all()
    session_hour = [{"hour": item.hour + ":00:00", "unique_session_count": item.unique_session_count}
                    for item in session_hour]
    return next_console_response(result={"session_hour": session_hour, "begin_time": begin_time, "end_time": end_time})


def get_session_day(params):
    """
    获取session，请求者公司的指定时间内的session，通过产生qa的数来计算
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
    session_source = params.get('session_source', 'next_search')
    session_day = NextConsoleSession.query.filter(
        NextConsoleSession.create_time.between(begin_time, end_time),
        NextConsoleSession.user_id.in_(all_company_staff_id),
        # NextConsoleSession.session_source == session_source
    ).join(
        NextConsoleMessage,
        NextConsoleSession.id == NextConsoleMessage.session_id
    ).with_entities(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD').label('day'),
        func.count(distinct(NextConsoleMessage.session_id)).label('unique_session_count')
    ).group_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).order_by(
        func.to_char(NextConsoleMessage.create_time, 'YYYY-MM-DD')
    ).all()
    session_day = [{
        "day": item.day + ":00:00", "unique_session_count": item.unique_session_count} for item in session_day]
    return next_console_response(result={"session_day": session_day, "begin_time": begin_time, "end_time": end_time})


def get_qa(params):
    """
        获取qa，请求者公司的指定时间内的qa，通过产生qa的数来计算
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
    qa = NextConsoleQa.query.filter(
        NextConsoleQa.create_time.between(begin_time, end_time),
        NextConsoleQa.user_id.in_(all_company_staff_id)
    ).count()
    return next_console_response(result={"qa": qa, "begin_time": begin_time, "end_time": end_time})


def get_session(params):
    """
        获取session，请求者公司的指定时间内的session，通过产生qa的数来计算
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
    session_source = params.get('session_source', 'next_search')
    session = NextConsoleSession.query.filter(
        NextConsoleSession.create_time.between(begin_time, end_time),
        NextConsoleSession.user_id.in_(all_company_staff_id),
        # NextConsoleSession.session_source == session_source
    ).count()
    return next_console_response(result={"session": session, "begin_time": begin_time, "end_time": end_time})


def get_app_active_user_rank(params):
    """
    获取基于使用用户数的应用排名
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
    top = params.get('top', 50)
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    session_sources = NextConsoleSession.query.filter(
        NextConsoleSession.create_time.between(begin_time, end_time),
        NextConsoleSession.user_id.in_(all_company_staff_id),
        NextConsoleSession.session_source.isnot(None),
        NextConsoleSession.session_source != ''
    ).with_entities(
        NextConsoleSession.session_source,
        func.count(distinct(NextConsoleSession.user_id)).label('user_count')
    ).group_by(
        NextConsoleSession.session_source
    ).order_by(
        func.count(distinct(NextConsoleSession.user_id)).desc()
    ).limit(top).all()
    all_app_codes = [item.session_source for item in session_sources]
    source_apps = AppMetaInfo.query.filter(
        AppMetaInfo.app_code.in_(all_app_codes),
        AppMetaInfo.app_status == '正常',
        AppMetaInfo.environment == '生产'
    ).all()
    source_app_map = {app.app_code: {
        "app_name": app.app_name,
        "app_code": app.app_code,
        "app_desc": app.app_desc,
        "app_icon": app.app_icon
    } for app in source_apps}
    session_sources = [
        {
            "app_info": source_app_map.get(item.session_source, {}),
            "user_count": item.user_count
        }
        for item in session_sources if item.session_source in source_app_map
    ]
    return next_console_response(result={
        "app_rank_user": session_sources,
        "begin_time": begin_time,
        "end_time": end_time
    })


def get_app_active_qa_rank(params):
    """
    获取基于请求数的应用排名
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
    top = params.get('top', 50)
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    session_sources = NextConsoleSession.query.filter(
        NextConsoleSession.create_time.between(begin_time, end_time),
        NextConsoleSession.user_id.in_(all_company_staff_id),
        NextConsoleSession.session_source.isnot(None),
        NextConsoleSession.session_source != ''
    ).join(
        NextConsoleQa,
        NextConsoleSession.id == NextConsoleQa.session_id
    ).with_entities(
        NextConsoleSession.session_source,
        func.count(NextConsoleQa.qa_id).label('qa_count')
    ).group_by(
        NextConsoleSession.session_source
    ).order_by(
        func.count(distinct(NextConsoleQa.qa_id)).desc()
    ).limit(top).all()
    all_app_codes = [item.session_source for item in session_sources]
    source_apps = AppMetaInfo.query.filter(
        AppMetaInfo.app_code.in_(all_app_codes),
        AppMetaInfo.app_status == '正常',
        AppMetaInfo.environment == '生产'
    ).all()
    source_app_map = {app.app_code: {
        "app_name": app.app_name,
        "app_code": app.app_code,
        "app_desc": app.app_desc,
        "app_icon": app.app_icon
    } for app in source_apps}
    session_sources = [
        {
            "app_info": source_app_map.get(item.session_source, {}),
            "qa_count": item.qa_count
        }
        for item in session_sources if item.session_source in source_app_map
    ]
    return next_console_response(result={
        "app_rank_qa": session_sources,
        "begin_time": begin_time,
        "end_time": end_time
    })


def get_app_active_token_rank(params):
    """
    获取基于消耗token数的应用排名
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
    top = params.get('top', 50)
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    session_sources = NextConsoleSession.query.filter(
        NextConsoleSession.create_time.between(begin_time, end_time),
        NextConsoleSession.user_id.in_(all_company_staff_id),
        NextConsoleSession.session_source.isnot(None),
        NextConsoleSession.session_source != ''
    ).join(
        NextConsoleMessage,
        NextConsoleSession.id == NextConsoleMessage.session_id
    ).with_entities(
        NextConsoleSession.session_source,
        func.sum(NextConsoleMessage.msg_token_used).label('token_count')
    ).group_by(
        NextConsoleSession.session_source
    ).order_by(
        func.sum(NextConsoleMessage.msg_token_used).label('token_count').desc()
    ).limit(top).all()
    all_app_codes = [item.session_source for item in session_sources]
    source_apps = AppMetaInfo.query.filter(
        AppMetaInfo.app_code.in_(all_app_codes),
        AppMetaInfo.app_status == '正常',
        AppMetaInfo.environment == '生产'
    ).all()
    source_app_map = {app.app_code: {
        "app_name": app.app_name,
        "app_code": app.app_code,
        "app_desc": app.app_desc,
        "app_icon": app.app_icon
    } for app in source_apps}
    session_sources = [
        {
            "app_info": source_app_map.get(item.session_source, {}),
            "token_count": item.token_count
        }
        for item in session_sources if item.session_source in source_app_map
    ]
    return next_console_response(result={
        "app_rank_token": session_sources,
        "begin_time": begin_time,
        "end_time": end_time
    })


def get_user_latest_questions(params):
    """
    获取用户的最新提问列表
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
    top = params.get('top', 50)
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    all_msgs = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time.between(begin_time, end_time),
        NextConsoleMessage.user_id.in_(all_company_staff_id),
        NextConsoleMessage.msg_role == 'user',
    ).order_by(
        NextConsoleMessage.create_time.desc()
    ).limit(top).all()
    # 补充用户信息
    all_user_ids = list(set([msg.user_id for msg in all_msgs]))
    user_info_map = {}
    if all_user_ids:
        all_users = UserInfo.query.filter(UserInfo.user_id.in_(all_user_ids)).all()
        user_info_map = {
            user.user_id: {
                "user_name": user.user_name,
                "user_avatar": user.user_avatar,
                "user_nick_name": user.user_nick_name,
                "user_nick_name_py": user.user_nick_name_py,
                "user_company": user.user_company,
                "user_department": user.user_department,
                "user_id": user.user_id,
            } for user in all_users
        }
    msg_list = [{
        "msg_id": msg.msg_id,
        "user_id": msg.user_id,
        "session_id": msg.session_id,
        "msg_content": msg.msg_content,
        "create_time": msg.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        "user_info": user_info_map.get(msg.user_id, {})
    } for msg in all_msgs]
    return next_console_response(result={
        "latest_questions": msg_list,
        "begin_time": begin_time,
        "end_time": end_time
    })


def get_qa_topic(params):
    """
    获取基于话题的QA分布情况
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
    top = params.get('top', 20)
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    qa_topics = NextConsoleQa.query.filter(
        NextConsoleQa.create_time.between(begin_time, end_time),
        NextConsoleQa.user_id.in_(all_company_staff_id),
        NextConsoleQa.qa_topic.isnot(None),
        NextConsoleQa.qa_topic != ''
    ).with_entities(
        NextConsoleQa.qa_topic,
        func.count(NextConsoleQa.qa_id).label('qa_count')
    ).group_by(
        NextConsoleQa.qa_topic
    ).order_by(
        func.count(NextConsoleQa.qa_id).desc()
    ).limit(top).all()
    qa_topics = [
        {
            "qa_topic": item.qa_topic,
            "qa_count": item.qa_count
        }
        for item in qa_topics
    ]
    return next_console_response(result={
        "qa_topic": qa_topics,
        "begin_time": begin_time,
        "end_time": end_time
    })














