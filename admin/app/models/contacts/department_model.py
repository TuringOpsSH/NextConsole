from app.app import db
from sqlalchemy.sql import func


class DepartmentInfo(db.Model):
    """

    """
    __tablename__ = 'department_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID 编号')
    company_id = db.Column(db.Integer, nullable=False, comment='归属公司id')
    parent_department_id = db.Column(db.Integer, comment='上级部门id')
    department_code = db.Column(db.String(255), nullable=False, comment='部门编号')
    department_name = db.Column(db.String(255), nullable=False, comment='部门名称')
    department_desc = db.Column(db.Text, default="", comment='部门介绍')
    department_status = db.Column(db.String(255), default="正常", comment='部门状态')
    department_logo = db.Column(db.Text, default="", comment='部门图标')
    create_time = db.Column(db.TIMESTAMP, server_default=func.now(), comment='创建时间')
    update_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'parent_department_id': self.parent_department_id,
            'department_code': self.department_code,
            'department_name': self.department_name,
            'department_desc': self.department_desc,
            'department_status': self.department_status,
            'department_logo': self.department_logo,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        }


