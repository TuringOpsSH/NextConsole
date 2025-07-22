from app.services.next_console.base import *
from app.app import app


def retrieve_messages_to_prompt(session_id, user_id, qa_id, k):
    """
    通过消息列表生成提示
        策略1：取最后k个问答对中question和排序最高的answer
            每个qa，选取排序最高的question，再选取排序最高的answer，如果没有合法的，就继续往下，直到找到合法的
            补充策略： 当一个问答对处于重试状态时，需要补充一个错误问答，即存在msg_parent_id
            重试问题：同一问题的上一个答案
            重新编辑问题：上一个版本的问题的最后一个答案
    """
    current_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == session_id,
        NextConsoleSession.user_id == user_id,
    ).first()
    if not current_session:
        return []
    all_qa = NextConsoleQa.query.filter(
        NextConsoleQa.session_id == session_id,
        NextConsoleQa.user_id == user_id,
        NextConsoleQa.qa_id <= qa_id,
        NextConsoleQa.qa_del == False,
    ).order_by(
        desc(NextConsoleQa.qa_id)
    ).limit(
        k
    ).all()
    # 增加清除状态的判断
    all_qa_id = []
    for qa in all_qa:
        if qa.qa_status != "清除":
            all_qa_id.append(qa.qa_id)
        else:
            break
    all_qa_id.reverse()
    all_msgs = NextConsoleMessage.query.filter(
        NextConsoleMessage.session_id == session_id,
        NextConsoleMessage.user_id == user_id,
        NextConsoleMessage.qa_id.in_(all_qa_id),
        NextConsoleMessage.msg_del == 0
    ).order_by(
        desc(NextConsoleMessage.session_id),
        desc(NextConsoleMessage.qa_id),
        asc(NextConsoleMessage.msg_role),
        asc(NextConsoleMessage.msg_version),
        asc(NextConsoleMessage.msg_remark)
    ).all()
    all_msgs = [msg_item.to_dict() for msg_item in all_msgs]
    all_msgs.reverse()
    messages = []
    retrieve_messages = {}
    for i in all_msgs:
        if i["qa_id"] not in retrieve_messages:  # 新的qa
            retrieve_messages[i["qa_id"]] = {
                "question": {},
                "answer": {}
            }
        if i["msg_role"] == "user" and retrieve_messages[i["qa_id"]]["question"] == {}:
            retrieve_messages[i["qa_id"]]["question"] = i
        elif i["msg_role"] == "assistant" and retrieve_messages[i["qa_id"]]["answer"] == {}:
            if retrieve_messages[i["qa_id"]]["question"] != {}:
                if i["msg_parent_id"] == retrieve_messages[i["qa_id"]]["question"]["msg_id"]:
                    retrieve_messages[i["qa_id"]]["answer"] = i
    for qa_id in all_qa_id:
        if qa_id in retrieve_messages:
            if retrieve_messages[qa_id]["question"] != {} and retrieve_messages[qa_id]["answer"] != {}:
                msg_inner_content = retrieve_messages[qa_id]["question"].get("msg_inner_content")
                if msg_inner_content:
                    # 任务拆解的内容
                    if isinstance(msg_inner_content, list):
                        question_combin = ",".join([item.get("content") for item in msg_inner_content])
                        messages.append(
                            {"role": "user", "content": question_combin}
                        )
                    else:
                        messages.append(
                            {"role": "user", "content": retrieve_messages[qa_id]["question"].get("msg_content")}
                        )
                else:
                    # 异常问题
                    messages.append(
                        {"role": "user", "content": retrieve_messages[qa_id]["question"].get("msg_content")}
                    )
                messages.append(
                    {"role": "assistant", "content": retrieve_messages[qa_id]["answer"]["msg_content"]}
                )

    return messages


def retrieve_qa_pre_k(session_id, qa_id, msg_id, k=2):
    """
    获取前k个qa
     前置问题定位逻辑：
            1. 查找同一个qa_id下的上一个的用户问题
            2. 查找同一个session_id下的上一个qa_id 的用户问题
    """
    # 查找之前的回答
    target_pre_msg = NextConsoleMessage.query.filter(
        NextConsoleMessage.session_id == session_id,
        NextConsoleMessage.qa_id <= qa_id,
        NextConsoleMessage.msg_id < msg_id,
        NextConsoleMessage.msg_del == 0,
        NextConsoleMessage.msg_role == "assistant",
        NextConsoleMessage.msg_format.in_(['text', 'messageFlow'])
    ).order_by(
        desc(NextConsoleMessage.qa_id),
        desc(NextConsoleMessage.msg_id)
    ).limit(
        k
    )
    if not target_pre_msg:
        return []
    # 查找对应的问题
    all_question_ids = [msg.msg_parent_id for msg in target_pre_msg if msg.msg_parent_id]
    all_questions = NextConsoleMessage.query.filter(
        NextConsoleMessage.msg_id.in_(all_question_ids),
        NextConsoleMessage.msg_role == "user",
        NextConsoleMessage.msg_del == 0,
    ).all()
    all_questions_dict = {msg.msg_id: msg for msg in all_questions}
    result = []

    for msg in target_pre_msg:
        question = all_questions_dict.get(msg.msg_parent_id)
        if not question:
            continue
        result.insert(0, all_questions_dict.get(msg.msg_parent_id))
        result.insert(1, msg)

    return result


def retrieve_instruction_context(target_msg, history_length):
    if not target_msg:
        return ""
    msg_id = target_msg.msg_id
    qa_id = target_msg.qa_id
    session_id = target_msg.session_id
    history_list = retrieve_qa_pre_k(session_id, qa_id, msg_id, history_length)
    history = []
    for sub_msg in history_list:
        if sub_msg.msg_role == "user":
            history.append({"role": "user", "content": sub_msg.msg_content})
        else:
            history.append({"role": "assistant", "content": sub_msg.msg_content})
    return history
