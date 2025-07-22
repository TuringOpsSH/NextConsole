{{define "errlog"}}

{{range $k, $v := .problems}}{{if eq $v._scope "errlog"}}
{{if .raw}}
|错误代码|
|:---|
{{range $kk, $vv := $v.raw}}|{{$vv}}|{{end}}
{{else}}
当前日志文件状态正常，未发现含有错误信息的日志。
{{end}}{{end}}
{{end}}
{{end}}
