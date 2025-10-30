from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from .service import *
blueprint = Blueprint('spdb', __name__, url_prefix='/next_console/app_center/spdb')


@blueprint.route('/md_table_to_excel', methods=["GET", "POST"])
@jwt_required()
def search_sales_price():
    # 处理请求
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return md_table_to_excel_service(data)

