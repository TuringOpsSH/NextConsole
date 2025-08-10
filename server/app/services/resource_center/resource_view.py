import json
from datetime import datetime
from app.models.resource_center.resource_model import ResourceObjectMeta, ResourceObjectHistory, ResourceAttachment
from app.models.resource_center.resource_model import ResourceViewRecord
from app.models.user_center.user_info import UserInfo
from app.services.configure_center.response_utils import next_console_response
from app.services.resource_center.resource_share_service import check_user_manage_access_to_resource
from app.services.resource_center.resource_share_service import get_user_access_to_resource
from app.app import app, db
import os
from app.services.configure_center.system_notice_service import send_wps_rename
from app.utils.oss.oss_client import generate_download_url, get_download_url_path, generate_new_path


def get_resource_view_meta(params):
    """
    获取资源视图元数据
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_id = params.get("resource_id")
    client_fingerprint = params.get("client_fingerprint")
    ip = params.get("ip", '')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    # 获取资源视图元数据
    resource_view = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not resource_view:
        return next_console_response(error_status=True, error_message="资源不存在！")
    # 检查资源权限
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": resource_view,
        "access_type": "read"
    }):
        return next_console_response(error_status=True, error_message="无权限查看资源！")
    new_resource_view_record = ResourceViewRecord(
        user_id=user_id,
        resource_id=resource_id,
        client_fingerprint=client_fingerprint,
        client_ip=ip
    )
    db.session.add(new_resource_view_record)
    db.session.commit()

    if not resource_view.resource_show_url and os.path.exists(resource_view.resource_path):
        resource_view.resource_show_url = generate_download_url(
            "resource_center",
            resource_view.resource_path,
            suffix=resource_view.resource_format
        ).json.get("result")
        db.session.add(resource_view)
        db.session.commit()
    res = resource_view.show_info()
    # todo 根据用户配置和系统配置生成
    view_config = {
        "support": True,
        "engine": "wps",
        "wps_config": {
            "wps_app_id": app.config.get("wps_app_id", "")
        }
    }
    if resource_view.resource_type in ("image", 'video', 'audio', 'media'):

        if resource_view.resource_type == 'image' or resource_view.resource_format in (
            "jpg", "jpeg", "png", "gif", "bmp", "webp", "svg",
        ):
            view_config["engine"] = "element"
        elif resource_view.resource_type == "video":
            view_config["engine"] = "video"
        elif resource_view.resource_type == "audio":
            view_config["engine"] = "audio"
        else:
            view_config["engine"] = "web"
    elif resource_view.resource_type in ('code', 'webpage', 'text'):
        if os.path.exists(resource_view.resource_path):
            try:
                with open(resource_view.resource_path, 'r', encoding='utf-8') as f:
                    res["resource_content"] = f.read()
            except Exception as e:
                res["resource_content"] = ""
        if resource_view.resource_format == "json":
            view_config["engine"] = "json"
            try:
                view_config["data"] = json.loads(res["resource_content"])
            except Exception as e:
                view_config["data"] = {}
        elif resource_view.resource_format == 'html':
            view_config["engine"] = "webpage"
        else:
            view_config["engine"] = "markdown"
    elif resource_view.resource_type == 'document':
        if resource_view.resource_format == 'txt':
            if os.path.exists(resource_view.resource_path):
                with open(resource_view.resource_path, 'r', encoding='utf-8') as f:
                    res["resource_content"] = f.read()
                    view_config["engine"] = "text"
        elif resource_view.resource_format == "pdf":
            # 尝试作为文档返回
            view_config["engine"] = "embed-pdf"
            res["resource_show_url"] = resource_view.resource_show_url
        elif resource_view.resource_format in ("docx", "doc", "pptx", "ppt"):
            view_config["engine"] = "embed-pdf"
            # 尝试转换为PDF
            res["resource_show_url"] = get_resource_pdf_view_url(resource_view)
        elif resource_view.resource_format in ("xlsx", "xls"):
            view_config["engine"] = "excel"
            # 尝试转换为PDF
            res["resource_show_url"] = get_resource_html_view_url(resource_view)
    # 尝试作为文本返回
    else:
        try:
            if os.path.exists(resource_view.resource_path):
                with open(resource_view.resource_path, 'r', encoding='utf-8') as f:
                    res["resource_content"] = f.read()
                    view_config["engine"] = "text"
        except Exception as e:
            app.logger.warning(e)
            view_config["support"] = False
    # 补充查看配置
    res["view_config"] = view_config
    return next_console_response(result=res)


def wps_get_file_meta(params):
    """
    获取资源视图元数据
    :param params:
    :return:
    """
    file_id = params.get("file_id")
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常",
    ).first()
    if not target_resource:
        app.logger.warning(f'资源不存在，：{file_id}：{user_id}')
        return next_console_response(error_status=True, error_message="资源不存在！")
    # 检查资源权限
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "read"
    }):
        return next_console_response(error_status=True, error_message="无权限查看资源！")
    res = {
        "code": 0,
        "data": {
            'id': str(target_resource.id),
            'name': target_resource.resource_name,
            'size': int(target_resource.resource_size_in_MB * 1024 * 1024),
            'version': target_resource.resource_version,
            "create_time": int(target_resource.create_time.timestamp()),
            "modify_time": int(target_resource.update_time.timestamp()),
            "creator_id": str(target_resource.user_id),
            "modifier_id": str(target_user.user_id),
        }
    }
    return res


def wps_get_file_download(params):
    """
    获取资源视图元数据
    :param params:
    :return:
    """
    file_id = params.get("file_id")
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")

    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")

    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "read"
    }):
        return next_console_response(error_status=True, error_message="无权限查看资源！")
    if not target_resource.resource_download_url and os.path.exists(target_resource.resource_path):
        # 生成下载链接
        resource_download_url = generate_download_url(
            'resource_center', target_resource.resource_path, suffix=target_resource.resource_format
        ).json.get("result")
        if not resource_download_url:
            return next_console_response(
                error_status=True, error_message="生成下载链接异常！"
            )
        target_resource.resource_download_url = resource_download_url
        db.session.add(target_resource)
        db.session.commit()
    res = {
        "code": 0,
        "data": {
            'url': target_resource.resource_download_url,
        }
    }
    return res


def wps_get_file_permission(params):
    """
    获取资源视图元数据
    :param params:
    :return:
    """
    file_id = params.get("file_id")
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    all_access = get_user_access_to_resource({
        "user": target_user,
        "resource": target_resource
    })
    res = {
        "code": 0,
        "data": {
            "read": 0,
            "history": 0,
            "copy": 0,
            "download": 0,
            "print": 0,
            "update": 0,
            "rename": 0,
            "comment": 0,
            "user_id": str(target_resource.user_id),
          }
        }
    if "阅读" in all_access:
        res["data"]["read"] = 1
        res["data"]["history"] = 1
    if "下载" in all_access:
        res["data"]["read"] = 1
        res["data"]["history"] = 1
        res["data"]["copy"] = 1
        res["data"]["download"] = 1
        res["data"]["print"] = 1
    if "编辑" in all_access or "管理" in all_access:
        res["data"]["read"] = 1
        res["data"]["history"] = 1
        res["data"]["copy"] = 1
        res["data"]["download"] = 1
        res["data"]["print"] = 1
        res["data"]["update"] = 1
        res["data"]["rename"] = 1
        res["data"]["comment"] = 1
    return res


def wps_get_file_users(params):
    """
    wps获取用户信息
    :param params:
    :return:
    """
    user_ids = params.get('user_ids', [])
    all_user_info = UserInfo.query.filter(
        UserInfo.user_id.in_(user_ids),
        UserInfo.user_status == 1
    ).all()
    res = {
        "code": 0,
        "data": [

        ]
    }
    for user in all_user_info:
        res.get("data").append({
            "id": str(user.user_id),
            "name": user.user_nick_name,
            "avatar_url": user.user_avatar
        })
    app.logger.warning(f"返回用户信息：{res}")
    return json.dumps(res)


def wps_upload_address(params):
    """
    wps上传地址
    :param params:
    :return:
    """
    file_id = params.get("file_id")
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "edit"
    }):
        return next_console_response(error_status=True, error_message="无权限编辑资源！")
    # 保存文件至指定目录
    new_resource_path = generate_new_path(
      module_name="resource_center",
      user_id=target_resource.user_id,
    ).json.get("result")
    res = {
        "code": 0,
        "data": {
            "method": "PUT",
            "url": app.config.get("domain") + "/next_console/resources_view/WPS/v3/3rd/files/{}/upload".format(file_id),
            "params": {
                "resource_path": new_resource_path,
                "user_id": user_id,
            },
            "send_back_params": {
                "resource_path": new_resource_path,
                "user_id": user_id,
            },
        },
        "message": ""
    }
    app.logger.warning(f'wps-address,返回结果,f{res}')
    return res


def wps_upload_file(params):
    """
    wps上传文件
    :param params:
    :return:
    """
    file_id = params.get("file_id")
    file_data = params.get("file_data")
    new_resource_path = params.get("resource_path")
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not target_user:
        app.logger.warning(f'wps-upload,用户不存在:{user_id}')
        return next_console_response(error_status=True, error_message="资源不存在！")

    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        app.logger.warning(f'wps-upload,资源不存在:{file_id}')
        return next_console_response(error_status=True, error_message="资源不存在！")
    if not file_data:
        app.logger.warning(f'wps-upload,文件数据为空')
        return next_console_response(error_status=True, error_message="文件数据为空！")
    with open(new_resource_path, 'wb') as f:
        f.write(file_data)
    app.logger.warning(f'wps-upload,写入成功：{new_resource_path}')
    return {
        "resource_path": new_resource_path,

    }


def wps_upload_complete(params):
    """
    wps上传完成
    :param params:
    :return:
    """
    app.logger.warning(f"上传完成：{params}")
    file_id = params.get("file_id")
    user_id = int(params.get("user_id"))
    resource_path = params.get("send_back_params").get("resource_path")
    digest = params.get("request").get("digest").get("sha256")
    size = params.get("request").get("size")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    # 保存当前资源记录
    new_resource_history = ResourceObjectHistory(
        resource_id=target_resource.id,
        resource_name=target_resource.resource_name,
        resource_path=target_resource.resource_path,
        resource_size_in_MB=target_resource.resource_size_in_MB,
        resource_feature_code=target_resource.resource_feature_code,
        resource_format=target_resource.resource_format,
        resource_type=target_resource.resource_type,
        resource_parent_id=target_resource.resource_parent_id,
        resource_status=target_resource.resource_status,
        resource_download_url=target_resource.resource_download_url,
        resource_show_url=target_resource.resource_show_url,
        user_id=target_resource.user_id,
        modifier_id=user_id,
        resource_version=target_resource.resource_version,
        resource_title=target_resource.resource_title,
        resource_desc=target_resource.resource_desc,
        resource_icon=target_resource.resource_icon,
        resource_source=target_resource.resource_source,
        resource_source_url=target_resource.resource_source_url,
        resource_source_url_site=target_resource.resource_source_url_site,
        resource_is_share=target_resource.resource_is_share,
        resource_is_public=target_resource.resource_is_public,
        resource_public_access=target_resource.resource_public_access,
        resource_language=target_resource.resource_language,
        create_time=target_resource.create_time,
        update_time=datetime.now()
    )
    db.session.add(new_resource_history)
    db.session.commit()
    # 更新资源信息
    target_resource.resource_version += 1
    target_resource.resource_path = resource_path
    target_resource.resource_size_in_MB = size / 1024 / 1024
    target_resource.resource_feature_code = digest
    # 更新下载链接
    old_download_link_path = get_download_url_path(target_resource.resource_download_url)
    try:
        os.remove(old_download_link_path)
    except Exception as e:
        app.logger.warning(f"删除旧下载链接失败：{old_download_link_path}，{e}")
    target_download_link = generate_download_url(
        'resource_center', resource_path, suffix=target_resource.resource_format
                                                 ).json.get("result")
    target_resource.resource_download_url = target_download_link
    db.session.add(target_resource)
    db.session.commit()
    return {
      "code": 0,
      "data": {
        "create_time": int(target_resource.create_time.timestamp()),
        "creator_id": str(target_resource.user_id),
        "id":  str(target_resource.id),
        "modifier_id":  str(user_id),
        "modify_time": int(target_resource.update_time.timestamp()),
        "name": target_resource.resource_name,
        "size": size,
        "version": target_resource.resource_version
      }
    }


def wps_rename(params):
    """

    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    file_id = params.get("file_id")
    name = params.get("name")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "edit"
    }):
        return next_console_response(error_status=True, error_message="无权限编辑资源！")
    target_resource.resource_name = name
    db.session.add(target_resource)
    db.session.commit()
    # websocket 推送至前端
    send_wps_rename({
        "user_id": user_id,
        "data": target_resource.show_info()
    })
    return {
      "code": 0,
      "data": {}
    }


