from sqlalchemy.sql import func

from app.app import db


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(256), default='')
    user_nick_name = db.Column(db.String(256), default='')
    user_nick_name_py = db.Column(db.String(6), default='')
    user_code = db.Column(db.String(256), default='')
    user_source = db.Column(db.String(256), default='')
    user_password = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255))
    user_phone = db.Column(db.String(20), default='')
    user_gender = db.Column(db.String(5), default='男')
    user_age = db.Column(db.Integer, default=18)
    user_company = db.Column(db.String(255), default='')
    user_account_type = db.Column(db.String(255), default='个人账号')
    user_department = db.Column(db.String(255), default='')
    user_resource_limit = db.Column(db.Float, default=20480)
    user_position = db.Column(db.String(255), default='')
    user_status = db.Column(db.Integer, nullable=False)
    user_avatar = db.Column(db.Text, default='')
    user_wx_nickname = db.Column(db.String(255), default='')
    user_wx_avatar = db.Column(db.Text, default='')
    user_wx_openid = db.Column(db.String(255), default='')
    user_wx_union_id = db.Column(db.String(255), default='')
    user_accept_contact = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())
    last_login_time = db.Column(db.DateTime, default=func.now())
    user_expire_time = db.Column(db.DateTime)
    user_area = db.Column(db.Integer)
    user_resource_base_path = db.Column(db.String, default='')
    user_company_id = db.Column(db.Integer)
    user_department_id = db.Column(db.Integer)
    user_invite_code = db.Column(db.String(100), default='')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_nick_name': self.user_nick_name,
            'user_nick_name_py': self.user_nick_name_py,
            'user_code': self.user_code,
            'user_source': self.user_source,
            'user_email': self.user_email,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login_time': self.last_login_time.strftime('%Y-%m-%d %H:%M:%S')
            if self.last_login_time else "2999-01-01 00:00:00",
            'user_expire_time': self.user_expire_time.strftime('%Y-%m-%d %H:%M:%S')
            if self.user_expire_time else "2999-01-01 00:00:00",
            'user_phone': self.user_phone,
            'user_gender': self.user_gender,
            'user_age': self.user_age,
            'user_avatar': self.user_avatar,
            'user_company': self.user_company,
            'user_account_type': self.user_account_type,
            'user_department': self.user_department,
            'user_position': self.user_position,
            'user_wx_nickname': self.user_wx_nickname,
            'user_wx_avatar': self.user_wx_avatar,
            'user_wx_openid': self.user_wx_openid,
            'user_wx_union_id': self.user_wx_union_id,
            'user_status': self.user_status,
            'user_area': self.user_area,
            'user_resource_limit': self.user_resource_limit,
            "user_invite_code": self.user_invite_code,
            "user_company_id": self.user_company_id,
            "user_department_id": self.user_department_id,
        }

    def get_id(self):
        return str(self.user_id)

    def show_info(self):
        """
        对外展示信息
        :return:
        """
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_nick_name': self.user_nick_name,
            'user_nick_name_py': self.user_nick_name_py,
            'user_avatar': self.user_avatar,
            'user_company': self.user_company,
            'user_email': self.user_email,
            'user_position': self.user_position,
            'user_gender': self.user_gender,
            'user_account_type': self.user_account_type,
        }


class UserSendCodeTask(db.Model):
    __tablename__ = 'user_send_code_task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    user_email = db.Column(db.String(255), default='')
    user_phone = db.Column(db.String(100), default='')
    new_email = db.Column(db.String(100), default='')
    new_password = db.Column(db.String(255), default='')
    new_phone = db.Column(db.String(100), default='')
    task_code = db.Column(db.String(255), nullable=False)
    task_status = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())
    update_time = db.Column(db.DateTime(timezone=True), default=func.now())

    def to_dict(self):
        return {'id': self.id,
                "user_id": self.user_id,
                'user_email': self.user_email,
                'user_phone': self.user_phone,
                'new_email': self.new_email,
                'new_password': self.new_password,
                'new_phone': self.new_phone,
                'task_code': self.task_code,
                'task_status': self.task_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                }


class UserFriendsRelation(db.Model):
    """
    用户好友关系表
    CREATE TABLE IF NOT EXISTS `user_friends_relation` (
     `id` int NOT NULL AUTO_INCREMENT COMMENT '记录id',
     `user_id` INTEGER NOT NULL COMMENT '用户id',
     `friend_id` INTEGER NOT NULL COMMENT '好友id',
     `rel_status` INTEGER NOT NULL COMMENT '关系状态',
     `create_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
     `update_time` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
     PRIMARY KEY (`id`)
    ) ENGINE=InnoDB COMMENT '用户好友关系表';
    """
    __tablename__ = 'user_friends_relation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    friend_id = db.Column(db.Integer, nullable=False)
    rel_status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'friend_id': self.friend_id,
                'rel_status': self.rel_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }


class SubscriptionInfo(db.Model):
    """
    '订阅信息表';
    """
    __tablename__ = 'subscription_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    subscribe_status = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'email': self.email,
                'subscribe_status': self.subscribe_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }


class UserInviteCodeViewRecord(db.Model):
    """
    """
    __tablename__ = 'user_invite_code_view_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    invite_code = db.Column(db.String(255), nullable=False)
    invite_type = db.Column(db.String(255), nullable=False)
    marketing_code = db.Column(db.String(255), default='', nullable=False)
    view_user_id = db.Column(db.Integer)
    view_client_id = db.Column(db.String(255), nullable=False)
    invite_status = db.Column(db.String(255), nullable=False, default='正常')
    begin_add_friend = db.Column(db.Boolean, default=False)
    finish_add_friend = db.Column(db.Boolean, default=False)
    begin_register = db.Column(db.Boolean, default=False)
    finish_register = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'invite_code': self.invite_code,
                'invite_type': self.invite_type,
                'marketing_code': self.marketing_code,
                'view_user_id': self.view_user_id,
                'view_client_id': self.view_client_id,
                'invite_status': self.invite_status,
                'begin_add_friend': self.begin_add_friend,
                'finish_add_friend': self.finish_add_friend,
                'begin_register': self.begin_register,
                'finish_register': self.finish_register,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }


class UserAccountInfo(db.Model):
    """
    '用户账户表';
    """
    __tablename__ = 'user_account_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=0, nullable=False)
    frozen_balance = db.Column(db.Integer, default=0, nullable=False)
    account_status = db.Column(db.String(255), default='正常', nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'account_id': self.account_id,
                'account_type': self.account_type,
                'balance': round(self.balance, 2),
                'frozen_balance': self.frozen_balance,
                'account_status': self.account_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }


class PointsTransactionInfo(db.Model):
    """
     '积分流水表';
    """
    __tablename__ = 'points_transaction_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.String(255), nullable=False)
    account_id = db.Column(db.String(255), nullable=False)
    transaction_amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(255), nullable=False)
    transaction_status = db.Column(db.String(255), nullable=False)
    order_id = db.Column(db.String(255), default="", nullable=False)
    role_id = db.Column(db.Integer, default=0, nullable=False)
    transaction_desc = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'transaction_id': self.transaction_id,
                'account_id': self.account_id,
                'transaction_amount': round(self.transaction_amount, 2),
                'transaction_type': self.transaction_type,
                'transaction_status': self.transaction_status,
                'order_id': self.order_id,
                'transaction_desc': self.transaction_desc,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }


class PointsRule(db.Model):
    """
    """
    __tablename__ = 'points_rule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule_code = db.Column(db.String(255), nullable=False)
    rule_name = db.Column(db.String(255), nullable=False)
    rule_type = db.Column(db.String(255), nullable=False)
    rule_desc = db.Column(db.String(255), nullable=False)
    rule_value = db.Column(db.Float, nullable=False)
    rule_status = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'rule_code': self.rule_code,
            'rule_name': self.rule_name,
            'rule_type': self.rule_type,
            'rule_desc': self.rule_desc,
            'rule_value': round(self.rule_value, 2),
            'rule_status': self.rule_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }


class PointsRuleTriggerRecord(db.Model):
    """
    """
    __tablename__ = 'points_rule_trigger_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(255), default="", nullable=False)
    user_phone = db.Column(db.String(255), default="", nullable=False)
    user_wx_id = db.Column(db.String(255), default="", nullable=False)
    account_id = db.Column(db.String(255), default="", nullable=False)
    rule_id = db.Column(db.Integer, nullable=False)
    transaction_id = db.Column(db.String(255), default="", nullable=False)
    result_status = db.Column(db.String(255), default="", nullable=False)
    error_code = db.Column(db.String(255), default="", nullable=False)
    error_message = db.Column(db.String(255), default="", nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'user_email': self.user_email,
                'user_phone': self.user_phone,
                'user_wx_id': self.user_wx_id,
                'account_id': self.account_id,
                'rule_id': self.rule_id,
                'transaction_id': self.transaction_id,
                'result_status': self.result_status,
                'error_code': self.error_code,
                'error_message': self.error_message,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }


