import time

from app.app import celery, db, app
from app.models.knowledge_center.rag_ref_model import RagRefInfo, ResourceChunkInfo
from app.services.configure_center.response_utils import next_console_response
from app.models.resource_center.resource_model import ResourceObjectMeta
import os
from app.utils.oss.oss_client import generate_download_url, generate_new_path
import numpy as np
from app.models.next_console.next_console_model import SessionAttachmentRelation
from app.services.knowledge_center.file_chunk_embedding import embedding_call, rerank_call
from app.services.knowledge_center.webpage_fetch import get_url_format
from app.models.knowledge_center.rag_ref_model import RagQueryLog


def stop_ref_task(params):
    """
    停止RAG-索引构建任务
        支持多任务并发执行
        支持停止任务
    """
    resource_id = params.get('resource_id')
    ref_id = params.get('ref_id')
    target_reg_ref = RagRefInfo.query.filter(
        RagRefInfo.ref_id == ref_id,
        RagRefInfo.resource_id == resource_id,
    ).order_by(RagRefInfo.create_time.desc()).first()
    if not target_reg_ref:
        return next_console_response(error_status=True, error_message="未找到对应的RAG索引记录")
    if target_reg_ref.ref_status in ("失败", "异常", "已停止", "成功"):
        return next_console_response(error_status=True, error_message="当前RAG索引状态不允许停止")
    celery.control.revoke(
        target_reg_ref.celery_task_id, terminate=True, signal='SIGKILL', force=True, wait=True, timeout=2
    )
    target_reg_ref.ref_status = "已停止"
    db.session.add(target_reg_ref)
    db.session.commit()
    return next_console_response(result={"ref_id": ref_id, "resource_id": resource_id})


def file_reader(params):
    """
    解析文档成指定的文本类格式
        加载配置
        根据配置加载对应的解析器
        组装对应的解析参数
        执行解析任务
        将结果对应生成子资源
        返回解析结果的元信息
    """
    resource_id = params.get('resource_id')
    ref_id = params.get('ref_id')
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == '正常'
    ).first()
    target_rag_ref = RagRefInfo.query.filter(RagRefInfo.id == ref_id).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="未找到对应的资源")
    if not target_rag_ref:
        return next_console_response(error_status=True, error_message="未找到对应的RAG索引记录")
    config = target_rag_ref.file_reader_config
    target_rag_ref.ref_status = "解析中"
    db.session.add(target_rag_ref)
    db.session.commit()
    if config["engine"] == "pandoc":
        from app.services.knowledge_center.file_reader import pandoc_reader
        new_resource_meta = pandoc_reader(target_resource, config.get("pandoc_config"))
    elif config["engine"] == "pymupdf":
        from app.services.knowledge_center.file_reader import pymupdf_reader
        new_resource_meta = pymupdf_reader(target_resource, config.get("pymupdf_config", {}))
    elif config["engine"] == "html2text":
        from app.services.knowledge_center.file_reader import html2text_reader
        new_resource_meta = html2text_reader(target_resource, config.get("html2text_config", {}))
    elif config["engine"] == "openpyxl":
        from app.services.knowledge_center.file_reader import openpyxl_reader
        new_resource_meta = openpyxl_reader(target_resource, config.get("openpyxl_config", {}))
    elif config["engine"] == "python-pptx":
        from app.services.knowledge_center.file_reader import pptx_reader
        new_resource_meta = pptx_reader(target_resource, config.get("python_pptx_config", {}))
    elif config["engine"] == "text":
        from app.services.knowledge_center.file_reader import text_reader
        new_resource_meta = text_reader(target_resource, config.get("text_config", {}))
    else:
        target_rag_ref.ref_status = "异常"
        target_rag_ref.task_trace_log = "不支持的解析引擎"
        db.session.add(target_rag_ref)
        db.session.commit()
        return next_console_response(error_status=True, error_message="不支持的解析引擎")
    if isinstance(new_resource_meta, str):
        # 如果是字符串，说明发生了错误
        target_rag_ref.ref_status = "失败"
        target_rag_ref.task_trace_log = new_resource_meta
        db.session.add(target_rag_ref)
        db.session.commit()
        return next_console_response(error_status=True, error_message=new_resource_meta)
    target_rag_ref.ref_status = "解析完成"
    db.session.add(target_rag_ref)
    db.session.commit()
    return new_resource_meta


