# CHANGELOG

## [ Version: 1.3.0 ] - 2025-01-04

- 解决 12c 以下版本 Sequence 使用率检查未判断版本的问题 @李俊龙
- 部分基本配置未采集到时不影响检查

## [ Version: 1.2.59 ] - 2024-12-20

- 移除报告的副标题

## [ Version: 1.2.58 ] - 2024-09-23

- 修改aix中df中的无用参数 @郑中豪

## [ Version: 1.2.57 ] - 2024-09-13

- 修改检查项OpenCursor使用的sql语句 @方加祥

## [ Version: 1.2.56 ] - 2024-08-27

- 修改scripts中脚本的换行符由windows改成unix @彭思琪

## [ Version: 1.2.55 ] - 2024-07-18

- oracle巡检脚本中parameter相关部分增加字段 @徐懿

## [ Version: 1.2.54 ] - 2024-07-18

- 修改脚本巡检中used_pct的值为百分比 @陈佼尧

## [ Version: 1.2.53 ] - 2024-07-15

- 修改_memory_imm_mode_without_autosga参数的推荐值为FALSE @姜劲松

## [ Version: 1.2.52 ] - 2024-05-20

- 主库上判断DG备库传输日志增加status=disabled情况 @刘明章

## [ Version: 1.2.51 ] - 2024-04-24

- RDBMS软件的ASM磁盘使用情况不能超过2TB @方加祥

## [ Version: 1.2.50 ] - 2024-04-03

- alert告警由匹配最后一行日志中的日期,改成当前日期 @李向飞

## [ Version: 1.2.49 ] - 2024-03-15

- 汇总报告中新增文件系统使用率汇总和磁盘组使用率汇总 @刘明章

## [ Version: 1.2.48 ] - 2024-01-23

- 减少失效索引检查结果显示数量 @李向飞
- 解决磁盘组使用率检查取小数点后两位失效问题 @曹诚武

## [ Version: 1.2.47 ] - 2023-10-23

- 修复_gc_read_mostly_locking参数检查 @肖晖
- 收集 `v$spparameter` 所有的非默认参数 @肖晖
- 优化透明大页设置采集检查 @刘明章
- 数据库基本信息新增数据库版本和是否集群信息 @代杰

## [ Version: 1.2.46 ] - 2023-08-09

- 解决spfile 参数设置优先级一致性检查中告警未汇总的问题 @谭德明
- 更新模板页眉页脚为公司最新 @陈大习
- 巡检时间修改为巡检报告生成时间 @李俊龙

## [ Version: 1.2.45 ] - 2023-06-26

- 操作系统基本配置增加一个主机名区分 @孙鑫
- 解决外键无索引检查当约束名称含特殊符号导致表格错位问题

## [ Version: 1.2.44 ] - 2023-06-21

- 脚本采集时排除网络文件系统和ISO @刘明章
- 增加 Windows 下对ISO的简单判断 @刘明章

## [ Version: 1.2.43 ] - 2023-06-21

- 参数设置检查中`job_queue_processes`为0时设为高风险 @王会民
- 优化参数设置检查展示

## [ Version: 1.2.42 ] - 2023-06-15

- 系统参数检查去除AIX字样，完善Linux使用eout情况下内存使用率计算方式 @刘明章
- Linux eout采集增加`MemAvailable|Buffers|Cached`采集 @刘明章
- 解决数据库时区设置检查告警时存在分项告警没有汇总告警的问题 @李俊龙
- 告警数量统计增加说明 @李俊龙
- 条件显示`MTU for lo`和`主机文件配置` @李付良

## [ Version: 1.2.41 ] - 2023-06-12

- 用户权限检查结果描述细分为DBA权限和其他高风险权限 @周健强

## [ Version: 1.2.40 ] - 2023-06-02

- 修复测试反馈问题 @黄大畅

## [ Version: 1.2.39 ] - 2023-06-02

