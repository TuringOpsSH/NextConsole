{{define "pg.autovacuum_resource_usage"}}
{{range $k, $v := .problems}}
{{if eq $v.id "autovacuum_resource_usage"}}
|Setting name|Value|Unit|
|:--|:---|:---|:---|
|{{range $kk, $vv := $v.raw}}{{$vv.name}}|{{$vv.setting}}|{{$vv.unit}}|
{{end}}
{{end}}
{{end}}
{{end}}