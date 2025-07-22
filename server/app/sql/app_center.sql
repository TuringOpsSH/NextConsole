
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
 "node_file_reader_config" json ,
CONSTRAINT "workflow_node_info_ibfk_178" FOREIGN KEY ("user_id") REFERENCES "next_console"."user_info"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION ,
CONSTRAINT "workflow_node_info_ibfk_277" FOREIGN KEY ("workflow_id") REFERENCES "next_console"."workflow_meta_info"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
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
 "workflow_node_file_reader_config" json
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
 "update_time" timestamp with time zone DEFAULT CURRENT_TIMESTAMP ,
CONSTRAINT "workflow_task_info_ibfk_179" FOREIGN KEY ("user_id") REFERENCES "next_console"."user_info"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION ,
CONSTRAINT "workflow_task_info_ibfk_280" FOREIGN KEY ("session_id") REFERENCES "next_console"."next_console_session_info"("id") ON UPDATE NO ACTION ON DELETE NO ACTION ,
CONSTRAINT "workflow_task_info_ibfk_381" FOREIGN KEY ("qa_id") REFERENCES "next_console"."next_console_qa_info"("qa_id") ON UPDATE NO ACTION ON DELETE NO ACTION ,
CONSTRAINT "workflow_task_info_ibfk_482" FOREIGN KEY ("msg_id") REFERENCES "next_console"."next_console_llm_message"("msg_id") ON UPDATE NO ACTION ON DELETE NO ACTION ,
CONSTRAINT "workflow_task_info_ibfk_583" FOREIGN KEY ("task_assistant_id") REFERENCES "next_console"."assistant_info"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
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