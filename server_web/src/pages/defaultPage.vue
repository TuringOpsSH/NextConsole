<script setup lang="ts">

import Next_console_left_menu from "@/components/global/next_console_global_aside/next_console_left_menu.vue";
import ConsolePanel from "@/components/next_console/ConsolePanel.vue";
import WelcomeHome from "@/components/next_console/WelcomeHome.vue";
</script>

<template>
  <el-container >
    <el-aside width="60px">
      <next_console_left_menu/>
    </el-aside>

    <el-main style="padding: 0 !important;">
      <el-container>
        <el-aside>
          <ConsolePanel/>
        </el-aside>
        <el-main style="padding: 0 !important;">

          <WelcomeHome />

        </el-main>
      </el-container>
    </el-main>
  </el-container>

</template>

<style scoped>
#layout_button2{
  position: fixed;
  left: 60px;
  top: 6px;
  margin: 10px;
  cursor: pointer;
  border-radius: 12px;
}
</style>
