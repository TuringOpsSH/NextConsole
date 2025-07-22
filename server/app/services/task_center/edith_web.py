from app.app import celery, app, db
import os
import shutil
import subprocess
from app.utils.oss.oss_client import *
from app.utils.edith_web.edith_model import *


@celery.task
def start_generate_report(data):
    """
    生成巡检报告
    """
    config_file_path = data.get("config_file_path")
    sidoc_path = data.get("sidoc_path")
    pandoc_path = data.get("pandoc_path")
    task_type = data.get("task_type")
    report_task_id = data.get("report_task_id")
    with app.app_context():
        new_report_task = EdithReportInfo.query.filter_by(id=report_task_id).first()
        if not new_report_task:
            return "任务不存在"
        try:
            # 切换至lib目录
            lib_path = str(os.path.join(os.path.dirname(sidoc_path), task_type))
            # 将配置文件拷贝至lib目录
            shutil.copy(config_file_path, lib_path)
            run_config_file_path = str(os.path.join(lib_path, os.path.basename(config_file_path)))
            # 生成报告命令
            report_command = f"{sidoc_path} -pandoc={pandoc_path} -c={run_config_file_path} "
            result = str(subprocess.run(report_command, shell=True, capture_output=True, text=True,
                                        encoding="utf8", errors='replace').stdout)
            app.logger.warning(f"生成报告命令:{report_command}, 结果:{result}")
            new_report_task.task_trace = result
            # 判断并更新任务状态
            if not result.strip().endswith('.docx'):
                new_report_task.report_status = "异常"
                db.session.add(new_report_task)
                db.session.commit()
                return next_console_response(error_status=True, error_message="生成失败")
            new_report_task.report_status = "成功"
            # 获取报告目录下最新的一个文件路径
            report_path = result.strip().splitlines()[-1].strip()
            new_report_task.report_path = report_path
            # 生成下载链接
            new_report_task.report_download_url = generate_download_url(
                'edith_web', report_path, suffix='docx'
            ).json.get("result")
            db.session.add(new_report_task)
            db.session.commit()
            # 删除运行的配置文件
            os.remove(run_config_file_path)
        except Exception as e:
            app.logger.error(f"生成报告失败, 错误信息:{str(e)}")
            new_report_task.report_status = "异常"
            new_report_task.task_trace = str(e)
            db.session.add(new_report_task)
            db.session.commit()
            return next_console_response(error_status=True, error_message="生成失败")
        from app.utils.edith_web.edith_service import save_edith_report_to_session
        save_edith_report_to_session(new_report_task, session_id=new_report_task.session_id)
        return new_report_task.show_info()
