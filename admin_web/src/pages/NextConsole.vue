<script setup lang="ts">
import { onMounted } from 'vue';
import { systemConfigGet, userConfigGet } from '@/api/user-center';
import NextConsoleLeftMenu from '@/components/global/NextConsoleLeftMenu.vue';
import router from '@/router';
import { useUserConfigStore } from '@/stores/user-config-store';
import { IUserConfig } from '@/types/user-center';
const userConfigStore = useUserConfigStore();
// 组件挂载时进行连接
onMounted(async () => {
  if (router.currentRoute.value.name === 'next_console') {
    router.push({
      name: 'appCenter'
    });
  }
  const userConfigData = await userConfigGet({});
  if (!userConfigData.error_status) {
    userConfigStore.updateUserConfig(userConfigData.result as IUserConfig);
  }
  const res = await systemConfigGet({});
  if (!res.error_status) {
    userConfigStore.updateSystemConfig(res.result);
  }
});
</script>

<template>
  <el-container>
    <el-aside width="48px">
      <NextConsoleLeftMenu />
    </el-aside>

    <el-main style="padding: 0 !important">
      <router-view />
    </el-main>
  </el-container>
</template>

<style scoped></style>
