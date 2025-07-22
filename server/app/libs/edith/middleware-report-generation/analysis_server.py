#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def check_disk(disk_df):
    flag = PASS
    for item in disk_df:
        if "Filesystem" or "文件系统" in item:
            continue
        temp_percent = item.split()[4].replace("%", "")
        if temp_percent.isdigit():
            percent = int(item.split()[4].replace("%", ""))
            if percent >= 80:
                flag = FAIL

    return [flag, "磁盘分区的使用率不能超过80%", "".join(disk_df).rstrip(),
            "文件系统使用率"]


def check_open_files(ulimit_conf):
    flag = PASS
    for item in ulimit_conf:
        if "nofile" in item and "hard" in item:
            try:
                max_open_files = (item.split()[3]).strip()
                if int(max_open_files) < 40000:
                    flag = FAIL
            except:
                print("Error--->" + item)
    return [flag, "最大打开文件数默认1024，硬限制建议配置为40000+",
            "".join(ulimit_conf).rstrip(), "单进程打开的最大文件数"]


def server_analysis(output_dir, ip, notes_list):
    server_file = output_dir + "/data/" + ip + "_server.txt"
    if not os.path.exists(server_file):
        return list()
    dict_list = utils.json_to_format_dict_list(server_file)
    analysis_dict_list = list()
    for item in dict_list:
        server_dict = dict()
        server_dict["服务器概况"] = ["", "", "", ""]
        server_dict["主机名"] = [PASS if "localhost" not in item["hostname"] else FAIL,
                              "非localhost.localdomain主机名",
                              item["hostname"],
                              "当前主机的主机名"]

        server_dict["IP地址"] = [PASS if utils.match_first(item["ip"], item["showIp"]) else FAIL,
                               "ip为本机实际有效IP",
                               item["ip"],
                               "当前主机名对应的IP地址"]

        server_dict["所有IP"] = ["", "无",
                               item["showIp"],
                               "当前主机所有IP地址"]

        if "MemTotal" and "MemFree" and "Buffers" and "Cached" in item:
            server_dict["总内存"] = ["", "无", str(
                int(int(item["MemTotal"]) / 1024)) + "MB", "当前主机的总内存(MB)"]

            actual_memory_usage = int(
                item["MemTotal"]) - int(item["MemFree"]) - int(item["Buffers"]) - int(item["Cached"])
            check_result = "符合" if actual_memory_usage < int(
                item["MemTotal"]) * 0.8 else "不符合"
            server_dict["实际已使用内存"] = [check_result, "小于总内存的80%",
                                      str(int(actual_memory_usage / 1024)) + "MB",
                                      "当前主机实际已使用的内存(MB)"]
        server_dict["CPU核数"] = ["", "", item["cpu"], "当前服务器的CPU核数"]
        server_dict["系统版本"] = ["", "", item["osVersion"], "操作系统版本"]
        if "machine" in item:
            #server_dict["机器型号"] = [PASS if utils.match_first("VMware", item["machine"]) else MAN,
            server_dict["机器型号"] = ["",
                                   #"应用服务器建议采用虚拟机",
                                   "无",
                                   utils.grep("Product Name: ",
                                              item["machine"])[1],
                                   "当前服务器型号"]
        server_dict["启动时间"] = ["", "启动时间", item["uptime"], "服务器启动时间"]
        server_dict["文件系统使用率"] = check_disk(item["disk"])
        server_dict["最大打开文件数"] = check_open_files(item["ulimit"])

        if "net_core_somaxconn" in item:
            check_result = PASS if int(
                item["net_core_somaxconn"]) >= 2048 else MAN
            server_dict["内核参数somaxconn"] = ["",
                                            "大于等于2048",
                                            item["net_core_somaxconn"],
                                            "socket监听(listen)的backlog上限，并发量高的应用需要配置此参数"]
        if "net_ipv4_tcp_max_syn_backlog" in item:
            check_result = PASS if int(
                item["net_ipv4_tcp_max_syn_backlog"]) >= 1024 else MAN
            server_dict["内核参数max_syn_backlog"] = ["",
                                                  "大于等于1024",
                                                  item["net_ipv4_tcp_max_syn_backlog"],
                                                  "处于SYN_RECV的TCP最大连接数，当处于SYN_RECV状态的TCP连接数超过tcp_max_syn_backlog后，会丢弃后续的SYN报文"]
        if "overcommit_memory" in item:
            try:
                check_result = PASS if int(
                    item["overcommit_memory"]) == 0 and notes_list[0]["redis进程数"][2] != '0' else FAIL
                server_dict["内核参数overcommit_memory"] = ["",
                                                        "默认0，如果有redis/rocketmq进程，建议设置为1",
                                                        item["overcommit_memory"],
                                                        "内存过载分配策略"]
            except:
                pass
        if "vm_swappiness" in item:
            check_result = PASS if int(item["vm_swappiness"]) == 10 else MAN
            server_dict["内核参数vm_swappiness"] = ["",
                                                "默认10，有调整的需要关注",
                                                item["vm_swappiness"],
                                                "当总内存剩余比例低于vm_swappiness时，系统会将最不经常使用的内存交换至swap硬盘分区"]

        analysis_dict_list.append(server_dict)
    return analysis_dict_list
