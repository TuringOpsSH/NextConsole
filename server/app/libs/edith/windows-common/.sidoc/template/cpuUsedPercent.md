{{define "cpuUsedPercent"}}
{{range .problems}}{{if eq .id "win.cpuUsedPercent"}}

|              时间              |       使用率        |                                    告警                                   |
|:----------------------------:|:----------------:|:-----------------------------------------------------------------------:|
| {{range .mixraw}}  {{.datetime}} | {{.metric}}{{"%"}} | {{if eq  .mixlevel  "高风险"}}{{Icon "red"}}{{else}}{{Icon "green"}}{{end}}|
{{end}}
{{end}}{{end}}

{{end}}