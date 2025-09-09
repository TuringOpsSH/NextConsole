import FingerprintJS from '@fingerprintjs/fingerprintjs';
import { ElMessage, ElNotification } from 'element-plus';
import { io } from 'socket.io-client';
import { ref } from 'vue';
import {
  AgentAppMsgFlow,
  currentGraphConfigs,
  QAWorkFlowMap,
  sendMessageToParent
} from '@/components/app-center/ts/agent-app';
import { consoleInput } from '@/components/app-center/ts/agent_console';
import { current_friend_request_cnt } from '@/components/contacts/contacts-panel/contacts_panel';
import { consoleInputRef, user_input } from '@/components/next-console/messages-flow/console_input';
import {
  msg_flow,
  msg_recommend_question,
} from '@/components/next-console/messages-flow/message_flow';
import { msgFlowRef } from '@/components/next-console/messages-flow/message_flow';
import { session_history_top5 } from '@/components/next-console/messages-flow/sessions';
import { current_resource_list, resourceDetailRef } from '@/components/resource/resource_list/resource_list';
import { current_resource_list as current_resource_shortcut_list } from '@/components/resource/resource_shortcut/resource_shortcut';
import { currentPathTree } from '@/components/resource/resource-view/resource-viewer';
import router from '@/router';
import { useSessionStore } from '@/stores/sessionStore';
import { useSystemNoticeStore } from '@/stores/systemNoticeStore';
import { useUserInfoStore } from '@/stores/userInfoStore';
import { Friend } from '@/types/contacts';
import { recommend_question_item, workflow_task_item, workflow_task_map } from '@/types/next-console';
import { ResourceItem } from '@/types/resource-type';
import { ISystemNotice } from '@/types/user-center';
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
  if (socket.value?.connected) {
    return;
  }

  if (!socket.value) {
    if (import.meta.env.VITE_APP_NODE_ENV === 'private') {
      const socketUrl = `${window.location.protocol === 'https:' ? 'wss://' : 'ws://'}${window.location.host}`;
      socket.value = io(socketUrl, {
        transports: ['websocket'],
        path: '/socket.io'
      });
    } else {
      socket.value = io(import.meta.env.VITE_APP_WEBSOCKET_URL, {
        transports: ['websocket'],
        path: '/socket.io'
      });
    }
  }
  // 监听连接事件
  socket.value.on('connect', () => {
    // 发送身份验证
    const userInfoStore = useUserInfoStore();
    socket.value?.emit('auth', {
      token: userInfoStore.token,
      clientFingerprint: clientFingerprint.value
    });
  });
  // 监听断开连接事件
  socket.value.on('disconnect', () => {
    // 发送身份验证,并退出
    const userInfoStore = useUserInfoStore();
    socket.value?.emit('remove_auth', {
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
  // 更新资源状态
  socket.value.on('updateRefStatus', data => {
    // console.log('updateRefStatus',data)
    updateRefStatus(data);
  });
  // 工作流更新
  socket.value.on('update_workflow_item_status', data => {
    // // console.log('update_workflow_item_status',data)
    if (router.currentRoute.value.name === 'agent_app') {
      update_workflow_item_status(data, QAWorkFlowMap.value);
    } else if (data.task_type == '会话命名') {
      const store = useSessionStore();
      if (store.getLatestSessionListRef) {
        store.getLatestSessionListRef();
      }
    } else {
      msgFlowRef?.value?.updateWorkflowItemStatus(data);
    }
  });
  // 推荐问题更新
  socket.value.on('update_recommend_questions', data => {
    msgFlowRef?.value?.updateRecommendQuestion(data);
  });
  // 好友申请提醒
  socket.value.on('new_friend_request', data => {
    update_friend_request(data);
  });
  // 更新站内信
  socket.value.on('new_system_notice', (data: ISystemNotice) => {
    // console.log('update_system_msg',data)
    updateSystemNotices(data);
  });
  // 更新资源名称
  socket.value.on('wps_rename', (data: ResourceItem) => {
    // console.log('update_system_msg',data)
    update_resource_view_name(data);
  });
  socket.value.on('disconnect', () => {
    console.log('Disconnected from server');
    // 这里可以执行清理操作，比如清空 socket 对象
    socket.value = null;
  });
  // 更新资源名称
  socket.value.on('iat_result', data => {
    // 更新语音识别结果
    console.log('iat_result', data);
    updateUserInput(data?.result);
  });
  // 更新bi图表

  socket.value.on('update_bi_graph', data => {
    // 更新语音识别结果
    sendMessageToParent({
      type: 'updateGraph',
      data: data
    });
  });
  socket.value.on('update_sql_result', data => {
    // 更新sql查询结果
    updateSqlResult(data);
  });
  socket.value.on('update_chart_options', data => {
    // 更新表格可视化结果
    updateChartOptionsResult(data);
  });
}

export function updateUserInput(newQuestion: string) {
  console.log(router.currentRoute.value.name, newQuestion);
  if (router.currentRoute.value.name === 'agent_app') {
    consoleInput.value += newQuestion;
  } else if (
    router.currentRoute.value.name === 'next_console_welcome_home' ||
    router.currentRoute.value.name === 'message_flow'
  ) {
    consoleInputRef.value?.handleAsr(newQuestion);
  }
}
export function updateRefStatus(data: ResourceItem[]) {
  // 根据传入的数据更新ref状态
  // data: 需要更新的资源对象列表
  // console.log('ref_status_update',data)
  if (router.currentRoute.value.name === 'resource_shortcut') {
    // 更新我的资源列表
    for (let i = 0; i < current_resource_shortcut_list.value.length; i++) {
      for (let j = 0; j < data.length; j++) {
        if (current_resource_list.value[i]?.id === data[j].id) {
          current_resource_list.value[i].rag_status = data[j].rag_status;
        }
      }
    }
  } else if (router.currentRoute.value.name === 'resource_list') {
    // 更新资源列表
    // // console.log('update',"resource_list")
    for (let i = 0; i < current_resource_list.value.length; i++) {
      for (let j = 0; j < data.length; j++) {
        if (current_resource_list.value[i].id == data[j].id) {
          // // console.log('update',data[j].rag_status)
          current_resource_list.value[i].rag_status = data[j].rag_status;
        }
        if (resourceDetailRef.value?.nowResourceId == data[j].id) {
          resourceDetailRef.value?.getResourceDetail();
        }
      }
    }
  }
  consoleInputRef.value?.updateSessionAttachment(data);
}
export function update_workflow_item_status(data: workflow_task_item, targetWorkflowMap: workflow_task_map) {
  // 根据传入工作流任务对象更新工作流任务状态
  // 如果不存在则新增，如果存在则更新
  // // console.log('收到工作流任务状态更新',data)
  // 剔除占位符
  if (targetWorkflowMap[data.qa_id]?.length === 1 && !targetWorkflowMap[data.qa_id][0].task_id) {
    targetWorkflowMap[data.qa_id] = [];
  }
  if (!targetWorkflowMap[data.qa_id]?.length) {
    targetWorkflowMap[data.qa_id] = [data];
  } else {
    let find_flag = false;
    for (let i = 0; i < targetWorkflowMap[data.qa_id].length; i++) {
      if (targetWorkflowMap[data.qa_id][i].task_id === data.task_id) {
        targetWorkflowMap[data.qa_id][i] = data;
        find_flag = true;
        break;
      }
    }
    if (!find_flag) {
      targetWorkflowMap[data.qa_id].push(data);
    }
  }
  // 打开工作流展示区域
  for (let i = 0; i < msg_flow.value.length; i++) {
    if (msg_flow.value[i].qa_id === data.qa_id) {
      msg_flow.value[i].qa_workflow_open = true;
    }
  }
  for (let i = 0; i < AgentAppMsgFlow.value.length; i++) {
    if (AgentAppMsgFlow.value[i].qa_id === data.qa_id) {
      AgentAppMsgFlow.value[i].qa_workflow_open = true;
    }
  }
  // 后续处理
  // // console.log('工作流任务状态更新',data)
  if (data.task_type == '会话命名') {
    // 更新会话列表中会话主题字段
    for (const history of session_history_top5.value) {
      if (history.id == data.session_id) {
        history.session_topic = data.task_result;
        return;
      }
    }
  }
}
export function update_recommend_question_lists(data: recommend_question_item[]) {
  for (const recommend_question of data) {
    if (!msg_recommend_question.value?.[recommend_question.msg_id]) {
      msg_recommend_question.value[recommend_question.msg_id] = [recommend_question];
    } else {
      msg_recommend_question.value[recommend_question.msg_id].push(recommend_question);
    }
  }
}
export function update_friend_request(new_friend: Friend) {
  // 好友申请提醒
  ElNotification.success({
    title: '好友申请',
    message: `您收到了${new_friend.user_nick_name}的好友申请`,
    duration: 0
  });
  // 更新好友申请数量
  current_friend_request_cnt.value += 1;
}
export function updateSystemNotices(data: ISystemNotice) {
  const unreadNotice = useSystemNoticeStore();
  unreadNotice.addNewNotice(data);
}
export function update_resource_view_name(new_resource: ResourceItem) {
  currentPathTree.value.forEach(item => {
    if (item.id == new_resource.id) {
      item.resource_name = new_resource.resource_name;
      ElMessage.success('重命名成功');
    }
  });
}
async function checkSocketConnection() {
  if (!socket.value || !socket.value.connected) {
    console.log('Socket is disconnected, reconnecting...');
    await initSocket();
  }
}
export function updateSqlResult(data) {
  // console.log(data)
  currentGraphConfigs.value[data.msg_id] = {
    options: data?.options,
    sql: data?.sql,
    raw_data: data?.data,
    columns: data?.columns
  };
  // console.log(currentGraphConfigs.value)
}
export function updateChartOptionsResult(data) {
  console.log(data);
  currentGraphConfigs.value[data.msg_id].options = data?.options?.options;
  currentGraphConfigs.value[data.msg_id].pane = 'graph';
}
// 每 30 秒检查一次连接状态
checkSocketConnection();
setInterval(checkSocketConnection, 10000);
