{{define "main_bak"}}

{{ $summary := JsCall "func.summary" .problems }}


---
title: {{.meta.customer}} {{.meta.title}}
subtitle: {{if .meta.sys}}{{.meta.sys}}{{else}}{{range .SysConfs}}{{JsCall "func.appname" .host.hostname}}{{end}}{{end}}
author:

- {{ .meta.author.name}} ({{ .meta.author.email}})
- {{ .meta.org}}

date: {{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}
---

# 巡检总结和建议

## 巡检信息概述

{{println ""}}巡检人员：{{ .meta.author.name}}
{{println ""}}巡检时间：{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}

## 巡检告警定义

| 风险等级 | 颜色  | 标识                | 定义                                                    |
|:-----|:----|:------------------|:------------------------------------------------------|
| 高风险  | 红色  | {{Icon "red"}}    | 该告警可能会影响生产系统使用、系统稳定性或系统安全性，建议及时安排变更窗口处理。              |
| 中风险  | 橙色  | {{Icon "orange"}} | 该告警一般为不影响生产系统使用、非关键，我们会在汇总报告提供对应的最佳实践，建议在合适的变更窗口进行调整。 |
| 低风险  | 绿色  | {{Icon "green"}}  | 最佳实践，不需要关注。                                           |

## 巡检总结和建议表

### 高风险

| 检查内容                                                                                           | 主机名         | 实例名           | 预期值           | 实际值             | 告警           | 建议              |
|:-----------------------------------------------------------------------------------------------|:------------|:--------------|:--------------|:----------------|:-------------|:----------------|
 {{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "高风险"}} | {{$v.name}} | {{.hostname}} | {{$v.expected}} | {{.actual}}  | {{Icon .level}} | {{$v.solution}}|
{{end}}{{end}}{{end}}

### 中低风险

| 检查内容                                                                                           | 主机名         | 实例名           | 预期值           | 实际值             | 告警          | 建议              |
|:-----------------------------------------------------------------------------------------------|:------------|:--------------|:--------------|:----------------|:------------|:----------------|
 {{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "中风险"}} | {{$v.name}} | {{.hostname}} | {{$v.expected}} | {{.actual}} | {{Icon .level}} | {{$v.solution}}|
{{end}}{{end}}{{end}}

## 告警数量统计

（实例名为空表示操作系统检查）

| 主机名                                                   | 实例名           | 高风险告警数量               | 中风险告警数量 |
|:------------------------------------------------------|:--------------|:----------------------|:--------|
{{range $host, $v := $summary.hosterrcount}}| {{$host}} | {{$v.danger}} | {{$v.warning}} |
{{end}}


## 巡检总结和建议表

{{ if $summary.iderr }}
| 检查内容 | 主机名 | 实例名 | 预期值 | 实际值 | 检查结果 | 建议 |
|:---|:---|:---|:---|:---|:---|:---| {{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "高风险"}} 
| {{$v.name}} | {{.hostname}} | {{$v.expected}} | {{.actual}} | {{Icon .level}} | {{$v.solution}} | {{end}}{{end}}{{end}}
{{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "中风险"}} | {{$v.name}} | {{.hostname}} | {{$v.expected}} | {{.actual}} | {{Icon .level}} | {{$v.solution}} |
{{end}}{{end}}{{end}}

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
