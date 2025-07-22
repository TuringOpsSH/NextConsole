{{define "nginx.errlog"}}
{{range $k, $v := .problems}}{{if eq $v._scope "nginx.errlog"}}
{{$v.raw}}
{{end}}
{{end}}
{{end}}