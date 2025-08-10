import os.path
import time
from datetime import datetime, timedelta, timezone
import hashlib
from sqlalchemy import or_
import json
import uuid
import tldextract
from app.app import celery, app, db
from app.models.user_center.user_info import UserInfo
from app.models.next_console.next_console_model import SessionAttachmentRelation
from app.app import redis_client, socketio
import asyncio
import smtplib
from email.mime.text import MIMEText
from jinja2 import Template
from app.models.resource_center.share_resource_model import ResourceDownloadCoolingRecord
from app.utils.oss.oss_client import get_download_url_path, generate_new_path, generate_download_url
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.models.knowledge_center.rag_ref_model import RagRefInfo
import gevent


@celery.task
def emit_resource_status(params):

    """
    推送资源状态
    :param params:
    :return:
    """
    with app.app_context():
        user_id = int(params.get("user_id"))
        resource_id = params.get("resource_id")
        rag_status = params.get("rag_status")
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource_id,
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status.in_(["正常", "异常"])
        ).first()
        if not target_resource:
            return "资源不存在"
        # 推送构建信息
        all_user_clients = redis_client.get(user_id)
        if not all_user_clients:
            return "无在线用户"
        all_user_clients = json.loads(all_user_clients)
        for client in all_user_clients:
            if client.get('status') == 'connected':
                data = target_resource.show_info()
                data["rag_status"] = rag_status
                socketio.emit("updateRefStatus", [data], room=client.get('session_id'))
        return f'推送资源状态成功{target_resource.show_info()}'


@celery.task
def clean_resource_file(params):
    """
    清理资源文件
    :param params:
    :return:
    """
    with app.app_context():
        resource_paths = params.get("resource_paths")
        for resource_path in resource_paths:
            # 删除文件
            if os.path.exists(resource_path):
                os.remove(resource_path)
        return resource_paths


@celery.task
def attachment_multiple_webpage_tasks(params):
    """
    一次性完成多个网页获取任务
        根据配置和网页类型进行分类处理
    :param params:
    :return:
    """
    with app.app_context():
        user_id = int(params.get("user_id"))
        resource_list = params.get("resource_list")
        session_id = params.get("session_id")
        driver = params.get("driver", "playwright")
        target_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id.in_(resource_list),
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == '正常'
        ).all()
        if not target_resources:
            return "资源不存在"
        from app.services.knowledge_center.webpage_fetch import fetch_page_content_main
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果事件循环正在运行，使用asyncio.ensure_future
                asyncio.run_coroutine_threadsafe(fetch_page_content_main(target_resources, session_id, driver=driver),
                                                 loop)
        except Exception as e:
            print(f"Error in asyncio event loop: {e}")
            try:
                asyncio.run(fetch_page_content_main(target_resources, session_id, driver=driver))
            except Exception as e:
                return f"Error fetching page content: {e}"

        # fetch_page_content_main(target_resources, session_id, driver=driver)
        # target_resources = [
        #     resource.to_dict() for resource in target_resources
        # ]
        # coroutine = gevent.spawn(fetch_page_content_main, target_resources, session_id, driver=driver)
        # gevent.joinall([coroutine])

        # greenlet = spawn(fetch_page_content_main_sync_wrapper,
        #                  target_resources, session_id, driver)

        return "任务完成"


@celery.task
def completely_delete_resources():
    """
    完全删除资源
    :return:
    """
    with app.app_context():
        # 获取删除资源
        delete_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.resource_status == "删除",
            ResourceObjectMeta.delete_time + timedelta(days=75) < datetime.now(timezone.utc)
        ).all()
        if not delete_resources:
            return "无需删除"
        all_finish_task_cnt = 0
        # 删除资源文件
        for delete_resource in delete_resources:
            if os.path.exists(delete_resource.resource_path):
                os.remove(delete_resource.resource_path)
                # 删除数据库记录
                db.session.delete(delete_resource)
                db.session.commit()
                all_finish_task_cnt += 1
        return f"删除完成{all_finish_task_cnt}条"


