
import asyncio
from playwright.sync_api import sync_playwright
from app.app import app, db
import tldextract
import os.path
import hashlib
from app.models.next_console.next_console_model import SessionAttachmentRelation
from app.utils.oss.oss_client import generate_new_path, generate_download_url
from app.models.resource_center.resource_model import ResourceObjectMeta
from concurrent.futures import ThreadPoolExecutor, wait
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_page_content_main(resources, session_id, auto_build=True, driver='playwright'):
    """
    获取多个网页内容
    :param resources:
    :param session_id:
    :param auto_build: 是否自动构建资源引用
    :param driver: 使用的浏览器驱动，默认为playwright
    :return:
    """
    if driver == 'playwright':
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            with ThreadPoolExecutor(max_workers=4) as executor:
                # 使用线程池来并发执行任务
                results = []
                for resource in resources:
                    future = executor.submit(fetch_page_content, browser, resource, session_id,
                                             timeout=6000, max_size=10, auto_build=auto_build
                                             )
                    future.add_done_callback(
                        lambda f: print(f"🎯 Child result: {f.result()}") if f.exception() is None
                        else print(f"❌ Child error: {f.exception()}")
                    )
                    results.append(future)
            # 关闭浏览器
            wait(results)  # 等待所有任务完成
            browser.close()
    else:
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = []
            for resource in resources:
                future = executor.submit(fetch_static_page_content, resource, session_id,
                                         timeout=6000, max_size=10, auto_build=auto_build
                                         )
                future.add_done_callback(
                    lambda f: print(f"🎯 Child result: {f.result()}") if f.exception() is None
                    else print(f"❌ Child error: {f.exception()}")
                )
                results.append(future)
                # 关闭浏览器
            wait(results)  # 等待所有任务完成

    for new_resource in resources:
        db.session.add(new_resource)
    db.session.commit()


