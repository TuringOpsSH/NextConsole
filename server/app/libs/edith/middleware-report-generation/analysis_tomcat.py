#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils
import json

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def tomcat_analysis(output_dir, ip, java_list):
    tomcat_file = output_dir + "/data/" + ip + "_tomcat.txt"
    if not os.path.exists(tomcat_file):
        return 0

    dict_list = utils.json_to_format_dict_list(tomcat_file)

    for item in dict_list:
        tomcat_dict = dict()

        tomcat_dict["进程类型："] = ["tomcat", "", "", ""]
        tomcat_dict["进程ID"] = ["", "进程信息标记", item["PID"], "当前进程的PID"]
        tomcat_dict["进程命令行"] = ["", "进程信息标记", item["CMD"], "当前进程的命令行"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 20000 else FAIL
            tomcat_dict["最大文件数(硬限制)"] = [check_result,
                                         "大于 20000",
                                         item["max_open_files"],
                                         "当前tomcat进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = PASS if int(item["lsof_count"]) < target_num else FAIL
                tomcat_dict["当前使用文件数"] = [check_result,
                                          "小于max_open_files * 80% = " + str(target_num),
                                          str(item["lsof_count"]),
                                          "当前进程的句柄使用数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 10000 else FAIL
            tomcat_dict["最大文件数(软限制)"] = [check_result,
                                         "大于 10000",
                                         item["max_open_files_s"],
                                         "当前tomcat进程使用句柄数超过这个值，则会产生告警(软限制)"]
        if "max_user_processes" in item and item["max_user_processes"].isdigit():
            check_result = PASS if int(item["max_user_processes"]) > 20000 else FAIL
            tomcat_dict["最大进程数(硬限制)"] = [check_result,
                                         "大于 20000",
                                         item["max_user_processes"],
                                         "当前tomcat进程管理用户被允许打开的最大进程数量(硬限制)"]
        if "max_user_processes_s" in item and item["max_user_processes_s"].isdigit():
            check_result = PASS if int(item["max_user_processes_s"]) > 20000 else FAIL
            tomcat_dict["最大进程数(软限制)"] = [check_result,
                                         "大于 10000",
                                         item["max_user_processes_s"],
                                         "当前tomcat进程管理用户打开进程数超过这个值，则会产生告警(软限制)"]
        if "netstat_count" in item:
            check_result = PASS if int(item["netstat_count"]) < 8000 else FAIL
            tomcat_dict["netstat_count"] = [check_result,
                                            "小于 8000",
                                            "".join(item["netstat_count"]).rstrip(),
                                            "与当前tomcat连接的各tcp状态连接的数量总和"]

        if "uptime_in_seconds" in item:
            seconds_to_days = int(int(item["uptime_in_seconds"]) / 86400)
            check_result = PASS if seconds_to_days < 730 else FAIL
            tomcat_dict["运行天数"] = [check_result,
                                   "小于2年",
                                   str(seconds_to_days),
                                   "当前tomcat进程持续运行的天数"]

        if "shutdown_cmd" in item and "shutdown_port" in item:
            check_result = FAIL if (
                    str(item["shutdown_cmd"]).upper() == "SHUTDOWN") and item["shutdown_port"] != "-1" else PASS
            tomcat_dict["shutdown端口"] = [check_result,
                                         "端口设置为-1（不开启shutdown端口），若开启该端口，请设置shutdown命令为密文串",
                                         str(item["shutdown_port"]),
                                         "为防止其他用户登录主机对tomcat进程进行telnet攻击，建议禁用shutdown端口"]
            tomcat_dict["shutdown命令"] = [check_result,
                                         "自定义shutdown命令（密文串）",
                                         str(item["shutdown_cmd"]),
                                         "为防止其他用户登录主机对tomcat进程进行telnet攻击，建议自定义加密命令为加密串"]

        if "show_report" in item and "show_server_info" in item:
            check_result = PASS if (
                    str(item["show_report"]).upper() == "FALSE" and str(
                item["show_server_info"]).upper() == "FALSE") else FAIL
            tomcat_dict["禁用版本信息显示"] = [check_result,
                                       "show_report及show_server_info均设置为flase",
                                       "show_report: " + str(item["show_report"]) + " |show_server_info: " + str(
                                           item["show_server_info"]),
                                       "为防止外部利用各版本漏洞对进程进行攻击，建议隐藏Tomcat自身版本号显示"]
        else:
            tomcat_dict["禁用版本信息显示"] = [FAIL,
                                       "show_report及show_server_info均设置为flase",
                                       "未配置",
                                       "为防止外部利用各版本漏洞对进程进行攻击，建议隐藏Tomcat自身版本号显示"]

        if "tomcat_version" in item:
            version = ""
            for line in item["tomcat_version"]:
                if "Server number" in line:
                    version = str(line).split(':')[1].strip()
            tomcat_dict["tomcat版本信息"] = ["",
                                         "建议使用各个大版本下的最新稳定小版本",
                                         version,
                                         "历史版本官方下载链接参考：http://archive.apache.org/dist/tomcat/"]
        if "connector_http" in item:
            tomcat_dict["HTTP Connector"] = ["",
                                             "为防止外部攻击，建议使用非默认（8080）端口",
                                             item["connector_http"],
                                             "当前Tomcat的 Http Connector"]

        if "connector_ajp" in item:
            tomcat_dict["AJP Connector"] = [FAIL,
                                            "在不使用AJP协议端口的情况下，建议将其关闭",
                                            item["connector_ajp"],
                                            "AJP端口开启时存在安全隐患，若未使用该协议，请将其关闭（注释掉）"]
        else:
            tomcat_dict["AJP Connector"] = [PASS,
                                            "在不使用AJP协议端口的情况下，建议将其关闭",
                                            "已注释",
                                            "AJP端口开启时存在安全隐患，若未使用该协议，请将其关闭（注释掉）"]

        if "all_dbresource" in item:
            tomcat_dict["数据源配置"] = ["",
                                    "建议对数据源用户名及密码进行加密",
                                    item["all_dbresource"],
                                    "Tomcat的数据源配置"]
        if "app_base" in item:
            tomcat_dict["AJP Connector"] = ["",
                                            "无",
                                            "".join(item["app_base"]).rstrip(),
                                            "Tomcat的应用部署目录"]
        if "app_name" in item:
            check_result = PASS
            app_names = str(item["app_name"]).split(",")
            if "docs" in app_names or "examples" in app_names or "host-manager" in app_names or "manager" in app_names:
                check_result = FAIL
            tomcat_dict["部署目录文件"] = [check_result,
                                     "示例文件docs,examples,host-manager,manager 均已删除",
                                     "".join(item["app_name"]).rstrip(),
                                     "Tomcat的应用部署目录下文件"]

        if "error_logs" in item:
            tomcat_dict["异常日志筛选"] = [MAN, "无异常错误信息", "见备注", str(item["error_logs"])[:1000]]

        if "tomcat_home" in item:
            tomcat_dict["tomcat_home"] = ["", "无", str(item["tomcat_home"]), "tomcat家目录"]

        # 将当前tomcat信息转存合并至java_dict中
        for java_dict in java_list:
            if java_dict["进程ID"] == tomcat_dict["进程ID"]:
                java_dict["进程类型："] = ["tomcat", "", "", ""]
                for k in tomcat_dict:
                    java_dict[k] = tomcat_dict[k]
