#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os
import utils
import json

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def comparison(replicas, isr):
    replicas_split = replicas.split(",")
    isr_split = isr.split(",")
    if sorted(replicas_split) == sorted(isr_split):
        return True
    else:
        return False


def judge_replicas(topic_describe):
    for one_topic in topic_describe:
        for one_partition in one_topic:
            # 这里加个判断，如果replication_factor小于等于4，则跳过
            if len(one_partition.split()) <= 4:
                continue
            if one_partition.split()[4] == "ReplicationFactor:":
                # replication_factor = one_partition.split()[5]
                # if int(replication_factor) <= 1:
                #     return False
                continue
            if one_partition.split()[4] == "Leader:":
                leader = one_partition.split()[5]
                if int(leader) == -1:
                    return False
            if one_partition.split()[6] == "Replicas:" and one_partition.split()[8] == "Isr:":
                replicas = one_partition.split()[7]
                isr = one_partition.split()[9]
                if not comparison(replicas, isr):
                    return False
        return True


def judge_consumers(consumers):
    for line in consumers:
        line_split = line.split()
        if len(line_split):
            if line_split[5] == "LAG" or line_split[5] == "-":
                continue
            if int(line_split[5]) >= 1000:
                return False
    return True


def check_server_config(kafka_dict, config_content):
    temp_dict = dict()
    temp_dict["num_partitions"] = 1
    temp_dict["auto_create_topics_enable"] = "true"
    temp_dict["unclean_leader_election_enable"] = "true"
    temp_dict["auto_leader_rebalance_enable"] = "true"
    temp_dict["log_retention_hours"] = 168
    temp_dict["zookeeper_connect"] = ""

    for line in config_content:
        if line.startswith("num.partitions"):
            temp_dict["num_partitions"] = line.split("=")[1].strip()
        if line.startswith("default.replication.factor"):
            temp_dict["default_replication_factor"] = line.split("=")[1].strip()
        if line.startswith("auto.create.topics.enable"):
            temp_dict["auto_create_topics_enable"] = line.split("=")[1].strip()
        if line.startswith("unclean.leader.election.enable"):
            temp_dict["unclean_leader_election_enable"] = line.split("=")[1].strip()
        if line.startswith("auto.leader.rebalance.enable"):
            temp_dict["auto_leader_rebalance_enable"] = line.split("=")[1].strip()
        if line.startswith("log.retention.hours"):
            temp_dict["log_retention_hours"] = line.split("=")[1].strip()
        if line.startswith("zookeeper.connect="):
            temp_dict["zookeeper_connect"] = line.split("=")[1].strip()

    # 开始检查各配置项
    check_result = PASS if int(temp_dict["num_partitions"]) >= 2 else FAIL
    kafka_dict["默认分区数"] = [check_result,
                           "大于等于2",
                           "num.partitions = " + str(temp_dict["num_partitions"]),
                           "topic的默认分区数"]

    if "default_replication_factor" in temp_dict:
        check_result = PASS if int(temp_dict["default_replication_factor"]) >= 2 else FAIL
        kafka_dict["默认备份因子数"] = [check_result,
                                 "大于等于2",
                                 "default.replication.factor = " + temp_dict["default_replication_factor"],
                                 "topic的默认备份数"]

    check_result = PASS if int(temp_dict["log_retention_hours"]) >= 72 else FAIL
    kafka_dict["持久化消息保存周期"] = [check_result,
                               "大于等于72小时",
                               "log.retention.hours = " + str(temp_dict["log_retention_hours"]),
                               "超过该周期将被清理(空间允许情况下建议设置为72小时及以上)"]

    check_result = PASS if temp_dict["auto_create_topics_enable"].upper() == "FALSE" else FAIL
    kafka_dict["自动创建topic"] = [check_result,
                               "生产环境建议设置为false，禁用topic自动创建，严格管理topic资源",
                               "auto.create.topics.enable = " + temp_dict["auto_create_topics_enable"],
                               "是否允许自动创建topic，默认值为true。当消息发送到服务端发现topic不存在时会自动创建topic。经常会因开发人员写错topic"
                               "名称，导致服务端存在一些稀奇古怪的topic"]

    check_result = PASS if temp_dict["unclean_leader_election_enable"].upper() == "FALSE" else FAIL
    kafka_dict["unclean leader 选举"] = [check_result,
                                       "生产环境建议设置为false，关闭Unclean leader选举，因为通常数据的一致性要比可用性更加重要。",
                                       "unclean.leader.election.enable = " + temp_dict["unclean_leader_election_enable"],
                                       "是否允许Unclean Leader选举，默认值为true。这个参数用于控制是否允许非同步副本（即不在ISR集合中的副本，参与leader选举，非同步副本中的消息远远落后于leader，如果选举这种副本作为leader可能会造成数据丢失，但会保证服务继续可用。"]

    check_result = PASS if temp_dict["auto_leader_rebalance_enable"].upper() == "FALSE" else FAIL
    kafka_dict["leader partition平衡"] = [check_result,
                                        "考虑到leader重选举的代价比较大，可能会带来性能影响，也可能会引发客户端的阻塞，生产环境建议设置为false",
                                        "auto.leader.rebalance.enable = " + temp_dict["auto_leader_rebalance_enable"],
                                        "是否允许自动leader rebalance功能，默认值为true。默认情况下，Kafka控制器会启动一个定时任务，在满足一定条件（Kafka认为当前leader"
                                        "不够均衡，参考leader.imbalance.per.broker.percentage）时进行leader重选举。"]

    zk_nodes = temp_dict["zookeeper_connect"].split(",")
    check_result = PASS if len(zk_nodes) >= 3 else FAIL
    kafka_dict["zookeeper配置"] = [check_result,
                                 "zk节点数大于等于3",
                                 "zookeeper.connect = " + temp_dict["zookeeper_connect"],
                                 "为保障高可用性，建议zk集群节点数量大于等于3"]


