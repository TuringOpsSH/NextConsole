from app.services.configure_center.response_utils import next_console_response
from app.models.resource_center.resource_model import ResourceTag, ResourceTagRelation
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.models.user_center.user_info import UserInfo
from app.app import db
from datetime import datetime
from sqlalchemy import or_


def add_resource_tag(params):
    """
    添加资源标签
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    tag_name = params.get("tag_name")
    tag_type = params.get("tag_type")
    tag_desc = params.get("tag_desc")
    tag_source = params.get("tag_source")
    tag_value = params.get("tag_value")
    tag_status = params.get("tag_status")
    tag_icon = params.get("tag_icon")
    tag_color = params.get("tag_color")

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1002, error_message="用户不存在")
    new_tag = ResourceTag(
        tag_name=tag_name,
        tag_type=tag_type,
        tag_desc=tag_desc,
        tag_source=tag_source,
        tag_value=tag_value,
        tag_status=tag_status,
        tag_icon=tag_icon,
        tag_color=tag_color,
        user_id=user_id
    )
    db.session.add(new_tag)
    db.session.commit()
    return next_console_response(result=new_tag.show_info())


def search_resource_tag(params):
    """
    搜索资源标签
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    tag_list = params.get("tag_list")
    tag_keyword = params.get("tag_keyword")
    page_size = params.get("page_size", 10)
    page_num = params.get("page_num", 1)
    fetch_all = params.get("fetch_all", False)

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1002, error_message="用户不存在")
    all_condition = [
        ResourceTag.user_id == user_id,
    ]
    if tag_keyword:
        all_condition.append(
            or_(
                ResourceTag.tag_name.like(f"%{tag_keyword}%"),
                ResourceTag.tag_desc.like(f"%{tag_keyword}%")
        ))
    if tag_list:
        all_condition.append(
            ResourceTag.id.in_(tag_list)
        )
    query = ResourceTag.query.filter(
        *all_condition
    ).order_by(ResourceTag.update_time.desc())
    if not fetch_all:
        query = query.limit(page_size).offset((page_num - 1) * page_size)
    tags = query.all()
    all_tags_id = [tag.id for tag in tags]
    all_related_resources = ResourceTagRelation.query.filter(
        ResourceTagRelation.tag_id.in_(all_tags_id)
    ).join(
        ResourceObjectMeta,
        ResourceObjectMeta.id == ResourceTagRelation.resource_id
    ).filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center"
    ).group_by(ResourceTagRelation.tag_id).with_entities(
        ResourceTagRelation.tag_id,
        db.func.count(ResourceTagRelation.resource_id).label("resource_count")
    ).all()

    related_resources_dict = {resource.tag_id: resource.resource_count for resource in all_related_resources}
    res = []
    for tag in tags:
        tag_dict = tag.show_info()
        tag_dict["tag_count"] = related_resources_dict.get(tag.id, 0)
        res.append(tag_dict)
    return next_console_response(result=res)


def delete_resource_tag(params):
    """
    删除资源标签
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    tag_list = params.get("tag_list")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1002, error_message="用户不存在")
    delete_tags = ResourceTag.query.filter(
        ResourceTag.id.in_(tag_list)
    ).all()
    for tag in delete_tags:
        db.session.delete(tag)
    db.session.commit()
    return next_console_response(result={
        "delete_count": len(delete_tags)
    })


def update_resource_tag(params):
    """
    更新资源标签
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    tag_id = params.get("tag_id")
    tag_name = params.get("tag_name")
    tag_desc = params.get("tag_desc")
    tag_color = params.get("tag_color")
    tag_icon = params.get("tag_icon")
    tag_status = params.get("tag_status")
    tag_click = params.get("tag_click")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1002, error_message="用户不存在")
    target_tag = ResourceTag.query.filter(
        ResourceTag.id == tag_id
    ).first()
    if not target_tag:
        return next_console_response(error_status=True, error_code=1002, error_message="标签不存在")
    if tag_name:
        target_tag.tag_name = tag_name
    if tag_desc is not None:
        target_tag.tag_desc = tag_desc
    if tag_color:
        target_tag.tag_color = tag_color
    if tag_icon:
        target_tag.tag_icon = tag_icon
    if tag_status:
        target_tag.tag_status = tag_status
    if tag_click:
        target_tag.update_time = datetime.now()
    db.session.add(target_tag)
    db.session.commit()
    return next_console_response(result=target_tag.show_info())


