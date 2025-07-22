from app.models.assistant_center.assistant import *
from app.models.next_console.next_console_model import NextConsoleMessage
from app.models.next_console.next_console_model import NextConsoleRecommendQuestion
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.services.next_console.next_console import next_console_response
from app.models.knowledge_center.rag_ref_model import RagQueryLog, ResourceChunkInfo


def search_reference(params):
    """
    按照问题ID，返回召回的分段信息。提供至前端文献侧边栏
    return : msg_parent_id(回答的ID）:[
        {
            "ref_text": rel.ref_text,
            "recall_score": rel.recall_score,
            "rerank_score": rel.rerank_score,
            "source_type": rel.source_type,
            "resource_id": raw_reference_id,
            "resource_icon": raw_reference.resource_icon,
            "resource_name": raw_reference.resource_name,
            "resource_title": raw_reference.resource_title or raw_reference.resource_name,
            "resource_source_url": raw_reference.resource_source_url or "",
        }
    ]
    从参考文献关系表中获取资源，再找到父资源再返回。
    """
    user_id = int(params.get("user_id"))
    msg_id_list = params.get("msg_id_list", [])
    if not msg_id_list:
        return next_console_response(result={})
    msg_reference_rel_all = {}
    msg_reference_results = NextConsoleMessage.query.filter(
        NextConsoleMessage.msg_id.in_(msg_id_list),
        NextConsoleMessage.user_id == user_id
    ).join(
        RagQueryLog,
        RagQueryLog.msg_id == NextConsoleMessage.msg_id
    ).with_entities(
        NextConsoleMessage.msg_id,
        RagQueryLog.result
    ).all()

    if not msg_reference_results:
        return next_console_response(result=msg_reference_rel_all)
    all_chunk_ids = []
    for msg_id, result in msg_reference_results:
        if result and result.get("final_result", {}).get("chunks", []):
            all_chunk_ids.extend(result.get("final_result", {}).get("chunks", []))
    all_chunks = ResourceChunkInfo.query.filter(
        ResourceChunkInfo.id.in_(all_chunk_ids),
        ResourceChunkInfo.status == '正常'
    ).join(
        ResourceObjectMeta,
        ResourceObjectMeta.id == ResourceChunkInfo.resource_id
    ).with_entities(
        ResourceChunkInfo.id,
        ResourceChunkInfo.chunk_raw_content,
        ResourceChunkInfo.resource_id
    ).all()
    chunk_info_map = {chunk.id: chunk for chunk in all_chunks}
    md_resource_ids = {chunk.resource_id for chunk in all_chunks if chunk.resource_id}
    md_raw_resources_ids = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(md_resource_ids),
        ResourceObjectMeta.resource_status == '正常'
    ).with_entities(
        ResourceObjectMeta.id,
        ResourceObjectMeta.resource_parent_id
    ).all()
    md_raw_resources_maps = {res.id: res.resource_parent_id for res in md_raw_resources_ids if res.resource_parent_id}
    raw_reference_ids = {res.resource_parent_id for res in md_raw_resources_ids if res.resource_parent_id}
    raw_reference = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(raw_reference_ids),
        ResourceObjectMeta.resource_status == '正常'
    ).with_entities(
        ResourceObjectMeta.id,
        ResourceObjectMeta.resource_type,
        ResourceObjectMeta.resource_icon,
        ResourceObjectMeta.resource_name,
        ResourceObjectMeta.resource_title,
        ResourceObjectMeta.resource_source_url,
        ResourceObjectMeta.resource_download_url
    ).all()
    raw_reference_map = {res.id: res for res in raw_reference}
    for msg_id, result in msg_reference_results:
        if msg_id not in msg_reference_rel_all:
            msg_reference_rel_all[msg_id] = []
        for chunk in result.get("final_result",{}).get("chunks", []):
            recall_score = 0
            for recall_item in result["recall_result"]:
                if recall_item[0] == chunk:
                    recall_score = recall_item[1]
                    break
            rerank_score = 0
            for rerank_item in result["rerank_result"]:
                if rerank_item[0] == chunk:
                    rerank_score = rerank_item[1]
                    break
            chunk_info = chunk_info_map.get(chunk)
            if not chunk_info:
                continue
            raw_resources = raw_reference_map.get(md_raw_resources_maps.get(chunk_info.resource_id))
            msg_reference_rel_all[msg_id].append({
                "ref_text": chunk_info.chunk_raw_content,
                "recall_score": recall_score,
                "rerank_score": rerank_score,
                "source_type": raw_resources.resource_type,
                "resource_id": raw_resources.id,
                "resource_icon": raw_resources.resource_icon,
                "resource_name": raw_resources.resource_name,
                "resource_title": raw_resources.resource_title or raw_resources.resource_name,
                "resource_source_url": raw_resources.resource_source_url or "",
                "resource_download_url": raw_resources.resource_download_url
            })
    return next_console_response(result=msg_reference_rel_all)


