# Desc: Coupon相关服务
# from sqlalchemy.sql import text
# from sqlalchemy.exc import IntegrityError
import random
import string
from sqlalchemy import inspect
from app.services.configure_center.response_utils import next_console_response
from app.models.user_center.coupon_info import *
from app.models.user_center.coupon_use_detail import *
from datetime import datetime,timedelta



def is_valid_datetime_ts(datetime_str):
    """
    判断日期时间格式是否正确yyyy-MM-dd HH:mm:ss
    """
    try:
        datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


def is_exist_coupon_info_table():
    """
    判断 coupon_info 表是否存在
    """
    inspector = inspect(db.engine)
    if "coupon_info" in inspector.get_table_names():
        return True
    else:
        return False


def generate_coupon_info_by_batch(params):
    """
    根据params，循环生成n个16位优惠券码，并插入到coupon_info表，而且与coupon_info中的coupon_text字段不重复，但是要保证n条记录都插入成功，如果发现重复，需要重新再生成一个优惠券码
    """
    n = params.get("coupon_number")
    created_count = 0
    coupon_name = params.get("coupon_name")
    coupon_desc = params.get("coupon_desc")
    coupon_token_points = params.get("coupon_token_points")
    coupon_start_date = params.get("coupon_start_date")
    coupon_end_date = params.get("coupon_end_date")
    coupon_status = params.get("coupon_status")
    coupon_type = params.get("coupon_type")
    coupon_used_cnt_limit = params.get("coupon_used_cnt_limit")

    max_attempts = 100000
    attempts = 0

    if not n:
        return next_console_response(error_status=True, error_code=1004, error_message="生成优惠券码数量不能为空！")
    elif not isinstance(n, int):
        return next_console_response(error_status=True, error_code=1004, error_message="生成优惠券码数量格式错误！")
    elif n <= 0:
        return next_console_response(error_status=True, error_code=1004, error_message="生成优惠券码数量必须大于0！")
    elif n>max_attempts:
        return next_console_response(error_status=True, error_code=1004, error_message="生成优惠券码数量不能超过100000！")
    elif not coupon_name:
        return next_console_response(error_status=True, error_code=1004, error_message="优惠券名称不能为空！")
    elif not coupon_start_date:
        return next_console_response(error_status=True, error_code=1004, error_message="优惠券开始日期不能为空！")
    elif not is_valid_datetime_ts(coupon_start_date):
        return next_console_response(error_status=True, error_code=1004, error_message="优惠券开始日期格式错误，应为yyyy-MM-dd HH:mm:ss！")
    elif not coupon_end_date:
        return next_console_response(error_status=True, error_code=1004, error_message="优惠券结束日期不能为空！")
    elif not is_valid_datetime_ts(coupon_end_date):
        return next_console_response(error_status=True, error_code=1004, error_message="优惠券结束日期格式错误，应为yyyy-MM-dd HH:mm:ss！")
    elif coupon_start_date >= coupon_end_date:
        return next_console_response(error_status=True, error_code=1004, error_message="优惠券开始日期必须小于结束日期！")
    elif not coupon_type:
        return next_console_response(error_status=True, error_code=1004, error_message="优惠券类型不能为空！")
    elif coupon_type =='1':
        if not coupon_used_cnt_limit:
            return next_console_response(error_status=True, error_code=1004, error_message="优惠券使用次数上限不能为空！")
        elif not isinstance(coupon_used_cnt_limit, int):
            return next_console_response(error_status=True, error_code=1004, error_message="优惠券使用次数上限格式错误！")
        elif coupon_used_cnt_limit <= 0:
            return next_console_response(error_status=True, error_code=1004, error_message="优惠券使用次数上限必须大于0！")    

    coupon_result = []

    while created_count < n and attempts < max_attempts:
        coupon_text = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        cpn = CouponInfo.query.filter(CouponInfo.coupon_text == coupon_text).first()
        if not cpn:
            if not coupon_desc:
                coupon_desc = ""
            if not coupon_token_points:
                coupon_token_points = 1000000
            if not coupon_status:
                coupon_status = '1'
            if coupon_type == '0':
                coupon_used_cnt_limit = 99999999
            new_coupon = CouponInfo(coupon_text=coupon_text,coupon_name=coupon_name,coupon_desc=coupon_desc,coupon_token_points=coupon_token_points,coupon_start_date=coupon_start_date,coupon_end_date=coupon_end_date,coupon_status=coupon_status,coupon_type=coupon_type,coupon_used_cnt_limit=coupon_used_cnt_limit)
            db.session.add(new_coupon)
            created_count += 1
            coupon_result.append(new_coupon.to_dict_result())
        attempts += 1
            
    if created_count == n:
        db.session.commit()
        return next_console_response(result={"total_counts":created_count,"coupon_result":coupon_result}, error_status=False, error_code=0, error_message="生成优惠券码成功！")
    else:
        return next_console_response(error_status=True, error_code=2001, error_message="生成优惠券码失败！")

def generate_coupon_info_simple(params):
    """
    根据params，生成一个16位优惠券码，并插入到coupon_info表，而且与coupon_info中的coupon_text字段不重复
    """
    if not params.get("coupon_name"):
        params["coupon_name"] = "优惠券"
    if not params.get("coupon_desc"):
        params["coupon_desc"] = "普通优惠券"
    if not params.get("coupon_token_points"):
        params["coupon_token_points"] = 1000000
    if not params.get("coupon_start_date"):
        params["coupon_start_date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 按照入参的优惠券有效天数计算结束日期
    coupon_days = params.get("coupon_days")
    if not coupon_days:
        params["coupon_days"] = 3
    elif not isinstance(coupon_days, int):
        return next_console_response(error_status=True, error_code=1004, error_message="优惠券有效天数格式错误！")
    elif coupon_days <= 0:
        return next_console_response(error_status=True, error_code=1004, error_message="优惠券有效天数必须大于0！")
    # 设置 params["coupon_end_date"] = params["coupon_start_date"] + 3 coupon_days 天
    params["coupon_end_date"] = (datetime.now() + timedelta(days=coupon_days)).replace(hour=23, minute=59, second=59).strftime('%Y-%m-%d %H:%M:%S')
    if not params.get("coupon_type"):
        params["coupon_type"] = '1'
        if not params.get("coupon_used_cnt_limit"):
            params["coupon_used_cnt_limit"] = 1
    if not params.get("coupon_number"):
        params["coupon_number"] = 10

    return generate_coupon_info_by_batch(params)

