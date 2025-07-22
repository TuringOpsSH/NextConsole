{{define "main"}}
{{$isopen := ""}}
{{range .OracleConfs}}{{$isopen = .instance.openmode}} {{end}}
{{if eq $isopen "OPEN"}}

{{$problems := GroupBy .problems "id"}}
{{$summary := JsCall "func.summary" .problems}}
{{$appnames := .meta.config.appnames}}
{{$version := JsCall "func.version" .OracleConfs}}

---
title: {{.meta.customer}} {{.meta.title}}
subtitle: 
author:
    - 巡检工程师：{{ .meta.author.name}}
    - {{ .meta.org}} 

date: {{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}
---


# 文档版本信息

|版本&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|日期&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|作者&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|说明&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}|{{ .meta.author.name}} |初稿|
|||||

# 巡检总结和建议

## 巡检信息概述 
{{println ""}}主机名：{{if .SysConfs}}{{range .SysConfs}}{{printf "%-13s" .host.hostname}}{{end}}{{else}}{{range .OracleConfs}}{{index .host "hostname"}} {{end}}{{end}}
{{println ""}}数据库实例：{{range .OracleConfs}}{{index .instance "sid"}} {{end}}
{{println ""}}巡检工程师：{{ .meta.author.name}} 
{{println ""}}巡检报告生成时间：{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}

## 巡检告警定义
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

# 基本配置检查

{{if .SysConfs}}
## 操作系统基本配置
{{range .SysConfs}}

### {{.host.hostname}}

|配置项|值|
|:---|:---|
{{range $k,$v := .base}}{{if ne $k "_check"}}|{{$k}}|{{$v}}|
{{end}}{{end}}

{{end}}
{{else}}
{{range .OracleConfs}}

|配置项|值|
|:---|:---|
{{range $k,$v := .host}}{{if ne $k "_check"}}|{{$k}}|{{$v}}|
{{end}}{{end}}

{{end}}
{{end}}

## 数据库基本配置

