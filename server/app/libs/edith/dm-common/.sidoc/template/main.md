{{define "main"}}

{{$problems := GroupBy .problems "id"}}
{{$summary := JsCall "func.summary" .problems}}
{{$appnames := .meta.config.appnames}}


---
title: {{.meta.customer}} {{.meta.title}}
subtitle: {{if .meta.sys}}{{.meta.sys}}{{else}}{{range .SysConfs}}{{JsCall "func.appname" .host.hostname}}{{end}}{{end}}
author:
- 巡检工程师：{{ .meta.author.name}}
- {{ .meta.org}}

date: {{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}
---

# 文档版本信息

|版本|日期|作者|说明&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}|{{ .meta.author.name}} |初稿|
|||||

# 巡检总结和建议

## 巡检信息概述
{{println ""}}主机名：{{if .SysConfs}}{{range .SysConfs}}{{printf "%-13s" .host.hostname}}{{end}}{{else}}{{range .OracleConfs}}{{index .host "hostname"}} {{end}}{{end}}
{{println ""}}数据库实例：{{range .DMDB}}{{index .port}} {{end}}
{{println ""}}巡检工程师：{{ .meta.author.name}}
{{println ""}}巡检时间：{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}

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

|配置项|值|
|:---|:---|
{{range $k,$v := .base}}{{if ne $k "_check"}}|{{$k}}|{{$v}}|
{{end}}{{end}}

{{end}}
{{else}}
{{range .PostgreSQL}}

|配置项|值|
|:---|:---|
{{range $k,$v := .host}}{{if ne $k "_check"}}|{{$k}}|{{$v}}|
{{end}}{{end}}

{{end}}
{{end}}

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



# 数据库总体概况

## 表空间检查

### 表空间信息

{{range $k, $v := .problems}}{{if eq $v.id "dm.tableInfo"}}
|表空间名称|表空间大小(M)|表空间使用大小(M)|表空间剩余大小(M)|使用率|
|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.TablespaceName}}|{{.Total}}|{{.Used}}|{{.Free}}|{{.UsageRate}}%|
{{end}}
{{end}}{{end}}



### 数据文件信息

{{range $k, $v := .problems}}{{if eq $v.id "dm.dataDocInfo"}}
|文件路径|创建时间|空闲页数|剩余空间|LastCKPTTime|最大空间|镜像路径|修改时间|
|:---|:---|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.Path}}|{{.CreateTime}}|{{.FreePageNo}}|{{.FreeSize}}|{{.LastCKPTTime}}|{{.MaxSize}}|{{.MirrorPath}}|{{.ModifyTime}}|
{{end}}
{{end}}{{end}}



## 死锁与阻塞检查

### 死锁历史信息记录
{{range $k, $v := .problems}}{{if eq $v.id "dm.deadlockHistory"}}
|SeqNo|TrxId|SessId|SessSeq|SqlText|HappenTime|
|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.SeqNo}}|{{.TrxId}}|{{.SessId}}|{{.SessSeq}}|{{.SqlText}}|{{.HappenTime}}|
{{end}}
{{end}}{{end}}

### 阻塞

{{range $k, $v := .problems}}{{if eq $v.id "dm.block"}}
|StatTime|WtTrxId|BlkTrxId|Blocked|WtTable|WtSess|BlkSess|WtUserName|BlkUserName|SqlText|CLntIp|SS|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.StatTime}}|{{.WtTrxId}}|{{.BlkTrxId}}|{{.Blocked}}|{{.WtTable}}|{{.WtSess}}|{{.BlkSess}}|{{.WtUserName}}|{{.BlkUserName}}|{{.SqlText}}|{{.CLntIp}}|{{.SS}}|
{{end}}
{{end}}{{end}}


## 内存池信息检查
### 字典缓存
{{range $k, $v := .problems}}{{if eq $v.id "dm.dictionaryCache"}}
|PoolId|TotalSize|UsedSize|DictNum|SizeLruDiscard|LruDiscard|DdlDiscard|DisabledSize|DisabledDictNum|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.PoolId}}|{{.TotalSize}}|{{.UsedSize}}|{{.DictNum}}|{{.SizeLruDiscard}}|{{.LruDiscard}}|{{.DdlDiscard}}|{{.DisabledSize}}|{{.DisabledDictNum}}|
{{end}}
{{end}}{{end}}

