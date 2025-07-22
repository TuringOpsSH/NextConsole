# CHANGELOG

## [ Version: 1.1.9 ] - 2024-06-04

- linux模板arm架构兼容

## [ Version: 1.1.8 ] - 2023-05-28

- 更新说明文档及预设参数默认值

## [ Version: 1.1.7 ] - 2023-05-25

- 新增新旧模板切换功能

## [ Version: 1.1.6 ] - 2023-04-20

- `linux.mountCheck` type为iso9660时ro为正常 @任海
-  修改 `linux.cpuUsedPercent` actual值问题
-  `check-config.json`文件中params添加ip值
-  汇总报告增加巡检结果汇总表和风险问题及建议列表，可以通过summary.js控制是否显示

## [ Version: 1.1.5 ] - 2023-02-26

- `linux.mountCheck` 同时满足tmpfs和/sys/fs/cgroup的视为正常 @徐旸

## [ Version: 1.1.4 ] - 2022-11-26

- 解决 platformVersion 数据为空时会导致`linux.eof`规则异常问题 @李泽林

## [ Version: 1.1.3 ] - 2022-11-15

- 修复 journalctlerr 拼写错误

## [ Version: 1.1.2 ] - 2022-09-29

- 聚合简化日志检查告警结果 `linux.bootlog`
- 聚合简化日志检查告警结果 `linux.dmesglog`
- 聚合简化日志检查告警结果 `linux.journalctlerr`
- 聚合简化日志检查告警结果 `linux.mcelog`
- 聚合简化日志检查告警结果 `linux.msglog`
- 日志检查部分直接使用日志路径或命令作为章节标题便于理解
- 合并`linux.varlogsecure`的检查结果使用一个ID
- 文件系统检查告警时增加展示当前剩余大小

## [ Version: 1.1.1 ] - 2022-09-25

- 调整章节结构以体现以检查项为纲
- 将可能影响展示至风险及建议列表建议处
- 文档审核替换为通用的文档版本信息
- 移除结束语章节
- 合并所有子模板为一个 main 模板
- 设置 Shell 空闲等待时间告警级别调整为中风险
- 关闭 CTRL+ALT+DEL 快捷键告警级别调整为中风险
- 文件系统使用率调整为 70% 和 90% 两个告警级别
- 移除 NTP 服务检查, 使用更全面的时钟同步检查
- 移除无用规则 linux.kdump、linux.ntpCheck、linux.psalx、linux.psaux、linux.pscount、linux.psef、linux.pselfL、linux.softnetstat、linux.systemauth
- 重写规则确保总检查结果唯一 linux.cpuUsedPercent
- 重写规则确保总检查结果唯一 linux.ntpServiceCheck
- 重写规则确保总检查结果唯一 linux.diskAvgUtil
- 重写规则确保总检查结果唯一 linux.mountCheck
- 重写规则确保总检查结果唯一 linux.inodeUsedPercent
- 重写规则确保总检查结果唯一 linux.cpuLoad
- 重写规则确保总检查结果唯一 linux.etcPasswordCheck
- 重写规则确保总检查结果唯一 linux.netused
- 修正内核架构检查中因数据输入范围过大导致多次检查的问题

## [ Version: 1.1.0 ] - 2022-09-20

- 修改模板封面及字体 @李仲秋
- 新增前统计和后统计脚本
- 新增扩展库脚本
- 更新汇总脚本为使用内置库实现, 提供若干可选项, 默认配置及说明如下：
    * show_document_version_information: "yes", // 文档版本信息
    * show_summary_of_check: "yes", // 巡检结果汇总
    * show_important_and_handling_plan: "yes", // 重要告警及处理计划
    * show_count_of_risks: "yes", // 告警数量统计
    * show_count_of_risks_with_score: "no", // 在 show_count_of_risks 中显示健康度
    * show_count_of_risks_orderby_score: "no", // 告警数量统计, 健康度从高至低
    * show_piechart: "no", // 告警数量统计饼图
    * show_list_of_risks_danger: "yes", // 高风险
    * show_list_of_risks_warning: "yes", // 中风险
    * show_list_of_risks_green: "yes", // 低风险
    * show_list_of_risks_ok: "no", // 正常
    * show_list_of_risks_group_by_category: "yes", // 风险及建议（按告警分类）
    * show_list_of_risks_group_by_category_order: ["系统配置检查", "系统容量检查", "系统健康检查", "系统合规检查", "系统日志检查"],
    * show_check_item_list: "no" // 双栏检查项列表
- 更新检查项分类为中文

## [ Version: 1.0.19 ] - 2022-09-11

- 修改模板封面及字体 @李仲秋

## [ Version: 1.0.18 ] - 2022-08-19

- 更新告警级别定义描述

## [ Version: 1.0.17 ] - 2022-08-19

- 更新告警级别定义描述

## [ Version: 1.0.16 ] - 2022-07-08

- 优化概述中操作系统版本展示以适用不同的Linux发行版

## [ Version: 1.0.15 ] - 2022-07-07

- 修改`PASS_MIN_DAYS`的中文描述为两次修改密码之间允许的最短天数

## [ Version: 1.0.14 ] - 2022-07-01

- 修复汇总报告中文件系统使用率检查显示文件系统名称不准确的问题

## [ Version: 1.0.13 ] - 2022-06-22

- 概述部分引用`.sidoc/rules/func.appname.js`定义的业务信息
- 概述部分自动生成巡检人员、巡检时间信息

## [ Version: 1.0.12 ] - 2022-05-22

- 去除`linux.etclogindefs.js`中的toString类型转换避免取不到值时发生错误
- 主配置增加`customer`项用于保存客户名称
- 移除`psinfo`规则

## [ Version: 1.0.11 ] - 2022-03-27

- 新增`.sidoc/rules/func.appname.js`用于当`*.sidoc`中`meta.sys`字段为空时获取应用系统名称, 其中`func.appname.js`中主机名与应用系统名称对应关系由用户维护
- 新增`.sidoc/rules/func.date.js`用于当`*.sidoc`中`meta.date`字段为空时生成报告时间
- 修复`linux.mcelog.js`中`actual`未定义的bug
- 新增一份 RedHat 5.11 的测试数据
