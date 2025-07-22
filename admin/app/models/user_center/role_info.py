from app.app import db
from sqlalchemy.sql import func


class RoleInfo(db.Model):
    __tablename__ = 'role_info'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(255), nullable=False)
    role_desc = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    status = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'role_id': self.role_id,
                'role_name': self.role_name,
                'role_desc': self.role_desc,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': self.status,
        }
