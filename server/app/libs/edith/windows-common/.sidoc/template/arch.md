{{define "arch"}}
{{range .problems}}{{if eq .id "win.arch"}}

|       期望值       |      实际值       |                                                                                                                     告警 |
|:---------------:|:--------------:|-----------------------------------------------------------------------------------------------------------------------:|
| {{.expected}}   | {{ .actual  }} |  {{if eq  .level  "高风险"}}{{Icon "red"}}{{else if eq .mixlevel  "中风险"}}{{Icon "orange"}}{{else}}{{Icon "green"}}{{end}} |

{{end}}{{end}}
{{end}}