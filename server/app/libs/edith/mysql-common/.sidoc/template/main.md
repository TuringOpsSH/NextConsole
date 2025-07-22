{{define "main"}}

{{ $summary := JsCall "func.summary" .problems }}
{{ $problems := GroupBy .problems "id"}}

---
title: {{.meta.customer}} {{.meta.title}}
subtitle:
author:

- {{ .meta.author.name}} ({{ .meta.author.email}})
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
{{println ""}}主机名：{{if .SysConfs}}{{range .SysConfs}}{{printf "%-13s" .host.hostname}}{{end}}{{else}}{{range .MySQLConf}}{{index .host "hostname"}} {{end}}{{end}}
{{println ""}}IP：{{range .MySQLConf}}{{XPathText .edith.ips "/*" ","}} {{end}}
{{println ""}}数据库实例：{{range .MySQLConf}}{{index .port}} {{end}}
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

|检查内容|主机名|端口号|预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "高风险"}}| {{$v.name}}| {{.hostInst}}| {{$v.expected}}| {{.actual}}| {{Icon .level}}| {{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}| 
{{end}}{{end}}{{end}}

### 中风险

|检查内容|主机名|端口号|预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "中风险"}}| {{$v.name}}| {{.hostInst}}| {{$v.expected}}| {{.actual}}| {{Icon .level}}| {{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}| 
{{end}}{{end}}{{end}}

### 低风险

|检查内容|主机名|端口号|预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "低风险"}}| {{$v.name}}| {{.hostInst}}| {{$v.expected}}| {{.actual}}| {{Icon .level}}| {{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}|
{{end}}{{end}}{{end}}

### 正常

|检查内容|主机名|端口号|预期值|实际值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|
{{range $id, $v := $summary.sumById}}{{range $kk, $vv := $v.hostInstErrArr}}{{if eq .level "正常"}}| {{$v.name}}| {{.hostInst}}| {{$v.expected}}| {{.actual}}| {{Icon .level}}| {{if ne .level "正常"}}{{if ne .effect ""}}{{.effect}}. {{end}}{{if ne .solution ""}}建议{{.solution}}.{{end}}{{end}}| 
{{end}}{{end}}{{end}}

# 操作系统概况

## 操作系统基本配置
{{template "base" .}}

## CPU负载
{{template "cpu" .}}

## 内存使用情况
{{template "mem" .}}

## 磁盘空间使用情况
{{template "disk" .}}


# 数据库总体概况

## 数据库基本信息
{{range $id, $vs := $problems}}{{if eq $id "mysql.basic_information_of_database"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

{{range .problems}} {{if eq .id "mysql.basic_information_of_database"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 存储引擎和DB的数量关系
{{range $id, $vs := $problems}}{{if eq $id "mysql.quantitative_relationship_between_storage_engine_and_db"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

{{range .problems}} {{if eq .id "mysql.quantitative_relationship_between_storage_engine_and_db"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## InnoDB系统表空间
{{range $id, $vs := $problems}}{{if eq $id "mysql.innodb_system_tablespace"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.innodb_system_tablespace"}}{{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 查询所有用户
{{range $id, $vs := $problems}}{{if eq $id "mysql.query_all_users"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.query_all_users"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 重要参数
{{range $id, $vs := $problems}}{{if eq $id "mysql.some_important_parameters"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.some_important_parameters"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 用户登录信息

### 当前连接的用户
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_users_and_hosts_currently_connected_to_the_database"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_users_and_hosts_currently_connected_to_the_database"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

### 主机连接数
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_current_connections_and_total_connections_of_each_host"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_current_connections_and_total_connections_of_each_host"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

### 登录统计
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_login_information_according_to_login_user_login_server"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_login_information_according_to_login_user_login_server"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

### 数据库登录统计
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_login_information_according_to_login_user_database_login_server"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_login_information_according_to_login_user_database_login_server"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 所有线程
{{range $id, $vs := $problems}}{{if eq $id "mysql.query_all_threads_excluding_sleep_threads"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.query_all_threads_excluding_sleep_threads"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## sleep线程Top20
{{range $id, $vs := $problems}}{{if eq $id "mysql.sleep_thread_top20"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.sleep_thread_top20"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 正在使用表的线程数量
{{range $id, $vs := $problems}}{{if eq $id "mysql.how_many_threads_are_using_the_table"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.how_many_threads_are_using_the_table"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## InnoDB锁
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_innodb_lock_generated_by_the_current_state_and_the_result_is_output_only_when_there_is_a"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_innodb_lock_generated_by_the_current_state_and_the_result_is_output_only_when_there_is_a"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## InnoDB锁等待
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_innodb_lock_wait_generated_by_the_current_state_the_result_is_output_only_when_there_is_a"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_innodb_lock_wait_generated_by_the_current_state_the_result_is_output_only_when_there_is_a"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 当前活跃事务
{{range $id, $vs := $problems}}{{if eq $id "mysql.current_active_transactions_in_the_current_innodb_kernel"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.current_active_transactions_in_the_current_innodb_kernel"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 锁详情
{{range $id, $vs := $problems}}{{if eq $id "mysql.lock_details"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.lock_details"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 元数据锁信息
{{range $id, $vs := $problems}}{{if eq $id "mysql.metadata_lock_related_information"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.metadata_lock_related_information"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 服务器的状态
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_status_of_the_server"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_status_of_the_server"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 长时间操作
{{range $id, $vs := $problems}}{{if eq $id "mysql.track_the_progress_of_long_term_operations"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.track_the_progress_of_long_term_operations"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 插件信息
{{range $id, $vs := $problems}}{{if eq $id "mysql.plug_in_information"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.plug_in_information"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 平均执行时间超长的语句
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_statements_whose_average_execution_time_value_is_greater_than_95pct_of_the_average_execut"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_statements_whose_average_execution_time_value_is_greater_than_95pct_of_the_average_execut"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 正在执行语句
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_currently_executing_statement_progress_information"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_currently_executing_statement_progress_information"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 使用临时表语句
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_statements_that_use_temporary_tables_by_default"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_statements_that_use_temporary_tables_by_default"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 有临时表语句Top10
{{range $id, $vs := $problems}}{{if eq $id "mysql.top_10_sql_statements_with_temporary_tables"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.top_10_sql_statements_with_temporary_tables"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 执行文件排序语句
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_statements_that_have_performed_file_sorting_by_default_they_are_sorted_in_descending_orde"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_statements_that_have_performed_file_sorting_by_default_they_are_sorted_in_descending_orde"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## SQL整体消耗百分比
{{range $id, $vs := $problems}}{{if eq $id "mysql.overall_consumption_percentage_of_query_sql"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.overall_consumption_percentage_of_query_sql"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## SQL执行次数Top10
{{range $id, $vs := $problems}}{{if eq $id "mysql.execution_times_top10"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.execution_times_top10"}}{{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 全表扫描的表
{{range $id, $vs := $problems}}{{if eq $id "mysql.sql_statement_using_full_table_scan"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.sql_statement_using_full_table_scan"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 全表扫描或未用最优索引的SQL
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_full_table_scan_or_the_statements_that_do_not_use_the_optimal_index_the_statement_text_af"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_full_table_scan_or_the_statements_that_do_not_use_the_optimal_index_the_statement_text_af"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 所有数据库的信息
{{range $id, $vs := $problems}}{{if eq $id "mysql.all_databases_of_the_current_database_instance_and_their_capacity"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.all_databases_of_the_current_database_instance_and_their_capacity"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 错误或警告语句
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_the_statements_that_generate_errors_or_warnings_by_default_they_are_sorted_in_descending_orde"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_the_statements_that_generate_errors_or_warnings_by_default_they_are_sorted_in_descending_orde"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 冗余索引
{{range $id, $vs := $problems}}{{if eq $id "mysql.redundant_index"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.redundant_index"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 无效索引
{{range $id, $vs := $problems}}{{if eq $id "mysql.invalid_index_index_never_used"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.invalid_index_index_never_used"}} {{range $k, $v := .raw}}


- 以下为前50条无效索引的信息：

{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 每张表的索引区分度
{{range $id, $vs := $problems}}{{if eq $id "mysql.index_discrimination_of_each_table_top_100"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.index_discrimination_of_each_table_top_100"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 主从复制参数
{{range $id, $vs := $problems}}{{if eq $id "mysql.important_parameters_involved_in_master-slave_replication"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.important_parameters_involved_in_master-slave_replication"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 主从库线程
{{range $id, $vs := $problems}}{{if eq $id "mysql.master_slave_library_thread"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.master_slave_library_thread"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 二进制日志
{{range $id, $vs := $problems}}{{if eq $id "mysql.binary_log"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.binary_log"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 从库信息
{{range $id, $vs := $problems}}{{if eq $id "mysql.view_all_slave_libraries_on_the_master_side"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.view_all_slave_libraries_on_the_master_side"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## MGR详情
{{range $id, $vs := $problems}}{{if eq $id "mysql.mgr_details"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.mgr_details"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 主库状态
{{range $id, $vs := $problems}}{{if eq $id "mysql.main_warehouse_status_monitoring"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.main_warehouse_status_monitoring"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 数据库对象
{{range $id, $vs := $problems}}{{if eq $id "mysql.database_object"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.database_object"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 从库状态
{{range $id, $vs := $problems}}{{if eq $id "mysql.slave_database_status_monitoring_data_is_available_only_when_the_slave_database_is_executed"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.slave_database_status_monitoring_data_is_available_only_when_the_slave_database_is_executed"}} {{range $k, $v := .raw}}
{{if $v}}
{{$aaa := JsCall "func.transpose" $v "*" "*"}}
| Name                       | Value |
|:---------------------------| :--- |
 {{range $kk, $vv := $aaa}} | {{$kk}} | {{range $kkk, $vvv := $vv}} {{$vvv}} | {{end}}
{{end}}{{end}}
{{end}}{{end}}{{end}}

## 二进制日志事件
{{range $id, $vs := $problems}}{{if eq $id "mysql.binary_log_event"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}

{{range .problems}} {{if eq .id "mysql.binary_log_event"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 性能参数
{{range $id, $vs := $problems}}{{if eq $id "mysql.performance_parameter_statistics"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.performance_parameter_statistics"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## setup_consumers
{{range $id, $vs := $problems}}{{if eq $id "mysql.setup_consumers"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.setup_consumers"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 自增ID Top20
{{range $id, $vs := $problems}}{{if eq $id "mysql.usage_of_self_increment_id_top_20"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.usage_of_self_increment_id_top_20"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 无主键或唯一键的表
{{range $id, $vs := $problems}}{{if eq $id "mysql.table_without_primary_key_or_unique_key_top_100"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.table_without_primary_key_or_unique_key_top_100"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 占用空间Top10的表
{{range $id, $vs := $problems}}{{if eq $id "mysql.top_10_big_tables_with_the_largest_space"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.top_10_big_tables_with_the_largest_space"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 占用空间Top10的索引
{{range $id, $vs := $problems}}{{if eq $id "mysql.top_10_indexes_with_the_largest_footprint"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.top_10_indexes_with_the_largest_footprint"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

## 所有存储引擎
{{range $id, $vs := $problems}}{{if eq $id "mysql.list_of_all_storage_engines"}}{{range $k, $v := $vs}}
|检查内容及结论|风险|建议|告警|
|:---|:---|:---|:---|
|{{.name}}{{if ne .desc ""}}, {{.desc}}{{end}}{{if ne .expected ""}}【预期值】{{.expected}}{{end}}{{if .actual}}【实际值】{{.actual}}{{end}}|{{if ne .level "正常"}}{{.effect}}{{else}}无{{end}}|{{if ne .level "正常"}}{{.solution}}{{else}}无{{end}}|{{Icon .level}}|
{{end}}{{end}}{{end}}
{{range .problems}} {{if eq .id "mysql.list_of_all_storage_engines"}} {{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

{{end}}
