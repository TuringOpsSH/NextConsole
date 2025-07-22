from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.services.resource_center.resource_object_service import *
from app.services.resource_center.resource_usage_service import get_resource_usage


@app.route('/next_console/resources/object/search', methods=['GET', 'POST'])
@jwt_required()
def resource_object_search():
    """
    获取资源目录列表
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_resource_object(params)


@app.route('/next_console/resources/object/search_by_keyword_in_resource', methods=['GET', 'POST'])
@jwt_required()
def resource_object_search_in_resource():
    """
    在指定目录下搜索资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_keyword = params.get("resource_keyword")
    if not resource_keyword:
        return next_console_response(error_status=True, error_message="关键字不能为空！")
    return search_by_keyword_in_resource(params)


@app.route('/next_console/resources/object/get_path', methods=['GET', 'POST'])
@jwt_required()
def resource_object_get_path():
    """
    获取资源目录列表
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return get_resource_object_path(params)


@app.route('/next_console/resources/object/get', methods=['GET', 'POST'])
@jwt_required()
def resource_object_get():
    """
    获取资源对象元信息
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return get_resource_object(params)


@app.route('/next_console/resources/object/upload_task/add', methods=['GET', 'POST'])
@jwt_required()
def resource_object_upload_task_add():
    """
    新增资源上传任务
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)

    resource_name = params.get("resource_name")
    resource_size_in_MB = params.get("resource_size")
    content_max_idx = params.get("content_max_idx")
    resource_md5 = params.get("resource_md5")
    if not resource_name:
        return next_console_response(error_status=True, error_message="资源名称不能为空！")
    if not resource_size_in_MB:
        return next_console_response(error_status=False, error_message="资源大小不能为空！")
    if content_max_idx is None:
        return next_console_response(error_status=True, error_message="资源分块数不能为空！")
    if not resource_md5:
        return next_console_response(error_status=True, error_message="资源md5值不能为空！")
    return add_resource_upload_task(params)


@app.route('/next_console/resources/object/upload_task/update', methods=['GET', 'POST'])
@jwt_required()
def resource_object_upload_task_update():
    """
    新增资源上传任务
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)

    task_id = params.get("task_id")

    if not task_id:
        return next_console_response(error_status=True, error_message="任务id缺失！")
    return update_resource_upload_task(params)


@app.route('/next_console/resources/object/upload', methods=['GET', 'POST'])
@jwt_required()
def resource_object_upload():
    """
    上传资源对象,form-data
    :return:
    """
    params = request.form.to_dict()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    chunk_content = request.files.get("chunk_content")
    if not chunk_content:
        return next_console_response(error_status=True, error_message="资源块不能为空！")
    chunk_task_id = params.get("chunk_task_id")
    if not chunk_task_id:
        return next_console_response(error_status=True, error_message="任务id不能为空！")
    chunk_index = params.get("chunk_index")
    if chunk_index is None:
        return next_console_response(error_status=True, error_message="块索引不能为空！")

    chunk_MD5 = params.get("chunk_MD5")
    if not chunk_MD5:
        return next_console_response(error_status=True, error_message="块MD5不能为空！")
    return upload_resource_object(params, chunk_content)


@app.route('/next_console/resources/object/delete', methods=['GET', 'POST'])
@jwt_required()
def resource_object_delete():
    """
    删除资源对象
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return delete_resource_object(params)


@app.route('/next_console/resources/object/batch_delete', methods=['GET', 'POST'])
@jwt_required()
def resource_object_batch_delete():
    """
    删除资源对象
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_list = params.get("resource_list")
    if not resource_list:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return batch_delete_resource_object(params)


@app.route('/next_console/resources/object/add', methods=['GET', 'POST'])
@jwt_required()
def resource_object_add():
    """
    新建资源对象
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_name = params.get("resource_name")
    if not resource_name:
        return next_console_response(error_status=True, error_message="资源名称不能为空！")
    return add_resource_object(params)


@app.route('/next_console/resources/object/batch_add_folder', methods=['GET', 'POST'])
@jwt_required()
def resource_object_batch_add_folder():
    """
    批量添加资源目录
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_list = params.get("resource_list")
    if not resource_list:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return batch_add_resource_folder(params)


@app.route('/next_console/resources/object/update', methods=['GET', 'POST'])
@jwt_required()
def resource_object_update():
    """
    更新资源对象
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return update_resource_object(params)


@app.route('/next_console/resources/object/download', methods=['GET', 'POST'])
@jwt_required()
def resource_object_download():
    """
    下载资源对象
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return download_resource_object(params)


@app.route('/next_console/resources/object/batch_download', methods=['GET', 'POST'])
@jwt_required()
def resource_object_batch_download():
    """
    批量下载资源对象
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_list = params.get("resource_list")
    if not resource_list:
        return next_console_response(error_status=True, error_message="资源id不能为空！")
    return batch_download_resource_object(params)


@app.route('/next_console/resources/object/move', methods=['GET', 'POST'])
@jwt_required()
def resource_object_move():
    """
    移动资源对象
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id_list = params.get("resource_id_list")
    try:
        resource_id_list = [int(i) for i in resource_id_list if i is not None]
        params["resource_id_list"] = resource_id_list
    except ValueError:
        return next_console_response(error_status=True, error_message="资源id错误！")
    target_resource_id = params.get("target_resource_id")
    if not resource_id_list or not target_resource_id:
        return next_console_response(error_status=True, error_message="资源id不能为空！")

    return mv_resource_object(params)


@app.route('/next_console/resources/usage/get', methods=['GET', 'POST'])
@jwt_required()
def resource_usage_get():
    """
    获取资源使用情况
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)

    return get_resource_usage(params)


@app.route('/next_console/resources/ref/build', methods=['GET', 'POST'])
@jwt_required()
def resource_ref_build():
    """
    构建资源引用
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_list = params.get("resource_list", [])
    try:
        resource_list = [int(i) for i in resource_list if i is not None]
        params["resource_list"] = resource_list
    except ValueError:
        return next_console_response(error_status=True, error_message="资源id错误！")
    return build_resource_object_ref(params)


@app.route('/next_console/resources/ref/rebuild', methods=['GET', 'POST'])
@jwt_required()
def resource_ref_rebuild():
    """
    重构资源引用
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_list = params.get("resource_list", [])
    try:
        resource_list = [int(i) for i in resource_list if i is not None]
        params["resource_list"] = resource_list
    except ValueError:
        return next_console_response(error_status=True, error_message="资源id错误！")
    return build_resource_object_ref(params)


@app.route('/next_console/resources/resource_recent_count', methods=['GET', 'POST'])
@jwt_required()
def resource_recent_count():
    """
    获取最近资源数量
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return get_resource_recent_count(params)


@app.route('/next_console/resources/search_by_recent_upload', methods=['GET', 'POST'])
@jwt_required()
def resource_search_by_recent_upload():
    """
    获取最近上传的资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_by_recent_upload(params)


@app.route('/next_console/resources/resource_type_count', methods=['GET', 'POST'])
@jwt_required()
def resource_type_count():
    """
    获取最近上传的资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return get_resource_type_count(params)


@app.route('/next_console/resources/resource_recent_format_count', methods=['GET', 'POST'])
@jwt_required()
def resource_format_count():
    """
    获取最近上传的资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return get_resource_recent_format_count(params)


@app.route('/next_console/resources/search_by_recent_index', methods=['GET', 'POST'])
@jwt_required()
def resource_search_by_recent_index():
    """
    获取最近索引的资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_by_recent_index(params)


@app.route('/next_console/resources/search_by_resource_type', methods=['GET', 'POST'])
@jwt_required()
def resource_search_by_resource_type():
    """
    获取最近索引的资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_by_resource_types(params)


@app.route('/next_console/resources/search_by_resource_tags', methods=['GET', 'POST'])
@jwt_required()
def resource_search_by_resource_tags():
    """
    获取用户标签的资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_by_resource_tags(params)


@app.route('/next_console/resources/search_by_resource_keyword', methods=['GET', 'POST'])
@jwt_required()
def resource_search_by_resource_keyword():
    """
    获取用户标签的资源
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_keyword = params.get("resource_keyword")
    auth_type = params.get("auth_type")
    allowed_auth_types = ['read', 'download', 'edit', 'manage']
    if not resource_keyword:
        return next_console_response(error_status=True, error_message="关键字不能为空！")
    if auth_type and auth_type not in allowed_auth_types:
        return next_console_response(error_status=True,
                                     error_message="无效的权限类型！仅支持: read, download, edit, manage")
    return search_by_resource_keyword(params)



