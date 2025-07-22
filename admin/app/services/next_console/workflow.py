from app.services.next_console.reference import *
from app.models.next_console.next_console_model import NextConsoleQa
from app.models.app_center.app_info_model import WorkFlowTaskInfo


def get_workflow_progress_batch(data):
    """
    批量获取工作流进度
    return= {
    qa_id :
      [
                {
                    task_name: number,
                    task_logs: string,
                    task_create_time: string,
                    task_finish_time: string,
                    task_status: string,
                }
            ]
       },
    """
    qa_ids = data.get("qa_ids")
    user_id = int(data.get("user_id"))
    qa_ids = NextConsoleQa.query.filter(
        NextConsoleQa.user_id == user_id,
        NextConsoleQa.qa_id.in_(qa_ids)
    ).all()
    qa_ids = {qa.qa_id for qa in qa_ids}
    data["qa_ids"] = qa_ids
    all_workflow_tasks = WorkFlowTaskInfo.query.filter(
        WorkFlowTaskInfo.user_id == user_id,
        WorkFlowTaskInfo.qa_id.in_(qa_ids),
        WorkFlowTaskInfo.task_type != "查询推荐"
    ).order_by(
        WorkFlowTaskInfo.qa_id,
        WorkFlowTaskInfo.create_time
    ).all()
    result = {}
    for workflow_task in all_workflow_tasks:
        qa_id = workflow_task.qa_id
        if qa_id not in result:
            result[qa_id] = []
        show_data = show_workflow_task_label(workflow_task.to_dict())
        result[qa_id].append(show_data)
    return next_console_response(result=result)


def show_workflow_task_label(workflow_task):
    """
    显示工作流任务标签
    """
    show_data = {
        "qa_id": workflow_task.get("qa_id"),
        "msg_id": workflow_task.get("msg_id"),
        "task_id": workflow_task.get("id"),
        "task_type": workflow_task.get("task_type"),
        "task_instruction": workflow_task.get("task_assistant_instruction"),
        "task_params": workflow_task.get("task_params"),
        "task_create_time": workflow_task.get("create_time"),
        "task_update_time": workflow_task.get("update_time"),
        "task_begin_time": workflow_task.get("begin_time"),
        "task_end_time": workflow_task.get("end_time"),
        "task_status": workflow_task.get("task_status"),
    }
    try:
        task_result = workflow_task.get("task_result", "").strip()
    except Exception as e:
        task_result = ""
    if workflow_task.get("task_type") == "资料检索":
        if len(task_result):
            show_data["task_label"] = f"共检索到{len(task_result)}字相关资料"
        else:
            show_data["task_label"] = '未检索到相关资料'
    elif workflow_task.get("task_type") == "意图理解":
        show_data["task_label"] = {
            "1": "报表问答",
            "2": "图表更新",
            "3": "数据查询",
            "4": "知识问答",
            "5": "其他问题",
        }.get(task_result, "")
    elif workflow_task.get("task_type") == "查询理解":
        if task_result.startswith("1"):
            show_data["task_label"] = task_result[2:-1]
        else:
            show_data["task_label"] = workflow_task.get("task_params").get("user_params", {}).get("message_text", "")
    elif workflow_task.get("task_type") in ("网页解析", "图像识别"):
        show_data["task_params"] = workflow_task.get("task_params")
    elif workflow_task.get("task_type") == "SQL查询":
        show_data["task_result"] = task_result
        show_data["task_label"] = workflow_task.get("task_params").get("user_params", {}).get("message_text", "")
    elif workflow_task.get("task_type") == "图表生成":
        show_data["task_result"] = task_result
        show_data["task_label"] = '配置成功'
    else:
        show_data["task_label"] = task_result
    return show_data
