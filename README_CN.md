
<p align="center">
  <img src="docs/logo_text.svg" width="200" alt="NextConsole Logo">
  <p align="center">释放大语言模型赋能企业的无限潜力💪</p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Apache 2.0 License">
  </p>
</p>
 
## 项目简介
NextConsole 是一款专门为企业用户精心打造的开源项目，旨在助力企业快速且高效地构建基于大语言模型的智能系统。借助 NextConsole，企业能够轻松搭建智能代理、知识库、工作流以及各类应用程序，大幅缩短开发时间、降低成本，加速企业数字化转型进程🚀。

### 核心特性
| 特性 | 描述 |
| ---- | ---- |
| **快速开发**⚡ | NextConsole 简化了开发流程，使企业能够迅速部署基于大语言模型的解决方案，无需深陷复杂的技术细节。 |
| **定制化**🛠️ | NextConsole 的开源特性让企业可根据自身特定需求对系统进行定制，量身打造智能代理、知识库和工作流，以契合独特的业务需求。 |
| **可扩展性**🔀 | NextConsole 的架构具备良好的可扩展性，能够适应企业数据量的增长和业务运营的拓展，确保长期的可行性和适应性。 |

### 应用场景

#### IT 运维
在 IT 运维领域，NextConsole 彻底改变了企业管理系统的方式。智能代理能够实时持续监控系统状态，利用知识库快速诊断并解决问题。通过优化工作流，NextConsole 提升了 IT 运维的效率和质量。

| 企业类型 | 使用 NextConsole 之前 | 使用 NextConsole 之后 |
| ---- | ---- | ---- |
| 跨国公司 | 事件响应时间：长 <br> 问题解决率：相对较低 | 事件响应时间缩短 50% <br> 问题解决率提高 30% |

例如，一家跨国公司的 IT 部门引入 NextConsole 后，取得了如表格所示的显著改善。

#### 文档智能评审
NextConsole 在文档智能评审场景中同样表现出色。它能够依据预定义规则和知识库内容，对文档进行快速、准确的评审，标记出错误、漏洞和改进建议。

| 企业类型 | 使用 NextConsole 之前 | 使用 NextConsole 之后 |
| ---- | ---- | ---- |
| 顶尖律师事务所 | 评审周期：数天 <br> 服务响应速度：受限 | 评审周期从数天缩短至数小时 <br> 服务响应速度显著提升 |

一家顶尖律师事务所将 NextConsole 融入其文档评审流程后，效果如表格所示。

NextConsole 为企业提供了一个强大的开源平台，它将大语言模型的最新进展与实际的现实应用相结合。无论您是希望提升 IT 运维效率，还是简化文档评审流程，NextConsole 都是您构建智能、高效且定制化企业应用的首选解决方案🌟。

### 快速启动

#### 基础资源依赖
在开始使用 NextConsole 之前，请确保您的环境满足以下基础资源依赖：
- **硬件配置**：至少 2 核 CPU、4GB 内存。
- **操作系统**：Linux 系统。
- **浏览器**：Chrome 浏览器，版本 110 及以上。
- **容器化工具**：Docker。

#### 操作步骤

##### 1. 进入项目目录
打开终端，使用 `cd` 命令进入 NextConsole 的 Docker 目录：
```bash
cd next_console/docker
```

##### 2. 配置服务
使用 `vi` 编辑器打开配置文件 `config/server/config_private.py`：
```bash
vi config/server/config_private.py
```
在配置文件中，您需要进行以下配置：

**域名配置**：
设置应用的域名，这里以本地地址为例：
```python
app.config["domain"] = "http://127.0.0.1:8080"
app.config["admin_domain"] = "http://127.0.0.1:8082"
```