class ProductInfo(db.Model):
    """
  '商品信息表';
    """
    __tablename__ = 'product_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_code = db.Column(db.String(255), nullable=False)
    category_name = db.Column(db.String(255), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    product_desc = db.Column(db.String(255), nullable=False)
    product_image = db.Column(db.Text, default='')
    accept_payment_methods = db.Column(db.Integer, nullable=False)
    point_cost = db.Column(db.Float, nullable=False)
    money_cost_in_rmb = db.Column(db.Float, nullable=False)
    product_status = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'product_code': self.product_code,
                'category_name': self.category_name,
                'product_name': self.product_name,
                'product_desc': self.product_desc,
                'product_image': self.product_image,
                'accept_payment_methods': self.accept_payment_methods,
                'point_cost': round(self.point_cost, 2),
                'money_cost_in_rmb': round(self.money_cost_in_rmb, 2),
                'product_status': self.product_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }

    def show_info(self):
        """
        对外展示信息
        :return:
        """
        return {
            'product_code': self.product_code,
            'category_name': self.category_name,
            'product_name': self.product_name,
            'product_desc': self.product_desc,
            'product_image': self.product_image,
            'accept_payment_methods': self.accept_payment_methods,
            'points_cost': round(self.points_cost, 2),
            'money_cost_in_rmb': round(self.money_cost_in_rmb, 2),
            'product_stock': self.product_stock,
            'product_status': self.product_status,
        }


class ProductItemInfo(db.Model):
    """
    '商品实例信息';
    """
    __tablename__ = 'product_item_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, nullable=False)
    item_code = db.Column(db.String(255), default='')
    item_exchange_code = db.Column(db.String(255), default='')
    item_status = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'product_id': self.product_id,
                'item_code': self.item_code,
                'item_exchange_code': self.item_exchange_code,
                'item_status': self.item_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }


class OrderInfo(db.Model):
    """
    '订单信息表';

    """
    __tablename__ = 'order_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_code = db.Column(db.String(255), nullable=False)
    order_type = db.Column(db.String(255), default="", nullable=False)
    order_desc = db.Column(db.String(255), default="", nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    point_cost = db.Column(db.Float, nullable=False)
    money_cost_in_rmb = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(255), nullable=False)
    delivery_message = db.Column(db.String(255), default="", nullable=False)
    delivery_status = db.Column(db.String(255), default="", nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'order_code': self.order_code,
                'order_type': self.order_type,
                'order_desc': self.order_desc,
                'quantity': self.quantity,
                'user_id': self.user_id,
                'account_id': self.account_id,
                'payment_method': self.payment_method,
                'point_cost': round(self.point_cost, 2),
                'money_cost_in_rmb': round(self.money_cost_in_rmb, 2),
                'order_status': self.order_status,
                'delivery_message': self.delivery_message,
                'delivery_status': self.delivery_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }


class OrderItemInfo(db.Model):
    """
    '订单商品信息';
    """
    __tablename__ = 'order_item_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_item_name = db.Column(db.String(255), default="", nullable=False)
    order_item_image = db.Column(db.String, default="", nullable=False)
    order_item_desc = db.Column(db.String(255), default="", nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_item_id = db.Column(db.Integer, nullable=False)
    order_code = db.Column(db.String, nullable=False)
    point_cost = db.Column(db.Float, nullable=False)
    money_cost_in_rmb = db.Column(db.Float, nullable=False)
    redemption_code = db.Column(db.String(255), default="", nullable=False)
    order_item_status = db.Column(db.String(255), default="", nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'order_item_name': self.order_item_name,
                'order_item_image': self.order_item_image,
                'order_item_desc': self.order_item_desc,
                'product_id': self.product_id,
                'product_item_id': self.product_item_id,
                'order_code': self.order_code,
                'point_cost': round(self.point_cost, 2),
                'money_cost_in_rmb': round(self.money_cost_in_rmb, 2),
                'redemption_code': self.redemption_code,
                'order_item_status': self.order_item_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }

