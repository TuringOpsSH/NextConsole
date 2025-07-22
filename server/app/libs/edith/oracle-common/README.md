# README

该应用用于 Oracle 巡检报告生成。

## 数据采集

使用oracle用户登录服务器，然后使用oracle用户运行数据收集命令，其中 `--sid` 的值 `t11fsdb` 需替换为对应的实例名：

```bash
c4d056ba-5bb9-46c4-913e-7462a8aa7f92 oracle get-conf --sid t11fsdb -f json -t conf -o /tmp # 收集实例 t11fsdb 的配置数据，各数据库实例分别以oracle用户身份执行一次
c4d056ba-5bb9-46c4-913e-7462a8aa7f92 oracle get-status --sid t11fsdb -f json -t status -o /tmp # 收集实例 t11fsdb 的状态数据，各数据库实例分别以oracle用户身份执行一次
c4d056ba-5bb9-46c4-913e-7462a8aa7f92 oracle get-log --sid t11fsdb -f json -t log -o /tmp # 收集实例 t11fsdb 的日志数据，各数据库实例分别以oracle用户身份执行一次

c4d056ba-5bb9-46c4-913e-7462a8aa7f92 os get-conf -o /tmp -f json # 收集配置数据，同一主机以oracle或root用户身份执行一次
c4d056ba-5bb9-46c4-913e-7462a8aa7f92 os get-status -o /tmp -c 5 -f json # 收集状态数据，同一主机以oracle或root用户身份执行一次
c4d056ba-5bb9-46c4-913e-7462a8aa7f92 os get-log -o /tmp -f json # 收集日志数据，同一主机以oracle或root用户身份执行一次
```

如果不清楚数据库实例名，可以使用脚本：

```bash
ps -ef | grep "ora_ckpt_" | grep -v ASM | grep -v grep | grep -v "+APX" | \
grep -v "MGMTDB" | awk '{print $NF}' | sed 's/ora_ckpt_//'| grep -v '/' | while read sid
do
    c4d056ba-5bb9-46c4-913e-7462a8aa7f92 oracle get-conf --sid $sid -f json -t conf -o /tmp
    c4d056ba-5bb9-46c4-913e-7462a8aa7f92 oracle get-status --sid $sid -f json -t status -o /tmp
    c4d056ba-5bb9-46c4-913e-7462a8aa7f92 oracle get-log --sid $sid -f json -t log -o /tmp
done

c4d056ba-5bb9-46c4-913e-7462a8aa7f92 os get-conf -o /tmp -f json
c4d056ba-5bb9-46c4-913e-7462a8aa7f92 os get-status -o /tmp -c 5 -f json
c4d056ba-5bb9-46c4-913e-7462a8aa7f92 os get-log -o /tmp -f json
```

命令执行完毕后，将在 /tmp 下生成 6 个类似如下命名格式的 json 数据格式的数据文件，其中 orafs11g 对应主机名字段：

```bash
OracleConfs.t11fsdb.orafs11g.20220325111733.json
OracleLogs.t11fsdb.orafs11g.20220325111739.json
OracleStatus.t11fsdb.orafs11g.20220325111738.json
SysConfs.linux.orafs11g.20220325111742.json
SysLogs.linux.orafs11g.20220325111743.json
SysStatus.linux.orafs11g.20220325111924.json
```

可以通过集中管理工具或脚本，将数据汇总到报告主机，在文件打包、传输等过程中**勿对 json 文件进行重命名操作**。

## 一键式采集

```bash
c4d056ba-5bb9-46c4-913e-7462a8aa7f92 oracle get-cmd # 打印采集脚本
c4d056ba-5bb9-46c4-913e-7462a8aa7f92 oracle get-cmd | bash  # 执行采集脚本
```

## Windows 下巡检脚本参考

```bat
rem =======================================================================================================
rem  1. 复制以下内容, 使用记事本新建一个.bat为后缀的批处理脚本, 然后双击该脚本开始收集
rem  2. 如果未将 edith.exe 所在路径加入系统 Path， 请确保 edith.exe 在当前路径下或手动替换为绝对路径
rem  3. 勿以 “edith oracle get-cmd --oraclehome xxx --gridhome yyy | cmd” 方式执行！
rem =======================================================================================================

@echo off & setlocal enabledelayedexpansion
cmd /C sc query | findstr OracleService | findstr SERVICE_NAME | findstr /v ASM | findstr -v MGMTDB | findstr -v APX >instlist.log
for /f "delims=: tokens=2" %%i in (.\instlist.log) do (
set "str=%%i"
set SID=nydyy
SET ORACLE_SID=nydyy
edith.exe oracle get-conf --sid nydyy -f json -t conf  --loglevel I --oraclehome=D:\app\Administrator\oracle19c -o ..\report_oracle
edith.exe oracle get-status --sid nydyy -f json -t status --loglevel I --oraclehome=D:\app\Administrator\oracle19c -o ..\report_oracle
edith.exe oracle get-log --sid nydyy -f json -t --loglevel I --oraclehome=D:\app\Administrator\oracle19c -o ..\report_oracle
)

edith.exe os get-conf -t base:disk:etchosts:mem:mount:ntpsync:sysctla:zone -o ..\report_oracle  -f json --loglevel I
rem edith os get-log -o ..\report_oracle  -f json --loglevel I
edith.exe os get-status -t cpupct:dfihP:ntpdstatus:psaux:psef -o ..\report_oracle  -f json -c 5 --loglevel I
del .\instlist.log 
rem =======================================================================================================

```
