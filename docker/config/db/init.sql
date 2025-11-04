CREATE SCHEMA IF NOT EXISTS next_console
AUTHORIZATION next_console;

-- 4. 设置默认搜索路径（可选）
ALTER ROLE next_console SET search_path TO next_console, public;

-- 创建 vector 扩展
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA next_console;


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

CREATE TABLE "next_console"."company_info"
(
 "id" SERIAL PRIMARY KEY,
 "parent_company_id" integer ,
 "company_code" varchar(255) NOT NULL ,
 "company_name" varchar(255) NOT NULL ,
 "company_country" varchar(255) NOT NULL ,
 "company_area" varchar(255) NOT NULL ,
 "company_industry" text NOT NULL ,
 "company_scale" text NOT NULL ,
 "company_desc" text NOT NULL ,
 "company_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "company_address" text ,
 "company_phone" varchar(100) ,
 "company_email" varchar(100) ,
 "company_website" text ,
 "company_logo" text ,
 "company_type" text

)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."company_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."company_info"."parent_company_id" IS '父企业id';
COMMENT ON COLUMN "next_console"."company_info"."company_code" IS '企业编号';
COMMENT ON COLUMN "next_console"."company_info"."company_name" IS '企业名称';
COMMENT ON COLUMN "next_console"."company_info"."company_country" IS '企业归属国家';
COMMENT ON COLUMN "next_console"."company_info"."company_area" IS '企业归属地区';
COMMENT ON COLUMN "next_console"."company_info"."company_industry" IS '企业行业';
COMMENT ON COLUMN "next_console"."company_info"."company_scale" IS '企业规模';
COMMENT ON COLUMN "next_console"."company_info"."company_desc" IS '企业介绍';
COMMENT ON COLUMN "next_console"."company_info"."company_status" IS '公司状态';
COMMENT ON COLUMN "next_console"."company_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."company_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."company_info"."company_address" IS '公司地址';
COMMENT ON COLUMN "next_console"."company_info"."company_phone" IS '公司电话';
COMMENT ON COLUMN "next_console"."company_info"."company_email" IS '公司邮箱';
COMMENT ON COLUMN "next_console"."company_info"."company_website" IS '公司网站';
COMMENT ON COLUMN "next_console"."company_info"."company_logo" IS '公司logo';
COMMENT ON COLUMN "next_console"."company_info"."company_type" IS '公司类型';
COMMENT ON TABLE "next_console"."company_info" IS '公司信息表';

CREATE INDEX "parent_company_id5"
ON "next_console"."company_info" USING btree ( "parent_company_id" )
;

