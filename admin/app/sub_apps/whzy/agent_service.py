import json
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy import text

from app.app import socketio, redis_client
from app.models.app_center.app_info_model import AppMetaInfo, WorkFlowTaskInfo
from app.models.next_console.next_console_model import *
from app.services.next_console.base import *
from app.models.configure_center.llm_kernel import LLMInstance
from app.services.assistant_center.assistant_instruction import run_assistant_instruction
from app.services.assistant_center.assistant_manager import get_assistant
from app.services.next_console.attachment import extract_attachment_images_to_question
from app.services.next_console.memory import retrieve_messages_to_prompt
from app.services.next_console.llm import llm_chat
from app.services.next_console.workflow import *
from app.services.task_center.workflow import async_generate_chart_options
from app.services.task_center.workflow import auto_naming_session, create_recommend_question
from app.utils.iat.iat_ws_client import XFWsClient

_global_user_audio = {}


def agent_add_message(params):
    # 会话参数
    user_id = int(params.get("user_id"))
    session_id = params.get("session_id")
    qa_id = params.get("qa_id")
    msg_version = params.get("msg_version", 0)
    msg_parent_id = params.get("msg_parent_id", None)
    question_content = params.get("msg_content", "")
    answer_flag = params.get("msg_answer_flag", True)
    stream = params.get("stream", True)
    response_format = params.get("response_format", "text")
    session_attach_data = params.get("session_attach_data", None)
    # 助手参数
    assistant = NextConsoleSession.query.filter(
        NextConsoleSession.user_id == user_id,
        NextConsoleSession.id == session_id
    ).join(
        AppMetaInfo,
        AppMetaInfo.app_code == NextConsoleSession.session_source
    ).join(
        Assistant,
        Assistant.id == AppMetaInfo.app_default_assistant
    ).with_entities(
        Assistant
    ).first()

    if assistant:
        assistant = assistant.to_dict()
    else:
        assistant = get_assistant({
            "id": -12345,
            "user_id": user_id,
            "caller": "next_console_add_message"
        }).json.get("result")
    assistant_memory_size = assistant["assistant_memory_size"]

    system_messages = {"role": "system", "content": assistant["assistant_role_prompt"]}
    temperature = assistant.get("assistant_temperature", 0.7)
    msg_inner_content_obj = {"role": "user", "content": question_content}
    answer_type = 0
    rag_flag = False

    current_session = NextConsoleSession.query.filter(
        NextConsoleSession.user_id == user_id,
        NextConsoleSession.id == session_id
    ).first()
    target_model_code = assistant["assistant_model_code"]
    if current_session.session_llm_code != target_model_code:
        target_model_code = current_session.session_llm_code
    msg_llm_type = LLMInstance.query.filter(
        LLMInstance.llm_code == target_model_code
    ).first()
    if (current_session.session_search_engine_switch or current_session.session_local_resource_switch
            or current_session.session_attachment_file_switch or current_session.session_attachment_webpage_switch
            or current_session.session_local_resource_use_all
    ):
        rag_flag = True
    if not msg_llm_type:
        params["msg_llm_type"] = "unknown"
    else:
        params["msg_llm_type"] = msg_llm_type.llm_name
    # 直接回答问题
    if answer_flag:
        # 保存用户问题
        if msg_parent_id is None:
            params["msg_inner_content"] = msg_inner_content_obj
            add_result = add_messages(params, inner_call=True)
            msg_parent_id = add_result.get("msg_id")
        IntentionUnderstand = AssistantInstruction.query.filter(
            AssistantInstruction.assistant_id == assistant["id"],
            AssistantInstruction.instruction_name == "IntentionUnderstand",
            AssistantInstruction.instruction_status == "正常",
        ).first()
        if IntentionUnderstand:
            true_intent = run_assistant_instruction(
                {
                    "instruction_id": IntentionUnderstand.id,
                    "user_id": user_id,
                    "msg_id": msg_parent_id,
                    "system_params": json.dumps(
                        {
                            'graph': session_attach_data,
                        }
                    ),
                    "user_params": json.dumps({
                        "message_text": question_content
                    })
                }
            ).json.get("result")
            try:
                true_intent = int(true_intent.strip())
                if true_intent == 1:
                    # 将图表信息新增至system prompt中
                    system_messages["content"] += f"客户当前查看问询的图表信息：{session_attach_data}"
                    rag_flag = True
                elif true_intent == 2:
                    GraphChange = AssistantInstruction.query.filter(
                        AssistantInstruction.assistant_id == assistant["id"],
                        AssistantInstruction.instruction_name == "GraphChange",
                        AssistantInstruction.instruction_status == "正常",
                    ).first()
                    if GraphChange:
                        change_params = run_assistant_instruction(
                            {
                                "instruction_id": GraphChange.id,
                                "user_id": user_id,
                                "msg_id": msg_parent_id,
                                "system_params": json.dumps(
                                    {
                                        'graph': session_attach_data,
                                        'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "current_weekday":  ['星期一', '星期二', '星期三',
                                                             '星期四', '星期五', '星期六', '星期日'][
                                            datetime.now().weekday()],
                                    }
                                ),
                                "user_params": json.dumps({
                                    "message_text": question_content
                                })
                            }
                        ).json
                        change_params = change_params.get("result")
                        spec_value = change_params.get("spec")
                        if change_params and (
                                not spec_value
                                or (spec_value and json.dumps(spec_value) in json.dumps(session_attach_data))):
                            # 新增规则： 规格字段的值必须在列表中
                            all_user_clients = redis_client.get(user_id)
                            if not all_user_clients:
                                return
                            all_user_clients = json.loads(all_user_clients)
                            for client in all_user_clients:
                                if client.get('status') == 'connected':
                                    socketio.emit('update_bi_graph', {
                                        "params": change_params
                                    }, room=client.get('session_id'))
                            rag_flag = False
                            msg_inner_content_obj['content'] += "\n 请直接回复：“好的，请关注左侧界面，已经为您更新图表”"
                            update_question_params = {
                                "user_id": user_id,
                                "session_id": session_id,
                                "qa_id": qa_id,
                                "msg_id": msg_parent_id,
                                "msg_inner_content": msg_inner_content_obj
                            }
                            update_messages(update_question_params)
                            messages = [system_messages, msg_inner_content_obj]
                            chat_params = {
                                "user_id": user_id,
                                "session_id": session_id,
                                "session_llm_code": target_model_code,
                                "qa_id": qa_id,
                                "msg_parent_id": msg_parent_id,
                                "assistant_id": assistant["id"],
                                "model": msg_llm_type,
                                "messages": messages,
                                "stream": stream,
                                "response_format": response_format,
                                "msg_version": msg_version,
                                "temperature": temperature,
                                "rag_flag": rag_flag,
                            }
                            return llm_chat(chat_params)
                elif true_intent == 3:
                    # 生成sql并执行
                    data_obj = generate_sql_to_data({
                        "user_id": user_id,
                        "session_id": session_id,
                        "msg_parent_id": msg_parent_id,
                        "msg_content": question_content,
                        "assistant_id": assistant["id"]
                    })
                    msg_inner_content_obj["content"] += f"\n 系统通过函数调用，获取到的精确结果数据： {data_obj}"
                    question_content += f"\n 系统通过函数调用，获取到的精确结果数据： {data_obj}"
                    # 提交异步任务进行图表配置生成
                    ChartVisualization_instruction = AssistantInstruction.query.filter(
                        AssistantInstruction.assistant_id == assistant["id"],
                        AssistantInstruction.instruction_name == "ChartVisualization",
                        AssistantInstruction.instruction_status == "正常",
                    ).first()
                    if ChartVisualization_instruction:
                        async_generate_chart_options.delay({
                                "instruction_id": ChartVisualization_instruction.id,
                                "user_id": user_id,
                                "msg_id": msg_parent_id,
                                "system_params": json.dumps(
                                    {
                                    }
                                ),
                                "user_params": json.dumps({
                                    "message_text": question_content,
                                    "data": data_obj
                                })
                            })
                elif true_intent == 4:
                    # 继续问答
                    rag_flag = True
                else:
                    rag_flag = True
            except Exception as e:
                pass
        # workflow - 创建推荐问题
        create_recommend_question.delay({
            "user_id": user_id,
            "assistant_id": assistant["id"],
            "msg_id": msg_parent_id,
            "msg_content": question_content
        })
        # workflow - 检索参考资料
        if rag_flag:
            # 新增问题理解
            QueryUnderstand_instruction = AssistantInstruction.query.filter(
                AssistantInstruction.assistant_id == assistant["id"],
                AssistantInstruction.instruction_name == "QueryUnderstand",
                AssistantInstruction.instruction_status == "正常",
            ).first()
            if QueryUnderstand_instruction:
                true_question = run_assistant_instruction(
                    {
                        "instruction_id": QueryUnderstand_instruction.id,
                        "user_id": user_id,
                        "msg_id": msg_parent_id,
                        "user_params": json.dumps({
                            "message_text": question_content
                        })
                    }
                ).json.get("result")
                if true_question and true_question[1]:
                    question_content = true_question[1]
            # 资源检索
            rag_instruction = AssistantInstruction.query.filter(
                AssistantInstruction.assistant_id == assistant["id"],
                AssistantInstruction.instruction_type == "rag",
                AssistantInstruction.instruction_status == "正常",
            ).first()
            if rag_instruction:
                true_question = run_assistant_instruction(
                    {
                        "instruction_id": rag_instruction.id,
                        "user_id": user_id,
                        "msg_id": msg_parent_id,
                        "user_params": json.dumps({
                            "query_text": question_content
                        }),
                    }
                ).json.get("result")
                if true_question:
                    msg_inner_content_obj = {"role": "user", "content": true_question}
        # 处理图片
        if current_session.session_attachment_image_switch:
            # 用户上传了图片
            attachment_images_questions = extract_attachment_images_to_question({
                "user_id": user_id,
                "session_id": session_id,
                "qa_id": qa_id,
                "msg_id": msg_parent_id,
                "assistant_id": assistant["id"],
                "model_name": msg_llm_type.llm_name,
            }).json.get("result")
            if attachment_images_questions:
                msg_inner_content_obj = {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": msg_inner_content_obj.get("content")
                        }]
                }
                msg_inner_content_obj["content"].extend(attachment_images_questions)
        # workflow - 召回记忆
        memory_messages = retrieve_messages_to_prompt(session_id, user_id, qa_id, assistant_memory_size)
        # workflow - 自动命名会话
        if len(memory_messages) >= 4 and current_session.session_topic == "未命名会话":
            auto_naming_session.delay({
                "user_id": user_id,
                "session_id": session_id,
                "assistant_id": assistant["id"],
                "msg_parent_id": msg_parent_id,
                "question_content": question_content
            })
        # workflow - 更新提问记录
        update_question_params = {
            "user_id": user_id,
            "session_id": session_id,
            "qa_id": qa_id,
            "msg_id": msg_parent_id,
            "msg_inner_content": msg_inner_content_obj
        }
        update_messages(update_question_params)
        # workflow - 组装消息队列
        messages = memory_messages
        messages.insert(0, system_messages)
        messages.append(msg_inner_content_obj)
        chat_params = {
            "user_id": user_id,
            "session_id": session_id,
            "session_llm_code": target_model_code,
            "qa_id": qa_id,
            "msg_parent_id": msg_parent_id,
            "assistant_id": assistant["id"],
            "model": msg_llm_type,
            "messages": messages,
            "stream": stream,
            "response_format": response_format,
            "msg_version": msg_version,
            "temperature": temperature,
            "rag_flag": rag_flag,
        }
        # workflow - 调用大模型驱动回答问题
        # 如果是分解问题，则并发获取rag，顺序调用llmchat
        return llm_chat(chat_params)
    # 优先仅保存消息
    else:
        return add_messages(params)


