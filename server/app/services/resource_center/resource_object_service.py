import hashlib
import mimetypes
import os
import time
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import or_, distinct

from app.app import app
from app.services.configure_center.user_config import get_user_config
from app.models.knowledge_center.rag_ref_model import *
from app.models.resource_center.resource_model import *
from app.models.resource_center.share_resource_model import ResourceDownloadCoolingRecord
from app.models.user_center.user_info import UserInfo
from app.services.configure_center.response_utils import next_console_response
from app.services.knowledge_center.rag_service_v3 import rag_query_v3
from app.services.resource_center.resource_share_service import check_user_manage_access_to_resource
from app.services.resource_center.resource_share_service import search_share_resource_by_keyword
from app.services.task_center.resources_center import auto_build_resource_ref_v2
from app.services.task_center.resources_center import send_resource_download_cooling_notice_email
from app.utils.oss.oss_client import generate_new_path, generate_download_url


def search_resource_object(params):
    """
    搜索资源对象,不传入参数则返回根目录
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_parent_id = params.get("resource_parent_id")
    resource_name = params.get("resource_name")
    resource_desc = params.get("resource_desc")
    resource_type = params.get("resource_type", [])
    resource_list = params.get("resource_list", [])
    resource_format = params.get("resource_format", [])
    resource_source = params.get("resource_source", ["resource_center"])
    resource_status = params.get("resource_status", "正常")
    is_global = params.get("is_global", False)
    has_root = params.get("has_root", False)
    show_dir = params.get("show_dir", False)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_filter = [
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == resource_status,
        ResourceObjectMeta.resource_parent_id.isnot(None),
    ]
    root_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
    ).first()

    if not root_resource:
        return next_console_response(error_status=True, error_message="根目录不存在！")
    if resource_parent_id is not None:
        all_filter.append(ResourceObjectMeta.resource_parent_id == resource_parent_id)
    elif is_global is False:
        all_filter.append(ResourceObjectMeta.resource_parent_id == root_resource.id)
    if resource_name:
        all_filter.append(
            or_(
                ResourceObjectMeta.resource_name.like(f"%{resource_name}%"),
                ResourceObjectMeta.resource_desc.like(f"%{resource_name}%")
            )
        )
    if resource_desc:
        or_(
            ResourceObjectMeta.resource_name.like(f"%{resource_name}%"),
            ResourceObjectMeta.resource_desc.like(f"%{resource_name}%")
        )
    if resource_type:
        if "recent" in resource_type:
            recent_end_time = datetime.now(timezone.utc) - timedelta(days=7)
            all_filter.append(
                ResourceObjectMeta.update_time > recent_end_time
            )
        elif "rag" in resource_type:
            pass
        else:
            all_filter.append(ResourceObjectMeta.resource_type.in_(resource_type))
    if resource_format:
        all_filter.append(ResourceObjectMeta.resource_format.in_(resource_format))
    if resource_source:
        all_filter.append(ResourceObjectMeta.resource_source.in_(resource_source))
    if resource_list:
        all_filter.append(ResourceObjectMeta.id.in_(resource_list))
    sub_resource_list = ResourceObjectMeta.query.filter(
        *all_filter
    ).order_by(
        ResourceObjectMeta.resource_type.asc(),
        ResourceObjectMeta.resource_name.asc(),
    ).all()
    total = len(sub_resource_list)
    data = [sub_resource_item.show_info() for sub_resource_item in sub_resource_list]
    if resource_parent_id is None and has_root:
        data = [root_resource.show_info()]
    if show_dir:
        # 展示父目录信息
        parent_ids = [resource_item.get("resource_parent_id") for resource_item in data]
        parent_ids = list(set(parent_ids))
        all_parent_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id.in_(parent_ids),
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.user_id == user_id
        ).all()
        all_parent_resource_dict = {resource_item.id: resource_item.show_info()
                                    for resource_item in all_parent_resource}
        for resource_item in data:
            if resource_item.get("resource_parent_id") in all_parent_resource_dict:
                resource_item["resource_parent_name"] = all_parent_resource_dict.get(
                    resource_item.get("resource_parent_id")
                ).get("resource_name")
    # 返回资源ref状态
    all_resource_ids = [resource_item.get("id") for resource_item in data]
    all_resource_ref = RagRefInfo.query.filter(
        RagRefInfo.resource_id.in_(all_resource_ids)
    ).all()
    resource_ref_dict = {}
    for resource_ref in all_resource_ref:
        if resource_ref.resource_id not in resource_ref_dict:
            resource_ref_dict[resource_ref.resource_id] = resource_ref
        if resource_ref.id > resource_ref_dict[resource_ref.resource_id].id:
            resource_ref_dict[resource_ref.resource_id] = resource_ref
    for resource_item in data:
        if resource_ref_dict.get(resource_item.get("id")):
            resource_item["rag_status"] = resource_ref_dict.get(resource_item.get("id")).ref_status
    if "rag" in resource_type:
        # 过滤掉非rag资源
        data = [resource_item for resource_item in data if resource_item.get("rag_status") == "成功"]
        total = len(data)
    # 启用手动分页
    # 获取参数并进行异常处理
    try:
        page_size = int(params.get("page_size", 50))
        page_num = int(params.get("page_num", 1))
    except ValueError:
        page_size = 50
        page_num = 1
    # 计算分页数据
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size

    # 检查索引是否超出列表范围
    if start_index >= len(data):
        paged_data = []
    else:
        paged_data = data[start_index:end_index]
    return next_console_response(result={
        "total": total,
        "data": paged_data,
        "root": root_resource.show_info()
    })


def get_resource_object_path(params):
    """
    获取资源对象路径
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_id = params.get("resource_id")
    resource_status = params.get("resource_status", "正常")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
        ResourceObjectMeta.resource_status == resource_status,
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    # 检查资源权限
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "read"
    }):
        return next_console_response(error_status=True, error_message="无权限查看资源！")
    resource_path = [target_resource.show_info()]
    share_flag = False
    if target_resource.user_id != user_id:
        share_flag = True
    while target_resource:
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == target_resource.resource_parent_id,
            ResourceObjectMeta.resource_status == resource_status
        ).first()
        if target_resource and check_user_manage_access_to_resource({
            "user": target_user,
            "resource": target_resource,
            "access_type": "read"
        }):
            resource_path.insert(0, target_resource.show_info())
        else:
            break
    if share_flag:
        resource_path.insert(0, {
            "resource_icon": "folder.svg",
            "resource_name": "共享资源",
            "resource_type": 'folder'
        })
    result = {
        "total": len(resource_path),
        "data": resource_path
    }
    return next_console_response(result=result)


def get_resource_object(params):
    """
    获取资源对象元信息，不传入参数则返回根目录
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_id = params.get("resource_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")

    if not resource_id:
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_parent_id.is_(None)
        ).first()
        if not target_resource:
            if not target_user.user_resource_base_path:
                target_user.user_resource_base_path = generate_new_path(
                    "resource_center",
                    user_id=target_user.user_id,
                    file_type="dir"
                ).json.get("result")
                db.session.add(target_user)
                db.session.commit()
            # 重新初始化用户基础资源目录
            target_resource = ResourceObjectMeta(
                user_id=user_id,
                resource_name="我的资源",
                resource_type="folder",
                resource_desc="用户资源库",
                resource_icon="folder.svg",
                resource_path=target_user.user_resource_base_path,
                resource_status="正常"
            )
            db.session.add(target_resource)
            db.session.commit()
    else:
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == int(resource_id),
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == "正常"
        ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")

    result = target_resource.show_info()
    # 如果是folder，增加资源大小与子资源数量统计
    if target_resource.resource_type == "folder":
        all_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_source == "resource_center",
        ).all()
        all_sub_resource_ids = [target_resource.id]
        add_cnt = 1
        while add_cnt > 0:
            add_cnt = 0
            for resource_item in all_resources:
                if (resource_item.resource_parent_id in all_sub_resource_ids
                        and resource_item.id not in all_sub_resource_ids):
                    all_sub_resource_ids.append(resource_item.id)
                    add_cnt += 1
        sub_resource_list = [resource_item for resource_item in all_resources
                             if resource_item.id in all_sub_resource_ids]
        sub_dir = [resource_item for resource_item in sub_resource_list
                   if resource_item.resource_type == "folder"]
        all_size = sum([resource_item.resource_size_in_MB for resource_item in sub_resource_list])
        result["resource_size_in_MB"] = all_size
        result["sub_resource_dir_cnt"] = len(sub_dir)
        result["sub_resource_file_cnt"] = len(sub_resource_list) - len(sub_dir)
        # rag资源数量
        all_rag_ref_info = RagRefInfo.query.filter(
            RagRefInfo.resource_id.in_(all_sub_resource_ids),
            RagRefInfo.ref_status == "成功"
        ).all()
        result["sub_rag_file_cnt"] = len(all_rag_ref_info)
    # 新增路径信息
    try:
        resource_path_res = get_resource_object_path({
            "user_id": user_id,
            "resource_id": target_resource.id
        }).json
        resource_path = resource_path_res.get("result").get("data")
        if not resource_path:
            return next_console_response(result=[])
        resource_path = [resource_item.get("resource_name") for resource_item in resource_path]
    except Exception as e:
        app.logger.warning(f"获取资源路径异常：{e.args}")
        resource_path = []
    result["resource_path"] = "/".join(resource_path)
    # 返回资源ref状态
    if resource_id:
        rag_ref = RagRefInfo.query.filter(
            RagRefInfo.resource_id == resource_id
        ).order_by(
            RagRefInfo.create_time.desc()
        ).first()
        if not rag_ref:
            result["rag_status"] = "未构建"
        else:
            result["rag_status"] = rag_ref.ref_status
        # 新增Tag信息
        all_tags = ResourceTagRelation.query.filter(
            ResourceTagRelation.resource_id == resource_id,
            ResourceTagRelation.rel_status == "正常"
        ).join(
            ResourceTag,
            ResourceTagRelation.tag_id == ResourceTag.id
        ).with_entities(
            ResourceTag
        ).all()
        result["resource_tags"] = [tag.show_info() for tag in all_tags]
    return next_console_response(result=result)


def add_resource_upload_task(params):
    """
    添加资源上传任务
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_parent_id = params.get("resource_parent_id")
    resource_name = params.get("resource_name")
    resource_size_in_MB = params.get("resource_size")
    content_max_idx = params.get("content_max_idx")
    resource_md5 = params.get("resource_md5")
    task_source = params.get("task_source", "resource_center")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    if resource_parent_id:
        if task_source == "session":
            target_resource = ResourceObjectMeta.query.filter(
                ResourceObjectMeta.id == resource_parent_id,
                ResourceObjectMeta.user_id == user_id,
                ResourceObjectMeta.resource_source == "session",
                ResourceObjectMeta.resource_status == "正常"
            ).first()
            if not target_resource:
                return next_console_response(error_status=True, error_message="目录不存在！")
        else:
            target_resource = ResourceObjectMeta.query.filter(
                ResourceObjectMeta.id == resource_parent_id,
                ResourceObjectMeta.user_id == user_id,
                ResourceObjectMeta.resource_status == "正常"
            ).first()
            if not target_resource:
                return next_console_response(error_status=True, error_message="目录不存在！")
    else:
        root_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_parent_id.is_(None)
        ).first()
        if not root_resource:
            # 初始化根目录
            root_resource = ResourceObjectMeta(
                user_id=user_id,
                resource_name="我的资源",
                resource_type="folder",
                resource_desc="用户资源库",
                resource_icon="folder.svg",
                resource_path=target_user.user_resource_base_path,
                resource_status="正常"
            )
            db.session.add(root_resource)
            db.session.commit()
        resource_parent_id = root_resource.id
    # 检查资源使用情况
    all_resources_usage = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常"
    ).all()
    all_resource_size = sum([resource_item.resource_size_in_MB for resource_item in all_resources_usage])
    if all_resource_size >= target_user.user_resource_limit:
        return next_console_response(error_status=True, error_message="资源空间已满！")
    if all_resource_size + resource_size_in_MB >= target_user.user_resource_limit:
        return next_console_response(error_status=True, error_message="资源空间不足！")
    content_prefix = uuid.uuid4().hex
    # 猜测文件类型
    resource_type, resource_format = guess_resource_type(resource_name)
    task_icon = set_task_icon(resource_type, resource_format)
    # 自动修改文件名
    same_dir_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_parent_id == resource_parent_id,
        ResourceObjectMeta.resource_status == "正常",
    ).all()
    all_resource_names = {resource_item.resource_name for resource_item in same_dir_resources}
    base, ext = os.path.splitext(resource_name)
    ext = ext.lower()  # 确保扩展名是小写
    reindex = 1
    while resource_name in all_resource_names:
        # 如果已经是重命名过的文件，则再原有基础上增加
        resource_name = f"{base}({reindex}){ext}"
        reindex += 1
    new_resource = ResourceObjectUpload(
        user_id=user_id,
        resource_parent_id=resource_parent_id,
        resource_name=resource_name,
        resource_size_in_mb=resource_size_in_MB,
        resource_type=resource_type,
        resource_format=resource_format,
        content_max_idx=content_max_idx,
        content_prefix=f"{user_id}_{content_prefix}",
        resource_md5=resource_md5,
        task_icon=task_icon,
        task_source=task_source
    )
    try:
        db.session.add(new_resource)
        db.session.commit()
    except Exception as e:
        return next_console_response(error_status=True, error_message=f"新增任务异常：{e.args}")
    return next_console_response(result=new_resource.show_info())


