#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os
import socket
import json
import xml
import xml.dom.minidom
import datetime
import xml.etree.ElementTree as ET
import re
import getopt
import sys
import traceback
import platform


# def getLocalIp():
#     try:
#         local_ip = socket.gethostbyname(socket.gethostname())
#         if local_ip == "127.0.0.1":
#             raise
#     except:
#         local_ip = os.popen(
#             "echo -n $(ip address | grep -v 127.0.0.1 | awk '/inet/ {print $2}' | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}') | sed 's/\ /','/g'").readline().split(",")[0]
#     return local_ip

#如果存在多网卡上面获取IP地址就不准确了
def getLocalIp():
    try:
        # 尝试通过UDP套接字获取IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("255.255.255.0", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        pass

    try:
        # 尝试通过hostname获取IP，并排除127.0.0.1
        local_ip = socket.gethostbyname(socket.gethostname())
        if local_ip.startswith("127."):
            raise Exception("本地IP是回环地址")
        return local_ip
    except Exception:
        pass

    # 最后，使用系统命令获取IP
    try:
        # 使用ip address命令获取IP，并排除127.0.0.1
        local_ip = os.popen(
             "echo -n $(ip address | grep -v 127.0.0.1 | awk '/inet/ {print $2}' | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}') | sed 's/\ /','/g'").readline().split(",")[0]
        return local_ip
    except Exception:
        pass

    return "127.0.0.1"


def contain_docker_nodes():
    docker_check = os.popen("docker ps 2> /dev/null| wc -l").readline().strip()
    if int(docker_check) > 1:
        return True
    else:
        return False


def getPath(file):
    return os.path.dirname(os.path.abspath(file))


def getScriptPath():
    return os.path.dirname(os.path.abspath(__file__))


def writeFile(path, name, content):
    if not os.path.exists(path):
        os.mkdir(path)
    file = open(path + "/" + name, mode="w")
    file.write(content)
    file.close()


def version_to_num(version):
    nums = version.split(".")
    multiple = pow(10, (len(nums) - 1))
    total = 0
    for int_item in nums:
        total += int(int_item) * multiple
        multiple = multiple / 10

    return total


def grep_zookeeper_process(processes):
    zookeeper_list = []
    process_dict = dict()
    java_list = []
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                java_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break

    for item in java_list:
        if "org.apache.zookeeper.server.quorum.QuorumPeerMain" in item["CMD"]:
            zookeeper_list.append(item)

    return zookeeper_list


def xunjian_zookeeper(serverInfo):
    zk_process_list = grep_zookeeper_process(serverInfo["psAll"])
    zkDetailList = []
    for zk_process in zk_process_list:
        bin_dir = ""
        config_file = ""
        config_path = ""
        zk = dict()
        pid = zk_process["PID"]
        uid = zk_process["UID"]
        zk["user"] = uid
        zk["PID"] = zk_process["PID"]
        zk["CMD"] = zk_process["CMD"]
        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            zk["max_user_processes"] = os.popen(
                "su - " + uid + " -c 'ulimit -Hu'").readline().rstrip()
            zk["max_user_processes_s"] = os.popen(
                "su - " + uid + " -c 'ulimit -Su'").readline().rstrip()
            zk["max_open_files"] = os.popen(
                "su - " + uid + " -c 'ulimit -Hn'").readline().rstrip()
            zk["max_open_files_s"] = os.popen(
                "su - " + uid + " -c 'ulimit -Sn'").readline().rstrip()
            lsof = os.popen("lsof -p " + pid +
                            "|awk -F ' ' '{print $NF}'").readlines()

        for line in zk_process["CMD"].split(" "):
            zk["zk_home"] = os.popen(
                "readlink -f " + "/proc/" + pid + "/cwd").readlines()[0].rstrip()
            if line.startswith("-Dzookeeper.log.dir") and "bin" in line:
                bin_dir = line.split("=")[1].split("/..")[0].strip()
            if line.endswith(".cfg") or line.endswith(".conf"):
                config_file = bin_dir.split(
                    "/bin")[0].strip() + line.split("..")[1].strip()

        if bin_dir == '.':
            bin_dir = zk["zk_home"]

        if os.path.exists(config_file):
            zk["config_file"] = config_file
            config_path = getPath(config_file)
            zk["config_content"] = os.popen(
                "cat " + config_file + "| grep -Ev '^#|^$' ").readlines()
            client_port = 2181
            for line in zk["config_content"]:
                if "clientPort" in line:
                    client_port = line.split("=")[1].strip()
            zk["client_port"] = client_port
            if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
                zk["zk_get_acl"] = os.popen("su - " + uid + " -c '" + bin_dir + "/zkCli.sh -server 127.0.0.1:" +
                                            client_port + "  getAcl /  | grep \'WATCHER::\' -A 50 | grep -v \'Exiting JVM\''").readlines()

        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            zk["zk_status"] = os.popen(
                "su - " + uid + " -c '" + bin_dir + "/zkServer.sh --config " + config_path + " status 2>&1'").readlines()
            zk["zk_version"] = os.popen(
                "su - " + uid + " -c '" + bin_dir + "/zkServer.sh --config " + config_path + "  version 2>&1'").readlines()
            for line in zk["zk_status"]:
                if "Mode" in line:
                    zk["mode"] = line.split(":")[1].strip()

        log_files = []
        for file_item in lsof:
            file_item = file_item.strip()
            if file_item.endswith(".log") or file_item.endswith(".out"):
                log_files.append(file_item)
        error_log_content = []
        for error in log_files:
            error_log_content.append(os.popen(
                "tail -n 1000 " + error + "| grep -v 'INFO' | tail -n 20").readlines())
        zk["error_logs"] = error_log_content
        zkDetailList.append(zk)

    return zkDetailList


def grep_weblogic_processes(psEfAll):
    processList = []
    process_dict = dict()
    for process in psEfAll:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                if "weblogic.Server" in process_dict["CMD"]:
                    processList.append(process_dict)
                    process_dict = dict()
                    break
            if i > 7:
                process_dict = dict()
                break
    return processList


def grep_was_processes(psEfAll):
    processList = []
    process_dict = dict()
    for process in psEfAll:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                if "com.ibm.ws.runtime.WsServer" in process_dict["CMD"]:
                    processList.append(process_dict)
                    process_dict = dict()
                    break
            if i > 7:
                process_dict = dict()
                break
    return processList


def xunjian_weblogic(serverInfo):
    weblogic_process_list = grep_weblogic_processes(serverInfo["psAll"])
    weblogic_detail = []
    for weblogic in weblogic_process_list:
        pid = weblogic["PID"]
        weblogic["base_domain"] = os.popen(
            "pwdx " + pid + " | awk '{print $2}'").readline().strip()
        weblogic["config_xml"] = os.popen(
            "cat " + weblogic["base_domain"] + "/config/config.xml").readlines()
        jdbc_list = []
        for jdbc_xml in os.listdir(weblogic["base_domain"] + "/config/jdbc/"):
            if ".xml" in jdbc_xml:
                cat_cmd = "cat " + \
                    weblogic["base_domain"] + "/config/jdbc/" + jdbc_xml
                jdbc_content = os.popen(cat_cmd).readlines()

                for line in jdbc_content:
                    if "test-connections-on-reserve" in line:
                        weblogic["test_connections_on_reserve"] = line
                    if "inactive-connection-timeout-seconds" in line:
                        weblogic["inactive_connection_timeout_seconds"] = line
                    if "test-frequency-seconds" in line:
                        weblogic["test_frequency_seconds"] = line

                jdbc_dict = dict()
                jdbc_dict[jdbc_xml] = jdbc_content
                jdbc_list.append(jdbc_dict)
        weblogic["jdbc_xml"] = jdbc_list
        weblogic["server_name"] = os.popen(
            "ps -fp " + pid + " | awk -F 'weblogic.Name=' '{print $2}' | awk '{print $1}' | tail -n 1").readline().strip()
        weblogic_log = os.popen(
            "tail -n 2000 " + weblogic["base_domain"] + "/servers/" + weblogic["server_name"] + "/logs/" + weblogic[
                "server_name"] + ".log | grep -v '\<Info\>' | grep " + weblogic[
                "server_name"] + " | tail -n 20 ").readlines()
        weblogic_log2 = os.popen(
            "tail -n 2000 " + weblogic["base_domain"] + "/servers/" + weblogic["server_name"] + "/logs/" + weblogic[
                "server_name"] + ".log | grep ' <BEA-000628> <Created' | grep " + weblogic[
                "server_name"] + " | tail -n 20 ").readlines()
        weblogic["log"] = weblogic_log + weblogic_log2
        weblogic["log_file"] = weblogic["base_domain"] + "/servers/" + weblogic["server_name"] + "/logs/" + weblogic[
            "server_name"] + ".log"

        if "wls_home" in weblogic:
            wls_env_path = \
                os.popen("find " + weblogic["wls_home"] + " -maxdepth 3 -name setWLSEnv.sh | head -1").readlines()[
                    0].rstrip()
            weblogic["wls_version"] = \
                os.popen("source " + wls_env_path + " 2&> /dev/null ; echo `java weblogic.version`;").readlines()[
                    0].rstrip()
        weblogic_detail.append(weblogic)
    return weblogic_detail


