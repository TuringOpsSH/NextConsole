from datetime import datetime, timedelta

from app import app
from app.models.knowledge_center.rag_ref_model import RagRefInfo
from app.models.resource_center.resource_model import *
from app.models.user_center.user_info import UserInfo
from app.services.configure_center.response_utils import next_console_response
from app.services.resource_center.resource_object_service import get_resource_object_path
from app.services.task_center.resources_center import clean_resource_file


def search_in_recycle_bin(params):
    """
    在回收站中搜索资源，新增返回删除时间，剩余时间等信息
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_type = params.get("resource_type", [])
    resource_format = params.get("resource_format", [])
    resource_tags = params.get("resource_tags", [])
    resource_keyword = params.get("resource_keyword", "")
    rag_enhance = params.get("rag_enhance", False)
    page_size = params.get("page_size", 50)
    page_num = params.get("page_num", 1)
    fetch_all = params.get("fetch_all", False)

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")

    all_conditions = [
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == '删除',
        ResourceObjectMeta.resource_source == 'resource_center'
    ]

    if resource_type:
        all_conditions.append(ResourceObjectMeta.resource_type.in_(resource_type))

    if resource_format:
        all_conditions.append(ResourceObjectMeta.resource_format.in_(resource_format))

    if resource_keyword:
        all_conditions.append(ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%"))

    all_resources = ResourceObjectMeta.query.filter(*all_conditions)
    if resource_tags:
        user_tags = ResourceTag.query.filter(
            ResourceTag.user_id == user_id,
            ResourceTag.tag_status == "正常",
            ResourceTag.id.in_(resource_tags)
        ).all()
        legal_tags = [tag.id for tag in user_tags]
        all_resources = all_resources.join(
            ResourceTagRelation,
            ResourceTagRelation.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceTagRelation.tag_id.in_(legal_tags)
        ).with_entities(
            ResourceObjectMeta
        )
    if rag_enhance:
        pass
    all_resources_results = all_resources.order_by(
        ResourceObjectMeta.create_time.desc()
    )
    # 组装返回结果
    total = all_resources_results.count()
    if not fetch_all:
        res = all_resources_results.paginate(page=page_num, per_page=page_size, error_out=False)
    else:
        res = all_resources_results.all()
    # 新增剩余时间
    from datetime import timezone
    now_time = datetime.now(timezone.utc)
    new_res = []
    for resource in res:
        resource_info = resource.show_info()
        # 计算距离删除75天的剩余时间
        finnish_time = resource.delete_time + timedelta(days=75)
        left_time = (finnish_time - now_time).days
        resource_info["left_time"] = left_time
        new_res.append(resource_info)
    return next_console_response(result={
        "data": new_res,
        "total": total
    })


def delete_resource_recycle_object(params):
    """
    彻底删除资源对象
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    clean_all = params.get("clean_all", False)
    resource_list = params.get("resource_list")

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_delete_data = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "删除"
    ).all()
    all_resource_paths = []
    if clean_all:
        for resource in all_delete_data:
            all_resource_paths.append(resource.resource_path)
            db.session.delete(resource)
    else:
        all_selected_resource_id = resource_list
        # 找到所有子资源
        all_cnt = len(all_selected_resource_id)
        while all_cnt > 0:
            all_cnt = 0
            for resource in all_delete_data:
                if resource.resource_parent_id in all_selected_resource_id and resource.id not in all_selected_resource_id:
                    all_selected_resource_id.append(resource.id)
                    all_cnt += 1
        for resource in all_delete_data:
            if resource.id in all_selected_resource_id:
                all_resource_paths.append(resource.resource_path)
                db.session.delete(resource)
    db.session.commit()
    task_params = {
        "resource_paths": all_resource_paths
    }
    clean_resource_file.delay(task_params)
    return next_console_response(result={
        "delete_cnt": len(all_resource_paths),
        "message": "删除成功！"

    })


