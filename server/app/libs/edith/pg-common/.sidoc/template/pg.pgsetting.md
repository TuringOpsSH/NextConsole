{{define "pg.pgsettings"}}
{{range $k, $v := .problems}}
{{if eq $v.id "pgsettings"}}
|Category|Setting|Value|Unit|
|:--|:---|:---|:---|
|{{range $kk, $vv := $v.raw}}{{$vv.category}}|{{$vv.name}}|{{$vv.setting}}|{{$vv.unit}}|
{{end}}{{end}}
{{end}}
{{end}}