import os
import getopt
import tarfile
import sys

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
        
        
import shutil
for subdir, dirs, files in os.walk(datadir):
    if subdir != datadir:
        for file in files:
            if file.endswith('.json'):
                shutil.move(os.path.join(subdir, file), datadir)