def file_split(params):
    """
    将文档内容进行分块处理
        核心是根据配置的分块方法进行文档内容的分块
        支持多种分块方法，如长度分块、符号分块、布局分块等
        每种分块方法都有对应的配置参数
        分块完成后，将分块内容和元信息存储到数据库中
        返回分块后的内容和元信息
    """
    resource_id = params.get('resource_id')
    ref_id = params.get('ref_id')
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == '正常'
    ).first()
    target_rag_ref = RagRefInfo.query.filter(RagRefInfo.id == ref_id).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="未找到对应的资源")
    if not target_rag_ref:
        return next_console_response(error_status=True, error_message="未找到对应的RAG索引记录")
    try:
        with open(target_resource.resource_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return next_console_response(error_status=True, error_message="资源文件不存在或无法读取")
    if not content:
        return next_console_response(error_status=True, error_message="资源文件内容为空")
    config = target_rag_ref.file_split_config
    config['content'] = content
    target_rag_ref.ref_status = "切分中"
    db.session.add(target_rag_ref)
    db.session.commit()
    if config['method'] == 'length':
        from app.services.knowledge_center.file_split import length_split
        split_result = length_split(config)
    elif config['method'] == 'symbol':
        from app.services.knowledge_center.file_split import symbol_split
        split_result = symbol_split(config)
    elif config['method'] == 'layout':
        from app.services.knowledge_center.file_split import layout_split
        split_result = layout_split(config)
    else:
        target_rag_ref.ref_status = "异常"
        target_rag_ref.task_trace_log = "不支持的切分方法"
        db.session.add(target_rag_ref)
        db.session.commit()
        return next_console_response(error_status=True, error_message="不支持的切分方法")
    if isinstance(split_result, str):
        # 如果是字符串，说明发生了错误
        target_rag_ref.ref_status = "失败"
        target_rag_ref.task_trace_log = split_result
        db.session.add(target_rag_ref)
        db.session.commit()
        return next_console_response(error_status=True, error_message=split_result)
    target_rag_ref.ref_chunk_cnt = len(split_result)
    target_rag_ref.ref_chunk_ready_cnt = 0
    db.session.add(target_rag_ref)
    db.session.commit()
    for chunk in split_result:
        chunk_raw_content = chunk.get('content', '')
        chunk_type = chunk.get('type', 'text')
        chunk_size = len(chunk_raw_content.encode('utf-8')) / 1024  # 转换为KB
        new_chunk_info = ResourceChunkInfo(
            resource_id=target_resource.id,
            split_method=config['method'],
            chunk_type=chunk_type,
            chunk_format=target_resource.resource_format,
            chunk_size=chunk_size,
            chunk_raw_content=chunk_raw_content,
            ref_id=target_rag_ref.id,
        )
        db.session.add(new_chunk_info)
    target_rag_ref.ref_status = "切分完成"
    db.session.add(target_rag_ref)
    db.session.commit()
    return {
        "ref_id": ref_id,
        "resource_id": resource_id,
        "chunk_count": target_rag_ref.ref_chunk_cnt,
        "chunk_ready_count": target_rag_ref.ref_chunk_ready_cnt,
        "status": "success"
    }


def file_chunk_abstract(params):
    """
    将文档内容进行摘要处理,构建嵌入向量的输入
        通过线程池并发处理多个文档分块
        每个分块内容进行摘要处理
        根据不同配置进行摘要处理
            元信息拼接
            todo：关键词提取
            todo：问题提炼
            todo：表格元素仅保留表头
            todo：图片元素仅保留图片描述

    """
    resource_id = params.get('resource_id')
    ref_id = params.get('ref_id')
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == '正常'
    ).first()
    target_rag_ref = RagRefInfo.query.filter(RagRefInfo.id == ref_id).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="未找到对应的资源")
    if not target_rag_ref:
        return next_console_response(error_status=True, error_message="未找到对应的RAG索引记录")
    target_rag_ref.ref_status = "摘要中"
    db.session.add(target_rag_ref)
    db.session.commit()
    config = target_rag_ref.file_chunk_abstract_config or {

    }
    chunk_infos = ResourceChunkInfo.query.filter(
        ResourceChunkInfo.resource_id == target_resource.id,
        ResourceChunkInfo.ref_id == target_rag_ref.id,
    ).all()
    if not chunk_infos:
        return next_console_response(error_status=True, error_message="未找到对应的分块信息")
    resource_name = target_resource.resource_name
    for chunk in chunk_infos:
        chunk_raw_content = chunk.chunk_raw_content.replace(' ', '')
        chunk_embedding_content = f"{resource_name}: {chunk_raw_content}"
        chunk.chunk_embedding_content = chunk_embedding_content
        db.session.add(chunk)
    target_rag_ref.ref_status = "摘要完成"
    db.session.add(target_rag_ref)
    db.session.commit()
    return {
        "ref_id": ref_id,
        "resource_id": resource_id,
        "chunk_count": len(chunk_infos),
        "status": "success"
    }


