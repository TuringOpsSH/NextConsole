{{define "dynamic"}}

| 检查项 | 实际值 | 预期值 | 说明 | 检查结果 |
|:---|:---|:---|:---|:---|
| 非正常页面检查 | {{range .problems}}{{if eq .id "apache.status.errreq"}}{{range .raw}}Code: {{.code}}, Count: {{.count}};{{end}}{{end}}{{end}} | 非正常的请求数在50以下 | 除状态码为200的其他请求 | {{range .problems}}{{if eq .id "apache.status.errreq"}}{{Icon .level}}{{end}}{{end}} |
| 客户端访问量检查 | {{range .problems}}{{if eq .id "apache.status.top10ip"}}{{range .raw}}IP: {{.ip}}, Count: {{.count}};<br>{{end}}{{end}}{{end}} | - | 列出访问httpd服务前10的客户端IP和访问次数 | - |
| 异常客户访问检查 | {{range .problems}}{{if eq .id "apache.status.gt500ip"}}{{if .raw}}{{range .mixraw}} IP: {{.ip}}&nbsp;Count: {{.count}};&nbsp;<br>{{end}}{{else}}无{{end}}{{end}}{{end}} | 单个IP访问数在500以下 | - | {{range .problems}}{{if eq .id "apache.status.gt500ip"}}{{Icon .level}}{{end}}{{end}} |
| 服务进程状态检查 | {{range .problems}}{{if eq .id "apache.status.process"}}{{.raw}}{{end}}{{end}} | 不存在Z进程 | Z进程查找 | {{range .problems}}{{if eq .id "apache.status.process"}}{{Icon .level}}{{end}}{{end}} |
| 服务监听状态检查 | {{range .problems}}{{if eq .id "apache.pstatus.network"}}{{if .network_info}}IP Port: {{.raw.ipport}};<br>Process: {{.raw.process}};<br>Status: {{.raw.status}};<br>{{else}}{{.actual}}{{end}}{{end}}{{end}} | 存在监听端口 | 端口是否在监听 | {{range .problems}}{{if eq .id "apache.pstatus.network"}}{{Icon .level}}{{end}}{{end}} |
| Apache进程CPU使用率 | {{range .problems}}{{if eq .id "apache.status.cpu_load"}}{{.raw.cpu_load}}{{end}}{{end}} | CPU占用率在70%以下 | Apache进程所使用的CPU | {{range .problems}}{{if eq .id "apache.status.cpu_load"}}{{Icon .level}}{{end}}{{end}} |
| 当前正在处理请求数（Requests currently being processed） | {{range .problems}}{{if eq .id "apache.status.requests_currently_being_processed"}}{{.raw.requests_currently_being_processed}}{{end}}{{end}} | 当前正在处理的请求数在200以下 | - | {{range .problems}}{{if eq .id "apache.status.requests_currently_being_processed"}}{{Icon .level}}{{end}}{{end}} |
| 空闲的活动（Idle workers） | {{range .problems}}{{if eq .id "apache.status.idle_workers"}}{{.raw.idle_workers}}{{end}}{{end}} | 空闲的活动数要超过50 | - | {{range .problems}}{{if eq .id "apache.status.idle_workers"}}{{Icon .level}}{{end}}{{end}} |
| 总访问量（Total accesses） | {{range .problems}}{{if eq .id "apache.status.total_accesses"}}{{.raw.total_accesses}}{{end}}{{end}} | - | - | - |
| 总流量（Total Traffic） | {{range .problems}}{{if eq .id "apache.status.total_traffic"}}{{.raw.total_traffic}}{{end}}{{end}} | - | - | - |
| 总持续时间（Total Duration） | {{range .problems}}{{if eq .id "apache.status.total_duration"}}{{.raw.total_duration}}{{end}}{{end}} | - | - | - |
| 正常运行时间（requests/sec，请求/秒） | {{range .problems}}{{if eq .id "apache.status.requests_per_sec"}}{{.raw.requests_per_sec}}{{end}}{{end}} | - | - | - |
| 正常运行时间（B/second，字节/秒） | {{range .problems}}{{if eq .id "apache.status.b_per_second"}}{{if .raw.b_per_second}}{{.raw.b_per_second}} {{else}} {{end}}{{end}}{{end}} | - | - | - |
| 正常运行时间（ms/request，毫秒/请求） | {{range .problems}}{{if eq .id "apache.status.ms_per_request"}}{{if .raw.ms_per_request}}{{.raw.ms_per_request}} {{else}} {{end}}{{end}}{{end}} | - | - | - |

{{end}}