def wps_get_version_list(params):
    """
    获取 wps历史版本
    :param params:
    :return:
    """

    file_id = params.get("file_id")
    user_id = int(params.get("user_id"))
    offset = params.get("offset", 0)
    limit = params.get("limit", 20)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        app.logger.warning(f"获取 wps历史版本:用户不存在,{user_id}")
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        app.logger.warning(f"获取 wps历史版本:资源不存在,{file_id}")
        return next_console_response(error_status=True, error_message="资源不存在！")
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "read"
    }):
        app.logger.warning(f"获取 wps历史版本:无权限查看资源,{file_id},{user_id}")
        return next_console_response(error_status=True, error_message="无权限查看资源！")
    all_resource_history = ResourceObjectHistory.query.filter(
        ResourceObjectHistory.resource_id == file_id,
    ).order_by(
        ResourceObjectHistory.resource_version.desc()
    ).offset(offset).limit(limit)
    all_data = []
    for resource_history in all_resource_history:
        all_data.append(
            {
                "id": str(file_id),
                "name": resource_history.resource_name,
                "version": resource_history.resource_version,
                "size": int(resource_history.resource_size_in_MB * 1024 * 1024),
                "create_time": int(resource_history.create_time.timestamp()),
                "modify_time": int(resource_history.update_time.timestamp()),
                "creator_id": str(resource_history.user_id),
                "modifier_id": str(resource_history.modifier_id),
            }
        )
    return {
        "code": 0,
        "data": all_data,
        "message": ""
    }