def file_chunk_embedding(params):
    """
    将文档摘要内容进行向量化处理，存储到向量数据库中
    """
    resource_id = params.get('resource_id')
    ref_id = params.get('ref_id')
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == '正常'
    ).first()
    target_rag_ref = RagRefInfo.query.filter(RagRefInfo.id == ref_id).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="未找到对应的资源")
    if not target_rag_ref:
        return next_console_response(error_status=True, error_message="未找到对应的RAG索引记录")
    target_rag_ref.ref_status = "向量化中"
    db.session.add(target_rag_ref)
    db.session.commit()
    config = target_rag_ref.file_chunk_embedding_config
    chunk_infos = ResourceChunkInfo.query.filter(
        ResourceChunkInfo.resource_id == target_resource.id,
        ResourceChunkInfo.ref_id == target_rag_ref.id,
    ).all()
    if not chunk_infos:
        return next_console_response(error_status=True, error_message="未找到对应的分块信息")
    from app.services.knowledge_center.file_chunk_embedding import chunk_embedding
    embedding_results = chunk_embedding({
        "contents": [chunk.chunk_embedding_content for chunk in chunk_infos],
        "config": config
    })
    if not embedding_results:
        target_rag_ref.ref_status = "失败"
        target_rag_ref.task_trace_log = "向量化处理失败"
        db.session.add(target_rag_ref)
        db.session.commit()
        return next_console_response(error_status=True, error_message="向量化处理失败")
    chunk_embeddings, total_tokens = embedding_results
    # 保存向量
    for chunk, embedding in zip(chunk_infos, chunk_embeddings):
        chunk.chunk_embedding = embedding
        chunk.chunk_embedding_type = target_rag_ref.file_chunk_embedding_config.get("model")
        db.session.add(chunk)
    db.session.commit()
    target_rag_ref.ref_status = "向量化完成"
    target_rag_ref.ref_chunk_ready_cnt = len(chunk_embeddings)
    target_rag_ref.ref_embedding_token_used = total_tokens
    db.session.add(target_rag_ref)
    db.session.commit()
    return {
        "ref_id": ref_id,
        "resource_id": resource_id,
        "chunk_count": len(chunk_embeddings),
        "chunk_ready_count": target_rag_ref.ref_chunk_ready_cnt,
        "status": "success"
    }


