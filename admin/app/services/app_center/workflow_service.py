import os.path
from sqlalchemy import or_
from app.models.app_center.app_info_model import *
from app.services.app_center.app_manage_service import check_has_role
import uuid
import json
from app.utils.oss.oss_client import *
from datetime import datetime
from app.models.user_center.user_info import UserInfo


def create_workflow(params):
    """
    新建工作流
        平台管理员和应用作者
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    app_code = params.get("app_code")
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    workflow_name = params.get("workflow_name")
    workflow_desc = params.get("workflow_desc", '')
    workflow_icon = params.get("workflow_icon", 'images/workflow.svg')
    workflow_is_main = params.get("workflow_is_main", False)
    workflow_code = str(uuid.uuid4())
    workflow_info = WorkFlowMetaInfo(
        user_id=user_id,
        workflow_code=workflow_code,
        workflow_name=workflow_name,
        workflow_desc=workflow_desc,
        workflow_icon=workflow_icon,
        workflow_is_main=workflow_is_main,
    )
    db.session.add(workflow_info)
    db.session.commit()

    new_relation = AppWorkFlowRelation(
        workflow_code=workflow_code,
        app_code=app_code,
        rel_type='使用',
        rel_desc='创建',
    )
    db.session.add(new_relation)
    db.session.commit()
    return next_console_response(result=workflow_info.to_dict())


def upload_workflow_icon(user_id, flow_icon_data):
    """
    上传应用图标
    :param user_id:
    :param flow_icon_data: 文件数据
    :return:
    """
    suffix = flow_icon_data.filename.split(".")[-1]
    avatar_path = generate_new_path("app_center",
                                    user_id=user_id, file_type="file", suffix=suffix
                                    ).json.get("result")
    flow_icon_data.save(avatar_path)
    flow_icon = generate_download_url(
        "app_center",
        avatar_path, suffix=suffix).json.get("result")
    return next_console_response(result={
        "workflow_icon": flow_icon,
    })


def delete_app_flow(params):
    """
    删除应用流程
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    flow_code = params.get("workflow_code")
    user_id = int(params.get("user_id"))
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    target_flow = WorkFlowMetaInfo.query.filter(
        WorkFlowMetaInfo.workflow_code == flow_code,
        WorkFlowMetaInfo.workflow_status != "已删除",
        WorkFlowMetaInfo.environment == '开发'
    ).first()
    if not target_flow:
        return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)
    target_flow.workflow_status = '已删除'
    db.session.add(target_flow)
    db.session.commit()
    target_relation = AppWorkFlowRelation.query.filter_by(workflow_code=flow_code).first()
    target_relation.rel_status = '已删除'
    db.session.add(target_relation)
    db.session.commit()

    return next_console_response()


def update_app_flow(params):
    """
    更新应用工作流
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    flow_code = params.get("workflow_code")
    flow_name = params.get("workflow_name")
    flow_desc = params.get("workflow_desc")
    flow_icon = params.get("workflow_icon")
    flow_schema = params.get("workflow_schema")
    workflow_edit_schema = params.get("workflow_edit_schema")
    flow_is_main = params.get("workflow_is_main")
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    target_flow = WorkFlowMetaInfo.query.filter(
        WorkFlowMetaInfo.workflow_code == flow_code,
        WorkFlowMetaInfo.workflow_status != "已删除",
        WorkFlowMetaInfo.environment == '开发'
    ).first()
    if not target_flow:
        return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != "已删除",
        AppMetaInfo.environment == '开发'
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and target_app.user_id != user_id:
        app_user = UserInfo.query.filter(
            UserInfo.user_id == target_app.user_id
        ).first()
        current_user = UserInfo.query.filter(
            UserInfo.user_id == user_id
        ).first()
        if not app_user or not current_user:
            return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
        if app_user.user_company_id != current_user.user_company_id:
            return next_console_response(error_status=True, error_message="没有权限查看该应用！", error_code=1002)
    if flow_name is not None:
        target_flow.workflow_name = flow_name
    if flow_desc is not None:
        target_flow.workflow_desc = flow_desc
    if flow_icon is not None:
        target_flow.workflow_icon = flow_icon
    if flow_schema is not None:
        target_flow.workflow_schema = flow_schema
    if workflow_edit_schema is not None:
        target_flow.workflow_edit_schema = workflow_edit_schema
    if flow_is_main is True and app_code:
        old_main_flow = AppWorkFlowRelation.query.filter(
            AppWorkFlowRelation.app_code == app_code,
            AppWorkFlowRelation.workflow_code != flow_code,
            AppWorkFlowRelation.rel_status != '已删除',
            AppWorkFlowRelation.environment == '开发'
        ).join(
            WorkFlowMetaInfo,
            WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
        ).filter(
            WorkFlowMetaInfo.workflow_status != '已删除',
            WorkFlowMetaInfo.environment == '开发',
            WorkFlowMetaInfo.workflow_is_main == True
        ).with_entities(
            WorkFlowMetaInfo
        ).order_by(
            WorkFlowMetaInfo.version.desc()
        ).first()
        if old_main_flow:
            old_main_flow.workflow_is_main = False
            db.session.add(old_main_flow)
            db.session.commit()
        target_flow.workflow_is_main = True
    db.session.add(target_flow)
    db.session.commit()
    return next_console_response(result=target_flow.to_dict())


def get_app_flow_detail(params):
    """
    获取应用代理详情
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    app_code = params.get("app_code")
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    flow_code = params.get("workflow_code")
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != '已删除',
        AppMetaInfo.environment == '开发'
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)

    target_flow = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.workflow_code == flow_code,
        AppWorkFlowRelation.app_code == app_code,
        AppWorkFlowRelation.rel_status != '已删除'
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        WorkFlowMetaInfo.workflow_status != '已删除',
        WorkFlowMetaInfo.environment == '开发'
    ).with_entities(
        WorkFlowMetaInfo
    ).first()
    if target_flow:
        return next_console_response(result={
            "workflow_code": target_flow.workflow_code,
            "workflow_name": target_flow.workflow_name,
            "workflow_desc": target_flow.workflow_desc,
            "workflow_icon": target_flow.workflow_icon,
            "workflow_schema": target_flow.workflow_schema,
            "workflow_edit_schema": target_flow.workflow_edit_schema,
            "workflow_is_main": target_flow.workflow_is_main,
            "id": target_flow.id
        })
    return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)