def recover_resource_recycle_object(params):
    """
    恢复资源对象
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_list = params.get("resource_list")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_recover_data = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "删除",
        ResourceObjectMeta.resource_source == 'resource_center'
    ).all()
    all_selected_resource_id = resource_list
    # 找到所有子资源
    all_cnt = len(all_selected_resource_id)
    all_recover_size = 0
    while all_cnt > 0:
        all_cnt = 0
        for resource in all_recover_data:
            if resource.resource_parent_id in all_selected_resource_id and resource.id not in all_selected_resource_id:
                all_selected_resource_id.append(resource.id)
                all_cnt += 1
                all_recover_size += resource.resource_size
    # 计算是否超过用户资源上限
    user_resource_limit = target_user.user_resource_limit
    all_resource_usage = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常"
    ).with_entities(
        func.sum(ResourceObjectMeta.resource_size_in_MB).label("total_size")
    ).first()
    all_resource_usage = all_resource_usage.total_size if all_resource_usage else 0
    if all_resource_usage + all_recover_size > user_resource_limit:
        return next_console_response(error_status=True, error_message="资源容量超出限制！")

    for resource in all_recover_data:
        if resource.id in all_selected_resource_id:
            resource.resource_status = "正常"
            db.session.add(resource)
    db.session.commit()
    return next_console_response(result={
        "recover_cnt": len(all_selected_resource_id),
        "message": "恢复成功！"
    })


def get_resource_recycle_object(params):
    """
    获取删除资源的详细信息
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_id = params.get("resource_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == "删除",
        ResourceObjectMeta.resource_source == 'resource_center'
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    result = target_resource.show_info()
    # 如果是folder，增加资源大小与子资源数量统计
    if target_resource.resource_type == "folder":
        all_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == "删除",
            ResourceObjectMeta.resource_source == 'resource_center'
        ).all()
        all_sub_resource_ids = [target_resource.id]
        add_cnt = 1
        while add_cnt > 0:
            add_cnt = 0
            for resource_item in all_resources:
                if (resource_item.resource_parent_id in all_sub_resource_ids
                        and resource_item.id not in all_sub_resource_ids):
                    all_sub_resource_ids.append(resource_item.id)
                    add_cnt += 1
        sub_resource_list = [resource_item for resource_item in all_resources
                             if resource_item.id in all_sub_resource_ids]
        sub_dir = [resource_item for resource_item in sub_resource_list if resource_item.resource_type == "folder"]
        all_size = sum([resource_item.resource_size_in_MB for resource_item in sub_resource_list])
        result["resource_size_in_MB"] = all_size
        result["sub_resource_dir_cnt"] = len(sub_dir)
        result["sub_resource_file_cnt"] = len(sub_resource_list) - len(sub_dir)
        # rag资源数量
        all_rag_ref_info = RagRefInfo.query.filter(
            RagRefInfo.resource_id.in_(all_sub_resource_ids),
            RagRefInfo.ref_status == "成功"
        ).all()
        result["sub_rag_file_cnt"] = len(all_rag_ref_info)
    # 新增路径信息
    try:
        resource_path_res = get_resource_object_path({
            "user_id": user_id,
            "resource_id": target_resource.id,
            "resource_status": "删除"
        }).json
        resource_path = resource_path_res.get("result").get("data")
        if not resource_path:
            return next_console_response(result=[])
        resource_path = [resource_item.get("resource_name") for resource_item in resource_path]
    except Exception as e:
        app.logger.warning(f"获取资源路径异常：{e.args}")
        resource_path = []
    result["resource_path"] = "/".join(resource_path)
    # 返回资源ref状态
    rag = RagRefInfo.query.filter(
        RagRefInfo.resource_id == resource_id
    ).order_by(
        RagRefInfo.create_time.desc()
    ).first()
    if rag:
        result["ref_status"] = rag.ref_status
    # 新增Tag信息
    all_tags = ResourceTagRelation.query.filter(
        ResourceTagRelation.resource_id == resource_id,
        ResourceTagRelation.rel_status == "正常"
    ).join(
        ResourceTag,
        ResourceTagRelation.tag_id == ResourceTag.id
    ).with_entities(
        ResourceTag
    ).all()
    result["resource_tags"] = [tag.show_info() for tag in all_tags]
    return next_console_response(result=result)