def handle_audio_message(message):
    """
        处理音频消息 ，并调用讯飞语音识别接口
    """
    user_id = message.get("user_id")
    data = message.get("data")
    LastFrame = message.get("LastFrame", False)
    if user_id not in _global_user_audio or not _global_user_audio[user_id].get("ws_client"):
        ws_client = XFWsClient(user_id)
        ws_client.init()
        _global_user_audio[user_id] = {
            "audio_data": [],
            "ws_client": ws_client
        }
    _global_user_audio[user_id]["audio_data"].append(
        {
            "data": data,
            "status": 0
        }
    )
    # 尝试发送音频数据
    if _global_user_audio[user_id]["ws_client"].ws.sock and _global_user_audio[user_id]["ws_client"].ws.sock.connected:
        # 合并所有未发送的音频数据
        audio_data = b"".join([audio.get("data") for audio in _global_user_audio[user_id]["audio_data"]
                               if audio.get("status") == 0])
        if audio_data:
            _global_user_audio[user_id]["ws_client"].send_audio(audio_data, LastFrame)
            for audio in _global_user_audio[user_id]["audio_data"]:
                audio["status"] = 1


def handle_audio_stop_message(message):
    """
        处理音频消息终止
    """
    user_id = message.get("user_id")
    if user_id in _global_user_audio:
        _global_user_audio[user_id]["ws_client"] = None
        _global_user_audio[user_id]["audio_data"] = []


