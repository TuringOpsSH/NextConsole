{{define "gc"}}

{{range .WlsLogs}}
{{$sidataFilePath := .sidataFilePath}}
{{range .WlsLog}}
## {{ .server}}

### 基本信息

{{if .gclogs.err }}
    {{printf "获取 gc 日志时异常。请查看是否设置的生成 gc 日志的启动参数 且 gc 日志名称是否标准"}}
{{else}}

{{with .gclogs.stat}}
时间范围:
 ~ {{printf "%-36s" .start}} -- {{printf "%-36s" .end}}

Heap空闲趋势:
 ~ {{printf "%0.0f" .firstFree}} -- {{printf "%0.0f" .lastFree}}

垃圾回收次数:
 ~ {{.count}}

单次垃圾回收字节数:
 ~ {{printf "%0.0f" .average}}

垃圾回收时间占比:
 ~ {{.gcTime}}({{printf "%g" .gcTimePercent}})

堆达到最大值:
 ~ {{printf "%0.0f" .maxTotal}}

虚拟机重启次数:
 ~ {{len .vms}}
{{end}}


### 垃圾回收图

{{if .gclogs}}
![Gc Log]({{RelativePath $sidataFilePath .gclogs.gcChartPath}})

{{end}}
    
{{end}}
{{end}}
{{end}}

{{end}}