### 数据缓冲池
{{range $k, $v := .problems}}{{if eq $v.id "dm.bufferPool"}}
|Id|Name|PageSize|NPages|NFixed|Free|NDirty|NClear|NTotalPages|NMaxPages|NLogicReads|NDiscard|NPhyReads|NPhyMReads|RatHit|NExpBufferPool|NUpdRemove|NPhyWrite|NUpdPut|NUpdSearch|NDiscard64|NPhyReads64|NPhyMReads64|NUpdRemove64|NPhyWrite64|NUpdPut64|NUpdSearch64|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.Id}}|{{.Name}}|{{.PageSize}}|{{.NPages}}|{{.NFixed}}|{{.Free}}|{{.NDirty}}|{{.NClear}}|{{.NTotalPages}}|{{.NMaxPages}}|{{.NLogicReads}}|{{.NDiscard}}|{{.NPhyReads}}|{{.NPhyMReads}}|{{.RatHit}}|{{.NExpBufferPool}}|{{.NUpdRemove}}|{{.NPhyWrite}}|{{.NUpdPut}}|{{.NUpdSearch}}|{{.NDiscard64}}|{{.NPhyReads64}}|{{.NPhyMReads64}}|{{.NUpdRemove64}}|{{.NPhyWrite64}}|{{.NUpdPut64}}|{{.NUpdSearch64}}|
{{end}}
{{end}}{{end}}

### 内存池
{{range $k, $v := .problems}}{{if eq $v.id "dm.memoryPool"}}
|Addr|Name|IsShared|ChkMagic|ChkLeak|IsOverFlow|IsDsaItem|OrgSize|TotalSize|ReservedSize|DataSize|ExtendSize|TargetSize|ExtendLen|NAlloc|NExtendNormal|NExtendExclusive|NFree|MaxExtendSize|MinExtendSize|FileName|FileLine|Creator|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.Addr}}|{{.Name}}|{{.IsShared}}|{{.ChkMagic}}|{{.ChkLeak}}|{{.IsOverFlow}}|{{.IsDsaItem}}|{{.OrgSize}}|{{.TotalSize}}|{{.ReservedSize}}|{{.DataSize}}|{{.ExtendSize}}|{{.TargetSize}}|{{.ExtendLen}}|{{.NAlloc}}|{{.NExtendNormal}}|{{.NExtendExclusive}}|{{.NFree}}|{{.MaxExtendSize}}|{{.MinExtendSize}}|{{.FileName}}|{{.FileLine}}|{{.Creator}}|
{{end}}
{{end}}{{end}}


## 数据库统计信息检查
### 系统统计信息
{{range $k, $v := .problems}}{{if eq $v.id "dm.systemStatistics"}}
|Id|ClassId|Name|StatVal|
|:---|:---|:---|:---|
|{{range $v.raw}}{{.Id}}|{{.ClassId}}|{{.Name}}|{{.StatVal}}|
{{end}}
{{end}}{{end}}

### 会话统计
{{range $k, $v := .problems}}{{if eq $v.id "dm.sessionStatistics"}}
|State|CLntIp|CLntType|CurrSch|UserName|Counts|
|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.State}}|{{.CLntIp}}|{{.CLntType}}|{{.CurrSch}}|{{.UserName}}|{{.Counts}}|
{{end}}
{{end}}{{end}}

### 对象统计
{{range $k, $v := .problems}}{{if eq $v.id "dm.objectStatistics"}}
|TablespaceName|ObjType|Counts|
|:---|:---|:---|
|{{range $v.raw}}{{.TablespaceName}}|{{.ObjType}}|{{.Counts}}|
{{end}}
{{end}}{{end}}

### 表行数统计
{{range $k, $v := .problems}}{{if eq $v.id "dm.tableRowStatistics"}}
|Owner|TableName|TablespaceName|Status|NumRows|
|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.Owner}}|{{.TableName}}|{{.TablespaceName}}|{{.Status}}|{{.NumRows}}|
{{end}}
{{end}}{{end}}

### DBLINK 统计
{{range $k, $v := .problems}}{{if eq $v.id "dm.dbLinkStatistics"}}
|Owner|DbLink|UserName|Host|Created|
|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.Owner}}|{{.DbLink}}|{{.UserName}}|{{.Host}}|{{.Created}}|
{{end}}
{{end}}{{end}}

