from app.models.user_center.user_info import *
from app.models.contacts.company_model import *
from app.services.configure_center.response_utils import next_console_response
import uuid
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from app.app import db, app
from sqlalchemy import or_, and_
from datetime import timedelta


def generate_account_id():
    """
    生成账户id
    :return:
    """
    account_id = "account_" + str(uuid.uuid1()).replace("-", "")
    return account_id


def generate_transaction_id():
    """
    生成交易id
        tx_id + 时间戳 + uuid
    :return:
    """
    transaction_id = "tx_" + str(uuid.uuid1()).replace("-", "")
    return transaction_id


def generate_order_id():
    """
    生成订单id
    :return:
    """
    order_id = "order_" + str(uuid.uuid1()).replace("-", "")
    return order_id


def init_user_account(params):
    """
    初始化用户账户
    :param params:
    :return:
    """
    user = params.get('user')
    if not user:
        return next_console_response(error_status=True, error_message="用户id不能为空")
    # 初始化积分账户
    exist_point_account = UserAccountInfo.query.filter(
        UserAccountInfo.user_id == user.user_id,
        UserAccountInfo.account_type == "point"
    ).first()
    if not exist_point_account:
        exist_point_account = UserAccountInfo(
            user_id=user.user_id,
            account_id=generate_account_id(),
            account_type="point",
            balance=0,
        )
        db.session.add(exist_point_account)
        db.session.commit()
        # 注册即送20积分
        rule = PointsRule.query.filter(
            PointsRule.rule_code == "rc_0001",
            PointsRule.rule_status == "正常"
        ).first()
        if rule:
            try:
                # 触发规则
                transaction_id = generate_transaction_id()
                new_rule_record = PointsRuleTriggerRecord(
                    user_id=user.user_id,
                    rule_id=rule.id,
                    transaction_id=transaction_id,
                    user_email=user.user_email,
                    user_phone=user.user_phone,
                    user_wx_id=user.user_wx_openid,
                    account_id=exist_point_account.account_id,
                    result_status="成功",
                )
                db.session.add(new_rule_record)
                point_transaction = PointsTransactionInfo(
                    account_id=exist_point_account.account_id,
                    transaction_id=transaction_id,
                    transaction_type=rule.rule_type,
                    transaction_amount=rule.rule_value,
                    transaction_status="成功",
                    transaction_desc=rule.rule_desc,
                )
                db.session.add(point_transaction)
                exist_point_account.balance += rule.rule_value
                db.session.add(exist_point_account)
                db.session.commit()
            except SQLAlchemyError as e:
                app.logger.error("初始化用户积分账户失败: %s" % e)
                db.session.rollback()
                return next_console_response(error_status=True, error_message="初始化用户积分账户失败")
    return next_console_response(result=exist_point_account.to_dict())


