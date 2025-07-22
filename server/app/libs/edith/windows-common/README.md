# README

## 巡检模板

Windows 巡检对应的巡检模板为 `windows-common-版本.zip`

## 数据采集

`windows-common-版本.zip` 模板要求采集3个数据：

```PowerShell
edith os get-conf -o ./ -f json --loglevel D
edith os get-log -o ./ -f json --loglevel D
edith os get-status -o ./ -f json -c 5 --loglevel D
```

## 支持的参数

- `-c` `--count` 设置采集次数，例如采集CPU占用率信息时需要多次取值观察结果
- `-i` `--interval` 设置采集间隔，例如采集CPU占用率信息时设置一段间隔的比率
- `-t` `--task` 设置采集项，使采集结果只输出指定采集项，采集项间使用冒号间隔
