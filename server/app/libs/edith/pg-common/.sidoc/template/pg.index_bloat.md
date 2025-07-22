{{define "pg.index_bloat"}}
{{range $k, $v := .problems}}
{{if eq $v.id "index_bloat"}}
|#|Table|Index Size|Table Size|Estimated bloat|Est. bloat, bytes|Est. bloat factor|Est. bloat level, %|Live Data Size|Fillfactor|
|:--|:---|:---|:---|:--|:--|:--|:--|:--|:--|
||TOTAL|{{$v.raw.index_bloat_total.real_size_bytes_sum}}|{{$v.raw.index_bloat_total.table_size_bytes_sum}}|{{$v.raw.index_bloat_total.bloat_size_bytes_sum}}|{{$v.raw.index_bloat_total.bloat_size_bytes_sum}}|{{$v.raw.index_bloat_total.bloat_ratio_factor_avg}}|{{$v.raw.index_bloat_total.bloat_ratio_percent_avg}}|{{$v.raw.live_data_size_bytes_sum}}||
|{{range $kk, $vv := $v.raw.index_bloat}}{{$vv.num}}|{{$vv.index_table_name}}|{{$vv.real_size_bytes}}|{{$vv.table_size_bytes}}|{{$vv.extra_size_bytes}}|{{$vv.bloat_size_bytes}}|{{$vv.bloat_ratio_factor}}|{{$vv.extra_ratio_percent}}|{{$vv.live_data_size_bytes}}|{{$vv.fillfactor}}|
{{end}}
{{end}}
{{end}}
{{end}}