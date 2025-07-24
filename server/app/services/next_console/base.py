from datetime import datetime
import uuid
import hashlib
import pytz
from sqlalchemy import desc, asc, or_
from app.models.next_console.next_console_model import *
from app.models.assistant_center.assistant import Assistant
from app.services.configure_center.response_utils import next_console_response
from app.models.configure_center.user_config import UserConfig
from app.app import app
from app.models.app_center.app_info_model import AppMetaInfo


def add_session(params):
    """
    新增会话
    """
    user_id = int(params.get("user_id"))
    session_topic = params.get("session_topic", "未命名会话")
    session_status = params.get("session_status", "进行中")
    session_assistant_id = params.get("session_assistant_id", -12345)
    session_shop_assistant_id = params.get("session_shop_assistant_id")
    session_task_id = params.get("session_task_id", None)
    session_source = params.get("session_source", "next_search")
    session_task_type = params.get("session_task_type")
    session_vis = params.get("session_vis", True)
    session_search_engine_switch = params.get("session_search_engine_switch")
    session_search_engine_language_type = params.get("session_search_engine_language_type")
    session_search_engine_resource_type = params.get("session_search_engine_resource_type")
    session_llm_code = params.get("session_llm_code")
    session_attachment_image_switch = params.get("session_attachment_image_switch", False)
    session_attachment_file_switch = params.get("session_attachment_file_switch", False)
    session_attachment_webpage_switch = params.get("session_attachment_webpage_switch", False)
    session_local_resource_switch = params.get("session_local_resource_switch", False)
    session_local_resource_use_all = params.get("session_local_resource_use_all", False)
    session_task_params_schema = params.get("session_task_params_schema", {})
    # 使用 UUID4 生成基于随机数的唯一标识符
    unique_id = uuid.uuid4().hex
    # 使用 SHA-256 生成哈希值，保证唯一性和长度一致
    hash_object = hashlib.sha256(unique_id.encode('utf-8'))
    session_code = hash_object.hexdigest()[:18]
    target_user_config = UserConfig.query.filter(
        UserConfig.user_id == user_id
    ).first()
    if not target_user_config:
        app.logger.error(f"用户配置不存在:{user_id}")
        return next_console_response(error_status=True, error_code=1001, error_message="用户配置不存在", result=params)
    if session_search_engine_resource_type is None:
        session_search_engine_resource_type = target_user_config.search_engine_resource_type
    if session_search_engine_language_type is None:
        session_search_engine_language_type = target_user_config.search_engine_language_type
    if session_search_engine_switch is None:
        session_search_engine_switch = False
    target_session_assistant = Assistant.query.filter_by(
        id=session_assistant_id
    ).first()
    if not session_llm_code and target_session_assistant:
        session_llm_code = target_session_assistant.assistant_model_code

    new_session = NextConsoleSession(
        user_id=user_id,
        session_topic=session_topic,
        session_status=session_status,
        session_assistant_id=session_assistant_id,
        session_shop_assistant_id=session_shop_assistant_id,
        session_task_id=session_task_id,
        session_source=session_source,
        session_task_type=session_task_type,
        session_search_engine_switch=session_search_engine_switch,
        session_search_engine_resource_type=session_search_engine_resource_type,
        session_search_engine_language_type=session_search_engine_language_type,
        session_code=session_code,
        session_vis=session_vis,
        session_llm_code=session_llm_code,
        session_attachment_image_switch=session_attachment_image_switch,
        session_attachment_file_switch=session_attachment_file_switch,
        session_attachment_webpage_switch=session_attachment_webpage_switch,
        session_local_resource_switch=session_local_resource_switch,
        session_local_resource_use_all=session_local_resource_use_all,
        session_task_params_schema=session_task_params_schema
    )
    db.session.add(new_session)
    db.session.commit()
    result = new_session.to_dict()
    return next_console_response(result=result)


def update_session(params):
    """
    更新会话
    """
    session_id = params.get("session_id")
    session_topic = params.get("session_topic")
    session_status = params.get("session_status")
    session_remark = params.get("session_remark")
    session_vis = params.get("session_vis")
    session_favorite = params.get("session_favorite")
    session_like_cnt = params.get("session_like_cnt")
    session_dislike_cnt = params.get("session_dislike_cnt")
    session_update_cnt = params.get("session_update_cnt")
    session_share_cnt = params.get("session_share_cnt")
    session_assistant_id = params.get("session_assistant_id")
    session_shop_assistant_id = params.get("session_shop_assistant_id")
    session_search_engine_switch = params.get("session_search_engine_switch")
    session_search_engine_resource_type = params.get("session_search_engine_resource_type")
    session_search_engine_language_type = params.get("session_search_engine_language_type")
    session_llm_code = params.get("session_llm_code")
    target_session = NextConsoleSession.query.filter_by(
        id=session_id,
        user_id=int(params.get("user_id"))
    ).first()
    session_attachment_image_switch = params.get("session_attachment_image_switch")
    session_attachment_file_switch = params.get("session_attachment_file_switch")
    session_attachment_webpage_switch = params.get("session_attachment_webpage_switch")
    session_local_resource_switch = params.get("session_local_resource_switch")
    session_local_resource_use_all = params.get("session_local_resource_use_all")
    session_task_params = params.get("session_task_params", {})
    if not target_session:
        return next_console_response(error_status=True, error_code=1001, error_message="会话不存在", result=params)

    if session_topic:
        target_session.session_topic = session_topic[:200]
    if session_status:
        target_session.session_status = session_status
    if session_remark is not None:
        target_session.session_remark = session_remark
    if session_vis is not None:
        target_session.session_vis = session_vis
    if session_favorite is not None:
        target_session.session_favorite = session_favorite
    if session_like_cnt:
        target_session.session_like_cnt += session_like_cnt
    if session_dislike_cnt:
        target_session.session_dislike_cnt += session_dislike_cnt
    if session_update_cnt:
        target_session.session_update_cnt += session_update_cnt
    if session_share_cnt:
        target_session.session_share_cnt += session_share_cnt
    if session_assistant_id is not None:
        target_session.session_assistant_id = session_assistant_id
    if session_shop_assistant_id:
        target_session.session_shop_assistant_id = session_shop_assistant_id
    if session_search_engine_switch in (0, 1, 2):
        target_session.session_search_engine_switch = session_search_engine_switch
    if session_search_engine_resource_type in ("search", "news", "scholar"):
        target_session.session_search_engine_resource_type = session_search_engine_resource_type
    if session_search_engine_language_type is not None:
        target_session.session_search_engine_language_type = session_search_engine_language_type
    if session_llm_code is not None:
        target_session.session_llm_code = session_llm_code
    if session_attachment_image_switch is not None:
        target_session.session_attachment_image_switch = session_attachment_image_switch
    if session_attachment_file_switch is not None:
        target_session.session_attachment_file_switch = session_attachment_file_switch
    if session_attachment_webpage_switch is not None:
        target_session.session_attachment_webpage_switch = session_attachment_webpage_switch
    if session_local_resource_switch is not None:
        target_session.session_local_resource_switch = session_local_resource_switch
        if not session_local_resource_switch:
            target_session.session_local_resource_use_all = False
    if session_local_resource_use_all is not None:
        target_session.session_local_resource_use_all = session_local_resource_use_all
    if session_task_params is not None:
        target_session.session_task_params = session_task_params
    try:
        db.session.add(target_session)
        db.session.commit()
    except Exception as e:
        return next_console_response(error_status=True, error_code=1001, error_message=str(e), result=params)
    return next_console_response(result=target_session.to_dict())


def delete_session(params):
    """
    删除会话
    """
    session_id = params.get("session_id")
    session = NextConsoleSession.query.filter_by(id=session_id).first()
    if session:
        session.session_vis = False
        db.session.commit()
    return next_console_response()