def rag_query_v3(params):
    """
    执行RAG查询任务
        支持多任务并发执行
        支持查询结果返回
        支持查询结果流式返回
        result: {
        }
    """
    user_id = int(params.get("user_id", 0))
    session_id = params.get("session_id")
    msg_id = params.get("msg_id")
    task_id = params.get("task_id")
    query = str(params.get("query", ""))
    if not query:
        return next_console_response(error_status=True, error_message="查询内容不能为空")
    if len(query) > 1000:
        return next_console_response(error_status=True, error_message="查询内容过长，请控制在1000字符以内")
    ref_ids = params.get("ref_ids", [])
    config = params.get("config", )
    inner_config = {
        "recall_threshold": 0.3,
        "recall_k": 30,
        "recall_similarity": "ip",
        "rerank_enabled": True,
        "max_chunk_per_doc": 1024,
        "overlap_tokens": 80,
        "rerank_threshold": 0.6,
        "rerank_k": 10,
        "search_engine_enhanced": True,
        "search_engine_config": {
            "api": app.config.get("search_engine_endpoint", ""),
            "key": app.config.get("search_engine_key", ""),
            "gl": "cn",
            "hl": "zh-cn",
            "location": "China",
            "num": 20,
            "timeout": 30,
        },
        "show_details": True
    }
    if config:
        inner_config = deep_merge(inner_config, config)
    rerank_enabled = inner_config.get("rerank_enabled", True)
    web_search_result = {
        "ref_ids": [],
        "webpage_resource_ids": []
    }
    result = {
        "details": [],
        'reference_texts': []
    }

    if not ref_ids and not inner_config.get("search_engine_enhanced", False):
        return next_console_response(error_status=False, error_message="查询参考信息不能为空", result=result)
    query_log = {
        "user_id": user_id,
        "session_id": session_id,
        "msg_id": msg_id,
        "task_id": task_id,
        "query_text": query,
        "ref_ids": [],
        "config": inner_config,
        "status": "运行中",
        "trace_log": "",
        "result": {},
        "time_usage": {}
    }

    # 搜索引擎增强查询
    if inner_config.get("search_engine_enhanced", False):
        web_search_time = time.time()
        web_search_result = get_web_search_result({
            "user_id": user_id,
            "query": query,
            "config": inner_config.get("search_engine_config", {})
        })
        ref_ids.extend(web_search_result.get("ref_ids", []))
        query_log["time_usage"]["web_search_time"] = time.time() - web_search_time
    # Rag-嵌入查询向量
    query_begin_time = time.time()
    query_embedding_result = embedding_call({
        "content": query,
        "config": {
            "api": app.config.get("EMBEDDING_ENDPOINT", ""),
            'key': app.config.get("EMBEDDING_KEY", ""),
            "model": app.config.get("EMBEDDING_MODEL", ""),
            "encoding_format": "float",
        }
    })
    if not query_embedding_result:
        return next_console_response(error_status=True, error_message="查询嵌入异常", result=result)
    query_embedding = query_embedding_result[1]
    query_log["time_usage"]["query_embedding_time"] = time.time() - query_begin_time
    if not query_embedding:
        query_log["status"] = "异常"
        query_log["trace_log"] = "查询向量化处理失败"
        query_log["result"] = {"error": "查询向量化处理失败"}
        save_rag_logs(query_log)
        return next_console_response(error_status=True, error_message="查询向量化处理失败")
    query_embedding = query_embedding[0]
    # Rag-获取参考向量
    embedding_begin_time = time.time()
    all_ref_chunks = recall_ref_chunks(ref_ids, query_embedding, inner_config)
    query_log["time_usage"]["embedding_time"] = time.time() - embedding_begin_time

    if rerank_enabled and all_ref_chunks:
        all_recall_chunks = rerank_ref_chunks(query, all_ref_chunks, inner_config, query_log)
        if isinstance(all_recall_chunks, list):
            all_ref_chunks = all_recall_chunks
    # 组装返回结果
    for resource_chunk in all_ref_chunks:
        result['details'].append({
            "meta": {
                "source": resource_chunk.get("resource_id", ""),
                "source_type": "resource"
            },
            "chunk_id": resource_chunk.get("id", ""),
            "text": resource_chunk.get("chunk_raw_content", ""),
            "recall_score": resource_chunk.get("recall_score", 0.0),
            "rerank_score":  resource_chunk.get("rerank_score", 0.0),
        })
        result['reference_texts'].append(resource_chunk.get("chunk_raw_content", ""))
    # 更新命中情况
    all_result_chunk_ids = [chunk.get("id") for chunk in all_ref_chunks]
    db.session.query(ResourceChunkInfo).filter(
        ResourceChunkInfo.id.in_(all_result_chunk_ids),
        ResourceChunkInfo.chunk_embedding.isnot(None)
    ).update(
        {"chunk_hit_counts": ResourceChunkInfo.chunk_hit_counts + 1},
        synchronize_session=False
    )
    db.session.commit()
    # 补充搜索引擎增强查询结果(chunk)
    if web_search_result.get("new_webpage_ids"):
        new_webpage_ids = web_search_result.get("new_webpage_ids", [])
        new_webpage_chunks = ResourceChunkInfo.query.filter(
            ResourceChunkInfo.resource_id.in_(new_webpage_ids)
        ).all()
        for new_webpage_chunk in new_webpage_chunks:
            result['reference_texts'].append(new_webpage_chunk.chunk_raw_content)
            if inner_config.get("show_details", True):
                result['details'].append({
                    "meta": {
                        "source": new_webpage_chunk.resource_id,
                        "source_type": "webpage"
                    },
                    "chunk_id": new_webpage_chunk.id,
                    "reference_texts": new_webpage_chunk.chunk_raw_content,
                    "recall_score": 1,  # 搜索引擎增强查询没有 recall_score
                    "rerank_score": 1,
                })
    # 更新日志
    query_log["ref_ids"] = ref_ids
    query_log["status"] = "运行完成"
    query_log["result"]["web_search_result"] = web_search_result

    query_log["result"]["recall_result"] = [
        [chunk.get("id"), chunk.get("recall_score")] for chunk in all_ref_chunks
    ]
    query_log["result"]["rerank_result"] = [
        [chunk.get("id"), chunk.get("rerank_score")] for chunk in all_ref_chunks
    ]
    query_log["result"]["final_result"] = {}
    query_log["result"]["final_result"]["chunks"] = [
        chunk["chunk_id"]
        for chunk in result["details"]
        if chunk["chunk_id"]
    ]
    save_rag_logs(query_log)
    return next_console_response(result=result)


