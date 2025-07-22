import json
import time
from abc import ABC, abstractmethod

from flask import stream_with_context, Response
from openai import OpenAI
from app.models.resource_center.resource_model import ResourceObjectMeta
from app.app import app
from app.models.configure_center.llm_kernel import *
from app.services.next_console.base import *
from app.services.task_center.workflow import emit_workflow_status


# 定义抽象基类
class LLMClient(ABC):
    @abstractmethod
    def __init__(self, config):
        self.user_id = config.get('user_id')
        self.base_url = config.get('base_url')
        self.proxy_url = config.get('proxy_url')
        self.llm_name = config.get('llm_name')
        self.api_key = config.get('api_key')
        self.llm_client = None
        self.llm_code = config.get('llm_code')
        self.llm_config = None
        self.is_std_openai = False

    @abstractmethod
    def chat(self, config):
        pass

    def refresh(self):
        pass


class NextConsoleLLMClient(LLMClient):
    def __init__(self, config):
        super().__init__(config)
        self.fetch_llm_instance()

    def fetch_llm_instance(self):
        llm_config = LLMInstance.query.filter(
            LLMInstance.llm_code == self.llm_code,
        ).first()
        if not llm_config:
            return False
        self.llm_config = llm_config
        self.llm_name = llm_config.llm_name
        if llm_config.is_std_openai:
            self.init_openai_instance()
        else:
            return None

    def init_openai_instance(self):
        """
            初始化openai实例
            :return:
            """
        if self.llm_config.llm_is_proxy:
            self.llm_client = OpenAI(
                api_key=self.llm_config.llm_api_secret_key,
                base_url=self.llm_config.llm_proxy_url
            )
        else:
            self.llm_client = OpenAI(
                api_key=self.llm_config.llm_api_secret_key,
                base_url=self.llm_config.llm_base_url
            )
        self.is_std_openai = True

    def init_ernie_instance(self):
        """
        初始化百度文心一言实例
        :return:
        """
        pass

    def chat(self, config):
        if self.is_std_openai:
            if config.get("stream") is True:
                if not config.get("use_default"):
                    return self.llm_client.chat.completions.create(
                        model=self.llm_name,
                        messages=config.get("messages"),
                        stream=config.get("stream"),
                        stream_options={"include_usage": True} if config.get("stream") else None,
                        response_format=config.get("response_format"),
                        max_tokens=config.get("max_tokens"),
                        frequency_penalty=config.get("frequency_penalty", 0),
                        presence_penalty=config.get("presence_penalty", 0),
                        temperature=config.get("temperature", 1),
                        top_p=config.get("top_p", 1),
                        stop=config.get("stop"),
                        extra_body=config.get("extra_body", {})
                    )
                else:
                    return self.llm_client.chat.completions.create(
                        model=self.llm_name,
                        messages=config.get("messages"),
                        stream=config.get("stream"),
                        stream_options={"include_usage": True} if config.get("stream") else None,
                        response_format=config.get("response_format"),
                        stop=config.get("stop"),
                        extra_body=config.get("extra_body", {})
                    )
            else:
                if not config.get("use_default"):
                    return self.llm_client.chat.completions.create(
                        model=self.llm_name,
                        messages=config.get("messages"),
                        stream=config.get("stream"),
                        response_format=config.get("response_format"),
                        max_tokens=config.get("max_tokens"),
                        frequency_penalty=config.get("frequency_penalty", 0),
                        presence_penalty=config.get("presence_penalty", 0),
                        temperature=config.get("temperature", 1),
                        top_p=config.get("top_p", 1),
                        stop=config.get("stop"),
                        extra_body=config.get("extra_body", {})
                    )
                else:
                    return self.llm_client.chat.completions.create(
                        model=self.llm_name,
                        messages=config.get("messages"),
                        stream=config.get("stream"),
                        response_format=config.get("response_format"),
                        stop=config.get("stop"),
                        extra_body=config.get("extra_body", {})
                    )
        elif self.llm_name.startswith("ERNIE-"):
            return self.llm_client.chat.completions.create
        else:
            return None

    def refresh(self):
        self.fetch_llm_instance()


