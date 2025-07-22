#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def check_status(status):
    for line in status:
        if "is running" in line:
            return True
    return False


def activemq_analysis(output_dir, ip, java_list):
    activemq_file = output_dir + "/data/" + ip + "_activemq.txt"
    if not os.path.exists(activemq_file):
        return list()
    dict_list = utils.json_to_format_dict_list(activemq_file)
    for item in dict_list:
        activemq_dict = dict()

        activemq_dict["进程类型："] = ["activemq", "", "", ""]
        activemq_dict["进程ID"] = ["", "进程信息标记", item["PID"], "当前进程的PID"]
        activemq_dict["进程命令行"] = ["", "进程信息标记", item["CMD"], "当前进程的命令行"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 20000 else FAIL
            activemq_dict["最大文件数(硬限制)"] = [check_result,
                                           "大于 20000",
                                           item["max_open_files"],
                                           "当前activemq进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = PASS if int(item["lsof_count"]) < target_num else FAIL
                activemq_dict["当前使用文件数"] = [check_result,
                                            "小于max_open_files * 80% = " + str(target_num),
                                            str(item["lsof_count"]),
                                            "当前进程的句柄使用数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 20000 else FAIL
            activemq_dict["用户最大文件数(软限制)"] = [check_result,
                                             "大于 20000",
                                             item["max_open_files_s"],
                                             "当前activemq进程使用句柄数超过这个值，则会产生告警(软限制)"]
        if "max_user_processes" in item and item["max_user_processes"].isdigit():
            check_result = PASS if int(item["max_user_processes"]) > 4096 else FAIL
            activemq_dict["用户最大进程数(硬限制)"] = [check_result,
                                             "大于 4096",
                                             item["max_user_processes"],
                                             "当前activemq进程管理用户被允许打开的最大进程数量(硬限制)"]
        if "max_user_processes_s" in item and item["max_user_processes_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 4096 else FAIL
            activemq_dict["最大进程数(软限制)"] = [check_result,
                                           "大于 4096",
                                           item["max_open_files_s"],
                                           "当前activemq进程管理用户打开进程数超过这个值，则会产生告警(软限制)"]

        if "error_logs" in item:
            activemq_dict["异常日志筛选"] = [MAN,
                                       "无异常错误信息", "见备注",str(item["error_logs"])[:1000]]
        if "activemq_home" in item:
            activemq_dict["activemq_home"] = ["", "无", str(item["activemq_home"]), "activemq家目录"]

        if "activemq_xml" in item:
            activemq_dict["主配置文件路径"] = ["", "activemq.xml", str(item["activemq_xml"]), "activemq.xml配置文件位置"]
            if "activemq_xml_content" in item:
                activemq_dict["主配置文件内容总览"] = ["", "无异常配置信息", "".join(item["activemq_xml_content"]).rstrip(),
                                              "activemq.xml配置文件内容"]

        if "jetty_realm" in item:
            activemq_dict["控制台用户配置路径"] = ["", "jetty-realm.properties", "".join(item["jetty_realm"]).rstrip(), "控制台用户配置文件位置"]
            if "jetty_realm_content" in item:
                activemq_dict["控制台用户配置内容"] = [MAN, "若控制台已启用，需对默认账号密码进行修改",
                                              "".join(item["jetty_realm_content"]).rstrip(),
                                              "jetty-realm.properties配置文件内容"]

        if "version" in item:
            activemq_dict["version"] = [MAN, "建议升级至无官宣漏洞版本",
                                        "".join(item["version"]).rstrip(),
                                        "当前ActiveMQ的版本，版本参考官网链接：https://activemq.apache.org/download-archives"]
        if "status" in item:
            check_result = PASS if check_status(item["status"]) else FAIL
            activemq_dict["运行状态"] = [check_result, "当前ActiveMQ为正常运行状态(ActiveMQ is running)",
                                     "".join(item["status"]).rstrip(),
                                     "当前ActiveMQ运行状态"]
        if "data_status" in item:
            activemq_dict["内部数据情况"] = [MAN, "内部数据情况",
                                       "".join(item["data_status"]).rstrip(),
                                       "查询队列的关键数值，如队列大小，生产者消费者数量，消息出队入队统计等"]

        # 将当前activemq信息转存合并至java_dict中
        for java_dict in java_list:
            if java_dict["进程ID"] == activemq_dict["进程ID"]:
                java_dict["进程类型："] = ["activemq", "", "", ""]
                for k in activemq_dict:
                    java_dict[k] = activemq_dict[k]
