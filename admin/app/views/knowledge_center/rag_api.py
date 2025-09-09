from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
import numpy as np
import requests
from flask import request
from app.app import app
from app.services.knowledge_center.rag_service_v3 import *


def auto_lower(texts):
    if app.config.get("EMBEDDING_AUTO_LOWER", False) and type(texts) is list:
        texts = [t.lower() for t in texts]
    return texts


@app.route('/next_console/knowledge_center/get_resource_rag_config', methods=['POST'])
@jwt_required()
def get_resource_rag_config():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    return get_parse_resource_service(params)


@app.route('/next_console/knowledge_center/get_parse_resource', methods=['POST'])
@jwt_required()
def get_parse_resource():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    return get_parse_resource_service(params)


@app.route('/next_console/knowledge_center/get_parse_resource_chunks', methods=['POST'])
@jwt_required()
def get_parse_resource_chunks():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    return get_parse_resource_chunks_service(params)


@app.route('/next_console/knowledge_center/delete_parse_resource_chunks', methods=['POST'])
@jwt_required()
def delete_parse_resource_chunks():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    chunk_ids = params.get("chunk_ids")
    if not chunk_ids:
        return next_console_response(error_status=True, error_message="参数异常！")
    return delete_parse_resource_chunks_service(params)


@app.route('/next_console/knowledge_center/update_parse_resource_chunk', methods=['POST'])
@jwt_required()
def update_parse_resource_chunks():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    chunk_id = params.get("chunk_id")
    if not chunk_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    return update_parse_resource_chunks_service(params)


@app.route('/next_console/knowledge_center/add_parse_resource_chunks', methods=['POST'])
@jwt_required()
def add_parse_resource_chunks():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    chunk_ids = params.get("chunk_ids")
    if not chunk_ids:
        return next_console_response(error_status=True, error_message="参数异常！")
    return delete_parse_resource_chunks_service(params)


@app.route('/next_console/knowledge_center/recall_parse_resource_chunk', methods=['POST'])
@jwt_required()
def recall_parse_resource_chunk():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    chunk_id = params.get("chunk_id")
    query_text = params.get("query_text", "")
    if not chunk_id or not query_text:
        return next_console_response(error_status=True, error_message="参数异常！")
    return parse_resource_chunk_recall_service(params)

