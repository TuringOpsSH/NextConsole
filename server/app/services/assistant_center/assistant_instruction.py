import json
import csv
from datetime import datetime
from jinja2 import Template
from jsonschema import validate
from app.app import db, app
from app.models.assistant_center.assistant import AssistantInstruction, UserAssistantRelation
from app.models.next_console.next_console_model import NextConsoleMessage, NextConsoleSession
from app.models.app_center.app_info_model import WorkFlowTaskInfo
from app.services.configure_center.response_utils import next_console_response
from app.services.next_console.rag import search_generate_rag_question
from app.services.next_console.memory import retrieve_instruction_context
from app.services.configure_center.llm import workflow_chat
from app.services.task_center.workflow import emit_workflow_status
from app.models.configure_center.llm_kernel import LLMInstance


def add_assistant_instruction(params):
    """
    添加助手指令
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    assistant_id = params.get("assistant_id")
    instruction_name = params.get("instruction_name")
    instruction_desc = params.get("instruction_desc")
    instruction_type = params.get("instruction_type", "llm")
    if instruction_type not in ("llm", "rag"):
        return next_console_response(error_status=True, error_message="指令类型错误！", error_code=1002)
    instruction_system_prompt_template = params.get("instruction_system_prompt_template")
    instruction_user_prompt_template = params.get("instruction_user_prompt_template")
    instruction_result_template = params.get("instruction_result_template")
    instruction_system_prompt_params_json_schema = params.get("instruction_system_prompt_params_json_schema")
    instruction_user_prompt_params_json_schema = params.get("instruction_user_prompt_params_json_schema")
    instruction_result_json_schema = params.get("instruction_result_json_schema")
    instruction_result_extract_format = params.get("instruction_result_extract_format", "json")
    instruction_result_extract_separator = params.get("instruction_result_extract_separator", ",")
    instruction_result_extract_quote = params.get("instruction_result_extract_quote", "")
    instruction_result_extract_columns = params.get("instruction_result_extract_columns", [])
    instruction_status = params.get("instruction_status", "正常")
    instruction_history_length = params.get("instruction_history_length", 0)
    instruction_max_tokens = params.get("instruction_max_tokens", None)
    if not assistant_id or not instruction_name:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    # 检查是否存在修改助手权限
    target_assistant_rels = UserAssistantRelation.query.filter(
        UserAssistantRelation.assistant_id == assistant_id,
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.rel_type == "权限",
        UserAssistantRelation.rel_status == "正常"
    ).first()
    if not target_assistant_rels or int(target_assistant_rels.rel_value) < 6:
        return next_console_response(error_status=True, error_message="无权限！", error_code=1002)
    # 检查指令是否存在
    assistant_instruction = AssistantInstruction.query.filter(
        AssistantInstruction.assistant_id == assistant_id,
        AssistantInstruction.instruction_name == instruction_name
    ).first()
    if assistant_instruction:
        return next_console_response(error_status=True, error_message="指令已存在！", error_code=1002)

    assistant_instruction = AssistantInstruction(
        user_id=user_id,
        assistant_id=assistant_id,
        instruction_name=instruction_name,
        instruction_type=instruction_type,
        instruction_desc=instruction_desc,
        instruction_system_prompt_template=instruction_system_prompt_template,
        instruction_user_prompt_template=instruction_user_prompt_template,
        instruction_result_template=instruction_result_template,
        instruction_system_prompt_params_json_schema=instruction_system_prompt_params_json_schema,
        instruction_user_prompt_params_json_schema=instruction_user_prompt_params_json_schema,
        instruction_result_json_schema=instruction_result_json_schema,
        instruction_result_extract_format=instruction_result_extract_format,
        instruction_result_extract_separator=instruction_result_extract_separator,
        instruction_result_extract_quote=instruction_result_extract_quote,
        instruction_result_extract_columns=instruction_result_extract_columns,
        instruction_status=instruction_status,
        instruction_history_length=instruction_history_length,
        instruction_max_tokens=instruction_max_tokens,

    )
    db.session.add(assistant_instruction)
    db.session.commit()
    return next_console_response(result=assistant_instruction.to_dict())


def del_assistant_instruction(params):
    """
    删除助手指令
    :param params:
    :return:
    """
    instruction_ids = params.get("instruction_ids", [])
    assistant_instructions = AssistantInstruction.query.filter(
        AssistantInstruction.id.in_(instruction_ids)
    ).all()
    if not assistant_instructions:
        return next_console_response(error_status=True, error_message="指令不存在！", error_code=1002)
    else:
        length_instruction = len(assistant_instructions)
    all_del_instruction_assistant_ids = [assistant_instruction.assistant_id
                                         for assistant_instruction in assistant_instructions]
    # 找到有权限的助手id
    all_assistant_ids = UserAssistantRelation.query.filter(
        UserAssistantRelation.assistant_id.in_(all_del_instruction_assistant_ids),
        UserAssistantRelation.rel_type == "权限",
        UserAssistantRelation.rel_value >= 6,
        UserAssistantRelation.rel_status == "正常"
    ).all()
    all_assistant_ids = [assistant_id.assistant_id for assistant_id in all_assistant_ids]
    for assistant_instruction in assistant_instructions:
        if assistant_instruction.assistant_id not in all_assistant_ids:
            return next_console_response(error_status=True,
                                         error_message=f"无权限！指令id:{assistant_instruction.id}", error_code=1002)
        db.session.delete(assistant_instruction)
        db.session.commit()
    return next_console_response(result=f"删除成功！共删除{length_instruction}条指令")


def update_assistant_instruction(params):
    """
    更新助手指令
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    instruction_id = params.get("id")
    instruction_name = params.get("instruction_name")
    instruction_desc = params.get("instruction_desc")
    instruction_type = params.get("instruction_type", "llm")
    if instruction_type not in ("llm", "rag"):
        return next_console_response(error_status=True, error_message="指令类型错误！", error_code=1002)

    instruction_system_prompt_template = params.get("instruction_system_prompt_template")
    instruction_user_prompt_template = params.get("instruction_user_prompt_template")
    instruction_result_template = params.get("instruction_result_template")
    instruction_system_prompt_params_json_schema = params.get("instruction_system_prompt_params_json_schema")
    instruction_user_prompt_params_json_schema = params.get("instruction_user_prompt_params_json_schema")
    instruction_result_json_schema = params.get("instruction_result_json_schema")
    instruction_result_extract_format = params.get("instruction_result_extract_format", "json")
    instruction_result_extract_separator = params.get("instruction_result_extract_separator", ",")
    instruction_result_extract_quote = params.get("instruction_result_extract_quote", "")
    instruction_result_extract_columns = params.get("instruction_result_extract_columns", [])
    instruction_status = params.get("instruction_status", "正常")
    instruction_history_length = params.get("instruction_history_length", 0)
    instruction_max_tokens = params.get("instruction_max_tokens", None)
    assistant_instruction = AssistantInstruction.query.filter(
        AssistantInstruction.id == instruction_id,
        AssistantInstruction.user_id == user_id
    ).first()
    if not assistant_instruction:
        return next_console_response(error_status=True, error_message="指令不存在！", error_code=1002)
    if instruction_name and instruction_name != assistant_instruction.instruction_name:
        assistant_instruction_same = AssistantInstruction.query.filter(
            AssistantInstruction.assistant_id == assistant_instruction.assistant_id,
            AssistantInstruction.instruction_name == instruction_name
        ).first()
        if assistant_instruction_same:
            return next_console_response(error_status=True, error_message=f"指令名称已被占用：{instruction_name}！",
                                         error_code=1002)
        assistant_instruction.instruction_name = instruction_name
    if instruction_desc is not None and instruction_desc != assistant_instruction.instruction_desc:
        assistant_instruction.instruction_desc = instruction_desc
    if (instruction_system_prompt_template
            and instruction_system_prompt_template != assistant_instruction.instruction_system_prompt_template):
        assistant_instruction.instruction_system_prompt_template = instruction_system_prompt_template
    if (instruction_user_prompt_template
            and instruction_user_prompt_template != assistant_instruction.instruction_user_prompt_template):
        assistant_instruction.instruction_user_prompt_template = instruction_user_prompt_template
    if (instruction_result_template
            and instruction_result_template != assistant_instruction.instruction_result_template):
        assistant_instruction.instruction_result_template = instruction_result_template
    if instruction_type and instruction_type != assistant_instruction.instruction_type:
        assistant_instruction.instruction_type = instruction_type
    if (instruction_system_prompt_params_json_schema
            and instruction_system_prompt_params_json_schema != assistant_instruction.instruction_system_prompt_params_json_schema):
        assistant_instruction.instruction_system_prompt_params_json_schema = instruction_system_prompt_params_json_schema
    if (instruction_user_prompt_params_json_schema
            and instruction_user_prompt_params_json_schema != assistant_instruction.instruction_user_prompt_params_json_schema):
        assistant_instruction.instruction_user_prompt_params_json_schema = instruction_user_prompt_params_json_schema
    if (instruction_result_extract_format
            and instruction_result_extract_format != assistant_instruction.instruction_result_extract_format):
        assistant_instruction.instruction_result_extract_format = instruction_result_extract_format
    if (instruction_result_extract_separator
            and instruction_result_extract_separator != assistant_instruction.instruction_result_extract_separator):
        assistant_instruction.instruction_result_extract_separator = instruction_result_extract_separator
    if (instruction_result_extract_quote
            and instruction_result_extract_quote != assistant_instruction.instruction_result_extract_quote):
        assistant_instruction.instruction_result_extract_quote = instruction_result_extract_quote
    if (instruction_result_json_schema
            and instruction_result_json_schema != assistant_instruction.instruction_result_json_schema):
        assistant_instruction.instruction_result_json_schema = instruction_result_json_schema
    if instruction_status in ("正常", "禁用") and instruction_status != assistant_instruction.instruction_status:
        assistant_instruction.instruction_status = instruction_status
    if (instruction_result_extract_columns and
            instruction_result_extract_columns != assistant_instruction.instruction_result_extract_columns):
        assistant_instruction.instruction_result_extract_columns = instruction_result_extract_columns
    if (instruction_history_length is not None and
            instruction_history_length != assistant_instruction.instruction_history_length):
        assistant_instruction.instruction_history_length = instruction_history_length
    if (instruction_max_tokens is not None and
            instruction_max_tokens != assistant_instruction.instruction_max_tokens):
        assistant_instruction.instruction_max_tokens = instruction_max_tokens
    db.session.commit()
    return next_console_response(result=assistant_instruction.to_dict())


