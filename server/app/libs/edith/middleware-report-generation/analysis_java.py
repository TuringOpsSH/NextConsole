#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def check_java_version_bool(java_version_list):
    return len(java_version_list) > 0 and java_version_list[0].split()[2].replace("\"", "").startswith("1.8")


def check_java_version(java_version_list):
    if check_java_version_bool(java_version_list):
        return [PASS, "当前jdk版本，建议使用JDK 1.8+ 版本", java_version_list[0], "当前使用jdk的版本"]
    else:
        #return [MAN, "建议升级到至1.8+", java_version_list[0], "jdk的版本"]
        return [MAN, "建议升级到至1.8+", java_version_list[0] if len(java_version_list) > 0 else "", "jdk的版本"]


def check_jvm(java_dict, cmd, javaVersion):
    jvm_dict = {
        "Xms": None,
        "Xmx": None,
        "MaxMetaspaceSize": None,
        "MaxPermSize": None,
        "Djava.security.egd": None,
        "Xrunjdwp": None
    }
    for item in cmd.split(" "):
        if "Xms" in item:
            jvm_dict["Xms"] = item
        if "Xmx" in item:
            jvm_dict["Xmx"] = item
        if "MaxMetaspaceSize" in item:
            jvm_dict["MaxMetaspaceSize"] = item.split("=")[1]
        if "MaxPermSize" in item:
            jvm_dict["MaxPermSize"] = item.split("=")[1]
        if "Djava.security.egd" in item:
            jvm_dict["Djava.security.egd"] = item
        if "Xrunjdwp:transport=dt_socket" in item:
            jvm_dict["Xrunjdwp"] = item

    check_result = PASS if jvm_dict["Xms"] is not None and utils.parse_size_to_kb(
        jvm_dict["Xms"].replace("-Xms", "")) >= 1 * 1000 * 1000 else MAN
    java_dict["堆内存最小值Xms"] = [check_result,
                              "生产环境建议大于1G，默认值见备注",
                              jvm_dict["Xms"],
                              "初始化JVM堆内存大小，可以通过java -XX:+PrintFlagsFinal查看默认值"]

    check_result = PASS if jvm_dict["Xmx"] is not None and 2 * 1000 * 1000 <= utils.parse_size_to_kb(
        jvm_dict["Xmx"].replace("-Xmx", "")) <= 4 * 1024 * 1024 else FAIL
    java_dict["堆内存最大值Xmx"] = [check_result,
                              "生产环境建议在2G到4G之间，默认值见备注",
                              jvm_dict["Xmx"],
                              "最大JVM堆内存大小，可以通过java -XX:+PrintFlagsFinal查看默认值"]

    if check_java_version_bool(javaVersion):
        check_result = PASS if jvm_dict["MaxMetaspaceSize"] is None or utils.parse_size_to_kb(
            jvm_dict["MaxMetaspaceSize"]) >= 512 * 1000 else MAN
        java_dict["元空间上限"] = [check_result,
                              "元空间最大值，建议不小于512M，系统稳定运行情况下可以不设置",
                              jvm_dict["MaxMetaspaceSize"],
                              "jdk1.8适用，默认无上限（实际操作系统最大可用内存）"]
    else:
        check_result = PASS if jvm_dict["MaxPermSize"] is not None and utils.parse_size_to_kb(
            jvm_dict["MaxPermSize"]) >= 512 * 1000 else MAN
        java_dict["方法区上限"] = [check_result,
                              "方法区最大值，建议不小于512M，默认值见备注",
                              jvm_dict["MaxPermSize"],
                              "适用jdk1.7及以下版本，默认值取决于JVM版本，硬件/ OS平台和/或物理内存大小，可以通过java -XX:+PrintFlagsFinal查看默认值"]
    jdk_type = ""
    if 'JRockit' in " ".join(javaVersion):
        jdk_type = "jrockit"
    if 'Java HotSpot' in " ".join(javaVersion):
        jdk_type = "oracle"
    if jdk_type == "oracle":
        java_dict["cmd_urandom"] = [
            PASS if jvm_dict["Djava.security.egd"] == "-Djava.security.egd=file:/dev/urandom" else FAIL,
            "-Djava.security.egd=file:/dev/urandom",
            jvm_dict["Djava.security.egd"],
            "使用无阻塞随机数生成器。默认是阻塞模式，可以通过/proc/sys/kernel/random/entropy_avail查看熵的余量，当余量小于500时，可能造成系统严重卡顿，"
            "配置-Djava.security.egd=file:/dev/urandom，也可通过jre/lib/security/java.security配置"]

    java_dict["远程调试"] = [PASS if jvm_dict["Xrunjdwp"] is None else FAIL,
                         "禁止在生产设置此参数",
                         jvm_dict["Xrunjdwp"],
                         "JAVA远程调试（Xrunjdwp），可以通过远程调试接口拦截并修改应用，仅在应急情况下使用"]


