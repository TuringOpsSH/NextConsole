<template>
  <el-scrollbar >
    <div id="app" @click="close_menu">
      <router-view/>
    </div>
  </el-scrollbar>
</template>

<script setup lang="ts">
import {onBeforeUnmount, onMounted} from 'vue'
import {check_version, get_version} from "@/utils/base";
// 导入样式
import "@/styles/global.css"
let versionCheckInterval = null;
onMounted(async () => {
  get_version()
  versionCheckInterval = setInterval(check_version, 180000);

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
