import smtplib
import time
from email.mime.text import MIMEText
from jinja2 import Template
import requests
import os
from app.app import app, db
from app.app import celery
from app.models.user_center.system_notice_model import NoticeTaskInfo, NoticeTaskInstance, SystemNotice


@celery.task
def notice_user_by_email(data_list):
    """
    通过邮件通知用户
    :param data_list:
    :return:
    """
    with app.app_context():
        # 发送邮件配置
        from app.models.configure_center.system_config import SystemConfig
        system_tool_config = SystemConfig.query.filter(
            SystemConfig.config_key == "tools",
            SystemConfig.config_status == 1
        ).first()
        smtp_server = system_tool_config.config_value.get("email", {}).get("smtp_server")
        smtp_ssl = system_tool_config.config_value.get("email", {}).get("smtp_ssl")
        smtp_port = system_tool_config.config_value.get("email", {}).get("smtp_port")
        smtp_user = system_tool_config.config_value.get("email", {}).get("smtp_user")
        smtp_password = system_tool_config.config_value.get("email", {}).get("smtp_password")
        if smtp_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        for data in data_list:
            task_instance_id = data.get("id")
            task_instance = NoticeTaskInstance.query.filter_by(id=task_instance_id).first()
            subject = task_instance.notice_params.get("subject")
            content = task_instance.notice_content
            user_email = task_instance.notice_params.get("user_email")
            if not user_email:
                app.logger.error("用户邮箱为空")
                # 更新任务状态
                task_info = NoticeTaskInfo.query.filter_by(id=task_instance.task_id).with_for_update().first()
                task_info.task_instance_failed += 1
                if not task_info.begin_time:
                    task_info.begin_time = db.func.now()
                if task_info.task_instance_total == task_info.task_instance_success + task_info.task_instance_failed:
                    task_info.task_status = "已完成"
                    task_info.finish_time = db.func.now()
                db.session.add(task_info)
                db.session.commit()
                return "用户邮箱为空"

            if task_instance.notice_status in ("已暂停", "已终止"):
                return "任务已被撤销"
            try:
                msg = MIMEText(content, 'html', 'utf-8')
                msg['Subject'] = subject
                msg['From'] = smtp_user
                msg['To'] = user_email
                server.sendmail(smtp_user, user_email, msg.as_string())
                task_instance.notice_status = "已通知"
            except Exception as e:
                app.logger.error("邮件发送失败: %s" % str(e))
                task_instance.notice_status = "通知失败"
                return "邮件发送失败"
            finally:
                # 更新通知状态
                db.session.add(task_instance)
                db.session.commit()
                # 更新任务状态
                task_info = NoticeTaskInfo.query.filter_by(id=task_instance.task_id).with_for_update().first()
                if task_instance.notice_status == "已通知":
                    task_info.task_instance_success += 1
                else:
                    task_info.task_instance_failed += 1
                if not task_info.begin_time:
                    task_info.begin_time = db.func.now()
                if task_info.task_instance_total == task_info.task_instance_success + task_info.task_instance_failed:
                    task_info.task_status = "已完成"
                    task_info.finish_time = db.func.now()
                db.session.add(task_info)
                db.session.commit()
        server.quit()
        return "邮件发送成功"


@celery.task
def notice_user_by_sms(data):
    """
    通过短信通知用户
    :param data:
    :return:
    """
    pass


@celery.task
def notice_user_by_message(data_list):
    """
    通过站内信通知用户
    :param data_list:
    :return:
    """
    with app.app_context():
        # 发送站内信
        app.logger.warning(f"开始发送站内信通知:{len(data_list)}")
        flag = False
        for data in data_list:
            task_instance_id = data.get("id")
            task_instance = NoticeTaskInstance.query.filter_by(id=task_instance_id).first()
            subject = task_instance.notice_params.get("subject")
            user_id = task_instance.notice_params.get("user_id")
            if task_instance.notice_status in ("已暂停", "已终止"):
                return "任务已被撤销"

            new_notice = SystemNotice(
                user_id=user_id,
                notice_title=subject,
                notice_icon="notice_success.svg",
                notice_type="系统通知",
                notice_level="普通",
                notice_content=task_instance.notice_content,
                notice_status="未读"
            )
            db.session.add(new_notice)
            task_instance.notice_status = "已通知"
        try:
            db.session.commit()
            flag = True
        except Exception as e:
            app.logger.error("站内信发送失败: %s" % str(e))
            db.session.rollback()
            flag = False
        finally:
            # 更新任务状态
            task_info = NoticeTaskInfo.query.filter_by(id=task_instance.task_id).with_for_update().first()
            if flag:
                task_info.task_instance_success += len(data_list)
            else:
                task_info.task_instance_failed += len(data_list)
            if not task_info.begin_time:
                task_info.begin_time = db.func.now()
            if task_info.task_instance_total == task_info.task_instance_success + task_info.task_instance_failed:
                task_info.task_status = "已完成"
                task_info.finish_time = db.func.now()
            db.session.add(task_info)
            db.session.commit()
        return "站内信发送成功"


@celery.task
def admin_notice_new_user(user_list):
    """
    管理员通知新用户
    :return:
    """
    with app.app_context():
        # 发送邮件配置
        from app.models.configure_center.system_config import SystemConfig
        system_tool_config = SystemConfig.query.filter(
            SystemConfig.config_key == "tools",
            SystemConfig.config_status == 1
        ).first()
        smtp_server = system_tool_config.config_value.get("email", {}).get("smtp_server")
        smtp_ssl = system_tool_config.config_value.get("email", {}).get("smtp_ssl")
        smtp_port = system_tool_config.config_value.get("email", {}).get("smtp_port")
        smtp_user = system_tool_config.config_value.get("email", {}).get("smtp_user")
        smtp_password = system_tool_config.config_value.get("email", {}).get("smtp_password")
        subject = '欢迎使用【NextConsole智能体服务平台】'
        if smtp_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        for new_user in user_list:
            hello_html = "user_welcome.html"
            with open(os.path.join(app.config["config_static"], hello_html), "r", encoding="utf8") as f:
                info_html = f.read()
            info_html_template = Template(info_html)
            info_params = {}
            info_html = info_html_template.render(info_params)
            # 创建 MIMEText 对象，并设置邮件主题、发件人、收件人
            msg = MIMEText(info_html, 'html', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = new_user.get("user_email")
            # 连接 SMTP 服务器并发送邮件
            try:
                server.sendmail(smtp_user, [new_user.get("user_email")], msg.as_string())
            except Exception as e:
                app.logger.error("邮件发送失败: %s" % str(e))
                time.sleep(30)
                continue
        server.quit()
