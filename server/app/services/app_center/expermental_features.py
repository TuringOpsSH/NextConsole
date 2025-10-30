import json
from datetime import datetime
from app.app import app, db
from app.models.next_console.next_console_model import NextConsoleMessage
from app.services.configure_center.llm import NextConsoleLLMClient
from app.services.next_console.next_console import next_console_response
from concurrent.futures import wait


def parallel_llm_node_execute(params, task_record, global_params):
    """
    平行执行 LLM 节点
        [] 根据队列属性，进行一次循环，组装llm-parmam变量
        [] 全部执行完成后汇总
        [] 其余性质相同，不支持
    """
    from app.services.app_center.llm_node_service import load_llm_prams
    workflow_node_llm_params = load_llm_prams(params, task_record, global_params)
    llm_client = NextConsoleLLMClient(workflow_node_llm_params)
    if not llm_client.llm_client:
        app.logger.error(f"工作流发现此模型{task_record.workflow_node_llm_code}暂不支持")
        task_record.task_status = "异常"
        task_record.task_trace_log = f"工作流发现此模型{task_record.workflow_node_llm_code}暂不支持"
        db.session.add(task_record)
        db.session.commit()
        return next_console_response(error_status=True,
                                     error_message=f"此模型{task_record.workflow_node_llm_code}暂不支持")
    parallel_attr = task_record.workflow_node_run_model_config.get("parallel_attr", "")
    if not parallel_attr or not isinstance(params[parallel_attr], list):
        raise ValueError("parallel_attr must be a list of attributes to parallelize.")
    msg_content = ""
    reasoning_content = ""
    msg_token_used = 0
    sub_results = []
    for item in params[parallel_attr]:
        new_sub_params = {k: params[k] for k in params if k not in params[parallel_attr]}
        new_sub_params[parallel_attr] = [item]
        workflow_node_llm_params = load_llm_prams(new_sub_params, task_record, global_params, imgUrl='base64')
        future = global_params["executor"].submit(single_llm_sub_node_execute,
                                                  llm_client, workflow_node_llm_params,
                                                  task_record.to_dict(), global_params)
        # 添加回调确保子任务完成（可选）
        future.add_done_callback(
            lambda f: print(f"🎯agent_run_workflow:result: {f.result()}") if f.exception() is None
            else print(f"agent_run_workflow:❌error: {f.exception()}"))
        sub_results.append(future)
    # 等待所有子任务完成
    wait(sub_results)
    for future in sub_results:
        try:
            msg_content_part, reasoning_content_part, msg_token_used_part, answer_msg = future.result()
            msg_content += msg_content_part
            reasoning_content += reasoning_content_part
            msg_token_used += msg_token_used_part
        except Exception as e:
            app.logger.error(f"执行 LLM 子节点时发生异常：{str(e)}")
            msg_content += "\n\n **对不起，模型服务正忙，请稍等片刻后重试，或者可以试试切换其他模型~**"
    task_record.task_result = json.dumps({
        "content": msg_content,
        "reasoning_content": reasoning_content,
    })
    task_record.end_time = datetime.now()
    task_record.task_status = "已完成"
    task_record.task_token_used = msg_token_used
    db.session.add(task_record)
    db.session.commit()
    return True


