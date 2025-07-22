from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.services.app_center.app_manage_service import *
from app.services.app_center.workflow_service import *
from app.services.user_center.roles import roles_required


@app.route('/next_console_admin/app_center/app_manage/search', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def search_ai_apps():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return search_all_apps(data)


@app.route('/next_console_admin/app_center/app_manage/icon/upload', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def upload_ai_app_icon():
    user_id = get_jwt_identity()
    app_icon_data = request.files.get('app_icon')
    if not app_icon_data:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return upload_app_icon(user_id, app_icon_data)


@app.route('/next_console_admin/app_center/app_manage/add', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def add_ai_app():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return add_app(data)


@app.route('/next_console_admin/app_center/app_manage/delete',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def delete_ai_app():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return delete_app(data)


@app.route('/next_console_admin/app_center/app_manage/detail',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def detail_ai_app():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return get_app_detail(data)


@app.route('/next_console_admin/app_center/app_manage/update',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def update_ai_app():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return update_app_detail(data)


@app.route('/next_console_admin/app_center/app_manage/upload',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def upload_ai_app():
    user_id = get_jwt_identity()
    app_schema = request.files.get('app_schema')
    if not app_schema:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return upload_app_schema(user_id, app_schema)


@app.route('/next_console_admin/app_center/app_manage/import',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def import_ai_app():
    user_id = get_jwt_identity()
    data = request.get_json()
    app_schema_url = data.get('app_schema_url')
    if not app_schema_url:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    data["user_id"] = user_id
    return import_app_schema(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/create',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def create_ai_app_flow():
    """
    添加应用流程
    :return:
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    flow_name = data.get("workflow_name")
    flow_desc = data.get("workflow_desc")
    if not app_code or not flow_name or not flow_desc:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return create_workflow(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/icon_upload', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def upload_ai_app_flow_icon():
    user_id = get_jwt_identity()
    flow_icon_data = request.files.get('workflow_icon')
    if not flow_icon_data:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return upload_workflow_icon(user_id, flow_icon_data)


@app.route('/next_console_admin/app_center/app_manage/workflow/delete',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def delete_ai_app_flow():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    flow_code = data.get("workflow_code")
    if not flow_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return delete_app_flow(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/update',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def update_ai_app_flow():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    workflow_code = data.get("workflow_code")
    if not app_code or not workflow_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return update_app_flow(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/detail',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def get_ai_app_flow_detail():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    workflow_code = data.get("workflow_code")
    if not app_code or not workflow_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return get_app_flow_detail(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/restore',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def restore_ai_app_flow():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    workflow_code = data.get("workflow_code")
    if not app_code or not workflow_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return restore_app_flow_schema(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/check',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def check_ai_app_flow():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    workflow_code = data.get("workflow_code")
    if not app_code or not workflow_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return check_app_flow_schema(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/export',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def export_ai_app_flow():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    workflow_code = data.get("workflow_code")
    if not app_code or not workflow_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return export_app_flow_schema(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/upload',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def upload_ai_app_flow():
    user_id = get_jwt_identity()
    workflow_schema = request.files.get('workflow_schema')
    if not workflow_schema:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return upload_app_flow_schema(user_id, workflow_schema)


@app.route('/next_console_admin/app_center/app_manage/workflow/import',  methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def import_ai_app_flow():
    user_id = get_jwt_identity()
    data = request.get_json()
    app_code = data.get("app_code")
    workflow_schema_url = data.get('workflow_schema_url')
    if not app_code or not workflow_schema_url:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    data["user_id"] = user_id
    return import_workflow_schema(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/node/init', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def init_ai_app_flow_node():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    workflow_code = data.get("workflow_code")
    node_type = data.get("node_type")
    if not app_code or not workflow_code or not node_type:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return init_app_flow_node(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/node/update', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def update_ai_app_flow_node():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    node_code = data.get("node_code")
    if not node_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return update_app_flow_node(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/node/delete', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def delete_ai_app_flow_node():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    node_code = data.get("nodes")
    if not node_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return delete_app_flow_node(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/node/detail', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def get_ai_app_flow_node_detail():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    node_code = data.get("node_code")
    if not node_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return get_app_flow_node_detail(data)


@app.route('/next_console_admin/app_center/app_manage/workflow/node/agent_avatar_upload', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def agent_avatar_upload():
    user_id = get_jwt_identity()
    node_agent_avatar = request.files.get('node_agent_avatar')
    if not node_agent_avatar:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return upload_node_agent_icon(user_id, node_agent_avatar)


@app.route('/next_console_admin/app_center/app_manage/workflow/node/search', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def search_ai_app_flow_node():
    """
    搜索应用流程节点
    :return:
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    workflow_code = data.get("workflow_code")
    if not workflow_code:
        return next_console_response(error_status=True, error_message="参数错误！", error_code=1002)
    return search_app_flow_node(data)


@app.route('/next_console_admin/app_center/publish_manage/search_prod_app', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def search_ai_apps_publish():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    data["environment"] = "生产"
    return search_all_apps(data)


@app.route('/next_console_admin/app_center/publish_manage/create', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def create_ai_apps_publish():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    publish_name = data.get("publish_name")
    if not app_code:
        return next_console_response(error_status=True, error_message="缺失应用编号！")
    if not publish_name:
        return next_console_response(error_status=True, error_message="缺失发布名称！")
    return create_app_publish(data)


@app.route('/next_console_admin/app_center/publish_manage/author', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def author_ai_apps_publish():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    user_list = data.get("user_list")
    department_list = data.get("department_list")
    company_list = data.get("company_list")
    if not app_code:
        return next_console_response(error_status=True, error_message="缺失应用编号！")
    if not user_list and department_list and company_list:
        return next_console_response(error_status=True, error_message="缺失授权对象列表！")
    return author_app_publish(data)


@app.route('/next_console_admin/app_center/publish_manage/unauthor', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def cancel_author_ai_apps_publish():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    user_list = data.get("user_list")
    department_list = data.get("department_list")
    company_list = data.get("company_list")
    if not app_code:
        return next_console_response(error_status=True, error_message="缺失应用编号！")
    if not user_list and not department_list and not company_list:
        return next_console_response(error_status=True, error_message="缺失授权对象列表！")
    return cancel_author_app_publish(data)


@app.route('/next_console_admin/app_center/publish_manage/search', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def search_ai_apps_publish_version():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="缺失应用编号！")
    return search_app_publish(data)


@app.route('/next_console_admin/app_center/publish_manage/search_access', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def search_ai_apps_publish_access():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="缺失应用编号！")
    return search_app_access(data)


@app.route('/next_console_admin/app_center/publish_manage/running_status', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def get_ai_apps_publish_running_status():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    index_type = data.get("index_type")
    if not app_code:
        return next_console_response(error_status=True, error_message="缺失应用编号！")
    if not index_type:
        return next_console_response(error_status=True, error_message="缺失指标类型！")
    return get_app_running_status(data)


@app.route('/next_console_admin/app_center/publish_manage/export', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def export_ai_apps_publish():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    publish_id = data.get("publish_id")
    if not app_code:
        return next_console_response(error_status=True, error_message="缺失应用编号！")
    if not publish_id:
        return next_console_response(error_status=True, error_message="缺失发布编号！")
    return export_app_schema(data)


@app.route('/next_console_admin/app_center/publish_manage/delete', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def delete_ai_apps_publish_version():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    app_code = data.get("app_code")
    if not app_code:
        return next_console_response(error_status=True, error_message="缺失应用编号！")
    return delete_app_publish(data)
