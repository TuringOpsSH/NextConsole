from app.app import app
from app.services.configure_center.response_utils import next_console_response


@app.route('/hello_world', methods=['GET', 'POST'])
def hello_world():
    """
    针对具体巡检项的结果、分析 生成整改方案
    包括 变更脚本，回退脚本
    """
    return next_console_response(result="你好，我是NextConsoleAdmin，有什么可以帮助你的吗？")

