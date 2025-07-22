CREATE OR REPLACE FUNCTION update_update_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_time = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
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


