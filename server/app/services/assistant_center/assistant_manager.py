import json
import os
from datetime import datetime, timedelta

from sqlalchemy import desc, Integer, cast
from sqlalchemy import or_, text
from sqlalchemy.exc import IntegrityError

from app.app import db, app
from app.models.assistant_center.assistant import *
from app.models.next_console.next_console_model import NextConsoleMessage
from app.services.configure_center.response_utils import next_console_response


def search_assistants(params):
    """
    搜索助手，返回权限值，返回来源信息，返回统计信息
    """
    user_id = int(params.get("user_id"))
    page_num = params.get('page_num', 1)
    page_size = params.get('page_size', 20)
    order = params.get('order', 'create_time')
    order = 'authority_create_time' if order == 'create_time' else order
    sort = params.get('sort', 'desc')
    assistant_ids = params.get('assistant_ids', [])
    assistant_name = params.get('assistant_name', '')
    assistant_status = params.get('assistant_status', [])
    assistant_desc = params.get('assistant_desc', '')
    assistant_tags = params.get('assistant_tags', '')
    assistant_is_start = params.get('assistant_is_start')
    rel_type = params.get('rel_type')
    all_filters = [UserAssistantRelation.user_id == user_id]
    if rel_type == "服务":
        all_filters.append(UserAssistantRelation.rel_type == rel_type)
    else:
        # 启用状态过滤
        if str(assistant_is_start) == '1':
            all_filters += [
                UserAssistantRelation.rel_type == "权限",
                cast(UserAssistantRelation.rel_value, Integer).in_([7, 5, 1])
            ]
        elif str(assistant_is_start) == '0':
            all_filters += [
                UserAssistantRelation.rel_type == "权限",
                cast(UserAssistantRelation.rel_value, Integer).in_([6, 4, 0])
            ]
        else:
            all_filters += [UserAssistantRelation.rel_type == "权限"]

    if assistant_ids:
        all_filters.append(Assistant.id.in_(assistant_ids))

    if assistant_status:
        all_filters.append(Assistant.assistant_status.in_(assistant_status))

    str_like_filters = []
    if assistant_name:
        str_like_filters.append(Assistant.assistant_name.like(f'%{assistant_name}%'))

    if assistant_desc:
        str_like_filters.append(Assistant.assistant_desc.like(f'%{assistant_desc}%'))

    if assistant_tags:
        assistant_tags_json = json.dumps(assistant_tags)
        condition = text(f"JSON_CONTAINS(assistant_tags, :tag)")
        str_like_filters.append(condition.params(tag=assistant_tags_json))

    all_filters.append(or_(*str_like_filters))
    all_filters.append(or_(
        Assistant.id > 0,
        Assistant.id == -12345,
    ))
    res = Assistant.query.join(
        UserAssistantRelation, UserAssistantRelation.assistant_id == Assistant.id
    ).filter(
        *all_filters,

    ).order_by(desc(UserAssistantRelation.create_time))

    res_cnt = res.count()
    if not res_cnt:
        return next_console_response(result={"cnt": 0, "data": []})
    assistants = res.paginate(page=page_num, per_page=page_size, error_out=False)
    assistants = [assistant.to_dict() for assistant in assistants.items]

    # 补充权限值，补充来源信息,补充统计信息
    assistant_relations = UserAssistantRelation.query.filter(
        UserAssistantRelation.assistant_id.in_([assistant['id'] for assistant in assistants])
    ).all()
    for assistant in assistants:
        for rel in assistant_relations:
            if rel.assistant_id == assistant['id']:
                if rel.rel_type == '创建':
                    assistant['assistant_source'] = 1
                if rel.rel_type == '权限':
                    assistant['authority_value'] = rel.rel_value
                    assistant['authority_create_time'] = rel.create_time.strftime('%Y-%m-%d %H:%M:%S')

    # 补充来源信息
    for assistant in assistants:
        if 'assistant_source' not in assistant:
            assistant['assistant_source'] = 2
        if 'authority_value' not in assistant:
            assistant['authority_value'] = 0
        if assistant['authority_value'] in (7, 5, 1):
            assistant['assistant_is_start'] = True
        else:
            assistant['assistant_is_start'] = False
        if 'authority_create_time' not in assistant:
            assistant['authority_create_time'] = ''
    # 补充统计信息
    if order == 'call_cnt':
        call_counts = AssistantRunInfo.query.filter(
            AssistantRunInfo.assistant_id.in_([assistant['id'] for assistant in assistants]),
            AssistantRunInfo.indicator_name == 'qa_counts'
        ).all()
        call_counts = {call.assistant_id: +call.indicator_value for call in call_counts}
        for assistant in assistants:
            assistant['call_cnt'] = call_counts.get(assistant['id'], 0)
    # 排序
    if sort == 'desc':
        assistants = sorted(assistants, key=lambda x: x[order], reverse=True)
    else:
        assistants = sorted(assistants, key=lambda x: x[order], reverse=False)
    # 剔除不需要的字段
    for assistant in assistants:
        del assistant['assistant_model_name']
        del assistant['assistant_model_temperature']
        del assistant['assistant_memory_size']
        del assistant['assistant_role_prompt']
    response = {"cnt": res_cnt, "data": assistants}
    return next_console_response(result=response)