- 完善内存及Swap使用检查规则 @黄大畅 @姜劲松
- 完善eout方式采集结果的内存、Swap和内存参数检查规则
- desk资源管理增加展示数据目录

## [ Version: 1.2.38 ] - 2023-05-25

- 新增自动解压和归集json文件到同一目录功能

## [ Version: 1.2.37 ] - 2023-04-25

- 集群状态检查在“除ora.gsd 组件外存在OFFLINE或UNKNOWN状态且集群各节点状态不一致”时才告警@郑中豪

## [ Version: 1.2.36 ] - 2023-04-20

- 未发现统计信息收集任务运行信息时设为高风险 @黄威

## [ Version: 1.2.35 ] - 2023-04-07

- PASSWORD_LIFE_TIME 预期值明确为 UNLIMITED @王其静

## [ Version: 1.2.34 ] - 2023-04-01

- 最佳实践参数检查移除 _olap_dimension_corehash_size @黄大畅
- 最佳实践参数检查修改 _optimizer_use_feedback 推荐值为FALSE @王会民

## [ Version: 1.2.33 ] - 2023-03-06

- 提升 crs alert 日志路径查找的准确性 @黄威

## [ Version: 1.2.32 ] - 2023-03-06

- 解决脚本中 cluster 字段不换行问题 @张明贵

## [ Version: 1.2.31 ] - 2023-03-01

- 磁盘组使用率检查和磁盘组offline 情况检查拆分为两个检查项 @邢凯威
- 集群状态检查中 ora.gsd 组件 OFFLINE 视为正常状态 @肖国树

## [ Version: 1.2.30 ] - 2023-02-16

- 新增CRS Alert日志检查 @姜劲松
- 采集脚本新增CRS Alert日志采集 @姜劲松
- Oracle Linux采集脚本新增`-a`参数以区分库名、实例名和主机名完全相同的情况 @黄大畅

## [ Version: 1.2.29 ] - 2023-02-13

- 解决脚本df输出换行问题 @张明贵

## [ Version: 1.2.28 ] - 2023-02-02

- 采集脚本增加若干校验规则, 异常时将直接退出等待问题排查 @景涵

## [ Version: 1.2.27 ] - 2023-01-09

- 修改sysdba未采集到数据时的告警级别

## [ Version: 1.2.26 ] - 2023-01-09

- 解决脚本中文乱码问题

## [ Version: 1.2.25 ] - 2022-12-30

- 采集脚本更新DG 配置参数SQL

## [ Version: 1.2.24 ] - 2022-12-27

- 新增 DG 配置参数展示 @景涵
- 采集脚本增加 DG 配置参数采集 @景涵

## [ Version: 1.2.23 ] - 2022-12-20

- 采集脚本增加 AIX 中文支持 @黄大畅

## [ Version: 1.2.22 ] - 2022-12-12

- 采集脚本设置 multitenant 属性默认为 NO
- 采集脚本修复 sqlplus 路径错误问题

## [ Version: 1.2.21 ] - 2022-12-06

- SYSDBA 权限用户检查告警描述优化 @谭德明

## [ Version: 1.2.20 ] - 2022-12-05

- 采集脚本限制为只采集当前节点的信息 @谭德明

## [ Version: 1.2.19 ] - 2022-11-25

- 采集脚本新增`instance.rac`和`instance.primary`属性用于判断数据库部署架构

## [ Version: 1.2.18 ] - 2022-11-25

- 将数据库版本信息传入规则，解决统计部分检查结果重复的问题 @李俊龙
- 修复基本配置检查`oracle.baseinfo`、`oracle.baseinfo12c`中总风险等级为低风险的问题 @李俊龙
- 修复审计设置取值问题

## [ Version: 1.2.17 ] - 2022-10-14

