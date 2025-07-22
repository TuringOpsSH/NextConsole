{{define "cpuLoad"}}
{{range .problems}}{{if eq .id "win.cpuLoad"}}

|                时间               |   cpu一分钟负载    |   cpu五分钟负载   |   cpu十五分钟负载    |                                    告警                                    |
|:-------------------------------:|:-------------:|:------------:|:--------------:|:------------------------------------------------------------------------:|
| {{range .mixraw}} {{.datetime}} | {{ .load1}}   | {{ .load5}}  | {{ .load15}}   | {{if eq  .mixlevel  "高风险"}}{{Icon "red"}}{{else}}{{Icon "green"}}{{end}} | 
{{end}}
{{end}}{{end}}

{{end}}