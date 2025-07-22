{{define "tomcat.webConf"}} {{range $k, $v := .problems}}{{if eq $v._scope "tomcatConfs.webConf"}}

| `配置项` | `值` |
|:-------------|:--------------------------|
| `version` |    {{$v.raw.version}}   |
| `xmlns`   |    {{$v.raw.xmlns}}   |
| `xsi`   |    {{$v.raw.xsi}}   |

{{end}} {{end}} {{end}}