from sqlalchemy.sql import func
from app.app import db


class SystemConfig(db.Model):
    """
    系统配置
    """
    __tablename__ = 'system_config_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='参数id')
    module_name = db.Column(db.String(255), nullable=False, comment='模块名称')
    component_name = db.Column(db.String(255), nullable=False, comment='组件名称')
    config_name = db.Column(db.String(255), nullable=False, comment='配置名称')
    config_desc = db.Column(db.String(255), nullable=False, comment='配置描述')
    config_default_value = db.Column(db.String(1024), nullable=False, comment='配置默认值')
    config_value = db.Column(db.String(1024), nullable=False, comment='配置值')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='配置创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='配置更新时间')
    config_status = db.Column(db.Integer, nullable=False, comment='配置状态')

    def to_dict(self):
        return {
            "id": self.id,
            "module_name": self.module_name,
            "component_name": self.component_name,
            "config_name": self.config_name,
            "config_desc": self.config_desc,
            "config_default_value": self.config_default_value,
            "config_value": self.config_value,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "config_status": self.config_status,
        }


class SupportArea(db.Model):
    """
    支持区域
      `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键，唯一标识每个国家记录',
  `name` VARCHAR(100) NOT NULL COMMENT '国家的名称，如“United States”',
  `iso_code_2` CHAR(2) NOT NULL COMMENT '国家的ISO 3166-1 alpha-2代码，如“US”',
  `iso_code_3` CHAR(3) NOT NULL COMMENT '国家的ISO 3166-1 alpha-3代码，如“USA”',
  `phone_code` VARCHAR(10) NOT NULL COMMENT '国家的国际电话区号，如“+1”',
  `continent` VARCHAR(50) NOT NULL COMMENT '国家所属的大洲，如“North America”',
  `region` VARCHAR(50) NOT NULL COMMENT '国家所属的地区，如“Americas”',
  `subregion` VARCHAR(50) NOT NULL COMMENT '国家所属的次区域，如“Northern America”',
  `area` VARCHAR(50) NOT NULL COMMENT '国家的地区，如“Shanghai”',
  `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建的时间戳',
  `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新的时间戳',
    """
    __tablename__ = 'support_area_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='区域id')
    country = db.Column(db.String(100), nullable=False, comment='国家的名称')
    iso_code_2 = db.Column(db.String(2), default='', comment='国家的ISO 3166-1 alpha-2代码')
    iso_code_3 = db.Column(db.String(3), default='', comment='国家的ISO 3166-1 alpha-3代码')
    phone_code = db.Column(db.String(10), default='', comment='国家的国际电话区号')
    continent = db.Column(db.String(50), default='', comment='国家所属的大洲')
    province = db.Column(db.String(50), nullable=False, comment='省')
    city = db.Column(db.String(50), nullable=False, comment='市')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='记录创建的时间戳')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='记录最后更新的时间戳')
    area_status = db.Column(db.String(50), nullable=False, comment='区域状态')

    def to_dict(self):
        return {
            "id": self.id,
            "country": self.country,
            "iso_code_2": self.iso_code_2,
            "iso_code_3": self.iso_code_3,
            "phone_code": self.phone_code,
            "continent": self.continent,
            "province": self.province,
            "city": self.city,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "area_status": self.area_status,
        }

