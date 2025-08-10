
<p align="center">
  <img src="docs/logo_text.svg" width="200" alt="NextConsole Logo">
  <p align="center">Unleashing the Power of LLM for Enterprises💪</p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Apache 2.0 License">
  </p>
</p>

## Introduction
NextConsole is an open - source project meticulously crafted for enterprise users, designed to empower businesses to rapidly and efficiently construct intelligent systems based on large - language models. With NextConsole, enterprises can effortlessly build intelligent agents, knowledge bases, workflows, and a wide range of applications, significantly reducing development time and costs while accelerating the process of enterprise digital transformation. 🚀

### Key Features
| Feature | Description |
| ---- | ---- |
| **Rapid Development** ⚡ | NextConsole streamlines the development process, allowing enterprises to quickly implement large - language model - based solutions without getting bogged down in complex technical details. |
| **Customization** 🛠️ | The open - source nature of NextConsole enables enterprises to customize the system according to their specific needs, tailoring intelligent agents, knowledge bases, and workflows to fit unique business requirements. |
| **Scalability** 🔀 | The architecture of NextConsole is designed to scale, accommodating the growth of enterprise data and business operations, ensuring long - term viability and adaptability. |

### Application Scenarios

#### IT Operations
In the realm of IT operations, NextConsole revolutionizes the way enterprises manage their systems. Intelligent agents can continuously monitor system status in real - time, leveraging the knowledge base to swiftly diagnose and resolve issues. By optimizing workflows, NextConsole enhances the efficiency and quality of IT operations. 

| Company Type | Before NextConsole | After NextConsole |
| ---- | ---- | ---- |
| Multinational Corporation | Incident response time: long <br> Problem resolution rate: relatively low | Incident response time reduced by 50% <br> Problem resolution rate increased by 30% |

For instance, a multinational corporation's IT department adopted NextConsole and witnessed remarkable improvements as shown in the table above.

#### Document Intelligent Review
NextConsole also excels in document intelligent review scenarios. It can perform rapid and accurate reviews of documents based on predefined rules and the knowledge base, highlighting errors, vulnerabilities, and improvement suggestions. 

| Company Type | Before NextConsole | After NextConsole |
| ---- | ---- | ---- |
| Leading Law Firm | Review cycle: days <br> Service responsiveness: limited | Review cycle reduced from days to hours <br> Service responsiveness significantly enhanced |

A leading law firm integrated NextConsole into its document review process, and the results are clearly presented in the table.

NextConsole offers enterprises a powerful, open - source platform that combines the latest advancements in large - language models with practical, real - world applications. Whether you're looking to enhance IT operations or streamline document review processes, NextConsole is your go - to solution for building intelligent, efficient, and customized enterprise applications. 🌟


### Quick Start

#### Basic Resource Dependencies
Before starting to use NextConsole, please ensure that your environment meets the following basic resource dependencies:
- **Hardware Configuration**: At least 2 CPU cores and 4GB of memory.
- **Operating System**: Linux system.
- **Browser**: Chrome browser, version 110 or higher.
- **Containerization Tool**: Docker.

#### Operation Steps

##### 1. Navigate to the Project Directory
Open the terminal and use the `cd` command to enter the Docker directory of NextConsole:
```bash
cd next_console/docker
```

##### 2. Configure the Service
Use the `vi` editor to open the configuration file `config/server/config_private.py`:
```bash
vi config/server/config_private.py
```
In the configuration file, you need to make the following configurations:

**Domain Configuration**:
Set the domain name of the application. Here is an example using the local address:
```python
app.config["domain"] = "http://127.0.0.1:8080"
```

