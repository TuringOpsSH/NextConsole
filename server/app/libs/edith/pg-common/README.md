# README

## 巡检模板

pg 巡检对应的巡检模板为 `pg-common-版本号.zip`

## 数据采集

### 一键式采集

```bash
edith pg get -u [PgSQL用户名] --password [密码] -f json -o /tmp
如果用户不是postgres用户 需要加-d参数指定数据库（默认巡检数据库为postgres）
edith pg get -u [PgSQL用户名] --password [密码] -d postgres  -f json -o /tmp

支持远程连接PgSQL
edith pg get  --host [远程主机的IP] --port [远程主机的数据库端口] -u [PgSQL用户名]  --password [密码] -f json -o /tmp
```

### 系统数据采集（目前报告尚未整合该数据，暂可不执行该命令）

```bash
edith os get-conf -o /tmp -f json # 收集配置数据
edith os get-log -o /tmp -f json # 收集日志数据
edith os get-status -o /tmp -f json -c 5 # 收集状态数据
```

命令执行完毕后，将在 /tmp 下生成 4 个类似如下命名格式的 json 数据格式的数据文件:

```bash
PostgreSQL.5432.localhost%localdomain.20220923105909.json
SysConfs.linux.localhost%localdomain.20220606025121.json
SysLogs.linux.localhost%localdomain.20220606025539.json
SysStatus.linux.localhost%localdomain.20220606025422.json
```

## 参数说明
- `-o` `--output`，该参数需传入 **输出数据的路径**
- `-f` `--format`，该参数需传入 **输出数据的格式**，如需格式化json文件，可以加入 `--pretty` 参数
- `-t`，该参数需传入指定的 **采集项**


可以通过集中管理工具或脚本，将数据汇总到报告主机，在文件打包、传输等过程中**勿对 json 文件进行重命名操作**。

