{{define "main"}}

{{$summary := JsCall "func.summary" .problems}}
{{$appnames := .meta.config.appnames}}

---
title: {{.meta.customer}} {{.meta.title}}
subtitle:
author:
    - 巡检工程师：{{ .meta.author.name}}
    - {{ .meta.org}} 

date: {{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}
---




{{if eq $summary.show_document_version_information "yes"}}
# 文档版本信息

|版本&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|日期&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|作者&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|说明&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}|{{ .meta.author.name}} |初稿|
|||||

{{end}}

{{if eq $summary.show_summary_of_check "yes"}}
# 巡检结果汇总

本次巡检检查了{{$summary.hostArrCount}} 台主机{{if eq $summary.group "instance"}}（{{$summary.instArrCount}}个实例）{{end}}共 {{$summary.sum}} 个指标，其中发现 {{$summary.danger}} 个高风险、{{$summary.warning}} 个中风险、{{$summary.green}} 个低风险， 其余{{$summary.ok}} 个正常。
告警定义如下：

|风险等级|颜色|标识|定义|
|:---|:---|:---|:---|
|高风险|红色|{{Icon "red"}}|经检查发现的最高级别告警，告警级别基于工程师从问题严重性、时间紧迫性、影响范围等方面的判断，建议及时进行处理。|
|中风险|橙色|{{Icon "orange"}}|经检查发现的中等级别告警，一般为仍然处在发展变化过程中且尚未转化为高风险告警的问题，建议关注问题发展趋势，结合实际情况进行处理。|
|低风险|绿色|{{Icon "green"}}|包括经检查未发现问题的，或虽然存在问题但一般情况下影响可以忽略的告警。此外，对于最佳实践方面的检查结果也归为此类。|

{{end}}

{{if eq $summary.show_important_and_handling_plan "yes"}}
# 重要告警及处理计划

下表为重要告警及处理进度。如为“待服务台安排人员处理”，后续项目经理会跟踪直到解决，如状态为“等客户通知再处理”，还请您密切关注，发现问题及时联系项目经理安排处理。

涉及IP地址|异常问题|{{if eq $summary.group "instance"}}实例名|{{end}}处理建议|处理进度（已现场处理/客户自行处理/待服务台安排人员处理/等客户通知再处理）|备注|
|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
||||||{{if ne $summary.group "instance"}}:---|{{end}}

{{end}}


# 巡检告警详情汇总

{{if eq $summary.show_count_of_risks "yes"}}
## 告警数量统计

按主机{{if eq $summary.group "instance"}}及实例{{end}}进行的统计结果列表如下：

|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}高风险告警数量|中风险告警数量|低风险告警数量|{{if eq $summary.show_count_of_risks_with_score "yes"}}健康度|{{end}}
|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}{{if eq $summary.show_count_of_risks_with_score "yes"}}:---|{{end}}
{{range $host, $v := $summary.sumByHostInst}}|{{$host}} | {{$v.danger}} | {{$v.warning}} | {{$v.green}} |{{if eq $summary.show_count_of_risks_with_score "yes"}}{{$v.score}}|{{end}}
{{end}}

{{end}}

{{if eq $summary.show_count_of_risks_orderby_score "yes"}}
## 告警数量统计

按主机{{if eq $summary.group "instance"}}及实例{{end}}进行的统计结果列表如下：

|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}高风险告警数量|中风险告警数量|低风险告警数量|{{if eq $summary.show_count_of_risks_with_score "yes"}}健康度|{{end}}
|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}{{if eq $summary.show_count_of_risks_with_score "yes"}}:---|{{end}}
{{range $summary.sumByHostInstSorted}}|{{.hostInst}} | {{.danger}} | {{.warning}} | {{.green}} |{{if eq $summary.show_count_of_risks_with_score "yes"}}{{.score}}|{{end}}
{{end}}

{{end}}

{{if eq $summary.show_piechart "yes"}}
## 告警数量统计图