def get_user_account_info(params):
    """
    获取用户账户信息
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    if not user_id:
        return next_console_response(error_status=True, error_message="用户id不能为空")
    account_type = params.get('account_type')
    if not account_type:
        return next_console_response(error_status=True, error_message="账户类型不能为空")
    account_info = UserAccountInfo.query.filter(
        UserAccountInfo.user_id == user_id,
        UserAccountInfo.account_type == account_type
    ).first()
    if not account_info:
        return next_console_response(error_status=True, error_message="账户信息不存在")
    return next_console_response(result=account_info.to_dict())


def list_points_transaction(params):
    """
    获取积分交易列表
    :return:
    """
    user_id = params.get('user_id')
    if not user_id:
        return next_console_response(error_status=True, error_message="用户id不能为空")
    page_num = params.get('page_num', 1)
    page_size = params.get('page_size', 10)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    point_account = UserAccountInfo.query.filter(
        UserAccountInfo.user_id == user_id,
        UserAccountInfo.account_type == "point"
    ).first()
    if not point_account:
        return next_console_response(error_status=True, error_message="积分账户不存在")
    point_transactions = PointsTransactionInfo.query.filter(
        PointsTransactionInfo.account_id == point_account.account_id
    ).order_by(
        PointsTransactionInfo.create_time.desc()
    ).paginate(page=page_num, per_page=page_size, error_out=False)
    result = {
        "total": point_transactions.total,
        "page_num": point_transactions.page,
        "page_size": point_transactions.per_page,
        "data": [point_transaction.to_dict() for point_transaction in point_transactions]
    }
    return next_console_response(result=result)


def add_invite_user_points_service(params):
    """
    邀请用户送积分
    :param params:
    :return:
    """
    new_user = params.get("new_user")
    invite_user = params.get("invite_user")
    if not new_user:
        return next_console_response(error_status=True, error_message="新用户信息不能为空")
    if not invite_user:
        return next_console_response(error_status=True, error_message="邀请用户信息不能为空")
    # 邀请用户送积分
    rule = PointsRule.query.filter(
        PointsRule.rule_code == "rc_0003",
        PointsRule.rule_status == "正常"
    ).first()
    if not rule:
        return next_console_response(error_status=True, error_message="邀请用户送积分规则不存在")
    # 触发规则
    # 如果该用户的邀新奖励已经被领取，则不再继续
    exist = PointsRuleTriggerRecord.query.filter(

        PointsRuleTriggerRecord.rule_id == rule.id,
        PointsRuleTriggerRecord.result_status == "成功",
        or_(
            PointsRuleTriggerRecord.user_id == new_user.user_id,
            and_(
                PointsRuleTriggerRecord.user_phone == new_user.user_phone,
                new_user.user_phone is not None,
                new_user.user_phone != ""
            ),
            and_(
                PointsRuleTriggerRecord.user_wx_id == new_user.user_wx_openid,
                new_user.user_wx_openid is not None,
                new_user.user_wx_openid != ""
            ),
        )
    ).all()
    if exist:
        new_failed_record = PointsRuleTriggerRecord(
            user_id=new_user.user_id,
            rule_id=rule.id,
            user_email=new_user.user_email,
            user_phone=new_user.user_phone,
            user_wx_id=new_user.user_wx_openid,
            result_status="失败",
            error_code="101",
            error_message="该用户邀新奖励已被领取",
        )
        db.session.add(new_failed_record)
        db.session.commit()
        return next_console_response(error_status=True, error_message="该用户邀新奖励已被领取")
    # 如果该用户仅有邮箱，则不再继续
    if not new_user.user_phone and not new_user.user_wx_openid:
        new_failed_record = PointsRuleTriggerRecord(
            user_id=new_user.user_id,
            rule_id=rule.id,
            user_email=new_user.user_email,
            user_phone=new_user.user_phone,
            user_wx_id=new_user.user_wx_openid,
            result_status="失败",
            error_code="102",
            error_message="该用户无手机号或微信号，无法领取邀新奖励",
        )
        db.session.add(new_failed_record)
        db.session.commit()
        return next_console_response(error_status=True, error_message="该用户无手机号或微信号，无法领取邀新奖励")
    try:
        target_account = UserAccountInfo.query.filter(
            UserAccountInfo.user_id == invite_user.user_id,
            UserAccountInfo.account_type == "point"
        ).first()
        transaction_id = generate_transaction_id()
        new_record = PointsRuleTriggerRecord(
            rule_id=rule.id,
            transaction_id=transaction_id,
            user_id=new_user.user_id,
            user_email=new_user.user_email,
            user_phone=new_user.user_phone,
            user_wx_id=new_user.user_wx_openid,
            account_id=target_account.account_id,
            result_status="成功",
        )
        db.session.add(new_record)
        point_transaction = PointsTransactionInfo(
            account_id=target_account.account_id,
            transaction_id=transaction_id,
            transaction_type=rule.rule_type,
            transaction_amount=rule.rule_value,
            transaction_status="成功",
            transaction_desc=rule.rule_desc,
        )
        db.session.add(point_transaction)
        target_account.balance += rule.rule_value
        db.session.add(invite_user)
        db.session.commit()
    except SQLAlchemyError as e:
        app.logger.error("邀请用户送积分失败: %s" % e)
        db.session.rollback()
        return next_console_response(error_status=True, error_message="邀请用户送积分失败")
    return next_console_response(result=invite_user.to_dict())


def list_products(params):
    """
    获取商品列表
    :param params:
    :return:
    """
    page_num = params.get('page_num', 1)
    page_size = params.get('page_size', 10)
    products = ProductInfo.query.filter(
        ProductInfo.product_status == "上架"
    ).order_by(
        ProductInfo.product_code.desc()
    ).paginate(page=page_num, per_page=page_size, error_out=False)
    # 获取商品库存
    all_product_ids = [product.id for product in products]
    product_stock = ProductItemInfo.query.filter(
        ProductItemInfo.product_id.in_(all_product_ids),
        ProductItemInfo.item_status == "正常"
    ).group_by(
        ProductItemInfo.product_id
    ).with_entities(
        ProductItemInfo.product_id,
        func.count(ProductItemInfo.id).label("product_stock")
    ).all()
    product_stock_dict = {stock.product_id: stock.product_stock for stock in product_stock}
    # 获取商品销量
    product_sales = OrderItemInfo.query.filter(
        OrderItemInfo.product_id.in_(all_product_ids),
        OrderItemInfo.order_item_status.in_(["待发货", "已交付"])
    ).group_by(
        OrderItemInfo.product_id
    ).with_entities(
        OrderItemInfo.product_id,
        func.count(OrderItemInfo.id).label("product_sales")
    ).all()
    product_sales_dict = {sale.product_id: sale.product_sales for sale in product_sales}
    data = []
    for product in products:
        product_dict = product.to_dict()
        product_dict['product_stock'] = product_stock_dict.get(product.id, 0)
        product_dict['product_sales'] = product_sales_dict.get(product.id, 0)
        data.append(product_dict)
    result = {
        "total": products.total,
        "page_num": products.page,
        "page_size": products.per_page,
        "data": data
    }
    return next_console_response(result=result)


def list_user_orders(params):
    """
    获取用户订单列表
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    if not user_id:
        return next_console_response(error_status=True, error_message="用户id不能为空")
    page_num = params.get('page_num', 1)
    page_size = params.get('page_size', 10)
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    orders = OrderInfo.query.filter(
        OrderInfo.user_id == user_id
    ).order_by(
        OrderInfo.create_time.desc()
    ).paginate(page=page_num, per_page=page_size, error_out=False)
    data = [order.to_dict() for order in orders]
    if data and data[0].get("order_status") == "待支付":
        # 获取订单商品实例
        all_order_items = OrderItemInfo.query.filter(
            OrderItemInfo.order_code == data[0].get("order_code"),
            OrderItemInfo.order_item_status == "待支付"
        ).all()
        data[0]["items"] = [item.to_dict() for item in all_order_items]

    result = {
        "total": orders.total,
        "page_num": orders.page,
        "page_size": orders.per_page,
        "data": data
    }
    return next_console_response(result=result)


