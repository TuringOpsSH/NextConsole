{{define "solution"}}

## 设备清单 

状态为绿色说明状态健康，为黄色表示需要关注，为红色表示需要重点关注处理。
{{ $syslist := JsCall "func.machinelist" .}}

|主机名|IP|操作系统|中间件|状态|
|:------:|:------:|:--------:|:-----:|:------:|
{{range $k,$v:= $syslist}}{{range $x,$y:=$v}}{{if $y}}|{{$y.hostname}}|{{$y.ip}}|{{$y.os}}|{{$y.midware}}|{{$y.status}}|
{{end}}{{end}}{{end}}


## 问题清单

### 系统信息
{{ $wlsdata := JsCall "func.sys" .}}
{{range $k,$v := $wlsdata.memnum}}
{{if $k}}
|IP|内存使用率|
|:------:|:------:|
|{{$k}}|{{$v}}|

{{end}}
{{end}}


{{range $k,$v := $wlsdata.cpunum}}
{{if $k}}
|IP|CPU使用率|
|:------:|:------:|
|{{$k}}|{{$v}}|

{{end}}
{{end}}

{{range $k,$v := $wlsdata.disknum}}
{{if $k}}
|IP|磁盘使用率|
|:------:|:------:|
|{{$k}}|{{$v}}|

{{end}}
{{end}}
### 中间件信息


#### Tomcat


#### Weblogic


#### Was



{{end}}