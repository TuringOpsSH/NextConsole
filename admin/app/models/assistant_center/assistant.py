from sqlalchemy.sql import func
from app.app import db


class Assistant(db.Model):
    """
    """
    __tablename__ = 'assistant_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    assistant_name = db.Column(db.String(255), nullable=False, comment='助手名称')
    assistant_desc = db.Column(db.Text, nullable=False, comment='助手描述')
    assistant_tags = db.Column(db.JSON, nullable=False, comment='助手标签')
    assistant_status = db.Column(db.String(255), nullable=False, comment='助手状态')
    assistant_role_prompt = db.Column(db.Text, nullable=False, comment='助手定义')
    assistant_avatar = db.Column(db.String(255), nullable=False, comment='助手头像')
    assistant_title = db.Column(db.String(255), nullable=False, comment='助手标题')
    assistant_language = db.Column(db.String(255), nullable=False, comment='助手语言')
    assistant_voice = db.Column(db.String(255), nullable=False, comment='助手声音')
    assistant_memory_size = db.Column(db.Integer, default=4, comment='助手记忆大小')
    assistant_prologue = db.Column(db.Text, default="", comment='助手序言')
    assistant_preset_question = db.Column(db.JSON, default=[], comment='助手预设问题')
    assistant_model_name = db.Column(db.String(255), nullable=False, comment='助手模型类型')
    assistant_model_code = db.Column(db.String(255), nullable=False, comment='助手模型编号')
    assistant_model_temperature = db.Column(db.Float, nullable=False, comment='助手模型温度')
    rag_miss = db.Column(db.Integer, default=1, comment='rag未命中应对')
    rag_miss_answer = db.Column(db.Text, default="", comment='rag未命中应对文本')
    rag_factor = db.Column(db.Float, default=0.75, comment='混合检索系数')
    rag_relevant_threshold = db.Column(db.Float, default=0.25, comment='语义相关度阈值')
    workflow_flag = db.Column(db.Boolean, default=False, comment='工作流标记')
    workflow = db.Column(db.JSON, comment='工作流')
    assistant_avatar_source = db.Column(db.Text, default="", comment='助手头像来源')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "assistant_name": self.assistant_name,
            "assistant_desc": self.assistant_desc,
            "assistant_tags": self.assistant_tags,
            "assistant_status": self.assistant_status,
            "assistant_role_prompt": self.assistant_role_prompt,
            "assistant_avatar": self.assistant_avatar,
            "assistant_language": self.assistant_language,
            "assistant_voice": self.assistant_voice,
            "assistant_memory_size": self.assistant_memory_size,
            "assistant_prologue": self.assistant_prologue,
            "assistant_preset_question": self.assistant_preset_question,
            "assistant_model_name": self.assistant_model_name,
            "assistant_model_code": self.assistant_model_code,
            "assistant_model_temperature": self.assistant_model_temperature,
            "rag_miss": self.rag_miss,
            "rag_miss_answer": self.rag_miss_answer,
            "rag_factor": self.rag_factor,
            "rag_relevant_threshold": self.rag_relevant_threshold,
            "workflow_flag": self.workflow_flag,
            "workflow": self.workflow,
            "assistant_avatar_source": self.assistant_avatar_source,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        return {
            "id": self.id,
            "assistant_name": self.assistant_name,
            "assistant_desc": self.assistant_desc,
            "assistant_title": self.assistant_title,
            "assistant_tags": self.assistant_tags,
            "assistant_status": self.assistant_status,
            "assistant_avatar": self.assistant_avatar,
        }


