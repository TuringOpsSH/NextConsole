{{define "pg.extensions"}}
{{range $k, $v := .problems}}
{{if eq $v.id "extensions"}}
|数据库名称|Extension name|安装版本|默认版本|is old|
|:--|:--|:--|:--|:--|
|{{range $kk, $vv := $v.raw}}{{$vv.database}}|{{$vv.name}}|{{$vv.installed_version}}|{{$vv.default_version}}|{{$vv.is_old}}|
{{end}}
{{end}}
{{end}}
{{end}}