def xunjian_was(serverInfo):
    was_process_list = grep_was_processes(serverInfo["psAll"])
    was_detail = []
    for was in was_process_list:
        pid = was["PID"]
        was["profile_path"] = os.popen(
            "pwdx " + pid + " | awk '{print $2}'").readline().strip()

        config_xml_path = ""
        cell_path = ""
        node_path = ""

        if os.path.exists(was["profile_path"] + "/config/cells/defaultCell/nodes/defaultNode/serverindex.xml"):
            config_xml_path = was["profile_path"] + \
                "/config/cells/defaultCell/nodes/defaultNode/serverindex.xml"
        elif os.path.exists(was["profile_path"] + "/config/cells/") and os.path.isdir(was["profile_path"] + "/config/cells/"):
            files = os.listdir(was["profile_path"]+"/config/cells/")
            for file in files:
                os.path.isdir(file) and file.find("Cell")
                cell_path = was["profile_path"]+"/config/cells/"+file
                break
            if os.path.exists(cell_path + "/nodes/"):
                file2s = os.listdir(cell_path + "/nodes/")
                for file2 in file2s:
                    os.path.isdir(file2) and file2.find("Node")
                    node_path = cell_path+"/nodes/"+file2
                    break

        if len(node_path) > 0:
            if os.path.exists(node_path + "/serverindex.xml"):
                config_xml_path = node_path + "/serverindex.xml"
        # was["config_xml"]
        if len(config_xml_path) > 0:
            was["config_xml"] = os.popen(
                "cat " + config_xml_path).readlines()
        else:
            was["config_xml"] = "配置文件未找到，请手动设置"

        # was["jdbc_xml"]
        if len(node_path) > 0:
            jdbc_list = []
            for jdbc_xml in os.listdir(node_path):
                if ".xml" in jdbc_xml:
                    cat_cmd = "cat " + node_path+"/" + jdbc_xml
                    jdbc_content = os.popen(cat_cmd).readlines()
                    for line in jdbc_content:
                        if "test-connections-on-reserve" in line:
                            was["test_connections_on_reserve"] = line
                        if "inactive-connection-timeout-seconds" in line:
                            was["inactive_connection_timeout_seconds"] = line
                        if "test-frequency-seconds" in line:
                            was["test_frequency_seconds"] = line

                    jdbc_dict = dict()
                    jdbc_dict[jdbc_xml] = jdbc_content
                    jdbc_list.append(jdbc_dict)
            was["jdbc_xml"] = jdbc_list
        else:
            was["jdbc_xml"] = "xml文件路径未找到，请手动设置"
        was["server_name"] = os.popen(
            "ps -fp " + pid + " | awk -F 'server.name=' '{print $2}' | awk '{print $1}' | tail -n 1").readline().strip()

        # was系统日志文件
        was_log_file = ""
        if os.path.exists(was["profile_path"] + "/logs/server1/SystemOut.log"):
            was_log_file = was["profile_path"] + "/logs/server1/SystemOut.log"
            was["log_file"] = was_log_file
            # log_content = os.popen(
            #     "cat " + was_log_file).readlines()
            with open(was_log_file, 'r') as f:
                log_content = f.read()
            errLog = []
            createLog = []
            for line in log_content.splitlines():
                if line.find("<BEA-000628> <Created") != -1:
                    createLog.append(line)
                    continue
                strs = line.split("]")
                if len(strs) > 1:
                    status = re.split("\s+", strs[1].strip())
                    if len(status) > 2:
                        logLevel = status[2]
                        if logLevel == "W" or logLevel == "Warn":
                            errLog.append(line)
            was["log"] = errLog[-20:]+createLog[-20:]
        else:
            was["log_file"] = "未找到was系统日志文件"
            was["log"] = ""
        if "was_home" in was:
            was_env_path = \
                os.popen("find " + was["was_home"] + " -maxdepth 3 -name setupCmdLine.sh | head -1").readlines()[
                    0].rstrip()
            was["was_version"] = \
                os.popen("source " + was_env_path + " 2&> /dev/null ; echo `$WAS_HOME/bin/versionInfo.sh | grep 'Full Version String' | awk -F ':' '{print $2}'`;").readlines()[
                    0].rstrip()
        was_detail.append(was)
    return was_detail


def grep_tomcat_processes(processes):
    java_list = []
    tomcat_list = []
    process_dict = dict()
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split) - 1])
                java_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break

    for item in java_list:
        if "org.apache.catalina.startup.Bootstrap" in item["CMD"]:
            tomcat_list.append(item)

    return tomcat_list


def xunjian_tomcat(serverInfo):
    tomcat_process_list = grep_tomcat_processes(serverInfo["psAll"])
    tomcat_detail_list = []
    for tomcat in tomcat_process_list:

        tomcat_home = ""
        uid = tomcat["UID"]
        lsof = os.popen(
            "lsof -p " + tomcat['PID'] + "|awk -F ' ' '{print $NF}'").readlines()
        tomcat["lsof_count"] = len(lsof)

        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            tomcat["max_user_processes"] = os.popen(
                "su - " + uid + " -c 'ulimit -Hu'").readline().rstrip()
            tomcat["max_user_processes_s"] = os.popen(
                "su - " + uid + " -c 'ulimit -Su'").readline().rstrip()
            tomcat["max_open_files"] = os.popen(
                "su - " + uid + " -c 'ulimit -Hn'").readline().rstrip()
            tomcat["max_open_files_s"] = os.popen(
                "su - " + uid + " -c 'ulimit -Sn'").readline().rstrip()

        for cmd in tomcat["CMD"].split(" "):
            if "-Dcatalina.home" in cmd:
                tomcat_home = cmd.split("=")[1].strip()

        if os.path.exists(tomcat_home):
            tomcat["tomcat_home"] = tomcat_home
            if os.path.exists(tomcat_home + "/bin/version.sh"):
                tomcat["tomcat_version"] = os.popen(
                    tomcat_home + "/bin/version.sh").readlines()

        appbase_real = ""
        if os.path.exists(tomcat_home + "/conf/server.xml"):
            server_xml_path = tomcat_home + "/conf/server.xml"
            dom_tree = xml.dom.minidom.parse(server_xml_path)
            collection = dom_tree.documentElement
            host_node = collection.getElementsByTagName("Host")
            for node in host_node:
                if node.hasAttribute("appBase"):
                    appbase = node.getAttribute("appBase")
                    if os.path.exists(appbase) and os.path.isdir(appbase):
                        appbase_real = appbase
                    else:
                        if os.path.isdir(tomcat_home + '/' + appbase):
                            appbase_real = tomcat_home + '/' + appbase
                else:
                    temp_appbase = tomcat_home + '/webapps'
                    if os.path.exists(temp_appbase):
                        appbase_real = tomcat_home + '/webapps'

        tomcat['app_base'] = appbase_real
        tomcat['app_name'] = ",".join(os.listdir(appbase_real))

        if os.path.exists(tomcat_home + "/conf/server.xml"):
            server_xml_path = tomcat_home + "/conf/server.xml"
            dom_tree = xml.dom.minidom.parse(server_xml_path)
            collection = dom_tree.documentElement

            valve_nodes = collection.getElementsByTagName("Valve")
            for node in valve_nodes:
                if node.hasAttribute("className") and node.getAttribute(
                        "className") == "org.apache.catalina.valves.ErrorReportValve":
                    tomcat['show_report'] = node.getAttribute("showReport")
                    tomcat['show_server_info'] = node.getAttribute(
                        "showServerInfo")

            tomcat['shutdown_port'] = collection.getAttribute("port")
            tomcat['shutdown_cmd'] = collection.getAttribute("shutdown")

            connector_nodes = collection.getElementsByTagName("Connector")
            connector_http_list = []
            connector_ajp_list = []
            for node in connector_nodes:
                connector_dict = dict()
                if "HTTP" in node.getAttribute("protocol"):
                    connector_dict["executor"] = node.getAttribute("executor")
                    connector_dict["port"] = node.getAttribute("port")
                    connector_dict["protocol"] = node.getAttribute("protocol")
                    connector_dict["connectionTimeout"] = node.getAttribute(
                        "connectionTimeout")
                    connector_dict["keepAliveTimeout"] = node.getAttribute(
                        "keepAliveTimeout")
                    connector_dict["maxKeepAliveRequests"] = node.getAttribute(
                        "maxKeepAliveRequests")
                    connector_dict["redirectPort"] = node.getAttribute(
                        "redirectPort")
                    connector_dict["maxHttpHeaderSize"] = node.getAttribute(
                        "maxHttpHeaderSize")
                    connector_dict["URIEncoding"] = node.getAttribute(
                        "URIEncoding")
                    connector_dict["enableLookups"] = node.getAttribute(
                        "enableLookups")
                    connector_dict["acceptCount"] = node.getAttribute(
                        "acceptCount")
                    connector_dict["disableUploadTimeout"] = node.getAttribute(
                        "disableUploadTimeout")
                    connector_dict["compression"] = node.getAttribute(
                        "compression")
                    connector_dict["compressionMinSize"] = node.getAttribute(
                        "compressionMinSize")
                    connector_dict["noCompressionUserAgents"] = node.getAttribute(
                        "noCompressionUserAgents")
                    connector_dict["compressableMimeType"] = node.getAttribute(
                        "compressableMimeType")
                    connector_dict["server"] = node.getAttribute("server")
                    connector_http_list.append(connector_dict)
                if "AJP" in node.getAttribute("protocol"):
                    connector_dict["protocol"] = node.getAttribute("protocol")
                    connector_dict["address"] = node.getAttribute("address")
                    connector_dict["port"] = node.getAttribute("port")
                    connector_dict["redirectPort"] = node.getAttribute(
                        "redirectPort")
                    connector_ajp_list.append(connector_dict)
            tomcat["connector_http"] = connector_http_list
            tomcat["connector_ajp"] = connector_ajp_list

        all_dbresource_list = []
        dbresource_dict = dict()
        if os.path.exists(tomcat_home + "/conf/context.xml"):
            context_xml_path = tomcat_home + "/conf/context.xml"
            dom_tree = xml.dom.minidom.parse(context_xml_path)
            collection = dom_tree.documentElement
            connector_node = collection.getElementsByTagName("Resource")
            for node in connector_node:
                dbresource_dict["name"] = node.getAttribute("name")
                dbresource_dict["auth"] = node.getAttribute("auth")
                dbresource_dict["type"] = node.getAttribute("type")
                dbresource_dict["driverClassName"] = node.getAttribute(
                    "driverClassName")
                dbresource_dict["url"] = node.getAttribute("url")
                dbresource_dict["username"] = node.getAttribute("username")
                dbresource_dict["password"] = node.getAttribute("password")
                dbresource_dict["maxActive"] = node.getAttribute("maxActive")
                dbresource_dict["maxIdle"] = node.getAttribute("maxIdle")
                dbresource_dict["maxWait"] = node.getAttribute("maxWait")
                dbresource_dict["initialSize"] = node.getAttribute(
                    "initialSize")
                dbresource_dict["maxTotal"] = node.getAttribute("maxTotal")
                dbresource_dict["minIdle"] = node.getAttribute("minIdle")
                dbresource_dict["maxWaitMillis"] = node.getAttribute(
                    "maxWaitMillis")
                for key in dbresource_dict.keys():
                    if dbresource_dict[key] == "":
                        dbresource_dict[key] = None
                all_dbresource_list.append(dbresource_dict)
                dbresource_dict = dict()
        tomcat['all_dbresource'] = all_dbresource_list

        log_files = []
        for file_item in lsof:
            file_item = file_item.strip()
            if file_item.endswith(".log") or "out" in file_item:
                log_files.append(file_item)

        log_files = set(log_files)
        error_log_content = []
        for error in log_files:
            error_log_content.append(
                os.popen("tail -n 1000 " + error + "| grep -v 'INFO' | tail -n 20").readlines())
        tomcat["error_logs"] = error_log_content

        tomcat_detail_list.append(tomcat)

    return tomcat_detail_list