def init_user_order(params):
    """
    初始化用户订单
    :param params:
    :return
    """
    user_id = params.get('user_id')
    account_id = params.get('account_id')
    payment_method = params.get('payment_method')
    product_info = params.get('product_info')
    quantity = 0
    point_cost = 0
    money_cost_in_rmb = 0
    raw_quantity = 0
    order_code = generate_order_id()
    if not user_id:
        return next_console_response(error_status=True, error_message="用户id不能为空")
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    # 检查是否有未支付订单
    exist_order = OrderInfo.query.filter(
        OrderInfo.user_id == user_id,
        OrderInfo.order_status == "待支付"
    ).first()
    if exist_order:
        return next_console_response(error_status=True, error_message="您有未支付订单，请先完成支付")
    order_pre_cnt = 0
    order_item_pre_cnt = 0
    for product_item in product_info:
        if not product_item.get("point_cost"):
            return next_console_response(error_status=False, error_message="商品积分不能为空")
        order_pre_cnt += product_item.get("product_cnt") * product_item.get("point_cost")
        order_item_pre_cnt += product_item.get("product_cnt")
    # 检查是否超过活动限制,总积分不超过2000
    history_orders = OrderInfo.query.filter(
        OrderInfo.user_id == user_id,
        OrderInfo.order_status.in_(["支付完成", "交付完成"]),
    ).with_entities(
        func.sum(OrderInfo.point_cost).label("total_point_cost")
    ).first()
    if history_orders:
        total_point_cost = history_orders.total_point_cost or 0
        if total_point_cost + order_pre_cnt > 2000:
            return next_console_response(error_status=True, error_message="当前活动积分已达兑换上限，感谢您的热情参与！")
    # 检查是否超过活动限制,每日最多兑换5次
        # 当日兑换商品个数
    today_orders = OrderInfo.query.filter(
        OrderInfo.user_id == user_id,
        OrderInfo.order_status.in_(["支付完成", "交付完成"]),
        OrderInfo.create_time > datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    ).with_entities(
        func.sum(OrderInfo.quantity).label("today_item_cnt")
    ).first()
    today_item_cnt = today_orders.today_item_cnt or 0
    if today_item_cnt + order_item_pre_cnt > 5:
        return next_console_response(error_status=True, error_message="当前活动每日最多兑换5次，感谢您的热情参与！")

    # 如果不是企业用户和企业邮箱，不可下单
    enterprise_user_check = False
    if target_user.user_company_id:
        enterprise_user_check = True
    try:
        user_email_name = target_user.user_email.split('@')[1]
        enterprise_email_check = EnterpriseEmailWhiteList.query.filter(
            EnterpriseEmailWhiteList.email_name == user_email_name,
            EnterpriseEmailWhiteList.email_status == "正常"
        ).first()
        if enterprise_email_check:
            enterprise_user_check = True
    except Exception as e:
        app.logger.error(f"获取用户邮箱后缀失败: {e}")
    if not enterprise_user_check:
        return next_console_response(error_status=True, error_message="非企业用户或企业邮箱，不可下单")
    # 3-12 批次商品最多500积分
    batch_2_orders = OrderInfo.query.filter(
        OrderInfo.user_id == user_id,
        OrderInfo.order_status.in_(["支付完成", "交付完成"]),
        OrderInfo.create_time >= datetime(2025, 3, 12, 0, 0, 0)
    ).with_entities(
        func.sum(OrderInfo.point_cost).label("batch_2_point_cost")
    ).first()
    batch_2_point_cost = batch_2_orders.batch_2_point_cost or 0
    if batch_2_point_cost + order_pre_cnt > 500:
        return next_console_response(error_status=True, error_message="当前活动积分已达兑换上限，感谢您的热情参与！")

    # 锁定商品实例
    all_items = []
    for product_item in product_info:
        sub_product_id = product_item.get("product_id")
        sub_product_cnt = product_item.get("product_cnt")
        raw_quantity += sub_product_cnt
        target_product = ProductInfo.query.filter(
            ProductInfo.id == sub_product_id,
            ProductInfo.product_status == "上架"
        ).first()
        if not target_product:
            continue
        available_product_items = ProductItemInfo.query.filter(
            ProductItemInfo.product_id == sub_product_id,
            ProductItemInfo.item_status == "正常"
        ).limit(sub_product_cnt).with_for_update().all()
        for item in available_product_items:
            item.item_status = "预定"
            db.session.add(item)
        db.session.commit()
        # 生成订单实例
        for item in available_product_items:
            new_order_item = OrderItemInfo(
                product_id=sub_product_id,
                product_item_id=item.id,
                order_code=order_code,
                order_item_name=target_product.product_name,
                order_item_image=target_product.product_image,
                order_item_desc=target_product.product_desc,
                point_cost=target_product.point_cost,
                money_cost_in_rmb=target_product.money_cost_in_rmb,
                redemption_code=item.item_exchange_code,
                order_item_status="待支付"
            )
            db.session.add(new_order_item)
            quantity += 1
            point_cost += target_product.point_cost
            money_cost_in_rmb += target_product.money_cost_in_rmb
            all_items.append(new_order_item)
        db.session.commit()
    # 库存为空，直接返回
    if not quantity:
        return next_console_response(error_status=True, error_message="抱歉，选中商品的库存已空！")
    # 初始化订单
    new_order = OrderInfo(
        order_code=order_code,
        account_id=account_id,
        payment_method=payment_method,
        quantity=quantity,
        user_id=user_id,
        order_status="待支付",
        point_cost=point_cost,
        money_cost_in_rmb=money_cost_in_rmb,
        order_desc="",
    )
    db.session.add(new_order)
    db.session.commit()
    res = new_order.to_dict()
    all_items = [item.to_dict() for item in all_items]
    res["items"] = all_items
    # 库存不足提醒
    error_msg = ""
    if raw_quantity != quantity:
        error_msg = "部分商品库存不足，已为您锁定可获取的最大数量"
    # 返回结果
    return next_console_response(error_message=error_msg, result=res)


