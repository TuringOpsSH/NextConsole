import shutil
import os
import getopt
import tarfile
import sys
import logging

log_dir = './logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'app.log')
if not os.path.isfile(log_file):
    open(log_file, 'a').close()

logging.basicConfig(level=logging.INFO, filename=log_file, encoding='UTF-8',
                    filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

datadir = ""
try:
    opts, args = getopt.getopt(sys.argv[1:], "hv", ["datadir="])
    for opt, value in opts:
        if opt == "--datadir":
            datadir = value.strip()
except Exception as e:
    print(e)
    sys.exit(1)

if datadir == "":
    sys.exit(1)

for filename in os.listdir(datadir):
    if filename.endswith(".tar.gz"):
        tar = tarfile.open(os.path.join(datadir, filename), "r:gz")
        tar.extractall(path=datadir)
        tar.close()


todatadir = os.path.join(datadir, 'data')
if not os.path.exists(todatadir):
    os.makedirs(todatadir)

for subdir, dirs, files in os.walk(datadir):
    if subdir != todatadir:
        for file in files:
            if file.endswith('.txt'):
                try:
                    shutil.move(os.path.join(subdir, file), todatadir)
                except Exception as e:
                    logger.warn(e)

if not os.path.exists(os.path.join(datadir, 'system_list.xlsx')):
    shutil.copy2('./templates/system_list.xlsx', datadir)

ips = []
for file in os.listdir(todatadir):
    ip = file.split('_')[0]
    if ip not in ips:
        ips.append(ip)

logging.info('* 解压完成')
logging.info('* IP 地址列表见操作日志标签\n' + '\n'.join(ips))