def guess_resource_type(resource_name):
    """
    猜测资源类型
        resource_type in (document, image, video, audio, code, webpage, archive, binary, other)
        code, image, audio, video, webpage, archive, binary, other, document
    :param resource_name:
    :return:
    """
    if "." in resource_name:
        resource_format = resource_name.split(".")[-1].lower()
    else:
        resource_format = ""
    resource_type, _ = mimetypes.guess_type(resource_name)
    # 根据情况判断类型
    # code
    code_format_map = {
        "css": "css.svg", "js": "js.svg", "json": "json.svg", "xml": "xml.svg",
        "java": "java.svg", "cpp": "cpp.svg", "c": "c.svg", "py": "py.svg", "php": "php.svg",
        "go": "go.svg", "h": "h.svg", "hpp": "hpp.svg", "rb": "rb.svg", "cs": "cs.svg",
        "sh": "sh.svg", "bat": "bat.svg", "swift": "swift.svg", "kt": "kt.svg", "ts": "ts.svg",
        "pl": "pl.svg", "lua": "lua.svg", "r": "r.svg", "scala": "scala.svg", "sql": "sql.svg",
        "vb": "vb.svg", "vbs": "vbs.svg", "yaml": "yaml.svg", "yml": "yml.svg", "md": "md.svg",
        "ps1": "ps1.svg", "ini": "ini.svg", "conf": "conf.svg", "properties": "properties.svg",
        "cmd": "cmd.svg", "vue": "vue.svg", "jsx": "jsx.svg", "perl": "perl.svg",
        "db2": "db2.svg", "rs": "rs.svg", "mm": "mm.svg", "m": "m.svg", "plsql": "plsql.svg",
        "hs": "hs.svg", "hsc": "hsc.svg", "Dockerfile": "Dockerfile.svg", "dart": "dart.svg",
        "pm": "pm.svg", "bash": "bash.svg", "svelte": "svelte.svg",
    }
    image_format_map = {
        "jpeg": "jpeg.svg", "jpg": "jpg.svg",
        "png": "png.svg", "gif": "gif.svg", "bmp": "bmp.svg",
        "webp": "webp.svg", "svg": "svg.svg",
    }
    video_format_map = {
        "mp4": "mp4.svg", "avi": "avi.svg", "mkv": "mkv.svg", "flv": "flv.svg", "mov": "mov.svg",
        "wmv": "wmv.svg", "webm": "webm.svg", "mpg": "mpg.svg", "3gp": "3gp.svg", "mpeg": "mpeg.svg",
    }
    audio_format_map = {
        "mp3": "mp3.svg", "wav": "wav.svg", "wma": "wma.svg", "flac": "flac.svg",
        "aac": "aac.svg", "ogg": "ogg.svg", "m4a": "m4a.svg", "amr": "amr.svg",
        "aiff": "aiff.svg", "aif": "aif.svg", "ra": "ra.svg",
    }
    archive_format_map = {
        "zip": "zip.svg", "rar": "rar.svg", "7z": "7z.svg", "gz": "gz.svg", "tar": "tar.svg",
    }
    binary_format_map = {
        "exe": "exe.svg", "apk": "apk.svg", "ipa": "ipa.svg", "deb": "deb.svg", "rpm": "rpm.svg",
        "dmg": "dmg.svg", "msi": "msi.svg", "bin": "bin.svg", "iso": "iso.svg",
    }
    document_format_map = {
        "doc": "doc.svg", "docx": "docx.svg",
        "xls": "xls.svg", "xlsx": "xls.svg", "csv": "csv.svg",
        "ppt": "ppt.svg", "pptx": "pptx.svg",
        "pdf": "pdf.svg",
        "txt": "txt.svg",
        "otl": "doc.svg", "dbt": "xls.svg"
    }
    if resource_format in code_format_map:
        resource_type = "code"
    elif (resource_type and resource_type.startswith("image")) or resource_format in image_format_map:
        resource_type = "image"
    elif (resource_type and resource_type.startswith("video")) or resource_format in video_format_map:
        resource_type = "video"
    elif (resource_type and resource_type.startswith("audio")) or resource_format in audio_format_map:
        resource_type = "audio"
    elif resource_format.startswith("htm"):
        resource_type = "webpage"
    elif resource_format in archive_format_map:
        resource_type = "archive"
    elif resource_format in binary_format_map:
        resource_type = "binary"
    elif resource_format in document_format_map:
        resource_type = "document"
    else:
        resource_type = "other"
    return resource_type, resource_format


def set_task_icon(resource_type, resource_format):
    """
    设置任务图标
    :param resource_type:
    :param resource_format:
    :return:
    """
    icon_base_url = "/images/"
    icon_url = 'file.svg'
    icon_format_map = {
        # 文档类型
        "doc": "doc.svg", "docx": "docx.svg",
        "xls": "xls.svg", "xlsx": "xlsx.svg", "csv": "csv.svg",
        "ppt": "ppt.svg", "pptx": "pptx.svg",
        "pdf": "pdf.svg",
        "txt": "txt.svg", "otl": "otl.svg", "dbt": "dbt.svg",

        # 图片类型
        "jpeg": "jpeg.svg", "jpg": "jpg.svg",
        "png": "png.svg", "gif": "gif.svg", "bmp": "bmp.svg",
        "webp": "webp.svg", "svg": "svg.svg",
        # 视频类型
        "mp4": "mp4.svg", "avi": "avi.svg", "mkv": "mkv.svg",  "flv": "flv.svg",  "mov": "mov.svg",
        "wmv": "wmv.svg", "webm": "webm.svg", "mpg": "mpg.svg", "3gp": "3gp.svg", "mpeg": "mpeg.svg",
        # 音频类型
        "mp3": "mp3.svg", "wav": "wav.svg", "wma": "wma.svg", "flac": "flac.svg",
        "aac": "aac.svg", "ogg": "ogg.svg", "m4a": "m4a.svg", "amr": "amr.svg",
        "aiff": "aiff.svg", "aif": "aif.svg", "ra": "ra.svg",
        # 代码
        "css": "css.svg", "js": "js.svg", "json": "json.svg", "xml": "xml.svg",
        "java": "java.svg", "cpp": "cpp.svg", "c": "c.svg", "py": "py.svg", "php": "php.svg",
        "go": "go.svg", "h": "h.svg", "hpp": "hpp.svg", "rb": "rb.svg", "cs": "cs.svg",
        "sh": "sh.svg", "bat": "bat.svg", "swift": "swift.svg", "kt": "kt.svg", "ts": "ts.svg",
        "pl": "pl.svg", "lua": "lua.svg", "r": "r.svg", "scala": "scala.svg", "sql": "sql.svg",
        "vb": "vb.svg", "vbs": "vbs.svg", "yaml": "yaml.svg", "yml": "yml.svg", "md": "md.svg",
        "ps1": "ps1.svg", "ini": "ini.svg", "conf": "conf.svg", "properties": "properties.svg",
        "cmd": "cmd.svg", "vue": "vue.svg", "jsx": "jsx.svg", "perl": "perl.svg",
        "db2": "db2.svg", "rs": "rs.svg", "mm": "mm.svg", "m": "m.svg", "plsql": "plsql.svg",
        "hs": "hs.svg", "hsc": "hsc.svg", "Dockerfile": "Dockerfile.svg", "dart": "dart.svg",
        "pm": "pm.svg", "bash": "bash.svg", "svelte": "svelte.svg",
        # 压缩包
        "zip": "zip.svg", "rar": "rar.svg", "7z": "7z.svg", "gz": "gz.svg", "tar": "tar.svg",
        # 网页
        "html": "html.svg",  "htm": "htm.svg",
        # 二进制程序
        "exe": "exe.svg", "apk": "apk.svg", "ipa": "ipa.svg",  "deb": "deb.svg", "rpm": "rpm.svg",
        "dmg": "dmg.svg", "msi": "msi.svg", "bin": "bin.svg", "iso": "iso.svg",
        }
    if icon_format_map.get(resource_format):
        icon_url = icon_format_map[resource_format]
        return icon_base_url + icon_url
    icon_type_map = {
        "folder": "folder.svg",
        "document": "document.svg",
        "image": "image.svg",
        "video": "video.svg",
        "audio": "audio.svg",
        "code": "code.svg",
        "webpage": "webpage.svg",
        "archive": "archive.svg",
        "binary": "binary.svg",
        "other": "file.svg",

    }
    if icon_type_map.get(resource_type):
        icon_url = icon_type_map[resource_type]
    return icon_base_url + icon_url


