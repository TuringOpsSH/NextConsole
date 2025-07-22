{{define "pg.autovacuum_wraparound"}}
{{range $k, $v := .problems}}
{{if eq $v.id "autovacuum_wraparound"}}
### Databases
|Database|Age|Capacity used, %|Warning|datfrozenxid|
|:--|:---|:---|:---|:--|
|{{range $kk, $vv := $v.raw.per_instance}}{{$vv.datname}}|{{$vv.age}}|{{$vv.capacity_used}}|{{$vv.warning}}|{{$vv.datfrozenxid}}|
{{end}}

### Tables in the observed database
|Relation|Age|Capacity used, %|Warning|rel_relfrozenxid|toast_relfrozenxid|
|:--|:---|:---|:---|:--|:---|
|{{range $kk, $vv := $v.raw.per_instance}}{{$vv.datname}}|{{$vv.age}}|{{$vv.capacity_used}}|{{$vv.warning}}|{{$vv.datfrozenxid}}|todo|
{{end}}
{{end}}
{{end}}
{{end}}