{{define "ifServiceDisabled"}}
{{range .problems}}{{if eq .id "win.ifServiceDisabled"}}

|             服务              |       状态        |   
|:---------------------------:|:---------------:|
| {{range .mixraw}} {{.name}} | {{ .status}} |
{{end}}
{{end}}{{end}}

{{end}}