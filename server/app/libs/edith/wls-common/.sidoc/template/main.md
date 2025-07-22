{{define "main"}}

{{template "meta" .}}

# 巡检信息

{{template "mission" .}}


# 主机列表

{{template "machinelist" .}}


# WebLogic概况

{{template "domainconfigs" .}}


# 基本配置

{{template "basicconfigs" .}}


# WebLogic 性能数据

{{template "wlsruntime" .}}


# 垃圾回收

{{template "gc" .}}


# 日志问题

{{template "log" .}}


{{end}}