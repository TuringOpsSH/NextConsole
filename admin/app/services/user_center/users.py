import hashlib
import os.path
import random
import uuid
from datetime import datetime, timezone, timedelta

import requests
import sqlalchemy

from flask_jwt_extended import (
    create_access_token, decode_token
)
from jinja2 import Template
from pypinyin import pinyin, Style
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app.app import app
from app.models.assistant_center.assistant import Assistant, UserAssistantRelation
from app.models.configure_center.system_config import SupportArea
from app.models.configure_center.system_config import SystemConfig
from app.models.contacts.company_model import *
from app.models.contacts.department_model import *
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.models.user_center.role_info import *
from app.models.user_center.user_info import *
from app.models.user_center.user_role_info import *
from app.services.configure_center.response_utils import next_console_response
from app.services.configure_center.user_config import init_user_config
from app.services.task_center.celery_fun_libs import send_user_create_email
from app.services.task_center.celery_fun_libs import send_user_verification_code_email
from app.services.task_center.user_notice import admin_notice_new_user
from app.services.user_center.account_service import init_user_account, add_invite_user_points_service
from app.services.user_center.system_notice_service import add_system_notice_service
from app.services.user_center.user_role import search_user_roles
from app.utils.oss.oss_client import generate_new_path, generate_download_url


def register_email_check(user_email):
    user = UserInfo.query.filter(
        UserInfo.user_email == user_email,
        UserInfo.user_status > 0
    ).first()
    result = {
        "user_email": user_email,
        "status": True,
        "error_message": "邮箱可以使用！",
    }
    if user:
        result["status"] = False
        result["error_message"] = "邮箱已被占用！"
    return next_console_response(result=result)


def register_user(data):
    """
    用户注册
    """
    user_email = data.get('user_email')
    user_password = data.get('user_password')
    is_sha256_flag = data.get("is_sha256_flag", True)
    if not is_sha256_flag:
        user_password = hashlib.sha256(user_password.encode()).hexdigest()  # 模拟前端提交过程
    user_password = generate_password_hash(user_password)
    user_name = data.get('user_name')
    user_source = data.get('user_source', "email")
    user_company = data.get("user_company", "")
    user_need_confirm = data.get('user_need_confirm', True)
    user_area_id = data.get("user_area_id", [])
    user_accept_contact = data.get("user_accept_contact", False)
    user_area = None
    if user_area_id and isinstance(user_area_id, list):
        user_area = SupportArea.query.filter(
            SupportArea.continent == user_area_id[0],
            SupportArea.region == user_area_id[1] if len(user_area_id) > 1 else None,
            SupportArea.name == user_area_id[2] if len(user_area_id) > 2 else None,
            SupportArea.area == user_area_id[3] if len(user_area_id) > 3 else None
        ).first()
        if user_area:
            user_area = user_area.id
    new_user = UserInfo(
        user_source=user_source,
        user_name=user_name,
        user_nick_name=user_name,
        user_password=user_password,
        user_email=user_email,
        user_status=0,
        user_company=user_company,
        user_area=user_area,
        user_nick_name_py=get_initial_py(user_name),
        user_account_type="个人账号",
        user_accept_contact=user_accept_contact
    )
    db.session.add(new_user)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return next_console_response(error_status=True, error_code=1005, error_message="邮箱已被占用！")
    data["user_id"] = new_user.user_id
    init_res = init_user(new_user, user_need_confirm, user_hello_flag=False)
    if init_res:
        return next_console_response(result=new_user.to_dict())
    else:
        return next_console_response(error_status=True, error_code=1005, error_message="用户初始化失败！")


def get_initial_py(user_name, k=3):
    chars = str(user_name)[:k]
    result = ""
    try:
        for char in chars:
            result += pinyin(char, style=Style.FIRST_LETTER)[0][0]
        return result.upper()
    except Exception as e:
        app.logger.error(f"提取拼音异常:{e}")
        return result


def init_user(user, user_confirm_flag=True, user_hello_flag=True):
    """
    初始化用户的一些列操作：
        1、设置用户角色
        2、设置用户对助手的权限
        3、发送邮件通知
        4、创建账号信息
        5、初始化应用配置
    """
    # 设置用户角色
    role = RoleInfo.query.filter(RoleInfo.role_name == "user").first()
    if role is None:
        return next_console_response(error_status=True, error_code=1004, error_message='角色设置错误')
    db.session.commit()

    new_user_role = UserRoleInfo(
        user_id=user.user_id,
        role_id=role.role_id,
        rel_status=1
    )
    db.session.add(new_user_role)
    db.session.commit()

    # 设置用户对助手的权限(向所有官方助手增加可用权限，为内置助手新增服务关系)
    # 获取所有官方助手，id < 0
    all_office_assistants = Assistant.query.filter(Assistant.id < 0).all()
    for assistant in all_office_assistants:
        new_user_assistant_rel = UserAssistantRelation(
            user_id=user.user_id,
            assistant_id=assistant.id,
            rel_type="权限",
            rel_value=1,
            rel_status="正常"
        )
        db.session.add(new_user_assistant_rel)
        try:
            db.session.commit()
        except IntegrityError as e:
            continue
    new_user_assistant_rel = UserAssistantRelation(
        user_id=user.user_id,
        assistant_id=-10086,
        rel_type="服务",
        rel_value=1,
        rel_status="正常"
    )
    db.session.add(new_user_assistant_rel)
    try:
        db.session.commit()
    except IntegrityError as e:
        pass

    # 发送确认邮件
    if user_confirm_flag and user.user_email:
        # 修改为验证码
        valid_code = register_email_generate_code(user.user_email).json.get("result")
        if not valid_code:
            return False
        target_email = app.config["smtp_user"]
        if user.user_source == "email":
            target_email = user.user_email
        elif user.user_source == "admin" or user.user_source == "qy_email":
            target_email = app.config["smtp_user"]
        with open(os.path.join(app.config["config_static"], "user_verification_code.html"), "r", encoding="utf8") as f:
            info_html = f.read()
            info_html_template = Template(info_html)
            info_html = info_html_template.render({
                "code": valid_code,
            })
        send_user_verification_code_email.delay([target_email], body=info_html)

    # 发生欢迎邮件
    if user_hello_flag and user.user_email:

        hello_html = "user_welcome.html"
        with open(os.path.join(app.config["config_static"], hello_html), "r", encoding="utf8") as f:
            info_html = f.read()
        info_html_template = Template(info_html)
        info_params = {
            "user_name": user.user_name,
            "user_email": user.user_email,
            "user_type": user.user_account_type,
            "user_company": user.user_company,
            "user_phone": user.user_phone,
        }
        info_html = info_html_template.render(info_params)
        send_user_create_email.delay([user.user_email], body=info_html)
    # 创建账号信息
    init_user_account({
        "user": user,
    })
    # 初始化应用配置
    init_user_config(user.user_id)

    # 初始化用户资源地址
    user.user_resource_base_path = generate_new_path(
        "resource_center", user_id=user.user_id, file_type="dir").json.get("result")
    db.session.add(user)
    db.session.commit()
    # 初始化用户资源库
    user_resource = ResourceObjectMeta(
        user_id=user.user_id,
        resource_name="我的资源",
        resource_type="folder",
        resource_desc="用户资源库",
        resource_status="正常",
        resource_path=user.user_resource_base_path,
        resource_icon="folder.svg",
        resource_source="resource_center",
    )
    db.session.add(user_resource)
    db.session.commit()
    return True