def grep_rocketmq_process(processes):
    rocketmq_list = []
    process_dict = dict()
    java_list = []
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                java_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break

    for item in java_list:
        if "org.apache.rocketmq.broker.BrokerStartup" in item["CMD"]:
            rocketmq_list.append(item)

    return rocketmq_list


def xunjian_rocketmq(serverInfo):
    rocketmq_process_list = grep_rocketmq_process(serverInfo["psAll"])
    rocketmqDetailList = []
    for rocketmq_process in rocketmq_process_list:
        rocketmq_home = ""
        rocketmq = dict()
        pid = rocketmq_process["PID"]
        uid = rocketmq_process["UID"]
        rocketmq["user"] = uid
        rocketmq["PID"] = rocketmq_process["PID"]
        rocketmq["CMD"] = rocketmq_process["CMD"]
        for cmd in rocketmq_process["CMD"].split(" "):
            if cmd.endswith("org.apache.rocketmq.broker.BrokerStartup"):
                rocketmq_home = os.popen(
                    "readlink -f " + "/proc/" + pid + "/cwd").readline().rstrip()
        rocketmq["rocketmq_home"] = rocketmq_home
        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            rocketmq["max_user_processes"] = os.popen(
                "su - " + uid + " -c 'ulimit -Hu'").readline().rstrip()
            rocketmq["max_user_processes_s"] = os.popen(
                "su - " + uid + " -c 'ulimit -Su'").readline().rstrip()
            rocketmq["max_open_files"] = os.popen(
                "su - " + uid + " -c 'ulimit -Hn'").readline().rstrip()
            rocketmq["max_open_files_s"] = os.popen(
                "su - " + uid + " -c 'ulimit -Sn'").readline().rstrip()
        lsof = os.popen("lsof -p " + pid +
                        "|awk -F ' ' '{print $NF}'").readlines()
        name_server_url = rocketmq_process["CMD"].split(" ")[-1].rstrip()
        rocketmq["name_server_url"] = name_server_url
        mqadmin = rocketmq_home + "/bin/mqadmin"
        rocketmq["config_file"] = os.popen("find " + rocketmq_home + " -name broker.conf | head -1").readlines()[
            0].rstrip()

        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            rocketmq["topic_status"] = os.popen(
                "su - " + uid + " -c  '" + mqadmin + " statsAll -n " + name_server_url + "' 2> /dev/null").readlines()
            rocketmq["cluster_list"] = os.popen(
                "su - " + uid + " -c  '" + mqadmin + " clusterList -n " + name_server_url + "' 2> /dev/null").readlines()
            rocketmq["name_server_config"] = os.popen(
                "su - " + uid + " -c  '" + mqadmin + " getNamesrvConfig -n " + name_server_url + "' 2> /dev/null").readlines()

        if os.path.exists(rocketmq["config_file"]):
            rocketmq["config_content"] = os.popen(
                "cat " + rocketmq["config_file"] + "| grep -Ev '^#|^$' ").readlines()

        log_files = []
        for file_item in lsof:
            file_item = file_item.strip()
            if file_item.endswith(".log") and "rocketmq" in file_item:
                log_files.append(file_item)
        error_log_content = []
        for error in log_files:
            error_log_content.append(os.popen(
                "tail -n 1000 " + error + "| grep -v 'INFO' | tail -n 20").readlines())
        rocketmq["error_logs"] = error_log_content

        rocketmqDetailList.append(rocketmq)
    return rocketmqDetailList


def grep_redis_process(psEfAll):
    redis_list = []
    process_dict = dict()
    for process in psEfAll:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7:
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                if "redis-server" in process_dict["CMD"] and "sentinel" not in process_dict["CMD"]:
                    redis_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break
    return redis_list


def xunjian_redis(serverInfo):
    redisProcessList = grep_redis_process(serverInfo["psAll"])
    redisDetailList = []
    for redis in redisProcessList:
        pid = redis["PID"]
        host_ip = getLocalIp()
        redis["cpu_usage"] = os.popen(
            " ps -p " + pid + " -o pcpu").readlines()[1].strip()
        redis["memory_usage"] = os.popen(
            " ps -p " + pid + " -o pmem").readlines()[1].strip()
        redis["port"] = redis["CMD"].split(" ")[1].split(':')[1].rstrip()
        redis["user"] = redis["UID"].rstrip()
        redis["lsof_count"] = os.popen(
            "lsof -p " + pid + " | wc -l").readlines()[0].strip()
        redis["netstat_count"] = os.popen(
            "netstat -anop 2> /dev/null| grep " + pid + " | wc -l").readlines()[0].strip()
        redis["exe_path"] = os.popen(
            "readlink -f " + "/proc/" + pid + "/exe").readlines()[0].strip()
        redis["redis_home"] = os.path.dirname(
            os.path.abspath(os.popen("readlink -f " + "/proc/" + pid + "/cwd").readline().rstrip()))
        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            redis["max_open_files"] = os.popen(
                "su - " + redis["user"] + " -c 'ulimit -Hn'").readline().rstrip()
            redis["max_open_files_s"] = os.popen(
                "su - " + redis["user"] + " -c 'ulimit -Sn'").readline().rstrip()
        redis_conf_path = os.popen(
            "find " + redis['redis_home'] + " -maxdepth 3 -type f -name redis_" + redis[
                "port"] + ".conf| head -1").readlines()
        if len(redis_conf_path):
            redis["conf_path"] = redis_conf_path[0].rstrip()
        else:
            redis_conf_path = os.popen(
                "find " + redis['redis_home'] + " -maxdepth 3 -type f -name redis*.conf | head -1").readlines()
            if len(redis_conf_path):
                redis["conf_path"] = redis_conf_path[0].rstrip()
            else:
                redis_conf_path = os.popen(
                    "find /etc/ -maxdepth 3 -type f -name redis*.conf | head -1").readlines()
                if len(redis_conf_path):
                    redis["conf_path"] = redis_conf_path[0].rstrip()
                else:
                    print("can't find config file!!!")
                    redis["conf_path"] = "/dev/null"

        main_conf_content = ""
        include_conf_path = ""
        execute_dir = getPath(redis["exe_path"])
        requirepass = ""
        if os.path.exists(redis["conf_path"]):
            main_conf_content = os.popen(
                "cat " + redis["conf_path"] + " | grep -Ev '^#|^$'").readlines()
        for line in main_conf_content:
            if line.startswith("include"):
                include_conf_path = line.split(" ")[1].rstrip()
        if os.path.exists(include_conf_path):
            redis["include_file_path"] = include_conf_path

        # 如果redis_password不为空的话，直接用该密码，如果为空的话，再从配置文件中获取
        if serverInfo["redis_password"]:
            requirepass = serverInfo["redis_password"]
        else:
            tmp_conf_content = os.popen(
                "cat " + redis["conf_path"] + " " + include_conf_path + " | grep -Ev '^#|^$'").readlines()

            for line in tmp_conf_content:
                if "requirepass" in line:
                    requirepass = line.split(" ")[1].strip()

        if requirepass != "":
            connect_str = execute_dir + "/redis-cli -p " + \
                redis["port"] + " -a " + requirepass + " -h " + host_ip
        else:
            connect_str = execute_dir + "/redis-cli -p " + \
                redis["port"] + " -h " + host_ip

        redis["info"] = os.popen(
            connect_str + " info 2> /dev/null").readlines()

        # info message filter
        redis["config_file"] = redis["conf_path"]
        redis["cluster_enabled"] = 0
        for item in redis["info"]:
            if item.startswith("redis_version"):
                redis["redis_version"] = item.split(":")[1].strip()
            if item.startswith("config_file"):
                redis["config_file"] = item.split(":")[1].strip()
            if item.startswith("uptime_in_days"):
                redis["uptime_in_days"] = item.split(":")[1].strip()
            if item.startswith("connected_clients"):
                redis["connected_clients"] = item.split(":")[1].strip()
            if item.startswith("blocked_clients"):
                redis["blocked_clients"] = item.split(":")[1].strip()
            if item.startswith("total_system_memory:"):
                redis["total_system_memory"] = item.split(":")[1].strip()
            if item.startswith("maxmemory:"):
                redis["maxmemory"] = item.split(":")[1].strip()
            if item.startswith("used_memory:"):
                redis["used_memory"] = item.split(":")[1].strip()
            if item.startswith("used_memory_rss:"):
                redis["used_memory_rss"] = item.split(":")[1].strip()
            if item.startswith("used_memory_rss_human"):
                redis["used_memory_rss_human"] = item.split(":")[1].strip()
            if item.startswith("used_memory_peak"):
                redis["used_memory_peak"] = item.split(":")[1].strip()
            if item.startswith("used_memory_human"):
                redis["used_memory_human"] = item.split(":")[1].strip()
            # 增加redis内存碎片率
            if item.startswith("mem_fragmentation_ratio"):
                redis["mem_fragmentation_ratio"] = item.split(":")[1].strip()
            if item.startswith("maxmemory_human"):
                redis["maxmemory_human"] = item.split(":")[1].strip()
            if item.startswith("used_memory_peak_human"):
                redis["used_memory_peak_human"] = item.split(":")[1].strip()
            if item.startswith("total_system_memory_human"):
                redis["total_system_memory_human"] = item.split(":")[1].strip()
            if item.startswith("maxmemory_policy"):
                redis["maxmemory_policy"] = item.split(":")[1].strip()
            if item.startswith("rdb_last_bgsave_status"):
                redis["rdb_last_bgsave_status"] = item.split(":")[1].strip()
            if item.startswith("rdb_last_bgsave_time_sec"):
                redis["rdb_last_bgsave_time_sec"] = item.split(":")[1].strip()
            if item.startswith("rdb_last_cow_size"):
                redis["rdb_last_cow_size"] = item.split(":")[1].strip()
            if item.startswith("aof_enabled"):
                redis["aof_enabled"] = item.split(":")[1].strip()
            if item.startswith("aof_last_bgrewrite_status"):
                redis["aof_last_bgrewrite_status"] = item.split(":")[1].strip()
                redis["aof_last_write_status"] = item.split(":")[1].strip()
            if item.startswith("aof_last_cow_size"):
                redis["aof_last_cow_size"] = item.split(":")[1].strip()
            if item.startswith("aof_current_size"):
                redis["aof_current_size"] = item.split(":")[1].strip()
            if item.startswith("rejected_connections"):
                redis["rejected_connections"] = item.split(":")[1].strip()
            if item.startswith("evicted_keys"):
                redis["evicted_keys"] = item.split(":")[1].strip()
            if item.startswith("latest_fork_usec"):
                redis["latest_fork_usec"] = item.split(":")[1].strip()
            if item.startswith("cluster_enabled"):
                redis["cluster_enabled"] = item.split(":")[1].strip()
            if item.startswith("role"):
                redis["role"] = item.split(":")[1].strip()
            if item.startswith("master_link_status"):
                redis["master_link_status"] = item.split(":")[1].strip()
            if item.startswith("connected_slaves"):
                redis["connected_slaves"] = item.split(":")[1].strip()
            if item.startswith("master_failover_state"):
                redis["master_failover_state"] = item.split(":")[1].strip()

        redis["conf_content"] = os.popen(
            "cat " + redis["config_file"] + " " + include_conf_path + " | grep -Ev '^#|^$'").readlines()

        # cluster message filter
        if redis["cluster_enabled"] == 1:
            cluster_info = os.popen(
                connect_str + " CLUSTER INFO 2> /dev/null").readlines()
            for item in cluster_info:
                if item.startswith("cluster_state"):
                    redis["cluster_state"] = item.split(":")[1].rstrip()
                if item.startswith("cluster_slots_assigned"):
                    redis["cluster_slots_assigned"] = item.split(":")[
                        1].rstrip()
                if item.startswith("cluster_slots_ok"):
                    redis["cluster_slots_ok"] = item.split(":")[1].rstrip()

        # config message filter
        rename_str = ""
        for item in redis["conf_content"]:
            if item.startswith("rename-command"):
                rename_str += item.split(" ")[1] + ","
            if item.startswith("tcp-backlog"):
                redis["tcp_backlog"] = item.split(" ")[1].rstrip()
            if item.startswith("requirepass"):
                redis["requirepass"] = item.split(" ")[1].rstrip()
                redis["masterauth"] = item.split(" ")[1].rstrip()
            if item.startswith("logfile"):
                log_file = item.split(" ")[1].replace("\"", "").rstrip()
                if os.path.exists(log_file):
                    redis["log_file"] = log_file
                    redis["error_logs"] = os.popen(
                        "tail -n 1000 " + redis["log_file"] + " | grep -iE 'Error|WARNING'").readlines()
        redis["rename_command"] = rename_str.rstrip(",")

        # linux kernel parameters filter
        redis["thp"] = serverInfo["thp"]
        redis["overcommit_memory"] = serverInfo["overcommit_memory"]
        redis["net_ipv4_tcp_max_syn_backlog"] = serverInfo["net_ipv4_tcp_max_syn_backlog"]
        redis["net_core_somaxconn"] = serverInfo["net_core_somaxconn"]
        redis["vm_swappiness"] = serverInfo["vm_swappiness"]

        redisDetailList.append(redis)

    return redisDetailList


