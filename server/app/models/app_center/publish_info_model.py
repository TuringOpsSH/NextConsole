from sqlalchemy.sql import func
from app.app import db


class AppPublishRecord(db.Model):
    """
    """
    __tablename__ = "app_publish_record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_code = db.Column(db.String(255), nullable=False, comment="应用编号")
    workflow_code = db.Column(db.String(255), comment="工作流编号")
    publish_code = db.Column(db.String(255), nullable=False, comment="发布编号")
    user_id = db.Column(db.Integer, nullable=False, comment="用户id")
    publish_name = db.Column(db.String(255), nullable=False, comment="发布名称")
    publish_desc = db.Column(db.Text, nullable=False, comment="发布描述")
    publish_config = db.Column(db.JSON, nullable=False, comment="发布配置")
    publish_status = db.Column(db.String(255), nullable=False, comment="发布状态")
    publish_version = db.Column(db.Integer, nullable=False, comment="发布版本")
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment="创建时间")
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def to_dict(self):
        return {
            "id": self.id,
            "app_code": self.app_code,
            "workflow_code": self.workflow_code,
            "publish_code": self.publish_code,
            "user_id": self.user_id,
            "publish_name": self.publish_name,
            "publish_desc": self.publish_desc,
            "publish_config": self.publish_config,
            "publish_status": self.publish_status,
            "publish_version": self.publish_version,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