def generate_sql_to_data(params):
    """
        生成sql语句
    """
    user_id = params.get("user_id")
    assistant_id = params.get("assistant_id")
    question_content = params.get("msg_content", "")
    msg_parent_id = params.get("msg_parent_id", None)
    sql_instruction = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == assistant_id,
        AssistantInstruction.instruction_name == "SQLGenerate",
        AssistantInstruction.instruction_status == "正常",
    ).first()
    if sql_instruction:
        sql_code_obj = run_assistant_instruction(
            {
                "instruction_id": sql_instruction.id,
                "user_id": user_id,
                "msg_id": msg_parent_id,
                "user_params": json.dumps({
                    "message_text": question_content
                })
            }
        ).json.get("result")
        if sql_code_obj:
            try:
                sql_code = sql_code_obj.get("sql_code")
                # 执行sql查询语句并获得结果
                if sql_code:
                    try:
                        sql_result = db.session.execute(text(sql_code))
                    except Exception as e:
                        db.session.rollback()
                        print(f"SQL 执行错误: {e}")
                        return {
                            "sql": sql_code,
                            "data": [],
                            "columns": [],
                            "msg_id": msg_parent_id
                        }
                    # 获取列名
                    columns = sql_result.keys()

                    def format_row(row, columns):
                        def format_value(val):
                            if isinstance(val, datetime):
                                return val.strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(val, timedelta):
                                return str(val)  # 将 timedelta 转换为字符串
                            elif isinstance(val, Decimal):
                                return float(val)  # 将 Decimal 转换为 float
                            elif isinstance(val, UUID):
                                return str(val)  # 将 UUID 转换为字符串
                            elif isinstance(val, (list, dict)):
                                return val  # 如果是列表或字典，直接返回
                            else:
                                return val  # 其他类型保持不变

                        return {
                            col: format_value(val)
                            for col, val in zip(columns, row)
                        }

                    sql_result = [format_row(row, columns) for row in sql_result]
                    data = {
                        "sql": sql_code,
                        "data": sql_result,
                        "columns": [str(col) for col in columns],
                        "msg_id": msg_parent_id
                    }
                    task = WorkFlowTaskInfo.query.filter(
                        WorkFlowTaskInfo.user_id == user_id,
                        WorkFlowTaskInfo.msg_id == msg_parent_id,
                        WorkFlowTaskInfo.task_type == "SQL查询",
                    ).first()
                    if task:
                        task.task_result = json.dumps(data)
                        db.session.add(task)
                        db.session.commit()
                    # 通过websocket 提交至前端
                    all_user_clients = redis_client.get(user_id)
                    if all_user_clients:
                        all_user_clients = json.loads(all_user_clients)
                        for client in all_user_clients:
                            if client.get('status') == 'connected':
                                socketio.emit('update_sql_result', data, room=client.get('session_id'))
                    return data
            except Exception as e:
                print(e)
                return ''

    return ''


