import subprocess
# import os
# from skywalking import agent, config
command = "grep -c ^processor /proc/cpuinfo"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
if result.returncode == 0:
    output = int(result.stdout.strip())
else:
    output = 5

bind = '0.0.0.0:5011'
workers = 8
timeout = 6000
