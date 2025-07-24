import time
from app.models.next_console.next_console_model import *
from app.models.app_center.app_info_model import WorkFlowTaskInfo
from app.services.task_center.workflow import auto_naming_session, create_recommend_question
from flask import Response, stream_with_context
from app.models.configure_center.llm_kernel import LLMInstance
from app.services.assistant_center.assistant_manager import get_assistant
from app.services.next_console.base import *
from app.services.next_console.llm import llm_chat
from app.services.next_console.workflow import *
from app.services.next_console.attachment import extract_attachment_images_to_question
from app.services.assistant_center.assistant_instruction import run_assistant_instruction
from app.services.next_console.memory import retrieve_messages_to_prompt
from datetime import datetime
from app.app import app
import json
import concurrent.futures
from jinja2 import Template
from app.services.next_console.rag import search_generate_rag_question


def next_search_add_message_v3(params):
    """
    工作台核心交互接口
    :param params:
    :return:
    """
    # 会话参数
    user_id = int(params.get("user_id"))
    session_id = params.get("session_id")
    msg_version = params.get("msg_version", 0)
    question_content = params.get("msg_content", "")
    stream = params.get("stream", True)
    response_format = params.get("response_format", "text")
    time_enhanced = params.get("time_enhanced", True)

    # 助手参数
    assistant_id = params.get("assistant_id", -12345)
    assistant = get_assistant({
        "id": assistant_id,
        "user_id": user_id,
        "caller": "next_console_add_message"
    }).json.get("result")
    if not assistant:
        assistant = get_assistant({
            "id": -12345,
            "user_id": user_id,
            "caller": "next_console_add_message"
        }).json.get("result")
    assistant_memory_size = assistant["assistant_memory_size"]

    system_messages = {"role": "system", "content": assistant["assistant_role_prompt"]}
    temperature = assistant.get("assistant_temperature", 0.7)
    msg_inner_content_obj = {"role": "user", "content": question_content}

    current_session = NextConsoleSession.query.filter(
        NextConsoleSession.user_id == user_id,
        NextConsoleSession.id == session_id
    ).first()
    msg_llm_type = LLMInstance.query.filter(
        LLMInstance.llm_code == current_session.session_llm_code
    ).first()
    if not msg_llm_type:
        params["msg_llm_type"] = "unknown"
    else:
        params["msg_llm_type"] = msg_llm_type.llm_name
    question = save_user_question({
        "user_id": user_id,
        "session": current_session.to_dict(),
        "message": question_content,
    }).json.get("result")
    msg_parent_id = question.get("msg_id")
    qa_id = question.get("qa_id")
    # 直接回答问题
    # workflow - 创建推荐问题
    create_recommend_question.delay({
        "user_id": user_id,
        "assistant_id": assistant_id,
        "msg_id": msg_parent_id,
        "msg_content": question_content
    })

    rag_flag = False
    if (current_session.session_search_engine_switch or current_session.session_local_resource_switch
            or current_session.session_attachment_file_switch or current_session.session_attachment_webpage_switch
            or current_session.session_local_resource_use_all
    ):
        rag_flag = True

    # workflow - 检索参考资料
    if rag_flag:
        # 新增问题理解
        QueryUnderstand_instruction = AssistantInstruction.query.filter(
            AssistantInstruction.assistant_id == assistant_id,
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
            try:
                if true_question and true_question[1]:
                    question_content = true_question[1]
            except Exception as e:
                app.logger.error(f"run instruction error: {e}")
        # 资源检索
        rag_instruction = AssistantInstruction.query.filter(
            AssistantInstruction.assistant_id == assistant_id,
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
            "assistant_id": assistant_id,
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
    if len(memory_messages) >= 2 and current_session.session_topic == "未命名会话":
        auto_naming_session.delay({
            "user_id": user_id,
            "session_id": session_id,
            "assistant_id": assistant_id,
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
    if time_enhanced:
        current_bei_jing_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        system_messages["content"] += f"\n现在的北京时间是{current_bei_jing_time}"
    messages.insert(0, system_messages)
    messages.append(msg_inner_content_obj)
    chat_params = {
        "user_id": user_id,
        "session_id": session_id,
        "session_llm_code": current_session.session_llm_code,
        "qa_id": qa_id,
        "msg_parent_id": msg_parent_id,
        "assistant_id": assistant_id,
        "model": msg_llm_type,
        "messages": messages,
        "stream": stream,
        "response_format": response_format,
        "msg_version": msg_version,
        "temperature": temperature,
        "rag_flag": rag_flag,
    }
    # workflow - 调用大模型驱动回答问题
    return llm_chat(chat_params)


def next_search_workflow_query_agent_v3(params):
    """
        query-agent-v2 基于上下文智能
            理解用户问题， 路由场景， 检索资料， 分配助手， 构建流程 ,给出最终问题
        return 问题对象，问题类型
        问题类型：0-普通问题，1-澄清问题，2-分解问题
    """
    # 会话参数
    user_id = int(params.get("user_id"))
    session_id = params.get("session_id")
    qa_id = params.get("qa_id")
    msg_parent_id = params.get("msg_parent_id")
    query_assistant = params.get("assistant", {})
    question_content = params.get("msg_content", "")
    msg_inner_content_obj = {"role": "user", "content": question_content}
    session_task_kg_list = params.get("session_task_kg_list", [])
    next_console_kg = params.get("session_task_kg_list", False)
    search_engine_enhanced = params.get("search_engine_enhanced", "auto")
    if not query_assistant:
        return msg_inner_content_obj, 0
    # todo 按照workflow进行处理
    # 0. 问答预检
    instruction_faq = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == -12345,
        AssistantInstruction.instruction_name == "FAQ"
    ).first()
    if instruction_faq:
        faq_question = run_assistant_instruction(
            {
                "instruction_id": instruction_faq.id,
                "user_id": user_id,
                "msg_id": msg_parent_id,
                "user_params": json.dumps({
                    "query_text": question_content
                }),
                "faq_direct_return": 'true'
            }
        )
        if faq_question and faq_question.json.get("result"):
            faq_question = faq_question.json.get("result")
            return {"role": "user", "content": faq_question}, 0

    # 1. 策略调度 and rag 判断
    instruction_pre_rag = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == -12345,
        AssistantInstruction.instruction_name == "PRE_RAG"
    ).first()
    rag_flag = False
    if instruction_pre_rag:
        rag_flag_model = run_assistant_instruction({
            "instruction_id": instruction_pre_rag.id,
            "user_id": user_id,
            "msg_id": msg_parent_id
        }).json.get("result")
        if rag_flag_model and rag_flag_model.strip()[0] in ("a", "b"):
            rag_flag = True
    instruction_ps = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == -12345,
        AssistantInstruction.instruction_name == "PolicySchedule"
    ).first()
    if not instruction_ps:
        return msg_inner_content_obj, 0
    try:
        continuity_flag, session_policy = run_assistant_instruction({
                "instruction_id": instruction_ps.id,
                "user_id": user_id,
                "msg_id": msg_parent_id,
            }
        ).json.get("result")
    except Exception as e:
        app.logger.error(f"run instruction error: {e}")
        return msg_inner_content_obj, 0
    # if session_policy == "task" and not rag_flag:
    #     return msg_inner_content_obj, 3
    if session_policy not in ("knowledge", "recommend") and not rag_flag:  # 仅知识模式
        return msg_inner_content_obj, 0

    # 2. 改写问题
    instruction_qu = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == -12345,
        AssistantInstruction.instruction_name == "QueryUnderstand"
    ).first()
    if not instruction_qu:
        return msg_inner_content_obj, 0
    try:
        rewrite_flag, rewrite_question = run_assistant_instruction(
            {
                "instruction_id": instruction_qu.id,
                "user_id": user_id,
                "msg_id": msg_parent_id,
            }
        ).json.get("result")
    except Exception as e:
        rewrite_flag = 0
        rewrite_question = question_content
    try:
        if int(rewrite_flag) == 0:
            rewrite_question = question_content
    except Exception as e:
        app.logger.error(f"run instruction error: {e}")
        rewrite_question = question_content
    msg_inner_content_obj = {"role": "user", "content": rewrite_question}
    # 2.1. 问答预检
    instruction_faq = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == -12345,
        AssistantInstruction.instruction_name == "FAQ"
    ).first()
    if instruction_faq:
        faq_question = run_assistant_instruction(
            {
                "instruction_id": instruction_faq.id,
                "user_id": user_id,
                "msg_id": msg_parent_id,
                "user_params": json.dumps({
                    "query_text": rewrite_question
                }),
                "faq_direct_return": 'true'
            }
        )
        if faq_question and faq_question.json.get("result"):
            faq_question = faq_question.json.get("result")
            return {"role": "user", "content": faq_question}, 0
    # 3. 澄清问题
    instruction_cl = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == -12345,
        AssistantInstruction.instruction_name == "QueryClarify"
    ).first()
    if not instruction_cl:
        return msg_inner_content_obj, 0
    try:
        clarify_flag, clarify_question = run_assistant_instruction(
            {
                "instruction_id": instruction_cl.id,
                "user_id": user_id,
                "msg_id": msg_parent_id,
                "user_params": json.dumps({
                    "question": rewrite_question
                })
            }
        ).json.get("result")
    except Exception as e:
        app.logger.error(f"run instruction error: {e}")
        return msg_inner_content_obj, 0
    if clarify_flag == "answer_clarify":
        msg_inner_content_obj = {"role": "user", "content": clarify_question}
    elif clarify_flag == "clarify_answer" and not rag_flag:
        clarify_question = clarify_question.strip().strip('"')
        msg_inner_content_obj = {"role": "user", "content": clarify_question}
        return msg_inner_content_obj, 1
    else:
        clarify_question = rewrite_question

    # 4. 分解问题
    instruction_de = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == -12345,
        AssistantInstruction.instruction_name == "QueryDecompose"
    ).first()
    if not instruction_de:
        return msg_inner_content_obj, 0
    decompose_question_list = run_assistant_instruction(
        {
            "instruction_id": instruction_de.id,
            "user_id": user_id,
            "msg_id": msg_parent_id,
            "user_params": json.dumps({
                "question": clarify_question
            })
        }
    ).json.get("result")
    decompose_question_list = [x for x in decompose_question_list if x.strip() and x.strip() not in ('0', "1")]
    if len(decompose_question_list) < 2:
        decompose_question_list = []
    # 5. 检索资料
    instruction_rag = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == -12345,
        AssistantInstruction.instruction_name == "RAG"
    ).first()
    if not decompose_question_list:
        if not instruction_rag:
            app.logger.warning(f"RAG instruction not found")
            return msg_inner_content_obj, 0
        rag_question = run_assistant_instruction(
            {
                "instruction_id": instruction_rag.id,
                "user_id": user_id,
                "msg_id": msg_parent_id,
                "user_params": json.dumps({
                    "query_text": clarify_question
                }),
                "session_task_kg_list": session_task_kg_list,
                "next_console_kg": next_console_kg,
                "search_engine_enhanced": search_engine_enhanced
            }
        ).json.get("result")
        if rag_question:
            return {"role": "user", "content": rag_question}, 0
        else:
            return msg_inner_content_obj, 0

    # 5.1 批量检索资料
    # 生成任务记录
    target_assistant = Assistant.query.filter(
        Assistant.id == -12345
    ).first()
    inner_task_params = {
        "system_params": {
            "message_text": decompose_question_list
        },
        "user_params": {
            "query_text": decompose_question_list,
            "message_text": decompose_question_list
        },
    }
    task_params = {
        "user_id": user_id,
        "session_id": session_id,
        "qa_id": qa_id,
        "msg_id": msg_parent_id,
        "task_assistant_id": -12345,
        "task_model_name": target_assistant.assistant_model_name,
        "task_type": instruction_rag.instruction_desc,
        "task_assistant_instruction": instruction_rag.instruction_name,
        "task_params": inner_task_params,
        "task_prompt": "",
        "task_status": "running",
        "begin_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    new_task = WorkFlowTaskInfo(**task_params)
    db.session.add(new_task)
    db.session.commit()
    all_sub_true_questions = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(decompose_question_list)) as executor:
        future_to_sub_question = {
            executor.submit(
                process_sub_question_v2,
                sub_question,
                i + 1,
                msg_parent_id,
                user_id,
                session_id,
                instruction_rag.instruction_result_template
            ): sub_question for i, sub_question in enumerate(decompose_question_list)
        }
        for future in concurrent.futures.as_completed(future_to_sub_question):
            sub_true_question = future.result()
            if sub_true_question:  # only append if not None
                all_sub_true_questions.append(sub_true_question)
    all_sub_true_questions.sort(key=lambda x: x['title'].strip()[0].lower() if x['title'].strip() else '')
    new_task.task_result = str(all_sub_true_questions)
    new_task.task_status = "finished"
    new_task.end_time = datetime.now()
    db.session.add(new_task)
    db.session.commit()
    return all_sub_true_questions, 2


