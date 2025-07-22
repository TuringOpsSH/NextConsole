# README

## 巡检模板

Apache 巡检对应的巡检模板为 `apache-common-版本号.zip`

## 数据采集

```bash
edith os get-conf -o /tmp -f json # 收集配置数据
edith os get-log -o /tmp -f json # 收集日志数据
edith os get-status -o /tmp -f json -c 5 # 收集状态数据
edith httpd get-log -o /tmp -f json -p /usr/local/httpd
edith httpd get-conf -o /tmp -f json -p /usr/local/httpd
edith httpd get-status -p /usr/local/httpd -u http://IP:PORT/server-status -o /tmp -f json
```

## 一键式采集

```bash
edith httpd get-cmd -p /usr/local/httpd # 打印采集脚本
edith httpd get-cmd -p /usr/local/httpd | bash  # 执行采集脚本
```

## 参数说明
- `-p` `--path`，该参数需传入Apache服务的 **安装路径**
- `-o` `--output`，该参数需传入 **输出数据的路径**
- `-f` `--format`，该参数需传入 **输出数据的格式**，如需格式化json文件，可以加入 `--pretty` 参数
- `-u` `--url`，如待检测的Apache服务已经开启了server-status服务，则需传入该服务的的完整 server-status URL
