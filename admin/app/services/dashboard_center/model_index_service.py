from datetime import datetime
from app.models.configure_center.llm_kernel import LLMInstance
from app.models.next_console.next_console_model import NextConsoleMessage, NextConsoleSession
from app.models.app_center.app_info_model import AppMetaInfo
from app.app import db
from app.services.configure_center.response_utils import next_console_response
from sqlalchemy import func


def model_base_cnt(params):
    """
    获取模型的token消耗数量，支持返回同期对比
    :param params:
    :return:
    """
    user_id = params.get("user_id", 0)
    llm_code = params.get("llm_code", "")
    begin_time = params.get("begin_time", "")
    end_time = params.get("end_time", "")
    duration = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(
        begin_time, '%Y-%m-%d %H:%M:%S')
    last_begin_time = (datetime.strptime(begin_time, '%Y-%m-%d %H:%M:%S') - duration
                       ).strftime('%Y-%m-%d %H:%M:%S')
    target_model = LLMInstance.query.filter(
        LLMInstance.llm_code == llm_code
    ).first()
    if not target_model:
        return next_console_response(error_status=True, error_message="模型不存在")
    from app.services.configure_center.model_manager import check_model_authorize
    authorize_check = check_model_authorize(user_id, [target_model], required_access='manage')
    if not authorize_check:
        return next_console_response(error_status=True, error_message="无权限查看该模型数据")

    result = {
        "begin_time": begin_time,
        "end_time": end_time,

        "data": {
            "total_token": {
                "title": '总Token消耗',
                "desc": '通过此模型实例产生的总token消耗数',
                "last_begin_time": last_begin_time,
                "cnt": 0,
                "compare": 'up',
                "percent": "0%",
            },
            "total_requests": {
                "title": '总问答次数',
                "desc": '用户实际发起的请求数，可以用于评估用户的活跃度',
                "last_begin_time": last_begin_time,
                "cnt": 0,
                "compare": 'up',
                "percent": "0%"
            },
            "total_sessions": {
                "title": '总会话数',
                "desc": '与此模型关联的会话数，可以用于评估关联的任务数',
                "last_begin_time": last_begin_time,
                "cnt": 0,
                "compare": 'up',
                "percent": "0%"
            },
            "total_apps": {
                "title": '关联应用数',
                "desc": '使用此模型实例的应用',
                "last_begin_time": last_begin_time,
                "cnt": 0,
                "compare": 'up',
                "percent": "0%"
            },
            "total_users": {
                "title": '关联用户数',
                "desc": '使用此模型实例的终端用户',
                "last_begin_time": last_begin_time,
                "cnt": 0,
                "compare": 'up',
                "percent": "0%"
            },
        },
    }
    phase1_messages = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time >= begin_time,
        NextConsoleMessage.create_time <= end_time,
        NextConsoleMessage.msg_llm_type == llm_code
    ).filter(
        NextConsoleMessage.msg_token_used > 0
    ).with_entities(
        db.func.sum(NextConsoleMessage.msg_token_used).label("total_token"),
        db.func.count(NextConsoleMessage.qa_id).label("total_requests"),
        db.func.count(db.distinct(NextConsoleMessage.session_id)).label("total_sessions"),
        db.func.count(db.distinct(NextConsoleMessage.task_id)).label("total_apps"),
        db.func.count(db.distinct(NextConsoleMessage.user_id)).label("total_users"),
    ).first()
    phase2_messages = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time >= last_begin_time,
        NextConsoleMessage.create_time <= begin_time,
        NextConsoleMessage.msg_llm_type == llm_code
    ).filter(
        NextConsoleMessage.msg_token_used > 0
    ).with_entities(
        db.func.sum(NextConsoleMessage.msg_token_used).label("total_token"),
        db.func.count(NextConsoleMessage.qa_id).label("total_requests"),
        db.func.count(db.distinct(NextConsoleMessage.session_id)).label("total_sessions"),
        db.func.count(db.distinct(NextConsoleMessage.task_id)).label("total_apps"),
        db.func.count(db.distinct(NextConsoleMessage.user_id)).label("total_users"),
    ).first()
    if phase1_messages:
        result["data"]["total_token"]["cnt"] = int(
            phase1_messages.total_token) if phase1_messages.total_token else 0
        result["data"]["total_requests"]["cnt"] = int(
            phase1_messages.total_requests) if phase1_messages.total_requests else 0
        result["data"]["total_sessions"]["cnt"] = int(
            phase1_messages.total_sessions) if phase1_messages.total_sessions else 0
        result["data"]["total_apps"]["cnt"] = int(
            phase1_messages.total_apps) if phase1_messages.total_apps else 0
        result["data"]["total_users"]["cnt"] = int(
            phase1_messages.total_users) if phase1_messages.total_users else 0
    if phase2_messages:
        for key in ["total_token", "total_requests", "total_sessions", "total_apps", "total_users"]:
            phase2_value = int(getattr(phase2_messages, key)) if getattr(phase2_messages, key) else 0
            phase1_value = result["data"][key]["cnt"]
            if phase2_value == 0 and phase1_value > 0:
                result["data"][key]["compare"] = 'up'
                result["data"][key]["percent"] = "100%"
            elif phase2_value == 0 and phase1_value == 0:
                result["data"][key]["compare"] = 'up'
                result["data"][key]["percent"] = "0%"
            elif phase2_value > 0 and phase1_value == 0:
                result["data"][key]["compare"] = 'down'
                result["data"][key]["percent"] = "-100%"
            elif phase2_value > 0 and phase1_value > 0:
                change_ratio = (phase1_value - phase2_value) / phase2_value
                if change_ratio > 0:
                    result["data"][key]["compare"] = 'up'
                    result["data"][key]["percent"] = f"{round(change_ratio * 100, 2)}%"
                elif change_ratio < 0:
                    result["data"][key]["compare"] = 'down'
                    result["data"][key]["percent"] = f"{round(change_ratio * 100, 2)}%"
                else:
                    result["data"][key]["compare"] = 'up'
                    result["data"][key]["percent"] = "0%"
    return next_console_response(result=result)


