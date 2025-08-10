<script setup lang="ts">
import 'highlight.js/styles/stackoverflow-light.min.css';
import {ref, watch} from 'vue';
import {onBeforeMount} from 'vue-demi';
import {appDetail, initAppSession} from '@/api/app-center';
import ConsoleInput from './ConsoleInput.vue';
import MessageFlowV2 from './MessageFlowV2.vue';
import {consoleInputRef} from './console_input';
import {msgFlowRef} from './message_flow';
import {useSessionStore} from '@/stores/sessionStore';
import {initSocket, socket} from '@/components/global/web_socket/web_socket';
import SessionParams from "./SessionParams.vue";
import router from "@/router";
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
async function initSession(appCode:string, newSessionCode:string) {
  if (!appCode) {
    return ;
  }
  if (currentSession.value?.session_code == newSessionCode) {
    return ;
  }
  const params = {
    app_code: appCode,
    session_code: newSessionCode,
  };
  const data = await initAppSession(params);
  if (!data.error_status) {
    if (currentSession.value?.session_code != data.result?.session_code) {
      currentSession.value = data.result;
      router.replace(
        {
          params: {
            appCode: currentSession.value.session_source,
            sessionCode: currentSession.value.session_code
          }
        }
      )

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
    if (newVal != currentSession.value.session_code) {
      await initSession(props.appCode, newVal);
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
    <SessionParams
        ref="sessionParamsRef"
        v-if="currentSession?.session_task_params_schema?.ncOrders?.length"
        :session="currentSession"
        :title="currentApp.app_config?.params?.title"
        style="width: 100%"
    />
    <MessageFlowV2
        ref="msgFlowRef"
        :session-code="currentSession.session_code"
        style="width: 100%"
        :streaming="streaming"
        :welcome-config="currentApp?.app_config?.welcome"
        @click-recommend-question="data => consoleInputRef?.clickRecommendQuestion(data)"
    />
    <ConsoleInput
      ref="consoleInputRef"
      :session="currentSession"
      style="width: 100%"
      :streaming="streaming"
      :socket="socket"
      @begin-answer="data => msgFlowRef.beginAnswer(data)"
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
  height: calc(100vh - 24px);
  background: white;
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
