from pathlib import Path
import base64
from openai import OpenAI
from app.models.next_console.next_console_model import NextConsoleMessage
from app.services.configure_center.llm import NextConsoleLLMClient, LLMInstance
from app.app import redis_client, app
from app.services.configure_center.response_utils import next_console_response
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.services.app_center.node_params_service import *
from app.services.next_console.memory import retrieve_instruction_context
from datetime import datetime


def llm_node_execute(params, task_record, global_params):
    """
    llm 节点执行器
        1. 读取节点信息
        2. 判断是否与结束节点相连，相连则yield结果
        3. 提取记忆
        4. 渲染prompt
        5. 解析模型驱动参数
        6. 处理消息
        7. 流式执行
        8. 非流式执行
        9. 处理消息
    :param params: 由node定义的参数，并从全局参数中获取到，key为变量名，value为变量值
    :param task_record:
    :param global_params
    :return:
    """
    workflow_node_llm_params = load_llm_prams(params, task_record, global_params)
    llm_client = NextConsoleLLMClient(workflow_node_llm_params)
    if not llm_client.llm_client:
        app.logger.error(f"工作流发现此模型{task_record.workflow_node_llm_code}暂不支持")
        task_record.task_status = "异常"
        task_record.task_trace_log = f"工作流发现此模型{task_record.workflow_node_llm_code}暂不支持"
        db.session.add(task_record)
        db.session.commit()
        return next_console_response(error_status=True, error_message=f"此模型{task_record.workflow_node_llm_code}暂不支持")
    msg_content = ""
    msg_reasoning_content = ""
    msg_token_used = 0
    answer_msg = None
    task_status = '执行中'
    task_trace_log = ''
    if workflow_node_llm_params.get("stream", False):
        all_message_format = [msg_schema.get("schema_type") for msg_schema in task_record.workflow_node_message_schema]
        output_flag = (task_record.workflow_node_enable_message
                       and ('messageFlow' in all_message_format or 'customize' in all_message_format)
                       )
        if output_flag:
            answer_msg = NextConsoleMessage(
                user_id=task_record.user_id,
                session_id=task_record.session_id,
                qa_id=task_record.qa_id,
                msg_format='messageFlow',
                task_id=task_record.id,
                msg_llm_type=task_record.workflow_node_llm_code,
                msg_role="assistant",
                msg_parent_id=task_record.msg_id,
                msg_content=''
            )
            db.session.add(answer_msg)
            db.session.commit()

        # 流式执行
        try:
            completion = llm_client.chat(workflow_node_llm_params)
            for chunk in completion:
                if global_params.get("stop_flag"):
                    raise GeneratorExit
                chunk_res = chunk.model_dump_json()
                chunk_res = json.loads(chunk_res)
                try:
                    total_tokens = chunk_res.get("usage").get("total_tokens", 0)
                except Exception as e:
                    total_tokens = 0
                try:
                    reasoning_content = chunk_res.get("choices")[0].get("delta").get("reasoning_content", "")
                except Exception as e:
                    reasoning_content = ""
                try:
                    content = chunk_res.get("choices")[0].get("delta").get("content", "")
                except Exception as e:
                    content = ""
                if not reasoning_content:
                    reasoning_content = ''
                if not content:
                    content = ''
                msg_reasoning_content += reasoning_content
                msg_content += content
                if total_tokens:
                    msg_token_used = total_tokens
                if global_params["stream"] and output_flag and (content or reasoning_content):
                    chunk_res["session_id"] = task_record.session_id
                    chunk_res["qa_id"] = task_record.qa_id
                    chunk_res["msg_parent_id"] = task_record.msg_id
                    chunk_res["msg_id"] = answer_msg.msg_id
                    chunk_res["choices"][0]["delta"]["content"] = content
                    chunk_res["choices"][0]["delta"]["reasoning_content"] = reasoning_content
                    global_params["message_queue"].put(chunk_res)
        except GeneratorExit:
            pass
        except Exception as e3:
            app.logger.error(f"调用基模型异常：{str(e3)}")
            task_status = "异常"
            task_trace_log = str(e3)
            msg_content += "\n\n **对不起，模型服务正忙，请稍等片刻后重试，或者可以试试切换其他模型~**"
            if task_record.workflow_node_enable_message and global_params["stream"] and output_flag:
                except_result = {
                    "id": "",
                    "session_id": task_record.session_id,
                    "qa_id": task_record.qa_id,
                    "msg_parent_id": task_record.msg_id,
                    'msg_id': answer_msg.msg_id,
                    "created": 0,
                    "model": '',
                    "object": "chat.completion",
                    "choices": [
                        {
                            "finish_reason": "error",
                            "index": 0,
                            "delta": {
                                "reasoning_content": "",
                                "content": msg_content,
                                "role": "assistant"
                            },

                        }
                    ]
                }
                global_params["message_queue"].put(except_result)
        finally:
            # 更新llm节点记录
            # 如果有RAG引用，则添加到消息中
            reference_md = ''
            if task_record.workflow_node_rag_ref_show:
                try:
                    reference_md = add_reference_md(task_record, global_params)
                except Exception as e:
                    app.logger.error(f"添加参考文献异常：{e}")
            global_params["message_queue"].put({
                "session_id": task_record.session_id,
                "qa_id": task_record.qa_id,
                "msg_parent_id": task_record.msg_id,
                "msg_id": answer_msg.msg_id,
                "msg_format": "messageFlow",
                "choices": [{
                    "finish_reason": "stop",
                    "index": 0,
                    "delta": {
                        "content": reference_md,
                        "role": "assistant"
                    },
                }]
            })
            msg_content += reference_md
            task_record.task_result = json.dumps({
                "content": msg_content,
                "reasoning_content": msg_reasoning_content,
            })
            task_record.end_time = datetime.now()
            if task_status == '执行中':
                task_status = "已完成"
            task_record.task_status = task_status
            task_record.task_trace_log = task_trace_log
            task_record.task_token_used = msg_token_used
            db.session.add(task_record)
            db.session.commit()
            if output_flag:
                answer_msg.msg_content = msg_content
                answer_msg.reasoning_content = msg_reasoning_content
                answer_msg.msg_token_used = msg_token_used
                db.session.add(answer_msg)
                db.session.commit()
        return True
    else:
        # 非流式执行
        try:
            res = llm_client.chat(workflow_node_llm_params).model_dump_json()
            res = json.loads(res)
            msg_content = res.get("choices")[0].get("message").get("content")
            msg_reasoning_content = res.get("choices")[0].get("reasoning_content", "")
            msg_token_used = res.get("usage", {}).get("total_tokens", 0)
            task_record.task_status = "已完成"
            task_record.task_token_used = msg_token_used
        except Exception as e:
            task_record.task_status = "异常"
            task_record.task_trace_log = str(e)
            app.logger.error(f"workflow_chat error: {e}")
            msg_content = '对不起，模型服务正忙，请稍等片刻后重试，或者可以试试切换其他模型~'

        if task_record.workflow_node_rag_ref_show:
            reference_md = add_reference_md(task_record, global_params)
            msg_content += reference_md
        task_record.task_result = json.dumps({
                "content": msg_content,
                "reasoning_content": msg_reasoning_content,
            })
        task_record.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(task_record)
        db.session.commit()
        return True


