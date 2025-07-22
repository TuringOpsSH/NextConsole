{{define "tomcat.versions"}} {{range $k, $v := .problems}}{{if eq $v._scope "tomcatConfs.versions"}}

| `配置项` | `值` |
|:-------------|:--------------------------|
| `java` |    {{$v.raw.javaVersion}}   |
| `tomcat`   |    {{$v.raw.tomcatVersion}}   |

{{end}} {{end}} {{end}}