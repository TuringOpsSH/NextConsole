<template>
  <el-scrollbar>
    <div id="app">
      <router-view />
    </div>
  </el-scrollbar>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { onBeforeUnmount, onMounted } from 'vue';
import { versionGet } from '@/api/base';

// 导入样式
import '@/styles/global.css';
import { systemConfigLoad } from '@/api/user-center';
import { clientFingerprint, getFingerPrint } from '@/components/global/web-socket';
import router from '@/router';
import { useUserConfigStore } from '@/stores/user-config-store';
import { useUserInfoStore } from '@/stores/user-info-store';

const userInfoStore = useUserInfoStore();
const userConfigStore = useUserConfigStore();
let versionCheckInterval = null;

async function getVersion() {
  try {
    const res = await versionGet();
    userConfigStore.systemVersion = res.result.version;
  } catch (error) {
    console.error('无法获取版本信息', error);
  }
}
async function checkVersion() {
  try {
    const res = await versionGet();
    if (res.result.version && userConfigStore.systemVersion && res.result.version !== userConfigStore.systemVersion) {
      window.location.reload();
    }
  } catch (error) {
    console.error('无法获取版本信息', error);
  }
}
async function loadSystemConfig() {
  const res = await systemConfigLoad({});
  if (res.result) {
    userConfigStore.updateSystemConfig(res.result);
    if (res.result.brand) {
      // 修改标签页图标与名字
      document.title = res.result.brand?.brand_name || 'NextConsole';
      const link: HTMLLinkElement | null = document.querySelector("link[rel~='icon']");
      if (link) {
        link.href = res.result.brand?.logo_url || '/images/logo.svg';
      }
    }
  }
}

async function acceptToken(event) {
  const data = event.data;
  console.log(event.origin, data);
  if (data.type === 'AUTH_TOKEN_TRANSFER') {
    console.log('Auth token received via postMessage');
    userInfoStore.token = data?.token;
    event.source.postMessage({ type: 'AUTH_SUCCESS' }, event.origin);
    const redirect = sessionStorage.getItem('redirectRoute');
    if (redirect) {
      const route = JSON.parse(redirect); // 将字符串解析为对象
      router.push(route); // 使用完整的路由对象
      sessionStorage.removeItem('redirectRoute');
      ElMessage.success('自动登录成功!');
      return;
    }
  }
}

onMounted(async () => {
  window.addEventListener('message', acceptToken, true);
  getVersion();
  loadSystemConfig();
  versionCheckInterval = setInterval(checkVersion, 180000);
  if (!clientFingerprint.value) {
    await getFingerPrint();
  }
  if (window.opener && !window.opener.closed) {
    window.opener.postMessage(
      {
        type: 'RECEIVER_READY'
      },
      '*'
    ); // 这里可以先使用 '*' 简化调试，上线前应替换为具体 origin
  }
});
onBeforeUnmount(() => {
  clearInterval(versionCheckInterval);
});
</script>

<style>
#app {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #ffffff;
}
</style>