@celery.task
def send_resource_download_cooling_notice_email(params):
    """
    发送资源下载冷却通知邮件
    :return:
    """
    with app.app_context():
        user_id = int(params.get("user_id"))
        cooling_record_id = params.get("cooling_record_id")
        resource_id = params.get("resource_id")
        cool_user_id = params.get("cool_user_id")
        target_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
        if not target_user:
            return "用户不存在"
        if not target_user.user_email:
            return "用户邮箱不存在"
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource_id
        ).first()
        if not target_resource:
            return "资源不存在"
        cool_user = UserInfo.query.filter(UserInfo.user_id == cool_user_id).first()
        if not cool_user:
            return "冷却用户不存在"
        cooling_record = ResourceDownloadCoolingRecord.query.filter(
            ResourceDownloadCoolingRecord.id == cooling_record_id
        ).first()
        # 发送邮件
        smtp_server = app.config['smtp_server']
        smtp_port = app.config['smtp_port']
        smtp_user = app.config['smtp_user']
        smtp_password = app.config['smtp_password']
        # 配置邮件信息
        from_email = app.config['notice_email']
        subject = '资源下载拦截告警'
        hello_html = "resource_cooling_notice.html"
        with open(os.path.join(app.config["config_static"], hello_html), "r", encoding="utf8") as f:
            info_html = f.read()
        info_html_template = Template(info_html)
        url = f"{app.config['domain']}/#/next_console/resources/resource_cooling/{cooling_record_id}"
        info_params = {
            "cooling_record": cooling_record,
            "url": url,
            "reason": "短时间内下载次数过多，已被系统拦截，请稍后再试",
            "resource_name": target_resource.resource_name,
            "cool_user_name": cool_user.user_nick_name,
            "cool_time": cooling_record.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        info_html = info_html_template.render(info_params)
        # 创建 MIMEText 对象，并设置邮件主题、发件人、收件人
        msg = MIMEText(info_html, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ",".join([target_user.user_email])

        # 连接 SMTP 服务器并发送邮件
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, [target_user.user_email], msg.as_string())
        server.quit()
        cooling_record.author_notice = True
        db.session.add(cooling_record)
        db.session.commit()
        return "邮件发送成功"


@celery.task
def auto_delete_resource_download_url():
    """
    自动删除资源下载链接
    :return:
    """
    with app.app_context():
        # 获取删除资源
        begin_time = datetime.now(timezone.utc) - timedelta(days=30)
        delete_resources = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.resource_status == "正常",
            or_(
                ResourceObjectMeta.resource_download_url.isnot(None),
            ),
            ResourceObjectMeta.update_time >= begin_time,
        ).all()
        if not delete_resources:
            return "无需删除"
        all_finish_task_cnt = 0
        # 删除资源文件
        for delete_resource in delete_resources:
            # 删除下载链接
            if not delete_resource.resource_download_url:
                continue
            target_download_link = get_download_url_path(delete_resource.resource_download_url)
            if target_download_link:
                os.remove(target_download_link)
                all_finish_task_cnt += 1
                delete_resource.resource_download_url = None
                db.session.add(delete_resource)
                db.session.commit()
        return f"删除完成{all_finish_task_cnt}条"


@celery.task
def auto_build_resource_ref_v2(params):
    """
    用户上传后的自动构建资源引用
    ref_status : Init, Uploading, Pending,Success, Failed, Error
    :param params:
    :return:
    """
    with app.app_context():
        user_id = int(params.get("user_id"))
        resource_id = params.get("resource_id")
        target_resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource_id,
            ResourceObjectMeta.user_id == user_id,
            ResourceObjectMeta.resource_status == '正常'
        ).first()
        if not target_resource:
            return "资源不存在"
        # 检查是否已经存在构建记录，删除后重新构建
        exist_refs = RagRefInfo.query.filter(
            RagRefInfo.resource_id == resource_id,
            RagRefInfo.ref_status != "已删除"
        ).all()
        for ref in exist_refs:
            # 删除失败的构建记录
            ref.ref_status = "已删除"
            db.session.add(ref)
        db.session.commit()
        # 启动构建初始化
        # todo 生成各项配置
        file_reader_config = {
            "engine": "pandoc",
            "pandoc_config": {
                "to_format": "markdown",
                "preserve-tabs": True,
                "wrap": "none",
                "mathml": True,
            }
        }
        file_split_config = {
            "method": "length",
            "chunk_size": 2000,
            "length_config": {
                "chunk_overlap": 500,
            },
            "symbol_config": {
                "separators": [],
                "keep_separator": True,
                "merge_chunks": True,
            },
            "layout_config": {
                "merge_chunks": True,
                "preserve_structures": True,
            }
        }
        file_chunk_abstract_config = {
            "image_abstract": False,
            "audio_abstract": False,
            "link_abstract": False,
            "video_abstract": False,
            "table_abstract": False,
            "code_abstract": False,
            "question_abstract": False
        }
        file_chunk_embedding_config = {
            "api":  app.config.get("EMBEDDING_ENDPOINT"),
            'key': app.config.get("EMBEDDING_KEY"),
            "model": app.config.get("EMBEDDING_MODEL"),
            "batch_size": 10,
            "dimension": 1024,
            "encoding_format": "float",
            "media_embedding": False,
            "media_embedding_config": {
                "api": '',
                "key": '',
                "model": '',
            },
        }
        ref_type = "resource"
        pandoc_input_formats = [
            "biblatex", "bibtex", "bits",
            "commonmark", "commonmark_x", "creole", "csljson", "csv",
            "djot", "docbook", "docx", "dokuwiki",
            "endnotexml", "epub",
            "fb2",
            "gfm",
            "haddock", "html",
            "ipynb",
            "jats", "jira",
            "latex",
            "man", "markdown", "markdown_github", "markdown_mmd", "markdown_phpextra", "markdown_strict", "mdoc",
            "mediawiki", "muse",
            "native",
            "odt", "opml", "org",
            "pod",
            "ris", "rst", "rtf",
            "t2t", "textile", "tikiwiki", "tsv", "twiki", "typst",
            "vimwiki",
        ]
        if target_resource.resource_format == "pdf":
            file_reader_config["engine"] = "pymupdf"
            file_reader_config["pymupdf_config"] = {}
        elif target_resource.resource_format in ("html", "shtml", "phtml", "htm"):
            file_reader_config["engine"] = "html2text"
            ref_type = "webpage"
        elif target_resource.resource_format in ("xlsx", "xls"):
            file_reader_config["engine"] = "openpyxl"
            file_reader_config["openpyxl_config"] = {}
        elif target_resource.resource_format == "pptx":
            file_reader_config["engine"] = "python-pptx"
            file_reader_config["python_pptx_config"] = {}
        elif target_resource.resource_format not in pandoc_input_formats:
            file_reader_config["engine"] = "text"

        new_ref_info = RagRefInfo(
            ref_code=str(uuid.uuid4()),
            resource_id=resource_id,
            ref_type=ref_type,
            user_id=user_id,
            file_reader_config=file_reader_config,
            file_split_config=file_split_config,
            file_chunk_abstract_config=file_chunk_abstract_config,
            file_chunk_embedding_config=file_chunk_embedding_config,
            ref_status="初始化"
        )
        db.session.add(new_ref_info)
        db.session.flush()
        ref_id = new_ref_info.id
        db.session.commit()
        # 启动构建
        celery_task = start_ref_task.delay({
            "user_id": user_id,
            "resource_id": resource_id,
            "ref_id": ref_id
        })
        if celery_task:
            new_ref_info.celery_task_id = celery_task.id
            new_ref_info.ref_status = "排队中"
            db.session.add(new_ref_info)
            db.session.commit()
        else:
            return "启动构建任务失败"
        return '启动构建任务成功'


