from sqlalchemy.sql import func
from app.app import db


class UserConfig(db.Model):
    """
    """
    __tablename__ = 'user_config_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    user_id = db.Column(db.Integer, nullable=False, comment='用户id')
    config_key = db.Column(db.String(255), nullable=False, comment='配置键名')
    config_value = db.Column(db.JSON, nullable=False, comment='配置值(JSON格式)')
    config_status = db.Column(db.String(255), nullable=False, comment='配置状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='配置创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='配置更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "config_status": self.config_status,
            "config_key": self.config_key,
            "config_value": self.config_value,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
