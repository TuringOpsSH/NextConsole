from sqlalchemy.sql import func

from app.app import db


class ResourceObjectMeta(db.Model):
    """

    """
    __tablename__ = 'resource_object_meta_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='id')
    resource_parent_id = db.Column(db.Integer, comment='父资源id')
    user_id = db.Column(db.Integer, comment='用户id')
    resource_name = db.Column(db.String(255), comment='资源名称')
    resource_type = db.Column(db.String(255), default="", comment='资源类型')
    resource_title = db.Column(db.String(255), default="", comment='资源标题')
    resource_desc = db.Column(db.Text, default="", comment='资源描述')
    resource_icon = db.Column(db.Text, default="", comment='资源图标')
    resource_format = db.Column(db.String(255), default="", comment='资源格式')
    resource_size_in_MB = db.Column(db.Float, default=0, comment='资源大小')
    resource_path = db.Column(db.Text, comment='资源存储路径')
    resource_source = db.Column(db.Text, default="", comment='资源来源')
    resource_source_url = db.Column(db.Text, default="", comment='资源来源地址')
    resource_source_url_site = db.Column(db.Text, default="", comment='文档url归属主站')
    resource_show_url = db.Column(db.Text, default="", comment='资源展示地址')
    resource_download_url = db.Column(db.Text, default="", comment='资源下载地址')
    resource_feature_code = db.Column(db.String(255), default="", comment='资源特征编码')
    resource_is_share = db.Column(db.Boolean, default=False, comment='资源是否共享')
    resource_is_public = db.Column(db.Boolean, default=False, comment='资源是否公开')
    resource_public_access = db.Column(db.String(255), default="", comment='资源公开访问权限')
    resource_language = db.Column(db.String(255), default="简体中文", comment='资源语言')
    resource_status = db.Column(db.String(255), default="正常", comment='资源状态')
    resource_version = db.Column(db.Integer, default=1, comment='资源版本')
    resource_rag_config = db.Column(db.JSON, default={}, comment='资源RAG配置')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')
    delete_time = db.Column(db.TIMESTAMP, comment='删除时间')

    def to_dict(self):
        
        resource_type_translate = {
            "folder": "文件夹",
            "webpage": "网页",
            "code": "代码",
            "audio": "音频",
            "video": "视频",
            "archive": "压缩包",
            "binary": "程序",
            "other": "其他",
            "document": "文档",
            "image": "图片",
        }
        return {
            'id': self.id,
            'resource_parent_id': self.resource_parent_id,
            'user_id': self.user_id,
            'resource_name': self.resource_name,
            'resource_type': self.resource_type,
            'resource_type_cn': resource_type_translate.get(self.resource_type, self.resource_type),
            'resource_desc': self.resource_desc,
            'resource_icon': self.resource_icon,
            'resource_title': self.resource_title,
            'resource_format': self.resource_format,
            'resource_size_in_MB': round(self.resource_size_in_MB, 4),
            'resource_path': self.resource_path,
            'resource_source': self.resource_source,
            'resource_source_url': self.resource_source_url,
            'resource_source_url_site': self.resource_source_url_site,
            'resource_show_url': self.resource_show_url,
            'resource_download_url': self.resource_download_url,
            'resource_feature_code': self.resource_feature_code,
            'resource_language': self.resource_language,
            'resource_version': self.resource_version,
            'resource_status': self.resource_status,
            "resource_rag_config": self.resource_rag_config,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "delete_time": self.delete_time.strftime('%Y-%m-%d %H:%M:%S') if self.delete_time else "",
        }

    def show_info(self):
        """
        展示资源信息
        :return:
        """
        
        resource_type_translate = {
            "folder": "文件夹",
            "webpage": "网页",
            "code": "代码",
            "audio": "音频",
            "video": "视频",
            "archive": "压缩包",
            "binary": "程序",
            "other": "其他",
            "document": "文档",
            "image": "图片",
        }
        return {
            'id': self.id,
            'resource_parent_id': self.resource_parent_id,
            'user_id': self.user_id,
            'resource_name': self.resource_name,
            'resource_desc': self.resource_desc,
            'resource_type': self.resource_type,
            'resource_type_cn': resource_type_translate.get(self.resource_type, self.resource_type),
            'resource_format': self.resource_format,
            'resource_title': self.resource_title,
            'resource_icon': self.resource_icon,
            'resource_size_in_MB': self.resource_size_in_MB,
            'resource_source': self.resource_source,
            'resource_source_url': self.resource_source_url,
            'resource_source_url_site': self.resource_source_url_site,
            'resource_show_url': self.resource_show_url,
            'resource_feature_code': self.resource_feature_code,
            'resource_language': self.resource_language,
            'resource_version': self.resource_version,
            'resource_status': self.resource_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "delete_time": self.delete_time.strftime('%Y-%m-%d %H:%M:%S') if self.delete_time else "",
        }


