from app.models.next_console.next_console_model import NextConsoleSession
from app.models.assistant_center.assistant import AssistantInstruction
from app.app import celery, redis_client, socketio, app, db
import json


@celery.task
def emit_workflow_status(params):
    """
    推送工作流状态
    :return:
    """
    user_id = int(params.get("user_id"))
    new_task = params.get("new_task")
    all_user_clients = redis_client.get(user_id)
    if not all_user_clients:
        # print(f"all_user_clients is None: {user_id}")
        return
    all_user_clients = json.loads(all_user_clients)
    for client in all_user_clients:
        # print(f"client: {client}")
        if client.get('status') == 'connected':
            data = {
                "session_id": new_task.get("session_id"),
                "qa_id": new_task.get("qa_id"),
                "msg_id": new_task.get("msg_id"),
                "task_id": new_task.get("id"),
                "task_type": new_task.get("task_type"),
                "task_instruction": new_task.get("task_assistant_instruction"),
                "task_params": new_task.get("task_params"),
                "task_status": new_task.get("task_status"),
            }
            if new_task.get("task_type") in ("会话命名", "查询推荐"):
                data["task_result"] = new_task.get("task_result")
            # app.logger.warning(f"{new_task}:{data}", )
            socketio.emit("update_workflow_item_status", data, room=client.get('session_id'))


@celery.task
def auto_naming_session(params):
    """
    自动命名会话
        在会话第三个问题发生时，调用助手指令，自动命名会话
    :param params:
    :return:
    """
    with app.app_context():
        from app.services.assistant_center.assistant_instruction import run_assistant_instruction
        user_id = int(params.get("user_id"))
        session_id = params.get("session_id")
        assistant_id = params.get("assistant_id")
        msg_parent_id = params.get("msg_parent_id")
        question_content = params.get("question_content")
        SessionNaming_instruction = AssistantInstruction.query.filter(
            AssistantInstruction.assistant_id == assistant_id,
            AssistantInstruction.instruction_name == "SessionNaming"
        ).first()
        ture_session_topic = run_assistant_instruction(
            {
                "instruction_id": SessionNaming_instruction.id,
                "user_id": user_id,
                "msg_id": msg_parent_id,
                "user_params": json.dumps({
                    "message_text": question_content
                })
            }
        ).json.get("result")
        # 更新会话结果
        if ture_session_topic:
            current_session = NextConsoleSession.query.filter(
                NextConsoleSession.id == session_id
            ).first()
            current_session.session_topic = ture_session_topic
            db.session.add(current_session)
            db.session.commit()


@celery.task
def create_recommend_question(params):
    """
    创建推荐问题
    """
    with app.app_context():
        from app.services.assistant_center.assistant_instruction import run_assistant_instruction
        from app.models.next_console.next_console_model import NextConsoleRecommendQuestion
        msg_id = params.get("msg_id")
        msg_content = params.get("msg_content")
        user_id = int(params.get("user_id"))
        assistant_id = params.get("assistant_id", -12345)
        # 获取关键助手指令
        instruction = AssistantInstruction.query.filter(
            AssistantInstruction.assistant_id == assistant_id,
            AssistantInstruction.instruction_name == "QuerySuggest",
            AssistantInstruction.instruction_status == "正常"
        ).first()
        answer = run_assistant_instruction({
                    "instruction_id": instruction.id,
                    "user_id": user_id,
                    "msg_id": msg_id,
                }).json.get("result")
        if not answer:
            return []
        else:
            res = []
            # 保存推荐问题用于后续点击更新并分析用户行为
            if len(answer) == 1:
                # ,默认中文分割，如果解析异常则更换为英文逗号解析
                answer = answer[0].split(",")
            for question in answer:
                if question == "" or question == "null":
                    continue
                new_question = NextConsoleRecommendQuestion(
                    msg_id=msg_id,
                    msg_content=msg_content,
                    recommend_question=question,
                    model="deepseek-chat"
                )
                db.session.add(new_question)
                res.append(new_question)
            db.session.commit()
            res = [question.show_info() for question in res]
            all_user_clients = redis_client.get(user_id)
            if not all_user_clients:
                return
            all_user_clients = json.loads(all_user_clients)
            for client in all_user_clients:
                if client.get('status') == 'connected':
                    socketio.emit("update_recommend_questions", res, room=client.get('session_id'))
            return res