def update_resource_upload_task(params):
    """
    更新资源上传任务
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    task_id = params.get("task_id")
    task_status = params.get("task_status")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource_upload = ResourceObjectUpload.query.filter(
        ResourceObjectUpload.id == task_id,
        ResourceObjectUpload.user_id == user_id
    ).first()
    if not target_resource_upload:
        return next_console_response(error_status=True, error_message="任务不存在！")
    target_resource_upload.task_status = task_status
    try:
        db.session.add(target_resource_upload)
        db.session.commit()
    except Exception as e:
        return next_console_response(error_status=True, error_message=f"更新任务异常：{e.args}")
    return next_console_response(result=target_resource_upload.show_info())


def upload_resource_object(params, chunk_content):
    """
    上传资源对象
        每个文件块存储在临时目录下
        最后一个文件块上传完成后,生成记录数据，合并文件块写入目标文件，
        并更新任务记录，
        最后删除临时文件块
    :param params:
    :param chunk_content:
    :return:
    """
    user_id = int(params.get("user_id"))
    chunk_task_id = params.get("chunk_task_id")
    try:
        chunk_idx = int(params.get("chunk_index"))
    except ValueError as e:
        return next_console_response(error_status=True, error_message="文件块索引异常！")
    chunk_MD5 = params.get("chunk_MD5")
    chunk_size = params.get("chunk_size")
    try:
        chunk_size = int(chunk_size)
    except ValueError as e:
        chunk_size = 0
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource_upload = ResourceObjectUpload.query.filter(
        ResourceObjectUpload.id == chunk_task_id,
        ResourceObjectUpload.user_id == user_id,
    ).first()
    if not target_resource_upload:
        return next_console_response(error_status=True, error_message="任务不存在！")
    tmp_save_base_path = os.path.join(target_user.user_resource_base_path, "tmp")
    if not os.path.exists(tmp_save_base_path):
        os.makedirs(tmp_save_base_path, exist_ok=True)
    tmp_save_path = os.path.join(tmp_save_base_path, f"{target_resource_upload.content_prefix}_{chunk_idx}")
    tmp_save_path_main = os.path.join(tmp_save_base_path, f"{target_resource_upload.content_prefix}")
    try:
        with open(tmp_save_path, "wb") as f:
            res = chunk_content.read()
            if len(res) > chunk_size:
                # 长度异常进行处理
                res = res[-chunk_size:]
            f.write(res)
    except Exception as e:
        return next_console_response(error_status=True, error_message=f"写入文件异常：{e.args}")
    # 检查文件MD5
    with open(tmp_save_path, "rb") as f:
        content_MD5 = hashlib.sha256(f.read()).hexdigest()
        if content_MD5.strip() != chunk_MD5.strip():
            app.logger.warning(f"文件MD5校验失败！{content_MD5} != {chunk_MD5} , {tmp_save_path}")
            return next_console_response(error_status=True, error_message="文件MD5校验失败！")
        with open(tmp_save_path_main, "ab") as f2:
            f2.write(res)
    os.remove(tmp_save_path)
    # 完成最后一个文件块上传
    if chunk_idx == target_resource_upload.content_max_idx:
        # 新增资源记录
        resource_icon = set_resource_icon({
            "resource_type": target_resource_upload.resource_type,
            "resource_format": target_resource_upload.resource_format
        })
        new_resource_path = generate_resource_path(
            user_resource_base_path=target_user.user_resource_base_path,
            target_resource_parent_id=target_resource_upload.resource_parent_id,
            target_type=target_resource_upload.resource_format,
        )
        # 自动修改文件名
        same_dir_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_parent_id == target_resource_upload.resource_parent_id,
            ResourceObjectMeta.resource_status == "正常",
        ).all()
        all_resource_names = {resource_item.resource_name for resource_item in same_dir_resources}
        base, ext = os.path.splitext(target_resource_upload.resource_name)
        reindex = 1
        while target_resource_upload.resource_name in all_resource_names:
            # 如果已经是重命名过的文件，则再原有基础上增加
            target_resource_upload.resource_name = f"{base}({reindex}){ext}"
            reindex += 1
        new_resource_meta = ResourceObjectMeta(
            user_id=user_id,
            resource_parent_id=target_resource_upload.resource_parent_id,
            resource_name=target_resource_upload.resource_name,
            resource_size_in_MB=target_resource_upload.resource_size_in_mb,
            resource_icon=resource_icon,
            resource_type=target_resource_upload.resource_type,
            resource_format=target_resource_upload.resource_format,
            resource_path=new_resource_path,
            resource_feature_code=target_resource_upload.resource_md5,
            resource_source=target_resource_upload.task_source,
        )
        try:
            db.session.add(new_resource_meta)
            db.session.commit()
        except Exception as e:
            return next_console_response(error_status=True, error_message=f"新增资源异常：{e.args}")
        # 合并文件块
        # for idx in range(target_resource_upload.content_max_idx + 1):
        #     tmp_chunk_path = os.path.join(tmp_save_base_path, f"{target_resource_upload.content_prefix}_{idx}")
        #     if not os.path.exists(tmp_chunk_path):
        #         target_resource_upload.task_status = "error"
        #         db.session.add(target_resource_upload)
        #         db.session.commit()
        #         return next_console_response(error_status=True, error_message="文件块不存在！")
        #     with open(tmp_chunk_path, "rb") as f:
        #         chunk_content = f.read()
        #     with open(new_resource_path, "ab") as f:
        #         f.write(chunk_content)
        #     # 读取完成后删除文件块
        #     os.remove(tmp_chunk_path)
        # 临时文件块重命名
        os.rename(tmp_save_path_main, new_resource_path)
        # 更新任务记录
        target_resource_upload.resource_id = new_resource_meta.id
        target_resource_upload.content_finish_idx = target_resource_upload.content_max_idx
        target_resource_upload.task_status = "success"
        try:
            db.session.add(target_resource_upload)
            db.session.commit()
        except Exception as e:
            return next_console_response(error_status=True, error_message=f"更新任务异常：{e.args}")
        # 满足条件后，提交自动构建任务
        user_config = get_user_config(user_id).json.get("result")
        if user_config and user_config["resources"]["auto_rag"]:
            # 判断类型是否支持构建
            if check_rag_is_support(new_resource_meta):
                build_params = {
                    "user_id": user_id,
                    "resource_id": new_resource_meta.id
                }
                auto_build_resource_ref_v2.delay(build_params)
        return next_console_response(result=target_resource_upload.show_info())
    else:
        target_resource_upload.content_finish_idx = chunk_idx
        target_resource_upload.task_status = "uploading"
        try:
            db.session.add(target_resource_upload)
            db.session.commit()
        except Exception as e:
            return next_console_response(error_status=True, error_message=f"更新任务异常：{e.args}")
        return next_console_response(result=target_resource_upload.show_info())


def check_rag_is_support(resource):
    if resource.resource_format in {
        # 文档
        "doc", "docx", "xls", "xlsx", "ppt", "pptx", "pdf", "txt",
        # 代码
        'css', 'js', 'json', 'xml', 'java', 'cpp', 'c', 'py', 'php', 'go', 'h', 'hpp',
        'rb', 'cs', 'sh', 'bat', 'swift', 'kt', 'ts', 'pl', 'lua', 'r', 'scala', 'sql', 'vb',
        'vbs', 'yaml', 'yml', 'md', 'ps1', 'ini', 'conf', 'properties', 'cmd', 'vue', 'jsx',
        'perl', 'db2', 'rs', 'mm', 'm', 'plsql', 'hs', 'hsc', 'Dockerfile', 'dart', 'pm', 'bash', 'svelte',
        # 网页
        "htm", "html",
        "log", "syslog", "audit", "wevt", "kmsg", "access", "cfg", "ini", "service", "rules", "policy", "rrd", "tsd",
        "metrics", "stats", "pcap", "flow", "sflow", "pdns", "crontab", "fstab", "grub", "conf", "ovf", "qcow2", "yaml",
        "toml", "hash", "sig", "gpg", "p12", "diff", "snap", "tar", "manifest"
    }:
        return True
    return False


def set_resource_icon(params):
    """
    根据资源类型设置资源图标
    :param params:
    :return:
    """
    resource_type = params.get("resource_type")
    resource_format = params.get("resource_format")
    default_icon_type_map = {
        "folder": "folder.svg",
        "document": "document.svg",
        "image": "image.svg",
        "video": "video.svg",
        "audio": "audio.svg",
        "code": "code.svg",
        "webpage": "webpage.svg",
        "archive": "archive.svg",
        "binary": "binary.svg",
        "other": "file.svg",
    }
    default_icon_format_map = {
        # 文档类型
        "doc": "doc.svg", "docx": "docx.svg",
        "xls": "xls.svg", "xlsx": "xlsx.svg", "csv": "csv.svg",
        "ppt": "ppt.svg", "pptx": "pptx.svg",
        "pdf": "pdf.svg",
        "txt": "txt.svg", "otl": "otl.svg", "dbt": "dbt.svg",
        # 图片类型
        "jpeg": "jpeg.svg", "jpg": "jpg.svg",
        "png": "png.svg", "gif": "gif.svg", "bmp": "bmp.svg",
        "webp": "webp.svg", "svg": "svg.svg",
        # 视频类型
        "mp4": "mp4.svg", "avi": "avi.svg", "mkv": "mkv.svg", "flv": "flv.svg", "mov": "mov.svg",
        "wmv": "wmv.svg", "webm": "webm.svg", "mpg": "mpg.svg", "3gp": "3gp.svg", "mpeg": "mpeg.svg",
        # 音频类型
        "mp3": "mp3.svg", "wav": "wav.svg", "wma": "wma.svg", "flac": "flac.svg",
        "aac": "aac.svg", "ogg": "ogg.svg", "m4a": "m4a.svg", "amr": "amr.svg",
        "aiff": "aiff.svg", "aif": "aif.svg", "ra": "ra.svg",
        # 代码
        "css": "css.svg", "js": "js.svg", "json": "json.svg", "xml": "xml.svg",
        "java": "java.svg", "cpp": "cpp.svg", "c": "c.svg", "py": "py.svg", "php": "php.svg",
        "go": "go.svg", "h": "h.svg", "hpp": "hpp.svg", "rb": "rb.svg", "cs": "cs.svg",
        "sh": "sh.svg", "bat": "bat.svg", "swift": "swift.svg", "kt": "kt.svg", "ts": "ts.svg",
        "pl": "pl.svg", "lua": "lua.svg", "r": "r.svg", "scala": "scala.svg", "sql": "sql.svg",
        "vb": "vb.svg", "vbs": "vbs.svg", "yaml": "yaml.svg", "yml": "yml.svg", "md": "md.svg",
        "ps1": "ps1.svg", "ini": "ini.svg", "conf": "conf.svg", "properties": "properties.svg",
        "cmd": "cmd.svg", "vue": "vue.svg", "jsx": "jsx.svg", "perl": "perl.svg",
        "db2": "db2.svg", "rs": "rs.svg", "mm": "mm.svg", "m": "m.svg", "plsql": "plsql.svg",
        "hs": "hs.svg", "hsc": "hsc.svg", "Dockerfile": "Dockerfile.svg", "dart": "dart.svg",
        "pm": "pm.svg", "bash": "bash.svg", "svelte": "svelte.svg",
        # 压缩包
        "zip": "zip.svg", "rar": "rar.svg", "7z": "7z.svg", "gz": "gz.svg", "tar": "tar.svg",
        # 网页
        "html": "html.svg", "htm": "htm.svg",
        # 二进制程序
        "exe": "exe.svg", "apk": "apk.svg", "ipa": "ipa.svg", "deb": "deb.svg", "rpm": "rpm.svg",
        "dmg": "dmg.svg", "msi": "msi.svg", "bin": "bin.svg", "iso": "iso.svg",
    }
    resource_icon = ""
    if default_icon_type_map.get(resource_type):
        resource_icon = default_icon_type_map[resource_type]
    if default_icon_format_map.get(resource_format):
        resource_icon = default_icon_format_map[resource_format]
    return resource_icon


def generate_resource_path(user_resource_base_path, target_resource_parent_id, target_type="file"):
    resource_path = user_resource_base_path
    # 如果存在上级目录
    if target_resource_parent_id:
        target_parent_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == target_resource_parent_id
        ).first()
        if (target_parent_resource and target_parent_resource.resource_path
                and os.path.exists(target_parent_resource.resource_path)):
            resource_path = target_parent_resource.resource_path
    new_resource_path = os.path.join(resource_path, str(uuid.uuid4())[:12])
    # 防止重名
    while os.path.exists(new_resource_path):
        new_resource_path = os.path.join(resource_path, str(uuid.uuid4())[:12])
    if target_type == "folder":
        os.mkdir(new_resource_path)
    else:
        new_resource_path += f".{target_type}"
    return new_resource_path


def delete_resource_object(params):
    """
    删除资源对象,标记为删除，不实际删除
    如果是目录，递归删除
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_id = params.get("resource_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == resource_id,
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    if not target_resource.resource_parent_id:
        return next_console_response(error_status=True, error_message="根目录不可删除！")
    # 检查权限
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": 'manage'
    }):
        return next_console_response(error_status=True, error_message="无权限！")
    # 如果不是目录，直接删除
    if target_resource.resource_type != "folder":
        target_resource.resource_status = "删除"
        target_resource.delete_time = db.func.now()
        try:
            db.session.add(target_resource)
            db.session.commit()
        except Exception as e:
            return next_console_response(error_status=True, error_message=f"删除资源异常：{e.args}")
        # 更新索引数据
        refs = RagRefInfo.query.filter(
            RagRefInfo.resource_id == target_resource.id,
            RagRefInfo.ref_status != "已删除",
        ).all()
        for ref in refs:
            ref.ref_status = "已删除"
            db.session.add(ref)
        db.session.commit()
        # 删除关联快捷方式
        shortcuts = ResourceObjectShortCut.query.filter(
            ResourceObjectShortCut.user_id == user_id,
            ResourceObjectShortCut.resource_id == resource_id,
        ).all()
        for shortcut in shortcuts:
            db.session.delete(shortcut)
        db.session.commit()
        return next_console_response(result=target_resource.show_info())
    # 如果是目录，递归删除
    all_resource_list = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
    ).all()
    target_resource_id_list = [resource_id]
    add_cnt = 1
    while add_cnt > 0:
        add_cnt = 0
        for resource_item in all_resource_list:
            if (resource_item.resource_parent_id in target_resource_id_list
                    and resource_item.id not in target_resource_id_list):
                target_resource_id_list.append(resource_item.id)
                add_cnt += 1
    for resource_item in all_resource_list:
        if resource_item.id in target_resource_id_list:
            resource_item.resource_status = "删除"
            resource_item.delete_time = db.func.now()
            db.session.add(resource_item)
    db.session.commit()
    # 更新索引数据
    refs = RagRefInfo.query.filter(
        RagRefInfo.resource_id.in_(target_resource_id_list),
        RagRefInfo.ref_status != "已删除",
    ).all()
    for ref in refs:
        ref.ref_status = "已删除"
        db.session.add(ref)
    db.session.commit()
    # 删除关联快捷方式
    shortcuts = ResourceObjectShortCut.query.filter(
        ResourceObjectShortCut.user_id == user_id,
        ResourceObjectShortCut.resource_id.in_(target_resource_id_list),
    ).all()
    for shortcut in shortcuts:
        db.session.delete(shortcut)
    db.session.commit()
    return next_console_response(result={"delete_cnt": len(target_resource_id_list)})


