# README

## 巡检模板

Nginx 巡检对应的巡检模板为 `nginx-common-版本号.zip`

## 数据采集

```bash
edith nginx get-conf -p /usr/local/nginx -o /tmp -f json  #收集nginx配置数据
edith nginx get-status -p /usr/local/nginx -o /tmp -f json    #收集nginx状态数据
edith nginx get-log -p /usr/local/nginx -o /tmp -f json     #收集nginx日志数据

edith os get-conf -o /tmp -f json # 收集配置数据，
edith os get-status -o /tmp -c 5 -f json # 收集状态数据
edith os get-log -o /tmp -f json # 收集日志数据
```

命令执行完毕后，将在 /tmp 下生成 6 个类似如下命名格式的 json 数据格式的数据文件:

```bash
NginxConfs.linux.localhost%localdomain.20220606030734.json
NginxLogs.linux.localhost%localdomain.20220606031145.json
NginxStatus.linux.localhost%localdomain.20220606031338.json
SysConfs.linux.localhost%localdomain.20220606025121.json
SysLogs.linux.localhost%localdomain.20220606025539.json
SysStatus.linux.localhost%localdomain.20220606025422.json
```

可以通过集中管理工具或脚本，将数据汇总到报告主机，在文件打包、传输等过程中**勿对 json 文件进行重命名操作**。