def process_sub_question_v2(sub_question, sub_question_index, question_id, user_id, session_id,
                            instruction_result_template):
    with app.app_context():
        try:
            sub_question_id = f"{question_id}_{sub_question_index}"
            reference_text = search_generate_rag_question(
                user_id,
                session_id,
                sub_question_id,
                sub_question,
                query_k=5,
                pre_fix=f"{sub_question_index}_"
            )
            workflow_res = {
                "message": sub_question,
                "query_text": sub_question,
                "reference_text": reference_text,
            }
            instruction_result_template = Template(instruction_result_template)
            sub_true_question = instruction_result_template.render(workflow_res)
            return {
                "role": "query-agent",
                "content": sub_true_question,
                "title": sub_question,
            }
        except Exception as e:
            print(f"Error processing sub_question {sub_question_index}: {e}")
            return None


def response_clarify_question(params):
    """
    流式返回澄清问题
    """

    new_message = NextConsoleMessage(
        user_id=int(params.get("user_id")),
        session_id=params.get("session_id"),
        qa_id=params.get("qa_id"),
        assistant_id=params.get("assistant_id", -12345),
        msg_llm_type=params["msg_llm_type"],
        msg_role="assistant",
        msg_prompt="",
        msg_content=params["msg_content"],
        msg_token_used=0,
        msg_time_used=0,
        msg_format="text",
        msg_remark=0,
        msg_del=0,
        msg_version=0,
        msg_parent_id=params["msg_parent_id"]
    )
    db.session.add(new_message)
    db.session.commit()
    # 流式返回澄清问题

    def generate(_msg_content):
        yield _msg_content

    return Response(stream_with_context(generate(params["msg_content"])))


