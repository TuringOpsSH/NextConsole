from functools import wraps

from app.models.resource_center.resource_model import *
from app.services.configure_center.response_utils import next_console_response


def validate_resource(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        params = args[0] if args else {}
        resource_id = params.get("resource_id")
        # 验证资源ID是否为空
        if not resource_id:
            return next_console_response(
                error_status=True,
                error_message="资源ID不能为空！",
                error_code=1002
            )
        # 查询资源是否存在
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource_id,
            ResourceObjectMeta.resource_status == "正常"
        ).first()
        if not target_resource:
            return next_console_response(
                error_status=True,
                error_message="资源不存在！",
                error_code=1002
            )
        # 将资源对象添加到参数中
        params["target_resource"] = target_resource
        return func(*args, **kwargs)

    return wrapper
