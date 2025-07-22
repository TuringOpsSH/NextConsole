#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os

import utils


def notes_analysis(output_dir, ip):
    notes_file = output_dir + "/data/" + ip + "_notes.txt"
    if not os.path.exists(notes_file):
        return list()
    dict_list = utils.json_to_format_dict_list(notes_file)
    analysis_dict_list = list()
    for item in dict_list:
        notes_dict = dict()
        if "javaCount" in item:
            notes_dict["java进程数"] = ['', '', str(item["javaCount"]), '']
        if "weblogicCount" in item:
            notes_dict["weblogic进程数"] = ['', '', str(item["weblogicCount"]), '']
        if "nginxCount" in item:
            notes_dict["nginx进程数"] = ['', '', str(item["nginxCount"]), '']
        if "redisCount" in item:
            notes_dict["redis进程数"] = ['', '', str(item["redisCount"]), '']
        if "rabbitmqCount" in item:
            notes_dict["rabbitmq进程数"] = ['', '', str(item["rabbitmqCount"]), '']
        if "rocketmqCount" in item:
            notes_dict["rocketmq进程数"] = ['', '', str(item["rocketmqCount"]), '']
        if "elasticSearchCount" in item:
            notes_dict["elasticsearch进程数"] = ['', '', str(item["elasticSearchCount"]), '']
        if "zookeeperCount" in item:
            notes_dict["zookeeper进程数"] = ['', '', str(item["zookeeperCount"]), '']
        if "tomcatCount" in item:
            notes_dict["Tomcat进程数"] = ['', '', str(item["tomcatCount"]), '']
        if "tomcatCount" in item:
            notes_dict["Tomcat进程数"] = ['', '', str(item["tomcatCount"]), '']
        if "httpdCount" in item:
            notes_dict["Apache httpd进程数"] = ['', '', str(item["httpdCount"]), '']
        analysis_dict_list.append(notes_dict)

    return analysis_dict_list
