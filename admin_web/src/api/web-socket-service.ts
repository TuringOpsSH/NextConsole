import { io, Socket } from 'socket.io-client';

// 定义 WebSocket 客户端类
class WebSocketClient {
    private socket: Socket;

    constructor(url: string) {
        this.socket = io(url);
        this.initializeSocketEvents();
    }

    private initializeSocketEvents(): void {
        this.socket.on('connect', () => {
            // console.log('已连接到服务器');
        });

        this.socket.on('system_notice', (data: string) => {
            // console.log('收到系统通知:', data);
        });

        this.socket.on('response', (data: string) => {
            // console.log('收到服务器消息:', data);
        });
    }

    public sendMessage(message: string): void {
        this.socket.emit('message', message);
    }
}

// 创建 WebSocket 客户端实例
const socketClient = new WebSocketClient("/web_socket");

// 发送消息的函数
export function sendMessage(): void {
    const message = 'Hello Server!';
    socketClient.sendMessage(message);
}