- 优化`oracle.crsctlstat` 打印异常组件名 @李付良
- 修复`oracle.fspct` 的一个数据转换异常 @罗志远
- 新增`oracle.osparm` 用于展示AIX系统参数  @罗志远
- 优化模板中OS系统参数部分的展示模板以适应不同系统平台
- 补充 AIX 下文件系统的 Inode 检查的内容及结论汇总表
- 修复`oracle.awkalert`在 Windows 下的一个异常
- 修复 bin 与 shell 采集项分类不同导致 `oracle.crsctlstat`读取数据问题
- 修复`oracle.userinfo`、`oracle.userinfo12c`用户名带$符号导致表格异常问题

## [ Version: 1.2.16 ] - 2022-10-12

- `oracle.archive_gap` 发现日志间隙时设为高风险 @孙鑫

## [ Version: 1.2.15 ] - 2022-09-29

- eout脚本/新增脚本的MD5校验文件MD5.txt @王振业

## [ Version: 1.2.14 ] - 2022-09-29

- 剩余大小展示增加四舍五入2位小数处理 @铁又熙

## [ Version: 1.2.13 ] - 2022-09-28

- `oracle.tbscheck12c`、`oracle.tbscheck` 表空间使用率告警时同时显示剩余大小 @王蒙
- `oracle.diskgroup` 磁盘组使用率告警时同时显示剩余大小 @王蒙
- `oracle.fspct` 文件系统使用率告警时同时显示剩余大小 @王蒙
- `linux.diskUsedPercent` 文件系统使用率告警时同时显示剩余大小 @王蒙
- 数据库版本信息章节改为数据库基本信息使之与内容匹配 @姜劲松

## [ Version: 1.2.12 ] - 2022-09-27

- eout脚本/新增ftp功能, $ftp_server 非空时自动启用 @代杰 
- eout脚本/补充数据库非OPEN情况下获取数据库版本的方法 @陈艺
- eout脚本/修正 df 等部分中文字符导致采集错误的问题 @张英瑞
- eout脚本/完善 alert 日志采集函数
- 解决 `oracle.diskgroup` 子告警覆盖的问题 @景涵

## [ Version: 1.2.11 ] - 2022-09-25

- 对`oracle.awkalert`进行二次过滤解决不包含关键词但告警的问题 @孙浩楠
- 完善`oracle.lo`影响及解决方案信息 @刘明章 @卞其龙
- 风险及建议列表中将影响（之前版本仅在详细报告显示）与建议合并显示至建议列, 正常时不展示建议
- 将集群报告、通用报告的风险及建议列表处理为与汇总报告一致
- 统计信息收集任务运行状况检查补充实际值展示 @张赛兰

## [ Version: 1.2.10 ] - 2022-09-20

- 修改汇总报告模板 @李仲秋
- 新增前统计和后统计脚本
- 新增扩展库脚本
- 更新汇总脚本为使用内置库实现, 提供若干可选项, 默认配置及说明如下：
    * show_document_version_information: "yes", // 文档版本信息
    * show_summary_of_check: "yes", // 巡检结果汇总
    * show_important_and_handling_plan: "yes", // 重要告警及处理计划
    * show_count_of_risks: "yes", // 告警数量统计
    * show_count_of_risks_with_score: "no", // 在 show_count_of_risks 中显示健康度 @章启慧
    * show_count_of_risks_orderby_score: "no", // 告警数量统计, 健康度从高至低
    * show_piechart: "no", // 告警数量统计饼图
    * show_list_of_risks_danger: "yes", // 高风险
    * show_list_of_risks_warning: "yes", // 中风险
    * show_list_of_risks_green: "yes", // 低风险
    * show_list_of_risks_ok: "no", // 正常
    * show_list_of_risks_group_by_category: "no", // 风险及建议（按告警分类）
    * show_list_of_risks_group_by_category_order: ["基本配置检查", "系统存储空间使用", "数据库组件及参数设置", "数据文件", "系统对象检查", "系统安全及审计", "系统运行状态", "集群状态", "系统备份"],
    * show_check_item_list: "yes" // 双栏检查项列表