def model_token_time_cnt(params):
    """
    获取模型在不同时间维度的消耗趋势
        官方应用
        自定义应用
    :param params:
    :return:
    """
    user_id = params.get("user_id", 0)
    llm_code = params.get("llm_code", "")
    begin_time = params.get("begin_time", "")
    end_time = params.get("end_time", "")
    time_type = params.get("duration", "day")  # 分钟,小时, 天, 周， 月
    time_format = {
        "minute": "%Y-%m-%d %H:%M",
        "hour": "%Y-%m-%d %H:00",
        "day": "%Y-%m-%d",
        "week": "%Y-%W",
        "month": "%Y-%m"
    }.get(time_type, "%Y-%m-%d")
    result = {
        'xAxis': [],
        'series': [
            {
                'data': [],
            },
            {
                'data': []
            },
        ]
    }
    target_model = LLMInstance.query.filter(
        LLMInstance.llm_code == llm_code
    ).first()
    if not target_model:
        return next_console_response(error_status=True, error_message="模型不存在")
    from app.services.configure_center.model_manager import check_model_authorize
    authorize_check = check_model_authorize(user_id, [target_model], required_access='manage')
    if not authorize_check:
        return next_console_response(error_status=True, error_message="无权限查看该模型数据")
    from sqlalchemy import func, case
    messages = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time >= begin_time,
        NextConsoleMessage.create_time <= end_time,
        NextConsoleMessage.msg_llm_type == llm_code
    ).filter(
        NextConsoleMessage.msg_token_used > 0
    ).group_by(
        func.date_trunc(time_type, NextConsoleMessage.create_time),
        case((NextConsoleMessage.task_id.is_(None), "xiaoyi"), else_="ai"),
    ).with_entities(
        func.date_trunc(time_type, NextConsoleMessage.create_time).label("time_period"),
        case((NextConsoleMessage.task_id.is_(None), "xiaoyi"), else_="ai").label("task_type"),
        func.sum(NextConsoleMessage.msg_token_used).label("total_token"),
    ).order_by(
        func.date_trunc(time_type, NextConsoleMessage.create_time).asc()
    ).all()
    for message in messages:
        if message.time_period.strftime(time_format) not in result['xAxis']:
            result['xAxis'].append(message.time_period.strftime(time_format))
    xiaoyi_map = {
        message.time_period.strftime(time_format): int(message.total_token) for message in messages if message.task_type == 'xiaoyi'
    }
    ai_map = {
        message.time_period.strftime(time_format): int(message.total_token) for message in messages if message.task_type == 'ai'
    }
    for xAxis in result['xAxis']:
        result['series'][0]['data'].append(xiaoyi_map.get(xAxis, 0))
        result['series'][1]['data'].append(ai_map.get(xAxis, 0))
    return next_console_response(result=result)