def register_email_generate_code(user_email):

    user = UserInfo.query.filter(UserInfo.user_email == user_email).first()
    if user is None:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    # 找出5分钟内的重置密码任务
    old_task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_email == user_email,
        UserSendCodeTask.task_status == "验证中",
        UserSendCodeTask.create_time > datetime.now() - timedelta(minutes=1)
    ).first()
    if old_task:
        remain_time = 60 - (datetime.now() - old_task.create_time).seconds
        return next_console_response(error_status=True,
                                     error_message="请勿频繁操作！还需等待{}秒".format(remain_time),
                                     error_code=1003)

    # 生成6位随机数字验证码
    user_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    new_reset_password_task = UserSendCodeTask(
        user_email=user_email,
        task_code=user_code,
        task_status="验证中"
    )
    db.session.add(new_reset_password_task)
    db.session.commit()

    return next_console_response(result=user_code)


def confirm_email_user(data):
    """
    验证用户提交的验证码，
        todo: 有多种验证业务
    :param data:
    :return:
    """
    user_email = data.get("email")
    task_code = data.get("code")
    # 找出最新的验证任务
    task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_email == user_email,
        UserSendCodeTask.task_code == task_code,
        UserSendCodeTask.task_status == "验证中"
    ).order_by(desc(UserSendCodeTask.create_time)).first()
    if task:
        # 超过5分钟，验证码失效
        if task.create_time < datetime.now() - timedelta(minutes=5):
            task.task_status = "已失效"
            db.session.add(task)
            db.session.commit()
            return next_console_response(result="验证码已失效！")
        target_user = UserInfo.query.filter(UserInfo.user_email == user_email).first()
        if target_user is None:
            return next_console_response(result="用户不存在！")
        task.task_status = "已验证"
        db.session.add(task)
        db.session.commit()
        # 更新用户状态

        userinfo = target_user.to_dict()
        # 获取用户角色与权限
        user_role = search_user_roles({"user_id": target_user.user_id}).get_json()
        user_role = user_role.get("result", [])
        user_role = [role.get("role_name") for role in user_role]
        userinfo["user_role"] = user_role
        data = {
            "user_id": target_user.user_id,
            "role_name": user_role,
            "user_code": target_user.user_code,
        }
        access_token = create_access_token(identity=str(target_user.user_id),
                                           expires_delta=timedelta(days=7),
                                           additional_claims=data
                                           )
        target_user.last_login_time = datetime.now()
        expire_time = datetime.now() + timedelta(days=7)
        target_user.user_status = 1
        db.session.add(target_user)
        db.session.commit()
        # 发送欢迎邮件
        hello_html = "user_welcome.html"
        with open(os.path.join(app.config["config_static"], hello_html), "r", encoding="utf8") as f:
            info_html = f.read()
        info_html_template = Template(info_html)
        info_params = {
            "user_name": target_user.user_name,
            "user_email": target_user.user_email,
            "user_type": target_user.user_account_type,
            "user_company": target_user.user_company,
            "user_phone": target_user.user_phone,
            "user_expire": "user_expire",

        }
        info_html = info_html_template.render(info_params)
        send_user_create_email.delay([target_user.user_email], body=info_html)
        return next_console_response(result={
            "token": access_token,
            "userinfo": userinfo,
            "expire_time": expire_time.strftime('%Y-%m-%d %H:%M:%S'),
        })

    else:
        return next_console_response(result="验证码错误!")


def resend_register_confirm_email_service(user_email):
    valid_code_result = register_email_generate_code(user_email)
    valid_code = valid_code_result.json.get("result")
    if not valid_code:
        error_message = valid_code_result.json.get("error_message")
        return next_console_response(error_status=True, error_message=error_message, error_code=1002)
    target_user = UserInfo.query.filter(UserInfo.user_email == user_email).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    target_email = app.config["smtp_user"]
    with open(os.path.join(app.config["config_static"], "user_verification_code.html"), "r", encoding="utf8") as f:
        info_html = f.read()
        info_htm_template = Template(info_html)
        info_html = info_htm_template.render(
            {"code": valid_code, }
        )
    send_user_verification_code_email.delay([target_email], body=info_html)
    return next_console_response(result="邮件已发送！")


def login_user(data):
    user_account = data.get('user_account')
    user_password = data.get('user_password')
    session_30_flag = data.get('session_30_flag')
    if "@" in user_account:
        user_email = user_account
        user_phone = None
    else:
        user_phone = user_account
        user_email = None
    if user_email:
        user = UserInfo.query.filter_by(user_email=user_email).first()
    else:
        user = UserInfo.query.filter_by(user_phone=user_phone).first()

    if (user and user.user_id == 1 and user.user_name == 'next_console'
            and user_password == '0cc5042d06a578e5eb453084a75aa2659aaf8564b87b26acec8cd3d0fd5c15ce'
            and user_password == user.user_password):
        if not user.user_resource_base_path:
            # 初始化用户资源地址
            user.user_resource_base_path = generate_new_path(
                "resource_center", user_id=user.user_id, file_type="dir").json.get("result")
            db.session.add(user)
            db.session.commit()
            # 初始化用户资源库
            user_resource = ResourceObjectMeta(
                user_id=user.user_id,
                resource_name="我的资源",
                resource_type="folder",
                resource_desc="用户资源库",
                resource_status="正常",
                resource_path=user.user_resource_base_path,
                resource_icon="folder.svg",
                resource_source="resource_center",
            )
            db.session.add(user_resource)
            db.session.commit()
    elif (user is None or not check_password_hash(
            user.user_password, user_password
    )):
        return next_console_response(error_status=True, error_message="账号或者密码错误！", error_code=401)
    # 检测用户状态
    if user.user_status <= 0:
        error_messages = {
            0: "用户还未激活，请查看邮箱！",
            -1: "用户已停用！",
            -2: "用户已被锁定！请联系管理员！",
        }
        error_message = error_messages.get(user.user_status, "用户状态异常！")
        return next_console_response(error_status=True, error_message=error_message, error_code=401)
    if session_30_flag:
        session_day = 30
    else:
        session_day = 7
    userinfo = user.to_dict()
    # 获取用户角色与权限
    user_role = search_user_roles({"user_id": user.user_id}).get_json()
    user_role = user_role.get("result", [])
    user_role = [role.get("role_name") for role in user_role]
    admin_flag = False
    for role in user_role:
        if "admin" in role:
            admin_flag = True
            break
    if not admin_flag:
        return next_console_response(error_status=True, error_message="无管理员权限！", error_code=401)
    userinfo["user_role"] = user_role
    data = {
        "user_id": user.user_id,
        "role_name": user_role,
        "user_code": user.user_code,
    }
    access_token = create_access_token(identity=str(user.user_id),
                                       expires_delta=timedelta(days=session_day),
                                       additional_claims=data
                                       )
    user.last_login_time = datetime.now()
    expire_time = datetime.now() + timedelta(days=session_day)
    db.session.add(user)
    db.session.commit()
    return next_console_response(result={
        "token": access_token,
        "userinfo": userinfo,
        "expire_time": expire_time.strftime('%Y-%m-%d %H:%M:%S'),
    })


