#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os

import utils

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def check_broker_config(rocketmq_dict, config_content):
    temp_dict = dict()
    temp_dict["fileReservedTime"] = 48
    temp_dict["brokerRole"] = "ASYNC_MASTER"
    temp_dict["flushDiskType"] = "ASYNC_FLUSH"
    temp_dict["autoCreateTopicEnable"] = "true"
    temp_dict["sendMessageThreadPoolNums"] = 1
    temp_dict["useReentrantLockWhenPutMessage"] = "false"  # 4.1 版本以上才有
    temp_dict["waitTimeMillsInSendQueue"] = 200
    temp_dict["transientStorePoolEnable"] = "false"
    temp_dict["slaveReadEnable"] = "false"
    temp_dict["transferMsgByHeap"] = "true"
    temp_dict["warmMapedFileEnable"] = "false"

    for line in config_content:
        if line.startswith("fileReservedTime"):
            temp_dict["fileReservedTime"] = line.split("=")[1].strip()
        if line.startswith("brokerRole"):
            temp_dict["brokerRole"] = line.split("=")[1].strip()
        if line.startswith("flushDiskType"):
            temp_dict["flushDiskType"] = line.split("=")[1].strip()
        if line.startswith("autoCreateTopicEnable"):
            temp_dict["autoCreateTopicEnable"] = line.split("=")[1].strip()
        if line.startswith("sendMessageThreadPoolNums"):
            temp_dict["sendMessageThreadPoolNums"] = line.split("=")[1].strip()
        if line.startswith("useReentrantLockWhenPutMessage"):
            temp_dict["useReentrantLockWhenPutMessage"] = line.split("=")[1].strip()
        if line.startswith("waitTimeMillsInSendQueue"):
            temp_dict["waitTimeMillsInSendQueue"] = line.split("=")[1].strip()
        if line.startswith("transientStorePoolEnable"):
            temp_dict["transientStorePoolEnable"] = line.split("=")[1].strip()
        if line.startswith("slaveReadEnable"):
            temp_dict["slaveReadEnable"] = line.split("=")[1].strip()
        if line.startswith("transferMsgByHeap"):
            temp_dict["transferMsgByHeap"] = line.split("=")[1].strip()
        if line.startswith("warmMapedFileEnable"):
            temp_dict["warmMapedFileEnable"] = line.split("=")[1].strip()

    # 开始检查各配置项
    check_result = PASS if int(temp_dict["fileReservedTime"]) >= 72 else FAIL
    rocketmq_dict["持久化消息保存周期"] = [check_result,
                                  "大于等于72小时",
                                  "fileReservedTime = " + str(temp_dict["fileReservedTime"]),
                                  "超过该周期将被清理(空间允许情况下建议设置为72小时及以上)"]

    check_result = PASS if str(temp_dict["brokerRole"]) == "ASYNC_MASTER" else FAIL
    rocketmq_dict["主从异步复制"] = [check_result,
                               "ASYNC_MASTER",
                               "brokerRole = " + temp_dict["brokerRole"],
                               "是否开启主从异步复制"]

    check_result = PASS if str(temp_dict["flushDiskType"]) == "ASYNC_FLUSH" else FAIL
    rocketmq_dict["异步刷盘"] = [check_result,
                             "ASYNC_FLUSH",
                             "flushDiskType = " + temp_dict["flushDiskType"],
                             "同步刷盘TPS过低，较难满足业务发展需求"]

    check_result = PASS if temp_dict["autoCreateTopicEnable"].upper() == "FALSE" else FAIL
    rocketmq_dict["自动创建topic"] = [check_result,
                                  "生产环境建议关闭(false)",
                                  "autoCreateTopicEnable = " + temp_dict["autoCreateTopicEnable"],
                                  "是否自动创建默认topic"]

    check_result = PASS if int(temp_dict["sendMessageThreadPoolNums"]) >= 32 else FAIL
    rocketmq_dict["发送消息的最大线程数"] = [check_result,
                                   "大于等于32",
                                   "sendMessageThreadPoolNums = " + str(temp_dict["sendMessageThreadPoolNums"]),
                                   "发送消息的最大线程数,默认1，建议32+"]

    check_result = PASS if temp_dict["useReentrantLockWhenPutMessage"].upper() == "TRUE" else FAIL
    rocketmq_dict["使用可重入锁"] = [check_result,
                               "建议开启(true)",
                               "useReentrantLockWhenPutMessage = " + temp_dict["useReentrantLockWhenPutMessage"],
                               "4.1版本以上才有该参数,小于该版本请忽略"]

    check_result = PASS if int(temp_dict["waitTimeMillsInSendQueue"]) >= 1000 else FAIL
    rocketmq_dict["发送消息等待时间"] = [check_result,
                                 "大于等于1000(ms)",
                                 "waitTimeMillsInSendQueue = " + str(temp_dict["waitTimeMillsInSendQueue"]),
                                 "发送消息线程等待时间,默认200ms"]

    check_result = PASS if temp_dict["transientStorePoolEnable"].upper() == "TRUE" else FAIL
    rocketmq_dict["临时存储池"] = [check_result,
                              "建议开启(true)",
                              "transientStorePoolEnable = " + temp_dict["transientStorePoolEnable"],
                              "开启临时存储池(消息写入到堆外内存，消费时从pageCache消费，读写分离，提升集群性能)"]

    check_result = PASS if temp_dict["slaveReadEnable"].upper() == "TRUE" else FAIL
    rocketmq_dict["Slave读权限"] = [check_result,
                                 "建议开启(true)",
                                 "slaveReadEnable = " + temp_dict["slaveReadEnable"],
                                 "消息占用物理内存的大小通过accessMessageInMemoryMaxRatio来配置默认为40%;如果消费的消息不在内存中，开启slaveReadEnable时会从slave节点读取.提高Master内存利用率）"]

    check_result = PASS if temp_dict["transferMsgByHeap"].upper() == "FALSE" else FAIL
    rocketmq_dict["堆内存数据传输"] = [check_result,
                                "建议关闭(false)",
                                "transferMsgByHeap = " + temp_dict["transferMsgByHeap"],
                                "关闭堆内存数据传输(Broker响应消费请求时，不必将数据重新读到堆内存再发送给客户端；直接从PageCache将数据发送给客户端)"]

    check_result = PASS if temp_dict["warmMapedFileEnable"].upper() == "TRUE" else FAIL
    rocketmq_dict["文件预热"] = [check_result,
                             "建议开启(true)",
                             "warmMapedFileEnable = " + temp_dict["warmMapedFileEnable"],
                             "开启文件预热(避免日志文件在分配内存时缺页中断)"]