def search_session(params):
    """
    搜索会话
    """
    user_id = int(params.get("user_id"))
    session_ids = params.get("session_ids", [])
    session_codes = params.get("session_codes", [])
    session_topic = params.get("session_topic")
    session_vis = params.get("session_vis", [True])
    session_status = params.get("session_status", [])
    session_remark = params.get("session_remark", [])
    session_assistant_id = params.get("session_assistant_id", [])
    session_favorite = params.get("session_favorite", [])
    session_remark_like = params.get("session_remark_like", False)
    session_remark_dislike = params.get("session_remark_dislike", False)
    session_remark_update = params.get("session_remark_update", False)
    session_remark_share = params.get("session_remark_share", False)
    session_task_id = params.get("session_task_id")
    session_source = params.get("session_source")
    session_task_type = params.get("session_task_type")
    session_update_time_rage = params.get("update_time", [])
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 100)
    fetch_all = params.get("fetch_all", False)
    all_conditions = [
        NextConsoleSession.user_id == user_id,
        NextConsoleSession.session_status != "测试",
    ]
    # 增加任务ID的过滤支持
    if session_task_id:
        all_conditions.append(NextConsoleSession.session_task_id == session_task_id)
        # 没有任务ID的会话则新增会话
        task_session_list = NextConsoleSession.query.filter(
            *all_conditions
        ).all()
        if not task_session_list:
            new_session_params = {
                "user_id": user_id,
                "session_assistant_id": -12345,
                "session_task_id": session_task_id,
                "session_status": "进行中",
                "session_source": session_source,
            }
            add_session(new_session_params)
    if session_ids:
        all_conditions.append(NextConsoleSession.id.in_(session_ids))
    if session_codes:
        all_conditions.append(NextConsoleSession.session_code.in_(session_codes))
    if session_topic:
        all_conditions.append(NextConsoleSession.session_topic.like("%{}%".format(session_topic)))
    if session_remark:
        all_conditions.append(NextConsoleSession.session_remark.in_(session_remark))
    if session_vis:
        all_conditions.append(NextConsoleSession.session_vis.in_(session_vis))
    if session_status:
        all_conditions.append(NextConsoleSession.session_status.in_(session_status))
    if session_assistant_id:
        all_conditions.append(NextConsoleSession.session_assistant_id.in_(session_assistant_id))
    if session_favorite:
        all_conditions.append(NextConsoleSession.session_favorite.in_(session_favorite))
    if session_source:
        all_conditions.append(NextConsoleSession.session_source == session_source)
    if session_task_type:
        all_conditions.append(NextConsoleSession.session_task_type == session_task_type)
    if session_update_time_rage:
        start_date = datetime.fromisoformat(session_update_time_rage[0].rstrip('Z'))
        end_date = datetime.fromisoformat(session_update_time_rage[1].rstrip('Z'))
        start_date_utc = start_date.replace(tzinfo=pytz.utc)
        end_date_utc = end_date.replace(tzinfo=pytz.utc)
        # 转换到东八区时间
        eastern_eight_zone = pytz.timezone('Asia/Shanghai')
        start_date_east8 = start_date_utc.astimezone(eastern_eight_zone)
        end_date_east8 = end_date_utc.astimezone(eastern_eight_zone)
        all_conditions.append(NextConsoleSession.update_time >= start_date_east8)
        all_conditions.append(NextConsoleSession.update_time <= end_date_east8)
    or_condition = []
    if session_remark_like:
        or_condition.append(NextConsoleSession.session_like_cnt > 0)
    if session_remark_dislike:
        or_condition.append(NextConsoleSession.session_dislike_cnt > 0)
    if session_remark_update:
        or_condition.append(NextConsoleSession.session_update_cnt > 0)
    if session_remark_share:
        or_condition.append(NextConsoleSession.session_share_cnt > 0)
    if session_remark == [1] and or_condition == []:
        return next_console_response(result=[])
    all_conditions.append(or_(*or_condition))
    session_list = NextConsoleSession.query.filter(
        NextConsoleSession.user_id == user_id,
        *all_conditions
    ).order_by(
        desc(NextConsoleSession.update_time))
    if fetch_all:
        session_list = session_list.all()
    else:
        session_list = session_list.paginate(
            page=page_num, per_page=page_size, error_out=False)
    session_list = [session.to_dict() for session in session_list]
    # 填充助手信息
    all_assistant_id = list(set([session["session_assistant_id"] for session in session_list]))
    all_assistant_info = Assistant.query.filter(
        Assistant.id.in_(all_assistant_id)
    ).all()

    assistant_info_dict = {assistant.id: assistant.to_dict() for assistant in all_assistant_info}


    for session in session_list:
        assistant_id = session["session_assistant_id"]
        assistant_info = assistant_info_dict.get(assistant_id)
        if assistant_info:
            session["session_assistant_id"] = assistant_info_dict.get(assistant_id).get("id", "")
            session["session_assistant_name"] = assistant_info_dict.get(assistant_id).get("assistant_name", "")
            session["session_assistant_avatar"] = assistant_info_dict.get(assistant_id).get("assistant_avatar", "")
            session["session_assistant_desc"] = assistant_info_dict.get(assistant_id).get("assistant_desc", "")
    # 填充应用信息
    all_app_ids = list(set([session["session_source"] for session in session_list if session["session_source"]]))
    all_app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code.in_(all_app_ids)
    ).all()
    app_info_dict = {app.app_code: app.to_dict() for app in all_app_info}
    for session in session_list:
        app_code = session["session_source"]
        if app_code and app_code in app_info_dict:
            session["app_name"] = app_info_dict[app_code].get("app_name", "")
            session["app_icon"] = app_info_dict[app_code].get("app_icon", "")
        else:
            session["app_name"] = ""
            session["app_icon"] = ""

    return next_console_response(result=session_list)