def add_assistant(params):
    """
    添加助手，增加默认关系
    """
    user_id = int(params.get("user_id"))
    assistant_model_name = params.get('assistant_model_name')
    assistant_role_prompt = params.get('assistant_role_prompt')
    assistant_name = params.get('assistant_name')
    assistant_desc = params.get('assistant_desc', '')
    assistant_tags = params.get('assistant_tags', [])
    assistant_status = params.get('assistant_status', '创建')
    assistant_avatar = params.get('assistant_avatar', '/images/menu_logo.png')
    assistant_language = params.get('assistant_language', '中文')
    assistant_voice = params.get('assistant_voice', '小燕')
    assistant_memory_size = params.get('assistant_memory_size', 4)
    assistant_model_temperature = params.get('assistant_model_temperature', 0.5)
    rag_miss = params.get('rag_miss', 1)
    rag_miss_answer = params.get('rag_miss_answer')
    rag_factor = params.get('rag_factor')
    rag_relevant_threshold = params.get('rag_relevant_threshold')
    new_assistant = Assistant(
        assistant_name=assistant_name,
        assistant_desc=assistant_desc,
        assistant_tags=assistant_tags,
        assistant_status=assistant_status,
        assistant_role_prompt=assistant_role_prompt,
        assistant_avatar=assistant_avatar,
        assistant_language=assistant_language,
        assistant_voice=assistant_voice,
        assistant_memory_size=assistant_memory_size,
        assistant_model_name=assistant_model_name,
        assistant_model_temperature=assistant_model_temperature,
        rag_miss=rag_miss,
        rag_miss_answer=rag_miss_answer,
        rag_factor=rag_factor,
        rag_relevant_threshold=rag_relevant_threshold
    )
    db.session.add(new_assistant)
    try:
        db.session.commit()
        new_rel_create = UserAssistantRelation(
            user_id=user_id,
            assistant_id=new_assistant.id,
            rel_type='创建',
            rel_value=7
        )
        new_rel_authority = UserAssistantRelation(
            user_id=user_id,
            assistant_id=new_assistant.id,
            rel_type='权限',
            rel_value=6
        )
        db.session.add(new_rel_create)
        db.session.add(new_rel_authority)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return next_console_response(error_status=True, error_code=500, error_message=str(e))
    result = new_assistant.to_dict()
    return next_console_response(result=result)


