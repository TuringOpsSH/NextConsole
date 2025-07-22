from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, decode_token
)

from app.app import app
from app.services.resource_center.resource_view import *
from app.services.wiki_center.wiki_file_service import *


@app.route('/next_console_admin/resources_view/get', methods=['GET', 'POST'])
@jwt_required()
def resource_view_meta_get():
    """
    获取资源视图元数据
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    resource_id = params.get("resource_id")
    if not resource_id:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0]
        # 如果 X-Forwarded-For 不存在，则使用 X-Real-IP
    elif 'X-Real-IP' in request.headers:
        ip = request.headers['X-Real-IP']
        # 如果都没有，则使用 remote_addr
    else:
        ip = request.remote_addr
    params["ip"] = ip
    return get_resource_view_meta(params)


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>', methods=['GET', 'POST'])
def WPS_view_meta_get(file_id):
    """
    为wps提供资源视图元数据
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        app.logger.warning(f"{token},{e}")
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")

    if not file_id:
        app.logger.warning(f"{token},资源id为空")
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    # todo 检验token
    # 如果 file_id 是 wiki_ 开头
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档请求: {file_id}")
        return wps_get_wiki_file_meta({"page_id": file_id[5:], 'user_id': user_id})
    return wps_get_file_meta({"file_id": file_id, 'user_id': user_id})


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/download', methods=['GET', 'POST'])
def WPS_view_meta_download(file_id):
    """
    为wps提供资源视图元数据
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="认证异常")

    if not file_id:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    # todo 检验token

    # 如果 file_id 是 wiki_ 开头
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档下载请求: {file_id}")
        return wps_get_wiki_file_download({"file_id": file_id, 'user_id': user_id})

    return wps_get_file_download({"file_id": file_id, 'user_id': user_id})


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/permission', methods=['GET', 'POST'])
def WPS_view_meta_permission(file_id):
    """
    为wps提供资源视图元数据
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not file_id:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    # 如果 file_id 是 wiki_ 开头
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档权限请求: {file_id}")
        return wps_get_wiki_file_permission({"file_id": file_id, 'user_id': user_id})
    return wps_get_file_permission({"file_id": file_id, 'user_id': user_id})


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/users', methods=['GET', 'POST'])
def WPS_view_meta_users():
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    user_ids = request.args.getlist('user_ids')
    return wps_get_file_users({"user_ids": user_ids})


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/upload/prepare', methods=['GET', 'POST'])
def WPS_view_prepare(file_id):
    """
    三阶段保存-准备
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not file_id:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    return {
      "code": 0,
      "data": {
        "digest_types": ["sha256"]
      },
      "message": ""
    }


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/upload/address', methods=['GET', 'POST'])
def WPS_view_address(file_id):
    """
    三阶段保存-上传地址
    :param file_id:
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        app.logger.warning(f'wps-address,认证异常,f{token}')
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not file_id:
        app.logger.warning(f'wps-address,资源id,f{file_id}')
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    # 如果 file_id 是 wiki_ 开头
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档上传地址请求: {file_id}")
        return wps_wiki_upload_address({
        "file_id": file_id,
        "user_id": user_id,
        'token': token,
        })

    return wps_upload_address({
        "file_id": file_id,
        "user_id": user_id,
        'token': token,
    })


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/upload/complete', methods=['GET', 'POST'])
def WPS_view_complete(file_id):
    """
    三阶段保存-提交
    :param file_id:
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not file_id:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    params = request.get_json()
    params["file_id"] = file_id
    params["user_id"] = user_id
    # 如果 file_id 是 wiki_ 开头
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档提交请求: {file_id}")
        return wps_wiki_upload_complete(params)
    return wps_upload_complete(params)


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/upload', methods=['GET', 'POST', 'PUT'])
def WPS_view_upload(file_id):
    """
    接受wps的上传文件
    :return:
    """
    if not file_id:
        app.logger.warning(f'wps-upload,文件不存在:{file_id}')
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    try:
        file_data = request.data
        params = request.args.to_dict()
        app.logger.warning(f"file_id:{file_id},params:{params}")
    except Exception as e:
        app.logger.warning(f"file_id:{file_id},params:{e}")
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档上传请求: {file_id}")
        # wiki文档上传
        return wps_wiki_upload_file({
            "file_id": file_id,
            "file_data": file_data,
            "resource_path": params.get("resource_path"),
            "user_id": params.get("user_id"),
        })

    # 保存文件
    return wps_upload_file({
        "file_id": file_id,
        "file_data": file_data,
        "resource_path": params.get("resource_path"),
        "user_id": params.get("user_id"),
    })


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/name', methods=['GET', 'POST', 'PUT'])
def WPS_rename(file_id):
    """

    :param file_id:
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        app.logger.warning(f"重命名鉴权失败：{token}")
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not file_id:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    params = request.get_json()
    name = params.get("name")
    if not name:
        app.logger.warning(f"重命名失败，资源名称为空：{file_id}")
        return next_console_response(error_status=True, error_code=1001, error_message="name")
    # 如果 file_id 是 wiki_ 开头
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档重命名请求: {file_id}")
        return wps_wiki_rename({
            "file_id": file_id,
            "name": name,
            "user_id": user_id,
        })
    return wps_rename({
        "user_id": user_id,
        "file_id": file_id,
        "name": name
    })


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/versions', methods=['GET'])
def WPS_get_history_version(file_id):
    """
    获取文档历史版本列表
    :param file_id:
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not file_id:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    params = request.args.to_dict()
    # 如果 file_id 是 wiki_ 开头
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档版本请求: {file_id}")
        return wps_get_wiki_version_list({
            "file_id": file_id,
            "user_id": user_id,
            "offset": params.get("offset"),
            "limit": params.get("limit"),
        })
    return wps_get_version_list({
        "file_id": file_id,
        "user_id": user_id,
        "offset": params.get("offset"),
        "limit": params.get("limit"),
    })


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/versions/<version>', methods=['GET'])
def WPS_get_history_version_meta(file_id, version):
    """
    获取文档指定历史版本
    :param file_id:
    :param version:
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not file_id:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    # 如果 file_id 是 wiki_ 开头
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档版本请求: {file_id}")
        return wps_get_wiki_version_meta({
            "file_id": file_id,
            "user_id": user_id,
            "version": version,
        })
    return get_history_version_meta({
        "file_id": file_id,
        "user_id": user_id,
        "version": version,
    })


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/files/<file_id>/versions/<version>/download', methods=['GET'])
def WPS_get_history_version_download(file_id, version):
    """
    获取文档指定历史版本
    :param file_id:
    :param version:
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not file_id:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    # 如果 file_id 是 wiki_ 开头
    if file_id.startswith("wiki_"):
        app.logger.info(f"处理wiki文档版本下载请求: {file_id}")
        return wps_get_wiki_version_download({
            "file_id": file_id,
            "user_id": user_id,
            "version": version,
        })
    return get_history_version_download({
        "file_id": file_id,
        "user_id": user_id,
        "version": version,
    })


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/object/<key>', methods=['PUT'])
def WPS_put_attachment(key):
    """
    上传附件
    :param key:
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not key:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    params = request.args.to_dict()
    name = params.get('name')
    file_data = request.data
    return put_new_attachment_for_wps({
        "key": key,
        "name": name,
        "file_data": file_data,
        "user_id": user_id,
    })


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/object/<key>/url', methods=['GET'])
def WPS_get_attachment_url(key):
    """
    获取附件地址
    :param key:
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    if not key:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    params = request.args.to_dict()
    scale_max_fit_width = params.get('scale_max_fit_width')
    scale_max_fit_height = params.get('scale_max_fit_height')
    scale_long_edge = params.get('scale_long_edge')
    return get_attachment_url({
        "key": key,
        "user_id": user_id,
        "scale_max_fit_width": scale_max_fit_width,
        "scale_max_fit_height": scale_max_fit_height,
        "scale_long_edge": scale_long_edge,

    })


@app.route('/next_console_admin/resources_view/WPS/v3/3rd/object/copy', methods=['POST'])
def WPS_copy_attachment():
    """
    复制附件
    :return:
    """
    # 获取token
    token = request.headers.get("X-WebOffice-Token")
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message="资源id")
    params = request.get_json()
    key_dict = params.get("key_dict")
    return copy_attachment({
        "key_dict": key_dict,
        "user_id": user_id,
    })
