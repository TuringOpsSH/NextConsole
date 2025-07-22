{{define "pg.timeouts_locks"}}
{{range $k, $v := .problems}}
{{if eq $v.id "timeouts_locks"}}
### Timeouts
|Setting name|Value|Unit|
|:--|:---|:---|
|{{range $kk, $vv := $v.raw.timeouts}}{{$vv.name}}|{{$vv.setting}}|{{$vv.unit}}|
{{end}}

### Locks
|Setting name|Value|Unit|
|:--|:---|:---|
|{{range $kk, $vv := $v.raw.locks}}{{$vv.name}}|{{$vv.setting}}|{{$vv.unit}}|
{{end}}

### Databases data
|#|Database|Conflicts|Deadlocks|Stats reset at|Stat reset|
|:--|:---|:---|:---|:---|:---|
|{{range $kk, $vv := $v.raw.databases_stat}}{{$vv.num}}|{{$vv.datname}}|{{$vv.conflicts}}|{{$vv.deadlocks}}|{{$vv.stats_reset}}|todo|
{{end}}

{{end}}
{{end}}
{{end}}