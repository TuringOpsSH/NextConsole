#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

from bs4 import BeautifulSoup

import utils

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def check_jdbc_config(wls_dict, name, xml):
    soup = BeautifulSoup(str(utils.convert(xml)), 'lxml')
    min_capabity = "1"
    initial_capacity = "1"
    max_capacity = "15"
    test_connections_on_reserve = "false"
    inactive_connection_timeout_seconds = "0"

    try:
        min_capabity = soup.find("min-capacity").string
    except:
        pass

    try:
        initial_capacity = soup.find("initial-capacity").string
    except:
        pass

    try:
        max_capacity = soup.find("max-capacity").string
    except:
        pass

    try:
        test_connections_on_reserve = soup.find("test-connections-on-reserve").string
    except:
        pass

    try:
        inactive_connection_timeout_seconds = soup.find("inactive-connection-timeout-seconds").string
    except:
        pass

    wls_dict["JDBC初始容量" + name] = [PASS if int(initial_capacity) >= 10 else FAIL,
                                   '建议调整到10以上，具体根据应用实际情况设置',
                                   initial_capacity,
                                   "连接池最小保留容量，默认1"]

    wls_dict["JDBC最小容量" + name] = [PASS if int(min_capabity) >= 10 else FAIL,
                                   '建议调整到10以上，具体根据应用实际情况设置',
                                   min_capabity,
                                   "连接池最小保留容量，默认1"]

    wls_dict["JDBC最大容量" + name] = [PASS if 20 <= int(max_capacity) <= 50 else FAIL,
                                   '建议设置为20-50，具体根据应用实际情况设置',
                                   max_capacity,
                                   "连接池最大保留容量，默认15"]

    wls_dict["JDBC保留时测试连接" + name] = [PASS if test_connections_on_reserve.upper() == "TRUE" else FAIL,
                                      '建议开启保留连接测试(true)',
                                      test_connections_on_reserve,
                                      "保留时测试连接,使WebLogic Server 能够在将连接提供给客户机之前对连接进行测试，默认false未开启"]

    wls_dict["JDBC非活动连接超时" + name] = [MAN if int(inactive_connection_timeout_seconds) > 10 else MAN,
                                      '建议加入此参数，最低不低于10秒，如果系统稳定可以不设置',
                                      inactive_connection_timeout_seconds,
                                      "默认0，当Connection未活动时间超过此配置后，weblogic会自动回收此连接，防止连接泄漏"]


def wls_analysis(output_dir, ip, java_list):
    wls_file = output_dir + "/data/" + ip + "_wls.txt"
    if not os.path.exists(wls_file):
        return list()
    dict_list = utils.json_to_format_dict_list(wls_file)
    for item in dict_list:
        wls_dict = dict()
        wls_dict["进程ID"] = ["",
                            "进程信息标记",
                            item["PID"],
                            "当前进程的PID"]

        wls_dict["进程命令行"] = ["",
                             "进程信息标记",
                             item["CMD"],
                             "当前进程的命令行"]

        wls_dict["监听端口"] = ['', '端口处于正常监听状态', "" if "port" not in item else item["port"], ""]
        wls_dict["域路径"] = ['', '', item["base_domain"], ""]
        wls_dict["server_name"] = ['', '', item["server_name"], ""]

        for jdbc_xml in item["jdbc_xml"]:
            tuple = jdbc_xml.popitem()
            name = tuple[0]
            xml = tuple[1]
            wls_dict[name] = ['', 'JDBC连接池配置详情', str(utils.convert(xml)), "JDBC连接池配置详情"]
            check_jdbc_config(wls_dict, name, xml)

        wls_dict["运行日志检查"] = [MAN,
                              "异常日志检查",
                              "".join(item["log"]).rstrip(),
                              "日志中存在异常输出，需要人工复查"
                              ]

        wls_dict["运行日志路径"] = ["",
                              "",
                              item["log_file"],
                              "运行日志路径"]

        if "wls_version" in item:
            wls_dict["版本信息"] = ["人工复核",
                                       "大于12.x",
                                       item["wls_version"].split()[2],
                                       "当前weblogic版本信息(包含当前补丁的版本)"]

        if "jdk_type" in item and item["jdk_type"] == "oracle":
            if "wls_urandom" in item:  # need to check urandom args
                check_result = "符合" if item["wls_urandom"] == "file:/dev/.urandom" else "不符合"
                wls_dict["wls_urandom"] = [check_result,
                                           "file:/dev/.urandom",
                                           item["wls_urandom"],
                                           "设置预期值可预防启动时因无法及时生成随机数，从而阻塞进程"]
            else:
                wls_dict["wls_urandom"] = ["不符合",
                                           "file:/dev/.urandom",
                                           "NULL",
                                           "设置预期值可预防启动时因无法及时生成随机数，从而阻塞进程"]

        t3_disable = list()
        iiop_disable = list()
        port_list = list()
        server_count = 0
        if "config_xml" in item:
            wls_dict["config_xml"] = ["",
                                      "无异常配置信息", "见备注",
                                      str(utils.convert(item["config_xml"]))]
            for line in item["config_xml"]:
                if "connection-filter" in line:
                    t3_disable.append(line)
                if "iiop-enabled" in line:
                    iiop_disable.append(line)
                if "listen-port" in line:
                    port_list.append(line)
                if "</server>" in line:
                    server_count = server_count + 1

        if len(t3_disable) == 0:
            wls_dict["t3协议禁用"] = ["不符合",
                                      "允许本机使用t3协议进行通信，禁止远程使用该协议",
                                      "NULL",
                                      "t3为weblogic内部通信协议，对外开放在安全隐患"]
        else:
            wls_dict["t3协议禁用"] = ["符合",
                                      "允许本机使用t3协议进行通信，禁止远程使用该协议",
                                      "".join(t3_disable).rstrip(),
                                      "t3为weblogic内部通信协议，对外开放存在安全隐患"]
        if len(iiop_disable) == 0:
            wls_dict["iiop协议禁用"] = ["不符合",
                                        "每个server都禁用了iiop协议",
                                        "NULL",
                                        "weblogic内部对象请求代理协议"]
        else:
            check_result = "符合" if len(iiop_disable) >= server_count else "不符合"
            wls_dict["iiop协议禁用"] = [check_result,
                                        "每个server都禁用了iiop协议,currentServerCount = " + str(server_count),
                                        "".join(iiop_disable).rstrip(),
                                        "weblogic内部对象请求代理协议"]

        for java_dict in java_list:
            if java_dict["进程ID"] == wls_dict["进程ID"]:
                java_dict["进程类型："] = ["weblogic", "", "", ""]
                for k in wls_dict:
                    java_dict[k] = wls_dict[k]