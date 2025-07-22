{{define "domainconfigs"}}

## 域信息
{{range .WlsConfs}}
* {{.domain.name}} ({{.domain.version}})
{{end}}

### Clusters

{{range .WlsConfs}}
{{if .domain}}
{{if not .clusters}}
{{range .domain.clusters}} * {{.name}} ({{ range $index, $element := .members}}{{if $index}}, {{end}}{{$element}}{{end}})
{{else}} * {{printf "没有配置集群"}}{{end}}
{{end}}{{end}}{{end}}

### Servers

| Server      	                                | Listen Address            | Listen Port                        | Cluster                         | 
|:---------------------------------------------|:--------------------------|:-----------------------------------|:--------------------------------| 
 {{range .WlsConfs}}{{range .domain.servers}} | {{printf " %-18s" .name}} | {{printf " %-18s" .listenAddress}} | {{printf " %-11s" .listenPort}} |{{printf " %-11s" .cluster}}|
{{end}}{{end}}

### Machines

| Machines | Listen Address | Listen Port | type |
| :-------------: |:-----------------: |:---------: | :---------: |
{{range .WlsConfs}}{{range .domain.machines}}|{{.name}}|{{.listenAddress}}|{{.listenPort}}|{{.type}}|
{{end}}{{end}}


{{end}}