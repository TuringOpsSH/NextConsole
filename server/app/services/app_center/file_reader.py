import json
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.app import db

from app.app import app

from app.services.knowledge_center.file_reader import pymupdf_reader,  pandoc_reader, text_reader
from app.services.knowledge_center.file_reader import openpyxl_reader, pptx_reader, html2text_reader
from app.services.knowledge_center.file_split import length_split, symbol_split, layout_split


def file_reader_node_execute(task_params, task_record, global_params):
    """
    根据任务参数和任务记录执行文档读取节点。并将其进行内容提取至指定格式
        src-format:
        transform-engine:
        tgt-format:
            文本：markdown，html，text
            图片：jpg，png，webp
    :param task_params:
    :param task_record:
    :param global_params:
    :return:
    """
    mode = task_record.workflow_node_file_reader_config.get("mode", "list")
    if mode == 'list':
        input_resources = task_params.get("input_resources", [])
    else:
        input_resources = [task_params.get("input_resource", {})]
    input_resources_ids = [resource.get("id") for resource in input_resources]
    config = task_record.workflow_node_file_reader_config
    src_format = task_record.workflow_node_file_reader_config.get("src_format", "pdf")
    transform_engine = task_record.workflow_node_file_reader_config.get("engine", "PyMuPDF")
    tgt_format = task_record.workflow_node_file_reader_config.get("tgt_format", "jpg")
    output_resources = []
    input_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(input_resources_ids)
    ).all()
    app.logger.info("开始执行文件读取节点，输入资源：{}, 源格式：{}, 转换引擎：{}, 目标格式：{}".format(
        input_resources,
        src_format,
        transform_engine,
        tgt_format,
        config,
        task_params
    ))
    for resource in input_resources:
        if src_format == "pdf" and resource.resource_format == "pdf":
            if transform_engine == "PyMuPDF":
                for k in config:
                    task_params[k] = config[k]
                output_resources.append(pymupdf_reader(resource, task_params))
        elif src_format in ("docx", "doc") and resource.resource_format in ("docx", "doc"):
            if transform_engine == "python-docx":
                pass
            elif transform_engine == "pandoc":
                output_resources.append(pandoc_reader(resource, config))
        elif src_format in ("pptx", "ppt") and resource.resource_format in ("pptx", "ppt"):
            if transform_engine == "python-pptx":
                output_resources.append(pptx_reader(resource, config))
        elif src_format in ('xlsx', 'xls') and resource.resource_format in ('xlsx', 'xls'):
            if transform_engine == "openpyxl":
                output_resources.append(openpyxl_reader(resource, config))
        elif src_format in ('html', 'htm') and resource.resource_format in ('html', 'htm'):
            if transform_engine == "html2text":
                output_resources.append(html2text_reader(resource, config))
        elif src_format == "未知":
            output_resources.append(text_reader(resource, config))
    if mode == 'list':
        node_results = {"output_resources": [resource for resource in output_resources]}
    elif src_format == 'pdf' and transform_engine == 'PyMuPDF' and tgt_format in ('jpg', 'png', 'webp'):
        node_results = {"output_resources": [resource for resource in output_resources[0]]}
    else:
        node_results = {"output_resource": output_resources[0] if output_resources else {}}
    task_record.task_result = json.dumps(node_results)
    db.session.add(task_record)
    db.session.commit()
    return task_record


def file_splitter_node_execute(task_params, task_record, global_params):
    """
    根据任务参数和任务记录执行文件分块节点。
        支持长度分块和分隔符，布局分块三种方式
    :param task_params:
    :param task_record:
    :param global_params:
    :return:
    """
    config = task_record.workflow_node_file_splitter_config
    content = task_params.get("content", [])
    config["content"] = content
    method = config.get("method", "length")
    if method == "length":
        results = length_split(config)
    elif method == "symbol":
        results = symbol_split(config)
    elif method == "layout":
        results = layout_split(config)
    else:
        raise ValueError('不支持的分块方法：{}'.format(method))
    node_results = {
        "content_chunks": []
    }
    idx = 1
    for chunk in results:
        node_results["content_chunks"].append({
            "id": idx,
            "chunk_content": chunk.get("content")
        })
        idx += 1
    task_record.task_result = json.dumps(node_results)
    db.session.add(task_record)
    db.session.commit()
    return task_record

