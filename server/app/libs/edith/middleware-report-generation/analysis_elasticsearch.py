#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils
import json

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"



def judge_shards(es_shards):
    flag = True
    actually_dict_list = json.loads("".join(es_shards).rstrip())
    for actually_dict in actually_dict_list:
        if "state" in actually_dict:
            if actually_dict["state"] != "STARTED":
                flag = False
                break
    return flag


def judge_pending_tasks(es_pending_tasks):
    actually_dict = json.loads("".join(es_pending_tasks).rstrip())
    if "tasks" in actually_dict:
        return actually_dict["tasks"] == []


def judge_thread_rejected(es_thread_pool):
    flag = True
    actually_dict_list = json.loads("".join(es_thread_pool).rstrip())
    for actually_dict in actually_dict_list:
        if "rejected" in actually_dict_list:
            if int(actually_dict["rejected"]) != 0:
                flag = False
                break
    return flag


def judge_by_status(health_dict):
    status = ""
    result = ""
    actually_dict = json.loads("".join(health_dict).rstrip())
    if isinstance(actually_dict, list):
        actually_dict = actually_dict[0]

    if "status" in actually_dict:
        status = actually_dict["status"]

    if status == "green":
        result = "所有的主分片和副本分片都已分配，目前节点(集群)是 100% 可用的。"
    if status == "yellow":
        result = "所有的主分片已经成功分配了，但至少还有一个副本是缺失的。此时不会有数据丢失(搜索结果依然是完整的),不过高可用性被弱化。如果更多的分片丢失，则可能出现数据丢失的情况。"
    if status == "red":
        result = "至少一个主分片(以及它的全部副本)都在缺失中。这意味着你的搜索只能返回部分数据，而分配到这个异常分片上的写入请求会返回一个异常。"

    return status, result


def check_allocation(es_dict, es_allocation):
    temp_dict = dict()
    temp_dict["tcp_port"] = 9300
    temp_dict["heap_percent"] = 0
    temp_dict["disk_used_percent"] = 0
    temp_dict["ram_percent"] = 0
    actually_dict = json.loads("".join(es_allocation).rstrip())[0]

    if "port" in actually_dict:
        temp_dict["tcp_port"] = actually_dict["port"]
    if "heap.percent" in actually_dict:
        temp_dict["heap_percent"] = actually_dict["heap.percent"]
    if "disk_used_percent" in actually_dict:
        temp_dict["disk_used_percent"] = actually_dict["disk.used_percent"]
    if "ram.percent" in actually_dict:
        temp_dict["ram_percent"] = actually_dict["ram.percent"]

    es_dict["es节点间通讯端口"] = ["", "无", temp_dict["tcp_port"], "es(集群)节点间内部通讯端口"]

    check_result = PASS if int(temp_dict["heap_percent"]) < 80 else FAIL
    es_dict["堆内存占用比例"] = [check_result,
                          "小于 80% ",
                          str(temp_dict["heap_percent"]),
                          "堆内存占用比例(%)"]

    check_result = PASS if int(temp_dict["disk_used_percent"]) < 90 else FAIL
    es_dict["磁盘占用比例"] = [check_result,
                         "小于 90% ",
                         str(temp_dict["disk_used_percent"]),
                         "当前es所在磁盘空间占用比例(%)"]

    check_result = PASS if int(temp_dict["ram_percent"]) < 90 else FAIL
    es_dict["内存占用比例"] = [check_result,
                         "小于 90% ",
                         str(temp_dict["ram_percent"]),
                         "当前es正在使用的内存百分比(%)"]


