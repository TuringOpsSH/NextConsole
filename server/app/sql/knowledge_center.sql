CREATE OR REPLACE FUNCTION update_update_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_time = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
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