def get_user_order_detail(params):
    """
    获取订单详情
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    order_code = params.get('order_code')
    target_order = OrderInfo.query.filter(
        OrderInfo.order_code == order_code,
        OrderInfo.user_id == user_id
    ).first()
    if not target_order:
        return next_console_response(error_status=True, error_message="订单不存在")
    # 如果超时未支付，自动取消订单
    if target_order.order_status == "待支付":
        if (datetime.now() - target_order.create_time).total_seconds() > 60 * 10:
            target_order.order_status = "已失效"
            db.session.add(target_order)
            order_items = OrderItemInfo.query.filter(
                OrderItemInfo.order_code == order_code
            ).all()
            for item in order_items:
                if item.order_item_status == "待支付":
                    item.order_item_status = "已取消"
                    db.session.add(item)
            product_items = ProductItemInfo.query.filter(
                ProductItemInfo.id.in_([item.product_item_id for item in order_items])
            ).all()
            for item in product_items:
                item.item_status = "正常"
                db.session.add(item)
            db.session.commit()

    order_items = OrderItemInfo.query.filter(
        OrderItemInfo.order_code == order_code,
        OrderItemInfo.order_item_status != "已删除"
    ).all()
    result = target_order.to_dict()
    result["items"] = [item.to_dict() for item in order_items]
    return next_console_response(result=result)


def confirm_user_order(params):
    """
    确认订单
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    order_code = params.get('order_code')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    target_order = OrderInfo.query.filter(
        OrderInfo.order_code == order_code,
        OrderInfo.user_id == user_id
    ).first()
    if not target_order:
        return next_console_response(error_status=True, error_message="订单不存在")
    if target_order.order_status != "待支付":
        return next_console_response(error_status=True, error_message="订单状态不允许确认")
    if not target_order.delivery_message:
        return next_console_response(error_status=True, error_message="请先填写收货信息")
    # 扣除积分
    point_account = UserAccountInfo.query.filter(
        UserAccountInfo.user_id == user_id,
        UserAccountInfo.account_type == "point"
    ).first()
    if not point_account:
        return next_console_response(error_status=True, error_message="积分账户不存在")
    if point_account.balance < target_order.point_cost:
        return next_console_response(error_status=True, error_message="积分余额不足")
    point_account.balance -= target_order.point_cost
    db.session.add(point_account)
    # 更新订单状态
    target_order.order_status = "支付完成"
    db.session.add(target_order)
    # 更新订单商品状态
    order_items = OrderItemInfo.query.filter(
        OrderItemInfo.order_code == order_code,
        OrderItemInfo.order_item_status == "待支付"
    ).all()
    for item in order_items:
        item.order_item_status = "待发货"
        db.session.add(item)
    # 更新商品实例状态
    product_items = ProductItemInfo.query.filter(
        ProductItemInfo.id.in_([item.product_item_id for item in order_items])
    ).with_for_update().all()
    for item in product_items:
        item.item_status = "已售出"
        db.session.add(item)
    db.session.commit()
    return next_console_response(result=target_order.to_dict())


