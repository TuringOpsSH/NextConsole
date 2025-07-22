import smtplib
from email.mime.text import MIMEText
import os
from app.app import app, celery
from jinja2 import Template


@celery.task
def send_user_create_email(to_emails, body):
    """
    发送用户创建成功邮件
    """
    # 配置 SMTP 服务器
    with app.app_context():
        smtp_server = app.config['smtp_server']
        smtp_port = app.config['smtp_port']
        smtp_user = app.config['smtp_user']
        smtp_password = app.config['smtp_password']
        # 配置邮件信息
        from_email = app.config['notice_email']
        subject = '欢迎使用【NextConsole智能体服务平台】'
        # 创建 MIMEText 对象，并设置邮件主题、发件人、收件人
        msg = MIMEText(body, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ",".join(to_emails)

        # 连接 SMTP 服务器并发送邮件
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()


@celery.task
def send_user_verification_code_email(to_emails, body):
    """
    发送用户创建验证码邮件
    """
    # 配置 SMTP 服务器
    with app.app_context():
        smtp_server = app.config['smtp_server']
        smtp_port = app.config['smtp_port']
        smtp_user = app.config['smtp_user']
        smtp_password = app.config['smtp_password']
        # 配置邮件信息
        from_email = app.config['notice_email']
        subject = '【NextConsole智能体服务平台】验证码'
        # 创建 MIMEText 对象，并设置邮件主题、发件人、收件人
        msg = MIMEText(body, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ",".join(to_emails)

        # 连接 SMTP 服务器并发送邮件
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()


@celery.task
def test_email(email_type):
    """
    测试邮件发送的模板效果
    :param email_type:
    :return:
    """
    with app.app_context():
        smtp_server = app.config['smtp_server']
        smtp_port = app.config['smtp_port']
        smtp_user = app.config['smtp_user']
        smtp_password = app.config['smtp_password']
        from_email = app.config['notice_email']
        to_email = "calvin.xing@turingops.com.cn"
        if email_type == "user_welcome":
            subject = '欢迎使用【NextConsole智能体服务平台】'
            hello_html = "user_welcome.html"
            with open(os.path.join(app.config["config_static"], hello_html), "r", encoding="utf8") as f:
                info_html = f.read()
            info_html_template = Template(info_html)
            info_params = {
                "user_name": "test_user"
            }
            info_html = info_html_template.render(info_params)
        elif email_type == "user_verification_code":
            subject = '【NextConsole智能体服务平台】验证码'
            hello_html = "user_verification_code.html"
            with open(os.path.join(app.config["config_static"], hello_html), "r", encoding="utf8") as f:
                info_html = f.read()
            info_html_template = Template(info_html)
            info_params = {
                "code": "232323"
            }
            info_html = info_html_template.render(info_params)
        else:
            return
        msg = MIMEText(info_html, 'html', 'utf-8')

        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # 连接 SMTP 服务器并发送邮件
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()


@celery.task
def send_user_first_subscription_email(email):
    """
    发送用户首次订阅邮件
    :param email:
    :return:
    """
    # 配置 SMTP 服务器
    with app.app_context():
        smtp_server = app.config['smtp_server']
        smtp_port = app.config['smtp_port']
        smtp_user = app.config['smtp_user']
        smtp_password = app.config['smtp_password']
        # 配置邮件信息
        from_email = app.config['notice_email']
        subject = '【NextConsole智能体服务平台】欢迎订阅'
        # 创建 MIMEText 对象，并设置邮件主题、发件人、收件人
        with open(os.path.join(app.config["config_static"], "user_subscription_notice.html"), "r",
                  encoding="utf8") as f:
            body = f.read()
        msg = MIMEText(body, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = email

        # 连接 SMTP 服务器并发送邮件
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, email, msg.as_string())
        server.quit()
