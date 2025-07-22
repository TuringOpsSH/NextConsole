{{define "main"}}

{{$summary := JsCall "func.summary" .problems}}
{{$appnames := .meta.config.appnames}}
{{$problems := GroupBy .problems "id"}}

---
title: {{.meta.customer}} {{.meta.title}}
subtitle:
author:

- 巡检工程师：{{ .meta.author.name}}
- {{ .meta.org}}

date: {{if .meta.date}}{{.meta.date}}{{else}}{{$summary.date}}{{end}}
---

# 文档版本信息

|版本|日期|作者|说明&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}|{{ .meta.author.name}} |初稿|
|||||

# 巡检总结和建议

## 巡检信息概述

{{println ""}}应用系统名称：{{range .SysConfs}}{{JsCall "func.appname" .host.hostname}}{{end}}
{{println ""}}主机名：{{range .SysConfs}}{{printf "%-13s" .host.hostname}}{{end}}
{{println ""}}IP地址：{{range .SysConfs}}{{range .ip}}{{printf "%-24s" .}}{{end}}{{end}}
{{println ""}}服务器型号：{{range .SysConfs}}{{index .base "Product Name"}}{{end}}
{{println ""}}操作系统版本：{{range .SysConfs}}{{.host.platformFamily}} {{.host.platformVersion}} (发行版: {{.host.platform}}, 内核版本: {{.host.kernelVersion}}){{end}}
{{println ""}}巡检工程师：{{ .meta.author.name}}
{{println ""}}巡检时间：{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}

## 巡检结果汇总

本次巡检检查了{{$summary.hostArrCount}} 台主机{{if eq $summary.group "instance"}}（{{$summary.instArrCount}}个实例）{{end}}共 {{$summary.sum}} 个指标，其中发现 {{$summary.danger}} 个高风险、{{$summary.warning}} 个中风险、{{$summary.green}} 个低风险， 其余{{$summary.ok}} 个正常。告警定义如下：

|风险等级|颜色|标识|定义|
|:---|:---|:---|:---|
|高风险|红色|{{Icon "red"}}|经检查发现的最高级别告警，告警级别基于工程师从问题严重性、时间紧迫性、影响范围等方面的判断，建议及时进行处理。|
|中风险|橙色|{{Icon "orange"}}|经检查发现的中等级别告警，一般为仍然处在发展变化过程中且尚未转化为高风险告警的问题，建议关注问题发展趋势，结合实际情况进行处理。|
|低风险及正常|绿色|{{Icon "green"}}|包括经检查未发现问题的，或虽然存在问题但一般情况下影响可以忽略的告警。此外，对于最佳实践方面的检查结果也归为此类。|

## 巡检总结和建议表

### 高风险

|应用系统|检查内容|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "高风险"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

### 中风险

|应用系统|检查内容|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "中风险"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

### 低风险

|应用系统|检查内容|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "低风险"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

### 正常

|应用系统|检查内容|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "正常"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

# 系统配置检查

## 系统基本配置

{{template "base" .}}

## 系统内核架构检查

{{template "arch" .}}

## 进程列表

{{template "processList" .}}

# 系统容量检查

## CPU使用率

