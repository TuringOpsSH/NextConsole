from app.models.user_center.system_notice_model import SystemNotice
from app.services.configure_center.response_utils import next_console_response
from app.app import db
from app.services.configure_center.system_notice_service import send_new_system_notice


def add_system_notice_service(params):
    """
    添加系统通知
    :param params:
    notice_icon
        notice_success.svg notice_primary.svg  notice_warning.svg  notice_error.svg
    :return:
    """
    user_id = params.get("user_id")
    notice_title = params.get("notice_title", "系统通知")
    notice_icon = params.get("notice_icon", "notice_primary.svg")
    notice_type = params.get("notice_type", "系统通知")
    notice_level = params.get("notice_level", "普通")
    notice_content = params.get("notice_content", "123")
    notice_status = params.get("notice_status", "未读")
    new_notice = SystemNotice(
        user_id=user_id,
        notice_title=notice_title,
        notice_icon=notice_icon,
        notice_type=notice_type,
        notice_level=notice_level,
        notice_content=notice_content,
        notice_status=notice_status
    )
    db.session.add(new_notice)
    db.session.commit()
    # 推送至前端
    send_new_system_notice(
        {
            "user_id": user_id,
            "data": new_notice.to_dict()
        }
    )
    return next_console_response(result=new_notice.to_dict())


def get_system_notice_service(params):
    """
    获取系统通知
    :param params:
    :return:
    """
    user_id = params.get("user_id")
    page = params.get("page", 1)
    page_size = params.get("page_size", 50)
    fetch_all = params.get("fetch_all", False)
    status = params.get("status")
    filter_conditions = [
        SystemNotice.user_id == user_id,
    ]
    if status is not None:
        filter_conditions.append(
            SystemNotice.notice_status == status
        )
    notice_list = SystemNotice.query.filter(
        *filter_conditions
    ).order_by(
        SystemNotice.create_time.desc()
    )
    if not fetch_all:
        notice_list = notice_list.paginate(page=page, per_page=page_size, error_out=False)
    else:
        notice_list = notice_list.all()
    notice_list = [notice.to_dict() for notice in notice_list]
    return next_console_response(result=notice_list)


def set_system_notices_read_service(params):
    """
    更新系统通知
    :param params:
    :return:
    """
    user_id = params.get("user_id")
    notice_id = params.get("notice_id")
    read_all = params.get("read_all", False)
    if read_all:
        target_notices = SystemNotice.query.filter(
            SystemNotice.user_id == user_id,
            SystemNotice.notice_status == "未读"
        ).all()
        for notice in target_notices:
            notice.notice_status = "已读"
            db.session.add(notice)
        db.session.commit()
        return next_console_response(result=[notice.to_dict() for notice in target_notices])
    target_notice = SystemNotice.query.filter(
        SystemNotice.id == notice_id,
        SystemNotice.user_id == user_id
    ).first()
    if not target_notice:
        return next_console_response(error_status=True, error_message="通知不存在！")
    target_notice.notice_status = "已读"
    db.session.add(target_notice)
    db.session.commit()
    return next_console_response(result=target_notice.to_dict())


