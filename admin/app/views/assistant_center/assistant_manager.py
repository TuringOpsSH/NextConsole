from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.services.assistant_center.assistant_manager import *


@app.route('/next_console/assistant_center/assistant_manage/assistants/search', methods=['GET', 'POST'])
@jwt_required()
def assistants_search():
    """
    搜索助手
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    order = params.get('order', 'create_time')
    if not order and order not in ('create_time', "call_cnt"):
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    assistant_is_start = params.get('assistant_is_start')
    if assistant_is_start and assistant_is_start not in ('0', "1"):
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    rel_type = params.get('rel_type')
    if rel_type and rel_type not in ('服务', "权限"):
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    return search_assistants(params)


@app.route('/next_console/assistant_center/assistant_manage/assistants/add', methods=['GET', 'POST'])
@jwt_required()
def assistants_add():
    """
    搜索助手
    """
    params = request.json
    assistant_name = params.get('assistant_name')
    assistant_model_name = params.get('assistant_model_name')
    assistant_status = params.get('assistant_status', '创建')
    if not assistant_name or not assistant_model_name:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    assistant_model_temperature = params.get('assistant_model_temperature')
    if assistant_model_temperature:
        try:
            assistant_model_temperature = float(assistant_model_temperature)
            if assistant_model_temperature < 0.0 or assistant_model_temperature > 2.0:
                return next_console_response(error_status=True, error_code=400, error_message='温度错误')
        except ValueError as e:
            return next_console_response(error_status=True, error_code=400, error_message='温度错误')
    if assistant_status not in ('正常', "创建", "发布", "锁定"):
        return next_console_response(error_status=True, error_code=400, error_message='状态参数错误')
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return add_assistant(params)


@app.route('/next_console/assistant_center/assistant_manage/assistants/delete', methods=['GET', 'POST'])
@jwt_required()
def assistants_delete():
    """
    搜索助手
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    assistant_ids = params.get('assistant_ids')
    if not user_id or not assistant_ids:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    return delete_assistant(params)


@app.route('/next_console/assistant_center/assistant_manage/assistants/update', methods=['GET', 'POST'])
@jwt_required()
def assistants_update():
    """
    更新助手
    """
    params = request.json
    assistant_id = params.get('id')
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not assistant_id or not user_id:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    if 'create_time' in params:
        del params['create_time']
    if 'update_time' in params:
        del params['update_time']
    return update_assistant(params)


@app.route('/next_console/assistant_center/assistant_manage/assistants/get', methods=['GET', 'POST'])
@jwt_required()
def assistants_get():
    """
    查看助手详细信息
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    return get_assistant(params)


@app.route('/next_console/assistant_center/assistant_manage/assistants/change', methods=['GET', 'POST'])
@jwt_required()
def assistants_change():
    """
    切换助手
    """
    params = request.json
    assistant_id = params.get('assistant_id')
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    if not assistant_id or not user_id:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    assistant_source = params.get('assistant_source')
    if assistant_source and assistant_source not in (1, 2, 3, 4):
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    return change_assistant(user_id, assistant_id, assistant_source)


@app.route('/next_console/assistant_center/assistant_manage/assistants/avatar/upload', methods=['POST'])
@jwt_required()
def assistant_avatar_upload():
    """
    上传助手头像
    """

    assistant_id = request.form.get('assistant_id')
    assistant_author_id = get_jwt_identity()
    avatar = request.files['avatar']
    avatar_name = request.form.get('avatar_name')
    if not avatar or not assistant_author_id or not assistant_id:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    return upload_avatar(assistant_id, assistant_author_id, avatar, avatar_name)


@app.route('/next_console/assistant_center/assistant_manage/assistants/user_rel/add', methods=['POST'])
@jwt_required()
def assistant_user_rel_add():
    """
    新增助手用户关系
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = int(user_id)
    assistant_id = request.json.get('assistant_id')
    rel_type = request.json.get('rel_type')
    rel_value = request.json.get('rel_value')
    if not user_id or assistant_id is None or not rel_type or not rel_value:
        return next_console_response(error_status=True, error_code=400, error_message='权限参数错误')
    if rel_type not in ('服务', "权限"):
        return next_console_response(error_status=True, error_code=400, error_message='类型参数错误')
    if rel_type == '服务':
        try:
            rel_value = int(rel_value)
            if rel_value not in (0, 1, 2, 3, 4, 5, 6, 7):
                return next_console_response(error_status=True, error_code=400, error_message='参数错误')
        except ValueError as e:
            return next_console_response(error_status=True, error_code=400, error_message='参数错误')

    return add_user_assistant_rel(user_id, assistant_id, rel_type, rel_value)


@app.route('/next_console/assistant_center/assistant_manage/assistants/user_rel/get', methods=['POST'])
@jwt_required()
def assistant_user_rel_get():
    """
    获取助手用户关系
    """
    user_id = get_jwt_identity()
    assistant_id = request.json.get('assistant_id')
    if not user_id or not assistant_id:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    return get_user_assistant_rel(user_id, assistant_id)


@app.route('/next_console/assistant_center/assistant_manage/assistants/user_rel/update', methods=['POST'])
@jwt_required()
def assistant_user_rel_update():
    """
    更新助手用户关系
    """
    user_id = get_jwt_identity()
    assistant_id = request.json.get('assistant_id')
    rel_type = request.json.get('rel_type')
    if not user_id or not assistant_id or not rel_type:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    if rel_type not in ('服务', "创建", "停用"):
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    return update_user_assistant_rel(user_id, assistant_id, rel_type)


@app.route('/next_console/assistant_center/assistant_manage/assistants/user_rel/del', methods=['POST'])
@jwt_required()
def assistant_user_rel_del():
    """
    删除助手用户关系
    """
    user_id = request.json.get('user_id')
    assistant_id = request.json.get('assistant_id')
    rel_type = request.json.get('rel_type')
    if not user_id or not assistant_id or not rel_type:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    if rel_type not in ('服务', "创建", "停用"):
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    return del_user_assistant_rel(user_id, assistant_id, rel_type)


@app.route('/next_console/assistant_center/assistant_manage/assistants/metric/get', methods=['POST'])
@jwt_required()
def assistant_metric_get():
    """
    获取助手运行指标
    """
    params = request.json
    user_id = get_jwt_identity()
    assistant_id = params.get('assistant_id')
    metric_name = params.get('metric_name')
    start_time = params.get('start_time')
    end_time = params.get('end_time')
    interval = params.get('interval', 360)
    if not user_id or not assistant_id or not metric_name:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    if metric_name not in (
            'qa_counts', "user_counts", "avg_time",
            "token_speed", "cost", "like_rate"):
        return next_console_response(error_status=True, error_code=400, error_message='暂不支持该指标')
    try:
        start_time_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time_date = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        interval = int(interval)
        params["start_time"] = start_time_date
        params["end_time"] = end_time_date
        params["interval"] = interval
    except ValueError as e:
        return next_console_response(error_status=True, error_code=400, error_message='时间格式错误')
    params["user_id"] = int(user_id)
    return get_assistant_metric(params)

