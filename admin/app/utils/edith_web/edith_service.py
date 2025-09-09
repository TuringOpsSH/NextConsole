from app.services.configure_center.response_utils import next_console_response
from app.app import db, app
from app.utils.oss.oss_client import generate_download_url, generate_new_path
from app.models.user_center.user_info import UserInfo
from .edith_model import *
import uuid
from sqlalchemy import or_
import os
import zipfile
import sys
from pathlib import Path
import time
from datetime import datetime
import shutil
import subprocess
from app.services.task_center.edith_web import start_generate_report
import requests
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.models.next_console.next_console_model import SessionAttachmentRelation, NextConsoleSession
import hashlib
import platform
import stat


edith_support_software = {
    "linux-common": 'Linux健康检查报告',
    "windows-common": "Windows健康检查报告",
    "oracle-common": 'Oracle健康检查报告',
    "mysql-common": 'MySQL健康检查报告',
    "pg-common": "pg健康检查报告",
    "sqlserver-common": "SQL Server 健康检查汇总报告",
    "mongo-common": "Mongo健康检查报告",
    "dm-common": "DM数据库健康检查报告",
    "apache-common": "Apache健康检查报告",
    "nginx-common": "Nginx健康检查报告",
    "tomcat-common": "Tomcat健康检查报告",
    "was-common": "WAS健康检查报告",
    "wls-common": "WebLogic健康检查报告",
    "mw-common": "中间件健康检查报告"
}


