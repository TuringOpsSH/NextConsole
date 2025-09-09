from datetime import timedelta
from app.app import app

# 应用配置
app.config["domain"] = "http://127.0.0.1:8080"
app.config['admin_domain'] = "http://127.0.0.1:8082"
app.config['bucket_size'] = 5000
app.config['data_dir'] = "/app/data"
app.config["download_dir"] = '/app/data/download'
app.config['JWT_SECRET_KEY'] = 'ncddodoieo494ifo'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['LOG_DIR'] = '/app/admin/logs'
app.config['LOG_FILE'] = 'next_console.log'
app.config['LOG_LEVEL'] = "INFO"
app.config['LOG_MAX_BYTES'] = 10*1024*1024
app.config['LOG_BACKUP_COUNT'] = 10
app.config['SECRET_KEY'] = '146c827-a8ac-4a28-8fd5-c13e5df11529'
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
app.config['next_console_channel'] = 2
app.config['websocket_channel'] = 3

# 调度配置
app.config['celery_broker_channel'] = 0
app.config['celery_result_channel'] = 1
app.config['timezone'] = 'Asia/Shanghai'
app.config['task_serializer'] = 'json'
app.config['result_serializer'] = 'json'
app.config['worker_concurrency'] = 12
app.config["task_timeout"] = 3600

