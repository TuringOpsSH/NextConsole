from sqlalchemy.sql import func
from app.app import db


class NextSearchSessionKgRelation(db.Model):
    """
    """
    __bind_key__ = 'business'
    __tablename__ = 'next_search_session_kg_relation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    session_id = db.Column(db.Integer, nullable=False, comment='会话id')
    kg_code = db.Column(db.String(255), nullable=False, comment='知识库编号')
    rel_status = db.Column(db.String(255), comment='关系状态', default='正常')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "kg_code": self.kg_code,
            "rel_status": self.rel_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class NextSearchMsgDocRelation(db.Model):
    """

    """
    __bind_key__ = 'business'
    __tablename__ = 'next_search_msg_doc_relation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    msg_id = db.Column(db.Integer, nullable=False, comment='消息id')
    ref_text = db.Column(db.Text, comment='参考文本')
    recall_score = db.Column(db.Float, comment='召回分值')
    rerank_score = db.Column(db.Float, comment='重排分值')
    source = db.Column(db.String(255), comment='来源id')
    source_type = db.Column(db.String(255), comment='来源类型')
    rel_status = db.Column(db.String(255), comment='关系状态', default='正常')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "msg_id": self.msg_id,
            "ref_text": self.ref_text,
            "recall_score": self.recall_score,
            "rerank_score": self.rerank_score,
            "source": self.source,
            "source_type": self.source_type,
            "rel_status": self.rel_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class NextSearchRecommendQuestion(db.Model):
    """
    """
    __bind_key__ = 'business'
    __tablename__ = 'next_search_recommend_question'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='推荐记录id')
    msg_id = db.Column(db.Integer, nullable=True, comment='问题id')
    msg_content = db.Column(db.Text, nullable=False, comment='问题内容')
    recommend_question = db.Column(db.Text, nullable=False, comment='推荐问题')
    is_click = db.Column(db.Integer, nullable=False, default=0, comment='是否采用')
    model = db.Column(db.String(255), nullable=False, default="deepseek-chat", comment='推荐问题模型')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    def to_dict(self):
        return {
            "id": self.id,
            "qa_id": self.msg_id,
            "msg_content": self.msg_content,
            "recommend_question": self.recommend_question,
            "is_click": self.is_click,
            "model": self.model,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class SessionShareInfo(db.Model):
    """
    """
    __bind_key__ = 'business'
    __tablename__ = 'session_share_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    session_id = db.Column(db.Integer, nullable=False, comment='session_id')
    share_token = db.Column(db.String(255), nullable=False, comment='分享token')
    share_duration = db.Column(db.Integer, default=0, comment='分享时限（秒）')
    share_endtime = db.Column(db.TIMESTAMP, comment='分享终止时间')
    view_cnt = db.Column(db.Integer, default=0, nullable=False, comment='浏览次数统计')
    invite_cnt = db.Column(db.Integer, default=0, nullable=False, comment='引流次数统计')
    last_view_time = db.Column(db.TIMESTAMP, comment='上一次浏览时间')
    share_status = db.Column(db.String(255), default="正常", nullable=False, comment='分享状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "share_token": self.share_token,
            "share_duration": self.share_duration,
            "share_endtime": self.share_endtime,
            "view_cnt": self.view_cnt,
            "invite_cnt": self.invite_cnt,
            "last_view_time": self.last_view_time,
            "share_status": self.share_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class WorkFlowTaskInfo(db.Model):
    """
    CREATE TABLE IF NOT EXISTS `workflow_task_info` (
  `id` INTEGER NOT NULL AUTO_INCREMENT COMMENT '自增id',
 `user_id` INTEGER NOT NULL COMMENT '用户id',
 `session_id` INTEGER NOT NULL COMMENT '会话id',
 `qa_id` INTEGER NOT NULL COMMENT '问答id',
 `msg_id` INTEGER NOT NULL COMMENT '消息id',
 `task_type` VARCHAR(255) NOT NULL COMMENT '任务类型',
 `task_status` VARCHAR(255) NOT NULL COMMENT '任务状态',
 `task_assistant_id` INTEGER NOT NULL COMMENT '任务助手',
 `task_model_name` VARCHAR(255) NOT NULL COMMENT '任务助手模型',
 `task_assistant_instruction` text NOT NULL COMMENT '任务助手指令',
 `task_params` text NOT NULL COMMENT '任务输入参数',
 `task_prompt` text NOT NULL COMMENT '任务提示词',
 `task_result` mediumtext  COMMENT '任务结果',
 `task_precondition` TEXT NOT NULL COMMENT '任务执行前置条件',
 `begin_time` timestamp COMMENT '任务开始时间',
 `end_time` timestamp COMMENT '任务结束时间',
 `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
 `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
 PRIMARY KEY (`id`),
 FOREIGN KEY (`user_id`) REFERENCES user_info(user_id) ON DELETE CASCADE,
    FOREIGN KEY (`session_id`) REFERENCES next_console_session_info(id) ON DELETE CASCADE,
    FOREIGN KEY (`qa_id`) REFERENCES next_console_qa_info(qa_id) ON DELETE CASCADE,
    FOREIGN KEY (`msg_id`) REFERENCES next_console_llm_message(msg_id) ON DELETE CASCADE,
    FOREIGN KEY (`task_assistant_id`) REFERENCES assistant_info(id) ON DELETE CASCADE

) ENGINE=InnoDB COMMENT '工作流任务信息表';
    """
    __bind_key__ = 'business'
    __tablename__ = 'workflow_task_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    user_id = db.Column(db.Integer, nullable=False, comment='用户id')
    session_id = db.Column(db.Integer, nullable=False, comment='会话id')
    qa_id = db.Column(db.Integer, nullable=False, comment='问答id')
    msg_id = db.Column(db.Integer, nullable=False, comment='消息id')
    task_type = db.Column(db.String(255), nullable=False, comment='任务类型')
    task_status = db.Column(db.String(255), nullable=False, comment='任务状态')
    task_assistant_id = db.Column(db.Integer, nullable=False, comment='任务助手')
    task_model_name = db.Column(db.String(255), nullable=False, comment='任务助手模型')
    task_assistant_instruction = db.Column(db.Text, nullable=False, comment='任务助手指令')
    task_params = db.Column(db.JSON, nullable=False, comment='任务输入参数')
    task_prompt = db.Column(db.JSON, nullable=False, comment='任务提示词')
    task_result = db.Column(db.Text, comment='任务结果')
    task_precondition = db.Column(db.Text, comment='任务执行前置条件')
    begin_time = db.Column(db.TIMESTAMP, comment='任务开始时间')
    end_time = db.Column(db.TIMESTAMP, comment='任务结束时间')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "qa_id": self.qa_id,
            "msg_id": self.msg_id,
            "task_type": self.task_type,
            "task_status": self.task_status,
            "task_assistant_id": self.task_assistant_id,
            "task_model_name": self.task_model_name,
            "task_assistant_instruction": self.task_assistant_instruction,
            "task_params": self.task_params,
            "task_prompt": self.task_prompt,
            "task_result": self.task_result,
            "task_precondition": self.task_precondition,
            "begin_time": self.begin_time.strftime('%Y-%m-%d %H:%M:%S') if self.begin_time else None,
            "end_time": self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class SearchMsgFeedBack(db.Model):
    """
    CREATE TABLE IF NOT EXISTS `search_msg_feedback` (
 `id` INTEGER NOT NULL COMMENT '自增id',
 `msg_id` INTEGER NOT NULL COMMENT '消息id',
 `feedback_type` VARCHAR(255) NOT NULL COMMENT '反馈类型',
 `feedback_desc` TEXT NOT NULL COMMENT '反馈描述',
 `feedback_status` VARCHAR(255) NOT NULL COMMENT '反馈状态',
 `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
 `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
 PRIMARY KEY (`id`),
 FOREIGN KEY (`msg_id`) REFERENCES next_console_llm_message(msg_id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT '用户反馈意见表';
    """
    __bind_key__ = 'business'
    __tablename__ = 'search_msg_feedback'
    id = db.Column(db.Integer, primary_key=True, comment='自增id')
    msg_id = db.Column(db.Integer, nullable=False, comment='消息id')
    feedback_type = db.Column(db.String(255), nullable=False, comment='反馈类型')
    feedback_desc = db.Column(db.Text, nullable=False, default="", comment='反馈描述')
    feedback_status = db.Column(db.String(255), nullable=False, default="正常", comment='反馈状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "msg_id": self.msg_id,
            "feedback_type": self.feedback_type,
            "feedback_desc": self.feedback_desc,
            "feedback_status": self.feedback_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }