<script setup lang="ts">
import { Memo } from '@element-plus/icons-vue';
import { ref } from 'vue';
import ConsolePanel from '@/components/next-console/ConsolePanel.vue';

const panelRef = ref();
</script>

<template>
  <el-container>
    <el-aside :width="panelRef?.panelWidth" class="panel-side">
      <ConsolePanel ref="panelRef" />
    </el-aside>
    <el-main style="padding: 0 !important">
      <router-view />
      <div v-show="!panelRef?.showSidebar" id="layout_button2">
        <el-tooltip content="打开侧边栏" placement="right" :show-after="1500">
          <el-button :icon="Memo" circle @click="panelRef?.switchPanel" />
        </el-tooltip>
      </div>
    </el-main>
  </el-container>
</template>

<style scoped lang="scss">
#layout_button2 {
  position: fixed;
  left: 60px;
  top: 60px;
}
.panel-side {
  transition: all 0.3s ease;
}
.el-button {
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