def elasticsearch_analysis(output_dir, ip, java_list):
    es_file = output_dir + "/data/" + ip + "_elasticsearch.txt"
    if not os.path.exists(es_file):
        return list()
    dict_list = utils.json_to_format_dict_list(es_file)
    for item in dict_list:
        es_dict = dict()
        es_dict["进程ID"] = ["", "进程信息标记", item["PID"], "当前进程的PID"]
        es_dict["进程命令行"] = ["", "进程信息标记", item["CMD"], "当前进程的命令行"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 60000 else FAIL
            es_dict["最大文件数(硬限制)"] = [check_result,
                                     "大于 60000",
                                     item["max_open_files"],
                                     "当前es进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = PASS if int(item["lsof_count"]) < target_num else FAIL
                es_dict["当前使用文件数"] = [check_result,
                                      "小于max_open_files * 80% = " + str(target_num),
                                      str(item["lsof_count"]),
                                      "当前进程的句柄使用数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 40000 else FAIL
            es_dict["最大文件数(软限制)"] = [check_result,
                                     "大于 40000",
                                     item["max_open_files_s"],
                                     "当前es进程使用句柄数超过这个值，则会产生告警(软限制)"]
        if "max_user_processes" in item and item["max_user_processes"].isdigit():
            check_result = PASS if int(item["max_user_processes"]) > 60000 else FAIL
            es_dict["最大进程数(硬限制)"] = [check_result,
                                     "大于 60000",
                                     item["max_user_processes"],
                                     "当前es进程管理用户被允许打开的最大进程数量(硬限制)"]
        if "max_user_processes_s" in item and item["max_user_processes_s"].isdigit():
            check_result = PASS if int(item["max_user_processes_s"]) > 40000 else FAIL
            es_dict["最大进程数(软限制)"] = [check_result,
                                     "大于 40000",
                                     item["max_user_processes_s"],
                                     "当前es进程管理用户打开进程数超过这个值，则会产生告警(软限制)"]

        if "error_logs" in item:
            es_dict["异常日志筛选"] = [MAN, "无异常错误信息", "(请查看原始日志)", str(item["error_logs"])[:1000]]
        if "jvm_options_content" in item:
            es_dict["jvm参数配置"] = ["", "无", str(item["jvm_options_content"]), "jvm参数配置"]
        if "http_port" in item:
            es_dict["http端口"] = ["", "无", str(item["http_port"]), "elasticSearch http端口配置"]

        if "network_host" in item:
            wrong_hosts = {"127.0.0.1", "[::1]", "0.0.0.0"}
            check_result = PASS if str(item["network_host"]) not in wrong_hosts else FAIL
            es_dict["绑定主机"] = [check_result,
                               "当前主机特定网卡地址",
                               "network_host: " + str(item["network_host"]),
                               "为了与其他服务器上的节点进行通信并形成集群，节点将需要绑定到非环回地址"]

        if "bootstrap_memory_lock" in item:
            check_result = PASS if str(item["bootstrap_memory_lock"]).upper() == "TRUE" else FAIL
            es_dict["内存锁定"] = [check_result,
                               "为保证es不使用swap空间,建议将该参数设置为true",
                               "bootstrap_memory_lock: " + str(item["bootstrap_memory_lock"]),
                               "为保证es不使用swap空间,建议将该参数设置为true(需要同步设置内核参数:/etc/security/limits.conf:elasticsearch hard(soft) memlock unlimited)"]

        if "action_destructive_requires_name" in item:
            check_result = PASS if str(item["action_destructive_requires_name"]).upper() == "TRUE" else FAIL
            es_dict["操作索引时指定名称"] = [check_result,
                                    "生产环境建议配置为true，防止索引被误删",
                                    "action_destructive_requires_name: " + str(
                                        item["action_destructive_requires_name"]),
                                    "设置为true后，只限于使用特定名称来删除索引，禁止使用_all或通配符来删除索引(action.destructive_requires_name)"]

        if "discovery_zen_minimum_master_nodes" in item:
            es_dict["绑定主机"] = [MAN,
                               "为了避免脑裂，候选主节点的数量应该设置为:(master_eligible_nodes / 2) + 1",
                               "discovery_zen_minimum_master_nodes: " + str(item["discovery_zen_minimum_master_nodes"]),
                               "为了防止数据丢失,以便每个候选主节点知道为了形成集群而必须可见的最少数量的候选主节点"]

        if "es_status" in item:
            es_dict["es基本信息"] = ["", "无", "".join(item["es_status"]).rstrip(), "当前es节点id,版本等基本信息"]

        if "es_allocation" in item and len(item["es_allocation"]) > 0:
            es_allocation_str = "".join(item["es_allocation"]).rstrip()
            es_dict["es资源分配总览"] = ["", "相应资源使用率均不超过80%",
                                   es_allocation_str,
                                   "当前es节点内部资源分配情况"]
            if "error" not in es_allocation_str:
                check_allocation(es_dict, item["es_allocation"])

        if "es_node_health" in item and len(item["es_node_health"]) > 0:
            status, result = judge_by_status(item["es_node_health"])
            check_result = PASS if str(status) == "green" else FAIL
            es_dict["当前节点健康情况"] = [check_result, "当前es节点健康情况为:green",
                                   str(status), result]

        if "es_cluster_health" in item and len(item["es_cluster_health"]) > 0:
            status, result = judge_by_status(item["es_cluster_health"])
            check_result = PASS if str(status) == "green" else FAIL
            es_dict["集群整体健康情况"] = [check_result, "当前es集群健康情况为:green",
                                   str(status), result]

        if "es_shards" in item and len(item["es_shards"]) > 0:
            check_result = PASS if judge_shards(item["es_shards"]) else FAIL
            es_dict["节点分片信息"] = [check_result, "state:所有分片状态都为STARTED(正常分片)",
                                 "".join(item["es_shards"]).rstrip(),
                                 "health健康状态为异常时才需要关注。state：分片状态，STARTED为正常分片，INITIALIZING为异常分片"]

        if "es_tasks" in item:
            es_dict["任务列表"] = ["", "所有任务正常执行",
                               "".join(item["es_tasks"]).rstrip(),
                               "es节点中的"]

        if "es_pending_tasks" in item and len(item["es_pending_tasks"]) > 0:
            check_result = PASS if judge_pending_tasks(item["es_pending_tasks"]) else FAIL
            es_dict["挂起任务"] = [check_result, "无挂起任务(\"tasks\" : [ ])",
                               "".join(item["es_pending_tasks"]).rstrip(),
                               "es节点中挂起的任务(pending_tasks)"]

        if "es_thread_pool" in item and len(item["es_thread_pool"]) > 0:
            check_result = PASS if judge_thread_rejected(item["es_thread_pool"]) else FAIL
            es_dict["线程池情况"] = [check_result, "rejected(写入被拒绝参数对应值)都为0",
                                "".join(item["es_thread_pool"]).rstrip(),
                                "查看当前线程情况"]

        # 将当前es信息转存合并至java_dict中
        for java_dict in java_list:
            if java_dict["进程ID"] == es_dict["进程ID"]:
                java_dict["进程类型："] = ["elasticsearch", "", "", ""]
                for k in es_dict:
                    java_dict[k] = es_dict[k]