def rocketmq_analysis(output_dir, ip, java_list):
    rocketmq_file = output_dir + "/data/" + ip + "_rocketmq.txt"
    if not os.path.exists(rocketmq_file):
        return list()
    dict_list = utils.json_to_format_dict_list(rocketmq_file)
    for item in dict_list:
        rocketmq_dict = dict()

        rocketmq_dict["进程类型："] = ["rocketmq", "", "", ""]
        rocketmq_dict["进程ID"] = ["", "进程信息标记", item["PID"], "当前进程的PID"]
        rocketmq_dict["进程命令行"] = ["", "进程信息标记", item["CMD"], "当前进程的命令行"]

        if "max_open_files" in item and item["max_open_files"].isdigit():
            check_result = PASS if int(item["max_open_files"]) > 60000 else FAIL
            rocketmq_dict["最大文件数(硬限制)"] = [check_result,
                                           "大于 60000",
                                           item["max_open_files"],
                                           "当前rocketmq进程所被允许打开的最大文件数(硬限制)"]
            if "lsof_count" in item:
                target_num = int(int(item["max_open_files"]) * 0.8)
                check_result = PASS if int(item["lsof_count"]) < target_num else FAIL
                rocketmq_dict["当前使用文件数"] = [check_result,
                                            "小于max_open_files * 80% = " + str(target_num),
                                            str(item["lsof_count"]),
                                            "当前进程的句柄使用数量"]
        if "max_open_files_s" in item and item["max_open_files_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 40000 else FAIL
            rocketmq_dict["最大文件数(软限制)"] = [check_result,
                                           "大于 40000",
                                           item["max_open_files_s"],
                                           "当前rocketmq进程使用句柄数超过这个值，则会产生告警(软限制)"]
        if "max_user_processes" in item and item["max_user_processes"].isdigit():
            check_result = PASS if int(item["max_user_processes"]) > 60000 else FAIL
            rocketmq_dict["最大进程数(硬限制)"] = [check_result,
                                           "大于 60000",
                                           item["max_user_processes"],
                                           "当前rocketmq进程管理用户被允许打开的最大进程数量(硬限制)"]
        if "max_user_processes_s" in item and item["max_user_processes_s"].isdigit():
            check_result = PASS if int(item["max_open_files_s"]) > 40000 else FAIL
            rocketmq_dict["最大进程数(软限制)"] = [check_result,
                                           "大于 40000",
                                           item["max_open_files_s"],
                                           "当前rocketmq进程管理用户打开进程数超过这个值，则会产生告警(软限制)"]

        if "error_logs" in item:
            rocketmq_dict["异常日志筛选"] = [MAN,
                                       "无异常错误信息", "见备注",
                                       str(item["error_logs"])]
        if "rocketmq_home" in item:
            rocketmq_dict["rocketmq_home"] = ["", "无", str(item["rocketmq_home"]), "rocketmq家目录"]

        if "config_file" in item:
            rocketmq_dict["配置文件位置"] = ["", "broker.conf", str(item["config_file"]), "broker配置文件位置"]

        if "config_content" in item:
            rocketmq_dict["配置文件内容总览"] = ["", "无异常配置信息", "".join(item["config_content"]).rstrip(), "broker配置文件内容"]
            check_broker_config(rocketmq_dict, item["config_content"])

        # 运行状态检查
        if "topic_status" in item:
            rocketmq_dict["topic详细情况"] = [MAN, "正常返回topic信息,消息积压(Accumulation)不超过5000",
                                          "".join(item["topic_status"]).rstrip(),
                                          "查看topic详细情况，包括消费组"]
        if "name_server_config" in item:
            rocketmq_dict["名称服务器配置"] = [MAN, "正常返回名称服务器配置信息(一般无需额外配置)",
                                        '"' + "".join(item["name_server_config"]).rstrip() + '"',
                                        "查看名称服务器配置信息"]
        if "clusterList" in item:
            rocketmq_dict["集群列表"] = [MAN, "返回集群列表",
                                     "".join(item["name_server_config"]).rstrip(),
                                     "由于RocketMQ常规配置无法进行主从切换，建议使用双主双从进行搭建"]

        # 将当前rocketmq信息转存合并至java_dict中
        for java_dict in java_list:
            if java_dict["进程ID"] == rocketmq_dict["进程ID"]:
                java_dict["进程类型："] = ["rocketmq", "", "", ""]
                for k in rocketmq_dict:
                    java_dict[k] = rocketmq_dict[k]
