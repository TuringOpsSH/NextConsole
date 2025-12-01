ALTER TABLE "next_console"."resource_object_meta_info" ADD COLUMN "resource_rag_config" json;
COMMENT ON COLUMN "next_console"."resource_object_meta_info"."resource_rag_config" IS '资源RAG配置';

UPDATE "next_console"."resource_object_meta_info" set "resource_source" = 'resource_center' where "resource_parent_id" is null and "resource_status" = '正常' and "resource_name"  = '我的资源';


/* 请确认以下SQL符合您的变更需求，务必确认无误后再提交执行 */

ALTER TABLE "next_console"."workflow_node_info" ADD COLUMN  "node_tool_configs" json;
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_tool_configs" IS '工具节点配置';


/* 请确认以下SQL符合您的变更需求，务必确认无误后再提交执行 */

ALTER TABLE "next_console"."workflow_node_instance" ADD COLUMN  "workflow_node_tool_configs" json;
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_tool_configs" IS '工具节点配置';

/* 请确认以下SQL符合您的变更需求，务必确认无误后再提交执行 */
ALTER TABLE "next_console"."workflow_node_info" ADD COLUMN "node_variable_cast_config" json;
COMMENT ON COLUMN "next_console"."workflow_node_info"."node_variable_cast_config" IS '变量转换节点配置'

ALTER TABLE "next_console"."workflow_node_instance" ADD COLUMN  "workflow_node_variable_cast_config" json;
COMMENT ON COLUMN "next_console"."workflow_node_instance"."workflow_node_variable_cast_config" IS '节点变量类型转换配置';