def recall_ref_chunks(ref_ids, query_embedding, inner_config):
    """
    获取所有参考信息的嵌入向量
        支持多参考信息
        返回嵌入向量列表和chunk_id，用于后续的查询和计算
    :param ref_ids: 参考信息ID列表
    :param query_embedding: 查询的嵌入向量
    :param inner_config: 内部配置参数
    :return: 返回满足条件的所有资源分段的字典形态
    """
    metric = inner_config.get("recall_similarity", "ip")
    recall_threshold = inner_config.get("recall_threshold", 0.3)
    recall_k = inner_config.get("recall_k", 30)
    all_ref_chunks = []
    if not ref_ids:
        return all_ref_chunks
    if metric == "cosine":
        all_ref_chunks = RagRefInfo.query.filter(
            RagRefInfo.id.in_(ref_ids),
            RagRefInfo.ref_status == "成功",
        ).join(
            ResourceChunkInfo,
            RagRefInfo.id == ResourceChunkInfo.ref_id
        ).filter(
            ResourceChunkInfo.status == "正常",
            (1 - ResourceChunkInfo.chunk_embedding.cosine_distance(query_embedding)) >= recall_threshold
        ).order_by(
            ResourceChunkInfo.chunk_embedding.cosine_distance(query_embedding).desc()
        ).with_entities(
            ResourceChunkInfo.id,
            ResourceChunkInfo.resource_id,
            ResourceChunkInfo.chunk_raw_content,
            ResourceChunkInfo.chunk_embedding_content,
            ResourceChunkInfo.chunk_embedding.cosine_distance(query_embedding).label("recall_score"),
        ).limit(recall_k).all()
    elif metric == "ip":
        all_ref_chunks = RagRefInfo.query.filter(
            RagRefInfo.id.in_(ref_ids),
            RagRefInfo.ref_status == "成功",
        ).join(
            ResourceChunkInfo,
            RagRefInfo.id == ResourceChunkInfo.ref_id
        ).filter(
            ResourceChunkInfo.chunk_embedding.max_inner_product(query_embedding) * -1 >= recall_threshold
        ).order_by(
            (ResourceChunkInfo.chunk_embedding.max_inner_product(query_embedding) * -1).desc()
        ).with_entities(
            ResourceChunkInfo.id,
            ResourceChunkInfo.resource_id,
            ResourceChunkInfo.chunk_raw_content,
            ResourceChunkInfo.chunk_embedding_content,
            (ResourceChunkInfo.chunk_embedding.max_inner_product(query_embedding) * -1).label("recall_score"),
        ).limit(recall_k).all()
    if not all_ref_chunks:
        return []
    all_ref_chunks = [{
        "id": chunk.id,
        "resource_id": chunk.resource_id,
        "chunk_raw_content": chunk.chunk_raw_content,
        "chunk_embedding_content": chunk.chunk_embedding_content,
        "recall_score": chunk.recall_score if chunk.recall_score is not None else 0.0,
        "rerank_score": 0,
    } for chunk in all_ref_chunks]
    return all_ref_chunks


