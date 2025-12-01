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
        "user_nick_name": item.user_nick_name,
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
        "user_nick_name": item.user_nick_name,
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

