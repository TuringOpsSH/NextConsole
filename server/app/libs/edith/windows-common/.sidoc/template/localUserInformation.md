{{define "whoExecutesTaskPlan"}}
{{range .problems}}{{if eq .id "win.whoExecutesTaskPlan"}}

|              任务名              |    用户     |   
|:-----------------------------:|:---------:|
| {{range .raw}}  {{.TaskName}} |{{.Users}} |
{{end}}{{end}}{{end}}
{{end}}