@celery.task
def start_ref_task(params):
    """
    启动RAG-索引构建任务
        支持多任务并发执行
        支持启动任务
        支持获取任务结果
        支持
    """
    with app.app_context():
        from app.services.knowledge_center.rag_service_v3 import file_reader, file_split
        from app.services.knowledge_center.rag_service_v3 import file_chunk_abstract, file_chunk_embedding
        user_id = int(params.get("user_id"))
        resource_id = params.get("resource_id")
        ref_id = params.get("ref_id")
        target_ref = RagRefInfo.query.filter(
            RagRefInfo.id == ref_id
        ).order_by(
            RagRefInfo.create_time.desc()
        ).first()
        # 文件解析
        reader_result = file_reader(params)
        db.session.refresh(target_ref)
        emit_resource_status.delay({
            "user_id": user_id,
            "resource_id": resource_id,
            "rag_status": target_ref.ref_status
        })
        if not (reader_result and isinstance(reader_result, dict) and reader_result.get("content")):
            target_ref.ref_status = "文件解析失败"
            db.session.add(target_ref)
            db.session.commit()
            return f'文件解析失败，请检查文件格式或内容:{reader_result.json.get("error_message")}'
        params["resource_id"] = reader_result["id"]
        params["content"] = reader_result["content"]
        # 文件切分
        split_result = file_split(params)
        db.session.refresh(target_ref)
        emit_resource_status.delay({
            "user_id": user_id,
            "resource_id": resource_id,
            "rag_status": target_ref.ref_status
        })
        if not (split_result and isinstance(split_result, dict) and split_result.get("status") == "success"):
            target_ref.ref_status = "文件切分失败"
            db.session.add(target_ref)
            db.session.commit()
            return f'文件切分失败，请检查文件格式或内容:{split_result.json.get("error_message")}'
        abstract_result = file_chunk_abstract(params)
        db.session.refresh(target_ref)
        emit_resource_status.delay({
            "user_id": user_id,
            "resource_id": resource_id,
            "rag_status": target_ref.ref_status
        })
        if not (abstract_result and isinstance(abstract_result, dict) and abstract_result.get("status") == "success"):
            return '文件摘要处理失败，请检查文件格式或内容'
        embedding_result = file_chunk_embedding(params)
        db.session.refresh(target_ref)
        emit_resource_status.delay({
            "user_id": user_id,
            "resource_id": resource_id,
            "rag_status": target_ref.ref_status
        })
        if not (embedding_result and isinstance(embedding_result, dict) and embedding_result.get("status") == "success"):
            return '文件向量化处理失败，请检查文件格式或内容'
        db.session.refresh(target_ref)
        if target_ref.ref_status == "向量化完成":
            target_ref.ref_status = "成功"
        else:
            target_ref.ref_status = "失败"
        db.session.add(target_ref)
        db.session.commit()
        emit_resource_status.delay({
            "user_id": user_id,
            "resource_id": resource_id,
            "rag_status": target_ref.ref_status
        })
        return '构建任务执行完成'


