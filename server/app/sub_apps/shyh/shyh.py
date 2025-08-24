from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from .service import *
blueprint = Blueprint('shyh', __name__, url_prefix='/next_console/app_center/shyh')


@blueprint.route('/mock/gateway', methods=["GET", "POST"])
def search_sales_price():
    # 处理请求
    data = request.get_json()
    return mock_gateway_service(data)

