<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';

const windowWidth = ref(window.innerWidth);
function updateWidth() {
  windowWidth.value = window.innerWidth;
}

onMounted(() => {
  window.addEventListener('resize', updateWidth);
});
// 在组件卸载时移除监听器，防止内存泄漏
onUnmounted(() => {
  window.removeEventListener('resize', updateWidth);
});
</script>

<template>
  <el-container style="height: 100vh">
    <el-container>
      <el-main style="padding: 0">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped />
