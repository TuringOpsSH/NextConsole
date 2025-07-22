<script setup lang="ts">
import 'highlight.js/styles/vs2015.min.css';
import {ref, watch} from 'vue';
import {onBeforeMount} from 'vue-demi';
import {appDetail, initAppSession} from '@/api/app-center';
import ConsoleInput from './ConsoleInput.vue';
import MessageFlowV2 from './MessageFlowV2.vue';
import {consoleInputRef} from './console_input';
import {msgFlowRef} from './message_flow';
import {useSessionStore} from '@/stores/sessionStore';

import {initSocket, socket} from '@/components/global/web_socket/web_socket';

const props = defineProps({
  appCode: {
    type: String,
    default: '',
    required: false
  },
  sessionCode: {
    type: String,
    default: '',
    required: false
  }
});
const agentAppRef = ref(null);
const consoleInputHeight = ref(180);
const currentSession = ref({
  session_code: '',
  session_source: '',
  id: null
});
const currentApp = ref();
const store = useSessionStore();
const isResizing = ref(false);
const startX = ref(0);
const startWidth = ref(0);
const streaming = ref(true);
async function initSession(newVal, keepSession = false) {
  if (!newVal) {
    return;
  }
  const params = {
    app_code: newVal,
    session_code: null
  };
  if (keepSession) {
    params.session_code = currentSession.value.session_code;
  }
  const data = await initAppSession(params);
  if (!data.error_status) {
    if (currentSession.value?.session_code != data.result?.session_code) {
      currentSession.value = data.result;
    } else {
      msgFlowRef.value?.refreshMsgFlow();
    }
    if (store.getLatestSessionListRef) {
      await store.getLatestSessionListRef();
    }
  }
  return data.result;
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
        currentApp.value = res.result;
      }
      currentSession.value.session_source = newVal;
    }
  },
  { immediate: true }
);
watch(
  () => props.sessionCode,
  async newVal => {
    if (currentSession.value?.session_code == newVal) {
      msgFlowRef.value?.refreshMsgFlow();
    } else {
      currentSession.value.session_code = newVal;
    }
    const res = await initSession(props.appCode, true);
    if (res) {
      currentSession.value = res;

    }

  },
  { immediate: true }
)
store.registerInitAppSessionFn(initSession);
defineExpose({
  initSession,
  currentSession
});

</script>

<template>
  <div
    ref="agentAppRef"
    class="agent-app-box"
  >
    <MessageFlowV2
      ref="msgFlowRef"
      :session-code="currentSession.session_code"
      :height="'calc(100% - ' + consoleInputHeight + 'px)'"
      style="width: 100%"
      :streaming="streaming"
      :welcome-config="currentApp?.app_config?.welcome"
      @click-recommend-question="data => consoleInputRef?.clickRecommendQuestion(data)"
    />
    <ConsoleInput
      ref="consoleInputRef"
      :session="currentSession"
      :height="consoleInputHeight.toString() + 'px'"
      style="width: 100%"
      :streaming="streaming"
      :socket="socket"
      @begin-answer="data => msgFlowRef.beginAnswer(data)"
      @update-answer="newMsg => msgFlowRef.updateAnswer(newMsg)"
      @finish-answer="args => msgFlowRef?.finishAnswer(args)"
      @stop-answer="args => msgFlowRef?.stopAnswer(args)"
      @height-change="args => (consoleInputHeight = args.newHeight)"
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
  height: calc(100vh - 24px);
  background: white;
  display: flex;
  justify-content: center;
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
