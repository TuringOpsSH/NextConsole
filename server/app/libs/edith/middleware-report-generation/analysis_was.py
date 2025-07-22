#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

from bs4 import BeautifulSoup

import utils

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def was_analysis(output_dir, ip, java_list):
    was_file = output_dir + "/data/" + ip + "_was.txt"
    if not os.path.exists(was_file):
        return list()
    dict_list = utils.json_to_format_dict_list(was_file)
    for item in dict_list:
        was_dict = dict()
        was_dict["进程ID"] = ["",
                            "进程信息标记",
                            item["PID"],
                            "当前进程的PID"]

        was_dict["进程命令行"] = ["",
                             "进程信息标记",
                             item["CMD"],
                             "当前进程的命令行"]

        was_dict["监听端口"] = ['', '端口处于正常监听状态', "" if "port" not in item else item["port"], ""]
        was_dict["server_name"] = ['', '', item["server_name"], ""]
        was_dict["运行日志检查"] = [MAN,
                              "异常日志检查",
                              "".join(item["log"]).rstrip(),
                              "日志中存在异常输出，需要人工复查"
                              ]

        was_dict["运行日志路径"] = ["",
                              "",
                              item["log_file"],
                              "运行日志路径"]
        for java_dict in java_list:
            if java_dict["进程ID"] == was_dict["进程ID"]:
                java_dict["进程类型："] = ["was", "", "", ""]
                for k in was_dict:
                    java_dict[k] = was_dict[k]
                java_dict.pop("OOM转储参数")
                java_dict.pop("JDK版本")
                if "元空间上限" in java_dict:
                    java_dict.pop("元空间上限")
                if "方法区上限" in java_dict:
                    java_dict.pop("方法区上限")