def reset_account_password_send_code(data):
    """
    生成验证码并发送重置密码邮件,可重复发送
    :param data:
    :return:
    """
    user_account = data.get("user_account")
    if "@" in user_account:
        user_email = user_account
        user_phone = None
    else:
        user_phone = user_account
        user_email = None
    if user_email:
        user = UserInfo.query.filter(UserInfo.user_email == user_email).first()
        if user is None:
            return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
        # 找出5分钟内的重置密码任务
        old_task = UserSendCodeTask.query.filter(
            UserSendCodeTask.user_email == user_email,
            UserSendCodeTask.task_status == "验证中",
            UserSendCodeTask.create_time > datetime.now(timezone.utc) - timedelta(minutes=1)
        ).first()
        if old_task:
            remain_time = 60 - (datetime.now(timezone.utc) - old_task.create_time).seconds
            return next_console_response(error_status=True,
                                         error_message="请勿频繁操作！还需等待{}秒".format(remain_time),
                                         error_code=1003)
        new_password = data.get("new_password")
        user_password = generate_password_hash(new_password)
        # 生成6位随机数字验证码
        user_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        new_reset_password_task = UserSendCodeTask(
            user_email=user_email,
            new_password=user_password,
            task_code=user_code,
            task_status="验证中"
        )
        db.session.add(new_reset_password_task)
        db.session.commit()
        # 发送邮件
        with open(os.path.join(app.config["config_static"], "user_verification_code.html"), "r", encoding="utf8") as f:
            info_html = f.read()
            info_htm_template = Template(info_html)
            info_html = info_htm_template.render(
                {"code": user_code, }
            )
        send_user_verification_code_email.delay([user_email], body=info_html)
        return next_console_response(result="邮件已发送！")
    else:
        user = UserInfo.query.filter(UserInfo.user_phone == user_phone).first()
        if user is None:
            return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
        # 找出5分钟内的重置密码任务
        old_task = UserSendCodeTask.query.filter(
            UserSendCodeTask.user_phone == user_phone,
            UserSendCodeTask.task_status == "验证中",
            UserSendCodeTask.create_time > datetime.now(timezone.utc) - timedelta(minutes=1)
        ).first()
        if old_task:
            remain_time = 60 - (datetime.now(timezone.utc) - old_task.create_time).seconds
            return next_console_response(error_status=True,
                                         error_message="请勿频繁操作！还需等待{}秒".format(remain_time),
                                         error_code=1003)
        new_password = data.get("new_password")
        user_password = generate_password_hash(new_password)
        # 生成6位随机数字验证码
        user_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # 发送短信
        template_param = f'{{"code":"{user_code}"}}'
        send_sms_by_client(user_phone, template_param)
        # 保存验证码任务
        # 旧任务失效，新任务生成
        if old_task:
            old_task.task_status = "已失效"
            db.session.add(old_task)
            db.session.commit()
        new_reset_password_task = UserSendCodeTask(
            user_phone=user_phone,
            new_password=user_password,
            task_code=user_code,
            task_status="验证中"
        )
        db.session.add(new_reset_password_task)
        db.session.commit()
        return next_console_response()


def valid_reset_password_code(data):
    user_account = data.get("user_account")
    task_code = data.get("code")
    if "@" in user_account:
        user_email = user_account
        user_phone = None
    else:
        user_phone = user_account
        user_email = None
    # 找出最新的重置密码任务
    if user_email:
        task = UserSendCodeTask.query.filter(
            UserSendCodeTask.user_email == user_email,
            UserSendCodeTask.task_code == task_code,
            UserSendCodeTask.task_status == "验证中"
        ).order_by(desc(UserSendCodeTask.create_time)).first()
    else:
        task = UserSendCodeTask.query.filter(
            UserSendCodeTask.user_phone == user_phone,
            UserSendCodeTask.task_code == task_code,
            UserSendCodeTask.task_status == "验证中"
        ).order_by(desc(UserSendCodeTask.create_time)).first()
    if task:
        # 超过5分钟，验证码失效
        if task.create_time < datetime.now() - timedelta(minutes=5):
            task.task_status = "已失效"
            db.session.add(task)
            db.session.commit()
            return next_console_response(error_status=True, error_message="验证码已失效！", error_code=1003)
        target_user = UserInfo.query.filter(UserInfo.user_email == user_email).first()
        if target_user is None:
            return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
        target_user.user_password = task.new_password
        task.task_status = "已验证"
        db.session.add(target_user)
        db.session.add(task)
        db.session.commit()
        return next_console_response()
    else:
        return next_console_response(error_status=True, error_message="验证码错误！", error_code=1003)


def get_user(user_id):
    user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    if user is None:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    # 判断用户是否过期
    if user.user_expire_time and user.user_expire_time < datetime.now():
        user.user_status = -1
        db.session.add(user)
        db.session.commit()
        return next_console_response(error_status=True, error_message="用户已过期！", error_code=401)
    user_role = search_user_roles({"user_id": user.user_id}).get_json()
    user_role = user_role.get("result", [])
    user_role = [role.get("role_name") for role in user_role]
    userinfo = user.to_dict()
    userinfo["user_role"] = user_role
    if user.user_account_type == '企业账号':
        target_company = CompanyInfo.query.filter(
            CompanyInfo.id == user.user_company_id,
            CompanyInfo.company_status == '正常'
        ).first()
        if target_company:
            userinfo["user_company"] = target_company.company_name
            userinfo["user_company_id"] = target_company.id
        target_department = DepartmentInfo.query.filter(
            DepartmentInfo.id == user.user_department_id,
            DepartmentInfo.department_status == '正常'
        ).first()
        if target_department:
            userinfo["user_department"] = target_department.department_name
            userinfo["user_department_id"] = target_department.id
    target_user_area = SupportArea.query.filter(
        SupportArea.id == user.user_area
    ).first()
    if target_user_area:
        userinfo["user_area"] = f"{target_user_area.province} {target_user_area.city}"
    return next_console_response(result=userinfo)


def delete_users(user_ids):
    UserInfo.query.filter(UserInfo.user_id.in_(user_ids)).delete(synchronize_session=False)
    db.session.commit()
    return next_console_response()


def update_user(params):
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if target_user is None:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    # 特殊处理字段
    user_area = params.get("user_area")
    if user_area and isinstance(user_area, list):
        user_area = SupportArea.query.filter(
            SupportArea.continent == user_area[0],
            SupportArea.country == user_area[1] if len(user_area) > 1 else None,
            SupportArea.province == user_area[2] if len(user_area) > 2 else None,
            SupportArea.city == user_area[3] if len(user_area) > 3 else None
        ).first()
        if user_area:
            target_user.user_area = user_area.id
    # 禁止更新字段
    forbidden_fields = [
        "user_id", "user_email", "user_code", "user_source",
        "create_time", "update_time", "last_login_time", "user_expire_time", "user_status",
        "user_account_type", "user_resource_limit", "user_is_servicer", "user_resource_base_path"
        "user_company_id", "user_company_id", "user_area"
    ]
    for k in forbidden_fields:
        if k in params:
            params.pop(k)
    if "user_password" in params:
        new_password = generate_password_hash(params["user_password"])
        params["user_password"] = new_password
    if "user_nick_name" in params:
        params["user_nick_name_py"] = get_initial_py(params["user_nick_name"])


    try:
        for k in params:
            setattr(target_user, k, params[k])
        db.session.add(target_user)
        db.session.commit()
        return next_console_response(result=target_user.to_dict())
    except IntegrityError as e:
        error_info = e.orig.args[1].split(" ")[2].strip("'")
        return next_console_response(error_status=True, error_code=1001,
                                     error_message=" {} 已经被占用！".format(error_info))


