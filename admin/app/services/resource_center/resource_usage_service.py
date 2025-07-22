from app.models.user_center.user_info import UserInfo
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.services.configure_center.response_utils import next_console_response


def get_resource_usage(params):
    """
    获取资源使用情况
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_resource_usage = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center"
    ).all()
    usage = 0
    for resource in all_resource_usage:
        usage += resource.resource_size_in_MB
    return next_console_response(result={"usage": round(usage, 2)})