def model_qa_time_cnt(params):
    """
    查询问答的成功和失败次数
    :param params:
    :return:
    """
    user_id = params.get("user_id", 0)
    llm_code = params.get("llm_code", "")
    begin_time = params.get("begin_time", "")
    end_time = params.get("end_time", "")
    time_type = params.get("duration", "day")  # 分钟,小时, 天, 周， 月
    time_format = {
        "minute": "%Y-%m-%d %H:%M",
        "hour": "%Y-%m-%d %H:00",
        "day": "%Y-%m-%d",
        "week": "%Y-%W",
        "month": "%Y-%m"
    }.get(time_type, "%Y-%m-%d")
    result = {
        'xAxis': [],
        'series': [
            {
                'data': [],
            },
            {
                'data': []
            },
        ]
    }
    target_model = LLMInstance.query.filter(
        LLMInstance.llm_code == llm_code
    ).first()
    if not target_model:
        return next_console_response(error_status=True, error_message="模型不存在")
    from app.services.configure_center.model_manager import check_model_authorize
    authorize_check = check_model_authorize(user_id, [target_model], required_access='manage')
    if not authorize_check:
        return next_console_response(error_status=True, error_message="无权限查看该模型数据")
    from sqlalchemy import func, case
    messages = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time >= begin_time,
        NextConsoleMessage.create_time <= end_time,
        NextConsoleMessage.msg_llm_type == llm_code
    ).group_by(
        func.date_trunc(time_type, NextConsoleMessage.create_time),
        NextConsoleMessage.msg_is_cut_off,
    ).with_entities(
        func.date_trunc(time_type, NextConsoleMessage.create_time).label("time_period"),
        NextConsoleMessage.msg_is_cut_off,
        func.count(NextConsoleMessage.qa_id).label("total_qa"),
    ).order_by(
        func.date_trunc(time_type, NextConsoleMessage.create_time).asc()
    ).all()
    for message in messages:
        if message.time_period.strftime(time_format) not in result['xAxis']:
            result['xAxis'].append(message.time_period.strftime(time_format))
    xiaoyi_map = {
        message.time_period.strftime(time_format): int(message.total_qa) for message in messages if not message.msg_is_cut_off
    }
    ai_map = {
        message.time_period.strftime(time_format): int(message.total_qa) for message in messages if message.msg_is_cut_off
    }
    for xAxis in result['xAxis']:
        result['series'][0]['data'].append(xiaoyi_map.get(xAxis, 0))
        result['series'][1]['data'].append(ai_map.get(xAxis, 0))
    return next_console_response(result=result)


def model_user_time_cnt(params):
    """
    查询使用模型的用户数趋势
    :param params:
    :return:
    """
    user_id = params.get("user_id", 0)
    llm_code = params.get("llm_code", "")
    begin_time = params.get("begin_time", "")
    end_time = params.get("end_time", "")
    time_type = params.get("duration", "day")  # 分钟,小时, 天, 周， 月
    time_format = {
        "minute": "%Y-%m-%d %H:%M",
        "hour": "%Y-%m-%d %H:00",
        "day": "%Y-%m-%d",
        "week": "%Y-%W",
        "month": "%Y-%m"
    }.get(time_type, "%Y-%m-%d")
    result = {
        'xAxis': [],
        'series': [
            {
                'data': [],
            },
        ]
    }
    target_model = LLMInstance.query.filter(
        LLMInstance.llm_code == llm_code
    ).first()
    if not target_model:
        return next_console_response(error_status=True, error_message="模型不存在")
    from app.services.configure_center.model_manager import check_model_authorize
    authorize_check = check_model_authorize(user_id, [target_model], required_access='manage')
    if not authorize_check:
        return next_console_response(error_status=True, error_message="无权限查看该模型数据")
    from sqlalchemy import func
    messages = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time >= begin_time,
        NextConsoleMessage.create_time <= end_time,
        NextConsoleMessage.msg_llm_type == llm_code
    ).group_by(
        func.date_trunc(time_type, NextConsoleMessage.create_time)
    ).with_entities(
        func.date_trunc(time_type, NextConsoleMessage.create_time).label("time_period"),
        func.count(NextConsoleMessage.user_id).label("total_user"),
    ).order_by(
        func.date_trunc(time_type, NextConsoleMessage.create_time).asc()
    ).all()
    for message in messages:
        if message.time_period.strftime(time_format) not in result['xAxis']:
            result['xAxis'].append(message.time_period.strftime(time_format))
            result['series'][0]['data'].append(int(message.total_user))
    return next_console_response(result=result)


