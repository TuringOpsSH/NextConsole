{{define "singleserver"}}

{{ $wlsproblems := JsCall "func.matchWlsMsg" .}}

{{if $wlsproblems}}
## Weblogic
{{end}}

{{range $k,$v := $wlsproblems}}
{{range $a,$b := $v.DomainName}}

|类别|参数|
|:---|:---|
|服务器编号/IP地址|{{$v.SysMsg.ip}}|
|操作系统|{{$v.SysMsg.os}}|
|CPU核心数|{{$v.SysMsg.cpus}}|
|内存大小|{{$v.SysMsg.mem}}|
|CPU使用率|{{$v.SysMsg.cpuused}}|
|内存使用率|{{$v.SysMsg.memused}}|
|磁盘使用率|{{$v.SysMsg.diskused}}|
|weblogic版本信息|{{$b.version}}|
|weblogic 补丁号|{{$b.patch}}|
|JDK版本|{{$b.jdk}}|
|weblogic安装目录|{{$b.oraclehome}}|
|weblogic域目录|{{$b.domainpath}}|
|server|{{$b.server}}|
|JDBC的数量	|{{$b.jdbc}}|
|JVM堆大小|{{$v.SysMsg.psArgs}}|
{{end}}
{{end}}

{{if $wlsproblems}}
## Tomcat
{{end}}

{{ $tomcatproblems := JsCall "func.matchTomcatMsg" .}}
{{range $k,$v := $tomcatproblems}}
{{if  $v.TomcatMsg }}
{{range $a,$b := $v.TomcatMsg}}
|类别|参数|
|:---|:---|
|服务器编号/IP地址|{{$v.SysMsg.ip}}|
|操作系统|{{$v.SysMsg.os}}|
|CPU核心数|{{$v.SysMsg.cpus}}|
|内存大小|{{$v.SysMsg.mem}}|
|CPU使用率|{{$v.SysMsg.cpuused}}|
|内存使用率|{{$v.SysMsg.memused}}|
|磁盘使用率|{{$v.SysMsg.diskused}}|
|tomcat版本信息|{{$b.version}}|
|JDK版本|{{$b.jdk}}|
|tomcat安装目录|{{$b.home}}|

{{end}}
{{end}}
{{end}}

{{end}}