# README

该应用用于 Linux 巡检报告生成。

## 数据采集

```bash
edith os get-conf -o /tmp -f json # 收集配置数据
edith os get-log -o /tmp -f json # 收集日志数据
edith os get-status -o /tmp -f json -c 5 # 收集状态数据
```

## 支持的参数

- `-c` | `--count` 设置采集次数，例如采集CPU占用率信息时需要多次取值观察结果
- `--start` 设置采集距当前时间段内的日志，例如采集Linux系统日志时只取近几天的日志内容，默认值为30d，支持输入格式："1d3h5m7s"
- `-i` | `--interval` 设置采集间隔，例如采集CPU占用率信息时设置一段间隔的比率
- `-t` | `--task` 设置采集项，使采集结果只输出指定采集项，采集项间使用冒号间隔

## 一键式采集

```bash
edith os get-cmd # 打印采集脚本
edith os get-cmd | bash  # 执行采集脚本
```
