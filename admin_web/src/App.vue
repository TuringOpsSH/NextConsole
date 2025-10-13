<template>
  <el-scrollbar>
    <div id="app">
      <router-view />
    </div>
  </el-scrollbar>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted } from 'vue';
import { versionGet } from '@/api/base';
import { clientFingerprint, getFingerPrint } from '@/components/global/web-socket';

// 导入样式
import '@/styles/global.css';
import { systemConfigLoad } from '@/api/user-center';
import { useUserConfigStore } from '@/stores/user-config-store';

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

onMounted(async () => {
  getVersion();
  loadSystemConfig();
  versionCheckInterval = setInterval(checkVersion, 180000);
  if (!clientFingerprint.value) {
    await getFingerPrint();
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
