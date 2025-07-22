# README

## 数据采集

```bash
### linux
edith os get-conf -o /tmp -f json # 收集配置数据
edith os get-log -o /tmp -f json # 收集日志数据
edith os get-status -o /tmp -f json -c 5 # 收集状态数据

### apache
edith httpd get-log -o /tmp -f json -p /usr/local/httpd
edith httpd get-conf -o /tmp -f json -p /usr/local/httpd
edith httpd get-status -p /usr/local/httpd -u http://IP:PORT/server-status -o /tmp -f json

### apache一键式采集
edith httpd get-cmd -p /usr/local/httpd # 打印采集脚本
edith httpd get-cmd -p /usr/local/httpd | bash  # 执行采集脚本

### apache 参数说明
# - `-p` `--path`，该参数需传入Apache服务的 **安装路径**
# - `-o` `--output`，该参数需传入 **输出数据的路径**
# - `-f` `--format`，该参数需传入 **输出数据的格式**，如需格式化json文件，可以加入 `--pretty` 参数
# - `-u` `--url`，如待检测的Apache服务已经开启了server-status服务，则需传入该服务的的完整 server-status URL


### nginx
edith nginx get-conf -p /usr/local/nginx -o /tmp -f json  #收集nginx配置数据
edith nginx get-status -p /usr/local/nginx -o /tmp -f json    #收集nginx状态数据
edith nginx get-log -p /usr/local/nginx -o /tmp -f json     #收集nginx日志数据


### tomcat
edith tomcat get-log --path /app/apache-tomcat-8.5.75 -o /tmp -f json
edith tomcat get-conf --path /app/apache-tomcat-8.5.75 -o /tmp -f json


### was
edith was get-log --profile /WebSphere/AppServer/profiles/AppSrv01/ -o /edith_data -f json
edith was get-conf --profile /WebSphere/AppServer/profiles/AppSrv01/ -o /edith_data -f json


### webLogic
edith wls get-conf -p /home/weblogic/user_projects/domains/base_domain/ -f json -o /tmp  --oraclehome /home/wls/Oracle/Middleware/Oracle_Home --extpath /jenkins/jdk1.8.0_201/bin
edith wls get-log -p  /home/weblogic/user_projects/domains/base_domain/  -f json -o /tmp --start 2006-01-02T15:04:05 --end 2026-01-02T15:04:05  --oraclehome /home/wls/Oracle/Middleware/Oracle_Home
edith wls get-status -p /home/weblogic/user_projects/domains/base_domain/ -f json -o /tmp --start 2006-01-02T15:04:05 --end 2026-01-02T15:04:05 --username weblogic --password weblogic12c --url t3://192.168.16.13:7001 -c 5 -i 1 --oraclehome /home/wls/Oracle/Middleware/Oracle_Home

### webLogic参数说明：
#-p  指定 WebLogic 的域目录
#-o  指定 Edith 收集到的数据文件存放的目录
#-f  json 指定输出为 json 数据格式
#--start 和 --end  日志信息的收集区间（在更改时需要注意格式）
#--username  WebLogic 控制台的账号
#--password  WebLogic 控制台对应账号的密码
#--url  WebLogic 控制台的 url
#--c  收集次数
#--i  多次收集的间隔时间
#--oraclehome  WebLogic 的Oracle_Home路径
```