def get_history_version_meta(params):
    file_id = params.get("file_id")
    version = params.get('version')
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        app.logger.warning(f"获取 wps历史版本:用户不存在,{user_id}")
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        app.logger.warning(f"获取 wps历史版本:资源不存在,{file_id}")
        return next_console_response(error_status=True, error_message="资源不存在！")
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "read"
    }):
        app.logger.warning(f"获取 wps历史版本:无权限查看资源,{file_id},{user_id}")
        return next_console_response(error_status=True, error_message="无权限查看资源！")
    target_resource_history = ResourceObjectHistory.query.filter(
        ResourceObjectHistory.resource_id == file_id,
        ResourceObjectHistory.resource_version == version,

    ).first()
    if not target_resource_history:
        app.logger.warning(f"获取 wps历史版本:版本异常,{file_id},{user_id}，{version}")
        return next_console_response(error_status=True, error_message="无权限查看资源！")

    res = {
      "code": 0,
      "message": "",
      "data": {
        "create_time": int(target_resource_history.create_time.timestamp()),
        "creator_id": str(target_resource_history.user_id),
        "id": file_id,
        "modifier_id": str(target_resource_history.modifier_id),
        "modify_time": int(target_resource_history.update_time.timestamp()),
        "name": target_resource_history.resource_name,
        "size": int(target_resource_history.resource_size_in_MB*1024*1024),
        "version": target_resource_history.resource_version
      }
    }
    return res