{{range $id, $vs := $problems}}{{if eq $id "win.cpuUsedPercent"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

{{template "cpuUsedPercent" .}}

## 内存

{{range $id, $vs := $problems}}{{if eq $id "win.memUsedPercent"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

{{template "memUsedPercent" .}}

## 磁盘

{{range $id, $vs := $problems}}{{if eq $id "win.diskUsedPercent"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

{{template "diskUsedPercent" .}}

# 安全合规

## 检查admin是否改名

{{range $id, $vs := $problems}}{{if eq $id "win.ifAdminNameChange"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 检查IPV6是否禁用

{{range $id, $vs := $problems}}{{if eq $id "win.ifDisabledIPV6"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 检查Guest用户是否禁用

{{range $id, $vs := $problems}}{{if eq $id "win.ifDisabledGuest"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 检查操作系统激活情况

{{range $id, $vs := $problems}}{{if eq $id "win.ifOperatingSystemActive"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 检查非域服务器关闭共享

{{range $id, $vs := $problems}}{{if eq $id "win.ifNonDomainServerClosedShare"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 检查非域服务器关闭共享

{{range $id, $vs := $problems}}{{if eq $id "win.memoryBeforeShutdown"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 检查任务计划是否已域admin身份启动

{{range $id, $vs := $problems}}{{if eq $id "win.ifTaskPlanStartedAsDomainAdmin"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 检查磁盘驱动器信息

{{range $id, $vs := $problems}}{{if eq $id "win.hardDiskSMARTInfo"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

{{range .problems}}{{if eq .id "win.hardDiskSMARTInfo"}}

|              磁盘驱动               |         状态         |         告警      |
|:-------------------------------:|:------------------:|:---------------:|
| {{range .mixraw}}  {{.caption}} | {{.status}} | {{Icon .mixlevel}} |

{{end}}
{{end}}{{end}}

## 检查服务是否禁用

{{template "ifServiceDisabled" .}}

## 检查默认共享文件夹情况

{{template "defaultSharedFolder" .}}

## 检查任务计划执行用户

{{template "whoExecutesTaskPlan" .}}
## 收集本地用户信息

{{template "localUserInformation" .}}

# 系统健康检查

##  TCP连接情况检查

{{template "conns" .}}

# 日志信息

## windows系统日志的最近10个错误和警告事件

{{template "recent10ErrorMsg" .}}

## 系统日志的配置信息

{{range .problems}}{{if eq .id "win.basicLogConfInfo"}}

| 配置项                | 值                              |
|:-------------------|:-------------------------------|
| channelAccess      | {{ .raw.channelAccess}}        |
| enabled            | {{ .raw.enabled}}              |
| isolation          | {{.raw.isolation}}             |
| name               | {{.raw.name}}                  |
| owningPublisher    | {{.raw.owningPublisher }}      |
| type               | {{.raw.type}}                  |
| logging            | -----------------------------  |
| \ autoBackup       | {{.raw.logging.autoBackup}}    |
| \ logFileName      | {{.raw.logging.logFileName}}   |
| \ maxSize          | {{.raw.logging.maxSize}}       |
| \ retention        | {{.raw.logging.retention}}     |
| publishing fileMax | {{.raw.publishing.fileMax}}    |

{{end}}{{end}}

## 安全日志配置信息

{{range .problems}}{{if eq .id "win.safeLogConfInfo"}}

| 配置项                | 值                              |
|:-------------------|:-------------------------------|
| channelAccess      | {{ .raw.channelAccess}}        |
| enabled            | {{ .raw.enabled}}              |
| isolation          | {{.raw.isolation}}             |
| name               | {{.raw.name}}                  |
| owningPublisher    | {{.raw.owningPublisher }}      |
| type               | {{.raw.type}}                  |
| logging            | -----------------------------  |
| \ autoBackup       | {{.raw.logging.autoBackup}}    |
| \ logFileName      | {{.raw.logging.logFileName}}   |
| \ maxSize          | {{.raw.logging.maxSize}}       |
| \ retention        | {{.raw.logging.retention}}     |
| publishing fileMax | {{.raw.publishing.fileMax}}    |

{{end}}{{end}}

## 应用程序日志的状态

{{range .problems}}{{if eq .id "win.logStatusInfo"}}

| 配置项                          | 值                             |
|:-----------------------------|:------------------------------|
| creationTime                 | {{ .raw.creationTime}}        |
| lastAccessTime               | {{ .raw.lastAccessTime}}      |
| lastWriteTime                | {{.raw.lastWriteTime}}        |
| fileSize                     | {{.raw.fileSize}}             |
| attributes                   | {{.raw.attributes }}          |
| numberOfLogRecords           | {{.raw.numberOfLogRecords}}   |
| oldestRecordNumber           | {{.raw.oldestRecordNumber}}   |

{{end}}{{end}}

## 系统事件日志中最近一个月内 Error 和 Warning 的记录数

{{range .problems}}{{if eq .id "win.errorLogForMonth"}}

|            Computer            |    Date     |    Description    |     EventID     |    Keyword    |    Level    |    LogName    |    Opcode    |   Source   | Task      |   User    |    UserName    | eventKey    |
|:------------------------------:|:-----------:|:-----------------:|:---------------:|:-------------:|:-----------:|:-------------:|:------------:|:----------:|:---------:|:---------:|:---------:|:---------:|
| {{range .raw}}  {{.Computer}}  | {{.Date}}   | {{.Description}}  | {{.EventID}}    | {{.Keyword}}  | {{.Level}}  | {{.LogName}}  | {{.Opcode}}  |{{.Source}} | {{.Task}} | {{.User}} |{{.UserName}} |{{.eventKey}} |
{{end}}{{end}}{{end}}




{{end}}