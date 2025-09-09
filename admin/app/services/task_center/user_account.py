import os
import smtplib
from datetime import timedelta, datetime
from email.mime.text import MIMEText

from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from jinja2 import Template
from app.app import app
from app.app import celery
from app.models.contacts.company_model import CompanyInfo
from app.models.contacts.department_model import DepartmentInfo
from app.models.user_center.user_info import *


@celery.task
def user_account_auto_upgrade():
    """
    自动升级企业账号
    :return:
    """
    with app.app_context():
        all_users = UserInfo.query.filter(
            UserInfo.user_status == 1,
            UserInfo.user_account_type == "个人账号",
            UserInfo.user_company_id.is_(None),
            UserInfo.user_email.like("%ce-service.com.cn")
        ).all()
        target_company = CompanyInfo.query.filter(
            CompanyInfo.company_name == "北京中亦安图科技股份有限公司"
        ).first()
        if not target_company:
            return "北京中亦安图科技股份有限公司 不存在"
        target_department = DepartmentInfo.query.filter(
            DepartmentInfo.company_id == target_company.id,
            DepartmentInfo.parent_department_id.is_(None)
        ).first()
        if not target_department:
            return "北京中亦安图科技股份有限公司 根部门 不存在"
        all_update_user = []
        for user in all_users:
            user.user_account_type = "企业账号"
            user.user_company_id = target_company.id
            user.user_department_id = target_department.id
            db.session.add(user)
            all_update_user.append(user)
        db.session.commit()
        return f"升级{len(all_update_user)}个用户账号"

@celery.task
def product_delivery_task(params):
    """
    产品交付
    :return:
    """
    with app.app_context():
        order_id = params.get("order_id")
        target_order = OrderInfo.query.filter(
            OrderInfo.id == order_id
        ).first()
        if not target_order:
            return "订单不存在"
        target_user = UserInfo.query.filter(
            UserInfo.user_id == target_order.user_id,
            UserInfo.user_status == 1
        ).first()
        if not target_user:
            return "用户不存在"
        all_order_item = OrderItemInfo.query.filter(
            OrderItemInfo.order_code == target_order.order_code,
            OrderItemInfo.order_item_status == "待发货"
        ).all()
        all_success_flag = True
        send_result = []
        from app.models.configure_center.system_config import SystemConfig
        system_tool_config = SystemConfig.query.filter(
            SystemConfig.config_key == "tools",
            SystemConfig.config_status == 1
        ).first()
        smtp_server = system_tool_config.config_value.get("email", {}).get("smtp_server")
        smtp_port = system_tool_config.config_value.get("email", {}).get("smtp_port")
        smtp_user = system_tool_config.config_value.get("email", {}).get("smtp_user")
        smtp_password = system_tool_config.config_value.get("email", {}).get("smtp_password")
        for order_item in all_order_item:

            try:
                if "@" in target_order.delivery_message:
                    subject = '【NextConsole智能体服务平台】商品交付通知'
                    # 创建 MIMEText 对象，并设置邮件主题、发件人、收件人
                    with open(os.path.join(app.config["config_static"], "product_delivery_message.html"), "r",
                              encoding="utf8") as f:
                        info_html = f.read()
                        info_html_template = Template(info_html)
                        info_html = info_html_template.render({
                            "item": order_item.order_item_name,
                            "code": order_item.redemption_code,
                        })
                    msg = MIMEText(info_html, 'html', 'utf-8')
                    msg['Subject'] = subject
                    msg['From'] = smtp_user
                    msg['To'] = target_order.delivery_message

                    # 连接 SMTP 服务器并发送邮件
                    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
                    server.login(smtp_user, smtp_password)
                    server.sendmail(smtp_user, target_order.delivery_message, msg.as_string())
                    server.quit()
                else:
                    # 发送短信
                    template_param = f'{{"code":"{order_item.redemption_code}" , "item":"{order_item.order_item_name}"}}'
                    # 发送短信
                    send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
                        phone_numbers=target_order.delivery_message,
                        sign_name=app.config["sign_name"],
                        template_code=app.config["product_delivery_code"],
                        template_param=template_param
                    )
                    runtime = util_models.RuntimeOptions()
                order_item.order_item_status = "已交付"
                db.session.add(order_item)
                db.session.commit()
            except Exception as e:
                print(f"交付失败:{str(e)}")
                app.logger.error(f"交付失败:{str(e)}")
                send_result.append(f"交付失败:{str(e)}")
                order_item.order_item_status = "交付失败"
                db.session.add(order_item)
                db.session.commit()
                all_success_flag = False
        db.session.commit()
        if all_success_flag:
            target_order.order_status = "交付完成"
        else:
            target_order.order_status = "交付异常"
        db.session.add(target_order)
        db.session.commit()
        return send_result








