from app.services.app_center.node_params_service import render_template_with_params, load_properties
import json
from datetime import datetime
from app.app import db


def variable_cast_node_execute(task_params, task_record, global_param):
    """
    变量转换节点执行器
        1. 读取节点信息
        2. 组装转换参数
        3. 执行转换逻辑
        4. 处理返回结果
        5. 更新任务状态
    """
    if task_record.workflow_node_variable_cast_config.get("cast_type") == "string":
        return variable_to_string(task_params, task_record, global_param)
    elif task_record.workflow_node_variable_cast_config.get("cast_type") == "object":
        return variable_to_object(task_params, task_record, global_param)


def variable_to_string(task_params, task_record, global_param):
    """
    变量转换为字符串
    """
    new_strings = render_template_with_params(
        task_record.workflow_node_variable_cast_config.get("string_template", ""),
        task_params
    )
    task_record.task_result = json.dumps({
        "content": new_strings
    })
    task_record.task_status = "已完成"
    task_record.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.add(task_record)
    db.session.commit()
    return task_record.task_result


def variable_to_object(task_params, task_record, global_param):
    """
    变量转换为对象
    """
    new_object = load_properties(
        task_record.workflow_node_variable_cast_config.get("cast_schema", {}).get("properties", {}),
        {
            task_record.workflow_node_code: task_params
        }
    )
    task_record.task_result = json.dumps(new_object)
    task_record.task_status = "已完成"
    task_record.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.add(task_record)
    db.session.commit()
    return task_record.task_result

