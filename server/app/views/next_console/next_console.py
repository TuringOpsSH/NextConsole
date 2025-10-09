from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.services.next_console.next_console import *
from app.services.next_console.search_engine import *
from app.app import socketio
from app.utils.iat.iat_ws_client import handle_audio_message, handle_audio_stop_message


@app.route('/next_console/session/add', methods=['GET', 'POST'])
@jwt_required()
def session_add():
    """
    新增会话
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    session_assistant_id = params.get("session_assistant_id", -12345)
    if session_assistant_id is None:
        return next_console_response(error_status=True, error_message="参数异常！")
    return add_session(params)


@app.route('/next_console/session/del', methods=['GET', 'POST'])
@jwt_required()
def session_delete():
    """
    删除会话
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return delete_session(params)


@app.route('/next_console/session/update', methods=['GET', 'POST'])
@jwt_required()
def session_update():
    """
    更新会话
    """
    params = request.get_json()
    session_id = params.get("session_id")
    session_status = params.get("session_status")
    session_like_cnt = params.get("session_like_cnt")
    session_dislike_cnt = params.get("session_dislike_cnt")
    session_update_cnt = params.get("session_update_cnt")
    session_share_cnt = params.get("session_share_cnt")
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not session_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    if (session_like_cnt and session_like_cnt not in (-1, 1)
    ) or (session_dislike_cnt and session_dislike_cnt not in (-1, 1)
    ) or (session_update_cnt and session_update_cnt not in (-1, 1)
    ) or (session_share_cnt and session_share_cnt not in (-1, 1)
    ) or (session_status and session_status not in ("新建", "进行中", "测试", "已关闭")
    ):
        return next_console_response(error_status=True, error_message="参数异常！")

    return update_session(params)


@app.route('/next_console/session/search', methods=['GET', 'POST'])
@jwt_required()
def session_search():
    """
    会话列表
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_session(params)


@app.route('/next_console/qa/add', methods=['GET', 'POST'])
@jwt_required()
def qa_add():
    """
    新增问答
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return add_qa(params)


@app.route('/next_console/qa/del', methods=['GET', 'POST'])
@jwt_required()
def qa_delete():
    """
    删除问答
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return delete_qa(params)


@app.route('/next_console/qa/update', methods=['GET', 'POST'])
@jwt_required()
def qa_update():
    """
    更新问答
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    qa_id = params.get("qa_id")
    if not user_id or not qa_id:
        return next_console_response(error_status=True, error_message="参数异常！")
    return update_qa(params)


@app.route('/next_console/qa/search', methods=['GET', 'POST'])
@jwt_required()
def qa_search():
    """
    搜索问答
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return search_qa(params)


@app.route('/next_console/messages/search', methods=['GET', 'POST'])
@jwt_required()
def messages_search():
    """
    搜索消息
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return next_console_search_messages(params)


@app.route('/next_console/messages/add', methods=['GET', 'POST'])
@jwt_required()
def messages_add():
    """
    新增消息,并返回答案

    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    session_id = params.get("session_id")
    session_source = params.get('session_source')
    assistant_id = params.get("assistant_id")
    assistant_source = params.get('assistant_source')
    if not session_id:
        return next_console_response(error_status=True, error_message="参数异常！")

    if assistant_id:
        return next_console_response(error_status=True, error_message="参数异常！")

    if assistant_source and assistant_source not in (1, 2, 3, 4):
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')

    # 判断用户是否过期
    from app.models.user_center.user_info import UserInfo
    user = UserInfo.query.filter_by(user_id=user_id).first()
    if user.user_expire_time and user.user_expire_time < datetime.now():
        user.user_status = -1
        db.session.add(user)
        db.session.commit()
        return next_console_response(error_status=True, error_message="用户已过期！", error_code=401)
    if session_source == "next_search":
        return next_search_add_message_v3(params)
    return next_console_response(error_status=True, error_message="参数异常！")


@app.route('/next_console/messages/update', methods=['GET', 'POST'])
@jwt_required()
def messages_update():
    """
    更新消息
    """
    params = request.get_json()
    msg_id = params.get("msg_id")
    if not msg_id:
        return next_console_response(error_status=True, error_message="参数错误")
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return update_messages(params)


@app.route('/next_console/messages/del', methods=['GET', 'POST'])
@jwt_required()
def messages_delete():
    """
    删除消息
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return delete_messages(params)


@socketio.on('audio_message')
def handle_user_audio_message(message):
    """
        处理音频消息 ，并调用讯飞语音识别接口
    """
    handle_audio_message(message)


@socketio.on('audio_message_stop')
def handle_user_audio_stop_message(message):
    """
        处理音频消息 ，并调用讯飞语音识别接口
    """
    handle_audio_stop_message(message)
