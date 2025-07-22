{{define "pg.heap_bloat"}}
{{range $k, $v := .problems}}
{{if eq $v.id "heap_bloat"}}
|#|Table|Real Size|Estimated bloat|Est. bloat, bytes|Est. bloat factor|Est. bloat level, %|Live Data Size|Last vacuum|Fillfactor|
|:--|:---|:---|:---|:--|:--|:--|:--|:--|:--|
||TOTAL|{{$v.raw.heap_bloat_total.real_size_bytes_sum}}|{{$v.raw.heap_bloat_total.bloat_size_bytes_sum}}|{{$v.raw.heap_bloat_total.extra_size_bytes_sum}}|{{$v.raw.heap_bloat_total.bloat_ratio_factor_avg}}|{{$v.raw.heap_bloat_total.bloat_ratio_percent_avg}}|{{$v.raw.heap_bloat_total.live_data_size_bytes_sum}}|||
|{{range $kk, $vv := $v.raw.heap_bloat}}{{$vv.num}}|{{$vv.table_name}}|{{$vv.real_size_bytes}}KiB|{{$vv.extra_size_bytes}}KiB|{{$vv.bloat_size_bytes}}|{{$vv.bloat_ratio_factor}}|{{$vv.bloat_ratio_percent}}|{{$vv.live_data_size_bytes}}||{{$vv.fillfactor}}|
{{end}}
{{end}}
{{end}}
{{end}}