def get_assistant_instruction(params):
    """
    获取助手指令
    :param params:
    :return:
    """
    instruction_id = params.get("id")
    assistant_instructions = AssistantInstruction.query.filter(
        AssistantInstruction.id == instruction_id
    ).first()
    if not assistant_instructions:
        return next_console_response(error_status=True, error_message="指令不存在！", error_code=1002)
    # 检查是否有权限
    user_id = int(params.get("user_id"))
    assistant_id = assistant_instructions.assistant_id
    target_assistant_rel = UserAssistantRelation.query.filter(
        UserAssistantRelation.assistant_id == assistant_id,
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.rel_type == "权限",
        UserAssistantRelation.rel_status == "正常"
    ).first()
    if not target_assistant_rel:
        return next_console_response(error_status=True, error_message="无权限！", error_code=1002)
    if target_assistant_rel.rel_value >= 6:
        return next_console_response(result=assistant_instructions.to_dict())
    else:
        res = assistant_instructions.to_dict()
        return next_console_response(result=res)


def search_assistant_instruction(params):
    """
    搜索助手指令
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    assistant_ids = params.get("assistant_ids", [])
    instruction_name = params.get("instruction_name", "")
    instruction_desc = params.get("instruction_desc", "")
    instruction_status = params.get("instruction_status", ["正常"])
    page_num = params.get("page", 1)
    page_size = params.get("page_size", 50)
    fetch_all = params.get("fetch_all", False)

    # 获取所有有权限的助手id
    all_assistant_ids = UserAssistantRelation.query.filter(
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.rel_type == "权限",
        UserAssistantRelation.rel_status == "正常"
    ).all()
    all_assistant_ids = [assistant_id.assistant_id for assistant_id in all_assistant_ids]
    if assistant_ids:
        all_assistant_ids = list(set(assistant_ids).intersection(set(all_assistant_ids)))
    filter_condition = [
        AssistantInstruction.assistant_id.in_(all_assistant_ids),
    ]
    if instruction_name:
        filter_condition.append(AssistantInstruction.instruction_name.like(f"%{instruction_name}%"))
    if instruction_desc:
        filter_condition.append(AssistantInstruction.instruction_desc.like(f"%{instruction_desc}%"))
    if instruction_status:
        filter_condition.append(AssistantInstruction.instruction_status.in_(instruction_status))
    if fetch_all:
        assistant_instructions = AssistantInstruction.query.filter(*filter_condition).all()
    else:
        assistant_instructions = AssistantInstruction.query.filter(*filter_condition).paginate(
            page=page_num, per_page=page_size, error_out=False)

    assistant_instructions_result = []
    for assistant_instruction in assistant_instructions:
        assistant_instruction_dict = assistant_instruction.to_dict()
        del assistant_instruction_dict["instruction_prompt"]
        assistant_instructions_result.append(assistant_instruction_dict)
    return next_console_response(result=assistant_instructions_result)


def render_assistant_instruction(params):
    """
    渲染助手指令
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    instruction_id = params.get("id")
    instruction_params = params.get("instruction_params", {})
    instruction = AssistantInstruction.query.filter(
        AssistantInstruction.id == instruction_id
    ).first()
    if not instruction:
        return next_console_response(error_status=True, error_message="指令不存在！", error_code=1002)
    # 检查是否有权限
    assistant_id = instruction.assistant_id
    target_assistant_rel = UserAssistantRelation.query.filter(
        UserAssistantRelation.assistant_id == assistant_id,
        UserAssistantRelation.user_id == user_id,
        UserAssistantRelation.rel_type == "权限",
        UserAssistantRelation.rel_status == "正常"
    ).first()
    if not target_assistant_rel:
        return next_console_response(error_status=True, error_message="无权限！", error_code=1002)
    instruction_prompt = Template(instruction.instruction_prompt or '')
    instruction_content = instruction_prompt.render(instruction_params)
    return next_console_response(result=instruction_content)


