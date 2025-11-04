
/* 请确认以下SQL符合您的变更需求，务必确认无误后再提交执行 */

ALTER TABLE "next_console"."llm_instance_authorize_info" ADD COLUMN  "auth_user_id" integer;
COMMENT ON COLUMN "next_console"."llm_instance_authorize_info"."auth_user_id" IS '被授权用户id';
/* 请确认以下SQL符合您的变更需求，务必确认无误后再提交执行 */

ALTER TABLE "next_console"."llm_instance_info" ADD COLUMN  "think_attr" json;
COMMENT ON COLUMN "next_console"."llm_instance_info"."think_attr" IS '推理标签';
