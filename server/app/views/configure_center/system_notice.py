import json
from datetime import datetime
from flask import request
from flask_jwt_extended import decode_token
from flask_socketio import disconnect
from flask_socketio import emit

from app.app import socketio, redis_client, app


@socketio.on('connect')
def handle_connect():
    """
    处理客户端连接事件，并记录客户端信息至redis
    :return:
    """
    return ''



@socketio.on('auth')
def handle_auth(data):
    # 为每个连接分配一个唯一标识符

    session_id = request.sid
    token = data.get('token')
    client_fingerprint = data.get('client_fingerprint')
    if not token:
        # print("Authentication failed: No token provided.")
        disconnect()
        return False
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        # print("Authentication failed:", e, token)
        disconnect()  # 验证失败则断开连接
        return False
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    client_info = {
        'session_id': session_id,
        'create_time': current_datetime,
        'connect_time': current_datetime,
        'status': 'connected',
        'client_fingerprint': client_fingerprint,
    }
    all_user_clients = redis_client.get(user_id)
    if all_user_clients:
        all_user_clients = json.loads(all_user_clients)
    else:
        all_user_clients = []
    for client in all_user_clients:
        if client.get('session_id') == session_id and client.get('client_fingerprint') == client_fingerprint:
            # 更新会话ID和连接时间
            client['session_id'] = session_id
            client['connect_time'] = current_datetime
            client['status'] = 'connected'
            redis_client.set(user_id, json.dumps(all_user_clients))
            return True
    all_user_clients.append(client_info)
    redis_client.set(user_id, json.dumps(all_user_clients))
    return True


@socketio.on('remove_auth')
def handle_disconnect(data):
    """
    处理客户端断开连接事件，并更新redis中的客户端信息
    :return:
    """
    session_id = request.sid
    token = data.get('token')
    client_fingerprint = data.get('client_fingerprint')
    if not token:
        disconnect()
        return False
    try:
        # 解码并验证JWT
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        # 进一步的用户认证操作
    except Exception as e:
        disconnect()  # 验证失败则断开连接
        return False
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        return
    all_user_clients = json.loads(all_user_clients)
    if all_user_clients:
        for client in all_user_clients:
            if client.get('client_fingerprint') == client_fingerprint:
                # 更新会话ID和连接时间
                client['session_id'] = session_id
                client['status'] = 'disconnected'
                client['disconnect_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                break
    redis_client.set(user_id, json.dumps(all_user_clients))
    return True


@socketio.on('message')
def handle_message(message):
    emit('response', {'data': 'Server received: ' + message})