{{PieChart "告警数量统计" $summary.pieChart}}

{{end}}

## 风险及建议列表

{{if eq $summary.show_list_of_risks_danger "yes"}}
### 高风险

|检查内容|主机名|{{if eq $summary.group "instance"}}端口号|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "高风险"}}|{{$v.name}}|{{.pName}}{{if ne .ip ""}} \[{{.ip}}\]{{end}}{{if eq $summary.group "instance"}}|{{.pSid}}{{end}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

{{end}}

{{if eq $summary.show_list_of_risks_warning "yes"}}
### 中风险

|检查内容|主机名|{{if eq $summary.group "instance"}}端口号|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "中风险"}}|{{$v.name}}|{{.pName}}{{if ne .ip ""}} \[{{.ip}}\]{{end}}{{if eq $summary.group "instance"}}|{{.pSid}}{{end}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

{{end}}

{{if eq $summary.show_list_of_risks_green "yes"}}
### 低风险

|检查内容|主机名|{{if eq $summary.group "instance"}}端口号|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "低风险"}}|{{$v.name}}|{{.pName}}{{if ne .ip ""}} \[{{.ip}}\]{{end}}{{if eq $summary.group "instance"}}|{{.pSid}}{{end}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

{{end}}

{{if eq $summary.show_list_of_risks_ok "yes"}}
### 正常

|应用系统|检查内容|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "正常"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

{{end}}

{{if eq $summary.show_list_of_risks_group_by_category "yes"}}
# 风险及建议（按告警分类）

## 高风险
{{ range $k, $v := $summary.problems }}{{if eq $v.level "高风险"}}
### **受影响主机**：{{$v._name}}；**端口号**：{{$v._sid}}

**预期值**：{{$v.expected}}

**影响**：{{$v.effect}}

{{if $v.solution}}**建议**：{{$v.solution}} {{end}}

实际值：
{{range $kk, $vv := .mixraw}}
{{JsCall "func.simpleTable" $vv "*" "*"}}
{{end}}
{{end}}{{end}}

## 中风险
{{ range $k, $v := $summary.problems }}{{if eq $v.level "中风险"}}
### **受影响主机**：{{$v._name}}；**端口号**：{{$v._sid}}；**巡检内容**：{{$v.name}}

**预期值**：{{$v.expected}}

**影响**：{{$v.effect}}

{{if $v.solution}}**建议**：{{$v.solution}} {{end}}

实际值：
{{range $kk, $vv := .mixraw}}
{{JsCall "func.simpleTable" $vv "*" "*"}}
{{end}}
{{end}}{{end}}

## 低风险
{{ range $k, $v := $summary.problems }}{{if eq $v.level "中风险"}}
### **受影响主机**：{{$v._name}}；**端口号**：{{$v._sid}}

**预期值**：{{$v.expected}}

**影响**：{{$v.effect}}

{{if $v.solution}}**建议**：{{$v.solution}} {{end}}

实际值：
{{range $kk, $vv := .mixraw}}
{{JsCall "func.simpleTable" $vv "*" "*"}}
{{end}}
{{end}}{{end}}


{{range $order, $category := $summary.show_list_of_risks_group_by_category_order}}
## {{$category}}

{{range $id, $v := $summary.sumById}}{{if $v.level}}{{if ne $v.level "正常"}}{{if $v.category}}


{{if eq $v.category $category }}
### {{$v.name}}【{{$v.level}}】
预期值：{{.expected}}
受影响主机及实际值：

|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}实际值|
|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $v.hostInstErrArr}}{{if ne .level "正常"}}|{{.hostInst}}|{{.actual}}|
{{end}}{{end}}

{{end}}{{end}}{{end}}{{end}}{{end}}

{{end}}
{{end}}

{{if eq $summary.show_check_item_list "yes"}}
# 检查项列表

|巡检项名称|巡检项名称|
|:---|:---|
{{range $summary.nameArr2col}}|{{.}}|
{{end}}

{{end}}
{{end}}
