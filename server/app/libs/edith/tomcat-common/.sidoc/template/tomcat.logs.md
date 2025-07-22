{{define "tomcat.logs"}}
|`错误码`|`等级`|`次数`|`详情`|`时间`|
|:---|:---|:---|:---|:---|
{{range $k, $v := .problems}}{{if eq $v._scope "tomcat.logs"}}{{range $v.raw}}| {{.code}}| {{.level}}| {{.count}}| {{.detail}}| {{.time}}|
{{end}}{{end}}{{end}}{{end}}