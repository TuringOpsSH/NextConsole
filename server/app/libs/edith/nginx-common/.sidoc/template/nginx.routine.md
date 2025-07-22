{{define "nginx.routine"}}
|检查|实际值|
|:---|:---|
|产品版本|{{range $k, $v := .problems}}{{if eq $v._scope "nginx.gversion"}}{{$v.raw}}{{end}}{{end}}|
|编译列表|{{range $k, $v := .problems}}{{if eq $v._scope "nginx.confargs"}}{{$v.raw}}{{end}}{{end}}|
{{end}}