def update_user_avatar(user_id, avatar):
    # 更新用户头像
    suffix = avatar.filename.split(".")[-1]
    avatar_path = generate_new_path("user_center",
                                    user_id=user_id, file_type="file", suffix=suffix
                                    ).json.get("result")
    avatar.save(avatar_path)
    user_avatar = generate_download_url(
        "user_center",
        avatar_path, suffix=suffix).json.get("result")
    params = {
        'user_id': user_id,
        'user_avatar': user_avatar
    }
    return update_user(params)


def close_user(params):
    # 关闭用户的一系列操作
    user_id = int(params.get("user_id"))
    delete_users([user_id])
    return next_console_response()


def reset_new_email_send_code(data):
    user_id = int(data.get("user_id"))
    new_email = data.get("new_email")
    user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    if not user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    exist_email = UserInfo.query.filter(
        UserInfo.user_email == new_email
    ).first()
    if exist_email:
        return next_console_response(error_status=True, error_message="邮箱已被占用！", error_code=1003)
    # 找出5分钟内的重置密码任务
    old_task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_id == user_id,
        UserSendCodeTask.new_email == new_email,
        UserSendCodeTask.task_status == "验证中",
        UserSendCodeTask.create_time > datetime.now() - timedelta(minutes=1)
    ).first()
    if old_task:
        remain_time = 60 - (datetime.now() - old_task.create_time).seconds
        return next_console_response(error_status=True,
                                     error_message="请勿频繁操作！还需等待{}秒".format(remain_time),
                                     error_code=1003)
    # 生成6位随机验证码
    user_code = str(random.randint(100000, 999999))
    new_reset_password_task = UserSendCodeTask(
        user_id=user_id,
        new_email=new_email,
        task_code=user_code,
        task_status="验证中"
    )
    db.session.add(new_reset_password_task)
    db.session.commit()
    # 发送邮件
    # 发送邮件
    with open(os.path.join(app.config["config_static"], "user_verification_code.html"), "r", encoding="utf8") as f:
        info_html = f.read()
        info_htm_template = Template(info_html)
        info_html = info_htm_template.render(
            {"code": user_code, }
        )
    send_user_verification_code_email.delay([data.get("new_email")], body=info_html)
    return next_console_response()


def valid_reset_email_code(data):
    user_id = int(data.get("user_id"))
    user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    task_code = data.get("code")
    new_email = data.get("new_email")

    # 找出最近重置密码任务
    task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_id == user_id,
        UserSendCodeTask.task_status == "验证中",
        UserSendCodeTask.new_email == new_email,
        UserSendCodeTask.task_code == task_code
    ).order_by(desc(UserSendCodeTask.create_time)).first()
    if task:
        # 超过5分钟，验证码失效
        if task.create_time < datetime.now() - timedelta(minutes=5):
            task.task_status = "已失效"
            db.session.add(task)
            db.session.commit()
            return next_console_response(error_status=True, error_message="验证码已失效！", error_code=1003)
        user.user_email = task.new_email
        task.task_status = "已验证"
        db.session.add(user)
        db.session.add(task)
        db.session.commit()
        return next_console_response()
    else:
        return next_console_response(error_status=True, error_message="验证码错误！", error_code=1003)


def send_text_code_aliyun(data):
    """
    基于阿里云发送短信验证码
    :param data:
    :return:
    """
    phone = data.get("user_phone")
    # 找出5分钟内的重置密码任务
    old_task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_phone == phone,
        UserSendCodeTask.task_status == "验证中",
        UserSendCodeTask.create_time > datetime.now(timezone.utc) - timedelta(minutes=1)
    ).first()
    if old_task:
        remain_time = 60 - (datetime.now(timezone.utc) - old_task.create_time).seconds
        return next_console_response(error_status=True,
                                     error_message="请勿频繁操作！还需等待{}秒".format(remain_time),
                                     error_code=1003)
    # 生成6位随机数字验证码
    verification_code = str(random.randint(100000, 999999))
    template_param = f'{{"code":"{verification_code}"}}'
    # 发送短信
    send_sms_by_client(phone, template_param)
    # 保存验证码任务
    # 旧任务失效，新任务生成
    if old_task:
        old_task.task_status = "已失效"
        db.session.add(old_task)
        db.session.commit()
    new_task = UserSendCodeTask(
        user_phone=phone,
        task_code=verification_code,
        task_status="验证中"
    )
    db.session.add(new_task)
    db.session.commit()
    return next_console_response()



def send_text_code_email(data):
    """
    发送邮箱验证码
    :param data:
    :return:
    """
    user_email = data.get("user_email")
    # 找出5分钟内的重置密码任务
    old_task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_email == user_email,
        UserSendCodeTask.task_status == "验证中",
        UserSendCodeTask.create_time > datetime.now() - timedelta(minutes=1)
    ).first()
    if old_task:
        remain_time = 60 - (datetime.now() - old_task.create_time).seconds
        return next_console_response(error_status=True,
                                     error_message="请勿频繁操作！还需等待{}秒".format(remain_time),
                                     error_code=1003)
    # 生成6位随机数字验证码
    user_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    new_reset_password_task = UserSendCodeTask(
        user_email=user_email,
        task_code=user_code,
        task_status="验证中"
    )
    db.session.add(new_reset_password_task)
    db.session.commit()
    # 发送邮件
    with open(os.path.join(app.config["config_static"], "user_verification_code.html"), "r", encoding="utf8") as f:
        info_html = f.read()
        info_htm_template = Template(info_html)
        info_html = info_htm_template.render(
            {"code": user_code, }
        )
    send_user_verification_code_email.delay([user_email], body=info_html)
    return next_console_response()


def valid_text_code(data):
    """
    验证短信验证码
    :param data:
    :return:
    """
    task_code = data.get("text_code")
    new_phone = data.get("user_phone")
    new_email = data.get("user_email")
    # 找出最近验证码任务
    if new_phone:
        task = UserSendCodeTask.query.filter(
            UserSendCodeTask.task_status == "验证中",
            UserSendCodeTask.user_phone == new_phone,
            UserSendCodeTask.task_code == task_code
        ).order_by(desc(UserSendCodeTask.create_time)).first()
    elif new_email:
        task = UserSendCodeTask.query.filter(
            UserSendCodeTask.task_status == "验证中",
            UserSendCodeTask.user_email == new_email,
            UserSendCodeTask.task_code == task_code
        ).order_by(desc(UserSendCodeTask.create_time)).first()
    else:
        return next_console_response(error_status=True, error_message="参数错误！")
    if task:
        # 超过5分钟，验证码失效
        from datetime import datetime, timezone, timedelta
        if task.create_time < datetime.now(timezone.utc) - timedelta(minutes=5):
            task.task_status = "已失效"
            db.session.add(task)
            db.session.commit()
            return next_console_response(error_status=True, error_message="验证码已失效！", error_code=1003)
        task.task_status = "已验证"
        db.session.add(task)
        db.session.commit()
        return next_console_response()
    else:
        return next_console_response(error_status=True, error_message="验证码错误！", error_code=1003)


