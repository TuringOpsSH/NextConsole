from sqlalchemy.sql import func

from app.app import db


class ShareResourceAuthorizeCompanyInfo(db.Model):
    """
    """
    __tablename__ = 'share_resource_authorize_company_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    resource_id = db.Column(db.Integer, comment='资源id')
    user_id = db.Column(db.Integer, comment='用户id')
    company_id = db.Column(db.Integer, comment='公司id')
    auth_type = db.Column(db.String(255), comment='授权类型')
    auth_status = db.Column(db.String(255), comment='授权状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'auth_type': self.auth_type,
            'auth_status': self.auth_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ShareResourceAuthorizeDepartmentInfo(db.Model):
    """
    '共享资源授权部门表'
    """
    __tablename__ = 'share_resource_authorize_department_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    resource_id = db.Column(db.Integer, comment='资源id')
    user_id = db.Column(db.Integer, comment='用户id')
    department_id = db.Column(db.Integer, comment='部门id')
    auth_type = db.Column(db.String(255), comment='授权类型')
    auth_status = db.Column(db.String(255), comment='授权状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'user_id': self.user_id,
            'department_id': self.department_id,
            'auth_type': self.auth_type,
            'auth_status': self.auth_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ShareResourceAuthorizeColleagueInfo(db.Model):
    """
     '共享资源授权同事表';
    """
    __tablename__ = 'share_resource_authorize_colleague_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    user_id = db.Column(db.Integer, comment='用户id')
    resource_id = db.Column(db.Integer, comment='资源id')
    auth_user_id = db.Column(db.Integer, comment='被授权用户id')
    auth_type = db.Column(db.String(255), comment='授权类型')
    auth_status = db.Column(db.String(255), comment='授权状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resource_id': self.resource_id,
            'auth_user_id': self.auth_user_id,
            'auth_type': self.auth_type,
            'auth_status': self.auth_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ShareResourceAuthorizeFriendInfo(db.Model):
    """
     '共享资源授权好友表';
    """
    __tablename__ = 'share_resource_authorize_friend_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    user_id = db.Column(db.Integer, comment='用户id')
    resource_id = db.Column(db.Integer, comment='资源id')
    auth_user_id = db.Column(db.Integer, comment='被授权用户id')
    auth_type = db.Column(db.String(255), comment='授权类型')
    auth_status = db.Column(db.String(255), comment='授权状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resource_id': self.resource_id,
            'auth_user_id': self.auth_user_id,
            'auth_type': self.auth_type,
            'auth_status': self.auth_status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ResourceDownloadCoolingRecord(db.Model):
    """
  '资源下载冷却记录表';
    """
    __tablename__ = 'resource_download_cooling_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    user_id = db.Column(db.Integer, comment='目标用户id')
    resource_id = db.Column(db.Integer, comment='目标资源id')
    author_id = db.Column(db.Integer, comment='资源作者id')
    author_notice = db.Column(db.Boolean, default=False, comment='是否通知作者')
    author_allow = db.Column(db.Boolean, default=False, comment='作者是否允许继续下载')
    author_allow_cnt = db.Column(db.Integer, default=0, comment='作者新增次数')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resource_id': self.resource_id,
            'author_id': self.author_id,
            'author_notice': self.author_notice,
            'author_allow': self.author_allow,
            'author_allow_cnt': self.author_allow_cnt,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }