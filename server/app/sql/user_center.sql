CREATE OR REPLACE FUNCTION update_update_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_time = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


------------------------------------------------------------
CREATE TABLE "next_console"."user_info"
(
 "user_id" SERIAL PRIMARY KEY,
 "user_name" varchar(256) NOT NULL ,
 "user_nick_name" varchar(256) ,
 "user_nick_name_py" varchar(6) ,
 "user_password" varchar(255) NOT NULL ,
 "user_email" varchar(255) ,
 "user_phone" varchar(20) ,
 "user_gender" varchar(5) ,
 "user_age" integer ,
 "user_avatar" text ,
 "user_department" varchar(255) ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "last_login_time" timestamp with time zone ,
 "user_status" integer NOT NULL ,
 "user_source" varchar(256) ,
 "user_code" varchar(256) ,
 "user_wx_nickname" varchar(255) ,
 "user_wx_avatar" text ,
 "user_wx_openid" varchar(255) ,
 "user_wx_union_id" varchar(255) ,
 "user_position" varchar(255) ,
 "user_company" varchar(255) ,
 "user_account_type" varchar(255) ,
 "user_name_py" varchar(6) ,
 "user_expire_time" timestamp with time zone ,
 "user_area" integer ,
 "user_resource_base_path" text ,
 "user_company_id" integer ,
 "user_department_id" integer ,
 "user_resource_limit" double precision ,
 "user_accept_contact" boolean ,
 "user_invite_code" varchar(100)
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."user_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."user_info"."user_name" IS '用户名称';
COMMENT ON COLUMN "next_console"."user_info"."user_nick_name" IS '用户昵称';
COMMENT ON COLUMN "next_console"."user_info"."user_nick_name_py" IS '用户名称拼音';
COMMENT ON COLUMN "next_console"."user_info"."user_password" IS '用户密码';
COMMENT ON COLUMN "next_console"."user_info"."user_email" IS '用户邮箱';
COMMENT ON COLUMN "next_console"."user_info"."user_phone" IS '用户手机';
COMMENT ON COLUMN "next_console"."user_info"."user_gender" IS '用户性别';
COMMENT ON COLUMN "next_console"."user_info"."user_age" IS '用户年龄';
COMMENT ON COLUMN "next_console"."user_info"."user_avatar" IS '用户头像';
COMMENT ON COLUMN "next_console"."user_info"."user_department" IS '用户部门';
COMMENT ON COLUMN "next_console"."user_info"."create_time" IS '用户创建时间';
COMMENT ON COLUMN "next_console"."user_info"."update_time" IS '用户更新时间';
COMMENT ON COLUMN "next_console"."user_info"."last_login_time" IS '用户上次登录时间';
COMMENT ON COLUMN "next_console"."user_info"."user_status" IS '用户状态';
COMMENT ON COLUMN "next_console"."user_info"."user_source" IS '用户来源';
COMMENT ON COLUMN "next_console"."user_info"."user_code" IS '用户编号';
COMMENT ON COLUMN "next_console"."user_info"."user_wx_nickname" IS '用户微信昵称';
COMMENT ON COLUMN "next_console"."user_info"."user_wx_avatar" IS '用户微信头像';
COMMENT ON COLUMN "next_console"."user_info"."user_wx_openid" IS '用户微信id';
COMMENT ON COLUMN "next_console"."user_info"."user_wx_union_id" IS '用户微信全局id';
COMMENT ON COLUMN "next_console"."user_info"."user_position" IS '用户职位';
COMMENT ON COLUMN "next_console"."user_info"."user_company" IS '用户公司';
COMMENT ON COLUMN "next_console"."user_info"."user_account_type" IS '用户账号类型';
COMMENT ON COLUMN "next_console"."user_info"."user_name_py" IS '用户名称拼音';
COMMENT ON COLUMN "next_console"."user_info"."user_expire_time" IS '用户过期时间';
COMMENT ON COLUMN "next_console"."user_info"."user_area" IS '用户区域';
COMMENT ON COLUMN "next_console"."user_info"."user_resource_base_path" IS '用户资源基础路径';
COMMENT ON COLUMN "next_console"."user_info"."user_company_id" IS '用户公司id';
COMMENT ON COLUMN "next_console"."user_info"."user_department_id" IS '用户部门id';
COMMENT ON COLUMN "next_console"."user_info"."user_resource_limit" IS '用户资源空间上限，以mb为单位';
COMMENT ON COLUMN "next_console"."user_info"."user_accept_contact" IS '是否接受联系';
COMMENT ON COLUMN "next_console"."user_info"."user_invite_code" IS '用户邀请码';
COMMENT ON TABLE "next_console"."user_info" IS '用户信息表';

CREATE TRIGGER update_user_info_trigger BEFORE UPDATE ON "next_console"."user_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."user_send_code_task"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer ,
 "user_email" varchar(255) ,
 "user_phone" varchar(100) ,
 "new_email" varchar(100) ,
 "new_password" varchar(255) ,
 "new_phone" varchar(100) ,
 "task_code" varchar(255) NOT NULL ,
 "task_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."user_send_code_task"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."user_send_code_task"."user_email" IS '目标邮箱';
COMMENT ON COLUMN "next_console"."user_send_code_task"."user_phone" IS '目标手机';
COMMENT ON COLUMN "next_console"."user_send_code_task"."new_email" IS '新邮箱';
COMMENT ON COLUMN "next_console"."user_send_code_task"."new_password" IS '新密码（加密后）';
COMMENT ON COLUMN "next_console"."user_send_code_task"."new_phone" IS '新手机';
COMMENT ON COLUMN "next_console"."user_send_code_task"."task_code" IS '发送验证码';
COMMENT ON COLUMN "next_console"."user_send_code_task"."task_status" IS '任务状态';
COMMENT ON COLUMN "next_console"."user_send_code_task"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."user_send_code_task"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."user_send_code_task"."user_id" IS '用户id';
COMMENT ON TABLE "next_console"."user_send_code_task" IS '用户验证码任务记录';

CREATE INDEX "user_send_code_task_task_code_FK84"
ON "next_console"."user_send_code_task" USING btree ( "task_code" )
;

CREATE TRIGGER update_user_send_code_task_trigger BEFORE UPDATE ON "next_console"."user_send_code_task" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."user_friends_relation"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "friend_id" integer NOT NULL ,
 "rel_status" integer NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."user_friends_relation"."id" IS '记录id';
COMMENT ON COLUMN "next_console"."user_friends_relation"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."user_friends_relation"."friend_id" IS '好友id';
COMMENT ON COLUMN "next_console"."user_friends_relation"."rel_status" IS '关系状态';
COMMENT ON COLUMN "next_console"."user_friends_relation"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."user_friends_relation"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."user_friends_relation" IS '用户好友关系表';

CREATE INDEX "friend_id77"
ON "next_console"."user_friends_relation" USING btree ( "friend_id" )
;
CREATE INDEX "user_id78"
ON "next_console"."user_friends_relation" USING btree ( "user_id" )
;

CREATE TRIGGER update_user_friends_relation_trigger BEFORE UPDATE ON "next_console"."user_friends_relation" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------

CREATE TABLE "next_console"."subscription_info"
(
 "id" SERIAL PRIMARY KEY,
 "email" varchar(255) NOT NULL ,
 "subscribe_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."subscription_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."subscription_info"."email" IS '订阅邮箱';
COMMENT ON COLUMN "next_console"."subscription_info"."subscribe_status" IS '订阅状态';
COMMENT ON COLUMN "next_console"."subscription_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."subscription_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."subscription_info" IS '订阅信息表';
CREATE TRIGGER update_subscription_info_trigger BEFORE UPDATE ON "next_console"."subscription_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------
CREATE TABLE "next_console"."user_invite_code_view_record"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "invite_code" varchar(255) NOT NULL ,
 "invite_type" varchar(255) NOT NULL ,
 "marketing_code" varchar(255) NOT NULL ,
 "view_user_id" integer ,
 "view_client_id" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "invite_status" varchar(100) ,
 "begin_register" boolean ,
 "finish_register" boolean ,
 "begin_add_friend" boolean ,
 "finish_add_friend" boolean
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."invite_code" IS '邀请码';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."invite_type" IS '邀请类型';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."marketing_code" IS '营销码';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."view_user_id" IS '浏览用户id';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."view_client_id" IS '浏览客户端id';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."invite_status" IS '邀请码状态';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."begin_register" IS '开始注册';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."finish_register" IS '完成注册';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."begin_add_friend" IS '开始加好友';
COMMENT ON COLUMN "next_console"."user_invite_code_view_record"."finish_add_friend" IS '完成加好友';
COMMENT ON TABLE "next_console"."user_invite_code_view_record" IS '用户邀请链接浏览记录表';

CREATE INDEX "user_id80"
ON "next_console"."user_invite_code_view_record" USING btree ( "user_id" )
;
CREATE TRIGGER update_user_invite_code_view_record_trigger BEFORE UPDATE ON "next_console"."user_invite_code_view_record" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------
CREATE TABLE "next_console"."user_account_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "account_id" varchar(255) NOT NULL ,
 "account_type" varchar(255) NOT NULL ,
 "balance" double precision NOT NULL ,
 "frozen_balance" integer NOT NULL ,
 "account_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."user_account_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."user_account_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."user_account_info"."account_id" IS '账号id';
COMMENT ON COLUMN "next_console"."user_account_info"."account_type" IS '账号类型';
COMMENT ON COLUMN "next_console"."user_account_info"."balance" IS '账号余额';
COMMENT ON COLUMN "next_console"."user_account_info"."frozen_balance" IS '冻结余额';
COMMENT ON COLUMN "next_console"."user_account_info"."account_status" IS '账号状态';
COMMENT ON COLUMN "next_console"."user_account_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."user_account_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."user_account_info" IS '用户账户表';

CREATE INDEX "user_id74"
ON "next_console"."user_account_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_user_account_info_trigger BEFORE UPDATE ON "next_console"."user_account_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------

CREATE TABLE "next_console"."points_transaction_info"
(
 "id" SERIAL PRIMARY KEY,
 "transaction_id" varchar(255) NOT NULL ,
 "account_id" varchar(255) NOT NULL ,
 "transaction_amount" double precision NOT NULL ,
 "transaction_type" varchar(255) NOT NULL ,
 "transaction_status" varchar(255) NOT NULL ,
 "order_id" varchar(255) NOT NULL ,
 "transaction_desc" text NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "role_id" integer
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."points_transaction_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."points_transaction_info"."transaction_id" IS '交易流水号';
COMMENT ON COLUMN "next_console"."points_transaction_info"."account_id" IS '账号id';
COMMENT ON COLUMN "next_console"."points_transaction_info"."transaction_amount" IS '交易积分';
COMMENT ON COLUMN "next_console"."points_transaction_info"."transaction_type" IS '交易类型';
COMMENT ON COLUMN "next_console"."points_transaction_info"."transaction_status" IS '交易状态';
COMMENT ON COLUMN "next_console"."points_transaction_info"."order_id" IS '订单号';
COMMENT ON COLUMN "next_console"."points_transaction_info"."transaction_desc" IS '交易说明';
COMMENT ON COLUMN "next_console"."points_transaction_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."points_transaction_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."points_transaction_info"."role_id" IS '关联规则id';
COMMENT ON TABLE "next_console"."points_transaction_info" IS '积分流水表';
CREATE TRIGGER update_points_transaction_info_trigger BEFORE UPDATE ON "next_console"."points_transaction_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------

CREATE TABLE "next_console"."points_rule"
(
 "id" SERIAL PRIMARY KEY,
 "rule_code" varchar(255) NOT NULL ,
 "rule_name" varchar(255) NOT NULL ,
 "rule_type" varchar(255) NOT NULL ,
 "rule_desc" varchar(255) NOT NULL ,
 "rule_value" integer NOT NULL ,
 "rule_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."points_rule"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."points_rule"."rule_code" IS '规则编号';
COMMENT ON COLUMN "next_console"."points_rule"."rule_name" IS '规则名称';
COMMENT ON COLUMN "next_console"."points_rule"."rule_type" IS '规则类型';
COMMENT ON COLUMN "next_console"."points_rule"."rule_desc" IS '规则描述';
COMMENT ON COLUMN "next_console"."points_rule"."rule_value" IS '规则值';
COMMENT ON COLUMN "next_console"."points_rule"."rule_status" IS '规则状态';
COMMENT ON COLUMN "next_console"."points_rule"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."points_rule"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."points_rule" IS '积分规则表';
CREATE TRIGGER update_points_rule_trigger BEFORE UPDATE ON "next_console"."points_rule" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------

CREATE TABLE "next_console"."points_rule_trigger_record" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_phone VARCHAR(255) NOT NULL,
    user_wx_id VARCHAR(255) NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    rule_id VARCHAR(255) NOT NULL,
    transaction_id VARCHAR(255) NOT NULL,
    result_status VARCHAR(255) NOT NULL,
    error_code VARCHAR(255) NOT NULL,
    error_message VARCHAR(255) NOT NULL,
    create_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
-- 为表添加注释
COMMENT ON TABLE "next_console"."points_rule_trigger_record" IS '积分规则触发记录';
-- 为各列添加注释
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".id IS '自增id';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".user_id IS '用户id';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".user_email IS '用户邮箱';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".user_phone IS '用户手机';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".user_wx_id IS '用户微信id';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".account_id IS '用户账户id';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".rule_id IS '规则id';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".transaction_id IS '交易流水号';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".result_status IS '触发结果';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".error_code IS '错误代码';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".error_message IS '错误原因';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."points_rule_trigger_record".update_time IS '更新时间';
CREATE TRIGGER update_points_rule_trigger_record_trigger BEFORE UPDATE ON "next_console"."points_rule_trigger_record" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."product_info"
(
 "id" SERIAL PRIMARY KEY,
 "product_code" varchar(255) NOT NULL ,
 "category_name" varchar(255) NOT NULL ,
 "product_name" varchar(255) NOT NULL ,
 "product_desc" varchar(255) NOT NULL ,
 "accept_payment_methods" integer NOT NULL ,
 "point_cost" double precision NOT NULL ,
 "money_cost_in_rmb" double precision NOT NULL ,
 "product_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "product_image" text
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."product_info"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."product_info"."product_code" IS '商品编码';
COMMENT ON COLUMN "next_console"."product_info"."category_name" IS '商品种类';
COMMENT ON COLUMN "next_console"."product_info"."product_name" IS '商品名称';
COMMENT ON COLUMN "next_console"."product_info"."product_desc" IS '商品描述';
COMMENT ON COLUMN "next_console"."product_info"."accept_payment_methods" IS '1=纯积分 2=现金 3=积分+现金';
COMMENT ON COLUMN "next_console"."product_info"."point_cost" IS '所需积分';
COMMENT ON COLUMN "next_console"."product_info"."money_cost_in_rmb" IS '所需人民币';
COMMENT ON COLUMN "next_console"."product_info"."product_status" IS '（0下架/1上架/2预售）';
COMMENT ON COLUMN "next_console"."product_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."product_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."product_info"."product_image" IS '产品图片';
COMMENT ON TABLE "next_console"."product_info" IS '商品信息表';
CREATE TRIGGER update_product_info_trigger BEFORE UPDATE ON "next_console"."product_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."product_item_info"
(
 "id" SERIAL PRIMARY KEY,
 "product_id" integer NOT NULL ,
 "item_code" varchar(255) ,
 "item_exchange_code" varchar(255) ,
 "item_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."product_item_info"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."product_item_info"."product_id" IS '商品id';
COMMENT ON COLUMN "next_console"."product_item_info"."item_code" IS '实例编码';
COMMENT ON COLUMN "next_console"."product_item_info"."item_exchange_code" IS '礼品卡类商品的兑换码';
COMMENT ON COLUMN "next_console"."product_item_info"."item_status" IS '实例状态：正常，已售，冻结，预定';
COMMENT ON COLUMN "next_console"."product_item_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."product_item_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."product_item_info" IS '商品实例信息';

CREATE TRIGGER update_product_item_info_trigger BEFORE UPDATE ON "next_console"."product_item_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."order_info"
(
 "id" SERIAL PRIMARY KEY,
 "order_code" varchar(255) NOT NULL ,
 "order_type" varchar(255) NOT NULL ,
 "order_desc" varchar(255) NOT NULL ,
 "quantity" integer NOT NULL ,
 "user_id" integer NOT NULL ,
 "account_id" integer NOT NULL ,
 "payment_method" varchar(255) NOT NULL ,
 "point_cost" double precision NOT NULL ,
 "money_cost_in_rmb" double precision NOT NULL ,
 "order_status" varchar(255) NOT NULL ,
 "delivery_message" varchar(255) NOT NULL ,
 "delivery_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."order_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."order_info"."order_code" IS '订单id订单编号';
COMMENT ON COLUMN "next_console"."order_info"."order_type" IS '订单类型';
COMMENT ON COLUMN "next_console"."order_info"."order_desc" IS '订单描述';
COMMENT ON COLUMN "next_console"."order_info"."quantity" IS '商品数量';
COMMENT ON COLUMN "next_console"."order_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."order_info"."account_id" IS '支付账户id';
COMMENT ON COLUMN "next_console"."order_info"."payment_method" IS '1:积分，2：钱，3积分加钱';
COMMENT ON COLUMN "next_console"."order_info"."point_cost" IS '支付积分';
COMMENT ON COLUMN "next_console"."order_info"."money_cost_in_rmb" IS '支付金额';
COMMENT ON COLUMN "next_console"."order_info"."order_status" IS '待支付，支付完成，支付失败，取消，交付完成';
COMMENT ON COLUMN "next_console"."order_info"."delivery_message" IS '运输信息';
COMMENT ON COLUMN "next_console"."order_info"."delivery_status" IS '运输状态';
COMMENT ON COLUMN "next_console"."order_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."order_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."order_info" IS '订单信息表';

CREATE TRIGGER update_order_info_trigger BEFORE UPDATE ON "next_console"."order_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------
CREATE TABLE "next_console"."order_item_info" (
    id SERIAL PRIMARY KEY,
    order_item_desc VARCHAR(255) NOT NULL,
    product_id INTEGER NOT NULL,
    product_item_id INTEGER NOT NULL,
    order_code VARCHAR(255) NOT NULL,
    point_cost REAL NOT NULL,
    money_cost_in_rmb REAL NOT NULL,
    redemption_code VARCHAR(255) NOT NULL,
    order_item_status VARCHAR(255) NOT NULL,
    create_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    order_item_name VARCHAR(100),
    order_item_image TEXT
);
COMMENT ON TABLE "next_console"."order_item_info" IS '订单商品信息';
COMMENT ON COLUMN "next_console"."order_item_info".id IS 'ID 编号';
COMMENT ON COLUMN "next_console"."order_item_info".order_item_desc IS '订单商品描述';
COMMENT ON COLUMN "next_console"."order_item_info".product_id IS '产品 id';
COMMENT ON COLUMN "next_console"."order_item_info".product_item_id IS '商品实例 id';
COMMENT ON COLUMN "next_console"."order_item_info".order_code IS '订单 id';
COMMENT ON COLUMN "next_console"."order_item_info".point_cost IS '积分价格';
COMMENT ON COLUMN "next_console"."order_item_info".money_cost_in_rmb IS '人民币价格';
COMMENT ON COLUMN "next_console"."order_item_info".redemption_code IS '兑换码';
COMMENT ON COLUMN "next_console"."order_item_info".order_item_status IS '待交付，已交付，交付异常';
COMMENT ON COLUMN "next_console"."order_item_info".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."order_item_info".update_time IS '更新时间';
COMMENT ON COLUMN "next_console"."order_item_info".order_item_name IS '订单商品名称';
COMMENT ON COLUMN "next_console"."order_item_info".order_item_image IS '商品图片';
CREATE TRIGGER update_order_item_info_trigger BEFORE UPDATE ON "next_console"."order_item_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."role_info" (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(64) NOT NULL,  -- 优化长度
    role_desc TEXT,                  -- 更适合长描述
    create_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP ,
    status SMALLINT NOT NULL,        -- 优化数据类型
    CONSTRAINT uq_role_name UNIQUE (role_name)
);
COMMENT ON COLUMN "next_console"."role_info"."role_name" IS '角色名称';
COMMENT ON COLUMN "next_console"."role_info"."role_desc" IS '角色描述';
COMMENT ON COLUMN "next_console"."role_info"."create_time" IS '角色创建时间';
COMMENT ON COLUMN "next_console"."role_info"."update_time" IS '角色更新时间';
COMMENT ON COLUMN "next_console"."role_info"."status" IS '角色状态';
COMMENT ON TABLE "next_console"."role_info" IS '角色信息表';

CREATE TRIGGER update_role_info_trigger BEFORE UPDATE ON "next_console"."role_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."user_role_info"
(
 "rel_id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "role_id" integer NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "rel_status" integer NOT NULL )
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."user_role_info"."rel_id" IS '关系id';
COMMENT ON COLUMN "next_console"."user_role_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."user_role_info"."role_id" IS '角色id';
COMMENT ON COLUMN "next_console"."user_role_info"."create_time" IS '关系创建时间';
COMMENT ON COLUMN "next_console"."user_role_info"."update_time" IS '关系更新时间';
COMMENT ON COLUMN "next_console"."user_role_info"."rel_status" IS '关系状态';
COMMENT ON TABLE "next_console"."user_role_info" IS '用户角色表';

CREATE INDEX "role_id81"
ON "next_console"."user_role_info" USING btree ( "role_id" )
;
CREATE INDEX "user_id82"
ON "next_console"."user_role_info" USING btree ( "user_id" )
;
CREATE UNIQUE INDEX "user_role_info_UN183"
ON "next_console"."user_role_info" USING btree ( "user_id" ,"role_id" )
;
CREATE TRIGGER update_user_role_info_trigger BEFORE UPDATE ON "next_console"."user_role_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."permission_info"
(
 "permission_id" SERIAL PRIMARY KEY,
 "permission_name" varchar(255) NOT NULL ,
 "permission_desc" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "permission_status" integer NOT NULL ,
 "permission_url" varchar(256) NOT NULL ,
 "permission_condition" varchar(256)
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."permission_info"."permission_id" IS '权限id';
COMMENT ON COLUMN "next_console"."permission_info"."permission_name" IS '权限名称';
COMMENT ON COLUMN "next_console"."permission_info"."permission_desc" IS '权限描述';
COMMENT ON COLUMN "next_console"."permission_info"."create_time" IS '权限创建时间';
COMMENT ON COLUMN "next_console"."permission_info"."update_time" IS '权限更新时间';
COMMENT ON COLUMN "next_console"."permission_info"."permission_status" IS '权限状态';
COMMENT ON COLUMN "next_console"."permission_info"."permission_url" IS '权限对象';
COMMENT ON COLUMN "next_console"."permission_info"."permission_condition" IS '权限条件';
COMMENT ON TABLE "next_console"."permission_info" IS '权限信息表';

CREATE TRIGGER update_permission_info_trigger BEFORE UPDATE ON "next_console"."permission_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."role_permission_info"
(
 "rel_id" SERIAL PRIMARY KEY,
 "role_id" integer NOT NULL ,
 "permission_id" integer NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "rel_status" integer NOT NULL
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."role_permission_info"."rel_id" IS '关系id';
COMMENT ON COLUMN "next_console"."role_permission_info"."role_id" IS '角色id';
COMMENT ON COLUMN "next_console"."role_permission_info"."permission_id" IS '权限id';
COMMENT ON COLUMN "next_console"."role_permission_info"."create_time" IS '关系创建时间';
COMMENT ON COLUMN "next_console"."role_permission_info"."update_time" IS '关系更新时间';
COMMENT ON COLUMN "next_console"."role_permission_info"."rel_status" IS '关系状态';
COMMENT ON TABLE "next_console"."role_permission_info" IS '角色权限表';

CREATE INDEX "permission_id45"
ON "next_console"."role_permission_info" USING btree ( "permission_id" )
;
CREATE INDEX "role_id43"
ON "next_console"."role_permission_info" USING btree ( "role_id" )
;
CREATE UNIQUE INDEX "role_permission_info_UN44"
ON "next_console"."role_permission_info" USING btree ( "role_id" ,"permission_id" )
;
CREATE TRIGGER update_role_permission_info_trigger BEFORE UPDATE ON "next_console"."role_permission_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."system_notice"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "notice_title" text NOT NULL ,
 "notice_icon" text ,
 "notice_type" varchar(255) NOT NULL ,
 "notice_level" varchar(255) NOT NULL ,
 "notice_content" text ,
 "notice_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP )
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."system_notice"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."system_notice"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."system_notice"."notice_title" IS '通知标题';
COMMENT ON COLUMN "next_console"."system_notice"."notice_icon" IS '通知图标';
COMMENT ON COLUMN "next_console"."system_notice"."notice_type" IS '通知图标';
COMMENT ON COLUMN "next_console"."system_notice"."notice_level" IS '通知等级';
COMMENT ON COLUMN "next_console"."system_notice"."notice_content" IS '通知内容';
COMMENT ON COLUMN "next_console"."system_notice"."notice_status" IS '通知状态';
COMMENT ON COLUMN "next_console"."system_notice"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."system_notice"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."system_notice" IS '站内信';

CREATE INDEX "user_id67"
ON "next_console"."system_notice" USING btree ( "user_id" )
;
CREATE TRIGGER update_system_notice_trigger BEFORE UPDATE ON "next_console"."system_notice" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------


CREATE TABLE "next_console"."user_notice_task_info" (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  notice_type VARCHAR(255) NOT NULL,
  notice_template TEXT NOT NULL,
  notice_params json NOT NULL,
  task_status VARCHAR(255) NOT NULL,
  begin_time TIMESTAMP,
  finish_time TIMESTAMP,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  task_name VARCHAR(255),
  task_desc TEXT,
  plan_begin_time TIMESTAMP,
  plan_finish_time TIMESTAMP,
  run_now boolean,
  task_instance_total INTEGER DEFAULT 0,
  task_instance_success INTEGER DEFAULT 0,
  task_instance_failed INTEGER DEFAULT 0,
  task_instance_batch_size INTEGER DEFAULT 1
);

COMMENT ON TABLE "next_console"."user_notice_task_info" IS '用户通知任务信息表';
COMMENT ON COLUMN "next_console"."user_notice_task_info".id IS 'ID 编号';
COMMENT ON COLUMN "next_console"."user_notice_task_info".user_id IS '用户id';
COMMENT ON COLUMN "next_console"."user_notice_task_info".notice_type IS '通知类型';
COMMENT ON COLUMN "next_console"."user_notice_task_info".notice_template IS '通知模版';
COMMENT ON COLUMN "next_console"."user_notice_task_info".notice_params IS '通知变量';
COMMENT ON COLUMN "next_console"."user_notice_task_info".task_status IS '任务状态';
COMMENT ON COLUMN "next_console"."user_notice_task_info".begin_time IS '任务开始时间';
COMMENT ON COLUMN "next_console"."user_notice_task_info".finish_time IS '任务完成时间';
COMMENT ON COLUMN "next_console"."user_notice_task_info".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."user_notice_task_info".update_time IS '更新时间';
COMMENT ON COLUMN "next_console"."user_notice_task_info".task_name IS '任务名称';
COMMENT ON COLUMN "next_console"."user_notice_task_info".task_desc IS '任务描述';
COMMENT ON COLUMN "next_console"."user_notice_task_info".plan_begin_time IS '计划启动时间';
COMMENT ON COLUMN "next_console"."user_notice_task_info".plan_finish_time IS '计划完成时间';
COMMENT ON COLUMN "next_console"."user_notice_task_info".run_now IS '立刻执行';
COMMENT ON COLUMN "next_console"."user_notice_task_info".task_instance_total IS '任务实例数量';
COMMENT ON COLUMN "next_console"."user_notice_task_info".task_instance_success IS '任务实例完成数';
COMMENT ON COLUMN "next_console"."user_notice_task_info".task_instance_failed IS '任务实例失败数量';
COMMENT ON COLUMN "next_console"."user_notice_task_info".task_instance_batch_size IS '任务实例事务大小';
CREATE TRIGGER update_user_notice_task_info_trigger BEFORE UPDATE ON "next_console"."user_notice_task_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


CREATE TABLE "next_console"."user_notice_task_instance" (
  id SERIAL PRIMARY KEY,
  task_id INTEGER NOT NULL ,
  receive_user_id INTEGER NOT NULL,
  task_celery_id VARCHAR(255) NOT NULL,
  notice_type VARCHAR(255) NOT NULL,
  notice_params json NOT NULL ,
  notice_content TEXT NOT NULL ,
  notice_status VARCHAR(255) NOT NULL ,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 添加表注释和列注释
COMMENT ON TABLE "next_console"."user_notice_task_instance" IS '用户通知任务实例';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".id IS 'ID 编号';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".task_id IS '任务id';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".receive_user_id IS '接受用户';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".task_celery_id IS 'celery-id';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".notice_type IS '通知类型';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".notice_params IS '通知变量';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".notice_content IS '通知内容';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".notice_status IS '通知状态';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."user_notice_task_instance".update_time IS '更新时间';

CREATE TRIGGER update_user_notice_task_instance_trigger BEFORE UPDATE ON "next_console"."user_notice_task_instance" FOR EACH ROW
EXECUTE FUNCTION update_update_time();