- oracle_eoutcollector_for_linux.sh 支持-p参数指定profile文件 @王志远

## [ Version: 1.2.9 ] - 2022-09-14

- 修改汇总报告模板 @李仲秋

## [ Version: 1.2.8 ] - 2022-09-09

- 修改模板封面及字体 @李仲秋
- 补充优化器统计顾问记录失效天数检查展示 @秦书月
- 最佳实践参数设置检查增加是否一致列 @邢凯威

## [ Version: 1.2.7 ] - 2022-09-08

- 解决特殊符号导致表格串行问题 @邢凯威

## [ Version: 1.2.6 ] - 2022-09-07

- 解决正常事件显示不全的问题 @姜沛
- 完善操作系统检查部分的章节标题 @姜沛

## [ Version: 1.2.5 ] - 2022-09-01

- 表空间碎片检查告警级别下调为中风险 @邢凯威

## [ Version: 1.2.4 ] - 2022-08-31

- `PASSWORD_LIFE_TIME` 检查告警级别由中风险调整为低风险 @孙鑫
- 数据库系统参数检查`log_archive_dest_2`值转为大写后再比较 @刘赟
- 更新单例报告的文件名为`{{instance}}@{{hostname}}`方式与集群报告一致
- 解决实例名相同导致实例数量统计不准确的问题 @罗志远
- 汇总报告新增统计饼图

## [ Version: 1.2.3 ] - 2022-08-31

- 修改告警统计方法及描述，区分低风险和正常 @邢凯威

## [ Version: 1.2.2 ] - 2022-08-30

- `系统备份检查`具体化为`系统备份(rman)检查` @韩二波

## [ Version: 1.2.1 ] - 2022-08-29

- 修复`oracle.tbscheck`字段名称与采集数据不一致的问题 @罗志远
- 修复`linux.diskUsedPercent`中对象浅拷贝导致的bug（eout方式采集不受影响）@罗志远
- 修复`文件系统使用`模板中字段顺序（eout方式采集不受影响）@罗志远
- 表空间检查告警时增加名称及当前值展示 @罗志远

## [ Version: 1.2.0 ] - 2022-08-28

- 合并`cluster`模板和`common`模板为一个模板即本模板, 可通过调用不同的主配置文件区分
- 新增`eout`脚本至`scripts`下与模板配套维护和使用
- 新增配置信息提取脚本`pre.stat`

## [ Version: 1.1.9 ] - 2022-08-26

- 修复`oracle.pdbstat`、`oracle.flashback12c`的`name`字段带特殊符号导致排版错误问题 @李元帅
- PDB仅在11g之后检查和展示(12C才引入PDB)并于`oracle.pdbstat`、`oracle.pdbsavedstate`备注适用版本 @王蒙

## [ Version: 1.1.8 ] - 2022-08-24

- 移除11g（含11g）之后表空间碎片检查 @孙鑫 @肖国树
- 增加`TOP 5 Event`的观测起止时间 @肖国树
- 更新示例数据

## [ Version: 1.1.7 ] - 2022-08-22

- 修复`oracle.logswitch`检查指标错误的问题
- 将独立报告的告警定义章节前置
- 更新了告警统计部分的用语

## [ Version: 1.1.6 ] - 2022-08-21

- 新增`{{costomer}}`用于在报告文件名中显示客户名称
- 修改参数设置检查、最佳实践参数设置检查、内核参数检查、内存参数检查的处理建议为“仅作为调优或问题排查时的参考”
- 修改`oracle.dgapply`、`oracle.dgdelay`、`oracle.jobs`、`oracle.jobs`描述
- 修复`oracle.invalidcons12c`、`oracle.invalididx12c`、`oracle.invalidobj12c`中输出带有特殊符号影响报告格式的问题
- 去除`oracle.profile`、`oracle.profile12c`、`oracle.recyclebin_12c`、`oracle.recyclebin`、`oracle.userinfo`、`oracle.userinfo12c`、`oracle.userpriv`、`oracle.userpriv12c`、`oracle.sysdba`、`oracle.flashback`、`oracle.flashback12c`正常情况下的实际值描述
- 更新告警级别定义描述
- 新增`{{name}}`用于在报告文件名中显示复杂集群名称

