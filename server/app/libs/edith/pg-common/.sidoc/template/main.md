{{define "main"}}

{{$problems := GroupBy .problems "id"}}
{{$summary := JsCall "func.summary" .problems}}
{{$appnames := .meta.config.appnames}}


---
title: {{.meta.customer}} {{.meta.title}}
subtitle: {{range .PostgreSQL}}{{JsCall "func.appname" .host.hostname $appnames}}{{end}}
author:
- 巡检工程师：{{ .meta.author.name}}
- {{ .meta.org}}

date: {{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}
---

# 文档版本信息

|版本|日期|作者|说明&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}|{{ .meta.author.name}} |初稿|
|||||

# 巡检总结和建议

## 巡检信息概述
{{println ""}}主机名：{{if .SysConfs}}{{range .SysConfs}}{{printf "%-13s" .host.hostname}}{{end}}{{else}}{{range .OracleConfs}}{{index .host "hostname"}} {{end}}{{end}}
{{println ""}}数据库实例：{{range .OracleConfs}}{{index .instance "sid"}} {{end}}
{{println ""}}巡检工程师：{{ .meta.author.name}}
{{println ""}}巡检报告生成时间：{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}

## 巡检告警定义
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



# 基本配置检查

{{if .SysConfs}}
## 操作系统基本配置
{{range .SysConfs}}

|配置项|值|
|:---|:---|
{{range $k,$v := .base}}{{if ne $k "_check"}}|{{$k}}|{{$v}}|
{{end}}{{end}}

{{end}}
{{else}}
{{range .PostgreSQL}}

|配置项|值|
|:---|:---|
{{range $k,$v := .host}}{{if ne $k "_check"}}|{{$k}}|{{$v}}|
{{end}}{{end}}

{{end}}
{{end}}


# 数据库总体概况
## 版本
{{template "pg.pgversion" .}}

## 基本配置
{{template "pg.pgsettings" .}}

## 集群信息
{{template "pg.cluster_info" .}}

## Extensions
{{template "pg.extensions" .}}

## 配置文件修改信息
{{template "pg.altersettings" .}}

## ext_settings  todo

## Autovacuum全局配置信息
{{template "pg.autovacuum_settings_global" .}}

## Autovacuum表配置信息
{{template "pg.autovacuum_settings_table" .}}

## Autovacuum事务ID换行检查
{{template "pg.autovacuum_wraparound" .}}

## Autovacuum堆膨胀
{{template "pg.heap_bloat" .}}

## Autovacuum Btree指数膨胀
{{template "pg.index_bloat" .}}

## Autovacuum资源使用情况
{{template "pg.autovacuum_resource_usage" .}}

## 内存配置信息
{{template "pg.memory_related_settings" .}}

## current_connections
{{template "pg.current_connections" .}}

## 超时、锁、死锁
{{template "pg.timeouts_locks" .}}

## Invalid Indexes todo

## Unused Indexes todo

## Non-indexed Foreign Keys todo

## Redundant Indexes todo

## 数据库表的大小信息
{{template "pg.table_sizes" .}}

## Integer (int2, int4) Out-of-range Risks in PKs   todo



{{end}}