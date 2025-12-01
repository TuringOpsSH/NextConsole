from sqlalchemy.sql import func
from app.app import db


class AppMetaInfo(db.Model):
    """
    'ai应用信息表';
    """
    __tablename__ = 'app_meta_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_code = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    app_name = db.Column(db.Text, nullable=False)
    app_desc = db.Column(db.Text, default='')
    app_icon = db.Column(db.Text, default='images/logo.svg')
    app_type = db.Column(db.String(255), default='个人应用')
    app_default_assistant = db.Column(db.Integer)
    app_status = db.Column(db.String(255), default='创建中')
    app_source = db.Column(db.String(255), default='local', comment='ai应用来源')
    app_agent_api_url = db.Column(db.String(255), default='', comment='ai应用api接口url')
    app_agent_api_key = db.Column(db.String(255), default='', comment='ai应用api接口key')
    app_config = db.Column(db.JSON, default={}, comment='ai应用配置参数')
    environment = db.Column(db.String(255), default='开发')
    version = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'app_code': self.app_code,
            'user_id': self.user_id,
            'app_name': self.app_name,
            'app_desc': self.app_desc,
            'app_icon': self.app_icon,
            'app_type': self.app_type,
            "app_default_assistant": self.app_default_assistant,
            'app_status': self.app_status,
            'app_source': self.app_source,
            'app_config': self.app_config or {},
            'environment': self.environment,
            'version': self.version,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class AppAccessInfo(db.Model):
    """

) ENGINE=InnoDB COMMENT '应用授权表';

    """
    __tablename__ = 'app_access_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_code = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    user_code = db.Column(db.String(255))
    access_type = db.Column(db.String(255), nullable=False)
    access_name = db.Column(db.String(255), nullable=False)
    access_desc = db.Column(db.String(255), default='')
    access_status = db.Column(db.String(255), default='正常')
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'app_code': self.app_code,
            'company_id': self.company_id,
            'department_id': self.department_id,
            'user_id': self.user_id,
            'user_code': self.user_code,
            'access_type': self.access_type,
            'access_name': self.access_name,
            'access_desc': self.access_desc,
            'access_status': self.access_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class WorkFlowMetaInfo(db.Model):
    """
    '工作流元信息';
    """
    __tablename__ = 'workflow_meta_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    workflow_code = db.Column(db.String(255), nullable=False)
    workflow_name = db.Column(db.String(255), nullable=False)
    workflow_desc = db.Column(db.Text, nullable=False)
    workflow_icon = db.Column(db.Text, nullable=False)
    workflow_schema = db.Column(db.JSON, default={})
    workflow_edit_schema = db.Column(db.JSON, default={})
    workflow_is_main = db.Column(db.Boolean, default=False)
    workflow_status = db.Column(db.String(255), default='正常')
    environment = db.Column(db.String(255), default='开发')
    version = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'workflow_code': self.workflow_code,
            'workflow_name': self.workflow_name,
            'workflow_desc': self.workflow_desc,
            'workflow_icon': self.workflow_icon,
            'workflow_schema': self.workflow_schema,
            "workflow_edit_schema": self.workflow_edit_schema,
            'workflow_is_main': self.workflow_is_main,
            'workflow_status': self.workflow_status,
            'environment': self.environment,
            'version': self.version,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class AppWorkFlowRelation(db.Model):
    """
   '应用工作流关系表';
    """
    __tablename__ = 'app_workflow_relation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_code = db.Column(db.String(255), nullable=False)
    workflow_code = db.Column(db.String(255), nullable=False)
    rel_type = db.Column(db.String(255), default='使用')
    rel_desc = db.Column(db.Text, default='')
    rel_status = db.Column(db.String(255), default='正常')
    environment = db.Column(db.String(255), default='开发')
    version = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'app_code': self.app_code,
            'workflow_code': self.workflow_code,
            'rel_type': self.rel_type,
            'rel_desc': self.rel_desc,
            'rel_status': self.rel_status,
            'environment': self.environment,
            'version': self.version,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class WorkflowNodeInfo(db.Model):
    """
    '工作流节点信息表';
    """
    __tablename__ = 'workflow_node_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    workflow_id = db.Column(db.Integer, nullable=False)
    node_code = db.Column(db.String(255), default='')
    node_type = db.Column(db.String(255), default='')
    node_icon = db.Column(db.Text, default='')
    node_name = db.Column(db.String(255), default='')
    node_desc = db.Column(db.Text, default='')
    node_run_model_config = db.Column(db.JSON, default={
        'node_run_model': 'sync',
    })
    node_llm_code = db.Column(db.String(255), default='')
    node_llm_params = db.Column(db.JSON, default={})
    node_llm_system_prompt_template = db.Column(db.Text, default='')
    node_llm_user_prompt_template = db.Column(db.Text, default='')
    node_result_format = db.Column(db.String(255), default='text')
    node_result_params_json_schema = db.Column(db.JSON, default={
            "type": "object",
            "properties": {},
    })
    node_result_extract_separator = db.Column(db.String(255), default='')
    node_result_extract_quote = db.Column(db.String(255), default='')
    node_result_extract_columns = db.Column(db.JSON, default=[])
    node_result_template = db.Column(db.Text, default='')
    node_timeout = db.Column(db.Integer, default=600)
    node_retry_max = db.Column(db.Integer, default=3)
    node_retry_duration = db.Column(db.Integer, default=60)
    node_retry_model = db.Column(db.Integer, default=1)
    node_failed_solution = db.Column(db.String(255), default='exit')
    node_failed_template = db.Column(db.Text, default='')
    node_session_memory_size = db.Column(db.Integer, default=4)
    node_deep_memory = db.Column(db.Boolean, default=False)
    node_agent_nickname = db.Column(db.String(100), default='助手')
    node_agent_desc = db.Column(db.Text, default='助手')
    node_agent_avatar = db.Column(db.Text, default='images/logo.svg')
    node_agent_prologue = db.Column(db.Text, default='你好')
    node_agent_preset_question = db.Column(db.JSON, default=[])
    node_agent_tools = db.Column(db.JSON, default=[])
    node_input_params_json_schema = db.Column(db.JSON, default={
            "type": "object",
            "properties": {},
    })
    node_status = db.Column(db.String(255), default='正常')
    environment = db.Column(db.String(255), default='开发')
    version = db.Column(db.Integer, default=0)
    node_tool_api_url = db.Column(db.Text, default='', comment='api-url')
    node_tool_http_method = db.Column(db.String(255), default='POST', comment='api请求方式')
    node_tool_http_header = db.Column(db.JSON, default={
            "type": "object",
            "properties": {},
    }, comment='api请求头')
    node_tool_http_params = db.Column(db.JSON, default={
            "type": "object",
            "properties": {},
    }, comment='api请求参数')
    node_tool_http_body = db.Column(db.JSON, default={
            "type": "object",
            "properties": {},
    }, comment='api请求体')
    node_tool_http_body_type = db.Column(db.String(255), default='json', comment='api请求体类型')
    node_rag_resources = db.Column(db.JSON, default=[], comment='RAG资源')
    node_rag_ref_show = db.Column(db.Boolean, default=True, comment='RAG引用显示开关')
    node_rag_query_template = db.Column(db.Text, default='', comment='RAG查询模板')
    node_rag_recall_config = db.Column(db.JSON, default={}, comment='RAG召回配置')
    node_rag_rerank_config = db.Column(db.JSON, default={}, comment='RAG重排序配置')
    node_rag_web_search_config = db.Column(db.JSON, default={}, comment='RAG联网搜索配置')
    node_enable_message = db.Column(db.Boolean, default=False, comment='节点消息开关')
    node_message_schema_type = db.Column(db.String(100), comment='节点消息结构类型')
    node_message_schema = db.Column(db.JSON, default=[], comment='节点消息结构')
    node_file_reader_config = db.Column(db.JSON, default={}, comment='文档读取配置')
    node_file_splitter_config = db.Column(db.JSON, default={}, comment='文档分割配置')
    node_sub_workflow_config = db.Column(db.JSON, default={}, comment='子工作流配置')
    node_tool_configs = db.Column(db.JSON, default={}, comment='节点工具配置')
    node_variable_cast_config = db.Column(db.JSON, default={}, comment='节点变量类型转换配置')
    create_time = db.Column(db.DateTime, default=func.now())
    update_time = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'workflow_id': self.workflow_id,
            'node_code': self.node_code,
            'node_type': self.node_type,
            'node_icon': self.node_icon,
            'node_name': self.node_name,
            'node_desc': self.node_desc,
            'node_run_model_config': self.node_run_model_config,
            'node_llm_code': self.node_llm_code,
            'node_llm_params': self.node_llm_params,
            'node_llm_system_prompt_template': self.node_llm_system_prompt_template,
            'node_llm_user_prompt_template': self.node_llm_user_prompt_template,
            'node_result_format': self.node_result_format,
            'node_result_params_json_schema': self.node_result_params_json_schema,
            'node_result_extract_separator': self.node_result_extract_separator,
            'node_result_extract_quote': self.node_result_extract_quote,
            'node_result_extract_columns': self.node_result_extract_columns,
            'node_result_template': self.node_result_template,
            "node_timeout": self.node_timeout,
            'node_retry_max': self.node_retry_max,
            'node_retry_duration': self.node_retry_duration,
            'node_retry_model': self.node_retry_model,
            'node_failed_solution': self.node_failed_solution,
            'node_failed_template': self.node_failed_template,
            'node_session_memory_size': self.node_session_memory_size,
            'node_deep_memory': self.node_deep_memory,
            'node_agent_nickname': self.node_agent_nickname,
            'node_agent_desc': self.node_agent_desc,
            'node_agent_avatar': self.node_agent_avatar,
            'node_agent_prologue': self.node_agent_prologue,
            'node_agent_preset_question': self.node_agent_preset_question,
            'node_agent_tools': self.node_agent_tools,
            'node_input_params_json_schema': self.node_input_params_json_schema,
            'node_status': self.node_status,
            'environment': self.environment,
            'version': self.version,
            'node_tool_api_url': self.node_tool_api_url,
            'node_tool_http_method': self.node_tool_http_method,
            'node_tool_http_header': self.node_tool_http_header,
            'node_tool_http_params': self.node_tool_http_params,
            'node_tool_http_body': self.node_tool_http_body,
            'node_tool_http_body_type': self.node_tool_http_body_type,
            'node_rag_resources': self.node_rag_resources,
            'node_rag_query_template': self.node_rag_query_template,
            "node_rag_ref_show": self.node_rag_ref_show,
            'node_rag_recall_config': self.node_rag_recall_config,
            'node_rag_rerank_config': self.node_rag_rerank_config,
            'node_rag_web_search_config': self.node_rag_web_search_config,
            'node_enable_message': self.node_enable_message,
            'node_message_schema_type': self.node_message_schema_type,
            'node_message_schema': self.node_message_schema,
            'node_file_reader_config': self.node_file_reader_config,
            'node_file_splitter_config': self.node_file_splitter_config,
            'node_sub_workflow_config': self.node_sub_workflow_config,
            'node_tool_configs': self.node_tool_configs,
            'node_variable_cast_config': self.node_variable_cast_config,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class WorkFlowNodeInstance(db.Model):
    """
    '工作流节点实例';
    """
    __tablename__ = 'workflow_node_instance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    user_id = db.Column(db.Integer, nullable=False, comment='用户id')
    workflow_id = db.Column(db.Integer, nullable=False, comment='工作流id')
    workflow_node_id = db.Column(db.Integer, nullable=False, comment='工作节点id')
    workflow_node_code = db.Column(db.String(255), nullable=False, comment='工作节点编码')
    workflow_node_type = db.Column(db.String(255), nullable=False, comment='工作节点类型')
    workflow_node_icon = db.Column(db.Text, nullable=False, comment='工作节点图标')
    workflow_node_name = db.Column(db.String(255), nullable=False, comment='工作节点名称')
    workflow_node_desc = db.Column(db.Text, nullable=False, comment='工作节点描述')
    workflow_node_run_model_config = db.Column(db.JSON, default={})
    workflow_node_llm_code = db.Column(db.String(255), default='', comment='节点模型编号')
    workflow_node_llm_params = db.Column(db.JSON, default={}, comment='节点模型参数')
    workflow_node_ipjs = db.Column(db.JSON, default={
        "type": "object",
        "properties": {},
    }, comment='节点输入变量结构')
    workflow_node_llm_spt = db.Column(db.Text, default='', comment='系统提示词模板')
    workflow_node_llm_upt = db.Column(db.Text, default='', comment='用户提示词模板')
    workflow_node_result_format = db.Column(db.Text, default='', comment='输出数据格式')
    workflow_node_rpjs = db.Column(db.JSON, default={
        "type": "object",
        "properties": {},
    }, comment='输出变量结构')
    workflow_node_result_template = db.Column(db.Text, default='', comment='节点输出模板')
    workflow_node_timeout = db.Column(db.Integer, default=600, comment='节点超时时间')
    workflow_node_retry_max = db.Column(db.Integer, default=3, comment='节点最大重试次数')
    workflow_node_retry_duration = db.Column(db.Integer, default=60, comment='节点重试间隔')
    workflow_node_retry_model = db.Column(db.Integer, default=1, comment='节点重试模型，1-失败重试，2-成功重试')
    workflow_node_failed_solution = db.Column(db.String(255), default='', comment='节点失败策略')
    workflow_node_failed_template = db.Column(db.Text, default='', comment='节点失败模板')
    node_session_memory_size = db.Column(db.Integer, default=4, comment='会话记忆长度')
    node_deep_memory = db.Column(db.Boolean, default=False, comment='深度记忆开关')
    node_agent_tools = db.Column(db.JSON, default=[], comment='助手工具配置')
    workflow_node_tool_api_url = db.Column(db.Text, default='', comment='api-url')
    workflow_node_tool_http_method = db.Column(db.String(255), default='POST', comment='api请求方式')
    workflow_node_tool_http_header = db.Column(db.JSON, default={}, comment='api请求头')
    workflow_node_tool_http_params = db.Column(db.JSON, default={}, comment='api请求参数')
    workflow_node_tool_http_body = db.Column(db.JSON, default={}, comment='api请求体')
    workflow_node_tool_http_body_type = db.Column(db.String(255), default='json', comment='api请求体类型')
    workflow_node_rag_resources = db.Column(db.JSON, default=[], comment='RAG资源')
    workflow_node_rag_query_template = db.Column(db.Text, default='', comment='RAG查询模板')
    workflow_node_rag_ref_show = db.Column(db.Boolean, default=True, comment='RAG引用显示开关')
    workflow_node_rag_recall_config = db.Column(db.JSON, default={}, comment='RAG召回配置')
    workflow_node_rag_rerank_config = db.Column(db.JSON, default={}, comment='RAG重排序配置')
    workflow_node_rag_web_search_config = db.Column(db.JSON, default={}, comment='RAG联网搜索配置')
    workflow_node_enable_message = db.Column(db.Boolean, default=False, comment='节点消息开关')
    workflow_node_message_schema_type = db.Column(db.String(100), comment='节点消息结构类型')
    workflow_node_message_schema = db.Column(db.JSON, default=[], comment='节点消息结构')
    workflow_node_file_reader_config = db.Column(db.JSON, default={}, comment='文档读取配置')
    workflow_node_file_splitter_config = db.Column(db.JSON, default={}, comment='文档分割配置')
    workflow_node_sub_workflow_config = db.Column(db.JSON, default={}, comment='子工作流配置')
    workflow_node_tool_configs = db.Column(db.JSON, default={}, comment='节点工具配置')
    workflow_node_variable_cast_config = db.Column(db.JSON, default={}, comment='节点变量类型转换配置')
    session_id = db.Column(db.Integer, nullable=False, comment='会话id')
    qa_id = db.Column(db.Integer, nullable=False, comment='问答id')
    msg_id = db.Column(db.Integer, nullable=False, comment='消息id')
    task_status = db.Column(db.String(255), nullable=False, comment='任务状态')
    task_precondition = db.Column(db.JSON, default=[], comment='任务执行前置条件')
    task_downstream = db.Column(db.JSON, default=[], comment='任务下游')
    task_params = db.Column(db.JSON, default={}, comment='任务输入参数')
    task_prompt = db.Column(db.JSON, default=[], comment='任务提示词')
    task_retry_cnt = db.Column(db.Integer, default=0, comment='任务重试次数')
    task_result = db.Column(db.Text, default='', comment='任务结果')
    task_result_summary = db.Column(db.String(255), default='', comment='任务结果总结')
    task_trace_log = db.Column(db.Text, default='', comment='任务异常日志')
    task_token_used = db.Column(db.Integer, default=0, comment='任务使用的token数')
    begin_time = db.Column(db.DATETIME, comment='任务开始时间')
    end_time = db.Column(db.DATETIME, comment='任务结束时间')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "workflow_id": self.workflow_id,
            "workflow_node_id": self.workflow_node_id,
            "workflow_node_code": self.workflow_node_code,
            "workflow_node_type": self.workflow_node_type,
            "workflow_node_icon": self.workflow_node_icon,
            "workflow_node_name": self.workflow_node_name,
            "workflow_node_desc": self.workflow_node_desc,
            "workflow_node_run_model_config": self.workflow_node_run_model_config,
            "workflow_node_llm_code": self.workflow_node_llm_code,
            "workflow_node_llm_params": self.workflow_node_llm_params,
            "workflow_node_ipjs": self.workflow_node_ipjs,
            "workflow_node_llm_spt": self.workflow_node_llm_spt,
            "workflow_node_llm_upt": self.workflow_node_llm_upt,
            "workflow_node_result_format": self.workflow_node_result_format,
            "workflow_node_rpjs": self.workflow_node_rpjs,
            "workflow_node_result_template": self.workflow_node_result_template,
            "workflow_node_retry_max": self.workflow_node_retry_max,
            "workflow_node_retry_duration": self.workflow_node_retry_duration,
            "workflow_node_retry_model": self.workflow_node_retry_model,
            "workflow_node_failed_solution": self.workflow_node_failed_solution,
            "workflow_node_failed_template": self.workflow_node_failed_template,
            "node_session_memory_size": self.node_session_memory_size,
            "node_deep_memory": self.node_deep_memory,
            "node_agent_tools": self.node_agent_tools,
            "session_id": self.session_id,
            "qa_id": self.qa_id,
            "msg_id": self.msg_id,
            "task_status": self.task_status,
            "task_precondition": self.task_precondition,
            "task_downstream": self.task_downstream,
            "task_params": self.task_params,
            "task_prompt": self.task_prompt,
            "task_retry_cnt": self.task_retry_cnt,
            "task_result": self.task_result,
            "task_result_summary": self.task_result_summary,
            "task_trace_log": self.task_trace_log,
            "task_token_used": self.task_token_used,
            "workflow_node_timeout": self.workflow_node_timeout,
            "workflow_node_tool_api_url": self.workflow_node_tool_api_url,
            "workflow_node_tool_http_method": self.workflow_node_tool_http_method,
            "workflow_node_tool_http_header": self.workflow_node_tool_http_header,
            "workflow_node_tool_http_params": self.workflow_node_tool_http_params,
            "workflow_node_tool_http_body": self.workflow_node_tool_http_body,
            "workflow_node_tool_http_body_type": self.workflow_node_tool_http_body_type,
            "workflow_node_rag_resources": self.workflow_node_rag_resources,
            "workflow_node_rag_query_template": self.workflow_node_rag_query_template,
            "workflow_node_rag_ref_show": self.workflow_node_rag_ref_show,
            "workflow_node_rag_recall_config": self.workflow_node_rag_recall_config,
            "workflow_node_rag_rerank_config": self.workflow_node_rag_rerank_config,
            "workflow_node_rag_web_search_config": self.workflow_node_rag_web_search_config,
            "workflow_node_enable_message": self.workflow_node_enable_message,
            "workflow_node_message_schema": self.workflow_node_message_schema,
            "workflow_node_message_schema_type": self.workflow_node_message_schema_type,
            "workflow_node_file_reader_config": self.workflow_node_file_reader_config,
            "workflow_node_file_splitter_config": self.workflow_node_file_splitter_config,
            "workflow_node_sub_workflow_config": self.workflow_node_sub_workflow_config,
            "workflow_node_tool_configs": self.workflow_node_tool_configs,
            "workflow_node_variable_cast_config": self.workflow_node_variable_cast_config,
            "begin_time": self.begin_time.strftime('%Y-%m-%d %H:%M:%S') if self.begin_time else None,
            "end_time": self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "workflow_node_code": self.workflow_node_code,
            "workflow_node_id": self.workflow_node_id,
            "workflow_node_type": self.workflow_node_type,
            "workflow_node_icon": self.workflow_node_icon,
            "workflow_node_name": self.workflow_node_name,
            "workflow_node_desc": self.workflow_node_desc,
            "workflow_node_run_model_config": self.workflow_node_run_model_config,
            "workflow_node_llm_code": self.workflow_node_llm_code,
            "workflow_node_llm_params": self.workflow_node_llm_params,
            "workflow_node_ipjs": self.workflow_node_ipjs,
            "workflow_node_llm_spt": self.workflow_node_llm_spt,
            "workflow_node_llm_upt": self.workflow_node_llm_upt,
            "workflow_node_result_format": self.workflow_node_result_format,
            "workflow_node_rpjs": self.workflow_node_rpjs,
            "workflow_node_result_template": self.workflow_node_result_template,
        }


class WorkFlowTaskInfo(db.Model):
    """
    COMMENT '工作流任务信息表';
    """
    __tablename__ = 'workflow_task_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    user_id = db.Column(db.Integer, nullable=False, comment='用户id')
    session_id = db.Column(db.Integer, nullable=False, comment='会话id')
    qa_id = db.Column(db.Integer, nullable=False, comment='问答id')
    msg_id = db.Column(db.Integer, nullable=False, comment='消息id')
    task_type = db.Column(db.String(255), nullable=False, comment='任务类型')
    task_status = db.Column(db.String(255), nullable=False, comment='任务状态')
    task_assistant_id = db.Column(db.Integer, nullable=False, comment='任务助手')
    task_model_name = db.Column(db.String(255), default='', comment='任务助手模型')
    task_assistant_instruction = db.Column(db.Text, nullable=False, comment='任务助手指令')
    task_params = db.Column(db.JSON, default=dict, comment='任务输入参数')
    task_prompt = db.Column(db.JSON, default={}, comment='任务提示词')
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
