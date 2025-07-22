from sqlalchemy.sql import func
from app.app import db


class UserConfig(db.Model):
    """
    """
    __tablename__ = 'user_config_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    user_id = db.Column(db.Integer, nullable=False, comment='用户id')
    open_query_agent = db.Column(db.Integer,  default=True, comment='是否启用query-agent')
    resource_shortcut_types = db.Column(db.JSON, default=[], comment='资源快捷方式类型')
    resource_table_show_fields = db.Column(db.JSON, default=[], comment='资源表格展示字段')
    resource_auto_rag = db.Column(db.Boolean, default=True, comment='资源自动rag')
    search_engine_language_type = db.Column(db.JSON, default={}, comment='搜索引擎语言类型')
    search_engine_resource_type = db.Column(db.String(255), default="search", comment='搜索引擎搜索类型')
    config_status = db.Column(db.String(255), nullable=False, comment='配置状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='配置创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='配置更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "config_status": self.config_status,
            "open_query_agent": self.open_query_agent,
            "resource_table_show_fields": self.resource_table_show_fields,
            "resource_auto_rag": self.resource_auto_rag,
            "resource_shortcut_types": self.resource_shortcut_types,
            "search_engine_language_type": self.search_engine_language_type,
            "search_engine_resource_type": self.search_engine_resource_type,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
