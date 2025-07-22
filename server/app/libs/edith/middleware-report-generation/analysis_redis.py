#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def redis_analysis(output_dir, ip):
    redis_file = output_dir + "/data/" + ip + "_redis.txt"
    if not os.path.exists(redis_file):
        return list()
    dict_list = utils.json_to_format_dict_list(redis_file)
    analysis_dict_list = list()
    loop_flag = 0
    for item in dict_list:
        redis_dict = dict()
        redis_dict["进程类型："] = ["redis", "", "", ""]
        redis_dict["进程ID"] = ["",
                              "进程信息标记",
                              item["PID"],
                              "当前进程的PID"]

        redis_dict["进程命令行"] = ["",
                               "进程信息标记",
                               item["CMD"],
                               "当前进程的命令行"]

        redis_dict["启动时间"] = ["",
                              "启动时间",
                              None if "startup" not in item or len(item["startup"]) == 0 else item["startup"][
                                  0].strip(),
                              "进程启动时间"]

        check_result = PASS if item["UID"] != "root" else FAIL
        redis_dict["运行用户"] = [check_result,
                              "禁止使用root用户运行redis",
                              item["UID"],
                              "运行redis的用户"]
        if "redis_version" in item:
            check_result = PASS if utils.version_to_num(item["redis_version"]) > utils.version_to_num("5.0.0") else FAIL
            redis_dict["redis版本"] = [check_result,
                                     "大于5.x ",
                                     item["redis_version"],
                                     "5.x 之前版本不在官方维护周期内,存在较多安全漏洞且性能较差，建议升级到5及以上版本"]

        if "uptime_in_days" in item:
            check_result = PASS if int(item["uptime_in_days"]) < 730 else FAIL
            redis_dict["启动天数"] = [check_result,
                                  "小于2年",
                                  item["uptime_in_days"],
                                  "当前redis进程持续运行的天数"]

        if "blocked_clients" in item:
            check_result = PASS if int(item["blocked_clients"]) == 0 else FAIL
            redis_dict["客户端阻塞数"] = [check_result,
                                    "等于0为正常",
                                    item["blocked_clients"],
                                    "当前客户端阻塞数(使用BLPOP, BRPOP, BRPOPLPUSH命令)"]

        if "total_system_memory_human" in item:
            redis_dict["系统内存总量"] = ["",
                                    "无",
                                    item["total_system_memory_human"],
                                    "当前redis-server所在节点系统内存总量"]

        if "maxmemory" in item:
            target_byte = int(item["total_system_memory"]) * 0.6
            check_result = PASS if int(item["maxmemory"]) < target_byte else FAIL
            redis_dict["redis内存上限"] = [check_result,
                                       "小于系统内存总量 * 60%",
                                       item["maxmemory_human"],
                                       "当前redis-server的最大内存使用量"]
        if "used_memory_human" in item:
            target_byte = int(item.get("maxmemory","0")) * 0.8
            if target_byte == 0:
                target_byte = int(item.get("total_system_memory",1e18)) * 0.6
            check_result = PASS if int(item["used_memory"]) < target_byte else FAIL
            redis_dict["redis已使用内存"] = [check_result,
                                        "小于redis内存上限 * 80%(或小于系统内存总量 * 60%)",
                                        item["used_memory_human"],
                                        "当前redis-server的内存使用量,若未设置内存上限，则需要当前值小于系统总内存 * 60%"]
        if "used_memory_rss_human" in item:
            target_byte = int(item["total_system_memory"]) * 0.8
            check_result = PASS if int(item["used_memory_rss"]) < target_byte else FAIL
            redis_dict["redis已使用物理内存"] = [check_result,
                                          "小于系统内存总量*80%",
                                          item["used_memory_rss_human"],
                                          "从系统角度，显示 redis 进程占用的物理内存总量，(同top,ps)"]

        # 增加redis内存碎片率
        if "mem_fragmentation_ratio" in item:
            mem_ratio = float(item["mem_fragmentation_ratio"])
            check_result = PASS if mem_ratio >= float(1) and mem_ratio <= float(1.5) else FAIL
            redis_dict["redis内存碎片率"] = [check_result,
                                     "大于等于1且小于等于1.5",
                                     item["mem_fragmentation_ratio"],
                                     "当前redis内存碎片率"]

        if "maxmemory_policy" in item:
            redis_dict["redis内存淘汰策略"] = ["",
                                         "根据业务需求,一般为 allkeys-lru",
                                         item["maxmemory_policy"],
                                         "redis内存淘汰策略，lru为最近最久未使用"]

        if "cpu_usage" in item:
            check_result = PASS if float(item["cpu_usage"]) < float(80) else FAIL
            redis_dict["进程CPU使用率"] = [check_result,
                                      "小于80%",
                                      item["cpu_usage"],
                                      "当前redis进程的CPU占用率（%）"]
        if "memory_usage" in item:
            check_result = PASS if float(item["memory_usage"]) < float(80) else FAIL
            redis_dict["进程内存使用率"] = [check_result,
                                     "小于80%",
                                     item["memory_usage"],
                                     "当前redis进程的内存占用率（%）"]

        if "rdb_last_bgsave_status" in item:
            check_result = PASS if item["rdb_last_bgsave_status"] == "ok" else FAIL
            redis_dict["上一次RDB执行状态"] = [check_result,
                                        "ok为正常",
                                        item["rdb_last_bgsave_status"],
                                        "上次写入RDB持久化文件的执行状态"]

        if "rdb_last_bgsave_time_sec" in item:
            check_result = PASS if int(item["rdb_last_bgsave_time_sec"]) < 60 else FAIL
            redis_dict["上一次RDB执行耗时"] = [check_result,
                                        "小于repl-timeout（60s）",
                                        item["rdb_last_bgsave_time_sec"],
                                        "上次重写RDB持久化文件用时（秒）"]

        if "rdb_last_cow_size" in item:
            check_result = PASS if "rdb_last_cow_size" not in item or int(item["rdb_last_cow_size"]) < 536870912 else FAIL
            redis_dict["rdb_last_cow_size"] = [check_result,
                                               "小于 512MB (536870912 byte) ",
                                               "" if "rdb_last_cow_size" not in item else item["rdb_last_cow_size"],
                                               "上次进行RDB持久化，因写入时数据key变动而造成的额外内存使用(byte)"]

        if "aof_last_bgrewrite_status" in item:
            check_result = PASS if item["aof_last_bgrewrite_status"] == "ok" else FAIL
            redis_dict["aof_last_bgrewrite_status"] = [check_result,
                                                       "ok",
                                                       item["aof_last_bgrewrite_status"],
                                                       "上次重写AOF文件的执行结果"]
        if "aof_last_write_status" in item:
            check_result = PASS if item["aof_last_write_status"] == "ok" else FAIL
            redis_dict["aof_last_write_status"] = [check_result,
                                                   "ok",
                                                   item["aof_last_write_status"],
                                                   "上次写入AOF文件的执行结果"]

        if "aof_current_size" in item:
            check_result = PASS if "aof_current_size" not in item or int(item["aof_current_size"]) < 2147483648 else FAIL
            redis_dict["aof_current_size"] = [check_result,
                                              "小于2GB(2147483648 byte)",
                                              "" if "aof_current_size" not in item else item["aof_current_size"],
                                              "当前AOF文件大小(byte)"]
        if "rejected_connections" in item:
            check_result = PASS if int(item["rejected_connections"]) == 0 else FAIL
            redis_dict["rejected_connections"] = [check_result,
                                                  "等于0", item["rejected_connections"], "redis 拒绝的连接数"]

        if "evicted_keys" in item:
            redis_dict["evicted_keys"] = ["",
                                          "无", item["evicted_keys"],
                                          "redis 因内存不足淘汰的key数量"]
        if "connected_clients" in item:
            check_result = PASS if int(item["connected_clients"]) < 8000 else FAIL
            redis_dict["connected_clients"] = [check_result,
                                               "小于 maxclients(默认值10000) * 80% ",
                                               item["connected_clients"],
                                               "当前连接redis的客户端数量"]

        if "latest_fork_usec" in item:
            check_result = PASS if int(item["latest_fork_usec"]) < 100000 else FAIL
            redis_dict["latest_fork_usec"] = [check_result,
                                              "小于0.1s(100000微秒)",
                                              item["latest_fork_usec"],
                                              "redis上次fork子进程使用(阻塞)的时间(微秒)"]

        if "port" in item:
            check_result = PASS if int(item["port"]) != 6379 else FAIL
            redis_dict["port"] = [check_result,
                                      "非默认(6379)端口",
                                      item["port"],
                                      "为预防外部利用默认端口的攻击性行为，不建议使用redis默认端口"]

        if "cluster_state" in item:
            check_result = PASS if "cluster_state" not in item or item["cluster_state"] != "ok" else FAIL
            redis_dict["cluster_state"] = [check_result,
                                           "ok",
                                           "" if "cluster_state" not in item else item["cluster_state"],
                                           "redis集群状态(是否可用)"]

        if "cluster_slots_assigned" in item:
            check_result = PASS if "cluster_slots_assigned" not in item or int(
                item["cluster_slots_assigned"]) != 16384 else FAIL
            redis_dict["当前已分配槽位"] = [check_result,
                                     "16384",
                                     "" if "cluster_slots_assigned" not in item else item["cluster_slots_assigned"],
                                     "redis当前已分配的槽位数量"]
        if "cluster_slots_ok" in item:
            check_result = PASS if "cluster_slots_ok" not in item or int(item["cluster_slots_ok"]) != 16384 else FAIL
            redis_dict["当前可使用槽位"] = [check_result,
                                     "16384",
                                     "" if "cluster_slots_ok" not in item else item["cluster_slots_ok"],
                                     "redis当前可正常使用的槽位数量"]
        if "netstat_count" in item:
            check_result = PASS if int(item["netstat_count"]) < 8000 else FAIL
            redis_dict["网络连接数"] = [check_result,
                                   "小于maxclient(10000) * 80% (8000)",
                                   item["netstat_count"],
                                   "与当前redis-server连接的各tcp状态连接的数量总和"]
        if "tcp_backlog" in item:
            check_result = PASS if "tcp_backlog" in item and int(item["tcp_backlog"]) >= 2048 else FAIL
            redis_dict["tcp_backlog"] = [check_result,
                                         "2048或更大值",
                                         "" if "tcp_backlog" not in item else item["tcp_backlog"],
                                         "Redis TCP队列长度，需要适当调大以应对大流量突发情况"]

        if "requirepass" in item:
            check_result = PASS if "requirepass" in item and item["requirepass"] is not None else FAIL
            redis_dict["requirepass"] = [check_result,
                                         "正常设置连接密码",
                                         "",
                                         "redis客户端连接密码"]
        if "masterauth" in item:
            check_result = PASS if "masterauth" in item and item["masterauth"] is not None else FAIL
            redis_dict["masterauth"] = [check_result,
                                        "正常设置连接密码",
                                        "",
                                        "redis主从连接密码"]
        if "rename_command" in item:
            check_result = PASS if "FLUSHALL" in item["rename_command"].upper() or "FLUSHDB" in item[
                "rename_command"].upper() else FAIL
            redis_dict["rename_command"] = [check_result,
                                            "需要禁用FLUSHALL,FLUSHDB等高危命令",
                                            "" if not check_result else item["rename_command"],
                                            "禁用清空数据库等高危命令"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 20000 else FAIL
            redis_dict["max_open_files"] = [check_result,
                                            "大于20000",
                                            item["max_open_files"],
                                            "当前redis用户所被允许打开的最大文件数(硬限制)"]

        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 12000 else FAIL
            redis_dict["max_open_files_s"] = [check_result,
                                              "大于12000",
                                              item["max_open_files_s"],
                                              "当前redis进程使用句柄数超过这个值，则会产生告警(软限制)"]

        if "log_file" in item:
            redis_dict["log_file"] = [PASS,
                                      "配合合理的日志路径",
                                      item["log_file"],
                                      "请合理配置日志文件(log_file)参数，以便后续进行排错等操作"]
        else:
            redis_dict["log_file"] = [FAIL, "配合合理的日志路径", "NULL",
                                      "未配置日志文件，请合理配置日志参数，以便后续进行排错等操作"]
        if "role" in item:
            check_result = FAIL if item["role"] == "master" and int(item["connected_slaves"]) == 0 else PASS
            redis_dict["connected_slaves"] = [check_result,
                                              "对于master节点需要大于0，当前节点为: " + item["role"],
                                              item["connected_slaves"],
                                              "当前master节点连接的slave节点数"]

        check_result = PASS if "master_link_status" not in item or item["master_link_status"] == "up" else FAIL
        redis_dict["master_link_status"] = [check_result,
                                            "状态为：up",
                                            "" if "master_link_status" not in item else item["master_link_status"],
                                            "当前slave节点所连接的master节点状态"]
        if "config_file" in item:
            redis_dict["配置文件路径"] = ['', '', str(item["config_file"]), 'redis.conf所在位置']
        if "include_file_path" in item:
            redis_dict["include配置文件路径"] = ['', '', str(item["include_file_path"]), 'redis.conf所在位置']
        if "exe_path" in item:
            redis_dict["可执行文件路径"] = ['', '', str(item["exe_path"]), "redis-server所在位置"]
        if "redis_home" in item:
            redis_dict["redis_home"] = ['', '', str(item["redis_home"]), 'redis运行的主目录']

        analysis_dict_list.append(redis_dict)

        loop_flag = loop_flag + 1
        if loop_flag >= len(dict_list):  # 最后一轮循环时将内核参数取出
            kernel_dict = dict()

            kernel_dict["内核参数检查"] = ["for redis", "", "", ""]
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
