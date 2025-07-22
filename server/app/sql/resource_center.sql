
CREATE OR REPLACE FUNCTION update_update_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_time = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
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
 "resource_version" integer DEFAULT 1
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


