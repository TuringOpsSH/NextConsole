#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import json

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def get_console_port(http_listeners):
    console_port = 1900
    for listener_line in http_listeners:
        if "default-virtual-server" in listener_line:
            if listener_line["default-virtual-server"] == "__admin":
                console_port = listener_line["port"]
    return console_port


def check_log_config(log_config):
    log_config = log_config[0]
    if "rotation-size" in log_config and "max-history-files" in log_config:
        if int(log_config["rotation-size"]) >= 104857600 and int(log_config["max-history-files"]) >= 10:
            return True
        else:
            return False


def check_hotdeploy(hotdeploy):
    hotdeploy = hotdeploy[0]
    if "enabled" in hotdeploy:
        if hotdeploy["enabled"] == "true":
            return False
        else:
            return True


def check_hotswap(hotswap):
    hotswap = hotswap[0]
    if "enabled" in hotswap:
        if hotswap["enabled"] == "true":
            return False
        else:
            return True


def check_thread_pool(thread_pools):
    for thread_pool in thread_pools:
        if "admin" in thread_pool["name"]:
            continue
        else:
            if int(thread_pool["max-queue-size"]) != 4096:
                return False
            if int(thread_pool["max-idle-time"]) != 60000:
                return False
            if int(thread_pool["min-spare-threads"]) < 50:
                return False
            if int(thread_pool["max-threads"]) != 200:
                return False
    return True


def check_jdbc_resource(jdbc_resources):
    for jdbc_resource in jdbc_resources:
        if int(jdbc_resource["min-idle"]) != 10:
            return False
        if str(jdbc_resource["test-on-borrow"]) != "true":
            return False
        if int(jdbc_resource["max-wait-time-in-millis"]) != 60000:
            return False
        if int(jdbc_resource["max-connection-age"]) != 1800:
            return False
        if int(jdbc_resource["idle-timeout"]) != 900:
            return False
        if int(jdbc_resource["initial-pool-size"]) != 10:
            return False
        if str(jdbc_resource["sql-trace"]) != "false":
            return False
        if int(jdbc_resource["validate-atmost-once-period-in-seconds"]) != 120:
            return False
        if str(jdbc_resource["test-while-idle"]) != "true":
            return False
        if int(jdbc_resource["max-pool-size"]) != 50:
            return False
    return True


def json_to_format_dict_list(file_path):
    dict_list = list()
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as text:
            json_data_utf8 = json.load(text)
            for dict_item in json_data_utf8:
                dict_list.append(dict_item)
    except:
        with open(file_path, 'r', encoding="gbk", errors="ignore") as text:
            json_data_gbk = json.load(text)
            for dict_item in json_data_gbk:
                dict_list.append(dict_item)
    return dict_list


def version_to_num(version):
    if version is None:
        return 0
    nums = version.split(".")
    multiple = pow(10, (len(nums) - 1))
    total = 0
    for int_item in nums:
        if int_item.isdigit():
            total += int(int_item) * multiple
            multiple = multiple / 10
        else:
            total = 0
            break
    return total


