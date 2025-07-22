#! /usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os


def server_analysis(output_dir, ip):
    server_file = output_dir + "/data/" + ip + "_server.txt"
    if not os.path.exists(server_file):
        return list()
    dict_list = utils.json_to_format_dict_list(server_file)
    analysis_dict_list = list()
    for item in dict_list:
        server_dict = dict()
        server_dict["hostname"] = ["主机名标记，符合", "非localhost.localdomain主机名",
                                   item["hostname"] if item["hostname"] != "localhost.localdomain" else "默认主机名，不符合",
                                   "当前主机的主机名"]
        server_dict["ip"] = ["人工复核", "", item["ip"], "当前主机的IP"]
        server_dict["cpu"] = ["人工复核", "", item["cpu"], "当前主机的CPU核数配置"]
        server_dict["osVersion"] = ["主机操作系统", "", item["osVersion"], "当前主机的操作系统版本"]
        if "MemTotal" and "MemFree" and "Buffers" and "Cached" in item:
            server_dict["MemTotal"] = ["无需", "无", str(int(int(item["MemTotal"]) / 1024)) + "MB", "当前主机的总内存(MB)"]
            actual_memory_usage = int(item["MemTotal"]) - int(item["MemFree"]) - int(item["Buffers"]) - int(
                item["Cached"])
            check_result = "符合" if actual_memory_usage < int(item["MemTotal"]) * 0.8 else "不符合"
            server_dict["actual_memory_usage"] = [check_result, "小于总内存的80%",
                                                  str(int(actual_memory_usage / 1024)) + "MB",
                                                  "当前主机实际已使用的内存(MB)"]
        if "machine" in item:
            for item2 in item["machine"]:
                if item2.strip().startswith("Product Name"):
                    server_dict["machine"] = ["主机安装类型", "物理机或虚拟机", item2.strip().replace("Product Name", "").strip(),
                                              "当前主机的安装类型，物理机或虚拟机"]
        server_dict["disk"] = ["人工复核", "磁盘分区的使用率要小于80%", str(utils.convert(item["disk"])),
                               "主机的磁盘信息"]
        server_dict["ulimit"] = ["人工复核", "最大打开文件数现在不能是默认值1024",
                                 str(utils.convert(item["ulimit"])), "主机系统的文件资源限制参数"]
        if "net_core_somaxconn" in item:
            check_result = "符合" if int(item["net_core_somaxconn"]) >= 2048 else "不符合"
            server_dict["net_core_somaxconn"] = [check_result,
                                                 "大于等于2048",
                                                 item["net_core_somaxconn"],
                                                 "Linux内核参数net_core_somaxconn"]
        if "net_ipv4_tcp_max_syn_backlog" in item:
            check_result = "符合" if int(item["net_ipv4_tcp_max_syn_backlog"]) >= 1024 else "不符合"
            server_dict["net_ipv4_tcp_max_syn_backlog"] = [check_result,
                                                           "大于等于2048",
                                                           item["net_ipv4_tcp_max_syn_backlog"],
                                                           "Linux内核参数net_ipv4_tcp_max_syn_backlog"]
        if "overcommit_memory" in item:
            check_result = "符合" if int(item["overcommit_memory"]) == 0 else "不符合"
            server_dict["overcommit_memory"] = [check_result,
                                                "等于0",
                                                item["overcommit_memory"],
                                                "Linux内核参数overcommit_memory，overcommit_memory取值又三种分别为0， 1， 2 "
                                                "overcommit_memory=0， 表示内核将检查是否有足够的可用内存供应用进程使用；如果有足够 "
                                                "的可用内存，内存申请允许；否则，内存申请失败，并把错误返回给应用进程。 overcommit_memory=1， "
                                                "表示内核允许分配所有的物理内存，而不管当前的内存状态如何。 overcommit_memory=2， "
                                                "表示内核允许分配超过所有物理内存和交换空间总和的内存 "
                                                "overcommit_memory参数就是控制分配内存是否可以超过CommitLimit，默认是0,"
                                                "即启发式的overcommitting handle,会尽量减少swap的使用,"
                                                "root可以分配比一般用户略多的内存。1表示允许超过CommitLimit,2表示不允许超过CommitLimit"]
        if "vm_swappiness" in item:
            check_result = "符合" if int(item["vm_swappiness"]) == 0 else "不符合"
            server_dict["vm_swappiness"] = [check_result,
                                            "等于0",
                                            item["vm_swappiness"],
                                            "Linux内核参数overcommit_memory，* 0：禁用交换* 1：不完全禁用交换的最小数量* "
                                            "10：当系统中有足够内存时为提高性能而推荐的值* 100：主动交换"]

        analysis_dict_list.append(server_dict)
    return analysis_dict_list


