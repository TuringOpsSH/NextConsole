{{define "machinelist"}}

| 主机名      	 | IP                  | 操作系统        |内存使用率  |CPU数量   |
| :------------: | :------------------: | :-------------: | :-------------: |:-------------: |
{{range .SysConfs}}|{{printf " %-13s" .host.hostname}}|{{range .ip}}{{printf " %-24s" .}}{{end}}|{{printf " %-13s" .host.os}}|{{printf "%.2f%%" .mem.usedPercent}}|{{len .cpu}}|
{{end}}



WebLogic 版本： {{range .WlsConfs}}{{printf "%-13s      "  .domain.version}}{{end}}

{{if .problems}}## 问题
{{$pros := GroupBy .problems "id"}}
{{ range $key, $values := $pros}}{{$v1 := index $values 0}}### {{$v1.name}} (严重程度：{{JsCall "func.level" $values}})
{{if eq $key "wls.dataSource"}}
| Scope      	| Target        | DataSource Name          | Descrtiption                               | 
| :------------ | :------------ | :------------------------| :----------------------------------------- | 
{{range $values}}|{{._scope}}|{{._name}}|{{._dsname}}|{{.desc}}|
{{end}}
{{$v1.solution}}{{end}}{{if eq $key "wls.logging"}}
| Server      	|  Descrtiption                               | 
| :------------ | :------------------------------------------ | 
{{range $values}}|{{._name}}|{{.desc}}|
{{end}}
{{$v1.solution}}{{end}}{{if HasPrefix $key "wls.serverRuntime"}}
| Server      	|  说明                                 | 
| :------------ | :------------------------------------|
{{range $values}}{{if ne .startupMode "RUNNING"}}|{{._name}}|{{.startupMode}}|{{end}}{{end}}
{{$v1.solution}}{{end}}

{{end}}{{end}}

{{end}}