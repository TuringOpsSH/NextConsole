
from app.app import app

"""
   v0.2.5 -> v0.2.6
    结构修改
        ALTER TABLE "system_config_info" 
        ALTER COLUMN config_default_value TYPE JSON 
        USING COALESCE(config_default_value::json, '{}'::json),
        ALTER COLUMN config_value TYPE JSON 
        USING COALESCE(config_value::json, '{}'::json);
        ALTER TABLE "system_config_info" DROP COLUMN "module_name";
        ALTER TABLE "system_config_info" DROP COLUMN "component_name";
        ALTER TABLE "system_config_info" RENAME COLUMN "config_name" TO "config_key";
        ALTER TABLE user_config_info ADD COLUMN  "config_key" varchar(255);
        COMMENT ON COLUMN user_config_info."config_key" IS '配置键名';
        ALTER TABLE user_config_info ADD COLUMN  "config_value" json;
        COMMENT ON COLUMN user_config_info."config_value" IS '配置值(JSON格式)';
         
        ALTER TABLE "user_config_info" DROP COLUMN "open_query_agent";
        ALTER TABLE "user_config_info" DROP COLUMN "resource_shortcut_types";
        ALTER TABLE "user_config_info" DROP COLUMN "resource_table_show_fields";
        ALTER TABLE "user_config_info" DROP COLUMN "resource_auto_rag";
        ALTER TABLE "user_config_info" DROP COLUMN "search_engine_language_type";
        ALTER TABLE "user_config_info" DROP COLUMN "search_engine_resource_type";
    数据修复
         UPDATE "app_meta_info" 
          SET app_icon = '/' || app_icon
          WHERE app_icon LIKE 'images/%';
          
        UPDATE "workflow_meta_info" 
        SET workflow_icon = '/' || workflow_icon
        WHERE workflow_icon LIKE 'images/%';

        UPDATE "assistant_info" 
          SET assistant_avatar = '/' || assistant_avatar
          WHERE assistant_avatar LIKE 'images/%';
          
        UPDATE "llm_instance_info" 
          SET llm_icon = '/' || llm_icon
          WHERE llm_icon LIKE 'images/%';
        -- 开始事务    
        BEGIN;
         
        -- 创建备份表
        CREATE TABLE workflow_meta_info_backup AS
        SELECT * FROM "workflow_meta_info" 
        WHERE json_typeof(workflow_edit_schema) = 'string'
           AND workflow_edit_schema::text LIKE '"%' 
           AND (workflow_edit_schema #>> '{}')::json IS NOT NULL;
         
        -- 更新异常数据
        UPDATE "workflow_meta_info" 
        SET workflow_edit_schema = (workflow_edit_schema #>> '{}')::json
        WHERE json_typeof(workflow_edit_schema) = 'string'
           AND workflow_edit_schema::text LIKE '"%' 
           AND (workflow_edit_schema #>> '{}')::json IS NOT NULL;
         
        -- 验证更新结果
        SELECT 
            COUNT(*) as total_updated,
            SUM(CASE WHEN json_typeof(workflow_edit_schema) = 'object' THEN 1 ELSE 0 END) as now_objects,
            SUM(CASE WHEN json_typeof(workflow_edit_schema) = 'string' THEN 1 ELSE 0 END) as still_strings
        FROM "workflow_meta_info" 
        WHERE id IN (SELECT id FROM workflow_meta_info_backup);
         
        -- 提交事务
        COMMIT;
        
        


"""


def update_schema_icon():
    with app.app_context():
        """
        升级脚本：v0.2.x 
        """
        from app.app import db
        from app.models.app_center.app_info_model import WorkFlowMetaInfo
        from sqlalchemy.orm.attributes import flag_modified
        all_workflow = WorkFlowMetaInfo.query.all()
        for workflow in all_workflow:
            new_workflow_edit_schema = []
            for cell in workflow.workflow_edit_schema.get("cells", []):
                if (cell.get("shape") == "custom-vue-node"
                        and cell.get("data",{}).get("nodeIcon", "").startswith("images/")):
                    cell["data"]["nodeIcon"] = "/" + cell["data"]["nodeIcon"]
                    print(cell["data"]["nodeIcon"])

                if (cell.get("shape") == "edge"
                        and cell.get("data",{}).get("edge_icon", "").startswith("images/")):
                    cell["data"]["edge_icon"] = "/" + cell["data"]["edge_icon"]
                    print(cell["data"]["edge_icon"])
                new_workflow_edit_schema.append(cell)
            workflow.workflow_edit_schema["cells"] = new_workflow_edit_schema
            # 标记为已修改
            flag_modified(workflow, "workflow_edit_schema")
            db.session.add(workflow)
        db.session.commit()


def update_user_config():
    """
    修复用户配置数据
    Returns
    -------

    """
    with app.app_context():
        """
        升级脚本：v0.2.x 
        """
        from app.app import db
        from app.models.user_center.user_info import UserInfo
        from app.models.configure_center.user_config import UserConfig
        all_users = UserInfo.query.all()
        default_config = {
            "workbench": {
                "model_list": [],
                "message_layout": "",
                "search_engine_language": "en",
                "search_engine_resource": "search",
            },
            "resources": {
                "auto_rag": True,
                "view_components": 'pdf',
            },
            "contact": {
                "allow_search": True,
            },
            "system": {
                "theme": "light",
                "language": "中文",
            }
        }
        for user in all_users:
            for key in default_config:
                new_sub_config = UserConfig(
                    user_id=user.user_id,
                    config_key=key,
                    config_value=default_config[key],
                    config_status='正常'
                )
                db.session.add(new_sub_config)
        db.session.commit()
        # 清理旧的无效数据
        all_old_configs = UserConfig.query.filter(
            UserConfig.config_key.is_(None)
        ).all()
        for old_config in all_old_configs:
            db.session.delete(old_config)
        db.session.commit()
    return True


def main():
    update_schema_icon()
    update_user_config()


if __name__ == "__main__":
    main()

