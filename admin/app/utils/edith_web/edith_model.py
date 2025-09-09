from sqlalchemy.sql import func
from app.app import db


class EdithClientMetaInfo(db.Model):
    """
    """
    __tablename__ = 'edith_client_meta_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(255), nullable=False, comment='客户端名称')
    client_desc = db.Column(db.String(255), nullable=False, comment='客户端描述')
    client_icon = db.Column(db.Text, nullable=False, comment='客户端图标')
    support_os = db.Column(db.Text, comment='支持操作系统')
    client_version = db.Column(db.String(255), nullable=False, comment='版本号')
    client_sub_version = db.Column(db.String(255), nullable=False, comment='子版本号')
    client_raw_path = db.Column(db.Text, nullable=False, comment='客户端原始路径')
    client_download_path = db.Column(db.Text, nullable=False, comment='客户端下载路径')
    client_status = db.Column(db.String(255), nullable=False, comment='客户端状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_desc': self.client_desc,
            'client_icon': self.client_icon,
            'support_os': self.support_os,
            'client_version': self.client_version,
            'client_sub_version': self.client_sub_version,
            'client_raw_path': self.client_raw_path,
            'client_download_path': self.client_download_path,
            'client_status': self.client_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_desc': self.client_desc,
            'client_icon': self.client_icon,
            'support_os': self.support_os,
            'client_version': self.client_version,
            'client_sub_version': self.client_sub_version,
            'client_download_path': self.client_download_path,
            'client_status': self.client_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class EdithTaskInfo(db.Model):
    """

    """
    __tablename__ = 'edith_task_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_code = db.Column(db.String(255), nullable=False, comment='巡检任务编号')
    session_id = db.Column(db.Integer, nullable=False, comment='会话id')
    user_id = db.Column(db.Integer, nullable=False, comment='用户id')
    task_name = db.Column(db.String(255), default='', comment='任务名称')
    task_desc = db.Column(db.String(255), default='', comment='任务描述')
    task_type = db.Column(db.String(255), default='', comment='任务类型')
    task_stage = db.Column(db.String(255), default='', comment='任务阶段')
    task_data_dir = db.Column(db.Text, default='', comment='任务数据目录')
    edith_client_id = db.Column(db.Integer, comment='edith客户端id')
    task_parent_id = db.Column(db.Integer, comment='父任务id')
    task_status = db.Column(db.String(255), default='初始化', comment='任务状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'task_code': self.task_code,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'task_name': self.task_name,
            'task_desc': self.task_desc,
            'task_type': self.task_type,
            'task_stage': self.task_stage,
            'task_data_dir': self.task_data_dir,
            'edith_client_id': self.edith_client_id,
            'task_parent_id': self.task_parent_id,
            'task_status': self.task_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        return {
            'id': self.id,
            'task_code': self.task_code,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'task_name': self.task_name,
            'task_desc': self.task_desc,
            'task_type': self.task_type,
            'task_stage': self.task_stage,
            'edith_client_id': self.edith_client_id,
            'task_parent_id': self.task_parent_id,
            'task_status': self.task_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class EdithReportInfo(db.Model):
    """
    CREATE TABLE IF NOT EXISTS `edith_report_info` (
) ENGINE=InnoDB COMMENT 'edith巡检报告信息表';
    """
    __tablename__ = 'edith_report_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, comment='用户id')
    edith_task_id = db.Column(db.Integer, nullable=False, comment='edith巡检任务id')
    report_code = db.Column(db.String(255), nullable=False, comment='报告编号')
    report_name = db.Column(db.Text, default='', comment='报告名称')
    report_desc = db.Column(db.Text, comment='报告描述')
    report_type = db.Column(db.String(255), nullable=False, comment='报告类型')
    report_data_dir = db.Column(db.Text, nullable=False, comment='报告数据目录')
    report_generate_config = db.Column(db.String(255), default='', comment='报告生成配置')
    run_model = db.Column(db.String(255), default='', comment='运行模式')
    celery_id = db.Column(db.String(255), comment='任务id')
    task_trace = db.Column(db.Text, comment='任务日志')
    report_path = db.Column(db.Text, comment='报告路径')
    report_download_url = db.Column(db.Text, comment='报告下载地址')
    report_status = db.Column(db.String(255), nullable=False, comment='报告状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'edith_task_id': self.edith_task_id,
            'report_code': self.report_code,
            'report_name': self.report_name,
            'report_desc': self.report_desc,
            'report_type': self.report_type,
            'report_data_dir': self.report_data_dir,
            'run_model': self.run_model,
            'report_generate_config': self.report_generate_config,
            'celery_id': self.celery_id,
            'task_trace': self.task_trace,
            'report_path': self.report_path,
            'report_download_url': self.report_download_url,
            'report_status': self.report_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'edith_task_id': self.edith_task_id,
            'report_code': self.report_code,
            'report_name': self.report_name,
            'report_desc': self.report_desc,
            'report_type': self.report_type,
            'run_model': self.run_model,
            'report_download_url': self.report_download_url,
            'report_status': self.report_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


