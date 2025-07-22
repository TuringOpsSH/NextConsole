import re

from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import jwt
from app.services.user_center.account_service import *
from app.services.user_center.users import *
from app.services.configure_center.system_config import get_support_area_data


@jwt.unauthorized_loader
def missing_token_callback(error):
    return next_console_response(error_status=True, error_message="请重新登录！", error_code=401)


@app.route("/next_console/get_support_area", methods=["GET", "POST"])
def get_support_area():
    return get_support_area_data()


@app.route("/next_console/check_register_email", methods=["GET", "POST"])
def check_register_email():
    data = request.get_json()
    user_email = data.get("user_email")
    if not user_email:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return register_email_check(user_email)


def register():
    """
    注册用户、初始化、发送确认邮件
    :return:
    """
    data = request.get_json()
    user_email = data.get('user_email')
    user_password = data.get('user_password')
    if not (user_email and user_password):
        return next_console_response(error_status=True, error_message="邮箱或密码未提交！", error_code=1002)
    user_source = data.get('user_source', "email")
    if user_source not in ("email", "qy_email", "admin", "wx", "qy_wx", "phone"):
        return next_console_response(error_status=True, error_message="用户来源错误！", error_code=1002)
    return register_user(data)


@app.route('/next_console/confirm_email', methods=['GET', 'POST'])
def confirm_register_email():
    """
    根据验证码确认注册邮箱
    :return:
    """
    data = request.get_json()
    user_email = data.get('email')
    valid_code = data.get('code')
    if not user_email or not valid_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return confirm_email_user(data)


@app.route('/next_console/resend_confirm_email', methods=['GET', 'POST'])
def resend_register_confirm_email():
    """
    重新发送注册确认邮件
    :return:
    """
    data = request.get_json()
    user_email = data.get('user_email')
    if not user_email:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)

    return resend_register_confirm_email_service(user_email)


@app.route('/next_console/login_by_password', methods=['POST'])
def login_by_password():
    """
    密码登录
    :return:
    """
    data = request.get_json()
    user_account = data.get('user_account')
    user_password = data.get('user_password')
    if not user_account and not user_password:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    client_ip = request.headers.get('X-Real-IP', request.remote_addr)
    if client_ip:
        app.logger.warning(f"ip监控:{client_ip}:{user_account}")
    return login_user(data)


@app.route("/next_console/reset_account_password", methods=["POST"])
def reset_account_password():
    """
    生成验证码并发送重置密码邮件
    :return:
    """
    data = request.get_json()
    user_account = data.get("user_account")
    new_password = data.get("new_password")
    if not user_account or not new_password:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return reset_account_password_send_code(data)


@app.route("/next_console/reset_password_code/valid", methods=["POST"])
def reset_password_code_valid():
    data = request.get_json()
    user_account = data.get("user_account")
    code = data.get("code")
    if not user_account or not code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return valid_reset_password_code(data)


@app.route('/next_console/user_center/users/get', methods=['POST'])
@jwt_required()
def user_get():
    """
    获取用户详情
    """
    user_id = get_jwt_identity()
    return get_user(user_id)


@app.route('/next_console/user_center/users/update', methods=['POST'])
@jwt_required()
def user_update():
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return update_user(params)


@app.route('/next_console/user_center/users/avatar/update', methods=['POST'])
@jwt_required()
def user_avatar_update():
    user_id = get_jwt_identity()
    avatar = request.files['avatar']
    if not user_id or not avatar:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return update_user_avatar(user_id, avatar)


@app.route('/next_console/user_center/users/close', methods=['POST'])
@jwt_required()
def user_close():
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return close_user(params)


@app.route("/next_console/reset_new_email", methods=["POST"])
@jwt_required()
def reset_new_email():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    new_email = data.get("new_email")
    if not new_email:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return reset_new_email_send_code(data)


@app.route("/next_console/reset_email_code/valid", methods=["POST"])
@jwt_required()
def reset_email_code_valid():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    new_email = data.get("new_email")
    code = data.get("code")
    if not code or not new_email:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return valid_reset_email_code(data)


@app.route('/next_console/user_center/generate_text_code', methods=['POST'])
def send_text_code():
    """
    根据请求发送验证码
    :return:
    """
    data = request.get_json()
    phone = data.get("user_phone")
    email = data.get("user_email")
    if not phone and not email:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    # 验证手机号格式
    if phone:
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return next_console_response(error_status=True, error_message="手机号格式错误！", error_code=1002)
        return send_text_code_aliyun(data)
    if email:
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return next_console_response(error_status=True, error_message="邮箱格式错误！", error_code=1002)
        return send_text_code_email(data)


@app.route('/next_console/login_by_code', methods=['POST'])
def login_by_code():
    data = request.get_json()
    user_account = data.get('user_account')
    text_code = data.get('text_code')
    if not user_account and not text_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    client_ip = request.headers.get('X-Real-IP', request.remote_addr)
    if client_ip:
        app.logger.warning(f"ip监控:{client_ip}:{user_account}")
    return register_or_login_account_by_code(data)


@app.route("/next_console/wx_register", methods=["POST"])
def wx_register():
    data = request.get_json()
    code = data.get("code")
    if not code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return wx_register_user(data)


@app.route("/next_console/user_center/bind_new_phone", methods=["POST"])
@jwt_required()
def bind_new_phone():
    """
    绑定新手机
    :return:
    """
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    new_phone = data.get("new_phone")
    if not new_phone:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return bind_new_phone_send_code(data)


@app.route("/next_console/user_center/valid_new_phone", methods=["POST"])
@jwt_required()
def valid_new_phone():
    """
    绑定新手机
    :return:
    """
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    new_phone = data.get("new_phone")
    code = data.get("code")
    if not new_phone or not code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return valid_bind_new_phone(data)


@app.route("/next_console/user_center/refresh_invite_code", methods=["POST"])
@jwt_required()
def refresh_invite_code():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    return refresh_user_invite_code(data)


@app.route("/next_console/user_center/send_invite_code_by_email", methods=["POST"])
@jwt_required()
def send_invite_email():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    user_email = data.get("user_email")
    if not user_email:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return send_invite_code_by_email(data)


@app.route("/next_console/user_center/get_invite_detail", methods=["POST"])
def get_invite_detail():
    data = request.get_json()
    invite_code = data.get("invite_code")
    if not invite_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return get_invite_detail_by_code(data)


@app.route("/next_console/user_center/accept_invite_friend", methods=["POST"])
@jwt_required()
def accept_invite_friend():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    invite_view_id = data.get("invite_view_id")
    try:
        data["invite_view_id"] = int(invite_view_id)
    except ValueError as e:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return accept_friend_by_code(data)


@app.route("/next_console/user_center/update_invite_status", methods=["POST"])
def update_invite_status():
    data = request.get_json()
    invite_view_id = data.get("invite_view_id")
    try:
        data["invite_view_id"] = int(invite_view_id)
    except ValueError as e:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return update_invite_stage(data)


@app.route("/next_console/user_center/add_website_invite", methods=["POST"])
def add_website_invite():
    data = request.get_json()
    return add_website_invite_code(data)


@app.route("/next_console/user_center/init_account", methods=["POST"])
@jwt_required()
def init_user_account_api():
    data = request.get_json()
    user_id = get_jwt_identity()
    target_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    data["user"] = target_user
    return init_user_account(data)


@app.route("/next_console/user_center/list_points_transaction", methods=["POST"])
@jwt_required()
def list_points_transaction_api():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    client_ip = request.headers.get('X-Real-IP', request.remote_addr)
    if client_ip:
        app.logger.warning(f"ip监控:{client_ip}:{user_id}")
    return list_points_transaction(data)


@app.route("/next_console/user_center/list_products", methods=["POST"])
def list_products_api():
    """
    获取用户产品列表
    :return:
    """
    data = request.get_json()
    return list_products(data)


@app.route("/next_console/user_center/init_order", methods=["POST"])
@jwt_required()
def init_order():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    product_info = data.get("product_info")
    account_id = data.get("account_id")
    payment_method = data.get("payment_method")
    if not product_info or not account_id or not payment_method:
        return next_console_response(error_status=True, error_message="参数错误！")
    return init_user_order(data)


@app.route("/next_console/user_center/get_order", methods=["POST"])
@jwt_required()
def get_order():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    order_code = data.get("order_code")
    if not order_code:
        return next_console_response(error_status=True, error_message="参数错误！")
    return get_user_order_detail(data)


@app.route("/next_console/user_center/confirm_order", methods=["POST"])
@jwt_required()
def confirm_order():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    order_code = data.get("order_code")
    if not order_code:
        return next_console_response(error_status=True, error_message="参数错误！")
    return confirm_user_order(data)


@app.route("/next_console/user_center/cancel_order", methods=["POST"])
@jwt_required()
def cancel_order():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    order_code = data.get("order_code")
    if not order_code:
        return next_console_response(error_status=True, error_message="参数错误！")
    return cancel_user_order(data)


@app.route("/next_console/user_center/remove_order_item", methods=["POST"])
@jwt_required()
def remove_order_item():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    order_item_id = data.get("order_item_id")
    if not order_item_id:
        return next_console_response(error_status=True, error_message="参数错误！")
    return remove_user_order_item(data)


@app.route("/next_console/user_center/add_order_item", methods=["POST"])
@jwt_required()
def add_order_item():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    order_code = data.get("order_code")
    if not order_code:
        return next_console_response(error_status=True, error_message="参数错误！")
    return add_user_order_item(data)


@app.route("/next_console/user_center/generate_exchange_code", methods=["POST"])
@jwt_required()
def generate_exchange_code():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    user_account = data.get("user_account")
    if not user_account:
        return next_console_response(error_status=True, error_message="参数错误！")
    return generate_exchange_valid_code(data)


@app.route("/next_console/user_center/valid_exchange_code", methods=["POST"])
@jwt_required()
def valid_exchange_code():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    user_account = data.get("user_account")
    user_code = data.get("user_code")
    if not user_account or not user_code:
        return next_console_response(error_status=True, error_message="参数错误！")
    return valid_exchange_valid_code(data)


@app.route("/next_console/user_center/list_orders", methods=["POST"])
@jwt_required()
def list_orders():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    return list_user_orders(data)


@app.route("/next_console/user_center/check_market_info", methods=["POST"])
@jwt_required()
def check_market_info():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id
    return get_market_valid_info(data)