**RAG (Retrieval Augmented Generation) Configuration**:
It is recommended to use the free embedding and reranking models provided by Siliconflow. The specific configurations are as follows:
```python
# Vector model (It is recommended to use the free embed and rerank models from Siliconflow)
app.config["EMBEDDING_ENDPOINT"] = "https://api.siliconflow.cn/v1/embeddings"
app.config["EMBEDDING_MODEL"] = "BAAI/bge-m3"
app.config["EMBEDDING_KEY"] = ""
app.config["RERANK_ENDPOINT"] = "https://api.siliconflow.cn/v1/rerank"
app.config["RERANK_MODEL"] = "BAAI/bge-reranker-v2-m3"
app.config["RERANK_KEY"] = ""
app.config["search_engine_endpoint"] = "https://google.serper.dev/search"
app.config["search_engine_key"] = ""
```
Please fill in the corresponding keys (`EMBEDDING_KEY`, `RERANK_KEY`, `search_engine_key`) according to the actual situation. If you don't have them for now, you can leave them blank.

##### 3. Start the Docker Containers
After the configuration is completed, use the following command to start the Docker containers:
```bash
docker compose up -d
```

##### 4. Access the Services
After the successful startup, you can access the corresponding services through the following addresses:
- **Server Service**: Visit `http://127.0.0.1:8080`
- **Admin Service**: Visit `http://127.0.0.1:8082`

**Default Login Information**:
- **Username**: `admin@nextconsole.cn`
- **Password**: `next_console`

##### 5. Initial Model Configuration
Log in to the Admin service at port `8082`. Find the "Model Management" function module and configure the corresponding models according to your needs.

##### 6. Start the First Conversation
Log in to the Server service at port `8080`. Click on the "AI Workbench" to start your intelligent experience!

By following the above steps, you can quickly start NextConsole and begin using it! 😃

## Building from Source

### Prerequisites
- Docker 21+ installed
- Node.js 16+ (for frontend build)
- Python 3.10+ (for backend services)

### Build Steps

#### 1. Build Backend Service Image
```bash
git clone https://github.com/TuringOpsSH/NextConsole.git
cd next_console/docker/build/server
docker build -t nc:standalone .
```

#### 2. Build Frontend Service Image
```bash
cd ../web
docker build -t nc-web:standalone .
```

#### 3. Launch Services
```bash
cd ../
docker compose up -d
```

### Core Feature Descriptions

#### 1. AI Resource Library 📚
The AI Resource Library serves as a reliable data management assistant, providing fundamental data for Retrieval Augmented Generation (RAG).

| Function | Description |
| ---- | ---- |
| File Management | Allows users to upload, download, delete, and rename files. It also supports creating folders for organized storage. For example, a company's R & D department can categorize technical documents. |
| File Preview | Enables direct preview of common file formats without the need for external applications. Marketing staff can quickly view research reports, for instance. |
| File Sharing | Supports sharing files with customizable access permissions through various methods. A project manager can share progress reports securely. |
| Data Provision for RAG | Conducts semantic analysis and indexing of files to assist large - language models in providing accurate responses. An intelligent customer service can refer to the library for answers. |

#### 2. AI Workbench 🛠️
The AI Workbench integrates AI search and AI - agent application functions, offering a one - stop interactive experience.

| Function | Description |
| ---- | ---- |
| AI Search | Supports both keyword - based and semantic searches, presenting sorted results. Searching for ways to enhance product competitiveness can yield comprehensive answers. |
| AI - agent Applications | Integrates a variety of professional AI - agents that can be invoked with simple instructions. Copywriters can use them to generate promotional copy. |

#### 3. AI Application Factory 🏭
The AI Application Factory enables visual construction and management of large - model agents.

| Function | Description |
| ---- | ---- |
| Visual Construction | Uses a graphical interface to drag and drop components without complex coding. A business department can build an intelligent customer - service workflow, for example. |
| Release Management | Supports version control, performance monitoring, etc., and allows for on - demand optimization. A development team can regularly optimize agents. |

### Official Resources

Visit [NextConsole Official Documentation](https://docs.nextconsole.cn) to access:
- Latest version documentation  
- API reference  
- Advanced development guides  
- Best practice cases  
- Frequently asked questions  

Our documentation center is continuously updated. We recommend bookmarking this address for the latest materials 📚