{{define "main"}}

{{$problems := GroupBy .problems "id"}}
{{$summary := JsCall "func.summary" .problems}}
{{$appnames := .meta.config.appnames}}


---
title: {{.meta.customer}} {{.meta.title}}
subtitle: {{range .Mongo}}{{JsCall "func.appname" .host.hostname $appnames}}{{end}}
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
{{println ""}}主机名：{{if .SysConfs}}{{range .SysConfs}}{{printf "%-13s" .host.hostname}}{{end}}{{else}}{{range .Mongo}}{{index .host "hostname"}} {{end}}{{end}}
{{println ""}}数据库实例：{{range .Mongo}}{{index  .port}} {{end}}
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
{{range .Mongo}}

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


# 数据库配置信息

## 构建信息

{{range .problems}}{{if eq .id "mongo.buildInfo"}}

| 配置项                     | 值                                                         |
|:------------------------|:----------------------------------------------------------|
| 版本                      | {{ .raw.version}}                                         |
| 存储引擎列表                  | {{range $k,$v := .raw.storageEngines}}{{$v}};{{end}}      |
| JavaScript引擎            | {{ .raw.javascriptEngine}}                                |
| 处理器体系结构的数字              | {{ .raw.bits }}                                           |
| debug                   | {{ .raw.debug}}                                           |
| 构建mongod时使用的TLS/SSL库的版本 | {{ .raw.openssl.compiled}}                                |
| 当前正在使用的TLS/SSL库版本       | {{ .raw.openssl.running}}                                 |
| 构建时使用的附加模块列表            | {{range $k,$v := .raw.modules}}{{$v}};{{end}}             |
| 最大BSON文档大小              | {{ .raw.maxBsonObjectSize}}                               |

{{end}}{{end}}


## 连接状态信息

{{range .problems}}{{if eq .id "mongo.connectionStatus"}}

| 配置项              | 值                                                                                        |
|:-----------------|:-----------------------------------------------------------------------------------------|
| 经过身份验证的用户        | {{range $k,$v := .raw.authInfo.authenticatedUsers}}库：{{$v.db}}用户:{{$v.user}};{{end}}     |
| 已验证用户关联的当前角色的定义  | {{range $k,$v := .raw.authInfo.authenticatedUserRoles}}库：{{$v.db}}定义:{{$v.role}};{{end}} |

{{end}}{{end}}


## 数据库集合

{{range .problems}}{{if eq .id "mongo.connectionStatus"}}

|集合            |   可以访问指定资源的特权操作 |
|:--------------:|:-------------:|
| {{range .raw.authInfo.authenticatedUserPrivileges}} 库：{{.resource.db}}集合：{{.resource.collection}}； | {{range .actions}}{{.}}；{{end}}  |
{{end}}
{{end}}{{end}}

## 存储统计信息
{{range .problems}}{{if eq .id "mongo.dbStats"}}

| 配置项                         | 值                              |
|:----------------------------|:-------------------------------|
| 数据库                         | {{ .raw.db}}                   |
| 数据库中的集合数                    | {{ .raw.collections}}          |
| 数据库中的视图数                    | {{ .raw.views}}                |
| 跨所有集合的数据库中对象(特别是文档)的数量      | {{ .raw.objects }}             |
| 每个文档的平均大小（字节）               | {{ .raw.avgObjSize}}           |
| 数据库中保存的未压缩数据的总大小            | {{ .raw.dataSize}}             |
| 分配给数据库中所有集合用于文档存储的空间总和      | {{ .raw.storageSize}}          |
| 分配给数据库中所有集合用于文档存储的空闲空间之和    | {{.raw.freeStorageSize}}       |
| 数据库中所有集合的索引总数               | {{ .raw.indexes}}              |
| 分配给数据库中所有索引的空间总和            | {{ .raw.indexSize}}            |
| 分配给数据库中所有索引的空闲空间之和          | {{ .raw.indexFreeStorageSize}} |
| 为数据库中所有集合中的文档和索引分配的空间之和     | {{ .raw.totalSize}}            |
| 为数据库中所有集合中的文档和索引分配的可用存储空间之和 | {{ .raw.totalFreeStorageSize}} |
| 命令使用的比例值                    | {{ .raw.scaleFactor}}          |
| 存储数据的文件系统上使用的所有磁盘空间的总大小     | {{ .raw.fsUsedSize}}           |
| 存储数据的文件系统上所有磁盘容量的总和         | {{ .raw.fsTotalSize}}          |

{{end}}{{end}}


# 数据库状态的概述

## 缓存使用率