def create_client_meta_info_service(data, icon_data, client_binary):
    """
    创建客户端版本信息,并上传客户端图标和客户端文件
    """
    user_id = data.get("user_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    client_name = data.get("client_name")
    client_desc = data.get("client_desc")
    support_os = data.get("support_os")
    client_version = data.get("client_version")
    client_sub_version = data.get("client_sub_version")
    client_status = data.get("client_status", "正常")
    client_icon_raw_path = generate_new_path("edith_web", user_id).json
    client_icon_raw_path = client_icon_raw_path.get("result")
    icon_data.save(client_icon_raw_path)
    client_icon = generate_download_url('edith_web', client_icon_raw_path).json.get("result")
    client_raw_path = generate_new_path("edith_web", user_id, file_name=client_binary.filename
                                        ).json
    client_raw_path = client_raw_path.get("result")
    client_binary.save(client_raw_path)
    client_download_path = generate_download_url('edith_web', client_raw_path).json.get("result")
    new_client = EdithClientMetaInfo(
        client_name=client_name,
        client_desc=client_desc,
        client_icon=client_icon,
        support_os=support_os,
        client_version=client_version,
        client_sub_version=client_sub_version,
        client_raw_path=client_raw_path,
        client_download_path=client_download_path,
        client_status=client_status
    )
    db.session.add(new_client)
    db.session.commit()
    return next_console_response(result=new_client.to_dict())


def get_client_meta_info_service():
    """
    获取客户端版本信息
    """
    all_edith_clients = EdithClientMetaInfo.query.filter(
        EdithClientMetaInfo.client_status == "正常"
    ).order_by(
        EdithClientMetaInfo.support_os,
        EdithClientMetaInfo.client_version,
        EdithClientMetaInfo.client_sub_version
    ).all()
    all_edith_clients = [client.show_info() for client in all_edith_clients]
    return next_console_response(result=all_edith_clients)


def create_edith_task_service(data):
    """
    创建巡检任务
    """
    user_id = data.get("user_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    session_id = data.get("session_id")
    task_name = data.get("task_name")
    task_desc = data.get("task_desc")
    task_type = data.get("task_type")
    if task_type not in edith_support_software:
        return next_console_response(error_status=True, error_message=f"不支持的软件类型:{task_type}")
    task_stage = data.get("task_stage", "数据采集")
    edith_client_id = data.get("edith_client_id")
    task_parent_id = data.get("task_parent_id")
    task_status = data.get("task_statys", "初始化")
    task_code = uuid.uuid1().hex
    task_data_dir = generate_new_path(
        "edith_web",
        user_id,
        task_code,
        file_type="dir"
    ).json.get("result")
    new_edith_task = EdithTaskInfo(
        task_code=task_code,
        session_id=session_id,
        user_id=user_id,
        task_name=task_name,
        task_desc=task_desc,
        task_type=task_type,
        task_stage=task_stage,
        edith_client_id=edith_client_id,
        task_parent_id=task_parent_id,
        task_status=task_status,
        task_data_dir=task_data_dir
    )
    db.session.add(new_edith_task)
    db.session.commit()
    return next_console_response(result=new_edith_task.show_info())


def search_edith_task_service(data):
    """
    查询巡检任务
    """
    user_id = data.get("user_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    task_keyword = data.get("task_keyword")
    task_type = data.get("task_type", [])
    task_stage = data.get("task_stage", [])
    task_status = data.get("task_status", [])
    page_num = data.get("page_num", 1)
    page_size = data.get("page_size", 20)
    all_condition = [
        EdithTaskInfo.user_id == user_id
    ]
    if task_keyword:
        all_condition.append(
            or_(
                EdithTaskInfo.task_name.like(f"%{task_keyword}%"),
                EdithTaskInfo.task_desc.like(f"%{task_keyword}%"),
                EdithTaskInfo.task_code.like(f"%{task_keyword}%")
        ))
    if task_type:
        all_condition.append(EdithTaskInfo.task_type.in_(task_type))
    if task_stage:
        all_condition.append(EdithTaskInfo.task_stage.in_(task_stage))
    if task_status:
        all_condition.append(EdithTaskInfo.task_status.in_(task_status))
    all_edith_tasks = EdithTaskInfo.query.filter(*all_condition).order_by(
        EdithTaskInfo.create_time.desc()
    )
    total_count = all_edith_tasks.count()
    all_edith_tasks = all_edith_tasks.paginate(page=page_num, per_page=page_size, error_out=False)
    all_edith_tasks = [task.to_dict() for task in all_edith_tasks.items]
    # 添加数据清单
    for task in all_edith_tasks:
        # 获取数据目录下的文件
        task_data_dir = task.get("task_data_dir")
        if not task_data_dir:
            continue
        task_data_dir_path = os.path.join(task_data_dir, "data")
        if not os.path.exists(task_data_dir_path):
            continue
        all_data_files = os.listdir(task_data_dir_path)
        task["data_files"] = all_data_files
        del task["task_data_dir"]

    return next_console_response(result={
        "total": total_count,
        "data": all_edith_tasks
    })


def update_edith_task_service(data):
    """
    更新巡检任务
    """
    user_id = data.get("user_id")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    task_id = data.get("task_id")
    task_name = data.get("task_name")
    task_desc = data.get("task_desc")
    task_type = data.get("task_type")
    task_stage = data.get("task_stage")
    task_status = data.get("task_status")
    target_task = EdithTaskInfo.query.filter(
        EdithTaskInfo.id == task_id,
        EdithTaskInfo.user_id == user_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在")
    if task_name:
        target_task.task_name = task_name
    if task_desc is not None:
        target_task.task_desc = task_desc
    if task_type:
        target_task.task_type = task_type
    if task_stage:
        target_task.task_stage = task_stage
    if task_status:
        target_task.task_status = task_status
    db.session.add(target_task)
    db.session.commit()
    return next_console_response(result=target_task.show_info())


def upload_edith_task_data(data, task_data=None):
    """
    上传巡检任务数据
    """
    user_id = data.get("user_id")
    task_code = data.get("task_code")
    task_data_url = data.get("task_data_url")
    task_data_resources = data.get("task_data_resources")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")

    target_task = EdithTaskInfo.query.filter(
        EdithTaskInfo.task_code == task_code,
        EdithTaskInfo.user_id == user_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在")
    # 解压至目标目录
    target_data_dir = os.path.join(target_task.task_data_dir, 'data')
    if not os.path.exists(target_data_dir):
        os.makedirs(target_data_dir)
    if task_data_url:
        try:
            response = requests.get(task_data_url, timeout=600)
            if response.status_code != 200:
                return next_console_response(error_status=True, error_message="数据下载失败")
            task_data = response.content
            task_file_name = extract_filename_from_url(task_data_url)
            if not task_file_name:
                return next_console_response(error_status=True, error_message="数据文件名不存在")
            zip_data_path = str(os.path.join(target_task.task_data_dir, task_file_name))
            with open(zip_data_path, "wb") as f:
                f.write(task_data)
            with zipfile.ZipFile(zip_data_path, 'r') as z:
                z.extractall(target_data_dir)
            return next_console_response(result="上传成功")
        except Exception as e:
            app.logger.error(f"下载数据失败, 错误信息:{str(e)}")
            return next_console_response(error_status=True, error_message="数据下载失败")

    if task_data:
        for sub_task_data in task_data:
            if sub_task_data.filename.endswith('.zip'):
                # 先保存zip文件
                zip_data_path = str(os.path.join(target_task.task_data_dir, sub_task_data.filename))
                with open(zip_data_path, "wb") as f:
                    f.write(sub_task_data.read())
                with zipfile.ZipFile(zip_data_path, 'r') as z:
                    z.extractall(target_data_dir)
            else:
                target_data_path = os.path.join(target_data_dir, sub_task_data.filename)
                with open(target_data_path, "wb") as f:
                    f.write(sub_task_data.read())
    if task_data_resources:
        valid_task_data_resources = []
        for resource_id in task_data_resources:
            try:
                valid_task_data_resources.append(int(resource_id))
            except ValueError:
                continue
        if valid_task_data_resources:
            all_resources = ResourceObjectMeta.query.filter(
                ResourceObjectMeta.id.in_(valid_task_data_resources),
                ResourceObjectMeta.resource_status == "正常",
                ResourceObjectMeta.user_id == user_id
            ).all()
            if all_resources:
                for resource in all_resources:
                    # 复制一份
                    target_path = os.path.join(target_data_dir, resource.resource_name)
                    shutil.copy(resource.resource_path, target_path)
            else:
                return next_console_response(error_status=True, error_message="数据资源不存在")
    return next_console_response(result="上传成功")


def delete_edith_task_data(data):
    """
    删除巡检任务数据
    """
    user_id = data.get("user_id")
    task_code = data.get("task_code")
    task_data_name = data.get("task_data_name")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    target_task = EdithTaskInfo.query.filter(
        EdithTaskInfo.task_code == task_code,
        EdithTaskInfo.user_id == user_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在")
    if target_task.task_status != "初始化":
        return next_console_response(error_status=True, error_message="任务状态不允许删除数据")
    target_data_dir = target_task.task_data_dir
    if not os.path.exists(target_data_dir):
        return next_console_response(error_status=True, error_message="任务目录不存在")
    target_data_path = os.path.join(target_data_dir, "data", task_data_name)
    if not os.path.exists(target_data_path):
        return next_console_response(error_status=True, error_message="目标数据不存在")
    if os.path.isdir(target_data_path):
        os.rmdir(target_data_path)
    else:
        os.remove(target_data_path)
    return next_console_response(result="删除成功")


def start_generate_report_service(data):
    """
    生成巡检报告
        1、生成配置文件
        2、拼接命令 sidoc -pandoc='' -c='' -o=''
        3、启动任务生成报告
        4、更新任务状态
    """
    user_id = data.get("user_id")
    task_code = data.get("task_code")
    report_type = data.get("report_type", 'single')
    run_model = data.get("run_model", 'sync')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    target_task = EdithTaskInfo.query.filter(
        EdithTaskInfo.task_code == task_code,
        EdithTaskInfo.user_id == user_id
    ).first()
    if not target_task:
        return next_console_response(error_status=True, error_message="任务不存在")
    report_data_dir = os.path.join(target_task.task_data_dir, "data")
    if not os.path.exists(report_data_dir):
        return next_console_response(error_status=True, error_message="数据目录不存在")
    if not os.listdir(report_data_dir):
        return next_console_response(error_status=True, error_message="数据目录为空")
    # 生成报告生成任务
    report_code = uuid.uuid1().hex
    new_report_task = EdithReportInfo(
        user_id=user_id,
        edith_task_id=target_task.id,
        report_code=report_code,
        report_type=report_type,
        report_name=edith_support_software.get("report_type"),
        report_data_dir=report_data_dir,
        report_status="初始化",
        run_model=run_model,
    )
    db.session.add(new_report_task)
    db.session.commit()
    # 生成报告
    tools_path = get_tools_path().json.get("result")
    sidoc_path = tools_path.get("sidoc")
    pandoc_path = tools_path.get("pandoc")
    if not sidoc_path:
        return next_console_response(error_status=True, error_message="sidoc工具不存在")
    if not pandoc_path:
        return next_console_response(error_status=True, error_message="pandoc工具不存在")
    # 生成配置文件目录
    config_dir = os.path.join(target_task.task_data_dir, "config")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    report_dir = os.path.join(target_task.task_data_dir, "report")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    # 生成配置文件
    config_file_path = os.path.join(config_dir, f"config_{time.time()}.json")
    with open(config_file_path, "w", encoding="utf8") as f:
        f.write(generate_report_config(target_task, new_report_task, target_user, report_dir))
    new_report_task.report_generate_config = config_file_path
    new_report_task.report_status = "生成中"
    db.session.add(new_report_task)
    db.session.commit()
    # 将配置文件拷贝至lib目录
    if run_model == 'sync':
        lib_path = str(os.path.join(os.path.dirname(sidoc_path), target_task.task_type))
        shutil.copy(config_file_path, lib_path)
        run_config_file_path = str(os.path.join(lib_path, os.path.basename(config_file_path)))
        # 生成报告命令
        report_command = f"{sidoc_path} -pandoc={pandoc_path} -c={run_config_file_path} "
        result = str(subprocess.run(report_command, shell=True, capture_output=True, text=True,
                                    encoding="utf8", errors='replace').stdout)
        app.logger.warning(f"生成报告命令:{report_command}, 结果:{result}")
        new_report_task.task_trace = result
        # 判断并更新任务状态
        if not result.strip().endswith('.docx'):
            new_report_task.report_status = "异常"
            db.session.add(new_report_task)
            db.session.commit()
            return next_console_response(error_status=True, error_message="生成失败")
        new_report_task.report_status = "成功"
        # 获取报告目录下最新的一个文件路径
        report_path = result.strip().splitlines()[-1]
        new_report_task.report_path = report_path
        # 生成下载链接
        new_report_task.report_download_url = generate_download_url(
            'edith_web', report_path, suffix='docx'
        ).json.get("result")
        db.session.add(new_report_task)
        db.session.commit()
        # 删除运行的配置文件
        os.remove(run_config_file_path)
    elif run_model == 'async':
        async_result = start_generate_report.delay({
            "config_file_path": config_file_path,
            "sidoc_path": sidoc_path,
            "pandoc_path": pandoc_path,
            "task_type": target_task.task_type,
            "report_task_id": new_report_task.id
        })
        new_report_task.celery_id = async_result.id
        db.session.add(new_report_task)
        db.session.commit()
    else:
        return next_console_response(error_status=True, error_message="不支持的运行模式")
    save_edith_report_to_session(new_report_task, session_id=target_task.session_id)
    return next_console_response(result=new_report_task.show_info())


def get_tools_path():
    """
    获取sidoc的绝对路径
        linux app.libs.edith.sidoc
        windows app.libs.edith.sidoc.exe
    """
    system = platform.system()
    machine = platform.machine()
    # 确定基本目录结构
    # 构建版本映射表
    version_map = {
        ('linux', 'x86_64'): ('pandoc', 'sidoc'),
        ('linux', 'amd64'): ('pandoc', 'sidoc'),
        ('linux', 'arm64'): ('pandoc-arm', 'sidoc-arm'),
        ('linux', 'aarch64'): ('pandoc-arm', 'sidoc-arm'),
        ('windows', 'amd64'): ('pandoc.exe', 'sidoc.exe'),
        ('windows', 'x86_64'): ('pandoc.exe', 'sidoc.exe'),
    }
    target_version = version_map.get((system.lower(), machine.lower()))
    if not target_version:
        return next_console_response(error_status=True, error_message="不支持的操作系统")
    pandoc_file, sidoc_file = target_version
    target_sidoc_path = Path(__file__).resolve().parent.parent.parent / 'libs' / 'edith' / sidoc_file
    target_pandoc_path = Path(__file__).resolve().parent.parent.parent / 'libs' / 'edith' / pandoc_file
    # 检查权限
    system = platform.system()
    if system != 'windows':
        # 获取当前文件权限
        for path in [target_sidoc_path, target_pandoc_path]:
            current_mode = os.stat(path).st_mode
            # 检查是否有执行权限
            if not (current_mode & stat.S_IXUSR):
                try:
                    # 添加用户执行权限
                    os.chmod(path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                except Exception as e:
                    raise Exception(f"Failed to set execute permission for {path}: {str(e)}")
    result = {
        "sidoc": str(target_sidoc_path),
        "pandoc": str(target_pandoc_path)
    }
    return next_console_response(result=result)


def generate_report_config(edith_task, report_task, user, report_path):
    """
    生成报告配置文件
    """
    groupby = {
        "single": "instance",
        "cluster": "cluster",
        "full": "all",
    }.get(report_task.report_type)
    if report_task.report_type != 'full' and edith_task.task_type in (
            "linux-common", "windows-common", "sqlserver-common"
    ):
        groupby = "hostname"
    config_id = edith_task.task_type.split("-")[0]
    if report_task.report_type == "full":
        config_id += ".full"

    datadir = os.path.join(edith_task.task_data_dir, 'data')
    customer = "我的客户"
    name = user.user_name or user.user_nick_name
    create_date = datetime.now().strftime('%Y-%m-%d')
    if groupby == 'full':
        config_id = "oracle.full"
    config = {
      "datadir": datadir,
      "groupby": groupby,
      "id": config_id,
      "latest": "true",
      "meta": {
        "author": {
          "email": user.user_email or '',
          "name": user.user_name or user.user_nick_name
        },
        "customer": customer,
        "date": create_date,
        "imagesdir": "./images",
        "org": user.user_company or "我的公司",
        "title": edith_support_software.get(edith_task.task_type),
        "sys": "副标题",
        "config": {
          "appnames": {}
        }
      },
      "output": str(os.path.join(report_path, "{}-{}-{}-{}").format(
          customer,
          name,
          edith_support_software.get(edith_task.task_type),
          create_date
      )),

    }
    if edith_task.task_type == "oracle-common":
        config["template"] = f"{report_task.report_type}-template"
    elif report_task.report_type == "full":
        config["template"] = f"{report_task.report_type}-template"

    return str(config).replace("'", '"')


def get_lasted_report_path(result):
    """
    解析出报告路径
    """
    report_path = result.splitlines()[-1].strip()
    return report_path


def extract_filename_from_url(url):
    from urllib.parse import urlparse, parse_qs
    # 解析 URL
    parsed_url = urlparse(url)

    # 提取查询参数并解析为字典
    query_params = parse_qs(parsed_url.query)

    # 遍历所有键，找到以 'filename' 结尾的键
    for key in query_params:
        if key.lower().endswith("name"):
            # 返回对应的值（注意：parse_qs 返回的是列表，取第一个值）
            return query_params[key][0]

    # 如果没有找到，返回 None
    return None


def save_edith_report_to_session(report_task, session_id):
    """
    将edith生成的报告添加为会话附件
        生成资源对象，加入会话附件关系
    """
    if report_task.report_status != "成功":
        return False

    task_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id
    ).first()
    if not task_session:
        return False
    report_name = os.path.basename(report_task.report_path)
    resource_size_in_MB = os.path.getsize(report_task.report_path) /1024 /1024
    with open(report_task.report_path, 'rb') as f:
        resource_feature_code = hashlib.sha256(f.read()).hexdigest()
    report_task.report_name = report_name
    new_resource = ResourceObjectMeta(
        resource_parent_id=None,
        user_id=report_task.user_id,
        resource_name=report_name,
        resource_type="document",
        resource_icon="docx.svg",
        resource_format="docx",
        resource_size_in_MB=resource_size_in_MB,
        resource_path=report_task.report_path,
        resource_source=task_session.session_source,
        resource_download_url=report_task.report_download_url,
        resource_feature_code=resource_feature_code
    )
    db.session.add(new_resource)
    db.session.add(report_task)
    db.session.commit()
    if not new_resource.id:
        db.session.refresh(new_resource)
    new_attachment_rel = SessionAttachmentRelation(
        session_id=session_id,
        resource_id=new_resource.id,
        attachment_source=task_session.session_source,
    )
    db.session.add(new_attachment_rel)
    db.session.commit()
    return True
