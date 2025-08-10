import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.app import app


def chunk_embedding(params):
    """
    将文件分块内容进行嵌入处理，生成向量表示，并存储到数据库中。
        输入配置
        输入content
    :param params: 包含文件分块信息的参数字典
    根据任务数n进行线程池并发处理。

    """
    contents = params.get("contents", [])
    config = params.get("config", {})
    if not contents:
        return
    # 将内容分批次处理
    batches = [contents[i:i + config['batch_size']] for i in range(0, len(contents), config['batch_size'])]
    # 使用线程池并发处理
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        index = 0
        for batch in batches:
            future = executor.submit(embedding_call, {
                "content": batch,
                "config": config,
                "index": index
            })
            futures.append(future)
            index += 1

        # 收集所有结果
        embeddings_map = {}
        total_tokens = 0
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    total_tokens += result[2]
                    embeddings_map[result[0]] = result[1]
            except Exception as e:
                print(f"Embedding processing failed: {str(e)}")
    result = []
    index = 0
    for i in range(0, len(contents), config['batch_size']):
        embeddings = embeddings_map.get(index, [])
        if embeddings:
            result.extend(embeddings)
        index += 1
    return result, total_tokens


def embedding_call(params):
    """
    调用嵌入模型进行文本内容的向量化处理。
        输入配置
        输入content
        实际调用嵌入模型API进行处理，返回向量表示
    """
    content = params.get("content", [])
    config = params.get("config", {})
    index = params.get("index", 0)
    api = config.get("api", "")
    key = config.get("key", "")
    model = config.get("model", "")
    encoding_format = config.get("encoding_format", "float")
    if not content or not config:
        return None
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": content,
        "model": model,
        "encoding_format": encoding_format
    }
    try:
        response = requests.post(api, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        # 提取嵌入向量
        embeddings = []
        for item in data.get("data", []):
            embedding = item.get("embedding", None)
            if embedding:
                embeddings.append(embedding)
        return index, embeddings, data.get("usage", {}).get("total_tokens", 0)
    except requests.exceptions.RequestException as e:
        print(e)
        app.logger.warning(e)
        return None
    except Exception as e:
        print(e)
        app.logger.warning(e)
        return None


def rerank_call(params):
    documents = params.get("documents", [])
    query = params.get('query', "")
    config = params.get("config", {})
    api = config.get("api", "")
    key = config.get("key", "")
    model = config.get("model", "")
    max_chunks_per_doc = config.get("max_chunks_per_doc", 1024)
    overlap_tokens = config.get("overlap_tokens", 80)
    if not documents or not query:
        return []
    if not api:
        return 'RERANK_ENDPOINT not configured'
    payload = {
        "model": model,
        "query": query,
        "documents": documents,
        "return_documents": False,
        "max_chunks_per_doc": max_chunks_per_doc,
        "overlap_tokens": overlap_tokens
    }
    if model == "gte-rerank-v2":
        payload = {
            "model": model,
            "input": {
                "query": query,
                "documents": documents
            },
            "parameters": {
                "return_documents": False
            }
        }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer {}".format(key)
    }
    scores = [0 for i in range(len(documents))]
    try:
        result = requests.post(api, json=payload, headers=headers).json()
    except Exception as e:
        app.logger.error(f"Rerank API call failed: {str(e)}")
        return []
    if model == "gte-rerank-v2":
        result = result.get("output", {})
    try:
        for e in result['results']:
            scores[e['index']] = e['relevance_score']
    except KeyError as e:
        return []
    return scores
    # try:
    #     response = requests.post(api, json=payload, headers=headers)
    #     response.raise_for_status()
    #     data = response.json()
    #     for item in data.get("results", []):
    #         scores[item['index']] = item['relevance_score']
    #     return scores
    # except requests.exceptions.RequestException as e:
    #     return []
    # except Exception as e:
    #     return []
