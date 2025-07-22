{{define "nginx.locationConf"}}
| 检查                                     | 实际值                                                                                             | 预期值                      | 检查结果                              |
|:------------------------------------------|:--------------------------------------------------------------------------------------------------|:-------------------------|:----------------------------------|
| 目录穿透                                  | {{range .problems}}{{if eq .id "nginx.pconf.through_directory"}}{{.raw.through_directory}}           | false                | {{Icon .level}}{{end}}{{end}}    |
|proxy_pass指令后禁止直接使用域名进行转发     | {{range .problems}}{{if eq .id "nginx.pconf.proxy_pass"}}{{.raw.proxy_pass}}                           | false                    | {{Icon .level}}{{end}}{{end}} |
{{end}}
