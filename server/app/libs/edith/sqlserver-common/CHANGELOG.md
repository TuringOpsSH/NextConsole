# CHANGELOG

## [ Version: 1.1.5 ] - 2024-09-27

- 修改日志碎片检查(sqlserver.loginfo_check.js)文件 @欧阳婉姗
  - 实际值增加空格分隔

## [ Version: 1.1.4 ] - 2024-09-20

- 修改查看所有数据库的索引碎片信息的规则 @欧阳婉姗

## [ Version: 1.1.3 ] - 2024-09-04

- 修改sqlserver数据库大小和利用率的模板 @罗志远

## [ Version: 1.1.2 ] - 2024-04-29

- 修复活跃的用户进程及数量检查等检查项中特殊符号导致表格错位问题

## [ Version: 1.1.1 ] - 2023-12-30

- 非空且元素是字符串均认定为执行遇到异常提升报告生成容错能力

## [ Version: 1.1.0 ] - 2023-11-14

- 调整sqlserver模板CUP显示细节 @李付良

## [ Version: 1.0.9 ] - 2023-11-09

- 新增Sqlserver集群巡检项 @苗玉玺
  - winodws集群信息检查
  - AG属性检查
  - 监听器信息检查
  - AG同步状态检查
  - 主备切换前后状态

## [ Version: 1.0.8 ] - 2023-10-10

- I/0读响应时间检查新增时间单位 @苗玉玺
- I/0写响应时间检查新增时间单位并修复一处标题错误 @苗玉玺

## [ Version: 1.0.7 ] - 2023-10-10

- 完善内存使用率检查规则 @苗玉玺

## [ Version: 1.0.6 ] - 2023-10-09

- 未开启审计时告警 @苗玉玺
- 限制近一周所有数据库备份信息检查记录显示数量 @李付良

## [ Version: 1.0.5 ] - 2023-10-08

- 新增集群参数检查展示 @苗玉玺
- 优化低版本数据库异常结果判断 @王东升
- 解决数据库版本信息被截断问题 @苗玉玺
- 增加数据库SQL文本显示长度 @苗玉玺
- 新增`--skip | -k` 跳过收集指定巡检项 @欧阳婉姗

## [ Version: 1.0.4 ] - 2023-10-07

- 移除1个多余的文件增长类型检查 @苗玉玺
- 新增新增数据库参数配置 @苗玉玺
- 新增检查具有sysadmin权限的用户 @苗玉玺
- 新增检查是否使用了密码策略 @苗玉玺
- 新增检查是否开启了审计 @苗玉玺
- 新增统计信息情况检查 @苗玉玺
- 新增查看所有数据库的索引碎片信息 @苗玉玺
- 新增查看索引空间大于100M的索引信息 @苗玉玺
- 新增集群状态检查 @苗玉玺
- 新增集群信息检查 @苗玉玺
- 新增AG信息及状态检查 @苗玉玺
- 新增操作系统CPU、内存等检查 @苗玉玺
- 新增集群参数检查 @苗玉玺

## [ Version: 1.0.3 ] - 2023-06-16

- 结果数据与规则输入要求不符时跳过并打印, 涉及：@王圣家
  - 近一周所有数据库备份信息检查
  - 所有数据库检查
  - Windows系统磁盘空闲率检查
  - 表行数检查
  - 没有主键的表检查
  - 查看失败的job检查
  - 查看job执行情况检查
  - 查看各数据库Bufferpool使用情况检查

- 新增【批量将文件名中IP.号改为%号】按钮 @王圣家
- 资源配置为全局数据目录

## [ Version: 1.0.2 ] - 2023-05-22

- 若干规则优化

## [ Version: 1.0.1 ] - 2023-05-16

- 首个公开发布版本 @苗玉玺 @戴林 @陈赛兰


## [ Version: 1.0.0 ] - 2023-05-12

- 初始版本
