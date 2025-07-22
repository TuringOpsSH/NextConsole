{{define "main"}}

{{$smy := JsCall "func.summary" .problems}}
{{$appnames := .meta.config.appnames}}

---
title: {{.meta.customer}} {{.meta.title}}
subtitle: 
author:
    - 巡检工程师：{{ .meta.author.name}}
    - {{ .meta.org}} 

date: {{if .meta.date}}{{.meta.date}}{{else}}{{$smy.date}}{{end}}
---

{{if eq $smy.show_document_version_information "yes"}}
# 文档版本信息

|版本|日期|作者|说明&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}|{{ .meta.author.name}} |初稿|
|||||

{{end}}

{{if eq $smy.show_summary_of_check "yes"}}
# 巡检结果汇总

本次巡检检查了{{$smy.hostArrCount}} 台主机{{if eq $smy.group "instance"}}（{{$smy.instArrCount}}个实例）{{end}}共 {{$smy.sum}} 个指标，其中发现 {{$smy.danger}} 个高风险、{{$smy.warning}} 个中风险、{{$smy.green}} 个低风险， 其余{{$smy.ok}} 个正常。
告警定义如下：

|风险等级|颜色|标识|定义|
|:---|:---|:---|:---|
|高风险|红色|{{Icon "red"}}|经检查发现的最高级别告警，告警级别基于工程师从问题严重性、时间紧迫性、影响范围等方面的判断，建议及时进行处理。|
|中风险|橙色|{{Icon "orange"}}|经检查发现的中等级别告警，一般为仍然处在发展变化过程中且尚未转化为高风险告警的问题，建议关注问题发展趋势，结合实际情况进行处理。|
|低风险|绿色|{{Icon "green"}}|包括经检查未发现问题的，或虽然存在问题但一般情况下影响可以忽略的告警。此外，对于最佳实践方面的检查结果也归为此类。|

{{end}}


{{if eq $smy.show_important_and_handling_plan "yes"}}
# 重要告警及处理计划

下表为重要告警及处理进度。如为“待服务台安排人员处理”，后续项目经理会跟踪直到解决，如状态为“等客户通知再处理”，还请您密切关注，发现问题及时联系项目经理安排处理。

涉及IP地址|异常问题|{{if eq $smy.group "instance"}}实例名|{{end}}处理建议|处理进度（已现场处理/客户自行处理/待服务台安排人员处理/等客户通知再处理）|备注|
|:---|:---|:---|:---|:---|{{if eq $smy.group "instance"}}:---|{{end}}
||||||{{if ne $smy.group "instance"}}:---|{{end}}

{{end}}



# 巡检告警详情汇总

{{if eq $smy.show_count_of_risks "yes"}}
## 告警数量统计

按主机{{if eq $smy.group "instance"}}及实例{{end}}进行的统计结果列表如下：

|主机名|{{if eq $smy.group "instance"}}实例名|{{end}}高风险告警数量|中风险告警数量|低风险告警数量|{{if eq $smy.show_count_of_risks_with_score "yes"}}健康度|{{end}}
|:---|:---|:---|:---|{{if eq $smy.group "instance"}}:---|{{end}}{{if eq $smy.show_count_of_risks_with_score "yes"}}:---|{{end}}
{{range $host, $v := $smy.sumByHostInst}}|{{$host}} | {{$v.danger}} | {{$v.warning}} | {{$v.green}} |{{if eq $smy.show_count_of_risks_with_score "yes"}}{{$v.score}}|{{end}}
{{end}}

{{end}}

{{if eq $smy.show_count_of_risks_orderby_score "yes"}}
## 告警数量统计

按主机{{if eq $smy.group "instance"}}及实例{{end}}进行的统计结果列表如下：

|主机名|{{if eq $smy.group "instance"}}实例名|{{end}}高风险告警数量|中风险告警数量|低风险告警数量|{{if eq $smy.show_count_of_risks_with_score "yes"}}健康度|{{end}}
|:---|:---|:---|:---|{{if eq $smy.group "instance"}}:---|{{end}}{{if eq $smy.show_count_of_risks_with_score "yes"}}:---|{{end}}
{{range $smy.sumByHostInstSorted}}|{{.hostInst}} | {{.danger}} | {{.warning}} | {{.green}} |{{if eq $smy.show_count_of_risks_with_score "yes"}}{{.score}}|{{end}}
{{end}}

{{end}}

{{if eq $smy.show_piechart "yes"}}
## 告警数量统计图

{{PieChart "告警数量统计" $smy.pieChart}}

{{end}}

## 风险及建议列表

{{if eq $smy.show_list_of_risks_danger "yes"}}
### 高风险

|应用系统|检查内容|主机名|{{if eq $smy.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $smy.group "instance"}}:---|{{end}}
{{range $id, $v := $smy.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "高风险"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{$v.solution}}|
{{end}}{{end}}{{end}}

{{end}}

{{if eq $smy.show_list_of_risks_warning "yes"}}
### 中风险

|应用系统|检查内容|主机名|{{if eq $smy.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $smy.group "instance"}}:---|{{end}}
{{range $id, $v := $smy.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "中风险"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{$v.solution}}|
{{end}}{{end}}{{end}}

{{end}}

{{if eq $smy.show_list_of_risks_green "yes"}}
### 低风险

|应用系统|检查内容|主机名|{{if eq $smy.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $smy.group "instance"}}:---|{{end}}
{{range $id, $v := $smy.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "低风险"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{$v.solution}}|
{{end}}{{end}}{{end}}

{{end}}

{{if eq $smy.show_list_of_risks_ok "yes"}}
### 正常

|应用系统|检查内容|主机名|{{if eq $smy.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $smy.group "instance"}}:---|{{end}}
{{range $id, $v := $smy.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "正常"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{$v.solution}}|
{{end}}{{end}}{{end}}

{{end}}



{{if eq $smy.show_list_of_risks_group_by_category "yes"}}
# 风险及建议（按告警分类）

{{range $order, $category := $smy.show_list_of_risks_group_by_category_order}}
## {{$category}}

{{range $id, $v := $smy.sumById}}{{if $v.level}}{{if ne $v.level "正常"}}{{if $v.category}}
{{if eq $v.category $category }}
### {{$v.name}}【{{$v.level}}】
预期值：{{.expected}}
受影响主机及实际值：

|主机名|{{if eq $smy.group "instance"}}实例名|{{end}}实际值|
|:---|:---|{{if eq $smy.group "instance"}}:---|{{end}}
{{range $v.hostInstErrArr}}{{if ne .level "正常"}}|{{.hostInst}}|{{.actual}}|
{{end}}{{end}}

{{end}}{{end}}{{end}}{{end}}{{end}}

{{end}}
{{end}}

{{if eq $smy.show_check_item_list "yes"}}
# 检查项列表

|巡检项名称|巡检项名称|
|:---|:---|
{{range $smy.nameArr2col}}|{{.}}|
{{end}}

{{end}}

{{template "extend"}}
{{end}}