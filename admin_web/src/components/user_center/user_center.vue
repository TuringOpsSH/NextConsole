<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { user_info } from '@/components/user_center/user';
import { getInfo } from '@/utils/auth';
import { useRouter } from 'vue-router';
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
  user_info.value = await getInfo(true);
  // 检查用户权限, 禁用不符合权限的组件
  for (let component of filteredComponents.value) {
    if (!user_info.value?.user_role.some(role => component.role_require.includes(role))) {
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
      <router-view />
    </el-main>
  </el-container>
</template>

<style scoped></style>
