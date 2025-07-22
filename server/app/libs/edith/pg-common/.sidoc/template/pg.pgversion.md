{{define "pg.pgversion"}}
{{range $k, $v := .problems}}{{if eq $v.id "pgversion"}}

| 名称                 | 值                                                       |
|:-------------------|:--------------------------------------------------------|
| server_major_ver   | {{.raw.server_major_ver}} |
| server_minor_ver   | {{.raw.server_minor_ver}}                               | 
| server_version_num | {{.raw.server_version_num}}                             | 
| version            | {{.raw.version}}                         |
{{end}}{{end}}
{{end}}