def batch_delete_resource_object(params):
    """
    批量删除资源对象
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_list = params.get("resource_list", [])
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_resource_list = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.id.in_(resource_list),
        ResourceObjectMeta.resource_parent_id.isnot(None)
    ).all()
    file_resource = [resource for resource in all_resource_list if resource.resource_type != "folder"]
    dir_resource_id_list = [resource.id for resource in all_resource_list if resource.resource_type == "folder"]
    # 删除文件资源
    for resource_item in file_resource:
        resource_item.resource_status = "删除"
        resource_item.delete_time = db.func.now()
        db.session.add_all(file_resource)
    db.session.commit()
    # 更新索引数据
    all_file_resource_id_list = [resource.id for resource in file_resource]
    refs = RagRefInfo.query.filter(
        RagRefInfo.resource_id.in_(all_file_resource_id_list),
        RagRefInfo.ref_status != "已删除",
    ).all()
    for ref in refs:
        ref.ref_status = "已删除"
        db.session.add(ref)
    db.session.commit()
    # 删除目录资源
    all_user_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == "正常",
        ).all()
    add_cnt = 1
    while add_cnt > 0:
        add_cnt = 0
        for resource_item in all_user_resource:
            if (resource_item.resource_parent_id in dir_resource_id_list
                    and resource_item.id not in dir_resource_id_list):
                dir_resource_id_list.append(resource_item.id)
                add_cnt += 1
    for resource_item in all_user_resource:
        if resource_item.id in dir_resource_id_list:
            resource_item.resource_status = "删除"
            resource_item.delete_time = db.func.now()
            db.session.add(resource_item)
    db.session.commit()
    # 更新索引数据
    refs = RagRefInfo.query.filter(
        RagRefInfo.resource_id.in_(dir_resource_id_list),
        RagRefInfo.ref_status != "已删除",
    ).all()
    for ref in refs:
        ref.ref_status = "已删除"
        db.session.add(ref)
    db.session.commit()
    return next_console_response(result={"delete_cnt": len(resource_list)})


def add_resource_object(params):
    """
    新增资源对象
        目前只支持目录
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_resource_parent_id = params.get("resource_parent_id")
    target_resource_name = params.get("resource_name", "")
    target_resource_desc = params.get("resource_desc", "")
    target_resource_type = params.get("resource_type", "folder")
    target_resource_icon = "folder.svg"
    if target_resource_type not in ('folder', 'document'):
        return next_console_response(error_status=True, error_message="目前只支持目录！")
    if target_resource_type == 'document':
        return create_new_document(params)

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    # 检查主目录是否存在
    if not target_user.user_resource_base_path:
        return next_console_response(error_status=True, error_message="存储空间异常！")
    if not os.path.exists(target_user.user_resource_base_path):
        os.mkdir(target_user.user_resource_base_path, )

    if not target_resource_parent_id:
        root_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_parent_id.is_(None)
        ).first()
        if not root_resource:
            return next_console_response(error_status=True, error_message="根目录不存在！")
        target_resource_parent_id = root_resource.id

    try:
        new_resource_path = generate_resource_path(
            user_resource_base_path=target_user.user_resource_base_path,
            target_resource_parent_id=target_resource_parent_id,
            target_type="folder",
        )
    except Exception as e:
        return next_console_response(error_status=True, error_message=f"生成资源路径异常：{e.args}")
    # 目录自动重命名
    same_dir_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_parent_id == target_resource_parent_id,
        ResourceObjectMeta.resource_status == "正常"
    ).all()
    if same_dir_resources:
        same_dir_resource_name_list = [resource.resource_name for resource in same_dir_resources]
        new_resource_name = target_resource_name
        reindex = 1
        while new_resource_name in same_dir_resource_name_list:
            new_resource_name = f"{target_resource_name}({reindex})"
            reindex += 1
        target_resource_name = new_resource_name
    new_dir_resource = ResourceObjectMeta(
        resource_parent_id=target_resource_parent_id,
        user_id=user_id,
        resource_name=target_resource_name,
        resource_desc=target_resource_desc,
        resource_type=target_resource_type,
        resource_icon=target_resource_icon,
        resource_path=new_resource_path,
        resource_source='resource_center',
    )
    db.session.add(new_dir_resource)
    db.session.commit()
    return next_console_response(result=new_dir_resource.show_info())


def batch_add_resource_folder(params):
    """
    批量新增资源目录
        resource_list:[ resource_path]
    输入为资源路径，解析出所有目录，去重后，分析目录结构，逐级创建目录
    目录节点结构：{ "dir1": { "dir2": { "dir3": {} } } }
    :param params:
    :return: resource_parent_id_map { resource_path: resource_parent_id }
    """
    user_id = int(params.get("user_id"))
    resource_list = params.get("resource_list", [])
    resource_parent_id = params.get("resource_parent_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    root_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_parent_id.is_(None)
    ).first()
    if not root_resource:
        return next_console_response(error_status=True, error_message="根目录不存在！")
    if not resource_parent_id:
        resource_parent_id = root_resource.id
    else:
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource_parent_id,
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_type == "folder"
        ).first()
        if not target_resource:
            return next_console_response(error_status=True, error_message="目标目录不存在！")
        resource_parent_id = target_resource.id


    # 解析目录结构
    resource_size_in_MB = 0
    dir_structure = {}
    for resource_item in resource_list:
        parent_path = os.path.dirname(resource_item.get('path'))
        resource_size_in_MB += resource_item.get('size') / 1024 / 1024
        all_dir_parts = parent_path.split("/")
        current_level = dir_structure
        for dir_part in all_dir_parts:
            if dir_part not in current_level:
                current_level[dir_part] = {}
            current_level = current_level[dir_part]
    # 校验空间资源
    # 检查资源使用情况
    all_resources_usage = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常"
    ).all()
    all_resource_size = sum([resource_item.resource_size_in_MB for resource_item in all_resources_usage])
    if all_resource_size >= target_user.user_resource_limit:
        return next_console_response(error_status=True, error_message="资源空间已满！")
    if all_resource_size + resource_size_in_MB >= target_user.user_resource_limit:
        return next_console_response(error_status=True, error_message="资源空间不足！")
    # 逐级创建目录资源
    # print("目录结构：", dir_structure)
    dir_result = {}

    def create_dir_resource(parent_id, dir_structure, parent_path):
        for dir_name, dir_item in dir_structure.items():
            try:
                new_resource_path = generate_resource_path(
                    user_resource_base_path=target_user.user_resource_base_path,
                    target_resource_parent_id=parent_id,
                    target_type="folder",
                )
            except Exception as e:
                return next_console_response(error_status=True, error_message=f"生成资源路径异常：{e.args}")
            new_dir_resource = ResourceObjectMeta(
                resource_parent_id=parent_id,
                user_id=user_id,
                resource_name=dir_name,
                resource_type="folder",
                resource_icon="folder.svg",
                resource_source='resource_center',
                resource_path=new_resource_path,
            )
            db.session.add(new_dir_resource)
            db.session.commit()
            dir_result[parent_path + "/" + dir_name] = new_dir_resource.id
            create_dir_resource(new_dir_resource.id, dir_item, parent_path + "/" + dir_name)
    # 为了防止重名，先创建第一级目录
    for dir_name, dir_item in dir_structure.items():
        # 目录自动重命名
        target_resource_name = dir_name
        same_dir_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_parent_id == resource_parent_id,
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_type == "folder",
        ).all()
        if same_dir_resources:
            same_dir_resource_name_list = [resource.resource_name for resource in same_dir_resources]
            new_resource_name = dir_name
            reindex = 1
            while new_resource_name in same_dir_resource_name_list:
                new_resource_name = f"{dir_name}({reindex})"
                reindex += 1
            target_resource_name = new_resource_name

        try:
            new_resource_path = generate_resource_path(
                user_resource_base_path=target_user.user_resource_base_path,
                target_resource_parent_id=resource_parent_id,
                target_type="folder",
            )
        except Exception as e:
            return next_console_response(error_status=True, error_message=f"生成资源路径异常：{e.args}")

        new_dir_resource = ResourceObjectMeta(
            resource_parent_id=resource_parent_id,
            user_id=user_id,
            resource_name=target_resource_name,
            resource_type="folder",
            resource_icon="folder.svg",
            resource_source='resource_center',
            resource_path=new_resource_path,
        )
        db.session.add(new_dir_resource)
        db.session.commit()
        dir_result[dir_name] = new_dir_resource.id

        create_dir_resource(new_dir_resource.id, dir_item, dir_name)
    # 组装返回结果
    final_result = {}
    for resource_item in resource_list:
        resource_path = resource_item.get('path')
        final_result[resource_path] = dir_result.get(os.path.dirname(resource_path))
    return next_console_response(result=final_result)


