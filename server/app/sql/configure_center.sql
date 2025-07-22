
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
 "response_format" json,
 "stop" json ,
 "stream" boolean ,
 "temperature" double precision ,
 "top_p" double precision ,
 "llm_icon" text ,
 "is_std_openai" boolean  ,
 "support_vis" boolean ,
 "support_file" boolean
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
COMMENT ON TABLE "next_console"."llm_instance_info" IS '基模型实例信息表';

CREATE INDEX "user_id12"
ON "next_console"."llm_instance_info" USING btree ( "user_id" )
;

CREATE TRIGGER update_llm_instance_info_trigger BEFORE UPDATE ON "next_console"."llm_instance_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------
CREATE TABLE "next_console"."system_config_info"
(
 "id" SERIAL PRIMARY KEY,
 "module_name" varchar(255) NOT NULL ,
 "component_name" varchar(255) NOT NULL ,
 "config_name" varchar(255) NOT NULL ,
 "config_desc" varchar(255) NOT NULL ,
 "config_default_value" varchar(1024) NOT NULL ,
 "config_value" varchar(1024) NOT NULL ,
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
COMMENT ON COLUMN "next_console"."system_config_info"."module_name" IS '模块名称';
COMMENT ON COLUMN "next_console"."system_config_info"."component_name" IS '组件名称';
COMMENT ON COLUMN "next_console"."system_config_info"."config_name" IS '配置名称';
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
 "open_query_agent" integer ,
 "resource_shortcut_types" json ,
 "resource_table_show_fields" json ,
 "resource_auto_rag" boolean ,
 "search_engine_language_type" json ,
 "search_engine_resource_type" varchar(255) DEFAULT 'search'::character varying
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
COMMENT ON COLUMN "next_console"."user_config_info"."open_query_agent" IS '是否启用query-agent';
COMMENT ON COLUMN "next_console"."user_config_info"."resource_shortcut_types" IS '我的资源种类快捷方式';
COMMENT ON COLUMN "next_console"."user_config_info"."resource_table_show_fields" IS '资源表格展示字段';
COMMENT ON COLUMN "next_console"."user_config_info"."resource_auto_rag" IS '上传资源是否自动构建为知识索引';
COMMENT ON COLUMN "next_console"."user_config_info"."search_engine_language_type" IS '搜索引擎语言种类';
COMMENT ON COLUMN "next_console"."user_config_info"."search_engine_resource_type" IS '搜索引擎资源类型';
COMMENT ON TABLE "next_console"."user_config_info" IS '用户配置表';
CREATE TRIGGER update_user_config_info_trigger BEFORE UPDATE ON "next_console"."user_config_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();