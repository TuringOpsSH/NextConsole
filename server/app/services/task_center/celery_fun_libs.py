import smtplib
from email.mime.text import MIMEText
import os
from app.app import app, celery
from jinja2 import Template


@celery.task
def send_user_create_email(to_emails, body):
    """
    发送用户创建邮件
    """
    # 配置 SMTP 服务器
    with app.app_context():
        subject = '欢迎您使用NextConsole下一代智能终端！'
        send_email_by_client(subject, to_emails, body)


@celery.task
def send_user_verification_code_email(to_emails, body):
    """
    发送用户创建邮件
    """
    # 配置 SMTP 服务器
    with app.app_context():
        subject = 'NextConsole智能体服务平台'
        send_email_by_client(subject, to_emails, body)


@celery.task
def send_user_invite_email(email, user_name, invite_url):
    """
    发送用户邀请邮件
    :param email:
    :param user_name:
    :param invite_url:
    :return:
    """
    # 配置 SMTP 服务器
    with app.app_context():
        subject = '【NextConsole】和我一起使用NextConsole吧！'
        # 创建 MIMEText 对象，并设置邮件主题、发件人、收件人
        with open(os.path.join(app.config["config_static"], "invite_code_email.html"), "r",
                  encoding="utf8") as f:
            body = f.read()
        body_template = Template(body)
        body_params = {
            "user_name": user_name,
            "invite_url": invite_url
        }
        body = body_template.render(body_params)
        send_email_by_client(subject, [email], body)


@celery.task
def send_user_first_subscription_email(email):
    """
    发送用户首次订阅邮件
    :param email:
    :return:
    """
    # 配置 SMTP 服务器
    with app.app_context():
        subject = '【NextConsole智能体服务平台】欢迎订阅'
        # 创建 MIMEText 对象，并设置邮件主题、发件人、收件人
        with open(os.path.join(app.config["config_static"], "user_subscription_notice.html"), "r",
                  encoding="utf8") as f:
            body = f.read()
        send_email_by_client(subject, [email], body)


def send_email_by_client(subject, to_emails, body):
    """
    发送邮件
    Returns
    -------
    """
    with app.app_context():
        from app.models.configure_center.system_config import SystemConfig
        system_tool_config = SystemConfig.query.filter(
            SystemConfig.config_key == "tools",
            SystemConfig.config_status == 1
        ).first()
        smtp_server = system_tool_config.config_value.get("email", {}).get("smtp_server")
        smtp_port = system_tool_config.config_value.get("email", {}).get("smtp_port")
        smtp_user = system_tool_config.config_value.get("email", {}).get("smtp_user")
        smtp_password = system_tool_config.config_value.get("email", {}).get("smtp_password")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        # 创建 MIMEText 对象，并设置邮件主题、发件人、收件人
        msg = MIMEText(body, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = ",".join(to_emails)
        server.sendmail(smtp_user, to_emails, msg.as_string())
        server.quit()