def add_qa(params):
    """
    新增问答
    """
    user_id = int(params.get("user_id"))
    session_id = params.get("session_id")
    qa_topic = params.get("qa_topic")
    new_qa = NextConsoleQa(
        user_id=user_id,
        session_id=session_id,
        qa_topic=qa_topic
    )
    db.session.add(new_qa)
    db.session.flush()
    db.session.commit()
    return next_console_response(result=new_qa.to_dict())


def update_qa(params):
    """
    更新问答
    """
    user_id = int(params.get("user_id"))
    qa_id = params.get("qa_id")
    qa_status = params.get("qa_status")
    qa_topic = params.get("qa_topic")
    qa_del = params.get("qa_del")
    new_update_params = {}
    if qa_status:
        new_update_params["qa_status"] = qa_status
    if qa_topic:
        new_update_params["qa_topic"] = qa_topic
    if qa_del:
        new_update_params["qa_del"] = qa_del
    NextConsoleQa.query.filter_by(
        qa_id=qa_id, user_id=user_id).update(new_update_params)
    db.session.commit()
    return next_console_response()


def delete_qa(params):
    """
    删除问答
    """
    qa_id = params.get("qa_id")
    qa = NextConsoleQa.query.filter_by(qa_id=qa_id).first()
    if qa:
        qa.qa_del = True
        db.session.commit()
    return next_console_response()


def search_qa(params):
    """
    搜索问答
    """
    user_id = int(params.get("user_id"))
    session_id = params.get("session_id", [])
    qa_id = params.get("qa_id", [])
    qa_status = params.get("qa_status", ["新建", "进行中", "已结束", "清除", "正常"])
    qa_topic = params.get("qa_topic")
    qa_del = params.get("qa_del", [False])
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 100)
    fetch_all = params.get("fetch_all", False)
    if not user_id:
        return next_console_response(error_status=True, error_code=1001, error_message="用户ID为空", result=params)
    all_conditions = [NextConsoleQa.user_id == user_id]
    if qa_id:
        all_conditions.append(NextConsoleQa.qa_id.in_(qa_id))
    if session_id:
        all_conditions.append(NextConsoleQa.session_id.in_(session_id))
    if qa_status:
        all_conditions.append(NextConsoleQa.qa_status.in_(qa_status))
    if qa_topic:
        all_conditions.append(NextConsoleQa.qa_topic.like("%{}%".format(qa_topic)))
    if qa_del:
        all_conditions.append(NextConsoleQa.qa_del.in_(qa_del))
    qa_list = NextConsoleQa.query.filter(
        NextConsoleQa.user_id == user_id,
        *all_conditions
    ).order_by(
        desc(NextConsoleQa.create_time))
    if not fetch_all:
        qa_list = qa_list.paginate(page=page_num, per_page=page_size, error_out=False)
    else:
        qa_list = qa_list.all()
    qa_list = [qa.to_dict() for qa in qa_list]
    return next_console_response(result=qa_list)


