# README

## 巡检模板

该应用用于 MongoDB 巡检报告生成。

## 数据采集

```bash
edith mongo get -u [mongo用户名] --password [mongo密码] --host [mongo服务器ip] --port [mongo端口号]  -o /tmp -f json  #收集mongo信息
eg:edith mongo get -u admin --password 123456 --host localhost --port 27017  -o /tmp -f json 

edith os get-conf -o /tmp -f json # 收集配置数据，
edith os get-status -o /tmp -c 5 -f json # 收集状态数据
edith os get-log -o /tmp -f json # 收集日志数据
```

命令执行完毕后，将在 /tmp 下生成 4 个类似如下命名格式的 json 数据格式的数据文件:

```bash
MongoDB.27017.localhost%localdomain.20230424032121.json
SysConfs.linux.localhost%localdomain.20220606025121.json
SysLogs.linux.localhost%localdomain.20220606025539.json
SysStatus.linux.localhost%localdomain.20220606025422.json
```

## 参数说明
- `-o` `--output`，该参数需传入 **输出数据的路径**
- `-f` `--format`，该参数需传入 **输出数据的格式**，如需格式化json文件，可以加入 `--pretty` 参数



可以通过集中管理工具或脚本，将数据汇总到报告主机，在文件打包、传输等过程中**勿对 json 文件进行重命名操作**。