def next_search_workflow_service_agent_v3(params):
    """
    query-agent-v3 基于助手的工作流配置只能执行指令
    """
    # 会话参数
    user_id = int(params.get("user_id"))
    session_id = params.get("session_id")
    qa_id = params.get("qa_id")
    msg_parent_id = params.get("msg_parent_id")
    assistant = params.get("assistant", {})
    question_content = params.get("msg_content", "")
    msg_inner_content_obj = {"role": "user", "content": question_content}
    if not assistant:
        return msg_inner_content_obj, 0
    # todo 通过通用工作流来执行与管理
    # 0. 问答预检
    instruction_faq = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == assistant["id"],
        AssistantInstruction.instruction_name == "FAQ"
    ).first()
    if instruction_faq:
        faq_question = run_assistant_instruction(
            {
                "instruction_id": instruction_faq.id,
                "user_id": user_id,
                "msg_id": msg_parent_id,
                "user_params": json.dumps({
                    "query_text": question_content
                }),
                "faq_direct_return": 'true'
            }
        )
        if faq_question and faq_question.json.get("result"):
            faq_question = faq_question.json.get("result")
            return {"role": "user", "content": faq_question}, 0
    # 1. 策略调度 and rag 判断
    instruction_qa = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == assistant["id"],
        AssistantInstruction.instruction_name == "QueryAgent"
    ).first()
    if instruction_qa:
        try:
            params["instruction"] = instruction_qa
            understand_result = run_assistant_instruction(
                {
                    "instruction_id": instruction_qa.id,
                    "user_id": user_id,
                    "msg_id": msg_parent_id,
                    "user_params": json.dumps({
                        "query_text": question_content
                    })
                }
            ).json.get("result")
            if understand_result:
                # 2. 检索资料
                rag_instruction = AssistantInstruction.query.filter(
                    AssistantInstruction.assistant_id == assistant["id"],
                    AssistantInstruction.instruction_name == "RAG"
                ).first()
                if rag_instruction:

                    rag_question = run_assistant_instruction(
                        {
                            "instruction_id": rag_instruction.id,
                            "user_id": user_id,
                            "msg_id": msg_parent_id,
                            "user_params": json.dumps({
                                "query_text": understand_result["query"]
                            })
                        }
                    )
                    if rag_question and rag_question.json.get("result"):
                        rag_question = rag_question.json.get("result")
                        return {"role": "user", "content": rag_question}, 0
                    else:
                        return msg_inner_content_obj, 0
        except Exception as e:
            app.logger.error(f"run instruction error: {e}")
            return msg_inner_content_obj, 0
    return msg_inner_content_obj, 0


def save_user_question(params):
    """
    保存用户问题
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    session = params.get("session")
    message = params.get("message")
    # 新增qa
    try:
        new_qa = NextConsoleQa(
            user_id=user_id,
            session_id=session.get("id"),
            qa_topic=message,
            qa_status="正常",
        )
        db.session.add(new_qa)
        db.session.commit()
        # 新增消息
        new_message = NextConsoleMessage(
            user_id=user_id,
            session_id=session.get("id"),
            qa_id=new_qa.qa_id,
            msg_role="user",
            msg_content=message,
            msg_llm_type=session.get("session_llm_code"),
        )
        db.session.add(new_message)
        db.session.commit()
        return next_console_response(result=new_message.to_dict())
    except Exception as e:
        print(e)
        db.session.rollback()
        return next_console_response(error_status=True, error_message="保存消息失败，请重试！")

