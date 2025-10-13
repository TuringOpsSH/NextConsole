import app
from app.services.configure_center.llm import *
from app.models.knowledge_center.rag_ref_model import RagRefInfo
from app.models.assistant_center.assistant import AssistantInstruction
from app.models.app_center.app_info_model import WorkFlowTaskInfo


def get_all_ref_ids(user_id, session_id, qa_id, msg_id, assistant_id, model_name):
    # rag模块 获取用户配置的kg_ref_id,或者用户可见的kg与其中的doc_ref_id，
    all_ref_ids, all_qa_ids = [], []
    all_file_ref_ids = []
    all_webpage_ref_ids = []
    all_resource_ref_ids = []
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.user_id == user_id,
        NextConsoleSession.id == session_id
    ).first()
    if not target_session:
        app.logger.warning(f"未获取到指定的session:{session_id},user_id:{user_id}")
        return [], []
    if target_session.session_attachment_file_switch:
        all_file_ref_ids = get_all_file_ref_ids(session_id)
    if target_session.session_attachment_webpage_switch:
        all_webpage_ref_ids = get_all_webpage_ref_ids(user_id, session_id, qa_id, msg_id, assistant_id, model_name)
    if target_session.session_local_resource_switch:
        # 如果为全部资源，则获取所有的ref_id
        all_resource_ref_ids = get_all_resource_ref_ids(target_session)
    all_qa_ids = list(set(all_qa_ids))
    all_ref_ids = all_file_ref_ids + all_webpage_ref_ids + all_resource_ref_ids
    all_ref_ids = list(set(all_ref_ids))
    return all_ref_ids, all_qa_ids


def get_all_file_ref_ids(session_id):
    # 获取会话附件文档的ref_id
    all_ref_ids = []
    attachment_files = SessionAttachmentRelation.query.filter(
        SessionAttachmentRelation.session_id == session_id,
        SessionAttachmentRelation.attachment_source == 'files',
        SessionAttachmentRelation.rel_status == '正常',
    ).join(
        RagRefInfo,
        RagRefInfo.resource_id == SessionAttachmentRelation.resource_id,
    ).filter(
        RagRefInfo.ref_status == '成功'
    ).with_entities(
        RagRefInfo
    ).all()
    for ref_id in attachment_files:
        all_ref_ids.append(ref_id.id)
    return all_ref_ids


def get_all_webpage_ref_ids(user_id, session_id, qa_id, msg_id, assistant_id, model_name):
    # 获取会话附件文档的ref_id
    attachment_files = SessionAttachmentRelation.query.filter(
        SessionAttachmentRelation.session_id == session_id,
        SessionAttachmentRelation.attachment_source == 'webpage',
        SessionAttachmentRelation.rel_status == '正常',
    ).join(
        RagRefInfo,
        SessionAttachmentRelation.resource_id == RagRefInfo.resource_id,
    ).filter(
        RagRefInfo.ref_status == '成功'
    ).with_entities(
        RagRefInfo
    ).all()
    all_pick_html = []
    all_ref_ids = []
    for ref in attachment_files:
        all_ref_ids.append(ref.id)
        all_pick_html.append(ref.resource_id)
    # 新建与推送工作流任务信息
    target_assistant_instruction = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == -12345,
        AssistantInstruction.instruction_name == "WebPageFetch",
        AssistantInstruction.instruction_status == "正常"
    ).first()
    if target_assistant_instruction:
        # 当前会话的所有网页截图
        all_html_pngs = SessionAttachmentRelation.query.filter(
            SessionAttachmentRelation.session_id == session_id,
            SessionAttachmentRelation.attachment_source == 'webpage',
            SessionAttachmentRelation.rel_status == '正常',
        ).join(
            ResourceObjectMeta,
            SessionAttachmentRelation.resource_id == ResourceObjectMeta.id,
        ).filter(
            ResourceObjectMeta.resource_format == 'png',
            ResourceObjectMeta.resource_show_url.isnot(None)
        ).with_entities(
            ResourceObjectMeta.resource_source_url,
            ResourceObjectMeta.resource_show_url
        ).all()
        task_params = [{
            "resource_source_url": png.resource_source_url,
            "resource_show_url": png.resource_show_url,
        } for png in all_html_pngs]
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
        db.session.commit()
        # 发送工作流日志
        emit_workflow_status.delay({
            "user_id": user_id,
            "new_task": new_workflow_task_info.to_dict()
        })
    return all_ref_ids