def load_llm_prams(task_params, task_record, global_params, imgUrl='url'):
    """
    载入大模型的所有参数
    """
    target_msg = NextConsoleMessage.query.filter(
        NextConsoleMessage.msg_id == task_record.msg_id,
        NextConsoleMessage.user_id == task_record.user_id
    ).first()
    # 提取记忆
    if task_record.node_session_memory_size:
        history_list = retrieve_instruction_context(target_msg, task_record.node_session_memory_size)
    else:
        history_list = []
    messages = [{"role": "system",
                 "content": render_template_with_params(task_record.workflow_node_llm_spt, task_params) or ''}]
    # 渲染prompt
    messages.extend(history_list)
    # 渲染user
    messages.append({"role": "user",
                     "content": render_template_with_params(task_record.workflow_node_llm_upt, task_params) or ''})
    # 解析模型驱动参数
    workflow_node_llm_params = task_record.workflow_node_llm_params
    workflow_node_llm_params['llm_code'] = task_record.workflow_node_llm_code
    response_format = workflow_node_llm_params.get("response_format", "text")
    if response_format == 'json':
        response_format = "json_object"
    workflow_node_llm_params["response_format"] = {"type": response_format}
    workflow_node_llm_params["extra_body"] = load_properties(
        workflow_node_llm_params.get("extra_body_schema", {}).get("properties"), global_params
    )
    # 视觉模式补充
    if (workflow_node_llm_params.get("support_vis") and
            workflow_node_llm_params.get("enable_visual") and workflow_node_llm_params.get("visual_schema")):
        # 获取图片信息
        visual_schema = workflow_node_llm_params.get("visual_schema")
        attachment_list = load_properties(visual_schema.get('properties'), {
            task_record.workflow_node_code: {
                task_record.workflow_node_code: task_params}
        }).get("images", [])
        if attachment_list:
            attachment_id_list = [attachment.get("id") for attachment in attachment_list]
            app.logger.warning(f"visual_schema: {visual_schema.get('properties')}, task_params: {task_params}, "
                               f"attachment_id_list: {attachment_id_list}")
            image_list = []
            target_attachments = ResourceObjectMeta.query.filter(
                ResourceObjectMeta.id.in_(attachment_id_list),
                ResourceObjectMeta.resource_status == "正常"
            ).all()
            for resource in target_attachments:
                if resource.resource_type in ("image", "media") and resource.resource_download_url:
                    url = app.config.get("domain") + "/next_console/knowledge_center/resource_images?resource_id={}".format(resource.id)
                    if imgUrl == 'base64':
                        # 如果是base64编码的图片
                        try:
                            with open(resource.resource_path, "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                            url = "data:image/png;base64,{}".format(encoded_string)
                        except Exception as e:
                            app.logger.error(f"读取图片文件失败：{e}")
                            continue
                    image_list.append({
                        "type": "image_url",
                        "image_url": {
                            "url": url,
                            "detail": "auto"
                        }
                    })
            if image_list:
                lastMessage = messages[-1]
                lastMessage = {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": lastMessage.get("content")},
                    ]
                }
                lastMessage["content"].extend(image_list)
                messages[-1] = lastMessage
    # 文件阅读模式补充
    if (workflow_node_llm_params.get("support_file") and
            workflow_node_llm_params.get("enable_file") and workflow_node_llm_params.get("file_ref")):
        file_ref = workflow_node_llm_params.get("file_ref")
        llm_code = workflow_node_llm_params.get("llm_code")
        llm_api_secret_key = LLMInstance.query.filter(
            LLMInstance.llm_code == llm_code,
        ).first()
        if llm_api_secret_key:
            client = OpenAI(
                # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
                api_key=llm_api_secret_key.llm_api_secret_key,
                base_url=llm_api_secret_key.llm_base_url,
            )
            # 获取文件信息
            attachment_id_list = load_properties(
                {"file_ref": {"ref": file_ref}}, global_params
            ).get("file_ref", [])
            app.logger.info(f"file_ref: {file_ref}, attachment_id_list: {attachment_id_list}")
            if attachment_id_list:
                all_attachments = ResourceObjectMeta.query.filter(
                    ResourceObjectMeta.id.in_(attachment_id_list),
                    ResourceObjectMeta.resource_status == "正常"
                ).all()
                all_files_content = ""
                for attachment in all_attachments:
                    # test.txt 是一个本地示例文件
                    # 从redis缓存中获取file_id 没有再上传，无超时时间
                    redis_attachment_file_key = f"{llm_code}-fileid-{attachment.id}"
                    if redis_client.get(redis_attachment_file_key):
                        file_object = redis_client.get(redis_attachment_file_key)
                        app.logger.warning(f"复用文件缓存：{file_object}")
                        file_object_info = json.loads(file_object)
                    else:
                        file_object = client.files.create(file=Path(attachment.resource_path), purpose="file-extract")
                        file_object_info = json.loads(file_object.model_dump_json())
                        # 将文件信息存入redis缓存
                        redis_client.set(redis_attachment_file_key, json.dumps(file_object_info))
                    all_files_content += "fileid://{},".format(file_object_info.get("id"))
                all_files_content = all_files_content.strip(",")
                if all_files_content:
                    messages.insert(1, {'role': 'system', 'content': all_files_content})
    workflow_node_llm_params['messages'] = messages
    task_record.task_prompt = workflow_node_llm_params["messages"]
    db.session.add(task_record)
    db.session.commit()
    return workflow_node_llm_params


