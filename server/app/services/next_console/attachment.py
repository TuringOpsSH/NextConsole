import base64
import os
import uuid
import time
from sqlalchemy import or_, func, distinct
from app.app import db, app
from app.models.assistant_center.assistant import AssistantInstruction
from app.models.knowledge_center.rag_ref_model import RagRefInfo
from app.models.next_console.next_console_model import NextConsoleSession, SessionAttachmentRelation
from app.models.app_center.app_info_model import WorkFlowTaskInfo
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.models.user_center.user_info import UserInfo
from app.services.configure_center.response_utils import next_console_response
from app.services.resource_center.resource_object_service import generate_resource_path
from app.services.task_center.resources_center import attachment_multiple_webpage_tasks
from app.services.task_center.workflow import emit_workflow_status
from app.services.knowledge_center.rag_service_v3 import rag_query_v3
from app.services.resource_center.resource_share_service import search_share_resource_by_keyword
from app.services.resource_center.resource_share_service import check_user_manage_access_to_resource
from app.utils.oss.oss_client import generate_download_url


def init_attachment_base(params):
    """
    初始化附件基础存储
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    session_id = params.get('session_id')
    resource_source = params.get('resource_source', "session")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id,
        NextConsoleSession.user_id == user_id
    ).first()
    if not target_session:
        return next_console_response(error_status=True, error_message="会话不存在！")
    # 检查是否目录存在
    exist_session_base = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_name == target_session.session_code,
        ResourceObjectMeta.resource_type == "folder",
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == resource_source
    ).first()
    if exist_session_base:
        return next_console_response(result=exist_session_base.show_info())
    # 创建目录
    root_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_parent_id.is_(None),
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center"
    ).first()
    try:
        new_resource_path = generate_resource_path(
            user_resource_base_path=target_user.user_resource_base_path,
            target_resource_parent_id=root_resource.id,
            target_type="folder",
        )
    except Exception as e:
        return next_console_response(error_status=True, error_message=f"生成资源路径异常：{e.args}")
    new_session_base = ResourceObjectMeta(
        resource_parent_id=root_resource.id,
        user_id=user_id,
        resource_name=target_session.session_code,
        resource_type="folder",
        resource_icon="folder.svg",
        resource_status="正常",
        resource_source="session",
        resource_path=new_resource_path
    )
    db.session.add(new_session_base)
    db.session.flush()
    db.session.commit()
    return next_console_response(result=new_session_base.show_info())


def add_attachment_into_session(params):
    """
    添加附件到会话
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    session_id = params.get('session_id')
    resource_id = params.get('resource_id')
    attachment_source = params.get('attachment_source')
    qa_id = params.get('qa_id')
    msg_id = params.get('msg_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id,
        NextConsoleSession.user_id == user_id
    ).first()
    if not target_session:
        return next_console_response(error_status=True, error_message="会话不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")

    # 检查是否已经存在
    exist_attachment = SessionAttachmentRelation.query.filter(
          SessionAttachmentRelation.session_id == session_id,
          SessionAttachmentRelation.resource_id == resource_id
    ).first()
    if exist_attachment:
        return next_console_response(result=exist_attachment.show_info())
    # 检查权限
    if target_resource.user_id != user_id and check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "read"
    }).get("error_status"):
        return next_console_response(error_status=True, error_message="无权限使用该资源！")
    new_attachment = SessionAttachmentRelation(
        session_id=session_id,
        resource_id=resource_id,
        qa_id=qa_id,
        msg_id=msg_id,
        attachment_source=attachment_source,
        rel_status="正常"
    )
    db.session.add(new_attachment)
    db.session.flush()
    db.session.commit()
    # 生成附件download_url
    if not target_resource.resource_download_url:
        resource_download_url = generate_download_url(
            'session', target_resource.resource_path, suffix=target_resource.resource_format
        ).json.get("result")
        if not resource_download_url:
            return next_console_response(
                error_status=True, error_message="生成下载链接异常！"
            )
        if target_resource.resource_type == "image":
            target_resource.resource_show_url = resource_download_url
        target_resource.resource_download_url = resource_download_url
        db.session.add(target_resource)
        db.session.commit()
    return next_console_response(result=new_attachment.show_info())