def restore_app_flow_schema(params):
    """
    回滚至上一版本的schema
        完全一致，返回
        不同：
            修改节点数据
            覆写schema
    workflow_edit_schema , workflow_schema 均为json-str
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    workflow_code = params.get("workflow_code")
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    target_workflow = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.workflow_code == workflow_code,
        AppWorkFlowRelation.app_code == app_code,
        AppWorkFlowRelation.rel_status != '已删除'
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        WorkFlowMetaInfo.workflow_status != '已删除',
        WorkFlowMetaInfo.environment == '开发'
    ).with_entities(
        WorkFlowMetaInfo
    ).first()
    if not target_workflow:
        return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)
    if target_workflow.workflow_schema == target_workflow.workflow_edit_schema and target_workflow.workflow_schema:
        return next_console_response(error_message="该工作流没有变化！", error_code=1002)
    target_workflow.workflow_edit_schema = target_workflow.workflow_schema
    db.session.add(target_workflow)
    db.session.commit()
    return next_console_response(result=target_workflow.to_dict())


def check_app_flow_schema(params):
    """
    检查工作流schema是否符合规范
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    workflow_code = params.get("workflow_code")
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    target_workflow = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.workflow_code == workflow_code,
        AppWorkFlowRelation.app_code == app_code,
        AppWorkFlowRelation.rel_status != '已删除'
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        WorkFlowMetaInfo.workflow_status != '已删除',
        WorkFlowMetaInfo.environment == '开发'
    ).with_entities(
        WorkFlowMetaInfo
    ).first()
    if not target_workflow:
        return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)
    if not target_workflow.workflow_schema:
        return next_console_response(error_status=True, error_message="工作流schema不存在！", error_code=1002)
    # 所有节点
    all_nodes = WorkflowNodeInfo.query.filter(
        WorkflowNodeInfo.workflow_id == target_workflow.id,
        WorkflowNodeInfo.node_status != '已删除',
        WorkflowNodeInfo.environment == '开发'
    ).all()
    if not all_nodes:
        return next_console_response(error_status=True, error_message="工作流没有节点！", error_code=1002)
    all_check_info = []

    has_message_config = False
    global_params = load_all_global_params(all_nodes)
    for target_node in all_nodes:
        # rule4 检查节点必要参数
        if target_node.node_type == "llm":
            if not target_node.node_llm_code:
                all_check_info.append({
                    "id": f'alter-模型配置{target_node.id}',
                    'title': f'工作流{target_workflow.workflow_name}-节点{target_node.node_name}:未配置模型类型',
                    'type': 'error'
                })
            if not target_node.node_llm_system_prompt_template:
                all_check_info.append({
                    "id": f'alter-模型配置{target_node.id}',
                    'title': f'工作流{target_workflow.workflow_name}-节点{target_node.node_name}:未配置系统提示词',
                    'type': 'error'
                })
            if not target_node.node_llm_user_prompt_template:
                all_check_info.append({
                    "id": f'alter-模型配置{target_node.id}',
                    'title': f'工作流{target_workflow.workflow_name}-节点{target_node.node_name}:未配置用户提示语',
                    'type': 'error'
                })
        if target_node.node_type == "rag":
            if not target_node.node_rag_query_template:
                all_check_info.append({
                    "id": f'alter-rag配置{target_node.id}',
                    'title': f'工作流{target_workflow.workflow_name}-节点{target_node.node_name}:未配置查询语句',
                    'type': 'error'
                })
        if target_node.node_type == 'tool':
            if not target_node.node_tool_api_url:
                all_check_info.append({
                    "id": f'alter-工具配置{target_node.id}',
                    'title': f'工作流{target_workflow.workflow_name}-节点{target_node.node_name}:未配置url',
                    'type': 'error'
                })
        # rule6 检查节点输入参数
        if isinstance(target_node.node_input_params_json_schema, dict):
            # 值为空
            for attr in target_node.node_input_params_json_schema["properties"]:
                attr_define = target_node.node_input_params_json_schema["properties"][attr]
                if attr_define and not attr_define.get("ref") and not attr_define.get("value"):
                    all_check_info.append({
                        "id": f'alter-输入参数{target_node.id}',
                        'title': f'工作流{target_workflow.workflow_name}-节点{target_node.node_name}:输入参数{attr}配置异常',
                        'type': 'error'
                    })
        all_check_info.extend(check_input_ref_params(target_workflow, target_node, global_params))
        if target_node.node_enable_message:
            has_message_config = True
            # rule7 检查节点消息参数
            all_check_info.extend(check_message_ref_params(target_workflow, target_node, global_params))
    # rule5 是否存在消息配置
    if not has_message_config:
        all_check_info.append({
            "id": 'alter-消息配置',
            'title': f'工作流{target_workflow.workflow_name}:未配置任何节点输出消息',
            'type': 'info'
        })
    return next_console_response(result=all_check_info)