### 高内存的20条SQL
{{range  .problems}}{{if eq .id "dm.highMemory20SQL"}}
|SqlID|SqlText|
|:---|:---|
|{{range .raw}}{{.SqlID}}|{{.SqlText}}|
{{end}}
{{end}}{{end}}

### 最慢的 20 条 SQL 统计
{{range $k, $v := .problems}}{{if eq $v.id "dm.slowest20SQL"}}
|StartTime|TimeUsed|TopSqlText|
|:---|:---|:---|
|{{range $v.raw}}{{.StartTime}}|{{.TimeUsed}}|{{.TopSqlText}}|
{{end}}
{{end}}{{end}}

### 前20条长耗时等待事件统计
{{range $k, $v := .problems}}{{if eq $v.id "dm.longtime20Events"}}
|EventId|Event|TotalWaits|TimeWaited|TimeWaitedMicro|AverageWaitMicro|SMaxTime|SMinTime|WaitClassId|WaitClass|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.EventId}}|{{.Event}}|{{.TotalWaits}}|{{.TimeWaited}}|{{.TimeWaitedMicro}}|{{.AverageWaitMicro}}|{{.SMaxTime}}|{{.SMinTime}}|{{.WaitClassId}}|{{.WaitClass}}|
{{end}}
{{end}}{{end}}

## 安全性设置检查
### 用户信息
{{range $k, $v := .problems}}{{if eq $v.id "dm.userinfo"}}
|UserName|UserId|PassWord|AccountStatus|LockDate|ExpiryDate|DefaultTablespace|DefaultIndexTablespace|TemporaryTablespace|Created|Profile|InitialRSrcConsumerGroup|ExternalName|PasswordVersions|EditionsEnabled|AuthenticationType|NowDate|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.UserName}}|{{.UserId}}|{{.PassWord}}|{{.AccountStatus}}|{{.LockDate}}|{{.ExpiryDate}}|{{.DefaultTablespace}}|{{.DefaultIndexTablespace}}|{{.TemporaryTablespace}}|{{.Created}}|{{.Profile}}|{{.InitialRSrcConsumerGroup}}|{{.ExternalName}}|{{.PasswordVersions}}|{{.EditionsEnabled}}|{{.AuthenticationType}}|{{.NowDate}}|
{{end}}
{{end}}{{end}}

### 密码策略
{{range $k, $v := .problems}}{{if eq $v.id "dm.passwordStrategy"}}
|ParaName|ParaValue|MinValue|MaxValue|DefaultValue|MppChk|SessValue|FileValue|Description|ParaType|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|{{range $v.raw}}{{.ParaName}}|{{.ParaValue}}|{{.MinValue}}|{{.MaxValue}}|{{.DefaultValue}}|{{.MppChk}}|{{.SessValue}}|{{.FileValue}}|{{.Description}}|{{.ParaType}}|
{{end}}
{{end}}{{end}}

## 日志健康检查
### 数据库实例日志
{{range $k, $v := .problems}}{{if eq $v.id "dm.instanceLogs"}}
{{range $v.raw}}
#### {{.Path}}
| ErrorTime                               |Location|ExecP|ExecT|Content|
|:----------------------------------------|:---|:---|:---|:---|
| {{range .ErrorInstances}}{{.ErrorTime}} |{{.Location}}|{{.ExecP}}|{{.ExecT}}|{{.Content}}|
{{end}}
{{end}}
{{end}}{{end}}


### DMAP 进程日志
{{range $k, $v := .problems}}{{if eq $v.id "dm.dampLogs"}}
{{range $v.raw}}
#### {{.Path}}
| ErrorTime                               |Location|ExecP|ExecT|Content|
|:----------------------------------------|:---|:---|:---|:---|
| {{range .ErrorDamps}}{{.ErrorTime}} |{{.Location}}|{{.ExecP}}|{{.ExecT}}|{{.Content}}|
{{end}}
{{end}}
{{end}}{{end}}

### 数据库备份日志
{{range $k, $v := .problems}}{{if eq $v.id "dm.backupLogs"}}
{{range $v.raw}}
#### {{.Path}}
| ErrorTime                               |Location|ExecP|ExecT|Content|
|:----------------------------------------|:---|:---|:---|:---|
| {{range .ErrorBackups}}{{.ErrorTime}} |{{.Location}}|{{.ExecP}}|{{.ExecT}}|{{.Content}}|
{{end}}
{{end}}
{{end}}{{end}}

{{end}}