# middleware-report-generation

# 数据收集

点击顶部【打开】按钮，在`middleware-report-generation\scripts`目录下找到脚本`middleware_collector.py`，
然后将该脚本上传至服务器的专门目录下，比如`/tmp/middleware_collector`下。执行脚本：

```
python middleware_collector.py
```

等待脚本执行完毕，将采集结果，如`20231027_xunjian_data.tar.gz`集中到生成报告的PC（也即部署了 Edith-Desk 的PC）

# 报告生成

1、将所有的压缩文件集中到PC（部署了 Edith-Desk 的PC）的某个目录下，在顶部点击选择全局数据目录到该目录，
点击【解压】按钮将所有压缩文件解压。

2、解压后全局数据目录下的文件结构应该如下，你也可以手动将文件结构调整为如下的形式：

```bash
（所选择的全局数据目录）
│ 
├─data  # 采集到的全部数据，多个IP地址的数据放到一起
│   ├─192.168.100.1_bes.txt
│   ├─192.168.100.1_elasticsearch.txt
│   ├─192.168.100.1_httpd.txt
│   ├─192.168.100.2_java.txt
│   ├─192.168.100.2_kafka.txt
│   └─...
├─report   # 报告生成目录
└─system_list.xlsx # 应用系统-IP地址-负责人对应关系配置文件
```
system_list.xlsx 示例文件可从 `middleware-report-generation\templates\system_list.xlsx` 获得，
拷贝至你的数据目录下填写即可。

3、点击对应的生成报告按钮，然后到`report`目录下查看生成的报告。


# 开发

本应用基于 Python 3.9
Clone 代码后首先需要下载依赖包到本地的 pyeek 目录:

```
# middleware-report-generation 目录下创建目录
md pyeek

# 安装 requirements.txt 文件中的包到 pyeek 目录
pip install -t ./pyeek -r requirements.txt
```

新增依赖包需要安装到 pyeek 目录下同时更新 requirements.txt：

```
# 安装 xxx 到 pyeek 目录
pip install -t ./pyeek xxx

# 更新 pyeek 依赖包列表到 requirements.txt 文件
pip freeze --path=./pyeek > requirements.txt
```

# 发布

发布时将打包整个 pyeek 目录，因此发布前须确保已经安装所有依赖包。
