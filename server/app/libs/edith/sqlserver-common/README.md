# README

## 数据收集命令

使用以下命令采集SQL Server 巡检数据：

Windows下:
```powershell
.\edith sqlserver get --host localhost --port 1433 --format json --output .\ --pretty --loglevel D

采集数据库的索引碎片信息可能耗时较长，可通过 -k 参数设置跳过不采集:
.\edith sqlserver get --host localhost --port 1433 --format json --output .\ --pretty --loglevel D -k view_index_fragmentation_information_for_all_databases
```

Linux下：
```bash
./edith sqlserver get --host localhost --port 1433 --format json --output ./ --pretty --loglevel D
```

`--username` 用户名（可选）
`--password` 用户密码（可选）
`--host`     设置服务器IP（必须）
`--port`     设置服务端口（必须）
`--format | -f`   指定输出文件格式为JSON（必须）
`--pretty`   对JSON进行格式化处理（可选）
`--loglevel` 设置日志级别: Debug(D), Info(I), Warning(W), Error(E) (default "E") （可选）
`--output | -o`   指定输出文件路径
`--skip | -k` 跳过收集指定巡检项， 如 -k view_index_fragmentation_information_for_all_databases

## 结果文件

SQL Server 巡检数据仅1个，示例如下：

```
SQLServer.localhost,1433.WINNEW2016.20230516104724.json
```
