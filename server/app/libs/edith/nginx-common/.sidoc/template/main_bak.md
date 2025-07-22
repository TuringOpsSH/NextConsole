{{define "main_bak"}}

{{template "meta" .}}
{{ $summary := JsCall "func.summary" .problems }}

# 概述

根据本项目的服务合同和用户的要求，我方对**Nginx（httpd）**中间件服务进行例行巡检。巡检过程中,北京中亦安图科技有限公司工程师得到了相关负责人的大力支持，按计划顺利完成了本次巡检工作。

## 范围

本次巡检包含了 {{$summary.hostsCount}} 台主机，及其上安装的Nginx（httpd）服务。

本次巡检主要使用工具进行统一数据收集、分析。在数据的基础上，与最佳实践比对，提出整改建议。

## 巡检项目

|**巡检项目**|
|:---|
{{range $summary.nameArr}}|{{.}}|
{{end}}

## 告警定义

|风险等级|颜色|标识|定义|
|:---|:---|:---|:---|
|高风险|红色|{{Icon "red"}}|该告警可能会影响生产系统使用、系统稳定性或系统安全性，建议及时安排变更窗口处理。|
|中风险|橙色|{{Icon "orange"}}|该告警一般为不影响生产系统使用、非关键，我们会在汇总报告提供对应的最佳实践，建议在合适的变更窗口进行调整。|
|低风险|绿色|{{Icon "green"}}|最佳实践，不需要关注。|

# 分析及建议汇总

## 总体分析及建议

此次巡检总计检查{{$summary.sum}}个关键项目，发现{{$summary.danger}}个高风险告警、{{$summary.warning}}个中风险告警。

## 告警数量统计

（实例名为空表示操作系统检查）

|主机名|实例名|高风险告警数量|中风险告警数量|
|:---|:---|:---|:---|
{{range $host, $v := $summary.hosterrcount}}|{{$host}} | {{$v.danger}} | {{$v.warning}}|
{{end}}


## 巡检总结和建议表

|检查内容|主机名|实例名|预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|
{{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "高风险"}}|{{$v.name}}//{{$id}}|{{.hostname}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{$v.solution}}|
{{end}}{{end}}{{end}}{{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "中风险"}}|{{$v.name}}//{{$id}}|{{.hostname}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{$v.solution}}|
{{end}}{{end}}{{end}}

# 系统参数检查

## CPU负载
{{template "cpu" .}}

## 内存使用情况
{{template "mem" .}}

## 磁盘使用率统计
{{template "disk" .}}

# Nginx检查
## 常规检查
{{template "nginx.routine" .}}

## 全局配置参数检查
{{template "nginx.globalConf" .}}

## HTTP 参数配置检查
{{template "nginx.httpConf" .}}

## Location 配置检查
{{template "nginx.locationConf" .}}

## Fast-cgi 配置检查
{{template "nginx.fast-cgiConf" .}}

## Stream 配置检查
{{template "nginx.streamConf" .}}

## 动态参数检查
{{template "nginx.dynamic_parameters" .}}

## 详细错误日志
{{template "nginx.errlog" .}}


# 结束语
感谢贵司各位领导和技术人员对中亦科技的信任和对我们服务的配合，我们将倾心用力做好每一次服务来答谢您的信任和支持！如果您发现我们的服务还不尽完美，还请及时指正，我们将不断努力提升服务质量，全力以赴地为贵司业务的持续迅猛发展和信息科技的现代化建设保驾护航！

{{end}}
