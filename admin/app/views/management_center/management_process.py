from flask import request, send_file
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.app import app
from app.services.management_center.management_session import *
from app.services.management_center.management_user import *
from app.services.management_center.management_company import *
from app.services.user_center.users import *
import pandas as pd
from app.services.user_center.roles import roles_required


@app.route('/next_console_admin/management_center/management/session/lookup', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin", "next_console_reader_admin"])
@jwt_required()
def session_details_lookup():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookup_session_details(params)


@app.route('/next_console_admin/management_center/management/session/search_source', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin", "next_console_reader_admin"])
@jwt_required()
def session_source_lookup():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return search_session_source(params)


@app.route('/next_console_admin/management_center/management/session/addtag', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def session_details_addtag():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return addtag_session_details(params)


@app.route('/next_console_admin/management_center/management/session/lookuptag', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def session_details_lookuptag():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookuptag_session_details(params)


@app.route('/next_console_admin/management_center/management/session/lookupmsg', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def session_message_details_lookup():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookup_session_message_details(params)


@app.route('/next_console_admin/management_center/management/session/updateadminfavorite', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def admin_favorite_update():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return update_admin_favorite(params)


@app.route('/next_console_admin/management_center/management/session/updateadminmsglike', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def admin_msg_like_update():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return update_admin_msg_like(params)


@app.route('/next_console_admin/management_center/management/session/lookupadminfavorite', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def admin_favorite_lookup():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookup_admin_favorite(params)


@app.route('/next_console_admin/management_center/management/session/lookupadminmsglike', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def admin_msg_like_lookup():
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookup_admin_msg_like(params)


@app.route('/next_console_admin/management_center/management/user/lookupbytwadmin', methods=['POST'])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def twadmin_lookup_user_details():
    """
    平台管理员查询用户详情
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookup_user_details_twadmin(params)


@app.route('/next_console_admin/management_center/management/user/updateroletwadmin', methods=['POST'])
@roles_required(["next_console_admin"])
@jwt_required()
def twadmin_update_user_role():
    """
    平台管理员更新用户角色
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    update_user_id = params.get("update_user_id")
    dest_role_desc = params.get("dest_role_desc")
    if update_user_id is None:
        return next_console_response(error_status=True, error_code=1004, error_message="参数update_user_id不能为空！")
    elif not isinstance(update_user_id, int):
        return next_console_response(error_status=True, error_code=1004, error_message="参数update_user_id格式错误！")
    elif not dest_role_desc:
        return next_console_response(error_status=True, error_code=1004, error_message="用户不能没有角色！")
    elif not isinstance(dest_role_desc, list):
        return next_console_response(error_status=True, error_code=1004,
                                     error_message="参数dest_role_desc应为列表格式！")
    return update_user_role_twadmin(params)


@app.route('/next_console_admin/management_center/management/user/add_user_by_excel_corp', methods=['GET', 'POST'])
@jwt_required()
def user_add_by_excel_corp():
    """
    通过excel新增用户
    :return:
    """
    params = {}
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    params["admin_type"] = "corpadmin"
    if request.method == 'GET':
        execl_file_path = os.path.join(app.config['config_static'], "user_template.xlsx")
        return send_file(execl_file_path, as_attachment=True)
    # 获取入参
    if 'file' not in request.files:
        return next_console_response(error_status=True, error_message="未上传文件！", error_code=1002)
    file = request.files["file"]
    try:
        df = pd.read_excel(file, sheet_name="用户数据", engine='openpyxl')
    except Exception as e:
        return next_console_response(error_status=True, error_message="文件格式错误！:{}".format(str(e)),
                                     error_code=1002)
    check_data_result = check_df_data_corp(df)
    if check_data_result is not True:
        return next_console_response(error_status=True, error_message=check_data_result.get_json()["error_message"],
                                     error_code=1002)
    else:
        res = add_user_by_excel(df, params)
        return res


@app.route('/next_console_admin/management_center/management/user/add_user_by_excel_twadmin', methods=['GET', 'POST'])
@jwt_required()
def user_add_by_excel_twadmin():
    """
    通过excel新增用户
    :return:
    """
    params = {}
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    params["admin_type"] = "twadmin"
    if request.method == 'GET':
        execl_file_path = os.path.join(app.config['config_static'], "user_template_twadmin.xlsx")
        return send_file(execl_file_path, as_attachment=True)
    # 获取入参
    if 'file' not in request.files:
        return next_console_response(error_status=True, error_message="未上传文件！", error_code=1002)
    file = request.files["file"]
    try:
        df = pd.read_excel(file, sheet_name="用户数据", engine='openpyxl',
                           keep_default_na=False, na_values=['nan'])

        # 将 DataFrame 中的 nan 转换为 None
        df = df.where(pd.notna(df), None)
    except Exception as e:
        return next_console_response(error_status=True, error_message="文件格式错误！:{}".format(str(e)),
                                     error_code=1002)
    check_data_result = check_df_data_twadmin(df)
    if check_data_result is not True:
        return next_console_response(error_status=True, error_message=check_data_result.get_json()["error_message"],
                                     error_code=1002)
    else:
        res = add_user_by_excel(df, params)
        return res


@app.route('/next_console_admin/management_center/management/user/create', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin"])
@jwt_required()
def user_create():
    """
    新增用户
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    user_name = params.get("user_name")
    if not user_name:
        return next_console_response(error_status=True, error_code=1004, error_message="用户名不能为空！")
    return create_user(params)


@app.route('/next_console_admin/management_center/management/user/lookupbyadmin', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin", "next_console_reader_admin"])
@jwt_required()
def admin_lookup_user_details():
    """
    管理员查询用户详情

    请求参数:
    - JSON格式请求体，包含筛选条件和分页参数

    返回:
    - 符合条件的用户列表及相关信息
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookup_user_details_admin(params)


@app.route('/next_console_admin/management_center/management/user/updateroleadmin', methods=['POST'])
@roles_required(["admin", "super_admin"])
@jwt_required()
def admin_update_user_role():
    """
    管理员更新用户角色

    请求参数:
    - JSON格式请求体，必须包含:
      - update_user_id: 待更新用户ID(整数)
      - dest_role_desc: 目标角色描述(列表)

    返回:
    - 角色更新操作的结果
    - 失败时返回错误信息
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    update_user_id = params.get("update_user_id")
    dest_role_desc = params.get("dest_role_desc")
    if update_user_id is None:
        return next_console_response(error_status=True, error_code=1004, error_message="参数update_user_id不能为空！")
    elif not isinstance(update_user_id, int):
        return next_console_response(error_status=True, error_code=1004, error_message="参数update_user_id格式错误！")
    elif not dest_role_desc:
        return next_console_response(error_status=True, error_code=1004, error_message="用户不能没有角色！")
    elif not isinstance(dest_role_desc, list):
        return next_console_response(error_status=True, error_code=1004,
                                     error_message="参数dest_role_desc应为列表格式！")
    return update_user_role_admin(params)


@app.route('/next_console_admin/management_center/management/user/updateuserstatusadmin', methods=['POST'])
@roles_required(["admin", "super_admin", "next_console_admin", "next_console_reader_admin"])
@jwt_required()
def user_status_update_admin():
    """
    管理员更新用户归档状态

    请求参数:
    - JSON格式请求体，必须包含:
      - update_user_id: 待更新用户ID
      - orig_is_archive: 原归档状态(整数)
      - dest_is_archive: 目标归档状态(整数)

    返回:
    - 归档状态更新操作的结果
    - 失败时返回错误信息
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    update_user_id = params.get("update_user_id")
    orig_is_archive = params.get("orig_is_archive")
    dest_is_archive = params.get("dest_is_archive")
    if update_user_id is None:
        return next_console_response(error_status=True, error_code=1004, error_message="参数update_user_id不能为空！")
    elif orig_is_archive is None:
        return next_console_response(error_status=True, error_code=1004, error_message="参数orig_is_archive不能为空！")
    elif not isinstance(orig_is_archive, int):
        return next_console_response(error_status=True, error_code=1004, error_message="参数orig_is_archive格式错误！")
    elif dest_is_archive is None:
        return next_console_response(error_status=True, error_code=1004, error_message="参数dest_is_archive不能为空！")
    elif not isinstance(dest_is_archive, int):
        return next_console_response(error_status=True, error_code=1004, error_message="参数dest_is_archive格式错误！")
    if orig_is_archive == dest_is_archive:
        return next_console_response(error_status=True, error_code=2001, error_message="原归档状态与目标归档状态相同！")
    return update_user_status_admin(params)


@app.route('/next_console_admin/management_center/management/user/updateuseraccounttypeadmin', methods=['POST'])
@roles_required(["super_admin", "next_console_admin"])
@jwt_required()
def user_company_update_admin():
    """
    管理员更新用户所属公司、所属部门

    请求参数:
    - JSON格式请求体，必须包含:
      - update_user_id: 待更新用户ID
      - user_account_type: 用户账号类型
      - dest_company_id: 目标公司ID
      - dest_department_id: 目标部门ID

    返回:
    - 用户所属公司、所属部门更新操作的结果
    - 失败时返回错误信息
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    update_user_id = params.get("update_user_id")
    user_account_type = params.get("user_account_type")
    dest_company_id = params.get("dest_company_id")
    dest_department_id = params.get("dest_department_id")
    if update_user_id is None:
        return next_console_response(error_status=True, error_code=1004, error_message="参数update_user_id不能为空！")
    if user_account_type is None:
        return next_console_response(error_status=True, error_code=1004, error_message="参数user_account_type不能为空！")
    # 仅支持变更为企业账号
    if user_account_type not in ["企业账号"]:
        return next_console_response(error_status=True, error_message="仅支持变更为企业账号！")
    else:
        if dest_company_id is None:
            return next_console_response(error_status=True, error_code=1004,
                                         error_message="参数dest_company_id不能为空！")
        elif dest_department_id is None:
            return next_console_response(error_status=True, error_code=1004,
                                         error_message="参数dest_department_id不能为空！")
    return update_user_company_admin(params)


@app.route('/next_console_admin/management_center/management/user/all_company/search', methods=["POST"])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def all_company_search():
    """
    管理员查询所有公司
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return search_all_company()


@app.route('/next_console_admin/management_center/management/user/company/lookupbytwadmin', methods=["POST"])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def twadmin_lookup_company():
    """
    平台管理员查询公司详情列表
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookup_company_twadmin(params)


@app.route('/next_console_admin/management_center/management/user/company/addbytwadmin', methods=["POST"])
@roles_required(["next_console_admin"])
@jwt_required()
def twadmin_add_company():
    """
    平台管理员新增公司
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    company_code = params.get("company_code")
    company_name = params.get("company_name")
    if not company_code:
        return next_console_response(error_status=True, error_code=1004, error_message="公司编码不能为空！")
    if not company_name:
        return next_console_response(error_status=True, error_code=1004, error_message="公司名称不能为空！")
    return add_company_twadmin(params)


@app.route('/next_console_admin/management_center/management/user/company/updatebyadmin', methods=["POST"])
@roles_required(["next_console_admin"])
@jwt_required()
def twadmin_update_company():
    """
    平台管理员更新公司
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    company_id = params.get("company_id")
    if not company_id:
        return next_console_response(error_status=True, error_code=1004, error_message="公司ID不能为空！")
    return update_company_twadmin(params)


@app.route('/next_console_admin/management_center/management/user/department/lookupbyadmin', methods=["POST"])
@roles_required(["admin", "super_admin"])
@jwt_required()
def admin_lookup_department():
    """
    平台管理员查询部门详情列表
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookup_department_admin(params)


@app.route('/next_console_admin/management_center/management/user/department/lookupbytwadmin', methods=["POST"])
@roles_required(["next_console_admin", "next_console_reader_admin"])
@jwt_required()
def twadmin_lookup_department():
    """
    平台管理员查询部门详情列表
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    return lookup_department_twadmin(params)


@app.route('/next_console_admin/management_center/management/user/department/addbytwadmin', methods=["POST"])
@roles_required(["next_console_admin"])
@jwt_required()
def twadmin_add_department():
    """
    平台管理员添加部门
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    department_name = params.get("department_name")
    department_code = params.get("department_code")
    parent_department_id = params.get('parent_department_id')
    company_id = params.get("company_id")
    if not department_name:
        return next_console_response(error_status=True, error_code=1004, error_message="部门名称不能为空！")
    if not department_code:
        return next_console_response(error_status=True, error_code=1004, error_message="部门编码不能为空！")
    if not company_id:
        return next_console_response(error_status=True, error_code=1004, error_message="公司ID不能为空！")
    if not parent_department_id:
        return next_console_response(error_status=True, error_code=1004, error_message="父部门ID不能为空！")
    return add_department_twadmin(params)


@app.route('/next_console_admin/management_center/management/user/department/updatebytwadmin', methods=["POST"])
@roles_required(["next_console_admin"])
@jwt_required()
def twadmin_update_department():
    """
    平台管理员更新部门
    """
    params = request.json
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    department_id = params.get("department_id")
    if not department_id:
        return next_console_response(error_status=True, error_code=1004, error_message="部门ID不能为空！")
    return update_department_twadmin(params)


@app.route('/next_console_admin/management_center/management/user/close', methods=['POST'])
@roles_required(["super_admin", "next_console_admin"])
@jwt_required()
def admin_user_close():
    """
    新增用户
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    user_code = params.get("user_code")
    if not user_code:
        return next_console_response(error_status=True, error_code=1004, error_message="用户编号不能为空！")
    return admin_close_user_service(params)


@app.route('/next_console_admin/management_center/management/user/update', methods=['POST'])
@roles_required(["super_admin", "next_console_admin"])
@jwt_required()
def admin_user_update():
    """
    新增用户
    :return:
    """
    params = request.get_json()
    user_id = get_jwt_identity()
    params["user_id"] = user_id
    user_code = params.get("user_code")
    if not user_code:
        return next_console_response(error_status=True, error_code=1004, error_message="用户编号不能为空！")
    return admin_update_user_service(params)
