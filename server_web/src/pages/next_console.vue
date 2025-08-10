<script setup lang="ts">

import Next_console_left_menu from "@/components/global/next_console_global_aside/next_console_left_menu.vue";
import {onMounted} from "vue";
import {clientFingerprint, getFingerPrint, initSocket} from "@/components/global/web_socket/web_socket";
import router from '@/router';
const phone_view =  window.innerWidth < 768

// 组件挂载时进行连接
onMounted(async () => {
  if( !clientFingerprint.value){
    await getFingerPrint()
  }
  initSocket()


});

</script>

<template>
  <el-container>

    <el-aside width="48px" >
      <next_console_left_menu/>
    </el-aside>

    <el-main style="padding: 0 !important;">
      <router-view/>
    </el-main>

  </el-container>

</template>

<style scoped>

</style>
