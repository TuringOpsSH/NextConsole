{{define "main"}}

{{template "meta" .}}
{{ $summary := JsCall "func.summary" .problems }}


# 巡检总结和建议

## 巡检信息概述
{{println ""}}主机名：{{range .SysConfs}}{{printf "%-13s" .host.hostname}}{{end}}
{{println ""}}操作系统版本：{{range .SysConfs}}{{printf .base.Distro}}{{end}}
{{println ""}}巡检人员：{{ .meta.author.name}}
{{println ""}}巡检时间：{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}

## 巡检告警定义
| 风险等级 | 颜色  | 标识                | 定义                                                    |
|:-----|:----|:------------------|:------------------------------------------------------|
| 高风险  | 红色  | {{Icon "red"}}    | 该告警可能会影响生产系统使用、系统稳定性或系统安全性，建议及时安排变更窗口处理。              |
| 中风险  | 橙色  | {{Icon "orange"}} | 该告警一般为不影响生产系统使用、非关键，我们会在汇总报告提供对应的最佳实践，建议在合适的变更窗口进行调整。 |
| 低风险  | 绿色  | {{Icon "green"}}  | 最佳实践，不需要关注。                                           |

## 巡检总结和建议表

此次巡检总计检查{{$summary.sum}}个关键项目，发现{{$summary.danger}}个高风险告警、{{$summary.warning}}个中风险告警。
{{ if $summary.iderr }} 
| 检查内容                                                                                                                | 预期值                  | 实际值             | 检查结果        | 建议              |
|:--------------------------------------------------------------------------------------------------------------------|:---------------------|:----------------|:------------|:----------------|
{{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "高风险"}}| {{$v.name}}//{{$id}} | {{$v.expected}} | {{.actual}} | {{Icon .level}} |{{$v.solution}}|
{{end}}{{end}}{{end}}{{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "中风险"}} | {{$v.name}}//{{$id}} | {{$v.expected}} | {{.actual}} | {{Icon .level}} |{{$v.solution}}|
{{end}}{{end}}{{end}}

{{end}}

## 操作系统基本配置
{{template "base" .}}

## 告警数量统计

（实例名为空表示操作系统检查）

| 主机名                                                   | 实例名           | 高风险告警数量               | 中风险告警数量 |
|:------------------------------------------------------|:--------------|:----------------------|:--------|
{{range $host, $v := $summary.hosterrcount}}| {{$host}} | {{$v.danger}} | {{$v.warning}} |
{{end}}
## 巡检总结和建议表

{{ if $summary.iderr }}
| 检查内容 | 主机名 | 实例名 | 预期值 | 实际值 | 检查结果 | 建议 |
|:---|:---|:---|:---|:---|:---|:---|
{{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "高风险"}}| {{$v.name}}//{{$id}} | {{.hostname}}|{{$v.expected}} | {{.actual}} | {{Icon .level}} | {{$v.solution}} |
{{end}}{{end}}{{end}}{{range $id, $v := $summary.iderr}}{{ range $kk, $vv := $v.hosterrlist}}{{if eq .level "中风险"}} | {{$v.name}}//{{$id}} | {{.hostname}}|{{$v.expected}} | {{.actual}} | {{Icon .level}} | {{$v.solution}} |
{{end}}{{end}}{{end}}

{{end}}

# 系统参数检查

## CPU负载
{{template "cpu" .}}

## 内存使用情况
{{template "mem" .}}

## 磁盘空间使用情况
{{template "disk" .}}

# Apache 检查

## 常规检查
{{template "static" .}}

## 动态参数项
{{template "dynamic" .}}

## 错误日志
{{template "errlog" .}}

{{end}}