def export_app_flow_schema(params):
    """
    导出选中工作流的schema
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    workflow_code = params.get("workflow_code")
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    target_workflow = AppWorkFlowRelation.query.filter(
        AppWorkFlowRelation.workflow_code == workflow_code,
        AppWorkFlowRelation.app_code == app_code,
        AppWorkFlowRelation.rel_status != '已删除'
    ).join(
        WorkFlowMetaInfo,
        WorkFlowMetaInfo.workflow_code == AppWorkFlowRelation.workflow_code
    ).filter(
        WorkFlowMetaInfo.workflow_status != '已删除',
        WorkFlowMetaInfo.environment == '开发'
    ).with_entities(
        WorkFlowMetaInfo
    ).first()
    if not target_workflow:
        return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)
    if not target_workflow.workflow_schema:
        return next_console_response(error_status=True, error_message="工作流schema不存在！", error_code=1002)
    target_workflow_nodes = WorkflowNodeInfo.query.filter(
        WorkflowNodeInfo.workflow_id == target_workflow.id,
        WorkflowNodeInfo.node_status == '正常',
        WorkflowNodeInfo.environment == '开发'
    ).all()
    return next_console_response(result={
        "workflows": [target_workflow.to_dict()],
        "workflow_nodes": [workflow_node.to_dict() for workflow_node in target_workflow_nodes],
        "meta": {
            "export_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
    })


def load_all_global_params(all_target_nodes):
    start_node = [node for node in all_target_nodes if node.node_type == 'start'][0]
    global_params = {
        start_node.node_code: {
            "USER_INPUT": "fake",
            "session_id": 1,
            "SessionAttachmentList": [{"id": 1, "name": "fake_session_attachment.txt", "format": "txt", "size": 1024}],
            "MessageAttachmentList": [{"id": 1, "name": "fake_session_attachment.txt", "format": "txt", "size": 1024}],
            "current_time": "2023-10-01T00:00:00Z"
        }
    }
    for target_node in all_target_nodes:
        properties = target_node.node_result_params_json_schema.get("properties", {})
        fake_result = generate_fake_result(properties)
        global_params[target_node.node_code] = fake_result
    return global_params


def generate_fake_result(properties):
    fake_result = {}
    for attr in properties:
        if properties[attr].get("type") == "string":
            fake_result[attr] = f"fake_{attr}"
        elif properties[attr].get("type") == "number":
            fake_result[attr] = 1
        elif properties[attr].get("type") == "integer":
            fake_result[attr] = 1
        elif properties[attr].get("type") == "null":
            fake_result[attr] = None
        elif properties[attr].get("type") == "boolean":
            fake_result[attr] = True
        elif properties[attr].get("type") == "object":
            fake_result[attr] = generate_fake_result(properties[attr].get("properties", {}))
        elif properties[attr].get("type") == "array":
            item_type = properties[attr].get("items", {}).get("type")
            if item_type == "string":
                fake_result[attr] = ["fake_item"]
            elif item_type == "number":
                fake_result[attr] = [1]
            elif item_type == "object":
                fake_result[attr] = [generate_fake_result(properties[attr].get("items", {}).get("properties", {}))]
            else:
                fake_result[attr] = []
    return fake_result


def check_input_ref_params(workflow, node, global_params):
    """
    检查工作流引用参数是否符合规范
        1、加载当前工作流的全部输出变量
        2、加载当前节点的引用变量
        3、如果结果为空，则说明引用参数不符合规范
    """
    error_info = []
    schema = node.node_input_params_json_schema
    if not schema or not isinstance(schema, dict):
        return error_info
    if not schema.get("properties"):
        return error_info
    from app.services.app_center.app_run_service import load_properties
    result = load_properties(schema.get("properties"), global_params)
    if not result:
        error_info.append({
            "id": f"alter-节点引用参数{node.id}",
            "title": f"工作流{workflow.workflow_name}-{node.node_name}:引用参数配置异常",
            "type": "error"
        })
    # 如果结果中字段的值为空，则说明该字段引用参数不符合规范
    error_result = valid_fake_result(schema.get("properties"), result)
    for error in error_result:
        error_info.append({
            "id": f"alter-节点引用参数{node.id}",
            "title": f"工作流{workflow.workflow_name}-{node.node_name}:引用参数{error}失效",
            "type": "error"
        })
    return error_info


def valid_fake_result(properties, fake_result):
    """
    验证生成的假数据是否符合规范
    :param properties: 属性定义
    :param fake_result: 假数据
    :return: 是否符合规范
    """
    invalid_attrs = []
    for attr, attr_define in properties.items():
        if attr not in fake_result:
            invalid_attrs.append(attr)
            continue
        if attr_define.get("type") == "string" and not isinstance(fake_result[attr], str):
            invalid_attrs.append(attr)
        elif attr_define.get("type") == "number" and not isinstance(fake_result[attr], (int, float)):
            invalid_attrs.append(attr)
        elif attr_define.get("type") == "integer" and not isinstance(fake_result[attr], int):
            invalid_attrs.append(attr)
        elif attr_define.get("type") == "boolean" and not isinstance(fake_result[attr], bool):
            invalid_attrs.append(attr)
        elif attr_define.get("type") == "object":
            invalid_attrs.extend(valid_fake_result(attr_define.get("properties", {}), fake_result[attr]))
        elif attr_define.get("type") == "array":
            if not isinstance(fake_result[attr], list):
                invalid_attrs.append(attr)
            else:
                item_type = attr_define.get("items", {}).get("type")
                if item_type == "string":
                    for item in fake_result[attr]:
                        if not isinstance(item, str):
                            invalid_attrs.append(attr)
                elif item_type == "number":
                    for item in fake_result[attr]:
                        if not isinstance(item, (int, float)):
                            invalid_attrs.append(attr)
                elif item_type == "integer":
                    for item in fake_result[attr]:
                        if not isinstance(item, int):
                            invalid_attrs.append(attr)
                elif item_type == "boolean":
                    for item in fake_result[attr]:
                        if not isinstance(item, bool):
                            invalid_attrs.append(attr)
                elif item_type == "object":
                    for item in fake_result[attr]:
                        invalid_attrs.extend(valid_fake_result(attr_define.get("items", {}).get("properties", {}), item))
                elif item_type == "null":
                    for item in fake_result[attr]:
                        if item is not None:
                            invalid_attrs.append(attr)
                elif item_type == 'array':
                    for item in fake_result[attr]:
                        if not isinstance(item, list):
                            invalid_attrs.append(attr)
                        else:
                            item_properties = attr_define.get("items", {}).get("items", {}).get("properties", {})
                            if item_properties:
                                invalid_attrs.extend(valid_fake_result(item_properties, item))

    return invalid_attrs


def check_message_ref_params(workflow, node, global_params):
    """
    检查工作流消息引用参数是否符合规范
        1、加载当前工作流的全部输出变量
        2、加载当前节点的引用变量
        3、如果结果为空，则说明引用参数不符合规范
    """
    error_info = []
    schema = node.node_message_schema
    if not schema or not isinstance(schema, list):
        return error_info
    from app.services.app_center.app_run_service import load_properties
    for message_schema in schema:
        result = load_properties(message_schema.get("schema").get("properties"), global_params)
        if not result:
            error_info.append({
                "id": f"alter-节点消息引用参数{node.id}",
                "title": f"工作流{workflow.workflow_name}-{node.node_name}:消息参数配置异常",
                "type": "error"
            })
        # 如果结果中字段的值为空，则说明该字段引用参数不符合规范
        error_result = valid_fake_result(message_schema.get("schema").get("properties"), result)
        for error in error_result:
            error_info.append({
                "id": f"alter-节点消息引用参数{node.id}",
                "title": f"工作流{workflow.workflow_name}-{node.node_name}:消息参数{error}失效",
                "type": "error"
            })
    return error_info


def init_app_flow_node(params):
    """
    初始化应用代理节点
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    app_code = params.get("app_code")
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    workflow_code = params.get("workflow_code")
    node_type = params.get("node_type", "llm")
    node_name = params.get("node_name", "Agent节点")
    node_desc = params.get("node_desc", "通过大语言模型构建Agent，智能生成回复")
    node_icon = params.get("node_icon", "images/node_llm.svg")
    node_code = params.get("node_code")
    node_llm_code = params.get("node_llm_code")
    node_llm_params = params.get("node_llm_params", {
        "temperature": 0.7,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 8192,
        "stop": None,
        "stream": False,
        "response_format": "text",
        "enable_visual": False,
        "visual_schema": {
            "type": "object",
            "properties": {
                "images": {
                    "type": "array[number]",
                    "items": {

                    },
                    "description": "图片列表",
                    "typeFixed": True,
                    "attrFixed": True,
                    "ref": {},
                }
            },
            "ncOrders": ["images"],
        },
        "use_default": True,
    })
    target_flow = WorkFlowMetaInfo.query.filter(
        WorkFlowMetaInfo.workflow_code == workflow_code,
        WorkFlowMetaInfo.workflow_status != '已删除',
        WorkFlowMetaInfo.environment == '开发'
    ).first()
    if not target_flow:
        return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)
    if not node_code:
        node_code = str(uuid.uuid4())
    node_input_params_json_schema = {
        "type": "object",
        "properties": {},
    }
    node_result_params_json_schema = {
        "type": "object",
        "properties": {
            "OUTPUT": {
                "type": "string",
                "description": "输出参数"
            }
        },
        "ncOrders": ['OUTPUT']
    }

    new_node = WorkflowNodeInfo(
        user_id=user_id,
        workflow_id=target_flow.id,
        node_code=node_code,
        node_type=node_type,
        node_name=node_name,
        node_desc=node_desc,
        node_icon=node_icon,
        node_llm_code=node_llm_code,
        node_llm_params=node_llm_params,
        node_input_params_json_schema=node_input_params_json_schema,
        node_result_params_json_schema=node_result_params_json_schema,
    )
    if node_type == 'start':
        init_start_node(new_node)
    if node_type == 'llm':
        init_llm_node(new_node)
    if node_type == 'rag':
        init_rag_node(new_node)
    if node_type == 'file_reader':
        init_file_reader_node(new_node)
    db.session.add(new_node)
    db.session.commit()
    # 修改工作流的schema
    new_workflow_schem = target_flow.workflow_schema
    if not new_workflow_schem:
        with open(os.path.join(app.config['config_static'], "schema.json"), 'r', encoding="utf8") as f:
            new_workflow_schem = json.load(f)
    if not isinstance(new_workflow_schem, dict):
        new_workflow_schem = json.loads(new_workflow_schem)
    # 根据节点类型添加前端节点
    first_node = new_workflow_schem.get("cells")[0]
    new_node_config = {
            "position": {
                "x": first_node["position"]["x"] + 100,
                "y": first_node["position"]["y"] + 100,
            },
            "size": {
                "width": 300,
                "height": 100
            },
            "shape": "custom-vue-node",
            "ports": {
                "groups": {
                    "top": {
                        "position": "left",
                        "attrs": {
                          "circle": {
                            "r": 4,
                            "magnet": True,
                            "stroke": "#31d0c6",
                            "strokeWidth": 2,
                            "fill": "#fff"
                          }
                        }
                      },
                    "bottom": {
                        "position": "right",
                        "attrs": {
                          "circle": {
                            "r": 4,
                            "magnet": True,
                            "stroke": "#31d0c6",
                            "strokeWidth": 2,
                            "fill": "#fff"
                          }
                        }
                      }
                },
                "items": [
                    {
                        "group": "top",
                        "id": uuid.uuid4().hex
                    },
                    {
                        "group": "bottom",
                        "id": uuid.uuid4().hex
                    }
                ]
            },
            "id": node_code,
            "data": {
                "nodeIcon": node_icon,
                "nodeType": node_type,
                "nodeDesc": node_desc,
                "nodeName": node_name,
                "nodeInput": "string",
                "nodeOutput": "string",
                "nodeModel": ""
            },
            "zIndex": 3
        }
    new_workflow_schem.get("cells").append(new_node_config)
    target_flow.workflow_schema = json.dumps(new_workflow_schem)
    target_flow.workflow_edit_schema = json.dumps(new_workflow_schem)
    db.session.add(target_flow)
    db.session.commit()

    return next_console_response(result={
        "node_code": new_node.node_code,
        "node_name": new_node.node_name,
        "node_desc": new_node.node_desc,
        "node_icon": new_node.node_icon,
        "node_llm_code": new_node.node_llm_code,
        "node_llm_params": new_node.node_llm_params,
        "node_failed_solution": new_node.node_failed_solution,
    })