def update_resource_object(params):
    """
    更新资源对象
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_resource_id = params.get("resource_id")
    target_resource_name = params.get("resource_name")
    target_resource_desc = params.get("resource_desc")
    target_resource_language = params.get("resource_language")
    resource_tags = params.get("resource_tags", [])
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == target_resource_id,
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")
    # 检查是否有管理权限
    if target_resource.user_id != user_id and not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access": "manage"
    }):
        return next_console_response(error_status=True, error_message="无权限！")
    # 检查是否有重名，有重名提示用户名称重复
    if target_resource_name:
        same_dir_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_parent_id == target_resource.resource_parent_id,
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.id != target_resource_id,
        ).all()
        all_resource_names = {resource.resource_name for resource in same_dir_resources}
        if target_resource_name in all_resource_names:
            return next_console_response(error_status=True,
                                         error_message=f"'{target_resource_name}' 已存在于当前目录中，请使用其他名称！")

    if target_resource.resource_name and target_resource.resource_name != target_resource_name:
        target_resource.resource_name = target_resource_name
    if target_resource.resource_desc is not None and target_resource.resource_desc != target_resource_desc:
        target_resource.resource_desc = target_resource_desc
    if target_resource_language and target_resource_language != target_resource.resource_language:
        target_resource.resource_language = target_resource_language
    db.session.add(target_resource)
    db.session.commit()
    # 新增资源标签
    exist_tags = ResourceTagRelation.query.filter(
        ResourceTagRelation.resource_id == target_resource_id,
        ResourceTagRelation.rel_status == '正常',
    ).all()
    exist_tag_ids = {tag.tag_id for tag in exist_tags}
    for tag in resource_tags:
        if tag.get('id') not in exist_tag_ids:
            new_tag_relation = ResourceTagRelation(
                resource_id=target_resource_id,
                tag_id=tag.get('id'),
            )
            db.session.add(new_tag_relation)
    db.session.commit()
    return next_console_response(result=target_resource.show_info())


def mv_resource_object(params):
    """
    移动资源对象,需要起点目录的管理权限和终点目录的管理权限
        修改资源的parent_id
        底层数据也需要移动:,resource_path
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_id_list = params.get("resource_id_list", [])
    target_resource_id = params.get("target_resource_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    source_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(resource_id_list),
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常"
    ).all()
    if not source_resources:
        return next_console_response(error_status=True, error_message="资源不存在！")
    all_source_parent_id = set([resource.resource_parent_id for resource in source_resources])
    target_dir_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == target_resource_id,
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_dir_resource:
        return next_console_response(error_status=True, error_message="目标资源不存在！")
    if target_dir_resource.resource_type != "folder":
        return next_console_response(error_status=True, error_message="目标资源不是目录！")
    # 检查目标目录是否是源目录的子目录，如果冲突则不允许移动
    if target_dir_resource.id in all_source_parent_id:
        return next_console_response(error_status=True, error_message="目标目录是源目录的子目录！")
    all_user_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
    ).all()
    target_resource_id_list = [target_dir_resource.resource_parent_id]
    add_cnt = 1
    while add_cnt > 0:
        add_cnt = 0
        for resource_item in all_user_resource:
            if (resource_item.id in target_resource_id_list
                    and resource_item.resource_parent_id not in target_resource_id_list):
                target_resource_id_list.append(resource_item.resource_parent_id)
                add_cnt += 1
    if set(resource_id_list) & set(target_resource_id_list):
        return next_console_response(error_status=True, error_message="目标目录是源目录的子目录！")
    # 开始更新
    all_path_map = {}
    for resource_item in source_resources:
        resource_item.resource_parent_id = target_dir_resource.id
        resource_item.resource_source = target_dir_resource.resource_source
        resource_item.resource_download_url = ''
        resource_item.resource_show_url = ''
        # 底层目录也需要修改
        base_path = target_dir_resource.resource_path
        if os.path.exists(base_path):
            resource_now_path = resource_item.resource_path
            new_resource_path = os.path.join(base_path, os.path.basename(resource_now_path))
            if os.path.exists(new_resource_path):
                new_resource_path = os.path.join(base_path, str(uuid.uuid4())[:12])
            try:
                os.rename(resource_now_path, new_resource_path)
            except Exception as e:
                app.logger.error(f"移动资源异常：{e.args}")
                return next_console_response(error_status=True, error_message=f"移动资源异常：{e.args}")
            resource_item.resource_path = new_resource_path
            if resource_now_path not in all_path_map:
                all_path_map[resource_now_path] = new_resource_path
        db.session.add(resource_item)
    db.session.commit()
    # 更新下层所有资源的路径字段与下载链接
    for resource in all_user_resource:
        for mv_resource in all_path_map:
            if resource.resource_path.startswith(mv_resource):
                new_path = resource.resource_path.replace(mv_resource, all_path_map[mv_resource])
                resource.resource_path = new_path
                resource.resource_download_url = ''
                resource.resource_show_url = ''
                db.session.add(resource)
    db.session.commit()
    result = {
        "target_resource_id": target_resource_id,
        "resource_id_list": resource_id_list
    }
    return next_console_response(result=result)


def download_resource_object(params):
    """
    下载资源对象, 返回文件下载链接（get)
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_resource_id = params.get("resource_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resource = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id == target_resource_id,
        ResourceObjectMeta.resource_status == "正常"
    ).first()
    if not target_resource:
        return next_console_response(error_status=True, error_message="资源不存在！")

    if target_resource.resource_type == "folder":
        return next_console_response(error_status=True, error_message="不支持目录下载！")
    if not os.path.exists(target_resource.resource_path):
        return next_console_response(error_status=True, error_message="文件不存在！")
    if not os.path.exists(app.config["download_dir"]):
        os.mkdir(app.config["download_dir"])
    # 检查文件下载权限
    if not check_user_manage_access_to_resource({
        "user": target_user,
        "resource": target_resource,
        "access_type": "download",
    }):
        return next_console_response(error_status=True, error_message="无权限！")

    if not target_resource.resource_download_url:
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

    # 查询下载记录
    if target_resource.user_id != user_id:
        begin_time = datetime.now(timezone.utc) - timedelta(seconds=app.config["download_cool_time"])
        download_records = ResourceDownloadRecord.query.filter(
            ResourceDownloadRecord.user_id == user_id,
            ResourceDownloadRecord.create_time >= begin_time,
        ).join(
            ResourceObjectMeta,
            ResourceDownloadRecord.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceObjectMeta.user_id == target_resource.user_id,
        ).with_entities(
            ResourceObjectMeta
        ).all()
        if len(download_records) >= app.config["download_max_count"]:
            # 查询冷却记录
            exist_cool_record = ResourceDownloadCoolingRecord.query.filter(
                ResourceDownloadCoolingRecord.user_id == user_id,
                ResourceDownloadCoolingRecord.author_id == target_resource.user_id,
                ResourceDownloadCoolingRecord.create_time >= begin_time,
            ).order_by(ResourceDownloadCoolingRecord.create_time.desc()).first()
            if not exist_cool_record:
                new_cool_record = ResourceDownloadCoolingRecord(
                    user_id=user_id,
                    author_id=target_resource.user_id,
                    resource_id=target_resource_id,
                    author_notice=False
                )
                db.session.add(new_cool_record)
                db.session.commit()
                # 发送下载冷却通知
                send_resource_download_cooling_notice_email.delay({
                    "cool_user_id": user_id,
                    "user_id": target_resource.user_id,
                    "resource_id": target_resource_id,
                    "cooling_record_id": new_cool_record.id
                })
                return next_console_response(error_status=True, error_message="下载次数过多，请稍后再试！或者联系作者进一步授权！")
            if not exist_cool_record.author_notice:
                # 发送下载冷却通知
                send_resource_download_cooling_notice_email.delay({
                    "cool_user_id": user_id,
                    "user_id": target_resource.user_id,
                    "resource_id": target_resource_id,
                    "cooling_record_id": exist_cool_record.id
                })
                return next_console_response(error_status=True,
                                             error_message="下载次数过多，请稍后再试！或者联系作者进一步授权！")
            if not exist_cool_record.author_allow:
                return next_console_response(error_status=True,
                                             error_message="下载次数过多，请稍后再试！或者联系作者进一步授权！")
            if (len(download_records) + exist_cool_record.author_allow_cnt) <= app.config["download_max_count"]:
                return next_console_response(error_status=True,
                                             error_message="下载次数过多，请稍后再试！或者联系作者进一步授权！")
    # 增加审计记录
    new_download_recoder = ResourceDownloadRecord(
        user_id=user_id,
        resource_id=target_resource_id,
        download_url=target_resource.resource_download_url
    )
    db.session.add(new_download_recoder)
    db.session.commit()
    return next_console_response(result={
        "download_url": target_resource.resource_download_url
    })


def batch_download_resource_object(params):
    """
    批量下载资源
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_list = params.get("resource_list", [])
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(resource_list),
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_type != 'folder'
    ).all()
    if not target_resources:
        return next_console_response(error_status=False, error_message="资源不存在！")
    all_download_link = []
    new_target_resources = []
    for resource_item in target_resources:
        if resource_item.resource_type == "folder":
            continue
        if not os.path.exists(resource_item.resource_path):
            continue
        # 检查文件下载权限
        if not check_user_manage_access_to_resource({
            "user": target_user,
            "resource": resource_item,
            "access_type": "download",
        }):
            continue
        if not resource_item.resource_download_url:
            # 生成下载链接
            resource_download_url = generate_download_url(
                'resource_center', resource_item.resource_path, suffix=resource_item.resource_format
            ).json.get("result")
            if not resource_download_url:
                continue
            resource_item.resource_download_url = resource_download_url
            db.session.add(resource_item)
            db.session.commit()
        new_target_resources.append(resource_item)

    # 查询下载记录
    begin_time = datetime.now() - timedelta(seconds=app.config["download_cool_time"])
    all_author_ids = list(set([resource.user_id for resource in new_target_resources if resource.user_id != user_id]))
    all_download_records = ResourceDownloadRecord.query.filter(
        ResourceDownloadRecord.user_id == user_id,
        ResourceDownloadRecord.create_time >= begin_time,
    ).join(
        ResourceObjectMeta,
        ResourceDownloadRecord.resource_id == ResourceObjectMeta.id
    ).filter(
        ResourceObjectMeta.user_id.in_(all_author_ids),
    ).with_entities(
        ResourceObjectMeta
    ).all()
    all_download_map = {}
    for record in all_download_records:
        if all_download_map.get(record.user_id):
            all_download_map[record.user_id].append(record)
        else:
            all_download_map[record.user_id] = [record]
    # 本次申请下载次数
    this_download_map = {}
    for resource in new_target_resources:
        if this_download_map.get(resource.user_id):
            this_download_map[resource.user_id].append(resource)
        else:
            this_download_map[resource.user_id] = [resource]
    limit_resource_author_id = []
    for author_id in all_author_ids:
        download_cnt = len(all_download_map.get(author_id, [])) + len(this_download_map.get(author_id, []))
        if download_cnt >= app.config["download_max_count"]:
            # 查询冷却记录
            exist_cool_record = ResourceDownloadCoolingRecord.query.filter(
                ResourceDownloadCoolingRecord.user_id == user_id,
                ResourceDownloadCoolingRecord.author_id == author_id,
                ResourceDownloadCoolingRecord.create_time >= begin_time,
            ).order_by(ResourceDownloadCoolingRecord.create_time.desc()).first()
            if not exist_cool_record:
                new_cool_record = ResourceDownloadCoolingRecord(
                    user_id=user_id,
                    author_id=author_id,
                    resource_id=this_download_map[author_id][0].id,
                    author_notice=False
                )
                db.session.add(new_cool_record)
                db.session.commit()
                # 发送下载冷却通知

                send_resource_download_cooling_notice_email.delay({
                    "cool_user_id": user_id,
                    "user_id": author_id,
                    "resource_id": this_download_map[author_id][0].id,
                    "cooling_record_id": new_cool_record.id
                })
                # 从下载列表中删除
                limit_resource_author_id.append(author_id)
                break
            if not exist_cool_record.author_notice:
                # 发送下载冷却通知
                send_resource_download_cooling_notice_email.delay({
                    "cool_user_id": user_id,
                    "user_id": author_id,
                    "resource_id": this_download_map[author_id][0].id,
                    "cooling_record_id": exist_cool_record.id
                })
                # 从下载列表中删除
                limit_resource_author_id.append(author_id)
                break
            if not exist_cool_record.author_allow:
                # 从下载列表中删除
                limit_resource_author_id.append(author_id)
                break
            if (download_cnt + exist_cool_record.author_allow_cnt) <= app.config["download_max_count"]:
                # 从下载列表中删除
                limit_resource_author_id.append(author_id)
                break
    # 增加审计记录
    for resource_item in new_target_resources:
        if resource_item.user_id in limit_resource_author_id:
            continue
        new_download_recoder = ResourceDownloadRecord(
            user_id=user_id,
            resource_id=resource_item.id,
            download_url=resource_item.resource_download_url
        )
        db.session.add(new_download_recoder)
        all_download_link.append({
            "resource_id": resource_item.id,
            "resource_name": resource_item.resource_name,
            "download_url": resource_item.resource_download_url

        })
    db.session.commit()
    return next_console_response(result=all_download_link)


