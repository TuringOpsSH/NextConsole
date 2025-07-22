{{define "cpu"}}

### CPU使用率数据
|时间|CPU使用率|检查结果|
|:---:|:---:|:---:|
{{range .problems}}{{if eq .id "linux.cpuUsedPercent"}}|{{printf "%-24s" .datetime}}|{{ if .metric }}{{.metric}}%  {{else}} 0% {{end}}|{{if eq .level "正常"}}{{Icon "green"}}{{else}}{{Icon "red"}}{{end}}|
{{end}}{{end}}

{{end}}
