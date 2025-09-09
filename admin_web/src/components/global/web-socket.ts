import FingerprintJS from '@fingerprintjs/fingerprintjs';
import { ElNotification } from 'element-plus';
import { io } from 'socket.io-client';
import { ref } from 'vue';
import { consoleInputRef } from '@/components/app-center/appPreview/console_input';
import { msgFlowRef } from '@/components/app-center/appPreview/message_flow';
import router from '@/router';
import { useUserInfoStore } from '@/stores/userInfoStore';
// 创建 Socket.IO 客户端实例，连接到服务器
export const socket = ref(null);
export const clientFingerprint = ref('');
export async function getFingerPrint() {
  const fp = await FingerprintJS.load();
  await fp.get().then(result => {
    clientFingerprint.value = result.visitorId;
  });
}
export async function initSocket() {
  if (socket.value) {
    return;
  }
  socket.value = io(import.meta.env.VITE_APP_WEBSOCKET_URL, {
    transports: ['websocket']
  });
  const userInfoStore = useUserInfoStore();
  // 监听连接事件
  socket.value.on('connect', () => {
    // console.log('Connected to server');
    // 发送身份验证
    if (!socket.value?.emit) {
      return;
    }

    socket.value.emit('auth', {
      token: userInfoStore.token,
      clientFingerprint: clientFingerprint.value
    });
  });
  // 监听断开连接事件
  socket.value.on('disconnect', () => {
    // 发送身份验证,并退出
    socket.value.emit('remove_auth', {
      token: userInfoStore.token,
      clientFingerprint: clientFingerprint.value
    });
  });
  // 系统通知
  socket.value.on('notification', data => {
    ElNotification({
      title: '系统通知',
      message: data,
      type: 'success',
      duration: 12000
    });
  });
  // 工作流更新
  socket.value.on('update_workflow_item_status', data => {
    // // console.log('update_workflow_item_status',data)
    msgFlowRef?.value?.updateWorkflowItemStatus(data);
  });
  // 推荐问题更新
  socket.value.on('update_recommend_questions', data => {
    msgFlowRef?.value?.updateRecommendQuestion(data);
  });
  socket.value.on('disconnect', () => {
    console.log('Disconnected from server');
    // 这里可以执行清理操作，比如清空 socket 对象
    socket.value = null;
  });
  // 语音识别信息
  socket.value.on('iat_result', data => {
    // 更新语音识别结果
    console.log('iat_result', data);
    updateUserInput(data?.result);
  });
}
export function updateUserInput(data) {
  if (router.currentRoute.value.name == 'workflowEdit') {
    consoleInputRef.value?.updateQuestion(data);
  }
}
function checkSocketConnection() {
  if (!socket.value || !socket.value.connected) {
    console.log('Socket is disconnected, reconnecting...');
    initSocket();
  } else {
    console.log('Socket is connected');
  }
}

// 每 30 秒检查一次连接状态
setInterval(checkSocketConnection, 10000);