class ResourceObjectUpload(db.Model):
    """
    资源对象上传信息

    """
    __tablename__ = 'resource_object_upload_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='任务id')
    user_id = db.Column(db.Integer, comment='用户id')
    resource_parent_id = db.Column(db.Integer, comment='父资源id')
    resource_name = db.Column(db.String(255), comment='资源名称')
    resource_size_in_mb = db.Column(db.Float, default=0, comment='资源大小')
    resource_type = db.Column(db.String(255), default='', comment='资源类型')
    resource_format = db.Column(db.String(255), default='', comment='资源格式')
    content_max_idx = db.Column(db.Integer, default=-1, comment='资源分块数')
    content_finish_idx = db.Column(db.Integer, default=-1, comment='资源分块完成数')
    content_prefix = db.Column(db.String(255), default='', comment='资源分块前缀')
    resource_md5 = db.Column(db.String(255), default='', comment='资源md5值')
    resource_id = db.Column(db.Integer, comment='资源id')
    task_icon = db.Column(db.Text, default='', comment='任务图标')
    task_source = db.Column(db.String(255), default='', comment='任务来源')
    task_status = db.Column(db.String(255), default='pending', comment='任务状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resource_parent_id': self.resource_parent_id,
            'resource_name': self.resource_name,
            'resource_size_in_mb': round(self.resource_size_in_mb, 4),
            'resource_type': self.resource_type,
            'resource_format': self.resource_format,
            'content_max_idx': self.content_max_idx,
            'content_finish_idx': self.content_finish_idx,
            'content_prefix': self.content_prefix,
            'resource_md5': self.resource_md5,
            'resource_id': self.resource_id,
            "task_icon": self.task_icon if self.task_icon else "images/other.svg",
            "task_source": self.task_source,
            'task_status': self.task_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        
        resource_type_translate = {
            "folder": "文件夹",
            "webpage": "网页",
            "code": "代码",
            "audio": "音频",
            "video": "视频",
            "archive": "压缩包",
            "binary": "程序",
            "other": "其他",
            "document": "文档",
            "image": "图片",
        }
        return {
            'id': self.id,
            "resource_id": self.resource_id,
            'resource_name': self.resource_name,
            'resource_size_in_mb': round(self.resource_size_in_mb, 4),
            'resource_type': self.resource_type,
            'resource_type_cn': resource_type_translate.get(self.resource_type, self.resource_type),
            'resource_format': self.resource_format,
            'content_max_idx': self.content_max_idx,
            'content_finish_idx': self.content_finish_idx,
            'content_prefix': self.content_prefix,
            'resource_md5': self.resource_md5,
            "task_icon": self.task_icon if self.task_icon else "images/other.svg",
            'task_status': self.task_status,
            'task_source': self.task_source,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ResourceObjectShortCut(db.Model):
    """
    '资源快捷方式信息';
    """
    __tablename__ = 'resource_object_shortcuts_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    user_id = db.Column(db.Integer, comment='用户id')
    resource_id = db.Column(db.Integer, comment='资源id')
    shortcut_status = db.Column(db.String(255), default="正常", comment='快捷方式状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resource_id': self.resource_id,
            'shortcut_status': self.shortcut_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ResourceDownloadRecord(db.Model):
    """

    """
    __tablename__ = 'resource_download_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    user_id = db.Column(db.Integer, comment='用户id')
    resource_id = db.Column(db.Integer, comment='资源id')
    download_url = db.Column(db.Text, comment='下载链接')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resource_id': self.resource_id,
            'download_url': self.download_url,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ResourceTag(db.Model):
    """
    资源标签信息表
    """
    __tablename__ = 'resource_tag_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    user_id = db.Column(db.Integer, comment='用户id')
    tag_name = db.Column(db.String(255), comment='标签名称')
    tag_type = db.Column(db.String(255), default="user", comment='标签类型')
    tag_source = db.Column(db.String(255), default="user", comment='标签来源')
    tag_value = db.Column(db.String(255), comment='标签值')
    tag_color = db.Column(db.String(255), default="blue", comment='标签颜色')
    tag_icon = db.Column(db.Text, default="", comment='标签图标')
    tag_desc = db.Column(db.Text, default="", comment='标签描述')
    tag_status = db.Column(db.String(255), default="正常", comment='标签状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tag_name': self.tag_name,
            'tag_type': self.tag_type,
            'tag_source': self.tag_source,
            'tag_value': self.tag_value,
            'tag_color': self.tag_color,
            'tag_icon': self.tag_icon,
            'tag_desc': self.tag_desc,
            'tag_status': self.tag_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def show_info(self):
        return {
            'id': self.id,
            'tag_name': self.tag_name,
            'tag_type': self.tag_type,
            'tag_source': self.tag_source,
            'tag_value': self.tag_value,
            'tag_color': self.tag_color,
            'tag_icon': self.tag_icon,
            'tag_desc': self.tag_desc,
            'tag_status': self.tag_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ResourceTagRelation(db.Model):
    """
    资源标签关系表

    """
    __tablename__ = 'resource_tag_relation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增id')
    resource_id = db.Column(db.Integer, comment='资源id')
    tag_id = db.Column(db.Integer, comment='标签id')
    rel_status = db.Column(db.String(255), default="正常", comment='关系状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'tag_id': self.tag_id,
            'rel_status': self.rel_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ResourceObjectHistory(db.Model):
    """
    资源对象历史信息表
    """
    __tablename__ = 'resource_object_history_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='id')
    resource_id = db.Column(db.Integer, comment='原始资源id')
    resource_parent_id = db.Column(db.Integer, comment='父资源id')
    user_id = db.Column(db.Integer, comment='用户id')
    modifier_id = db.Column(db.Integer, comment='修改用户id')
    resource_name = db.Column(db.String(255), comment='资源名称')
    resource_type = db.Column(db.String(255), default="", comment='资源类型')
    resource_title = db.Column(db.String(255), default="", comment='资源标题')
    resource_desc = db.Column(db.Text, default="", comment='资源描述')
    resource_icon = db.Column(db.Text, default="", comment='资源图标')
    resource_format = db.Column(db.String(255), default="", comment='资源格式')
    resource_size_in_MB = db.Column(db.Float, default=0, comment='资源大小')
    resource_path = db.Column(db.Text, comment='资源存储路径')
    resource_source = db.Column(db.Text, default="", comment='资源来源')
    resource_source_url = db.Column(db.Text, default="", comment='资源来源地址')
    resource_source_url_site = db.Column(db.Text, default="", comment='文档url归属主站')
    resource_show_url = db.Column(db.Text, default="", comment='资源展示地址')
    resource_download_url = db.Column(db.Text, default="", comment='资源下载地址')
    resource_feature_code = db.Column(db.String(255), default="", comment='资源特征编码')
    resource_is_share = db.Column(db.Boolean, default=False, comment='资源是否共享')
    resource_is_public = db.Column(db.Boolean, default=False, comment='资源是否公开')
    resource_public_access = db.Column(db.String(255), default="", comment='资源公开访问权限')
    resource_language = db.Column(db.String(255), default="简体中文", comment='资源语言')
    resource_status = db.Column(db.String(255), default="正常", comment='资源状态')
    resource_version = db.Column(db.Integer, default=1, comment='资源版本')
    create_time = db.Column(db.TIMESTAMP, comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, comment='更新时间')
    delete_time = db.Column(db.TIMESTAMP, comment='删除时间')

    def to_dict(self):
        
        resource_type_translate = {
            "folder": "文件夹",
            "webpage": "网页",
            "code": "代码",
            "audio": "音频",
            "video": "视频",
            "archive": "压缩包",
            "binary": "程序",
            "other": "其他",
            "document": "文档",
            "image": "图片",
        }
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'resource_parent_id': self.resource_parent_id,
            'user_id': self.user_id,
            'modifier_id': self.modifier_id,
            'resource_name': self.resource_name,
            'resource_type': self.resource_type,
            'resource_type_cn': resource_type_translate.get(self.resource_type, self.resource_type),
            'resource_desc': self.resource_desc,
            'resource_icon': self.resource_icon,
            'resource_title': self.resource_title,
            'resource_format': self.resource_format,
            'resource_size_in_MB': round(self.resource_size_in_MB, 4),
            'resource_path': self.resource_path,
            'resource_source': self.resource_source,
            'resource_source_url': self.resource_source_url,
            'resource_source_url_site': self.resource_source_url_site,
            'resource_show_url': self.resource_show_url,
            'resource_download_url': self.resource_download_url,
            'resource_feature_code': self.resource_feature_code,
            'resource_language': self.resource_language,
            'resource_version': self.resource_version,
            'resource_status': self.resource_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "delete_time": self.delete_time.strftime('%Y-%m-%d %H:%M:%S') if self.delete_time else "",
        }

    def show_info(self):
        """
        展示资源信息
        :return:
        """
        
        resource_type_translate = {
            "folder": "文件夹",
            "webpage": "网页",
            "code": "代码",
            "audio": "音频",
            "video": "视频",
            "archive": "压缩包",
            "binary": "程序",
            "other": "其他",
            "document": "文档",
            "image": "图片",
        }
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'resource_parent_id': self.resource_parent_id,
            'user_id': self.user_id,
            'modifier_id': self.modifier_id,
            'resource_name': self.resource_name,
            'resource_desc': self.resource_desc,
            'resource_type': self.resource_type,
            'resource_type_cn': resource_type_translate.get(self.resource_type, self.resource_type),
            'resource_format': self.resource_format,
            'resource_title': self.resource_title,
            'resource_icon': self.resource_icon,
            'resource_size_in_MB': self.resource_size_in_MB,
            'resource_source': self.resource_source,
            'resource_source_url': self.resource_source_url,
            'resource_source_url_site': self.resource_source_url_site,
            'resource_show_url': self.resource_show_url,
            'resource_feature_code': self.resource_feature_code,
            'resource_language': self.resource_language,
            'resource_version': self.resource_version,
            'resource_status': self.resource_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "delete_time": self.delete_time.strftime('%Y-%m-%d %H:%M:%S') if self.delete_time else "",
        }


class ResourceAttachment(db.Model):
    """
    '资源附件表';
    """
    __tablename__ = 'resource_attachment_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    user_id = db.Column(db.Integer, comment='目标用户id')
    attachment_key = db.Column(db.Text, comment='附件对象 ID')
    attachment_name = db.Column(db.Text, comment='附件名称')
    attachment_path = db.Column(db.Text, comment='附件存储路径')
    attachment_size = db.Column(db.Text, comment='附件大小')
    attachment_url = db.Column(db.Text, comment='附件下载地址')
    attachment_status = db.Column(db.String(255), default="正常", comment='附件状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'attachment_key': self.attachment_key,
            'attachment_name': self.attachment_name,
            'attachment_path': self.attachment_path,
            'attachment_size': self.attachment_size,
            'attachment_url': self.attachment_url,
            'attachment_status': self.attachment_status,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ResourceViewRecord(db.Model):
    """
     '资源查看记录表';
    """
    __tablename__ = 'resource_view_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    user_id = db.Column(db.Integer, comment='目标用户id')
    resource_id = db.Column(db.Integer, comment='资源id')
    client_fingerprint = db.Column(db.String(255), default='', comment='客户端指纹')
    client_ip = db.Column(db.String(255), default='', comment='客户端ip')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resource_id': self.resource_id,
            'client_fingerprint': self.client_fingerprint,
            'client_ip': self.client_ip,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