def init_start_node(new_node):
    """
    初始化开始节点
    """
    new_node.node_result_format = 'json'
    new_node.node_result_params_json_schema = {
        "type": "object",
        "properties": {
            "USER_INPUT": {
                "type": "string",
                "description": "输入参数"
            },
            "SessionAttachmentList": {
                "type": "array",
                "description": "会话附件",
                "items": {
                    "properties": {
                        "format": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "string",
                            "value": ""
                        },
                        "id": {
                            "showSubArea": False,
                            "type": "number"
                        },
                        "name": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "string",
                            "value": ""
                        },
                        "size": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "number",
                            "value": ""
                        }
                    },
                    "type": "object",
                    "ncOrders": ["id", "name", "format", "size"]
                },
                "showSubArea": True,
            },
            "MessageAttachmentList": {
                "description": "消息附件",
                "items": {
                    "properties": {
                        "format": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "string",
                            "value": ""
                        },
                        "id": {
                            "showSubArea": False,
                            "type": "number"
                        },
                        "name": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "string",
                            "value": ""
                        },
                        "size": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "number",
                            "value": ""
                        }
                    },
                    "type": "object",
                    "ncOrders": ["id", "name", "format", "size"]
                },
                "showSubArea": True,
                "type": "array"
            },
            "session_id": {
                "type": "number",
                "description": "会话id"
            },
            "current_time": {
                "type": "string",
                "description": "当前时间"
            }
        },
        "ncOrders": ['USER_INPUT', 'session_id', 'SessionAttachmentList', 'MessageAttachmentList', 'current_time']
    }


