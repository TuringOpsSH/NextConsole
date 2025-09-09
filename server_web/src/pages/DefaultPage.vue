<script setup lang="ts">
import NextConsoleLeftMenu from '@/components/global/NextConsoleLeftMenu.vue';
import ConsolePanel from '@/components/next-console/ConsolePanel.vue';
import WelcomeHome from '@/components/next-console/WelcomeHome.vue';
</script>

<template>
  <el-container>
    <el-aside width="60px">
      <NextConsoleLeftMenu />
    </el-aside>

    <el-main style="padding: 0 !important">
      <el-container>
        <el-aside>
          <ConsolePanel />
        </el-aside>
        <el-main style="padding: 0 !important">
          <WelcomeHome />
        </el-main>
      </el-container>
    </el-main>
  </el-container>
</template>

<style scoped>
#layout_button2 {
  position: fixed;
  left: 60px;
  top: 6px;
  margin: 10px;
  cursor: pointer;
  border-radius: 12px;
}
</style>
