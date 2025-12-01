<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import WelcomeHome from '@/components/resource/WelcomeHome.vue';
import ResourcePanel from '@/components/resource/resource-panel/ResourcePanel.vue';

const router = useRouter();
const resourcePanelRef = ref();

defineOptions({
  name: 'ResourceMain'
});
</script>

<template>
  <el-container>
    <el-aside :width="resourcePanelRef?.panelWidth">
      <ResourcePanel ref="resourcePanelRef" />
    </el-aside>
    <el-main style="padding: 0 !important">
      <WelcomeHome v-if="router.currentRoute.value.path == '/next-console/resources'" />
      <router-view v-else />
      <div v-show="resourcePanelRef?.panelWidth == '0px'" id="layout_button2" @click="resourcePanelRef?.switchPanel">
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
