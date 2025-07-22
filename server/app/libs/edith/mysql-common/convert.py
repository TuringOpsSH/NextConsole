import getopt
import json
import logging
import os
import sys
import chardet
from collections import namedtuple, defaultdict
import re
import traceback
import xml.etree.ElementTree as ET



def log():
    log_dir = './logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'app.log')
    if not os.path.isfile(log_file):
        open(log_file, 'a').close()

    logging.basicConfig(level=logging.INFO, filename=log_file, encoding='UTF-8',
                        filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

class EOut:
    def __init__(self, filename, logencoding):
        self.filename = filename
        self.lines = self.read_file(filename, logencoding)

    @staticmethod
    def is_gbk(data):
        result = chardet.detect(data)
        return result['encoding'] == 'gbk'

    @staticmethod
    def read_file(filename, logencoding):
        with open(filename, 'rb') as file:
            byte_content = file.read()

        if EOut.is_gbk(byte_content) or logencoding.lower() == "gbk":
            content = byte_content.decode('gb18030', errors='ignore')
        else:
            content = byte_content.decode('utf-8', errors='ignore')

        return content.replace('\r\n', '\n').split('\n')

    def get_instances(self):
        instances = []
        for line in self.lines:
            if line.startswith("${edith:") and line.endswith("}"):
                instance = ""
                if "@" in line:
                    instance = line.replace("${edith:", "").replace("}", "").split("@")[1]
                    if " " in instance:
                        instance = instance.split(" ")[0]

                if instance not in instances:
                    instances.append(instance)
        return instances

    def get_items(self, instance):
        items = []
        for line in self.lines:
            if line.startswith("${edith:") and line.endswith("}"):
                if "${edith:" in line and "@" not in line:
                    item = line.replace("${edith:", "", 1).replace("}", "", 1).strip()
                    if item not in items:
                        items.append(item)
                elif f"@{instance} " in line or f"@{instance}" in line:
                    item = line.replace("${edith:", "", 1).replace("}", "", 1).split("@")[0]
                    if item not in items:
                        items.append(item)
        return items

    def get_msg(self, instance, item):
        lines = []
        will_append = False
        for line in self.lines:
            if line.endswith("}"):
                if line.startswith("${edith:") and "@" not in line:
                    will_append = True
                    continue

                if line.startswith(f"${{edith:{item}@{instance} ") or line.startswith(f"${{edith:{item}@{instance}}}"):
                    will_append = True
                    continue

            if will_append and line.startswith("${edith:") and line.endswith("}"):
                break

            if will_append:
                if '< ?xml version = "1.0"? >' in line or len(line) == 0:
                    continue
                lines.append(line)

        return lines


    def get_lines(self, instance, item):
        lines = []
        will_append = False
        for line in self.lines:
            if line.endswith("}"):
                if line.startswith("${edith:") and "@" not in line:
                    will_append = True
                    continue

                if line.startswith(f"${{edith:{item}@{instance} ") or line.startswith(f"${{edith:{item}@{instance}}}"):
                    will_append = True
                    continue

            if will_append and line.startswith("${edith:") and line.endswith("}"):
                break

            if will_append:
                lines.append(line)

        return lines

    def get_string(self, instance, item):
        lines = self.get_lines(instance, item)
        return "\n".join(lines)


class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def load_eout_group_by_instance_and_family(filename,outpath, logencoding):
    eout = EOut(filename, logencoding)

    instances = eout.get_instances()
    for instance in instances:
        confdata = {}
        statusdata = {}
        logdata = {}

        items = eout.get_items(instance)
        for item in items:
            if item == "host":
                d = eout.get_msg(instance, item)
                if len(d) == 0:
                    continue
                content = '\n'.join(d)
                # 将XML字符串转换为ElementTree对象
                xmlStr = ET.fromstring(content)
                fields = xmlStr.findall('.//field')
                host_dict = {}
                for field in fields:
                    host_dict[field.get('name')] = field.text
                logdata[item] = host_dict
                confdata[item] = host_dict
                statusdata[item] = host_dict
            elif item == "port":
                d = eout.get_msg(instance, item)
                if len(d) == 0:
                    continue
                content = '\n'.join(d)
                # 将XML字符串转换为ElementTree对象
                xmlStr = ET.fromstring(content)
                fields = xmlStr.findall('.//field')
                port_dict = {}
                for field in fields:
                    port_dict[field.get('name')] = field.text
                logdata[item] = port_dict.get("port")
                confdata[item] = port_dict.get("port")
                statusdata[item] = port_dict.get("port")
            elif item == "ipaddr":
                d = eout.get_msg(instance, item)
                if len(d) == 0:
                    continue
                content = '\n'.join(d)
                # 将XML字符串转换为ElementTree对象
                xmlStr = ET.fromstring(content)
                fields = xmlStr.findall('.//field')
                ip_dict = {}
                for field in fields:
                    ip_dict["ips"] = [{"eth0": field.text}]
                logdata["edith"] = ip_dict
                confdata["edith"] = ip_dict
                statusdata["edith"] = ip_dict
            else:
                list = []
                d = eout.get_msg(instance, item)
                if len(d) == 0:
                    continue

                resultset_blocks = []
                current_block = []
                in_resultset = False

                # 遍历每一行
                for line in d:
                    # 检查是否是resultset的开始
                    if line.strip().startswith('<resultset'):
                        in_resultset = True
                        current_block = [line]
                    # 如果在resultset块内,继续添加行
                    elif in_resultset:
                        current_block.append(line)
                        # 检查是否是resultset的结束
                        if line.strip() == '</resultset>':
                            in_resultset = False
                            resultset_blocks.append(current_block)


                for block in resultset_blocks:
                    cur_list = []
                    content = '\n'.join(block)
                    try:
                        xmlStr = ET.fromstring(content)
                        rows = xmlStr.findall('row')
                    except Exception as e:
                        rows = []
                    for row in rows:
                        fields = row.findall('field')
                        dict_tmp = {}
                        for field in fields:
                            dict_tmp[field.get('name')] = field.text
                        cur_list.append(dict_tmp)
                    list.append(cur_list)
                if len(list) == 0:
                    logdata[item] = None
                else:
                    logdata[item] = list

        #eout转换成json格式数据输出
        commonName = '.'.join(filename.split(".")[1:-1])
        confName = "MySQLConf." + commonName + ".json"
        logName = "MySQLLog." + commonName + ".json"
        statusName = "MySQLStatus." + commonName + ".json"
        with open(os.path.join(outpath, confName), "w") as f:
            f.write(json.dumps(confdata, indent=4))
        with open(os.path.join(outpath, logName), "w") as f:
            f.write(json.dumps(logdata, indent=4))
        with open(os.path.join(outpath, statusName), "w") as f:
            f.write(json.dumps(statusdata, indent=4))

    return


def run():
    datadir = ""

    opts, args = getopt.getopt(
        sys.argv[1:], "hv", ["datadir="])

    #datapath = r'E:\中亦安图\项目\数据工具部\工作内容\mysql新需求开发\测试数据'
    #opts = [('--datadir', datapath)]

    for opt, value in opts:
        if opt == "--datadir":
            datadir = value.strip()


    fileList = []
    for dirpath, dirnames, filenames in os.walk(datadir):
        for filename in filenames:
            fileList.append(os.path.join(dirpath, filename))

    if len(fileList) == 0:
        # 没有找到数据,抛出一个异常
        raise CustomError("没有找到数据，请设置全局数据目录")
        sys.exit(1)


    for file in fileList:
        fileName = os.path.basename(file)
        # 获取文件后缀
        fileSuffix = fileName.split(".")[-1]

        if fileSuffix != "eout":
            continue

        load_eout_group_by_instance_and_family(file,datadir, "")



if __name__ == '__main__':
    try:
        logger = log()
        run()
        logger.info("****转换成功****")
    except Exception as e:
        # IDE中查看错误堆栈
        print(traceback.print_exc())
        # Edith Desk中显示错误堆栈
        logger.error("提取【失败】，原因请查看操作日志", exc_info=True)

