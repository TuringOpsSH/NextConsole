<script setup lang="ts">

import Next_console_left_menu from "@/components/global/next_console_global_aside/next_console_left_menu.vue";
</script>

<template>
  <el-container >
    <el-aside width="60px">
      <next_console_left_menu/>
    </el-aside>

    <el-main style="padding: 0 !important;">
      <el-container>
        <el-aside :width="panel_width">

        </el-aside>
        <el-main style="padding: 0 !important;">

          <div id="layout_button2" @click="switch_panel()" v-if="panel_width=='0px'">
            <el-image src="images/layout_alt_grey.svg"/>
          </div>
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