def get_history_version_download(params):
    """获取历史版本下载信息"""
    file_id = params.get("file_id")
    version = params.get('version')
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        app.logger.warning(f"获取 wps历史版本:用户不存在,{user_id}")
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == file_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        app.logger.warning(f"获取 wps历史版本:资源不存在,{file_id}")
        return next_console_response(error_status=True, error_message="资源不存在！")
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "read"
    }):
        app.logger.warning(f"获取 wps历史版本:无权限查看资源,{file_id},{user_id}")
        return next_console_response(error_status=True, error_message="无权限查看资源！")
    target_resource_history = ResourceObjectHistory.query.filter(
        ResourceObjectHistory.resource_id == file_id,
        ResourceObjectHistory.resource_version == version,
    ).first()
    if not target_resource_history:
        app.logger.warning(f"获取 wps历史版本:版本异常,{file_id},{user_id}，{version}")
        return next_console_response(error_status=True, error_message="无权限查看资源！")

    if not target_resource_history.resource_download_url and os.path.exists(target_resource_history.resource_path):
        target_resource_history.resource_download_url = generate_download_url(
            "resource_center", target_resource_history.resource_path,
            suffix=target_resource_history.resource_format
        )
        db.session.add(target_resource_history)
        db.session.add(target_resource_history)
    return {
      "code": 0,
      "message": "",
      "data": {
        "url": target_resource_history.resource_download_url
        }
    }


