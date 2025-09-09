from app.services.configure_center.response_utils import next_console_response
from app.models.user_center.user_info import SubscriptionInfo, UserInviteCodeViewRecord
from app.app import db
from app.services.task_center.celery_fun_libs import send_user_first_subscription_email


def add_subscribe_service(data):
    """
    订阅公司邮件
    """
    email = data.get("email")
    # 判断是否已经订阅
    subscription_info = SubscriptionInfo.query.filter(
        SubscriptionInfo.email == email,
    ).first()
    if not subscription_info:
        subscription_info = SubscriptionInfo(
            email=email,
            subscribe_status="正常"
        )
        db.session.add(subscription_info)
        db.session.commit()
        # 发生首封订阅邮件
        send_user_first_subscription_email.delay(email)
        return next_console_response(result=subscription_info.to_dict())
    if subscription_info.subscribe_status == "正常":
        return next_console_response(error_message="您已经成功订阅！")
    else:
        subscription_info.subscribe_status = "正常"
        db.session.add(subscription_info)
        db.session.commit()
        # 发生订阅邮件
        send_user_first_subscription_email.delay(email)
        return next_console_response(result=subscription_info.to_dict())


def cancel_subscribe_service(data):
    """
    取消订阅公司邮件
    """
    email = data.get("email")
    subscription_info = SubscriptionInfo.query.filter(
        SubscriptionInfo.email == email,
    ).first()
    if not subscription_info:
        subscription_info = SubscriptionInfo(
            email=email,
            subscribe_status="禁用"
        )
        db.session.add(subscription_info)
        db.session.commit()
        return next_console_response(result=subscription_info.to_dict())
    if subscription_info.subscribe_status == "禁用":
        return next_console_response(error_message="您已经取消订阅！")
    subscription_info.subscribe_status = "禁用"
    db.session.add(subscription_info)
    db.session.commit()
    return next_console_response(result=subscription_info.to_dict())


def valid_invite_service(data):
    """
    验证邀请id合法性
    :param data:
    :return:
    """
    try:
        invite_id = int(data.get("invite_id"))
    except Exception as e:
        return next_console_response(error_message="邀请id错误！")
    invite_record = UserInviteCodeViewRecord.query.filter(
        UserInviteCodeViewRecord.id == invite_id,
    ).first()
    if not invite_record:
        return next_console_response(error_message="邀请id错误！")
    res = {
        "valid": True
    }
    if invite_record.user_id == 1 or not invite_record.marketing_code:
        res["homepage"] = True
    return next_console_response(result=res)

