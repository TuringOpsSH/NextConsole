from flask import Blueprint, request

from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

blueprint = Blueprint('pufa', __name__, url_prefix='/next_console/app_center/pufa')


@blueprint.route('/convert_and_upload', methods=["GET", "POST"])
@jwt_required()
def convert_and_upload():
    """
    API端点：将Markdown表格转换为Excel并上传到第三方服务
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    from app.sub_apps.pufa.pufa_service import convert_markdown_to_excel_and_upload
    return convert_markdown_to_excel_and_upload(data)