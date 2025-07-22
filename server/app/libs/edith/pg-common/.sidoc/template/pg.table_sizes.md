{{define "pg.table_sizes"}}
{{range $k, $v := .problems}}
{{if eq $v.id "table_sizes"}}
|#|Table|Rows|Total size|Table size|Index(es) Size|
|:--|:---|:---|:---|:---|:---|
||TOTAL|{{$v.raw.tables_data_total.row_estimate_sum}}|{{$v.raw.tables_data_total.total_size_bytes_sum}}|{{$v.raw.tables_data_total.table_size_bytes_sum}}|{{$v.raw.tables_data_total.indexes_size_bytes_sum}}|
|{{range $kk, $vv := $v.raw.tables_data}}{{$vv.num}}|{{$vv.table}}|{{$vv.row_estimate}}|{{$vv.total_size_bytes}}({{$vv.total_size_percent}})|{{$vv.table_size_bytes}}({{$vv.table_size_percent}})|{{$vv.indexes_size_bytes}}|
{{end}}
{{end}}
{{end}}
{{end}}