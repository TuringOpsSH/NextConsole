import xml.etree.ElementTree as ET


content = '''<?xml version="1.0"?>
<resultset statement="SELECT
    version() Server_version,
    ( SELECT sum( TRUNCATE ( ( data_length + index_length ) / 1024 / 1024, 2 ) ) AS 'all_db_size(MB)' FROM information_schema.TABLES b ) db_size_MB,
    (select truncate(sum(total_extents*extent_size)/1024/1024,2) from  information_schema.FILES b) datafile_size_MB,
    ( SELECT @@datadir ) datadir,
    ( SELECT @@SOCKET ) SOCKET,
    ( SELECT @@log_bin ) log_bin,
    ( SELECT @@server_id ) server_id" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
	<field name="Server_version">8.0.34</field>
	<field name="db_size_MB">8072.12</field>
	<field name="datafile_size_MB">9217.00</field>
	<field name="datadir">/usr/local/mysql/data/</field>
	<field name="SOCKET">/tmp/mysql.sock</field>
	<field name="log_bin">1</field>
	<field name="server_id">1</field>
  </row>
</resultset>
'''

content1 = '''<?xml version="1.0"?>
<resultset statement="SELECT  CONCAT(FLOOR(UPTIME / 86400), ' days, ', FLOOR((UPTIME % 86400) / 3600), ' hours, ', FLOOR((UPTIME % 3600) / 60), ' minutes, ',(UPTIME % 60), ' seconds' ) AS Uptime FROM (SELECT VARIABLE_VALUE AS UPTIME  FROM performance_schema.GLOBAL_STATUS  WHERE VARIABLE_NAME = 'Uptime') AS T" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
	<field name="Uptime">26 days, 23 hours, 41 minutes, 41 seconds</field>
  </row>
</resultset>
'''

content2 = '''<?xml version="1.0"?>
<resultset statement="SELECT
    version() Server_version,
    ( SELECT sum( TRUNCATE ( ( data_length + index_length ) / 1024 / 1024, 2 ) ) AS 'all_db_size(MB)' FROM information_schema.TABLES b ) db_size_MB,
    (select truncate(sum(total_extents*extent_size)/1024/1024,2) from  information_schema.FILES b) datafile_size_MB,
    ( SELECT @@datadir ) datadir,
    ( SELECT @@SOCKET ) SOCKET,
    ( SELECT @@log_bin ) log_bin,
    ( SELECT @@server_id ) server_id" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
	<field name="Server_version">8.0.34</field>
	<field name="db_size_MB">8072.12</field>
	<field name="datafile_size_MB">9217.00</field>
	<field name="datadir">/usr/local/mysql/data/</field>
	<field name="SOCKET">/tmp/mysql.sock</field>
	<field name="log_bin">1</field>
	<field name="server_id">1</field>
  </row>
</resultset>
<?xml version="1.0"?>
<resultset statement="SELECT  CONCAT(FLOOR(UPTIME / 86400), ' days, ', FLOOR((UPTIME % 86400) / 3600), ' hours, ', FLOOR((UPTIME % 3600) / 60), ' minutes, ',(UPTIME % 60), ' seconds' ) AS Uptime FROM (SELECT VARIABLE_VALUE AS UPTIME  FROM performance_schema.GLOBAL_STATUS  WHERE VARIABLE_NAME = 'Uptime') AS T" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
	<field name="Uptime">26 days, 23 hours, 41 minutes, 41 seconds</field>
  </row>
</resultset>
'''

xmlStr = ET.fromstring(content1)
rows = xmlStr.findall('resultset')
print(rows)