from app.app import db
from sqlalchemy.sql import func


class CompanyInfo(db.Model):
    """
      '公司信息表';
    """
    __tablename__ = 'company_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    parent_company_id = db.Column(db.Integer, comment='父企业id')
    company_code = db.Column(db.String(255), nullable=False, comment='企业编号')
    company_name = db.Column(db.String(255), nullable=False, comment='企业名称')
    company_country = db.Column(db.String(255), default="", comment='企业归属国家')
    company_area = db.Column(db.String(255), default="", comment='企业归属地区')
    company_industry = db.Column(db.Text, default="", comment='企业行业')
    company_scale = db.Column(db.Text, default="", comment='企业规模')
    company_desc = db.Column(db.Text, default="", comment='企业介绍')
    company_address = db.Column(db.Text, default="", comment='企业地址')
    company_phone = db.Column(db.String(255), default="", comment='企业电话')
    company_email = db.Column(db.String(255), default="", comment='企业邮箱')
    company_website = db.Column(db.Text, default="", comment='企业网站')
    company_logo = db.Column(db.Text, default="", comment='企业logo')
    company_type = db.Column(db.String(255), default="", comment='企业类型')
    company_status = db.Column(db.String(255), default="正常", comment='公司状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'parent_company_id': self.parent_company_id,
            'company_code': self.company_code,
            'company_name': self.company_name,
            'company_country': self.company_country,
            'company_area': self.company_area,
            'company_industry': self.company_industry,
            'company_scale': self.company_scale,
            'company_desc': self.company_desc,
            'company_address': self.company_address,
            'company_phone': self.company_phone,
            'company_email': self.company_email,
            'company_website': self.company_website,
            'company_logo': self.company_logo,
            'company_type': self.company_type,
            'company_status': self.company_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class EnterpriseEmailWhiteList(db.Model):
    """
    """
    __tablename__ = 'enterprise_email_whitelist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    email_name = db.Column(db.String(255), nullable=False, comment='邮箱后缀')
    company_id = db.Column(db.Integer, comment='公司id')
    company_name = db.Column(db.String(255), default="", comment='公司名称')
    company_desc = db.Column(db.String(255), default="", comment='公司描述')
    company_status = db.Column(db.String(255), default="", comment='公司状态')
    email_status = db.Column(db.String(255), nullable=False, comment='企业邮箱状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'email_name': self.email_name,
            'company_id': self.company_id,
            'company_name': self.company_name,
            'company_desc': self.company_desc,
            'company_status': self.company_status,
            'email_status': self.email_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
