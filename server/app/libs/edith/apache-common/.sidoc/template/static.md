{{define "static"}}


| 检查 | 实际值 | 检查结果 |
|:---|:---|:---|
| 产品版本（Server Version） | {{range .problems}}{{if eq .id "apache.status.server_version"}}{{.raw.server_version}} | {{Icon "green"}}{{end}}{{end}} |
| 查看运行模式（Server Mpm） | {{range .problems}}{{if eq .id "apache.status.server_mpm"}}{{.raw.server_mpm}} | {{Icon "green"}}{{end}}{{end}} |
| 服务器时间（Current Time） | {{range .problems}}{{if eq .id "apache.status.current_time"}}{{.raw.current_time}} | {{Icon "green"}}{{end}}{{end}} |
| 上次重启时间（Restart Time） | {{range .problems}}{{if eq .id "apache.status.restart_time"}}{{.raw.restart_time}} | {{Icon "green"}}{{end}}{{end}} |
| 父进程重新启动次数（Parent Server Config. Generation） | {{range .problems}}{{if eq .id "apache.status.parent_server_config_generation"}}{{.raw.parent_server_config_generation}} | {{Icon "green"}}{{end}}{{end}} |
| 父服务器MPM生成（Parent Server Mpm Generation） | {{range .problems}}{{if eq .id "apache.status.parent_server_mpm_generation"}}{{.raw.parent_server_mpm_generation}} | {{Icon "green"}}{{end}}{{end}} |
| 服务器正常运行时间（Server Uptime） | {{range .problems}}{{if eq .id "apache.status.server_uptime"}}{{.raw.server_uptime}} | {{Icon "green"}}{{end}}{{end}} |

{{end}}
