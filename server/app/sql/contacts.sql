CREATE OR REPLACE FUNCTION update_update_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_time = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

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