def model_session_source_cnt(params):
    """
    查询使用模型的会话数趋势
    :param params:
    :return:
    """
    user_id = params.get("user_id", 0)
    llm_code = params.get("llm_code", "")
    begin_time = params.get("begin_time", "")
    end_time = params.get("end_time", "")
    result = {
        'series': [
            {
                'data': [],
            },
        ]
    }
    target_model = LLMInstance.query.filter(
        LLMInstance.llm_code == llm_code
    ).first()
    if not target_model:
        return next_console_response(error_status=True, error_message="模型不存在")
    from app.services.configure_center.model_manager import check_model_authorize
    authorize_check = check_model_authorize(user_id, [target_model], required_access='manage')
    if not authorize_check:
        return next_console_response(error_status=True, error_message="无权限查看该模型数据")
    from sqlalchemy import func, case
    from app.models.app_center.app_info_model import WorkFlowMetaInfo
    messages = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time >= begin_time,
        NextConsoleMessage.create_time <= end_time,
        NextConsoleMessage.msg_llm_type == llm_code
    ).join(
        NextConsoleSession, NextConsoleSession.id == NextConsoleMessage.session_id
    ).join(
        WorkFlowMetaInfo, WorkFlowMetaInfo.workflow_code == NextConsoleSession.session_task_id
    ).group_by(
        WorkFlowMetaInfo.workflow_name
    ).with_entities(
        WorkFlowMetaInfo.workflow_name,
        func.sum(NextConsoleMessage.msg_token_used).label("total_token"),
    ).order_by(
        func.sum(NextConsoleMessage.msg_token_used).label("total_token").asc()
    ).all()
    office_messages_cnt = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time >= begin_time,
        NextConsoleMessage.create_time <= end_time,
        NextConsoleMessage.msg_llm_type == llm_code
    ).join(
        NextConsoleSession, NextConsoleSession.id == NextConsoleMessage.session_id
    ).filter(
        NextConsoleSession.session_task_id.is_(None)
    ).with_entities(
        func.sum(NextConsoleMessage.msg_token_used).label("total_token"),
    ).first()
    for message in messages:

        result['series'][0]['data'].append({
            "name": message.workflow_name,
            "value": int(message.total_token)
        })
    if office_messages_cnt and office_messages_cnt.total_token:
        result['series'][0]['data'].append({
            "name": "官方应用",
            "value": int(office_messages_cnt.total_token)
        })
    return next_console_response(result=result)


def model_app_top_cnt(params):
    """
    查询使用模型的应用数趋势
    :param params:
    :return:
    """
    user_id = params.get("user_id", 0)
    llm_code = params.get("llm_code", "")
    begin_time = params.get("begin_time", "")
    end_time = params.get("end_time", "")
    result = {
        'yAxis': [],
        'series': [
            {
                'data': [],
            },
        ]
    }
    target_model = LLMInstance.query.filter(
        LLMInstance.llm_code == llm_code
    ).first()
    if not target_model:
        return next_console_response(error_status=True, error_message="模型不存在")
    from app.services.configure_center.model_manager import check_model_authorize
    authorize_check = check_model_authorize(user_id, [target_model], required_access='manage')
    if not authorize_check:
        return next_console_response(error_status=True, error_message="无权限查看该模型数据")

    messages = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time >= begin_time,
        NextConsoleMessage.create_time <= end_time,
        NextConsoleMessage.msg_llm_type == llm_code
    ).filter(
        NextConsoleMessage.task_id.isnot(None)
    ).join(
        NextConsoleSession, NextConsoleSession.id == NextConsoleMessage.session_id
    ).join(
        AppMetaInfo, AppMetaInfo.app_code == NextConsoleSession.session_source
    ).group_by(
        AppMetaInfo.app_name
    ).with_entities(
        AppMetaInfo.app_name,
        func.sum(NextConsoleMessage.msg_token_used).label("total_token"),
    ).order_by(
        func.sum(NextConsoleMessage.msg_token_used).label("total_token").desc()
    ).all()
    office_messages_cnt = NextConsoleMessage.query.filter(
        NextConsoleMessage.create_time >= begin_time,
        NextConsoleMessage.create_time <= end_time,
        NextConsoleMessage.msg_llm_type == llm_code
    ).filter(
        NextConsoleMessage.task_id.is_(None)
    ).with_entities(
        func.sum(NextConsoleMessage.msg_token_used).label("total_token"),
    ).first()
    for message in messages:
        result['yAxis'].append(message.app_name)
        result['series'][0]['data'].append({
            "name": message.app_name,
            "value": int(message.total_token)
        })
    if office_messages_cnt and office_messages_cnt.total_token:
        idx = 0
        insert_flag = False
        for data in result['series'][0]['data']:
            if office_messages_cnt.total_token > data['value']:
                result['yAxis'].insert(idx, "官方应用")
                result['series'][0]['data'].insert(idx, {
                     "name": "官方应用",
                     "value": int(office_messages_cnt.total_token)
                })
                insert_flag = True
                break
            idx += 1
        if not insert_flag:
            result['yAxis'].append("官方应用")
            result['series'][0]['data'].append({
                "name": "官方应用",
                "value": int(office_messages_cnt.total_token)
            })
    return next_console_response(result=result)