def search_messages(params, in_call=False):
    """
    搜索消息:
    """
    msg_id = params.get("msg_id", [])
    user_id = int(params.get("user_id"))
    session_id = params.get("session_id", [])
    qa_id = params.get("qa_id", [])
    msg_format = params.get("msg_format", [])
    msg_llm_type = params.get("msg_llm_type", [])
    msg_role = params.get("msg_role", [])
    msg_remark = params.get("msg_remark", [])
    msg_del = params.get("msg_del", [0])
    msg_version = params.get("msg_version", [])
    order = params.get("order", "desc")
    if not qa_id:
        if in_call:
            return []
        return next_console_response(result=[])
    # 过滤条件
    if not user_id:
        return next_console_response(error_status=True, error_code=1001, error_message="用户ID为空", result=params)
    all_conditions = []
    if msg_id:
        all_conditions.append(NextConsoleMessage.msg_id.in_(msg_id))
    if session_id:
        all_conditions.append(NextConsoleMessage.session_id.in_(session_id))
    if qa_id:
        all_conditions.append(NextConsoleMessage.qa_id.in_(qa_id))
    if msg_format:
        all_conditions.append(NextConsoleMessage.msg_format.in_(msg_format))
    if msg_llm_type:
        all_conditions.append(NextConsoleMessage.msg_llm_type.in_(msg_llm_type))
    if msg_role:
        all_conditions.append(NextConsoleMessage.msg_role.in_(msg_role))
    if msg_remark:
        all_conditions.append(NextConsoleMessage.msg_remark.in_(msg_remark))
    if msg_del:
        all_conditions.append(NextConsoleMessage.msg_del.in_(msg_del))
    if msg_version:
        all_conditions.append(NextConsoleMessage.msg_version.in_(msg_version))
    if order == "desc":
        messages_list = NextConsoleMessage.query.filter(
            NextConsoleMessage.user_id == user_id,
            *all_conditions
        ).order_by(
            desc(NextConsoleMessage.session_id),
            desc(NextConsoleMessage.qa_id),
            asc(NextConsoleMessage.msg_version),
            asc(NextConsoleMessage.msg_remark)
        )
    else:
        messages_list = NextConsoleMessage.query.filter(
            NextConsoleMessage.user_id == user_id,
            *all_conditions
        ).order_by(
            asc(NextConsoleMessage.session_id),
            asc(NextConsoleMessage.qa_id),
            asc(NextConsoleMessage.msg_version),
            asc(NextConsoleMessage.msg_remark)
        )
    messages_list = [message.to_dict() for message in messages_list]
    messages_list.reverse()
    if in_call:
        return messages_list
    return messages_list


def add_messages(params, inner_call=False):
    """
    新增消息
    """
    user_id = int(params.get("user_id"))
    session_id = params.get("session_id")
    qa_id = params.get("qa_id")
    assistant_id = params.get("assistant_id")
    if not (user_id and session_id and qa_id):
        return next_console_response(error_status=True, error_message="参数错误")

    msg_role = params.get("msg_role", "user")
    msg_prompt = params.get("msg_prompt", "")
    msg_content = params.get("msg_content", "")
    msg_inner_content = params.get("msg_inner_content")
    msg_token_used = params.get("msg_token_used", 0)
    msg_time_used = params.get("msg_time_used", 0)
    msg_llm_type = params.get("msg_llm_type", "deepseek-chat")
    msg_format = params.get("msg_format", "text")
    msg_remark = params.get("msg_remark", 0)
    msg_del = params.get("msg_vis", 0)
    msg_parent_id = params.get("msg_parent_id", None)
    msg_version = params.get("msg_version")
    if msg_version is None:
        pre_msg = NextConsoleMessage.query.filter(
            NextConsoleMessage.qa_id == qa_id,
            NextConsoleMessage.msg_role == msg_role,
        ).order_by(
            desc(NextConsoleMessage.msg_version)
        ).first()
        if pre_msg:
            msg_version = pre_msg.msg_version + 1
        else:
            msg_version = 0
    # 保存提问
    new_message = NextConsoleMessage(
        user_id=user_id,
        session_id=session_id,
        qa_id=qa_id,
        assistant_id=assistant_id,
        msg_llm_type=msg_llm_type,
        msg_role=msg_role,
        msg_prompt=msg_prompt,
        msg_content=msg_content,
        msg_inner_content=msg_inner_content,
        msg_token_used=msg_token_used,
        msg_time_used=msg_time_used,
        msg_format=msg_format,
        msg_remark=msg_remark,
        msg_del=msg_del,
        msg_version=msg_version,
        msg_parent_id=msg_parent_id
    )
    db.session.add(new_message)
    db.session.commit()
    params["msg_id"] = new_message.msg_id
    if assistant_id and (assistant_id > 0 or assistant_id != -12345):
        target_session = NextConsoleSession.query.filter_by(
            id=session_id,
            user_id=user_id
        ).first()
        if target_session:
            target_session.session_assistant_id = assistant_id
            target_session.session_shop_assistant_id = None
            db.session.add(target_session)
            db.session.commit()
    if inner_call:
        return params
    return next_console_response(result=new_message.to_dict())


