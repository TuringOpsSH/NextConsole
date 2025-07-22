{{define "basicInfo"}}

|              |                                                                                                                                                     |
|:-------------|:----------------------------------------------------------------------------------------------------------------------------------------------------|
| `操作系统版本`     | {{range $k, $v := .problems}}{{if eq $v._scope "hostInfo"}}{{$v.raw.platform}} {{$v.raw.platformFamily}} {{$v.raw.platformVersion}} {{end}} {{end}} |
| `主机CPU`      | {{range $k, $v := .problems}}{{if eq $v._scope "basicInfo"}}{{$v.raw.CPUs}}核 {{end}} {{end}}                                                        |
| `主机内存`       | {{range $k, $v := .problems}}{{if eq $v._scope "basicInfo"}}{{$v.raw.TotalMemory}}  {{end}} {{end}}                                                 |
| `Tomcat版本`   | {{range $k, $v := .problems}}{{if eq $v._scope "tomcatConfs.versions"}}{{$v.raw.tomcatVersion}} {{end}} {{end}}                                     |
| `JVM版本`      | {{range $k, $v := .problems}}{{if eq $v._scope "tomcatConfs.versions"}}{{$v.raw.javaVersion}} {{end}} {{end}}                                       |
| `Tomcat安装路径` | {{range $k, $v := .problems}}{{if eq $v._scope "tomcat.flags"}}{{$v.raw.path}} {{end}} {{end}}                                                      |
| `监听端口`       | {{range $k, $v := .problems}}{{if eq $v._scope "tomcatConfs.serverConf"}}{{$v.raw.port}} {{end}} {{end}}                                            |                                                                                                                                            |

{{end}}