def bes_analysis(output_dir, ip, java_list):
    bes_file = output_dir + "/data/" + ip + "_bes.txt"
    if not os.path.exists(bes_file):
        return 0

    dict_list = json_to_format_dict_list(bes_file)

    for item in dict_list:
        bes_dict = dict()

        bes_dict["进程类型："] = ["bes_server", "", "", ""]
        bes_dict["进程ID"] = ["", "进程信息标记", item["PID"], "当前进程的PID"]
        bes_dict["进程命令行"] = ["", "进程信息标记", item["CMD"], "当前进程的命令行"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 20000 else FAIL
            bes_dict["最大文件数(硬限制)"] = [check_result,
                                      "大于 20000",
                                      item["max_open_files"],
                                      "当前bes进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = PASS if int(item["lsof_count"]) < target_num else FAIL
                bes_dict["当前使用文件数"] = [check_result,
                                       "小于max_open_files * 80% = " + str(target_num),
                                       str(item["lsof_count"]),
                                       "当前进程的句柄使用数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 10000 else FAIL
            bes_dict["最大文件数(软限制)"] = [check_result,
                                      "大于 10000",
                                      item["max_open_files_s"],
                                      "当前bes进程使用句柄数超过这个值，则会产生告警(软限制)"]
        if "netstat_count" in item:
            check_result = PASS if int(item["netstat_count"]) < 2000 else FAIL
            bes_dict["netstat_count"] = [check_result,
                                         "小于 2000",
                                         "".join(item["netstat_count"]).rstrip(),
                                         "与当前bes连接的各tcp状态连接的数量总和"]

        if "uptime_in_seconds" in item and item["uptime_in_seconds"].isdigit():
            seconds_to_days = int(int(item["uptime_in_seconds"]) / 86400)
            check_result = PASS if seconds_to_days < 730 else FAIL
            bes_dict["运行天数"] = [check_result,
                                "连续运行超过2年的进程需要适当关注（是否还在使用，磁盘是否写满等）",
                                str(seconds_to_days),
                                "当前bes server进程持续运行的天数"]

        if "build_version" in item:
            bes_version = item["build_version"]
            check_result = PASS if version_to_num(item["build_version"]) >= version_to_num("9.5.5.7266") else FAIL
            bes_dict["bes版本信息"] = [check_result,
                                   "建议使用9.5.5.7266及以上版本",
                                   bes_version,
                                   "当前BES Server的版本号"]
        if "patch_version" in item:
            check_result = FAIL
            if item["patch_version"] is None:
                item["patch_version"] = "None"
                check_result = FAIL
            else:
                item["patch_version"] = PASS if version_to_num(item["patch_version"]) >= version_to_num("015") else FAIL
            bes_dict["补丁版本"] = [check_result,
                                "需要安装当前最新补丁（015版本）",
                                item["patch_version"],
                                "当前bes补丁版本号，当前最新为015版本"]
        if "bes_home" in item:
            check_result = PASS if item["bes_home"] == "/app/BES" else MAN
            bes_dict["bes运行目录"] = [check_result,
                                   "/app/BES",
                                   item["bes_home"],
                                   "bes家目录，本地一律采用/app/BES"]
        if "http-listener" in item:
            console_port = get_console_port(item["http-listener"])
            check_result = PASS if console_port != "1900" else FAIL
            bes_dict["控制台端口号"] = [check_result,
                                  "要求使用非默认（1900）端口",
                                  console_port,
                                  "默认为1900端口，为预防外部攻击行为，需要将其修改为非默认值（1909）"]

        if "log-service" in item:
            check_result = PASS if check_log_config(item["log-service"]) else FAIL
            bes_dict["日志配置"] = [check_result,
                                "日志切割文件大小不小于100M，且日志切割文件不小于10个",
                                str(item["log-service"]),
                                "基线要求日志切割文件大小不小于100M（104857600字节），且日志切割文件不小于10个"]

        if "hotdeploy-config" in item:
            check_result = PASS if check_hotdeploy(item["hotdeploy-config"]) else FAIL
            bes_dict["自动部署配置"] = [check_result,
                                  "hotdeploy-config：应用的自动部署配置，要求禁用该服务",
                                  str(item["hotdeploy-config"]),
                                  "用来自动处理目录中应用的增加和删除动作，默认为开启状态，要求禁用自动部署"]

        if "hotswap-service" in item:
            check_result = PASS if check_hotswap(item["hotswap-service"]) else FAIL
            bes_dict["类热加载配置"] = [check_result,
                                  "hotswap-service：类热加载服务配置，要求禁用该服务",
                                  str(item["hotswap-service"]),
                                  "部署目录资源修改后实时生效有可能导致安全隐患，默认为禁用，要求禁用类的热加载"]

        if "thread-pool" in item:
            check_result = PASS if check_thread_pool(item["thread-pool"]) else FAIL
            bes_dict["线程池配置"] = [check_result,
                                 "max-queue-size: 4096,max-idle-time: 60000,min-spare-threads: 50,max-threads: 200",
                                 str(item["thread-pool"]),
                                 "各个Server线程池配置，控制台线程池（admin-thread）保持默认即可，本处不对控制台线程池进行校验"]

        if "jdbc-resource" in item:
            check_result = PASS if check_jdbc_resource(item["jdbc-resource"]) else FAIL
            bes_dict["数据源配置"] = [check_result,
                                 "min-idle: 10,test-on-borrow: true,max-wait-time-in-millis: 60000,"
                                 "max-connection-age: 1800,idle-timeout: 900,initial-pool-size: 10,"
                                 "sql-trace: false,validate-atmost-once-period-in-seconds: 120,"
                                 "test-while-idle: true,max-pool-size: 50",
                                 str(item["jdbc-resource"]),
                                 "各个数据源配置信息，请参考运维手册进行规范配置"]

        # 将当前bes信息转存合并至java_dict中
        for java_dict in java_list:
            if java_dict["进程ID"] == bes_dict["进程ID"]:
                java_dict["进程类型："] = ["bes", "", "", ""]
                for k in bes_dict:
                    java_dict[k] = bes_dict[k]
