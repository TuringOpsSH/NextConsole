from sqlalchemy.sql import func
from app.app import db


class ZYSalesDataInfo(db.Model):
    """

) ENGINE=InnoDB COMMENT 'ZY产品价格数据信息';
    """
    __tablename__ = 'ZYPriceDataInfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.TIMESTAMP, nullable=False, comment='数据统计开始时间')
    end_time = db.Column(db.TIMESTAMP, nullable=False, comment='数据统计完成时间')
    product_name = db.Column(db.String(255), nullable=False, comment='产品名称')
    product_level = db.Column(db.String(255), nullable=False, comment='产品等级')
    product_specification = db.Column(db.String(255), nullable=False, comment='产品规格')
    wholesale_price = db.Column(db.Float, nullable=False, comment='批发价格')
    recommended_retail_price = db.Column(db.Float, nullable=False, comment='建议零售价')
    city = db.Column(db.String(255), nullable=False, comment='城市')
    purchase_price = db.Column(db.Float, comment='进货价')
    sale_price = db.Column(db.Float, comment='出货价')
    status = db.Column(db.String(255), nullable=False, comment='数据状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'startTime': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'endTime': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'productName': self.product_name,
            'productLevel': self.product_level,
            'productSpecification': self.product_specification,
            'wholesalePrice': self.wholesale_price,
            'recommendedRetailPrice': self.recommended_retail_price,
            'city': self.city,
            'purchasePrice': self.purchase_price,
            'salePrice': self.sale_price,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


class ZYInventoryDataInfo(db.Model):
    """
    """
    __tablename__ = 'ZYInventoryDataInfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.TIMESTAMP, nullable=False, comment='数据开始时间')
    end_time = db.Column(db.TIMESTAMP, nullable=False, comment='数据结束时间')
    product_level = db.Column(db.String(255), nullable=False, comment='产品等级')
    product_specification = db.Column(db.String(255), nullable=False, comment='产品规格')
    product_inventory = db.Column(db.Float, comment='产品库存')
    product_remain_days = db.Column(db.Integer, comment='产品库存可销天数')
    city = db.Column(db.String(255), nullable=False, comment='城市')
    status = db.Column(db.String(255), nullable=False, comment='数据状态')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'startTime': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'endTime': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'productLevel': self.product_level,
            'productSpecification': self.product_specification,
            'productInventory': self.product_inventory,
            'productRemainDays': self.product_remain_days,
            'city': self.city,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
