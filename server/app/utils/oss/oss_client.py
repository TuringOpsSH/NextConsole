import uuid
import os
from app.app import app
from app.services.configure_center.response_utils import next_console_response
from pathlib import Path

module_base_map = {
    "app_center": "app_center",
    "assistant_center": "assistant_center",
    "contact": "contact",
    "function_center": "function_center",
    "knowledge_center": "knowledge_center",
    "next_console": "next_console",
    "online_service": "online_service",
    "resource_center": "resource_center",
    "support_ticket": "support_ticket",
    "user_center": "user_center",
    "task_center": "task_center",
    "configure_center": "configure_center",
    "edith_web": "edith_web",
    "wiki_center": "wiki_center",
    "session": "session"
}


def get_current_bucket_id(base_dir, module_name):
    """
    获取当前模块的bucket_id
    """
    module_base_dir = str(os.path.join(base_dir, module_base_map[module_name]))
    # 获取最新的bucket_id
    all_bucket_ids = []
    for bucket_id_str in os.listdir(module_base_dir):
        if not bucket_id_str.isdigit():
            continue
        bucket_id = int(bucket_id_str)
        if not os.path.isdir(os.path.join(module_base_dir, bucket_id_str)):
            continue
        all_bucket_ids.append(bucket_id)
    max_bucket_id = max(all_bucket_ids) if all_bucket_ids else 0
    # 如果当前bucket_id的文件数量超过10000，则新建一个bucket_id
    current_bucket_dir = os.path.join(module_base_dir, str(max_bucket_id))
    if not os.path.exists(current_bucket_dir):
        os.makedirs(current_bucket_dir)
    if len(os.listdir(current_bucket_dir)) >= app.config["bucket_size"]:
        max_bucket_id += 1
        os.makedirs(os.path.join(module_base_dir, str(max_bucket_id)))
    return max_bucket_id


def generate_new_path(module_name, user_id, file_name=None, suffix='', prefix='', file_type="file"):
    """
    生成文件或者文件夹的路径
        module_name: 模块名
        user_id : 用户id
        suffix: 资源的前缀
        data目录下的文件路径格式：{data_dir}/{module_name}/{bucket_id}/{user_id}/{file_name}
    资源库
    """
    if module_name not in module_base_map:
        return next_console_response(error_status=True, error_message=f"模块{module_name}不存在！")
    module_base_dir = str(os.path.join(app.config['data_dir'], module_base_map[module_name]))
    if not os.path.exists(module_base_dir):
        os.makedirs(module_base_dir)
    # 获取最新的bucket_id
    current_bucket_id = get_current_bucket_id(app.config['data_dir'], module_name)
    # 检查用户目录是否存在
    user_dir = os.path.join(module_base_dir, str(current_bucket_id), str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    # 生成文件名
    file_code = uuid.uuid4().hex
    prefix = prefix.replace('/', '-')
    suffix = suffix.replace('/', '-')
    if not file_name:
        file_name = f"{prefix}.{file_code}.{suffix}"
    # 生成文件路径
    file_path = os.path.join(user_dir, file_name)
    # 检查文件是否存在
    if os.path.exists(file_path):
        return next_console_response(error_status=True, error_message=f"文件{file_path}已存在！")
    if file_type == "dir":
        os.makedirs(file_path)
    elif file_type == "file":
        with open(file_path, "w") as f:
            f.write("")
    return next_console_response(result=file_path)


def generate_download_url(module_name, file_path, suffix='', prefix=''):
    """
    为平台内的资源生成对外的下载软链接，需要保证软链接的有效性，
    软连接的格式类型由调用方自行定义
    软连接的幂等性由调用方保证
    软连接的生命周期由调用方自行管理
        file: 资源的路径
        链接格式：{download_dir}/{module_name}/{bucket_id}/{uuid}
    return: 资源的下载链接
        {domain}/download/{module_name}/{bucket_id}/{uuid}
    """
    if module_name not in module_base_map:
        return next_console_response(error_status=True, error_message=f"模块{module_name}不存在！")
    module_base_dir = str(os.path.join(app.config['download_dir'], module_base_map[module_name]))
    if not os.path.exists(module_base_dir):
        os.makedirs(module_base_dir)
    # 验证文件是否存在
    if not os.path.exists(file_path):
        return next_console_response(error_status=True, error_message=f"文件{file_path}不存在！")
    # 获取最新的bucket_id
    current_bucket_id = get_current_bucket_id(app.config['download_dir'], module_name)
    # 生成uuid
    uuid_code = f"{prefix}.{uuid.uuid4().hex}.{suffix}"
    dest_link = os.path.join(module_base_dir, str(current_bucket_id), uuid_code)
    # 创建相对路径的软连接
    src = Path(file_path)
    dest = Path(dest_link)
    relative_path = os.path.relpath(src, dest.parent)
    if not os.path.exists(dest.parent):
        os.makedirs(dest.parent)
    try:
        dest.symlink_to(relative_path)
    except FileExistsError:
        return next_console_response(error_status=True, error_message=f"文件{dest_link}已存在！")
    dest_link_url = f"{app.config['domain']}/download/{module_base_map[module_name]}/{current_bucket_id}/{uuid_code}"
    return next_console_response(result=dest_link_url)


def get_download_url_path(download_url):
    """
    获取url对应的软连接的路径
    """
    download_url = download_url.split("download")[-1]
    download_url = download_url.split("/")
    module_name = download_url[1]
    bucket_id = download_url[2]
    uuid_code = download_url[3]
    module_base_dir = str(os.path.join(app.config['download_dir'], module_base_map[module_name]))
    target_path = os.path.join(module_base_dir, bucket_id, uuid_code)
    if os.path.exists(target_path):
        return target_path
    else:
        return None


