#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def httpd_analysis(output_dir, ip):
    httpd_file = output_dir + "/data/" + ip + "_httpd.txt"
    if not os.path.exists(httpd_file):
        return list()
    dict_list = utils.json_to_format_dict_list(httpd_file)
    analysis_dict_list = list()
    for item in dict_list:
        httpd_dict = dict()
        httpd_dict["进程类型："] = ["httpd", "", "", ""]
        httpd_dict["进程ID"] = ["",
                              "进程信息标记",
                              item["PID"],
                              "当前进程的PID"]

        httpd_dict["进程命令行"] = ["",
                               "进程信息标记",
                               item["CMD"],
                               "当前进程的命令行"]

        check_result = PASS if item["UID"] != "root" else FAIL
        httpd_dict["运行用户"] = [check_result,
                              "为减小受外部攻击时的影响面，建议使用非root用户运行进程",
                              item["UID"],
                              "运行httpd的用户"]

        httpd_dict["监听端口"] = ["", '端口处于正常监听状态', "".join(item["port"]).rstrip(), ""]

        check_result = PASS if float(item["cpu_usage"]) < float(80) else FAIL
        httpd_dict["进程CPU使用率"] = [check_result,
                                  "小于80%",
                                  item["cpu_usage"],
                                  "当前httpd进程的CPU占用率（%）"]

        check_result = PASS if float(item["mem_usage"]) < float(80) else FAIL
        httpd_dict["进程内存使用率"] = [check_result,
                                 "小于80%",
                                 item["mem_usage"],
                                 "当前httpd进程的内存占用率（%）"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 40000 else FAIL
            httpd_dict["进程最大文件数(硬限制)"] = [check_result,
                                          "大于 40000",
                                          item["max_open_files"],
                                          "当前httpd进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = "符合" if int(item["lsof_count"]) < target_num else "不符合"
                httpd_dict["lsof_count"] = [check_result,
                                            "小于max_open_files * 80% = " + str(target_num),
                                            str(item["lsof_count"]),
                                            "当前进程的句柄使用数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = "符合" if int(item["max_open_files_s"]) > 20000 else "不符合"
            httpd_dict["进程最大文件数(软限制)"] = [check_result,
                                          "大于 20000",
                                          item["max_open_files_s"],
                                          "当前httpd进程使用句柄数超过这个值，则会产生告警(软限制)"]

        check_result = PASS if utils.version_to_num(item["httpd_version"]) > utils.version_to_num("2.4.50") else FAIL
        httpd_dict["httpd_version"] = [check_result,
                                       "大于2.4.50",
                                       item["httpd_version"],
                                       "2.4.50前版本存在较多安全漏洞，建议升级到当前较新稳定版"]

        if "netstat_count" in item:
            check_result = PASS if int(item["netstat_count"]) < 5000 else FAIL
            httpd_dict["netstat_count"] = [check_result,
                                           "小于5000",
                                           item["netstat_count"],
                                           "与当前httpd连接的各tcp状态连接的数量总和"]

        check_result = PASS if "options_index" not in item else FAIL
        httpd_dict["options_index"] = [check_result,
                                       "Options FollowSymLinks",
                                       "" if "options_index" not in item else item["options_index"],
                                       "禁止Apache列表显示文件（文件服务器忽略该配置项）"]

        check_result = PASS if "server_signature" in item and str(item["server_signature"]).upper() == "OFF" else FAIL
        httpd_dict["server_signature"] = [check_result,
                                          "ServerSignature Off",
                                          "Null" if "server_signature" not in item else item["server_signature"],
                                          "404页面、目录列表等页面的底部是否显示版本信息"]

        check_result = PASS if "server_tokens" in item and str(item["server_tokens"]).upper() == "PROD" else FAIL
        httpd_dict["server_tokens"] = [check_result,
                                       "ServerTokens Prod",
                                       "Null" if "server_tokens" not in item else item["server_tokens"],
                                       "这个指令是用来控制服务器回应给客户端的Server应答头是否包含关于服务器操做系统类型和编译进的模块描述信息。"]

        check_result = PASS if "trace_enable" in item and str(item["trace_enable"]).upper() == "OFF" else FAIL
        httpd_dict["trace_enable"] = [check_result,
                                      "TraceEnable Off",
                                      "Null" if "trace_enable" not in item else item["trace_enable"],
                                      "是否禁用TRACE请求"]
        if "test_cgi_is_del" in item:
            check_result = PASS if item["test_cgi_is_del"] == "0" else FAIL
            httpd_dict["test_cgi_is_del"] = [check_result,
                                             "APACHE_HOME/cgi-bin/test-cgi文件已删除",
                                             "目标文件计数 = " + item["test_cgi_is_del"],
                                             "是否删除安全隐患文件APACHE_HOME/cgi-bin/test-cgi"]

        if "access_log" in item:
            httpd_dict["access_log"] = [MAN,
                                        "无异常错误信息", "见备注",
                                        str(utils.convert(item["access_log"]))]
        if "error_log" in item:
            httpd_dict["error_log"] = [MAN,
                                        "无异常错误信息", "见备注",
                                        str(utils.convert(item["error_log"]))]

        if "httpd_conf" in item:
            httpd_dict["httpd主配置文件路径"] = ["",
                                          "httpd配置文件",
                                          item["httpd_conf"],
                                          "httpd配置文件路径"]

        if "main_config_content" in item:
            httpd_dict["httpd主配置信息"] = ["",
                                        "无异常配置信息",
                                        "".join(item["main_config_content"]).rstrip(),
                                        "httpd主配置信息"]

        if "include_config_content" in item:
            httpd_dict["httpd包含配置信息（Include）"] = ["",
                                                  "无异常配置信息",
                                                  "".join(item["include_config_content"]).rstrip(),
                                                  "httpd Include配置文件信息"]

        analysis_dict_list.append(httpd_dict)

    return analysis_dict_list