def init_llm_node(new_node):
    """
    初始化LLM节点
    """
    new_node.node_result_format = 'json'
    new_node.node_result_params_json_schema = {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "输出消息",
                "attrFixed": True
            },
            "reasoning_content": {
                "type": "string",
                "description": "推理消息",
                "attrFixed": True,
                "typeFixed": True
            },
        },
        "ncOrders": ['content', 'reasoning_content']
    }


def init_rag_node(new_node):
    """

    :param new_node:
    :return:
    """
    new_node.node_failed_solution = "pass"
    new_node.node_result_format = 'json'
    new_node.node_result_params_json_schema = {
        "properties": {
            "details": {
                "items": {
                    "properties": {
                        "meta": {
                            "properties": {
                                "source": {
                                    "showSubArea": False,
                                    "type": "number"
                                },
                                "source_type": {
                                    "ref": "",
                                    "showSubArea": False,
                                    "type": "string",
                                    "value": ""
                                }
                            },
                            "ref": "",
                            "showSubArea": True,
                            "type": "object",
                            "value": "",
                            "ncOrders": ["source", "source_type"]
                        },
                        "recall_score": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "number",
                            "value": ""
                        },
                        "rerank_score": {
                            "showSubArea": False,
                            "type": "number"
                        },
                        "text": {
                            "ref": "",
                            "showSubArea": True,
                            "type": "string",
                            "value": ""
                        }
                    },
                    "type": "object",
                    "ncOrders": ["meta", "text", "recall_score", "rerank_score"]
                },
                "ref": "",
                "showSubArea": True,
                "type": "array",
                "value": ""
            },
            "reference_texts": {
                "items": {
                    "type": "string"
                },
                "ref": "",
                "showSubArea": True,
                "type": "array",
                "value": ""
            },
        },
        "type": "object",
        "ncOrders": ["details", "reference_texts"]
    }
    new_node.node_rag_resources = [
        {
            "id": "message_attachments",
            "resource_ready": True,
            "resource_icon": "images/node_rag.svg",
            "resource_name": "消息附件",
        },
        {
            "id": "session_attachments",
            "resource_ready": True,
            "resource_icon": "images/node_rag.svg",
            "resource_name": "会话附件",
        },
    ]
    new_node.node_rag_recall_config = {
        "recall_similarity": "cosine",
        "recall_threshold": 0.3,
        "recall_k": 30,
    }
    new_node.node_rag_rerank_config = {
        "rerank_enabled": True,
        "max_chunk_per_doc": 1024,
        "overlap_tokens": 80,
        "rerank_threshold": 0.6,
        "rerank_k": 10,
    }
    new_node.node_rag_web_search_config = {
        "search_engine_enhanced": True,
        "gl": "cn",
        "hl": "zh-cn",
        "location": "China",
        "num": 20,
        "timeout": 30,
    }


def init_file_reader_node(new_node):
    """

    :return:
    """
    new_node.node_result_format = 'json'
    new_node.node_result_params_json_schema = {
        "ncOrders": [
            "output_resources"
        ],
        "properties": {
            "output_resources": {
                "items": {
                    "ncOrders": [
                        "id",
                        "content",
                        "url",
                        "format"
                    ],
                    "properties": {
                        "content": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "string",
                            "value": ""
                        },
                        "format": {
                            "ref": "",
                            "showSubArea": True,
                            "type": "string",
                            "value": ""
                        },
                        "id": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "number",
                            "value": ""
                        },
                        "tmpAttr": {
                            "showSubArea": False,
                            "type": "string"
                        },
                        "url": {
                            "ref": "",
                            "showSubArea": False,
                            "type": "string",
                            "value": ""
                        }
                    },
                    "type": "object"
                },
                "ref": "",
                "showSubArea": True,
                "type": "array",
                "value": ""
            }
        },
        "type": "object"
    }
    new_node.node_input_params_json_schema = {
        "ncOrders": [
            "input_resources"
        ],
        "properties": {
            "input_resources": {
                "items": {
                    "type": "number",
                    "typeFixed": True,
                },
                "ref": "",
                "showSubArea": True,
                "type": "array",
                "value": "",
                "attrFixed": True,
                "typeFixed": True
            }
        }

    }


def update_app_flow_node(params):
    """
    更新应用代理节点
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    node_code = params.get("node_code")
    node_name = params.get("node_name")
    node_desc = params.get("node_desc")
    node_llm_code = params.get("node_llm_code")
    node_llm_params = params.get("node_llm_params")
    node_run_model_config = params.get("node_run_model_config")
    node_llm_system_prompt_template = params.get("node_llm_system_prompt_template")
    node_llm_user_prompt_template = params.get("node_llm_user_prompt_template")
    node_result_format = params.get("node_result_format")
    node_result_format_params_json_schema = params.get("node_result_format_params_json_schema")
    node_result_extract_separator = params.get("node_result_extract_separator")
    node_result_extract_quote = params.get("node_result_extract_quote")
    node_result_extract_columns = params.get("node_result_extract_columns")
    node_retry_max = params.get("node_retry_max")
    node_retry_duration = params.get("node_retry_duration")
    node_retry_model = params.get("node_retry_model")
    node_failed_solution = params.get("node_failed_solution")
    node_failed_template = params.get("node_failed_template")
    node_result_template = params.get("node_result_template")
    node_session_memory_size = params.get("node_session_memory_size")
    node_deep_memory = params.get("node_deep_memory")
    node_agent_nickname = params.get("node_agent_nickname")
    node_agent_desc = params.get("node_agent_desc")
    node_agent_avatar = params.get("node_agent_avatar")
    node_agent_prologue = params.get("node_agent_prologue")
    node_agent_preset_question = params.get("node_agent_preset_question")
    node_agent_tools = params.get("node_agent_tools")
    node_input_params_json_schema = params.get("node_input_params_json_schema")
    node_result_params_json_schema = params.get("node_result_params_json_schema")
    node_tool_api_url = params.get("node_tool_api_url")
    node_tool_http_method = params.get("node_tool_http_method")
    node_tool_http_params = params.get("node_tool_http_params")
    node_tool_http_header = params.get("node_tool_http_header")
    node_tool_http_body = params.get("node_tool_http_body")
    node_tool_http_body_type = params.get("node_tool_http_body_type")
    node_timeout = params.get("node_timeout")
    node_rag_resources = params.get("node_rag_resources")
    node_rag_query_template = params.get("node_rag_query_template")
    node_rag_recall_config = params.get("node_rag_recall_config")
    node_rag_rerank_config = params.get("node_rag_rerank_config")
    node_rag_web_search_config = params.get("node_rag_web_search_config")
    node_enable_message = params.get("node_enable_message")
    node_message_schema_type = params.get("node_message_schema_type")
    node_message_schema = params.get("node_message_schema")
    node_rag_ref_show = params.get("node_rag_ref_show")
    node_file_reader_config = params.get("node_file_reader_config")
    target_node = WorkflowNodeInfo.query.filter(
        WorkflowNodeInfo.node_code == node_code,
        WorkflowNodeInfo.node_status == "正常",
        WorkflowNodeInfo.environment == "开发"
    ).first()
    if not target_node:
        return next_console_response(error_status=True, error_message="节点不存在！", error_code=1002)
    if node_llm_code is not None:
        target_node.node_llm_code = node_llm_code
    if node_llm_params is not None:
        target_node.node_llm_params = node_llm_params
    if node_llm_system_prompt_template is not None:
        target_node.node_llm_system_prompt_template = node_llm_system_prompt_template
    if node_llm_user_prompt_template is not None:
        target_node.node_llm_user_prompt_template = node_llm_user_prompt_template
    if node_result_format is not None:
        target_node.node_result_format = node_result_format
    if node_result_format_params_json_schema is not None:
        target_node.node_result_format_params_json_schema = node_result_format_params_json_schema
    if node_result_template is not None:
        target_node.node_result_template = node_result_template
    if node_session_memory_size is not None:
        target_node.node_session_memory_size = node_session_memory_size
    if node_deep_memory is not None:
        target_node.node_deep_memory = node_deep_memory
    if node_agent_nickname is not None:
        target_node.node_agent_nickname = node_agent_nickname
    if node_agent_desc is not None:
        target_node.node_agent_desc = node_agent_desc
    if node_agent_avatar is not None:
        target_node.node_agent_avatar = node_agent_avatar
    if node_agent_prologue is not None:
        target_node.node_agent_prologue = node_agent_prologue
    if node_agent_preset_question is not None:
        target_node.node_agent_preset_question = node_agent_preset_question
    if node_input_params_json_schema is not None:
        target_node.node_input_params_json_schema = node_input_params_json_schema
    if node_agent_tools is not None:
        target_node.node_agent_tools = node_agent_tools
    if node_result_extract_separator is not None:
        target_node.node_result_extract_separator = node_result_extract_separator
    if node_result_extract_quote is not None:
        target_node.node_result_extract_quote = node_result_extract_quote
    if node_result_extract_columns is not None:
        target_node.node_result_extract_columns = node_result_extract_columns
    if node_retry_max is not None:
        target_node.node_retry_max = node_retry_max
    if node_retry_duration is not None:
        target_node.node_retry_duration = node_retry_duration
    if node_retry_model is not None:
        target_node.node_retry_model = node_retry_model
    if node_failed_solution is not None:
        target_node.node_failed_solution = node_failed_solution
    if node_failed_template is not None:
        target_node.node_failed_template = node_failed_template
    if node_run_model_config is not None:
        target_node.node_run_model_config = node_run_model_config
    if node_result_params_json_schema is not None:
        target_node.node_result_params_json_schema = node_result_params_json_schema
    if node_tool_api_url is not None:
        target_node.node_tool_api_url = node_tool_api_url
    if node_tool_http_method is not None:
        target_node.node_tool_http_method = node_tool_http_method
    if node_tool_http_header is not None:
        target_node.node_tool_http_header = node_tool_http_header
    if node_tool_http_params is not None:
        target_node.node_tool_http_params = node_tool_http_params
    if node_tool_http_body is not None:
        target_node.node_tool_http_body = node_tool_http_body
    if node_tool_http_body_type is not None:
        target_node.node_tool_http_body_type = node_tool_http_body_type
    if node_timeout is not None:
        target_node.node_timeout = node_timeout
    if node_name:
        target_node.node_name = node_name
    if node_desc is not None:
        target_node.node_desc = node_desc
    if node_rag_resources is not None:
        target_node.node_rag_resources = node_rag_resources
    if node_rag_query_template is not None:
        target_node.node_rag_query_template = node_rag_query_template
    if node_rag_recall_config is not None:
        target_node.node_rag_recall_config = node_rag_recall_config
    if node_rag_rerank_config is not None:
        target_node.node_rag_rerank_config = node_rag_rerank_config
    if node_rag_web_search_config is not None:
        target_node.node_rag_web_search_config = node_rag_web_search_config
    if node_enable_message is not None:
        target_node.node_enable_message = node_enable_message
    if node_message_schema is not None:
        target_node.node_message_schema = node_message_schema
    if node_message_schema_type is not None:
        target_node.node_message_schema_type = node_message_schema_type
    if node_rag_ref_show is not None:
        target_node.node_rag_ref_show = node_rag_ref_show
    if node_file_reader_config is not None:
        target_node.node_file_reader_config = node_file_reader_config
    db.session.add(target_node)
    db.session.commit()
    return next_console_response(result=target_node.to_dict())


def delete_app_flow_node(params):
    """
    删除应用代理节点
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    workflow_code = params.get("workflow_code")
    nodes = params.get("nodes", [])
    target_nodes = WorkflowNodeInfo.query.filter(
        WorkflowNodeInfo.node_code.in_(nodes),
        WorkflowNodeInfo.node_status != '已删除',
        WorkflowNodeInfo.environment == "开发"
    ).all()
    all_workflow_ids = [node.workflow_id for node in target_nodes]
    target_workflows = WorkFlowMetaInfo.query.filter(
        or_(WorkFlowMetaInfo.id.in_(all_workflow_ids), WorkFlowMetaInfo.workflow_code == workflow_code),
        WorkFlowMetaInfo.workflow_status != '已删除',
        WorkFlowMetaInfo.environment == '开发'
    ).all()
    if not target_workflows:
        return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)
    # 修改工作流的schema
    for target_workflow in target_workflows:
        new_workflow_schem = json.loads(target_workflow.workflow_edit_schema)
        new_workflow_schem.get("cells").remove(
            next(filter(lambda x: x.get("id") in nodes, new_workflow_schem.get("cells")), None)
        )
        target_workflow.workflow_edit_schema = json.dumps(new_workflow_schem)
        db.session.add(target_workflow)
        db.session.commit()
    for target_node in target_nodes:
        target_node.node_status = '已删除'
        db.session.add(target_node)
        db.session.commit()
    return next_console_response(result="删除成功！")