def remove_from_session(params):
    """
    从会话中移除附件
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    session_id = params.get('session_id')
    resource_list = params.get('resource_list')
    clean_all = params.get('clean_all', False)
    attachment_source = params.get('attachment_source')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id,
        NextConsoleSession.user_id == user_id
    ).first()
    if not target_session:
        return next_console_response(error_status=True, error_message="会话不存在！")
    if clean_all and attachment_source:
        target_relation = SessionAttachmentRelation.query.filter(
            SessionAttachmentRelation.session_id == session_id,
            SessionAttachmentRelation.rel_status == "正常",
            SessionAttachmentRelation.attachment_source == attachment_source
        ).all()
        for relation in target_relation:
            relation.rel_status = "删除"
            db.session.add(relation)
        db.session.commit()
        return next_console_response(result={
            "clean_all": True,
            "clean_count": len(target_relation)
        })
    if not resource_list:
        return next_console_response(error_status=True, error_message="参数异常！")
    target_relations = SessionAttachmentRelation.query.filter(
        SessionAttachmentRelation.session_id == session_id,
        SessionAttachmentRelation.resource_id.in_(resource_list),
        SessionAttachmentRelation.rel_status == "正常"
    ).all()
    for relation in target_relations:
        relation.rel_status = "删除"
        db.session.add(relation)
    db.session.commit()
    return next_console_response(result={
        "clean_all": False,
        "clean_count": len(target_relations)
    })


def search_in_session(params):
    """
    查询会话中的附件
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    session_id = params.get('session_id')
    msg_id = params.get('msg_id')
    attachment_sources = params.get('attachment_sources', [])
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id,
        NextConsoleSession.user_id == user_id
    ).first()
    if not target_session:
        return next_console_response(error_status=True, error_message="会话不存在！")
    all_conditions = [
        SessionAttachmentRelation.session_id == session_id,
        SessionAttachmentRelation.rel_status == "正常"
    ]
    if attachment_sources:
        all_conditions.append(SessionAttachmentRelation.attachment_source.in_(attachment_sources))
    if msg_id == 0:
        all_conditions.append(SessionAttachmentRelation.msg_id.is_(None))
    target_attachments = SessionAttachmentRelation.query.filter(
        *all_conditions
    ).join(
        ResourceObjectMeta,
        SessionAttachmentRelation.resource_id == ResourceObjectMeta.id
    ).with_entities(
        SessionAttachmentRelation.attachment_source,
        ResourceObjectMeta
    ).all()
    res = []
    all_resource_ids = []
    for attachment_source, attachment in target_attachments:
        all_resource_ids.append(attachment.id)
    # 添加ref_status 状态
    all_rag_refs = RagRefInfo.query.filter(
        RagRefInfo.resource_id.in_(all_resource_ids),
    ).group_by(RagRefInfo.resource_id).with_entities(
        RagRefInfo.resource_id,
        func.max(RagRefInfo.id).label('rag_id')
    ).all()
    all_resource_rag_maps = {resource_id: rag_id for resource_id, rag_id in all_rag_refs}
    all_rag_ids = [item.rag_id for item in all_rag_refs]
    all_rag_record = RagRefInfo.query.filter(
        RagRefInfo.id.in_(all_rag_ids),
    ).with_entities(
        RagRefInfo.resource_id,
        RagRefInfo.id,
        RagRefInfo.ref_status
    ).all()
    all_rag_maps = {rag.id:rag for rag in all_rag_record}
    for attachment_source, attachment in target_attachments:
        sub_res = attachment.show_info()
        sub_res["attachment_source"] = attachment_source
        rag_id = all_resource_rag_maps.get(attachment.id)
        if rag_id:
            rag_record = all_rag_maps.get(rag_id)
            if rag_record:
                sub_res["ref_status"] = rag_record.ref_status
        res.append(sub_res)
    return next_console_response(result=res)