{{range $id, $vs := $problems}}{{if eq $id "mongo.cacheUtilization"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}


## 缓存中脏数据比率

{{range $id, $vs := $problems}}{{if eq $id "mongo.dirtyDataInCache"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}


## 异常信息数量
{{range .problems}}{{if eq .id "mongo.serverStatus"}}

| 名称               | 值                                                               |
|:-----------------|:----------------------------------------------------------------|
| 进程启动以来发生的“用户断言”数 | {{ .raw.asserts.user}}                                          |
| 进程启动以来引发的警告数     | {{ .raw.asserts.warning}}                                       |
| 缺页中断总数           | {{JsCall "func.replaceNumberLong" .raw.extra_info.page_faults}} |



## 连接信息数量

| 名称                | 值                                        |
|:------------------|:-----------------------------------------|
| 从客户端到数据库服务器的连接数   | {{ .raw.connections.current}}            |
| 创建到数据库的所有连接       | {{ .raw.connections.totalCreated}}       |
| 客户端连接数据库总数        | {{ .raw.globalLock.activeClients.total}} |

## 流量

| 名称                 | 值                                                           |
|:-------------------|:------------------------------------------------------------|
| 数据库接收的网络流量字节数      | {{JsCall "func.replaceNumberLong" .raw.network.bytesIn}}    |
| 数据库发送的网络流量的字节数     | {{JsCall "func.replaceNumberLong" .raw.network.bytesOut}}   |

## QPS&TPS

| 名称                          | 值                                                            |
|:----------------------------|:-------------------------------------------------------------|
| 自上次启动mongod实例以来收到的插入操作总数    | {{JsCall "func.replaceNumberLong" .raw.opcounters.insert}}   |
| 自上次启动mongod实例以来收到的查询总数      | {{JsCall "func.replaceNumberLong" .raw.opcounters.query}}    |
| 自上次启动mongod实例以来收到的更新操作总数    | {{JsCall "func.replaceNumberLong" .raw.opcounters.update}}   |
| 自上次启动mongod实例以来的删除操作总数      | {{JsCall "func.replaceNumberLong" .raw.opcounters.delete}}   |
| 自上次启动mongod实例以来执行其他操作的次数    | {{JsCall "func.replaceNumberLong" .raw.opcounters.command}}  |

{{if  .raw.opcountersRepl}}
## Repl

| 名称                        | 值                                                                |
|:--------------------------|:-----------------------------------------------------------------|
| 自上次启动mongod实例以来复制插入操作的总数  | {{JsCall "func.replaceNumberLong" .raw.opcountersRepl.insert}}   |
| 自上次启动mongod实例以来复制更新操作总数   | {{JsCall "func.replaceNumberLong" .raw.opcountersRepl.update}}   |
| 自上次启动mongod实例以来复制的删除操作总数  | {{JsCall "func.replaceNumberLong" .raw.opcountersRepl.delete}}   |
{{end}}

## 内存

| 名称             | 值                                                     |
|:---------------|:------------------------------------------------------|
| mongo使用的物理内存   | {{JsCall "func.replaceNumberLong" .raw.mem.resident}} |

{{if  .raw.locks}}
## 锁

| 名称              | 值                                                                           |
|:----------------|:----------------------------------------------------------------------------|
| 获得实例级排他锁的次数     | {{JsCall "func.replaceNumberLong" .raw.locks.Global.acquireCount.W}}        |
| 获得实例级排他锁的时间     | {{JsCall "func.replaceNumberLong" .raw.locks.Global.timeAcquiringMicros.W}} |
| 获得数据库级排他锁的次数    | {{JsCall "func.replaceNumberLong" .raw.locks.Database.acquireCount.W}}      |
| 获得集合级别排他锁的次数    | {{JsCall "func.replaceNumberLong" .raw.locks.Collection.acquireCount.W}}    |
| 获得元数据排他锁的次数     | {{JsCall "func.replaceNumberLong" .raw.locks.Metadata.acquireCount.W}}      |
| 当前排队等待全局写锁的操作数  | {{JsCall "func.replaceNumberLong" .raw.globalLock.currentQueue.writers}}    |
| 当前排队等待全局读锁的操作数  | {{JsCall "func.replaceNumberLong" .raw.globalLock.currentQueue.readers}}    |
| 获取全局读锁的活跃客户端    | {{JsCall "func.replaceNumberLong" .raw.globalLock.activeClients.readers}}   |
| 获取全局写锁的活跃客户端    | {{JsCall "func.replaceNumberLong" .raw.globalLock.activeClients.writers}}   |

{{end}}
{{if  .raw.wiredTiger}}

## Transaction

| 名称               | 值                                                                                       |
|:-----------------|:----------------------------------------------------------------------------------------|
| 已用写trasactions数  | {{JsCall "func.replaceNumberLong" .raw.wiredTiger.concurrentTransactions.write.out}}    |
| 已用读trasactions数  | {{JsCall "func.replaceNumberLong" .raw.wiredTiger.concurrentTransactions.read.out}}     |


## wiretiger

| 名称                     | 值                                                                                                           |
|:-----------------------|:------------------------------------------------------------------------------------------------------------|
| 被驱逐的干净页，累计值            | {{JsCall "func.replaceNumberLong"  (index  .raw.wiredTiger.cache "unmodified pages evicted")}}              |
| 从磁盘读进入cache的大小。累计值     | {{JsCall "func.replaceNumberLong"  (index  .raw.wiredTiger.cache "bytes read into cache")}}                 |
| 从cache写入磁盘大小。累计值       | {{JsCall "func.replaceNumberLong"  (index  .raw.wiredTiger.cache "bytes written from cache")}}              |
| eviction线程驱逐页面数。累计值    | {{JsCall "func.replaceNumberLong"  (index  .raw.wiredTiger.cache "eviction worker thread evicting pages")}} |
| wireTiger中ckpt耗时（毫秒）   | {{index  .raw.wiredTiger.transaction "transaction checkpoint total time (msecs)" }}                         |
| 用户线程参与eventing时间       | {{index (index  .raw.wiredTiger "thread-yield")  "application thread time evicting (usecs)" }}              |

{{end}}
{{end}}{{end}}


# 日志

{{range .problems}}{{if eq .id "mongo.warningLog"}}


|                   时间                   |   日志内容   |
|:--------------------------------------:|:--------:|
| {{range .raw.log}}{{index .t "$date"}} | {{.msg}} |
{{end}}
{{end}}{{end}}



{{end}}