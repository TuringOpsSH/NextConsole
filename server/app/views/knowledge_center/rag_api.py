
import numpy as np
import requests
from flask import request
from app.app import app


def auto_lower(texts):
    if app.config.get("EMBEDDING_AUTO_LOWER", False) and type(texts) is list:
        texts = [t.lower() for t in texts]
    return texts


@app.route('/next_console/knowledge_center/embedding', methods=['POST'])
def embedding():
    texts = request.json.get("texts", [])

    url = app.config.get("EMBEDDING_ENDPOINT")
    if not url:
        return 'EMBEDDING_ENDPOINT not configured'
    model = app.config.get("EMBEDDING_MODEL", "BAAI/bge-m3")
    payload = {
        "model": model,
        "input": auto_lower(texts),
        "encoding_format": "float"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer {}".format(app.config.get("EMBEDDING_KEY"))
    }

    r = requests.post(url, json=payload, headers=headers).json()
    rn = {'dense_vecs': [d['embedding'] for d in r['data']],
          'lexical_weights': [{} for d in r['data']],
          'colbert_vecs': [[] for d in r['data']]}
    return rn


@app.route('/next_console/knowledge_center/recall', methods=['GET', 'POST', 'PUT', 'DELETE'])
def recall():
    query = request.json.get("query", "")
    texts = request.json.get("texts", [])
    if len(texts) == 0:
        return []
    url = app.config.get("EMBEDDING_ENDPOINT")
    if not url:
        return 'EMBEDDING_ENDPOINT not configured'
    model = app.config.get("EMBEDDING_MODEL", "BAAI/bge-m3")
    payload = {
        "model": model,
        "input": auto_lower([query] + texts),
        "encoding_format": "float"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer {}".format(app.config.get("EMBEDDING_KEY"))
    }
    r = requests.post(url, json=payload, headers=headers).json()
    embeddings = [d['embedding'] for d in r['data']]
    score = np.array(embeddings[0]) @ np.array(embeddings[1:]).T
    return score.tolist()


@app.route('/next_console/knowledge_center/reranker', methods=['GET', 'POST', 'PUT', 'DELETE'])
def reranker():
    pairs = request.json.get("pairs", [])
    if len(pairs) == 0:
        return []
    query = pairs[0][0]
    documents = [p[1] for p in pairs]
    url = app.config.get("RERANK_ENDPOINT")
    if not url:
        return 'RERANK_ENDPOINT not configured'
    model = app.config.get("RERANK_MODEL", "BAAI/bge-reranker-v2-m3")
    payload = {
        "model": model,
        "query": query,
        "documents": documents,
        "return_documents": False,
        "max_chunks_per_doc": 1024,
        "overlap_tokens": 80
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer {}".format(app.config.get("RERANK_KEY"))
    }
    scores = [0 for p in pairs]
    for e in requests.post(url, json=payload, headers=headers).json()['results']:
        scores[e['index']] = e['relevance_score']
    return scores

