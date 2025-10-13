from gevent import monkey
import platform
if platform.system().lower().startswith('darwin'):
    monkey.patch_socket()
else:
    monkey.patch_all()
from app.app import app, socketio
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5123, log_output=True, debug=True)
