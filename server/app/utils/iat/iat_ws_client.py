import base64
import datetime
import hashlib
import hmac
import json
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import threading
import websocket

from app.app import app, socketio, redis_client

_global_user_audio = {}


class XFWsClient(object):
    # 初始化
    def __init__(self, user_id):
        from app.models.configure_center.system_config import SystemConfig
        system_ai_config = SystemConfig.query.filter(
            SystemConfig.config_key == "ai",
            SystemConfig.config_status == 1
        ).first()
        self.API = system_ai_config.config_value.get('stt', {}).get("xf_api")
        self.APPID = system_ai_config.config_value.get('stt', {}).get("xf_api_id")
        self.APIKey = system_ai_config.config_value.get('stt', {}).get("xf_api_key")
        self.APISecret = system_ai_config.config_value.get('stt', {}).get("xf_api_secret")
        self.wsUrl = self.create_url()
        self.ws = None
        self.current_finish_idx = -1
        self.user_id = user_id
        self.ws_thread = None
        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin",
                             "vinfo": 1,
                             "vad_eos": 10000
                             }
        self.status = 0

    def on_message(self, ws, message, event_type='iat_result'):
        """
        处理消息
        """
        code = json.loads(message)["code"]
        sid = json.loads(message)["sid"]
        if code != 0:
            errMsg = json.loads(message)["message"]
            app.logger.error("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            return
        data = json.loads(message)["data"]["result"]["ws"]
        result = ""
        for i in data:
            for w in i["cw"]:
                result += w["w"]
        all_user_clients = redis_client.get(self.user_id)
        if not all_user_clients:
            return
        all_user_clients = json.loads(all_user_clients)
        for client in all_user_clients:
            if client.get('status') == 'connected':
                socketio.emit(event_type, {'result': result}, room=client.get('session_id'))

    def on_close(self, ws, *args, **kwargs):
        """
        关闭连接
        """
        print("### websocket closed ###")
        app.logger.info("### websocket closed ###")

    def on_open(self, ws):
        """
        建立连接
        """
        app.logger.info("### websocket open ###")

    def on_error(self, ws, error):
        print(f"### websocket error ###: {error}")

    def create_url(self):

        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = self.API + '?' + urlencode(v)
        return url

    def init(self):
        self.ws = websocket.WebSocketApp(self.wsUrl,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open
                                         )
        self.ws_thread = threading.Thread(target=self.ws.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}})
        self.ws_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
        self.ws_thread.start()
        return self.ws

    def send_audio(self, data, LastFrame=False):
        if LastFrame:
            self.status = 2
        if self.status == 0:
            d = {"common": self.CommonArgs,
                 "business": self.BusinessArgs,
                 "data": {"status": self.status, "format": "audio/L16;rate=16000",
                          "audio": str(base64.b64encode(data), 'utf-8'),
                          "encoding": "raw"}
                 }
            d = json.dumps(d)
            self.status = 1
        else:
            d = {"data": {"status": self.status, "format": "audio/L16;rate=16000",
                          "audio": str(base64.b64encode(data), 'utf-8'),
                          "encoding": "raw"}
                 }
            d = json.dumps(d)
        self.ws.send(d)
        self.current_finish_idx += 1


def handle_audio_message(message):
    """
        处理音频消息 ，并调用讯飞语音识别接口
    """
    user_id = message.get("user_id")
    data = message.get("data")
    LastFrame = message.get("LastFrame", False)
    if user_id not in _global_user_audio or not _global_user_audio[user_id].get("ws_client"):
        ws_client = XFWsClient(user_id)
        ws_client.init()
        _global_user_audio[user_id] = {
            "audio_data": [],
            "ws_client": ws_client
        }
    _global_user_audio[user_id]["audio_data"].append(
        {
            "data": data,
            "status": 0
        }
    )
    # 尝试发送音频数据
    if _global_user_audio[user_id]["ws_client"].ws.sock and _global_user_audio[user_id]["ws_client"].ws.sock.connected:
        # 合并所有未发送的音频数据
        audio_data = b"".join([audio.get("data") for audio in _global_user_audio[user_id]["audio_data"]
                               if audio.get("status") == 0])
        if audio_data:
            _global_user_audio[user_id]["ws_client"].send_audio(audio_data, LastFrame)
            for audio in _global_user_audio[user_id]["audio_data"]:
                audio["status"] = 1


def handle_audio_stop_message(message):
    """
        处理音频消息终止
    """
    user_id = message.get("user_id")
    if user_id in _global_user_audio:
        _global_user_audio[user_id]["ws_client"] = None
        _global_user_audio[user_id]["audio_data"] = []
