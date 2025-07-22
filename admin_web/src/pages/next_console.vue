<script setup lang="ts">
import { onMounted } from 'vue';
import NextConsoleLeftMenu from '@/components/global/next_console_global_aside/next_console_left_menu.vue';
import router from '@/router';

// 组件挂载时进行连接
onMounted(async () => {
  if (router.currentRoute.value.name === 'next_console') {
    router.push({
      name: 'appCenter'
    });
  }
});
</script>

<template>
  <el-container>
    <el-aside width="60px">
      <NextConsoleLeftMenu />
    </el-aside>

    <el-main style="padding: 0 !important">
      <router-view />
    </el-main>
  </el-container>
</template>

<style scoped></style>
