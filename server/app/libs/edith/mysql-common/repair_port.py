import sys,getopt

datadir = ""
try:
    opts, args = getopt.getopt(sys.argv[1:], "hv", ["datadir=", ])
    for opt, value in opts:
        if opt == "--datadir":
            datadir = value.strip()

except Exception as e:
    print(e)
    sys.exit(1)

import os,json
for file in os.listdir(datadir):
    if file.endswith(".json"):
        data = {}
        with open(os.path.join(datadir, file), "r", encoding="UTF-8") as f:
            data = json.loads(f.read())
            port = file.split(".")[1]
            if "port" not in data:
                print(file)
                if file.startswith("MySQLConf."):
                    with open(os.path.join(datadir, file), "w", encoding="UTF-8") as w:
                        data["port"] = port
                        w.write(json.dumps(data))
                if file.startswith("MySQLLog."):
                    with open(os.path.join(datadir, file), "w", encoding="UTF-8") as w:
                        data["port"] = port
                        w.write(json.dumps(data))
                if file.startswith("MySQLStatus."):
                    with open(os.path.join(datadir, file), "w", encoding="UTF-8") as w:
                        data["port"] = [{"metric": port,"datetime":"2023-05-26 17:34:33"}]
                        w.write(json.dumps(data))