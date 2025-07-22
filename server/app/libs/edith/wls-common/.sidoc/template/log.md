{{define "log"}}

{{range .WlsLogs}}{{range .WlsLog}}## {{.server}}

{{ $first := JsCall "func.first" .logs }}
{{ $first.code  }}


{{range .logs}}

### {{.code}} {{.level}} ({{.count}}次)

Module
 ~ {{ .module}}

Origin File
 ~ {{ .origin}}

Time
 ~ {{ .time}}

ErrorCode
 ~ {{ .code}}

{{if .msg}}Message
 ~ {{ .msg}}{{end}}

{{if ._check.results}}{{$v1 := index ._check.results 0}}问题（{{$v1.level}}）
 ~ {{$v1.name}}

解决方案
 ~ {{$v1.solution}}{{end}}

{{end}}
{{end}}{{end}}

{{end}}