def register_or_login_account_by_code(data):
    """
    手机号、邮箱注册或登录，根据验证码判断是否可以登录，如果没有用户则注册
    :param data:
    :return:
    """
    user_account = data.get('user_account')
    # 邮箱路线
    if "@" in user_account:
        user_email = user_account
        return register_or_login_email({
            "user_email": user_email,
            "text_code": data.get("text_code"),
            "session_30_flag": data.get("session_30_flag")
        })
    # 手机号路线
    else:
        user_phone = user_account
        return register_or_login_phone(
            {
                "user_phone": user_phone,
                "text_code": data.get("text_code"),
                "session_30_flag": data.get("session_30_flag")
            }
        )


def add_user(params):
    """
    新增用户
    """
    user_email = params.get("user_email")
    user_role = params.get("user_role", "user")
    if user_role not in ("visitor", "user", "admin", "super_admin"):
        return next_console_response(error_status=True, error_code=1000, error_message="用户角色不合法！")
    user_code = params.get("user_code", "")
    user_source = params.get("user_source", "email")
    user_name = params.get("user_name", "")
    user_password = params.get("user_password", "123456")
    is_sha256_flag = params.get("is_sha256_flag", True)
    if not is_sha256_flag:
        user_password = hashlib.sha256(user_password.encode()).hexdigest()  # 模拟前端提交过程
    user_password = generate_password_hash(user_password)
    user_phone = params.get("user_phone", "")
    user_gender = params.get("user_gender", "男")
    user_age = params.get("user_age", 18)
    user_avatar = params.get("user_avatar", "")
    user_company = params.get("user_company", "")
    user_department = params.get("user_department", "")
    user_status = params.get("user_status", 1)
    user_wx_nickname = params.get("user_wx_nickname", "")
    user_wx_avatar = params.get("user_wx_avatar", "")
    user_wx_openid = params.get("user_wx_openid", "")
    user_wx_union_id = params.get("user_wx_unionid", "")
    user_confirm_flag = params.get("user_confirm_flag", True)
    user_expire_time = params.get("user_expire_time")
    new_user = UserInfo(
        user_code=user_code,
        user_source=user_source,
        user_nick_name=user_name,
        user_nick_name_py=get_initial_py(user_name),
        user_password=user_password,
        user_email=user_email,
        user_phone=user_phone,
        user_gender=user_gender,
        user_age=user_age,
        user_avatar=user_avatar,
        user_company=user_company,
        user_department=user_department,
        user_status=user_status,
        user_wx_nickname=user_wx_nickname,
        user_wx_avatar=user_wx_avatar,
        user_wx_openid=user_wx_openid,
        user_wx_union_id=user_wx_union_id,
        user_expire_time=user_expire_time
    )
    db.session.add(new_user)
    db.session.commit()
    params["user_id"] = new_user.user_id
    init_res = init_user(new_user, user_confirm_flag)
    if init_res:
        return next_console_response(result=new_user.to_dict())
    else:
        return next_console_response(error_status=True, error_code=1005, error_message="用户初始化失败！")


def register_or_login_phone(data):
    """
    手机号注册或登录，根据验证码判断是否可以登录，如果没有用户则注册
    :param data:
    :return:
    """
    res = valid_text_code(data).json
    if res.get("error_status"):
        return res
    user_phone = data.get('user_phone')
    text_code = data.get('text_code')
    success_task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_phone == user_phone,
        UserSendCodeTask.task_code == text_code,
        UserSendCodeTask.task_status == "已验证",
        UserSendCodeTask.update_time > datetime.now() - timedelta(minutes=5)
    ).first()
    if success_task is None:
        return next_console_response(error_status=True, error_message="验证码已失效！", error_code=1002)
    user = UserInfo.query.filter_by(user_phone=user_phone).first()
    if user is None:
        return next_console_response(error_status=True, error_message="账号不存在！", error_code=1002)
    # 检测用户状态
    if user.user_status <= 0:
        error_messages = {
            0: "用户还未激活，请查看邮箱！",
            -1: "用户已停用！",
            -2: "用户已被锁定！请联系管理员！",
        }
        error_message = error_messages.get(user.user_status, "用户状态异常！")
        return next_console_response(error_status=True, error_message=error_message, error_code=401)
    session_day = 7
    userinfo = user.to_dict()
    # 获取用户角色与权限
    user_role = search_user_roles({"user_id": user.user_id}).get_json()
    user_role = user_role.get("result", [])
    user_role = [role.get("role_name") for role in user_role]
    admin_flag = False
    for role in user_role:
        if "admin" in role:
            admin_flag = True
            break
    if not admin_flag:
        return next_console_response(error_status=True, error_message="无管理员权限！", error_code=401)
    userinfo["user_role"] = user_role
    data = {
        "user_id": user.user_id,
        "role_name": user_role,
        "user_code": user.user_code,
    }
    access_token = create_access_token(identity=str(user.user_id),
                                       expires_delta=timedelta(days=session_day),
                                       additional_claims=data
                                       )
    user.last_login_time = datetime.now()
    db.session.add(user)
    db.session.commit()
    return next_console_response(result={"token": access_token, "userinfo": userinfo})


def register_or_login_email(data):
    """
    邮箱注册或登录，根据验证码判断是否可以登录，如果没有用户则注册
    :param data:
    :return:
    """
    res = valid_text_code(data).json
    if res.get("error_status"):
        return res
    user_email = data.get('user_email')
    text_code = data.get('text_code')
    success_task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_email == user_email,
        UserSendCodeTask.task_code == text_code,
        UserSendCodeTask.task_status == "已验证",
        UserSendCodeTask.update_time > datetime.now() - timedelta(minutes=5)
    ).first()
    if success_task is None:
        return next_console_response(error_status=True, error_message="验证码已失效！", error_code=1002)
    user = UserInfo.query.filter_by(user_email=user_email).first()
    if user is None:
        return next_console_response(error_status=True, error_message="账号不存在！", error_code=1002)
    # 检测用户状态
    if user.user_status <= 0:
        error_messages = {
            0: "用户还未激活，请查看邮箱！",
            -1: "用户已停用！",
            -2: "用户已被锁定！请联系管理员！",
        }
        error_message = error_messages.get(user.user_status, "用户状态异常！")
        return next_console_response(error_status=True, error_message=error_message, error_code=401)
    session_day = 7
    userinfo = user.to_dict()
    # 获取用户角色与权限
    user_role = search_user_roles({"user_id": user.user_id}).get_json()
    user_role = user_role.get("result", [])
    user_role = [role.get("role_name") for role in user_role]
    admin_flag = False
    for role in user_role:
        if "admin" in role:
            admin_flag = True
            break
    if not admin_flag:
        return next_console_response(error_status=True, error_message="无管理员权限！", error_code=401)
    userinfo["user_role"] = user_role
    data = {
        "user_id": user.user_id,
        "role_name": user_role,
        "user_code": user.user_code,
    }
    access_token = create_access_token(identity=str(user.user_id),
                                       expires_delta=timedelta(days=session_day),
                                       additional_claims=data
                                       )
    user.last_login_time = datetime.now()
    db.session.add(user)
    db.session.commit()
    return next_console_response(result={"token": access_token, "userinfo": userinfo})


