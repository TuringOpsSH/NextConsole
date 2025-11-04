
from app.models.app_center.app_info_model import AppMetaInfo
from sqlalchemy import and_, case, func, literal_column, cast, Integer, Numeric, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from app.app import app
from app.models.next_console.next_console_model import *
# from app.models.user_center.user_package_info import *
# from app.models.user_center.user_package_relation import *
# from app.models.user_center.user_token_sta_info import *
# from app.models.user_center.user_token_used_current_info import *
from app.models.user_center.user_info import *
from app.services.configure_center.response_utils import next_console_response
from app.services.next_console.next_console import next_console_search_messages


def lookup_session_details(params):
    """
    查询 session 会话信息详情
    """
    user_id = int(params.get("user_id"))
    create_start_date = params.get("create_start_date")
    create_end_date = params.get("create_end_date")
    session_topic = params.get("session_topic")
    session_favorite = params.get("session_favorite")
    session_remark = params.get("session_remark")
    session_user_id = params.get("session_user_id")
    try:
        session_user_id = int(session_user_id)
    except (TypeError, ValueError):
        session_user_id = 0
    session_source = params.get("session_source", [])
    tag = params.get("tag")
    page_num = params.get("page_num", 1)
    page_size = params.get("page_size", 20)

    all_condition = [
        NextConsoleSession.session_source != "support_ticket",
        NextConsoleSession.session_source != "online_service",
    ]
    check_session_source_list = []
    is_nc_admin = check_has_role(user_id, "next_console_admin")
    admin_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    for session_source_item in session_source:
        if session_source_item in ('support_ticket', 'online_service'):
            continue
        if is_nc_admin:
            check_session_source_list.append(session_source_item)
            continue
    if create_start_date:
        all_condition.append(NextConsoleSession.create_time >= create_start_date)
    if create_end_date:
        all_condition.append(NextConsoleSession.create_time <= create_end_date)
    if session_topic:
        all_condition.append(NextConsoleSession.session_topic.like(f"%{session_topic}%"))
    if session_favorite is not None:
        all_condition.append(NextConsoleSession.session_favorite == session_favorite)
    if session_remark is not None:
        all_condition.append(NextConsoleSession.session_remark == session_remark)
    if session_user_id:
        all_condition.append(NextConsoleSession.user_id == session_user_id)
    if check_session_source_list:
        all_condition.append(NextConsoleSession.session_source.in_(check_session_source_list))
    target_sessions = NextConsoleSession.query.filter(
        and_(*all_condition)
    )
    if not is_nc_admin:
        target_sessions = target_sessions.join(
            UserInfo,
            UserInfo.user_id == NextConsoleSession.user_id
        ).filter(
            UserInfo.user_company_id == admin_user.user_company_id
        )
    total = target_sessions.count()
    target_sessions = target_sessions.order_by(
        NextConsoleSession.create_time.desc()
    ).paginate(page=page_num, per_page=page_size, error_out=False)
    # 计算qa_cnt and msg_token_used
    target_session_ids = [session.id for session in target_sessions]
    all_idx = NextConsoleMessage.query.filter(
        NextConsoleMessage.session_id.in_(target_session_ids)
    ).group_by(NextConsoleMessage.session_id).with_entities(
        NextConsoleMessage.session_id,
        func.count(func.distinct(NextConsoleMessage.qa_id)).label("qa_cnt"),
        func.sum(NextConsoleMessage.msg_token_used).label("msg_token_used")
    ).all()
    all_idx_dict = {idx[0]: {"qa_cnt": idx[1], "msg_token_used": idx[2]} for idx in all_idx}
    all_session_sources = list(set([session.session_source for session in target_sessions]))
    all_app_info = AppMetaInfo.query.filter(
        AppMetaInfo.app_code.in_(all_session_sources),
        AppMetaInfo.app_status == "正常",
        AppMetaInfo.environment == "生产"
    ).all()
    all_app_info_dict = {app.app_code: app.to_dict() for app in all_app_info}
    session_list = []
    for session in target_sessions:
        session_dict = session.to_dict()
        session_dict["qa_cnt"] = all_idx_dict.get(session.id, {}).get("qa_cnt", 0)
        session_dict["msg_token_used"] = all_idx_dict.get(session.id, {}).get("msg_token_used", 0)
        session_dict["session_source"] = all_app_info_dict.get(session.session_source)
        if not session_dict["session_source"]:
            if session.session_source == "next_search":
                session_dict["session_source"] = {
                    "app_code": "next_search",
                    "app_name": "小亦助手",
                    "app_icon": "/images/logo.svg"
                }
                from app.models.configure_center.system_config import SystemConfig
                system_config = SystemConfig.query.filter(
                    SystemConfig.config_key == "ai",
                    SystemConfig.config_status == 1
                ).first()
                if system_config:
                    xiaoyi_config = system_config.config_value.get("xiaoyi", {})
                    if xiaoyi_config.get("avatar_url"):
                        session_dict["session_source"]["app_icon"] = xiaoyi_config.get("avatar_url")
                    if xiaoyi_config.get("name"):
                        session_dict["session_source"]["app_name"] = xiaoyi_config.get("name")
            elif session.session_source == "support_ticket":
                session_dict["session_source"] = {
                    "app_code": "support_ticket",
                    "app_name": "帮助工单",
                    "app_icon": "/images/tickets_blue.svg"
                }
            elif session.session_source == "online_service":
                session_dict["session_source"] = {
                    "app_code": "online_service",
                    "app_name": "在线支持",
                    "app_icon": "/images/online_service_blue.svg"
                }
            else:
                session_dict["session_source"] = {
                    "app_code": session.session_source,
                    "app_name": "未知",
                    "app_icon": "/images/unknown_service.svg"
                }
        session_list.append(session_dict)
    return next_console_response(result={
        "total": total,
        "data": session_list
    })


