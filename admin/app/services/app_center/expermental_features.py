import json
from datetime import datetime
from app.app import app, db
from app.models.next_console.next_console_model import NextConsoleMessage
from app.services.next_console.llm import NextConsoleLLMClient
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
        workflow_node_llm_params = load_llm_prams(new_sub_params, task_record, global_params)
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

