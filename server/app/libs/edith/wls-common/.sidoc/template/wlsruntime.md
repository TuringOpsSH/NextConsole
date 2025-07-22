{{define "wlsruntime"}}

## Server 运行状态

| server | RunTime | 状态 | 建议 |
| :------: | :--------: | :--------: | :--------: |
{{range .problems}}{{if eq .id "wls.serverRuntime"}}| {{._name}} | {{.startupMode}} | {{if eq .startupMode "RUNNING"}}{{Icon "green"}}{{else}}{{Icon "red"}}{{end}} | {{.solution}} |
{{end}}{{end}}


## JVM 性能

{{range .WlsStatus}}{{range .servers}}

{{if .JVMRuntime }}

### {{.Name}}

{{LineChart .JVMRuntime "" "//*/datetime" "//*/HeapFreeCurrent;//*/HeapSizeCurrent;//*/HeapUsedCurrent"}}

{{end}}

{{end}}{{end}}


## 线程池性能

{{range .WlsStatus}}{{range .servers}}

{{if .ThreadPoolRuntime}}

### {{.Name}}

{{LineChart .ThreadPoolRuntime "" "//*/datetime" "//*/CompletedRequestCount;//*/ExecuteThreadIdleCount;//*/ExecuteThreadTotalCount;//*/PendingUserRequestCount"}}

{{end}}

{{end}}{{end}}


## JDBC连接池性能

{{range .WlsStatus}}{{range .servers}}

{{if .JDBCDataSourceRuntime }}

### {{.Name}}

{{$jdbcs := GroupBy .JDBCDataSourceRuntime "jsonpath:metric/jdbcName"}}{{ range $key, $values := $jdbcs}}

#### {{$key}}

{{LineChart $values "" "//*/datetime" "//*/ActiveConnectionsCurrentCount;//*/ConnectionsTotalCount;//*/HighestNumAvailable;//*/NumAvailable;//*/WaitingForConnectionTotal"}}


{{end}}

{{end}}

{{end}}{{end}}




{{end}}