def java_analysis(output_dir, ip):
    java_file = output_dir + "/data/" + ip + "_java.txt"
    if not os.path.exists(java_file):
        return list()
    dict_list = utils.json_to_format_dict_list(java_file)
    analysis_dict_list = list()
    for item in dict_list:
        java_dict = dict()
        java_dict["进程类型："] = ["java", "", "", ""]
        java_dict["进程ID"] = ["", "进程信息标记", item["PID"], "当前进程的PID"]
        java_dict["进程命令行"] = ["", "进程信息标记", item["CMD"], "当前进程的命令行"]
        java_dict["启动时间"] = ["",
                             "启动时间",
                             None if "startup" not in item or len(item["startup"]) == 0 else item["startup"][0].strip(),
                             "进程启动时间"]

        if "uptime_in_seconds" in item and item["uptime_in_seconds"].isdigit():
            if item["uptime_in_seconds"] != "":
                seconds_to_days = int(int(item["uptime_in_seconds"]) / 86400)
                check_result = PASS if seconds_to_days < 730 else FAIL
                java_dict["运行天数"] = [check_result,
                                     "进程运行时间超过2年的需要关注",
                                     str(seconds_to_days),
                                     "当前weblogic进程持续运行的天数"]

        # javaVersion可能不存在，增加容错处理
        if "javaVersion" in item:
            javaVersionTmp = item["javaVersion"]
        else:
            javaVersionTmp = []
        java_dict["JDK版本"] = check_java_version(javaVersionTmp)
        java_dict["OOM转储参数"] = [PASS if item["javaCheck"]["HeapDumpOnOutOfMemoryError"] else FAIL,
                                "JAVA_OPTS=-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/applog",
                                "",
                                "当发生OOM时，JVM可以生成堆内存转储，以便精确定位代码问题"]
        java_dict["awt.headless检查"] = [PASS if item["javaCheck"]["java.awt.headless"] else MAN,
                                       "如果有使用awt/swing的api则必须设置，否则忽略",
                                       "无",
                                       "避免Java中的一些awt方法在不支持显示器、键盘和鼠标等情，造成java进程异常退出"]

        check_jvm(java_dict, item["CMD"], javaVersionTmp)
        #check_jvm(java_dict, item["CMD"], item["javaVersion"])
        java_dict["运行用户"] = [PASS if item["UID"] != "root" else FAIL,
                             "为减小受外部攻击时的影响面，建议使用非root用户运行",
                             item["UID"],
                             "为减小被外部攻击时的影响面，建议使用普通用户对java进程进行管理"]

        lsof_count = item["lsof_count"][0].replace("\n", "")
        java_dict["打开句柄数"] = [PASS if lsof_count == "" or int(lsof_count) < 10000 else FAIL,
                              "进程打开文件句柄数一般不超过10000",
                              lsof_count,
                              "当前进程打开文件句柄数"]
        netstat_count = item["netstat_count"][0].replace("\n", "")
        java_dict["网络连接数"] = [PASS if int(netstat_count) < 2000 else FAIL,
                              "连接数大于2000需要特别关注",
                              netstat_count,
                              "当前java进程打开socket数量"]
        cpu_usage = item["cpu_usage"]
        java_dict["进程CPU使用率"] = [PASS if float(cpu_usage) < 80 else FAIL,
                                 "cpu使用率小于80%",
                                 cpu_usage,
                                 "当前java进程CPU使用率"]
        mem_usage = item["mem_usage"]
        java_dict["进程内存使用率"] = [PASS if float(mem_usage) < 80 else FAIL,
                                "内存使用率小于80%",
                                mem_usage,
                                "当前java进程内存使用率"]
        if "port_status" in item:
            java_dict["端口状态"] = ["", '端口处于正常监听状态', "".join(item["port_status"]).rstrip(), '当前进程的端口监听情况']
        if "jdk_urandom" in item:
            check_result = "符合" if str(item["jdk_urandom"]) == "securerandom.source=file:/dev/./urandom" else "不符合"
            java_dict["jdk_urandom"] = [check_result,
                                        "securerandom.source=file:/dev/./urandom",
                                        str(item["jdk_urandom"]),
                                        "设置预期值可预防启动时因无法及时生成随机数，从而阻塞进程"]

        analysis_dict_list.append(java_dict)
    return analysis_dict_list
