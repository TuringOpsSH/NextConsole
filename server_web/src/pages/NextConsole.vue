<script setup lang="ts">
import { onMounted } from 'vue';
import NextConsoleLeftMenu from '@/components/global/NextConsoleLeftMenu.vue';
import { clientFingerprint, getFingerPrint, initSocket } from '@/components/global/web_socket';

// 组件挂载时进行连接
onMounted(async () => {
  if (!clientFingerprint.value) {
    await getFingerPrint();
  }
  initSocket();
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
