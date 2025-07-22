from app.app import db
from sqlalchemy.sql import func


class RolePermissionInfo(db.Model):
    __tablename__ = 'role_permission_info'
    rel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_id = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())
    rel_status = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'rel_id': self.rel_id,
                'permission_id': self.permission_id,
                'role_id': self.role_id,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                'rel_status': self.user_status,
                }

