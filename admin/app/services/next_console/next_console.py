from app.services.next_console.rag import *


def next_console_search_messages(params):
    """
        根据qa_id查询消息
        返回消息列表格式为
        [
            {
                "qa_id": "35",
                "qa_status": "清除",
                "qa_value"{
                    "question": [{},{},{}],
                    "answer":
                        {
                            "msg_id": [{},{}],
                        },
                    }
            }
        ]
    """
    # 先按照时间顺序捞取k个role为user的问题,并按照创建时间顺序排序
    new_params = {
        "user_id": int(params.get("user_id")),
        'qa_id': params.get('qa_id'),
        "fetch_all": True,

    }
    if params.get("order"):
        new_params["order"] = params.get("order")
    all_qas = search_qa(new_params).json["result"]
    all_qas = {qa["qa_id"]: qa for qa in all_qas}
    all_msgs = search_messages(new_params, in_call=True)
    res_msgs = []
    # 组装
    current_qa_id = ''
    all_session_ids = set()

    for msg in all_msgs:
        # 剔除内部数据
        all_session_ids.add(msg["session_id"])
        if (msg["assistant_id"] and msg["assistant_id"] < 0
                and msg["assistant_id"] not in (-12345, -12345)
                and not params.get("inner_call")):
            continue
        if msg["qa_id"] != current_qa_id:
            current_qa_id = msg["qa_id"]
            if current_qa_id not in all_qas:
                continue
            res_msgs.append({
                "qa_id": current_qa_id,
                "qa_status": all_qas[current_qa_id]["qa_status"],  # "清除
                "qa_topic": all_qas[current_qa_id]["qa_topic"],
                "qa_value": {
                    "question": [],
                    "answer": {},
                }
            })
        if msg["msg_role"] == "user":
            res_msgs[-1]["qa_value"]["question"].append(msg)
        else:
            if msg["msg_parent_id"] not in res_msgs[-1]["qa_value"]["answer"]:
                res_msgs[-1]["qa_value"]["answer"][msg["msg_parent_id"]] = []
            res_msgs[-1]["qa_value"]["answer"][msg["msg_parent_id"]].insert(0, msg)

    all_session_ids = list(all_session_ids)
    all_attachments = SessionAttachmentRelation.query.filter(
        SessionAttachmentRelation.session_id.in_(all_session_ids),
        SessionAttachmentRelation.rel_status == "正常"
    ).join(
        ResourceObjectMeta,
        ResourceObjectMeta.id == SessionAttachmentRelation.resource_id
    ).with_entities(
        SessionAttachmentRelation.msg_id,
        ResourceObjectMeta
    ).all()
    attachment_dict = {}
    for msg_id, attachment in all_attachments:
        if msg_id not in attachment_dict:
            attachment_dict[msg_id] = []
        item = attachment.to_dict()
        item["resource_url"] = attachment.resource_download_url
        attachment_dict[msg_id].append(item)

    # 剔除无关字段
    for qa in res_msgs:
        for question in qa["qa_value"]["question"]:
            question["attachment_list"] = attachment_dict.get(question["msg_id"], [])
            question.pop("msg_prompt")
            question.pop("msg_inner_content")
            question.pop("msg_llm_type")
            question.pop("assistant_id")

        for answer in qa["qa_value"]["answer"]:
            for msg in qa["qa_value"]["answer"][answer]:
                msg.pop("msg_prompt")
                msg.pop("msg_inner_content")
                msg.pop("msg_llm_type")
    # 剔除无效数据：
    new_res_msgs = []
    for msg_item in res_msgs:
        # 删除了问题，但是答案还在
        if not msg_item["qa_value"]["question"]:
            continue
        # 删除了答案，但是问题还在
        valid_questions = []
        for question in msg_item["qa_value"]["question"]:
            if question["msg_id"] in msg_item["qa_value"]["answer"]:
                valid_questions.append(question)
        msg_item["qa_value"]["question"] = valid_questions
        if not valid_questions:
            continue
        new_res_msgs.append(msg_item)
    # 增加附件搜索
    return next_console_response(result=new_res_msgs)
