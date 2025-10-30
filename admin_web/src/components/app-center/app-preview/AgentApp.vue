<script setup lang="ts">
import 'highlight.js/styles/vs2015.min.css';
import { ref, watch } from 'vue';
import { onBeforeMount } from 'vue-demi';
import { appDetail, initAppSession } from '@/api/app-center-api';
import { search_session as ISearchSession } from '@/api/next-console';
import { initSocket, socket } from '@/components/global/web-socket';
import ConsoleInput from './ConsoleInput.vue';
import MessageFlowV2 from './MessageFlowV2.vue';
import SessionParams from './SessionParams.vue';
import { consoleInputRef } from './console_input';
import { msgFlowRef } from './message_flow';
const props = defineProps({
  appCode: {
    type: String,
    default: '',
    required: false
  },
  show: {
    type: Boolean,
    default: false,
    required: false
  },
  workflowCode: {
    type: String,
    default: '',
    required: false
  }
});
const agentAppRef = ref(null);
const currentSession = ref({
  session_code: '',
  session_source: '',
  session_task_params_schema: {}
});
const agentAppWidth = ref(500);
const showAgentApp = ref(false);
const currentWorkflowCode = ref('');
const isResizing = ref(false);
const startX = ref(0);
const startWidth = ref(0);
const streaming = ref(true);
const currentApp = ref({
  app_config: {}
});
const sessionParamsRef = ref(null);
const skipUserInput = ref(false);
async function initTestSession(newVal, keepSession = false) {
  const params = {
    app_code: newVal,
    session_test: true,
    session_code: null,
    workflow_code: currentWorkflowCode.value
  };
  if (keepSession) {
    params.session_code = currentSession.value.session_code;
  }
  const data = await initAppSession(params);
  if (!data.error_status) {
    if (currentSession.value?.session_code != data.result?.session_code) {
      currentSession.value = data.result;
      skipUserInput.value = data.result?.session_task_params_schema?.skip_user_question;
      console.log('初始化测试会话：', data.result, skipUserInput.value);
    } else {
      msgFlowRef.value?.refreshMsgFlow();
    }
  }
  return data.result;
}
function handleOverAgentApp() {
  const rect = agentAppRef.value.getBoundingClientRect();
  const leftBorderWidth = 10; // 左侧边框可触发拖拉的宽度范围
  if (event.clientX >= rect.left && event.clientX <= rect.left + leftBorderWidth) {
    agentAppRef.value.style.cursor = 'ew-resize';
  } else {
    agentAppRef.value.style.cursor = 'default';
  }
}
const onMouseDown = event => {
  const rect = agentAppRef.value.getBoundingClientRect();
  const leftBorderWidth = 10; // 左侧边框可触发拖拉的宽度范围
  if (event.clientX >= rect.left && event.clientX <= rect.left + leftBorderWidth) {
    isResizing.value = true;
    startX.value = event.clientX;
    startWidth.value = agentAppWidth.value;
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    agentAppRef.value.style.cursor = 'ew-resize';
  }
};
const onMouseMove = event => {
  if (isResizing.value) {
    const deltaX = event.clientX - startX.value;
    agentAppWidth.value = startWidth.value - deltaX;
    // 可设置最小宽度限制
    if (agentAppWidth.value < 300) {
      agentAppWidth.value = 300;
    }
  }
};
const onMouseUp = () => {
  if (isResizing.value) {
    isResizing.value = false;
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
    const rect = agentAppRef.value.getBoundingClientRect();
    const leftBorderWidth = 10;
    // @ts-ignore
    const mouseX = event.clientX;
    if (mouseX >= rect.left && mouseX <= rect.left + leftBorderWidth) {
      agentAppRef.value.style.cursor = 'ew-resize';
    } else {
      agentAppRef.value.style.cursor = 'default';
    }
  }
};
const onMouseLeave = () => {
  agentAppRef.value.style.cursor = 'default';
};
async function changeTestSession(appCode: string, sessionCode: string) {
  const data = await ISearchSession({
    session_codes: [sessionCode],
    session_source: appCode
  });
  if (!data.error_status) {
    currentSession.value = data.result[0];
    skipUserInput.value = data.result[0]?.session_task_params_schema?.skip_user_question;
    return data.result[0];
  }
}
async function handleBeginAnswer(data) {
  msgFlowRef.value?.beginAnswer(data);
  sessionParamsRef.value?.close();
}
onBeforeMount(async () => {
  initSocket();
});
watch(
  () => props.appCode,
  async newVal => {
    if (newVal) {
      const res = await appDetail({
        app_code: newVal
      });
      if (!res.error_status) {
        currentApp.value = res.result?.meta;
      }
    }
    if (newVal && newVal != currentSession.value?.session_source && showAgentApp.value) {
      await initTestSession(newVal);
    }
  },
  { immediate: true }
);
watch(
  () => props.show,
  async newVal => {
    showAgentApp.value = newVal;
  },
  { immediate: true }
);
watch(
  () => props.workflowCode,
  async newVal => {
    if (newVal && newVal != currentWorkflowCode.value) {
      currentWorkflowCode.value = newVal;
    }
  },
  { immediate: true }
);
defineExpose({
  initTestSession,
  currentSession,
  changeTestSession
});
</script>

<template>
  <div
    v-show="showAgentApp"
    ref="agentAppRef"
    class="agent-app-box"
    :style="{ width: agentAppWidth + 'px' }"
    @mousemove="handleOverAgentApp"
    @mousedown="onMouseDown"
    @mouseup="onMouseUp"
    @mouseleave="onMouseLeave"
  >
    <SessionParams
      v-if="currentSession?.session_task_params_schema?.ncOrders?.length"
      ref="sessionParamsRef"
      :session="currentSession"
      :title="currentApp.app_config?.params?.title"
      style="width: 100%"
      @begin-workflow="consoleInputRef?.askQuestion"
      @stop-workflow="consoleInputRef?.stopQuestion"
    />
    <MessageFlowV2
      ref="msgFlowRef"
      :session-code="currentSession?.session_code"
      style="width: 100%; height: 100%"
      :streaming="streaming"
      :debug="true"
      :disable="sessionParamsRef && !sessionParamsRef?.schemaReady"
      :welcome-config="currentApp.app_config?.welcome"
      @click-recommend-question="data => consoleInputRef?.clickRecommendQuestion(data)"
    />
    <ConsoleInput
      ref="consoleInputRef"
      :show="!skipUserInput"
      :session="currentSession"
      style="width: 100%"
      :streaming="streaming"
      :socket="socket"
      :disable="sessionParamsRef && !sessionParamsRef?.schemaReady"
      :row="1"
      @begin-answer="data => handleBeginAnswer(data)"
      @update-answer="newMsg => msgFlowRef.updateAnswer(newMsg)"
      @finish-answer="args => msgFlowRef?.finishAnswer(args)"
      @stop-answer="args => msgFlowRef?.stopAnswer(args)"
    />
  </div>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
#choose-model-area {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  width: calc(100% - 24px);
  max-width: 900px;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
}
.agent-app-box {
  position: fixed;
  top: 140px;
  right: 20px;
  height: calc(100vh - 200px);
  background: white;
  z-index: 999;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  box-shadow:
    0 4px 8px rgba(0, 0, 0, 0.1),
    0 6px 20px rgba(0, 0, 0, 0.1);
}
.agent-node-detail {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 6px;
  max-height: calc(100vh - 240px);
}
@media (width<768px) {
  #choose-model-area {
    padding: 8px;
    gap: 6px;
  }
}
</style>
