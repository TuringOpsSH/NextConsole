{{define "main"}}

{{$summary := JsCall "func.summary" .problems}}
{{$appnames := .meta.config.appnames}}
{{$problems := GroupBy .problems "id"}}

---
title: {{.meta.customer}} {{.meta.title}}
subtitle: 
author:
    - 巡检工程师：{{ .meta.author.name}}
    - {{ .meta.org}} 

date: {{if .meta.date}}{{.meta.date}}{{else}}{{$summary.date}}{{end}}
---

# 文档版本信息

|版本|日期|作者|说明&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}|{{ .meta.author.name}} |初稿|
|||||

# 巡检总结和建议

## 巡检信息概述 

{{println ""}}应用系统名称：{{range .SysConfs}}{{JsCall "func.appname" .host.hostname}}{{end}}
{{println ""}}主机名：{{range .SysConfs}}{{printf "%-13s" .host.hostname}}{{end}}
{{println ""}}IP地址：{{range .SysConfs}}{{range .ip}}{{printf "%-24s" .}}{{end}}{{end}}
{{println ""}}服务器型号：{{range .SysConfs}}{{index .base "Product Name"}}{{end}}
{{println ""}}操作系统版本：{{range .SysConfs}}{{.host.platformFamily}} {{.host.platformVersion}} (发行版: {{.host.platform}}, 内核版本: {{.host.kernelVersion}}){{end}}
{{println ""}}巡检工程师：{{ .meta.author.name}}
{{println ""}}巡检时间：{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}

## 巡检结果汇总

本次巡检检查了{{$summary.hostArrCount}} 台主机{{if eq $summary.group "instance"}}（{{$summary.instArrCount}}个实例）{{end}}共 {{$summary.sum}} 个指标，其中发现 {{$summary.danger}} 个高风险、{{$summary.warning}} 个中风险、{{$summary.green}} 个低风险， 其余{{$summary.ok}} 个正常。告警定义如下：

|风险等级|颜色|标识|定义|
|:---|:---|:---|:---|
|高风险|红色|{{Icon "red"}}|经检查发现的最高级别告警，告警级别基于工程师从问题严重性、时间紧迫性、影响范围等方面的判断，建议及时进行处理。|
|中风险|橙色|{{Icon "orange"}}|经检查发现的中等级别告警，一般为仍然处在发展变化过程中且尚未转化为高风险告警的问题，建议关注问题发展趋势，结合实际情况进行处理。|
|低风险及正常|绿色|{{Icon "green"}}|包括经检查未发现问题的，或虽然存在问题但一般情况下影响可以忽略的告警。此外，对于最佳实践方面的检查结果也归为此类。|

## 巡检总结和建议表

### 高风险

|应用系统|检查内容|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "高风险"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

### 中风险

|应用系统|检查内容|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "中风险"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

### 低风险

|应用系统|检查内容|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "低风险"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

### 正常

