<script setup lang="ts">
import router from '@/router';
import {onBeforeMount} from 'vue-demi';
import {setToken, getInfo} from '@/utils/auth';
import { ref } from 'vue';
import {user_info} from "@/components/user_center/user";

const error_msg = ref('请选择一个应用')
onBeforeMount(async () => {

  // 初始化鉴权信息
  if (router.currentRoute.value.query?.token) {
    setToken(router.currentRoute.value.query.token as string)
  }
  user_info.value = await getInfo(true);

})
</script>

<template>
<el-container>
  <el-main v-if="!router.currentRoute.value.params?.app_code">
    <div style="width:100vw; height: 100vh">
      <el-empty :description="error_msg" />
    </div>
  </el-main>
  <router-view v-else />
</el-container>
</template>

<style scoped>

</style>
