#!/bin/bash
user=$(whoami)
# 尝试 source /home/$user/anaconda3/etc/profile.d/conda.sh
if ! source /home/$user/anaconda3/etc/profile.d/conda.sh; then
    # 如果 source 失败，则尝试 source /data/NextConsole/anaconda3/etc/profile.d/conda.sh
    source /data/NextConsole/anaconda3/etc/profile.d/conda.sh
fi
CONDA_ENV_NAME=next_console

# change env
conda activate $CONDA_ENV_NAME
pip install -r requirements.txt
# Find the appropriate number of workers

while getopts "m:" opt; do
  case $opt in
    m)
      export FLASK_MODEL=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done


nohup gunicorn app.app:app -c next_console_admin_conf.py --pid app/tmp/gunicorn.pid > next_console_admin.log 2>&1 &

nohup python run_admin_celery_worker.py > celery.log 2>&1 &


