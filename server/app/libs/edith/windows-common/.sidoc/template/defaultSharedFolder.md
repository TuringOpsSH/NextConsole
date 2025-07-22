{{define "defaultSharedFolder"}}
{{range .problems}}{{if eq .id "win.defaultSharedFolder"}}

|              共享名               |      状态       |     路径     |   
|:------------------------------:|:-------------:|-----------:|
| {{range .raw}} {{.ShareName}}  | {{ .Status}}  | {{ .Path}} |
{{end}}
{{end}}{{end}}

{{end}}