def java_analysis(output_dir, ip):
    java_file = output_dir + "/data/" + ip + "_java.txt"
    if not os.path.exists(java_file):
        return list()
    dict_list = utils.json_to_format_dict_list(java_file)
    analysis_dict_list = list()
    for item in dict_list:
        java_dict = dict()
        java_dict["PID"] = ["进程信息标记", "", item["PID"], "当前进程的PID"]
        java_dict["CMD"] = ["进程信息标记", "", item["CMD"], "当前进程执行的命令行"]
        java_dict["lsof_count"] = ["人工复核", "小于10000", "无", "当前java进程打开文件数量"]
        java_dict["netstat_count"] = ["人工复核", "小于8000", "无", "当前java进程打开socket连接数量"]
        java_dict["cpu_usage"] = ["不符合", "小于80%", "无", "当前java进程CPU使用率"]
        java_dict["mem_usage"] = ["不符合", "小于80%", "无", "当前java进程内存使用率"]
        java_dict["java_version"] = ["人工复核", "建议升级到1.8以上版本", "无", "jdk的版本"]
        java_dict["java_distribution"] = ["人工复核", "建议使用Oraclejdk", "无", "jdk的发行商"]
        java_dict["HeapDumpOnOutOfMemoryError"] = ["建议", "建议配置项", "无",
                                                   "jvm参数HeapDumpOnOutOfMemoryError，JVM将Java堆转储为HPROF二进制格式("
                                                   "当发生内存不足错误时)，建议有该配置项"]
        java_dict["HeapDumpPath"] = ["建议", "建议配置项", "无", "jvm参数HeapDumpPath，Dump文件存储路径，建议有该配置项"]
        java_dict["java.awt.headless"] = ["建议", "建议配置项", "无",
                                          "jvm参数java.awt.headless，强制使用Headless版本的AWT实现类，就能避免图形环境缺失所导致的程序出错，建议设置为true"]
        java_dict["DappName"] = ["建议", "建议配置项", "无", "为方便后续信息收集，增加的系统名称信息配置参数"]
        java_dict["Dport"] = ["建议", "建议配置项", "无", "为方便后续信息收集，增加的端口信息配置参数"]
        java_dict["Xms"] = ["不符合", "必须设置项", "无", "初始化JVM堆内存大小"]
        java_dict["Xmx"] = ["不符合", "必须设置项", "无", "最大JVM堆内存大小"]
        java_dict["Xmn"] = ["建议", "建议配置项", "无", "Jvm新生代大小配置,官方建议最大堆内存的3/8,一般可以配置为1/4"]
        java_dict["XX:MaxMetaspaceSize"] = ["不符合", "必须设置项", "无", "jdk1.8以上版本的最大元数据空间"]
        java_dict["XX:MaxPermSize"] = ["不符合", "必须设置项", "无", "jdk1.8以下版本的最大元数据空间"]
        java_dict["XX:+DisableExplicitGC"] = ["建议", "建议配置项", "无", "禁止代码中手动调用System.gc()"]
        java_dict["XX:+ExplicitGCInvokesConcurrent"] = ["建议", "建议配置项", "无",
                                                        "打开此参数后，在做System.gc()时会做background模式CMS GC，即并行FULL GC，可提高FULL "
                                                        "GC效率，该参数在允许systemGC且使用CMS GC时有效"]
        java_dict["XX:+UseParNewGC"] = ["建议", "建议配置项", "无",
                                        "并发串行收集器，它是工作在新生代的垃圾收集器，在收集过程中，应用程序会全部暂停。目前只有它能与CMS收集器配合工作。"]
        java_dict["XX:+UseConcMarkSweepGC"] = ["建议", "建议配置项", "无", "基于标记清除算法实现的多线程老年代垃圾回收器。"]
        java_dict["XX:ParallelGCThreads"] = ["建议", "建议配置项", "无", "gc并发线程数，根据操作系统核数匹配，如果操作系统CPU核数很多，建议最大配置8"]
        java_dict["XX:ParallelCMSThreads"] = ["建议", "建议配置项", "无", "CMS并发线程数，根据操作系统核数匹配，如果操作系统CPU核数很多，建议最大配置8"]
        java_dict["verbose:gc"] = ["建议", "建议配置项", "无", "建议开启gc记录"]
        java_dict["PrintGCDetails"] = ["建议", "建议配置项", "无", "打印GC细节"]
        java_dict["PrintGCDateStamps"] = ["建议", "建议配置项", "无", "GC记录时间戳"]
        java_dict["Xloggc"] = ["建议", "建议配置项", "无", "GC记录日志路径"]
        java_dict["ErrorFile"] = ["建议", "建议配置项", "无", "GC记录日志路径"]
        java_dict["Djava.security.egd"] = ["建议", "建议配置项", "无", "GC记录日志路径"]

        if "UID" in item:
            check_result = "符合" if item["UID"] != "root" else "不符合"
            java_dict["user"] = [check_result,
                                 "非root用户",
                                 item["UID"],
                                 "为减小被外部攻击时的影响面，建议使用普通用户对java进程进行管理"]

        if "cpu_usage" in item:
            check_result = "符合" if float(item["cpu_usage"]) < float(80) else "不符合"
            java_dict["cpu_usage"] = [check_result,
                                      "小于80%",
                                      item["cpu_usage"],
                                      "当前java进程的CPU占用率（%）"]
        if "mem_usage" in item:
            check_result = "符合" if float(item["mem_usage"]) < float(80) else "不符合"
            java_dict["mem_usage"] = [check_result,
                                      "小于80%",
                                      item["mem_usage"],
                                      "当前java进程的内存占用率（%）"]

        if "lsof_count" in item:
            check_result = "符合" if int(item["lsof_count"]) < 10000 else "不符合"
            java_dict["lsof_count"] = [check_result,
                                       "小于10000",
                                       item["lsof_count"],
                                       "当前java进程打开文件数量"]

        if "netstat_count" in item:
            check_result = "符合" if int(item["netstat_count"]) < 8000 else "不符合"
            java_dict["netstat_count"] = [check_result,
                                          "小于8000",
                                          item["netstat_count"],
                                          "与当前java进程连接的各tcp状态连接的数量总和"]

        if "javaVersion" in item:
            java_version = ""
            java_distribution = ""
            for line in item["javaVersion"]:
                if line.startswith("java version"):
                    java_version = line.replace('java version', '').replace('\"', '').strip()
                    java_distribution = 'oracle'
                if line.startswith("openjdk version"):
                    java_version = line.replace('openjdk version', '').replace('\"', '').strip()
                    java_distribution = 'openjdk'
            java_dict["java_version"] = ["人工复核",
                                         "建议升级到1.8以上版本",
                                         java_version,
                                         "jdk的版本"]
            java_dict["java_distribution"] = ["人工复核",
                                              "建议使用Oraclejdk",
                                              java_distribution,
                                              "jdk的发行商"]
        if "javaCheck" in item:
            for item1 in item:
                if "HeapDumpOnOutOfMemoryError" in item1:
                    java_dict["HeapDumpOnOutOfMemoryError"] = ["建议",
                                                               "建议配置项",
                                                               "已配置" if item1[
                                                                            "HeapDumpOnOutOfMemoryError"] == True else "无",
                                                               "jvm参数HeapDumpOnOutOfMemoryError，JVM将Java堆转储为HPROF"
                                                               "二进制格式(当发生内存不足错误时)，建议有该配置项"]
                if "HeapDumpPath" in item1:
                    java_dict["HeapDumpPath"] = ["建议",
                                                 "建议配置项",
                                                 "已配置" if item1["HeapDumpPath"] is True else "无",
                                                 "jvm参数HeapDumpPath，Dump文件存储路径，建议有该配置项"]
                if "java.awt.headless" in item1:
                    java_dict["java.awt.headless"] = ["建议",
                                                      "建议配置项",
                                                      "已配置" if item1["java.awt.headless"] is True else "无",
                                                      "jvm参数java.awt.headless，强制使用Headless版本的AWT"
                                                      "实现类，就能避免图形环境缺失所导致的程序出错，建议设置为true"]
        if "CMD" in item:
            for item2 in item["CMD"].split():
                if item2.startswith("-DappName"):
                    java_dict["DappName"] = ["符合",
                                             "建议配置项",
                                             item2.split("=")[-1],
                                             "为方便后续信息收集，增加的系统名称信息配置参数"]
                if item2.startswith("-Dport"):
                    java_dict["Dport"] = ["符合",
                                          "建议配置项",
                                          item2.split("=")[-1],
                                          "为方便后续信息收集，增加的端口信息配置参数"]
                if item2.startswith("-Xms"):
                    java_dict["Xms"] = ["符合",
                                        "必须设置项",
                                        item2.replace("-Xms", ""),
                                        "初始化JVM堆内存大小"]
                if item2.startswith("-Xmx"):
                    java_dict["Xmx"] = ["符合",
                                        "必须设置项",
                                        item2.replace("-Xmx", ""),
                                        "最大JVM堆内存大小"]
                if item2.startswith("-Xmn"):
                    java_dict["Xmn"] = ["符合",
                                        "建议配置项",
                                        item2.replace("-Xmn", ""),
                                        "Jvm新生代大小配置,官方建议最大堆内存的3/8,一般可以配置为1/4"]
                if item2.startswith("-XX:MaxMetaspaceSize"):
                    java_dict["XX:MaxMetaspaceSize"] = ["符合",
                                                        "必须设置项",
                                                        item2.split("=")[-1],
                                                        "jdk1.8以上版本的最大元数据空间"]
                if item2.startswith("-XX:MaxPermSize"):
                    java_dict["XX:MaxPermSize"] = ["符合",
                                                   "必须设置项",
                                                   item2.split("=")[-1],
                                                   "jdk1.8以下版本的最大元数据空间"]
                if item2 == "-XX:+DisableExplicitGC":
                    java_dict["XX:+DisableExplicitGC"] = ["人工复核",
                                                          "建议配置项",
                                                          "存在",
                                                          "禁止代码中手动调用System.gc()"]
                if item2 == "-XX:+ExplicitGCInvokesConcurrent":
                    java_dict["XX:+ExplicitGCInvokesConcurrent"] = ["人工复核",
                                                                    "建议配置项",
                                                                    "存在",
                                                                    "打开此参数后，在做System.gc()时会做background模式CMS "
                                                                    "GC，即并行FULL GC，可提高FULL GC效率，该参数在允许systemGC且使用CMS "
                                                                    "GC时有效"]
                if item2 == "-XX:+UseParNewGC":
                    java_dict["XX:+UseParNewGC"] = ["人工复核",
                                                    "建议配置项",
                                                    "存在",
                                                    "并发串行收集器，它是工作在新生代的垃圾收集器，在收集过程中，应用程序会全部暂停。目前只有它能与CMS收集器配合工作。"]
                if item2 == "-XX:+UseConcMarkSweepGC":
                    java_dict["XX:+UseConcMarkSweepGC"] = ["人工复核",
                                                           "建议配置项",
                                                           "存在",
                                                           "基于标记清除算法实现的多线程老年代垃圾回收器。"]
                if item2.startswith("-XX:ParallelGCThreads"):
                    java_dict["XX:ParallelGCThreads"] = ["人工复核",
                                                         "建议配置项",
                                                         item2.split("=")[-1],
                                                         "gc并发线程数，根据操作系统核数匹配，如果操作系统CPU核数很多，建议最大配置8"]
                if item2.startswith("-XX:ParallelCMSThreads"):
                    java_dict["XX:ParallelCMSThreads"] = ["人工复核",
                                                          "建议配置项",
                                                          item2.split("=")[-1],
                                                          "CMS并发线程数，根据操作系统核数匹配，如果操作系统CPU核数很多，建议最大配置8"]
                if item2 == "-verbose:gc":
                    java_dict["verbose:gc"] = ["人工复核",
                                               "建议配置项",
                                               "存在",
                                               "建议开启gc记录"]
                if item2 == "-XX:+PrintGCDetails":
                    java_dict["PrintGCDetails"] = ["人工复核",
                                                   "建议配置项",
                                                   "存在",
                                                   "打印GC细节"]
                if item2 == "-XX:+PrintGCDateStamps":
                    java_dict["PrintGCDateStamps"] = ["人工复核",
                                                      "建议配置项",
                                                      "存在",
                                                      "GC记录时间戳"]
                if item2.startswith("-Xloggc"):
                    java_dict["Xloggc"] = ["人工复核",
                                           "建议配置项",
                                           item2.split(":")[-1],
                                           "GC记录日志路径"]
                if item2.startswith("-XX:ErrorFile"):
                    java_dict["ErrorFile"] = ["人工复核",
                                              "建议配置项",
                                              item2.split("=")[-1],
                                              "GC记录日志路径"]
                if item2.startswith("-Djava.security.egd"):
                    java_dict["Djava.security.egd"] = ["人工复核",
                                                       "建议配置项",
                                                       item2.split("=")[-1],
                                                       "GC记录日志路径"]
        analysis_dict_list.append(java_dict)
    return analysis_dict_list