class UserAssistantRelation(db.Model):
    """
    用户助手关系表
    """

    __tablename__ = 'user_assistant_relation'
    id = db.Column(db.Integer, primary_key=True, comment='自增')
    user_id = db.Column(db.Integer, nullable=False, comment='用户')
    assistant_id = db.Column(db.Integer, nullable=False, comment='助手')
    rel_type = db.Column(db.String(255), default='服务中', comment='关系类型')
    rel_value = db.Column(db.Double, comment='关系值')
    rel_status = db.Column(db.String(255), default='正常', comment='关系状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "assistant_id": self.assistant_id,
            "rel_type": self.rel_type,
            "rel_value": self.rel_value,
            "rel_status": self.rel_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class AssistantRunInfo(db.Model):
    """

    """
    __tablename__ = 'assistant_run_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    assistant_id = db.Column(db.Integer, nullable=False, comment='助手id')
    indicator_name = db.Column(db.String(255), nullable=False, comment='指标名称')
    indicator_desc = db.Column(db.String(255), nullable=False, comment='指标描述')
    indicator_type = db.Column(db.String(255), nullable=False, comment='指标类型')
    indicator_value = db.Column(db.Double, nullable=False, comment='指标值')
    begin_time = db.Column(db.TIMESTAMP, nullable=False, comment='开始时间')
    end_time = db.Column(db.TIMESTAMP, nullable=False, comment='结束时间')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "assistant_id": self.assistant_id,
            "indicator_name": self.indicator_name,
            "indicator_desc": self.indicator_desc,
            "indicator_type": self.indicator_type,
            "indicator_value": self.indicator_value,
            "begin_time": self.begin_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class AssistantKgRelation(db.Model):

    __tablename__ = 'assistant_kg_relation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='关系id')
    assistant_id = db.Column(db.Integer, nullable=False, comment='助手id')
    kg_code = db.Column(db.String(255), nullable=False, comment='知识库id')
    rel_type = db.Column(db.String(255), comment='关系类型')
    rel_value = db.Column(db.String(255), comment='关系值')
    rel_status = db.Column(db.String(255), comment='关系状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "assistant_id": self.assistant_id,
            "kg_code": self.kg_code,
            "rel_type": self.rel_type,
            "rel_value": self.rel_value,
            "rel_status": self.rel_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class AssistantInstruction(db.Model):
    __tablename__ = 'assistant_instruction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='指令id')
    user_id = db.Column(db.Integer, comment='用户id')
    assistant_id = db.Column(db.Integer, nullable=False, comment='助手id')
    instruction_name = db.Column(db.String(255), nullable=False, comment='指令名称')
    instruction_desc = db.Column(db.Text, default="", comment='指令描述')
    instruction_type = db.Column(db.String(255), default="llm", comment='指令类型')
    instruction_system_prompt_template = db.Column(db.Text, default="", comment='系统提示模板')
    instruction_user_prompt_template = db.Column(db.Text, default="", comment='用户提示模板')
    instruction_result_template = db.Column(db.Text, default="", comment='结果模板')
    instruction_system_prompt_params_json_schema = db.Column(db.JSON, comment='系统提示参数json schema')
    instruction_user_prompt_params_json_schema = db.Column(db.JSON, comment='用户提示参数json schema')
    instruction_result_json_schema = db.Column(db.JSON, comment='结果json schema')
    instruction_result_extract_format = db.Column(db.String(255), default="json", comment='结果提取格式')
    instruction_result_extract_separator = db.Column(db.String(255), default=",", comment='结果提取分隔符')
    instruction_result_extract_quote = db.Column(db.String(255), comment='结果提取引号')
    instruction_result_extract_columns = db.Column(db.JSON, comment='结果提取列')
    instruction_history_length = db.Column(db.Integer, default=0, comment='指令历史长度')
    instruction_temperature = db.Column(db.Float, default=0, comment='指令温度')
    instruction_max_tokens = db.Column(db.Integer, default=0, comment='指令最大token')
    instruction_status = db.Column(db.String(255), default="正常", comment='指令状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "assistant_id": self.assistant_id,
            "instruction_name": self.instruction_name,
            "instruction_type": self.instruction_type,
            "instruction_desc": self.instruction_desc,
            "instruction_system_prompt_template": self.instruction_system_prompt_template,
            "instruction_user_prompt_template": self.instruction_user_prompt_template,
            "instruction_result_template": self.instruction_result_template,
            "instruction_system_prompt_params_json_schema": self.instruction_system_prompt_params_json_schema,
            "instruction_user_prompt_params_json_schema": self.instruction_user_prompt_params_json_schema,
            "instruction_result_json_schema": self.instruction_result_json_schema,
            "instruction_result_extract_format": self.instruction_result_extract_format,
            "instruction_result_extract_separator": self.instruction_result_extract_separator,
            "instruction_result_extract_quote": self.instruction_result_extract_quote,
            "instruction_result_extract_columns": self.instruction_result_extract_columns,
            "instruction_status": self.instruction_status,
            "instruction_history_length": self.instruction_history_length,
            "instruction_temperature": self.instruction_temperature,
            "instruction_max_tokens": self.instruction_max_tokens,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