def get_app_flow_node_detail(params):
    """
    获取应用代理节点详情
    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    node_code = params.get("node_code")
    target_node = WorkflowNodeInfo.query.filter(
        WorkflowNodeInfo.node_code == node_code,
        WorkflowNodeInfo.node_status != '已删除',
        WorkflowNodeInfo.environment == "开发"
    ).first()

    if target_node:
        return next_console_response(result=target_node.to_dict())
    return next_console_response(error_status=True, error_message="节点不存在！", error_code=1002)


def upload_node_agent_icon(user_id, node_agent_avatar):
    """
    上传节点代理图标
    """
    suffix = node_agent_avatar.filename.split(".")[-1]
    avatar_path = generate_new_path("app_center",
                                    user_id=user_id, file_type="file", suffix=suffix
                                    ).json.get("result")
    node_agent_avatar.save(avatar_path)
    app_icon = generate_download_url(
        "app_center",
        avatar_path, suffix=suffix).json.get("result")
    return next_console_response(result={
        "node_agent_avatar": app_icon,
    })


def search_app_flow_node(params):
    """

    :param params:
    :return:
    """
    app_code = params.get("app_code")
    user_id = int(params.get("user_id"))
    check_res = check_workflow_permission(user_id, app_code)
    if check_res is not True:
        return check_res
    workflow_code = params.get("workflow_code")
    node_code = params.get("node_code", [])
    node_keyword = params.get("node_keyword", "")
    node_type = params.get("node_type", [])
    page_size = params.get("page_size", 10)
    page_num = params.get("page_num", 1)
    fetch_all = params.get("fetch_all", False)
    target_workflow = WorkFlowMetaInfo.query.filter(
        WorkFlowMetaInfo.workflow_code == workflow_code,
        WorkFlowMetaInfo.workflow_status != '已删除',
        WorkFlowMetaInfo.environment == '开发'
    ).first()
    if not target_workflow:
        return next_console_response(error_status=True, error_message="工作流不存在！", error_code=1002)
    all_condition = [
        WorkflowNodeInfo.workflow_id == target_workflow.id,
        WorkflowNodeInfo.node_status != '已删除',
        WorkflowNodeInfo.environment == "开发"
    ]

    if node_code:
        all_condition.append(WorkflowNodeInfo.node_code.in_(node_code))
    if node_keyword:
        all_condition.append(
            or_(
                WorkflowNodeInfo.node_name.like(f"%{node_keyword}%"),
                WorkflowNodeInfo.node_desc.like(f"%{node_keyword}%"),
            ))
    if node_type:
        all_condition.append(WorkflowNodeInfo.node_type.in_(node_type))
    target_node = WorkflowNodeInfo.query.filter(*all_condition).order_by(WorkflowNodeInfo.create_time.desc())
    total = target_node.count()
    if not fetch_all:
        target_node = target_node.paginate(page=page_num, per_page=page_size, error_out=False)
    else:
        target_node = target_node.all()
        page_num = 1
        page_size = total
    data = [
        node_info.to_dict() for node_info in target_node
    ]
    result = {
        "total": total,
        "page_num": page_num,
        "page_size": page_size,
        "data": data
    }
    return next_console_response(result=result)


def check_workflow_permission(user_id, app_code):
    """
    检查工作流权限
    :param user_id:
    :param app_code:
    :return:
    """
    target_app = AppMetaInfo.query.filter(
        AppMetaInfo.app_code == app_code,
        AppMetaInfo.app_status != "已删除",
        AppMetaInfo.environment == '开发'
    ).first()
    if not target_app:
        return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
    if not check_has_role(user_id, "next_console_admin") and target_app.user_id != user_id:
        app_user = UserInfo.query.filter(
            UserInfo.user_id == target_app.user_id
        ).first()
        current_user = UserInfo.query.filter(
            UserInfo.user_id == user_id
        ).first()
        if not app_user or not current_user:
            return next_console_response(error_status=True, error_message="应用不存在！", error_code=1002)
        if app_user.user_company_id != current_user.user_company_id:
            return next_console_response(error_status=True, error_message="没有权限查看该应用！", error_code=1002)
    return True
