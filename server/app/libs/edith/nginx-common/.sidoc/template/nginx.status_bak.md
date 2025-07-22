{{define "nginx.status_bak"}}
{{range $k, $v := .problems}}{{if eq $v._scope "nginx.status"}}

|Task|次数|
|:---|:---|
|`Reading`|{{$v.raw.Reading}}|
|`Waiting`|{{$v.raw.Waiting}}|
|`Writing`|{{$v.raw.Writing}}|
|`active_connections`|{{$v.raw.active_connections}}|
|`server_accepts`|{{$v.raw.server_accepts}}|
|`server_handled`|{{$v.raw.server_handled}}|
|`server_requests`|{{$v.raw.server_requests}}|
{{end}}
{{end}}
{{end}}