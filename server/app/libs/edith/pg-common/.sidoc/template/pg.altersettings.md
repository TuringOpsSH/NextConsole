{{define "pg.altersettings"}}
{{range $k, $v := .problems}}{{if eq $v.id "altersettings"}}

|修改文件|修改数量|修改内容|
|:--|:---|:---|
|{{$v.raw.res.sourcefile}}|{{$v.raw.res.count}}|{{$v.raw.res.examples}}|
|{{$v.raw.defaults.sourcefile}}|{{$v.raw.res.count}}|{{$v.raw.res.examples}}|
{{end}}
{{end}}
{{end}}