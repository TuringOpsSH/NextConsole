{{define "pg.cluster_info"}}
{{range $k, $v := .problems}}
{{if eq $v.id "cluster_info"}}

### 数据库大小
|数据库名称|大小|
|:--|:---|
|{{range $kk, $vv := $v.raw.database_sizes}}{{$vv.name}}|{{$vv.size}}MiB|
{{end}}

### Observations
|名称|值|
|:--|:---|
|{{range $kk, $vv := $v.raw.general_info}}{{$vv.metric}}|{{$vv.value}}|
{{end}}

{{end}}
{{end}}
{{end}}