from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import socketio

from app.sub_apps.whzy.index_service import *

blueprint = Blueprint('whzy', __name__, url_prefix='/next_console/app_center/whzy')


@blueprint.route('/salesData/price', methods=["GET", "POST"])
@jwt_required()
def search_sales_price():
    # 处理请求
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return get_salesData_price(data)


@blueprint.route('/salesData/inventory', methods=["GET", "POST"])
@jwt_required()
def search_sales_inventory():
    # 处理请求
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return get_salesData_inventory(data)


@blueprint.route('/salesData/purchase', methods=["GET", "POST"])
@jwt_required()
def search_sales_purchase():
    # 处理请求
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return get_salesData_inventory(data)


@blueprint.route('/messages/add', methods=["GET", "POST"])
@jwt_required()
def app_add_message():
    # 处理请求
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    from app.sub_apps.whzy.agent_service import agent_add_message
    return agent_add_message(data)


@socketio.on('whzy_audio_message')
def handle_whzy_audio_message(message):
    """
        处理音频消息 ，并调用讯飞语音识别接口
    """
    from app.sub_apps.whzy.agent_service import handle_audio_message
    handle_audio_message(message)


@socketio.on('whzy_audio_message_stop')
def handle_whzy_audio_stop_message(message):
    """
        处理音频消息 ，并调用讯飞语音识别接口
    """
    from app.sub_apps.whzy.agent_service import handle_audio_stop_message
    handle_audio_stop_message(message)