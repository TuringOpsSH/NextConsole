import requests
import json


def search_engine_serper(params):
    """
    Serper搜索引擎查询，返回资源对象
        {
      "title": "RAG检索增强生成技术进展| 2024年相关论文总结 - 知乎专栏",
      "link": "https://zhuanlan.zhihu.com/p/24843497294",
      "snippet": "本文将整理并简要介绍10篇与RAG相关的最新论文，帮助读者了解该领域的研究热点与发展趋势。 1. RankRAG: Unifying Retrieval-Augmented Generation ...",
      "date": "2025年2月24日",
      "position": 1
    },
    """
    query = params.get("query", "")
    key = params.get("key", "")
    config = params.get("config", {})
    headers = {
        'X-API-KEY': key,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "q": query,
        "gl": config.get("gl", "cn"),
        "hl": config.get("hl", "zh-cn"),
        "num": config.get("num", 10)
    })
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers, data=payload)
        response_data = response.json()
        credits = response_data.get('credits', 0)
        pages = response_data.get('organic', [])
    except Exception as e:
        print(f"Error parsing response: {e}")
        return [], 0
    return pages, credits

