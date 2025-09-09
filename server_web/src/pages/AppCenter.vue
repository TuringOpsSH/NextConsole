<script setup lang="ts">
import { ref } from 'vue';
import { onBeforeMount } from 'vue-demi';
import { getUser } from '@/api/user-center';
import router from '@/router';
import { useUserInfoStore } from '@/stores/userInfoStore';
const userInfoStore = useUserInfoStore();
const errorMsg = ref('请选择一个应用');
onBeforeMount(async () => {
  // 初始化鉴权信息
  if (router.currentRoute.value.query?.token) {
    userInfoStore.token = router.currentRoute.value.query.token as string;
  }
  const res = await getUser({});
  if (res.error_status) {
    userInfoStore.$reset();
    router.push({ name: 'login' });
  }
  userInfoStore.updateUserInfo(res.result);
});
</script>

<template>
  <el-container>
    <el-main v-if="!router.currentRoute.value.params?.app_code">
      <div style="width: 100vw; height: 100vh">
        <el-empty :description="errorMsg" />
      </div>
    </el-main>
    <router-view v-else />
  </el-container>
</template>

<style scoped></style>
