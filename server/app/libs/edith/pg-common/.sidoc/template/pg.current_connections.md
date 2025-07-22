{{define "pg.current_connections"}}
{{range $k, $v := .problems}}
{{if eq $v.id "current_connections"}}
|#| User | DB | Current state | Count | State changed >1m ago | State changed >1h ago | Tx age >1m | Tx age >1h|
|:--|:---|:---|:---|:--|:---|:---|:---|:---|
|{{range $kk, $vv := $v.raw}}{{$vv.num}}|{{$vv.user}}|{{$vv.database}}|{{$vv.current_state}}|{{$vv.count}}|{{$vv.state_changed_more_1m_ago}}|{{$vv.state_changed_more_1h_ago}}|{{$vv.tx_age_more_1m}}|{{$vv.tx_age_more_1h}}|
{{end}}
{{end}}
{{end}}
{{end}}