from app.app import db
from sqlalchemy.sql import func


class PermissionInfo(db.Model):
    __tablename__ = 'permission_info'
    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_name = db.Column(db.String(255), nullable=False)
    permission_url = db.Column(db.String(255), nullable=False)
    permission_desc = db.Column(db.String(255))
    permission_condition = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())
    permission_status = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'permission_id': self.permission_id,
                'permission_name': self.permission_name,
                'permission_url': self.permission_url,
                'permission_desc': self.permission_desc,
                'permission_condition': self.permission_condition,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                'permission_status': self.permission_status,

                }