def delete_assistant(params):
    """
    删除助手,通过创建关系找到对应的助手，进行删除
    """
    user_id = int(params.get("user_id"))
    assistant_ids = params.get('assistant_ids')
    # 找到对应的助手

    del_relations = UserAssistantRelation.query.filter(
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.assistant_id.in_(assistant_ids),
        UserAssistantRelation.rel_type == '创建'
    ).all()
    result = []
    for rel in del_relations:
        target_assistant = Assistant.query.filter(
            Assistant.id == rel.assistant_id
        ).first()
        if not target_assistant:
            continue
        result.append(target_assistant.to_dict())
        db.session.delete(target_assistant)
        db.session.commit()

    return next_console_response(result=result)


def update_assistant(params):
    """
    更新助手
    """
    assistant_id = params.get('id')
    user_id = int(params.get("user_id"))
    del params['id']
    del params['user_id']
    user_assistant_rel = UserAssistantRelation.query.filter(
        UserAssistantRelation.assistant_id == assistant_id,
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.rel_type == '权限',
    ).first()
    if not user_assistant_rel:
        return next_console_response(error_status=True, error_code=404, error_message='助手不存在')
    target_assistant = Assistant.query.filter(
        Assistant.id == user_assistant_rel.assistant_id
    ).first()
    if not target_assistant:
        return next_console_response(error_status=True, error_code=404, error_message='助手不存在')

    operate_type = params.get("operate_type")
    if operate_type:
        target_assistant = target_assistant.to_dict()
        if operate_type == "stop":
            trans_stop_map = {
                7: 6,
                5: 4,
                1: 0
            }
            user_assistant_rel.rel_value = trans_stop_map.get(user_assistant_rel.rel_value,
                                                              user_assistant_rel.rel_value)
            db.session.add(user_assistant_rel)
            db.session.commit()
            target_assistant["authority_value"] = user_assistant_rel.rel_value
            target_assistant["assistant_is_start"] = False
        elif operate_type == "start":
            trans_start_map = {
                6: 7,
                4: 5,
                0: 1
            }
            user_assistant_rel.rel_value = trans_start_map.get(user_assistant_rel.rel_value,
                                                               user_assistant_rel.rel_value)
            db.session.add(user_assistant_rel)
            db.session.commit()
            target_assistant["authority_value"] = user_assistant_rel.rel_value
            target_assistant["assistant_is_start"] = True
        return next_console_response(result=target_assistant)
    else:
        if user_assistant_rel.rel_value not in (6, 7):
            return next_console_response(error_status=True, error_code=403, error_message='权限不足')

        for key, value in params.items():
            setattr(target_assistant, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return next_console_response(error_status=True, error_code=500, error_message=str(e))
        # 更新知识库关系
        assistant_knowledge_base = params.get('assistant_knowledge_base', [])
        kg_relations = AssistantKgRelation.query.filter(
            AssistantKgRelation.assistant_id == assistant_id,
            AssistantKgRelation.rel_status == '正常'
        ).all()
        old_kg_codes = [kg.kg_code for kg in kg_relations]
        new_kg_codes = [kg["kg_code"] for kg in assistant_knowledge_base]
        # 删除多余的关系
        for kg in kg_relations:
            if kg.kg_code not in new_kg_codes:
                db.session.delete(kg)
    return next_console_response(result=target_assistant.to_dict())


def get_assistant(params):
    """
    获取助手详细信息，必须有可读权限
    """
    assistant_id = params.get('assistant_id')
    assistant_id_list = params.get('assistant_id_list')
    caller = params.get('caller')
    if caller == "next_console_add_message":
        target_assistant = Assistant.query.filter(
            Assistant.id == params.get("id"),
        ).first()
        if not target_assistant:
            return next_console_response(error_status=True, error_code=404, error_message='助手不存在')
        return next_console_response(result=target_assistant.to_dict())
    filter_condition = []
    if assistant_id is not None:
        filter_condition.append(Assistant.id == assistant_id)
    if assistant_id_list is not None:
        try:
            assistant_id_list = [int(assistant_id) for assistant_id in assistant_id_list]
            filter_condition.append(Assistant.id.in_(assistant_id_list))
        except ValueError as e:
            return next_console_response(error_status=True, error_code=400, error_message='参数错误')
    target_assistant = Assistant.query.filter(
        *filter_condition
    ).all()
    if not target_assistant:
        return next_console_response(error_status=True, error_code=404, error_message='助手不存在')
    res = []
    for assistant in target_assistant:
        res.append(assistant.show_info())
    return next_console_response(result=res)


def change_assistant(user_id, assistant_id, assistant_source):
    """
    更换助手
    """
    # 删除原有关系
    old_rel = UserAssistantRelation.query.filter(
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.rel_type == '服务'
    ).first()
    if old_rel:
        db.session.delete(old_rel)
    # 增加新关系
    if not assistant_source or assistant_source in (1, 2):
        new_rel = UserAssistantRelation(
            user_id=user_id,
            assistant_id=assistant_id,
            rel_type='服务'
        )
        db.session.add(new_rel)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return next_console_response(error_status=True, error_message="该助手已在服务中！")
        target_assistant = Assistant.query.filter(
            Assistant.id == assistant_id
        ).first()
        return next_console_response(result=target_assistant.to_dict())
    else:
        return next_console_response(error_status=True, error_code=400, error_message='参数错误')


def upload_avatar(assistant_id, assistant_author_id, avatar, avatar_name):
    """
    上传助手头像:
        保存头像至指定目录
        更新助手头像字段
    """
    avatar_filename = '{}_{}_{}'.format(
        assistant_author_id,
        assistant_id,
        avatar_name)
    avatar_path = os.path.join(app.config['images_dir'], avatar_filename)
    avatar.save(avatar_path)
    params = {
        'id': assistant_id,
        'user_id': assistant_author_id,
        'assistant_avatar': "/images/{}".format(avatar_filename)
    }
    return update_assistant(params)


def add_user_assistant_rel(user_id, assistant_id, rel_type, rel_value):
    """
    添加用户助手关系
    """
    new_rel = UserAssistantRelation(
        user_id=user_id,
        assistant_id=assistant_id,
        rel_type=rel_type,
        rel_value=rel_value
    )
    db.session.add(new_rel)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return next_console_response(error_status=True, error_code=400, error_message="该关系已存在")
    return next_console_response(result=new_rel.to_dict())


def get_user_assistant_rel(user_id, assistant_id):
    """
        获取用户助手关系
        """
    rels = UserAssistantRelation.query.filter(
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.assistant_id == assistant_id,
        UserAssistantRelation.rel_status == '正常'
    ).all()
    if not rels:
        return next_console_response(result={})
    return next_console_response(result=[rel.to_dict() for rel in rels])


def update_user_assistant_rel(user_id, assistant_id, rel_type):
    """
    更新用户助手关系
    """
    rel = UserAssistantRelation.query.filter(
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.rel_type == rel_type,
        UserAssistantRelation.rel_status == '正常'
    ).first()
    if not rel:
        new_relation = UserAssistantRelation(
            user_id=user_id,
            assistant_id=assistant_id,
            rel_type=rel_type
        )
        db.session.add(new_relation)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return next_console_response(error_status=True, error_code=500, error_message=str(e))
        return next_console_response(result=new_relation.to_dict())
    rel.assistant_id = assistant_id
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return next_console_response(error_status=True, error_code=500, error_message=str(e))
    return next_console_response(result=rel.to_dict())


def del_user_assistant_rel(user_id, assistant_id, rel_type):
    """
    删除用户助手关系
    """
    rel = UserAssistantRelation.query.filter(
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.assistant_id == assistant_id,
        UserAssistantRelation.rel_type == rel_type
    ).first()
    if not rel:
        return next_console_response(result={})
    db.session.delete(rel)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return next_console_response(error_status=True, error_code=500, error_message=str(e))
    return next_console_response(result=rel.to_dict())


def get_assistant_metric(params):
    """
    获取助手运行指标
    """
    user_id = int(params.get("user_id"))
    assistant_id = params.get('assistant_id')
    create_rels = UserAssistantRelation.query.filter(
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.assistant_id == assistant_id,
        UserAssistantRelation.rel_type == '创建',
        UserAssistantRelation.rel_status == '正常'
    ).all()
    if not create_rels:
        return next_console_response(error_status=True, error_code=404, error_message='助手不存在')
    metric_name = params.get('metric_name')
    end_time = params.get('end_time', datetime.now())
    start_time = params.get('start_time', end_time - timedelta(days=7))
    interval = params.get('interval', 30)
    if metric_name in ("qa_counts", "cost"):
        return get_assistant_metric_time_series(
            assistant_id, start_time, end_time, interval, metric_name, "sum", "sum"
        )
    elif metric_name in ("user_counts", "avg_time", "token_speed"):
        return get_assistant_metric_time_series(
            assistant_id, start_time, end_time, interval, metric_name, "avg", "reset"
        )
    elif metric_name == "like_rate":
        data = db.session.query(
            NextConsoleMessage.msg_remark,
            func.count(NextConsoleMessage.msg_id).label('msg_count')
        ).filter(
            NextConsoleMessage.assistant_id == assistant_id,
            NextConsoleMessage.msg_del == 0,
            NextConsoleMessage.create_time >= start_time,
            NextConsoleMessage.create_time <= end_time
        ).group_by(
            NextConsoleMessage.msg_remark
        ).all()
        result = []
        name_dict = {
            1: "用户点赞",
            -1: "用户点踩",
            0: "用户未评论",

        }
        for item in data:
            result.append({
                'name': name_dict.get(item.msg_remark, "未知"),
                'value': item.msg_count
            })
        return next_console_response(result=result)

    return next_console_response(error_status=True, error_code=400, error_message='参数错误')


def get_assistant_metric_time_series(assistant_id, start_time, end_time, interval, metric_name, feature_way, accum_way):
    """
        获取助手用户指标
        """
    res = AssistantRunInfo.query.filter(
        AssistantRunInfo.assistant_id == assistant_id,
        AssistantRunInfo.indicator_name == metric_name,
        AssistantRunInfo.create_time >= start_time,
        AssistantRunInfo.create_time <= end_time
    ).all()

    result = []
    cursor_time = start_time + timedelta(minutes=interval)
    cursor_metric_index = 0
    region_sum = 0
    region_cnt = 0
    while cursor_time <= end_time:
        if cursor_metric_index >= len(res) or res[cursor_metric_index].create_time > cursor_time:
            if region_cnt:
                if feature_way == "avg":
                    feature_value = round(region_sum / region_cnt, 3)
                elif feature_way == "sum":
                    feature_value = region_sum
                else:
                    feature_value = 0

                if accum_way == "reset":
                    new_value = feature_value
                elif accum_way == "sum":
                    if not result:
                        new_value = feature_value
                    else:
                        new_value = feature_value + result[-1]["value"][1]
                else:
                    new_value = 0
                result.append({
                    'value': [int(cursor_time.timestamp()) * 1000,
                              new_value]
                })
                region_cnt = 0
                region_sum = 0
            else:
                if accum_way == "reset":
                    result.append({
                        'value': [int(cursor_time.timestamp()) * 1000, 0]
                    })
                elif accum_way == "sum":
                    if not result:
                        result.append({
                            'value': [int(cursor_time.timestamp()) * 1000, 0]
                        })
                    else:
                        result.append({
                            'value': [int(cursor_time.timestamp()) * 1000, result[-1]["value"][1]]
                        })
            cursor_time += timedelta(minutes=interval)
            continue
        region_sum += res[cursor_metric_index].indicator_value
        region_cnt += 1
        cursor_metric_index += 1
    return next_console_response(result=result)
