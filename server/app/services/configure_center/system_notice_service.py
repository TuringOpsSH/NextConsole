from app.app import app, redis_client, socketio
import json


def send_update_ref_status(params):
    """
    发送更新索引状态
    :return:
    """
    user_id = int(params.get("user_id"))
    data = params.get("data")
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('update_ref_status', data, room=client.get('session_id'))
    return "success"


def send_add_friend_msg(params):
    """
    发送好友申请消息
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    data = params.get("data")
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('new_friend_request', data, room=client.get('session_id'))
    return "success"


def send_ticket_status_update(ticket):
    user_id = ticket.user_id
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('ticket_status_update', ticket.to_dict(), room=client.get('session_id'))
    return "success"


def send_ticket_msg_update(ticket, msg):
    user_id = ticket.user_id
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('ticket_msg_update', {"ticket": ticket.to_dict(), "msg": msg},
                          room=client.get('session_id'))
    return "success"


def send_ticket_msg_attachment_update(target_user, msg_id, target_resource):
    user_id = target_user.user_id
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('ticket_msg_attachment_update', {
                "msg_id": msg_id,
                "attachment": target_resource.to_dict()}, room=client.get('session_id'))
    return "success"


def send_online_service_message_update(session, msg):
    """
    发送在线服务消息更新
    :param session:
    :param msg:
    :return:
    """
    user_id = session.user_id
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('online_service_message_update', {"session": session.to_dict(), "msg": msg},
                          room=client.get('session_id'))


def send_online_service_msg_attachment_update(target_user, qa_id, msg_id, target_resource):
    user_id = target_user.user_id
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('service_msg_attachment_update', {
                "qa_id": qa_id,
                "msg_id": msg_id,
                "attachment": target_resource.to_dict()}, room=client.get('session_id'))
    return "success"


def send_service_session_status_update(target_session):
    """
    发送服务会话状态更新
    :param target_session:
    :return:
    """
    user_id = target_session.user_id
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('service_session_status_update', target_session.to_dict(), room=client.get('session_id'))
    return "success"


def send_service_session_assistant_update(target_session, assistant):
    """
    发送服务会话协助人更新
    :param target_session:
    :param assistant:
    :return:
    """
    user_id = target_session.user_id
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('service_session_assistant_update', {"session": target_session.to_dict(),
                                                               "assistant": assistant},
                          room=client.get('session_id'))
    return "success"


def send_new_system_notice(params):
    """
        发送新增站内信
    :return:
    """
    user_id = int(params.get("user_id"))
    data = params.get("data")
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('new_system_notice', data, room=client.get('session_id'))

    return "success"


def send_wps_rename(params):
    """

    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    data = params.get("data")
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        if client.get('status') == 'connected':
            socketio.emit('wps_rename', data, room=client.get('session_id'))

    return "success"