def get_attachment_detail(params):
    """
    获取附件详情
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    session_id = params.get('session_id')
    attachment_source = params.get('attachment_source')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    if attachment_source == "all":
        attachment_source = ["images", "files", "webpage", "resources"]
        target_attachments = SessionAttachmentRelation.query.filter(
            SessionAttachmentRelation.session_id == session_id,
            SessionAttachmentRelation.rel_status == "正常",
            SessionAttachmentRelation.attachment_source.in_(attachment_source)
        ).join(
            ResourceObjectMeta,
            SessionAttachmentRelation.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceObjectMeta.resource_status == "正常",
        ).with_entities(
            ResourceObjectMeta
        ).all()
        result = [attachment.show_info() for attachment in target_attachments]
        return next_console_response(result=result)
    target_attachments = SessionAttachmentRelation.query.filter(
        SessionAttachmentRelation.session_id == session_id,
        SessionAttachmentRelation.rel_status == "正常",
        SessionAttachmentRelation.attachment_source == attachment_source
    ).all()
    if not target_attachments:
        return next_console_response(result=[])
    target_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_([i.resource_id for i in target_attachments]),
    ).all()
    if attachment_source == "images":
        return get_attachment_images_detail(target_resources)
    elif attachment_source == "files":
        return get_attachment_files_detail(target_resources)
    elif attachment_source == "webpage":
        return get_attachment_webpage_detail(target_resources)
    elif attachment_source == "resources":
        return get_attachment_resources_detail(target_resources)
    return next_console_response(result=[resource.show_info() for resource in target_resources])


def get_attachment_images_detail(target_resources):
    """
    :param target_resources:
    :return:
    """
    # 为图片附件生成resource_show_url
    # 在download目录下生成一个软链接，指向原始文件
    for resource in target_resources:
        if resource.resource_type == "image" and not resource.resource_show_url:
            # 生成下载链接
            resource.resource_show_url = generate_download_url(
                "session",
                resource.resource_path,
                suffix=resource.resource_format
            ).json.get("result")
    db.session.commit()
    res = [resource.show_info() for resource in target_resources]
    return next_console_response(result=res)


def get_attachment_files_detail(target_resources):
    # 返回资源ref状态
    all_resource_ids = [resource_item.id for resource_item in target_resources]
    all_resource_ref = RagRefInfo.query.filter(
        RagRefInfo.resource_id.in_(all_resource_ids),
        RagRefInfo.ref_status == "成功"
    ).all()
    resource_ref_dict = {resource_item.resource_id: resource_item.ref_status for resource_item in all_resource_ref}
    # 在download目录下生成一个软链接，指向原始文件
    for resource in target_resources:
        resource.resource_show_url = generate_download_url(
            "session",
            resource.resource_path,
            suffix=resource.resource_format
        ).json.get("result")
    db.session.commit()
    res = [resource.show_info() for resource in target_resources]
    for resource_item in res:
        resource_item["ref_status"] = resource_ref_dict.get(resource_item.get("id"))
    return next_console_response(result=res)


def get_attachment_webpage_detail(target_resources):
    # 返回资源ref状态
    all_resource_ids = [resource_item.id for resource_item in target_resources]
    all_resource_ref = RagRefInfo.query.filter(
        RagRefInfo.resource_id.in_(all_resource_ids),
        RagRefInfo.ref_status == "成功"
    ).all()
    resource_ref_dict = {resource_item.resource_id: resource_item.ref_status for resource_item in all_resource_ref}
    for resource in target_resources:
        if resource.resource_type == "image" and not resource.resource_show_url:
            # 生成下载链接
            resource.resource_show_url = generate_download_url(
                "session",
                resource.resource_path,
                suffix=resource.resource_format
            ).json.get("result")
    db.session.commit()
    res = [resource.show_info() for resource in target_resources if resource.resource_type == "webpage"]
    for i in res:
        i["ref_status"] = resource_ref_dict.get(i.get("id"))
    return next_console_response(result=res)


def get_attachment_resources_detail(target_resources):
    return next_console_response(result=[resource.show_info() for resource in target_resources])


def extract_attachment_images_to_question(params):
    """
    将图片附件提取到问题中，改为url，防止图片过大，出现nginx 413错误

        [{
          "type": "image_url",
          "image_url": {
            "url": f"data:image/{base64_image_format};base64,{base64_image}",
            "detail": "high"
          },
        },{
          "type": "image_url",
          "image_url": {
            "url": f"data:image/{base64_image_format};base64,{base64_image}",
          },
        },
        ]
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    session_id = params.get('session_id')
    qa_id = params.get('qa_id')
    msg_id = params.get('msg_id')
    assistant_id = params.get('assistant_id')
    detail = params.get('detail', "auto")
    model_name = params.get('model_name', "gpt-4o")
    all_session_attachments_images = SessionAttachmentRelation.query.filter(
        SessionAttachmentRelation.session_id == session_id,
        SessionAttachmentRelation.attachment_source == "images",
        SessionAttachmentRelation.rel_status == "正常"
    ).all()
    res = []
    if not all_session_attachments_images:
        return next_console_response(result=res)
    all_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_([i.resource_id for i in all_session_attachments_images]),
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "session",
    ).all()
    for resource in all_resources:
        if resource.resource_type != "image":
            continue
        if not resource.resource_show_url:
            resource.resource_show_url = generate_download_url(
                'resource_center',
                resource.resource_path,
                suffix=resource.resource_format
            ).json.get("result")
        db.session.add(resource)
        db.session.flush()
        if resource.resource_format not in ["jpg", "jpeg", "png", "gif", "webp"]:
            continue
        if resource.resource_size_in_MB > 20:
            continue
        res.append({
            "type": "image_url",
            "image_url": {
                "url": resource.resource_show_url,
                "detail": detail
            }
        })
    # 保存指令数据
    if not res:
        return next_console_response(result=res)

    target_assistant_instruction = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == assistant_id,
        AssistantInstruction.instruction_name == "CV",
        AssistantInstruction.instruction_status == "正常"
    ).first()
    if target_assistant_instruction:
        task_params = [resource.resource_show_url for resource in all_resources
                       if resource.resource_show_url]
        new_workflow_task_info = WorkFlowTaskInfo(
            user_id=user_id,
            session_id=session_id,
            qa_id=qa_id,
            msg_id=msg_id,
            task_assistant_instruction=target_assistant_instruction.instruction_name,
            task_type=target_assistant_instruction.instruction_desc,
            task_status="finished",
            task_assistant_id=assistant_id,
            task_model_name=model_name,
            task_params=task_params,
            task_prompt='',
            task_result='',
        )
        db.session.add(new_workflow_task_info)
        db.session.flush()
        # 发送工作流日志
        emit_workflow_status.delay({
            "user_id": user_id,
            "new_task": new_workflow_task_info.to_dict()
        })

    return next_console_response(result=res)


