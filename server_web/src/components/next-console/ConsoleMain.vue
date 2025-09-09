<script setup lang="ts">
import {ref} from 'vue';
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
      <div v-if="!panelRef?.showSidebar" id="layout_button2" @click="panelRef?.switchPanel">
        <el-tooltip effect="light" content="打开侧边栏">
          <el-image src="/images/layout_alt_grey.svg" />
        </el-tooltip>
      </div>
    </el-main>
  </el-container>
</template>

<style scoped lang="scss">
#layout_button2 {
  position: fixed;
  left: 60px;
  top: 6px;
  margin: 10px;
  cursor: pointer;
  border-radius: 12px;
}
.panel-side {
  transition: all 0.3s ease;
}
</style>
