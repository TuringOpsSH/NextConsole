<script setup lang="ts">
import { panel_width, switch_panel } from '@/components/contacts/contacts-panel/contacts_panel';
import ContactsPanel from '@/components/contacts/contacts-panel/contacts_panel.vue';
import WelcomeHome from '@/components/contacts/WelcomeHome.vue';
import router from '@/router';

</script>

<template>
  <el-container>
    <el-aside :width="panel_width">
      <ContactsPanel />
    </el-aside>
    <el-main style="padding: 0 !important">
      <WelcomeHome v-if="router.currentRoute.value.path == '/next-console/contacts'" />
      <router-view v-else />
      <div v-show="panel_width == '0px'" id="layout_button2" @click="switch_panel()">
        <el-image id="layout-alt" src="/images/layout_alt_blue.svg" />
      </div>
    </el-main>
  </el-container>
</template>

<style scoped>
#layout_button2 {
  position: fixed;
  left: 60px;
  top: 8px;
  margin: 10px;
  cursor: pointer;
  border-radius: 12px;
}
#layout-alt {
  width: 14px;
  height: 14px;
}
</style>