def rerank_ref_chunks(query, all_ref_chunks, inner_config, query_log):
    """
    执行RAG查询的重排序任务
    :param query: 查询内容
    :param all_ref_chunks: 所有参考信息的分段列表
    :param inner_config: 内部配置参数
    :param query_log: 查询日志对象
    :return: 返回重排序后的参考信息分段列表
    """
    rerank_k = inner_config.get("rerank_k", 10)
    rerank_threshold = inner_config.get("rerank_threshold", 0.5)
    max_chunk_per_doc = inner_config.get("max_chunk_per_doc", 1024)
    overlap_tokens = inner_config.get("overlap_tokens", 80)
    documents = [resource_chunk.get("chunk_embedding_content") for resource_chunk in all_ref_chunks]
    rerank_result = []
    rerank_begin_time = time.time()
    rerank_scores = rerank_call({
        "documents": documents,
        "query": query,
        "config": {
            "api": app.config.get("RERANK_ENDPOINT", ""),
            "key": app.config.get("RERANK_KEY", ""),
            "model": app.config.get("RERANK_MODEL", ""),
            "max_chunks_per_doc": max_chunk_per_doc,
            "overlap_tokens": overlap_tokens,
        }
    })
    query_log["time_usage"]["rerank_time"] = time.time() - rerank_begin_time
    if not rerank_scores:
        query_log["status"] = "异常"
        query_log["trace_log"] = "Rerank处理失败"
        save_rag_logs(query_log)
        return next_console_response(error_status=True, error_message="Rerank处理失败")
    # 按照阈值过滤
    index = 0
    for resource_chunk in all_ref_chunks:
        if rerank_scores[index] >= rerank_threshold:
            resource_chunk["rerank_score"] = rerank_scores[index]
            rerank_result.append(resource_chunk)
        index += 1
    # 按照分数排序并限制数量
    rerank_result = sorted(rerank_result, key=lambda x: x.get("rerank_score"), reverse=True)[:rerank_k]
    return rerank_result