def grep_rabbitmq_process(processes):
    rabbitmq_list = []
    process_dict = dict()
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("beam.smp")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                rabbitmq_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break

    return rabbitmq_list


def xunjian_rabbitmq(serverInfo):
    rabbitmqProcessList = grep_rabbitmq_process(serverInfo["psAll"])
    rabbitmqDetailList = []
    for rabbitmq in rabbitmqProcessList:
        pid = rabbitmq["PID"]
        rabbitmq["erlang_exe"] = \
            os.popen("readlink -f " + "/proc/" +
                     rabbitmq["PID"] + "/exe").readline().rstrip().split("/beam.smp")[0]
        rabbitmq_home = os.popen(
            "readlink -f " + "/proc/" + rabbitmq["PID"] + "/cwd").readline().rstrip()

        if os.path.exists(rabbitmq_home + "/rabbitmqctl"):
            rabbitmq["rabbitmq_home"] = rabbitmq_home
        else:
            rabbitmqctl_path = os.popen(
                "find /data/" + " -maxdepth 3 -type f -name rabbitmqctl | head -1").readline().rstrip()
            rabbitmq_home = rabbitmqctl_path.split("/rabbitmqctl")[0]
            rabbitmq["rabbitmq_home"] = rabbitmq_home

        rabbitmq["netstat_count"] = os.popen(
            "netstat -anop | grep " + pid + " | wc -l").readlines()[0]
        rabbitmq["cpu_usage"] = os.popen(
            " ps -p " + pid + " -o pcpu").readlines()[1].strip()
        rabbitmq["mem_usage"] = os.popen(
            " ps -p " + pid + " -o pmem").readlines()[1].strip()
        rabbitmq["user"] = rabbitmq["UID"].rstrip()
        rabbitmq["ulimit"] = os.popen(
            "cat /proc/" + pid + "/limits").readlines()

        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            rabbitmq["max_user_processes"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c 'ulimit -Hu'").readline().rstrip()
            rabbitmq["max_user_processes_s"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c 'ulimit -Su'").readline().rstrip()
            rabbitmq["max_open_files"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c 'ulimit -Hn'").readline().rstrip()
            rabbitmq["max_open_files_s"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c 'ulimit -Sn'").readline().rstrip()
        rabbitmq["port_status"] = os.popen(
            "netstat -luntp | grep " + pid).readlines()
        lsof = os.popen("lsof -p " + pid +
                        "|awk -F ' ' '{print $NF}'").readlines()
        rabbitmq["lsof_count"] = len(lsof)

        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            rabbitmq["rabbitmq_status"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl status'").readlines()
            rabbitmq["list_users"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl list_users'").readlines()
            rabbitmq["list_permissions"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl list_permissions'").readlines()
            rabbitmq["list_vhosts"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl list_vhosts'").readlines()
            rabbitmq["list_channels"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl list_channels'").readlines()
            rabbitmq["list_consumers"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl list_consumers'").readlines()
            rabbitmq["list_exchanges"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl list_exchanges'").readlines()
            rabbitmq["list_queues"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl list_queues'").readlines()
            rabbitmq["list_unresponsive_queues"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl list_unresponsive_queues'").readlines()
            rabbitmq["node_health_check"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl node_health_check'").readlines()
            rabbitmq["cluster_status"] = os.popen(
                "su - " + rabbitmq["UID"] + " -c '" + rabbitmq_home + "/rabbitmqctl cluster_status'").readlines()
        rabbitmq["erlang_version"] = os.popen(rabbitmq["erlang_exe"] + "/erl -eval '{ok, Version} = file:read_file("
                                                                       "filename:join([code:root_dir(), \"releases\", "
                                                                       "erlang:system_info(otp_release), "
                                                                       "\"OTP_VERSION\"])), io:fwrite(Version), "
                                                                       "halt().' -noshell ").readline().rstrip()

        log_files = []
        for file_item in lsof:
            file_item = file_item.strip()
            if file_item.endswith(".log") and "rabbitmq" in file_item:
                log_files.append(file_item)
        error_log_content = []
        for error in log_files:
            error_log_content.append(
                os.popen("tail -n 1000 " + error + "| grep -v '\[info\]' | tail -n 20").readlines())
        rabbitmq["error_logs"] = error_log_content

        rabbitmqDetailList.append(rabbitmq)
    return rabbitmqDetailList


def grep_nginx_process(processes):
    nginx_list = []
    process_dict = dict()
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7:
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                nginx_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break
    nginx_master_list = []
    for nginx in nginx_list:
        if nginx["CMD"].startswith("nginx: master process"):
            nginx_master_list.append(nginx)
    return nginx_master_list


def xunjian_nginx(serverInfo):
    nginxProcessList = grep_nginx_process(serverInfo["psAll"])
    nginxDetailList = []

    for nginx in nginxProcessList:
        pid = nginx["PID"]
        nginx["nginx_exe"] = os.popen(
            "readlink -f " + "/proc/" + nginx["PID"] + "/exe").readline().rstrip()
        nginx["nginx_home"] = os.popen(
            "readlink -f " + "/proc/" + nginx["PID"] + "/cwd").readline().rstrip()
        nginx["nginx_version"] = os.popen(
            nginx["nginx_exe"] + " -v 2>&1").readline().rstrip().split("/", 1)[1]
        nginx["nginx_module"] = os.popen(
            nginx["nginx_exe"] + " -V 2>&1").readlines()
        nginx["netstat_count"] = os.popen(
            "netstat -anop | grep " + pid + " | wc -l").readlines()[0]
        nginx["cpu_usage"] = os.popen(
            " ps -p " + pid + " -o pcpu").readlines()[1].strip()
        nginx["mem_usage"] = os.popen(
            " ps -p " + pid + " -o pmem").readlines()[1].strip()
        nginx["cpu_count"] = os.popen(
            "cat /proc/cpuinfo| grep 'processor'| wc -l").readline().strip()
        nginx["umask"] = os.popen(
            "cat /proc/" + pid + "/status | grep -i umask").readlines()
        nginx["ulimit"] = os.popen("cat /proc/" + pid + "/limits").readlines()
        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            nginx["max_open_files"] = os.popen(
                "su - " + nginx["UID"] + " -c 'ulimit -Hn'").readline().rstrip()
            nginx["max_open_files_s"] = os.popen(
                "su - " + nginx["UID"] + " -c 'ulimit -Sn'").readline().rstrip()
        nginx["port"] = os.popen("netstat -luntp | grep " + pid).readlines()
        lsof = os.popen("lsof -p " + pid +
                        "|awk -F ' ' '{print $NF}'").readlines()
        nginx["lsof_count"] = len(lsof)
        nginx["worker_count"] = \
            os.popen("ps -ef | grep nginx | grep worker | awk '{print $3}'  | grep " + pid + " | wc -l").readlines()[
                0].strip()

        nginx_conf_path = None
        temp_nginx_conf_path = None
        if '-c' in nginx["CMD"]:
            it = iter(nginx["CMD"].split(' '))
            while True:
                try:
                    if next(it) == '-c':
                        temp_nginx_conf_path = next(it)
                        break
                except StopIteration:
                    break
        if temp_nginx_conf_path is not None and os.path.exists(temp_nginx_conf_path):
            nginx_conf_path = temp_nginx_conf_path
        else:
            nginx_conf_path = os.popen(
                "find " + nginx[
                    'nginx_home'] + "/../ -maxdepth 3 -type f -name nginx*.conf | head -1").readline().rstrip()

        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            if nginx_conf_path is None or ~os.path.exists(nginx_conf_path):
                exe_path = nginx["nginx_exe"]
                for line in os.popen("su - " + nginx["PID"] + " -c '" + exe_path + " -t' 2>&1").readlines():
                    if "syntax" in line:
                        it = iter(line.split(' '))
                        while True:
                            try:
                                nginx_conf_path = next(it)
                                if os.path.exists(nginx_conf_path):
                                    break
                            except StopIteration:
                                break

        if nginx_conf_path is not None and os.path.exists(nginx_conf_path):
            include_file_list = []
            nginx["nginx_conf"] = nginx_conf_path
            config_dir = os.path.dirname(os.path.abspath(nginx_conf_path))
            main_config_content = os.popen(
                "cat " + nginx_conf_path + "|grep -Ev '^#|^$'| sed 's/^M//'").readlines()
            # config filter
            for line in main_config_content:
                if "worker_processes" in line:  # == auto or == cpu_count
                    nginx["worker_processes"] = line.split()[1].rstrip(';')
                if "server_tokens" in line:  # default:on ; need:off
                    nginx["server_tokens"] = line.split()[1].rstrip(';')
                if "worker_connections" in line:  # need >= 2048
                    nginx["worker_connections"] = line.split()[1].rstrip(';')
                if "include" in line:
                    include_file_list.append(line.split()[1].rstrip(';'))

            all_config_file_list = []
            all_config_file_list.append(nginx_conf_path)
            for include_file in include_file_list:
                files = os.popen("ls " + include_file +
                                 " 2> /dev/null").readlines()
                if len(files) > 0:
                    for item in files:
                        all_config_file_list.append(item.rstrip())
                else:
                    files = os.popen("ls " + config_dir + "/" +
                                     include_file + " 2> /dev/null").readlines()
                    if len(files) > 0:
                        for item in files:
                            all_config_file_list.append(item.rstrip())

            nginx["config_content"] = os.popen(
                "cat " + " ".join(all_config_file_list) + "|grep -Ev '^#|^$'| sed 's/^M//'").readlines()

        access_log_files = set()
        error_log_files = set()

        for file_item in lsof:
            file_item = file_item.strip()
            if file_item.endswith(".log") and "access" in file_item:
                access_log_files.add(file_item)
            if file_item.endswith(".log") and "error" in file_item:
                error_log_files.add(file_item)
        access_logs = []
        error_logs = []

        for access in access_log_files:
            access_logs.append(os.popen("tail -n 50 " + access).readlines())
        for error in error_log_files:
            error_logs.append(os.popen("tail -n 2 " + error +
                              "| grep -v '\[info\]' | tail -n 20").readlines())

        nginx["access_log"] = access_logs
        nginx["error_logs"] = error_logs

        nginxDetailList.append(nginx)
    return nginxDetailList


def check_linux():
    linuxDetailList = []
    serverInfo = {}
    serverInfo["whoami"] = os.popen("whoami").readlines()[0].strip()
    serverInfo["hostname"] = os.popen("hostname").readlines()[0].strip()
    serverInfo["ip"] = getLocalIp()
    serverInfo["hosts"] = os.popen("cat /etc/hosts").readlines()
    serverInfo["showIp"] = os.popen(
        "ip add show | grep inet | grep -v inet6 | grep -v 127.0.0.1").readlines()
    serverInfo["cpu"] = os.popen(
        "cat /proc/cpuinfo | grep processor | wc -l").readlines()[0].strip()
    serverInfo["MemTotal"] = \
        os.popen("cat /proc/meminfo | grep MemTotal | awk -F':' '{print $NF}' | awk '{print $1}'").readlines()[
            0].strip()
    serverInfo["MemFree"] = \
        os.popen("cat /proc/meminfo | grep MemFree\: | awk -F':' '{print $NF}' | awk '{print $1}'").readlines()[
            0].strip()
    serverInfo["Buffers"] = \
        os.popen("cat /proc/meminfo | grep Buffers\: | awk -F':' '{print $NF}' | awk '{print $1}'").readlines()[
            0].strip()
    serverInfo["Cached"] = \
        os.popen("cat /proc/meminfo | grep Cached\: | awk -F':' '{print $NF}' | awk '{print $1}'").readlines()[
            0].strip()
    serverInfo["disk"] = os.popen("df -hP").readlines()
    serverInfo["machine"] = os.popen(
        "[ $(whoami) == 'root' ] && { dmidecode --t 1 2; } || { echo 'Permission denied'; }").readlines()
    serverInfo["uptime"] = os.popen("uptime").readlines()[0].strip()

    try:
        dist_name, dist_version, dist_id = platform.linux_distribution()
        serverInfo["osVersion"] = "{} {}".format(dist_name, dist_version)
    except:
        serverInfo["osVersion"] = os.popen(
            "cat /etc/redhat-release").readlines()[0].strip()
    serverInfo["psAll"] = os.popen(
        "ps -o ruser=userForLongName -e -o pid,ppid,c,stime,tty,time,cmd").readlines()
    serverInfo["ulimit"] = os.popen(
        "cat /etc/security/limits.conf | grep -v ^#").readlines()
    serverInfo["top"] = os.popen("top -b -n 1").readlines()
    serverInfo["sysctl.conf"] = os.popen(
        "cat /etc/sysctl.conf  | grep -Ev '^#|^$'").readlines()
    serverInfo["thp"] = os.popen(
        "cat /sys/kernel/mm/transparent_hugepage/enabled").readlines()[0].strip()
    serverInfo["overcommit_memory"] = os.popen(
        "sysctl -n vm.overcommit_memory").readlines()[0].strip()
    serverInfo["net_ipv4_tcp_max_syn_backlog"] = os.popen("sysctl -n net.ipv4.tcp_max_syn_backlog").readlines()[
        0].strip()
    serverInfo["net_core_somaxconn"] = os.popen(
        "sysctl -n net.core.somaxconn").readlines()[0].strip()
    serverInfo["vm_swappiness"] = os.popen(
        "sysctl -n vm.swappiness").readlines()[0].strip()
    linuxDetailList.append(serverInfo)

    return linuxDetailList


def grep_kafka_process(processes):
    kafka_list = []
    process_dict = dict()
    java_list = []
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                java_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break

    for item in java_list:
        if "-Dkafka" in item["CMD"]:
            kafka_list.append(item)

    return kafka_list


def xunjian_kafka(serverInfo):
    kafka_process_list = grep_kafka_process(serverInfo["psAll"])
    kafkaDetailList = []
    for kafka_process in kafka_process_list:
        kafka_home = ""
        config_path = ""
        local_ip = getLocalIp()
        kafka_port = 9092

        kafka = dict()
        pid = kafka_process["PID"]
        uid = kafka_process["UID"]
        kafka["user"] = uid
        kafka["PID"] = kafka_process["PID"]
        kafka["CMD"] = kafka_process["CMD"]
        kafka["max_user_processes"] = os.popen(
            "su - " + uid + " -c 'ulimit -Hu'").readline().rstrip()
        kafka["max_user_processes_s"] = os.popen(
            "su - " + uid + " -c 'ulimit -Su'").readline().rstrip()
        kafka["max_open_files"] = os.popen(
            "su - " + uid + " -c 'ulimit -Hn'").readline().rstrip()
        kafka["max_open_files_s"] = os.popen(
            "su - " + uid + " -c 'ulimit -Sn'").readline().rstrip()
        lsof = os.popen("lsof -p " + pid +
                        "|awk -F ' ' '{print $NF}'").readlines()

        for line in kafka_process["CMD"].split(" "):
            if "-Dkafka" in line:
                kafka_home = line.split("=")[1].split("/bin/")[0].strip()
                kafka["kafka_home"] = kafka_home
        for line in kafka_process["CMD"].split(" "):
            if "properties" in line:
                temp_path = line.strip()
                if os.path.exists(temp_path):
                    config_path = temp_path
                else:
                    if ".." in temp_path:
                        config_path = kafka_home + temp_path.split("..")[1]

        if not os.path.exists(config_path):
            config_path = kafka_home + "/config/server.properties"

        if os.path.exists(config_path):
            kafka["config_path"] = config_path
            kafka["config_content"] = os.popen(
                "cat " + kafka["config_path"] + "| grep -Ev '^#|^$' ").readlines()

        if "config_content" in kafka:
            for line in kafka["config_content"]:
                if "port" in line:
                    kafka_port = line.split("=")[1].strip()
                if "host.name" in line:
                    local_ip = line.split("=")[1].strip()
                if "listeners" in line:
                    temp_node = line.split("PLAINTEXT://")[1].strip()
                    temp_ip = temp_node.split(":")[0]
                    kafka_port = temp_node.split(":")[1]
                    if temp_ip != "":
                        local_ip = temp_ip

            kafka_nodes = local_ip + ":" + str(kafka_port)
            topic_list = os.popen(
                kafka_home + "/bin/kafka-topics.sh --bootstrap-server " + kafka_nodes + " --list").readlines()

            # just get head 3 topic
            num = 0
            topic_describe_list = []
            for topic in topic_list:
                if "consumer_offsets" in topic:
                    continue
                if num == 3:
                    break
                topic_describe = os.popen(
                    kafka_home + "/bin/kafka-topics.sh --bootstrap-server " + kafka_nodes + " --describe --topic " + topic).readlines()
                topic_describe_list.append(topic_describe)
                num = num + 1
            kafka["topic_describes"] = topic_describe_list
            kafka["consumers_stat"] = os.popen(
                kafka_home + "/bin/kafka-consumer-groups.sh --bootstrap-server " + kafka_nodes + " --describe --all-groups 2> /dev/null").readlines()

        log_files = []
        for file_item in lsof:
            file_item = file_item.strip()
            if file_item.endswith(".log") or file_item.endswith(".out"):
                log_files.append(file_item)

        error_log_content = []
        log_files = set(log_files)

        for error in log_files:
            temp_content = os.popen(
                "tail -n 1000 " + error + "| grep -iv 'INFO' | tail -n 20").readlines()
            if len(temp_content):
                error_log_content.append(temp_content)
        kafka["error_logs"] = error_log_content

        kafkaDetailList.append(kafka)

    return kafkaDetailList


def grep_java_processes(psEfAll):
    processList = []
    process_dict = dict()
    for process in psEfAll:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                processList.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break
    return processList, process_dict


def xunjian_java(serverInfo):  # dict{UID,PID,PPID,C,STIME,TTY,TIME,CMD}
    javaProcessList, _ = grep_java_processes(serverInfo["psAll"])
    javaDetailList = []
    for java in javaProcessList:
        pid = java["PID"]

        try:
            java["javaPath"] = os.popen(
                "readlink /proc/" + pid + "/exe").readlines()[0].strip()  # java path
        except Exception as e:
            print("缺少权限, 请使用 --su yes 参数或用 root 执行")
        else:
            java["javaVersion"] = os.popen(
                java["javaPath"] + " -version 2>&1").readlines()  # java version
            javaPath = java["javaPath"]
            java_home = javaPath[0: javaPath.rfind("/bin")]
            java["jstat_exe"] = javaPath[0: javaPath.rfind("/")] + "/jstat"
            java["jstat_exe2"] = java["jstat_exe"] + \
                " -gc " + pid + " 1000 1 2>&1"
            java["jstat"] = os.popen(
                java["jstat_exe"] + " -gc " + pid + " 1000 5 2>&1").readlines()
            if os.path.exists(java_home + "/jre/lib/security/java.security"):
                java["jdk_urandom"] = os.popen(
                    "cat " + java_home + "/jre/lib/security/java.security | grep -Ev '^#|^$' | grep securerandom.source").readline().rstrip()

        javaCheck = {
            "HeapDumpOnOutOfMemoryError": False,
            "HeapDumpPath": False,
            "java.awt.headless": False
        }
        if "HeapDumpOnOutOfMemoryError" in java["CMD"]:
            javaCheck["HeapDumpOnOutOfMemoryError"] = True
        if "HeapDumpPath" in java["CMD"]:
            javaCheck["HeapDumpPath"] = True
        if "java.awt.headless" in java["CMD"]:
            javaCheck["java.awt.headless"] = True

        java["javaCheck"] = javaCheck

        java["netstat_count"] = os.popen(
            "netstat -anop | grep " + pid + " | wc -l").readline().rstrip()
        java["cpu_usage"] = os.popen(
            " ps -p " + pid + " -o pcpu").readlines()[1].strip()
        java["mem_usage"] = os.popen(
            " ps -p " + pid + " -o pmem").readlines()[1].strip()
        java["umask"] = os.popen(
            "cat /proc/" + pid + "/status | grep -i umask").readlines()
        java["ulimit"] = os.popen("cat /proc/" + pid + "/limits").readlines()
        java["port_status"] = os.popen(
            "netstat -luntp | grep " + pid).readlines()
        java["lsof_count"] = os.popen(
            "lsof -p " + pid + " | wc -l").readline().rstrip()
        java["psHp"] = os.popen("top -Hbp " + pid + " -n 1").readlines()
        java["startup"] = os.popen(
            "ps -o lstart -p " + pid + " | tail -n 1").readlines()

        javaDetailList.append(java)
    return javaDetailList


def grep_elasticsearch_process(processes):
    elasticsearch_list = []
    process_dict = dict()
    java_list = []
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                java_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break

    for item in java_list:
        if "org.elasticsearch.bootstrap.Elasticsearch" in item["CMD"]:
            elasticsearch_list.append(item)

    return elasticsearch_list


def xunjian_elasticsearch(serverInfo):
    es_process_list = grep_elasticsearch_process(serverInfo["psAll"])
    local_ip = getLocalIp()
    esDetailList = []
    for es_process in es_process_list:
        config_path = ""
        es = dict()
        pid = es_process["PID"]
        uid = es_process["UID"]
        es["user"] = uid
        es["PID"] = es_process["PID"]
        es["CMD"] = es_process["CMD"]
        es["es_home"] = os.popen(
            "readlink -f " + "/proc/" + pid + "/cwd").readline().rstrip()

        temp_home = "/"
        for line in es_process["CMD"].split(" "):
            if line.startswith("-Des.path.conf"):
                config_path = line.split("=")[1].strip()
            if line.startswith("-Des.path.home"):
                temp_home = line.split("=")[1].strip()
        if config_path == "":
            config_path = temp_home

        # 增加巡检用户不是root时权限不足的问题
        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            es["max_user_processes"] = os.popen(
                "su - " + uid + " -c 'ulimit -Hu'").readline().rstrip()
            es["max_user_processes_s"] = os.popen(
                "su - " + uid + " -c 'ulimit -Su'").readline().rstrip()
            es["max_open_files"] = os.popen(
                "su - " + uid + " -c 'ulimit -Hn'").readline().rstrip()
            es["max_open_files_s"] = os.popen(
                "su - " + uid + " -c 'ulimit -Sn'").readline().rstrip()

        lsof = os.popen("lsof -p " + pid +
                        "|awk -F ' ' '{print $NF}'").readlines()

        jvm_options_file = os.popen(
            "find " + config_path + " -name jvm.options | head -1").readlines()
        if len(jvm_options_file):
            es["jvm_options_file"] = jvm_options_file[0].strip()
            if os.path.exists(es["jvm_options_file"]):
                es["jvm_options_content"] = os.popen(
                    "cat " + es["jvm_options_file"] + "| grep -Ev '^#|^$' ").readlines()

        es["config_content"] = ""
        config_file = os.popen("find " + config_path +
                               " -name elasticsearch.yml | head -1").readlines()
        if len(config_file):
            es["config_file"] = config_file[0].strip()
            if os.path.exists(es["config_file"]):
                es["config_content"] = os.popen(
                    "cat " + es["config_file"] + "| grep -Ev '^#|^$' ").readlines()
            else:
                print("error,can't find config file!")

        # 赋默认值
        es["http_port"] = 9200
        es["network_host"] = local_ip
        es["bootstrap_memory_lock"] = "false"
        es["action_destructive_requires_name"] = "true"
        for item in es["config_content"]:
            if "http.port" in item:
                es["http_port"] = item.split(': ')[1].rstrip()
            if "network.host" in item:
                es["network_host"] = item.split(': ')[1].rstrip()
            if "bootstrap.memory_lock" in item:
                es["bootstrap_memory_lock"] = item.split(': ')[1].rstrip()
            if "discovery.zen.minimum_master_nodes" in item:
                es["discovery_zen_minimum_master_nodes"] = item.split(': ')[
                    1].rstrip()
            if "action.destructive_requires_name" in item:
                es["action_destructive_requires_name"] = item.split(': ')[
                    1].rstrip()

        es_http_port = es["http_port"]
        es_bind_ip = es["network_host"]
        curl_str = "curl -s -XGET http://" + \
            es_bind_ip + ":" + str(es_http_port)
        es["es_status"] = os.popen(curl_str).readlines()

        es["es_allocation"] = os.popen(
            curl_str + "'/_cat/nodes?v&h=id,ip,port,heap.max,heap.percent,disk.total,disk.used,disk.avail,"
                       "disk.used_percent,ram.max,ram.current,ram.percent&format=json&pretty'").readlines()

        es["es_node_health"] = os.popen(
            curl_str + "'/_cat/health?v&format=json&pretty'").readlines()

        es["es_cluster_health"] = os.popen(
            curl_str + "/_cluster/health?pretty").readlines()

        es["es_shards"] = os.popen(
            curl_str + "'/_cat/shards?v&format=json&pretty'").readlines()

        es["es_tasks"] = os.popen(curl_str + "/_cat/tasks/?v").readlines()

        es["es_pending_tasks"] = os.popen(
            curl_str + "/_cluster/pending_tasks?pretty").readlines()

        es["es_thread_pool"] = os.popen(
            curl_str + "'/_cat/thread_pool?v&format=json&pretty'").readlines()

        log_files = []
        for file_item in lsof:
            file_item = file_item.strip()
            if file_item.endswith(".log"):
                log_files.append(file_item)
        error_log_content = []
        for error in log_files:
            error_log_content.append(os.popen(
                "tail -n 1000 " + error + "| grep -v 'INFO' | tail -n 20").readlines())
        es["error_logs"] = error_log_content
        esDetailList.append(es)

    return esDetailList


def get_build_version(text):
    # 使用正则表达式提取数字
    pattern = r"\d+"
    matches = re.findall(pattern, text)
    # 拼接数字为指定格式
    version = ".".join(matches)
    return version


def get_patch_version(text):
    # 使用正则表达式提取数字
    pattern = r"\d+\.\d+\.\d+\.\d+.\d+"
    match = re.search(pattern, text)
    if match:
        version = match.group()
        return version
    else:
        return None


def get_node_attrs(server_xml_path, node_name):
    nodes = []
    node_attrs = dict()
    with open(server_xml_path, 'r') as file:
        # 读取文件内容
        xml_content = file.read()
    # 解析XML内容
    root = ET.fromstring(xml_content)
    # 获取所有http-listener元素
    http_listeners = root.findall(node_name)
    # 循环输出每个http-listener的属性值
    for http_listener in http_listeners:
        attributes = http_listener.attrib
        for attr_name, attr_value in attributes.items():
            node_attrs[attr_name] = attr_value
        nodes.append(node_attrs)
        node_attrs = dict()
    return nodes


def grep_bes_processes(processes):
    java_list = []
    bes_list = []
    process_dict = dict()
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split) - 1])
                java_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break
    for item in java_list:
        if "com.bes.enterprise.startup.ASMain" in item["CMD"]:
            bes_list.append(item)
    return bes_list


def xunjian_bes(serverInfo):
    bes_process_list = grep_bes_processes(serverInfo["psAll"])
    bes_detail_list = []
    for bes in bes_process_list:
        bes_home = ""
        uid = bes["UID"]
        lsof = os.popen(
            "lsof -p " + bes['PID'] + "|awk -F ' ' '{print $NF}'").readlines()
        bes["lsof_count"] = len(lsof)
        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            bes["max_open_files"] = os.popen(
                "su - " + uid + " -c 'ulimit -Hn'").readline().rstrip()
            bes["max_open_files_s"] = os.popen(
                "su - " + uid + " -c 'ulimit -Sn'").readline().rstrip()

        for cmd in bes["CMD"].split(" "):
            if "-Dbes.home" in cmd:
                bes_home = cmd.split("=")[1].strip()

        if os.path.exists(bes_home):
            bes["bes_home"] = bes_home
            version = os.popen(
                bes_home + "/bin/iastool --passwordfile " + bes_home + "/conf/.passwordfile version").readlines()
            if version[-1] == 'Command version executed successfully.\n':
                bes["build_version"] = get_build_version(version[0])
                if "patch build" in version[1]:
                    bes["patch_version"] = get_patch_version(version[1])
                else:
                    bes["patch_version"] = None
            else:
                bes["build_version"] = None
                bes["patch_version"] = None

        if os.path.exists(bes_home + "/conf/server.config"):
            server_xml_path = bes_home + "/conf/server.config"
            bes["http-listener"] = get_node_attrs(
                server_xml_path, './/http-listener')
            bes["thread-pool"] = get_node_attrs(
                server_xml_path, ".//thread-pool")
            bes["jdbc-resource"] = get_node_attrs(
                server_xml_path, ".//jdbc-resource")
            bes["compress-log"] = get_node_attrs(
                server_xml_path, "compress-log")
            bes["log-service"] = get_node_attrs(server_xml_path, "log-service")
            bes["hotdeploy-config"] = get_node_attrs(
                server_xml_path, "hotdeploy-config")
            bes["hotswap-service"] = get_node_attrs(
                server_xml_path, "hotswap-service")

        bes_detail_list.append(bes)

    return bes_detail_list


def grep_httpd_process(processes):
    httpd_list = []
    process_dict = dict()
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and "httpd" in ps_split[i]:
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                httpd_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break

    httpd_main_process_list = []
    for httpd in httpd_list:
        if httpd["PPID"] == "1":
            httpd_main_process_list.append(httpd)
    return httpd_main_process_list


def xunjian_httpd(serverInfo):
    httpdProcessList = grep_httpd_process(serverInfo["psAll"])
    httpdDetailList = []
    for httpd in httpdProcessList:
        pid = httpd["PID"]
        try:
            httpd["httpd_exe"] = os.popen(
                "readlink -f " + "/proc/" + httpd["PID"] + "/exe").readline().rstrip()
        except Exception as e:
            print("缺少权限, 请使用 --su yes 参数或用 root 执行")
        else:
            httpd["httpd_home"] = os.popen(
                "readlink -f " + "/proc/" + httpd["PID"] + "/cwd").readline().rstrip()
            httpd["httpd_version"] = os.popen(httpd["httpd_exe"] + " -v 2>&1").readline().rstrip().split("/", 1)[1].split()[
                0].strip()
            httpd["httpd_module"] = os.popen(
                httpd["httpd_exe"] + " -V 2>&1").readlines()
        httpd["netstat_count"] = os.popen(
            "netstat -anop | grep " + pid + " | wc -l").readlines()[0]
        httpd["cpu_usage"] = os.popen(
            " ps -p " + pid + " -o pcpu").readlines()[1].strip()
        httpd["mem_usage"] = os.popen(
            " ps -p " + pid + " -o pmem").readlines()[1].strip()
        httpd["cpu_count"] = os.popen(
            "cat /proc/cpuinfo| grep 'processor'| wc -l").readline().strip()
        httpd["umask"] = os.popen(
            "cat /proc/" + pid + "/status | grep -i umask").readlines()
        httpd["ulimit"] = os.popen("cat /proc/" + pid + "/limits").readlines()
        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            httpd["max_open_files"] = os.popen(
                "su - " + httpd["UID"] + " -c 'ulimit -Hn'").readline().rstrip()
            httpd["max_open_files_s"] = os.popen(
                "su - " + httpd["UID"] + " -c 'ulimit -Sn'").readline().rstrip()
        httpd["port"] = os.popen("netstat -luntp | grep " + pid).readlines()
        lsof = os.popen("lsof -p " + pid +
                        "|awk -F ' ' '{print $NF}'").readlines()
        httpd["lsof_count"] = len(lsof)
        httpd["subprocess"] = \
            os.popen("ps -ef | grep httpd | grep -v grep | awk '{print $3}'  | grep " + pid + " | wc -l").readlines()[
                0].strip()

        work_dir = getPath(httpd["httpd_exe"]).rstrip("/bin")
        httpd["work_dir"] = work_dir

        httpd["test_cgi_is_del"] = os.popen(
            "find " + work_dir + "/cgi-bin -name 'test-cgi' 2> /dev/null| wc -l").readline().strip()

        config_path = ""
        for line in httpd["CMD"].split():
            if "-f" in line:
                config_path = httpd["CMD"].split()[-1]

        if config_path is None or not os.path.exists(config_path):
            config_file_name = \
                os.popen(httpd["httpd_exe"] + " -V 2> /dev/null| grep SERVER_CONFIG_FILE").readline().rstrip().split(
                    "=")[
                    1].strip("\"").split("/")[1]
            config_path = os.popen(
                "find " + work_dir + " -maxdepth 3 -type f -name " + config_file_name + " | head -1").readline().rstrip()

        include_file_list = []
        httpd["httpd_conf"] = config_path
        main_config_content = os.popen(
            "cat " + config_path + "|sed 's/^[ ]*//g'|grep -Ev '^$|^#'| sed 's/^M//' | tr -s ' '").readlines()
        httpd["main_config_content"] = main_config_content
        # config filter
        for line in main_config_content:
            if "Options Indexes FollowSymLinks" in line:  # need:Options FollowSymLinks
                httpd["options_index"] = line.rstrip()
            if "ServerSignature" in line:  # default:on ; need:Off
                httpd["server_signature"] = line.split()[1].rstrip()
            if "ServerTokens" in line:  # need:Prod
                httpd["server_tokens"] = line.split()[1].rstrip()
            if "TraceEnable" in line:  # need:Off
                httpd["trace_enable"] = line.split()[1].rstrip()
            if "Include" in line:
                if "modsecurity" not in line:
                    include_file_list.append(line.split()[1].rstrip())

        all_config_file_list = []
        for include_file in include_file_list:
            files = os.popen("ls " + include_file +
                             " 2> /dev/null").readlines()
            if len(files) > 0:
                for item in files:
                    all_config_file_list.append(item.rstrip())
            else:
                files = os.popen("ls " + work_dir + "/" +
                                 include_file + " 2> /dev/null").readlines()
                if len(files) > 0:
                    for item in files:
                        all_config_file_list.append(item.rstrip())

        if len(all_config_file_list) > 0:
            httpd["include_config_content"] = os.popen(
                "cat " + " ".join(all_config_file_list) + "|grep -Ev '^#|^$'| sed 's/^M//'").readlines()
        else:
            httpd["include_config_content"] = []

        access_log_files = set()
        error_log_files = set()

        for file_item in lsof:
            file_item = file_item.strip()
            if file_item.endswith("log") and "access" in file_item:
                access_log_files.add(file_item)
            if file_item.endswith("log") and "error" in file_item:
                error_log_files.add(file_item)
        access_logs = []
        error_logs = []

        for access in access_log_files:
            #access_logs.append(os.popen("tail -n 50 " + access).readlines())
            #修复httpd中access和error日志过多导致无法生成docx的问题
            access_logs.append(os.popen("tail -n 10 " + access).readlines())
        for error in error_log_files:
            #error_logs.append(os.popen("tail -n 200 " + error + "| grep 'error' | tail -n 50").readlines())
            error_logs.append(os.popen("tail -n 200 " + error + "| grep 'error' | tail -n 10").readlines())

        httpd["access_log"] = access_logs
        httpd["error_log"] = error_logs
        httpdDetailList.append(httpd)

    return httpdDetailList

# 过滤activemq进程信息
def grep_activemq_process(processes):
    activemq_list = list()
    process_dict = dict()
    java_list = list()
    for process in processes:
        ps_split = process.split()
        for i in range(len(ps_split)):
            if i == 0:
                process_dict["UID"] = ps_split[i]
            if i == 1:
                process_dict["PID"] = ps_split[i]
            if i == 2:
                process_dict["PPID"] = ps_split[i]
            if i == 3:
                process_dict["C"] = ps_split[i]
            if i == 4:
                process_dict["STIME"] = ps_split[i]
            if i == 5:
                process_dict["TTY"] = ps_split[i]
            if i == 6:
                process_dict["TIME"] = ps_split[i]
            if i == 7 and (ps_split[i].endswith("java")):
                process_dict["CMD"] = " ".join(ps_split[i:len(ps_split)])
                java_list.append(process_dict)
                process_dict = dict()
                break
            if i > 7:
                process_dict = dict()
                break

    for item in java_list:
        if "activemq" in item["CMD"]:
            activemq_list.append(item)

    return activemq_list


# 获取activemq进程/配置/错误日志等信息
def xunjian_activemq(serverInfo):
    activemq_process_list = grep_activemq_process(serverInfo["psAll"])
    activemqDetailList = list()
    for activemq_process in activemq_process_list:
        activemq = dict()
        pid = activemq_process["PID"]
        uid = activemq_process["UID"]
        activemq["user"] = uid
        activemq["PID"] = activemq_process["PID"]
        activemq["CMD"] = activemq_process["CMD"]
        activemq_cwd = os.popen("readlink -f " + "/proc/" + pid + "/cwd").readline().rstrip()
        activemq_home = os.popen("find " + activemq_cwd + "/../ -name 'bin' -type d | head -1").readline().rstrip()
        activemq["activemq_home"] = activemq_home
        if serverInfo.get('whoami') == "root" or serverInfo.get('option_su') == "yes":
            activemq["max_user_processes"] = os.popen("su - " + uid + " -c 'ulimit -Hu'").readline().rstrip()
            activemq["max_user_processes_s"] = os.popen("su - " + uid + " -c 'ulimit -Su'").readline().rstrip()
            activemq["max_open_files"] = os.popen("su - " + uid + " -c 'ulimit -Hn'").readline().rstrip()
            activemq["max_open_files_s"] = os.popen("su - " + uid + " -c 'ulimit -Sn'").readline().rstrip()
            lsof = os.popen("lsof -p " + pid + "|awk -F ' ' '{print $NF}'").readlines()

            activemq["status"] = os.popen(
                "su - " + uid + " -c  '" + activemq_home + "/activemq status" "' 2> /dev/null").readlines()
            activemq["data_status"] = os.popen(
                "su - " + uid + " -c  '" + activemq_home + "/activemq dstat" "' 2> /dev/null").readlines()
            activemq["version"] = os.popen(
                "su - " + uid + " -c  '" + activemq_home + "/activemq --version | grep ActiveMQ""' 2> /dev/null").readlines()

        activemq_xml = os.popen(
            "find " + activemq_home + "/../ -name 'activemq.xml' | grep -v 'examples' | uniq").readline().rstrip()
        jetty_realm = os.popen(
            "find " + activemq_home + "/../ -name 'jetty-realm.properties'  | uniq").readline().rstrip()
        if os.path.exists(activemq_xml):
            activemq["activemq_xml"] = activemq_xml
            activemq["activemq_xml_content"] = os.popen("cat " + activemq["activemq_xml"]).readlines()
        if os.path.exists(jetty_realm):
            activemq["jetty_realm"] = jetty_realm
            activemq["jetty_realm_content"] = os.popen(
                "cat " + activemq["jetty_realm"] + "| grep -Ev '^#|^$' ").readlines()

        log_files = list()
        for file_item in lsof:
            file_item = file_item.strip()
            if file_item.endswith(".log") or file_item.endswith(".out"):
                not_binary = os.popen("file '" + file_item + "' | grep -i text | wc -l").readline().rstrip()
                if not_binary == "1":
                    log_files.append(file_item)

        error_log_content = []
        log_files = set(log_files)

        for error in log_files:
            temp_content = os.popen("tail -n 500 " + error + "| grep -iv 'INFO' | tail -n 30").readlines()
            if len(temp_content):
                error_log_content.append(temp_content)
        activemq["error_logs"] = error_log_content

        activemqDetailList.append(activemq)
    return activemqDetailList

USAGE = """

以 root 用户执行： python middleware_collector.py
以非 root 用户执行： python middleware_collector.py --su no          # 跳过需要 su 的采集项（--su 默认为no）
以非 root 用户执行： python middleware_collector.py --su yes         # 不跳过需要 su 的采集项，需要逐一输入密码
python middleware_collector.py --softlist --softlist=java:weblogic   # 指定采集的软件列表
python middleware_collector.py --notinsoftlist=java:weblogic         # 指定不采集的软件列表

"""

option_su = 'no'
redis_password = ''
option_softlist = []
option_notinsoftlist = []


def print_log(s):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(s))


def xunjian_and_print(title, serverInfo, xunjian_func, file_name, notes_key):
    if len(option_softlist) != 0:
        if title not in option_softlist:
            return

    if title in option_notinsoftlist:
        return

    print_log(title)
    try:
        result = xunjian_func(serverInfo)
        result_json = json.dumps(
            result, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        writeFile(base_dir, file_name, result_json)
        notes[notes_key] = len(result)
    except Exception as e:
        print(traceback.print_exc())
        print("-"*100)


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:", [
                                   "help", "su=", "softlist=", "notinsoftlist=", "redis_password="])
        for opt, value in opts:
            if opt == "-h" or opt == "--help":
                print(USAGE)
                sys.exit(0)
            if opt == "--su":
                option_su = value.strip()
            if opt == "--redis_password":
                redis_password = value.strip()
            if opt == "--softlist":
                option_softlist = option_softlist.split(':')
                option_softlist = [x.strip() for x in option_softlist]
            if opt == "--notinsoftlist":
                option_notinsoftlist = option_notinsoftlist.split(':')
                option_notinsoftlist = [x.strip()
                                        for x in option_notinsoftlist]
    except Exception as e:
        sys.exit(1)

    path = getScriptPath()
    date_now = datetime.datetime.now().strftime('%Y%m%d')
    base_dir = path + "/" + date_now + "_xunjian_data/"

    # 获取服务器信息
    serverInfoTmp = check_linux()
    serverInfoJson = json.dumps(serverInfoTmp, sort_keys=True, indent=4, separators=(
        ',', ': '), ensure_ascii=False)
    serverInfo = serverInfoTmp[0]

    serverInfo['option_su'] = option_su
    # 添加redis_password用于手动填写rediscli密码取info信息
    serverInfo['redis_password'] = redis_password

    # for key in serverInfo.keys():
    #     print(key)
    print(serverInfo['whoami'])
    ip = serverInfo["ip"]

    writeFile(base_dir, ip + "_server.txt", serverInfoJson)
    # 巡检并打印日志、写入文件
    notes = {}

    xunjian_and_print("java", serverInfo, xunjian_java,
                      ip+"_java.txt", "javaCount")
    xunjian_and_print("weblogic", serverInfo, xunjian_weblogic,
                      ip+"_wls.txt", "weblogicCount")
    xunjian_and_print("was", serverInfo, xunjian_was,
                      ip+"_was.txt", "wasCount")
    xunjian_and_print("nginx", serverInfo, xunjian_nginx,
                      ip+"_nginx.txt", "nginxCount")
    xunjian_and_print("redis", serverInfo, xunjian_redis,
                      ip+"_redis.txt", "redisCount")
    xunjian_and_print("rabbitmq", serverInfo, xunjian_rabbitmq,
                      ip+"_rabbitmq.txt", "rabbitmqCount")
    xunjian_and_print("rocketmq", serverInfo, xunjian_rocketmq,
                      ip+"_rocketmq.txt", "rocketmqCount")
    xunjian_and_print("elasticsearch", serverInfo, xunjian_elasticsearch,
                      ip+"_elasticsearch.txt", "elasticSearchCount")
    xunjian_and_print("zookeeper", serverInfo, xunjian_zookeeper,
                      ip+"_zookeeper.txt", "zookeeperCount")
    xunjian_and_print("tomcat", serverInfo, xunjian_tomcat,
                      ip+"_tomcat.txt", "tomcatCount")
    xunjian_and_print("kafka", serverInfo, xunjian_kafka,
                      ip+"_kafka.txt", "kafkaCount")
    xunjian_and_print("httpd", serverInfo, xunjian_httpd,
                      ip+"_httpd.txt", "httpdCount")
    xunjian_and_print("bes", serverInfo, xunjian_bes,
                      ip+"_bes.txt", "besCount")
    xunjian_and_print("activemq", serverInfo, xunjian_activemq, ip+"_activemq.txt", "activemqCount")

    # 写入总结文件
    writeFile(base_dir, ip+"_notes.txt",
              json.dumps([notes], sort_keys=True, indent=4, separators=(',', ': ')))

    # 打包巡检数据
    # print(ip, date_now, date_now)
    # os.system(
    #     "tar -zcf {}_xunjian_data-{}.tar.gz {}_xunjian_data".format(ip, date_now, date_now))
    # os.system("rm -rf {}_xunjian_data".format(date_now))
    # os.system("ls -lrt | grep xunjian")

    os.system(
        "tar -zcf %s_xunjian_data-%s.tar.gz %s_xunjian_data" % (ip, date_now, date_now))
    os.system("rm -rf %s_xunjian_data" % date_now)
    os.system("ls -lrt | grep xunjian")