CREATE TRIGGER update_company_info_trigger BEFORE UPDATE ON "next_console"."company_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------
CREATE TABLE "next_console"."enterprise_email_whitelist" (
    id SERIAL PRIMARY KEY,
    email_name VARCHAR(255) NOT NULL,
    company_id INTEGER,
    company_name VARCHAR(255),
    company_desc VARCHAR(255),
    company_status VARCHAR(255),
    email_status VARCHAR(255) NOT NULL,
    create_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "next_console"."enterprise_email_whitelist" IS '企业邮箱白名单';
COMMENT ON COLUMN "next_console"."enterprise_email_whitelist".id IS 'ID 编号';
COMMENT ON COLUMN "next_console"."enterprise_email_whitelist".email_name IS '邮箱后缀';
COMMENT ON COLUMN "next_console"."enterprise_email_whitelist".company_id IS '公司 id';
COMMENT ON COLUMN "next_console"."enterprise_email_whitelist".company_name IS '公司名称';
COMMENT ON COLUMN "next_console"."enterprise_email_whitelist".company_desc IS '公司描述';
COMMENT ON COLUMN "next_console"."enterprise_email_whitelist".company_status IS '公司状态';
COMMENT ON COLUMN "next_console"."enterprise_email_whitelist".email_status IS '企业邮箱状态';
COMMENT ON COLUMN "next_console"."enterprise_email_whitelist".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."enterprise_email_whitelist".update_time IS '更新时间';
CREATE INDEX idx_enterprise_email_whitelist_company_id ON "next_console"."enterprise_email_whitelist" (company_id);
CREATE TRIGGER update_enterprise_email_whitelist_trigger BEFORE UPDATE ON "next_console"."enterprise_email_whitelist" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."department_info"
(
 "id" SERIAL PRIMARY KEY,
 "company_id" integer NOT NULL ,
 "parent_department_id" integer ,
 "department_code" varchar(255) NOT NULL ,
 "department_name" varchar(255) NOT NULL ,
 "department_desc" text NOT NULL ,
 "department_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "department_logo" text
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."department_info"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."department_info"."company_id" IS '归属公司id';
COMMENT ON COLUMN "next_console"."department_info"."parent_department_id" IS '上级部门id';
COMMENT ON COLUMN "next_console"."department_info"."department_code" IS '部门编号';
COMMENT ON COLUMN "next_console"."department_info"."department_name" IS '部门名称';
COMMENT ON COLUMN "next_console"."department_info"."department_desc" IS '部门介绍';
COMMENT ON COLUMN "next_console"."department_info"."department_status" IS '部门状态';
COMMENT ON COLUMN "next_console"."department_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."department_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."department_info"."department_logo" IS '部门图标';
COMMENT ON TABLE "next_console"."department_info" IS '部门信息表';

CREATE INDEX "department_info_company_info_FK6"
ON "next_console"."department_info" USING btree ( "company_id" )
;
CREATE INDEX "department_info_department_info_FK7"
ON "next_console"."department_info" USING btree ( "parent_department_id" )
;
CREATE TRIGGER update_department_info_trigger BEFORE UPDATE ON "next_console"."department_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."resource_object_meta_info"
(
 "id" SERIAL PRIMARY KEY,
 "resource_parent_id" integer ,
 "user_id" integer NOT NULL ,
 "resource_name" varchar(255) NOT NULL ,
 "resource_type" varchar(255) NOT NULL ,
 "resource_desc" text NOT NULL ,
 "resource_icon" text NOT NULL ,
 "resource_format" varchar(255) NOT NULL ,
 "resource_size_in_MB" double precision NOT NULL ,
 "resource_path" text NOT NULL ,
 "resource_source_url" text NOT NULL ,
 "resource_source_url_site" text NOT NULL ,
 "resource_show_url" text NOT NULL ,
 "resource_feature_code" varchar(255) NOT NULL ,
 "resource_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "resource_download_url" text ,
 "delete_time" timestamp with time zone ,
 "resource_is_share" boolean ,
 "resource_is_public" boolean ,
 "resource_title" text ,
 "resource_source" varchar(100) ,
 "resource_language" varchar(100) ,
 "resource_public_access" varchar(255) ,
 "resource_version" integer DEFAULT 1,
 "resource_is_open" boolean
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."id" IS 'id';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_parent_id" IS '父资源id';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_name" IS '资源名称';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_type" IS '资源类型';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_desc" IS '资源描述';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_icon" IS '资源图标';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_format" IS '资源格式';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_size_in_MB" IS '资源大小';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_path" IS '资源存储路径';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_source_url" IS '资源来源地址';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_source_url_site" IS '文档url归属主站';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_show_url" IS '资源展示地址';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_feature_code" IS '资源特征编码';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_status" IS '资源状态';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_download_url" IS '资源下载链接';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."delete_time" IS '删除时间';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_is_share" IS '资源是否分享';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_is_public" IS '资源是否公开';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_title" IS '资源标题';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_source" IS '资源来源';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_language" IS '资源语言';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_public_access" IS '资源公开权限';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_version" IS '资源版本';
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_is_open" IS '资源是否公开';
COMMENT ON TABLE "next_console"."resource_object_meta_info" IS '大模型提问信息';



CREATE TRIGGER update_resource_object_meta_info_trigger BEFORE UPDATE ON "next_console"."resource_object_meta_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------

CREATE TABLE "next_console"."resource_object_upload_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "resource_parent_id" integer ,
 "resource_name" varchar(255) NOT NULL ,
 "resource_size_in_mb" double precision NOT NULL ,
 "resource_type" varchar(255) NOT NULL ,
 "resource_format" varchar(255) NOT NULL ,
 "content_max_idx" integer NOT NULL ,
 "content_finish_idx" integer NOT NULL ,
 "content_prefix" varchar(255) NOT NULL ,
 "resource_md5" varchar(255) NOT NULL ,
 "resource_id" integer ,
 "task_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "task_icon" text ,
 "task_source" varchar(255)
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."id" IS '任务id';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."resource_parent_id" IS '父资源id';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."resource_name" IS '资源名称';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."resource_size_in_mb" IS '资源大小';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."resource_type" IS '资源类型';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."resource_format" IS '资源格式';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."content_max_idx" IS '资源分块数';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."content_finish_idx" IS '资源分块完成数';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."content_prefix" IS '资源分块前缀';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."resource_md5" IS '资源md5值';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."task_status" IS '任务状态';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."task_icon" IS '任务图标';
COMMENT ON COLUMN "next_console"."resource_object_upload_info"."task_source" IS '任务来源';
COMMENT ON TABLE "next_console"."resource_object_upload_info" IS '资源对象上传信息';

CREATE INDEX "resource_id37"
ON "next_console"."resource_object_upload_info" USING btree ( "resource_id" )
;
CREATE INDEX "resource_parent_id38"
ON "next_console"."resource_object_upload_info" USING btree ( "resource_parent_id" )
;
CREATE INDEX "user_id36"
ON "next_console"."resource_object_upload_info" USING btree ( "user_id" )
;


CREATE TRIGGER update_resource_object_upload_info_trigger BEFORE UPDATE ON "next_console"."resource_object_upload_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."resource_object_shortcuts_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "resource_id" integer NOT NULL ,
 "shortcut_status" varchar(255) ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_object_shortcuts_info"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."resource_object_shortcuts_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."resource_object_shortcuts_info"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."resource_object_shortcuts_info"."shortcut_status" IS '快捷方式状态';
COMMENT ON COLUMN "next_console"."resource_object_shortcuts_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_object_shortcuts_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."resource_object_shortcuts_info" IS '资源快捷方式信息';

CREATE INDEX "resource_id35"
ON "next_console"."resource_object_shortcuts_info" USING btree ( "resource_id" )
;
CREATE INDEX "user_id34"
ON "next_console"."resource_object_shortcuts_info" USING btree ( "user_id" )
;


CREATE TRIGGER update_resource_object_shortcuts_info_trigger BEFORE UPDATE ON "next_console"."resource_object_shortcuts_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


------------------------------------------------------------

CREATE TABLE "next_console"."resource_download_record"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "resource_id" integer NOT NULL ,
 "download_url" text NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_download_record"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."resource_download_record"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."resource_download_record"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."resource_download_record"."download_url" IS '下载链接';
COMMENT ON COLUMN "next_console"."resource_download_record"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_download_record"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."resource_download_record" IS '资源下载记录表';

CREATE INDEX "resource_id31"
ON "next_console"."resource_download_record" USING btree ( "resource_id" )
;
CREATE INDEX "user_id30"
ON "next_console"."resource_download_record" USING btree ( "user_id" )
;

CREATE TRIGGER update_resource_download_record_trigger BEFORE UPDATE ON "next_console"."resource_download_record" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


------------------------------------------------------------

CREATE TABLE "next_console"."resource_tag_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "tag_name" varchar(255) NOT NULL ,
 "tag_type" varchar(255) NOT NULL ,
 "tag_source" varchar(255) NOT NULL ,
 "tag_value" varchar(255) NOT NULL ,
 "tag_color" varchar(255) NOT NULL ,
 "tag_icon" text NOT NULL ,
 "tag_desc" text NOT NULL ,
 "tag_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_tag_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."resource_tag_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."resource_tag_info"."tag_name" IS '标签名称';
COMMENT ON COLUMN "next_console"."resource_tag_info"."tag_type" IS '标签类型';
COMMENT ON COLUMN "next_console"."resource_tag_info"."tag_source" IS '标签来源';
COMMENT ON COLUMN "next_console"."resource_tag_info"."tag_value" IS '标签值';
COMMENT ON COLUMN "next_console"."resource_tag_info"."tag_color" IS '标签颜色';
COMMENT ON COLUMN "next_console"."resource_tag_info"."tag_icon" IS '标签图标';
COMMENT ON COLUMN "next_console"."resource_tag_info"."tag_desc" IS '标签描述';
COMMENT ON COLUMN "next_console"."resource_tag_info"."tag_status" IS '标签状态';
COMMENT ON COLUMN "next_console"."resource_tag_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_tag_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."resource_tag_info" IS '资源标签信息表';

CREATE INDEX "user_id39"
ON "next_console"."resource_tag_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_resource_tag_info_trigger BEFORE UPDATE ON "next_console"."resource_tag_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------
CREATE TABLE "next_console"."resource_tag_relation"
(
 "id" SERIAL PRIMARY KEY,
 "resource_id" integer NOT NULL ,
 "tag_id" integer NOT NULL ,
 "rel_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_tag_relation"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."resource_tag_relation"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."resource_tag_relation"."tag_id" IS '标签id';
COMMENT ON COLUMN "next_console"."resource_tag_relation"."rel_status" IS '关系状态';
COMMENT ON COLUMN "next_console"."resource_tag_relation"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_tag_relation"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."resource_tag_relation" IS '资源标签关系表';

CREATE INDEX "resource_id40"
ON "next_console"."resource_tag_relation" USING btree ( "resource_id" )
;
CREATE INDEX "tag_id41"
ON "next_console"."resource_tag_relation" USING btree ( "tag_id" )
;
CREATE TRIGGER update_resource_tag_relation_trigger BEFORE UPDATE ON "next_console"."resource_tag_relation" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------


CREATE TABLE "next_console"."resource_object_history_info"
(
 "id" SERIAL PRIMARY KEY,
 "resource_id" integer NOT NULL ,
 "resource_parent_id" integer ,
 "user_id" integer NOT NULL ,
 "resource_name" varchar(255) NOT NULL ,
 "resource_type" varchar(255) NOT NULL ,
 "resource_desc" text NOT NULL ,
 "resource_icon" text NOT NULL ,
 "resource_format" varchar(255) NOT NULL ,
 "resource_size_in_MB" double precision NOT NULL ,
 "resource_path" text NOT NULL ,
 "resource_source_url" text NOT NULL ,
 "resource_source_url_site" text NOT NULL ,
 "resource_show_url" text NOT NULL ,
 "resource_download_url" varchar(255) NOT NULL ,
 "resource_feature_code" varchar(255) NOT NULL ,
 "resource_is_share" boolean ,
 "resource_is_public" boolean ,
 "resource_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "resource_title" varchar(255) ,
 "resource_public_access" varchar(255) ,
 "resource_language" varchar(255) ,
 "resource_version" integer ,
 "delete_time" timestamp with time zone ,
 "resource_source" text ,
 "modifier_id" integer
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_object_history_info"."id" IS 'id';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_parent_id" IS '父资源id';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_name" IS '资源名称';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_type" IS '资源类型';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_desc" IS '资源描述';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_icon" IS '资源图标';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_format" IS '资源格式';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_size_in_MB" IS '资源大小';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_path" IS '资源存储路径';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_source_url" IS '资源来源地址';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_source_url_site" IS '文档url归属主站';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_show_url" IS '资源展示地址';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_download_url" IS '资源md5值';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_feature_code" IS '资源特征编码';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_is_share" IS '资源是否共享';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_is_public" IS '资源是否公开';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_status" IS '资源状态';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_title" IS '资源标题';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_public_access" IS '资源公开访问权限';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_language" IS '资源语言';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_version" IS '资源版本';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."delete_time" IS '删除时间';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."resource_source" IS '资源来源';
COMMENT ON COLUMN "next_console"."resource_object_history_info"."modifier_id" IS '修改用户id';
COMMENT ON TABLE "next_console"."resource_object_history_info" IS '资源对象历史版本信息';

CREATE INDEX "resource_parent_id32"
ON "next_console"."resource_object_history_info" USING btree ( "resource_parent_id" )
;
CREATE TRIGGER update_resource_object_history_info_trigger BEFORE UPDATE ON "next_console"."resource_object_history_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."resource_attachment_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "attachment_key" text NOT NULL ,
 "attachment_name" text NOT NULL ,
 "attachment_path" text NOT NULL ,
 "attachment_size" text NOT NULL ,
 "attachment_url" text NOT NULL ,
 "attachment_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_attachment_info"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."resource_attachment_info"."user_id" IS '目标用户id';
COMMENT ON COLUMN "next_console"."resource_attachment_info"."attachment_key" IS '附件对象 ID';
COMMENT ON COLUMN "next_console"."resource_attachment_info"."attachment_name" IS '附件名称';
COMMENT ON COLUMN "next_console"."resource_attachment_info"."attachment_path" IS '附件存储路径';
COMMENT ON COLUMN "next_console"."resource_attachment_info"."attachment_size" IS '附件大小';
COMMENT ON COLUMN "next_console"."resource_attachment_info"."attachment_url" IS '附件下载地址';
COMMENT ON COLUMN "next_console"."resource_attachment_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_attachment_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."resource_attachment_info" IS '资源附件信息';

CREATE INDEX "user_id29"
ON "next_console"."resource_attachment_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_resource_attachment_info_trigger BEFORE UPDATE ON "next_console"."resource_attachment_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();



------------------------------------------------------------

CREATE TABLE "next_console"."resource_view_record"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "resource_id" integer NOT NULL ,
 "client_fingerprint" varchar(255) ,
 "client_ip" varchar(255) ,
 "create_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_view_record"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."resource_view_record"."user_id" IS '目标用户id';
COMMENT ON COLUMN "next_console"."resource_view_record"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."resource_view_record"."client_fingerprint" IS '客户端指纹';
COMMENT ON COLUMN "next_console"."resource_view_record"."client_ip" IS '客户端ip';
COMMENT ON COLUMN "next_console"."resource_view_record"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_view_record"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."resource_view_record" IS '资源查看记录表';
CREATE TRIGGER update_resource_view_record_trigger BEFORE UPDATE ON "next_console"."resource_view_record" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------

CREATE TABLE "next_console"."share_resource_authorize_company_info"
(
 "id" SERIAL PRIMARY KEY,
 "resource_id" integer NOT NULL ,
 "user_id" integer NOT NULL ,
 "company_id" integer NOT NULL ,
 "auth_type" varchar(255) NOT NULL ,
 "auth_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."share_resource_authorize_company_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_company_info"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_company_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_company_info"."company_id" IS '公司id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_company_info"."auth_type" IS '授权类型';
COMMENT ON COLUMN "next_console"."share_resource_authorize_company_info"."auth_status" IS '授权状态';
COMMENT ON COLUMN "next_console"."share_resource_authorize_company_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."share_resource_authorize_company_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."share_resource_authorize_company_info" IS '共享资源授权公司信息表';

CREATE INDEX "company_id52"
ON "next_console"."share_resource_authorize_company_info" USING btree ( "company_id" )
;
CREATE INDEX "resource_id54"
ON "next_console"."share_resource_authorize_company_info" USING btree ( "resource_id" )
;
CREATE INDEX "user_id53"
ON "next_console"."share_resource_authorize_company_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_share_resource_authorize_company_info_trigger BEFORE UPDATE ON "next_console"."share_resource_authorize_company_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


------------------------------------------------------------

CREATE TABLE "next_console"."share_resource_authorize_department_info"
(
 "id" SERIAL PRIMARY KEY,
 "resource_id" integer NOT NULL ,
 "user_id" integer NOT NULL ,
 "department_id" integer NOT NULL ,
 "auth_type" varchar(255) NOT NULL ,
 "auth_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."share_resource_authorize_department_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_department_info"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_department_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_department_info"."department_id" IS '部门id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_department_info"."auth_type" IS '授权类型';
COMMENT ON COLUMN "next_console"."share_resource_authorize_department_info"."auth_status" IS '授权状态';
COMMENT ON COLUMN "next_console"."share_resource_authorize_department_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."share_resource_authorize_department_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."share_resource_authorize_department_info" IS '共享资源授权部门表';

CREATE INDEX "department_id55"
ON "next_console"."share_resource_authorize_department_info" USING btree ( "department_id" )
;
CREATE INDEX "resource_id57"
ON "next_console"."share_resource_authorize_department_info" USING btree ( "resource_id" )
;
CREATE INDEX "user_id56"
ON "next_console"."share_resource_authorize_department_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_share_resource_authorize_department_info_trigger BEFORE UPDATE ON "next_console"."share_resource_authorize_department_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."share_resource_authorize_colleague_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "resource_id" integer NOT NULL ,
 "auth_user_id" integer NOT NULL ,
 "auth_type" varchar(255) NOT NULL ,
 "auth_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."share_resource_authorize_colleague_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_colleague_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_colleague_info"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_colleague_info"."auth_user_id" IS '被授权用户id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_colleague_info"."auth_type" IS '授权类型';
COMMENT ON COLUMN "next_console"."share_resource_authorize_colleague_info"."auth_status" IS '授权状态';
COMMENT ON COLUMN "next_console"."share_resource_authorize_colleague_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."share_resource_authorize_colleague_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."share_resource_authorize_colleague_info" IS '共享资源授权用户表';

CREATE INDEX "auth_user_id51"
ON "next_console"."share_resource_authorize_colleague_info" USING btree ( "auth_user_id" )
;
CREATE INDEX "resource_id50"
ON "next_console"."share_resource_authorize_colleague_info" USING btree ( "resource_id" )
;
CREATE INDEX "user_id49"
ON "next_console"."share_resource_authorize_colleague_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_share_resource_authorize_colleague_info_trigger BEFORE UPDATE ON "next_console"."share_resource_authorize_colleague_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."share_resource_authorize_friend_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "resource_id" integer NOT NULL ,
 "auth_user_id" integer NOT NULL ,
 "auth_type" varchar(255) NOT NULL ,
 "auth_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."share_resource_authorize_friend_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_friend_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_friend_info"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_friend_info"."auth_user_id" IS '被授权用户id';
COMMENT ON COLUMN "next_console"."share_resource_authorize_friend_info"."auth_type" IS '授权类型';
COMMENT ON COLUMN "next_console"."share_resource_authorize_friend_info"."auth_status" IS '授权状态';
COMMENT ON COLUMN "next_console"."share_resource_authorize_friend_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."share_resource_authorize_friend_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."share_resource_authorize_friend_info" IS '共享资源授权好友表';

CREATE INDEX "auth_user_id60"
ON "next_console"."share_resource_authorize_friend_info" USING btree ( "auth_user_id" )
;
CREATE INDEX "resource_id59"
ON "next_console"."share_resource_authorize_friend_info" USING btree ( "resource_id" )
;
CREATE INDEX "user_id58"
ON "next_console"."share_resource_authorize_friend_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_share_resource_authorize_friend_info_trigger BEFORE UPDATE ON "next_console"."share_resource_authorize_friend_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------

CREATE TABLE "next_console"."resource_download_cooling_record" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    resource_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    author_notice BOOLEAN,
    author_allow BOOLEAN,
    author_allow_cnt INTEGER,
    create_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE "next_console"."resource_download_cooling_record" IS '资源下载冷却记录表';
-- 为各列添加注释
COMMENT ON COLUMN "next_console"."resource_download_cooling_record".id IS 'ID 编号';
COMMENT ON COLUMN "next_console"."resource_download_cooling_record".user_id IS '目标用户 id';
COMMENT ON COLUMN "next_console"."resource_download_cooling_record".resource_id IS '目标资源 id';
COMMENT ON COLUMN "next_console"."resource_download_cooling_record".author_id IS '资源作者 id';
COMMENT ON COLUMN "next_console"."resource_download_cooling_record".author_notice IS '是否通知作者';
COMMENT ON COLUMN "next_console"."resource_download_cooling_record".author_allow IS '作者是否允许继续下载';
COMMENT ON COLUMN "next_console"."resource_download_cooling_record".author_allow_cnt IS '作者新增次数';
COMMENT ON COLUMN "next_console"."resource_download_cooling_record".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_download_cooling_record".update_time IS '更新时间';

-- 创建 user_id 列的索引
CREATE INDEX idx_resource_download_cooling_record_user_id ON "next_console"."resource_download_cooling_record" (user_id);
-- 创建 resource_id 列的索引
CREATE INDEX idx_resource_download_cooling_record_resource_id ON "next_console"."resource_download_cooling_record" (resource_id);
-- 创建 author_id 列的索引
CREATE INDEX idx_resource_download_cooling_record_author_id ON "next_console"."resource_download_cooling_record" (author_id);

CREATE TRIGGER update_resource_download_cooling_record_trigger BEFORE UPDATE ON "next_console"."resource_download_cooling_record" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

CREATE TABLE "next_console"."rag_ref_info"
(
 "id" SERIAL PRIMARY KEY,
 "resource_id" integer ,
 "ref_code" varchar(255) NOT NULL ,
 "user_id" integer NOT NULL ,
 "celery_task_id" varchar(255) ,
 "task_trace_log" text ,
 "file_reader_config" json ,
 "file_split_config" json ,
 "file_chunk_abstract_config" json ,
 "file_chunk_embedding_config" json ,
 "ref_type" varchar(255) NOT NULL ,
 "ref_chunk_cnt" integer ,
 "ref_chunk_ready_cnt" integer ,
 "ref_embedding_token_used" integer ,
 "ref_hit_counts" integer ,
 "ref_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP

)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."rag_ref_info"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."rag_ref_info"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."rag_ref_info"."ref_code" IS '索引任务编号';
COMMENT ON COLUMN "next_console"."rag_ref_info"."user_id" IS '创建用户id';
COMMENT ON COLUMN "next_console"."rag_ref_info"."celery_task_id" IS '任务id';
COMMENT ON COLUMN "next_console"."rag_ref_info"."task_trace_log" IS '任务异常日志';
COMMENT ON COLUMN "next_console"."rag_ref_info"."file_reader_config" IS '文件阅读配置';
COMMENT ON COLUMN "next_console"."rag_ref_info"."file_split_config" IS '文件切分配置';
COMMENT ON COLUMN "next_console"."rag_ref_info"."file_chunk_abstract_config" IS '文件摘要提取配置';
COMMENT ON COLUMN "next_console"."rag_ref_info"."file_chunk_embedding_config" IS '文件嵌入向量配置';
COMMENT ON COLUMN "next_console"."rag_ref_info"."ref_type" IS '索引类型';
COMMENT ON COLUMN "next_console"."rag_ref_info"."ref_chunk_cnt" IS '分块个数';
COMMENT ON COLUMN "next_console"."rag_ref_info"."ref_chunk_ready_cnt" IS '就绪分块个数';
COMMENT ON COLUMN "next_console"."rag_ref_info"."ref_embedding_token_used" IS '分段嵌入使用的token数量';
COMMENT ON COLUMN "next_console"."rag_ref_info"."ref_hit_counts" IS '索引命中次数';
COMMENT ON COLUMN "next_console"."rag_ref_info"."ref_status" IS '索引状态';
COMMENT ON COLUMN "next_console"."rag_ref_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."rag_ref_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."rag_ref_info" IS 'rag索引信息';

CREATE INDEX "user_id28"
ON "next_console"."rag_ref_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_rag_ref_info_trigger BEFORE UPDATE ON "next_console"."rag_ref_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."resource_chunk_info"
(
 "id" SERIAL PRIMARY KEY,
 "resource_id" integer NOT NULL ,
 "split_method" varchar(255) NOT NULL ,
 "chunk_type" varchar(255) NOT NULL ,
 "chunk_format" varchar(255) NOT NULL ,
 "chunk_size" integer NOT NULL ,
 "chunk_raw_content" text NOT NULL ,
 "ref_id" integer ,
 "chunk_embedding_content" text ,
 "chunk_embedding_type" varchar(255) ,
 "chunk_embedding" vector ,
 "chunk_hit_counts" integer ,
 "status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."resource_chunk_info"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."split_method" IS '切分方法';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."chunk_type" IS '分段类型';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."chunk_format" IS '分段格式';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."chunk_size" IS '分段大小（kB）';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."chunk_raw_content" IS '分段原始内容';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."ref_id" IS '参考索引ID';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."chunk_embedding_content" IS '分段嵌入内容';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."chunk_embedding_type" IS '分段嵌入类型';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."chunk_embedding" IS '分段嵌入向量';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."chunk_hit_counts" IS '分块命中次数';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."status" IS '分段状态';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."resource_chunk_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."resource_chunk_info" IS '资源分段信息表';
CREATE TRIGGER update_resource_chunk_info_trigger BEFORE UPDATE ON "next_console"."resource_chunk_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."rag_query_log"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer ,
 "session_id" integer ,
 "msg_id" integer ,
 "task_id" integer ,
 "query_text" text ,
 "ref_ids" json ,
 "status" varchar(255) NOT NULL ,
 "trace_log" text ,
 "config" json ,
 "result" json ,
 "time_usage" json ,
 "create_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."rag_query_log"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."rag_query_log"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."rag_query_log"."session_id" IS '会话id';
COMMENT ON COLUMN "next_console"."rag_query_log"."msg_id" IS '问题id';
COMMENT ON COLUMN "next_console"."rag_query_log"."task_id" IS '任务id';
COMMENT ON COLUMN "next_console"."rag_query_log"."query_text" IS '查询语句';
COMMENT ON COLUMN "next_console"."rag_query_log"."ref_ids" IS '文献列表';
COMMENT ON COLUMN "next_console"."rag_query_log"."status" IS '运行状态';
COMMENT ON COLUMN "next_console"."rag_query_log"."trace_log" IS '运行日志';
COMMENT ON COLUMN "next_console"."rag_query_log"."config" IS '查询配置';
COMMENT ON COLUMN "next_console"."rag_query_log"."result" IS '查询结果';
COMMENT ON COLUMN "next_console"."rag_query_log"."time_usage" IS '查询时间消耗';
COMMENT ON COLUMN "next_console"."rag_query_log"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."rag_query_log"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."rag_query_log" IS 'rag查询日志';
CREATE TRIGGER update_rag_query_log_trigger BEFORE UPDATE ON "next_console"."rag_query_log" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

CREATE TABLE "next_console"."assistant_info"
(
 "id" SERIAL PRIMARY KEY,
 "assistant_name" varchar(255) NOT NULL ,
 "assistant_desc" text NOT NULL ,
 "assistant_tags" JSON NOT NULL ,
 "assistant_status" varchar(255) NOT NULL ,
 "assistant_role_prompt" text NOT NULL ,
 "assistant_avatar" varchar(255) NOT NULL ,
 "assistant_language" varchar(255) NOT NULL ,
 "assistant_voice" varchar(255) NOT NULL ,
 "assistant_model_name" varchar(255) NOT NULL ,
 "assistant_model_temperature" double precision NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "assistant_memory_size" integer ,
 "rag_miss" integer ,
 "rag_miss_answer" text ,
 "rag_factor" double precision ,
 "rag_relevant_threshold" double precision ,
 "workflow" json ,
 "workflow_flag" boolean ,
 "assistant_model_code" varchar(100) ,
 "assistant_title" varchar(100) ,
 "assistant_avatar_source" text ,
 "assistant_prologue" text ,
 "assistant_preset_question" json
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."assistant_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_name" IS '助手名称';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_desc" IS '助手描述';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_tags" IS '助手标签';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_status" IS '助手状态';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_role_prompt" IS '助手定义';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_avatar" IS '助手头像';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_language" IS '助手语言';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_voice" IS '助手声音';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_model_name" IS '助手模型类型';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_model_temperature" IS '助手模型温度';
COMMENT ON COLUMN "next_console"."assistant_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."assistant_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_memory_size" IS '助手脑容量';
COMMENT ON COLUMN "next_console"."assistant_info"."rag_miss" IS 'rag未命中应对';
COMMENT ON COLUMN "next_console"."assistant_info"."rag_miss_answer" IS 'rag未命中应对文本';
COMMENT ON COLUMN "next_console"."assistant_info"."rag_factor" IS '混合检索系数';
COMMENT ON COLUMN "next_console"."assistant_info"."rag_relevant_threshold" IS '语义相关度阈值';
COMMENT ON COLUMN "next_console"."assistant_info"."workflow" IS '工作流';
COMMENT ON COLUMN "next_console"."assistant_info"."workflow_flag" IS '是否启用工作流';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_model_code" IS '助手模型编号';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_title" IS '助手岗位';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_avatar_source" IS '助手头像来源';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_prologue" IS '助手开场白';
COMMENT ON COLUMN "next_console"."assistant_info"."assistant_preset_question" IS '助手预置问题';
COMMENT ON TABLE "next_console"."assistant_info" IS '助手信息表';
CREATE TRIGGER update_assistant_info_trigger BEFORE UPDATE ON "next_console"."assistant_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


------------------------------------------------------------

CREATE TABLE "next_console"."user_assistant_relation"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "assistant_id" integer NOT NULL ,
 "rel_type" varchar(255) NOT NULL ,
 "rel_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "rel_value" double precision
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."user_assistant_relation"."id" IS '自增';
COMMENT ON COLUMN "next_console"."user_assistant_relation"."user_id" IS '用户';
COMMENT ON COLUMN "next_console"."user_assistant_relation"."assistant_id" IS '助手';
COMMENT ON COLUMN "next_console"."user_assistant_relation"."rel_type" IS '关系类型';
COMMENT ON COLUMN "next_console"."user_assistant_relation"."rel_status" IS '关系状态';
COMMENT ON COLUMN "next_console"."user_assistant_relation"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."user_assistant_relation"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."user_assistant_relation"."rel_value" IS '关系值';
COMMENT ON TABLE "next_console"."user_assistant_relation" IS '用户助手关系表';

CREATE INDEX "user_assistant_relation_ibfk_276"
ON "next_console"."user_assistant_relation" USING btree ( "assistant_id" )
;
CREATE UNIQUE INDEX "user_assistant_relation_unique75"
ON "next_console"."user_assistant_relation" USING btree ( "user_id" ,"assistant_id" ,"rel_type" COLLATE "pg_catalog"."default" )
;
CREATE TRIGGER update_user_assistant_relation_trigger BEFORE UPDATE ON "next_console"."user_assistant_relation" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------
CREATE TABLE "next_console"."assistant_run_info"
(
 "id" SERIAL PRIMARY KEY,
 "assistant_id" integer NOT NULL ,
 "indicator_name" varchar(255) NOT NULL ,
 "indicator_desc" varchar(255) NOT NULL ,
 "indicator_type" varchar(255) NOT NULL ,
 "indicator_value" double precision ,
 "begin_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP ,
 "end_time" timestamp with time zone NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."assistant_run_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."assistant_run_info"."assistant_id" IS '助手id';
COMMENT ON COLUMN "next_console"."assistant_run_info"."indicator_name" IS '指标名称';
COMMENT ON COLUMN "next_console"."assistant_run_info"."indicator_desc" IS '指标描述';
COMMENT ON COLUMN "next_console"."assistant_run_info"."indicator_type" IS '指标类型';
COMMENT ON COLUMN "next_console"."assistant_run_info"."indicator_value" IS '指标值';
COMMENT ON COLUMN "next_console"."assistant_run_info"."begin_time" IS '开始时间';
COMMENT ON COLUMN "next_console"."assistant_run_info"."end_time" IS '结束时间';
COMMENT ON COLUMN "next_console"."assistant_run_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."assistant_run_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."assistant_run_info" IS '个人助手运行指标表';

CREATE INDEX "assistant_id4"
ON "next_console"."assistant_run_info" USING btree ( "assistant_id" )
;
------------------------------------------------------------

CREATE TABLE "next_console"."assistant_kg_relation"
(
 "id" SERIAL PRIMARY KEY,
 "assistant_id" integer NOT NULL ,
 "kg_code" varchar(255) NOT NULL ,
 "rel_type" varchar(255) ,
 "rel_value" varchar(255) ,
 "rel_status" varchar(255) ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."assistant_kg_relation"."id" IS '关系id';
COMMENT ON COLUMN "next_console"."assistant_kg_relation"."assistant_id" IS '助手id';
COMMENT ON COLUMN "next_console"."assistant_kg_relation"."kg_code" IS '知识库id';
COMMENT ON COLUMN "next_console"."assistant_kg_relation"."rel_type" IS '关系类型';
COMMENT ON COLUMN "next_console"."assistant_kg_relation"."rel_value" IS '关系值';
COMMENT ON COLUMN "next_console"."assistant_kg_relation"."rel_status" IS '关系状态';
COMMENT ON COLUMN "next_console"."assistant_kg_relation"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."assistant_kg_relation"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."assistant_kg_relation" IS '个人助手与知识库关系表';

CREATE INDEX "assistant_id2"
ON "next_console"."assistant_kg_relation" USING btree ( "assistant_id" )
;

------------------------------------------------------------

CREATE TABLE "next_console"."assistant_instruction"
(
 "id" SERIAL PRIMARY KEY,
 "assistant_id" integer NOT NULL ,
 "instruction_name" varchar(255) NOT NULL ,
 "instruction_desc" text ,
 "instruction_system_prompt_template" text ,
 "instruction_status" varchar(255) NOT NULL ,
 "instruction_user_prompt_params_json_schema" json ,
 "instruction_result_json_schema" json ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "instruction_type" varchar(255) ,
 "instruction_user_prompt_template" text ,
 "instruction_result_template" text ,
 "user_id" integer ,
 "instruction_result_extract_format" varchar(255) ,
 "instruction_result_extract_separator" varchar(255) ,
 "instruction_result_extract_quote" varchar(255) ,
 "instruction_system_prompt_params_json_schema" json ,
 "instruction_result_extract_columns" json ,
 "instruction_history_length" integer DEFAULT 0 ,
 "instruction_temperature" double precision DEFAULT '0'::double precision ,
 "instruction_max_tokens" integer
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."assistant_instruction"."id" IS '指令id';
COMMENT ON COLUMN "next_console"."assistant_instruction"."assistant_id" IS '助手id';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_name" IS '指令名称';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_desc" IS '指令描述';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_system_prompt_template" IS '系统提示模板';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_status" IS '指令状态';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_user_prompt_params_json_schema" IS '用户提示参数json schema';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_result_json_schema" IS '指令结果json schema';
COMMENT ON COLUMN "next_console"."assistant_instruction"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."assistant_instruction"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_type" IS '指令类型';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_user_prompt_template" IS '指令入参内容';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_result_template" IS '指令结果内容';
COMMENT ON COLUMN "next_console"."assistant_instruction"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_result_extract_format" IS '结果提取格式';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_result_extract_separator" IS '结果提取分隔符';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_result_extract_quote" IS '结果提取引号';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_system_prompt_params_json_schema" IS '系统提示参数json schema';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_result_extract_columns" IS '结果列';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_history_length" IS '历史记录长度';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_temperature" IS '指令温度';
COMMENT ON COLUMN "next_console"."assistant_instruction"."instruction_max_tokens" IS '指令输出最大token';
COMMENT ON TABLE "next_console"."assistant_instruction" IS '助手指令表';

CREATE INDEX "assistant_id0"
ON "next_console"."assistant_instruction" USING btree ( "assistant_id" )
;
CREATE INDEX "assistant_instruction_user_info_FK1"
ON "next_console"."assistant_instruction" USING btree ( "user_id" )
;
CREATE TRIGGER update_assistant_instruction_trigger BEFORE UPDATE ON "next_console"."assistant_instruction" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


CREATE TABLE "next_console"."next_console_session_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "session_topic" varchar(255) NOT NULL ,
 "session_status" varchar(255) NOT NULL ,
 "session_remark" integer NOT NULL DEFAULT 0 ,
 "session_vis" boolean NOT NULL DEFAULT true ,
 "session_assistant_id" integer ,
 "create_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "session_favorite" boolean DEFAULT false,
 "session_like_cnt" integer DEFAULT 0 ,
 "session_dislike_cnt" integer DEFAULT 0 ,
 "session_update_cnt" integer DEFAULT 0 ,
 "session_share_cnt" integer DEFAULT 0 ,
 "session_shop_assistant_id" integer ,
 "session_task_id" varchar(255) ,
 "session_source" varchar(255) ,
 "session_task_type" varchar(255) ,
 "session_search_engine_switch" boolean DEFAULT false ,
 "session_search_engine_resource_type" varchar(255) ,
 "session_code" varchar(40) ,
 "session_search_engine_language_type" json ,
 "session_local_resource_switch" boolean ,
 "session_local_resource_use_all" boolean ,
 "session_attachment_image_switch" boolean ,
 "session_llm_code" varchar(100) ,
 "session_attachment_file_switch" boolean ,
 "session_attachment_webpage_switch" boolean ,
 "session_customer_score" double precision ,
 "session_customer_evaluation" text ,
 "session_evaluation_close" boolean ,
 "session_cancel_reason" text ,
 "session_task_params" json ,
 "session_task_params_schema" json
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."next_console_session_info"."id" IS '会话id';
COMMENT ON COLUMN "next_console"."next_console_session_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_topic" IS '会话主题';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_status" IS '会话状态';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_remark" IS '会话评价';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_vis" IS '会话可视化标志';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_assistant_id" IS '会话负责助手id';
COMMENT ON COLUMN "next_console"."next_console_session_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."next_console_session_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_favorite" IS '会话收藏';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_like_cnt" IS '点赞计数';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_dislike_cnt" IS '点踩计数';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_update_cnt" IS '纠正计数';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_share_cnt" IS '分享计数';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_shop_assistant_id" IS '最新商店助手id';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_task_id" IS '会话任务id';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_source" IS '会话来源';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_task_type" IS '会话任务类型';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_search_engine_switch" IS '会话是否启用搜索引擎';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_search_engine_resource_type" IS '搜索引擎资源类型';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_code" IS '会话对外编码';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_search_engine_language_type" IS '搜索引擎语言种类';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_local_resource_switch" IS '是否启用本地资源库';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_local_resource_use_all" IS '是否使用全部资源库';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_attachment_image_switch" IS '是否使用会话附件图片资源库';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_llm_code" IS '会话指定大模型驱动实例';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_attachment_file_switch" IS '是否使用会话附件文件资源库';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_attachment_webpage_switch" IS '是否使用会话附件网页资源库';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_customer_score" IS '会话客户评分';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_customer_evaluation" IS '会话客户评价';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_evaluation_close" IS '会话评价结束';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_cancel_reason" IS '会话取消原因';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_task_params" IS '会话任务参数';
COMMENT ON COLUMN "next_console"."next_console_session_info"."session_task_params_schema" IS '会话任务参数结构';
COMMENT ON TABLE "next_console"."next_console_session_info" IS '大模型会话信息';

CREATE INDEX "user_id27"
ON "next_console"."next_console_session_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_next_console_session_info_trigger BEFORE UPDATE ON "next_console"."next_console_session_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


------------------------------------------------------------


CREATE TABLE "next_console"."next_console_qa_info"
(
 "qa_id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "session_id" integer NOT NULL ,
 "qa_del" boolean NOT NULL default false,
 "qa_status" varchar(255) NOT NULL ,
 "qa_topic" text NOT NULL ,
 "qa_is_cut_off" boolean ,
 "create_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."next_console_qa_info"."qa_id" IS '问答对id';
COMMENT ON COLUMN "next_console"."next_console_qa_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."next_console_qa_info"."session_id" IS '会话id';
COMMENT ON COLUMN "next_console"."next_console_qa_info"."qa_del" IS '问答对删除标志';
COMMENT ON COLUMN "next_console"."next_console_qa_info"."qa_status" IS '问答对状态';
COMMENT ON COLUMN "next_console"."next_console_qa_info"."qa_topic" IS '问答对主题';
COMMENT ON COLUMN "next_console"."next_console_qa_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."next_console_qa_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."next_console_qa_info"."qa_is_cut_off" IS '问答中断标签';
COMMENT ON TABLE "next_console"."next_console_qa_info" IS '大模型问答信息';

CREATE INDEX "session_id25"
ON "next_console"."next_console_qa_info" USING btree ( "session_id" )
;
CREATE INDEX "user_id24"
ON "next_console"."next_console_qa_info" USING btree ( "user_id" )
;
CREATE TRIGGER update_next_console_qa_info_trigger BEFORE UPDATE ON "next_console"."next_console_qa_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


------------------------------------------------------------

CREATE TABLE "next_console"."next_console_llm_message"
(
 "msg_id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "session_id" integer NOT NULL ,
 "qa_id" integer ,
 "msg_llm_type" varchar(255) NOT NULL ,
 "msg_role" varchar(255) NOT NULL ,
 "msg_prompt" text NOT NULL ,
 "msg_format" varchar(255) NOT NULL ,
 "reasoning_content" text ,
 "msg_content" text NOT NULL ,
 "msg_token_used" integer NOT NULL ,
 "msg_time_used" double precision NOT NULL ,
 "msg_remark" integer NOT NULL DEFAULT 0 ,
 "msg_del" integer NOT NULL DEFAULT 1 ,
 "msg_version" integer NOT NULL DEFAULT 0 ,
 "msg_parent_id" integer ,
 "create_time" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "assistant_id" integer ,
 "msg_attachment_list" text ,
 "msg_inner_content" text ,
 "task_id" integer ,
 "msg_is_cut_off" boolean default false
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_id" IS '消息id';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."session_id" IS '会话id';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."qa_id" IS '问答id';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_llm_type" IS '调用模型类型';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_role" IS '角色';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_prompt" IS '提示';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_format" IS '格式';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."reasoning_content" IS '推理内容';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_content" IS '内容';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_token_used" IS 'token开销';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_time_used" IS '时间开销';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_remark" IS '评价';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_del" IS '可视化标志';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_version" IS 'msg版本';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_parent_id" IS '问题id';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."assistant_id" IS '助手id';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_attachment_list" IS '问题引用附件列表';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_inner_content" IS '真实内容';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."task_id" IS '任务id';
COMMENT ON COLUMN "next_console"."next_console_llm_message"."msg_is_cut_off" IS '消息是否被截断';
COMMENT ON TABLE "next_console"."next_console_llm_message" IS '大模型提问信息';

CREATE INDEX "msg_parent_id17"
ON "next_console"."next_console_llm_message" USING btree ( "msg_parent_id" )
;
CREATE INDEX "next_console_llm_message_assistant_info_FK19"
ON "next_console"."next_console_llm_message" USING btree ( "assistant_id" )
;
CREATE INDEX "qa_id22"
ON "next_console"."next_console_llm_message" USING btree ( "qa_id" )
;
CREATE INDEX "session_id20"
ON "next_console"."next_console_llm_message" USING btree ( "session_id" )
;
CREATE INDEX "user_id18"
ON "next_console"."next_console_llm_message" USING btree ( "user_id" )
;

CREATE TRIGGER update_next_console_llm_message_trigger BEFORE UPDATE ON "next_console"."next_console_llm_message" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


------------------------------------------------------------
CREATE TABLE "next_console"."next_console_recommend_question"
(
 "id" SERIAL PRIMARY KEY,
 "msg_id" integer ,
 "msg_content" text NOT NULL ,
 "recommend_question" text NOT NULL ,
 "is_click" integer NOT NULL ,
 "model" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."next_console_recommend_question"."id" IS '推荐记录id';
COMMENT ON COLUMN "next_console"."next_console_recommend_question"."msg_id" IS '问题id';
COMMENT ON COLUMN "next_console"."next_console_recommend_question"."msg_content" IS '问题内容';
COMMENT ON COLUMN "next_console"."next_console_recommend_question"."recommend_question" IS '推荐问题';
COMMENT ON COLUMN "next_console"."next_console_recommend_question"."is_click" IS '是否采用';
COMMENT ON COLUMN "next_console"."next_console_recommend_question"."model" IS '推荐问题模型';
COMMENT ON COLUMN "next_console"."next_console_recommend_question"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."next_console_recommend_question"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."next_console_recommend_question" IS '检索任务推荐问题表';

CREATE INDEX "next_search_recomm_llm_message_FK26"
ON "next_console"."next_console_recommend_question" USING btree ( "msg_id" )
;
CREATE TRIGGER update_next_console_recommend_question_trigger BEFORE UPDATE ON "next_console"."next_console_recommend_question" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


------------------------------------------------------------

CREATE TABLE "next_console"."session_attachment_relation"
(
 "id" SERIAL PRIMARY KEY,
 "session_id" integer NOT NULL ,
 "qa_id" integer ,
 "msg_id" integer ,
 "resource_id" integer NOT NULL ,
 "rel_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "attachment_source" varchar(100)
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."session_attachment_relation"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."session_attachment_relation"."session_id" IS '会话id';
COMMENT ON COLUMN "next_console"."session_attachment_relation"."qa_id" IS 'qa_id';
COMMENT ON COLUMN "next_console"."session_attachment_relation"."msg_id" IS '消息id';
COMMENT ON COLUMN "next_console"."session_attachment_relation"."resource_id" IS '资源id';
COMMENT ON COLUMN "next_console"."session_attachment_relation"."rel_status" IS '关系状态';
COMMENT ON COLUMN "next_console"."session_attachment_relation"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."session_attachment_relation"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."session_attachment_relation"."attachment_source" IS '附件来源';
COMMENT ON TABLE "next_console"."session_attachment_relation" IS '会话附件关系表';

CREATE INDEX "resource_id46"
ON "next_console"."session_attachment_relation" USING btree ( "resource_id" )
;
CREATE INDEX "session_id47"
ON "next_console"."session_attachment_relation" USING btree ( "session_id" )
;

CREATE TRIGGER update_session_attachment_relation_trigger BEFORE UPDATE ON "next_console"."session_attachment_relation" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."llm_instance_info"
(
 "id" SERIAL PRIMARY KEY,
 "llm_code" varchar(255) NOT NULL ,
 "llm_name" varchar(255) NOT NULL ,
 "user_id" integer NOT NULL ,
 "llm_api_secret_key" varchar(1000) NOT NULL ,
 "llm_api_access_key" varchar(1000) ,
 "llm_type" varchar(255) ,
 "llm_desc" text ,
 "llm_tags" json ,
 "llm_company" varchar(255) ,
 "llm_status" varchar(255) ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "llm_is_proxy" boolean ,
 "llm_base_url" text ,
 "llm_proxy_url" text ,
 "llm_source" varchar(255) ,
 "llm_is_public" boolean ,
 "frequency_penalty" double precision ,
 "max_tokens" integer ,
 "n" integer ,
 "presence_penalty" double precision ,
 "response_format" json ,
 "stop" json ,
 "stream" boolean ,
 "temperature" double precision ,
 "top_p" double precision ,
 "llm_icon" text ,
 "is_std_openai" boolean ,
 "support_vis" boolean ,
 "support_file" boolean ,
 "llm_label" varchar(255) ,
 "extra_body" json ,
 "extra_headers" json ,
 "use_default" boolean,
 "think_attr" json
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_code" IS '基模型实例编号';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_name" IS '基模型名称';
COMMENT ON COLUMN "next_console"."llm_instance_info"."user_id" IS '创建用户';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_api_secret_key" IS '基模型认证钥匙';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_api_access_key" IS '基模型访问钥匙';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_type" IS '基模型类型';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_desc" IS '基模型描述';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_tags" IS '基模型特征标签';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_company" IS '基模型厂商';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_status" IS '实例状态';
COMMENT ON COLUMN "next_console"."llm_instance_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."llm_instance_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_is_proxy" IS '基模型是否需要代理';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_base_url" IS '基模型访问地址';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_proxy_url" IS '基模型代理地址';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_source" IS '基模型来源';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_is_public" IS '基模型是否公开';
COMMENT ON COLUMN "next_console"."llm_instance_info"."frequency_penalty" IS '频率惩罚系数';
COMMENT ON COLUMN "next_console"."llm_instance_info"."max_tokens" IS '最大令牌数';
COMMENT ON COLUMN "next_console"."llm_instance_info"."n" IS '聊天完成选项个数';
COMMENT ON COLUMN "next_console"."llm_instance_info"."presence_penalty" IS '出现处罚系数';
COMMENT ON COLUMN "next_console"."llm_instance_info"."response_format" IS '响应格式';
COMMENT ON COLUMN "next_console"."llm_instance_info"."stop" IS '停止词';
COMMENT ON COLUMN "next_console"."llm_instance_info"."stream" IS '流式开关';
COMMENT ON COLUMN "next_console"."llm_instance_info"."temperature" IS '模型温度';
COMMENT ON COLUMN "next_console"."llm_instance_info"."top_p" IS '核采样系数';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_icon" IS '模型图标';
COMMENT ON COLUMN "next_console"."llm_instance_info"."is_std_openai" IS '是否支持openai-sdk';
COMMENT ON COLUMN "next_console"."llm_instance_info"."support_vis" IS '是否支持视觉';
COMMENT ON COLUMN "next_console"."llm_instance_info"."support_file" IS '是否支持文件';
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_label" IS '模型显示名称';
COMMENT ON COLUMN "next_console"."llm_instance_info"."extra_body" IS '额外请求头';
COMMENT ON COLUMN "next_console"."llm_instance_info"."extra_headers" IS '额外请求体';
COMMENT ON COLUMN "next_console"."llm_instance_info"."use_default" IS '使用默认参数';
COMMENT ON COLUMN "next_console"."llm_instance_info"."think_attr" IS '推理标签';
COMMENT ON TABLE "next_console"."llm_instance_info" IS '基模型实例信息表';

CREATE INDEX "user_id12"
ON "next_console"."llm_instance_info" USING btree ( "user_id" )
;

CREATE TRIGGER update_llm_instance_info_trigger BEFORE UPDATE ON "next_console"."llm_instance_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
    CREATE TABLE "next_console"."llm_supplier_info"
(
  id SERIAL PRIMARY KEY,
 "supplier_code" varchar(256) ,
 "supplier_name" varchar(256) ,
 "supplier_desc" text ,
 "supplier_icon" text ,
 "supplier_type" varchar(10) ,
 "supplier_website" text ,
 "supplier_models" json ,
 "supplier_status" varchar(10) ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "supplier_api_url" text
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."llm_supplier_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_code" IS '基模型厂商编号';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_name" IS '基模型厂商名称';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_desc" IS '基模型厂商描述';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_icon" IS '基模型厂商图标';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_type" IS '基模型厂商类型';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_website" IS '基模型厂商官网';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_models" IS '基模型厂商支持的模型列表';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_status" IS '基模型厂商状态';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_api_url" IS '厂商api地址';
COMMENT ON TABLE "next_console"."llm_supplier_info" IS '基模型厂商信息表';

-----------------------------------------------------------


CREATE TABLE "next_console"."llm_instance_authorize_info"
(
  id SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "model_id" integer NOT NULL ,
 "auth_colleague_id" integer ,
 "auth_friend_id" integer ,
 "auth_department_id" integer ,
 "auth_company_id" integer ,
 "auth_user_id" integer ,
 "auth_type" varchar(255) NOT NULL ,
 "auth_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."model_id" IS '模型id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_colleague_id" IS '被授权同事id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_friend_id" IS '被授权联系人id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_department_id" IS '被授权部门id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_company_id" IS '被授权公司id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_user_id" IS '被授权用户id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_type" IS '授权类型';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_status" IS '授权状态';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."llm_instance_authorize_info" IS '模型授权用户表';

CREATE INDEX "llm_instance_authorize_user_id49"
ON "next_console"."llm_instance_authorize_info" USING btree ( "user_id" )
;
CREATE INDEX "model_id50"
ON "next_console"."llm_instance_authorize_info" USING btree ( "model_id" )
;


------------------------------------------------------------
CREATE TABLE "next_console"."system_config_info"
(
 "id" SERIAL PRIMARY KEY,
 "config_key" varchar(255) NOT NULL ,
 "config_desc" varchar(255) NOT NULL ,
 "config_default_value" json NOT NULL ,
 "config_value" json NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "config_status" integer NOT NULL
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."system_config_info"."id" IS '参数id';
COMMENT ON COLUMN "next_console"."system_config_info"."config_desc" IS '配置描述';
COMMENT ON COLUMN "next_console"."system_config_info"."config_default_value" IS '配置默认值';
COMMENT ON COLUMN "next_console"."system_config_info"."config_value" IS '配置值';
COMMENT ON COLUMN "next_console"."system_config_info"."create_time" IS '配置创建时间';
COMMENT ON COLUMN "next_console"."system_config_info"."update_time" IS '配置更新时间';
COMMENT ON COLUMN "next_console"."system_config_info"."config_status" IS '配置状态';
COMMENT ON TABLE "next_console"."system_config_info" IS '系统配置表';
CREATE TRIGGER update_system_config_info_trigger BEFORE UPDATE ON "next_console"."system_config_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."support_area_info"
(
 "id" SERIAL PRIMARY KEY,
 "country" varchar(100) NOT NULL ,
 "iso_code_2" character(2) NOT NULL ,
 "iso_code_3" character(3) NOT NULL ,
 "phone_code" varchar(10) NOT NULL ,
 "continent" varchar(50) NOT NULL ,
 "province" varchar(50) NOT NULL ,
 "city" varchar(50) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "area_status" varchar(50) NOT NULL
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."support_area_info"."id" IS '主键，唯一标识每个国家记录';
COMMENT ON COLUMN "next_console"."support_area_info"."country" IS '国家的名称，如“United States”';
COMMENT ON COLUMN "next_console"."support_area_info"."iso_code_2" IS '国家的ISO 3166-1 alpha-2代码，如“US”';
COMMENT ON COLUMN "next_console"."support_area_info"."iso_code_3" IS '国家的ISO 3166-1 alpha-3代码，如“USA”';
COMMENT ON COLUMN "next_console"."support_area_info"."phone_code" IS '国家的国际电话区号，如“+1”';
COMMENT ON COLUMN "next_console"."support_area_info"."continent" IS '国家所属的大洲，如“North America”';
COMMENT ON COLUMN "next_console"."support_area_info"."province" IS '省';
COMMENT ON COLUMN "next_console"."support_area_info"."city" IS '市';
COMMENT ON COLUMN "next_console"."support_area_info"."create_time" IS '记录创建的时间戳';
COMMENT ON COLUMN "next_console"."support_area_info"."update_time" IS '记录最后更新的时间戳';
COMMENT ON COLUMN "next_console"."support_area_info"."area_status" IS '配置状态';
COMMENT ON TABLE "next_console"."support_area_info" IS '区域信息表';
CREATE TRIGGER update_support_area_info_trigger BEFORE UPDATE ON "next_console"."support_area_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();



------------------------------------------------------------
CREATE TABLE "next_console"."user_config_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "config_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "config_key" varchar(255) ,
 "config_value" json
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."user_config_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."user_config_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."user_config_info"."config_status" IS '配置状态';
COMMENT ON COLUMN "next_console"."user_config_info"."create_time" IS '配置创建时间';
COMMENT ON COLUMN "next_console"."user_config_info"."update_time" IS '配置更新时间';
COMMENT ON COLUMN "next_console"."user_config_info"."config_key" IS '配置键名';
COMMENT ON COLUMN "next_console"."user_config_info"."config_value" IS '配置值(JSON格式)';
COMMENT ON TABLE "next_console"."user_config_info" IS '用户配置表';
CREATE TRIGGER update_user_config_info_trigger BEFORE UPDATE ON "next_console"."user_config_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


CREATE TABLE "next_console"."zypricedatainfo" (
  id SERIAL PRIMARY KEY,
  start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  end_time TIMESTAMP NOT NULL DEFAULT '0001-01-01 00:00:00',
  product_name VARCHAR(255) NOT NULL,
  product_level VARCHAR(255) NOT NULL,
  product_specification VARCHAR(255) NOT NULL,
  wholesale_price DOUBLE PRECISION NOT NULL,
  recommended_retail_price DOUBLE PRECISION NOT NULL,
  city VARCHAR(255) NOT NULL,
  purchase_price DOUBLE PRECISION,
  sale_price DOUBLE PRECISION,
  status VARCHAR(255) NOT NULL DEFAULT '正常',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;

COMMENT ON TABLE "next_console"."zypricedatainfo"  IS 'ZY产品价格数据信息';
COMMENT ON COLUMN "next_console"."zypricedatainfo".id IS '自增id';
COMMENT ON COLUMN "next_console".zypricedatainfo.start_time IS '数据统计开始时间';
COMMENT ON COLUMN "next_console".zypricedatainfo.end_time IS '数据统计完成时间';
COMMENT ON COLUMN "next_console".zypricedatainfo.product_name IS '产品名称';
COMMENT ON COLUMN "next_console".zypricedatainfo.product_level IS '产品等级';
COMMENT ON COLUMN "next_console".zypricedatainfo.product_specification IS '产品规格';
COMMENT ON COLUMN "next_console".zypricedatainfo.wholesale_price IS '批发价格';
COMMENT ON COLUMN "next_console".zypricedatainfo.recommended_retail_price IS '建议零售价';
COMMENT ON COLUMN "next_console".zypricedatainfo.city IS '城市';
COMMENT ON COLUMN "next_console".zypricedatainfo.purchase_price IS '进货价';
COMMENT ON COLUMN "next_console".zypricedatainfo.sale_price IS '出货价';
COMMENT ON COLUMN "next_console".zypricedatainfo.status IS '数据状态';
COMMENT ON COLUMN "next_console".zypricedatainfo.create_time IS '创建时间';
COMMENT ON COLUMN "next_console".zypricedatainfo.update_time IS '更新时间';
CREATE TRIGGER update_zypricedatainfo_trigger BEFORE UPDATE ON "next_console"."zypricedatainfo" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
---------------------------------------------------------------------------------------
CREATE TABLE "next_console".zyinventorydatainfo (
  id SERIAL PRIMARY KEY,
  start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  end_time TIMESTAMP NOT NULL DEFAULT '0001-01-01 00:00:00',
  product_level VARCHAR(255) NOT NULL,
  product_specification VARCHAR(255) NOT NULL,
  product_inventory DOUBLE PRECISION,
  product_remain_days INTEGER,
  city VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL DEFAULT '正常',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


COMMENT ON TABLE "next_console".zyinventorydatainfo IS 'ZY产品库存数据信息';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.id IS '自增id';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.start_time IS '数据开始时间';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.end_time IS '数据结束时间';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.product_level IS '产品等级';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.product_specification IS '产品规格';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.product_inventory IS '产品库存';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.product_remain_days IS '产品库存可销天数';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.city IS '城市';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.status IS '数据状态';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.create_time IS '创建时间';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.update_time IS '更新时间';

CREATE TRIGGER update_zyinventorydatainfo_trigger BEFORE UPDATE ON "next_console"."zyinventorydatainfo" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


---------------------------------------------------------------------------------------
CREATE TABLE "next_console"."zypurchasedatainfo" (
  id SERIAL PRIMARY KEY,
  start_time VARCHAR(255) NOT NULL,
  end_time VARCHAR(255) NOT NULL,
  product_level VARCHAR(255) NOT NULL,
  product_specification VARCHAR(255) NOT NULL,
  city VARCHAR(255) NOT NULL,
  customer_level VARCHAR(255) NOT NULL,
  avg_purchase DOUBLE PRECISION,
  avg_purchase_all DOUBLE PRECISION,
  status VARCHAR(255) NOT NULL DEFAULT '正常',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add table comment
COMMENT ON TABLE "next_console".zypurchasedatainfo IS '产品采购数据信息';

-- Add column comments
COMMENT ON COLUMN "next_console".zypurchasedatainfo.id IS '自增id';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.start_time IS '开始时间';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.end_time IS '结束时间';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.product_level IS '产品等级';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.product_specification IS '产品规格';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.city IS '城市';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.customer_level IS '客户等级';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.avg_purchase IS '户均投放条数';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.avg_purchase_all IS '户均进货条数';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.status IS '状态';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.create_time IS '创建时间';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.update_time IS '更新时间';
CREATE TRIGGER update_zypurchasedatainfo_trigger BEFORE UPDATE ON "next_console"."zypurchasedatainfo" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


CREATE TABLE "next_console"."app_meta_info"
(
 "id" SERIAL PRIMARY KEY,
 "app_code" varchar(255) NOT NULL ,
 "user_id" integer NOT NULL ,
 "app_name" text NOT NULL ,
 "app_desc" text NOT NULL ,
 "app_icon" text NOT NULL ,
 "app_type" varchar(255) NOT NULL ,
 "app_status" varchar(255) NOT NULL ,
 "app_default_assistant" integer ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "environment" varchar(10) ,
 "version" integer ,
 "app_source" varchar(255) ,
 "app_agent_api_url" varchar(255) ,
 "app_agent_api_key" varchar(255) ,
 "app_config" json
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."app_meta_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_code" IS '应用编码';
COMMENT ON COLUMN "next_console"."app_meta_info"."user_id" IS '作者id';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_name" IS '应用名称';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_desc" IS '应用描述';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_icon" IS '应用图标';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_type" IS '应用类型';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_status" IS '应用状态';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_default_assistant" IS '应用默认助手';
COMMENT ON COLUMN "next_console"."app_meta_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."app_meta_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."app_meta_info"."environment" IS '应用环境';
COMMENT ON COLUMN "next_console"."app_meta_info"."version" IS '应用版本';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_source" IS '应用来源';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_agent_api_url" IS 'ai应用api接口url';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_agent_api_key" IS 'ai应用api接口key';
COMMENT ON COLUMN "next_console"."app_meta_info"."app_config" IS 'ai应用配置';
COMMENT ON TABLE "next_console"."app_meta_info" IS 'ai应用信息表';
CREATE TRIGGER update_app_meta_info_trigger BEFORE UPDATE ON "next_console"."app_meta_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."app_access_info"
(
 "id" SERIAL PRIMARY KEY,
 "app_code" varchar(255) NOT NULL ,
 "user_code" varchar(255) ,
 "access_type" varchar(255) NOT NULL ,
 "access_name" varchar(255) NOT NULL ,
 "access_desc" varchar(255) ,
 "access_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "user_id" integer ,
 "department_id" integer ,
 "company_id" integer
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."app_access_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."app_access_info"."app_code" IS '应用编号';
COMMENT ON COLUMN "next_console"."app_access_info"."user_code" IS '用户编号';
COMMENT ON COLUMN "next_console"."app_access_info"."access_type" IS '权限类型';
COMMENT ON COLUMN "next_console"."app_access_info"."access_name" IS '权限名称';
COMMENT ON COLUMN "next_console"."app_access_info"."access_desc" IS '权限描述';
COMMENT ON COLUMN "next_console"."app_access_info"."access_status" IS '权限状态';
COMMENT ON COLUMN "next_console"."app_access_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."app_access_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."app_access_info"."user_id" IS '用户ID';
COMMENT ON COLUMN "next_console"."app_access_info"."department_id" IS '部门ID';
COMMENT ON COLUMN "next_console"."app_access_info"."company_id" IS '公司ID';
COMMENT ON TABLE "next_console"."app_access_info" IS 'ai应用授权表';
CREATE TRIGGER update_app_access_info_trigger BEFORE UPDATE ON "next_console"."app_access_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."workflow_meta_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "workflow_code" varchar(255) NOT NULL ,
 "workflow_name" varchar(255) NOT NULL ,
 "workflow_desc" text NOT NULL ,
 "workflow_icon" text NOT NULL ,
 "workflow_schema" json NOT NULL ,
 "workflow_edit_schema" json ,
 "workflow_is_main" boolean ,
 "workflow_status" varchar(255) NOT NULL ,
 "environment" varchar(100) ,
 "version" integer ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."workflow_meta_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."user_id" IS '作者id';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."workflow_code" IS '工作流编码';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."workflow_name" IS '工作流名称';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."workflow_desc" IS '工作流描述';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."workflow_icon" IS '工作流图标';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."workflow_schema" IS '工作流结构';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."workflow_is_main" IS '为主流程';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."workflow_status" IS '工作流状态';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."environment" IS '工作流运行环境';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."version" IS '工作流版本号';
COMMENT ON COLUMN "next_console"."workflow_meta_info"."workflow_edit_schema" IS '工作流编辑态结构';
COMMENT ON TABLE "next_console"."workflow_meta_info" IS '工作流元信息';
CREATE TRIGGER update_workflow_meta_info_trigger BEFORE UPDATE ON "next_console"."workflow_meta_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."app_workflow_relation"
(
 "id"  SERIAL PRIMARY KEY,
 "rel_type" varchar(255) NOT NULL ,
 "rel_desc" varchar(255) NOT NULL ,
 "rel_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "app_code" varchar(255) ,
 "workflow_code" varchar(255) ,
 "environment" varchar(100) ,
 "version" integer
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."app_workflow_relation"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."app_workflow_relation"."rel_type" IS '关系类型';
COMMENT ON COLUMN "next_console"."app_workflow_relation"."rel_desc" IS '关系描述';
COMMENT ON COLUMN "next_console"."app_workflow_relation"."rel_status" IS '关系状态';
COMMENT ON COLUMN "next_console"."app_workflow_relation"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."app_workflow_relation"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."app_workflow_relation"."app_code" IS '应用编号';
COMMENT ON COLUMN "next_console"."app_workflow_relation"."workflow_code" IS '工作流编号';
COMMENT ON COLUMN "next_console"."app_workflow_relation"."environment" IS '环境';
COMMENT ON COLUMN "next_console"."app_workflow_relation"."version" IS '版本';
COMMENT ON TABLE "next_console"."app_workflow_relation" IS '应用工作流关系表';
CREATE TRIGGER update_app_workflow_relation_trigger BEFORE UPDATE ON "next_console"."app_workflow_relation" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."workflow_node_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "workflow_id" integer NOT NULL ,
 "node_code" varchar(255) NOT NULL ,
 "node_type" varchar(255) NOT NULL ,
 "node_icon" text NOT NULL ,
 "node_name" varchar(255) NOT NULL ,
 "node_desc" text NOT NULL ,
 "node_run_model_config" json NOT NULL ,
 "node_llm_code" varchar(255) NOT NULL ,
 "node_llm_params" json ,
 "node_llm_system_prompt_template" text ,
 "node_llm_user_prompt_template" text ,
 "node_result_format" varchar(255) NOT NULL ,
 "node_result_params_json_schema" json ,
 "node_result_template" text ,
 "node_retry_max" integer ,
 "node_retry_duration" integer ,
 "node_retry_model" integer ,
 "node_failed_solution" varchar(255) NOT NULL ,
 "node_failed_template" text ,
 "node_status" varchar(255) NOT NULL ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "node_session_memory_size" integer DEFAULT 4 ,
 "node_deep_memory" boolean ,
 "node_agent_nickname" varchar(100) ,
 "node_agent_avatar" text ,
 "node_agent_desc" text ,
 "node_agent_prologue" text ,
 "node_agent_preset_question" json ,
 "node_agent_tools" json ,
 "node_input_params_json_schema" json ,
 "node_result_extract_separator" varchar(100) ,
 "node_result_extract_quote" varchar(100) ,
 "node_result_extract_columns" json ,
 "node_timeout" integer DEFAULT 600 ,
 "environment" varchar(100) ,
 "version" integer ,
 "node_tool_api_url" text ,
 "node_tool_http_method" text ,
 "node_tool_http_header" json ,
 "node_tool_http_params" json ,
 "node_tool_http_body" json ,
 "node_tool_http_body_type" varchar(100) ,
 "node_rag_resources" json ,
 "node_rag_query_template" text ,
 "node_rag_recall_config" json ,
 "node_rag_rerank_config" json ,
 "node_rag_web_search_config" json ,
 "node_rag_ref_show" boolean ,
 "node_enable_message" boolean ,
 "node_message_schema" json ,
 "node_message_schema_type" varchar(100) ,
 "node_file_reader_config" json,
 "node_file_splitter_config" json ,
 "node_sub_workflow_config" json
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."workflow_node_info"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."workflow_node_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."workflow_node_info"."workflow_id" IS 'workflow_id';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_code" IS '节点编号';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_type" IS '节点类型';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_icon" IS '节点图标';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_name" IS '节点名称';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_desc" IS '节点描述';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_run_model_config" IS '节点运行模式';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_llm_code" IS '节点大模型编号';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_llm_params" IS '节点大模型参数';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_llm_system_prompt_template" IS '系统提示词模板';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_llm_user_prompt_template" IS '用户提示词模板';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_result_format" IS '节点输出数据格式';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_result_params_json_schema" IS '节点变量结构';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_result_template" IS '节点输出模板';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_retry_max" IS '节点最大重试次数';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_retry_duration" IS '节点重试间隔';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_retry_model" IS '节点重试模式：1.重试后退出，2，重试后异常处理';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_failed_solution" IS '节点失败策略';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_failed_template" IS '节点失败模板';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_status" IS '节点状态';
COMMENT ON COLUMN "next_console"."workflow_node_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."workflow_node_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_session_memory_size" IS '会话记忆长度';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_deep_memory" IS '深度记忆开关';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_agent_nickname" IS '助手昵称';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_agent_avatar" IS '助手头像';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_agent_desc" IS '助手描述';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_agent_prologue" IS '助手开场白';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_agent_preset_question" IS '助手预置问题';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_agent_tools" IS '助手工具配置';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_input_params_json_schema" IS '节点输入变量结构';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_result_extract_separator" IS '结果提取分隔符';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_result_extract_quote" IS '结果提取引号';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_result_extract_columns" IS '结果列名';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_timeout" IS '节点超时';
COMMENT ON COLUMN "next_console"."workflow_node_info"."environment" IS '环境';
COMMENT ON COLUMN "next_console"."workflow_node_info"."version" IS '版本';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_tool_api_url" IS 'api-url';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_tool_http_method" IS '请求方法';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_tool_http_header" IS '请求头定义';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_tool_http_params" IS '请求参数定义';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_tool_http_body" IS '请求体定义';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_tool_http_body_type" IS '节点请求体类型';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_rag_resources" IS '知识清单';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_rag_query_template" IS '查询知识模板';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_rag_recall_config" IS 'rag召回配置';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_rag_rerank_config" IS 'rag重排序配置';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_rag_web_search_config" IS 'rag联网搜索配置';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_rag_ref_show" IS '展示参考资料';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_enable_message" IS '节点允许输出消息';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_message_schema" IS '节点消息结构';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_message_schema_type" IS '节点消息结构类型';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_file_reader_config" IS '文档阅读器配置';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_file_reader_config" IS '文档阅读器配置';
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_file_splitter_config" IS '文本切分配置';
COMMENT ON TABLE "next_console"."workflow_node_info" IS '工作流节点信息表';

CREATE INDEX "user_id89"
ON "next_console"."workflow_node_info" USING btree ( "user_id" )
;
CREATE INDEX "workflow_id88"
ON "next_console"."workflow_node_info" USING btree ( "workflow_id" )
;
CREATE TRIGGER update_workflow_node_info_trigger BEFORE UPDATE ON "next_console"."workflow_node_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


------------------------------------------------------------
CREATE TABLE "next_console"."workflow_node_instance"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "workflow_id" integer NOT NULL ,
 "workflow_node_id" integer NOT NULL ,
 "workflow_node_type" varchar(255) NOT NULL ,
 "workflow_node_icon" text NOT NULL ,
 "workflow_node_name" varchar(255) NOT NULL ,
 "workflow_node_desc" text NOT NULL ,
 "workflow_node_run_model_config" json NOT NULL ,
 "workflow_node_llm_code" varchar(255) NOT NULL ,
 "workflow_node_llm_params" json NOT NULL ,
 "workflow_node_ipjs" json NOT NULL ,
 "workflow_node_llm_spt" text NOT NULL ,
 "workflow_node_llm_upt" text NOT NULL ,
 "workflow_node_result_format" text NOT NULL ,
 "workflow_node_rpjs" json NOT NULL ,
 "workflow_node_result_template" text NOT NULL ,
 "workflow_node_retry_max" integer NOT NULL ,
 "workflow_node_retry_duration" integer NOT NULL ,
 "workflow_node_retry_model" integer NOT NULL ,
 "workflow_node_failed_solution" varchar(255) NOT NULL ,
 "workflow_node_failed_template" text NOT NULL ,
 "node_session_memory_size" integer NOT NULL ,
 "node_deep_memory" boolean NOT NULL ,
 "node_agent_tools" json NOT NULL ,
 "session_id" integer NOT NULL ,
 "qa_id" integer NOT NULL ,
 "msg_id" integer NOT NULL ,
 "task_status" varchar(255) NOT NULL ,
 "task_precondition" json NOT NULL ,
 "task_downstream" json NOT NULL ,
 "task_params" json NOT NULL ,
 "task_prompt" json NOT NULL ,
 "task_retry_cnt" integer NOT NULL ,
 "task_result" text NOT NULL ,
 "task_result_summary" varchar(255) NOT NULL ,
 "task_token_used" integer ,
 "task_trace_log" text NOT NULL ,
 "begin_time" timestamp with time zone ,
 "end_time" timestamp with time zone ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "workflow_node_timeout" integer DEFAULT 600 ,
 "workflow_node_code" varchar(100) ,
 "workflow_node_tool_http_method" text ,
 "workflow_node_tool_http_header" json ,
 "workflow_node_tool_http_params" json ,
 "workflow_node_tool_http_body" json ,
 "workflow_node_tool_api_url" text ,
 "workflow_node_tool_http_body_type" varchar(100) ,
 "workflow_node_rag_resources" json ,
 "workflow_node_rag_query_template" text ,
 "workflow_node_rag_ref_show" boolean ,
 "workflow_node_rag_recall_config" json ,
 "workflow_node_rag_rerank_config" json ,
 "workflow_node_rag_web_search_config" json ,
 "workflow_node_enable_message" boolean ,
 "workflow_node_message_schema_type" varchar(100) ,
 "workflow_node_message_schema" json ,
 "workflow_node_file_reader_config" json ,
 "workflow_node_file_splitter_config" json ,
 "workflow_node_sub_workflow_config" json
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."workflow_node_instance"."id" IS 'ID 编号';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_id" IS '工作流id';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_id" IS '工作节点id';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_type" IS '工作节点类型';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_icon" IS '工作节点图标';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_name" IS '工作节点名称';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_desc" IS '工作节点描述';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_run_model_config" IS '节点运行模式';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_llm_code" IS '节点模型编号';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_llm_params" IS '节点模型参数';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_ipjs" IS '节点输入变量结构';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_llm_spt" IS '系统提示词模板';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_llm_upt" IS '用户提示词模板';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_result_format" IS '输出数据格式';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_rpjs" IS '输出变量结构';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_result_template" IS '节点输出模板';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_retry_max" IS '节点最大重试次数';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_retry_duration" IS '节点重试间隔';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_retry_model" IS '节点重试策略';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_failed_solution" IS '节点失败策略';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_failed_template" IS '节点失败模板';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."node_session_memory_size" IS '会话记忆长度';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."node_deep_memory" IS '深度记忆开关';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."node_agent_tools" IS '助手工具配置';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."session_id" IS '会话id';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."qa_id" IS '问答id';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."msg_id" IS '消息id';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_status" IS '任务状态';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_precondition" IS '任务执行前置条件';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_downstream" IS '任务下游';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_params" IS '任务输入参数';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_prompt" IS '任务提示词';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_retry_cnt" IS '任务重试次数';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_result" IS '任务结果';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_result_summary" IS '任务结果总结';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_token_used" IS '任务使用的token数';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."task_trace_log" IS '任务异常日志';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."begin_time" IS '任务开始时间';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."end_time" IS '任务结束时间';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_timeout" IS '节点运行超时';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_code" IS '工作流节点编号';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_tool_http_method" IS '请求方法';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_tool_http_header" IS '请求头定义';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_tool_http_params" IS '请求参数定义';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_tool_http_body" IS '请求体定义';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_tool_api_url" IS 'api-url';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_tool_http_body_type" IS '请求体类型';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_rag_resources" IS 'RAG资源清单';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_rag_query_template" IS 'RAG查询模板';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_rag_ref_show" IS 'RAG显示参考文献';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_rag_recall_config" IS 'RAG召回配置';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_rag_rerank_config" IS 'RAG重排序配置';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_rag_web_search_config" IS 'RAG联网搜索配置';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_enable_message" IS '节点消息开关';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_message_schema_type" IS '节点消息结构类型';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_message_schema" IS '节点消息结构';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_file_reader_config" IS '文档阅读器配置';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_file_reader_config" IS '文档阅读器配置';
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_file_splitter_config" IS '文档切分配置';
COMMENT ON TABLE "next_console"."workflow_node_instance" IS '工作流节点实例';


CREATE TRIGGER update_workflow_node_instance_trigger BEFORE UPDATE ON "next_console"."workflow_node_instance" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."workflow_task_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "session_id" integer NOT NULL ,
 "qa_id" integer NOT NULL ,
 "msg_id" integer NOT NULL ,
 "task_type" varchar(255) NOT NULL ,
 "task_status" varchar(255) NOT NULL ,
 "task_assistant_id" integer NOT NULL ,
 "task_model_name" varchar(255) NOT NULL ,
 "task_assistant_instruction" text NOT NULL ,
 "task_params" json NOT NULL ,
 "task_prompt" JSON NOT NULL ,
 "task_result" text ,
 "task_precondition" text ,
 "begin_time" timestamp with time zone ,
 "end_time" timestamp with time zone ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;
COMMENT ON COLUMN "next_console"."workflow_task_info"."id" IS '自增id';
COMMENT ON COLUMN "next_console"."workflow_task_info"."user_id" IS '用户id';
COMMENT ON COLUMN "next_console"."workflow_task_info"."session_id" IS '会话id';
COMMENT ON COLUMN "next_console"."workflow_task_info"."qa_id" IS '问答id';
COMMENT ON COLUMN "next_console"."workflow_task_info"."msg_id" IS '消息id';
COMMENT ON COLUMN "next_console"."workflow_task_info"."task_type" IS '任务类型';
COMMENT ON COLUMN "next_console"."workflow_task_info"."task_status" IS '任务状态';
COMMENT ON COLUMN "next_console"."workflow_task_info"."task_assistant_id" IS '任务助手';
COMMENT ON COLUMN "next_console"."workflow_task_info"."task_model_name" IS '任务助手模型';
COMMENT ON COLUMN "next_console"."workflow_task_info"."task_assistant_instruction" IS '任务助手指令';
COMMENT ON COLUMN "next_console"."workflow_task_info"."task_params" IS '任务输入参数';
COMMENT ON COLUMN "next_console"."workflow_task_info"."task_prompt" IS '任务提示词';
COMMENT ON COLUMN "next_console"."workflow_task_info"."task_result" IS '任务结果';
COMMENT ON COLUMN "next_console"."workflow_task_info"."task_precondition" IS '任务执行前置条件';
COMMENT ON COLUMN "next_console"."workflow_task_info"."begin_time" IS '任务开始时间';
COMMENT ON COLUMN "next_console"."workflow_task_info"."end_time" IS '任务结束时间';
COMMENT ON COLUMN "next_console"."workflow_task_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."workflow_task_info"."update_time" IS '更新时间';
COMMENT ON TABLE "next_console"."workflow_task_info" IS '工作流任务信息表';

CREATE INDEX "msg_id93"
ON "next_console"."workflow_task_info" USING btree ( "msg_id" )
;
CREATE INDEX "qa_id94"
ON "next_console"."workflow_task_info" USING btree ( "qa_id" )
;
CREATE INDEX "session_id92"
ON "next_console"."workflow_task_info" USING btree ( "session_id" )
;
CREATE INDEX "task_assistant_id91"
ON "next_console"."workflow_task_info" USING btree ( "task_assistant_id" )
;
CREATE INDEX "user_id90"
ON "next_console"."workflow_task_info" USING btree ( "user_id" )
;

CREATE TRIGGER update_workflow_task_info_trigger BEFORE UPDATE ON "next_console"."workflow_task_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


CREATE TABLE "next_console"."app_publish_record" (
  id SERIAL PRIMARY KEY,
  app_code VARCHAR(255) NOT NULL,
  workflow_code VARCHAR(255),
  publish_code VARCHAR(255) NOT NULL,
  user_id INTEGER NOT NULL,
  publish_name VARCHAR(255) NOT NULL,
  publish_desc TEXT NOT NULL,
  publish_config json,
  publish_status VARCHAR(255),
  publish_version INTEGER,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE "next_console"."app_publish_record" IS '应用发布记录';
COMMENT ON COLUMN "next_console"."app_publish_record".id IS '自增id';
COMMENT ON COLUMN "next_console"."app_publish_record".app_code IS '应用编号';
COMMENT ON COLUMN "next_console"."app_publish_record".workflow_code IS '工作流编号';
COMMENT ON COLUMN "next_console"."app_publish_record".publish_code IS '发布编号';
COMMENT ON COLUMN "next_console"."app_publish_record".user_id IS '用户id';
COMMENT ON COLUMN "next_console"."app_publish_record".publish_name IS '发布名称';
COMMENT ON COLUMN "next_console"."app_publish_record".publish_desc IS '发布描述';
COMMENT ON COLUMN "next_console"."app_publish_record".publish_config IS '发布配置';
COMMENT ON COLUMN "next_console"."app_publish_record".publish_status IS '发布状态';
COMMENT ON COLUMN "next_console"."app_publish_record".publish_version IS '发布版本';
COMMENT ON COLUMN "next_console"."app_publish_record".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."app_publish_record".update_time IS '更新时间';
CREATE TRIGGER update_app_publish_record_trigger BEFORE UPDATE ON "next_console"."app_publish_record" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

CREATE TABLE "next_console"."edith_client_meta_info" (
  id SERIAL PRIMARY KEY,
  client_name VARCHAR(255) NOT NULL,
  client_desc VARCHAR(255) NOT NULL,
  client_icon TEXT NOT NULL,
  support_os TEXT,
  client_version VARCHAR(255) NOT NULL,
  client_sub_version VARCHAR(255) NOT NULL,
  client_raw_path TEXT NOT NULL,
  client_download_path TEXT NOT NULL,
  client_status VARCHAR(255) NOT NULL,
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE "next_console"."edith_client_meta_info" IS 'edith版本信息';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".id IS '自增id';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_name IS '客户端名称';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_desc IS '客户端描述';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_icon IS '客户端图标';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".support_os IS '支持操作系统';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_version IS '版本号';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_sub_version IS '子版本号';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_raw_path IS '客户端原始路径';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_download_path IS '客户端下载路径';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_status IS '客户端状态';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".update_time IS '更新时间';

CREATE TRIGGER update_edith_client_meta_info_trigger BEFORE UPDATE ON "next_console"."edith_client_meta_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."edith_report_info" (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  edith_task_id INTEGER NOT NULL,
  report_code VARCHAR(255) NOT NULL,
  report_name TEXT NOT NULL,
  report_desc TEXT,
  report_type VARCHAR(255) NOT NULL,
  report_data_dir TEXT NOT NULL,
  report_generate_config VARCHAR(255) NOT NULL,
  celery_id VARCHAR(255),
  task_trace TEXT,
  report_path TEXT,
  report_download_url TEXT,
  report_status VARCHAR(255) NOT NULL,
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  run_model VARCHAR(20)
);

-- 表注释
COMMENT ON TABLE "next_console"."edith_report_info" IS 'edith巡检报告信息表';

-- 列注释
COMMENT ON COLUMN "next_console"."edith_report_info".id IS '自增id';
COMMENT ON COLUMN "next_console"."edith_report_info".user_id IS '用户id';
COMMENT ON COLUMN "next_console"."edith_report_info".edith_task_id IS 'edith巡检任务id';
COMMENT ON COLUMN "next_console"."edith_report_info".report_code IS '报告编号';
COMMENT ON COLUMN "next_console"."edith_report_info".report_name IS '报告名称';
COMMENT ON COLUMN "next_console"."edith_report_info".report_desc IS '报告描述';
COMMENT ON COLUMN "next_console"."edith_report_info".report_type IS '报告类型';
COMMENT ON COLUMN "next_console"."edith_report_info".report_data_dir IS '报告数据目录';
COMMENT ON COLUMN "next_console"."edith_report_info".report_generate_config IS '报告生成配置';
COMMENT ON COLUMN "next_console"."edith_report_info".celery_id IS '任务id';
COMMENT ON COLUMN "next_console"."edith_report_info".task_trace IS '任务日志';
COMMENT ON COLUMN "next_console"."edith_report_info".report_path IS '报告路径';
COMMENT ON COLUMN "next_console"."edith_report_info".report_download_url IS '报告下载地址';
COMMENT ON COLUMN "next_console"."edith_report_info".report_status IS '报告状态';
COMMENT ON COLUMN "next_console"."edith_report_info".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."edith_report_info".update_time IS '更新时间';
COMMENT ON COLUMN "next_console"."edith_report_info".run_model IS '运行模式';

CREATE TRIGGER update_edith_report_info_trigger BEFORE UPDATE ON "next_console"."edith_report_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."edith_task_info" (
  id SERIAL PRIMARY KEY,
  task_code VARCHAR(255) NOT NULL,
  session_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  task_name VARCHAR(255) NOT NULL,
  task_desc VARCHAR(255) NOT NULL,
  task_type VARCHAR(255) NOT NULL,
  task_stage VARCHAR(255) NOT NULL,
  task_data_dir TEXT NOT NULL,
  edith_client_id INTEGER,
  task_parent_id INTEGER,
  task_status VARCHAR(255) NOT NULL,
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 表注释
COMMENT ON TABLE "next_console"."edith_task_info" IS 'edith巡检任务信息表';

-- 列注释
COMMENT ON COLUMN "next_console"."edith_task_info".id IS '自增id';
COMMENT ON COLUMN "next_console"."edith_task_info".task_code IS '巡检任务编号';
COMMENT ON COLUMN "next_console"."edith_task_info".session_id IS '会话id';
COMMENT ON COLUMN "next_console"."edith_task_info".user_id IS '用户id';
COMMENT ON COLUMN "next_console"."edith_task_info".task_name IS '任务名称';
COMMENT ON COLUMN "next_console"."edith_task_info".task_desc IS '任务描述';
COMMENT ON COLUMN "next_console"."edith_task_info".task_type IS '任务类型';
COMMENT ON COLUMN "next_console"."edith_task_info".task_stage IS '任务阶段';
COMMENT ON COLUMN "next_console"."edith_task_info".task_data_dir IS '任务上传数据目录';
COMMENT ON COLUMN "next_console"."edith_task_info".edith_client_id IS 'edith客户端id';
COMMENT ON COLUMN "next_console"."edith_task_info".task_parent_id IS '父任务id';
COMMENT ON COLUMN "next_console"."edith_task_info".task_status IS '任务状态';
COMMENT ON COLUMN "next_console"."edith_task_info".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."edith_task_info".update_time IS '更新时间';

CREATE TRIGGER update_edith_task_info_trigger BEFORE UPDATE ON "next_console"."edith_task_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
------------------------------------------------------------


INSERT INTO "next_console"."role_info" ("role_id","role_name","role_desc","create_time","update_time","status") VALUES ('1','super_admin','超级管理员','2025-07-17 16:47:55.630237+08','2025-07-17 16:47:55.630237+08',1);
INSERT INTO "next_console"."role_info" ("role_id","role_name","role_desc","create_time","update_time","status") VALUES ('2','admin','系统管理员','2025-07-17 16:47:55.67634+08','2025-07-17 16:47:55.67634+08',1);
INSERT INTO "next_console"."role_info" ("role_id","role_name","role_desc","create_time","update_time","status") VALUES ('3','visitor','游客','2025-07-17 16:47:55.721003+08','2025-07-17 16:47:55.721003+08',1);
INSERT INTO "next_console"."role_info" ("role_id","role_name","role_desc","create_time","update_time","status") VALUES ('4','user','普通用户','2025-07-17 16:47:55.766311+08','2025-07-17 16:47:55.766311+08',1);
INSERT INTO "next_console"."role_info" ("role_id","role_name","role_desc","create_time","update_time","status") VALUES ('5','next_console_admin','NextConsole管理员','2025-07-17 16:47:55.810655+08','2025-07-17 16:47:55.810655+08',1);
INSERT INTO "next_console"."role_info" ("role_id","role_name","role_desc","create_time","update_time","status") VALUES ('6','next_console_reader_admin','NextConsole只读管理员','2025-07-17 16:47:55.854884+08','2025-07-17 16:47:55.854884+08',1);
INSERT INTO "next_console"."user_info" ("user_id","user_name","user_nick_name","user_nick_name_py","user_password","user_email","user_phone","user_gender","user_age","user_avatar","user_department","create_time","update_time","last_login_time","user_status","user_source","user_code","user_wx_nickname","user_wx_avatar","user_wx_openid","user_wx_union_id","user_position","user_company","user_account_type","user_name_py","user_expire_time","user_area","user_resource_base_path","user_company_id","user_department_id","user_resource_limit","user_accept_contact","user_invite_code") VALUES ('1','next_console','管理员','GLY','0cc5042d06a578e5eb453084a75aa2659aaf8564b87b26acec8cd3d0fd5c15ce','admin@nextconsole.cn','','男',28,'','产品研发部','2023-12-12 17:06:28+08','2025-04-20 09:36:34+08','2025-04-20 09:36:34+08',1,'admin','595793bd-477b-4277-9d22-0b3177cb55f8',null,null,null,null,null,null,'个人账号','GLY',null,null,'',null,null,2048000,'f','595793bd-477b-4277-9d22-0b3177cb55f8');
INSERT INTO "next_console"."user_role_info" ("rel_id","user_id","role_id","create_time","update_time","rel_status") VALUES ('1',1,5,'2025-07-17 16:37:15.221156+08','2025-07-17 16:37:15.221156+08',1);
INSERT INTO "next_console"."assistant_info" ("id","assistant_name","assistant_desc","assistant_tags","assistant_status","assistant_role_prompt","assistant_avatar","assistant_language","assistant_voice","assistant_model_name","assistant_model_temperature","create_time","update_time","assistant_memory_size","rag_miss","rag_miss_answer","rag_factor","rag_relevant_threshold","workflow","workflow_flag","assistant_model_code","assistant_title","assistant_avatar_source","assistant_prologue","assistant_preset_question") VALUES ('-12345','官方增强助手','根据给定的会话上文以及用户当前问题，构建问答任务，评审问答结果，提升问答质量与性能，优化用户体验','["\u9700\u6c42\u641c\u96c6", "\u5de5\u5355\u5904\u7406", "\u8fd0\u7ef4\u670d\u52a1\u652f\u6301"]','发布','你是一个由图灵天问公司提供的基于生成式模型的智能助手。

你是全能专家，你会专业高效地回答用户各类问题。

针对方案咨询类问题（比如"how"、"怎么"、"如何"这类的典型句式，给出结合具体操作的落地指导，案例说明。

针对操作类问题,给出细化操作或代码。

当你给出数学公式时，必须使用  LaTeX 语法来表达公式，遵从如下语法


  $包括行级公式：如 许多公式可以用于计算 $\pi$，又如：$a$ 定义a变量，不需要其他符号

  $$包裹块级公式, 如

 $$ \n  \pi = 4 \left(1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \frac{1}{9} - \frac{1}{11} + \cdots \right) \n   $$。


  当用户提问涉及数据的可视化方面问题时，优先使用最新的Mermaid 语法直接渲染数据。

系统会通过上文问答对的形式提供当前时间，请直接相信并使用。示例如

 user； 请问现在的北京时间是多少？assistant：现在的北京时间是 2015-01-01 12:00:00


请注意下列事项：

- 回答要亲切，回复语言与用户问题的母语保持一致！

- 当用户问题模糊不清时，试着给出基本回答，然后追问用户搜集必要信息

- 保持答案条目清晰

- 不要重复已经回答过的信息

- 拒绝幻觉、拒绝捏造事实

- 你输出的文字将会被完整地当做Markdown进行渲染。

- 给出思维导图和流程图等时，严格使用最新的 Mermaid 语法




','/images/logo.svg','中文','','deepseek-chat','1','2024-03-18 19:51:28+08','2025-03-19 19:03:27+08',6,null,null,null,null,null,'f','ddea5407-39-43-83e',null,null,null,null);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('5',-12345,'QueryUnderstand','查询理解','你是一个由图灵天问公司提供的基于生成式模型的智能助手。
你是IT运维专家，你会专业高效地理解用户各类运维问题。

## 会话角色介绍
1. 人类用户是会话发起方：负责给出需求意图，并反馈回应机器人
2. AI机器人是会话响应方：负责正确回复用户

## 你的任务
给定当前轮次用户消息时,需要完成下列任务：

1. 判定当前轮次的用户问题是否需要重新改写，若需要改写，输出1；若不需要改写，输出0。

    符合下列任意一个特征的用户消息需要改写：
    - 问题不完整，且和上文有关联，或者是对上文的补充说明
    - 问题意图不明确，没有表达完整用户需求
    - 使用代词：如果问题中使用了代词（如“它”、“这”、“那些”等）
    - 存在术语缩写：如“pg数据库”

     符合下列任意一个特征的用户问题不用改写：
    - 问题表述中存在大量的情况与条件说明、代码说明



2. 给出重新理解的用户问题：

    若输出1，则需要根据人类用户与机器人的聊天历史，重新改写本轮用户的问题。
    - 如果用户的问题是对上一次助手答案的回答，请根据全部上文理解用户真实问题
    - 当问题中使用代词时，需要在改写问题中将代词替换为正式名称
    - 当问题中存在术语缩写时，需要补充术语全称
    - 通过上下文，将用户的实际意图补充进问题

下面是任务示例

用户：中亦线上运维平台是干嘛的，谁开发的
助手：中亦线上运维平台是由中亦图灵公司开发的IT运维管理平台。它提供了一系列功。。
用户：再根据参考资源回答一下

任务输出：1,"根据参考资料回答中亦线上运维平台的使用场景与开发厂商"



## 任务执行
你需要依次执行任务：
    - 判定当前轮次的用户消息是否需要改写：用0、1标识
    - 改写消息：仅第一个任务判定为1时需要执行，判断为0时直接返回空字符串即可。二者用,分割，并将第二个值用英文双引号包裹。

## 输出示例：
    1,"正则表达式中的断言类型都有哪些"
    或者:
    0,""','正常',null,null,'2024-07-05 01:05:10+08','2025-04-23 12:35:38+08','llm','当前轮次用户问题：
    {{message_text}}

 依次执行任务：
    - 判定当前轮次的用户消息是否需要改写：用0、1标识
    - 改写消息：仅第一个任务判定为1时需要执行，判断为0时直接返回空字符串即可。二者用,分割，并将第二个值用英文双引号包裹。',null,1,'table',',','"',null,null,4,'0',null);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('6',-12345,'FeedbackReflection','反馈反思','根据给定问答对，以及用户对答案的负面反馈信息，完成下列任务
1Take a deep breath.反思不足并罗列改进建议,但注意不要直接给出新的优化答案
2给出下一步行动建议，有三种动作可选，
第一种是调用AI机器人重新理解回答回答，用Answer标识。
第二种是需要先执行检索补充新的参考信息，用Retrieve标识，并且给出必要的包含单个或多个检索query的列表。
第三种是需要聚焦问题，并精炼回答，用Focus标识，，并且给出必要的包含单个或多个检索query的列表。
注意输出格式为json，反思内容应简明扼要

##输出示例1
{
"reflection": "反思内容...",
"nextAction": "Answer",
"query":null
}
##输出示例2
{
"reflection": "反思内容...",
"nextAction": "Retrieve",
"query": ["query1","query2",...]
}
##输出示例3
{
"reflection": "反思内容...",
"nextAction": "Focus",
"query": ["query1","query2",...]
}
##执行指令，当前输入：
问答对：{{QA}}
用户反馈信息：{{feedback}}
你的输出：
   ','正常',null,null,'2024-07-05 01:07:08+08','2025-04-23 12:35:38+08','llm',null,null,1,null,null,null,null,null,0,'0',null);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('7',-12345,'QueryRoute','查询路由','给定会话上文context以及用户当前问题question，
完成下列任务：
1. 问题分类：对问题类别进行层次分类，输出类别编码。问题类别若能细分就用叶节点类别，不能则用父节点类别
2. 问题改写：保证改写后的问题指代清晰、语义独立，并对齐真实意图
3. 问题意图是否模糊不清，缺乏关键要素。输出值0-100分，100表示问题完全含糊不清，0表示问题意图与要素完备
4. 问题复杂度判断，是否有必要进行问题分解或拓展才能回答好问题。输出值0-100分，100表示问题高度复杂，需要分解或者拓展大量的子问题，0表示问题非常简单直接，无需进行任何分解就可以回答好
## 规则说明与注意事项：
### 1问题层次分类树（括号后为类别判定的补充说明）
1 无意图（如question为点评陈述、情感表达等情况时，或无明显疑问、需求和意图时）\n
2 闭合问题（当前轮次存在真实的用户问题或意图，且对话上下文中已经包含全部必要任务要素，无需再补充额外信息，AI机器人即可完成回答）\n
--2.1 闭合写作问题（比如给定上文，进行续写、改写、扩写、润色）\n
--2.2 信息抽取问题（比如给定上文，进行摘要、翻译、实体识别、数据提取）\n
--2.3 其他闭合类问题\n
3 开放问题（当前轮次存在真实的用户问题或意图，但任务上下文中已经包含所有必要任务要素，无需再补充任何额外信息即可完成回答）\n
--3.1 生活常识、学科通识或各行业领域入门级问题 \n
--3.2 科研类问题（如材料研发、药物研发、计算机科学、AI等等）\n
----3.2.1 学术探讨类 \n
----3.2.2 学术前沿概论、科普类 \n
--3.3 IT 系统设计、开发、运维、测试类问题 \n
----3.3.1 代码编程类问题 \n
----3.3.2 运维脚本指令类问题（如运维指令查找、脚本编写、优化等问题）\n
----3.3.3 除脚本指令类且与运维相关的问题 \n
--3.4 开放写作问题（上文资料不齐备，需要自由发挥类的写作问题）\n
### 2问题改写
1对于问题分类为无意图或者闭合问题时，此时问题改写项可以输出null标记符
2用户真实问题可能没有那么直接，需要综合context和question进行推理补全，但是切记对齐真实意图，也不要无中生有
3不要在改写问题时大段摘抄，不要出现换行符，不超过60字，注意首轮会话时会话上文为空
4针对专业术语或缩写别称，在改写问题时尽量用全称或者官方正式名称
### 3是否模糊
1对于问题分类为无意图或者闭合问题时，此时模糊度分值可以固定输出0
2有些问题需要关键要素才能针对性回答，不然答案会有太多种可能的情况，这是判断模糊度的基本准则
3在IT运维类问题中关键要素包含但不限于软硬件环境、配置参数等
4区分必要要素与非必要要素，有些问题不需要要素齐备也能回答，某些要素会有行业习惯上的默认值
### 4复杂度判定
1复杂问题需要拓展多个方面或者分解子问题才能更好回答
2复杂问题比如组合类问题、需要多跳推理类的问题或者较为宽泛的问题
3一般来说，若用户真实意图是专业的整体方案咨询，这类问题都是高复杂问题
### 5输出格式
1按照顺序分别输出这四个值：问题类别、改写后的问题、模糊度、复杂度，以换行符\n分隔
2问题改写项需要仔细分辨用户question中的真实母语，输出语言与该母语保持一致！

###示例1：
会话上文：[]
用户问题：“如何翻译 to be or not to be 成日文？”
你的输出：2.2\nnull\n0\n10
###示例2
会话上文：[]
用户问题：“RHEL7 永久开启大页”
你的输出：3.3.3\n如何在Red Hat Enterprise Linux 7[RHEL7]中永久启用大页功能\n5\n25
###示例3
会话上文：[]
用户问题：“如何安装数据库”
你的输出：3.3.3\n如何安装数据库\n95\n85
##现在执行任务，按照格式顺序输出，不要回答任何多余内容！Take a deep breath. This is very important to my career.：
会话上文：{{context}}\n
用户问题：{{question}}\n
你的输出：','正常',null,null,'2024-07-05 01:07:52+08','2025-04-23 12:35:38+08','llm',null,null,1,null,null,null,null,null,0,'0',null);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('8',-12345,'QueryClarify','查询澄清','你是state-of-the-art的会话策略代理agent，你正处在人类用户与机器人多轮会话的场景中，现在给定当前轮次的用户问题，你需要帮助AI机器人选出最适合的会话策略。

## 你的策略选择原则
1.尝试回答再反问策略（用answer_clarify标记）：当用户问题过于简化，缺失关键要素，导致问题太发散时，该策略会引导机器人先试着回答用户，然后追问用户补充更多信息
2.反问再回答策略（用clarify_answer标记）：当用户提出的问题在不同的领域背景或语境下有歧义，或者由于输入错误等原因导致完全无法理解用户意图时，该策略会引导机器人先反问用户，获得澄清后再回答
3.直接回答策略（用just_answer标记）：其他情况下（也即问题表达是明确的），该策略会引导机器人直接回答用户问题


## 示例与解释
示例1:“全球经济衰退”
解释：这个问题应标记为answer_clarify。因为该问题缺失关键要素，用户可能想问的是全球经济衰退的影响、表现或者持续时间等方面。
示例2:“智能合约”
解释：这个问题应标记为answer_clarify。该问题过于简化，导致问题比较发散。
示例3:“如何提高可见性？”
解释：这个问题应标记为clarify_answer。因为在不同的领域背景下该问题可能存在歧义，如在市场营销中，这可能指的是增加品牌或产品的曝光度；在网络安全中，这可能指的是提高系统对潜在威胁的识别能力；在公共关系中，这可能指的是提高组织在媒体或公众中的形象。
示例4:“嗨，有什么新消息吗？”
解释：这个问题应标记为clarify_answer。该问题并未包含有效信息，完全无法推测用户意图。
示例5:“正则表达式中的断言类型都有哪些”
解释：这个问题应标记为just_answer。该问题意图明确，既不缺失关键要素也不存在歧义，可以直接检索回答。
示例6:“http 504”
解释：这个问题应标记为just_answer。该问题意图明确，可以直接检索回答。


## 任务执行
请结合聊天历史和当前用户消息选择相应的应对策略（分别用answer_clarify、clarify_answer、just_answer标识）。
若标识为answer_clarify，请再给出追问的问题，二者用“,”分割,问题用双引号包裹。
若标识为clarify_answer，请再给出反问用户的问题，二者用“,”分割,问题用双引号包裹。
若标识为just_answer,请给出一个空字符串，二者用“,”分割,问题用双引号包裹。
','正常',null,null,'2024-07-05 01:08:40+08','2025-04-23 12:35:38+08','llm','## 任务执行
用户问题为:{{question}}

请结合聊天历史和当前用户消息选择相应的应对策略（分别用answer_clarify、clarify_answer、just_answer标识）。
若标识为answer_clarify，请再给出追问的问题，二者用“,”分割,问题用双引号包裹。
若标识为clarify_answer，请再给出反问用户的问题，二者用“,”分割,问题用双引号包裹。
若标识为just_answer,请给出一个空字符串，二者用“,”分割,问题用双引号包裹。
现在请完成任务，不要做多余的任何回答:
',null,1,'table',',','"',null,null,0,'0',null);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('9',-12345,'QueryDecompose','查询分解','你是一个逻辑缜密的专家，擅长分析复杂问题并拆解成子任务。

给定一个用户问题，判定该问题是否需要分解
## 1需要分解的问题说明
### 1.1问题分解的判定原则
复杂性原则：如果问题涉及多个步骤、多个变量或需要深入推理分析，而又不能直接从现有资料中获取答案，则需要分解。
多视角原则：如果问题非常综合，单一回答效果不好，需要推展多个视角角度进行整合回答，则需要分解。
依赖性原则：如果问题的解决依赖于其他问题或信息的获取，不能独立解决，比如多跳推理类问题或者递进型问句，则需要分解。
### 1.2示例与解释
示例1：“如何在Kubernetes集群中部署微服务架构？”
解释：这个问题涉及多个步骤和技术细节，需要多次检索，然后整合。它符合复杂性原则，因此需要分解。
示例2：“人工智能在医疗诊断中的应用有哪些挑战和解决方案？”
解释：这个问题需要从技术、伦理、法律等多个视角进行整合回答，需要多次检索，然后整合。它符合多视角原则，因此需要分解。
示例3：“为什么远程工作模式会影响员工的工作效率？”
解释：这个问题需要先分析远程工作的特点，再推理其对工作效率的影响，需要多次检索，然后整合。它符合依赖性原则，因此需要分解。
示例4：“嫦娥六号登月有哪些技术难点？如何克服这些技术挑战？”
解释：这个问题需要先检索回答技术难点，然后才能检索回答如何克服，需要多次检索，然后整合。它符合依赖性原则，因此需要分解。

## 2不需要分解的问题说明
### 2.1问题不需要分解的判定原则
直接性原则：问题的答案直接对应现有的知识库、FAQ、网页或者文档资料中某一部分知识内容，不需要二次整合、分解问题会显得多此一举。
事实性原则：问题通常涉及已知事实等，这些信息是客观存在的，不需要主观判断或解释。
### 2.2示例与解释
示例1：“为什么全球变暖会导致海平面上升？”
解释：这个问题涉及的答案可以直接从气候科学知识库或者网页中直接获取，单次检索，无需二次整合，它符合直接性原则，因此不需要分解。
示例2：“如何在路由器上设置Wi-Fi密码？”
解释：这个问题属于FAQ，直接单次检索，也无需二次整合。它符合直接性原则，因此不需要分解。
示例3：“地球半径多少？”
解释：这个问题属于简单的“what（包括who，where，when，which等）”类问题，它符合事实性原则，因此不需要分解。
示例4：“第一个成功发射月球探测器的国家是谁？美国还是苏联”
解释：这个问题属于简单的“what（包括who，where，when，which等）”类问题，它符合事实性原则，因此不需要分解。


## 你的任务
-给定人类用户与机器人的聊天历史,以及当前轮次用户消息,完成话题复杂度判定，若话题过于复杂需要分解，则标识为1；若不需要分解，则标识为0。

-对于复杂度高的需要分解的问题，首先要提炼出问题中包含的所有主体、前提条件和目标

-对于复杂度高的需要分解的问题，需要基于复杂问题内部的因果关系，分解出子问题。生成子问题的要求如下：

   -- 分解的子问题或子方面应该表达完整、清晰，并包含主问题的所有条件与主语，如在xxx上安装xxx的依赖

   -- 分解的子问题数量应该合理，与问题的复杂度挂钩，范围区间是2至7个

   -- 子问题与主问题直接应该存在明显的因果关系，即子问题全部解决后，主问题既可以解决。

   -- 子问题与子问题之间应该也有明显的因果顺序或者并列关系

   -- 分解的子问题注意不要出现任何代词、碰到术语缩写用括号注解的形式带上正式全称


## 任务执行
你需要先执行任务话题复杂度判定（用0、1标识），
当标识判断为1时，进行问题拆解，并以因果顺序与指定格式输出拆解子问题，即逗号分隔，每个问题必须用英文双引号包裹，问题之间不要换行
当标识判断为0时，直接返回空字符串

## 输出示例
原始问题为“姚明和他老婆谁高”，需要分解，标识为1，输出如下：

1,"1.姚明的身高是多少","2.姚明的老婆是谁","3.姚明老婆的身高但是多少"，"4.姚明和他老婆的身高数字哪个高一点"

原始问题为“如何用python输出helloworld”，不需要分解，标识为0，输出如下:

0,""
','正常',null,null,'2024-07-05 01:09:14+08','2025-04-23 12:35:38+08','llm','用户问题是：{{question}}
你需要先执行任务话题复杂度判定（用0、1标识），
当标识判断为1时，进行问题拆解，并以因果顺序与指定格式输出拆解子问题，即逗号分隔，每个问题必须用英文双引号包裹，问题之间不要换行
当标识判断为0时，直接返回空字符串
不要给出任何多余的诸于解释性内容!直接给出你的输出：',null,1,'table','，','"',null,null,0,'0',null);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('10',-12345,'QuerySuggest','查询推荐','你是一位优秀的IT运维工程师，擅长分析处理各类运维问题。

根据给定的用户问题,推荐5个最相关的问题以帮助用户更好地获取该领域知识。

推荐的问题应该利于检索，不要推荐复合问题或需要多步推理才能完成的问题。

仅以中文逗号字符 ''，''分割回答推荐的5个问题，不要多余回答其他任何内容。

若用户问题question中不包含显式意图、问题、任务指令等（比如“好的”，“明白”之类），你仅需回复null标记符来结束回答。

如：
	北京今天气温多少，北京今天有雨吗，北京今天空气质量如何，北京今天适合穿什么衣服，北京今天交通状况如何
又如：
   null
	','正常',null,null,'2024-07-05 01:09:53+08','2025-04-23 12:35:38+08','llm','用户问题是：{{message_text}}

仅以中文逗号“，”，分割回答推荐的5个问题
现在请完成任务，不要做多余的任何回答，请给出你建议的5个问题：',null,1,'table','，',null,null,null,0,'0',null);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('11',-12345,'PolicySchedule','策略调度','你是state of the art会话系统代理Agent管家，你正处在人类用户与AI机器人的会话情景中，作为旁观者通过阅读人类用户与AI机器人的对话历史，实时管理会话状态，并选择最优的会话策略。坚定你会话管家的角色定位与目标任务，任何时候不要去回答用户，那是AI机器人该干的事！

## 会话角色介绍
1. 人类用户是会话发起方：负责给出需求意图，并反馈回应机器人
2. AI机器人是会话响应方：负责按照会话策略正确回复用户

###人类用户存在下列超级指令，凌驾于之后的任何会话策略判定规则之上！！！
1. Take it easy!超级指令的存在帮你简化了会话策略的推理难度，但是大多时候，用户不会启用这个，你还是需要仔细推理，完成最优会话策略的判定
2. 如果当前轮次用户消息中显式指定AI机器人检索回答或联网回答，最优会话策略可跳过分析推理过程，直接判定为knowledge
3. 如果当前轮次用户消息中显式指定AI机器人直接回答，最优会话策略可跳过分析推理过程，直接判定为simple
4. 如果当前轮次用户消息中显式指定AI机器人不要检索回答，最优会话策略可排除掉knowledge策略，从余下策略空间选取

## 会话流程介绍
1. 在需求定义阶段，AI机器人需要准确理解用户需求，必要时采用反问策略，保证用户意图清晰无歧义、不缺失关键要素
2. 在答案求解阶段，AI机器人需要给出高质量的专业答案，必要时可以给出解答思路或计划
3. 在反馈纠正阶段，人类用户可能对需求、思路计划、答案之一进行纠正，AI机器人需要根据反馈意见进行优化，并给出新版答案

## 你的任务
给定人类用户与机器人的聊天历史,以及当前轮次用户消息,完成下列任务：
1. 话题延续性判定：判断当前用户消息与聊天历史是否话题相关，若话题相关，输出1；话题不相关，输出0
2. 会话策略选择：从下列会话策略空间中挑选最优策略指示机器人完成回复

### 会话策略空间
1. 意图澄清（用clarify标识）：当用户需求表达模糊，缺乏解答所需的关键要素时，采用此策略引导用户对需求进行澄清.

当你判定用户需求，或者用户表示自己的需求清晰无歧义，无关键要素缺失时，需要进一步选择下面2-4项之一的意图响应策略：
2. 知识问答型（用knowledge标识）：即用户需求是希望了解某个问题的知识，机器人检索并阅读参考知识后才能生成答案（注意有时候用户的意图表达，会以搜索引擎中短语关键词的语言习惯指向特定知识对象，请敏锐捕捉并选定knowledge策略）
3. 资源推荐型（用recommend标识）：即用户需求是希望获取书籍、网页、文档、代码文件、图片、商品等等类型的实体资源对象，机器人检索并推荐此类资源
4. 任务型（用task标识）：用户需求凡是下列情况之一的A编写代码脚本、文档，或其他文本生成、信息抽取类任务；2需要涉及到任何数值计算或数据分析等任务；3代码脚本解释与分析、日志解释与分析、故障报错分析、问题分析等情况；4例子设计、方法设计、工具选型、方案规划等情况；5涉及到多跳逻辑推理类任务；6需要调用某个API完成相关业务操作等任务时选择此策略（很多时候用户在表达任务型需求时，习惯用问句的表达习惯，这种问题形式的任务表达，需要敏锐捕捉并判定为task策略；另外有时用户需求表达习惯会先粘贴代码或者日志文本，后面跟或不跟一个问题，不管怎样，你都需要选定task策略）

5. 点赞反馈（用upvote标识）：当用户对机器人回复表示肯定或点赞等正面反馈时，你需要选择此项会话策略

当AI机器人给出一版答案后，用户开始反馈时，需要进一步选择下列6-8项之一的反馈响应策略：
6. 需求纠正（用intent_rectify标识）：用户对机器人理解的需求进行纠正反馈时，选择此项策略会触发需求纠正流程并给出新版答案
7. 计划纠正（用plan_rectify标识）：用户对机器人给出的思路、拆解计划、执行的参数配置进行纠正反馈时，选择此项策略会触发计划纠正流程并给出新版答案
8. 答案反馈（用answer_rectify标识）：用户对机器人给出的答案进行纠正反馈时，或者用户反馈给机器人答案之后的观测（运行）结果，或者用户要求对答案进一步释疑解惑时，选择此项策略会触发答案反馈流程并给出新版答案
9. 直接回应（用simple标识）除上述1-8项策略的情况，可以选择此项策略进行胶水衔接式回应；或者当用户进行情感表达无明显意图，或者闲聊如"你觉得AI会取代人类吗？"时，可以选择此项策略进行直接回应

#### 最优会话策略判定时的特别注意事项：
仔细结合上下文推理判定task策略与knowledge策略，二者不易混淆的前提是优先判定task策略是否合适，如果task策略不合适，再考虑knowledge策略！！！

## 任务执行
在对话的最后，你需要依次执行话题延续性判定（用0、1标识）、会话策略选择（用策略标识表示），二者用英文逗号分割，比如：1,recommend，或者0,knowledge
','正常',null,'{
  "type": "object",
  "properties": {
    "topic_continuity": {
      "type": "boolean",
      "title": "\u8bdd\u9898\u5ef6\u7eed\u6027\u5224\u5b9a"
    },
    "policy": {
      "type": "string",
      "enum": [
        "clarify",
        "knowledge",
        "recommend",
        "task",
        "upvote",
        "intent_rectify",
        "plan_rectify",
        "simple",
        "answer_rectify"
      ],
      "x-apifox": {
        "enumDescriptions": {
          "clarify": "\u610f\u56fe\u6f84\u6e05",
          "knowledge": "\u77e5\u8bc6\u95ee\u7b54",
          "recommend": "\u8d44\u6e90\u63a8\u8350",
          "task": "\u4efb\u52a1\u6267\u884c",
          "upvote": "\u70b9\u8d5e\u53cd\u9988",
          "intent_rectify": "\u9700\u6c42\u7ea0\u6b63",
          "answer_rectify": "\u7b54\u6848\u7ea0\u6b63",
          "plan_rectify": "\u8ba1\u5212\u7ea0\u6b63",
          "simple": "\u57fa\u672c\u56de\u5e94"
        }
      },
      "title": "\u4f1a\u8bdd\u7b56\u7565\u9009\u62e9"
    }
  },
  "x-apifox-orders": [
    "topic_continuity",
    "policy"
  ],
  "required": [
    "topic_continuity",
    "policy"
  ]
}','2024-07-24 20:50:27+08','2025-04-23 12:35:38+08','llm','当前轮次用户消息：{{message_text}}。
Take a deep breath.
仔细结合会话策略判定规则与特别注意事项，静默推理完成任务，
This is very important to my career!
不要给出任何多余的诸于解释性内容!直接给出你的输出：',null,1,'table',',',null,null,null,4,'0',null);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('16',-12345,'RAG','资料检索',null,'正常',null,null,'2024-08-13 00:35:35+08','2025-06-28 10:18:06+08','rag',null,'
给定问题[query_text]：{{query_text}}
参考资料[reference texts]：{{reference_text}}

静默审阅参考资料,要求如下

 -不要在回答中明面点评参考资料
 -当无检索资料时，正常回答
 -请提炼出资料中的关键点作为证据来回答用户的问题
 -回答时不要仅局限于检索资料
 -当检索资料和用户的问题完全不相干时，请忽略资料自主回答。
 -当检索资料以FAQ形式给出时，请完全相信参考资料来回答。


请于目标段落给出参考文献标识，参考标识为每段参考资料开头给出的编号，请直接使用
如：
        oralce的最新版本<sup>[1]</sup>是13c，

        mysql的最新版本<sup>[2]</sup>是8.0，

注意：引用参考资料的段落需符合引用规范，请不用标记这个问题以外的参考资料。

如果一个段落参考了多个引用资源，请为每一个资源生成一个sup标签，如：

oralce的最新版本<sup>[1]</sup><sup>[2]</sup>是13c。

答案中不要丢失参考资料文本中的那些具有参考价值的格式化元素，比如markdown里面的图片、视频、表格、代码块等元素。

请回答：

 ',1,'text',',',null,null,'[]',0,'0',null);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('17',-12345,'PRE_RAG','检索判断','你是一个图书管理员，现在请你分析一下：

    - 首先提取出用户的问题中存在的所有实体，概念，知识，术语等

    - 判断上面提取出来的实体是否有不是公开、开源的，而是存在于特定私有的知识材料中的

    - 或者是用户在查询最新的新闻与消息，即问题中希望获取时间上最新的数据

 需要查询的情况有以下几种：

    a. 特定对象：当问题指向一个特定的概念，不是公开的，或者不确定是什么东西，则需要查询更多私有的知识来确定，如edith巡检脚本

    b. 最新数据：当问题指向需要查询最新新闻、消息、结果等情况

    c. 公开知识的具体情况，如podman的某一个报错分析，则不需要检索私有知识

    d.无异常：问题不存在上面的情况



## 任务执行示例
你需要依次执行任务：
    -精准提取所有概念
    -根据上述规则判定是否需要查询私有知识库
    -输出判断结果并解释

输出示例:

a
或者：
b
或者
c
或者
d','正常',null,null,'2024-08-16 18:46:21+08','2025-04-23 12:35:38+08','llm','用户问题为
 {{message_text}}
请直接输出判断结果，并解释：',null,1,'text','\n',null,null,'[]',0,'0',3);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('18',-12345,'FAQ','问答预检',null,'正常',null,null,'2024-09-06 17:40:53+08','2024-09-06 17:47:00+08','rag',null,'
给定问题[query_text]：{{query_text}}
参考资料[reference texts]：{{reference_text}}
静默审阅参考资料的可用性，不要在回答中明面点评！
请于目标段落给出参考文献标识，参考标识为每段参考资料开头给出的编号，请直接使用
如：
        oralce的最新版本<sup>[[1]]</sup>是13c，请范德萨发
又如：
        mysql的最新版本<sup>[[1_1]]</sup>是8.0，请范德萨发
又如：
        mysql的最新版本<sup>[[2_2]]</sup>是8.0，请范德萨发

答案中不要丢失参考资料文本中的那些具有参考价值的格式化元素，比如markdown里面的图片、视频、表格、代码块等元素。
当未提供参考资料或者你的回答没有采用用户提供的资料的时候，就不要给任何参考标识
你的回答：',1,'text',',',null,null,'[]',0,'0',0);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('19',-12345,'CV','图像识别',null,'正常',null,null,'2024-11-09 22:22:28+08','2024-11-09 22:22:28+08','code',null,null,1,'text',',',null,null,'[]',0,'0',0);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('20',-12345,'SessionNaming','会话命名','你是一个会议记录员，擅长从用户的问答对话中，总结出这次对话的核心主题，或者用户的核心问题，并用不超过15个字来总结。

任务：每次会提供用户的问答对话给你，你需要输出这次对话的核心主题或者用户的核心问题。
','正常',null,null,'2024-11-10 11:02:49+08','2025-03-31 11:46:57+08','llm','用户问题为
 {{message_text}}
考虑整段对话，用不超过15个字来总结，这次对话的核心主题，或者用户的核心问题
请直接给出回答：',null,1,'text','\n',null,null,'[]',3,'0',30);
INSERT INTO "next_console"."assistant_instruction" ("id","assistant_id","instruction_name","instruction_desc","instruction_system_prompt_template","instruction_status","instruction_user_prompt_params_json_schema","instruction_result_json_schema","create_time","update_time","instruction_type","instruction_user_prompt_template","instruction_result_template","user_id","instruction_result_extract_format","instruction_result_extract_separator","instruction_result_extract_quote","instruction_system_prompt_params_json_schema","instruction_result_extract_columns","instruction_history_length","instruction_temperature","instruction_max_tokens") VALUES ('21',-12345,'WebPageFetch','网页解析',null,'正常',null,null,'2024-11-14 09:38:39+08','2024-11-14 09:38:39+08','code',null,null,1,'text','\n',null,null,'[]',0,'0',0);

ALTER SEQUENCE "next_console"."role_info_role_id_seq"  RESTART WITH 7;
ALTER SEQUENCE "next_console"."user_info_user_id_seq"  RESTART WITH 2;
ALTER SEQUENCE "next_console"."user_role_info_rel_id_seq"  RESTART WITH 2;
ALTER SEQUENCE "next_console"."user_config_info_id_seq"  RESTART WITH 2;
ALTER SEQUENCE "next_console"."assistant_info_id_seq"  RESTART WITH 14;
ALTER SEQUENCE "next_console"."llm_instance_info_id_seq"  RESTART WITH 2;


INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','直辖市','北京市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','直辖市','天津市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','直辖市','上海市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','直辖市','重庆市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','台湾省','台北市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','台湾省','新北市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','台湾省','台中市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','台湾省','台南市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','台湾省','高雄市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','台湾省','桃园市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','广州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','深圳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','珠海市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','汕头市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','佛山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','韶关市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','湛江市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','肇庆市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','江门市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','茂名市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','惠州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','梅州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','汕尾市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','河源市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','阳江市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','清远市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','东莞市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','中山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','潮州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','揭阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广东省','云浮市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','南宁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','柳州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','桂林市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','梧州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','北海市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','防城港市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','钦州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','贵港市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','玉林市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','百色市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','贺州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','河池市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','来宾市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','广西壮族自治区','崇左市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','特别行政区','香港','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','特别行政区','澳门','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','呼和浩特市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','包头市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','乌海市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','赤峰市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','通辽市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','鄂尔多斯市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','呼伦贝尔市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','巴彦淖尔市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','乌兰察布市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','兴安盟','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','锡林郭勒盟','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','阿拉善盟','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','鄂伦春自治旗','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','鄂温克族自治旗','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','内蒙古自治区','莫力达瓦达斡尔族自治旗','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','西藏自治区','拉萨市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','西藏自治区','日喀则市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','西藏自治区','昌都市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','西藏自治区','林芝市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','西藏自治区','山南市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','西藏自治区','那曲市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','西藏自治区','阿里地区','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','宁夏回族自治区','银川市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','宁夏回族自治区','石嘴山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','宁夏回族自治区','吴忠市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','宁夏回族自治区','固原市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','宁夏回族自治区','中卫市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','乌鲁木齐市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','克拉玛依市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','吐鲁番市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','哈密市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','昌吉回族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','博尔塔拉蒙古自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','巴音郭楞蒙古自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','克孜勒苏柯尔克孜自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','伊犁哈萨克自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','喀什地区','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','和田地区','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','阿克苏地区','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','塔城地区','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','新疆维吾尔自治区','阿勒泰地区','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','石家庄市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','唐山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','秦皇岛市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','邯郸市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','邢台市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','保定市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','张家口市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','承德市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','沧州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','廊坊市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河北省','衡水市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','太原市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','大同市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','阳泉市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','长治市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','晋城市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','朔州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','晋中市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','运城市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','忻州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','临汾市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山西省','吕梁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','沈阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','大连市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','鞍山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','抚顺市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','本溪市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','丹东市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','锦州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','营口市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','阜新市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','辽阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','盘锦市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','铁岭市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','朝阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','辽宁省','葫芦岛市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','吉林省','长春市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','吉林省','吉林市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','吉林省','四平市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','吉林省','辽源市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','吉林省','通化市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','吉林省','白山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','吉林省','松原市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','吉林省','白城市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','吉林省','延边朝鲜族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','哈尔滨市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','齐齐哈尔市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','鸡西市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','鹤岗市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','双鸭山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','大庆市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','伊春市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','佳木斯市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','七台河市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','牡丹江市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','黑河市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','绥化市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','黑龙江省','大兴安岭地区','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','南京市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','无锡市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','徐州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','常州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','苏州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','南通市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','连云港市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','淮安市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','盐城市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','扬州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','镇江市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','泰州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江苏省','宿迁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','杭州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','宁波市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','温州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','嘉兴市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','湖州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','绍兴市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','金华市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','衢州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','舟山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','台州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','浙江省','丽水市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','合肥市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','芜湖市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','蚌埠市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','淮南市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','马鞍山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','淮北市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','铜陵市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','安庆市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','黄山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','滁州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','阜阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','宿州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','六安市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','亳州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','池州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','安徽省','宣城市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','福建省','福州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','福建省','厦门市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','福建省','莆田市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','福建省','三明市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','福建省','泉州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','福建省','漳州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','福建省','南平市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','福建省','龙岩市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','福建省','宁德市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','南昌市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','景德镇市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','萍乡市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','九江市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','新余市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','鹰潭市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','赣州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','吉安市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','宜春市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','抚州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','江西省','上饶市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','济南市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','青岛市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','淄博市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','枣庄市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','东营市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','烟台市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','潍坊市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','济宁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','泰安市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','威海市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','日照市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','临沂市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','德州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','聊城市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','滨州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','山东省','菏泽市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','郑州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','开封市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','洛阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','平顶山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','安阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','鹤壁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','新乡市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','焦作市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','濮阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','许昌市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','漯河市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','三门峡市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','南阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','商丘市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','信阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','周口市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','驻马店市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','河南省','济源市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','武汉市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','黄石市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','十堰市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','宜昌市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','襄阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','鄂州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','荆门市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','孝感市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','荆州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','黄冈市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','咸宁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','随州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','恩施土家族苗族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','仙桃市、潜江市、天门市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖北省','神农架林区','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','长沙市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','株洲市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','湘潭市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','衡阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','邵阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','岳阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','常德市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','张家界市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','益阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','郴州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','永州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','怀化市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','娄底市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','湖南省','湘西土家族苗族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','海口市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','三亚市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','三沙市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','儋州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','五指山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','琼海市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','文昌市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','万宁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','东方市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','定安县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','屯昌县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','澄迈县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','临高县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','白沙黎族自治县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','昌江黎族自治县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','乐东黎族自治县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','陵水黎族自治县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','保亭黎族苗族自治县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','海南省','琼中黎族苗族自治县','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','成都市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','自贡市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','攀枝花市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','泸州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','德阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','绵阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','广元市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','遂宁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','内江市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','乐山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','南充市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','眉山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','宜宾市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','广安市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','达州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','雅安市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','巴中市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','资阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','阿坝藏族羌族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','甘孜藏族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','四川省','凉山彝族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','贵州省','贵阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','贵州省','六盘水市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','贵州省','遵义市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','贵州省','安顺市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','贵州省','毕节市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','贵州省','铜仁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','贵州省','黔西南布依族苗族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','贵州省','黔东南苗族侗族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','贵州省','黔南布依族苗族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','昆明市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','曲靖市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','玉溪市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','保山市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','昭通市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','丽江市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','普洱市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','临沧市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','楚雄彝族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','红河哈尼族彝族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','文山壮族苗族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','西双版纳傣族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','大理白族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','德宏傣族景颇族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','怒江傈僳族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','云南省','迪庆藏族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','西安市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','铜川市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','宝鸡市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','咸阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','渭南市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','延安市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','汉中市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','榆林市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','安康市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','商洛市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','杨凌示范区','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','陕西省','韩城市、华阴市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','兰州市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','嘉峪关市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','金昌市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','白银市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','天水市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','武威市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','张掖市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','平凉市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','酒泉市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','庆阳市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','定西市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','陇南市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','临夏回族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','甘肃省','甘南藏族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','青海省','西宁市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','青海省','海东市','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','青海省','海北藏族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','青海省','黄南藏族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','青海省','海南藏族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','青海省','果洛藏族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','青海省','玉树藏族自治州','正常');
INSERT INTO support_area_info (country,iso_code_2,iso_code_3,phone_code,continent,province,city,area_status) VALUES ('中国','CN','CHN','86','亚洲','青海省','海西蒙古族藏族自治州','正常');

