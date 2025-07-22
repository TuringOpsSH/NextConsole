#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def nginx_analysis(output_dir, ip):
    nginx_file = output_dir + "/data/" + ip + "_nginx.txt"
    if not os.path.exists(nginx_file):
        return list()
    dict_list = utils.json_to_format_dict_list(nginx_file)
    analysis_dict_list = list()
    for item in dict_list:
        item["max_connections"]  = 0
        item["nginx_conf"]  = ''
        nginx_dict = dict()
        nginx_dict["进程类型："] = ["nginx", "", "", ""]
        nginx_dict["进程ID"] = ["",
                              "进程信息标记",
                              item["PID"],
                              "当前进程的PID"]

        nginx_dict["进程命令行"] = ["",
                               "进程信息标记",
                               item["CMD"],
                               "当前进程的命令行"]

        # if "uptime_in_seconds" in item:
        #     seconds_to_days = int(int(item["uptime_in_seconds"]) / 86400)
        #     check_result = PASS if seconds_to_days < 730 else FAIL
        #     nginx_dict["运行天数"] = [check_result,
        #                           "小于2年",
        #                           str(seconds_to_days),
        #                           "当前nginx进程持续运行的天数"]

        check_result = PASS if item["UID"] != "root" else FAIL
        nginx_dict["运行用户"] = [check_result,
                              "为减小受外部攻击时的影响面，建议使用非root用户运行进程",
                              item["UID"],
                              "运行nginx的用户"]

        nginx_dict["监听端口"] = ["", '端口处于正常监听状态', "".join(item["port"]).rstrip(), ""]

        check_result = PASS if float(item["cpu_usage"]) < float(80) else FAIL
        nginx_dict["进程CPU使用率"] = [check_result,
                                  "小于80%",
                                  item["cpu_usage"],
                                  "当前nginx进程的CPU占用率（%）"]

        check_result = PASS if float(item["mem_usage"]) < float(80) else FAIL
        nginx_dict["进程内存使用率"] = [check_result,
                                 "小于80%",
                                 item["mem_usage"],
                                 "当前nginx进程的内存占用率（%）"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 40000 else FAIL
            nginx_dict["进程最大文件数(硬限制)"] = [check_result,
                                          "大于 40000",
                                          item["max_open_files"],
                                          "当前nginx进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = "符合" if int(item["lsof_count"]) < target_num else "不符合"
                nginx_dict["lsof_count"] = [check_result,
                                            "小于max_open_files * 80% = " + str(target_num),
                                            str(item["lsof_count"]),
                                            "当前进程的句柄使用数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = "符合" if int(item["max_open_files_s"]) > 20000 else "不符合"
            nginx_dict["进程最大文件数(软限制)"] = [check_result,
                                          "大于 20000",
                                          item["max_open_files_s"],
                                          "当前nginx进程使用句柄数超过这个值，则会产生告警(软限制)"]

        check_result = PASS if utils.version_to_num(item["nginx_version"]) > utils.version_to_num("1.20.1") else FAIL
        nginx_dict["nginx_version"] = [check_result,
                                       "大于1.20.1 ",
                                       item["nginx_version"],
                                       "1.20.1以前版本存在较多安全漏洞，建议升级到当前最新稳定版：1.22.1"]
        if "worker_processes" in item:
            item["worker_processes"] = item["cpu_count"] if item["worker_processes"] == "auto" else item[
                "worker_processes"]
            item["max_connections"] = int(item["worker_connections"]) * int(item["worker_processes"])

        if "worker_processes" in item and "cpu_count" in item:
            check_result = "符合" if int(item["worker_processes"]) >= int(item["cpu_count"]) else "不符合"
            nginx_dict["worker_processes"] = [check_result,
                                              "大于等于当前主机CPU核数 = " + str(item["cpu_count"]),
                                              item["worker_processes"],
                                              "当前nginx工作进程(worker)的数量"]
            nginx_dict["worker进程数"] = ["",
                                       "",
                                       item["worker_processes"],
                                       "当前nginx工作进程(worker)的数量"]


        check_result = PASS if int(item["max_connections"]) >= 2048 else FAIL
        nginx_dict["nginx最大连接数"] = [check_result,
                                    "大于等于2048",
                                    str(item["max_connections"]),
                                    "nginx支持的最大连接数量，反向代理/正向代理场景下实际承载并发需要除4"]

        if "netstat_count" in item:
            target_num = 5000
            if "max_connections" in item:
                target_num = int(int(item["max_connections"]) * 0.8)
            check_result = PASS if int(item["netstat_count"]) < target_num else FAIL
            nginx_dict["netstat_count"] = [check_result,
                                           "小于max_connections * 80% = " + str(target_num),
                                           item["netstat_count"],
                                           "与当前nginx连接的各tcp状态连接的数量总和"]

        check_result = PASS if "server_tokens" in item and item["server_tokens"] == "off" else FAIL
        nginx_dict["server_tokens"] = [check_result,
                                       "off",
                                       "" if "server_tokens" not in item else item["server_tokens"],
                                       "是否禁用nginx版本信息显示"]

        if "访问日志" in item:
            nginx_dict["access_log"] = [MAN,
                                        "无异常错误信息", "见备注",
                                        str(utils.convert(item["access_log"]))]
        if "错误日志" in item:
            nginx_dict["error_logs"] = [MAN,
                                        "无异常错误信息", "见备注",
                                        str(utils.convert(item["error_logs"]))]

        nginx_dict["nginx配置文件路径"] = ["",
                                     "nginx配置文件",
                                     item["nginx_conf"],
                                     "nginx配置文件路径"]

        if "config_content" in item:
            nginx_dict["nginx配置信息"] = ["",
                                       "无异常配置信息",
                                       "".join(item["config_content"]).rstrip(),
                                       "nginx配置"]

        analysis_dict_list.append(nginx_dict)

    return analysis_dict_list
