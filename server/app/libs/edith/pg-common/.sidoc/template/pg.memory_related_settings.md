{{define "pg.memory_related_settings"}}
{{range $k, $v := .problems}}
{{if eq $v.id "memory_related_settings"}}
|Setting name|Value|Unit|
|:--|:---|:---|
|{{range $kk, $vv := $v.raw}}{{$vv.name}}|{{$vv.setting}}|{{$vv.unit}}|
{{end}}
{{end}}
{{end}}
{{end}}