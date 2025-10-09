from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.app import app
from app.services.contacts_service.friends_service import *


@app.route('/next_console_admin/contacts/friends/get_friend_list', methods=['POST'])
@jwt_required()
def get_friends():
    """
    获取好友列表
    """
    user_id = get_jwt_identity()
    return get_friends_service(user_id)


@app.route('/next_console_admin/user_center/friends/search', methods=['POST'])
@jwt_required()
def search_friends():
    """
    搜索好友
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return search_friends_service(data)


@app.route('/next_console_admin/user_center/friends/add', methods=['POST'])
@jwt_required()
def add_friends():
    """
    申请好友
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    friend_id = data.get("friend_id")
    if not friend_id:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    if user_id == friend_id:
        return next_console_response(error_status=True, error_message="不能添加自己为好友！")
    return add_friends_service(data)


@app.route('/next_console_admin/user_center/friends/accept_friend_request', methods=['POST'])
@jwt_required()
def accept_friends():
    """
    申请好友
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    friend_id = data.get("friend_id")
    if not friend_id:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    if user_id == friend_id:
        return next_console_response(error_status=True, error_message="不能添加自己为好友！")
    return accept_friends_service(data)


@app.route('/next_console_admin/user_center/friends/reject_friend_request', methods=['POST'])
@jwt_required()
def reject_friends():
    """
    申请好友
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    friend_id = data.get("friend_id")
    if not friend_id:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    if user_id == friend_id:
        return next_console_response(error_status=True, error_message="不能添加自己为好友！")
    return reject_friends_service(data)


@app.route('/next_console_admin/user_center/friends/delete', methods=['POST'])
@jwt_required()
def delete_friends():
    """
    删除好友
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    friend_id = data.get("friend_id")
    if not friend_id:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    if user_id == friend_id:
        return next_console_response(error_status=True, error_message="不能删除自己！")
    return delete_friends_service(data)


@app.route('/next_console_admin/user_center/friends/stranger', methods=['POST'])
@jwt_required()
def get_stranger():
    """
    获取陌生人信息
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    friend_email = data.get("new_friend_email")
    if not friend_email:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return get_stranger_service(data)


@app.route('/next_console_admin/user_center/friends/friend_requests_history', methods=['POST'])
@jwt_required()
def get_request_record():
    """
    获取好友申请记录
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return get_friend_request_service(data)


@app.route('/next_console_admin/user_center/friends/friend_requests_cnt', methods=['POST'])
@jwt_required()
def get_request_record_cnt():
    """
    获取好友申请记录
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return get_friend_request_count(data)

