{{define "tomcat.host"}} {{range $k, $v := .problems}}{{if eq $v._scope "tomcatConfs.host"}}

| `配置项` | `值` |
|:---|:---|
| `ID`                   | {{$v.raw.hostId}}  |
| `Name`                 | {{$v.raw.hostname}}        |
| `bootTime`             | {{$v.raw.bootTime}}         |
| `kernelArch`           | {{$v.raw.kernelArch}}        |
| `kernelVersion`        | {{$v.raw.kernelVersion}}       |
| `os`                   | {{$v.raw.os}}            |
| `platform`             | {{$v.raw.platform}}            |
| `platformFamily`       | {{$v.raw.platformFamily}}            |
| `platformVersion`      | {{$v.raw.platformVersion}}            |
| `procs`                | {{$v.raw.procs}}            |
| `uptime`               | {{$v.raw.uptime}}            |
| `virtualizationRole`   | {{$v.raw.virtualizationRole}}     |
| `virtualizationSystem` | {{$v.raw.virtualizationSystem}}    |
{{end}} {{end}}
{{end}}