def update_messages(params):
    """
    更新消息
    """

    msg_id = params.get("msg_id")
    user_id = int(params.get("user_id"))
    msg_role = params.get("msg_role")
    msg_prompt = params.get("msg_prompt")
    msg_content = params.get("msg_content")
    msg_remark = params.get("msg_remark")
    msg_del = params.get("msg_del")
    msg_version = params.get("msg_version")
    msg_inner_content = params.get("msg_inner_content")
    msg_token_used = params.get("msg_token_used")
    msg_time_used = params.get("msg_time_used")
    msg_llm_type = params.get("msg_llm_type")
    msg_is_cut_off = params.get("msg_is_cut_off")
    reasoning_content = params.get("reasoning_content")
    target_msg = NextConsoleMessage.query.filter_by(
        msg_id=msg_id,
        user_id=user_id
    ).first()
    if not target_msg:
        return next_console_response(error_status=True, error_message="消息不存在", result=params)
    session_id = target_msg.session_id
    target_session = NextConsoleSession.query.filter_by(
        id=session_id,
        user_id=user_id
    ).first()
    if not target_session:
        return next_console_response(error_status=True, error_message="会话不存在", result=params)
    if msg_role and msg_role != target_msg.msg_role:
        target_msg.msg_role = msg_role
    if msg_prompt and msg_prompt != target_msg.msg_prompt:
        target_msg.msg_prompt = msg_prompt
    if msg_content and msg_content != target_msg.msg_content:
        target_msg.msg_content = msg_content
        target_session.session_remark = 1
        target_session.session_update_cnt += 1
    if msg_remark is not None and msg_remark != target_msg.msg_remark:
        target_session.session_remark = 1
        if msg_remark == 1:
            target_session.session_like_cnt += 1
            if target_msg.msg_remark != 0:
                target_session.session_dislike_cnt -= 1

        elif msg_remark == -1:
            target_session.session_dislike_cnt += 1
            if target_msg.msg_remark != 0:
                target_session.session_like_cnt -= 1

        target_msg.msg_remark = msg_remark
    if msg_del and msg_del != target_msg.msg_del:
        target_msg.msg_del = msg_del
    if msg_version and msg_version != target_msg.msg_version:
        target_msg.msg_version = msg_version
    if msg_inner_content is not None and msg_inner_content != target_msg.msg_inner_content:
        target_msg.msg_inner_content = msg_inner_content
    if msg_token_used is not None and msg_token_used != target_msg.msg_token_used:
        target_msg.msg_token_used = msg_token_used
    if msg_time_used is not None and msg_time_used != target_msg.msg_time_used:
        target_msg.msg_time_used = msg_time_used
    if msg_llm_type is not None and msg_llm_type != target_msg.msg_llm_type:
        target_msg.msg_llm_type = msg_llm_type
    if msg_is_cut_off is not None and msg_is_cut_off != target_msg.msg_is_cut_off:
        target_msg.msg_is_cut_off = msg_is_cut_off
    if reasoning_content is not None and reasoning_content != target_msg.reasoning_content:
        target_msg.reasoning_content = reasoning_content
    db.session.add(target_msg)
    try:
        db.session.commit()
        return next_console_response(result=target_msg.to_dict())
    except Exception as e:
        return next_console_response(error_status=True, error_message=str(e), result=params)


def delete_messages(params):
    """
    删除消息
    """
    msg_id_list = params.get("msg_id", [])
    msg_del = params.get("msg_del", 1)
    qa_id = params.get("qa_id", None)
    msg_version = params.get("msg_version", None)
    # 更新 msg_id 在 msg_id_list 中的所有消息
    res = NextConsoleMessage.query.filter(NextConsoleMessage.msg_id.in_(msg_id_list)).update(
        {NextConsoleMessage.msg_del: msg_del}, synchronize_session=False)
    db.session.commit()
    if msg_version:
        other_version = NextConsoleMessage.query.filter(
         NextConsoleMessage.qa_id == qa_id,
         NextConsoleMessage.msg_version > msg_version,
         NextConsoleMessage.msg_del == 0
        )
        for record in other_version:
            record.msg_version -= 1
        db.session.commit()
    return next_console_response()