def kafka_analysis(output_dir, ip, java_list):
    kafka_file = output_dir + "/data/" + ip + "_kafka.txt"
    if not os.path.exists(kafka_file):
        return list()
    dict_list = utils.json_to_format_dict_list(kafka_file)
    for item in dict_list:
        kafka_dict = dict()

        kafka_dict["进程类型："] = ["kafka", "", "", ""]
        kafka_dict["进程ID"] = ["", "进程信息标记", item["PID"], "当前进程的PID"]
        kafka_dict["进程命令行"] = ["", "进程信息标记", item["CMD"], "当前进程的命令行"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 60000 else FAIL
            kafka_dict["最大文件数(硬限制)"] = [check_result,
                                        "大于 60000",
                                        item["max_open_files"],
                                        "当前kafka进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = PASS if int(item["lsof_count"]) < target_num else FAIL
                kafka_dict["当前使用文件数"] = [check_result,
                                         "小于max_open_files * 80% = " + str(target_num),
                                         str(item["lsof_count"]),
                                         "当前进程的句柄使用数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 40000 else FAIL
            kafka_dict["最大文件数(软限制)"] = [check_result,
                                        "大于 40000",
                                        item["max_open_files_s"],
                                        "当前kafka进程使用句柄数超过这个值，则会产生告警(软限制)"]
        if "max_user_processes" in item and item["max_user_processes"].isdigit():
            check_result = PASS if int(item["max_user_processes"]) > 60000 else FAIL
            kafka_dict["最大进程数(硬限制)"] = [check_result,
                                        "大于 60000",
                                        item["max_user_processes"],
                                        "当前kafka进程管理用户被允许打开的最大进程数量(硬限制)"]
        if "max_user_processes_s" in item and item["max_user_processes_s"].isdigit():
            check_result = PASS if int(item["max_user_processes_s"]) > 40000 else FAIL
            kafka_dict["最大进程数(软限制)"] = [check_result,
                                        "大于 40000",
                                        item["max_user_processes_s"],
                                        "当前kafka进程管理用户打开进程数超过这个值，则会产生告警(软限制)"]

        if "error_logs" in item:
            kafka_dict["异常日志筛选"] = [MAN,
                                    "无异常错误信息", "见备注",
                                    str(item["error_logs"])[:1000]]
        if "kafka_home" in item:
            kafka_dict["kafka_home"] = ["", "无", str(item["kafka_home"]), "kafka家目录"]

        if "config_file" in item:
            kafka_dict["配置文件位置"] = ["", "broker.conf", str(item["config_file"]), "broker配置文件位置"]

        if "config_content" in item:
            kafka_dict["配置文件内容总览"] = ["", "无异常配置信息", "".join(item["config_content"]).rstrip(), "broker配置文件内容"]
            check_server_config(kafka_dict, item["config_content"])

        # topic状态检查
        if "topic_describes" in item:
            check_result = PASS if judge_replicas(item["topic_describes"]) else FAIL
            kafka_dict["topic健康状态"] = [check_result, "topic各个partitions的leader都不为-1且replicas和lsr一致",
                                       # "".join('%s' % topic for topic in item["topic_describes"]),
                                       "".join('%s' % "".join(topic) for topic in item["topic_describes"]),
                                       "topic详细情况(describe)，除筛选项外，每个分区建议有2个以上副本"]
        # consumer 检查
        if "consumers_stat" in item:
            check_result = PASS if judge_consumers(item["consumers_stat"]) else FAIL
            kafka_dict["consumers状况检查"] = [check_result, "每个分区（partition）积压消息数量（LAG）小于1000",
                                           "".join('%s' % "".join(topic) for topic in item["consumers_stat"]),
                                           "当前broker的消费者情况"]

        # 将当前kafka信息转存合并至java_dict中
        for java_dict in java_list:
            if java_dict["进程ID"] == kafka_dict["进程ID"]:
                java_dict["进程类型："] = ["kafka", "", "", ""]
                for k in kafka_dict:
                    java_dict[k] = kafka_dict[k]
