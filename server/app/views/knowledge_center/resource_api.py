from app.app import app
from app.models.resource_center.resource_model import ResourceObjectMeta
from flask import request, send_file, abort
from werkzeug.utils import secure_filename
import os


@app.route('/next_console/knowledge_center/resource_images', methods=['GET'])
def resource_tmp_download():
    """
    获取临时下载链接
    """
    resource_id = request.args.get('resource_id')
    if not resource_id:
        return {'error': 'resource_id parameter is required'}, 400
    try:
        resource = ResourceObjectMeta.query.filter(
            ResourceObjectMeta.id == resource_id,
            ResourceObjectMeta.resource_status == "正常"
        ).first()
        if not resource:
            return {'error': 'Resource not found'}, 404
        if not resource.resource_path:
            return {'error': 'Resource file not found'}, 404
        if not os.path.exists(resource.resource_path):
            return {'error': 'Resource file does not exist'}, 404
        if resource.resource_type not in ['image', 'video', 'audio', 'file', 'media']:
            return {'error': 'Unsupported resource type'}, 400
        # 安全处理文件名
        filename = secure_filename(resource.resource_name)

        # 发送文件
        return send_file(
            resource.resource_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    except Exception as e:
        return {'error': str(e)}, 500