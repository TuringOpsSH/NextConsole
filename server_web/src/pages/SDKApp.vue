<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { appDetail } from '@/api/app-center';
import { loginByToken } from '@/api/user-center';
import router from '@/router';
import { useAppInfoStore } from '@/stores/app-info-store';
import { useUserInfoStore } from '@/stores/user-info-store';

// 0 默认，1 正常，2 用户鉴权中，3 应用初始化中，-1 未知异常， -2 用户鉴权失败， -3 应用初始化失败
const initStatus = ref(0);
const appInfoStore = useAppInfoStore();
const userInfoStore = useUserInfoStore();
let parentEvent = null;
async function loadAppInfo(data) {
  // 加载应用信息与配置
  const res = await appDetail({
    app_code: data?.appCode
  });
  if (!res.error_status) {
    // 检查域名配置
    if (res.result?.connectors) {
      for (const connection of res.result?.connectors) {
        if (connection.id !== 3) {
          continue;
        }
        if (!connection?.picked) {
          continue;
        }
        if (connection?.config?.domains.includes(data.origin) || connection?.config?.domains.includes('*')) {
          return res.result;
        }
      }
    }
  }
  return {};
}
async function routerToSession(data) {
  const appInfo = await loadAppInfo(data);
  if (!appInfo?.id) {
    initStatus.value = -3;
    return;
  }
  appInfoStore.updateAppInfo(appInfo);
  appInfoStore.taskCode = data?.taskCode;
  appInfoStore.updateWorkflowParams(data?.workflowParams);
  appInfoStore.updateAttachments(data?.attachments);
  appInfoStore.question = data?.question;

  initStatus.value = 1;
  await router.push({
    name: 'agentApp',
    params: {
      appCode: data?.appCode,
      sessionCode: data.sessionCode
    },
    query: {
      autoAsk: data?.autoAsk
    }
  });
}
async function initAppInfo(event) {
  // 根据sdk传入的config 进行页面更新
  const data = event.data;
  data.origin = event.origin;
  parentEvent = event;
  await routerToSession(data);
}
async function acceptToken(event) {
  // 接受token信息并向后端进行校验
  const data = event.data;
  console.log(event.origin, data);
  if (data.type === 'SDK_TOKEN_TRANSFER') {
    console.log('Auth token received via postMessage');
    // 后端校验并兑换token
    const res = await loginByToken({
      token: data.token,
      extra_data: data?.extraData
    });
    if (!res.error_status) {
      userInfoStore.updateUserInfo(res.result?.userinfo);
      userInfoStore.token = res.result?.token;
      userInfoStore.expireTime = res.result?.expire_time;
      event.source.postMessage({ type: 'SDK_AUTH_SUCCESS' }, event.origin);
      parentEvent = event;
      await routerToSession(data);
    } else {
      initStatus.value = -2;
    }
  } else if (data.type === 'SDK_INIT_CONFIG') {
    initAppInfo(event);
  } else if (data.type === 'SDK_CONFIG_UPDATE') {
    initAppInfo(event);
  }
}
function emitSessionCode(data) {
  if (!parentEvent) {
    return;
  }
  parentEvent.source.postMessage({ type: 'SDK_UPDATE_SUCCESS', sessionCode: data.sessionCode }, parentEvent.origin);
}
onMounted(async () => {
  window.addEventListener('message', acceptToken, false);
  if (window.opener && !window.opener.closed) {
    window.opener.postMessage(
      {
        type: 'SDK_RECEIVER_READY'
      },
      '*'
    );
  }
  if (parent) {
    parent.postMessage(
      {
        type: 'SDK_RECEIVER_READY'
      },
      '*'
    );
  }
});
</script>

<template>
  <div v-loading="initStatus == 0" class="main-area">
    <div v-show="initStatus == 1">
      <router-view
        @session-ready="
          args => {
            emitSessionCode(args);
          }
        "
      />
    </div>
    <div v-show="initStatus == 2" class="std-middle-box">
      <h5>用户自动登录中...</h5>
    </div>
    <div v-show="initStatus == -2" class="std-middle-box">
      <h5>用户自动登录失败，请关闭！</h5>
    </div>
    <div v-show="initStatus == 3" class="std-middle-box">
      <h5>应用加载中...</h5>
    </div>
    <div v-show="initStatus == -3" class="std-middle-box">
      <h5>应用加载失败，请关闭！</h5>
    </div>
    <div v-show="initStatus == -1" class="std-middle-box">
      <h5>未知异常，请联系平台管理员！</h5>
    </div>
    <div v-show="initStatus == 0" class="std-middle-box">
      <el-empty />
    </div>
  </div>
</template>

<style scoped>
.main-area {
  width: 100vw;
  height: 100vh;
}
.std-middle-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
</style>
