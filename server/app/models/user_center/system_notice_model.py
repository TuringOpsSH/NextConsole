from app.app import db
from sqlalchemy.sql import func


class SystemNotice(db.Model):
    """
    '站内信';
    """
    __tablename__ = 'system_notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    notice_title = db.Column(db.Text, nullable=False)
    notice_icon = db.Column(db.Text, default='')
    notice_type = db.Column(db.String(255), nullable=False)
    notice_level = db.Column(db.String(255), nullable=False)
    notice_content = db.Column(db.Text, default='')
    notice_status = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'notice_title': self.notice_title,
                'notice_icon': self.notice_icon,
                'notice_type': self.notice_type,
                'notice_level': self.notice_level,
                'notice_content': self.notice_content,
                'notice_status': self.notice_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }


