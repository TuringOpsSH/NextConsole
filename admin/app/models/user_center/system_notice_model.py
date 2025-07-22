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


class NoticeTaskInfo(db.Model):
    """

    """
    __tablename__ = 'user_notice_task_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    task_name = db.Column(db.String(255), default='')
    task_desc = db.Column(db.Text, default='')
    notice_type = db.Column(db.String(255), nullable=False)
    notice_template = db.Column(db.Text, default='', nullable=False)
    notice_params = db.Column(db.JSON, default={}, nullable=False)
    task_instance_batch_size = db.Column(db.Integer, default=1)
    task_instance_total = db.Column(db.Integer, default=0)
    task_instance_success = db.Column(db.Integer, default=0)
    task_instance_failed = db.Column(db.Integer, default=0)
    task_status = db.Column(db.String(255), nullable=False)
    begin_time = db.Column(db.DateTime)
    finish_time = db.Column(db.DateTime)
    run_now = db.Column(db.Boolean, default=True)
    plan_begin_time = db.Column(db.DateTime)
    plan_finish_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        task_instance_finish_cnt = self.task_instance_success + self.task_instance_failed
        if task_instance_finish_cnt == 0:
            task_progress = 0
        elif self.task_instance_total == 0:
            task_progress = 0
        else:
            task_progress = round(task_instance_finish_cnt / self.task_instance_total, 4) * 100
        return {'id': self.id,
                'user_id': self.user_id,
                'task_name': self.task_name,
                'task_desc': self.task_desc,
                'notice_type': self.notice_type,
                'notice_template': self.notice_template,
                'notice_params': self.notice_params,
                'task_instance_batch_size': self.task_instance_batch_size,
                "task_instance_total": self.task_instance_total,
                "task_instance_success": self.task_instance_success,
                "task_instance_failed": self.task_instance_failed,
                "task_progress": task_progress,
                'task_status': self.task_status,
                'begin_time': self.begin_time.strftime('%Y-%m-%d %H:%M:%S') if self.begin_time else '',
                'finish_time': self.finish_time.strftime('%Y-%m-%d %H:%M:%S') if self.finish_time else '',
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                'run_now': self.run_now,
                'plan_begin_time': self.plan_begin_time.strftime('%Y-%m-%d %H:%M:%S') if self.plan_begin_time else '',
                'plan_finish_time': self.plan_finish_time.strftime('%Y-%m-%d %H:%M:%S') if self.plan_finish_time else ''
                }


class NoticeTaskInstance(db.Model):
    """
     '用户通知任务实例';
    """
    __tablename__ = 'user_notice_task_instance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, nullable=False)
    receive_user_id = db.Column(db.Integer, nullable=False)
    task_celery_id = db.Column(db.String(255), nullable=False)
    notice_type = db.Column(db.String(255), nullable=False)
    notice_params = db.Column(db.JSON, nullable=False)
    notice_content = db.Column(db.Text, nullable=False)
    notice_status = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {'id': self.id,
                'task_id': self.task_id,
                'receive_user_id': self.receive_user_id,
                'task_celery_id': self.task_celery_id,
                'notice_type': self.notice_type,
                'notice_params': self.notice_params,
                'notice_content': self.notice_content,
                'notice_status': self.notice_status,
                'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
                }

