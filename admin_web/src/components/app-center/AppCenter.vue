<script setup lang="ts">
import { Document, Menu as IconMenu, Link, Cpu, Medal } from '@element-plus/icons-vue';
import { onMounted, onUnmounted, ref } from 'vue';
import router from '@/router';
const windowWidth = ref(window.innerWidth);
const currentIndex = ref('/next-console/appCenter/app_list');
function updateWidth() {
  windowWidth.value = window.innerWidth;
}

onMounted(() => {
  window.addEventListener('resize', updateWidth);
  currentIndex.value = router.currentRoute.value.path;
  // 应用详情页也高亮
  router.afterEach(to => {
    if (to.path.startsWith('/next-console/appCenter/app_detail/')) {
      currentIndex.value = '/next-console/appCenter/app_list';
    } else {
      currentIndex.value = to.path;
    }
  });
});
// 在组件卸载时移除监听器，防止内存泄漏
onUnmounted(() => {
  window.removeEventListener('resize', updateWidth);
});
</script>

<template>
  <el-container style="height: 100vh">
    <el-container>
      <el-aside width="120px">
        <div id="app-panel">
          <el-menu router :default-active="currentIndex">
            <el-menu-item index="/next-console/appCenter/app_list">
              <el-icon><IconMenu /></el-icon>
              <span>应用管理</span>
            </el-menu-item>
            <el-menu-item index="/next-console/appCenter/resource_manage" disabled>
              <el-icon><Document /></el-icon>
              <span>资源管理</span>
            </el-menu-item>
            <el-menu-item index="/next-console/appCenter/publish_list">
              <el-icon><Link /></el-icon>
              <span>发布管理</span>
            </el-menu-item>
            <el-menu-item index="/next-console/appCenter/llm_manage/llm">
              <el-icon><Cpu /></el-icon>
              <span>模型管理</span>
            </el-menu-item>
            <el-menu-item index="/next-console/appCenter/effect_manage" disabled>
              <el-icon><Medal /></el-icon>
              <span>效果评测</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-aside>
      <el-main style="padding: 0">
        <div v-if="router.currentRoute.value.name == 'appCenter'" id="welcome-box">
          <div class="slogan-container">
            <h1 class="slogan">欢迎使用AI应用工厂</h1>
          </div>
        </div>
        <router-view v-else />
      </el-main>
    </el-container>
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
