from sqlalchemy.sql import func

from app.app import db
from pgvector.sqlalchemy import Vector


class RagRefInfo(db.Model):
    """
    """
    __tablename__ = 'rag_ref_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    ref_code = db.Column(db.String(255), default="", comment='ref_id')
    resource_id = db.Column(db.Integer, default=0, comment='资源id')
    user_id = db.Column(db.Integer, nullable=False, comment='创建用户id')
    celery_task_id = db.Column(db.String(255), default="", comment='celery任务ID')
    task_trace_log = db.Column(db.Text, default="", comment='任务追踪日志')
    file_reader_config = db.Column(db.JSON, default={}, comment='文件读取配置')
    file_split_config = db.Column(db.JSON, default={}, comment='文件切分配置')
    file_chunk_abstract_config = db.Column(db.JSON, default={}, comment='文件摘要配置')
    file_chunk_embedding_config = db.Column(db.JSON, default={}, comment='文件向量化配置')
    ref_type = db.Column(db.String(255), default='', comment='索引类型')
    ref_hit_counts = db.Column(db.Integer, default=0, comment='索引命中次数')
    ref_chunk_cnt = db.Column(db.Integer, default=0, comment='分段数量')
    ref_chunk_ready_cnt = db.Column(db.Integer, default=0, comment='分段已准备数量')
    ref_embedding_token_used = db.Column(db.Integer, default=0, comment='分段嵌入使用的token数量')
    ref_status = db.Column(db.String(255), default="", comment='索引状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'ref_code': self.ref_code,
            'resource_id': self.resource_id,
            'user_id': self.user_id,
            'celery_task_id': self.celery_task_id,
            'task_trace_log': self.task_trace_log,
            'ref_type': self.ref_type,
            'ref_hit_counts': self.ref_hit_counts,
            'ref_chunk_cnt': self.ref_chunk_cnt,
            'ref_chunk_ready_cnt': self.ref_chunk_ready_cnt,
            'ref_embedding_token_used': self.ref_embedding_token_used,
            'ref_status': self.ref_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ResourceChunkInfo(db.Model):
    """
    """
    __tablename__ = 'resource_chunk_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    resource_id = db.Column(db.Integer, nullable=False, comment='资源id')
    ref_id = db.Column(db.Integer, comment='参考索引ID')
    split_method = db.Column(db.String(255), nullable=False, comment='切分方法')
    chunk_type = db.Column(db.String(255), nullable=False, comment='分段类型')
    chunk_format = db.Column(db.String(255), nullable=False, comment='分段格式')
    chunk_size = db.Column(db.Integer, nullable=False, comment='分段大小（kB）')
    chunk_raw_content = db.Column(db.Text, nullable=False, comment='分段原始内容')
    chunk_embedding_content = db.Column(db.Text, comment='分段嵌入内容')
    chunk_embedding_type = db.Column(db.String(255), comment='分段嵌入类型')
    chunk_embedding = db.Column(Vector, comment='分段嵌入向量')
    chunk_hit_counts = db.Column(db.Integer, default=0, comment='分块命中次数')
    status = db.Column(db.String(255), nullable=False, default='正常', comment='分段状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'split_method': self.split_method,
            'chunk_type': self.chunk_type,
            'chunk_format': self.chunk_format,
            'chunk_size': self.chunk_size,
            'chunk_raw_content': self.chunk_raw_content,
            'ref_id': self.ref_id,
            'chunk_embedding_content': self.chunk_embedding_content,
            'chunk_embedding_type': self.chunk_embedding_type,
            'chunk_embedding': self.chunk_embedding,
            'chunk_hit_counts': self.chunk_hit_counts,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class RagQueryLog(db.Model):
    """
    用于记录RAG查询日志
    """
    __tablename__ = 'rag_query_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    query_text = db.Column(db.Text, nullable=False, comment='查询文本')
    user_id = db.Column(db.Integer, nullable=False, comment='创建用户id')
    session_id = db.Column(db.Integer, nullable=True, comment='会话id')
    msg_id = db.Column(db.Integer, nullable=True, comment='问题id')
    task_id = db.Column(db.Integer, nullable=True, comment='任务id')
    ref_ids = db.Column(db.JSON, default=[], comment='文献列表')
    status = db.Column(db.String(255), nullable=False, comment='运行状态')
    trace_log = db.Column(db.Text, comment='运行日志')
    config = db.Column(db.JSON, default={}, comment='查询配置')
    result = db.Column(db.JSON, default={}, comment='查询结果')
    time_usage = db.Column(db.JSON, default={}, comment='查询时间消耗')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'query_text': self.query_text,
            "user_id": self.user_id,
            'session_id': self.session_id,
            'msg_id': self.msg_id,
            'task_id': self.task_id,
            'ref_ids': self.ref_ids,
            'status': self.status,
            'trace_log': self.trace_log,
            'config': self.config,
            'result': self.result,
            'time_usage': self.time_usage,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

