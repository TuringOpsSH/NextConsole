{{define "nginx.gt500ip"}}
{{range $k, $v := .problems}}{{if eq $v._scope "gt500ip"}}

|IP|访问次数|
|:---|:---|
{{range $kk, $vv := $v.raw}}|{{$vv.ip}}|{{$vv.count}}|
{{end}}{{end}}
{{end}}
{{end}}