def get_resource_tag(params):
    """
    获取资源标签
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    tag_id = params.get("tag_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1002, error_message="用户不存在")
    target_tag = ResourceTag.query.filter(
        ResourceTag.id == tag_id
    ).first()
    if not target_tag:
        return next_console_response(error_status=True, error_code=1002, error_message="标签不存在")
    return next_console_response(result=target_tag.to_dict())


def add_resource_tag_for_resource(params):
    """
    使用资源标签
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    tag_id = params.get("tag_id")
    resource_list = params.get("resource_list")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1002, error_message="用户不存在")
    target_tag = ResourceTag.query.filter(
        ResourceTag.id == tag_id
    ).first()
    if not target_tag:
        return next_console_response(error_status=True, error_code=1002, error_message="标签不存在")
    target_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(resource_list),
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常"
    ).all()
    if not target_resources:
        return next_console_response(error_status=True, error_code=1002, error_message="资源不存在")
    # 过滤掉已经存在的关系
    exist_relations = ResourceTagRelation.query.filter(
        ResourceTagRelation.tag_id == tag_id,
        ResourceTagRelation.resource_id.in_(resource_list)
    ).all()
    exist_resource_ids = [relation.resource_id for relation in exist_relations]
    new_relations = []
    for resource in target_resources:
        if resource.id not in exist_resource_ids:
            new_relation = ResourceTagRelation(
                tag_id=tag_id,
                resource_id=resource.id
            )
            new_relations.append(new_relation)
            db.session.add(new_relation)
    db.session.commit()
    new_relations = [relation.to_dict() for relation in new_relations]
    return next_console_response(result=new_relations)


def remove_resource_tag_for_resource(params):
    """
    移除资源标签
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    tag_id = params.get("tag_id")
    resource_list = params.get("resource_list")
    rel_list = params.get("rel_list")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1002, error_message="用户不存在")
    target_tag = ResourceTag.query.filter(
        ResourceTag.id == tag_id
    ).first()
    if not target_tag:
        return next_console_response(error_status=True, error_code=1002, error_message="标签不存在")
    target_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(resource_list),
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常"
    ).all()
    resource_list = [resource.id for resource in target_resources]
    # 过滤掉不存在的关系
    exist_relations = ResourceTagRelation.query.filter(
        ResourceTagRelation.tag_id == tag_id,
        or_(
            ResourceTagRelation.resource_id.in_(resource_list),
            ResourceTagRelation.id.in_(rel_list)
        )
    ).all()

    for relation in exist_relations:
        db.session.delete(relation)
    db.session.commit()
    return next_console_response(result={
        "delete_count": len(exist_relations)
    })


def list_resource_tag_for_resource(params):
    """
    获取资源标签下的资源
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    tag_id = params.get("tag_id")
    page_size = params.get("page_size", 10)
    page_num = params.get("page_num", 1)
    fetch_all = params.get("fetch_all", False)

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1002, error_message="用户不存在")

    target_tag = ResourceTag.query.filter(
        ResourceTag.id == tag_id,
        ResourceTag.user_id == user_id
    ).first()
    if not target_tag:
        return next_console_response(error_status=True, error_code=1002, error_message="标签不存在")

    list_resources = ResourceTagRelation.query.filter(
        ResourceTagRelation.tag_id == tag_id
    ).join(
        ResourceObjectMeta,
        ResourceObjectMeta.id == ResourceTagRelation.resource_id
    ).filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常"
    ).with_entities(
        ResourceObjectMeta
    )
    if not fetch_all:
        list_resources = list_resources.limit(page_size).offset((page_num - 1) * page_size)
    list_resources = list_resources.all()
    res = [resource.show_info() for resource in list_resources]
    return next_console_response(result=res)