def redis_analysis(output_dir, ip):
    redis_file = output_dir + "/data/" + ip + "_redis.txt"
    if not os.path.exists(redis_file):
        return list()
    dict_list = utils.json_to_format_dict_list(redis_file)
    analysis_dict_list = list()
    flag = 0
    for item in dict_list:
        redis_dict = dict()
        if "redis_version" in item:
            check_result = "符合" if utils.version_to_num(item["redis_version"]) > utils.version_to_num(
                "5.0.0") else "不符合"
            redis_dict["redis_version"] = [check_result,
                                           "大于5.x ",
                                           item["redis_version"],
                                           "5.x 之前版本不在官方维护周期内,存在较多安全漏洞且性能较差，建议升级到5及以上版本"]
        if "connected_clients" in item:
            check_result = "符合" if int(item["connected_clients"]) < 8000 else "不符合"
            redis_dict["connected_clients"] = [check_result,
                                               "小于 maxclients(默认值10000) * 80% =" + str(8000),
                                               item["connected_clients"],
                                               "当前连接redis的客户端数量"]

        if "uptime_in_days" in item:
            check_result = "符合" if int(item["uptime_in_days"]) < 730 else "不符合"
            redis_dict["uptime_in_days"] = [check_result,
                                            "小于2年",
                                            item["connected_clients"],
                                            "当前redis进程持续运行的天数"]

        if "blocked_clients" in item:
            check_result = "符合" if int(item["blocked_clients"]) == 0 else "不符合"
            redis_dict["blocked_clients"] = [check_result,
                                             "等于 0",
                                             item["blocked_clients"],
                                             "当前客户端阻塞数(使用BLPOP, BRPOP, BRPOPLPUSH命令)"]

        if "total_system_memory_human" in item:
            redis_dict["total_system_memory_human"] = ["符合",
                                                       "无",
                                                       item["total_system_memory_human"],
                                                       "当前redis-server所在节点系统内存总量"]

        if "maxmemory_human" and "maxmemory" and "total_system_memory" in item:
            target_byte = int(item["total_system_memory"]) * 0.6
            check_result = "符合" if int(item["maxmemory"]) < target_byte else "不符合"
            redis_dict["maxmemory_human"] = [check_result,
                                             "小于 total_system_memory *  60% = " + str(
                                                 int(target_byte / 1048576)) + " MB",
                                             item["maxmemory_human"],
                                             "当前redis-server的最大内存使用量"]

        if "used_memory_human" and "used_memory" and "maxmemory" in item:
            target_byte = int(item["maxmemory"]) * 0.8
            check_result = "符合" if int(item["used_memory"]) < target_byte else "不符合"
            redis_dict["used_memory_human"] = [check_result,
                                               "小于 maxmemory * 80% = " + str(int(target_byte / 1048576)) + " MB",
                                               item["used_memory_human"],
                                               "当前redis-server的内存使用量"]

        if "used_memory_rss_human" and "used_memory_rss" and "total_system_memory" in item:
            target_byte = int(item["total_system_memory"]) * 0.8
            check_result = "符合" if int(item["used_memory_rss"]) < target_byte else "不符合"
            redis_dict["used_memory_rss_human"] = [check_result,
                                                   "小于 total_system_memory * 80% = " + str(
                                                       int(target_byte / 1048576)) + " MB",
                                                   item["used_memory_rss_human"],
                                                   "从系统角度，显示 redis 进程占用的物理内存总量，(同top,ps)"]

        if "maxmemory_policy" in item:
            check_result = "符合" if item["maxmemory_policy"] == "noeviction" else "不符合"
            redis_dict["connected_clients"] = [check_result,
                                               "noeviction(不对key进行淘汰)",
                                               item["maxmemory_policy"],
                                               "redis 内存即将写满，当有新key加入时，对已有key的淘汰策略"]
        if "cpu_usage" in item:
            check_result = "符合" if float(item["cpu_usage"]) < float(80) else "不符合"
            redis_dict["cpu_usage"] = [check_result,
                                       "小于80%",
                                       item["cpu_usage"],
                                       "当前redis进程的CPU占用率（%）"]
        if "memory_usage" in item:
            check_result = "符合" if float(item["memory_usage"]) < float(80) else "不符合"
            redis_dict["memory_usage"] = [check_result,
                                          "小于80%",
                                          item["memory_usage"],
                                          "当前redis进程的内存占用率（%）"]

        if "rdb_last_bgsave_status" in item:
            check_result = "符合" if item["rdb_last_bgsave_status"] == "ok" else "不符合"
            redis_dict["rdb_last_bgsave_status"] = [check_result,
                                                    "ok",
                                                    item["rdb_last_bgsave_status"],
                                                    "上次写入RDB持久化文件的执行状态"]

        if "rdb_last_bgsave_time_sec" in item:
            check_result = "符合" if int(item["rdb_last_bgsave_time_sec"]) < 60 else "不符合"
            redis_dict["rdb_last_bgsave_time_sec"] = [check_result,
                                                      "小于repl-timeout（60s）",
                                                      item["rdb_last_bgsave_time_sec"],
                                                      "上次重写RDB持久化文件用时（秒）"]

        if "rdb_last_cow_size" in item:
            check_result = "符合" if int(item["rdb_last_cow_size"]) < 536870912 else "不符合"
            redis_dict["rdb_last_cow_size"] = [check_result,
                                               "小于 512MB (536870912 byte) ",
                                               item["rdb_last_cow_size"],
                                               "上次进行RDB持久化，因写入时数据key变动而造成的额外内存使用(byte)"]

        if "aof_last_bgrewrite_status" in item:
            check_result = "符合" if item["aof_last_bgrewrite_status"] == "ok" else "不符合"
            redis_dict["aof_last_bgrewrite_status"] = [check_result,
                                                       "ok",
                                                       item["aof_last_bgrewrite_status"],
                                                       "上次重写AOF文件的执行结果"]

        if "aof_last_write_status" in item:
            check_result = "符合" if item["aof_last_write_status"] == "ok" else "不符合"
            redis_dict["aof_last_write_status"] = [check_result,
                                                   "ok",
                                                   item["aof_last_write_status"],
                                                   "上次写入AOF文件的执行结果"]

        if "aof_last_cow_size" in item:
            check_result = "符合" if int(item["aof_last_cow_size"]) < 536870912 else "不符合"
            redis_dict["aof_last_cow_size"] = [check_result,
                                               "小于 512MB (536870912 byte) ",
                                               item["aof_last_cow_size"],
                                               "上次重写AOF因写入时数据变动而造成的额外内存使用(byte)"]

        if "aof_current_size" in item:
            check_result = "符合" if int(item["aof_current_size"]) < 2147483648 else "不符合"
            redis_dict["aof_current_size"] = [check_result,
                                              "小于2GB(2147483648 byte)", item["aof_current_size"],
                                              "当前AOF文件大小(byte)"]

        if "rejected_connections" in item:
            check_result = "符合" if int(item["rejected_connections"]) == 0 else "不符合"
            redis_dict["rejected_connections"] = [check_result,
                                                  "等于0", item["rejected_connections"], "redis 拒绝的连接数"]

        if "evicted_keys" in item:
            check_result = "符合" if int(item["evicted_keys"]) == 0 else "不符合"
            redis_dict["evicted_keys"] = [check_result,
                                          "等于0", item["evicted_keys"],
                                          "redis 因内存不足淘汰的key数量"]

        if "connected_clients" in item:
            check_result = "符合" if int(item["connected_clients"]) < 8000 else "不符合"
            redis_dict["connected_clients"] = [check_result,
                                               "小于 maxclients(默认值10000) * 80% ",
                                               item["connected_clients"],
                                               "当前连接redis的客户端数量"]

        if "latest_fork_usec" in item:
            check_result = "符合" if int(item["latest_fork_usec"]) < 100000 else "不符合"
            redis_dict["latest_fork_usec"] = [check_result,
                                              "小于0.1s(100000微秒)",
                                              item["latest_fork_usec"],
                                              "redis上次fork子进程使用(阻塞)的时间(微秒)"]

        if "port" in item:
            check_result = "符合" if int(item["port"]) != 6379 else "不符合"
            redis_dict["port"] = [check_result,
                                  "非默认(6379)端口",
                                  item["port"],
                                  "为预防外部利用默认端口的攻击性行为，不建议使用redis默认端口"]
        if "user" in item:
            check_result = "符合" if item["port"] != "root" else "不符合"
            redis_dict["user"] = [check_result,
                                  "非root用户",
                                  item["user"],
                                  "为减小被外部攻击时的影响面，建议使用普通用户对redis进程进行管理"]
        if "cluster_state" in item:
            check_result = "符合" if item["port"] != "ok" else "不符合"
            redis_dict["cluster_state"] = [check_result,
                                           "ok",
                                           item["cluster_state"],
                                           "redis 集群状态(是否可用)"]
        if "cluster_slots_assigned" in item:
            check_result = "符合" if int(item["cluster_slots_assigned"]) != 16384 else "不符合"
            redis_dict["user"] = [check_result,
                                  "16384",
                                  item["cluster_slots_assigned"],
                                  "redis当前已分配的槽位数量"]

        if "cluster_slots_ok" in item:
            check_result = "符合" if int(item["cluster_slots_ok"]) != 16384 else "不符合"
            redis_dict["user"] = [check_result,
                                  "16384",
                                  item["cluster_slots_ok"],
                                  "redis当前可正常使用的槽位数量"]
        if "netstat_count" in item:
            check_result = "符合" if int(item["netstat_count"]) < 8000 else "不符合"
            redis_dict["netstat_count"] = [check_result,
                                           "小于maxclient * 80% (8000)",
                                           item["netstat_count"],
                                           "与当前redis-server连接的各tcp状态连接的数量总和"]

        if "tcp_backlog" in item:
            check_result = "符合" if int(item["tcp_backlog"]) > 2048 else "不符合"
            redis_dict["tcp_backlog"] = [check_result,
                                         "2048或更大值",
                                         item["tcp_backlog"],
                                         "Redis TCP队列长度，需要适当调大以应对大流量突发情况"]
        if "errorLogs" in item:
            redis_dict["tcp_backlog"] = ["人工复核",
                                         "无错误日志",
                                         "筛选当前redis节点错误日志",
                                         item["errorLogs"]]

        if "requirepass" in item:
            check_result = "人工复核"
            redis_dict["requirepass"] = [check_result,
                                         "存在，且为复杂密码/加密串",
                                         item["requirepass"],
                                         "redis 客户端连接密码"]
        else:
            redis_dict["requirepass"] = ["不符合",
                                         "存在，且为复杂密码/加密串",
                                         "",
                                         "redis 客户端连接密码"]
        if "masterauth" in item:
            check_result = "人工复核"
            redis_dict["masterauth"] = [check_result,
                                        "存在，且为复杂密码/加密串",
                                        item["masterauth"],
                                        "redis 主从连接密码"]
        else:
            redis_dict["masterauth"] = ["不符合",
                                        "存在，且为复杂密码/加密串",
                                        "",
                                        "redis 主从连接密码"]
        if "rename_command" in item:
            check_result = "人工复核"
            redis_dict["rename_command"] = [check_result,
                                            "FLUSHALL,FLUSHDB 等",
                                            item["rename_command"],
                                            "禁用清空数据等高危命令"]
        if "max_open_files" in item:
            check_result = "符合" if int(item["max_open_files"]) > 12000 else "不符合"
            redis_dict["max_open_files"] = [check_result,
                                            "大于 12000",
                                            item["max_open_files"],
                                            "当前redis进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = "符合" if int(item["lsof_count"]) < target_num else "不符合"
                redis_dict["lsof_count"] = [check_result,
                                            "小于max_open_files * 80% = " + str(target_num),
                                            str(item["lsof_count"]),
                                            "当前进程的句柄使用数量"]

        if "max_open_files_s" in item:
            check_result = "符合" if int(item["max_open_files_s"]) > 12000 else "不符合"
            redis_dict["max_open_files_s"] = [check_result,
                                              "大于 12000",
                                              item["max_open_files_s"],
                                              "当前redis进程使用句柄数超过这个值，则会产生告警(软限制)"]

        if "log_file" not in item:
            redis_dict["log_file"] = ["不符合",
                                      "配合合理路径",
                                      "NULL",
                                      "未配置日志文件，请合理配置日志参数，以便后续进行排错等操作"]

        if "role" and "connected_slaves" in item:
            if item["role"] == "master":
                check_result = "符合" if int(item["connected_slaves"]) > 0 else "不符合"
                redis_dict["connected_slaves"] = [check_result,
                                                  "大于0",
                                                  item["connected_slaves"],
                                                  "当前master节点连接的slave节点数"]
            else:
                if item["master_link_status"] in item:
                    check_result = "符合" if item["connected_slaves"] != "up" else "不符合"
                    redis_dict["master_link_status"] = [check_result,
                                                        "状态为：up",
                                                        item["master_link_status"],
                                                        "当前slave节点所连接的master节点状态"]
        if "config_file" in item:
            redis_dict["config_file"] = ['', '', '', str(item["config_file"])]
        if "exe_path" in item:
            redis_dict["exe_path"] = ['', '', '', str(item["exe_path"])]
        if "redis_home" in item:
            redis_dict["redis_home"] = ['', '', '', str(item["redis_home"])]

        analysis_dict_list.append(redis_dict)

        flag = flag + 1
        if flag >= len(dict_list):  # 最后一轮循环时将内核参数取出
            kernel_dict = dict()
            # linux kernel parameters filter
            if "thp" in item:
                check_result = "符合" if item["thp"] == "always madvise [never]" else "不符合"
                kernel_dict["thp"] = [check_result,
                                      "always madvise [never]",
                                      item["thp"],
                                      "禁用内存透明大页可有效减少redis持久化时的额外内存消耗"]

            if "overcommit_memory" in item:
                check_result = "符合" if int(item["overcommit_memory"]) == 1 else "不符合"
                kernel_dict["overcommit_memory"] = [check_result,
                                                    "等于1",
                                                    item["overcommit_memory"],
                                                    "将该值设置为1时，可预防fork子进程进行写盘时，因内核拒绝分配内存而返回失败结果"]

            if "net_ipv4_tcp_max_syn_backlog" in item:
                check_result = "符合" if int(item["net_ipv4_tcp_max_syn_backlog"]) >= 1024 else "不符合"
                kernel_dict["net_ipv4_tcp_max_syn_backlog"] = [check_result,
                                                               "大于等于 1024",
                                                               item["net_ipv4_tcp_max_syn_backlog"],
                                                               "TCP半连接上限，默认值是128,建议适当调大，以应对突发流量"]

            if "net_core_somaxconn" in item:
                check_result = "符合" if int(item["net_core_somaxconn"]) >= 2048 else "不符合"
                kernel_dict["net_core_somaxconn"] = [check_result,
                                                     "大于等于 2048",
                                                     item["net_core_somaxconn"],
                                                     "TCP完全连接上限，默认值是128,建议适当调大，以应对突发流量"]

            if "vm_swappiness" in item:
                check_result = "符合" if int(item["vm_swappiness"]) <= 10 else "不符合"
                kernel_dict["vm_swappiness"] = [check_result,
                                                "小于等于 10",
                                                item["vm_swappiness"],
                                                "设置较小值表示不积极的使用swap分区，过多使用swap分区将极大拖慢redis运行速度"]

            analysis_dict_list.append(kernel_dict)

    return analysis_dict_list


def nginx_analysis(output_dir, ip):
    nginx_file = output_dir + "/data/" + ip + "_nginx.txt"
    if not os.path.exists(nginx_file):
        return list()
    dict_list = utils.json_to_format_dict_list(nginx_file)
    analysis_dict_list = list()
    for item in dict_list:
        nginx_dict = dict()

        if "worker_processes" and "cpu_count" in item:
            if item["worker_processes"] == "auto":
                item["worker_processes"] = item["cpu_count"]
            if "worker_connections" in item:
                item["max_connections"] = int(item["worker_connections"]) * int(item["worker_processes"])

        if "cpu_usage" in item:
            check_result = "符合" if float(item["cpu_usage"]) < float(80) else "不符合"
            nginx_dict["cpu_usage"] = [check_result,
                                       "小于80%",
                                       item["cpu_usage"],
                                       "当前nginx进程的CPU占用率（%）"]
        if "memory_usage" in item:
            check_result = "符合" if float(item["memory_usage"]) < float(80) else "不符合"
            nginx_dict["memory_usage"] = [check_result,
                                          "小于80%",
                                          item["memory_usage"],
                                          "当前nginx进程的内存占用率（%）"]

        if "max_open_files" in item:
            check_result = "符合" if int(item["max_open_files"]) > 40000 else "不符合"
            nginx_dict["max_open_files"] = [check_result,
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
        if "max_open_files_s" in item:
            check_result = "符合" if int(item["max_open_files_s"]) > 20000 else "不符合"
            nginx_dict["max_open_files_s"] = [check_result,
                                              "大于 20000",
                                              item["max_open_files_s"],
                                              "当前nginx进程使用句柄数超过这个值，则会产生告警(软限制)"]
        if "nginx_version" in item:
            check_result = "符合" if utils.version_to_num(item["nginx_version"]) > utils.version_to_num(
                "1.20.1") else "不符合"
            nginx_dict["nginx_version"] = [check_result,
                                           "大于1.20.1 ",
                                           item["nginx_version"],
                                           "1.20.1以前版本存在较多安全漏洞，建议升级到1.20.1+"]

        if "worker_connections" in item:
            check_result = "符合" if int(item["worker_connections"]) >= 2048 else "不符合"
            nginx_dict["worker_connections"] = [check_result,
                                                "大于等于2048",
                                                item["worker_connections"],
                                                "单个工作进程可以允许同时建立外部连接的数量"]

        if "worker_processes" and "cpu_count" in item:
            check_result = "符合" if int(item["worker_processes"]) >= int(item["cpu_count"]) else "不符合"
            nginx_dict["worker_processes"] = [check_result,
                                              "大于等于当前主机CPU核数 = " + str(item["cpu_count"]),
                                              item["worker_processes"],
                                              "当前nginx工作进程(worker)的数量"]
        if "netstat_count" in item:
            target_num = 5000
            if "max_connections" in item:
                target_num = int(int(item["max_connections"]) * 0.8)
            check_result = "符合" if int(item["netstat_count"]) < target_num else "不符合"
            nginx_dict["netstat_count"] = [check_result,
                                           "小于max_connections * 80% = " + str(target_num),
                                           item["netstat_count"],
                                           "与当前nginx连接的各tcp状态连接的数量总和"]

        if "uptime_in_seconds" in item:
            seconds_to_days = int(int(item["uptime_in_seconds"]) / 86400)
            check_result = "符合" if seconds_to_days < 730 else "不符合"
            nginx_dict["uptime_in_days"] = [check_result,
                                            "小于2年",
                                            str(seconds_to_days),
                                            "当前nginx进程持续运行的天数"]

        if "server_tokens" in item:
            check_result = "符合" if item["server_tokens"] == "off" else "不符合"
            nginx_dict["server_tokens"] = [check_result,
                                           "off",
                                           item["server_tokens"],
                                           "是否禁用nginx版本信息显示"]

        if "port" in item:
            nginx_dict["port"] = ['人工复核', '端口处于正常监听状态', '见备注', str(utils.convert(item["port"]))]

        if "access_log" in item:
            nginx_dict["access_log"] = ["人工复核",
                                        "无异常错误信息", "见备注",
                                        str(utils.convert(item["access_log"]))]
        if "error_logs" in item:
            nginx_dict["error_logs"] = ["人工复核",
                                        "无异常错误信息", "见备注",
                                        str(utils.convert(item["error_logs"]))]
        if "config_content" in item:
            nginx_dict["config_content"] = ["人工复核",
                                            "无异常配置信息", "见备注",
                                            str(utils.convert(item["config_content"]))]

        analysis_dict_list.append(nginx_dict)

    return analysis_dict_list


def wls_analysis(output_dir, ip):
    wls_file = output_dir + "/data/" + ip + "_wls.txt"
    if not os.path.exists(wls_file):
        return list()
    dict_list = utils.json_to_format_dict_list(wls_file)
    analysis_dict_list = list()
    for item in dict_list:
        wls_dict = dict()
        if "base_domain" in item:
            wls_dict["base_domain"] = ['', '', '见备注', str(utils.convert(item["base_domain"]))]
        if "server_name" in item:
            wls_dict["server_name"] = ['', '', '见备注', str(utils.convert(item["server_name"]))]

        if "UID" in item:
            check_result = "符合" if item["UID"] != "root" else "不符合"
            wls_dict["user"] = [check_result,
                                "非root用户",
                                item["UID"],
                                "为减小被外部攻击时的影响面，建议使用普通用户对weblogic进程进行管理"]

        if "jdbc_xml" in item:
            wls_dict["jdbc_xml"] = ['人工复核', '', '见备注', str(utils.convert(item["jdbc_xml"]))]

            if "test_connections_on_reserve" in item:
                check_result = "符合" if "true" in item["test_connections_on_reserve"] else "不符合"
                wls_dict["test_connections_on_reserve"] = [check_result, 'true', item["test_connections_on_reserve"],
                                                           "保留时测试连接,使WebLogic Server 能够在将连接提供给客户机之前对连接进行测试"]
            if "inactive_connection_timeout_seconds" in item:
                check_result = "符合" if "600" in item["inactive_connection_timeout_seconds"] else "不符合"
                wls_dict["inactive_connection_timeout_seconds"] = [check_result, '600s',
                                                                   item["inactive_connection_timeout_seconds"],
                                                                   "非活动连接超时：(默认值：0)保留连接处于不活动状态的秒数, 该时间过后 WebLogic Server "
                                                                   "将收回该连接并将其释放回连接池。"]
            if "test_frequency_seconds" in item:
                check_result = "符合" if "30" in item["test_frequency_seconds"] else "不符合"
                wls_dict["test_frequency_seconds"] = [check_result, '30s', item["test_frequency_seconds"],
                                                      "测试频率:(默认值:120s),WebLogic Server 实例对未用连接进行测试的间隔秒数,(要求指定测试表名称)"]

        if "log" in item:
            wls_dict["log"] = ["人工复核",
                               "无异常错误信息", "见备注",
                               str(utils.convert(item["log"]))]
        if "log_file" in item:
            wls_dict["log_file"] = ["",
                                    "", "见备注",
                                    str(utils.convert(item["log_file"]))]
        if "java_home" in item:
            wls_dict["java_home"] = ["",
                                        "", "见备注",
                                        str(utils.convert(item["java_home"]))]

        if "jdk_type" in item and item["jdk_type"] == "oracle":
            if "wls_urandom" in item:  # need to check urandom args
                check_result = "符合" if item["wls_urandom"] == "file:/dev/./urandom" else "不符合"
                wls_dict["wls_urandom"] = [check_result,
                                           "file:/dev/./urandom",
                                           item["wls_urandom"],
                                           "设置预期值可预防启动时因无法及时生成随机数，从而阻塞进程"]
            else:
                wls_dict["wls_urandom"] = ["不符合",
                                           "file:/dev/./urandom",
                                           "NULL",
                                           "设置预期值可预防启动时因无法及时生成随机数，从而阻塞进程"]

        if "uptime_in_seconds" in item:
            seconds_to_days = int(int(item["uptime_in_seconds"]) / 86400)
            check_result = "符合" if seconds_to_days < 730 else "不符合"
            wls_dict["uptime_in_days"] = [check_result,
                                          "小于2年",
                                          str(seconds_to_days),
                                          "当前weblogic进程持续运行的天数"]

        if "wls_version" in item:
            wls_dict["wls_version"] = ["人工复核",
                                       "大于12.x",
                                       item["wls_version"].split()[2],
                                       "当前weblogic版本信息(包含当前补丁的版本)"]
        t3_disable = list()
        iiop_disable = list()
        port_list = list()
        server_count = 0
        if "config_xml" in item:
            wls_dict["config_xml"] = ["人工复核",
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
            wls_dict["t3_disable"] = ["不符合",
                                      "允许本机使用t3协议进行通信，禁止远程使用该协议",
                                      "NULL",
                                      "t3为weblogic内部通信协议，对外开放在安全隐患"]
        else:
            wls_dict["t3_disable"] = ["符合",
                                      "允许本机使用t3协议进行通信，禁止远程使用该协议",
                                      str(utils.convert(t3_disable)),
                                      "t3为weblogic内部通信协议，对外开放存在安全隐患"]
        if len(iiop_disable) == 0:
            wls_dict["iiop_disable"] = ["不符合",
                                        "每个server都禁用了iiop协议",
                                        "NULL",
                                        "weblogic内部对象请求代理协议"]
        else:
            check_result = "符合" if len(iiop_disable) >= server_count else "不符合"
            wls_dict["iiop_disable"] = [check_result,
                                        "每个server都禁用了iiop协议,当前server数量 = " + str(server_count),
                                        str(utils.convert(iiop_disable)),
                                        "weblogic内部对象请求代理协议"]
        if "PID" in item:
            wls_dict["PID"] = ["",
                               "",
                               item["PID"],
                               "当前weblogic进程PID号"]

        analysis_dict_list.append(wls_dict)

    return analysis_dict_list


def notes_analysis(output_dir, ip):
    notes_file = output_dir + "/data/" + ip + "_notes.txt"
    if not os.path.exists(notes_file):
        return list()
    dict_list = utils.json_to_format_dict_list(notes_file)
    analysis_dict_list = list()
    for item in dict_list:
        notes_dict = dict()
        if "javaCount" in item:
            notes_dict["javaCount"] = ['', '', str(item["javaCount"]), '']
        if "weblogicCount" in item:
            notes_dict["weblogicCount"] = ['', '', str(item["weblogicCount"]), '']
        if "nginxCount" in item:
            notes_dict["nginxCount"] = ['', '', str(item["nginxCount"]), '']
        if "redisCount" in item:
            notes_dict["redisCount"] = ['', '', str(item["redisCount"]), '']
        if "rabbitmqCount" in item:
            notes_dict["rabbitmqCount"] = ['', '', str(item["rabbitmqCount"]), '']
        analysis_dict_list.append(notes_dict)

    return analysis_dict_list


def rabbitmq_analysis(output_dir, ip):
    rabbitmq_file = output_dir + "/data/" + ip + "_rabbitmq.txt"
    if not os.path.exists(rabbitmq_file):
        return list()

    dict_list = utils.json_to_format_dict_list(rabbitmq_file)
    analysis_dict_list = list()
    for item in dict_list:
        rabbitmq_dict = dict()
        if "cpu_usage" in item:
            check_result = "符合" if float(item["cpu_usage"]) < float(80) else "不符合"
            rabbitmq_dict["cpu_usage"] = [check_result,
                                          "小于80%",
                                          item["cpu_usage"],
                                          "当前rabbitmq进程的CPU占用率（%）"]
        if "memory_usage" in item:
            check_result = "符合" if float(item["memory_usage"]) < float(80) else "不符合"
            rabbitmq_dict["memory_usage"] = [check_result,
                                             "小于80%",
                                             item["memory_usage"],
                                             "当前rabbitmq进程的内存占用率（%）"]
        if "user" in item:
            check_result = "符合" if item["user"] != "root" else "不符合"
            rabbitmq_dict["user"] = [check_result,
                                     "非root用户",
                                     item["user"],
                                     "为减小被外部攻击时的影响面，建议使用普通用户对rabbitmq进程进行管理"]

        if "max_open_files" in item:
            check_result = "符合" if int(item["max_open_files"]) > 40000 else "不符合"
            rabbitmq_dict["max_open_files"] = [check_result,
                                               "大于 40000",
                                               item["max_open_files"],
                                               "当前rabbitmq进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = "符合" if int(item["lsof_count"]) < target_num else "不符合"
                rabbitmq_dict["lsof_count"] = [check_result,
                                               "小于max_open_files * 80% = " + str(target_num),
                                               str(item["lsof_count"]),
                                               "当前进程的句柄使用数量"]
        if "max_open_files_s" in item:
            check_result = "符合" if int(item["max_open_files_s"]) > 20000 else "不符合"
            rabbitmq_dict["max_open_files_s"] = [check_result,
                                                 "大于 20000",
                                                 item["max_open_files_s"],
                                                 "当前rabbitmq进程使用句柄数超过这个值，则会产生告警(软限制)"]
        if "max_user_processes" in item:
            check_result = "符合" if int(item["max_open_files"]) > 40000 else "不符合"
            rabbitmq_dict["max_open_files"] = [check_result,
                                               "大于 40000",
                                               item["max_open_files"],
                                               "当前rabbitmq进程管理用户被允许打开的最大进程数量(硬限制)"]
        if "max_user_processes_s" in item:
            check_result = "符合" if int(item["max_open_files_s"]) > 20000 else "不符合"
            rabbitmq_dict["max_open_files_s"] = [check_result,
                                                 "大于 20000",
                                                 item["max_open_files_s"],
                                                 "当前rabbitmq进程管理用户打开进程数超过这个值，则会产生告警(软限制)"]
        if "netstat_count" in item:
            check_result = "符合" if int(item["netstat_count"]) < 8000 else "不符合"
            rabbitmq_dict["netstat_count"] = [check_result,
                                              "小于 8000",
                                              item["netstat_count"],
                                              "与当前rabbitmq连接的各tcp状态连接的数量总和"]

        if "uptime_in_seconds" in item:
            seconds_to_days = int(int(item["uptime_in_seconds"]) / 86400)
            check_result = "符合" if seconds_to_days < 730 else "不符合"
            rabbitmq_dict["uptime_in_days"] = [check_result,
                                               "小于2年",
                                               str(seconds_to_days),
                                               "当前rabbitmq进程持续运行的天数"]
        if "list_users" in item:
            flag = 0
            for line in item["list_users"]:
                if "guest" in line:
                    flag = 1
                    break
            check_result = "符合" if flag == 0 else "不符合"
            rabbitmq_dict["list_users"] = [check_result, '使用自己创建的用户，并且默认用户(guest)已删除',
                                           str(utils.convert(item["list_users"])),
                                           "当前rabbitmq所包含的用户列表"]
        if "list_permissions" in item:
            rabbitmq_dict["list_permissions"] = ['人工复核', '用户设置合理权限',
                                                 str(utils.convert(item["list_permissions"])),
                                                 '当前rabbitmq用户的权限信息']
        if "list_queues" in item:
            rabbitmq_dict["port"] = ['人工复核', '每个队列积压的msg少于1000条',
                                     str(utils.convert(item["list_queues"])),
                                     '当前rabbitmq的队列列表']

        if "list_unresponsive_queues" in item:
            check_result = "符合" if len(item["list_unresponsive_queues"]) == 1 else "不符合"
            rabbitmq_dict["list_unresponsive_queues"] = [check_result, '不存在无响应队列',
                                                         str(utils.convert(item["list_unresponsive_queues"])),
                                                         '当前rabbitmq中无响应的队列列表']
        if "node_health_check" in item:
            flag = 0
            for line in item["node_health_check"]:
                if "Health check passed" in line:
                    flag = 1
                    break
            check_result = "符合" if flag == 1 else "不符合"
            rabbitmq_dict["node_health_check"] = [check_result, 'Health check passed',
                                                  str(utils.convert(
                                                      item["node_health_check"])),
                                                  '当前rabbitmq服务健康状态检查']
        if "cluster_status" in item:
            flag = 0
            for line in item["node_health_check"]:
                if "{partitions,[]}" in line:
                    flag = 1
                    break
            check_result = "符合" if flag == 1 else "不符合"
            rabbitmq_dict["cluster_status"] = [check_result, '无网络分区情况({partitions,[]})',
                                               str(utils.convert(item["cluster_status"])),
                                               "当前rabbitmq集群状态"]

        if "port_status" in item:
            rabbitmq_dict["port"] = ['人工复核', '端口处于正常监听状态', '见备注',
                                     str(utils.convert(item["port_status"]))]

        if "error_logs" in item:
            rabbitmq_dict["error_logs"] = ["人工复核",
                                           "无异常错误信息", "见备注",
                                           str(utils.convert(item["error_logs"]))]

        if "erlang_exe" in item:
            rabbitmq_dict["erlang_exe"] = ["符合",
                                           "无", "见备注",
                                           str(utils.convert(item["erlang_exe"]))]
        if "rabbitmq_home" in item:
            rabbitmq_dict["rabbitmq_home"] = ["符合",
                                              "无", "见备注",
                                              str(utils.convert(item["rabbitmq_home"]))]
        if "erlang_version" in item:
            rabbitmq_dict["erlang_version"] = ["符合",
                                               "无", "见备注",
                                               str(utils.convert(item["erlang_version"]))]
        if "erlang_version" in item:
            rabbitmq_dict["erlang_version"] = ["人工复核",
                                               "无", str(utils.convert(item["erlang_version"])),
                                               "同rabbitmq版本对应关系参考官网链接：https://www.rabbitmq.com/which-erlang.html"]
        if "rabbitmq_status" in item:
            rabbitmq_dict["rabbitmq_status"] = ["人工复核",
                                                "无",
                                                str(utils.convert(item["rabbitmq_status"])),
                                                "同rabbitmq版本对应关系参考官网链接：https://www.rabbitmq.com/which-erlang.html"]

        # if "rabbitmq_version" in item:
        #     check_result = "符合" if utils.version_to_num(item["nginx_version"]) > utils.version_to_num(
        #         "1.20.1") else "不符合"
        #     rabbitmq_dict["nginx_version"] = [check_result,
        #                                    "大于1.20.1 ",
        #                                    item["nginx_version"],
        #                                    "1.20.1以前版本存在较多安全漏洞，建议升级到1.20.1+"]

        analysis_dict_list.append(rabbitmq_dict)

    return analysis_dict_list