def add_webpage_tasks(params):
    """
    添加网页任务
        新建网页资源，并加入会话，提交异步任务，返回资源id
            异步任务：下载网页，解析网页，更新资源数据，构建索引，推送状态
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    session_id = params.get('session_id')
    resource_parent_id = params.get('resource_parent_id')
    urls = params.get('urls')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id,
        NextConsoleSession.user_id == user_id
    ).first()
    if not target_session:
        return next_console_response(error_status=True, error_message="会话不存在！")
    # 异常防范：查看会话中是否已经存在相同附件，如果存在则直接返回
    exist_webpage = SessionAttachmentRelation.query.filter(
        SessionAttachmentRelation.session_id == session_id,
        SessionAttachmentRelation.attachment_source == "webpage",
        SessionAttachmentRelation.rel_status == "正常"
    ).with_entities(
        SessionAttachmentRelation.resource_id
    ).join(
        ResourceObjectMeta,
        SessionAttachmentRelation.resource_id == ResourceObjectMeta.id
    ).with_entities(
        ResourceObjectMeta
    ).filter(
        ResourceObjectMeta.resource_source_url.in_(urls),
        ResourceObjectMeta.resource_type == "webpage",
    ).all()
    if exist_webpage:
        return next_console_response(
            error_message="资源已存在！",
            result=[i.show_info() for i in exist_webpage])
    root_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.id == resource_parent_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "session"
    ).first()
    if not root_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    new_webpages = []
    for url in urls:
        # 创建资源占位
        new_resource_path = generate_resource_path(
            user_resource_base_path=target_user.user_resource_base_path,
            target_resource_parent_id=root_resource.id,
        )
        new_webpage = ResourceObjectMeta(
            resource_parent_id=root_resource.id,
            user_id=user_id,
            resource_name=url + ".html",
            resource_format="html",
            resource_title=url,
            resource_type="webpage",
            resource_icon="html.svg",
            resource_status="正常",
            resource_source="session",
            resource_source_url=url,
            resource_path=new_resource_path
        )
        db.session.add(new_webpage)
        new_webpages.append(new_webpage)
    db.session.commit()
    # 添加到会话
    resource_list = []
    for new_webpage in new_webpages:
        new_attachment = SessionAttachmentRelation(
            session_id=session_id,
            resource_id=new_webpage.id,
            attachment_source="webpage",
            rel_status="正常"
        )
        db.session.add(new_attachment)
        # 提交网页解析异步任务
        print(f"提交网页解析异步任务:{new_webpage.resource_source_url}")
        resource_list.append(new_webpage.id)
    attachment_multiple_webpage_tasks.delay(
        {
            "user_id": user_id,
            "session_id": session_id,
            "resource_list": resource_list,
        }
    )

    db.session.commit()
    return next_console_response(result=[i.show_info() for i in new_webpages])


def search_resources(params):
    """
    搜索资源，实现分页，并搜索共享资源
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    resource_keyword = params.get('resource_keyword')
    search_type = params.get('search_type', "all")
    resource_type_cn = params.get('resource_type', [])
    resource_format = params.get('resource_format', [])
    search_recently = params.get('search_recently', False)
    rag_enhance = params.get("rag_enhance", False)
    try:
        page_size = int(params.get("page_size", 50))
        page_num = int(params.get("page_num", 1))
    except ValueError:
        page_size = 50
        page_num = 1
    if search_recently:
        return search_resources_by_recent(params)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_conditions = [
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center",
    ]

    if resource_keyword:
        or_conditions = [ResourceObjectMeta.resource_name.like(f"%{resource_keyword}%"),
                         ResourceObjectMeta.resource_title.like(f"%{resource_keyword}%"),
                         ResourceObjectMeta.resource_source_url.like(f"%{resource_keyword}%"),
                         ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%")]
        all_conditions.append(or_(*or_conditions))
    if resource_type_cn:
        resource_translates = {
            "图片": "image",
            "文档": "document",
            "文件夹": "folder",
            "网页": "webpage",
            "代码": "code",
        }
        resource_type = [resource_translates.get(i) for i in resource_type_cn if resource_translates.get(i)]
        all_conditions.append(ResourceObjectMeta.resource_type.in_(resource_type))
    if resource_format:
        all_conditions.append(ResourceObjectMeta.resource_format.in_(resource_format))
    if search_type == 'file':
        all_conditions.append(ResourceObjectMeta.resource_type != 'folder')
    if search_type == 'folder':
        all_conditions.append(ResourceObjectMeta.resource_type == 'folder')
    if search_type == 'tag':
        # todo 过滤tag
        pass
    all_resources = ResourceObjectMeta.query.filter(
        *all_conditions
    ).order_by(
        ResourceObjectMeta.update_time.desc()
    ).all()

    all_resource_ids = [resource.id for resource in all_resources]
    # 过滤ref状态
    all_resource_ref = RagRefInfo.query.filter(
        RagRefInfo.resource_id.in_(all_resource_ids),
        RagRefInfo.ref_status == "成功"
    ).all()
    all_success_ref_ids = [i.resource_id for i in all_resource_ref]

    res = []
    for resource in all_resources:
        resource_dict = resource.show_info()
        # 文件夹直接加入
        if search_type in ("all", "folder") and resource.resource_type == "folder":
            res.append(resource_dict)
            continue
        # 文件过滤掉不是success的
        if search_type == "file" and resource.id not in all_success_ref_ids:
            continue
        res.append(resource_dict)

    if rag_enhance:
        rag_res = search_resources_by_rag(params).json.get("result")
        for rag_resource in rag_res:
            # 去重加入
            find_flag = False
            for key_resource in res:
                if key_resource.get("id") == rag_resource.get("id"):
                    find_flag = True
                    key_resource["rerank_score"] = rag_resource["rerank_score"]
                    key_resource["ref_text"] = rag_resource["ref_text"]
            if not find_flag:
                res.append(rag_resource)
    # 搜索共享资源
    share_res = search_share_resources(params).json.get("result")
    for share_resource in share_res.get("data"):
        # 去重添加
        find_flag = False
        for resource in res:
            if resource.get("id") == share_resource.get("id"):
                find_flag = True
                break
        if not find_flag:
            res.append(share_resource)
    # 手动分页
    # 计算分页数据
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    if start_index >= len(res):
        paged_data = []
    else:
        paged_data = res[start_index:end_index]
    author_info = share_res.get("author_info", [target_user.show_info()])

    return next_console_response(result={
        "data": paged_data,
        "total": len(res),
        "resource_tags": share_res.get("resource_tags"),
        "author_info": author_info
    })


def search_resources_by_rag(params):
    """
    通过rag搜索资源,搜索用户全部ref_id，并返回关联资源
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    resource_keyword = params.get('resource_keyword')
    resource_type_cn = params.get('resource_types', [])
    resource_formats = params.get('resource_formats', [])
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    resource_conditions = [
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center",
    ]
    if resource_formats:
        resource_conditions.append(ResourceObjectMeta.resource_format.in_(resource_formats))
    if resource_type_cn:
        resource_translates = {
            "图片": "image",
            "文档": "document",
            "文件夹": "folder",
            "网页": "webpage",
            "代码": "code",
        }
        resource_types = [resource_translates.get(i) for i in resource_type_cn if resource_translates.get(i)]
        resource_conditions.append(ResourceObjectMeta.resource_type.in_(resource_types))
    all_rag_ref = RagRefInfo.query.filter(
        RagRefInfo.user_id == user_id,
        RagRefInfo.ref_status == "成功"
    ).all()
    if not all_rag_ref:
        return next_console_response(result=[])
    all_rag_ref_ids = [i.id for i in all_rag_ref]
    rag_params = {
        "user_id": user_id,
        "query": resource_keyword,
        "ref_ids": all_rag_ref_ids,
        "config": {
            "search_engine_enhanced": False,
        }
    }
    try:
        rag_response = rag_query_v3(rag_params)
        end_time = time.time()
        # print(f'搜索资源:{round(end_time - begin_time,2)}秒', rag_response)
        reference_source = rag_response.get("reference_source", [])
        if not reference_source:
            return next_console_response(result=[])
        all_ref_ids = list(set([i.get("source") for i in reference_source]))
        # 获取所有对应资源
        all_resources = RagRefInfo.query.filter(
            RagRefInfo.ref_id.in_(all_ref_ids),
            RagRefInfo.ref_status == "成功",
            RagRefInfo.user_id == user_id
        ).join(
            ResourceObjectMeta,
            RagRefInfo.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceObjectMeta.resource_status == "正常",
        ).with_entities(
            RagRefInfo.ref_id,
            ResourceObjectMeta,
        ).all()
        details = rag_response.get("details", [])
        res = []
        for resource in all_resources:
            # 从detail中获取rerank_score最高的 text
            resource_dict = resource.ResourceObjectMeta.show_info()
            resource_dict["rerank_score"] = 0
            for detail in details:
                if (detail.get("meta").get("source") == resource.ref_id
                        and detail.get("rerank_score") > resource_dict.get("rerank_score")):
                    resource_dict["rerank_score"] = detail.get("rerank_score")
                    resource_dict["ref_text"] = detail.get("text")
            res.append(resource_dict)

        return next_console_response(result=res)
    except Exception as e:
        return next_console_response(error_status=False, error_message=f"搜索资源异常：{e.args}", result=[])


def add_resources_into_session(params):
    user_id = params.get('user_id')
    session_id = params.get('session_id')
    resource_list = params.get('resource_list')

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id,
        NextConsoleSession.user_id == user_id
    ).first()
    if not target_session:
        return next_console_response(error_status=True, error_message="会话不存在！")

    target_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(resource_list),
        ResourceObjectMeta.resource_status == "正常",
    ).all()
    if not target_resources:
        return next_console_response(error_status=True, error_message="资源不存在！")

    for resource in target_resources:
        if resource.user_id != user_id and not check_user_manage_access_to_resource({
            "user": target_user,
            "resource": resource,
            "access_type": "read"
        }):
            continue
            # 共享资源权限检查

        new_attachment = SessionAttachmentRelation(
            session_id=session_id,
            resource_id=resource.id,
            attachment_source="resources",
            rel_status="正常"
        )
        db.session.add(new_attachment)
    db.session.commit()
    return next_console_response(result=[resource.show_info() for resource in target_resources])


def get_all_resource_formats(params):
    """
    获取所有资源格式
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_resource_formats = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
    ).with_entities(
        ResourceObjectMeta.resource_format,
        func.count(ResourceObjectMeta.resource_format).label('count')
    ).group_by(
        ResourceObjectMeta.resource_format
    ).order_by(
        func.count(ResourceObjectMeta.resource_format).desc()
    ).all()
    res = [{"name": i.resource_format, "count": i.count}
           for i in all_resource_formats if i.resource_format]
    return next_console_response(result=res)


