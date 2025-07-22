#! /usr/bin/python
# -*- coding: UTF-8 -*-

import re
import warnings
import time
import datetime
import getopt
import logging
import os
import sys
import json

log_dir = './logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'app.log')
if not os.path.isfile(log_file):
    open(log_file, 'a').close()

logging.basicConfig(level=logging.INFO, filename=log_file, encoding='UTF-8',
                    filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    global_pyeek = os.path.join(os.path.dirname(__file__), '../eek-pyeek')
    sys.path.insert(0, global_pyeek)
    #
    # 在这里导入 Edith-Desk 公共模块可以避免代码格式化时可能导致的导入次序错误
    #
except Exception as e:
    logging.error(f"导入模块失败: {e}")
    sys.exit(1)

try:
    buildin_pyeek = os.path.join(os.path.dirname(__file__), './pyeek')
    sys.path.insert(0, buildin_pyeek)

    sys.path.insert(0, './')
    #
    # 在这里导入应用私有模块可以避免代码格式化时可能导致的导入次序错误
    #
    import utils
    import func_style
    import analysis_bes
    import analysis_httpd
    import analysis_kafka
    import analysis_wls
    import analysis_tomcat
    import analysis_zookeeper
    import analysis_elasticsearch
    import analysis_rocketmq
    import analysis_rabbitmq
    import analysis_server
    import analysis_redis
    import analysis_notes
    import analysis_nginx
    import analysis_java
    import analysis_activemq
    import pandas as pd
    import gen_word
    import analysis_was
except Exception as e:
    logging.error(f"导入模块失败: {e}")
    sys.exit(1)

usage = """"""
action = ""
datadir = ""


warnings.filterwarnings("ignore")

PASS = "符合"
FAIL = "不符合"
MAN = "人工复核"


def analysis_data(system):
    # 这里完成我们数据的写入工作
    result_fail = list()
    result_man = list()
    result_ok = list()
    result_info = list()
    summary = {}
    for current_ip in system.ips:
        summary[current_ip] = {
            'name': system.name,
            'danger': 0,
            'warn': 0,
            'ok': 0,
        }
        analysis_dict_list = list()
        try:
            notes_list = analysis_notes.notes_analysis(base_dir, current_ip)
            server_list = analysis_server.server_analysis(base_dir, current_ip, notes_list)
            java_list = analysis_java.java_analysis(base_dir, current_ip)
            redis_list = analysis_redis.redis_analysis(base_dir, current_ip)
            nginx_list = analysis_nginx.nginx_analysis(base_dir, current_ip)
            rabbitmq_list = analysis_rabbitmq.rabbitmq_analysis(base_dir, current_ip)
            httpd_list = analysis_httpd.httpd_analysis(base_dir, current_ip)
            # 合并weblogic到java
            analysis_wls.wls_analysis(base_dir, current_ip, java_list)
            # 合并rocketmq到java
            analysis_rocketmq.rocketmq_analysis(base_dir, current_ip, java_list)
            # 合并elasticsearch到java
            analysis_elasticsearch.elasticsearch_analysis(
                base_dir, current_ip, java_list)
            # 合并zookeeper到java
            analysis_zookeeper.zookeeper_analysis(base_dir, current_ip, java_list)
            # 合并tomcat到java
            analysis_tomcat.tomcat_analysis(base_dir, current_ip, java_list)
            # 合并kafka到java
            analysis_kafka.kafka_analysis(base_dir, current_ip, java_list)
            # 合并bes application server 到java
            analysis_bes.bes_analysis(base_dir, current_ip, java_list)
            # 合并Activemq到 java
            analysis_activemq.activemq_analysis(base_dir, current_ip, java_list)
            # 合并was到java
            analysis_was.was_analysis(base_dir, current_ip, java_list)

            analysis_dict_list.append(notes_list)
            analysis_dict_list.append(server_list)
            analysis_dict_list.append(java_list)
            analysis_dict_list.append(redis_list)
            analysis_dict_list.append(nginx_list)
            analysis_dict_list.append(rabbitmq_list)
            analysis_dict_list.append(httpd_list)

            # 过滤筛选有问题的检查项
            for d_class_list in analysis_dict_list:
                for d_process_dict in d_class_list:
                    for item in d_process_dict:
                        if "进程ID" in d_process_dict:
                            pid = d_process_dict["进程ID"][2]
                        else:
                            pid = ""

                        if "进程类型：" in d_process_dict:
                            pidType = d_process_dict["进程类型："][0]
                        else:
                            pidType = ""

                        result = [system.name, current_ip, pid, pidType, item, d_process_dict[item][0], d_process_dict[item][1],
                                 d_process_dict[item][2], d_process_dict[item][3]]

                        result = [str(x).strip() for x in result]

                        if re.match('#', result[7]) or re.search('\\n', result[7]):
                            result[7] = '(请查看原始日志)'

                        if not result[6].startswith('建议'):
                            result[6] = '建议' + result[6]

                        #处理统计信息被合并的问题
                        #if d_process_dict[item][0] == FAIL and pidType == system.name:
                        if d_process_dict[item][0] == FAIL:
                            summary[current_ip]['danger'] += 1
                            result_fail.append(result)
                        elif d_process_dict[item][0] == MAN:
                            summary[current_ip]['warn'] += 1
                            result_man.append(result)
                        elif d_process_dict[item][0] == PASS:
                            summary[current_ip]['ok'] += 1
                            result_ok.append(result)
                        else:
                             result_info.append(result)
        except Exception as e:
            logging.error(f"Error analyzing data for IP {current_ip}: {str(e)}")
    return {
        'result_fail': result_fail,
        'result_man': result_man,
        'result_ok': result_ok,
        'result_info': result_info,
        'summary': summary,
        'app': system.name
    }


def write_data(output_file, system_statistics):
    # 这里完成我们数据的写入工作
    result_fail = list()
    result_man = list()
    for current_ip in system.ips:
        analysis_dict_list = list()
        notes_list = analysis_notes.notes_analysis(base_dir, current_ip)
        server_list = analysis_server.server_analysis(
            base_dir, current_ip, notes_list)
        java_list = analysis_java.java_analysis(base_dir, current_ip)
        redis_list = analysis_redis.redis_analysis(base_dir, current_ip)
        nginx_list = analysis_nginx.nginx_analysis(base_dir, current_ip)
        rabbitmq_list = analysis_rabbitmq.rabbitmq_analysis(
            base_dir, current_ip)
        httpd_list = analysis_httpd.httpd_analysis(base_dir, current_ip)
        # 合并weblogic到java
        analysis_wls.wls_analysis(base_dir, current_ip, java_list)
        # 合并rocketmq到java
        analysis_rocketmq.rocketmq_analysis(base_dir, current_ip, java_list)
        # 合并elasticsearch到java
        analysis_elasticsearch.elasticsearch_analysis(
            base_dir, current_ip, java_list)
        # 合并zookeeper到java
        analysis_zookeeper.zookeeper_analysis(base_dir, current_ip, java_list)
        # 合并tomcat到java
        analysis_tomcat.tomcat_analysis(base_dir, current_ip, java_list)
        # 合并kafka到java
        analysis_kafka.kafka_analysis(base_dir, current_ip, java_list)
        # 合并bes application server 到java
        analysis_bes.bes_analysis(base_dir, current_ip, java_list)
        # 合并Activemq到 java
        analysis_activemq.activemq_analysis(base_dir, current_ip, java_list)
        # 合并Activemq到 java
        analysis_was.was_analysis(base_dir, current_ip, java_list)

        analysis_dict_list.append(notes_list)
        analysis_dict_list.append(server_list)
        analysis_dict_list.append(java_list)
        analysis_dict_list.append(redis_list)
        analysis_dict_list.append(nginx_list)
        analysis_dict_list.append(rabbitmq_list)
        analysis_dict_list.append(httpd_list)
        one_ip_node_data = pd.DataFrame.from_dict(dict())
        split_line = dict()
        split_line["----split----"] = ['------------',
                                       '------------', '------------', '------------']
        for mw_item_list in analysis_dict_list:
            for item in mw_item_list:
                temp_df = pd.DataFrame.from_dict(data=item, orient='index', columns=[
                                                 '检查结果', '预期值', '当前值', '备注'])
                one_ip_node_data = pd.concat([one_ip_node_data, temp_df])
                temp_df = pd.DataFrame.from_dict(split_line, orient='index', columns=[
                                                 '检查结果', '预期值', '当前值', '备注'])
                one_ip_node_data = pd.concat([one_ip_node_data, temp_df])

        if os.path.exists(output_file):
            with pd.ExcelWriter(output_file, mode='a', engine='openpyxl') as writer:
                if len(one_ip_node_data) == 0:  # 当前ip无可写入的数据
                    continue
                else:
                    one_ip_node_data.reset_index(drop=False).style \
                        .applymap(func_style.result, subset=['检查结果']) \
                        .applymap(func_style.param, subset=['index']) \
                        .applymap(func_style.split, subset=['预期值', '当前值', '备注']) \
                        .to_excel(writer, sheet_name=current_ip, index=False, header=True, encoding='utf-8')
                    func_style.set_width_ip_data(writer, current_ip)
        else:
            one_ip_node_data.to_excel(output_file, sheet_name=current_ip, index=True, index_label='参数',
                                      header=True)
        # 过滤筛选有问题的检查项
        for d_class_list in analysis_dict_list:
            for d_process_dict in d_class_list:
                for item in d_process_dict:
                    system_statistics.plus_total_items()
                    if "进程ID" in d_process_dict:
                        pid = d_process_dict["进程ID"][2]
                    else:
                        pid = ""
                    if "进程类型：" in d_process_dict:
                        pidType = d_process_dict["进程类型："][0]
                    else:
                        pidType = ""
                    if d_process_dict[item][0] == FAIL:
                        system_statistics.plus_total_fail()
                        result_fail.append(
                            [current_ip, pid, pidType, item, d_process_dict[item][0], d_process_dict[item][1],
                             d_process_dict[item][2],
                             d_process_dict[item][3]])
                    if d_process_dict[item][0] == MAN:
                        system_statistics.plus_total_man()
                        result_man.append(
                            [current_ip, pid, pidType, item, d_process_dict[item][0], d_process_dict[item][1],
                             d_process_dict[item][2],
                             d_process_dict[item][3]])
        system_statistics.calculation_total_pass()

    # 写入有问题的检查项
    result_fail_final = utils.uniq_dict_list(result_fail)
    result_man_final = utils.uniq_dict_list(result_man)
    split_line = [['', '', '', '', '', '', '', '']]
    overview = pd.DataFrame(data=result_fail_final,
                            columns=['IP地址', '进程ID', '进程类型', '巡检项', '检查结果', '巡检建议', '当前值', '备注'])
    overview = pd.concat([overview,
                          pd.DataFrame(data=split_line, columns=['IP地址', '进程ID', '进程类型', '巡检项', '检查结果', '巡检建议', '当前值', '备注'])])
    overview = pd.concat([overview,
                          pd.DataFrame(data=result_man_final, columns=['IP地址', '进程ID', '进程类型', '巡检项', '检查结果', '巡检建议', '当前值', '备注'])])

    with pd.ExcelWriter(output_file, mode='a', engine='openpyxl') as wrong_writer:
        overview.reset_index(drop=True).style \
            .applymap(func_style.result, subset=['检查结果']) \
            .to_excel(wrong_writer, sheet_name=u"问题项总览", index=False, header=True)
        func_style.set_width_result(wrong_writer)

    return system_statistics


def write_overall(system_report_dict, output_file, system_stat_list):
    # 1、写入系统列表汇总
    system_sheet_data = []
    for one_system_stat in system_stat_list:
        fail_proportion = 0
        man_proportion = 0
        if one_system_stat.total_items != 0:
            fail_proportion = round(
                (one_system_stat.total_fail / one_system_stat.total_items) * 100, 2)
            man_proportion = round(
                (one_system_stat.total_man / one_system_stat.total_items) * 100, 2)
        line = [
            one_system_stat.name, one_system_stat.leader, one_system_stat.total_items,
            one_system_stat.total_fail, one_system_stat.total_man, fail_proportion, man_proportion]
        system_sheet_data.append(line)
    system_sheet = pd.DataFrame(data=system_sheet_data, columns=[
                                '系统名称', '负责人', '总检查项', FAIL, MAN, '高优先级优化项占比(%)', '低优先级优化项占比(%)'])
    with pd.ExcelWriter(output_file, mode='w', engine='openpyxl') as system_writer:
        system_sheet.to_excel(
            system_writer, sheet_name=u"系统列表", index=False, header=True)
        func_style.set_width_system(system_writer)


def write_wrong_item(report_file_dict):
    overview = pd.DataFrame(data=dict(), columns=[
                            'IP地址', '进程ID', '进程类型', '巡检项', '检查结果', '巡检建议', '当前值', '备注'])
    # item=系统名  output_file_dict[item]=读取excel文件路径
    for item in report_file_dict:
        data = utils.load_error_list_from_excel(report_file_dict[item])
        report_date = datetime.datetime.now().strftime('%Y%m%d')
        error_output_file = report_file_dict[item].rsplit(
            "/", 1)[0] + "/异常一览表_" + report_date + ".xlsx"
        if len(data) != 0:
            split_line = [['所属系统: ', item, '', '', '', '', '', '']]
            split_line_df = pd.DataFrame(data=split_line, columns=[
                                         'IP地址', '进程ID', '进程类型', '巡检项', '检查结果', '巡检建议', '当前值', '备注'])
            data_df = pd.DataFrame(data=data, columns=[
                                   'IP地址', '进程ID', '进程类型', '巡检项', '检查结果', '巡检建议', '当前值', '备注'])
            overview = pd.concat([overview, split_line_df, data_df])

            with pd.ExcelWriter(error_output_file, mode='w', engine='openpyxl') as wrong_writer:
                overview.reset_index(drop=True).style \
                    .applymap(func_style.result, subset=['检查结果']) \
                    .to_excel(wrong_writer, sheet_name=u"问题项总览", index=False, header=True)
                func_style.set_width_result(wrong_writer)


try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["action=", "datadir="])

    # opts = [('--action', 'xls'), ('--datadir', 'E:\\中亦安图\\项目\\运维工具部\\工作内容\\新建文件夹 (6)\\测试')]
    for opt, value in opts:
        if opt == "-h":
            logger.info(usage)
            sys.exit(0)
        if opt == "--action":
            action = value.strip()
        if opt == "--datadir":
            datadir = value.strip("\"")
