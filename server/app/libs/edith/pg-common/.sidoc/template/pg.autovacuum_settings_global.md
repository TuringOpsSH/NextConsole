{{define "pg.autovacuum_settings_global"}}
{{range $k, $v := .problems}}
{{if eq $v.id "autovacuum_settings_global"}}
|Setting name|Value|Unit|
|:--|:---|:---|
|{{range $kk, $vv := $v.raw}}{{$vv.name}}|{{$vv.setting}}|{{$vv.unit}}|
{{end}}
{{end}}
{{end}}
{{end}}