def get_all_resource_ref_ids(target_session):
    # 如果为全部资源，则获取所有的ref_id
    all_ref_ids = []
    if target_session.session_local_resource_use_all:
        all_ref_ids = RagRefInfo.query.filter(
            RagRefInfo.ref_status == '成功',
            RagRefInfo.user_id == target_session.user_id
        ).all()
        all_ref_ids = [ref.id for ref in all_ref_ids]
    else:
        # 获取会话附件文档的ref_id
        attachment_files = SessionAttachmentRelation.query.filter(
            SessionAttachmentRelation.session_id == target_session.id,
            SessionAttachmentRelation.attachment_source == 'resources',
            SessionAttachmentRelation.rel_status == '正常',
        ).join(
            RagRefInfo,
            SessionAttachmentRelation.resource_id == RagRefInfo.resource_id,
        ).filter(
            RagRefInfo.ref_status == '成功'
        ).with_entities(
            RagRefInfo
        ).all()
        for ref in attachment_files:
            all_ref_ids.append(ref.id)
        # 处理文件夹下的资源
        all_folders = SessionAttachmentRelation.query.filter(
            SessionAttachmentRelation.session_id == target_session.id,
            SessionAttachmentRelation.attachment_source == 'resources',
            SessionAttachmentRelation.rel_status == '正常',
        ).join(
            ResourceObjectMeta,
            SessionAttachmentRelation.resource_id == ResourceObjectMeta.id,
        ).filter(
            ResourceObjectMeta.resource_type == 'folder'
        ).with_entities(
            ResourceObjectMeta.id
        ).all()
        if all_folders:
            # 如果为文件夹，则获取文件夹下的子资源
            all_user_resources = ResourceObjectMeta.query.filter(
                ResourceObjectMeta.user_id == target_session.user_id,
                ResourceObjectMeta.resource_status == '正常',
            ).all()
            all_sub_resource_ids = [folder.id for folder in all_folders]
            add_cnt = 1
            while add_cnt > 0:
                add_cnt = 0
                for resource_item in all_user_resources:
                    if (resource_item.resource_parent_id in all_sub_resource_ids
                            and resource_item.id not in all_sub_resource_ids):
                        all_sub_resource_ids.append(resource_item.id)
                        add_cnt += 1
            sub_resource_list_id = [resource_item.id for resource_item in all_user_resources
                                    if resource_item.id in all_sub_resource_ids
                                    and resource_item.resource_type != 'folder']
            all_sub_resource_ref_ids = RagRefInfo.query.filter(
                RagRefInfo.resource_id.in_(sub_resource_list_id)
            ).filter(
                RagRefInfo.ref_status == '成功'
            ).with_entities(
                RagRefInfo
            ).all()
            for ref in all_sub_resource_ref_ids:
                all_ref_ids.append(ref.id)
    return all_ref_ids


def search_generate_rag_question(user_id, session_id, qa_id, msg_id, question_content, assistant_id, model_name
                                 , query_k=10, dense_threshold=0.6
                                 , pre_fix="", faq_direct_return='false'):
    """
    检索模式下生成rag问题
        ai搜索- user_config :
            search_engine_switch
            search_engine_language_type
            search_engine_resource_type
        ai搜索 rag参数
            search_engine_enhanced: auto
            llm_router: false
            search_engine_config: {
            "gl": "cn",
            "hl": "zh-cn",
            "type": "search",
            }
    """
    all_ref_ids, all_qa_ids = [], []
    current_session = NextConsoleSession.query.filter_by(user_id=user_id, id=session_id).first()
    # ai搜索配置
    search_engine_enhanced = False
    search_engine_config = {
        "type": "search",
    }
    if current_session.session_search_engine_switch:
        search_engine_enhanced = True
        if current_session.session_search_engine_language_type:
            search_engine_config.update(current_session.session_search_engine_language_type)
        search_engine_config["type"] = current_session.session_search_engine_resource_type
    rag_params = {
        "user_id": user_id,
        "session_id": session_id,
        "msg_id": msg_id,
        "query": question_content,
        "ref_ids": all_ref_ids,
        "config": {
            "search_engine_enhanced": search_engine_enhanced,
            "search_engine_config": search_engine_config,
        }
    }
    if (current_session.session_local_resource_switch or current_session.session_attachment_file_switch
            or current_session.session_attachment_webpage_switch):
        all_ref_ids, all_qa_ids = get_all_ref_ids(user_id, session_id, qa_id, msg_id, assistant_id, model_name)
        rag_params["ref_ids"] = all_ref_ids
    from app.services.knowledge_center.rag_service_v3 import rag_query_v3
    rag_response = rag_query_v3(rag_params).json.get("result", {})
    ref_text = rag_response.get("reference_texts", "")
    if ref_text and isinstance(ref_text, list):
        new_ref_text = ""
        for i in range(len(ref_text)):
            new_ref_text += f"[{pre_fix}{i + 1}] {ref_text[i]}\n"
        return new_ref_text
    return ''




