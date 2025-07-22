
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
 "session_cancel_reason" text
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