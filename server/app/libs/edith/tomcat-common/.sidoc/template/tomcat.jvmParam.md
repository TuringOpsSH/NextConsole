{{define "tomcat.jvmParam"}} {{range $k, $v := .problems}}{{if eq $v._scope "tomcatConfs.confRest"}}

| `配置项`        | `值`                                                 |
|:-------------|:----------------------------------------------------|
| `Xms`        | {{$v.raw.jvmParam.Xms}}                             |
| `Xmx`       | {{$v.raw.jvmParam.Xmx}}                             |
| `Xloggx`   | {{$v.raw.jvmParam.Xloggx}}                          |
| `HeapDumpOnOutOfMemoryError` | {{$v.raw.jvmParam.HeapDumpOnOutOfMemoryError}}      |
{{end}} {{end}}
{{end}}