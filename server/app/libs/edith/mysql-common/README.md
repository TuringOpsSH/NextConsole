# MySQL 巡检

## 巡检模板

MySQL 巡检对应的巡检模板为 `mysql-common-版本号.zip`

## ***请各位工程师在与生产环境相同或相近的测试环境中执行命令，确认无误后再进入生产环境进行采集！**
## ***请各位工程师反复检查命令的完整性和正确性！**
## ***请各位工程师反复检查生成的文件是否是 .json 格式！**
## ***如遇问题，请使用 MySQL 命令行执行登录命令，对应向 edith 添加参数；若问题仍存在，请联系 edith 开发人员！**

## 数据采集

- 从 1.4.0 版本的模板开始，MySQL 报告新增系统检查项的检查结果
```bash
edith mysql get log conf status -u [MySQL用户名] --password [密码] -f json -o /tmp # MySQL

edith os get-conf -o /tmp -f json # 收集配置数据
edith os get-status -o /tmp -f json -c 5 # 收集状态数据
```
- 至此，一次完整的 MySQL 报告生成前的数据采集工作已经准备完毕，请工程师直接到 /tmp 或自定义目录下下载json文件，并结合 sidoc 完成后续报告生成工作。



## 高级功能（建议在测试环境中熟练使用后再到生产环境中使用）

### 按数据类型分别采集

```bash
edith mysql get-log  -u [MySQL用户名] --password [密码] -f json -o /tmp
edith mysql get-conf  -u [MySQL用户名] --password [密码] -f json -o /tmp
edith mysql get-status -u [MySQL用户名] --password [密码] -f json -o /tmp

指定 MySQL bin 路径
edith mysql get log conf status -u [MySQL用户名] --password [密码] --extpath [MySQL/bin路径] -f json -o /tmp

指定端口
edith mysql get log conf status -u [MySQL用户名] --password [密码] --port [远程主机的数据库端口] -f json -o /tmp

支持远程连接 MySQL
edith mysql get log conf status  --host [远程主机的IP] --port [远程主机的数据库端口] -u [MySQL用户名] --password [密码] -f json -o /tmp

指定 .sock 文件路径
edith mysql get log conf status -u [MySQL用户名] --password [密码] --sock [.sock路径] -f json -o /tmp
```

## 参数说明

- `-u` `--username`，该参数需传入MySQL的 **用户名**
- `--password`，该参数需传入 **用户密码**
- `-o` `--output`，该参数需传入 **输出数据的路径**
- `-f` `--format`，该参数需传入 **输出数据的格式**，如需格式化json文件，可以加入 `--pretty` 参数
- `-t`，该参数需传入指定的 **采集项**
- `--host`，该参数需传入远程主机的IP地址，配合 `--port` 传入远程主机的数据库端口（默认3306），可以达到对远程主机上的数据库实例进行巡检数据的采集

可以通过集中管理工具或脚本，将数据汇总到报告主机，在文件打包、传输等过程中**勿对 json 文件进行重命名操作**。

## 省略输入参数的数据采集

用户可以将部分命令行参数提前写入配置文件，然后直接可以省略这些参数进行数据采集

1. 通过 edith infra search --save 命令获取各个产品安装及实例信息被存入到 ~/.edith/registry.json 配置文件中
2. 找到并按下面提示编辑 ~/.edith/registry.json 配置文件中mysql的实例数据
```
...
   "instances": [
    {
    "product": "mysql",
    "version": "5.7.41",
    "name": "",
    "root_path": "/usr/sbin/mysqld",
    "ignored": false,
    "default": false,
    "defined": {
       "host": "", //数据库主机ip
       "password": "", //数据库密码
       "port": "", //数据库端口
       "sock_path": "", //数据库sock_path
       "username": ""   //数据库用户名
        }
    }
   ]
...
```

其中 "defined"内字段为用户编辑字段，参数规则同上，例如：
```
...
   "instances": [
    {
    "product": "mysql",
    "version": "5.7.41",
    "name": "",
    "root_path": "/usr/sbin/mysqld",
    "ignored": false,
    "default": false,
    "defined": {
       "host": "192.168.239.162",
       "password": "123456",
       "port": "3306",
       "sock_path": "/var/lib/mysql/mysql.sock",
       "username": "root"
        }
    }
   ]
...
```


编辑后保存。

3.后面数据采集命令中已经配置过的参数可以直接省略。例如原收集mysql配置的命令为 :
```
edith mysql get-conf -u [MySQL用户名] --password [密码] -f json -o /tmp
```

现在可以省略为:
```
edith mysql get-conf -f json -o /tmp -I
```


### 参数说明

- `-I` `--ignoreflag`，省略部分命令行参数
