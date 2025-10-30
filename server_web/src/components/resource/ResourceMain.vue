<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import { useRouter } from 'vue-router';
import { panel_width, switch_panel } from '@/components/resource/resource-panel/panel';
import Resource_panel from '@/components/resource/resource-panel/ResourcePanel.vue';

import WelcomeHome from '@/components/resource/WelcomeHome.vue';

const isShowResourcePanel = useSessionStorage('isShowResourcePanel', true);
const router = useRouter();

function switchPanel() {
  isShowResourcePanel.value = true;
  switch_panel();
}

defineOptions({
  name: 'ResourceMain'
});
</script>

<template>
  <el-container>
    <el-aside :width="panel_width">
      <resource_panel />
    </el-aside>
    <el-main style="padding: 0 !important">
      <welcome-home v-if="router.currentRoute.value.path == '/next_console/resources'" />
      <router-view v-else />
      <div v-show="panel_width == '0px'" id="layout_button2" @click="switchPanel">
        <el-tooltip :content="$t('openSidebar')" effect="light">
          <el-image id="layout_alt" src="/images/layout_alt_blue.svg" />
        </el-tooltip>
      </div>
    </el-main>
  </el-container>
</template>

<style scoped>
#layout_button2 {
  position: fixed;
  left: 50px;
  top: 8px;
  margin: 10px;
  cursor: pointer;
  border-radius: 12px;
}
@media (max-width: 768px) {
  #layout_button2 {
    left: 55px;
  }
  #layout_alt {
    width: 14px;
    height: 14px;
  }
}
</style>
