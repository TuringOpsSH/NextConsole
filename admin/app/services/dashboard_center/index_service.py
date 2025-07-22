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
    uv_hour = NextConsoleSession.query.filter(
        NextConsoleSession.session_source == "next_search",
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
    qa_hour = NextConsoleSession.query.filter(
        NextConsoleSession.session_source == "next_search",
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
    uv_day = NextConsoleSession.query.filter(
        NextConsoleSession.session_source == "next_search",
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
    qa_day = NextConsoleSession.query.filter(
        NextConsoleSession.session_source == "next_search",
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
    session = NextConsoleSession.query.filter(
        NextConsoleSession.create_time.between(begin_time, end_time),
        NextConsoleSession.user_id.in_(all_company_staff_id),
        NextConsoleSession.session_source == "next_search"
    ).count()
    return next_console_response(result={"session": session, "begin_time": begin_time, "end_time": end_time})


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

    session_hour = NextConsoleSession.query.filter(
        NextConsoleSession.create_time.between(begin_time, end_time),
        NextConsoleSession.user_id.in_(all_company_staff_id),
        NextConsoleSession.session_source == "next_search"
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
    session_day = NextConsoleSession.query.filter(
        NextConsoleSession.create_time.between(begin_time, end_time),
        NextConsoleSession.user_id.in_(all_company_staff_id),
        NextConsoleSession.session_source == "next_search"
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


def get_doc_download_count(params):
    """
    获取文档下载次数
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
    doc_download_count = ResourceDownloadRecord.query.filter(
        ResourceDownloadRecord.create_time.between(begin_time, end_time),
        ResourceDownloadRecord.user_id.in_(all_company_staff_id)
    ).count()
    return next_console_response(result={
        "doc_download_count": doc_download_count,
        "begin_time": begin_time,
        "end_time": end_time}
    )


def get_doc_download_top(params):
    """
    获取文档下载次数排行榜
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
    top = params.get('top')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    doc_download_top = ResourceDownloadRecord.query.filter(
        ResourceDownloadRecord.create_time.between(begin_time, end_time),
        ResourceDownloadRecord.user_id.in_(all_company_staff_id)
    ).with_entities(
        ResourceDownloadRecord.resource_id,
        func.count(ResourceDownloadRecord.id).label('download_count')
    ).group_by(
        ResourceDownloadRecord.resource_id
    ).order_by(
        func.count(ResourceDownloadRecord.id).desc()
    ).limit(
        top
    ).all()
    doc_download_top = [{"resource_id": item.resource_id, "download_count": item.download_count}
                        for item in doc_download_top]
    all_doc_id = [item["resource_id"] for item in doc_download_top]
    doc_info = ResourceObjectMeta.query.filter(ResourceObjectMeta.id.in_(all_doc_id)).all()
    doc_info_dict = {item.id: item.to_dict() for item in doc_info}
    for item in doc_download_top:
        item.update(doc_info_dict.get(item["resource_id"], {}))
    return next_console_response(result={
        "doc_download_top": doc_download_top,
        "begin_time": begin_time,
        "end_time": end_time}
    )


def get_user_download_top(params):
    """
    获取用户下载次数排行榜
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
    top = params.get('top', 10)
    user_download_top = ResourceDownloadRecord.query.filter(
        ResourceDownloadRecord.create_time.between(begin_time, end_time),
        ResourceDownloadRecord.user_id.in_(all_company_staff_id)
    ).with_entities(
        ResourceDownloadRecord.user_id,
        func.count(ResourceDownloadRecord.id).label('download_count')
    ).group_by(
        ResourceDownloadRecord.user_id
    ).order_by(
        func.count(ResourceDownloadRecord.id).desc()
    ).limit(
        top
    ).all()
    user_download_top = [{"user_id": item.user_id, "download_count": item.download_count} for item in user_download_top]
    all_user_id = [item["user_id"] for item in user_download_top]
    user_info = UserInfo.query.filter(UserInfo.user_id.in_(all_user_id)).all()
    user_info_dict = {item.user_id: {
        "user_avatar": item.user_avatar,
        "user_name": item.user_name,
        "user_company": item.user_company,
        "user_department": item.user_department,
        "user_id": item.user_id,
    } for item in user_info}
    # 删除敏感信息

    for item in user_download_top:
        item.update(user_info_dict.get(item["user_id"], {}))
    return next_console_response(result={
        "user_download_top": user_download_top,
        "begin_time": begin_time,
        "end_time": end_time}
    )


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

    subquery = NextConsoleSession.query.filter(
        NextConsoleSession.user_id.in_(all_company_staff_id),
        NextConsoleSession.session_source == 'next_search'
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
    subquery = NextConsoleSession.query.filter(
        NextConsoleSession.user_id.in_(all_company_staff_id),
        NextConsoleSession.session_source == 'next_search',
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


def get_doc_read_count(params):
    """
    获取文档阅读次数
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
    all_document_view_record = ResourceViewRecord.query.filter(
        ResourceViewRecord.user_id.in_(all_company_staff_id),
        ResourceViewRecord.create_time.between(begin_time, end_time)
    ).with_entities(
        ResourceViewRecord.resource_id
    ).distinct().count()
    return next_console_response(result={"doc_read_count": all_document_view_record,
                                         "begin_time": begin_time, "end_time": end_time})


def get_doc_view_top(params):
    """
    获取文档阅读次数top
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
    top = params.get('top')
    company_id = params.get('company_id')
    if company_id:
        if company_id == "all":
            all_company_staff = UserInfo.query.all()
        else:
            all_company_staff = UserInfo.query.filter_by(user_company_id=company_id).all()
    else:
        all_company_staff = UserInfo.query.filter_by(user_company_id=request_user.user_company_id).all()
    all_company_staff_id = [staff.user_id for staff in all_company_staff]
    doc_view_top = ResourceViewRecord.query.filter(
        ResourceViewRecord.create_time.between(begin_time, end_time),
        ResourceViewRecord.user_id.in_(all_company_staff_id)
    ).with_entities(
        ResourceViewRecord.resource_id,
        func.count(ResourceViewRecord.id).label('download_count')
    ).group_by(
        ResourceViewRecord.resource_id
    ).order_by(
        func.count(ResourceViewRecord.id).desc()
    ).limit(
        top
    ).all()
    doc_view_top = [{"resource_id": item.resource_id, "view_count": item.download_count}
                        for item in doc_view_top]
    all_doc_id = [item["resource_id"] for item in doc_view_top]
    doc_info = ResourceObjectMeta.query.filter(ResourceObjectMeta.id.in_(all_doc_id)).all()
    doc_info_dict = {item.id: item.to_dict() for item in doc_info}
    for item in doc_view_top:
        item.update(doc_info_dict.get(item["resource_id"], {}))
    return next_console_response(result={
        "doc_view_top": doc_view_top,
        "begin_time": begin_time,
        "end_time": end_time}
    )


def get_user_view_resource_top(params):
    """
    获取用户查看资源top
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
    top = params.get('top', 10)
    user_view_resource_top = ResourceViewRecord.query.filter(
        ResourceViewRecord.create_time.between(begin_time, end_time),
        ResourceViewRecord.user_id.in_(all_company_staff_id)
    ).with_entities(
        ResourceViewRecord.user_id,
        func.count(ResourceViewRecord.id).label('view_resource_count')
    ).group_by(
        ResourceViewRecord.user_id
    ).order_by(
        func.count(ResourceViewRecord.id).desc()
    ).limit(
        top
    ).all()
    user_view_resource_top = [{"user_id": item.user_id, "view_count": item.view_resource_count}
                              for item in user_view_resource_top]
    all_user_id = [item["user_id"] for item in user_view_resource_top]
    user_info = UserInfo.query.filter(UserInfo.user_id.in_(all_user_id)).all()
    user_info_dict = {item.user_id: {
        "user_avatar": item.user_avatar,
        "user_name": item.user_name,
        "user_company": item.user_company,
        "user_department": item.user_department,
        "user_id": item.user_id,
    } for item in user_info}
    # 删除敏感信息
    for item in user_view_resource_top:
        item.update(user_info_dict.get(item["user_id"], {}))
    return next_console_response(result={
        "user_view_resource_top": user_view_resource_top,
        "begin_time": begin_time,
        "end_time": end_time}
    )