## [ Version: 1.1.5 ] - 2022-08-16

- 修改`oracle.tbscheck`及`oracle.tbscheck12c`模板表头

## [ Version: 1.1.4 ] - 2022-08-01

- 优化文件系统及 Inode 使用率检查规则以适应来自`json` 及`eout` 的不同数据

## [ Version: 1.1.3 ] - 2022-08-01

- 汇总报告增加以主机及实例名进行分组显示
- 根据上下文语义对汇总报告章节结构进行适当调整
- 报告增加正常事件展示
- 优化`linux.inodeUsedPercent`
- 优化`linux.diskUsedPercent`
- 移除`linux.cpuLoad`
- 移除`linux.cpuUsedPercent`
- 移除`linux.ntpServiceCheck`
- 移除`linux.ntpsync`
- 移除`linux.base`
- 移除`linux.psaux`
- 移除`linux.psef`
- 参数设置`oracle.parameter` 检查结果不纳入告警
- 最佳实践参数设置 `oracle.hiddenparms` 检查结果不纳入告警
- 内核参数`oracle.sysctla` 检查结果不纳入告警
- 内存参数`oracle.mem` 检查结果不纳入告警

## [ Version: 1.1.2 ] - 2022-07-29

- 移除字符拼接时多余的分号
- 优化MTU查询为空时的描述

## [ Version: 1.1.1 ] - 2022-07-25

- 优化巡检项分类

## [ Version: 1.1.0 ] - 2022-07-13

- 移除报告中的邮箱地址展示，使用`巡检工程师：姓名`
- 移除报告首页页眉
- 报告时间保留年月日去除时分秒
- 增加文档版本信息章节
- 汇总报告中 1.2 - 1.4 放到后面做附件
- 高风险和中风险分表
- 修改了概述部分的文字叙述
- 移除不需要的子模板
- 配置文件增加`meta.config.appnames`字段用于配置主机名与应用系统名之间的对应关系

## [ Version: 1.0.15 ] - 2022-07-01

- `oracle.archive_dest_status`中检查`gap_status`字段修改为检查`status`字段

## [ Version: 1.0.14 ] - 2022-06-22

- 新增对 Oracle for windows 的支持
- 新增对 Oracle for AIX 的支持

## [ Version: 1.0.13 ] - 2022-06-08

- 修复`oracle.profile`检查结果正常后直接返回导致原始数据不能展示的问题
- 增加`oracle.efficent`检查规则
- 移除巡检总结和建议表章节保留巡检总结和建议表
- 调整巡检告警定义章节至巡检总结和建议表之前
- 移除`Logic Read 每秒`
- 移除`Physic Read 每秒`
- 移除`Hist Undo Usage`
- 移除`优化器统计顾问记录失效天数`
- 移除用于 Debug 的`rule id`

## [ Version: 1.0.12 ] - 2022-05-22

- 去除汇总报告中受影响主机及实际值部分中对正常实例的展示
- 新增集群状态检查`oracle.crsctlstat`
- 主配置增加`customer`项用于保存客户名称
- 移除`psinfo`规则

## [ Version: 1.0.11 ] - 2022-03-27

- 当配置文件的`groupBy`参数设置为`hostname`时，1台主机生成1个巡检报告; 设置为`instance`时, 1个实例生成1个巡检报告（在模板上设置即可）
- alert 展示近半个月的数据（目前通过规则实现，原始采集已经限制为1万行，本身不算多）
- 汇总报告、单个报告均增加汇总表格展示，高风险告警靠前展示（即巡检总结和建议表）
- 关于采集时增加数据条数限制的，待后续重新采集数据生效
