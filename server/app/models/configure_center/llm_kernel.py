from sqlalchemy.sql import func
from app.app import db


class LLMInstance(db.Model):
    """基模型实例信息表
    """
    __tablename__ = 'llm_instance_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    llm_code = db.Column(db.String(255), comment='基模型实例编号')
    llm_name = db.Column(db.String(255), nullable=False, comment='基模型名称')
    llm_label = db.Column(db.String(255), nullable=False, comment='模型显示标签')
    user_id = db.Column(db.Integer, nullable=False, comment='创建用户')
    llm_api_secret_key = db.Column(db.String(1000), comment='基模型认证钥匙')
    llm_api_access_key = db.Column(db.String(1000), comment='基模型访问钥匙')
    llm_type = db.Column(db.String(255), comment='基模型类型')
    llm_desc = db.Column(db.Text, comment='基模型描述')
    llm_icon = db.Column(db.Text, comment='基模型图标')
    llm_tags = db.Column(db.JSON, comment='基模型特征标签')
    llm_company = db.Column(db.String(255), comment='基模型厂商')
    llm_is_proxy = db.Column(db.Boolean, comment='是否代理', default=False)
    llm_base_url = db.Column(db.String(255), comment='基模型基础url')
    llm_proxy_url = db.Column(db.String(255), comment='基模型代理url')
    llm_status = db.Column(db.String(255), comment='实例状态')
    llm_source = db.Column(db.String(255), comment='基模型来源')
    llm_is_public = db.Column(db.Boolean, comment='是否公开', default=False)
    frequency_penalty = db.Column(db.Float, comment='频率惩罚系数')
    max_tokens = db.Column(db.Integer, comment='最大令牌数')
    n = db.Column(db.Integer, comment='聊天完成选项个数')
    presence_penalty = db.Column(db.Float, comment='出现处罚系数')
    response_format = db.Column(db.JSON, comment='响应格式')
    stop = db.Column(db.JSON, comment='停止词')
    stream = db.Column(db.Boolean, comment='流式开关', default=False)
    temperature = db.Column(db.Float, comment='模型温度')
    top_p = db.Column(db.Float, comment='核采样系数')
    is_std_openai = db.Column(db.Boolean, default=True, comment='是否支持openai-sdk')
    support_vis = db.Column(db.Boolean, default=False, comment='是否支持视觉')
    support_file = db.Column(db.Boolean, default=False, comment='是否支持文件')
    extra_headers = db.Column(db.JSON, comment='请求头', default={})
    extra_body = db.Column(db.JSON, comment='请求体', default={})
    use_default = db.Column(db.Boolean, default=True, comment='是否使用默认配置')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "llm_code": self.llm_code,
            "llm_name": self.llm_name,
            "llm_label": self.llm_label,
            "user_id": self.user_id,
            "llm_type": self.llm_type,
            "llm_desc": self.llm_desc,
            "llm_tags": self.llm_tags,
            "llm_company": self.llm_company,
            "llm_is_proxy": self.llm_is_proxy,
            "llm_base_url": self.llm_base_url,
            "llm_proxy_url": self.llm_proxy_url,
            "llm_status": self.llm_status,
            "llm_source": self.llm_source,
            "llm_is_public": self.llm_is_public,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "frequency_penalty": self.frequency_penalty,
            "max_tokens": self.max_tokens,
            "n": self.n,
            "presence_penalty": self.presence_penalty,
            "response_format": self.response_format,
            "stop": self.stop,
            "stream": self.stream,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "is_std_openai": self.is_std_openai,
            "support_file": self.support_file,
            "support_vis": self.support_vis,
            "extra_headers": self.extra_headers,
            "extra_body": self.extra_body,
            "use_default": self.use_default,
        }

    def show_info(self):
        return {
            "user_id": self.user_id,
            "llm_code": self.llm_code,
            "llm_name": self.llm_name,
            "llm_company": self.llm_company if self.llm_company else "未知厂商",
            "llm_label": self.llm_label if self.llm_label else "",
            "llm_type": self.llm_type,
            "llm_desc": self.llm_desc,
            "llm_icon": self.llm_icon,
            "llm_status": self.llm_status,
            "llm_is_proxy": self.llm_is_proxy,
            "support_vis": self.support_vis,
            "support_file": self.support_file,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class LLMInstanceAuthorizeInfo(db.Model):
    """
    基模型实例授权信息表
    """
    __tablename__ = 'llm_instance_authorize_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    user_id = db.Column(db.Integer, nullable=False, comment='用户id')
    model_id = db.Column(db.Integer, nullable=False, comment='模型id')
    auth_colleague_id = db.Column(db.Integer, comment='被授权用户id')
    auth_department_id = db.Column(db.Integer, comment='被授权部门id')
    auth_company_id = db.Column(db.Integer, comment='被授权公司id')
    auth_friend_id = db.Column(db.Integer, comment='被授权联系人id')
    auth_type = db.Column(db.String(255), nullable=False, comment='授权类型')
    auth_status = db.Column(db.String(255), nullable=False, comment='授权状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "model_id": self.model_id,
            "auth_colleague_id": self.auth_colleague_id,
            "auth_department_id": self.auth_department_id,
            "auth_company_id": self.auth_company_id,
            "auth_friend_id": self.auth_friend_id,
            "auth_type": self.auth_type,
            "auth_status": self.auth_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class LLMSupplierInfo(db.Model):
    """
    基模型厂商信息表
    """
    __tablename__ = 'llm_supplier_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    supplier_code = db.Column(db.String(255), nullable=False, comment='基模型厂商编号')
    supplier_name = db.Column(db.String(255), nullable=False, comment='基模型厂商名称')
    supplier_desc = db.Column(db.Text, comment='基模型厂商描述')
    supplier_icon = db.Column(db.Text, comment='基模型厂商图标')
    supplier_type = db.Column(db.String(10), comment='基模型厂商类型')
    supplier_website = db.Column(db.String(255), comment='基模型厂商官网')
    supplier_models = db.Column(db.JSON, comment='基模型厂商支持的模型列表')
    supplier_api_url = db.Column(db.Text, comment='基模型厂商API地址')
    supplier_status = db.Column(db.String(255), comment='基模型厂商状态', default='正常')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "supplier_code": self.supplier_code,
            "supplier_name": self.supplier_name,
            "supplier_desc": self.supplier_desc,
            "supplier_icon": self.supplier_icon,
            "supplier_website": self.supplier_website,
            "supplier_models": self.supplier_models,
            "supplier_api_url": self.supplier_api_url,
            "supplier_type": self.supplier_type,
            "supplier_status": self.supplier_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        return {
            "id": self.id,
            "supplier_code": self.supplier_code,
            "supplier_name": self.supplier_name,
            "supplier_desc": self.supplier_desc,
            "supplier_icon": self.supplier_icon,
            "supplier_type": self.supplier_type,
        }

