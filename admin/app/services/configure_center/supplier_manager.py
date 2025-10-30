from app.app import app, db
from app.services.configure_center.response_utils import next_console_response
from app.models.configure_center.llm_kernel import LLMSupplierInfo
from sqlalchemy import or_
from urllib.parse import urlparse
import socket
import time
import requests
import json


def llm_supplier_search_service(data):
    """
    基模型厂商搜索服务
    :param data:
    :return:
    """
    page_size = data.get("page_size", 10)
    page_num = data.get("page_num", 1)
    keyword = data.get("keyword", "")
    types = data.get("types", [])
    fetch_all = data.get("fetch_all", False)
    filter_conditions = [
        LLMSupplierInfo.supplier_status == '正常'
    ]
    if keyword:
        or_conditions = or_(
            LLMSupplierInfo.supplier_name.ilike(f"%{keyword}%"),
            LLMSupplierInfo.supplier_desc.ilike(f"%{keyword}%"),
            LLMSupplierInfo.supplier_website.ilike(f"%{keyword}%"),
        )
        filter_conditions.append(or_conditions)
    if types:
        filter_conditions.append(LLMSupplierInfo.supplier_type.in_(types))
    target_suppliers = LLMSupplierInfo.query.filter(
        *filter_conditions
    ).order_by(
        LLMSupplierInfo.id.asc()
    )
    total = target_suppliers.count()
    if fetch_all:
        suppliers = target_suppliers.all()
    else:
        suppliers = target_suppliers.offset((page_num - 1) * page_size).limit(page_size).all()
    supplier_list = [supplier.show_info() for supplier in suppliers]
    return next_console_response(result={
        "total": total,
        "data": supplier_list
    })


def llm_supplier_detail_service(data):
    """
    基模型厂商详情服务
    :param data:
    :return:
    """
    supplier_id = data.get("supplier_id")
    target_supplier = LLMSupplierInfo.query.filter_by(
        id=supplier_id,
        supplier_status='正常'
    ).first()
    if not target_supplier:
        return next_console_response(error_status=True, error_message="基模型厂商不存在！", error_code=1004)
    return next_console_response(result=target_supplier.to_dict())


def model_health_check_service(data):
    """
    检查新模型是否可用
        step 0: 联通性
        step 1：功能性（是否能够正常调用）
    :param data:
    :return:
    """
    step = data.get("step", 0)
    if step == 0:
        # 网络连通性测试
        return web_connection_check(data)
    elif step == 1:
        # 功能性测试
        return llm_dry_run(data)
    else:
        return next_console_response(error_code=1002, result={'status': '成功'})


def web_connection_check(data):
    """
    检查URL的网络连通性
    :param data:
    :return:

    """
    model = data.get("model", {})
    step = data.get("step", 0)
    timeout = 5
    url = model.get("llm_base_url", "")
    check_result = {
        "llm_base_url": url,
        "domain": '',
        "ip": '',  # 解析域名到IP地址
        "port": '',
        "duration": '',
        "step": step,
        "status": "",
        "msg": ""
    }
    domain = ''
    port = ''
    # 解析出 domain 和 port
    try:
        parsed = urlparse(url)
        domain = parsed.hostname
        port = parsed.port

        if port is None:
            if parsed.scheme == 'https':
                port = 443
            elif parsed.scheme == 'http':
                port = 80
            else:
                check_result["status"] = "失败"

        # 设置 domain 和 port 到 check_result
        check_result["domain"] = domain
        check_result["port"] = port

    except Exception as e:
        check_result["status"] = "失败"

    if check_result["status"] == "失败":
        check_result["msg"] = "模型URL协议错误，无法解析！"
        check_result["ip"] = "未知"  # 设置默认值
        return next_console_response(result=check_result)
    # 检查指定域名的端口连通性（使用 socket）
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((domain, port))
            if result != 0:
                check_result["status"] = "失败"

    except Exception as e:
        check_result["status"] = "失败"

    if check_result["status"] == "失败":
        check_result["msg"] = f"模型URL端口{port}不可达，请检查网络或URL是否正确！"
        # 尝试解析 IP 用于信息
        try:
            ip = socket.gethostbyname(domain)

        except Exception:
            ip = "解析失败"
        check_result["ip"] = ip

        return next_console_response(result=check_result)

    # 使用 requests 库测试 HTTP/HTTPS 端口的连通性
    try:
        start_time = time.time()
        requests.get(url, timeout=timeout, verify=False, allow_redirects=True)  # 忽略 SSL 证书验证
        duration = time.time() - start_time

    except requests.RequestException:
        check_result["status"] = "失败"
        check_result["msg"] = f"模型URL端口{port}不可达，请检查网络或URL是否正确！"

        # 尝试解析 IP 用于信息
        try:
            ip = socket.gethostbyname(domain)
        except Exception:
            ip = "解析失败"
        check_result["ip"] = ip
        return next_console_response(result=check_result)

    # 成功时解析 IP
    try:
        ip = socket.gethostbyname(domain)
    except Exception as e:
        ip = "解析失败"
    return next_console_response(result={
        "llm_base_url": url,
        "domain": domain,
        "ip": ip,
        "port": port,
        "status": "成功",
        "duration": f"{duration:.2f}秒",
        "msg": "模型URL网络连通性测试通过！"
    })


def llm_dry_run(data):
    """
    模型干跑,
        根据不同厂商，执行不同的干跑逻辑：
            优先使用厂商的sdk
            其次使用openai sdk
            最后使用通用的http请求
        自定义模型厂商的干跑逻辑：
            根据参数
    :return:
    """
    model = data.get("model", {})
    llm_company = model.get("llm_company", "")
    llm_type = model.get("llm_type", "")
    schema_type = model.get("schema_type", "nc")
    check_result = {
        "llm_type": llm_type,
        "llm_company": llm_company,
        "test_case": "你好,请简单自我介绍",
        "answer": "",
        "duration": "",
        "status": "",
        "msg": ""
    }
    from app.services.configure_center.llm import NextConsoleLLMClient
    from app.services.app_center.node_params_service import load_properties
    extra_headers_schema = model.get("extra_headers", {})
    extra_body_schema = model.get("extra_body", {})
    if schema_type == 'nc':
        try:
            extra_headers = load_properties(extra_headers_schema.get('properties', {}), {})
        except Exception as e:
            extra_headers = {}
        try:
            extra_body = load_properties(extra_body_schema.get('properties', {}), {})
        except Exception as e:
            extra_body = {}
    else:
        extra_headers = extra_headers_schema
        extra_body = extra_body_schema
    model["extra_headers"] = extra_headers
    model["extra_body"] = extra_body
    begin_time = time.time()
    try:
        llm_client = NextConsoleLLMClient({
            'base_url': model.get("llm_base_url", ""),
            'api_key': model.get("llm_api_secret_key", ''),
            'max_tokens': model.get("max_tokens", 204800),
            'model_type': llm_type,
            'llm_company': llm_company,
            'is_std_openai': model.get("is_std_openai", True),
            'llm_config': {
                'llm_name': model.get("llm_name", ""),
                'use_default': model.get("use_default", True),
                'temperature': model.get("temperature", 0.7),
                'top_p': model.get("top_p", 1),
                'n': model.get("n", 1),
                'stream': model.get("stream", True),
                'stop': model.get("stop", []),
                'presence_penalty': model.get("presence_penalty", 0),
                'frequency_penalty': model.get("frequency_penalty", 0),
                'response_format': model.get("response_format", {"type": "text"}),
                'extra_headers': model.get("extra_headers", {}),
                'extra_body': model.get("extra_body", {})
            },
        })
    except ValueError as ve:
        check_result["status"] = "失败"
        check_result["msg"] = f"模型功能性测试失败，错误信息：{str(ve)}"
        check_result["duration"] = f"{(time.time() - begin_time):.2f}秒"
        return next_console_response(result=check_result)
    if llm_type in ("文本生成", '全模态'):
        text_generate_model_dry_run(llm_client, check_result)
    elif llm_type == "推理模型":
        reason_model_dry_run(llm_client, check_result)
    elif llm_type == "图片理解":
        image_understand_model_dry_run(llm_client, check_result)
    elif llm_type == "向量模型":
        embedding_model_dry_run(llm_client, check_result)
    elif llm_type == "排序模型":
        rerank_model_dry_run(llm_client, check_result)
    elif llm_type == "图片生成":
        image_generate_model_dry_run(llm_client, check_result)

    else:
        check_result["status"] = "失败"
        check_result["msg"] = f"模型功能性测试失败，错误信息：暂不支持此模型的调用！"
    check_result["duration"] = f"{(time.time() - begin_time):.2f}秒"
    return next_console_response(result=check_result)


def text_generate_model_dry_run(llm_client, check_result):
    """
    文本模型干跑
    """

    messages = [{"role": "user", "content": "你好,请简单自我介绍"}]
    chat_params = {
        "messages": messages,
        "stream": False,
        "use_default": True
    }
    try:
        res = llm_client.chat(chat_params).model_dump_json()
        res = json.loads(res)
        msg = res.get("choices")[0].get("message").get("content")
        check_result["answer"] = msg
        check_result["status"] = "成功"
        check_result["msg"] = "模型功能性测试通过！"
    except Exception as e:
        check_result["status"] = "失败"
        check_result["msg"] = f"模型功能性测试失败，错误信息：{str(e)}"