def single_llm_sub_node_execute(llm_client, workflow_node_llm_params, task_record, global_params):
    """
    执行单个 LLM 子节点
    """
    with app.app_context():
        msg_content = ""
        reasoning_content = ""
        msg_token_used = 0
        answer_msg = None
        if workflow_node_llm_params.get("stream", False):
            all_message_format = [msg_schema.get("schema_type")
                                  for msg_schema in task_record.get("workflow_node_message_schema")]
            output_flag = task_record.get("workflow_node_enable_message") and global_params[
                "stream"] and 'messageFlow' in all_message_format
            if output_flag:
                answer_msg = NextConsoleMessage(
                    user_id=task_record.get("user_id"),
                    session_id=task_record.get("session_id"),
                    qa_id=task_record.get("qa_id"),
                    msg_format='messageFlow',
                    msg_llm_type=task_record.get("workflow_node_llm_code"),
                    msg_role="assistant",
                    msg_parent_id=task_record.get("msg_id"),
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
                    if hasattr(chunk, "usage") and chunk.usage and chunk.usage.total_tokens > 0:
                        msg_token_used = chunk.usage.total_tokens
                    if chunk.choices and (
                            chunk.choices[0].delta.content or hasattr(chunk.choices[0].delta, "reasoning_content")):
                        if hasattr(chunk.choices[0].delta, "reasoning_content") and chunk.choices[0].delta.reasoning_content:
                            reasoning_content += chunk.choices[0].delta.reasoning_content
                        elif chunk.choices[0].delta.content:
                            msg_content += chunk.choices[0].delta.content
                        if global_params["stream"] and output_flag:
                            chunk_res = chunk.model_dump_json()
                            chunk_res = json.loads(chunk_res)
                            chunk_res["session_id"] = task_record.get("session_id"),
                            chunk_res["qa_id"] = task_record.get("qa_id"),
                            chunk_res["msg_parent_id"] = task_record.get("msg_id"),
                            chunk_res["msg_id"] = answer_msg.msg_id
                            global_params["message_queue"].put(chunk_res)
            except GeneratorExit:
                pass
            except Exception as e3:
                app.logger.error(f"调用基模型异常：{str(e3)}")
                msg_content += "\n\n **对不起，模型服务正忙，请稍等片刻后重试，或者可以试试切换其他模型~**"
                if task_record.get("workflow_node_enable_message") and global_params["stream"]:
                    if task_record.get("workflow_node_message_schema_type") == "messageFlow":
                        except_result = {
                            "id": "",
                            "session_id": task_record.get("session_id"),
                            "qa_id": task_record.get("qa_id"),
                            "msg_parent_id": task_record.get("msg_id"),
                            "created": 0,
                            "model": '',
                            "object": "chat.completion",
                            "choices": [
                                {
                                    "finish_reason": "error",
                                    "index": 0,
                                    "delta": {
                                        "content": msg_content,
                                        "role": "assistant"
                                    },

                                }
                            ]
                        }
                        global_params["message_queue"].put(except_result)
            finally:
                if output_flag:
                    answer_msg.msg_content = msg_content
                    answer_msg.reasoning_content = reasoning_content
                    answer_msg.msg_token_used = msg_token_used
                    db.session.add(answer_msg)
                    db.session.commit()
            return msg_content, reasoning_content, msg_token_used, answer_msg
        else:
            # 非流式执行
            try:
                res = llm_client.chat(workflow_node_llm_params).model_dump_json()
                res = json.loads(res)
                msg_content = res.get("choices")[0].get("message").get("content")
                reasoning_content = res.get("choices")[0].get("reasoning_content", "")
                msg_token_used = res.get("usage", {}).get("total_tokens", 0)
            except Exception as e:
                msg_content = '对不起，模型服务正忙，请稍等片刻后重试，或者可以试试切换其他模型~'
            return msg_content, reasoning_content, msg_token_used, answer_msg


def parallel_rag_node_execute(params, task_record, global_params):
    # 获取节点信息
    from app.models.configure_center.system_config import SystemConfig
    parallel_attr = task_record.workflow_node_run_model_config.get("parallel_attr", "")
    if not parallel_attr or not isinstance(params[parallel_attr], list):
        raise ValueError("parallel_attr must be a list of attributes to parallelize.")
    system_tool_config = SystemConfig.query.filter(
        SystemConfig.config_key == "tools",
        SystemConfig.config_status == 1
    ).first()
    sub_results = []
    for item in params[parallel_attr]:
        new_sub_params = {k: params[k] for k in params if k not in params[parallel_attr]}
        new_sub_params[parallel_attr] = [item]
        future = global_params["executor"].submit(single_rag_node_execute, new_sub_params,
                                                  task_record.to_dict(), global_params,
                                                  system_tool_config.config_value.get("search_engine", {}))
        # 添加回调确保子任务完成（可选）
        future.add_done_callback(
            lambda f: print(f"🎯agent_run_workflow:result: {f.result()}") if f.exception() is None
            else print(f"agent_run_workflow:❌error: {f.exception()}"))
        sub_results.append(future)
    # 等待所有子任务完成
    wait(sub_results)
    final_result = {
        "details": [],
        'reference_texts': []
    }
    for future in sub_results:
        try:
            sub_rag_response = future.result()
            if sub_rag_response:
                details = sub_rag_response.get("details")
                reference_texts = sub_rag_response.get("reference_texts")
                final_result["details"] += details
                final_result["reference_texts"] += reference_texts
        except Exception as e:
            app.logger.error(f"执行 RAG 子节点时发生异常：{str(e)}")
            pass
    # 去重和限制逻辑
    if task_record.workflow_node_run_model_config.get("result_merge_model") == "set":
        tmp_results = []
        for item in final_result["reference_texts"]:
            if item not in tmp_results:
                tmp_results.append(item)
        final_result["reference_texts"] = tmp_results
    task_record.task_result = json.dumps(final_result)
    task_record.end_time = datetime.now()
    task_record.task_status = "已完成"
    db.session.add(task_record)
    db.session.commit()
    return True


def single_rag_node_execute(params, task_record, global_params, search_engine_config):
    with app.app_context():
        from app.services.app_center.node_params_service import render_template_with_params
        from app.services.app_center.app_run_service import get_all_resource_ref_ids
        from app.services.app_center.node_params_service import load_properties
        query = str(render_template_with_params(task_record.get("workflow_node_rag_query_template"), params))
        if not query:
            return
        # 获取知识ref
        all_resource_ids = []
        for resource in task_record.get("workflow_node_rag_resources"):
            if resource.get("id") == "message_attachments":
                if global_params.get("MessageAttachmentList"):
                    all_resource_ids.extend(
                        [attachment.id for attachment in global_params.get("MessageAttachmentList")])
            elif resource.get("id") == "session_attachments":
                if global_params.get("SessionAttachmentList"):
                    all_resource_ids.extend(
                        [attachment.id for attachment in global_params.get("SessionAttachmentList")])
            elif resource.get("type") == "param":
                params_ids = load_properties(resource.get("schema", {}).get("properties"), global_params)
                if params_ids.get('resource_list'):
                    for param_id in params_ids.get('resource_list'):
                        try:
                            param_id = int(param_id)
                        except Exception as e:
                            print(e)
                            continue
                        all_resource_ids.append(param_id)
                elif params_ids.get('resource_id'):
                    try:
                        params_id = int(params_ids.get('resource_id'))
                    except Exception as e:
                        print(e)
                        continue
                    all_resource_ids.append(params_id)
            else:
                all_resource_ids.append(resource.get("id"))
        all_resource_ids = list(set(all_resource_ids))
        all_ref_ids = get_all_resource_ref_ids(all_resource_ids, global_params)
        if not all_ref_ids and not task_record.get("workflow_node_rag_web_search_config").get("search_engine_enhanced"):
            return

        rag_params = {
            "user_id": task_record.get("user_id"),
            "session_id": task_record.get("session_id"),
            "msg_id": task_record.get("msg_id"),
            "task_id": task_record.get("id"),
            "query": query,
            "ref_ids": all_ref_ids,
            "config": {
                "recall_threshold": task_record.get("workflow_node_rag_recall_config").get("recall_threshold", 0.3),
                "recall_k": task_record.get("workflow_node_rag_recall_config").get("recall_k", 30),
                "recall_similarity": task_record.get("workflow_node_rag_recall_config").get(
                    "recall_similarity", "cosine"),
                "rerank_enabled": task_record.get("workflow_node_rag_rerank_config").get("rerank_enabled", True),
                "max_chunk_per_doc": task_record.get("workflow_node_rag_rerank_config").get("max_chunk_per_doc", 1024),
                "overlap_tokens": task_record.get("workflow_node_rag_rerank_config").get("overlap_tokens", 80),
                "rerank_threshold": task_record.get("workflow_node_rag_rerank_config").get("rerank_threshold", 0.3),
                "rerank_k": task_record.get("workflow_node_rag_rerank_config").get("rerank_k", 10),
                "search_engine_enhanced": task_record.get("workflow_node_rag_web_search_config").get(
                    "search_engine_enhanced", False),
                "search_engine_config": {
                    "api": search_engine_config.get("endpoint"),
                    "key": search_engine_config.get("key"),
                    "gl": "cn",
                    "hl": "zh-cn",
                    "location": "China",
                    "num": task_record.get("workflow_node_rag_web_search_config").get("num", 20),
                    "timeout": task_record.get("workflow_node_rag_web_search_config").get("timeout", 30),
                },
            }
        }
        from app.services.knowledge_center.rag_service_v3 import rag_query_v3
        rag_response = rag_query_v3(rag_params).json.get("result", {})
        return rag_response
