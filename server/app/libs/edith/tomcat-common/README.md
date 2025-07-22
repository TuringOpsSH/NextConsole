# README

## 巡检模板

Tomcat 巡检对应的巡检模板为 `tomcat-common-版本.zip`。

## 数据采集

```bash
edith tomcat get-log --path /app/apache-tomcat-8.5.75 -o /tmp -f json
edith tomcat get-conf --path /app/apache-tomcat-8.5.75 -o /tmp -f json
```
其中`--path` 用于指定安装目录，即`webapps`的上层目录。