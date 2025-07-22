#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils
import json

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"

def replace_spec_str(str):
    return str.replace("\u001b", "").replace("[0m", "").replace("[1m", "").rstrip()

def rabbitmq_analysis(output_dir, ip):
    rabbitmq_file = output_dir + "/data/" + ip + "_rabbitmq.txt"
    if not os.path.exists(rabbitmq_file):
        return list()

    dict_list = utils.json_to_format_dict_list(rabbitmq_file)
    analysis_dict_list = list()
    for item in dict_list:
        rabbitmq_dict = dict()

        rabbitmq_dict["进程类型："] = ["rabbitmq", "", "", ""]
        rabbitmq_dict["进程ID"] = ["", "进程信息标记", item["PID"], "当前进程的PID"]
        rabbitmq_dict["进程命令行"] = ["", "进程信息标记", item["CMD"], "当前进程的命令行"]

        if "cpu_usage" in item:
            check_result = PASS if float(item["cpu_usage"]) < float(80) else FAIL
            rabbitmq_dict["cpu使用率"] = [check_result,
                                       "小于80%",
                                       item["cpu_usage"],
                                       "当前rabbitmq进程的CPU占用率（%）"]
        if "memory_usage" in item:
            check_result = PASS if float(item["memory_usage"]) < float(80) else FAIL
            rabbitmq_dict["内存使用率"] = [check_result,
                                      "小于80%",
                                      item["memory_usage"],
                                      "当前rabbitmq进程的内存占用率（%）"]
        if "user" in item:
            check_result = PASS if item["user"] != "root" else FAIL
            rabbitmq_dict["进程用户"] = [check_result,
                                     "非root用户",
                                     item["user"],
                                     "为减小被外部攻击时的影响面，建议使用普通用户对rabbitmq进程进行管理"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 40000 else FAIL
            rabbitmq_dict["最大文件数(硬限制)"] = [check_result,
                                           "大于 40000",
                                           item["max_open_files"],
                                           "当前rabbitmq进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = PASS if int(item["lsof_count"]) < target_num else FAIL
                rabbitmq_dict["当前使用文件数"] = [check_result,
                                            "小于max_open_files * 80% = " + str(target_num),
                                            str(item["lsof_count"]),
                                            "当前进程的句柄使用数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 20000 else FAIL
            rabbitmq_dict["最大文件数(软限制)"] = [check_result,
                                           "大于 20000",
                                           item["max_open_files_s"],
                                           "当前rabbitmq进程使用句柄数超过这个值，则会产生告警(软限制)"]

        if "max_user_processes" in item and item["max_user_processes"].isdigit():
            check_result = PASS if int(item["max_user_processes"]) > 40000 else FAIL
            rabbitmq_dict["最大进程数(硬限制)"] = [check_result,
                                           "大于 40000",
                                           item["max_user_processes"],
                                           "当前rabbitmq进程管理用户被允许打开的最大进程数量(硬限制)"]

        if "max_user_processes_s" in item and item["max_user_processes_s"].isdigit():
            check_result = PASS if int(item["max_user_processes_s"]) > 20000 else FAIL
            rabbitmq_dict["最大进程数(软限制)"] = [check_result,
                                           "大于 20000",
                                           item["max_user_processes_s"],
                                           "当前rabbitmq进程管理用户打开进程数超过这个值，则会产生告警(软限制)"]
        if "netstat_count" in item:
            check_result = PASS if int(item["netstat_count"]) < 8000 else FAIL
            rabbitmq_dict["netstat_count"] = [check_result,
                                              "小于 8000",
                                              "".join(item["netstat_count"]).rstrip(),
                                              "与当前rabbitmq连接的各tcp状态连接的数量总和"]

        if "uptime_in_seconds" in item:
            seconds_to_days = int(int(item["uptime_in_seconds"]) / 86400)
            check_result = PASS if seconds_to_days < 730 else FAIL
            rabbitmq_dict["运行天数"] = [check_result,
                                     "小于2年",
                                     str(seconds_to_days),
                                     "当前rabbitmq进程持续运行的天数"]
        if "list_users" in item:
            flag = 0
            for line in item["list_users"]:
                if "guest" in line:
                    flag = 1
                    break
            check_result = PASS if flag == 0 else FAIL
            rabbitmq_dict["用户列表"] = [check_result, '使用自己创建的用户，并且默认用户(guest)已删除',
                                     replace_spec_str("".join(item["list_users"])),
                                     "当前rabbitmq所包含的用户列表"]
        if "list_permissions" in item:
            rabbitmq_dict["权限列表"] = ['人工复核', '用户设置合理权限', replace_spec_str("".join(item["list_permissions"])).rstrip(),
                                     '当前rabbitmq用户的权限信息']
        if "list_queues" in item:
            rabbitmq_dict["队列列表"] = ['人工复核', '每个队列积压的msg少于1000条',
                                     replace_spec_str("".join(item["list_queues"])).rstrip(),
                                     '当前rabbitmq的队列列表']

        if "list_unresponsive_queues" in item:
            check_result = PASS if len(item["list_unresponsive_queues"]) == 1 else FAIL
            rabbitmq_dict["无响应队列列表"] = [check_result, '不存在无响应队列',
                                        replace_spec_str("".join(item["list_unresponsive_queues"])).rstrip(),
                                        '当前rabbitmq中无响应的队列列表']
        if "node_health_check" in item:
            flag = 0
            for line in item["node_health_check"]:
                if "Health check passed" in line:
                    flag = 1
                    break
            check_result = PASS if flag == 1 else FAIL
            rabbitmq_dict["健康检查"] = [check_result, 'Health check passed',
                                     replace_spec_str("".join(item["node_health_check"])).rstrip(),
                                     '当前rabbitmq服务健康状态检查']
        if "cluster_status" in item:
            flag = 0
            for line in item["cluster_status"]:
                if "{partitions,[]}" in line:
                    flag = 1
                    break
            check_result = PASS if flag == 1 else MAN
            rabbitmq_dict["cluster_status"] = [check_result, '无网络分区情况({partitions,[]}) 或 Network Partitions ：(none)',
                                               replace_spec_str("".join(item["cluster_status"])).rstrip(),
                                               "当前rabbitmq集群状态"]
        if "port_status" in item:
            rabbitmq_dict["端口状态"] = [MAN, '端口处于正常监听状态', replace_spec_str("".join(item["port_status"])).rstrip(), '当前mq的端口监听情况']

        if "error_logs" in item:
            rabbitmq_dict["异常日志筛选"] = [MAN,
                                       "无异常错误信息", "见备注",
                                       str(item["error_logs"])]

        if "erlang_exe" in item:
            rabbitmq_dict["erlang_exe"] = ["", "无", str(item["erlang_exe"]), "erlang可执行文件路径", ]
        if "rabbitmq_home" in item:
            rabbitmq_dict["rabbitmq_home"] = ["", "无", str(item["rabbitmq_home"]), "rabbitmq家目录"]

        if "erlang_version" in item:
            rabbitmq_dict["erlang版本"] = [MAN,
                                         "同当前rabbitmq版本适配", str(utils.convert(item["erlang_version"])),
                                         "同rabbitmq版本对应关系参考官网链接：https://www.rabbitmq.com/which-erlang.html"]
        if "rabbitmq_status" in item:
            for line in item["rabbitmq_status"]:
                if "listeners" in line:
                    rabbitmq_dict["监听配置"] = [MAN, "不建议使用默认端口(5672，15672)",
                                             line,
                                             "当前rabbitmq的监听配置"]
                if "rabbit,\"RabbitMQ\"" in line:
                    rabbitmq_dict["rabbtimq版本"] = ["", "建议使用3.7.15及以上版本",
                                                   replace_spec_str(line),
                                                   "当前rabbitmq版本"]
            rabbitmq_dict["rabbitmq_status"] = ["",
                                                "无",
                                                replace_spec_str("".join(item["rabbitmq_status"])),
                                                "rabbitmq信息总览"]

        analysis_dict_list.append(rabbitmq_dict)

    return analysis_dict_list
