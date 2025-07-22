{{define "pg.autovacuum_dead_tuples"}}
{{range $k, $v := .problems}}{{if eq $v.id "autovacuum_dead_tuples"}}

|database_stat_age|database_stat_reset|dead_tuples|overridden_settings_count|
|:--|:---|:---|:---|
|{{$v.raw.database_stat.stats_age}}|{{$v.raw.database_stat.stats_reset}}|{{$v.raw.dead_tuples}}|{{$v.raw.overridden_settings_count}}|
{{end}}{{end}}
{{end}}