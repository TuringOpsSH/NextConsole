import os
import getopt
import re
import sys

datadir = ""
try:
    opts, args = getopt.getopt(sys.argv[1:], "hv", ["datadir="])
    for opt, value in opts:
        if opt == "--datadir":
            datadir = value.strip("\"")
except Exception as e:
    print(e)
    sys.exit(1)

if datadir == "":
    sys.exit(1)

def replace_ip(file_name):
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    match = re.search(ip_pattern, file_name)
    if match:
        ip = match.group()
        new_ip = ip.replace('.', '%')
        return file_name.replace(ip, new_ip)
    else:
        return file_name

for root, dirs, files in os.walk(datadir):
    for file_name in files:
        if file_name.endswith(".json"):
            new_name = replace_ip(file_name)
            if new_name != file_name:
                os.rename(os.path.join(root, file_name), os.path.join(root, new_name)) 