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
