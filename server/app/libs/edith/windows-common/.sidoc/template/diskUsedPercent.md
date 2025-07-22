{{define "diskUsedPercent"}}
{{range .problems}}{{if eq .id "win.diskUsedPercent"}}

|        磁盘                   |      空间      |     剩余空间      |     使用率     |                                                                        告警                                                |
|:---------------------------:|:------------:|:-------------:|:-----------------:|:------------------------------------------------------------------------------------------------------------------------:|
| {{range .mixraw}} {{.path}} | {{ .total}}  | {{ .free}}    | {{ .usedPercent}} | {{if eq  .mixlevel  "高风险"}}{{Icon "red"}}{{else if eq .mixlevel  "中风险"}}{{Icon "orange"}}{{else}}{{Icon "green"}}{{end}} |
{{end}}
{{end}}{{end}}

{{end}}