{{define "localUserInformation"}}
{{range .problems}}{{if eq .id "win.localUserInformation"}}

|              账户               |     内容     |   
|:-----------------------------:|:----------:|
| {{range .raw}}  {{.account}} | {{.content}} |
{{end}}{{end}}{{end}}
{{end}}