def reason_model_dry_run(llm_client, check_result):
    messages = [{"role": "user", "content": "你好,3.11 和 3.8 两个数字哪个大"}]
    chat_params = {
        "messages": messages,
        "stream": True,
        "use_default": True
    }
    check_result["test_case"] = "你好,3.11 和 3.8 两个数字哪个大"
    reason_content = ""
    content = ""
    try:
        completion = llm_client.chat(chat_params)
        for chunk in completion:
            chunk_res = chunk.model_dump_json()
            chunk_res = json.loads(chunk_res)
            try:
                reason_content += chunk_res.get("choices")[0].get("delta").get("reasoning_content", "")
            except Exception as e:
                pass
            try:
                content += chunk_res.get("choices")[0].get("delta").get("content", "")
            except Exception as e:
                pass
        check_result["answer"] = f"推理过程：{reason_content}，最终答案：{content}"
        check_result["status"] = "成功"
        check_result["msg"] = "模型功能性测试通过！"
    except Exception as e:
        check_result["status"] = "失败"
        check_result["msg"] = f"模型功能性测试失败，错误信息：{str(e)}"


def image_understand_model_dry_run(llm_client, check_result):
    """
    图像模型干跑
    """
    import os
    import base64
    test_image_path = os.path.join(app.root_path, 'config', 'static', 'ide-empty.png')
    with open(test_image_path, 'rb') as f:
        encoded_string = base64.b64encode(f.read()).decode('utf-8')
        url = "data:image/png;base64,{}".format(encoded_string)
    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": "你好,请问图中有几个盒子？"},
            {
                "type": "image_url",
                "image_url": {
                    "url": url,
                    "detail": "auto"
                }
            }
        ]}
    ]
    chat_params = {
        "messages": messages,
        "stream": False,
        "use_default": True
    }
    check_result["test_case"] = "你好,请问图中有几个盒子？"
    check_result["test_image"] = url
    try:
        res = llm_client.chat(chat_params).model_dump_json()
        res = json.loads(res)
        msg = res.get("choices")[0].get("message").get("content")
        check_result["answer"] = msg
        check_result["status"] = "成功"
        check_result["msg"] = "模型功能性测试通过！"
    except Exception as e:
        check_result["status"] = "失败"
        check_result["msg"] = f"模型功能性测试失败，错误信息：{str(e)}"


def embedding_model_dry_run(llm_client, check_result):
    """

    """
    input_messages = [
        "你好,请简单自我介绍",
        "请介绍一下你自己",
    ]
    embedding_params = {
        "input": input_messages,
        "dimensions": 1024
    }
    check_result["test_case"] = "你好,请简单自我介绍;请介绍一下你自己"
    try:
        res = llm_client.embedding(embedding_params)
        res = json.loads(res)
        if res.get("data") and len(res.get("data")) == 2:
            check_result["answer"] = "模型返回了正确的向量结果！"
            check_result["status"] = "成功"
            check_result["msg"] = "模型功能性测试通过！"
        else:
            check_result["status"] = "失败"
            check_result["msg"] = f"模型功能性测试失败，错误信息：返回的向量结果异常！"
    except Exception as e:
        check_result["status"] = "失败"
        check_result["msg"] = f"模型功能性测试失败，错误信息：{str(e)}"


def rerank_model_dry_run(llm_client, check_result):
    """
    重排序模型干跑
    """
    input_messages = [
        "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序",
        "量子计算是计算科学的一个前沿领域",
        "预训练语言模型的发展给文本排序模型带来了新的进展"
    ]
    query = "什么是文本排序模型？"
    rerank_params = {
        "documents": input_messages,
        "query": query,
        "top_n": 3
    }
    check_result["test_case"] = "什么是文本排序模型？"
    try:
        res = llm_client.rerank(rerank_params)
        if res:
            check_result["answer"] = res
            check_result["status"] = "成功"
            check_result["msg"] = "模型功能性测试通过！"
        else:
            check_result["status"] = "失败"
            check_result["msg"] = f"模型功能性测试失败，错误信息：返回的重排序结果异常！"
    except Exception as e:
        check_result["status"] = "失败"
        check_result["msg"] = f"模型功能性测试失败，错误信息：{str(e)}"


def image_generate_model_dry_run(llm_client, check_result):
    """
    图像生成模型干跑
    """
    import base64
    prompt = "一只在草地上奔跑的柴犬，阳光明媚，背景是蓝天白云，高清摄影"
    image_params = {
        "prompt": prompt,
        "n": 1,
        "size": "1328*1328"
    }
    check_result["test_case"] = prompt
    answer_images = []
    try:
        res = llm_client.generate_image(image_params)
        for result in res.output.results:
            encoded_string = base64.b64encode(requests.get(result.url).content).decode('utf-8')
            url = "data:image/png;base64,{}".format(encoded_string)
            answer_images.append(url)
        if len(answer_images):
            check_result["answer_images"] = answer_images
            check_result["status"] = "成功"
            check_result["msg"] = "模型功能性测试通过！"
        else:
            check_result["status"] = "失败"
            check_result["msg"] = f"模型功能性测试失败，错误信息：返回的图像结果异常！"
    except Exception as e:
        check_result["status"] = "失败"
        check_result["msg"] = f"模型功能性测试失败，错误信息：{str(e)}"


def video_generate_model_dry_run(llm_client, check_result):
    """
    视频生成模型干跑
    :param llm_client:
    :param check_result:
    :return:
    """
    # todo
