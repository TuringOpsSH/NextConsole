from gevent import monkey
import platform
if platform.system().lower().startswith('darwin'):
    monkey.patch_socket()
else:
    monkey.patch_all()
import logging
import os
from logging.handlers import RotatingFileHandler
from flask_socketio import SocketIO
from socketio import RedisManager
import redis
from celery import Celery
from flask import Flask
from flask_jwt_extended import (
    JWTManager
)
from flask_principal import Principal
from flask_sqlalchemy import SQLAlchemy
import socket
from urllib.parse import quote_plus
app = Flask(__name__)
model = os.environ.get('FLASK_MODEL')  # 从环境变量获取配置文件路径
if not model:
    config_path = "./config/config_local.py"
else:
    config_path = "./config/config_{}.py".format(model)
app.config.from_pyfile(config_path)
app.config['base_dir'] = os.path.dirname(__file__)
app.config['tmp_dir'] = os.path.join(app.config['base_dir'], "tmp")
app.config['config_static'] = os.path.join(os.path.dirname(__file__), "config", "static")
app.config['public_dir'] = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "next_console_frontend", "public"
)
if app.config.get('db_type') == 'mysql':
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(
        app.config.get('db_user'),
        quote_plus(app.config.get('db_password')),
        app.config.get('db_host'),
        app.config.get('db_port'),
        app.config.get('db_name'),
        app.config.get('db_charset', 'utf8mb4')
    )
elif app.config.get('db_type') == 'postgresql':
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{}:{}@{}:{}/{}?options=-c%20search_path={},public".format(
        app.config.get('db_user'),
        quote_plus(app.config.get('db_password')),
        app.config.get('db_host'),
        app.config.get('db_port'),
        app.config.get('db_name'),
        app.config.get('db_schema')
    )
if app.config.get('redis_password'):
    app.config['CELERY_BROKER_URL'] = 'redis://{}:{}@{}:{}/{}'.format(
        app.config['redis_username'] if app.config.get('redis_username') else '',
        quote_plus(app.config.get('redis_password')),
        app.config['redis_host'],
        app.config['redis_port'],
        app.config['celery_broker_channel']
    )
    app.config['result_backend'] = 'redis://{}:{}@{}:{}/{}'.format(
        app.config['redis_username'] if app.config.get('redis_username') else '',
        quote_plus(app.config.get('redis_password')),
        app.config['redis_host'],
        app.config['redis_port'],
        app.config['celery_result_channel']
    )
    redis_url = 'redis://{}:{}@{}:{}/{}'.format(
        app.config['redis_username'] if app.config.get('redis_username') else '',
        quote_plus(app.config.get('redis_password')),
        app.config['redis_host'],
        app.config['redis_port'],
        app.config['websocket_channel']
    )
else:
    app.config['CELERY_BROKER_URL'] = 'redis://{}:{}/{}'.format(
        app.config['redis_host'],
        app.config['redis_port'],
        app.config['celery_broker_channel']
    )
    app.config['result_backend'] = 'redis://{}:{}/{}'.format(
        app.config['redis_host'],
        app.config['redis_port'],
        app.config['celery_result_channel']
    )
    redis_url = 'redis://{}:{}/{}'.format(
        app.config['redis_host'],
        app.config['redis_port'],
        app.config['websocket_channel']
    )

celery = Celery("next_console",
                broker=app.config['CELERY_BROKER_URL'],
                backend=app.config['result_backend'],
                include=[
                    'app.services.task_center.celery_fun_libs',
                    'app.services.task_center.user_account',
                    'app.services.task_center.workflow',
                    'app.services.task_center.resources_center',
                ])
hostname = socket.gethostname()
celery.conf.task_default_queue = f'nc_server_queue'
celery.conf.update(app.config)
redis_client = redis.Redis(
    host=app.config['redis_host'],
    port=app.config['redis_port'],
    decode_responses=True,
    username=app.config['redis_username'],
    password=app.config['redis_password'],
    db=app.config['next_console_channel'])

client_mgr = RedisManager(redis_url)
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode="gevent",
                    client_manager=client_mgr)

jwt = JWTManager(app)
db = SQLAlchemy()
db.init_app(app)
principals = Principal(app)
if not os.path.exists(app.config['LOG_DIR']):
    try:
        os.mkdir(app.config['LOG_DIR'])
    except Exception as e:
        pass
log_filename = os.path.join(app.config['LOG_DIR'], app.config['LOG_FILE'])
handler = RotatingFileHandler(str(log_filename),
                              maxBytes=app.config['LOG_MAX_BYTES'],
                              backupCount=app.config['LOG_BACKUP_COUNT']
                              )
handler.setLevel(app.config['LOG_LEVEL'])
format_str = '%(asctime)s [%(levelname)s] %(filename)s: %(message)s'
formatter = logging.Formatter(format_str)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(app.config['LOG_LEVEL'])


from app.sub_apps.whzy.whzy import blueprint as whzy_blueprint
from app.sub_apps.shyh.shyh import blueprint as shyh_blueprint
from app.sub_apps.spdb.spdb import blueprint as spdb_blueprint
app.register_blueprint(whzy_blueprint)
app.register_blueprint(shyh_blueprint)
app.register_blueprint(spdb_blueprint)