def wx_register_user(data):
    domain = data.get("domain")
    code = data.get("code")
    from app.models.configure_center.system_config import SystemConfig
    system_connectors_config = SystemConfig.query.filter(
        SystemConfig.config_key == "connectors",
        SystemConfig.config_status == 1
    ).first()
    config = None
    for wx in system_connectors_config.config_value.get("weixin"):
        if wx.get("domain") == domain:
            config = wx
            break
    if not config:
        return next_console_response(error_status=True, error_message="未配置微信登录！", error_code=1002)

    wx_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    wx_params = {
        "appid": config.get("wx_app_id"),
        "secret": config.get("wx_app_secret"),
        "code": code,
        "grant_type": "authorization_code",
    }
    wx_res = requests.get(wx_url, params=wx_params).json()
    if "errcode" in wx_res:
        return next_console_response(error_status=True, error_message="微信授权失败！", error_code=1002)
    access_token = wx_res.get("access_token")
    refresh_token = wx_res.get("refresh_token")
    openid = wx_res.get("openid")
    union_id = wx_res.get("unionid")
    # 检验授权凭证（access_token）是否有效
    wx_check_url = "https://api.weixin.qq.com/sns/auth"
    wx_check_params = {
        "access_token": access_token,
        "openid": openid,
    }
    wx_check_res = requests.get(wx_check_url, params=wx_check_params).json()
    if wx_check_res.get("errcode") != 0:
        # 刷新access_token
        wx_refresh_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"
        wx_refresh_params = {
            "appid": config.get("wx_app_id"),
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        wx_refresh_res = requests.get(wx_refresh_url, params=wx_refresh_params).json()
        if "errcode" in wx_refresh_res:
            return next_console_response(error_status=True,
                                         error_message="微信授权失败！{}".format(wx_refresh_res),
                                         error_code=1002)
        access_token = wx_refresh_res.get("access_token")
    wx_user_info_url = "https://api.weixin.qq.com/sns/userinfo"
    wx_params = {
        "access_token": access_token,
        "openid": openid,
        "lang": "zh_CN",
    }
    wx_user_info_res = requests.get(wx_user_info_url, params=wx_params).json()
    if "errcode" in wx_user_info_res:
        return next_console_response(error_status=True,
                                     error_message="微信授权失败！{}".format(wx_user_info_res),
                                     error_code=1002)
    state = data.get("state")
    app.logger.warning(f"state: {state}")
    invite_view_id = None
    if state.startswith("login_"):
        try:
            invite_view_id = int(state.split("_")[1])
            state = "login"
        except Exception:
            pass
    if state in ("login", "register"):
        user = UserInfo.query.filter(UserInfo.user_wx_openid == openid).first()
        if not user:
            # 自动创建用户
            # 保存头像图片
            avatar_url = wx_user_info_res.get("headimgurl")
            avatar_path = save_wx_avatar(avatar_url, openid)
            user_code = str(uuid.uuid4())
            new_user_params = {
                "user_code": user_code,
                'user_name': wx_user_info_res.get("nickname").encode("iso-8859-1").decode("utf-8"),
                'user_source': "wx",
                "user_password": union_id,
                "is_sha256_flag": False,
                'user_email': None,
                'user_phone': None,
                "user_avatar": avatar_path,
                'user_status': 1,
                'user_wx_nickname': wx_user_info_res.get("nickname").encode("iso-8859-1").decode("utf-8"),
                'user_wx_avatar': avatar_url,
                'user_wx_openid': openid,
                'user_wx_union_id': union_id,
                "user_confirm_flag": False,
            }
            add_user(new_user_params)
            user = UserInfo.query.filter_by(user_code=user_code).first()
            if user is None:
                return next_console_response(error_status=True, error_message="微信自动注册失败！", error_code=1002)
            if invite_view_id:
                invite_record = UserInviteCodeViewRecord.query.filter(
                    UserInviteCodeViewRecord.id == invite_view_id
                ).first()
                invite_user = UserInfo.query.filter(
                    UserInfo.user_id == invite_record.user_id,
                    UserInfo.user_status == 1
                ).first()
                if invite_record and invite_user:
                    # 更新邀请情况
                    invite_record.view_user_id = user.user_id
                    invite_record.finish_register = True
                    db.session.add(invite_record)
                    db.session.commit()
                    # 尝试新增积分
                    add_invite_user_points_service(
                        {
                            "new_user": user,
                            "invite_user": invite_user,
                        }
                    )
                    # 给双方发送站内信(欢迎，加好友，邀请)
                    if invite_user.user_id != 1:
                        # 新建好友
                        new_relation = UserFriendsRelation(
                            user_id=invite_record.user_id,
                            friend_id=user.user_id,
                            rel_status=1
                        )
                        db.session.add(new_relation)
                        invite_record.finish_add_friend = True
                        db.session.add(invite_record)
                        db.session.commit()
                        add_system_notice_service(
                            {
                                "user_id": user.user_id,
                                "notice_title": "欢迎使用NextConsole智能体服务平台",
                                "notice_content": f"恭喜您通过好友{invite_user.user_nick_name}的邀请码成功创建NextConsole智能体服务平台的账号，请前往工作台开启您的第一次问答体验吧~",
                                "notice_icon": "notice_success.svg",
                            }
                        )
                        add_system_notice_service(
                            {
                                "user_id": invite_user.user_id,
                                "notice_title": "欢迎使用NextConsole智能体服务平台",
                                "notice_content": f"恭喜您的好友{user.user_nick_name}通过您的邀请码成功创建NextConsole智能体服务平台的账号!",
                                "notice_icon": "notice_success.svg",
                            }
                        )
        else:
            # 判断用户状态
            if user.user_status == -1:
                return next_console_response(error_status=True, error_message="用户已停用，请联系管理员！")
            elif user.user_status == -2:
                return next_console_response(error_status=True, error_message="用户活动异常，已被锁定！")
            if invite_view_id:
                # 检查是否为好友，不是则自动添加，发送站内信，并更新邀请记录
                if invite_view_id:
                    invite_record = UserInviteCodeViewRecord.query.filter(
                        UserInviteCodeViewRecord.id == invite_view_id
                    ).first()
                    invite_user = UserInfo.query.filter(
                        UserInfo.user_id == invite_record.user_id,
                        UserInfo.user_status == 1
                    ).first()
                    if invite_record and invite_user and invite_user.user_id != 1 and invite_user.user_id != user.user_id:
                        is_friend = UserFriendsRelation.query.filter(
                            UserFriendsRelation.rel_status == 1,
                            and_(
                                UserFriendsRelation.friend_id.in_([user.user_id, invite_record.user_id]),
                                UserFriendsRelation.user_id.in_([user.user_id, invite_record.user_id])
                            ),
                        ).first()
                        if not is_friend:
                            # 新建好友
                            new_relation = UserFriendsRelation(
                                user_id=invite_record.user_id,
                                friend_id=user.user_id,
                                rel_status=1
                            )
                            db.session.add(new_relation)
                            db.session.commit()
                            # 更新邀请情况
                            invite_record.view_user_id = user.user_id
                            invite_record.finish_add_friend = True
                            db.session.add(invite_record)
                            db.session.commit()
                            # 给双方发送站内信(欢迎，加好友，邀请)
                            add_system_notice_service(
                                {
                                    "user_id": user.user_id,
                                    "notice_title": "欢迎使用NextConsole智能体服务平台",
                                    "notice_content": f"恭喜您通过好友{invite_user.user_nick_name}的邀请码成功添加好友！",
                                    "notice_icon": "notice_success.svg",
                                }
                            )

        # 直接登录
        userinfo = user.to_dict()
        user_role = search_user_roles({"user_id": userinfo['user_id']}).json
        user_role = user_role.get("result", [])
        user_role = [role.get("role_name") for role in user_role]
        userinfo["user_role"] = user_role
        data = {
            "user_id": userinfo['user_id'],
            "role_name": user_role,
        }
        access_token = create_access_token(identity=str(userinfo['user_id']),
                                           expires_delta=timedelta(days=7),
                                           additional_claims=data
                                           )
        user.last_login_time = datetime.now(timezone.utc)
        db.session.add(user)
        db.session.commit()
        expire_time = (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        return next_console_response(result={"token": access_token, "userinfo": userinfo, "expire_time": expire_time})

    elif state in ("bind", "update"):
        old_user = UserInfo.query.filter(UserInfo.user_wx_openid == openid).first()
        if old_user:
            return next_console_response(error_status=True, error_message="微信已被绑定！", error_code=1004)
        token = data.get("token")
        if not token:
            return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
        try:
            decode_token_value = decode_token(token)
            user_id = decode_token_value.get("user_id")
        except Exception as e:
            return next_console_response(error_status=True, error_message="Token解析失败！", error_code=1002)
        target_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
        if target_user is None:
            return next_console_response(error_status=True, error_message="用户不存在！")
        # 保存头像图片
        avatar_url = wx_user_info_res.get("headimgurl")
        avatar_path = save_wx_avatar(avatar_url, openid)
        if not target_user.user_avatar:
            target_user.user_avatar = avatar_path
        target_user.user_wx_nickname = wx_user_info_res.get("nickname").encode("iso-8859-1").decode("utf-8")
        target_user.user_wx_openid = openid
        target_user.user_wx_union_id = union_id
        target_user.user_wx_avatar = avatar_url
        target_user.last_login_time = datetime.now(timezone.utc)
        db.session.add(target_user)
        db.session.commit()
        userinfo = target_user.to_dict()
        user_role = search_user_roles({"user_id": userinfo['user_id']}).json
        user_role = user_role.get("result", [])
        user_role = [role.get("role_name") for role in user_role]
        userinfo["user_role"] = user_role
        data = {
            "user_id": userinfo['user_id'],
            "role_name": user_role,
        }
        expire_time = (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        access_token = create_access_token(identity=str(userinfo['user_id']),
                                           expires_delta=timedelta(days=7),
                                           additional_claims=data
                                           )
        return next_console_response(result={"token": access_token, "userinfo": userinfo, "expire_time": expire_time})
    else:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)


def save_wx_avatar(avatar_url, openid):
    avatar_path = generate_new_path("user_center",
                                    user_id=openid, file_type="file",
                                    suffix=avatar_url.split(".")[-1]
                                    ).json.get("result")
    avatar = requests.get(avatar_url)
    if avatar.status_code == 200:
        # 以二进制写模式打开文件
        with open(avatar_path, 'wb') as file:
            # 写入图片内容
            file.write(avatar.content)
        return avatar_path
    return avatar_url


def bind_new_phone_send_code(data):
    """

    :param data:
    :return:
    """
    user_id = data.get("user_id")
    new_phone = data.get("new_phone")
    user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    exist_phone = UserInfo.query.filter(
        UserInfo.user_phone == new_phone,
        UserInfo.user_status == 1
    ).first()
    if exist_phone:
        return next_console_response(error_status=True, error_message="手机已被占用！", error_code=1003)
    # 找出5分钟内的重置密码任务
    old_task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_id == user_id,
        UserSendCodeTask.new_phone == new_phone,
        UserSendCodeTask.task_status == "验证中",
        UserSendCodeTask.create_time > datetime.now(timezone.utc) - timedelta(minutes=1)
    ).first()
    if old_task:
        remain_time = 60 - (datetime.now(timezone.utc) - old_task.create_time).seconds
        return next_console_response(error_status=True,
                                     error_message="请勿频繁操作！还需等待{}秒".format(remain_time),
                                     error_code=1003)
    # 生成6位随机验证码
    user_code = str(random.randint(100000, 999999))
    new_reset_password_task = UserSendCodeTask(
        user_id=user_id,
        new_phone=new_phone,
        task_code=user_code,
        task_status="验证中"
    )
    db.session.add(new_reset_password_task)
    db.session.commit()
    # 发送短信
    template_param = f'{{"code":"{user_code}"}}'
    send_sms_by_client(new_phone, template_param)
    if old_task:
        old_task.task_status = "已失效"
        db.session.add(old_task)
        db.session.commit()
    return next_console_response()


def valid_bind_new_phone(data):
    """

    :param data:
    :return:
    """
    new_phone = data.get("new_phone")
    code = data.get("code")
    user_id = int(data.get("user_id"))
    user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    # 找出最近重置密码任务
    task = UserSendCodeTask.query.filter(
        UserSendCodeTask.user_id == user_id,
        UserSendCodeTask.task_status == "验证中",
        UserSendCodeTask.new_phone == new_phone,
        UserSendCodeTask.task_code == code
    ).order_by(desc(UserSendCodeTask.create_time)).first()
    if task:
        # 超过5分钟，验证码失效
        if task.create_time < datetime.now() - timedelta(minutes=5):
            task.task_status = "已失效"
            db.session.add(task)
            db.session.commit()
            return next_console_response(error_status=True, error_message="验证码已失效！", error_code=1003)
        user.user_phone = task.new_phone
        task.task_status = "已验证"
        db.session.add(user)
        db.session.add(task)
        db.session.commit()
        return next_console_response()
    else:
        return next_console_response(error_status=True, error_message="验证码错误！", error_code=1003)


def add_user_by_excel(df, params):
    """
    通过excel批量新增用户
    返回{
        all_cnt: 1,
        finished_cnt: 1,
        error_cnt: 0,
        trace:[
        {row: 1, error: "邮箱已经被占用！"},
        ]
    """
    res_logs = []
    err_cnt = 0
    user_id = params.get("user_id")
    request_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not request_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    step1_user = []
    for index, row in df.iterrows():
        row = row.to_dict()
        user_name = str(row.get("用户名称（必填）", "测试用户"))
        user_password = str(row.get("密码（选填）", str(uuid.uuid4())))
        user_password = hashlib.sha256(str(user_password).encode()).hexdigest()
        user_password = generate_password_hash(user_password, method='pbkdf2:sha256:100000')
        user_nick_name = str(row.get("昵称（选填）", user_name))
        user_nick_name_py = get_initial_py(str(user_nick_name))
        user_email = str(row.get("邮箱（选填）", ""))
        user_phone = str(row.get("手机号（选填）", ""))
        user_gender = str(row.get("性别（选填）", "其他"))
        user_age = row.get("年龄（选填）")
        try:
            user_age = int(user_age)
        except Exception as e:
            user_age = 26
        user_company = row.get("公司（选填）", "")
        user_department = row.get("部门（选填）", "")
        user_position = row.get("职位（选填）", "")
        user_company_id = row.get("公司ID（选填）", '')
        user_department_id = row.get("部门ID（选填）", '')
        user_resource_limit = row.get("资源库空间上限，以mb为单位（选填）")

        try:
            user_resource_limit = int(user_resource_limit)
        except Exception as e:
            user_resource_limit = 2048
        user_account_type = "个人账号"
        if user_email:
            exist_user = UserInfo.query.filter(
                UserInfo.user_email == user_email
            ).first()
            if exist_user:
                res_logs.append({"error": "邮箱已被占用！", "row": index + 1})
                err_cnt += 1
                continue
        if user_phone:
            exist_user = UserInfo.query.filter(
                UserInfo.user_phone == user_phone
            ).first()
            if exist_user:
                res_logs.append({"error": "手机号已被占用！", "row": index + 1})
                err_cnt += 1
                continue
        if params["admin_type"] != 'twadmin':
            user_company_id = request_user.user_company_id
            user_department_id = request_user.user_department_id
        if user_company_id:
            target_company = CompanyInfo.query.filter(
                CompanyInfo.id == user_company_id
            ).first()
            if not target_company:
                res_logs.append({"error": "公司不存在！", "row": index + 1})
                err_cnt += 1
                continue
            user_company_id = target_company.id
            target_department = DepartmentInfo.query.filter(
                DepartmentInfo.id == user_department_id
            ).first()
            if not target_department:
                res_logs.append({"error": "部门不存在！", "row": index + 1})
                err_cnt += 1
                continue
            user_department_id = target_department.id
            user_account_type = "企业账号"
        if not user_company_id:
            user_company_id = None
        if not user_department_id:
            user_department_id = None
        new_user = UserInfo(
            user_name=user_name,
            user_password=user_password,
            user_nick_name=user_nick_name,
            user_nick_name_py=user_nick_name_py,
            user_email=user_email,
            user_phone=user_phone,
            user_gender=user_gender,
            user_age=user_age,
            user_company=user_company,
            user_department=user_department,
            user_position=user_position,
            user_resource_limit=user_resource_limit,
            user_status=1,
            user_account_type=user_account_type,
            user_company_id=user_company_id,
            user_department_id=user_department_id,
            user_source='admin',
            user_code=str(uuid.uuid4()),
        )
        db.session.add(new_user)
        step1_user.append(new_user)
    try:
        db.session.commit()
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        res_logs.append({"error": "用户创建失败", "trace": e})
        resp = {
            "total_cnt": len(df),
            "finished_cnt": 0,
            "error_cnt": len(step1_user),
            "trace": res_logs
        }
        return next_console_response(result=resp)
    init_res = batch_init_user(step1_user)
    if not init_res:
        res_logs.append({"error": "用户初始化错误"})
        return next_console_response(error_status=True, error_message="用户初始化失败！", error_code=1005)

    new_user_list = [user.to_dict() for user in step1_user if user.user_status == 1]
    admin_notice_new_user.delay(new_user_list)
    if not len(res_logs):
        res_logs.append("成功完成{}条数据的导入！".format(len(df)))

    resp = {
        "total_cnt": len(df),
        "finished_cnt": len(df) - err_cnt,
        "error_cnt": err_cnt,
        "trace": res_logs
    }
    return next_console_response(result=resp)


def batch_init_user(users):
    """
    批量初始化用户，主要是为了给用户分配角色和权限
    :return:
    """
    # 设置用户角色
    role = RoleInfo.query.filter(RoleInfo.role_name == "user").first()
    if role is None:
        return next_console_response(error_status=True, error_code=1004, error_message='角色设置错误')
    for user in users:
        new_user_role = UserRoleInfo(
            user_id=user.user_id,
            role_id=role.role_id,
            rel_status=1
        )
        db.session.add(new_user_role)
    # 设置用户对助手的权限(向所有官方助手增加可用权限，为内置助手新增服务关系)
    # 获取所有官方助手，id < 0
    all_office_assistants = Assistant.query.filter(Assistant.id < 0).all()
    for user in users:
        for assistant in all_office_assistants:
            new_user_assistant_rel = UserAssistantRelation(
                user_id=user.user_id,
                assistant_id=assistant.id,
                rel_type="权限",
                rel_value=1,
                rel_status="正常"
            )
            db.session.add(new_user_assistant_rel)
    # 创建账号信息
    from app.services.user_center.account_service import generate_account_id
    for user in users:
        exist_point_account = UserAccountInfo(
            user_id=user.user_id,
            account_id=generate_account_id(),
            account_type="point",
            balance=0,
        )
        db.session.add(exist_point_account)
    # 初始化应用配置
    from app.models.configure_center.user_config import UserConfig
    for user in users:
        user_config = UserConfig(
            user_id=user.user_id,
            open_query_agent=0,
            config_status='正常',
            resource_shortcut_types=[]
        )
        db.session.add(user_config)
    # 初始化用户资源地址
    for user in users:
        user.user_resource_base_path = generate_new_path(
            "resource_center", user_id=user.user_id, file_type="dir").json.get("result")
        db.session.add(user)
    # 初始化用户资源库
    for user in users:
        user_resource = ResourceObjectMeta(
            user_id=user.user_id,
            resource_name="我的资源",
            resource_type="folder",
            resource_desc="用户资源库",
            resource_status="正常",
            resource_path=user.user_resource_base_path,
            resource_icon="folder.svg",
            resource_source="resource_center",
        )
        db.session.add(user_resource)
    try:
        db.session.commit()
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        return next_console_response(error_status=True, error_code=1004, error_message='初始化错误')
    return True


def refresh_token_service(data):
    """
    根据超时时间，创建新的token
    Parameters
    ----------
    data

    Returns
    -------
    """
    user_id = data.get("user_id")
    expire_time = data.get("expire_time")
    user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1,
    ).first()
    if not user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1003)
    # 解析和验证过期时间
    expire_time = datetime.strptime(expire_time, "%Y-%m-%d %H:%M:%S")

    # 计算剩余有效时间
    now = datetime.now()
    if expire_time <= now:
        return next_console_response(
            error_status=True,
            error_message="过期时间必须大于当前时间！",
            error_code=1004
        )

    expires_delta = expire_time - now
    new_token = create_access_token(
        identity=str(user.user_id),
        expires_delta=expires_delta,
        additional_claims={
             "user_id": user.user_id,
        }
    )
    return next_console_response(result={"token": new_token, "expire_time": expire_time.strftime("%Y-%m-%d %H:%M:%S")})


