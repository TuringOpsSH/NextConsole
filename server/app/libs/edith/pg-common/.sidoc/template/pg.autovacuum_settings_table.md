{{define "pg.autovacuum_settings_table"}}
{{range $k, $v := .problems}}
{{if eq $v.id "autovacuum_settings_table"}}
|name|boot_val|category|context|enumvals|extra_desc|max_val|min_val|pending_restart|reset_val|setting|short_desc|source|sourcefile|sourceline|unit|vartype|
|:--|:---|:---|:---|:--|:---|:---|:---|:--|:---|:---|:---|:--|:---|:---|:---|:---|
|{{range $kk, $vv := $v.raw}}{{$vv.name}}|{{$vv.boot_val}}|{{$vv.category}}|{{$vv.context}}|{{$vv.enumvals}}|{{$vv.context}}|{{$vv.enumvals}}|{{$vv.extra_desc}}|{{$vv.max_val}}|{{$vv.min_val}}|{{$vv.pending_restart}}|{{$vv.reset_val}}|{{$vv.setting}}|{{$vv.short_desc}}|{{$vv.context}}|{{$vv.source}}|{{$vv.sourcefile}}|{{$vv.sourceline}}|{{$vv.unit}}|{{$vv.vartype}}|
{{end}}
{{end}}
{{end}}
{{end}}