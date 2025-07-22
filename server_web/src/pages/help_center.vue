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
  {"name":"社区趋势","url":"/next_console/help_center/community_trends"},
  {"name":"互动论坛","url":"/next_console/help_center/forum"},
  {"name":"视频资源","url":"/next_console/help_center/video_resources"},
  {"name":"培训课程","url":"/next_console/help_center/training_course"},
  {"name":"产品文档","url":"/next_console/help_center/product_document"},



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