**RAG（检索增强生成）配置**：
推荐使用 Siliconflow 免费的嵌入（embed）和重排（rerank）模型，具体配置如下：
```python
# 向量模型（推荐sliconflow免费的embed和rerank模型）
app.config["EMBEDDING_ENDPOINT"] = "https://api.siliconflow.cn/v1/embeddings"
app.config["EMBEDDING_MODEL"] = "BAAI/bge-m3"
app.config["EMBEDDING_KEY"] = ""
app.config["RERANK_ENDPOINT"] = "https://api.siliconflow.cn/v1/rerank"
app.config["RERANK_MODEL"] = "BAAI/bge-reranker-v2-m3"
app.config["RERANK_KEY"] = ""
app.config["search_engine_endpoint"] = "https://google.serper.dev/search"
app.config["search_engine_key"] = ""
```
请根据实际情况填写相应的密钥（`EMBEDDING_KEY`、`RERANK_KEY`、`search_engine_key`），若暂时没有可以先留空。

##### 3. 启动 Docker 容器
配置完成后，使用以下命令启动 Docker 容器：
```bash
docker compose up -d
```

##### 4. 访问服务
启动成功后，您可以通过以下地址访问相应的服务：
- **Server 服务**：访问 `http://127.0.0.1:8080`
- **Admin 服务**：访问 `http://127.0.0.1:8082`

**默认登录信息**：
- **用户名**：`admin@nextconsole.cn`
- **密码**：`next_console`

##### 5. 初始模型配置
登录 `8082` 的 Admin 服务，找到“模型管理”功能模块，根据您的需求配置相应的模型。

##### 6. 开启首次会话
登录 `8080` 的 Server 服务，点击“AI 工作台”，即可开启智能体验之旅！

按照以上步骤操作，您就可以快速启动 NextConsole 并开始使用啦😃。


### 源码构建镜像

#### 前置准备
- 已安装 Docker 21+
- 已安装 Node.js 16+ (用于前端构建)
- 已安装 Python 3.10+ (用于后端服务)

#### 构建步骤

##### 1. 构建后端服务镜像
```bash
git clone https://github.com/TuringOpsSH/NextConsole.git
cd next_console/docker/build/server
docker build -t nc:standalone .

```
##### 2. 构建前端服务镜像
```bash
cd ../web
docker build -t nc-web:standalone .
```

##### 3. 启动服务
```bash
cd ../
docker compose up -d
```






### 核心功能特性说明

#### 1、AI 资源库 📚
AI 资源库是数据管理的好帮手，为 RAG 提供基础数据。

|功能|描述|
| ---- | ---- |
|文件管理|可上传、下载、删除、重命名文件，还能创建文件夹分类整理，如企业研发部可分类存放技术文档。|
|文件预览|无需外部程序，直接预览常见格式文件，像营销人员能快速查看调研报告。|
|文件分享|能设置权限分享文件，方式多样，如项目经理分享进度报告。|
|为 RAG 供数|对文件语义分析和索引，助力大语言模型精准回答，如智能客服参考资源库解答问题。|

#### 2、AI 工作台 🛠️
AI 工作台集成了 AI 搜索和 AI - agent 应用功能，一站式交互体验。

|功能|描述|
| ---- | ---- |
|AI 搜索|支持关键词和语义搜索，排序展示结果，如搜索提升产品竞争力的方法能获全面回答。|
|AI - agent 应用|集成多种专业 AI - agent，简单指令即可调用，如文案人员用其生成宣传文案。|

#### 3、AI 应用工厂 🏭
AI 应用工厂可可视化构建大模型智能体并管理发布。

|功能|描述|
| ---- | ---- |
|可视化构建|图形界面拖放组件，无需复杂代码，如业务部门构建智能客服流程。|
|发布管理|支持版本控制、性能监控等，可按需优化调整，如开发团队定期优化智能体。|


### 官方资源

访问 [NextConsole官方文档](https://docs.nextconsole.cn) 获取：
- 最新版本文档
- API接口说明
- 进阶开发指南
- 最佳实践案例
- 常见问题解答

我们的文档中心会持续更新，建议收藏该地址以便随时查阅最新资料 📚