def send_sms_by_client(phone, template_param):
    """
    发送短信
    Returns
    -------
    """
    from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
    from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
    from alibabacloud_tea_openapi import models as open_api_models
    from alibabacloud_tea_util import models as util_models
    system_tool_config = SystemConfig.query.filter(
        SystemConfig.config_key == "tools",
        SystemConfig.config_status == 1
    ).first()
    aliyun_config = open_api_models.Config(
        access_key_id=system_tool_config.config_value.get("sms", {}).get("key_id"),
        access_key_secret=system_tool_config.config_value.get("sms", {}).get("key_secret"),
        endpoint=system_tool_config.config_value.get("sms", {}).get("endpoint"),
    )
    aliyun_client = Dysmsapi20170525Client(aliyun_config)
    send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
        phone_numbers=phone,
        sign_name=system_tool_config.config_value.get("sms", {}).get("sign_name"),
        template_code=system_tool_config.config_value.get("sms", {}).get("template_code"),
        template_param=template_param
    )
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        res = aliyun_client.send_sms_with_options(send_sms_request, runtime)
        app.logger.info("短信发送结果：{}".format(res.body))
        if res.body.code != "OK":
            return next_console_response(error_status=True, error_message=res.body.message)
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        app.logger.error(error)
        return next_console_response(error_status=True, error_message="短信发送失败，请稍后重试！")