def build_resource_object_ref(params):
    """
    构建资源对象引用
        如果是文件对象，则找到所有子对象，构建引用
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_list = params.get("resource_list", [])
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    target_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(resource_list),
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center"
    ).all()
    if not target_resources:
        return next_console_response(error_status=True, error_message="资源不存在！")
    all_dir_resources = [resource for resource in target_resources if resource.resource_type == "folder"]
    all_file_resources = [resource for resource in target_resources if resource.resource_type != "folder"]
    al_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center"
    ).all()
    all_dir_sub_resources = [
        resource.id for resource in all_dir_resources
    ]
    all_cnt = len(all_dir_sub_resources)
    while all_cnt > 0:
        all_cnt = 0
        for resource_item in al_resources:
            if (resource_item.resource_parent_id in all_dir_sub_resources
                    and resource_item.id not in all_dir_sub_resources):
                all_dir_sub_resources.append(resource_item.id)
                all_cnt += 1
    all_dir_sub_file_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.id.in_(all_dir_sub_resources),
        ResourceObjectMeta.resource_type != "folder",
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center"
    ).all()
    all_file_resources.extend(all_dir_sub_file_resources)
    for resource_item in all_file_resources:
        # 提交构建任务
        build_params = {
            "user_id": user_id,
            "resource_id": resource_item.id
        }
        # print("提交构建任务：", build_params)
        auto_build_resource_ref_v2.delay(build_params)
    return next_console_response(result={"build_cnt": len(all_file_resources)})


def get_resource_recent_count(params):
    """
    获取资源最近的统计数据
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    duration = params.get("duration", 30)
    recent_shortcuts = params.get("recent_shortcuts", ["recent_upload", "recent_index"])
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    now_time = datetime.now()
    start_time = now_time - timedelta(days=duration)
    res = {i: 0 for i in recent_shortcuts}
    for shortcut in recent_shortcuts:
        if shortcut == "recent_upload":
            recent_upload_cnt = ResourceObjectMeta.query.filter(
                ResourceObjectMeta.user_id == user_id,
                ResourceObjectMeta.resource_status == "正常",
                ResourceObjectMeta.create_time >= start_time,
                ResourceObjectMeta.resource_source == "resource_center"
            ).join(
                ResourceObjectUpload,
                ResourceObjectUpload.resource_id == ResourceObjectMeta.id
            ).count()
            res[shortcut] = recent_upload_cnt
        if shortcut == "recent_index":
            recent_index_cnt = ResourceObjectMeta.query.filter(
                ResourceObjectMeta.user_id == user_id,
                ResourceObjectMeta.resource_status == "正常",
                ResourceObjectMeta.create_time >= start_time,
                ResourceObjectMeta.resource_source == "resource_center"
            ).join(
                RagRefInfo,
                RagRefInfo.resource_id == ResourceObjectMeta.id
            ).with_entities(
                distinct(ResourceObjectMeta.id)
            ).count()
            res[shortcut] = recent_index_cnt
    return next_console_response(result=res)


def get_resource_type_count(params):
    """
    获取资源类型统计
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    all_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.resource_source == "resource_center"
    ).with_entities(
        ResourceObjectMeta.resource_type,
        func.count(ResourceObjectMeta.id).label("cnt"),
    ).group_by(
        ResourceObjectMeta.resource_type
    ).order_by(
        func.count(ResourceObjectMeta.id).desc(),
    ).all()
    res = []
    for item in all_resources:
        res.append({
            "name": item.resource_type,
            "cnt": item.cnt
        })
    return next_console_response(result=res)


def get_resource_recent_format_count(params):
    """
    获取资源格式统计
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    duration = params.get("duration", 30)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    now_time = datetime.now()
    begin_time = now_time - timedelta(days=duration)
    all_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == "正常",
        ResourceObjectMeta.create_time >= begin_time,
        ResourceObjectMeta.resource_source == "resource_center"
    ).with_entities(
        ResourceObjectMeta.resource_format,
        func.count(ResourceObjectMeta.id).label("cnt"),
    ).group_by(
        ResourceObjectMeta.resource_format
    ).order_by(
        func.count(ResourceObjectMeta.id).desc(),
    ).all()
    res = []
    for item in all_resources:
        if item.resource_format:
            res.append({
                "name": item.resource_format,
                "cnt": item.cnt
            })
        else:
            res.append({
                "name": "未知",
                "cnt": item.cnt
            })
    return next_console_response(result=res)