def run_assistant_instruction(params):
    """
    根据指令完成任务
        参数解析，任务执行，结果解析，渲染结果，返回结果
    """
    instruction_id = params.get("instruction_id")
    user_id = int(params.get("user_id"))
    msg_id = params.get("msg_id", 0)
    system_params = params.get("system_params", '{}')
    user_params = params.get("user_params", '{}')
    dry_run = params.get("dry_run", False)
    faq_direct_return = params.get("faq_direct_return", 'false')
    assistant_instruction = AssistantInstruction.query.filter(
        AssistantInstruction.id == instruction_id
    ).first()
    if not assistant_instruction:
        app.logger.warning(f"RAG instruction not found")
        return next_console_response(error_status=True, error_message="指令不存在！", error_code=1002)

    # 检查是否有权限
    assistant_id = assistant_instruction.assistant_id
    target_msg = NextConsoleMessage.query.filter(
        NextConsoleMessage.msg_id == msg_id,
        NextConsoleMessage.user_id == user_id
    ).first()

    if not target_msg:
        return next_console_response(error_status=True, error_message="消息不存在！", error_code=1002)
    history_length = assistant_instruction.instruction_history_length
    if history_length:
        history_list = retrieve_instruction_context(target_msg, history_length)
    else:
        history_list = []
    message_text = target_msg.msg_content
    messages = []
    # 渲染system
    try:
        system_params = json.loads(system_params)
        system_params["message_text"] = message_text
    except Exception as e:
        app.logger.warning(f"system_params格式错误,{e}")
        return next_console_response(error_status=True, error_message="system_params格式错误！", error_code=1002)
    if assistant_instruction.instruction_system_prompt_params_json_schema:
        try:
            validate(system_params, json.loads(assistant_instruction.instruction_system_prompt_params_json_schema))
        except Exception as e:
            app.logger.warning(f"system_params参数错误,{e}")
            return next_console_response(error_status=True, error_message="system_params参数错误！", error_code=1002)
    try:
        system_prompt_template = Template(assistant_instruction.instruction_system_prompt_template or '')
        system_prompt = system_prompt_template.render(system_params)
    except Exception as e:
        app.logger.warning(f"system_prompt模板渲染错误,{e}")
        return next_console_response(error_status=True, error_message="system_prompt模板渲染错误！", error_code=1002)
    messages.append({"role": "system", "content": system_prompt})
    messages.extend(history_list)
    # 渲染user
    try:
        user_params = json.loads(user_params)
        user_params["message_text"] = message_text
    except Exception as e:
        app.logger.warning(f"user_params格式错误,{e}")
        return next_console_response(error_status=True, error_message="user_params格式错误！", error_code=1002)
    if assistant_instruction.instruction_user_prompt_params_json_schema:
        try:
            validate(user_params, json.loads(assistant_instruction.instruction_user_prompt_params_json_schema))
        except Exception as e:
            app.logger.warning(f"user_params格式错误,{e}")
            return next_console_response(error_status=True, error_message="user_params参数错误！", error_code=1002)
    try:
        user_prompt_template = Template(assistant_instruction.instruction_user_prompt_template or '')
        user_prompt = user_prompt_template.render(user_params)
    except Exception as e:
        app.logger.warning(f"user_prompt模板渲染错误,{e}")
        return next_console_response(error_status=True, error_message="user_prompt模板渲染错误！", error_code=1002)
    messages.append({"role": "user", "content": user_prompt})
    if dry_run:
        return next_console_response(result=messages)
    target_session = NextConsoleSession.query.filter(
        NextConsoleSession.id == target_msg.session_id,
        NextConsoleSession.user_id == user_id
    ).first()
    target_llm_config = LLMInstance.query.filter(
            LLMInstance.llm_code == target_session.session_llm_code,
        ).first()
    # 生成任务数据
    inner_task_params = {
        "system_params": system_params,
        "user_params": user_params,
    }
    task_params = {
        "user_id": user_id,
        "session_id": target_msg.session_id,
        "qa_id": target_msg.qa_id,
        "msg_id": target_msg.msg_id,
        "task_assistant_id": assistant_id,
        "task_model_name": target_llm_config.llm_name,
        "task_type": assistant_instruction.instruction_desc,
        "task_assistant_instruction": assistant_instruction.instruction_name,
        "task_params": inner_task_params,
        "task_prompt": messages,
        "task_status": "running",
        "begin_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    new_task = WorkFlowTaskInfo(**task_params)
    db.session.add(new_task)
    db.session.commit()
    emit_workflow_status.delay({
        "user_id": user_id,
        "new_task": new_task.to_dict()
    })
    # 执行任务
    if assistant_instruction.instruction_type == "llm":
        workflow_chat_params = {
            "session_llm_code": target_llm_config.llm_code,
            "user_id": user_id,
            "model": target_llm_config.llm_name,
            "messages": messages,
            "stream": False,
            "new_task": new_task,
            "temperature": assistant_instruction.instruction_temperature,
            "max_tokens": assistant_instruction.instruction_max_tokens,
            "response_format": assistant_instruction.instruction_result_extract_format,
        }
        workflow_res = workflow_chat(workflow_chat_params)
    elif assistant_instruction.instruction_type == "rag":
        query_text = user_params.get("query_text", "")
        if not query_text:
            return next_console_response(error_status=True, error_message="query_text参数错误！", error_code=1002)
        workflow_res = {
            "message": message_text,
            "query_text": query_text,
        }
        reference_text = search_generate_rag_question(
            user_id=user_id,
            session_id=target_msg.session_id,
            qa_id=target_msg.qa_id,
            msg_id=target_msg.msg_id,
            assistant_id=assistant_id,
            model_name=target_llm_config.llm_name,
            question_content=query_text,
            faq_direct_return=faq_direct_return,
        )
        workflow_res["reference_text"] = reference_text
        # 更新任务状态
        new_task.task_status = "finished"
        new_task.end_time = datetime.now()
        new_task.task_result = str(reference_text)
        db.session.add(new_task)
        db.session.commit()
        emit_workflow_status.delay({
            "user_id": user_id,
            "new_task": new_task.to_dict()
        })
        if not reference_text:
            return next_console_response()
    else:
        return next_console_response(error_status=True, error_message="指令类型错误！", error_code=1002)
    # 解析结果
    if assistant_instruction.instruction_result_extract_format == "json":
        workflow_res = workflow_res.strip()
        if workflow_res.startswith("```json"):
            workflow_res = workflow_res.lstrip("```json").rstrip("```")
        try:
            instruction_result = json.loads(workflow_res)
        except Exception as e:
            return next_console_response(error_status=True, error_message="解析结果错误！", error_code=1002,
                                         result=workflow_res)
        try:
            if assistant_instruction.instruction_result_json_schema:
                validate(instruction_result, json.loads(assistant_instruction.instruction_result_json_schema))
        except Exception as e:
            return next_console_response(error_status=True, error_message="结果参数错误！", error_code=1002)
    elif assistant_instruction.instruction_result_extract_format == "table":
        try:
            reader = csv.reader([workflow_res.replace("\n", "")],
                                delimiter=assistant_instruction.instruction_result_extract_separator,
                                quotechar=assistant_instruction.instruction_result_extract_quote
                                if assistant_instruction.instruction_result_extract_quote else None
                                )
            # 获取切分后的结果
            result = next(reader)
        except Exception as e:
            app.logger.warning(f"解析结果错误,{e}")
            return None
        columns = assistant_instruction.instruction_result_extract_columns
        if columns:
            instruction_result = {}
            if len(columns) != len(result):
                app.logger.warning(f"解析结果错误，列数不匹配")
                return None
            for i, column in enumerate(columns):

                instruction_result[column] = result[i]
        else:
            instruction_result = result
    else:  # text
        instruction_result = workflow_res
    # 渲染结果
    if assistant_instruction.instruction_result_template:
        instruction_result_template = Template(assistant_instruction.instruction_result_template or '')
        instruction_result = instruction_result_template.render(instruction_result)
    # 推送指令结果

    return next_console_response(result=instruction_result)


