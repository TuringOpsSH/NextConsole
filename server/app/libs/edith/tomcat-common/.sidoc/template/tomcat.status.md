{{define "tomcat.status"}} {{range $k, $v := .problems}}{{if eq $v._scope "tomcat.status"}}

| `配置项`          | `值`                 |
|:---------------|:--------------------|
| `tomcat运行状态`   | {{$v.raw.gcLogState}}  |
| `GC日志是否产生`     | {{$v.raw.heapDumpState}} |
| `HeapDump是否产生` | {{$v.raw.runningState}} |
{{end}} {{end}}
{{end}}