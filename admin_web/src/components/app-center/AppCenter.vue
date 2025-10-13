<script setup lang="ts">
import { Cpu, Link, Menu as IconMenu } from '@element-plus/icons-vue';
import { onMounted, onUnmounted, ref } from 'vue';
import router from '@/router';

const windowWidth = ref(window.innerWidth);
const currentIndex = ref('/next-console/appCenter/app_list');
function updateWidth() {
  windowWidth.value = window.innerWidth;
}
function changeCurrentIndexValue() {
  if (router.currentRoute.value.path.startsWith('/next-console/app-center/app-detail/')) {
    currentIndex.value = '/next-console/app-center/app-list';
  } else if (router.currentRoute.value.path.includes('/next-console/app-center/publish-detail/')) {
    currentIndex.value = '/next-console/app-center/publish-list';
  } else if (
    router.currentRoute.value.path.includes('/next-console/app-center/llm-create') ||
    router.currentRoute.value.path.includes('/next-console/app-center/llm-detail')
  ) {
    currentIndex.value = '/next-console/app-center/llm-manage';
  } else {
    currentIndex.value = router.currentRoute.value.path;
  }
}
onMounted(() => {
  window.addEventListener('resize', updateWidth);
  currentIndex.value = router.currentRoute.value.path;
  // 应用详情页也高亮

  router.afterEach(to => {
    if (to.path.startsWith('/next-console/app-center/app-detail/')) {
      currentIndex.value = '/next-console/app-center/app-list';
    } else if (to.path.includes('/next-console/app-center/publish-detail/')) {
      currentIndex.value = '/next-console/app-center/publish-list';
    } else if (
      to.path.includes('/next-console/app-center/llm-create') ||
      to.path.includes('/next-console/app-center/llm-detail')
    ) {
      currentIndex.value = '/next-console/app-center/llm-manage';
    } else {
      currentIndex.value = to.path;
    }
  });
  changeCurrentIndexValue();
});
// 在组件卸载时移除监听器，防止内存泄漏
onUnmounted(() => {
  window.removeEventListener('resize', updateWidth);
});
</script>

<template>
  <el-container style="height: 100%">
    <el-header>
      <div id="app-panel">
        <el-menu router :default-active="currentIndex" mode="horizontal">
          <el-menu-item index="/next-console/app-center/llm-manage">
            <el-icon><Cpu /></el-icon>
            <span>模型管理</span>
          </el-menu-item>
          <el-menu-item index="/next-console/app-center/app-list">
            <el-icon><IconMenu /></el-icon>
            <span>应用管理</span>
          </el-menu-item>
          <el-menu-item index="/next-console/app-center/publish-list">
            <el-icon><Link /></el-icon>
            <span>发布管理</span>
          </el-menu-item>
        </el-menu>
      </div>
    </el-header>
    <el-main style="padding: 0">
      <div v-if="router.currentRoute.value.name == 'appCenter'" id="welcome-box">
        <div class="slogan-container">
          <h1 class="slogan">欢迎使用AI应用工厂</h1>
        </div>
      </div>
      <router-view v-else />
    </el-main>
  </el-container>
</template>

<style scoped>
#app-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #dcdfe6;
}
#welcome-box {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}
.el-menu {
  border-right: none;
}
.slogan-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: white;
  perspective: 1000px;
}

.slogan {
  font-size: 60px;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.slogan:hover {
  transform: rotateX(10deg) rotateY(10deg);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}
</style>