def add_reference_md(task_record, global_params):
    """
    添加参考文献元数据
        从入参中获取参考文献相关的元数据，并渲染成Markdown格式。
    :param task_record:
    :param global_params:
    :return:
    """
    ncOrders = task_record.workflow_node_ipjs.get('ncOrders', [])
    md_content = ''
    for attr in ncOrders:
        try:
            prop = task_record.workflow_node_ipjs.get('properties', {}).get(attr, {})
        except Exception as e:
            continue
        if prop.get('ref', {}).get("nodeType") == "rag":
            node_code = prop.get('ref', {}).get("nodeCode")
            node_results = global_params.get(node_code, {})
            if not node_results:
                continue
            all_source_resource_ids = []
            details = node_results.get("details", [])
            chunk_resource_map = {}
            for detail in details:
                if isinstance(detail, dict) and detail.get("chunk_id"):
                    resource_id = detail.get("meta",{}).get("source")
                    if resource_id:
                        all_source_resource_ids.append(resource_id)
                        chunk_resource_map[detail.get("chunk_id")] = resource_id
            all_source_resources = ResourceObjectMeta.query.filter(
                ResourceObjectMeta.id.in_(all_source_resource_ids),
                ResourceObjectMeta.resource_status == "正常"
            ).all()
            all_parent_resources_map = {res.id: res for res in all_source_resources}
            index = 1
            for detail in details:
                resource_id = detail.get("meta", {}).get("source")
                source_resource = all_parent_resources_map.get(resource_id)
                if not source_resource:
                    continue
                if source_resource.resource_type == "webpage":
                    md_content += f"\n\n[{index}]: {source_resource.resource_source_url}"
                elif source_resource.resource_type == "document":
                    md_content += f"\n\n[{index}]: {app.config['domain']}/#/next_console/resources/resource_viewer/{resource_id}"
                else:
                    md_content += f"\n\n[{index}]: {source_resource.resource_download_url}"
                index += 1
    return md_content