def cancel_user_order(params):
    """
    取消订单
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    order_code = params.get('order_code')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    target_order = OrderInfo.query.filter(
        OrderInfo.order_code == order_code,
        OrderInfo.user_id == user_id
    ).first()
    if not target_order:
        return next_console_response(error_status=True, error_message="订单不存在")
    if target_order.order_status != "待支付":
        return next_console_response(error_message="订单状态不允许取消")
    target_order.order_status = "已取消"
    db.session.add(target_order)
    order_items = OrderItemInfo.query.filter(
        OrderItemInfo.order_code == order_code
    ).all()
    for item in order_items:
        item.order_item_status = "已取消"
        db.session.add(item)
    product_items = ProductItemInfo.query.filter(
        ProductItemInfo.id.in_([item.product_item_id for item in order_items])
    ).with_for_update().all()
    for item in product_items:
        item.item_status = "正常"
        db.session.add(item)
    db.session.commit()
    return next_console_response(result=target_order.to_dict())


def remove_user_order_item(params):
    """
    移除订单商品
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    order_item_id = params.get('order_item_id')
    target_order_item = OrderItemInfo.query.filter(
        OrderItemInfo.id == order_item_id
    ).first()
    if not target_order_item:
        return next_console_response(error_status=True, error_message="订单商品不存在")
    if target_order_item.order_item_status != "待支付":
        return next_console_response(error_message="订单商品状态不允许移除")
    target_order = OrderInfo.query.filter(
        OrderInfo.order_code == target_order_item.order_code,
        OrderInfo.user_id == user_id
    ).first()
    if target_order.order_status != "待支付":
        return next_console_response(error_message="订单状态不允许移除商品")
    target_order_item.order_item_status = "已删除"
    db.session.add(target_order_item)
    product_item = ProductItemInfo.query.filter(
        ProductItemInfo.id == target_order_item.product_item_id
    ).with_for_update().first()
    product_item.item_status = "正常"
    target_order.quantity -= 1
    target_order.point_cost -= target_order_item.point_cost
    target_order.money_cost_in_rmb -= target_order_item.money_cost_in_rmb
    db.session.add(target_order)
    db.session.add(product_item)
    db.session.commit()
    return next_console_response(result=target_order.to_dict())


