<script setup lang="ts">

import Contacts_panel from "@/components/contacts/contacts_panel/contacts_panel.vue";
import {panel_width,switch_panel} from "@/components/contacts/contacts_panel/contacts_panel";
import Welcome_home from "@/components/contacts/welcome_home.vue";
import router from "@/router";
import {} from "@/components/resource/resource_panel/panel";
</script>

<template>
   <el-container>
     <el-aside :width="panel_width">
        <Contacts_panel/>
     </el-aside>
     <el-main style="padding: 0 !important;">
       <welcome_home v-if="router.currentRoute.value.path == '/next_console/contacts'"/>
       <router-view v-else/>
       <div id="layout_button2" @click="switch_panel()" v-show="panel_width=='0px'">
         <el-image src="images/layout_alt_blue.svg" id="layout-alt"/>
       </div>
     </el-main>
   </el-container>
</template>

<style scoped>
#layout_button2{
  position: fixed;
  left: 60px;
  top: 8px;
  margin: 10px;
  cursor: pointer;
  border-radius: 12px;
}
#layout-alt{
  width: 14px;
  height: 14px;
}
</style>
