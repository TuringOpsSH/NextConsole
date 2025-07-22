{{define "main"}}

{{$problems := GroupBy .problems "id"}}
{{$summary := JsCall "func.summary" .problems}}
{{$appnames := .meta.config.appnames}}


---
title: {{.meta.customer}} {{.meta.title}}
subtitle: {{range .NginxConfs}}{{JsCall "func.appname" .host.hostname $appnames}}{{end}}
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
{{println ""}}实例名：{{range .NginxConfs}}{{if .edith}}{{.edith.flags.path}} {{end}}{{end}}
{{println ""}}巡检工程师：{{ .meta.author.name}}
{{println ""}}巡检时间：{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}

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
