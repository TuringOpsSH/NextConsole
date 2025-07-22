{{define "main"}}

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

|版本|日期|作者|说明&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}|{{ .meta.author.name}} |初稿|
|||||

# 巡检总结和建议

## 巡检信息概述 


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


# 基础巡检
## 服务器信息

{{range $id, $vs := $problems}}{{if eq $id "sqlserver.server_information"}}{{range $k, $v := $vs}}

|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Id|Name|Value|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.id}}|{{.name}}|{{.value}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

最大服务器内存建议： SQL Server数据库内存的使用由SQL OS分配和控制，主要分为数据缓冲区和非数据缓冲区。前者包括读缓冲区和写缓冲区，后者包括执行计划、SQL CLR、代理作业等对内存的使用。在SQL Server Management Studio中设置的内存主要是数据缓冲区，一般建议预留5-10G内存。
CPU最大并行度建议：多个CPU可以并行执行一个大的查询操作，从而提高响应速度。但是同时会造成CPU的占用，而阻塞其他查询操作。微软的最佳实践中建议在系统CPU总核数不超过8时，CPU最大并行度设置为0，即不做限制；当CPU总核数超过8时，CPU最大并行度设置为8，对于OLTP系统CPU最大并行度设置为1也可以，既不允许并行计算。


## CPU信息

|检查项|检查内容及结论|风险|建议|值|
|:---|:---|:---|:---|:--|
| CPU核数   |{{range $id, $vs := $problems}} {{if eq $id "sqlserver.cpu_count"}}{{range $k, $v := $vs}} {{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}} |{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}| {{if .mixraw}} {{range .mixraw}}{{.cpu_cores}}{{end}}{{end}}{{end}}{{end}}{{end}}              |
| CPU物理个数   |{{range $id, $vs := $problems}} {{if eq $id "sqlserver.cpu_physic_count"}}{{range $k, $v := $vs}} {{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}} |{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}| {{if .mixraw}} {{range .mixraw}}{{.number_of_physical_cpus}}{{end}}{{end}}{{end}}{{end}}{{end}}|
| CPU型号   |{{range $id, $vs := $problems}} {{if eq $id "sqlserver.cpu_type"}}{{range $k, $v := $vs}} {{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}} |{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}| {{if .mixraw}} {{range .mixraw}}{{.cpu_model}}{{end}}{{end}}{{end}}{{end}}{{end}}              |


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

## 磁盘剩余空间
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.volume_available"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Drive_Letter|File_System|Total_Size|Available_Size|Disk_Usage_Rate|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.drive_letter}}|{{.file_system}}|{{.total_size}}|{{.available_size}}|{{.disk_usage_rate}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 物理内存大小
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.physical_memory"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|
|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|

{{if .mixraw}}
|Physical_Memory|
|:---|
{{range .mixraw}}|{{.physical_memory}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 内存使用率
{{range $id, $vs := $problems}}{{if eq $id "linux.memUsedPercent"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|


{{if .mixraw}}
|Total(MB)|Used(MB)|UsedPercent|Level|
|:---|:---|:---|
{{range .mixraw}}|{{JsCall "func.byte2mb" .total}}|{{JsCall "func.byte2mb" .used}}|{{.usedPercent}}%|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 当前连接数
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.process"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Process_Count|Level|
|:---|:---|
{{range .mixraw}}|{{.process_count}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## SQLServer的版本
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.sql_version"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Sql_Version|Level|
|:---|:---|
{{range .mixraw}}|{{.sql_version}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## SQLServer的补丁
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.patch_version"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Patch|Level|
|:---|:---|
{{range .mixraw}}|{{.database_patch}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## Windows系统磁盘空闲率
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.system_disk_idle_rate"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Dname|Free_Mb|Free_Gb|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.dname}}|{{.free_mb}}|{{.free_gb}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 服务器错误日志
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.server_error_log"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Logdate|Loginfo|Count|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.logdate}}|{{.loginfo}}|{{.count}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据库完整备份检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_full_backup"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Database_Recovery_Mode|Backup_Type|Last_Backup_Time|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.database_recovery_mode}}|{{.backup_type}}|{{.last_backup_time}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 无备份的数据库
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.database_without_backup"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Last_Full_Backup|Recovery_Model_Desc|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}||{{.last_full_backup}}|{{.recovery_model_desc}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据库事务日志备份检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_log_backup"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Database_Recovery_Mode|Backup_Type|Last_Backup_Time|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.database_recovery_mode}}|{{.backup_type}}|{{.last_backup_time}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 近一周所有数据库备份信息
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.all_database_backup_information_in_the_past_week"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Server_Name|User_Name|Database_Name|Bak_Start_Time|Bak_End_Time|Bak_Time_Seconds|Bak_Files|Bak_File_Available|Bak_Type|Bak_Size_Mb|Compressed_Size_Mb|First_Lsn|Last_Lsn|Checkpoint_Lsn|Database_Backup_Lsn|Software_Major_Version|Software_Minor_Version|Software_Build_Version|Recovery_Model|Collation_Name|Database_Version|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.server_name}}|{{.user_name}}|{{.database_name}}|{{.bak_start_time}}|{{.bak_end_time}}|{{.bak_time_seconds}}|{{.bak_files}}|{{.bak_file_available}}|{{.bak_type}}|{{.bak_size_mb}}|{{.compressed_size_mb}}|{{.first_lsn}}|{{.last_lsn}}|{{.checkpoint_lsn}}|{{.database_backup_lsn}}|{{.software_major_version}}|{{.software_minor_version}}|{{.software_build_version}}|{{.recovery_model}}|{{.collation_name}}|{{.database_version}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据库日志大小和使用率检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_log_size"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Total_Log_Size|Log_Space_Usage|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.total_log_size}}|{{.log_space_usage}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 数据库最大内存配置
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_max_memory"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|
|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|

{{if .mixraw}}
|Database_Maximum_Memory_Configuration|
|:---|
{{range .mixraw}}|{{.database_maximum_memory_configuration}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据库最小内存配置
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_min_memory"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|
|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|

{{if .mixraw}}
|Database_Minimum_Memory_Configuration|
|:---|
{{range .mixraw}}|{{.database_minimum_memory_configuration}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 数据库的读写模式
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_read_write_model"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Database_Read_And_Write_Mode|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.database_read_and_write_mode}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据库恢复模式检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_recovery_model"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Recovery_Mode|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.recovery_mode}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 实例的排序规则
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.instance_collation"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Sorting_Rules_For_Instances|Level|
|:---|:---|
{{range .mixraw}}|{{.sorting_rules_for_instances}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 数据库启动参数
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_startup_parameters"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Configuration_Id|Name|Value|Minimum|Maximum|Value_In_Use|Description|Is_Dynamic|Is_Advanced|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.configuration_id}}|{{.name}}|{{.value}}|{{.minimum}}|{{.maximum}}|{{.value_in_use}}|{{.description}}|{{.is_dynamic}}|{{.is_advanced}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 所有数据库
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.all_database_object_information"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Database_Id|Database_Name|Create_Date|Recovery_Model_Desc|Collation_Name|User_Access_Desc|State_Desc|Create_Stats_On|Update_Stats_On|Close_On|Shrink_On|Update_Stats_Async_On|Compatibility_Level|Log_Reuse_Wait_Desc|Page_Verify_Option_Desc|Is_Cdc_Enabled|Td|Mirroring_State|Data_File_Size_Mb|Log_Size_Mb|Database_Size_Mb|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_id}}|{{.database_name}}|{{.create_date}}|{{.recovery_model_desc}}|{{.collation_name}}|{{.user_access_desc}}|{{.state_desc}}|{{.create_stats_on}}|{{.update_stats_on}}|{{.close_on}}|{{.shrink_on}}|{{.update_stats_async_on}}|{{.compatibility_level}}|{{.log_reuse_wait_desc}}|{{.page_verify_option_desc}}|{{.is_cdc_enabled}}|{{.td}}|{{.mirroring_state}}|{{.data_file_size_mb}}|{{.log_size_mb}}|{{.database_size_mb}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 各个数据库的对象情况
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.object_status_of_each_database"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Xtype|Cnt|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.xtype}}|{{.cnt}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 表行数
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.table_rows"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Table_Schema|Table_Name|Tb_Rows|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.table_schema}}|{{.table_name}}|{{.tb_rows}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 排序规则检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.collation"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Name|Desc|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.desc}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}




## 数据库的排序规则
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.database_collation"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Sort_Rule_Name|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.sort_rule_name}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据库上次重启时间
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.dbstart_time"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Last_Server_Restart_Time|Level|
|:---|:---|
{{range .mixraw}}|{{.last_server_restart_time}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据库的状态
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.dbstate"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|State|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.state}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}






## 数据库服务检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_service_check"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Service_Name|Activate_The_Account|Start_Mode|Startup_Status|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.service_name}}|{{.activate_the_account}}|{{.start_mode}}|{{.startup_status}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}






## 临时数据库使用情况
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.temporary_database_usage"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|User_Objects_Kb|Internal_Objects_Kb|Version_Store_Kb|Freespace_Kb|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.user_objects_kb}}|{{.internal_objects_kb}}|{{.version_store_kb}}|{{.freespace_kb}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据库大小和使用率检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_size"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Database_Total_Size|Unallocated|Space_Usage|db_max_size|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.database_total_size}}|{{.unallocated}}|{{.space_usage}}|{{.db_max_size}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## Tempdb健康检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.tempdb_check"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Number_Of_Tempdb_Data_Files|Level|
|:---|:---|
{{range .mixraw}}|{{.number_of_tempdb_data_files}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 查看各数据库Bufferpool使用情况
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.view_the_usage_of_bufferpools_in_various_databases"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Buffer_Pool_Rank|Database_Name|Cachedsize_Mb|Buffer_Pool_Percent|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.buffer_pool_rank}}|{{.database_name}}|{{.cachedsize_mb}}|{{.buffer_pool_percent}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 作业状态和所有者检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.agent_state"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Job_Name|Job_Owner|Job_Status|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.job_name}}|{{.job_owner}}|{{.job_status}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 查看失败的job
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.view_failed_jobs"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Name|Enabled|Last_Run_Outcome|Database_Name|Step_Id|Step_Name|Command|Last_Run_Duration|Last_Run_Date|Next_Run_Date|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.enabled}}|{{.last_run_outcome}}|{{.database_name}}|{{.step_id}}|{{.step_name}}|{{.command}}|{{.last_run_duration}}|{{.last_run_date}}|{{.next_run_date}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 查看job执行情况
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.view_job_execution_status"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Name|Start_Execution_Date|Stop_Execution_Date|Run_Status|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.start_execution_date}}|{{.stop_execution_date}}|{{.run_status}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 最近一周执行较慢的作业
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.executing_slower_in_past_week"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Name|Start_Execution_Date|Executedmin|Avgruntimeonsuccee|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.start_execution_date}}|{{.executedmin}}|{{.avgruntimeonsuccee}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 所有数据库文件信息
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.all_database_file_information"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Database_Name|File_Id|File_Name|File_Path|File_Type|File_Status|Pct_Increase|Growth|Size_Mb|Avg_Read|Avg_Write|Io_Stall_Read_Ms|Num_Of_Reads|Io_Stall_Write_Ms|Num_Of_Writes|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.file_id}}|{{.file_name}}|{{.file_path}}|{{.file_type}}|{{.file_status}}|{{.pct_increase}}|{{.growth}}|{{.size_mb}}|{{.avg_read}}|{{.avg_write}}|{{.io_stall_read_ms}}|{{.num_of_reads}}|{{.io_stall_write_ms}}|{{.num_of_writes}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 临时数据库文件情况
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.temporary_database_file_status"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Filename|Filesizeinmb|Max_Size|Growth|Growthvalue|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.filename}}|{{.filesizeinmb}}|{{.max_size}}|{{.growth}}|{{.growthvalue}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据库文件的存放位置
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.filepath"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|File_Name|File_Type|Storage_Location|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.file_name}}|{{.file_type}}|{{.storage_location}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 数据文件的状态
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.filestate"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|File_Name|File_Type|File_Status|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.file_name}}|{{.file_type}}|{{.file_status}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 文件增长类型检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.file_growth_type"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|File_Name|File_Type|Growth_Type|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.file_name}}|{{.file_type}}|{{.growth_type}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}




## 检查具有sysadmin权限的用户
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.check_users_with_sysadmin_privileges"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Name|Sysadmin|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.sysadmin}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 检查是否使用了密码策略
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.check_if_password_policy_is_used"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Name|Is_Policy_Checked|Is_Expiration_Checked|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.is_policy_checked}}|{{.is_expiration_checked}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 检查是否开启了审计
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.check_if_auditing_has_been_enabled"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Name|Is_State_Enabled|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.is_state_enabled}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 统计信息情况检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.statistical_information_inspection"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Db_Name|Result|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.db_name}}|{{.result}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



# 数据库用户


## 数据库用户访问设置
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_single_multi_user"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Database_User_Access_Settings|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.database_user_access_settings}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 空密码用户、密码与用户名相同
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.empty_password_user_password_is_the_same_as_username"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Type|Username|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.type}}|{{.username}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 用户和进程详情
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.user_and_process_details"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Spid|Status|Loginame|Dbname|Cpu|Physical_Io|Login_Time|Last_Batch|Hostname|Cmd|Blocked|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.spid}}|{{.status}}|{{.loginame}}|{{.dbname}}|{{.cpu}}|{{.physical_io}}|{{.login_time}}|{{.last_batch}}|{{.hostname}}|{{.cmd}}|{{.blocked}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 活跃的用户进程及数量
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.active_user_processes_and_quantity"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Loginame|Status|Count|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.loginame}}|{{.status}}|{{.count}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}














## 用户和角色
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.users_and_roles"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|User_Id|User_Status|Username|Role_Id|Role_Status|Rolename|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.user_id}}|{{.user_status}}|{{.username}}|{{.role_id}}|{{.role_status}}|{{.rolename}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}




## 数据库所有者检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_owner"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Owner|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.owner}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}




# 数据库性能


## 数据库读写比
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.db_read_write"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Number_Of_Readings|Write_Times|Reading_Proportion|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.number_of_readings}}|{{.write_times}}|{{.reading_proportion}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 每个数据库文件的平均读写阻塞时间
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.average_readwrite_blocking_time_per_database_file"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Database_Name|Avg_Read_Stall_Ms|Avg_Write_Stall_Ms|File_Size_Mb|Physical_Name|Type_Desc|Io_Stall_Read_Ms|Num_Of_Reads|Io_Stall_Write_Ms|Num_Of_Writes|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.avg_read_stall_ms}}|{{.avg_write_stall_ms}}|{{.file_size_mb}}|{{.physical_name}}|{{.type_desc}}|{{.io_stall_read_ms}}|{{.num_of_reads}}|{{.io_stall_write_ms}}|{{.num_of_writes}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## I/0读响应时间检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.IO_read_time"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Drive_Letter|Database_Name|File_Name|Total_Number_Of_Reads|_Average_Response_Time_Per_Read(ms)|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.drive_letter}}|{{.database_name}}|{{.file_name}}|{{.total_number_of_reads}}|{{._average_response_time_per_read}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## I/0写响应时间检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.IO_write_time"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|_Drive_Letter|Database_Name|File_Name|Total_Number_Of_Write|_Average_Response_Time_Per_Write(ms)|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{._drive_letter}}|{{.database_name}}|{{.file_name}}|{{.total_number_of_reads}}|{{._average_response_time_per_write}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 数据库服务器磁盘IO和CPU统计信息
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.database_server_disk_io_and_cpu_statistics"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Total_Read|Total_Write|Total_Errors|Io_Busy|Timeticks|Io_Operation|Cpu_Busy|Cpu_Working|Cpu_Idle|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.total_read}}|{{.total_write}}|{{.total_errors}}|{{.io_busy}}|{{.timeticks}}|{{.io_operation}}|{{.cpu_busy}}|{{.cpu_working}}|{{.cpu_idle}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## CPU瓶颈
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.cpu_bottleneck"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Scheduler_Id|Current_Tasks_Count|Runnable_Tasks_Count|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.scheduler_id}}|{{.current_tasks_count}}|{{.runnable_tasks_count}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 日志碎片检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.loginfo_check"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|Inspection_Results|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.inspection_results}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 最大工作线程数检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.maxworkers"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Max_Workers_Count|Level|
|:---|:---|
{{range .mixraw}}|{{.max_workers_count}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## CPU最大并行度
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.max_parallelism_degree"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Cpu_Maximum_Parallelism|Level|
|:---|:---|
{{range .mixraw}}|{{.cpu_maximum_parallelism}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 无效视图检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.invalid_view"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Database_Name|View_Name|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.database_name}}|{{.view_name}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 没有主键的表
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.tables_without_primary_keys"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|Table_Catalog|Table_Schema|Table_Name|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.table_catalog}}|{{.table_schema}}|{{.table_name}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 所有数据库高开销的缺失索引
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.high_cost_missing_indexes_for_all_databases"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Total_Cost|Avg_User_Impact|Statement|Equality_Columns|Inequality_Columns|Included_Columns|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.total_cost}}|{{.avg_user_impact}}|{{.statement}}|{{.equality_columns}}|{{.inequality_columns}}|{{.included_columns}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## CPU平均占用率最高的前10个SQL语句
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.top_10_sql_with_the_highest_average_cpu_usage"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Avg_Cpu_Time|Total_Elapsed_Time|Total_Worker_Time|Execution_Count|Creation_Time|Last_Execution_Time|Query_Text|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.avg_cpu_time}}|{{.total_elapsed_time}}|{{.total_worker_time}}|{{.execution_count}}|{{.creation_time}}|{{.last_execution_time}}|{{.query_text}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 前10个缓存使用率高最消耗缓存的SQL语句
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.top_10_sql_statements_with_high_cache_usage_and_the_highest_cache_consumption"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Usecounts|Objtype|Size_In_Bytes|Text|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.usecounts}}|{{.objtype}}|{{.size_in_bytes}}|{{.text}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 死锁检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.deadlock"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|

{{if .mixraw}}
|The_Total_Number_Of_Occurrences_Of_Deadlocks|Average_Number_Of_Occurrences_Per_Day|Level|
|:---|:---|:---|
{{range .mixraw}}|{{.the_total_number_of_occurrences_of_deadlocks}}|{{.average_number_of_occurrences_per_day}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 数据库里的锁情况
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.locks_in_the_database"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Request_Session_Id|Db_Name|Obj_Name|Resource_Description|Request_Type|Request_Status|Request_Mode|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.request_session_id}}|{{.db_name}}|{{.obj_name}}|{{.resource_description}}|{{.request_type}}|{{.request_status}}|{{.request_mode}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 计算资源等待和信号量等待时间
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.calculate_resource_wait_and_semaphore_wait_times"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Signal_Cpu_Waits(%)|Resource_Waits|Level(%)|
|:---|:---|:---|
{{range .mixraw}}|{{.signal_cpu_waits}}|{{.resource_waits}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 阻塞的会话
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.blocked_session"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Blocking_Session_Id|Wait_Duration_Ms|Session_Id|Level|
|:---|:---|:---|:---|
{{range .mixraw}}|{{.blocking_session_id}}|{{.wait_duration_ms}}|{{.session_id}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 查看所有数据库的索引碎片信息
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.view_index_fragmentation_information_for_all_databases"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Databasename|Schemaname|Tablename|Indexname|Averagefragmentation|Fragmentationseverity|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.DatabaseName}}|{{.SchemaName}}|{{.TableName}}|{{.IndexName}}|{{.AverageFragmentation}}|{{.FragmentationSeverity}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 查看索引空间大于100M的索引信息
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.view_index_information_with_an_index_space_greater_than_100m"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Databasename|Schemaname|Tablename|Indexname|Indexspacemb|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.DatabaseName}}|{{.SchemaName}}|{{.TableName}}|{{.IndexName}}|{{.IndexSpaceMB}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}




# 高可用


## 镜像服务器
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.mirror_server"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Name|Database_Id|Mr_State_Desc|Mr_Role_Desc|Mr_Safety_Level_Desc|Mr_Partner_Name|Mr_Partner_Instance|Mr_Witness_Name|Mr_Witness_State_Desc|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.name}}|{{.database_id}}|{{.mr_state_desc}}|{{.mr_role_desc}}|{{.mr_safety_level_desc}}|{{.mr_partner_name}}|{{.mr_partner_instance}}|{{.mr_witness_name}}|{{.mr_witness_state_desc}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 集群参数检查
{{range $id, $vs := $problems}}{{if eq $id "os.clusterfl"}}{{range $k, $v := $vs}}
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


## 集群状态检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.cluster_status_check"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Cluster_Name|Quorum_Type_Desc|Quorum_State_Desc|Hostname|Servername|Serverip|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.cluster_name}}|{{.quorum_type_desc}}|{{.quorum_state_desc}}|{{.hostname}}|{{.servername}}|{{.serverip}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 集群信息检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.cluster_info_check"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Member_Name|Member_Type_Desc|Member_State_Desc|Number_Of_Quorum_Votes|Level|
|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.member_name}}|{{.member_type_desc}}|{{.member_state_desc}}|{{.number_of_quorum_votes}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## winodws集群信息
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.win_cluster_information"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Cluster_Name|Quorum_Type|Quorum_Type_Desc|Quorum_State|Quorum_State_Desc|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.cluster_name}}|{{.quorum_type}}|{{.quorum_type_desc}}|{{.quorum_state}}|{{.quorum_state_desc}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## winodws集群信息members
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.win_cluster_members_information"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Member_Name|Member_Type|Member_Type_Desc|Member_State|Member_State_Desc|Number_Of_Quorum_Votes|Level|
|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.member_name}}|{{.member_type}}|{{.member_type_desc}}|{{.member_state}}|{{.member_state_desc}}|{{.number_of_quorum_votes}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## AG信息及状态检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.ag_information_and_status_check"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Groupname|Replica|Role|Health_Check_Timeout_Ms|Failure_Condition_Level|Availabilitymode|Primary_Recovery_Health_Desc|Secondary_Recovery_Health_Desc|Failovermode|Recovery_Health_Desc|Synchronization_Health_Desc|Seedingmode|Endpointurl|Listener|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.GroupName}}|{{.Replica}}|{{.Role}}|{{.health_check_timeout_ms}}|{{.failure_condition_level}}|{{.AvailabilityMode}}|{{.primary_recovery_health_desc}}|{{.secondary_recovery_health_desc}}|{{.FailoverMode}}|{{.recovery_health_desc}}|{{.synchronization_health_desc}}|{{.SeedingMode}}|{{.EndpointURL}}|{{.Listener}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 集群AG属性检查groups
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.ag_property_groups"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Group_Id|Name|Resource_Id|Resource_Group_Id|Failure_Condition_Level|Health_Check_Timeout|Automated_Backup_Preference|Automated_Backup_Preference_Desc|Version|Basic_Features|Dtc_Support|Db_Failover|Is_Distributed|Cluster_Type|Cluster_Type_Desc|Required_Synchronized_Secondaries_To_Commit|Sequence_Number|Is_Contained|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.group_id}}|{{.name}}|{{.resource_id}}|{{.resource_group_id}}|{{.failure_condition_level}}|{{.health_check_timeout}}|{{.automated_backup_preference}}|{{.automated_backup_preference_desc}}|{{.version}}|{{.basic_features}}|{{.dtc_support}}|{{.db_failover}}|{{.is_distributed}}|{{.cluster_type}}|{{.cluster_type_desc}}|{{.required_synchronized_secondaries_to_commit}}|{{.sequence_number}}|{{.is_contained}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}

## 集群AG属性检查replicas
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.ag_property_replicas"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Replica_Id|Group_Id|Replica_Metadata_Id|Replica_Server_Name|Owner_Sid|Endpoint_Url|Availability_Mode|Availability_Mode_Desc|Failover_Mode|Failover_Mode_Desc|Session_Timeout|Primary_Role_Allow_Connections|Primary_Role_Allow_Connections_Desc|Secondary_Role_Allow_Connections|Secondary_Role_Allow_Connections_Desc|Create_Date|Modify_Date|Backup_Priority|Read_Only_Routing_Url|Seeding_Mode|Seeding_Mode_Desc|Read_Write_Routing_Url|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.replica_id}}|{{.group_id}}|{{.replica_metadata_id}}|{{.replica_server_name}}|{{.owner_sid}}|{{.endpoint_url}}|{{.availability_mode}}|{{.availability_mode_desc}}|{{.failover_mode}}|{{.failover_mode_desc}}|{{.session_timeout}}|{{.primary_role_allow_connections}}|{{.primary_role_allow_connections_desc}}|{{.secondary_role_allow_connections}}|{{.secondary_role_allow_connections_desc}}|{{.create_date}}|{{.modify_date}}|{{.backup_priority}}|{{.read_only_routing_url}}|{{.seeding_mode}}|{{.seeding_mode_desc}}|{{.read_write_routing_url}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}


## 监听器信息检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.listener_message"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Group_Id|Name|Resource_Id|Resource_Group_Id|Failure_Condition_Level|Health_Check_Timeout|Automated_Backup_Preference|Automated_Backup_Preference_Desc|Version|Basic_Features|Dtc_Support|Db_Failover|Is_Distributed|Cluster_Type|Cluster_Type_Desc|Required_Synchronized_Secondaries_To_Commit|Sequence_Number|Is_Contained|Group_Id_Def|Listener_Id|Dns_Name|Port|Is_Conformant|Ip_Configuration_String_From_Cluster|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.group_id}}|{{.name}}|{{.resource_id}}|{{.resource_group_id}}|{{.failure_condition_level}}|{{.health_check_timeout}}|{{.automated_backup_preference}}|{{.automated_backup_preference_desc}}|{{.version}}|{{.basic_features}}|{{.dtc_support}}|{{.db_failover}}|{{.is_distributed}}|{{.cluster_type}}|{{.cluster_type_desc}}|{{.required_synchronized_secondaries_to_commit}}|{{.sequence_number}}|{{.is_contained}}|{{.group_id_def}}|{{.listener_id}}|{{.dns_name}}|{{.port}}|{{.is_conformant}}|{{.ip_configuration_string_from_cluster}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## 主备切换前后状态
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.status_before_and_after_active_switchover"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Replica_Name|Ag_Name|Time|Previous_State|Current_State|Level|
|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.replica_name}}|{{.ag_name}}|{{.time}}|{{.previous_state}}|{{.current_state}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



## AG同步状态检查
{{range $id, $vs := $problems}}{{if eq $id "sqlserver.ag_synchronization_status_check"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if ne .actual ""}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{if .mixraw}}
|Group_Name|Replica_Server_Name|Node_Name|Role_Desc|Dbname|Synchronization_State_Desc|Synchronization_Health_Desc|Level|
|:---|:---|:---|:---|:---|:---|:---|:---|
{{range .mixraw}}|{{.group_name}}|{{.replica_server_name}}|{{.node_name}}|{{.role_desc}}|{{.DBName}}|{{.synchronization_state_desc}}|{{.synchronization_health_desc}}|{{Icon .mixlevel}}|
{{end}}
{{end}}
{{end}}{{end}}{{end}}



{{end}}