def search_by_recent_upload(params):
    """
    按最近上传时间搜索,并补充上传失败信息
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_type = params.get("resource_type", [])
    resource_format = params.get("resource_format", [])
    resource_tags = params.get("resource_tags", [])
    resource_keyword = params.get("resource_keyword", "")
    duration = params.get("duration", 30)
    page_size = params.get("page_size", 50)
    page_num = params.get("page_num", 1)
    fetch_all = params.get("fetch_all", False)

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    now_time = datetime.now()
    begin_time = now_time - timedelta(days=duration)

    # 获取资源上传任务，补充上传失败信息

    all_conditions = [
        ResourceObjectUpload.user_id == user_id,
        or_(
            ResourceObjectUpload.task_status != "success",
            ResourceObjectUpload.resource_id.isnot(None)
        ),
        ResourceObjectUpload.create_time >= begin_time
    ]

    if resource_type:
        all_conditions.append(ResourceObjectUpload.resource_type.in_(resource_type))

    if resource_format:
        all_conditions.append(ResourceObjectUpload.resource_format.in_(resource_format))

    if resource_keyword:
        all_conditions.append(ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%"))

    all_resources = ResourceObjectUpload.query.filter(
        *all_conditions
    ).join(
        ResourceObjectMeta,
        ResourceObjectMeta.id == ResourceObjectUpload.resource_id,
        isouter=True
    ).filter(
        ResourceObjectMeta.resource_status != "删除",
        ResourceObjectMeta.resource_source == "resource_center"
    ).with_entities(
        ResourceObjectUpload,
        ResourceObjectMeta
    )

    if resource_tags:

        user_tags = ResourceTag.query.filter(
            ResourceTag.user_id == user_id,
            ResourceTag.tag_status == "正常",
            ResourceTag.id.in_(resource_tags)
        ).all()
        legal_tags = [tag.id for tag in user_tags]
        all_resources = all_resources.join(
            ResourceTagRelation,
            ResourceTagRelation.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceTagRelation.tag_id.in_(legal_tags)
        ).with_entities(
            ResourceObjectUpload,
            ResourceObjectMeta
        )

    all_resources_results = all_resources.order_by(
        ResourceObjectUpload.create_time.desc()
    ).all()
    # 组装返回结果
    res = []
    for upload_task, resource in all_resources_results:
        res.append({
            "upload_task": upload_task.show_info(),
            "resource": resource.show_info() if resource else {}
        })
    if not fetch_all:
        res = res[(page_num - 1) * page_size: page_num * page_size]
    return next_console_response(result={
        "data": res,
        "total": len(all_resources_results)
    })


def search_by_recent_index(params):
    """
    按最近索引时间搜索,本质根据 RagRefInfo 表进行搜索 ,
    rag-resource 可能出现一对多的情况下，最后需要进行调整
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_type = params.get("resource_type", [])
    resource_format = params.get("resource_format", [])
    resource_tags = params.get("resource_tags", [])
    resource_keyword = params.get("resource_keyword", "")
    duration = params.get("duration", 30)
    page_size = params.get("page_size", 50)
    page_num = params.get("page_num", 1)
    fetch_all = params.get("fetch_all", False)

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    now_time = datetime.now()
    begin_time = now_time - timedelta(days=duration)

    # 获取资源索引构建任务，补充索引失败信息
    all_conditions = [
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.create_time >= begin_time,
        ResourceObjectMeta.resource_status == '正常',
        ResourceObjectMeta.resource_source == "resource_center"
    ]
    if resource_type:
        all_conditions.append(ResourceObjectMeta.resource_type.in_(resource_type))

    if resource_format:
        all_conditions.append(ResourceObjectMeta.resource_format.in_(resource_format))

    if resource_keyword:
        all_conditions.append(ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%"))
    # join后会出现一个resource多条记录
    build_resources = ResourceObjectMeta.query.filter(
        *all_conditions
    ).join(
        RagRefInfo,
        RagRefInfo.resource_id == ResourceObjectMeta.id
    ).with_entities(
        ResourceObjectMeta,
        RagRefInfo,
    )
    if resource_tags:
        user_tags = ResourceTag.query.filter(
            ResourceTag.user_id == user_id,
            ResourceTag.tag_status == "正常",
            ResourceTag.id.in_(resource_tags)
        ).all()
        legal_tags = [tag.id for tag in user_tags]
        build_resources = build_resources.join(
            ResourceTagRelation,
            ResourceTagRelation.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceTagRelation.tag_id.in_(legal_tags)
        ).with_entities(
            ResourceObjectMeta,
            RagRefInfo,
        )

    all_resources_results = build_resources.order_by(
        ResourceObjectMeta.create_time.desc(),
        RagRefInfo.update_time.desc()
    ).all()
    # 组装返回结果
    res = []
    exist_map = {}
    index = 0
    # 去重组装
    for resource, rag_info in all_resources_results:
        if resource.id not in exist_map:
            exist_map[resource.id] = index
            res.append({
                "rag_info": [rag_info.to_dict()],
                "resource": resource.show_info() if resource else {}
            })
            index += 1
        else:
            res[exist_map[resource.id]]["rag_info"].append(rag_info.to_dict())

    if not fetch_all:
        res = res[(page_num - 1) * page_size: page_num * page_size]
    return next_console_response(result={
        "data": res,
        "total": index
    })


def search_by_resource_types(params):
    """
    按资源种类进行搜索，返回资源列表,后续可以根据不同种类进行优化处理
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_type = params.get("resource_type", [])
    resource_format = params.get("resource_format", [])
    resource_tags = params.get("resource_tags", [])
    resource_keyword = params.get("resource_keyword", "")
    rag_enhance = params.get("rag_enhance", False)
    duration = params.get("duration", 3000)
    page_size = params.get("page_size", 50)
    page_num = params.get("page_num", 1)
    fetch_all = params.get("fetch_all", False)

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    now_time = datetime.now()
    begin_time = now_time - timedelta(days=duration)

    # 获取资源索引构建任务，补充索引失败信息
    all_conditions = [
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.create_time >= begin_time,
        ResourceObjectMeta.resource_status == '正常',
        ResourceObjectMeta.resource_source == "resource_center"
    ]

    if resource_type:
        all_conditions.append(ResourceObjectMeta.resource_type.in_(resource_type))

    if resource_format:
        all_conditions.append(ResourceObjectMeta.resource_format.in_(resource_format))

    if resource_keyword:
        all_conditions.append(ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%"))

    all_resources = ResourceObjectMeta.query.filter(*all_conditions)
    if resource_tags:
        user_tags = ResourceTag.query.filter(
            ResourceTag.user_id == user_id,
            ResourceTag.tag_status == "正常",
            ResourceTag.id.in_(resource_tags)
        ).all()
        legal_tags = [tag.id for tag in user_tags]
        all_resources = all_resources.join(
            ResourceTagRelation,
            ResourceTagRelation.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceTagRelation.tag_id.in_(legal_tags)
        ).with_entities(
            ResourceObjectMeta
        )

    # todo 启用rag增强的话，调用rag接口匹配资源
    if rag_enhance:
        pass
    all_resources_results = all_resources.order_by(
        ResourceObjectMeta.create_time.desc()
    )
    # 组装返回结果
    total = all_resources_results.count()
    if not fetch_all:
        res = all_resources_results.paginate(page=page_num, per_page=page_size, error_out=False)
    else:
        res = all_resources_results.all()
    res = [resource.show_info() for resource in res]
    return next_console_response(result={
        "data": res,
        "total": total
    })


def search_by_resource_tags(params):
    """
    根据用户自定义标签进行搜索
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_type = params.get("resource_type", [])
    resource_format = params.get("resource_format", [])
    resource_tags = params.get("resource_tags", [])
    resource_keyword = params.get("resource_keyword", "")
    rag_enhance = params.get("rag_enhance", False)
    duration = params.get("duration", 30)
    page_size = params.get("page_size", 50)
    page_num = params.get("page_num", 1)
    fetch_all = params.get("fetch_all", False)

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    now_time = datetime.now()
    begin_time = now_time - timedelta(days=duration)

    # 获取资源索引构建任务，补充索引失败信息
    all_conditions = [
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.create_time >= begin_time,
        ResourceObjectMeta.resource_status == '正常',
        ResourceObjectMeta.resource_source == "resource_center"
    ]

    if resource_type:
        all_conditions.append(ResourceObjectMeta.resource_type.in_(resource_type))

    if resource_format:
        all_conditions.append(ResourceObjectMeta.resource_format.in_(resource_format))

    if resource_keyword:
        all_conditions.append(ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%"))

    all_resources = ResourceObjectMeta.query.filter(*all_conditions)
    if resource_tags:
        user_tags = ResourceTag.query.filter(
            ResourceTag.user_id == user_id,
            ResourceTag.tag_status == "正常",
            ResourceTag.id.in_(resource_tags)
        ).all()
        legal_tags = [tag.id for tag in user_tags]
        all_resources = all_resources.join(
            ResourceTagRelation,
            ResourceTagRelation.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceTagRelation.tag_id.in_(legal_tags)
        ).with_entities(
            ResourceObjectMeta
        )

    # todo 启用rag增强的话，调用rag接口匹配资源
    if rag_enhance:
        pass
    all_resources_results = all_resources.order_by(
        ResourceObjectMeta.create_time.desc()
    )
    # 组装返回结果
    total = all_resources_results.count()
    if not fetch_all:
        res = all_resources_results.paginate(page=page_num, per_page=page_size, error_out=False)
    else:
        res = all_resources_results.all()
    # 获取资源对应的所有用户标签
    all_resource_id = [resource.id for resource in res]
    all_resource_tag_rels = ResourceTagRelation.query.filter(
        ResourceTagRelation.resource_id.in_(all_resource_id),
        ResourceTagRelation.rel_status == "正常"
    ).all()
    resource_tag_map = {}
    for tag_rel in all_resource_tag_rels:
        if tag_rel.resource_id not in resource_tag_map:
            resource_tag_map[tag_rel.resource_id] = []
        resource_tag_map[tag_rel.resource_id].append(tag_rel.tag_id)
    all_tags_id = list(set([tag_rel.tag_id for tag_rel in all_resource_tag_rels]))
    all_tags = ResourceTag.query.filter(
        ResourceTag.id.in_(all_tags_id)
    ).all()
    tags = [tag.to_dict() for tag in all_tags]
    new_res = []
    for resource in res:
        resource_info = resource.show_info()
        resource_info["resource_tags"] = list(set(resource_tag_map.get(resource.id, [])))
        new_res.append(resource_info)
    return next_console_response(result={
        "data": new_res,
        "total": total,
        "resource_tags": tags
    })


def search_by_keyword_in_resource(params):
    """
    在指定目录根据关键字进行搜索,需分页
    只搜索个人资源，若未提供resource_id则搜索所有个人资源，否则根据资源ID递归搜索子资源
    :param params: 参数字典，包含用户ID、资源ID、关键字等
    :return: 分页后的搜索结果
    """
    user_id = int(params.get("user_id"))  # 用户ID
    resource_id = params.get("resource_id")  # 指定的父资源ID，可选
    resource_keyword = params.get("resource_keyword")  # 搜索关键字
    resource_type = params.get("resource_type", [])  # 资源类型过滤条件
    resource_format = params.get("resource_format", [])  # 资源格式过滤条件
    resource_tags = params.get("resource_tags", [])  # 资源标签过滤条件
    rag_enhance = params.get("rag_enhance", False)  # 是否启用RAG增强
    # 处理分页参数，设置默认值
    try:
        page_size = int(params.get("page_size", 50))  # 每页数量
        page_num = int(params.get("page_num", 1))  # 页码
    except ValueError:
        page_size = 50
        page_num = 1
    # 验证用户是否存在
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    # 如果提供了resource_id，验证资源是否存在且属于该用户
    if resource_id:
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource_id,
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == '正常'
        ).first()
        if not target_resource:
            return next_console_response(error_status=True, error_message="资源不存在或不属于用户！")

    def get_all_subresource_ids(resource_parent_id, visited=None):
        # 递归获取所有子资源的ID（不包含当前resource_id）
        # 如果visited为None，初始化一个空集合用于记录已访问的资源ID
        if visited is None:
            visited = set()
        resource_ids = []  # 不包含父ID本身
        # 避免重复处理已经访问过的资源
        if resource_parent_id in visited:
            return resource_ids
        # 标记当前资源为已访问
        visited.add(resource_parent_id)
        sub_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.resource_parent_id == resource_parent_id,
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == '正常'
        ).all()
        for sub_res in sub_resources:
            resource_ids.append(sub_res.id)  # 添加当前子资源ID
            # 递归添加更深层的子资源
            resource_ids.extend(get_all_subresource_ids(sub_res.id, visited))
        return resource_ids
    # 构建查询条件
    all_conditions = [
        ResourceObjectMeta.user_id == user_id,  # 限定用户
        ResourceObjectMeta.resource_status == '正常',  # 资源状态正常
        or_(
            ResourceObjectMeta.resource_name.like(f"%{resource_keyword}%"),  # 资源名称模糊匹配
            ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%"),  # 资源描述模糊匹配
        )
    ]
    # 如果提供了resource_id，则限定在子资源范围内
    all_resource_ids = []
    if resource_id:
        all_resource_ids = get_all_subresource_ids(resource_id)
        if not all_resource_ids:  # 如果没有子资源，直接返回空结果
            return next_console_response(result={
                "data": [],
                "total": 0,
                "resource_tags": [],
                "author_info": {}
            })
        all_conditions.append(ResourceObjectMeta.id.in_(all_resource_ids))
    # 添加资源类型和格式的过滤条件
    if resource_type:
        all_conditions.append(ResourceObjectMeta.resource_type.in_(resource_type))
    if resource_format:
        all_conditions.append(ResourceObjectMeta.resource_format.in_(resource_format))
    # 查询资源
    all_resources = ResourceObjectMeta.query.filter(*all_conditions)
    # 如果指定了标签，则加入标签过滤
    if resource_tags:
        user_tags = ResourceTag.query.filter(
            ResourceTag.user_id == user_id,
            ResourceTag.tag_status == "正常",
            ResourceTag.id.in_(resource_tags)
        ).all()
        legal_tags = [tag.id for tag in user_tags]
        all_resources = all_resources.join(
            ResourceTagRelation,
            ResourceTagRelation.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceTagRelation.tag_id.in_(legal_tags)
        ).with_entities(
            ResourceObjectMeta
        )
    # 先获取总数和所有结果，再进行分页
    total = all_resources.count()
    res = all_resources.order_by(
        ResourceObjectMeta.create_time.desc()  # 按创建时间降序排序
    ).all()
    # 获取资源对应的标签信息
    all_resource_id = [resource.id for resource in res]
    all_resource_tag_rels = ResourceTagRelation.query.filter(
        ResourceTagRelation.resource_id.in_(all_resource_id),
        ResourceTagRelation.rel_status == "正常"
    ).all()
    resource_tag_map = {}
    for tag_rel in all_resource_tag_rels:
        if tag_rel.resource_id not in resource_tag_map:
            resource_tag_map[tag_rel.resource_id] = []
        resource_tag_map[tag_rel.resource_id].append(tag_rel.tag_id)

    all_tags_id = list(set([tag_rel.tag_id for tag_rel in all_resource_tag_rels]))
    all_tags = ResourceTag.query.filter(
        ResourceTag.id.in_(all_tags_id)
    ).all()
    tags = [tag.to_dict() for tag in all_tags]
    # 格式化资源信息
    new_res = []
    for resource in res:
        resource_info = resource.show_info()
        resource_info["resource_tags"] = list(set(resource_tag_map.get(resource.id, [])))
        new_res.append(resource_info)
    # 如果启用RAG增强
    if rag_enhance:
        rag_res = search_rag_enhanced({
            "user_id": user_id,
            "resource_keyword": resource_keyword
        })
        for rag_item in rag_res:
            # 如果未指定resource_id，或rag结果在指定范围内，则加入结果
            if not resource_id or (rag_item.get("id") in all_resource_ids):
                if rag_item.get("id") not in [r["id"] for r in new_res]:
                    new_res.append(rag_item)
                    total += 1
                for item in new_res:
                    if item.get("id") == rag_item.get("id"):
                        item["rerank_score"] = rag_item.get("rerank_score")
                        item["ref_text"] = rag_item.get("ref_text")
                        break
        new_res = sorted(new_res, key=lambda x: x.get("rerank_score", 0), reverse=True)
    # 计算分页数据
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    if start_index >= len(new_res):
        paged_data = []
    else:
        paged_data = new_res[start_index:end_index]
    return next_console_response(result={
        "data": paged_data,  # 分页后的数据
        "total": total,  # 总记录数
        "resource_tags": tags,  # 相关标签信息
        "author_info": {}  # 个人资源无需作者信息
    })


