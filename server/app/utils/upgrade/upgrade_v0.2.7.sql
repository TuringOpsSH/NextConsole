ALTER TABLE "next_console"."llm_instance_info" ADD COLUMN  "llm_label" varchar(255);
COMMENT ON COLUMN "next_console"."llm_instance_info"."llm_label" IS '模型显示名称';
ALTER TABLE "next_console"."llm_instance_info" ADD COLUMN  "extra_body" json;
COMMENT ON COLUMN "next_console"."llm_instance_info"."extra_body" IS '额外请求头';
ALTER TABLE "next_console"."llm_instance_info" ADD COLUMN  "extra_headers" json;
COMMENT ON COLUMN "next_console"."llm_instance_info"."extra_headers" IS '额外请求体';
ALTER TABLE "next_console"."llm_instance_info" ADD COLUMN  "use_default" boolean;
COMMENT ON COLUMN "next_console"."llm_instance_info"."use_default" IS '使用默认参数';


CREATE TABLE "next_console"."llm_instance_authorize_info"
(
 "id" SERIAL PRIMARY KEY,
 "user_id" integer NOT NULL ,
 "model_id" integer NOT NULL ,
 "auth_colleague_id" integer ,
 "auth_friend_id" integer ,
 "auth_department_id" integer ,
 "auth_company_id" integer ,
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
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_department_id" IS '被授权部门id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_company_id" IS '被授权公司id';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_type" IS '授权类型';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_status" IS '授权状态';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_friend_id" IS '被授权联系人id';
COMMENT ON TABLE "next_console"."llm_instance_authorize_info" IS '模型授权用户表';


CREATE INDEX "model_id50"
ON "next_console"."llm_instance_authorize_info" USING btree ( "model_id" )
;
CREATE INDEX "llm_instance_authorize_user_id49"
ON "next_console"."llm_instance_authorize_info" USING btree ( "user_id" )
;
CREATE TRIGGER llm_instance_authorize_info BEFORE UPDATE ON "next_console"."llm_instance_authorize_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


CREATE TABLE "next_console"."llm_supplier_info"
(
 "id" SERIAL PRIMARY KEY,
 "supplier_code" varchar(256) ,
 "supplier_name" varchar(256) ,
 "supplier_desc" text ,
 "supplier_icon" text ,
 "supplier_type" varchar(10) ,
 "supplier_website" text ,
 "supplier_models" json ,
 "supplier_status" varchar(10) ,
 "supplier_api_url" text ,
 "create_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
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
COMMENT ON COLUMN "next_console"."llm_supplier_info"."supplier_api_url" IS '厂商api地址';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "next_console"."llm_supplier_info"."update_time" IS '更新时间';

COMMENT ON TABLE "next_console"."llm_supplier_info" IS '基模型厂商信息表';

CREATE TRIGGER update_llm_supplier_info_trigger BEFORE UPDATE ON "next_console"."llm_supplier_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

UPDATE "next_console"."llm_instance_info" set "llm_label" = "llm_type";