|应用系统|检查内容|主机名|{{if eq $summary.group "instance"}}实例名|{{end}}预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|{{if eq $summary.group "instance"}}:---|{{end}}
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "正常"}}|{{JsCall "func.appname" .hostInst $appnames}}|{{$v.name}}|{{.hostInst}}|{{$v.expected}}|{{.actual}}|{{Icon .level}}|{{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

# 系统配置检查

## 系统基本配置
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
|IP address|{{index .base "IP address"}}|
|Distro|{{.base.Distro}}|
|OS kernel|{{index .base "OS kernel"}}|
|Runlevel|{{.base.Runlevel}}|
|Default Target|{{index .base "Default Target"}}|
|Uptime|{{.base.Uptime}}|
|Local Time|{{index .base "Local Time"}}|
|Time zone|{{index .base "Time zone"}}|
|SELinux|{{.base.SELinux}}|

{{end}}

## 时区设置
{{range $id, $vs := $problems}}{{if eq $id "linux.zone"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## PCI 配置
{{range .SysConfs}}{{range .lspci._check.results}}
{{range .raw}}
{{.}}
{{end}}
{{end}}{{end}}

## 磁盘配置
{{range $id, $vs := $problems}}{{if eq $id "linux.partition"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}


{{range .SysConfs}}
{{if .dmsetup}}
## Device Mapper
{{range .dmsetup}}
{{.}}
{{end}}
{{end}}
{{end}}


{{range .SysConfs}}
{{if .lvm}}

## LVM Filter

{{range $id, $vs := $problems}}{{if eq $id "linux.lvmconf"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{end}}{{end}}{{end}}

{{range .SysConfs}}
|配置项|值|
|:-----|:---|
|`filter`|{{ if .lvmconf.devices.filter}}{{.lvmconf.devices.filter}}{{else}}未设置{{end}}|
|`volume_list`|{{if .lvmconf.devices.volume_list}}{{ .lvmconf.devices.volume_list}}{{else}}未设置{{end}}|
{{end}}

## LVM 配置
{{range .lvm}}
{{.}}
{{end}}
{{end}}
{{end}}

## Mount 状态

{{range $id, $vs := $problems}}{{if eq $id "linux.mountCheck"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Source|Mountpoint|Type|Opts|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.source}}|{{.mountpoint}}|{{.type}}|{{.opts}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}

## SELinux

{{range $id, $vs := $problems}}{{if eq $id "linux.base"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}


## 魔术键

{{range $id, $vs := $problems}}{{if eq $id "linux.sysrq"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}


## NUMA

{{range $id, $vs := $problems}}{{if eq $id "linux.numastat"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 内核参数
{{range .SysConfs}}

|内核参数类型|内核参数|单位|当前值|推荐值|
|:--:|:--:|:--:|:--:|:--:|
|kernel|sem|arry|{{index .sysctla "kernel.sem"}}|250 32000 100 128（for Oracle）|
|kernel|threads-max|num|{{index .sysctla "kernel.threads-max"}}|-|
|kernel|shmall|4-KiB pages|{{index .sysctla "kernel.shmall"}}|-|
|kernel|shmmax|bytes|{{index .sysctla "kernel.shmmax"}}|-|
|kernel|shmmni|segments|{{index .sysctla "kernel.shmmni"}}|-|
|fs|file-max|num|{{index .sysctla "kernel.shmall"}}|-|
|fs|nr_open|num|{{index .sysctla "fs.file-max"}}|-|
|net|core.rmem_default|bytes|{{index .sysctla "net.core.rmem_default"}}|-|
|net|core.wmem_default|bytes|{{index .sysctla "net.core.wmem_default"}}|-|
|net|core.rmem_max|bytes|{{index .sysctla "net.core.rmem_max"}}|4M 即 4194304|
|net|core.wmem_max|bytes|{{index .sysctla "net.core.wmem_max"}}|4M 即 4194304|
|net|ipv4.ip_forward|bool|{{index .sysctla "net.ipv4.ip_forward"}}|0|
|net|ipv4.ip_local_port_range|ports|{{index .sysctla "net.ipv4.ip_local_port_range"}}|9000 65500（for Oracle）|

{{end}}

# 系统服务检查

## Chrony 与 NTP
{{range $id, $vs := $problems}}{{if eq $id "linux.ntpsync"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

{{range $id, $vs := $problems}}{{if eq $id "linux.ntpServiceCheck"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|时间|服务状态|告警|
|:---:|:---:|:---:|
{{range .mixraw}}|{{.datetime}}|{{.metric}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}

## Kdump 服务

{{range $id, $vs := $problems}}{{if eq $id "linux.kdumpCheck"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|时间|服务状态|告警|
|:---:|:---:|:---:|
{{range .mixraw}}|{{.datetime}}|{{.metric}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}

{{range .SysConfs}}

|配置项|值|
|:---|:---|
|kexec-tools|{{index .kdump "kexec-tools"}}|
|kdump.service|{{index .kdump "kdump.service"}}|
|/proc/cmdline|{{index .kdump "kexec-tools"}}|
|grub.cfg|{{index .kdump "grub.cfg"}}|
|kdump.conf|{{index .kdump "kdump.conf"}}|
|system memTotal|{{index .kdump "system memTotal"}}|
|/var/crash|{{index .kdump "/var/crash"}}|

{{end}}

## 僵尸进程

{{range $id, $vs := $problems}}{{if eq $id "linux.psaxoZz"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if ne .level "正常"}}
原始数据:
{{range .raw}}
>{{.}}
{{end}}
{{end}}

{{end}}{{end}}{{end}}

## 不可中断进程

{{range $id, $vs := $problems}}{{if eq $id "linux.psaxoDd"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if ne .level "正常"}}
原始数据:
{{range .raw}}
>{{.}}
{{end}}
{{end}}

{{end}}{{end}}{{end}}


## 占用内存 TOP10
{{range .SysStatus}}
|进程使用内存 TOP 10 (PID %MEM %CPU COMMAND)|
|:---|
{{range $k, $v := .top10mem}}{{if eq $k 0}}{{range .metric}}|{{.}}|
{{end}}
{{end}}
{{end}}
{{end}}

## 占用CPU TOP10
{{range .SysStatus}}
|进程使用 CPU TOP 10 (PID %MEM %CPU COMMAND)|
|:---|
{{range $k, $v := .top10cpu}}{{if eq $k 0}}{{range .metric}}|{{.}}|
{{end}}
{{end}}
{{end}}
{{end}}


# 产品兼容检查

## 产品生命周期

当前系统产品生命周期分析：

{{range .SysConfs}}
{{range .host._check.results}}
{{if eq .id "linux.eof"}}
|检查内容|告警影响|处理建议|检查结果|
|:---|:---|:---|:---|
|{{.name}}。预期为{{.expected}} |{{.effect}}|{{.solution}}|{{Icon .level}}|

{{end}}
{{end}}
{{end}}

|操作系统版本|End-Of-Life(EOL)|
|:---|:---|
|CentOS Linux 8发行版|2021年12月31日|
|CentOS Linux 7发行版|2024年6月30日|
|CentOS Linux 6发行版|2020年11月30日|

|操作系统版本|End-Of-Life(EOL)|
|:---|:---|
|RedHat Linux 8企业版|2029年5月1日|
|RedHat Linux 7企业版|2024年6月30日|
|RedHat Linux 6企业版|2020年11月30日|

## 系统兼容性
操作系统版本：{{range .SysConfs}}{{index .base "Distro"}}{{end}}
服务器型号：{{range .SysConfs}}{{index .base "Product Name"}}{{end}}
分析结果：

## RPM 兼容性

{{range $id, $vs := $problems}}{{if eq $id "linux.rpmqalast"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if ne .level "正常"}}
异常:
{{range .raw}}
>{{.}}
{{end}}
{{end}}

{{end}}{{end}}{{end}}

## RPM 完整性

{{range $id, $vs := $problems}}{{if eq $id "linux.rpmVa"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if ne .level "正常"}}

标识含义:

- S file Size differs
- M Mode differs (includes permissions and file type)
- 5 digest (formerly MD5 sum) differs
- D Device major/minor number mismatch
- L readLink(2) path mismatch
- U User ownership differs
- G Group ownership differs
- T mTime differs
- P caPabilities differ

原始数据:
{{range .raw}}
>{{.}}
{{end}}
{{end}}

{{end}}{{end}}{{end}}

# 系统容量检查

## CPU 使用率

{{range $id, $vs := $problems}}{{if eq $id "linux.cpuUsedPercent"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|时间|CPU使用率(%)|告警|
|:---:|:---:|:---:|
{{range .mixraw}}|{{.datetime}}|{{.metric}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}

{{range .SysConfs}}
| 逻辑核心数|CPU标号|物理核心数|型号 |
|:---:|:---:|:---:|:---:|
{{range .cpu}}|{{printf " %-0.0f" .cpu}}|{{printf " %-13s" .physicalId}}|{{printf " %-0.0f" .cores}}|{{print .modelName}}|
{{end}}
{{end}}

## CPU 负载

{{range $id, $vs := $problems}}{{if eq $id "linux.cpuLoad"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|时间|1分钟|5分钟|15分钟|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.datetime}}|{{.load1}}|{{.load5}}|{{.load15}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}

## 内存使用率

{{range .SysConfs}}

| 总量 (MB)| 已使用(MB)| 可用(MB) |缓存(MB)| swap总量(MB)| swap可用(MB) | 内存使用率|检查结果|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| {{JsCall "func.byte2mb" .mem.total}}  |{{JsCall "func.byte2mb" .mem.used }} |{{JsCall "func.byte2mb" .mem.free  }} | {{JsCall "func.byte2mb" .mem.cached }} | {{JsCall "func.byte2mb" .mem.swapTotal }}|  {{JsCall "func.byte2mb" .mem.swapFree }} | {{printf "%.2f%%" .mem.usedPercent }} |{{if gt  .mem.usedPercent 70.00}}{{Icon "red"}}{{else}}{{Icon "green"}} {{end}}|

{{end}}

{{if .problems}}
{{$pros := GroupBy .problems "id"}}{{ range $key, $values := $pros}}{{$v1 := index $values 0}}
{{if eq $key "linux.swapCheck"}}
### {{$v1.name}}【{{$v1.level}}】
|描述|建议|检查结果|
|:---:|:---:|:---:|
{{range $values}}|{{.desc}}|{{.expected}}|{{if eq .level "正常"}}{{Icon "green"}}{{else}}{{Icon "Orange"}}{{end}}|
{{end}}{{end}}

{{if eq $key "linux.swapUsedPercent"}}
### {{$v1.name}} 【{{$v1.level}}】
|内存使用率|描述|检查结果|
|:---:|:---:|:---:|
{{range $values}}|{{.actual}}|{{.desc}}|{{if eq .level "正常"}}{{Icon "green"}}{{else}}{{Icon "red"}}{{end}}|
{{end}}{{end}}

{{if eq $key "linux.memUsedPercent"}}
### {{$v1.name}} 【{{$v1.level}}】
| 内存使用率| 描述| 检查结果|
|:---:|:---:|:---:|
{{range $values}}|{{.usedPercent}}|{{.desc}}|{{if eq .level "正常"}}{{Icon "green"}}{{else}}{{Icon "red"}}{{end}}|
{{end}}{{end}}{{end}}{{end}}

## 文件系统使用率

{{range $id, $vs := $problems}}{{if eq $id "linux.diskUsedPercent"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|路径|文件系统类型|总量(MB)|已用(MB)|剩余(MB)|使用率|检查结果|
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
{{range .mixraw}}|{{.path}}|{{.fstype}}|{{.total}}|{{.used}}|{{.free}}|{{.usedPercent}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 磁盘繁忙

{{range $id, $vs := $problems}}{{if eq $id "linux.diskAvgUtil"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|DEV|tps|rd_sec/s|wr_sec/s|avgrq-sz|avgqu-sz|await|svctm|%util|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.DEV}}|{{.tps}}|{{.rd_secs}}|{{.wr_secs}}|{{.avgrqsz}}|{{.avgqusz}}|{{.await}}|{{.svctm}}|{{.utilpct}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## Inode 使用率

{{range $id, $vs := $problems}}{{if eq $id "linux.inodeUsedPercent"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Filesystem|IFree|IUse%|IUsed|Inodes|Mounted on|Level|
|:---|:---|:---|:---|:---|:---|:---:|
{{range .mixraw}}|{{.Filesystem}}|{{.IFree}}|{{.IUse_PCT}}|{{.IUsed}}|{{.Inodes}}|{{.Mounted}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}


## 网络使用率

{{range $id, $vs := $problems}}{{if eq $id "linux.netused"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Net|RX|Speed|TX|Used%|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.net}}|{{.rx}}|{{.speed}}|{{.tx}}|{{.used}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}



# 系统日志检查


## /var/log/messages
{{range $id, $vs := $problems}}{{if eq $id "linux.msglog"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## /var/log/mcelog
{{range $id, $vs := $problems}}{{if eq $id "linux.mcelog"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## /var/log/dmesg
{{range $id, $vs := $problems}}{{if eq $id "linux.dmesglog"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## /var/log/boot.log
{{range $id, $vs := $problems}}{{if eq $id "linux.bootlog"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## /var/log/secure
{{range $id, $vs := $problems}}{{if eq $id "linux.varlogsecure"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## journalctl err
{{range $id, $vs := $problems}}{{if eq $id "linux.journalctlerr"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## journalctl crit
{{range $id, $vs := $problems}}{{if eq $id "linux.journalctlcrit"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

# 网络相关检查

## TCP 连接
{{$problems := GroupBy .problems "id"}}
{{range $id, $vs := $problems}}{{if eq $id "linux.conns"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Established|Listen|Time_wait|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.established}}|{{.listen}}|{{.time_wait}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 网络链路
{{range .SysStatus}}
{{range .ethtooli._check.results}}

|检查内容|告警影响|处理建议|检查结果|
|:---|:---|:---|:---|
|{{.desc}}|{{.effect}}|{{.solution}}|{{Icon .level}}|

{{end}}
{{end}}

{{range .problems}}
{{if eq .id "linux.ethtooli"}}
{{if ne .level "正常"}}

原始数据:

|网卡|链路|速率|工作模式|端口类型|网卡驱动|驱动微码|
|:---|:---|:---|:---|:---|:---|:---|
{{range $key,$values := .raw}}|{{range $k,$v := $values}}{{$k}}|{{index . "Link_detected"}}|{{index . "Speed"}}|{{index . "Duplex"}}|{{index . "Supported_ports"}}|{{index . "driver"}}|{{index . "version"}}{{end}}|
{{end}}
{{end}}
{{end}}
{{end}}

## 网络地址
{{range .SysConfs}}
|数据|
|:---| 
|{{range .ifconfiga}}{{.}}|{{end}}
{{end}}

## 端口聚合
{{range .SysConfs}}
{{range .bonding._check.results}}
|类型|端口聚合设置|检查结果|
|:---|:---|:---|
|/proc/net/bonding/* |{{ .raw.bonding1}}|{{Icon .level}}|
|nmcli connection show (team)|{{.raw.bonding2}}|{{Icon .level}}|
{{end}}
{{end}}

## 网卡CRC及帧错误

{{range .SysStatus}}
{{range .ethtoolS._check.results}}

|检查内容|告警影响|处理建议|检查结果|
|:---|:---|:---|:---|
|{{.desc}}|{{.effect}}|{{.solution}}|{{Icon .level}}|

{{end}}
{{end}}

## 网卡驱动丢包

{{range .SysConfs}}
{{range .procnetdev._check.results}}

|检查内容|告警影响|处理建议|检查结果|
|:---|:---|:---|:---|
|{{.desc}}|{{.effect}}|{{.solution}}|{{Icon .level}}|

{{end}}
{{end}}

## 多路径状态

{{range $id, $vs := $problems}}{{if eq $id "linux.multipath"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if ne .level "正常"}}
原始数据:
{{range .raw}}
>{{.}}
{{end}}
{{end}}

{{end}}{{end}}{{end}}

## 防火墙
{{range .SysStatus}}
{{range .iptables._check.results}}

|检查内容|告警影响|处理建议|检查结果|
|:---|:---|:---|:---|
|{{.desc}}|{{.effect}}|{{.solution}}|{{Icon .level}}|

{{end}}
{{end}}

# 安全合规检查

## 用户密码加密

{{range $id, $vs := $problems}}{{if eq $id "linux.etcPasswordCheck"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|User|Password|UID|GID|Homedir|Comment|Shell|Level|
|:---|:---|:---|:---|:---|:---|---:|---:|
{{range .mixraw}}|{{.user}}|{{.password}}|{{.uid}}|{{.gid}}|{{.homedir}}|{{.comment}}|{{.shell}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}


## SSH 与 FTP 安全

{{range $id, $vs := $problems}}{{if eq $id "linux.sec"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|项目|预期值|实际值|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.item}}|{{.expected}}|{{.actual}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}

## 密码最大使用天数
{{range $id, $vs := $problems}}{{if eq $id "linux.etclogindefs1"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 两次修改密码之间允许的最短天数

{{range $id, $vs := $problems}}{{if eq $id "linux.etclogindefs2"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 密码过期前警告天数

{{range $id, $vs := $problems}}{{if eq $id "linux.etclogindefs3"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

## 其他安全

{{range $id, $vs := $problems}}{{if eq $id "linux.othersec"}}{{range $k, $v := $vs}} 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|项目|预期值|实际值|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.item}}|{{.expected}}|{{.actual}}|{{Icon .mixlevel}}|
{{end}}
{{end}}

{{end}}{{end}}{{end}}


{{end}}
