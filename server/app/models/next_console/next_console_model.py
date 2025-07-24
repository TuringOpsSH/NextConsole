from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint
from app.app import db


class NextConsoleSession(db.Model):
    __tablename__ = 'next_console_session_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    session_topic = db.Column(db.String(255), nullable=False)
    session_status = db.Column(db.String(255), nullable=False, default="新建")
    session_remark = db.Column(db.Integer, nullable=False, default=0, comment='会话备注开关')
    session_vis = db.Column(db.Boolean, nullable=False, default=True)
    session_favorite = db.Column(db.Boolean, nullable=False, default=False)
    session_like_cnt = db.Column(db.Integer, nullable=False, default=0)
    session_dislike_cnt = db.Column(db.Integer, nullable=False, default=0)
    session_update_cnt = db.Column(db.Integer, nullable=False, default=0)
    session_share_cnt = db.Column(db.Integer, nullable=False, default=0)
    session_assistant_id = db.Column(db.Integer)
    session_shop_assistant_id = db.Column(db.Integer)
    session_task_id = db.Column(db.String(255))
    session_task_type = db.Column(db.String(255))
    session_source = db.Column(db.String(255))
    session_code = db.Column(db.String(40))
    session_search_engine_switch = db.Column(db.Boolean, default=False)
    session_search_engine_resource_type = db.Column(db.String(255), default="search")
    session_search_engine_language_type = db.Column(db.JSON, default={})
    session_local_resource_switch = db.Column(db.Boolean, default=False)
    session_local_resource_use_all = db.Column(db.Boolean, default=True)
    session_attachment_image_switch = db.Column(db.Boolean, default=False)
    session_attachment_file_switch = db.Column(db.Boolean, default=False)
    session_attachment_webpage_switch = db.Column(db.Boolean, default=False)
    session_llm_code = db.Column(db.String(255))
    session_customer_score = db.Column(db.Float, comment='会话客户评分')
    session_customer_evaluation = db.Column(db.Text, comment='会话客户评价')
    session_evaluation_close = db.Column(db.Boolean, default=False, comment='会话评价关闭')
    session_cancel_reason = db.Column(db.Text, comment='会话取消原因')
    session_task_params_schema = db.Column(db.JSON, default={}, comment='任务参数schema')
    session_task_params = db.Column(db.JSON, default={}, comment='任务参数')
    create_time = db.Column(db.DateTime, default=func.now(), comment='接受时间')
    update_time = db.Column(db.DateTime, default=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_topic": self.session_topic,
            "session_status": self.session_status,
            "session_remark": self.session_remark,
            "session_vis": self.session_vis,
            "session_favorite": self.session_favorite,
            "session_like_cnt": self.session_like_cnt,
            "session_dislike_cnt": self.session_dislike_cnt,
            "session_update_cnt": self.session_update_cnt,
            "session_share_cnt": self.session_share_cnt,
            "session_assistant_id": self.session_assistant_id,
            "session_shop_assistant_id": self.session_shop_assistant_id,
            "session_task_id": self.session_task_id,
            "session_task_type": self.session_task_type,
            "session_source": self.session_source,
            "session_code": self.session_code,
            "session_search_engine_switch": self.session_search_engine_switch,
            "session_search_engine_resource_type": self.session_search_engine_resource_type,
            "session_search_engine_language_type": self.session_search_engine_language_type,
            "session_local_resource_switch": self.session_local_resource_switch,
            "session_local_resource_use_all": self.session_local_resource_use_all,
            "session_attachment_image_switch": self.session_attachment_image_switch,
            "session_attachment_file_switch": self.session_attachment_file_switch,
            "session_attachment_webpage_switch": self.session_attachment_webpage_switch,
            "session_llm_code": self.session_llm_code,
            "session_customer_score": self.session_customer_score,
            "session_customer_evaluation": self.session_customer_evaluation,
            "session_evaluation_close": self.session_evaluation_close,
            "session_cancel_reason": self.session_cancel_reason,
            "session_task_params_schema": self.session_task_params_schema,
            "session_task_params": self.session_task_params,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class NextConsoleQa(db.Model):
    __tablename__ = 'next_console_qa_info'
    qa_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('next_console_session_info.id'), nullable=False)
    qa_del = db.Column(db.Boolean, nullable=False, default=False)
    qa_status = db.Column(db.String(255), nullable=False, default="新建")
    qa_topic = db.Column(db.Text, nullable=False, default="未命名")
    qa_is_cut_off = db.Column(db.Boolean, default=False, comment='问题是否被截断')
    create_time = db.Column(db.DateTime, default=func.now(), comment='接受时间')
    update_time = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            "qa_id": self.qa_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "qa_del": self.qa_del,
            "qa_status": self.qa_status,
            "qa_topic": self.qa_topic,
            "qa_is_cut_off": self.qa_is_cut_off,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class NextConsoleMessage(db.Model):
    __tablename__ = 'next_console_llm_message'
    msg_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    assistant_id = db.Column(db.Integer, )
    qa_id = db.Column(db.Integer)
    msg_format = db.Column(db.String(255), default='text')
    msg_llm_type = db.Column(db.String(255), default='')
    msg_role = db.Column(db.String(255), nullable=False)
    msg_prompt = db.Column(db.JSON, default={})
    msg_content = db.Column(db.Text, nullable=False)
    msg_inner_content = db.Column(db.JSON)
    reasoning_content = db.Column(db.Text, default='')
    msg_token_used = db.Column(db.Integer, default=0)
    msg_time_used = db.Column(db.Float, default=0)
    msg_remark = db.Column(db.Integer, nullable=False, default=0)
    msg_del = db.Column(db.Integer, nullable=False, default=0)
    msg_version = db.Column(db.Integer, nullable=False, default=0)
    msg_parent_id = db.Column(db.Integer)
    msg_is_cut_off = db.Column(db.Boolean, default=False, comment='消息是否被截断')
    task_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=func.now(), comment='接受时间')
    update_time = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        res = {
            "msg_id": self.msg_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "qa_id": self.qa_id,
            "assistant_id": self.assistant_id,
            "msg_format": self.msg_format,
            "msg_llm_type": self.msg_llm_type,
            "msg_role": self.msg_role,
            "msg_prompt": self.msg_prompt,
            "msg_content": self.msg_content,
            "msg_inner_content": self.msg_inner_content,
            "reasoning_content": self.reasoning_content,
            "msg_token_used": self.msg_token_used,
            "msg_time_used": self.msg_time_used,
            "msg_remark": self.msg_remark,
            "msg_del": self.msg_del,
            "msg_version": self.msg_version,
            "msg_parent_id": self.msg_parent_id,
            "msg_is_cut_off": self.msg_is_cut_off,
            "task_id": self.task_id,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return res


class NextConsoleRecommendQuestion(db.Model):
    """
    """
    __tablename__ = 'next_console_recommend_question'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='推荐记录id')
    msg_id = db.Column(db.Integer, nullable=True, comment='问题id')
    msg_content = db.Column(db.Text, nullable=False, comment='问题内容')
    recommend_question = db.Column(db.Text, nullable=False, comment='推荐问题')
    is_click = db.Column(db.Integer, nullable=False, default=0, comment='是否采用')
    model = db.Column(db.String(255), nullable=False, default="deepseek-chat", comment='推荐问题模型')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            "id": self.id,
            "msg_id": self.msg_id,
            "msg_content": self.msg_content,
            "recommend_question": self.recommend_question,
            "is_click": self.is_click,
            "model": self.model,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        
        return {
            "id": self.id,
            "msg_id": self.msg_id,
            "msg_content": self.msg_content,
            "recommend_question": self.recommend_question,
            "is_click": self.is_click,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class SessionAttachmentRelation(db.Model):
    """
    会话附件关系表

    """
    __tablename__ = 'session_attachment_relation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    session_id = db.Column(db.Integer, nullable=False, comment='会话id')
    qa_id = db.Column(db.Integer, comment='qa_id')
    msg_id = db.Column(db.Integer, comment='消息id')
    resource_id = db.Column(db.Integer, nullable=False, comment='资源id')
    attachment_source = db.Column(db.String(100), nullable=False, comment='附件来源')
    rel_status = db.Column(db.String(255), default="正常", comment='关系状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            "id": self.id,
            "session_id": self.session_id,
            "qa_id": self.qa_id,
            "msg_id": self.msg_id,
            "resource_id": self.resource_id,
            "attachment_source": self.attachment_source,
            "rel_status": self.rel_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        
        return {
            "id": self.id,
            "session_id": self.session_id,
            "qa_id": self.qa_id,
            "msg_id": self.msg_id,
            "resource_id": self.resource_id,
            "attachment_source": self.attachment_source,
            "rel_status": self.rel_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }