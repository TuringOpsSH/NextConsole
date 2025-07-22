{{define "nginx.dynamic_parameters"}}
| 检查                                                                            | 实际值                                                                                                                         | 预期值                      |  说明                       |检查结果                           |
|:---------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|:-------------------------|:-------------------------------|:---------------------------|
| {{range  .problems}}{{if eq .id  "nginx.tcpstate.time_wait"}} {{.name}}          | {{.raw}}                                                           |无                         |-                  |{{Icon .level}}{{end}}{{end}} |
| {{range  .problems}}{{if eq .id  "nginx.tcpstate.established"}} {{.name}}       | {{.raw}}                                                  |无                          |-                  |{{Icon .level}}{{end}}{{end}}|
|客户端访问量统计检查（单日单用户超过500访问量）                                    |{{range $k, $v := .problems}}{{if eq $v._scope "gt500ip"}}{{range $v.raw}}IP: {{.ip}}&nbsp;Count: {{.count}} ;    {{end}}        |无                      | -                            |{{Icon $v.level}}{{end}}{{end}}|
|客户端访问量统计检查（单日访问量前十用户）                                           |{{range $k, $v := .problems}}{{if eq $v._scope "top10ip"}}{{range $v.raw}}IP: {{.ip}}&nbsp;Count: {{.count}} ;     {{end}}           |无                     |-                              |{{Icon $v.level}}{{end}}{{end}}|
| Nginx进程的CPU使用率                                               | {{range .problems}}{{if eq .id "nginx.status.cpuusage"}}{{.actual}}                                                               | {{.expected}}        |{{.desc}}  |{{Icon .level}}{{end}}{{end}} |
|{{range .problems}}{{if eq .id "nginx.gstat.waiting"}}{{.name}}       |{{.raw}}                                                                                                      |{{.expected}}   |{{.desc}}|{{Icon .level}}{{end}}{{end}}|
|{{range .problems}}{{if eq .id "nginx.gstat.reading"}}{{.name}}        |{{.raw}}                                                                                                     |{{.expected}}|{{.desc}}|{{Icon .level}}{{end}}{{end}}|
|{{range .problems}}{{if eq .id "nginx.gstat.server_handled"}}{{.name}} |{{.raw}}                                                                                                     |{{.expected}}|{{.desc}}|{{Icon .level}}{{end}}{{end}}|
|{{range .problems}}{{if eq .id "nginx.gstat.active_connections"}}{{.name}} |{{.raw}}                                                                                                   |{{.expected}}|{{.desc}}|{{Icon .level}}{{end}}{{end}}|
|{{range .problems}}{{if eq .id "nginx.gstat.server_requests"}}{{.name}}  |{{.raw}}                                                                                                     |{{.expected}}|{{.desc}}|{{Icon .level}}{{end}}{{end}}|
|{{range .problems}}{{if eq .id "nginx.gstat.server_accepts"}}{{.name}}  |{{.raw}}                 |{{.expected}}|{{.desc}}|{{Icon .level}}{{end}}{{end}}|
|{{range .problems}}{{if eq .id "nginx.gstat.writing"}}{{.name}}  |{{.raw}}                  |{{.expected}}|{{.desc}}|{{Icon .level}}{{end}}{{end}}|
|{{range .problems}}{{if eq .id "nginx.errlog"}}{{.name}} |   {{.actual}}   |{{.expected}}|{{.desc}}|{{Icon .level}}{{end}}{{end}}|
{{end}}