def add_user_order_item(params):
    """
    添加订单商品
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    order_code = params.get('order_code')

    target_order = OrderInfo.query.filter(
        OrderInfo.order_code == order_code,
        OrderInfo.user_id == user_id
    ).first()
    if target_order.order_status != "待支付":
        return next_console_response(error_message="订单状态不允许移除商品")
    product_info = params.get('product_info')
    if not product_info:
        return next_console_response(error_status=True, error_message="商品信息不能为空")
    quantity = 0
    point_cost = 0
    money_cost_in_rmb = 0
    raw_quantity = 0
    # 锁定商品实例
    all_items = []
    for product_item in product_info:
        sub_product_id = product_item.get("product_id")
        sub_product_cnt = product_item.get("product_cnt")
        raw_quantity += sub_product_cnt
        target_product = ProductInfo.query.filter(
            ProductInfo.id == sub_product_id,
            ProductInfo.product_status == "上架"
        ).first()
        if not target_product:
            continue
        available_product_items = ProductItemInfo.query.filter(
            ProductItemInfo.product_id == sub_product_id,
            ProductItemInfo.item_status == "正常"
        ).with_for_update().limit(sub_product_cnt).all()
        for item in available_product_items:
            item.item_status = "预定"
            db.session.add(item)
        db.session.commit()
        # 生成订单实例
        for item in available_product_items:
            new_order_item = OrderItemInfo(
                product_id=sub_product_id,
                product_item_id=item.id,
                order_code=order_code,
                order_item_name=target_product.product_name,
                order_item_image=target_product.product_image,
                order_item_desc=target_product.product_desc,
                point_cost=target_product.point_cost,
                money_cost_in_rmb=target_product.money_cost_in_rmb,
                redemption_code=item.item_exchange_code,
                order_item_status="待支付"
            )
            db.session.add(new_order_item)
            quantity += 1
            point_cost += target_product.point_cost
            money_cost_in_rmb += target_product.money_cost_in_rmb
            all_items.append(new_order_item)
        db.session.commit()
    # 库存为空，直接返回
    if not quantity:
        return next_console_response(error_status=True, error_message="抱歉，选中商品的库存已空！")
    # 更新订单
    target_order.quantity += quantity
    target_order.point_cost += point_cost
    target_order.money_cost_in_rmb += money_cost_in_rmb
    db.session.add(target_order)
    res = target_order.to_dict()
    all_items = [item.to_dict() for item in all_items]
    res["items"] = all_items
    # 库存不足提醒
    error_msg = ""
    if raw_quantity != quantity:
        error_msg = "部分商品库存不足，已为您锁定可获取的最大数量"
    # 返回结果
    return next_console_response(error_message=error_msg, result=res)


def generate_exchange_valid_code(params):
    """
    生成接受兑换码的验证码
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    user_account = params.get('user_account')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    if "@" in user_account:
        if target_user.user_email and target_user.user_email != user_account:
            return next_console_response(error_message="用户邮箱不匹配")
        if not target_user.user_email:
            # 检查邮箱是否已被使用
            exist_email = UserInfo.query.filter(
                UserInfo.user_email == user_account,
                UserInfo.user_status == 1
            ).first()
            if exist_email:
                return next_console_response(error_message="邮箱已被使用")
        from app.services.user_center.users import send_text_code_email
        return send_text_code_email({
            "user_email": user_account,
        })
    else:
        if target_user.user_phone and target_user.user_phone != user_account:
            return next_console_response(error_message="用户手机号不匹配")
        if not target_user.user_phone:
            # 检查手机号是否已被使用
            exist_phone = UserInfo.query.filter(
                UserInfo.user_phone == user_account,
                UserInfo.user_status == 1
            ).first()
            if exist_phone:
                return next_console_response(error_message="手机号已被使用")
        from app.services.user_center.users import send_text_code_aliyun
        return send_text_code_aliyun({
            "user_phone": user_account,
        })


