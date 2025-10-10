<script setup lang="ts">
import { ElMessage } from 'element-plus';

import { cancelSubscribeApi } from '@/api/contacts';
import router from '@/router';
import { useUserInfoStore } from '@/stores/user-info-store';

const userInfoStore = useUserInfoStore();
const visFlag = true;
function handleClose() {
  router.push({
    name: 'next_console_welcome_home'
  });
}
async function handleUnsubscribe() {
  // 更新邀请状态
  let params = {
    email: userInfoStore.userInfo.user_email
  };
  let res = await cancelSubscribeApi(params);
  if (!res.error_status) {
    ElMessage.success('取消订阅成功!');
    await router.push({
      name: 'next_console_welcome_home'
    });
  }
}
const phoneView = window.innerWidth < 768;
</script>

<template>
  <el-container>
    <el-main style="padding: 0 !important">
      <el-dialog
        v-model="visFlag"
        :modal="false"
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        :fullscreen="phoneView"
        @close="router.push({ name: 'next_console_welcome_home' })"
      >
        <div id="main_area">
          <div style="padding: 24px">
            <el-image src="/images/logo_text.svg" />
          </div>
          <div v-if="userInfoStore.userInfo?.user_email">
            <el-text>尊敬的用户：{{ userInfoStore.userInfo.user_email }}</el-text>
          </div>
          <div v-else>
            <el-text>尊敬的用户：{{ userInfoStore.userInfo.user_nick_name }}</el-text>
          </div>
          <div v-if="userInfoStore.userInfo?.user_email">
            <el-text type="danger" size="large"> 是否取消订阅NextConsole的最新产品信息邮件？ </el-text>
            <br />
            <br />
            <el-text type="info"> 退订后您将无法收到平台的最新促销活动、折扣信息等。 </el-text>
          </div>
          <div v-else>
            <el-empty description="暂无订阅数据" />
          </div>
          <div v-if="userInfoStore.userInfo?.user_email">
            <el-button type="primary" @click="handleUnsubscribe">确认取消</el-button>
            <el-button @click="handleClose">暂不取消</el-button>
          </div>
        </div>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<style scoped>
#main_area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
</style>
