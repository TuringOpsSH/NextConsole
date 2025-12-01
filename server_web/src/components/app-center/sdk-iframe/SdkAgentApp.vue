<script setup lang="ts">
import 'highlight.js/styles/stackoverflow-light.min.css';
import { nextTick, ref, watch } from 'vue';
import { onBeforeMount } from 'vue-demi';
import { appDetail, initAppSession } from '@/api/app-center';
import { initSocket, socket } from '@/components/global/web_socket';
import ConsoleInput from '@/components/next-console/workbenches/ConsoleInput.vue';
import MessageFlowV2 from '@/components/next-console/workbenches/MessageFlowV2.vue';
import SessionParams from '@/components/next-console/workbenches/SessionParams.vue';
import { consoleInputRef } from '@/components/next-console/workbenches/console_input';
import { msgFlowRef } from '@/components/next-console/workbenches/message_flow';
import router from '@/router';
import { useAppInfoStore } from '@/stores/app-info-store';
import { useSessionStore } from '@/stores/sessionStore';
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
  },
  autoAsk: {
    type: String,
    default: 'false',
    required: false
  }
});
const appInfoStore = useAppInfoStore();
const agentAppRef = ref(null);
const currentSession = ref({
  session_code: '',
  session_source: '',
  session_task_params_schema: {
    ncOrders: []
  },
  id: null
});
const currentApp = ref();
const sessionParamsRef = ref(null);
const store = useSessionStore();
const streaming = ref(true);
const skipUserInput = ref(false);
const autoAskQuery = ref(false);
const emits = defineEmits(['session-ready']);
async function initSession(appCode: string, newSessionCode: string) {
  if (!appCode) {
    return;
  }
  if (currentSession.value?.session_code == newSessionCode && newSessionCode) {
    return;
  }
  const params = {
    app_code: appCode,
    session_code: newSessionCode,
    session_task_params: appInfoStore.workflowParams,
    task_code: appInfoStore.taskCode
  };
  const data = await initAppSession(params);
  if (!data.error_status) {
    if (currentSession.value?.session_code != data.result?.session_code) {
      currentSession.value = data.result;
      skipUserInput.value = data.result?.session_task_params_schema?.skip_user_question;
      router.replace({
        params: {
          appCode: currentSession.value.session_source,
          sessionCode: currentSession.value.session_code
        },
        query: {
          ...router.currentRoute.value.query
        }
      });
    }
    if (store.getLatestSessionListRef) {
      await store.getLatestSessionListRef();
    }
    if (autoAskQuery.value && currentSession.value.id) {
      consoleInputRef.value?.updateQuestion(appInfoStore.question);
    }
  }
  await nextTick();
  emits('session-ready', { sessionCode: router.currentRoute.value.params.sessionCode });
  return data.result;
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
    await initSession(props.appCode, newVal);
  },
  { immediate: true }
);
watch(
  () => props.autoAsk,
  newVal => {
    if (newVal == 'true') {
      autoAskQuery.value = true;
    } else {
      autoAskQuery.value = false;
    }
  },
  { immediate: true }
);
store.registerInitAppSessionFn(initSession);
defineExpose({
  initSession,
  currentSession
});
</script>

<template>
  <div ref="agentAppRef" class="agent-app-box">
    <SessionParams
      v-if="currentSession?.session_task_params_schema?.ncOrders?.length"
      ref="sessionParamsRef"
      :session="currentSession"
      :title="currentApp?.app_config?.params?.title"
      style="width: 100%"
      @begin-workflow="consoleInputRef?.askQuestion"
      @stop-workflow="consoleInputRef?.stopQuestion"
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
      :show="!skipUserInput"
      :session="currentSession"
      :auto-ask="autoAskQuery"
      style="width: 100%"
      :streaming="streaming"
      :socket="socket"
      :disable="sessionParamsRef && !sessionParamsRef?.schemaReady"
      :row="1"
      :asr-able="currentApp?.app_config?.params?.asr"
      :rag-lock="currentApp.app_config?.params?.ragLock"
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