def search_by_resource_keyword(params):
    """
    根据关键字进行搜索,需分页, 包括共享资源
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    resource_type = params.get("resource_type", [])
    resource_format = params.get("resource_format", [])
    resource_tags = params.get("resource_tags", [])
    resource_keyword = params.get("resource_keyword")
    rag_enhance = params.get("rag_enhance", False)
    auth_type = params.get("auth_type")
    try:
        page_size = int(params.get("page_size", 50))
        page_num = int(params.get("page_num", 1))
    except ValueError:
        page_size = 50
        page_num = 1
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id
    ).first()

    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")

    all_conditions = [
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_status == '正常',
        ResourceObjectMeta.resource_source == "resource_center",
        or_(
            ResourceObjectMeta.resource_name.like(f"%{resource_keyword}%"),
            ResourceObjectMeta.resource_desc.like(f"%{resource_keyword}%"),
        )
    ]
    if resource_type:
        all_conditions.append(ResourceObjectMeta.resource_type.in_(resource_type))

    if resource_format:
        all_conditions.append(ResourceObjectMeta.resource_format.in_(resource_format))
    all_resources = ResourceObjectMeta.query.filter(*all_conditions)
    if resource_tags:
        user_tags = ResourceTag.query.filter(
            ResourceTag.user_id == user_id,
            ResourceTag.tag_status == "正常",
            ResourceTag.id.in_(resource_tags)
        ).all()
        legal_tags = [tag.id for tag in user_tags]
        all_resources = all_resources.join(
            ResourceTagRelation,
            ResourceTagRelation.resource_id == ResourceObjectMeta.id
        ).filter(
            ResourceTagRelation.tag_id.in_(legal_tags)
        ).with_entities(
            ResourceObjectMeta
        )
    # 先获取所有结果，最后再进行分页
    total = all_resources.count()
    res = all_resources.order_by(
        ResourceObjectMeta.create_time.desc()
    ).all()
    # 获取资源对应的所有用户标签
    all_resource_id = [resource.id for resource in res]
    all_resource_tag_rels = ResourceTagRelation.query.filter(
        ResourceTagRelation.resource_id.in_(all_resource_id),
        ResourceTagRelation.rel_status == "正常"
    ).all()
    resource_tag_map = {}
    for tag_rel in all_resource_tag_rels:
        if tag_rel.resource_id not in resource_tag_map:
            resource_tag_map[tag_rel.resource_id] = []
        resource_tag_map[tag_rel.resource_id].append(tag_rel.tag_id)
    all_tags_id = list(set([tag_rel.tag_id for tag_rel in all_resource_tag_rels]))
    all_tags = ResourceTag.query.filter(
        ResourceTag.id.in_(all_tags_id)
    ).all()
    tags = [tag.to_dict() for tag in all_tags]
    new_res = []

    for resource in res:
        resource_info = resource.show_info()
        resource_info["resource_tags"] = list(set(resource_tag_map.get(resource.id, [])))
        resource_info["auth_type"] = "manage"
        new_res.append(resource_info)

    if rag_enhance:
        rag_res = search_rag_enhanced({
            "user_id": user_id,
            "resource_keyword": resource_keyword,
            "resource_source": "resource_center",
        })

        # merge 入 new_res
        for rag_item in rag_res:
            if rag_item.get("id") not in all_resource_id:
                rag_item["auth_type"] = "manage"
                new_res.append(rag_item)
                total += 1
            for item in new_res:
                if item.get("id") == rag_item.get("id"):
                    item["rerank_score"] = rag_item.get("rerank_score")
                    item["ref_text"] = rag_item.get("ref_text")
                    break
        # 根据rerank_score排序
        new_res = sorted(new_res, key=lambda x: x.get("rerank_score", 0), reverse=True)
    # 默认同时搜索共享资源
    share_res = search_share_resource_by_keyword(params).json.get("result", {})

    share_data = share_res.get("data", [])
    for share_resource in share_data:
        find_flag = False
        for item in new_res:
            if item.get("id") == share_resource.get("id"):
                find_flag = True
                break
        if not find_flag:
            share_resource["auth_type"] = share_resource.get("auth_type", "read")
            new_res.append(share_resource)
            total += 1

    # 内部函数：根据 auth_type 筛选资源
    def filter_by_auth_type(resources, auth_type, permission_levels):
        # 定义权限等级（从低到高）
        required_level = permission_levels.get(auth_type, 0)
        new_filter_resources = []
        for item in resources:
            if permission_levels.get(item["auth_type"], 0) >= required_level > 0:
                new_filter_resources.append(item)
        return new_filter_resources
    if auth_type:
        permission_levels = {
            "read": 1,
            "download": 2,
            "edit": 3,
            "manage": 4
        }
        new_res = filter_by_auth_type(new_res, auth_type, permission_levels)
    # 计算分页数据
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    if start_index >= len(new_res):
        paged_data = []
    else:
        paged_data = new_res[start_index:end_index]
    return next_console_response(result={
        "data": paged_data,
        "total": total,
        "resource_tags": tags,
        "author_info": share_res.get("author_info", {})
    })


def search_rag_enhanced(params):
    user_id = int(params.get("user_id", 0))
    resource_keyword = params.get("resource_keyword")
    all_resource_id = params.get("all_resource_id", [])
    resource_source = params.get("resource_source")
    all_conditions = [RagRefInfo.ref_status == "成功"]
    if user_id:
        all_conditions.append(RagRefInfo.user_id == user_id)
    if all_resource_id:
        all_conditions.append(RagRefInfo.resource_id.in_(all_resource_id))

    all_rag_ref = RagRefInfo.query.filter(*all_conditions).all()
    if not all_rag_ref:
        return []
    all_rag_ref_ids = [i.id for i in all_rag_ref]
    rag_params = {
        "user_id": user_id,
        "query": resource_keyword,
        "ref_ids": all_rag_ref_ids,
        "config": {
            "search_engine_enhanced": False,
            "rerank_enabled": False,
        }
    }
    try:
        t1 = time.time()
        rag_response = rag_query_v3(rag_params).json.get("result", {})
        details = rag_response.get("details", [])
        if not details:
            return []
        all_resource_id = list(set([i.get("meta").get("source") for i in details]))
        # 获取所有对应资源
        all_md_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id.in_(all_resource_id),
            ResourceObjectMeta.resource_status == "正常"
        ).all()
        all_md_resource_ids = list(set([i.resource_parent_id for i in all_md_resources if i.resource_parent_id]))
        md_map = {resource.id: resource.resource_parent_id for resource in all_md_resources}
        all_resources_conditions = [
            ResourceObjectMeta.id.in_(all_md_resource_ids),
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_type != 'folder'
        ]
        if resource_source:
            all_resources_conditions.append(ResourceObjectMeta.resource_source == resource_source)
        all_ref_resources = ResourceObjectMeta.query.filter(*all_resources_conditions).all()
        res = []
        for resource in all_ref_resources:
            # 从detail中获取rerank_score最高的 text
            resource_dict = resource.show_info()
            # 补充 ref_text（第一条）
            for detail in details:
                if resource.id == md_map.get(detail.get("meta").get("source")):
                    resource_dict["rerank_score"] = detail.get("rerank_score") or detail.get("recall_score")
                    resource_dict["ref_text"] = detail.get("text")
                    break
            res.append(resource_dict)
        return res
    except Exception as e:
        print(e)
        return []


def create_new_document(params):
    """
    创建新文档资源
        根据条件新建元数据，通过复制写入数据，返回元数据信息
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_resource_parent_id = params.get("resource_parent_id")
    target_resource_name = params.get("resource_name", "")
    target_resource_desc = params.get("resource_desc", "")
    target_resource_type = params.get("resource_type", "")
    target_resource_format = params.get("resource_format", "")
    target_user = UserInfo.query.filter(
            UserInfo.user_id == user_id
        ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    # 检查主目录是否存在
    if not target_user.user_resource_base_path:
        return next_console_response(error_status=True, error_message="存储空间异常！")
    if not os.path.exists(target_user.user_resource_base_path):
        os.mkdir(target_user.user_resource_base_path, )
    document_template_path = os.path.join(app.config['config_static'], f"empty.{target_resource_format}")
    if not os.path.exists(document_template_path):
        app.logger.warning(f"模板文件损坏！f{document_template_path}")
        return next_console_response(error_status=True, error_message="模板文件损坏！")
    if not target_resource_parent_id:
        root_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_parent_id.is_(None)
        ).first()
        if not root_resource:
            return next_console_response(error_status=True, error_message="根目录不存在！")
        target_resource_parent_id = root_resource.id
    try:
        new_resource_path = generate_resource_path(
            user_resource_base_path=target_user.user_resource_base_path,
            target_resource_parent_id=target_resource_parent_id,
        )
    except Exception as e:
        return next_console_response(error_status=True, error_message=f"生成资源路径异常：{e.args}")

    # 文档自动重命名
    same_dir_resources = ResourceObjectMeta.query.filter(
        ResourceObjectMeta.user_id == user_id,
        ResourceObjectMeta.resource_parent_id == target_resource_parent_id,
        ResourceObjectMeta.resource_status == "正常"
    ).all()
    if same_dir_resources:
        same_dir_resource_name_list = [resource.resource_name for resource in same_dir_resources]
        base_name = target_resource_name
        extension = target_resource_format
        new_resource_name = f"{base_name}.{extension}"
        reindex = 1
        while new_resource_name in same_dir_resource_name_list:
            base_name = f"{target_resource_name}({reindex})"
            new_resource_name = f"{base_name}.{extension}"
            reindex += 1
        target_resource_name = base_name
    resource_size_in_MB = int(os.path.getsize(document_template_path) / 1024/1024)
    new_resource = ResourceObjectMeta(
        resource_parent_id=target_resource_parent_id,
        user_id=user_id,
        resource_name=f"{target_resource_name}.{target_resource_format}",
        resource_desc=target_resource_desc,
        resource_type=target_resource_type,
        resource_icon=f"{target_resource_format}.svg",
        resource_path=new_resource_path,
        resource_source='resource_center',
        resource_size_in_MB=resource_size_in_MB,
        resource_format=target_resource_format,

    )
    db.session.add(new_resource)
    db.session.commit()
    import shutil
    try:
        shutil.copyfile(document_template_path, new_resource_path)
    except Exception as e:
        app.logger.warning(f"创建模板资源异常：{e}")
        return next_console_response(error_status=True, error_message="新建模板文件异常")
    return next_console_response(result=new_resource.show_info())


def simple_upload_resource(params, data):
    """
    简单上传资源
    Parameters
    ----------
    params

    Returns
    -------

    """
    user_id = int(params.get("user_id"))
    auto_index = params.get("auto_index")
    try:
        resource_parent_id = int(params.get("resource_parent_id"))
    except Exception:
        resource_parent_id = None
    filename = data.filename
    resource_type, resource_format = guess_resource_type(filename)
    new_resource_path = generate_new_path(
        module_name='resource_center',
        user_id=user_id,
        suffix=resource_format
    ).json.get("result")
    with open(new_resource_path, "wb") as f:
        f.write(data.read())
    # # 生成下载链接
    resource_show_url = generate_download_url(
        module_name="resource_center",
        file_path=new_resource_path,
        suffix=resource_format,
    ).json.get("result")
    if not resource_parent_id:
        user_folder = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_parent_id.is_(None),
            ResourceObjectMeta.resource_status == "正常",
            ResourceObjectMeta.resource_source == "resource_center"
        ).first()
        resource_parent_id = user_folder.id
    new_resource = ResourceObjectMeta(
        user_id=user_id,
        resource_parent_id=resource_parent_id,
        resource_name=filename,
        resource_type=resource_type,
        resource_format=resource_format,
        resource_size_in_MB=os.path.getsize(new_resource_path) / 1024 / 1024,
        resource_path=new_resource_path,
        resource_source_url=resource_show_url,
        resource_show_url=resource_show_url,
        resource_status="正常",
        resource_source='resource_center'
    )
    db.session.add(new_resource)
    db.session.commit()
    # 满足条件后，提交自动构建任务
    user_config = get_user_config(user_id).json.get("result")
    if auto_index is True or (auto_index is None and user_config and user_config["resources"]["auto_rag"]):
        # 判断类型是否支持构建
        if check_rag_is_support(new_resource):
            build_params = {
                "user_id": user_id,
                "resource_id": new_resource.id
            }
            auto_build_resource_ref_v2.delay(build_params)
    return next_console_response(result={
        "id": new_resource.id,
        "name": new_resource.resource_name,
        "url": new_resource.resource_show_url
    })
