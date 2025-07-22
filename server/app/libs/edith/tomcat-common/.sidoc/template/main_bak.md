{{define "main_bak"}}

{{template "meta" .}}

# 巡检信息

{{template "mission" .}}

# 系统参数检查

## CPU负载
{{template "cpu" .}}

## 内存使用情况
{{template "mem" .}}

## 磁盘使用率统计
{{template "disk" .}}

# Tomcat
## 基本信息 
{{template "basicInfo" .}}

## JVM参数
{{template "tomcat.jvmParam" .}}

## 版本信息
{{template "tomcat.webConf" .}}

## 配置参数
### 主机列表
{{template "tomcat.host" .}}

### 配置文件server.xml
{{template "tomcat.serverConf" .}}

### 配置文件web.xml
{{template "tomcat.webConf" .}}

## 状态信息
{{template "tomcat.status" .}}

## 日志
{{template "tomcat.logs" .}}
{{end}}