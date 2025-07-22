# README

## 巡检模板

WebLogic 巡检对应的巡检模板为 `wls-common-版本.zip`

## 数据采集

使用以下命令收集数据，收集完成后数据文件会保存在 `/tmp`目录下，其中一些参数需要根据实际系统环境做更改，详见参数说明。

```bash
edith wls get-conf -p /home/weblogic/user_projects/domains/base_domain/ -f json -o /tmp  --oraclehome /home/wls/Oracle/Middleware/Oracle_Home --extpath /jenkins/jdk1.8.0_201/bin
edith wls get-log -p  /home/weblogic/user_projects/domains/base_domain/  -f json -o /tmp --start 2006-01-02T15:04:05 --end 2026-01-02T15:04:05  --oraclehome /home/wls/Oracle/Middleware/Oracle_Home
edith wls get-status -p /home/weblogic/user_projects/domains/base_domain/ -f json -o /tmp --start 2006-01-02T15:04:05 --end 2026-01-02T15:04:05 --username weblogic --password weblogic12c --url t3://192.168.16.13:7001 -c 5 -i 1 --oraclehome /home/wls/Oracle/Middleware/Oracle_Home

edith os get-conf -o /tmp -f json 
edith os get-status -o /tmp -f json 
edith os get-log -o /tmp -f json
```

参数说明：

```bash
-p  指定 WebLogic 的域目录
-o  指定 Edith 收集到的数据文件存放的目录
-f  json 指定输出为 json 数据格式
--start 和 --end  日志信息的收集区间（在更改时需要注意格式）
--username  WebLogic 控制台的账号
--password  WebLogic 控制台对应账号的密码
--url  WebLogic 控制台的 url
--c  收集次数
--i  多次收集的间隔时间
--oraclehome  WebLogic 的Oracle_Home路径
```

注意：建议使用一个监控专用的 WebLogic 控制台用户去收集数据(例如：`monitor` 用户 `monitor` 用户的创建方法请参考最后一章 **附加** )，而不是直接使用 `weblogic` 用户去收集数据，这样可以控制收集数据使用的用户的权限，使其只能做收集数据时使用

## 在 WebLogic 控制台创建监控用户

创建一个 `monitor` 用户去收集 WebLogic 性能数据。并对该用户的权限进行限制，使其只能进行收集数据的相关操作。

进入 WebLogic 控制台，一次点击 `域结构 --> 安全领域 --> myrealm --> 用户和组 --> 用户 --> 新建` 在新页面中填写：

```bash
名称：monitor
密码：(根据需求填写)
确认密码：(重复输入密码)
```

填写完成后点击 `确认` 完成用户的创建。

在 `用户` 列表中点击自己创建的用户，进入用户的设置。点击 `组` 为当前用户添加 `Monitors` 组后点击保存，为新建用户添加权限。
