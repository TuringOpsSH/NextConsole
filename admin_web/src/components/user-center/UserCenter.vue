<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserInfoStore } from '@/stores/userInfoStore';
const router = useRouter();
const filteredComponents = ref([
  {
    name: 'user_manage',
    label: '用户管理',
    route: {
      name: 'user_manage'
    },
    disable: false,
    role_require: ['admin', 'super_admin', 'next_console_admin', 'next_console_reader_admin']
  },
  {
    name: 'enterpriseManagement',
    label: '企业管理',
    route: {
      name: 'enterpriseManagement'
    },
    disable: false,
    role_require: ['next_console_admin', 'next_console_reader_admin']
  },
  {
    name: 'user_notification_list',
    label: '用户通知',
    route: {
      name: 'user_notification_list'
    },
    disable: false,
    role_require: ['next_console_admin', 'next_console_reader_admin']
  }
]);
onMounted(async () => {
  const userInfoStore = useUserInfoStore();
  // 检查用户权限, 禁用不符合权限的组件
  for (let component of filteredComponents.value) {
    if (!userInfoStore.userInfo?.user_role.some(role => component.role_require.includes(role))) {
      component.disable = true;
    }
  }
});

defineOptions({
  name: 'UserCenter'
});
</script>

<template>
  <el-container style="height: 100%">
    <el-header height="59px" style="padding: 0 !important">
      <div class="next-console-admin-header">
        <div class="component-box">
          <el-menu
            :default-active="router.currentRoute.value.name"
            class="el-menu-demo"
            mode="horizontal"
            router
            :ellipsis="false"
          >
            <el-menu-item
              v-for="component in filteredComponents"
              :key="component.name"
              :index="component.name"
              :route="component.route"
              :disabled="component.disable"
              class="menu-header-item"
            >
              {{ component.label }}
            </el-menu-item>
          </el-menu>
        </div>
      </div>
    </el-header>
    <el-main style="padding: 0 !important">
      <div v-if="router.currentRoute.value.name == 'user_center'" id="welcome-box">
        <div class="slogan-container">
          <h1 class="slogan">欢迎进入用户中心</h1>
        </div>
      </div>
      <router-view v-else />
    </el-main>
  </el-container>
</template>

<style scoped>
#welcome-box {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
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