def llm_chat(params):
    """
    访问聊天机器人接口
        model：模型名称
        messages：消息列表
        stream：是否流式
        response_format：返回格式
        n：返回条数
    return:
        n_messages
        token_used
        time_used
    """
    user_id = int(params.get("user_id"))
    messages = params.get("messages", [])
    model = params.get("model", "deepseek-chat")
    session_llm_code = params.get("session_llm_code")
    stream = params.get("stream", True)
    response_format_option = params.get("response_format", "text")
    if response_format_option == "json_object":
        response_format = {"type": "json_object"}
    else:
        response_format = {"type": "text"}
    msg_version = params.get("msg_version", 0)
    session_id = params.get("session_id")
    qa_id = params.get("qa_id")
    msg_parent_id = params.get("msg_parent_id")
    assistant_id = params.get("assistant_id")
    llm_instance_params = {
        "llm_code": session_llm_code,
        "user_id": user_id,
    }
    llm_client = NextConsoleLLMClient(llm_instance_params)
    if not llm_client.llm_client:
        app.logger.error(f"此模型{model}暂不支持")
        return next_console_response(error_status=True, error_message=f"此模型{model}暂不支持")
    temperature = params.get("temperature", 0.7)
    max_tokens = params.get("max_tokens", None)
    # 新增回答消息
    answer_params = {
        "user_id": user_id,
        "session_id": session_id,
        "qa_id": qa_id,
        "assistant_id": assistant_id,
        "msg_llm_type": llm_client.llm_name,
        "msg_prompt": messages,
        "msg_role": "assistant",
        "msg_format": "text",
        "msg_content": "",
        "msg_token_used": 0,
        "msg_time_used": 0,
        "msg_version": msg_version,
        "msg_parent_id": msg_parent_id,
    }
    answer = add_messages(answer_params).json.get("result")
    if stream:
        # 同步流式请求
        return Response(
            stream_with_context(generate(
                user_id=user_id,
                session_id=session_id,
                qa_id=qa_id,
                msg_parent_id=msg_parent_id,
                msg_id=answer.get("msg_id"),
                assistant_id=assistant_id,
                llm_client=llm_client,
                messages=messages,
                stream=stream,
                response_format=response_format,
                temperature=temperature,
                max_tokens=max_tokens,
                create_time=answer.get("create_time"),
            ))
            , mimetype="text/event-stream")
    else:
        # 同步请求
        begin_time = time.time()
        chat_params = {
            "messages": messages,
            "stream": stream,
            "response_format": response_format,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        res = llm_client.chat(chat_params).model_dump_json()
        end_time = time.time()
        res = json.loads(res)
        msg = res.get("choices")[0].get("message")
        try:
            msg_token_used = res.get("usage").get("total_tokens")
        except Exception as e:
            msg_token_used = 0
        # 更新回答消息
        answer_params = {
            "user_id": user_id,
            "session_id": session_id,
            "msg_id": answer.get("msg_id"),
            "msg_content": msg.get("content"),
            "msg_token_used": msg_token_used,
            "msg_time_used": end_time - begin_time,
        }
        res = update_messages(answer_params)
        # 更新session状态
        target_session = NextConsoleSession.query.filter(
            NextConsoleSession.id == session_id,
        ).first()
        target_session.assistant_id = assistant_id
        target_session.update_time = func.now()
        db.session.add(target_session)
        db.session.commit()
        return res


def workflow_chat(params):
    """
    工作流内置聊天
    :param params:
    :return:
    """
    model = params.get("model", "deepseek-chat")
    session_llm_code = params.get("session_llm_code")
    messages = params.get("messages", [])
    stream = params.get("stream", False)
    new_task = params.get("new_task")
    response_format_option = params.get("response_format", "text")
    user_id = int(params.get("user_id"))
    if response_format_option == "json_object":
        response_format = {"type": "json_object"}
    else:
        response_format = {"type": "text"}

    llm_instance_params = {
        "llm_code": session_llm_code,
        "user_id": -1,
    }
    llm_client = NextConsoleLLMClient(llm_instance_params)
    if not llm_client.llm_client:
        app.logger.error(f"工作流发现此模型{model}，{session_llm_code}暂不支持")
        return next_console_response(error_status=True, error_message=f"此模型{model}暂不支持")
    temperature = params.get("temperature", 0)
    max_tokens = params.get("max_tokens", None)
    if stream:
        # 同步流式请求
        return Response(
            stream_with_context(workflow_generate(
                user_id=user_id,
                new_task=new_task,
                llm_client=llm_client,
                messages=messages,
                stream=stream,
                response_format=response_format,
                temperature=temperature,
                max_tokens=max_tokens,
            ))
            , mimetype="text/event-stream")
    else:
        # 同步请求
        chat_params = {
            "messages": messages,
            "stream": stream,
            "response_format": response_format,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        try:
            res = llm_client.chat(chat_params).model_dump_json()
            res = json.loads(res)
            msg = res.get("choices")[0].get("message").get("content")
            if new_task:
                new_task.task_status = "finished"
                new_task.task_result = msg
                new_task.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db.session.add(new_task)
                db.session.flush()
                db.session.commit()
                emit_workflow_status.delay({
                    "user_id": user_id,
                    "new_task": new_task.to_dict()
                })
            return msg
        except Exception as e:
            app.logger.error(f"workflow_chat error: {e}")
            return "对不起，模型服务正忙，请稍等片刻后重试，或者可以试试切换其他模型~"


def generate(user_id, session_id, qa_id, msg_parent_id, msg_id, assistant_id,
             llm_client, messages, stream, response_format, temperature=0,
             max_tokens=None, create_time=None):
    begin_time = time.time()
    reasoning_content = ""
    msg_content = ""
    msg_token_used = 0
    msg_is_cut_off = False
    stream_chat_params = {
        "messages": messages,
        "stream": stream,
        "response_format": response_format,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    try:
        completion = llm_client.chat(stream_chat_params)
        for chunk in completion:
            if hasattr(chunk, "usage") and chunk.usage and chunk.usage.total_tokens > 0:
                msg_token_used = chunk.usage.total_tokens
            if chunk.choices and (
                    chunk.choices[0].delta.content or hasattr(chunk.choices[0].delta, "reasoning_content")):
                if hasattr(chunk.choices[0].delta, "reasoning_content"):
                    reasoning_content += chunk.choices[0].delta.reasoning_content
                else:
                    msg_content += chunk.choices[0].delta.content
                chunk_res = chunk.model_dump_json()
                chunk_res = json.loads(chunk_res)
                chunk_res["session_id"] = session_id
                chunk_res["qa_id"] = qa_id
                chunk_res["msg_parent_id"] = msg_parent_id
                chunk_res["msg_id"] = msg_id
                chunk_res["create_time"] = create_time
                chunk_res = json.dumps(chunk_res)
                yield f'data: {chunk_res}\n\n'
    except GeneratorExit:
        msg_is_cut_off = True
    except Exception as e3:
        raw_log = str(e3).lower()
        trace_log = "\n\n **对不起，模型服务正忙，请稍等片刻后重试，或者可以试试切换其他模型~**"
        trace_mark = False
        if "exceeds the maximum length" in raw_log:
            trace_log = "\n\n **您的问题太长了，暂时无法回答~**"
            trace_mark = True
        app.logger.error(f"调用基模型异常：{raw_log}, 消息id: {msg_parent_id}, 是否翻译: {trace_mark}")
        msg_content += trace_log
        except_result = {
            "id": "",
            "session_id": session_id,
            "qa_id": qa_id,
            "msg_parent_id": msg_id,
            "msg_id": msg_id,
            "created": 0,
            "model": '',
            "object": "chat.completion",
            "choices": [
                {
                    "finish_reason": "error",
                    "index": 0,
                    "message": {
                        "content": msg_content,
                        "role": "assistant"
                    },

                }
            ]
        }
        except_result = json.dumps(except_result)
        yield f'data: {except_result}\n\n'
    finally:
        end_time = time.time()
        # 更新回答消息
        answer_params = {
            "user_id": user_id,
            "session_id": session_id,
            "msg_id": msg_id,
            "msg_content": msg_content,
            "msg_token_used": msg_token_used,
            "msg_time_used": end_time - begin_time,
            "msg_is_cut_off": msg_is_cut_off,
            "reasoning_content": reasoning_content,
        }
        if "对不起，模型服务正忙，请稍等片刻后重试，或者可以试试切换其他模型~" in msg_content:
            answer_params["msg_is_cut_off"] = True
        update_messages(answer_params)
        # 更新session状态
        target_session = NextConsoleSession.query.filter(
            NextConsoleSession.id == session_id,
        ).first()
        target_session.assistant_id = assistant_id
        target_session.update_time = func.now()
        db.session.add(target_session)
        db.session.commit()
        yield 'data: [DONE]\n\n'


def workflow_generate(user_id, new_task, llm_client, messages, stream, response_format,
                      temperature=0, max_tokens=None):
    msg_content = ""
    stream_chat_params = {
        "messages": messages,
        "stream": stream,
        "response_format": response_format,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    try:
        completion = llm_client.chat(stream_chat_params)
        for chunk in completion:
            if chunk.choices[0].delta.content:
                msg_content += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content
    except Exception as e:
        app.logger.error(f"调用基模型异常：{str(e)}")
        # 换license重试
        llm_client.refresh()
        try:
            completion = llm_client.chat(stream_chat_params)
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    msg_content += chunk.choices[0].delta.content
                    yield chunk.choices[0].delta.content
        except Exception as e:
            app.logger.error(f"调用基模型异常：{str(e)}")
            yield "对不起，模型服务正忙，请稍等片刻后重试~"
    finally:
        # 更新任务状态
        if new_task:
            new_task.task_status = "finished"
            new_task.task_result = msg_content
            new_task.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.add(new_task)
            db.session.flush()
            db.session.commit()
            emit_workflow_status.delay({
                "user_id": user_id,
                "new_task": new_task.to_dict()
            })