def get_web_search_result(params):
    """
    获取搜索引擎增强查询的参考信息ID
        1、调用搜索引擎获取结果
        2、查询缓存，是否有缓存结果
        3、爬取未有缓存的结果
        4、进行构建未缓存结果
        5、返回
        {
            "ref_ids": [1, 2, 3, ...],
            "new_webpage_ids":[]
        }
    """
    user_id = int(params.get("user_id", 0))
    session_id = int(params.get("session_id", 0))
    query = params.get("query", "")
    config = params.get("config", {})
    api = config.get("api", "")
    key = config.get("key", "")
    timeout = config.get("timeout", 30)
    result = {
        "ref_ids": [],
        "new_webpage_ids": [],
    }
    if not api or not key or not query:
        return result
    if api == "https://google.serper.dev/search":
        from app.services.knowledge_center.search_engine_utils import search_engine_serper
        pages, credits = search_engine_serper(
            {
                "query": query,
                "key": key,
                "config": config
            }
        )
        if not pages:
            return result
        all_links = [page.get("link", "") for page in pages if page.get("link")]
        # 全平台复用的网页资源
        all_exist_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.resource_source_url.in_(all_links),
            ResourceObjectMeta.resource_status == '正常'
        ).join(
            RagRefInfo,
            RagRefInfo.resource_id == ResourceObjectMeta.id
        ).filter(
            RagRefInfo.ref_status == "成功"
        ).with_entities(
            ResourceObjectMeta,
            RagRefInfo
        ).all()
        exist_links = []
        for resource, rag_ref in all_exist_resources:
            result["ref_ids"].append(rag_ref.id)
            exist_links.append(resource.resource_source_url)
        # 未缓存的资源实时爬取并构建
        new_webpage_ids = []
        for page in pages:
            link = page.get("link", "")
            if link in exist_links:
                continue
            page_format = get_url_format(link)
            new_resource_path = generate_new_path(
                "knowledge_center", user_id, suffix=page_format
            ).json.get("result", "")
            new_webpage = ResourceObjectMeta(
                user_id=user_id,
                resource_name=page.get("title", "未命名网页"),
                resource_type="webpage",
                resource_title=page.get("title", ""),
                resource_desc=page.get("snippet", ""),
                resource_icon=f"{page_format}.svg",
                resource_format=page_format,
                resource_path=new_resource_path,
                resource_source="knowledge_center",
                resource_source_url=page.get("link", ""),
                resource_status="正常",
            )
            db.session.add(new_webpage)
            db.session.flush()
            new_webpage_ids.append(new_webpage.id)
        db.session.commit()
        if session_id:
            for new_webpage_id in new_webpage_ids:
                new_attachment = SessionAttachmentRelation(
                    session_id=session_id,
                    resource_id=new_webpage_id,
                    attachment_source="webpage",
                    rel_status="正常"
                )
                db.session.add(new_attachment)
                db.session.add(new_attachment)
            db.session.commit()
        from app.services.task_center.resources_center import attachment_multiple_webpage_tasks
        webpage_tasks_result = attachment_multiple_webpage_tasks.delay({
            "session_id": session_id,
            "resource_list": new_webpage_ids,
            "user_id": user_id,
            "driver": "requests",
        })
        t1 = time.time()
        try:
            webpage_tasks_result.get(timeout=timeout)
        except Exception as e:
            print("webpage_tasks_result：", e)
        result["new_webpage_ids"].extend(new_webpage_ids)
        new_webpage_rag_refs = RagRefInfo.query.filter(
            RagRefInfo.resource_id.in_(new_webpage_ids),
            RagRefInfo.ref_status == "成功"
        ).all()
        result["ref_ids"].extend([rag_ref.id for rag_ref in new_webpage_rag_refs])
    return result


def deep_merge(original: dict, new: dict) -> dict:
    """深度合并，避免直接修改original"""
    result = original.copy()
    for key, value in new.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                # 如果两个值都是字典，递归合并
                result[key] = deep_merge(result[key], value)
            elif isinstance(result[key], list) and isinstance(value, list):
                # 如果两个值都是列表，合并列表
                result[key].extend(value)
            else:
                # 否则直接覆盖
                result[key] = value
        else:
            result[key] = value
    return result


def save_rag_logs(params):
    """
    保存每次检索的rag的日志,供后续分析使用
    """
    user_id = params.get("user_id")
    session_id = params.get("session_id")
    msg_id = params.get("msg_id")
    task_id = params.get("task_id")
    query_text = params.get("query_text", "")
    ref_ids = params.get("ref_ids", [])
    status = params.get("status", "success")
    trace_log = params.get("trace_log", "")
    config = params.get("config", {})
    result = params.get("result", {})
    time_usage = params.get("time_usage", {})
    try:
        new_rag_log = RagQueryLog(
            user_id=user_id,
            session_id=session_id,
            msg_id=msg_id,
            task_id=task_id,
            query_text=query_text,
            ref_ids=ref_ids,
            status=status,
            trace_log=trace_log,
            config=config,
            result=result,
            time_usage=time_usage
        )
        db.session.add(new_rag_log)
        db.session.commit()
    except Exception as e:
        print(e)
    return True


def fetch_query_log(params):
    """
    获取结构化查询日志
    """