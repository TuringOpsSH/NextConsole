{{define "main"}}

---
title: {{ .meta.title}}
subtitle: {{.meta.sys}}
author:
    - {{ .meta.author.name}} ({{ .meta.author.email}})
    - {{ .meta.org}} 

date: {{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}
---

# 巡检范围

## 主机列表

| 主机名      	 | IP                  | 操作系统                                          | WAS版本        |
| :------------ | :------------------ |:----------------------------------------------| :------------ | 
{{range .WasConfs}}|{{printf " %-13s| " .host.hostname}}{{"todo"}}|{{printf " %-13s |" .host.os}}{{"todo"}}|
{{end}}

## Cells
{{range .WasConfs}}
### {{ .cell.name}}

#### 节点

{{range .nodes}} * {{.name}} 
 {{end}}

{{$st := JsCall "func.check" .clusters}}
{{ if eq $st "ok"}}
{{range .clusters}}
#### 集群

{{.name}} ({{len .members}} 个成员)
 ~ {{range .members}} {{.name}} {{end}}
{{end}}
{{end}}
{{end}}

# 核心参数


## 数据源

{{range .WasConfs}}{{$st2 := JsCall "func.check2" .dataSources.cluster}}{{ if eq $st2 "ok"}}{{range .dataSources.cluster}}
#### 集群{{.target}}的数据源



{{if .dataSources}}{{range .dataSources}}
| 名称        | JNDI 名称        | 最小连接数    | 最大连接数    | Url    |
| :--------- | :------------ | -----: | -----: | :--------------------------- |
|{{printf " %-13s|" .name}}{{printf " %-13s|" .jndi}}{{printf " %-13s|" .connectionPool.min}}{{printf " %-13s|" .connectionPool.max}}{{printf " %-13s|" .url}}
{{end}}{{else}}	No Datasource{{end}}{{end}}

{{end}}
{{end}}

## 线程池

| 应用程序服务器| 最小大小 | 最大大小 | 线程不活动超时 | 
| :---------------- | --: | --: | ----------------: | 
{{range .WasConfs}}{{range .servers}}{{if eq .name "dmgr"}}{{else}}{{if eq .name "nodeagent"}}{{else}}{{printf "| %-18s|" .name}}{{printf " %3s |" .threadPool.min}}{{printf " %3s |" .threadPool.max}}{{printf " %17s |" .threadPool.inactivityTimeout}}
{{end}}{{end}}{{end}}{{end}}

## 虚拟机

{{range .WasConfs}}

| 应用程序服务器            |      初始内存大小 |                 最大堆内存大小 | 输出垃圾回收情况                   | 参数                           |
|:----------------------------------------------------------------------------------------------|------------:|------------------------:|:---------------------------|:-----------------------------|
 {{range .servers}}{{if eq .name "dmgr"}}{{else}}{{if eq .name "nodeagent"}}{{else}}{{printf " |       %-18s | " .name}}{{printf " %6s | " .jvm.xms}}{{printf " %5s | " .jvm.xmx}}{{printf " %-13s |" .jvm.verboseGC}}{{printf " %-62s|" .jvm.arguments}}
{{end}}{{end}}{{end}}
----------------------------------------------------------------------------------------------

{{end}}

## 日志配置

### SystemOut

| 应用程序服务器 | 日志文件循环 | 文件大小 | 重复时间 | 历史日志文件的最大数 |开始时间 | 文件名 |
| :---------------- |:-------|--------------------------:|--------------------------------------------------:|--------------------------------------------------:|----------------------------------------------------:|:------------------------------------------------------------|
{{range .WasConfs}}{{range .servers}}{{if eq .name "dmgr"}}{{else}}{{if eq .name "nodeagent"}}{{else}}{{printf "| %-18s  | " .name}}{{printf " %-13s | " .logging.systemOut.rolloverType}}{{printf " %5s | " .logging.systemOut.rolloverSize}}{{printf " %6s | " .logging.systemOut.rolloverPeriod}}{{printf " %7s | " .logging.systemOut.maxNumberOfBackupFiles}}{{printf " %8s |" .logging.systemOut.baseHour}}{{printf " %-35s|" .logging.systemOut.fileName}}
{{end}}{{end}}{{end}}{{end}}

### SystemErr

| 应用程序服务器 | 日志文件循环 | 文件大小  | 重复时间 | 历史日志文件的最大数  | 开始时间 | 文件名|
| :---------------- | :----------- | ----: | -----: | ------: | -------: | :--------------------------------- |
{{range .WasConfs}}{{range .servers}}{{if eq .name "dmgr"}}{{else}}{{if eq .name "nodeagent"}}{{else}}{{printf "| %-18s|" .name}}{{printf " %-13s|" .logging.systemErr.rolloverType}}{{printf " %5s |" .logging.systemErr.rolloverSize}}{{printf " %6s |" .logging.systemErr.rolloverPeriod}}{{printf " %7s |" .logging.systemErr.maxNumberOfBackupFiles}}{{printf " %8s |" .logging.systemErr.baseHour}}{{printf " %-35s|" .logging.systemErr.fileName}}
{{end}}{{end}}{{end}}{{end}}

# 垃圾回收 todo
{{range .gclogs}}{{$sidataFilePath := .sidataFilePath}}
{{range .WasLog}}
## {{ .server}}

### 基本信息

{{with .gclog.stat}}
时间范围:
 ~ {{.start}} -- {{.end}}

Heap空闲趋势:
 ~ {{.firstFree}} -- {{.lastFree}}

垃圾回收次数:
 ~ {{.count}}

单次垃圾回收字节数:
 ~ {{.average}}

垃圾回收时间占比:
 ~ {{.gcTime}}({{printf "%g" .gcTimePercent}})

堆达到最大值:
 ~ {{.maxTotal}}

虚拟机重启次数:
 ~ {{len .vms}}
{{end}}

### 垃圾回收图

![Gc Log]({{RelativePath $sidataFilePath .gclog.gcChartPath}})



{{end}}
{{end}}

# 日志问题

{{range .WasLogs}}
{{range .WasLog}}## 应用程序服务器: {{ .server}}

### SystemOut Warnings and Errors ({{ len .SystemOut}} Types) 
{{range .SystemOut}}
#### '{{.module}}' {{.level}} ({{.count}} times)

源文件
 ~ {{ .origin}}

时间
 ~ {{ .time}}

错误代码
 ~ {{ .code}}

{{if .msg}}信息
 ~ {{ .msg}}{{end}}

{{if .detail}}详情
 ~ {{ .detail}}{{end}}

{{end}}{{end}}
{{end}}

{{end}}