def valid_exchange_valid_code(params):
    """
    校验接受兑换码的验证码
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    user_account = params.get('user_account')
    valid_code = params.get('user_code')
    order_id = params.get('order_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    target_order = OrderInfo.query.filter(
        OrderInfo.id == order_id,
        OrderInfo.user_id == user_id
    ).first()
    if not target_order:
        return next_console_response(error_status=True, error_message="订单不存在")
    from app.services.user_center.users import valid_text_code
    if "@" in user_account:
        res = valid_text_code({
            "user_email": user_account,
            "text_code": valid_code,
        }).json
        if res.get("error_status"):
            return res
        success_task = UserSendCodeTask.query.filter(
            UserSendCodeTask.user_email == user_account,
            UserSendCodeTask.task_code == valid_code,
            UserSendCodeTask.task_status == "已验证",
            UserSendCodeTask.update_time > datetime.now() - timedelta(minutes=5)
        ).first()
        if success_task is None:
            return next_console_response(error_status=True, error_message="验证码已失效！", error_code=1002)
        if not target_user.user_email:
            target_user.user_email = user_account
            db.session.add(target_user)
            db.session.commit()

    else:
        res = valid_text_code({
            "user_phone": user_account,
            "text_code": valid_code,
        }).json
        if res.get("error_status"):
            return res
        success_task = UserSendCodeTask.query.filter(
                UserSendCodeTask.user_phone == user_account,
                UserSendCodeTask.task_code == valid_code,
                UserSendCodeTask.task_status == "已验证",
                UserSendCodeTask.update_time > datetime.now() - timedelta(minutes=5)
            ).first()
        if success_task is None:
            return next_console_response(error_status=True, error_message="验证码已失效！", error_code=1002)
        if not target_user.user_phone:
            target_user.user_phone = user_account
            db.session.add(target_user)
            db.session.commit()

    target_order.delivery_message = user_account
    db.session.add(target_order)
    db.session.commit()
    return next_console_response(result=target_order.to_dict())


def get_market_valid_info(params):
    """
    获取是否能够继续兑换
        订单到达2000积分后无法继续兑换
        当日商品数超过20次后无法继续兑换
    :param params:
    :return:
    """
    user_id = params.get('user_id')
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在")
    point_account = UserAccountInfo.query.filter(
        UserAccountInfo.user_id == user_id,
        UserAccountInfo.account_type == "point"
    ).first()
    if not point_account:
        return next_console_response(error_status=True, error_message="积分账户不存在")
    all_paid_orders = OrderInfo.query.filter(
        OrderInfo.user_id == user_id,
        OrderInfo.order_status.in_(["支付完成", "交付完成"])
    ).with_entities(
        func.sum(OrderInfo.point_cost).label("total_point_cost")
    ).first()
    total_point_cost = all_paid_orders.total_point_cost or 0

    # 当日兑换商品个数
    today_orders = OrderInfo.query.filter(
        OrderInfo.user_id == user_id,
        OrderInfo.order_status.in_(["支付完成", "交付完成"]),
        OrderInfo.create_time > datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    ).with_entities(
        func.sum(OrderInfo.quantity).label("today_item_cnt")
    ).first()
    today_item_cnt = today_orders.today_item_cnt or 0
    can_exchange = True
    reason = ''
    if total_point_cost >= 2000:
        can_exchange = False
        reason = '当前可兑换积分已达活动上限！感谢您的热情参与！未使用的积分将保留在您的账户，可在后续活动中继续使用~'
    if today_item_cnt >= 5:
        can_exchange = False
        reason = '今日兑换商品数量已达上限，请明日再来~'
    # 是否为企业邮箱
    is_corporate_email = False
    if target_user.user_company_id:
        company = CompanyInfo.query.filter(
            CompanyInfo.id == target_user.user_company_id,
            CompanyInfo.company_status == "正常"
        ).first()
        if company and company.company_email and company.company_email in target_user.user_email:
            is_corporate_email = True
    if not is_corporate_email and target_user.user_email and "@" in target_user.user_email:
        target_user_email_name = target_user.user_email.split('@')[1]
        white_list = EnterpriseEmailWhiteList.query.filter(
            EnterpriseEmailWhiteList.email_name == target_user_email_name,
            EnterpriseEmailWhiteList.email_status == "正常"
        ).first()
        if white_list:
            is_corporate_email = True
    if not is_corporate_email:
        can_exchange = False
        reason = '非企业用户或企业邮箱，不可继续兑换奖品'
    # 计算250312后的订单积分，不能超过500
    batch_2_orders = OrderInfo.query.filter(
        OrderInfo.user_id == user_id,
        OrderInfo.order_status.in_(["支付完成", "交付完成"]),
        OrderInfo.create_time >= datetime(2025, 3, 12, 0, 0, 0)
    ).with_entities(
        func.sum(OrderInfo.point_cost).label("batch_2_point_cost")
    ).first()
    batch_2_point_cost = batch_2_orders.batch_2_point_cost or 0
    if batch_2_point_cost >= 500:
        can_exchange = False
        reason = '当前可兑换积分已达活动上限！感谢您的热情参与！未使用的积分将保留在您的账户，可在后续活动中继续使用~'
    return next_console_response(result={
        "can_exchange": can_exchange,
        "total_point_cost": int(total_point_cost),
        "today_item_cnt": int(today_item_cnt),
        "reason": reason,
        "is_corporate_email": is_corporate_email,
        "batch_2_point_cost": batch_2_point_cost
    })

