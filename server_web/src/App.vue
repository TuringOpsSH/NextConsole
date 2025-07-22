<template>
  <el-scrollbar >
    <div id="app" @click="close_menu">
      <router-view/>
    </div>
  </el-scrollbar>
</template>

<script setup lang="ts">
import {onBeforeUnmount, onMounted} from 'vue'
import {checkVersion, getVersion} from "@/utils/base";
import {resource_list_context_menu_flag} from "@/components/resource/resource_list/resource_context_menu/context_menu";
import {clientFingerprint, getFingerPrint} from "@/components/global/web_socket/web_socket";
// 导入样式
import "@/styles/global.css"
import {
  resource_shortcut_context_menu_flag
} from "@/components/resource/resource_shortcut/resource_context_menu/context_menu";
import {resource_share_context_menu_flag} from "@/components/resource/share_resources/context_menu/context_menu";

let versionCheckInterval = null;
onMounted(async () => {
  getVersion()
  versionCheckInterval = setInterval(checkVersion, 180000);
  if( !clientFingerprint.value){
    await getFingerPrint()
  }
})
onBeforeUnmount(() => {
  clearInterval(versionCheckInterval);
});
function close_menu(event){
  // 关闭菜单
  if (
      event.target.id !== 'resource_list_menu_box'
      && event.target.id !== 'resource_shortcut_menu_box'
      && event.target.id !== 'resource_share_menu_box'

  ) {
    resource_shortcut_context_menu_flag.value = false;
    resource_list_context_menu_flag.value = false;
    resource_share_context_menu_flag.value = false;
  }

}



</script>

<style>
#app {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #FFFFFF;
}

</style>
