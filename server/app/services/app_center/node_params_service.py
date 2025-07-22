import json

from bs4 import BeautifulSoup
from jinja2 import Template
from jsonschema import validate

from app.app import db


def check_task_precondition(task_record):
    """
    依次判断前置条件是否满足
        如果存在必要条件，则需要都为已完成
        如果存在充分条件，则可以执行
    """
    precondition = task_record.task_precondition
    if not precondition:
        return True
    ready_flag = False
    necessary_all_cnt = 0
    necessary_finish_cnt = 0
    # 充分条件
    for i in precondition:
        if i.get("type") == "必要":
            necessary_all_cnt += 1
            if i.get("status") == "已完成":
                necessary_finish_cnt += 1
        if i.get("status") == "已完成" and i.get("type") == "充分":
            ready_flag = True
    if ready_flag:
        return True
    if necessary_all_cnt == necessary_finish_cnt:
        return True


def load_task_params(task_record, global_params, model="input"):
    """
    加载入参
    """
    # 加载入参
    if model == "input":
        properties = task_record.workflow_node_ipjs.get("properties", {})
    elif model == "output":
        properties = task_record.workflow_node_rpjs.get("properties", {})
    else:
        properties = {}
    task_params = load_properties(properties, global_params)
    return task_params


def load_task_result(task_record):
    """
    解析任务结果
    """
    exec_result = task_record.task_result.strip()
    if task_record.workflow_node_result_format == "json" and exec_result:
        if exec_result.startswith("```json"):
            exec_result = exec_result.lstrip("```json").rstrip("```")
        try:
            exec_result = json.loads(exec_result)
        except Exception as e:
            task_record.task_trace_log = str(e)
            db.session.add(task_record)
            db.session.commit()
            return
        if "content" in exec_result:
            content = exec_result["content"]
            if isinstance(content, str) and task_record.workflow_node_llm_params.get("response_format") == "json":
                # 如果是字符串，则尝试解析为JSON
                try:
                    content = content.lstrip("```json").rstrip("```")
                    exec_result["content"] = json.loads(content)
                except json.JSONDecodeError:
                    pass
        try:
            if task_record.workflow_node_rpjs:
                validate(exec_result, task_record.workflow_node_rpjs)
        except Exception as e:
            task_record.task_trace_log = str(e)
            db.session.add(task_record)
            db.session.commit()
            return
    else:
        # 渲染结果
        exec_result = {
            'OUTPUT': exec_result
        }
    return exec_result


def render_template_with_params(template, params):
    """
    渲染模板参数
    template 为 html字符串，需要依次提取innertext，用户输入部分作为原始文本，系统参数作为模板变量
    :param template: 模板字符串
    :param params: 参数字典
    :return: 渲染后的字符串
    """
    soup = BeautifulSoup(template, 'html.parser')
    result = []
    current_raw_section = []

    for element in soup.descendants:
        if element.name == 'div' and 'dy-variable' in element.get('class', []):
            # 结束当前原始文本部分（如果有）
            if current_raw_section:
                result.append("{% raw %}" + "".join(current_raw_section) + "{% endraw %}")
                current_raw_section = []

            # 处理变量部分
            strong_tag = element.find('strong')
            if strong_tag:
                result.append(f"{{{{{strong_tag.text}}}}}")
        elif isinstance(element, str):
            skip = False
            for parent in element.parents:
                if parent.name == 'div' and 'dy-variable' in parent.get('class', []) and parent.get(
                        'contenteditable') == 'false':
                    skip = True
            if not skip:
                current_raw_section.append(element)

    # 添加最后剩余的原始文本部分
    if current_raw_section:
        result.append("{% raw %}" + "".join(current_raw_section) + "{% endraw %}")

    new_template = ''.join(result)
    try:
        template = Template(new_template)
        return template.render(params)
    except Exception as e:
        return new_template  # 返回未渲染的模板作为回退


def check_edge_conditions(edge_config, global_params):
    """
    计算边上条件是否成立
    :return:
    """
    condition_type = edge_config.get("condition_type", "or")
    conditions = edge_config.get("conditions", [])
    if condition_type == "or":
        edge_condition_result = False
    else:
        edge_condition_result = True
    if not conditions:
        return True
    for condition in conditions:
        sub_result = False
        src_node = condition.get("src_node")
        if src_node and not isinstance(src_node, (str, int, float)):
            src_node = load_properties({
                'src_node': {
                    'ref': src_node
                }
            }, global_params).get("src_node")
        tgt_node = condition.get("tgt_node")
        if tgt_node and not isinstance(tgt_node, (str, int, float)):
            tgt_node = load_properties({
                'tgt_node': {
                    'ref': tgt_node
                }
            }, global_params).get("tgt_node")
        # 计算条件
        operator = condition.get("operator")
        try:
            if operator == "==":
                sub_result = src_node == tgt_node
            elif operator == "!=":
                sub_result = src_node != tgt_node
            elif operator == ">":
                sub_result = src_node > tgt_node
            elif operator == "<":
                sub_result = src_node < tgt_node
            elif operator == ">=":
                sub_result = src_node >= tgt_node
            elif operator == "<=":
                sub_result = src_node <= tgt_node
            elif operator == "in":
                sub_result = src_node in tgt_node
            elif operator == "not in":
                sub_result = src_node not in tgt_node
            elif operator == "is null":
                if not src_node:
                    sub_result = True
                else:
                    sub_result = False
            elif operator == "not null":
                if src_node:
                    sub_result = True
                else:
                    sub_result = False
        except Exception as e:
            #print("条件计算异常", e)
            sub_result = False
        if condition_type == "or":
            if sub_result:
                edge_condition_result = True
                break
        elif condition_type == "and":
            if not sub_result:
                edge_condition_result = False
                break
    #print("条件校验结果", edge_condition_result)
    return edge_condition_result


def load_properties(properties, global_params):
    """
    从全局变量中加载出所有的变量
    :return:
    """
    data = {}
    try:
        for k in properties:
            ref = properties.get(k).get("ref")
            # 固定值
            if properties.get(k).get("value"):
                data[k] = properties.get(k).get("value")
                continue
            elif ref:
                # 固定值
                if isinstance(ref, (str, int)):
                    if properties.get(k).get("type") == "boolean":
                        if ref == 'false':
                            ref = False
                        elif ref == 'true':
                            ref = True
                    data[k] = ref
                    continue
                node_code = ref.get("nodeCode")
                target_params = global_params.get(node_code, '')
                if target_params:
                    node_path = ref.get("refAttrPath").split('.')
                    find_flag = False
                    for sub_k in node_path:
                        if sub_k in target_params:
                            target_params = target_params.get(sub_k)
                            find_flag = True
                        elif isinstance(target_params, list):
                            target_params = [item.get(sub_k, '') for item in target_params if isinstance(item, dict)]
                            find_flag = True
                    if not find_flag:
                        target_params = ''
                data[k] = target_params
            else:
                data[k] = global_params.get(k, '')
        return data
    except Exception as e:
        return data