except Exception as e:
    logger.error(e)
    sys.exit(1)

if action == "xls":

    time_start = time.time()

    # 源数据目录 base_dir + "/data/"
    # 报告目录 base_dir + "/report/"
    now_time = datetime.datetime.now()
    report_date = datetime.datetime.now().strftime('%Y%m%d')
    base_dir = datadir
    if not os.path.exists(base_dir + "/report/"):
        os.mkdir(base_dir + "/report/")

    # 步骤1： 加载系统台账信息
    try:
        system_list = utils.load_system_list_from_excel(
            datadir + "/system_list.xlsx")
        print(system_list)

        # 步骤2： 解析源数据，生成报告
        report_file_dict = dict()
        system_stat_list = list()
        for system in system_list.list:
            logger.info(system.name)
            output_file = base_dir + "/report/" + \
                system.name + "_中间件巡检报告_" + report_date + '.xlsx'
            report_file_dict[system.name] = output_file

            system_ips = {'服务器列表': system.ips,
                        '系统名称': system.name, '负责人': system.leader}
            system_ips_sheet = pd.DataFrame(system_ips)
            with pd.ExcelWriter(output_file, mode='w', engine='openpyxl') as writer:
                system_ips_sheet.to_excel(
                    writer, sheet_name=u"服务器列表", index=False, header=True)
                func_style.set_width_ip_list(writer)
            system_stat_list.append(write_data(output_file, system))

        # 将所有系统错误信息汇总写入到单独表中
        write_wrong_item(report_file_dict)
        logger.info(report_file_dict)

        # 计算问题占比，总结错误汇总表
        overview_output_file = base_dir + "/report/" + \
            "中间件巡检报告_结论总览_" + report_date + ".xlsx"
        write_overall(report_file_dict, overview_output_file, system_stat_list)

        time_end = time.time()
        logger.info("结束执行时间 ---> " + datetime.datetime.now().__str__())
        logger.info("报告生成总耗时---> ", (time_end - time_start))
    except Exception as e:
        logger.error(e)

elif action == "doc":
    base_dir = datadir
    if not os.path.exists(base_dir + "/report/"):
        os.mkdir(base_dir + "/report/")

    # 步骤1： 加载系统台账信息
    try:
        if not os.path.exists(os.path.join(datadir, 'system_list.xlsx')):
            logger.error("未配置 system_list.xlsx ，已将模板复制到数据目录，请填写后再次点击生成按钮")
            sys.exit(1)

        system_list = utils.load_system_list_from_excel(
            datadir + "/system_list.xlsx")

        # 步骤2： 解析源数据，生成报告
        report_file_dict = dict()
        system_stat_list = list()
        # print(type(system_list.list))
        for system in system_list.list:
            system_stat_list.append(analysis_data(system))
        # logger.info(json.dumps(system_stat_list, indent=4, ensure_ascii=False))
        # print(system_stat_list)
        gen_word.write_to_summary_word(datadir, system_stat_list)
        gen_word.write_to_app_word(datadir, system_stat_list)
    except Exception as e:
        logger.error(e)