def fetch_page_content(browser, resource, session_id, timeout=6000, max_size=10, auto_build=True):
    """
    获取多个网页内容
        支持网页内容的获取，截图
        支持pdf，docx等文件的下载
    :param browser:
    :param resource:
    :param session_id:
    :param timeout: 超时时间
    :param max_size: 最大资源大小，单位为MB
    :return:
    """
    with app.app_context():
        from app.services.configure_center.response_utils import next_console_response
        resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource.id
        ).first()
        if not resource:
            return next_console_response(
                error_status=True,
                error_message="资源不存在或者已被删除"
            )
        document_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        # 导航到指定的URL
        try:
            # 使用请求拦截
            page.route('**/*', lambda route, request: handle_request(route, request, max_size=max_size))
            page.goto(resource.resource_source_url, timeout=timeout)
            page.wait_for_load_state('domcontentloaded')
        except Exception as e:
            resource.resource_desc = f'页面加载异常：{e}'
            db.session.add(resource)
            db.session.commit()
        if resource.resource_source_url.lower().split(".")[-1] in document_extensions:
            with page.expect_download(timeout=timeout) as download_info:
                page.click('body')
            download = download_info.value
            download.save_as(resource.resource_path)
        else:
            content = page.content()
            title = page.title()
            icon_url = page.evaluate("""
                () => {
                    const link = document.querySelector('link[rel="icon"]') || 
                                 document.querySelector('link[rel="shortcut icon"]');
                    return link ? link.href : null;
                }
            """)
            # 更新资源
            if content:
                with open(resource.resource_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        if title:
            resource.resource_name = title
            resource.resource_title = title
        if icon_url:
            resource.resource_icon = icon_url
        extract_res = tldextract.extract(url=resource.resource_source_url)
        resource.resource_source_url_site = f"{extract_res.domain}.{extract_res.suffix}"
        resource.resource_size_in_MB = os.path.getsize(resource.resource_path) / 1024 / 1024
        with open(resource.resource_path, 'rb') as f:
            resource.resource_feature_code = hashlib.sha256(f.read()).hexdigest()
        db.session.add(resource)
        db.session.commit()
        if session_id:
            # 保存截图为图片型资源
            screenshot = page.screenshot(full_page=True, timeout=1000)
            new_resource_path = generate_new_path(
                module_name="session",
                user_id=resource.user_id,
            ).json.get("result")
            with open(new_resource_path, 'wb') as f:
                f.write(screenshot)
            resource_feature_code = hashlib.sha256(screenshot).hexdigest()
            # 生成下载链接
            resource_show_url = generate_download_url(
                module_name="session",
                file_path=new_resource_path,
                suffix="png",
            ).json.get("result")
            new_resource = ResourceObjectMeta(
                resource_parent_id=resource.resource_parent_id,
                user_id=resource.user_id,
                resource_name=f"{resource.resource_name}.png",
                resource_title=resource.resource_title,
                resource_desc=resource.resource_desc,
                resource_icon=resource.resource_icon,
                resource_type="image",
                resource_format="png",
                resource_size_in_MB=os.path.getsize(new_resource_path) / 1024 / 1024,
                resource_path=new_resource_path,
                resource_source_url=resource.resource_source_url,
                resource_source_url_site=resource.resource_source_url_site,
                resource_show_url=resource_show_url,
                resource_feature_code=resource_feature_code,
                resource_status="正常",
                resource_source='session'
            )
            db.session.add(new_resource)
            db.session.commit()
            # 增加到会话附件中去
            new_attachment = SessionAttachmentRelation(
                session_id=session_id,
                resource_id=new_resource.id,
                attachment_source="webpage",
                rel_status="正常"
            )
            db.session.add(new_attachment)
            db.session.commit()
        page.close()
        context.close()
        if auto_build:
            from app.services.task_center.resources_center import auto_build_resource_ref_v2
            auto_build_resource_ref_v2.delay({
                "user_id": resource.user_id,
                "resource_id": resource.id,
            })
            return resource


def handle_request(route, request, max_size=10):
    """
    拦截压缩包资源
    拦截超过20m的资源
    :param route:
    :param request:
    :param max_size: 最大资源大小，单位为MB
    :return:
    """
    url = request.url.lower()
    headers = request.headers
    # 检查 URL 是否是非 HTML 内容（例如压缩包）
    non_html_extensions = ['.zip', '.rar', '.tar', '.gz', '.7z']

    if any(url.endswith(ext) for ext in non_html_extensions):
        # 取消请求
        route.abort()
        return
    content_length = headers.get('content-length')
    if content_length and int(content_length) > max_size * 1024 * 1024:
        route.abort()
        return
    route.continue_()


def get_url_format(url):
    try:
        page_name = url.split('/')[-1]
        page_format = page_name.split('.')[-1].lower()
        if len(page_format) >= 8 or not page_format or "." not in page_name:
            page_format = 'html'
    except Exception as e:
        page_format = 'html'
    return page_format


def fetch_static_page_content(resource, session_id, timeout=6000, max_size=10, auto_build=True):
    """
    使用 requests库获取静态网页内容
    """
    with app.app_context():
        from app.services.configure_center.response_utils import next_console_response
        resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource.id
        ).first()
        if not resource:
            return next_console_response(
                error_status=True,
                error_message="资源不存在或者已被删除"
            )
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.tianyancha.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
        }
        document_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']
        if resource.resource_format in document_extensions:
            try:
                response = requests.get(
                    resource.resource_source_url,
                    stream=True,
                    headers=headers,
                    timeout=timeout / 1000  # 毫秒转秒
                )
                response.raise_for_status()
                with open(resource.resource_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            except requests.RequestException as e:
                resource.resource_desc = f'页面加载异常：{e}'
                db.session.add(resource)
                db.session.commit()
                return next_console_response(
                    error_status=True,
                    error_message=f"页面加载异常：{e}"
                )
        else:
            try:
                response = requests.get(
                    resource.resource_source_url,
                    headers=headers,
                    timeout=timeout / 1000  # 毫秒转秒
                )
                response.raise_for_status()
                content = response.text
                with open(resource.resource_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except requests.RequestException as e:
                resource.resource_desc = f'页面加载异常：{e}'
                db.session.add(resource)
                db.session.commit()
                return next_console_response(
                    error_status=True,
                    error_message=f"页面加载异常：{e}"
                )
            if content:
                page_metadata = parse_page_metadata(content, base_url=resource.resource_source_url)
                resource.resource_icon = page_metadata.get('icon')
                resource.resource_title = page_metadata.get('title') or resource.resource_title
        extract_res = tldextract.extract(url=resource.resource_source_url)
        resource.resource_source_url_site = f"{extract_res.domain}.{extract_res.suffix}"
        resource.resource_size_in_MB = os.path.getsize(resource.resource_path) / 1024 / 1024
        with open(resource.resource_path, 'rb') as f:
            resource.resource_feature_code = hashlib.sha256(f.read()).hexdigest()
        db.session.add(resource)
        db.session.commit()
        if auto_build:
            from app.services.task_center.resources_center import auto_build_resource_ref_v2
            auto_build_resource_ref_v2.delay({
                "user_id": resource.user_id,
                "resource_id": resource.id,
            })
            return resource


def parse_page_metadata(html_text, base_url=None):
    """
    从HTML文本解析标题和图标链接
    :param html_text: 网页HTML内容
    :param base_url: 用于拼接相对路径的基准URL（可选）
    :return: dict {title, icon}
    """
    soup = BeautifulSoup(html_text, 'html.parser')

    # 解析标题
    title = soup.title.string if soup.title else None

    # 解析图标（优先顺序：icon -> shortcut icon -> 默认/favicon.ico）
    icon_link = None
    for rel in ['icon', 'shortcut icon']:
        tag = soup.find('link', rel=rel)
        if tag and tag.get('href'):
            icon_link = tag['href']
            if base_url:
                icon_link = urljoin(base_url, icon_link)
            break

    # 如果没有找到link标签，尝试默认favicon.ico
    if not icon_link and base_url:
        icon_link = urljoin(base_url, '/favicon.ico')

    return {
        'title': title,
        'icon': icon_link
    }