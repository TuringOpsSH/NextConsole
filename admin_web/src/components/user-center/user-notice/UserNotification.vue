<script setup lang="ts">
import { onMounted } from 'vue';
</script>

<template>
  <el-container>
    <router-view />
  </el-container>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  height: 100%;
  gap: 12px;
}
#notice-head {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  width: 100%;
  height: 60px;
  gap: 12px;
}
#notice-head-left {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  max-width: 100px;
  height: 100%;
  gap: 12px;
}
#notice-head-right {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: flex-end;
  width: 100%;
  height: 100%;
  gap: 12px;
}
#notice-table-area {
  width: 100%;
  height: 100%;
}
</style>
