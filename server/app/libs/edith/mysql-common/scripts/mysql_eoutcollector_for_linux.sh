#!/bin/bash

# 定义关联数组，模拟字典
declare -A sql_dict=(
    ["basic_information_of_database"]="
-- set GLOBAL show_compatibility_56=1;
SELECT
    version() Server_version,
    ( SELECT sum( TRUNCATE ( ( data_length + index_length ) / 1024 / 1024, 2 ) ) AS 'all_db_size(MB)' FROM information_schema.TABLES b ) db_size_MB,
    (select truncate(sum(total_extents*extent_size)/1024/1024,2) from  information_schema.FILES b) datafile_size_MB,
    ( SELECT @@datadir ) datadir,
    ( SELECT @@SOCKET ) SOCKET,
    ( SELECT @@log_bin ) log_bin,
    ( SELECT @@server_id ) server_id;
SELECT  CONCAT(FLOOR(UPTIME / 86400), ' days, ', FLOOR((UPTIME % 86400) / 3600), ' hours, ', FLOOR((UPTIME % 3600) / 60), ' minutes, ',(UPTIME % 60), ' seconds' ) AS Uptime FROM (SELECT VARIABLE_VALUE AS UPTIME  FROM performance_schema.GLOBAL_STATUS  WHERE VARIABLE_NAME = 'Uptime') AS T;
"
    ["quantitative_relationship_between_storage_engine_and_db"]="
SELECT a.\`ENGINE\`,count( * ) counts
FROM    information_schema.\`TABLES\` a
GROUP BY a.\`ENGINE\`;
SELECT  a.TABLE_SCHEMA,
	a.\`ENGINE\`,
	count( * ) counts
FROM    information_schema.\`TABLES\` a
GROUP BY  a.TABLE_SCHEMA,a.\`ENGINE\`
ORDER BY a.TABLE_SCHEMA;
"
    ["innodb_system_tablespace"]="
SELECT name,CONCAT(ROUND(space / 1024 / 1024, 2), 'M') AS space,CONCAT(ROUND(page_size / 1024 / 1024, 2), 'M') AS page_size,zip_page_size,CONCAT(ROUND(file_size / 1024 / 1024, 2), 'M') AS file_size,state FROM information_schema.innodb_tablespaces WHERE space_type <> 'Single';

SELECT file_id,file_name,file_type,tablespace_name,engine,data_free,status FROM INFORMATION_SCHEMA.FILES a WHERE FILE_TYPE <>'TABLESPACE' or a.TABLESPACE_NAME in ('innodb_system','innodb_temporary');
"
    ["query_all_users"]="
SELECT
    u.Host,
    u.User,
    COALESCE(GROUP_CONCAT(p.COLUMN_NAME ORDER BY p.COLUMN_NAME), '') AS privileges
FROM mysql.user u
LEFT JOIN (
    SELECT 'Select_priv' AS COLUMN_NAME, user.Host, user.User FROM mysql.user AS user WHERE user.Select_priv = 'Y'
    UNION ALL
    SELECT 'Insert_priv', Host, User FROM mysql.user WHERE Insert_priv = 'Y'
    UNION ALL
    SELECT 'Update_priv', Host, User FROM mysql.user WHERE Update_priv = 'Y'
    UNION ALL
    SELECT 'Delete_priv', Host, User FROM mysql.user WHERE Delete_priv = 'Y'
    UNION ALL
    SELECT 'Create_priv', Host, User FROM mysql.user WHERE Create_priv = 'Y'
    UNION ALL
    SELECT 'Drop_priv', Host, User FROM mysql.user WHERE Drop_priv = 'Y'
    UNION ALL
    SELECT 'Reload_priv', Host, User FROM mysql.user WHERE Reload_priv = 'Y'
    UNION ALL
    SELECT 'Shutdown_priv', Host, User FROM mysql.user WHERE Shutdown_priv = 'Y'
    UNION ALL
    SELECT 'Process_priv', Host, User FROM mysql.user WHERE Process_priv = 'Y'
    UNION ALL
    SELECT 'File_priv', Host, User FROM mysql.user WHERE File_priv = 'Y'
    UNION ALL
    SELECT 'Grant_priv', Host, User FROM mysql.user WHERE Grant_priv = 'Y'
    UNION ALL
    SELECT 'References_priv', Host, User FROM mysql.user WHERE References_priv = 'Y'
    UNION ALL
    SELECT 'Index_priv', Host, User FROM mysql.user WHERE Index_priv = 'Y'
    UNION ALL
    SELECT 'Alter_priv', Host, User FROM mysql.user WHERE Alter_priv = 'Y'
                UNION ALL
    SELECT 'Show_db_priv', Host, User FROM mysql.user WHERE Show_db_priv = 'Y'
                UNION ALL
    SELECT 'Super_priv', Host, User FROM mysql.user WHERE Super_priv = 'Y'
                UNION ALL
    SELECT 'Create_tmp_table_priv', Host, User FROM mysql.user WHERE Create_tmp_table_priv = 'Y'
                UNION ALL
    SELECT 'Lock_tables_priv', Host, User FROM mysql.user WHERE Lock_tables_priv = 'Y'
                UNION ALL
    SELECT 'Execute_priv', Host, User FROM mysql.user WHERE Execute_priv = 'Y'
                UNION ALL
    SELECT 'Repl_slave_priv', Host, User FROM mysql.user WHERE Repl_slave_priv = 'Y'
                UNION ALL
    SELECT 'Create_view_priv', Host, User FROM mysql.user WHERE Create_view_priv = 'Y'
                UNION ALL
    SELECT 'Show_view_priv', Host, User FROM mysql.user WHERE Show_view_priv = 'Y'
                UNION ALL
    SELECT 'Create_routine_priv', Host, User FROM mysql.user WHERE Create_routine_priv = 'Y'
                UNION ALL
    SELECT 'Alter_routine_priv', Host, User FROM mysql.user WHERE Alter_routine_priv = 'Y'
                UNION ALL
    SELECT 'Create_user_priv', Host, User FROM mysql.user WHERE Create_user_priv = 'Y'
                UNION ALL
    SELECT 'Event_priv', Host, User FROM mysql.user WHERE Event_priv = 'Y'
                UNION ALL
    SELECT 'Trigger_priv', Host, User FROM mysql.user WHERE Trigger_priv = 'Y'
                UNION ALL
    SELECT 'Create_tablespace_priv', Host, User FROM mysql.user WHERE Create_tablespace_priv = 'Y' UNION ALL SELECT 'Create_role_priv', Host, User FROM mysql.user WHERE Create_role_priv = 'Y' UNION ALL SELECT 'Drop_role_priv', Host, User FROM mysql.user WHERE Drop_role_priv = 'Y'
) AS p ON u.Host = p.Host AND u.User = p.User
GROUP BY u.Host, u.User;
"
    ["query_all_character_sets_supported_by_mysql"]="
show character set;
"
    ["some_important_parameters"]="
  SELECT
          Variable_name,
          CASE
                  WHEN Variable_name = 'innodb_buffer_pool_size' THEN CONCAT(ROUND(VARIABLE_VALUE / 1024 / 1024, 2),'M')
                  ELSE VARIABLE_VALUE
          END AS Value
  FROM
          performance_schema.GLOBAL_VARIABLES
  WHERE
          Variable_name IN (
                  'port',
                  'skip_name_resolve',
                  'innodb_page_size',
                  'lock_wait_timeout',
                  'performance_schema',
                  'transaction_isolation',
                  'datadir',
                  'SQL_MODE',
                  'socket',
                  'TIME_ZONE',
                  'tx_isolation',
                  'autocommit',
                  'innodb_lock_wait_timeout',
                  'max_connections',
                  'max_user_connections',
                  'slow_query_log',
                  'log_output',
                  'slow_query_log_file',
                  'long_query_time',
                  'log_queries_not_using_indexes',
                  'log_throttle_queries_not_using_indexes',
                  'pid_file',
                  'log_error',
                  'lower_case_table_names',
                  'innodb_buffer_pool_size',
                  'innodb_flush_log_at_trx_commit',
                  'read_only',
                  'log_slave_updates',
                  'innodb_io_capacity',
                  'query_cache_type',
                  'query_cache_size',
                  'max_connect_errors',
                  'server_id',
                  'innodb_file_per_table'
          );
"
    ["view_the_users_and_hosts_currently_connected_to_the_database"]="
select concat(processlist_user,'@',processlist_host) as Account, count(*) as Connections from performance_schema.threads  where TYPE != 'BACKGROUND'  and processlist_user is not null group by  processlist_user,processlist_host;
"
    ["view_the_current_connections_and_total_connections_of_each_host"]="
-- 系统表performance_schema.hosts在MySQL 5.6.3版本中引入，用来保存MySQL服务器启动后的连接情况。
SELECT * FROM performance_schema.hosts;
show variables like 'max_connections';
"
    ["view_login_information_according_to_login_user_login_server"]="
SELECT USER AS login_user,
	LEFT ( HOST, POSITION( ':' IN HOST ) - 1 ) AS login_ip,
	count( 1 ) AS login_count
FROM \`information_schema\`.\`PROCESSLIST\` P
WHERE P.USER NOT IN ( 'root', 'repl', 'system user' )
GROUP BY USER,LEFT ( HOST, POSITION( ':' IN HOST ) - 1 );
"
    ["view_login_information_according_to_login_user_database_login_server"]="
SELECT  DB AS database_name,
	USER AS login_user,
	LEFT ( HOST, POSITION( ':' IN HOST ) - 1 ) AS login_ip,
	count( 1 ) AS login_count
FROM  \`information_schema\`.\`PROCESSLIST\` P
WHERE P.USER NOT IN ( 'root', 'repl', 'system user' )
GROUP BY DB,USER,LEFT(HOST, POSITION( ':' IN HOST ) - 1 );

"
    ["query_all_threads_excluding_sleep_threads"]="
SELECT name,thread_id,type,processlist_user as user, processlist_host as host,processlist_command as command, processlist_time as time, processlist_state as state ,PROCESSLIST_INFO as info FROM performance_schema.threads a where  a.PROCESSLIST_ID<>CONNECTION_id() ;
"
    ["version_information"]="-- show variables like 'version_%';

select version();
"
    ["sleep_thread_top20"]="
SELECT name,thread_id,type,processlist_user as user, processlist_host as host,processlist_command as command, processlist_time as time, processlist_state as state,processlist_info as info  FROM performance_schema.threads a where  a.PROCESSLIST_COMMAND = 'Sleep'  and a.PROCESSLIST_ID<>CONNECTION_id() order by time desc  limit 20;
"
    ["how_many_threads_are_using_the_table"]="
show open tables where in_use > 0;
"
    ["query_the_runtime_information_of_innodb_storage_engine_including_the_details_of_deadlock"]="
show engine innodb status;
"
    ["view_the_innodb_lock_generated_by_the_current_state_and_the_result_is_output_only_when_there_is_a"]="
select * from information_schema.innodb_locks;
"
    ["view_the_innodb_lock_wait_generated_by_the_current_state_the_result_is_output_only_when_there_is_a"]="
select * from information_schema.innodb_lock_waits;
"
    ["current_active_transactions_in_the_current_innodb_kernel"]="
select trx_id as id, trx_weight as weight, trx_state as state,trx_wait_started as started,trx_isolation_level as level,trx_query as query from information_schema.innodb_trx;
"
    ["lock_details"]="
select r.trx_isolation_level,
       r.trx_id              waiting_trx_id,
       r.trx_mysql_thread_id waiting_trx_thread,
       r.trx_state           waiting_trx_state,
       lr.lock_mode          waiting_trx_lock_mode,
       lr.lock_type          waiting_trx_lock_type,
       lr.lock_table         waiting_trx_lock_table,
       lr.lock_index         waiting_trx_lock_index,
       r.trx_query           waiting_trx_query,
       b.trx_id              blocking_trx_id,
       b.trx_mysql_thread_id blocking_trx_thread,
       b.trx_state           blocking_trx_state,
       lb.lock_mode          blocking_trx_lock_mode,
       lb.lock_type          blocking_trx_lock_type,
       lb.lock_table         blocking_trx_lock_table,
       lb.lock_index         blocking_trx_lock_index,
       b.trx_query           blocking_query
  from information_schema.innodb_lock_waits w
 inner join information_schema.innodb_trx b
    on b.trx_id = w.blocking_trx_id
 inner join information_schema.innodb_trx r
    on r.trx_id = w.requesting_trx_id
 inner join information_schema.innodb_locks lb
    on lb.lock_trx_id = w.blocking_trx_id
 inner join information_schema.innodb_locks lr
    on lr.lock_trx_id = w.requesting_trx_id;
    "
    ["metadata_lock_related_information"]="select * from performance_schema.setup_instruments WHERE name='wait/lock/metadata/sql/mdl';
"
    ["view_the_status_of_the_server"]="
show status where  variable_name in
('Handler_external_lock',
'Innodb_row_lock_current_waits',
'Innodb_row_lock_time',
'Innodb_row_lock_time_avg',
'Innodb_row_lock_time_max ',
'Innodb_row_lock_waits',
'Key_blocks_not_flushed',
'Key_blocks_unused',
'Key_blocks_used',
'Locked_connects',
'Performance_schema_locker_lost',
'Performance_schema_metadata_lock_lost',
'Performance_schema_rwlock_classes_lost',
'Performance_schema_rwlock_instances_lost',
'Performance_schema_table_lock_stat_lost',
'Table_locks_immediate',
'Table_locks_waited',
'Connection_errors_internal',
'Connection_errors_max_connections',
'Innodb_buffer_pool_pages_data',
'Innodb_buffer_pool_pages_free',
'Innodb_buffer_pool_pages_total',
'Innodb_buffer_pool_read_ahead',
'Innodb_buffer_pool_read_ahead_evicted',
'Innodb_buffer_pool_read_requests',
'Innodb_buffer_pool_reads',
'Innodb_buffer_pool_wait_free',
'Innodb_log_waits',
'Innodb_page_size',
'Max_used_connections',
'Slow_queries');
"
    ["track_the_progress_of_long_term_operations"]="
select event_name as name,thread_id,timer_start as start,timer_end as end, timer_wait as wait from performance_schema.events_stages_current;
"
    ["plug_in_information"]="SELECT PLUGIN_NAME as Name, PLUGIN_VERSION as version, PLUGIN_STATUS as status, PLUGIN_TYPE as type FROM INFORMATION_SCHEMA.PLUGINS; -- SHOW PLUGINS;
"
    ["view_the_statements_whose_average_execution_time_value_is_greater_than_95pct_of_the_average_execut"]="SELECT DIGEST,REPLACE(REPLACE(QUERY_SAMPLE_TEXT, '\n', ''), '\r', '') AS query,
       SCHEMA_NAME as db,
       COUNT_STAR AS exec_count,
       SUM_ERRORS AS err_count,
       round(AVG_TIMER_WAIT/1e9,6) as avg_latency_ms,
       round(MAX_TIMER_WAIT/1e9,6) AS max_latency_ms,
       ROUND(IFNULL(SUM_ROWS_SENT / NULLIF(COUNT_STAR, 0), 0)) AS rows_sent_avg,
       ROUND(IFNULL(SUM_ROWS_EXAMINED / NULLIF(COUNT_STAR, 0), 0)) AS rows_examined_avg
FROM performance_schema.events_statements_summary_by_digest stmts
         JOIN sys.x\$ps_digest_95th_percentile_by_avg_us AS top_percentile
              ON ROUND(stmts.avg_timer_wait/1000000) >= top_percentile.avg_us  where COUNT_STAR > 10
ORDER BY AVG_TIMER_WAIT DESC limit 10;
"
    ["view_the_currently_executing_statement_progress_information"]="
select conn_id,user,db,command,state,tmp_tables,last_statement,program_name from sys.session where conn_id!=connection_id() and trx_state='ACTIVE';
"
    ["view_statistics_related_to_executed_statements"]="
select thd_id,conn_id,user,db,command,time,last_statement_latency,current_memory,trx_latency,trx_autocommit,pid from sys.session where conn_id!=connection_id() and trx_state='COMMITTED';
"
    ["view_the_statements_that_use_temporary_tables_by_default_they_are_sorted_in_descending_order_by_th"]="
select REPLACE(REPLACE(QUERY_SAMPLE_TEXT, '\n', ''), '\r', '') as query,
       SCHEMA_NAME as db,
       COUNT_STAR AS exec_count,
       sys.format_time(SUM_TIMER_WAIT) as total_latency,
       SUM_CREATED_TMP_TABLES AS total_tmp_tables,
       SUM_CREATED_TMP_DISK_TABLES AS disk_tmp_tables,
       ROUND(IFNULL(SUM_CREATED_TMP_TABLES / NULLIF(COUNT_STAR, 0), 0)) AS avg_tmp_tables_per_query,
       ROUND(IFNULL(SUM_CREATED_TMP_DISK_TABLES / NULLIF(SUM_CREATED_TMP_TABLES, 0), 0) * 100) AS tmp_tables_to_disk_pct
FROM performance_schema.events_statements_summary_by_digest
WHERE SUM_CREATED_TMP_TABLES > 0 and COUNT_STAR > 10
ORDER BY SUM_CREATED_TMP_DISK_TABLES DESC, SUM_CREATED_TMP_TABLES DESC limit 10;
"
    ["top_10_sql_statements_with_temporary_tables"]="
SELECT
        REPLACE(REPLACE(performance_schema.events_statements_summary_by_digest.DIGEST_TEXT, '\n', ''), '\r', '') AS query,
        performance_schema.events_statements_summary_by_digest.SCHEMA_NAME AS db,
        performance_schema.events_statements_summary_by_digest.COUNT_STAR AS exec_count,
        CONCAT(ROUND(performance_schema.events_statements_summary_by_digest.AVG_TIMER_WAIT / 10000000000, 2), ' ms')  AS avg_latency,
        ROUND(IFNULL((performance_schema.events_statements_summary_by_digest.SUM_ROWS_SENT / NULLIF(performance_schema.events_statements_summary_by_digest.COUNT_STAR,0)),0),0) AS rows_sent_avg,
        ROUND(IFNULL((performance_schema.events_statements_summary_by_digest.SUM_ROWS_EXAMINED / NULLIF(performance_schema.events_statements_summary_by_digest.COUNT_STAR,0)),0),0) AS rows_examined_avg,
        performance_schema.events_statements_summary_by_digest.SUM_CREATED_TMP_TABLES AS tmp_tables,
        performance_schema.events_statements_summary_by_digest.SUM_CREATED_TMP_DISK_TABLES AS tmp_disk_tables,
        performance_schema.events_statements_summary_by_digest.SUM_SORT_ROWS AS rows_sorted
FROM
        performance_schema.events_statements_summary_by_digest where  performance_schema.events_statements_summary_by_digest.SUM_CREATED_TMP_TABLES > 0
ORDER BY performance_schema.events_statements_summary_by_digest.SUM_CREATED_TMP_TABLES DESC LIMIT 10;
"
    ["view_the_statements_that_have_performed_file_sorting_by_default_they_are_sorted_in_descending_orde"]="
SELECT REPLACE(REPLACE(QUERY_SAMPLE_TEXT, '\n', ''), '\r', '') AS query,
       SCHEMA_NAME db,
       COUNT_STAR AS exec_count,
       sys.format_time(SUM_TIMER_WAIT) AS total_latency,
       SUM_SORT_SCAN AS sorts_using_scans,
       SUM_SORT_RANGE AS sort_using_range,
       SUM_SORT_ROWS AS rows_sorted,
       ROUND(IFNULL(SUM_SORT_ROWS / NULLIF(COUNT_STAR, 0), 0)) AS avg_rows_sorted
FROM performance_schema.events_statements_summary_by_digest
WHERE SUM_SORT_ROWS > 0
ORDER BY SUM_TIMER_WAIT DESC limit 10;
"
    ["overall_consumption_percentage_of_query_sql"]="
select state,
       sum(duration) as total_r,
       round(100 * sum(duration) / (select sum(duration) from information_schema.profiling  where query_id = 1),2) as pct_r,
       count(*) as calls,
       sum(duration) / count(*) as \"r/call\"
  from information_schema.profiling
 where query_id = 1
 group by state
 order by total_r desc;
 "
    ["execution_times_top10"]="
SELECT
		REPLACE(REPLACE(performance_schema.events_statements_summary_by_digest.DIGEST_TEXT, '\n', ''), '\r', '') AS query,
		performance_schema.events_statements_summary_by_digest.SCHEMA_NAME AS db,
		performance_schema.events_statements_summary_by_digest.COUNT_STAR AS exec_count,
		CONCAT(ROUND(performance_schema.events_statements_summary_by_digest.AVG_TIMER_WAIT / 10000000000, 2), ' ms') AS avg_latency,
		ROUND(IFNULL((performance_schema.events_statements_summary_by_digest.SUM_ROWS_SENT / NULLIF(performance_schema.events_statements_summary_by_digest.COUNT_STAR,0)),0),0) AS rows_sent_avg,
		ROUND(IFNULL((performance_schema.events_statements_summary_by_digest.SUM_ROWS_EXAMINED / NULLIF(performance_schema.events_statements_summary_by_digest.COUNT_STAR,0)),0),0) AS rows_examined_avg,
		performance_schema.events_statements_summary_by_digest.SUM_CREATED_TMP_TABLES AS tmp_tables,
		performance_schema.events_statements_summary_by_digest.SUM_CREATED_TMP_DISK_TABLES AS tmp_disk_tables,
		performance_schema.events_statements_summary_by_digest.SUM_SORT_ROWS AS rows_sorted
FROM
		performance_schema.events_statements_summary_by_digest where  performance_schema.events_statements_summary_by_digest.SUM_CREATED_TMP_TABLES > 0
ORDER BY performance_schema.events_statements_summary_by_digest.COUNT_STAR DESC LIMIT 10
"
    ["sql_statement_using_full_table_scan"]="SELECT object_schema,
  object_name, -- 表名
  count_read AS rows_full_scanned,  -- 全表扫描的总数据行数
  sys.format_time(sum_timer_wait) AS latency -- 完整的表扫描操作的总延迟时间（执行时间）
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NULL
AND count_read > 0
ORDER BY count_read DESC limit 10;
"
    ["view_the_full_table_scan_or_the_statements_that_do_not_use_the_optimal_index_the_statement_text_af"]="
SELECT REPLACE(REPLACE(QUERY_SAMPLE_TEXT, '\n', ''), '\r', '') AS query,
       SCHEMA_NAME as db,
       COUNT_STAR AS exec_count,
       sys.format_time(SUM_TIMER_WAIT) AS total_latency,
       SUM_NO_INDEX_USED AS no_index_used_count,
       SUM_NO_GOOD_INDEX_USED AS no_good_index_used_count,
       ROUND(IFNULL(SUM_NO_INDEX_USED / NULLIF(COUNT_STAR, 0), 0) * 100) AS no_index_used_pct,
       SUM_ROWS_SENT AS rows_sent,
       SUM_ROWS_EXAMINED AS rows_examined,
       ROUND(SUM_ROWS_SENT/COUNT_STAR) AS rows_sent_avg,
       ROUND(SUM_ROWS_EXAMINED/COUNT_STAR) AS rows_examined_avg
FROM performance_schema.events_statements_summary_by_digest
WHERE (SUM_NO_INDEX_USED > 0
    OR SUM_NO_GOOD_INDEX_USED > 0)
  AND DIGEST_TEXT NOT LIKE 'SHOW%'
ORDER BY no_index_used_pct DESC, total_latency DESC limit 10;
"
    ["all_databases_of_the_current_database_instance_and_their_capacity"]="-- show databases;
select a.SCHEMA_NAME,a.DEFAULT_COLLATION_NAME,
       sum(table_rows) as table_rows,
       truncate(sum(data_length)/1024/1024, 2) as data_size_mb,
       truncate(sum(index_length)/1024/1024, 2) as index_size_mb,
       truncate(sum(data_length+index_length)/1024/1024, 2) as all_size_mb,
       truncate(sum(data_free)/1024/1024, 2) as free_size_mb
from INFORMATION_SCHEMA.SCHEMATA a
         left outer join information_schema.tables b
                         on a.SCHEMA_NAME=b.TABLE_SCHEMA
         left outer join
     (select substring(b.file_name,3,locate('/',b.file_name,3)-3) as db_name,
             truncate(sum(total_extents*extent_size)/1024/1024,2) filesize_M
      from  information_schema.FILES b
      group by substring(b.file_name,3,locate('/',b.file_name,3)-3)) f
     on ( a.SCHEMA_NAME= f.db_name)
group by a.SCHEMA_NAME,a.DEFAULT_COLLATION_NAME
order by sum(data_length) desc, sum(index_length) desc;
"
    ["view_the_statements_that_generate_errors_or_warnings_by_default_they_are_sorted_in_descending_orde"]="
SELECT REPLACE(REPLACE(QUERY_SAMPLE_TEXT, '\n', ''), '\r', '') AS query,
       SCHEMA_NAME as db,
       COUNT_STAR AS exec_count,
       SUM_ERRORS AS errors,
       IFNULL(SUM_ERRORS / NULLIF(COUNT_STAR, 0), 0) * 100 as error_pct,
       SUM_WARNINGS AS warnings,
       IFNULL(SUM_WARNINGS / NULLIF(COUNT_STAR, 0), 0) * 100 as warning_pct
FROM performance_schema.events_statements_summary_by_digest
WHERE SUM_ERRORS > 0
   OR SUM_WARNINGS > 0
ORDER BY SUM_ERRORS DESC, SUM_WARNINGS DESC limit 10;

"
    ["redundant_index"]="
-- 若库很大，这个视图可能查询不出结果，可以摁一次“ctrl+c”跳过这个SQL
-- select * from sys.schema_redundant_indexes;
"
    ["invalid_index_index_never_used"]="SELECT * FROM sys.schema_unused_indexes WHERE object_schema NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');
"
    ["index_discrimination_of_each_table_top_100"]="
SELECT
i.database_name ASdb,
i.table_name AStable,
i.index_name ASindex_name,
i.stat_description AScols,
i.stat_value ASdefferRows,
t.n_rows ASROWS,
ROUND(((i.stat_value / IFNULL(IF(t.n_rows < i.stat_value,i.stat_value,t.n_rows),0.01))),2) AS sel_persent
FROM mysql.innodb_index_stats i
INNER JOIN mysql.innodb_table_stats t
ON i.database_name = t.database_name AND i.table_name= t.table_name
WHERE i.index_name != 'PRIMARY' AND i.stat_name LIKE '%n_diff_pfx%'
and ROUND(((i.stat_value / IFNULL(IF(t.n_rows < i.stat_value,i.stat_value,t.n_rows),0.01))),2)<0.1
and t.n_rows !=0
and i.stat_value !=0
and i.database_name not in ('mysql', 'information_schema', 'sys', 'performance_schema')
limit 100;

"
    ["important_parameters_involved_in_master-slave_replication"]="
show global VARIABLES where  VARIABLE_NAME in  ('slave_preserve_commit_order','slave_parallel_type','slave_parallel_workers','gtid_mode','enforce_gtid_consistency','server_id','server_uuid','log_bin','log_bin_basename','sql_log_bin','log_bin_index','log_slave_updates','read_only','slave_skip_errors','max_allowed_packet','slave_max_allowed_packet','auto_increment_increment','auto_increment_offset','sync_binlog','binlog_format','expire_logs_days','max_binlog_size','slave_skip_errors','sql_slave_skip_counter','slave_exec_mode') ;
"
    ["master_slave_library_thread"]="
-- show full processlist;
-- SELECT * FROM information_schema.\`PROCESSLIST\`;
SELECT THREAD_ID,NAME,TYPE,PROCESSLIST_ID as ID,PROCESSLIST_USER AS USER,PROCESSLIST_HOST AS HOST,PROCESSLIST_DB AS DB,PROCESSLIST_COMMAND AS COMMAND,PROCESSLIST_TIME AS TIME,PROCESSLIST_STATE AS STATE,PROCESSLIST_INFO AS INFO
FROM performance_schema.threads a
WHERE a.\`NAME\` IN ( 'thread/sql/slave_io', 'thread/sql/slave_sql' ) or a.PROCESSLIST_COMMAND='Binlog Dump' ;
SELECT * FROM information_schema.\`PROCESSLIST\` a where a.USER='system user' or a.command='Binlog Dump';
"
    ["binary_log"]="
show binary logs; -- show master logs;
"
    ["view_all_slave_libraries_on_the_master_side"]="
show slave hosts;
"
    ["mgr_details"]="
SELECT * FROM performance_schema.replication_group_members;
"
    ["main_warehouse_status_monitoring"]="
show master status;
"
    ["database_object"]="select db as db_name ,type as ob_type,cnt as sums from
(select 'TABLE' type,table_schema db, count(*) cnt  from information_schema.\`TABLES\` a where table_type='BASE TABLE' group by table_schema
union all
select 'EVENTS' type,event_schema db,count(*) cnt from information_schema.\`EVENTS\` b group by event_schema
union all
select 'TRIGGERS' type,trigger_schema db,count(*) cnt from information_schema.\`TRIGGERS\` c group by trigger_schema
union all
select 'PROCEDURE' type,routine_schema db,count(*) cnt from information_schema.ROUTINES d where\`ROUTINE_TYPE\` = 'PROCEDURE' group by db
union all
select 'FUNCTION' type,routine_schema db,count(*) cnt  from information_schema.ROUTINES d where\`ROUTINE_TYPE\` = 'FUNCTION' group by db
union all
select 'VIEWS' type,TABLE_SCHEMA db,count(*) cnt  from information_schema.VIEWS f group by table_schema  ) t
order by db,type;
"
    ["slave_database_status_monitoring_data_is_available_only_when_the_slave_database_is_executed"]="show slave status;
"
    ["binary_log_events"]="
show binlog events limit 2,60 ;
-- show binlog events in 'rhel6lhr-bin.000003';

"
    ["performance_parameter_statistics"]="
show global status where  VARIABLE_NAME  in ('Innodb_buffer_pool_pages_data','Innodb_buffer_pool_pages_free','Innodb_buffer_pool_pages_total','Innodb_buffer_pool_read_ahead','Innodb_buffer_pool_read_ahead_evicted','Innodb_buffer_pool_read_requests','Innodb_buffer_pool_reads','Innodb_buffer_pool_wait_free','Innodb_log_waits','Innodb_page_size','connections','uptime','slow_queries','Created_tmp_tables','Created_tmp_files','Created_tmp_disk_tables','table_cache','Handler_read_rnd_next','Table_locks_immediate','Table_locks_waited','Open_files','Opened_tables','Sort_merge_passes','Sort_range','Sort_rows','Sort_scan');
"
    ["_setup_consumers"]="
SELECT * FROM performance_schema.setup_consumers;
"
    ["usage_of_self_increment_id_top_20"]="SELECT table_schema,table_name,engine, Auto_increment
 FROM information_schema.tables a
 where TABLE_SCHEMA not in ('mysql', 'information_schema', 'sys', 'performance_schema')
 and  a.Auto_increment<>''
 order by a.AUTO_INCREMENT desc
limit 20 ;
"
    ["table_without_primary_key_or_unique_key_top_100"]="select table_schema, table_name
 from information_schema.tables
where table_type='BASE TABLE'
 and  (table_schema, table_name) not in ( select /*+ subquery(materialization) */ a.TABLE_SCHEMA,a.TABLE_NAME
           from information_schema.TABLE_CONSTRAINTS a
		   where a.CONSTRAINT_TYPE in ('PRIMARY KEY','UNIQUE')
		   and table_schema not in    ('mysql', 'information_schema', 'sys', 'performance_schema')	)
 AND table_schema not in  ('mysql', 'information_schema', 'sys', 'performance_schema')
limit 100 ;
"
    ["view_the_running_status_of_the_database"]="status;
"
    ["top_10_big_tables_with_the_largest_space"]="SELECT
    table_schema AS db_name,
    table_name AS table_name,
    a.\`ENGINE\`,
    table_rows AS table_rows,
    TRUNCATE(a.DATA_LENGTH / 1024 / 1024, 2 ) AS tb_size_mb,
    TRUNCATE( ( data_length + index_length ) / 1024 / 1024, 2 ) AS all_size_mb,
    TRUNCATE( a.DATA_FREE / 1024 / 1024, 2 ) AS free_size_mb
FROM information_schema.TABLES a
         left outer join
     (select substring(b.file_name,3,locate('/',b.file_name,3)-3) as db_name,
             substring(b.file_name,locate('/',b.file_name,3)+1,(LENGTH(b.file_name)-locate('/',b.file_name,3)-4)) as tb_name,
             b.file_name,
             (total_extents*extent_size)/1024/1024 filesize_M
      from  information_schema.FILES b
      order by filesize_M desc limit 20 ) f
     on ( a.TABLE_SCHEMA= f.db_name and a.TABLE_NAME=f.tb_name )
ORDER BY	( data_length + index_length ) DESC
    LIMIT 10;
"
    ["top_10_indexes_with_the_largest_footprint"]="
select
iis.database_name,
iis.table_name,
iis.index_name,
round((iis.stat_value*@@innodb_page_size)/1024/1024, 2) SizeMB,
-- round(((100/(SELECT INDEX_LENGTH FROM INFORMATION_SCHEMA.TABLES t WHERE t.TABLE_NAME = iis.table_name and t.TABLE_SCHEMA = iis.database_name))*(stat_value*@@innodb_page_size)), 2) \`Percentage\`,
s.NON_UNIQUE,
s.INDEX_TYPE,
GROUP_CONCAT(s.COLUMN_NAME order by SEQ_IN_INDEX) COLUMN_NAME
from (select * from mysql.innodb_index_stats
				WHERE index_name  not in ('PRIMARY','GEN_CLUST_INDEX') and stat_name='size'
				order by (stat_value*@@innodb_page_size) desc limit 10
			) iis
left join INFORMATION_SCHEMA.STATISTICS s
on (iis.database_name=s.TABLE_SCHEMA and iis.table_name=s.TABLE_NAME and iis.index_name=s.INDEX_NAME)
GROUP BY iis.database_name,iis.TABLE_NAME,iis.INDEX_NAME,(iis.stat_value*@@innodb_page_size),s.NON_UNIQUE,s.INDEX_TYPE
order by (stat_value*@@innodb_page_size) desc;
"
    ["list_of_all_storage_engines"]="
show engines;
-- SELECT * from information_schema.\`ENGINES\`;
"
)

getMysqlInfo(){
	mysqlusername="$1"
	mysqlpassword="$2"
	mysqlport="$3"
	mysqlsockpath="$4"
	outputfile="$5"
	hostname="$6"


	for key in "${!sql_dict[@]}"; do
		#sql="${sql_dict[$key]}"
		# 使用 sed 动态替换 {query_text_field} 为实际字段名
        sql=$(echo "${sql_dict[$key]}" | sed "s/QUERY_SAMPLE_TEXT/${query_text_field}/g")
		sql=$(echo "${sql}" | sed -e "s|UNION ALL SELECT 'Create_role_priv', Host, User FROM mysql.user WHERE Create_role_priv = 'Y' UNION ALL SELECT 'Drop_role_priv', Host, User FROM mysql.user WHERE Drop_role_priv = 'Y'|${create_and_drop}|g")

		echo "\${edith:$key@$hostname}" >> $outputfile
		# 这里替换成实际执行SQL的命令
		#mysql -u$mysqlUsername -p$mysqlPassword -X -e "$sql"  > /dev/null 2>&1 >> $outputfile
		mysql -u$mysqlusername -p$mysqlpassword -P$mysqlport -S $mysqlsockpath"/mysql.sock"  -X -e "$sql" 2>&1 >> $outputfile
	done
}

getHost(){
	local output_file="$1"

	# 获取主机名
	hostname=$(hostname)
	# 获取系统运行时间（以秒为单位）
	uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
	# 获取启动时间（以秒为单位，自1970年1月1日UTC以来的秒数）
	boot_time=$(awk '/btime/ {print $2}' /proc/stat)
	# 获取进程数
	procs=$(ps -e | wc -l)
	# 获取操作系统信息
	os=$(uname -s)
	# 获取平台信息
	platform=$(grep -oP '(?<=^ID=).+' /etc/os-release | tr -d '"')
	platform_family=$(cat /etc/os-release | grep ^ID_LIKE= | cut -d= -f2 | cut -d' ' -f1 | tr -d '"')
	platform_version=$(grep -oP '(?<=^VERSION_ID=).+' /etc/os-release | tr -d '"')
	# 获取内核版本和架构
	kernel_version=$(uname -r)
	kernel_arch=$(uname -m)
	# 获取虚拟化系统信息
	virtualization_system=""
	virtualization_role="guest"
	# 获取主机ID
	host_id=$(dmidecode -s system-serial-number)

	# 输出XML格式的信息到文件
cat << EOF > $output_file
\${edith:host@$hostname}
<?xml version="1.0"?>
<resultset statement="" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
		<field name="hostname">$hostname</field>
		<field name="uptime">$uptime_seconds</field>
		<field name="bootTime">$boot_time</field>
		<field name="procs">$procs</field>
		<field name="os">$os</field>
		<field name="platform">$platform</field>
		<field name="platformFamily">$platform_family</field>
		<field name="platformVersion">$platform_version</field>
		<field name="kernelVersion">$kernel_version</field>
		<field name="kernelArch">$kernel_arch</field>
		<field name="virtualizationSystem">$virtualization_system</field>
		<field name="virtualizationRole">$virtualization_role</field>
		<field name="hostId">$host_id</field>
  </row>
</resultset>
EOF
}

getPort(){
	local port="$1"
	local output_file="$2"
	cat << EOF >> $output_file
\${edith:port@$hostname}
<?xml version="1.0"?>
<resultset statement="" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
		<field name="port">$port</field>
  </row>
</resultset>
EOF
}


getIPADDR(){
	local ipaddr="$1"
	local output_file="$2"
	cat << EOF >> $output_file
\${edith:ipaddr@$hostname}
<?xml version="1.0"?>
<resultset statement="" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
		<field name="ipaddr">$ipaddr</field>
  </row>
</resultset>
EOF
}


# 获取 MySQL 版本号
get_mysql_version() {
    local mysqlusername="$1"
    local mysqlpassword="$2"
    local mysqlport="$3"
    local mysqlsockpath="$4"
    local version=$(mysql -u$mysqlusername -p$mysqlpassword -P$mysqlport -S $mysqlsockpath/mysql.sock -e "SELECT VERSION();" 2>/dev/null | tail -n 1)
    echo $version
}

# 根据 MySQL 版本设置查询字段
set_query_text_field() {
    local version="$1"
    if [[ $version == 5.7* ]]; then
        query_text_field="DIGEST_TEXT"
		create_and_drop=""
    else
        query_text_field="QUERY_SAMPLE_TEXT"
		create_and_drop=" UNION ALL SELECT 'Create_role_priv', Host, User FROM mysql.user WHERE Create_role_priv = 'Y' UNION ALL SELECT 'Drop_role_priv', Host, User FROM mysql.user WHERE Drop_role_priv = 'Y'"
    fi
}


shell(){

	# 检查参数个数
	if [ $# -ne 5 ]; then
		echo "--help:"
		echo "      sh $0 mysql用户名 mysql密码 mysql端口 sock路径 输出eout路径"
		echo "示例：sh $0 root root1234 3306 /tmp ./"
		exit 1
	fi

	username="$1"
	password="$2"
	port="$3"
	sockpath="$4"
	outputpath="$5"

	# 获取 MySQL 版本
    version=$(get_mysql_version $username $password $port $sockpath)
	echo "MySQL Version: $version"
	set_query_text_field "$version"

	# 获取主机名
	hostname=$(hostname)

	# 获取当前时间
	curDateTime=$(date +"%Y%m%d%H%M%S")

	#pid=$(ps -ef | grep "mysqld" | grep -v grep | awk '{print $2}')
	#port=$(netstat -tnlp | grep "$pid" | awk '{print $4}' | awk -F ":" '{print $2}' | uniq | head -1)

	# 检查 $outputpath 是否以斜杠结尾
	if [[ "$outputpath" == */ ]]; then
	  # 去掉结尾的斜杠
	  outputpath="${outputpath%/}"
	fi

	# 检查 $sockpath 是否以斜杠结尾
	if [[ "$sockpath" == */ ]]; then
	  # 去掉结尾的斜杠
	  sockpath="${sockpath%/}"
	fi

	outputfile="$outputpath/MySQL.$port.$hostname.$curDateTime.eout"

	# 获取host信息
	getHost $outputfile

	# 写入端口信息
	getPort $port $outputfile

	# 写入IP信息
    pyIP=$(python -c 'import socket;s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);s.connect(("255.255.255.0",80));ip = s.getsockname()[0];s.close();print(ip)')
    if [ "$pyIP" = "" ];then
      ip=$(cat /etc/hosts| grep -v "#" |awk -v HN=$(hostname) '($NF==HN){print $1}')
    else
      ip=$pyIP
    fi
    if [ "$ip" = "" ];then
	  ip='127.0.0.1'
    fi
    getIPADDR $ip $outputfile

	# 获取mysql信息
	getMysqlInfo $username $password $port $sockpath $outputfile $hostname
}

shell $1 $2 $3 $4 $5
