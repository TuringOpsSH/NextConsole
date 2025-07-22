<template>

  <el-container style="height: 100vh;">
    <el-aside width="81px">
      <next_console_menu></next_console_menu>
    </el-aside>

    <el-container class="main_container">
      <el-header  style="height:80px;" >
        <next_console_page_header :components="component_list"/>
      </el-header>

      <el-main >
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>

</template>




<script setup>
import next_console_menu from '@/components/global/next_console_menu.vue'
import next_console_page_header from '@/components/global/next_console_page_header.vue'
import {onMounted, onUnmounted, ref} from "vue";
const component_list = [
  {"name":"工具管理","url":"/next_console/function_center/tool_manage"},
  {"name":"组件管理","url":"/next_console/function_center/component_manage"},
  {"name":"环境管理","url":"/next_console/function_center/env_manage"},

]
</script >
<style scoped>


.main_container{
  height: 100vh;
  width: 100vw;
}
.el-aside{
  width: 81px ;
}
.el-main {
  --el-main-padding: 0;
  height:  calc(100vh - 80px);
}
.el-header{
  height: 60px !important;
}
</style>