def search_resources_by_recent(params):
    """
    搜索最近检索的资源
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    resource_keyword = params.get('resource_keyword')
    page_size = params.get('page_size', 10)
    page_num = params.get('page_num', 1)
    if page_num < 1:
        page_num = 1
    if page_size < 1:
        page_size = 10
    search_type = params.get('search_type', "all")
    resource_type_cn = params.get('resource_type', [])
    resource_format = params.get('resource_format', [])
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_conditions = [
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center",
    ]
    if resource_keyword:
        or_conditions = [ResourceObjectMeta.resource_name.like(f"%{resource_keyword}%"),
                         ResourceObjectMeta.resource_title.like(f"%{resource_keyword}%"),
                         ResourceObjectMeta.resource_source_url.like(f"%{resource_keyword}%"),
                         ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%")]
        all_conditions.append(or_(*or_conditions))
    if resource_type_cn:
        resource_translates = {
            "图片": "image",
            "文档": "document",
            "文件夹": "folder",
            "网页": "webpage",
            "代码": "code",
        }
        resource_type = [resource_translates.get(i) for i in resource_type_cn if resource_translates.get(i)]
        all_conditions.append(ResourceObjectMeta.resource_type.in_(resource_type))
    if resource_format:
        all_conditions.append(ResourceObjectMeta.resource_format.in_(resource_format))
    if search_type == 'file':
        all_conditions.append(ResourceObjectMeta.resource_type != 'folder')
    if search_type == 'folder':
        all_conditions.append(ResourceObjectMeta.resource_type == 'folder')
    if search_type == 'share':
        all_conditions.append(ResourceObjectMeta.user_id != user_id)

    all_recent_resources = NextConsoleSession.query.filter(
        NextConsoleSession.user_id == user_id,
        NextConsoleSession.session_vis == True,
    ).join(
        SessionAttachmentRelation,
        NextConsoleSession.id == SessionAttachmentRelation.session_id
    ).filter(
        SessionAttachmentRelation.rel_status == "正常"
    ).join(
        ResourceObjectMeta,
        SessionAttachmentRelation.resource_id == ResourceObjectMeta.id,
    ).filter(
        *all_conditions
    ).with_entities(
        SessionAttachmentRelation.update_time.label("rag_time"),
        ResourceObjectMeta
    ).all()

    # 手动根据资源id去重并取最新一条
    pre_res = []
    lasted_rag_time = {}
    for rag_time, resource in all_recent_resources:
        if resource.id not in lasted_rag_time:
            lasted_rag_time[resource.id] = rag_time
        else:
            if rag_time > lasted_rag_time[resource.id]:
                lasted_rag_time[resource.id] = rag_time
    for rag_time, resource in all_recent_resources:
        if lasted_rag_time[resource.id] == rag_time:
            pre_res.append({
                "rag_time": rag_time,
                "resource": resource
            })
    # 按照rag_time倒序
    pre_res.sort(key=lambda x: x["rag_time"], reverse=True)

    # 如果是分享权限，检查是否还有权限
    if search_type == 'share':
        pre_res2 = []
        for pre_res_item in pre_res:
            if check_user_manage_access_to_resource({
                "user": target_user,
                "resource": pre_res_item.get("resource"),
                "access_type": "read"
            }):
                pre_res2.append(pre_res_item)
        pre_res = pre_res2
    #分页
    if (page_num - 1) * page_size > len(pre_res):
        return next_console_response(result=[])
    if page_num * page_size > len(pre_res):
        res = pre_res[(page_num - 1) * page_size:]
    else:
        res = pre_res[(page_num - 1) * page_size: page_num * page_size]
    final_res = []
    for i in res:
        resource = i["resource"].show_info()
        resource["rag_time"] = i["rag_time"].strftime('%Y-%m-%d %H:%M:%S')
        final_res.append(resource)
    return next_console_response(result=final_res)


def search_share_resources(params):
    """
    搜索分享资源
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_share_resources = search_share_resource_by_keyword(
        {
            "user_id": user_id,
            "resource_keyword": params.get("resource_keyword"),
            "rag_enhance":  params.get("rag_enhance"),

        }
    )
    if all_share_resources.json.get("error_status"):
        return all_share_resources
    all_share_resources = all_share_resources.json.get("result")
    # search_type 过滤
    search_type = params.get('search_type', "all")
    if search_type == "file":
        all_share_resources["data"] = [i for i in all_share_resources.get("data") if i.get("resource_type") != "folder"]
    elif search_type == "folder":
        all_share_resources["data"] = [i for i in all_share_resources.get("data") if i.get("resource_type") == "folder"]
    elif search_type == "share":
        all_share_resources["data"] = [i for i in all_share_resources.get("data") if i.get("user_id") != user_id]
    # 过滤掉不是success
    all_need_check_resource_ids = []
    for resource in all_share_resources.get("data"):
        if resource.get("resource_type") != "folder":
            all_need_check_resource_ids.append(resource.get("id"))
    all_resource_ref = RagRefInfo.query.filter(
        RagRefInfo.resource_id.in_(all_need_check_resource_ids),
        RagRefInfo.ref_status == "成功"
    ).all()
    all_has_ref_resource = [i.resource_id for i in all_resource_ref]
    new_res = {
        "data": [],
        "total": all_share_resources.get("total"),
        "resource_tags": all_share_resources.get("resource_tags"),
        "author_info": all_share_resources.get("author_info")
    }
    for resource in all_share_resources.get("data"):
        if resource.get("resource_type") == "folder":
            new_res["data"].append(resource)
        else:
            if resource.get("id") in all_has_ref_resource:
                new_res["data"].append(resource)
    return next_console_response(result=new_res)