{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.baseinfo"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Parameter|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.parameter}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.baseinfo12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 数据库基本信息

控制文件中关于数据库的信息( V$DATABASE )。

{{range $id, $vs := $problems}}{{if eq $id "oracle.version"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Parameter|Value|
|:---|:---|
{{range .mixraw}}|Dbid|{{index . "dbid"}}|
|Name|{{index . "name"}}|
|Version|{{index . "version"}}|
|Cluster_Database|{{index . "cluster_database"}}|
|Created|{{index . "created"}}|
|Resetlogs_change|{{index . "resetlogs_change"}}|
|Resetlogs_time|{{index . "resetlogs_time"}}|
|Log_mode|{{index . "log_mode"}}|
|Checkpoint_change|{{index . "checkpoint_change"}}|
|Open_mode|{{index . "open_mode"}}|
|Protection_mode|{{index . "protection_mode"}}|
|Protection_level|{{index . "protection_level"}}|
|Database_role|{{index . "database_role"}}|
|Force_logging|{{index . "force_logging"}}|
|Platform_id|{{index . "platform_id"}}|
|Platform_name|{{index . "platform_name"}}|
|Flashback_on|{{index . "flashback_on"}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## OS 系统参数

{{range $id, $vs := $problems}}{{if eq $id "oracle.osparm"}}{{range $k, $v := $vs}}
### {{._name}} 系统参数

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Name|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


{{range $id, $vs := $problems}}{{if eq $id "oracle.sysctla"}}{{range $k, $v := $vs}}
### {{._name}} 内核参数

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Name|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

{{range $id, $vs := $problems}}{{if eq $id "oracle.mem"}}{{range $k, $v := $vs}}
### {{._name}} 内存参数及使用率

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Name|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


{{range $id, $vs := $problems}}{{if eq $id "oracle.limits"}}{{range $k, $v := $vs}}
### {{._name}} 资源限制

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|用户名|类型|项目|当前值|推荐值|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.user}}|{{.type}}|{{.item}}|{{.value}}||{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


{{range $id, $vs := $problems}}{{if eq $id "linux.etchosts"}}{{range $k, $v := $vs}}
## 主机文件配置

### {{._name}}

{{if .mixraw}}
|IP|Names|
|:---|:---|
{{range .mixraw}}|{{.IP}}|{{.names}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

{{range $id, $vs := $problems}}{{if eq $id "oracle.etchosts"}}{{range $k, $v := $vs}}

### {{._name}}
{{if .mixraw}}
|IP|Names|
|:---|:---|
{{range .mixraw}}|{{.IP}}|{{.names}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


{{range $id, $vs := $problems}}{{if eq $id "oracle.lo"}}{{range $k, $v := $vs}}
## MTU for lo

{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Item|Value|
|:---|:---|
{{range .mixraw}}|{{.item}}|{{.value}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

# 系统存储空间使用

## 文件系统使用

{{range $id, $vs := $problems}}{{if eq $id "linux.diskUsedPercent"}}{{range $k, $v := $vs}}

### {{._name}}

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

{{range $id, $vs := $problems}}{{if eq $id "oracle.fspct"}}{{range $k, $v := $vs}}

### {{._name}}

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Mounted|Filesystem|All(GB)|Free(GB)|Used|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.Mounted}}|{{.Filesystem}}|{{.GB}}|{{.Free}}|{{.Used}}|{{Icon .mixlevel}}
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 文件系统 Inode 使用

{{range $id, $vs := $problems}}{{if eq $id "linux.inodeUsedPercent"}}{{range $k, $v := $vs}}

### {{._name}}

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}

### {{._name}}

|Mounted|Filesystem|Used|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.Mounted}}|{{.Filesystem}}|{{.Used}}|{{Icon .mixlevel}}
{{end}}
{{end}}
{{end}}{{end}}{{end}}

{{range $id, $vs := $problems}}{{if eq $id "oracle.inodepct"}}{{range $k, $v := $vs}}

### {{._name}}

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Mounted|Filesystem|Used|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.Mounted}}|{{.Filesystem}}|{{.Used}}|{{Icon .mixlevel}}
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 磁盘组使用率
{{range $id, $vs := $problems}}{{if eq $id "oracle.diskgroup"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Au_Size|State|Type|Total_Disk_Size_Mb|Dg_Total_Mb|Dg_Free_Mb|Dg_Used_Pct|Offline_Disks|Redundancy|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.au_size}}|{{.state}}|{{.type}}|{{.total_disk_size_mb}}|{{.dg_total_mb}}|{{.dg_free_mb}}|{{.dg_used_pct}}|{{.offline_disks}}|{{.redundancy}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## RDBMS软件的ASM磁盘使用情况
{{range $id, $vs := $problems}}{{if eq $id "oracle.compatible_rdbms"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|diskgroup_name|path|os_mb|total_mb|compatible_asm|compatible_rdbms|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.diskgroup_name}}|{{.path}}|{{.os_mb}}|{{.total_mb}}|{{.compatible_asm}}|{{.compatible_rdbms}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 磁盘组 Offline 情况检查
{{range $id, $vs := $problems}}{{if eq $id "oracle.diskgroupoffline"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Au_Size|State|Type|Total_Disk_Size_Mb|Dg_Total_Mb|Dg_Free_Mb|Dg_Used_Pct|Offline_Disks|Redundancy|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.au_size}}|{{.state}}|{{.type}}|{{.total_disk_size_mb}}|{{.dg_total_mb}}|{{.dg_free_mb}}|{{.dg_used_pct}}|{{.offline_disks}}|{{.redundancy}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 磁盘使用率
{{range $id, $vs := $problems}}{{if eq $id "oracle.asm_disk_detail"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Group_Number|Diskgroupname|Namedisk|Path|State|Total_Mb|Os_Mb|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.group_number}}|{{.diskgroupname}}|{{.namedisk}}|{{.path}}|{{.state}}|{{.total_mb}}|{{.os_mb}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 表空间使用

{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.tbscheck"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Tablespace_Name|Bigfile|Count_File|Used(%)|Used_Extent_Able(%)|Total(MB)|Used(MB)|Free(MB)|MAX_Extent(MB)|Max_Fragment(MB)|FSFI|Extent|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.tablespace_name}}|{{.bigfile}}|{{.count_file}}|{{.usedpct}}|{{.xxx}}|{{.total}}|{{.used}}|{{.free}}|{{.extent_total}}|{{.max_fragment_mb}}|{{.fsfi}}|{{.yesno}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.tbscheck12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Tablespace_Name|Bigfile|Count_File|Used(%)|Used_Extent_Able(%)|Total(MB)|Used(MB)|Free(MB)|MAX_Extent(MB)|Max_Fragment(MB)|FSFI|Extent|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.tablespace_name}}|{{.bigfile}}|{{.count_file}}|{{.usedpct}}|{{.pct}}|{{.total}}|{{.used}}|{{.free}}|{{.extent_total}}|{{.max_fragment_mb}}|{{.fsfi}}|{{.yesno}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if lt $version.ver 11}}## 表空间碎片
{{range $id, $vs := $problems}}{{if eq $id "oracle.tbs_fragement_pct"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Tablespace_Name|FSFI|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.tablespace_name}}|{{.pct}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 闪回区使用

{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.flashback"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|File_Type|Percent_Space_Used|Percent_Space_Reclaimable|Number_Of_Files|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.file_type}}|{{.percent_space_used}}|{{.percent_space_reclaimable}}|{{.number_of_files}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}



{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.flashback12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|File_Type|Percent_Space_Used|Percent_Space_Reclaimable|Number_Of_Files|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.file_type}}|{{.percent_space_used}}|{{.percent_space_reclaimable}}|{{.number_of_files}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 回收站使用

{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.recyclebin"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Tbs_Name|Cnt|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.tbs_name}}|{{.cnt}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.recyclebin_12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Pdb_Name|Tbs_Name|Cnt|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.pdb_name}}|{{.tbs_name}}|{{.cnt}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

# 数据库组件及参数设置


## 参数设置

{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.parameter"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}【实际值】见检查结果汇总|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .actuals}}
|检查结果汇总|
|:-|
{{range .actuals}}|{{.}}|
{{end}}
{{end}}


{{if .mixraw}}
|Inst_Id|Name|Value|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.inst_id}}|{{.name}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.parameter12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}【实际值】见检查结果汇总|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .actuals}}
|检查结果汇总|
|:-|
{{range .actuals}}|{{.}}|
{{end}}
{{end}}

{{if .mixraw}}
|Name|Inst_Id|Name|Value|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.container}}|{{.inst_id}}|{{.name}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

## 最佳实践参数设置

{{range $id, $vs := $problems}}{{if eq $id "oracle.hiddenparms"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|参数名|当前值|推荐值|是否一致|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.ksppinm}}|{{.ksppstvl}}|{{.expected}}|{{.iseq}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## Spfile 参数优先级设置

{{range $id, $vs := $problems}}{{if eq $id "oracle.spfile_warning"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Inst_Id|Sid|Name|Value|Warning|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.inst_id}}|{{.sid}}|{{.name}}|{{.value}}|{{.warning}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 数据库组件


{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.comp"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Comp_Id|Comp_Name|Version|Status|Modified|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.comp_id}}|{{.comp_name}}|{{.version}}|{{.status}}|{{.modified}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.comp12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Comp_Id|Comp_Name|Version|Status|Modified|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.comp_id}}|{{.comp_name}}|{{.version}}|{{.status}}|{{.modified}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}



## 时区设置

{{range $id, $vs := $problems}}{{if eq $id "oracle.timezone"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Db_Time_Zone|Dbtimezone|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.db_time_zone}}|{{.dbtimezone}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 时区文件版本

{{range $id, $vs := $problems}}{{if eq $id "oracle.dstcheck"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Db_Version|Dst_Version|Regist_Version|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.db_version}}|{{.dst_version}}|{{.regist_version}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

{{if $version.v12}}
## PDB 状态

{{range $id, $vs := $problems}}{{if eq $id "oracle.pdbstat"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Con_Id|Name|Inst_Id|Open_Mode|Restricted|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.con_id}}|{{.name}}|{{.inst_id}}|{{.open_mode}}|{{.restricted}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

{{end}}

{{if $version.v12}}
## PDB 状态保留

{{range $id, $vs := $problems}}{{if eq $id "oracle.pdbsavedstate"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Con_Name|Instance_Name|State|Restricted|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.con_name}}|{{.instance_name}}|{{.state}}|{{.restricted}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

{{end}}

# 数据文件


## 补丁安装

{{range $id, $vs := $problems}}{{if eq $id "oracle.lspatches"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .raw}}
|Patch Info|
|:---|
{{range .raw}}|{{.}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 补丁注册记录

{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.patchapply"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Action_Time|Action|Namespace|Version|Id|Comments|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.action_time}}|{{.action}}|{{.namespace}}|{{.version}}|{{.id}}|{{.comments}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.patchapply12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Action_Time|Action|Namespace|Version|Id|Comments|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.action_time}}|{{.action}}|{{.namespace}}|{{.version}}|{{.id}}|{{.comments}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 联机日志
{{range $id, $vs := $problems}}{{if eq $id "oracle.onlinelog"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Thread|Group|Member|Status|Sequence|Mb|Logtype|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.thread}}|{{.group}}|{{.member}}|{{.status}}|{{.sequence}}|{{.MB}}|{{.logtype}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 联机日志切换
{{range $id, $vs := $problems}}{{if eq $id "oracle.logswitch"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Day|H00|H01|H02|H03|H04|H05|H06|H07|H08|H09|H10|H11|H12|H13|H14|H15|H16|H17|H18|H19|H20|H21|H22|H23|Total|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.day}}|{{.h00}}|{{.h01}}|{{.h02}}|{{.h03}}|{{.h04}}|{{.h05}}|{{.h06}}|{{.h07}}|{{.h08}}|{{.h09}}|{{.h10}}|{{.h11}}|{{.h12}}|{{.h13}}|{{.h14}}|{{.h15}}|{{.h16}}|{{.h17}}|{{.h18}}|{{.h19}}|{{.h20}}|{{.h21}}|{{.h22}}|{{.h23}}|{{.total}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 控制文件

{{range $id, $vs := $problems}}{{if eq $id "oracle.controlfile"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Mirrored|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.mirrored}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 数据文件
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.datafile"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Type|Tablespace_Name|File_Name|Size_Mb|Max_Size_Mb|Autoextensible|Status|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.type}}|{{.tablespace_name}}|{{.file_name}}|{{.size_mb}}|{{.max_size_mb}}|{{.autoextensible}}|{{.status}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.datafile12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Type|Tablespace_Name|File_Name|Size_Mb|Max_Size_Mb|Autoextensible|Status|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.type}}|{{.tablespace_name}}|{{.file_name}}|{{.size_mb}}|{{.max_size_mb}}|{{.autoextensible}}|{{.status}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

## 资源使用限制
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.resourcelimit"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Resource_Name|Current_Utilization|Max_Utilization|Initial_Allocation|Limit_Value|Yesno|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.resource_name}}|{{.current_utilization}}|{{.max_utilization}}|{{.initial_allocation}}|{{.limit_value}}|{{.yesno}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.resourcelimit12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Resource_Name|Current_Utilization|Max_Utilization|Initial_Allocation|Limit_Value|Yesno|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.resource_name}}|{{.current_utilization}}|{{.max_utilization}}|{{.initial_allocation}}|{{.limit_value}}|{{.yesno}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

# 系统对象检查


## 使用率超过70%的序列
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.sequence"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Sequence_Owner|Sequence_Name|Used_Pct|Min_Value|Max_Value|Increment_By|Cycle_Flag|Order_Flag|Cache_Size|Last_Number|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.sequence_owner}}|{{.sequence_name}}|{{.used_pct}}|{{.min_value}}|{{.max_value}}|{{.increment_by}}|{{.cycle_flag}}|{{.order_flag}}|{{.cache_size}}|{{.last_number}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.sequence12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Sequence_Owner|Sequence_Name|Used_Pct|Min_Value|Max_Value|Increment_By|Cycle_Flag|Order_Flag|Cache_Size|Last_Number|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.sequence_owner}}|{{.sequence_name}}|{{.used_pct}}|{{.min_value}}|{{.max_value}}|{{.increment_by}}|{{.cycle_flag}}|{{.order_flag}}|{{.cache_size}}|{{.last_number}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 缓存小于500的序列

{{range $id, $vs := $problems}}{{if eq $id "oracle.sequence_cache"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Sequence_Owner|Sequence_Name|Cache_Size|Order_Flag|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.sequence_owner}}|{{.sequence_name}}|{{.cache_size}}|{{.order_flag}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 失效对象
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.invalidobj"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Owner|Object_Name|Object_Type|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.owner}}|{{.object_name}}|{{.object_type}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.invalidobj12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Owner|Object_Name|Object_Type|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.owner}}|{{.object_name}}|{{.object_type}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 失效索引
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.invalididx"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Owner|Index_Name|Index_Type|Partition_Name|Status|Table_Name|Tablespace_Name|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.owner}}|{{.index_name}}|{{.index_type}}|{{.partition_name}}|{{.status}}|{{.table_name}}|{{.tablespace_name}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}



{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.invalididx12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Index_Owner|Index_Name|Index_Type|Partition_Name|Status|Table_Name|Tablespace_Name|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.index_owner}}|{{.index_name}}|{{.index_type}}|{{.partition_name}}|{{.status}}|{{.table_name}}|{{.tablespace_name}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 失效触发器
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.invalidtrigger"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Owner|Trigger_Name|Trigger_Type|Status|Table_Owner_And_Name|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.owner}}|{{.trigger_name}}|{{.trigger_type}}|{{.status}}|{{.table_owner_and_name}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.invalidtrigger12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Owner|Trigger_Name|Trigger_Type|Status|Table_Owner_Table_Name|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.owner}}|{{.trigger_name}}|{{.trigger_type}}|{{.status}}|{{.table_owner_table_name}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

## 失效约束
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.invalidcons"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Owner|Constraint_Name|Constraint_Type|Table_Name|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.owner}}|{{.constraint_name}}|{{.constraint_type}}|{{.table_name}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.invalidcons12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Owner|Constraint_Name|Constraint_Type|Table_Name|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.owner}}|{{.constraint_name}}|{{.constraint_type}}|{{.table_name}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

## 外键无索引
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.foreignkey"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Owner|Constraint_Name|Table_Name|Column_Name|Status|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.owner}}|{{.constraint_name}}|{{.table_name}}|{{.column_name}}|{{.status}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.foreignkey12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Owner|Constraint_Name|Table_Name|Column_Name|Status|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.owner}}|{{.constraint_name}}|{{.table_name}}|{{.column_name}}|{{.status}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 系统定时任务
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.jobs"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Job|Priv_User|What|Status|Warning|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.job}}|{{.priv_user}}|{{.what}}|{{.status}}|{{.warning}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.jobs12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Job|Priv_User|What|Status|Warning|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.job}}|{{.priv_user}}|{{.what}}|{{.status}}|{{.warning}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

## 系统自动任务

{{range $id, $vs := $problems}}{{if eq $id "oracle.autotask"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Autotask|Status|Warning|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.autotask}}|{{.status}}|{{.warning}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 系统计划任务窗口

{{range $id, $vs := $problems}}{{if eq $id "oracle.scheduler_windows"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Window_Name|Next_Start_Date|Enabled|Active|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.window_name}}|{{.next_start_date}}|{{.enabled}}|{{.active}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## Open Cursor 使用

{{range $id, $vs := $problems}}{{if eq $id "oracle.cursor_monitor"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Sid|Value|Parameter|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.sid}}|{{.value}}|{{.parameter}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

# 系统安全及审计


## 用户(sysdba)

{{range $id, $vs := $problems}}{{if eq $id "oracle.sysdba"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Username|Sysdba|Sysoper|Yesno|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.username}}|{{.sysdba}}|{{.sysoper}}|{{.yesno}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 用户信息
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.userinfo"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Username|Default_Tablespace|Temporary_Tablespace|Created|Lock_Date|Expiry_Date|Profile|Account_Status|Yesno|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.username}}|{{.default_tablespace}}|{{.temporary_tablespace}}|{{.created}}|{{.lock_date}}|{{.expiry_date}}|{{.profile}}|{{.account_status}}|{{.yesno}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.userinfo12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Username|Default_Tablespace|Temporary_Tablespace|Created|Lock_Date|Expiry_Date|Profile|Account_Status|Yesno|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.username}}|{{.default_tablespace}}|{{.temporary_tablespace}}|{{.created}}|{{.lock_date}}|{{.expiry_date}}|{{.profile}}|{{.account_status}}|{{.yesno}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 用户权限
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.userpriv"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Username|Granted_Role|Admin_Option|Default_Role|Yesno|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.username}}|{{.granted_role}}|{{.admin_option}}|{{.default_role}}|{{.yesno}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.userpriv12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Username|Granted_Role|Admin_Option|Default_Role|Yesno|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.username}}|{{.granted_role}}|{{.admin_option}}|{{.default_role}}|{{.yesno}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 审计设置
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.audit"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|User_Name|Privilege|Success|Failure|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.user_name}}|{{.privilege}}|{{.success}}|{{.failure}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.audit12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|User_Name|Privilege|Success|Failure|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.user_name}}|{{.privilege}}|{{.success}}|{{.failure}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

## 统一审计
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.unified_audit"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Parameter|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.parameter}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.unified_audit_12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Parameter|Value|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.parameter}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 统一审计设置

{{range $id, $vs := $problems}}{{if eq $id "oracle.unified_audit_option"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Parameter_Name|Parameter_Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.parameter_name}}|{{.parameter_value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## SCN 检查

{{range $id, $vs := $problems}}{{if eq $id "oracle.indicator"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Current_Scn|Indicator|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.current_scn}}|{{.indicator}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


{{range $id, $vs := $problems}}{{if eq $id "oracle.scnhealthcheck"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Key|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.key}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 比特币勒索病毒

{{range $id, $vs := $problems}}{{if eq $id "oracle.bitcoin"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Owner|Object_Name|Object_Type|Created|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.owner}}|{{.object_name}}|{{.object_type}}|{{.created}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## Profile 配置
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.profile"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Profile|Resource_Name|Resource_Type|Limit|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.profile}}|{{.resource_name}}|{{.resource_type}}|{{.limit}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}




{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.profile12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Profile|Resource_Name|Resource_Type|Limit|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.profile}}|{{.resource_name}}|{{.resource_type}}|{{.limit}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

# 系统运行状态


## 全表扫描语句
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.fullscan"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Sql_Id|Plan_Hash_Value|Total_Buffer_Gets|Total_Executions|Buffer_Get_Onetime|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.sql_id}}|{{.plan_hash_value}}|{{.total_buffer_gets}}|{{.total_executions}}|{{.buffer_get_onetime}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}



{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.fullscan12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Sql_Id|Plan_Hash_Value|Total_Buffer_Gets|Total_Executions|Buffer_Get_Onetime|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.sql_id}}|{{.plan_hash_value}}|{{.total_buffer_gets}}|{{.total_executions}}|{{.buffer_get_onetime}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## TOP 5 Event

{{if eq $version.ver 10}}{{range $id, $vs := $problems}}{{if eq $id "oracle.topevent10g"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|StartObserveTime|EndObserveTime|Event|Waits|Time|Avgwait|Pctdbtime|Waitclfass|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.starttime}}|{{.endtime}}|{{.event}}|{{.waits}}|{{.time}}|{{.avgwait}}|{{.pctdbtime}}|{{.waitclfass}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

{{if ne $version.ver 10}}{{range $id, $vs := $problems}}{{if eq $id "oracle.topevent"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|StartObserveTime|EndObserveTime|Event|Waits|Time|Avgwait|Pctdbtime|Waitclfass|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.starttime}}|{{.endtime}}|{{.event}}|{{.waits}}|{{.time}}|{{.avgwait}}|{{.pctdbtime}}|{{.waitclfass}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


## 实例运行指标

{{range $id, $vs := $problems}}{{if eq $id "oracle.efficent"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## Alert 日志
{{range $id, $vs := $problems}}{{if eq $id "oracle.awkalert"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Event|Level|
|:---|:---|
{{range .mixraw}}|{{.event}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## AWR 采样设置
{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.snapsetting"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Snap_Interval|Retention|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.snap_interval}}|{{.retention}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}



{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.snapsetting12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Xsnap_Interval|Xretention|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.xsnap_interval}}|{{.xretention}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

## DB Time 每秒

{{range $id, $vs := $problems}}{{if eq $id "oracle.db_time_per_second"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
{{LineChart .mixraw "DB Time" "/*/end_interval_time" "/*/value"}}

|End_Interval_Time|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.end_interval_time}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 统计信息收集任务运行

{{range $id, $vs := $problems}}{{if eq $id "oracle.stats_job_running"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Job_Start_Time|Job_Status|Job_Duration|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.job_start_time}}|{{.job_status}}|{{.JOB_DURATION}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 优化器统计顾问记录失效天数检查

{{if $version.v11}}{{range $id, $vs := $problems}}{{if eq $id "oracle.optimizer_stats_advisor"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Parameter_Name|Parameter_Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.parameter_name}}|{{.parameter_value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}


{{if $version.v12}}{{range $id, $vs := $problems}}{{if eq $id "oracle.optimizer_stats_advisor12c"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Parameter_Name|Parameter_Value|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.parameter_name}}|{{.parameter_value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}{{end}}

# 集群状态


## 集群状态检查
{{range $id, $vs := $problems}}{{if eq $id "oracle.crsctlstat"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Details|Level|
|:---|:---|
{{range .mixraw}}|{{.detail}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## CRS Alert 日志检查
{{range $id, $vs := $problems}}{{if eq $id "oracle.crsalert"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Event|Level|
|:---|:---|
{{range .mixraw}}|{{.line}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 节点间 LMS 进程数量

{{range $id, $vs := $problems}}{{if eq $id "oracle.lmscount"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Inst_Id|Count|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.inst_id}}|{{.count}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 节点间私网流量

{{range $id, $vs := $problems}}{{if eq $id "oracle.ges_traffic"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Inst_Id|Local_Nid|Remote_Rid|Remote_Inc|Tckt_Avail|Tckt_Limit|Tckt_Wait|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.inst_id}}|{{.local_nid}}|{{.remote_rid}}|{{.remote_inc}}|{{.tckt_avail}}|{{.tckt_limit}}|{{.tckt_wait}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## DLM 流量

{{range $id, $vs := $problems}}{{if eq $id "oracle.dlm_traffic"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Inst_Id|Local_Nid|Remote_Rid|Remote_Inc|Tckt_Avail|Tckt_Limit|Tckt_Wait|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.inst_id}}|{{.local_nid}}|{{.remote_rid}}|{{.remote_inc}}|{{.tckt_avail}}|{{.tckt_limit}}|{{.tckt_wait}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

# 系统备份


## 系统备份

{{range $id, $vs := $problems}}{{if eq $id "oracle.rman"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Date|Stat|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.date}}|{{.stat}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## DG 配置

{{range $id, $vs := $problems}}{{if eq $id "oracle.archive_dest_status"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Dest_Id|Dest_Name|Destination|Db_Unique_Name|Type|Database_Mode|Recovery_Mode|Status|Standby_Logfile_Count|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.dest_id}}|{{.dest_name}}|{{.DESTINATION}}|{{.DB_UNIQUE_NAME}}|{{.type}}|{{.DATABASE_MODE}}|{{.RECOVERY_MODE}}|{{.status}}|{{.STANDBY_LOGFILE_COUNT}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## DG 配置参数

{{range $id, $vs := $problems}}{{if eq $id "oracle.dg_parameters"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .raw}}
|参数名称|值|
|:--|:---|
{{range $kk, $vv := .raw}}|{{$vv.name}}|{{$vv.value}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## DG 日志应用

{{range $id, $vs := $problems}}{{if eq $id "oracle.dgapply"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Thread|Name|Open_Mode|Protection_Mode|Protection_Level|Database_Role|Switchover_Status|Applog|Nowlog|Yesno|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.thread}}|{{.name}}|{{.open_mode}}|{{.protection_mode}}|{{.protection_level}}|{{.database_role}}|{{.switchover_status}}|{{.applog}}|{{.nowlog}}|{{.YESNO}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## DG 应用延时

{{range $id, $vs := $problems}}{{if eq $id "oracle.dgdelay"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Process|Status|Group#|Thread#|Sequence#|Delay_Mins|Yesno|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.process}}|{{.status}}|{{.group}}|{{.thread}}|{{.sequence}}|{{.delay_mins}}|{{.YESNO}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## DG 归档缺失

{{range $id, $vs := $problems}}{{if eq $id "oracle.archive_gap"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Instance|High_Thread|Low_Lsq|High_Hsq|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.instance}}|{{.high_thread}}|{{.low_lsq}}|{{.high_hsq}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## DG 相关日志信息

{{range $id, $vs := $problems}}{{if eq $id "oracle.dataguard_stats"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Name|Value|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



{{range $id, $vs := $problems}}{{if eq $id "oracle.dataguard_status"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Inst_Id|Timestamp|Dest_Id|Error_Code|Message|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.inst_id}}|{{.timestamp}}|{{.dest_id}}|{{.error_code}}|{{.message}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 归档日生成量

{{range $id, $vs := $problems}}{{if eq $id "oracle.archsize"}}{{range $k, $v := $vs}}
{{if gt $summary.instArrCount 1}}### {{$v._sid}}{{if ne $v.level "正常"}}【{{$v.level}}】{{end}}{{end}}
 
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
{{LineChart .mixraw "归档日生成量" "/*/first_time" "/*/size"}}

|First_Time|Size|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.first_time}}|{{.size}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


{{end}}
{{end}}