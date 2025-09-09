from app.models.contacts.company_model import *
from app.models.user_center.user_info import *
from app.services.configure_center.response_utils import *


def get_company_info(params):
    """
    获取公司信息
    """
    user_id = params.get('user_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_code=1001, error_message='用户不存在')
    if target_user.user_account_type != '企业账号':
        return next_console_response(error_message='用户未认证')
    if not target_user.user_company_id:
        return next_console_response(error_message='用户未加入公司')
    company_info = CompanyInfo.query.filter(
        CompanyInfo.id == target_user.user_company_id,
        CompanyInfo.company_status == '正常'
    ).first()
    if not company_info:
        return next_console_response(error_message='公司不存在')
    # 新增员工统计
    user_count = UserInfo.query.filter(
        UserInfo.user_company_id == company_info.id,
        UserInfo.user_status == 1
    ).count()
    company_info_dict = company_info.to_dict()
    company_info_dict['user_count'] = user_count
    return next_console_response(result=company_info_dict)





