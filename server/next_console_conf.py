import subprocess
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)

# 获取 CPU 核心数
command = "grep -c ^processor /proc/cpuinfo"
result = subprocess.run(command, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    try:
        output = int(result.stdout.strip())
    except ValueError as e:
        logging.error(f"Failed to parse CPU count: {e}")
        output = 5
else:
    logging.error(f"Failed to get CPU count: {result.stderr}")
    output = 5

# 配置 Gunicorn
bind = '0.0.0.0:5123'  # 绑定到所有网络接口
# workers = (output * 2 + 1)
timeout = 30
# logging.info(f"Gunicorn configured with {workers} workers")