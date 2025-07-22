#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils
import json

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"

def judge_status(zk_status):
    flag = True
    for line in zk_status:
        if "Error contacting service. It is probably not running" in line:
                flag = False
                break
    return flag

def zookeeper_analysis(output_dir, ip,java_list):
    es_file = output_dir + "/data/" + ip + "_zookeeper.txt"
    if not os.path.exists(es_file):
        return 0

    dict_list = utils.json_to_format_dict_list(es_file)
    for item in dict_list:
        zk_dict = dict()
        zk_dict["进程ID"] = ["", "进程信息标记", item["PID"], "当前进程的PID"]
        zk_dict["进程命令行"] = ["", "进程信息标记", item["CMD"], "当前进程的命令行"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 40000 else FAIL
            zk_dict["最大文件数(硬限制)"] = [check_result,
                                     "大于 40000",
                                     item["max_open_files"],
                                     "当前zookeeper进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = PASS if int(item["lsof_count"]) < target_num else FAIL
                zk_dict["当前使用文件数"] = [check_result,
                                      "小于max_open_files * 80% = " + str(target_num),
                                      str(item["lsof_count"]),
                                      "当前zk进程已使用的句柄数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 20000 else FAIL
            zk_dict["最大文件数(软限制)"] = [check_result,
                                     "大于 40000",
                                     item["max_open_files_s"],
                                     "当前zookeeper进程使用句柄数超过这个值，则会产生告警(软限制)"]
        if "max_user_processes" in item and item["max_user_processes"].isdigit():
            check_result = PASS if int(item["max_user_processes"]) > 40000 else FAIL
            zk_dict["最大进程数(硬限制)"] = [check_result,
                                     "大于 40000",
                                     item["max_user_processes"],
                                     "当前zookeeper进程管理用户被允许打开的最大进程数量(硬限制)"]
        if "max_user_processes_s" in item and item["max_user_processes_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 20000 else FAIL
            zk_dict["最大进程数(软限制)"] = [check_result,
                                     "大于 20000",
                                     item["max_open_files_s"],
                                     "当前zookeeper进程管理用户打开进程数超过这个值，则会产生告警(软限制)"]

        if "error_logs" in item:
            zk_dict["异常日志筛选"] = [MAN,"无异常错误信息", "见备注",str(item["error_logs"])]
        if "client_port" in item:
            zk_dict["client连接端口"] = ["","无",str(item["client_port"]), "zookeeper 客户端连接端口(clientPort)"]


        if "mode" in item:
            check_result = PASS if str(item["mode"]).upper() != "STANDALONE" else FAIL
            zk_dict["zk启动模式"] = [check_result,
                               "以集群方式启动(非standalone)",
                               str(item["mode"]),
                               "为保证zk高可用性，建议使用集群方式对zk节点进行管理"]

        if "zk_version" in item:
            version_line = ""
            for line in item["zk_version"]:
                if "version" in line:
                    version_line = line
            zk_dict["当前zk版本"] = ["",
                               "接近最新稳定版(3.7.1)",
                               version_line,
                               "当前zk版本，建议使用较新版，参考官网链接:https://zookeeper.apache.org/releases.html"]


        if "zk_status" in item:
            check_result = PASS if judge_status(item["zk_status"]) else FAIL
            zk_dict["zk状态"] = [check_result, "正常返回zk状态信息",
                               "".join(item["zk_status"]).rstrip(),
                               "当前zk节点运行状态，异常时为：Error contacting service. It is probably not running"]

        if "config_content" in item:
            zk_dict["zk配置信息"] = ["", "无异常配置", "".join(item["config_content"]).rstrip(), "当前zk节点配置信息"]

        if "zk_get_acl" in item:
            zk_dict["zk白名单配置"] = [MAN, "允许特定IP连接zk进行指定操作",
                                  "".join(item["zk_get_acl"]).rstrip(),
                                  "当前zk白名单配置，未配置时为：'world,'anyone:cdrwa"]

        # 将当前zk信息转存合并至java_dict中
        for java_dict in java_list:
            if java_dict["进程ID"] == zk_dict["进程ID"]:
                java_dict["进程类型："] = ["zookeeper", "", "", ""]
                for k in zk_dict:
                    java_dict[k] = zk_dict[k]