def put_new_attachment_for_wps(params):
    """
    上传附件
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    key = params.get("key")
    name = params.get("name")
    file_data = params.get("file_data")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")

    target_attachment = ResourceAttachment.query.filter(
        ResourceAttachment.attachment_key == key,
        ResourceAttachment.attachment_name == name,
        ResourceAttachment.attachment_status == "正常"
    ).first()
    if target_attachment:
        try:
            with open(target_attachment.attachment_path, 'wb') as f:
                f.write(file_data)
                return {
                  "code": 0,
                  "data": {}
                }
        except Exception as e:
            app.logger.error(f"上传附件异常：{e.args}")
            return next_console_response(error_status=True, error_message="上传附件异常！")
    # 保存附件至指定目录
    new_attachment_path = generate_new_path(
        module_name="resource_center",
        user_id=user_id
    ).json.get("result")

    with open(new_attachment_path, 'wb') as f:
        f.write(file_data)

    # 生成下载链接
    attachment_url = generate_download_url('resource_center', new_attachment_path)
    # 在下载目录下生成软链接
    # target_download_link = os.path.join(app.config["download_dir"], attachment_url)
    # if not os.path.exists(target_download_link):
    #     try:
    #         os.symlink(new_attachment_path, target_download_link)
    #     except Exception as e:
    #         app.logger.error(f"生成下载链接异常：{e.args}")
    #         return next_console_response(error_status=True, error_message=f"生成下载链接异常：{e.args}")
    new_attachment = ResourceAttachment(
        user_id=user_id,
        attachment_key=key,
        attachment_name=name,
        attachment_path=new_attachment_path,
        attachment_size=len(file_data),
        attachment_url=attachment_url
    )
    db.session.add(new_attachment)
    db.session.commit()
    return {
      "code": 0,
      "data": {}
    }


def get_attachment_url(params):
    """
    获取附件下载链接
    :param params:
    :return:
    """
    key = params.get("key")
    user_id = int(params.get("user_id"))
    scale_max_fit_width = params.get("scale_max_fit_width")
    scale_max_fit_height = params.get("scale_max_fit_height")
    scale_long_edge = params.get("scale_long_edge")

    target_attachment = ResourceAttachment.query.filter(
        ResourceAttachment.attachment_key == key,
        ResourceAttachment.attachment_status == "正常"
    ).first()
    if not target_attachment:
        return next_console_response(error_status=True, error_message="附件不存在！")
    # url = "{}/downloads/{}".format(app.config.get("domain"), target_attachment.attachment_url)
    # app.logger.warning(f"附件下载链接：{url}")
    return {
        "code": 0,
        "data": {
            "url": target_attachment.attachment_url
        }
        }


def copy_attachment(params):
    """
    复制附件
    :param params:
    :return:
    """
    key_dict = params.get("key_dict")
    user_id = int(params.get("user_id"))

    for key in key_dict:
        source_attachment = ResourceAttachment.query.filter(
            ResourceAttachment.attachment_key == key,
            ResourceAttachment.attachment_status == "正常"
        ).first()
        if not source_attachment:
            continue
        target_attachment = ResourceAttachment(
            user_id=user_id,
            attachment_key=key_dict[key],
            attachment_name=source_attachment.attachment_name,
            attachment_path=source_attachment.attachment_path,
            attachment_size=source_attachment.attachment_size,
            attachment_url=source_attachment.attachment_url
        )
        db.session.add(target_attachment)
    db.session.commit()
    return {
      "code": 0,
      "data": {}
    }


def get_resource_pdf_view_url(resource):
    """
    获取资源的PDF预览链接
        基于liboffice转换为PDF
    """
    pdf_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.resource_parent_id == resource.id,
        ResourceObjectMeta.resource_format == "pdf",
        ResourceObjectMeta.resource_size_in_MB > 0
    ).order_by(
        ResourceObjectMeta.id.desc()
    ).first()
    if pdf_resource:
        return pdf_resource.resource_show_url
    # 检查liboffice 是否安装
    import subprocess
    try:
        subprocess.run(["soffice", "--version"], check=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except Exception:
        app.logger.error("LibreOffice is not installed or not found in PATH.")
        return None
    # 使用liboffice转换为PDF
    output_dir = os.path.dirname(resource.resource_path)
    try:
        subprocess.run([
            "soffice", "--headless", "--convert-to", "pdf",
            resource.resource_path, "--outdir", output_dir

        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        error_msg = f"""
                LibreOffice转换失败！
                命令: {e.cmd}
                错误代码: {e.returncode}
                标准输出: {e.stdout}
                错误输出: {e.stderr}
                """
        app.logger.error(error_msg)
        return None
    input_filename = os.path.basename(resource.resource_path)
    default_pdf = os.path.join(output_dir, os.path.splitext(input_filename)[0] + ".pdf")
    pdf_path = resource.resource_path + ".pdf"
    if not os.path.exists(default_pdf):
        return None
    os.rename(default_pdf, pdf_path)
    if os.path.exists(pdf_path):
        pdf_url = generate_download_url(
            "resource_center", pdf_path, suffix="pdf"
        ).json.get("result")
        if not pdf_url:
            app.logger.error("Failed to generate PDF download URL.")
            return None
        new_pdf_resource = ResourceObjectMeta(
            resource_parent_id=resource.id,
            user_id=resource.user_id,
            resource_name=resource.resource_name,
            resource_type=resource.resource_type,
            resource_title=resource.resource_title,
            resource_desc=resource.resource_desc,
            resource_icon="pdf.svg",
            resource_format="pdf",
            resource_size_in_MB=os.path.getsize(pdf_path)/1024/1024,
            resource_path= pdf_path,
            resource_source="resource_center",
            resource_show_url=pdf_url,
            resource_download_url=pdf_url,
            resource_feature_code=resource.resource_feature_code,
        )
        db.session.add(new_pdf_resource)
        db.session.commit()
        return pdf_url
    return None


def get_resource_html_view_url(resource):
    """
    获取资源的HTML预览链接
    """
    html_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.resource_parent_id == resource.id,
        ResourceObjectMeta.resource_format == "html",
        ResourceObjectMeta.resource_size_in_MB > 0
    ).order_by(
        ResourceObjectMeta.id.desc()
    ).first()
    if html_resource:
        if not html_resource.resource_show_url and os.path.exists(html_resource.resource_path):
            html_resource.resource_show_url = generate_download_url(
                "resource_center", html_resource.resource_path, suffix="html"
            ).json.get("result")
            db.session.add(html_resource)
            db.session.commit()
        return html_resource.resource_show_url
    # 检查liboffice 是否安装
    import subprocess
    try:
        subprocess.run(["soffice", "--version"], check=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except Exception as e:
        app.logger.error("LibreOffice is not installed or not found in PATH.")
        return None
    # 使用liboffice转换为HTML
    output_dir = os.path.join(os.path.dirname(resource.resource_path), "html")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        # 清理旧的HTML文件
        for file in os.listdir(output_dir):
            if file.endswith(".html"):
                os.remove(os.path.join(output_dir, file))
    try:
        subprocess.run([
            "soffice", "--headless", "--convert-to", "html",
            resource.resource_path, "--outdir", output_dir
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        error_msg = f"""
                LibreOffice转换失败！
                命令: {e.cmd}
                错误代码: {e.returncode}
                标准输出: {e.stdout}
                错误输出: {e.stderr}
                """
        app.logger.error(error_msg)
        return None
    input_filename = os.path.basename(resource.resource_path)
    html_path = os.path.join(output_dir, os.path.splitext(input_filename)[0] + ".html")
    if not os.path.exists(html_path):
        app.logger.error(f"HTML file not found after conversion: {html_path}")
        return None
    html_url = generate_download_url(
        "resource_center", html_path, suffix="html"
    ).json.get("result")
    if not html_url:
        app.logger.error("Failed to generate HTML download URL.")
        return None
    new_html_resource = ResourceObjectMeta(
        resource_parent_id=resource.id,
        user_id=resource.user_id,
        resource_name=resource.resource_name,
        resource_type=resource.resource_type,
        resource_title=resource.resource_title,
        resource_desc=resource.resource_desc,
        resource_icon="html.svg",
        resource_format="html",
        resource_size_in_MB=os.path.getsize(html_path)/1024/1024,
        resource_path=html_path,
        resource_source="resource_center",
        resource_show_url=html_url,
        resource_download_url=html_url,
        resource_feature_code=resource.resource_feature_code,
    )
    db.session.add(new_html_resource)
    db.session.flush()
    resource_parent_id = new_html_resource.id
    db.session.commit()
    # 保存附件资源
    media_list = os.listdir(output_dir)
    media_name_map = {}
    for media_name in media_list:
        new_media_path = os.path.join(output_dir, media_name)
        resource_show_url = generate_download_url(
                "resource_center", new_media_path, suffix=media_name.split('.')[-1]
            ).json.get("result")
        resource_format = media_name.split('.')[-1]
        new_media_resource = ResourceObjectMeta(
            resource_parent_id=resource_parent_id,
            user_id=resource.user_id,
            resource_name=media_name,
            resource_type="media",
            resource_title=media_name,
            resource_desc="",
            resource_icon=f"{resource_format}.svg",
            resource_format=resource_format,
            resource_size_in_MB=os.path.getsize(new_media_path)/1024/1024,
            resource_path=new_media_path,
            resource_source="resource_center",
            resource_show_url=resource_show_url,
            resource_download_url=resource_show_url,
            resource_feature_code=resource.resource_feature_code,
        )
        db.session.add(new_media_resource)
        media_name_map[media_name] = resource_show_url
    db.session.commit()
    # 替换HTML中的资源链接
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    for media_name in media_list:
        media_url = media_name_map.get(media_name)
        if media_url:
            html_content = html_content.replace(media_name, media_url)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return html_url

