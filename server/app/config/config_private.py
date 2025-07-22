from datetime import timedelta
from app.app import app
from celery.schedules import crontab

# 应用配置
app.config["domain"] = ""
app.config['bucket_size'] = 5000
app.config['data_dir'] = "/app/data"
app.config["download_dir"] = '/app/data/download'
app.config['JWT_SECRET_KEY'] = 'ncddodoieo494ifo'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['LOG_DIR'] = 'logs'
app.config['LOG_FILE'] = 'next_console.log'
app.config['LOG_LEVEL'] = "INFO"
app.config['LOG_MAX_BYTES'] = 10*1024*1024
app.config['LOG_BACKUP_COUNT'] = 10
app.config['SECRET_KEY'] = '146827-a8ac-4a28-8efd5-c13e5df11529'
app.config['download_cool_time'] = 7200
app.config['download_max_count'] = 100

# 数据库配置
app.config["db_type"] = "postgresql"
app.config["db_user"] = "next_console"
app.config["db_password"] = "ncDBPassword"
app.config["db_host"] = "db"
app.config["db_port"] = "5432"
app.config["db_name"] = "next_console"
app.config["db_schema"] = "next_console"
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['SQLALCHEMY_EXPIRE_ON_COMMIT'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# redis 配置
app.config['redis_host'] = "redis"
app.config['redis_port'] = 6379
app.config['redis_username'] = None
app.config['redis_password'] = 'ncRedisPassword'
app.config['next_console_channel'] = 8
app.config['websocket_channel'] = 9

# 调度配置
app.config['celery_broker_channel'] = 4
app.config['celery_result_channel'] = 5
app.config['timezone'] = 'Asia/Shanghai'
app.config['task_serializer'] = 'json'
app.config['result_serializer'] = 'json'
app.config['worker_concurrency'] = 24
app.config["task_timeout"] = 3600

# rag 配置
app.config["EMBEDDING_ENDPOINT"] = "https://api.siliconflow.cn/v1/embeddings"
app.config["EMBEDDING_MODEL"] = "BAAI/bge-m3"
app.config["EMBEDDING_KEY"] = ""
app.config["RERANK_ENDPOINT"] = "https://api.siliconflow.cn/v1/rerank"
app.config["RERANK_MODEL"] = "BAAI/bge-reranker-v2-m3"
app.config["RERANK_KEY"] = ""
app.config["search_engine_endpoint"] = "https://google.serper.dev/search"
app.config["search_engine_key"] = ""

# 企微配置
app.config['sToken'] = ""
app.config['sEncodingAESKey'] = ""
app.config['sCorpID'] = ""
app.config['corpsecret'] = ""
app.config['agent_id'] = ""


# 微信配置
app.config['WX_APP_ID'] = ""
app.config["WX_APP_SECRET"] = ""

# 短信配置
app.config["ALIBABA_CLOUD_ACCESS_KEY_ID"] = ""
app.config["ALIBABA_CLOUD_ACCESS_KEY_SECRET"] = ""
app.config["ALIBABA_CLOUD_ENDPOINT"] = "dysmsapi.aliyuncs.com"
app.config["sign_name"] = ""
app.config["template_code"] = ""

# 邮箱配置
app.config["admin_email"] = "support@turingops.com.cn"
app.config["smtp_server"] = "smtphz.qiye.163.com"
app.config["smtp_port"] = 465
app.config["smtp_user"] = "support@turingops.com.cn"
app.config["smtp_password"] = ""
app.config["notice_email"] = "support@turingops.com.cn"

# 讯飞配置
app.config['XF_API'] = ""
app.config["XF_APP_ID"] = ""
app.config["XF_API_KEY"] = ""
app.config["XF_API_SECRET"] = ""