def search_session_source(params):
    """
    查询session_source
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    keyword = params.get("keyword")
    is_nc_admin = check_has_role(user_id, "next_console_admin")
    admin_user = UserInfo.query.filter(UserInfo.user_id == user_id).first()
    all_condition = [
        AppMetaInfo.app_status == "正常",
        AppMetaInfo.environment == "生产"
    ]
    if keyword:
        all_condition.append(
            or_(
                AppMetaInfo.app_code.like(f"%{keyword}%"),
                AppMetaInfo.app_name.like(f"%{keyword}%"),
                AppMetaInfo.app_desc.like(f"%{keyword}%")
            )
        )
    if not is_nc_admin:
        all_session_sources = UserInfo.query.filter(
            UserInfo.user_company_id == admin_user.user_company_id
        ).join(
            NextConsoleSession,
            NextConsoleSession.user_id == UserInfo.user_id
        ).with_entities(NextConsoleSession.session_source).distinct().all()
        all_session_sources = [session_source[0] for session_source in all_session_sources]
        all_condition.append(
            AppMetaInfo.app_code.in_(all_session_sources)
        )
    all_source_apps = AppMetaInfo.query.filter(
        *all_condition
    ).all()
    result = {
        "total": len(all_source_apps),
        "data": [source_app.to_dict() for source_app in all_source_apps]
    }
    return next_console_response(result=result)


def addtag_session_details(params):
    """
    给特定session添加标签
    """
    session_id = params.get("session_id")
    tag = params.get("tag")
    user_id = int(params.get("user_id"))
    if not session_id:
        return next_console_response(error_status=True, error_code=1004, error_message="session_id不能为空！")
    elif tag is None:
        return next_console_response(error_status=True, error_code=1004, error_message="tag不能为空！")
    elif not user_id:
        return next_console_response(error_status=True, error_code=1004, error_message="user_id不能为空！")
    # 如果tag已经在，则返回tag_id，如果tag不存在，则创建tag
    else:
        try:
            if str(tag).strip() != "":
                tag_list = tag.split(',')
                # NextConsoleSessionTagRelation.query.filter(NextConsoleSessionTagRelation.session_id == session_id).delete()
                # db.session.commit()
                # 获取当前session的所有标签tag_name，组成一个list，与taglist比较，如果taglist中的tag不在当前session的标签中，则添加
                cur_tag_name_list = []
                cur_tag_dict = {}
                cur_session = NextConsoleSessionTagRelation.query.with_entities(
                        NextConsoleTag.tag_name,
                        NextConsoleSessionTagRelation.tag_id
                    ).filter(NextConsoleSessionTagRelation.session_id == session_id).join(NextConsoleTag, NextConsoleTag.tag_id == NextConsoleSessionTagRelation.tag_id).all()
                for cur_tag in cur_session:
                    cur_tag_name_list.append(cur_tag[0])
                    cur_tag_dict[cur_tag[0]] = cur_tag[1]
                
                # 标签去重
                tag_list = list(set(tag_list))
                cur_tag_name_list = list(set(cur_tag_name_list))

                # 两个标签集相减，获得需要删除的标签和需要添加的标签
                set_org_tag = set(cur_tag_name_list)
                set_dest_tag = set(tag_list)
                del_tag = set_org_tag - set_dest_tag
                add_tag = set_dest_tag - set_org_tag
                # 新增tag不存在的话，先初始化新增的tag
                for tag in add_tag:
                    tag_row = NextConsoleTag.query.filter(NextConsoleTag.tag_name == tag).first()
                    if not tag_row:
                        tag_row = NextConsoleTag(tag_name=tag, create_user_id=user_id)
                        db.session.add(tag_row)
                db.session.commit()
                # 删除session的标签
                for tag in del_tag:
                    session_tag = NextConsoleSessionTagRelation.query.filter(
                            and_(NextConsoleSessionTagRelation.session_id == session_id, NextConsoleSessionTagRelation.tag_id == cur_tag_dict[tag])).first()
                    db.session.delete(session_tag)
                # 添加session的标签
                for tag in add_tag:
                    tag_row = NextConsoleTag.query.filter(NextConsoleTag.tag_name == tag).first()
                    session_tag = NextConsoleSessionTagRelation(
                        session_id=session_id,
                        tag_id=tag_row.tag_id,
                        create_user_id=user_id)
                    db.session.add(session_tag)
                db.session.commit()
                return next_console_response(result="添加标签成功！")
            else:
                # 删除session的所有标签
                NextConsoleSessionTagRelation.query.filter(NextConsoleSessionTagRelation.session_id == session_id).delete()
                db.session.commit()
                return next_console_response(result="删除标签成功！")
        except Exception as e:
            print(e)
            app.logger.error(e)
            return next_console_response(error_status=True, error_code=2001, error_message="添加标签失败！")


def lookuptag_session_details(params):
    """
    查询特定session的标签
    """
    session_id = params.get("session_id")
    if not session_id:
        return next_console_response(error_status=True, error_code=1004, error_message="session_id不能为空！")
    else:
        try:
            tag_list = []
            tag_ids = NextConsoleSessionTagRelation.query.filter(NextConsoleSessionTagRelation.session_id == session_id).all()
            for tag_id in tag_ids:
                tag = NextConsoleTag.query.filter(NextConsoleTag.tag_id == tag_id.tag_id).first()
                tag_list.append(tag.tag_name)
            return next_console_response(result={"session_id":session_id,"tag_list":tag_list})
        except Exception as e:
            return next_console_response(error_status=True, error_code=2001, error_message="查询标签失败！")


def lookup_session_message_details(params):
    """
    传进来一个session_id，返回session_id对应的message详情
    """
    session_id = params.get("session_id")
    if not session_id:
        return next_console_response(error_status=True, error_code=1004, error_message="session_id不能为空！")
    else:
        try:
            # 根据session_id 查询qa_id
            qa_id = []
            qa = NextConsoleQa.query.filter(
                NextConsoleQa.session_id == session_id,

            ).all()
            for q in qa:
                qa_id.append(q.qa_id)
        except Exception as e:
            return next_console_response(error_status=True, error_code=2001, error_message="查询qa_id失败！")
        if not qa_id:
            return next_console_response(result=[])
        params["qa_id"] = qa_id
        params["fetch_all"] = True
        message = next_console_search_messages(params)
        result = message.get_json()["result"]
        admin_msg = NextConsoleLlmMsgAdminEvaluate.query.filter(
            NextConsoleLlmMsgAdminEvaluate.session_id == session_id).all()
        if admin_msg is not None:
            admin_msg_dict = {msg.msg_id: msg.admin_msg_remark for msg in admin_msg}
        else:
            admin_msg_dict = {}
        # 将 admin_msg_dict 中的msg_id 对应 admin_msg_remark 添加到 message_list 中的每个对应msg_id的message中
        for qa in result:
            for msg_id,msg_list in qa["qa_value"]["answer"].items():
                for msg in msg_list:
                    msg["admin_msg_remark"] = admin_msg_dict.get(msg["msg_id"], 0)

        return next_console_response(result=result)


def update_admin_favorite(params):
    """
    更新session的session_admin_favorite 管理员收藏标志
    """
    session_id = params.get("session_id")
    admin_session_favorite = params.get("admin_session_favorite")
    operate_user_id = int(params.get("user_id"))
    if not session_id:
        return next_console_response(error_status=True, error_code=1004, error_message="session_id不能为空！")
    elif admin_session_favorite not in [0, 1]:
        return next_console_response(error_status=True, error_code=1004, error_message="admin_favorite格式错误！")
    elif not operate_user_id:
        return next_console_response(error_status=True, error_code=1004, error_message="user_id不能为空！")
    else:
        try:
            session = NextConsoleSessionAdminEvaluate.query.filter(NextConsoleSessionAdminEvaluate.session_id == session_id).first()
            # 查询 session 是否存在，如果不存在，则插一条记录，如果存在，则更新 admin_session_favorite 字段值
            if not session:
                user = NextConsoleSession.query.with_entities(
                    NextConsoleSession.user_id).filter(NextConsoleSession.id == session_id).first()
                session = NextConsoleSessionAdminEvaluate(
                    session_id=session_id, user_id=user[0], operate_user_id=operate_user_id)
                db.session.add(session)
            session.admin_session_favorite = admin_session_favorite
            session.operate_user_id = operate_user_id
            db.session.commit()
            return next_console_response(result="更新admin_session_favorite成功！")
        except Exception as e:
            return next_console_response(error_status=True, error_code=2001, error_message="更新admin_session_favorite失败！")


def lookup_admin_favorite(params):
    """
    查询管理员收藏的session
    """
    session_id = params.get("session_id")
    if not session_id:
        return next_console_response(error_status=True, error_code=1004, error_message="session_id不能为空！")
    else:
        try:
            session = NextConsoleSessionAdminEvaluate.query.filter(
                NextConsoleSessionAdminEvaluate.session_id == session_id).first()
            if session:
                return next_console_response(result={
                    "session_id": session_id,
                    "admin_session_favorite": session.admin_session_favorite})
            else:
                return next_console_response(result={"session_id": session_id,"admin_session_favorite": 0})
        except Exception as e:
            return next_console_response(
                error_status=True, error_code=2001, error_message="查询admin_session_favorite失败！")


def update_admin_msg_like(params):
    """
    更新管理员对于message的点赞和点踩信息
    """
    msg_id = params.get("msg_id")
    admin_msg_remark = params.get("admin_msg_remark")
    operate_user_id = int(params.get("user_id"))
    if not msg_id:
        return next_console_response(error_status=True, error_code=1004, error_message="msg_id不能为空！")
    elif admin_msg_remark not in [-1, 0, 1]:
        return next_console_response(error_status=True, error_code=1004, error_message="admin_msg_remark格式错误！")
    elif not operate_user_id:
        return next_console_response(error_status=True, error_code=1004, error_message="user_id不能为空！")
    else:
        try:
            message = NextConsoleLlmMsgAdminEvaluate.query.filter(NextConsoleLlmMsgAdminEvaluate.msg_id == msg_id).first()
            # 查询 message 是否存在，如果不存在，则插一条记录，如果存在，则更新 msg_remark 字段值，同时还要更新 NextConsoleSessionAdminEvaluateInfo 的点踩计数和点赞计数
            if not message:
                msg_info = NextConsoleMessage.query.with_entities(NextConsoleMessage.session_id,NextConsoleMessage.user_id).filter(NextConsoleMessage.msg_id == msg_id).first()
                message = NextConsoleLlmMsgAdminEvaluate(msg_id=msg_id, session_id=msg_info[0], user_id=msg_info[1], admin_msg_remark=admin_msg_remark,operate_user_id=operate_user_id)
                db.session.add(message)
                message = NextConsoleLlmMsgAdminEvaluate.query.filter(NextConsoleLlmMsgAdminEvaluate.msg_id == msg_id).first()
            else:
                message.admin_msg_remark = admin_msg_remark
                message.operate_user_id = operate_user_id
            user_id = message.user_id
            # 更新 NextConsoleSessionAdminEvaluateInfo 的点赞计数和点踩计数            
            session_id = message.session_id
            session_ori = NextConsoleSessionAdminEvaluate.query.filter(NextConsoleSessionAdminEvaluate.session_id == session_id).first()
            if not session_id:
                return next_console_response(error_status=True, error_code=1004, error_message="session_id不能为空！")
            # 如果这个session_id 在管理员收藏表中不存在，则插入一条记录
            if not session_ori:
                session = NextConsoleSessionAdminEvaluate(session_id=session_id, user_id=user_id, operate_user_id=operate_user_id)
                db.session.add(session)
                session_ori = NextConsoleSessionAdminEvaluate.query.filter(NextConsoleSessionAdminEvaluate.session_id == session_id).first()
            # 汇总计算点赞和点踩的数量
            query = db.session.query(
                NextConsoleLlmMsgAdminEvaluate.session_id,
                func.sum(case((NextConsoleLlmMsgAdminEvaluate.admin_msg_remark < 0, 1), else_=0)).label('dislike_cnt'),
                func.sum(case((NextConsoleLlmMsgAdminEvaluate.admin_msg_remark > 0, 1), else_=0)).label('like_cnt')
                ).filter(
                    NextConsoleLlmMsgAdminEvaluate.session_id == session_id
                ).group_by(
                    NextConsoleLlmMsgAdminEvaluate.session_id
                ).first()
            if query:
                session_ori.admin_session_dislike_cnt = query[1]
                session_ori.admin_session_like_cnt = query[2]
            else:
                return next_console_response(error_status=True, error_code=1004, error_message="查询原始session会话点赞和点踩数量失败！")
            db.session.commit()
            return next_console_response(result=f"更新msg_remark成功！")
        except Exception as e:
            return next_console_response(error_status=True, error_code=2001, error_message=f"更新msg_remark失败！{e}")


def lookup_admin_msg_like(params):
    """
    查询管理员对于message的点赞和点踩信息
    """
    msg_id = params.get("msg_id")
    if not msg_id:
        return next_console_response(error_status=True, error_code=1004, error_message="msg_id不能为空！")
    else:
        try:
            message = NextConsoleLlmMsgAdminEvaluate.query.filter(NextConsoleLlmMsgAdminEvaluate.msg_id == msg_id).first()
            if message:
                return next_console_response(result={"msg_id":msg_id,"admin_msg_remark":message.admin_msg_remark})
            else:
                return next_console_response(result={"msg_id":msg_id,"admin_msg_remark":0})
        except Exception as e:
            return next_console_response(error_status=True, error_code=2001, error_message="查询admin_msg_remark失败！")


def check_has_role(user_id, role_name):
    """
    检查用户是否有指定角色
    :param user_id:
    :param role_name:
    :return:
    """
    from app.models.user_center.user_role_info import UserRoleInfo
    from app.models.user_center.role_info import RoleInfo
    user_roles = UserRoleInfo.query.filter(UserRoleInfo.user_id == user_id).all()
    all_role_ids = [role.role_id for role in user_roles]
    all_roles = RoleInfo.query.filter(RoleInfo.role_id.in_(all_role_ids)).all()
    user_roles = [role.role_name for role in all_roles]
    if role_name in user_roles:
        return True
    return False