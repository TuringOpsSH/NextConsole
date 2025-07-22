{{define "base"}}
{{range .SysConfs}}

|配置项|值|
|:---|:---|
|hostname|{{.base.hostname}}|
|Product Name|{{index .base "Product Name"}}|
|Serial Number|{{index .base "Serial Number"}}|
|UUID|{{.base.UUID}}|
|Arch|{{.base.Arch}}|
|CPUs|{{.base.CPUs}}|
|Total Memory|{{index .base "Total Memory"}}|
|Distro|{{.base.Distro}}|
|OS kernel|{{index .base "OS kernel"}}|
|Runlevel|{{.base.Runlevel}}|
|Default Target|{{index .base "Default Target"}}|
|Uptime|{{.base.Uptime}}|
|Local Time|{{index .base "Local Time"}}|
|Time zone|{{index .base "Time zone"}}|
|SELinux|{{.base.SELinux}}|

{{end}}
{{end}}