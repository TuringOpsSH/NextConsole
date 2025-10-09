<script setup lang="ts">
// 定义属性
import { ElMessage } from 'element-plus';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { wxRegister } from '@/api/user-center';
import { useUserInfoStore } from '@/stores/user-info-store';

const props = defineProps({
  code: {
    type: String,
    required: true,
    default: null
  },
  state: {
    type: String,
    default: 'true',
    required: false
  }
});
const localCode = ref(null);
const localState = ref(null);
const modelStr = ref(null);
const router = useRouter();
const loading = ref(true);
const errStatus = ref(false);
const errMsg = ref('');
const userInfoStore = useUserInfoStore();
onMounted(() => {
  localCode.value = props.code;
  localState.value = props.state;
  if (localState.value == 'register') {
    modelStr.value = '自动注册';
  } else if (localState.value == 'login' || localState.value.includes('login')) {
    modelStr.value = '自动登录';
  } else if (localState.value == 'bind') {
    modelStr.value = '自动绑定';
  } else if (localState.value == 'update') {
    modelStr.value = '自动更新';
  } else {
    router.push({ path: '/403' });
    return;
  }

  let params = {
    code: localCode.value,
    state: localState.value,
    domain: window.location.hostname
  };
  if (localState.value == 'bind' || localState.value == 'update') {
    params['token'] = userInfoStore.token;
  }
  wxRegister(params).then(res => {
    if (!res.error_status) {
      userInfoStore.updateUserInfo(res.result?.userinfo);
      userInfoStore.token = res.result?.token;
      userInfoStore.expireTime = res.result?.expire_time;
      ElMessage.success(modelStr.value + '成功！');
      if (localState.value == 'register' || localState.value == 'login' || localState.value.includes('login')) {
        const redirect = sessionStorage.getItem('redirectRoute');
        if (redirect) {
          const route = JSON.parse(redirect); // 将字符串解析为对象
          router.push(route); // 使用完整的路由对象
          sessionStorage.removeItem('redirectRoute');
          return;
        }
        router.push({
          name: 'appCenter'
        });
      } else if (localState.value == 'bind' || localState.value == 'update') {
        loading.value = false;
        // 更新用户信息
      }
    } else {
      if (res.error_code == 1004) {
        loading.value = false;
        errMsg.value = res.error_message;
        errStatus.value = true;
        return;
      }

      router.push({ path: '/403' });
    }
  });
});
</script>

<template>
  <div style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center">
    <el-text v-show="loading && !errStatus">微信{{ modelStr }}中，请稍候。。。</el-text>
    <el-text v-show="!loading && !errStatus">恭喜微信{{ modelStr }}成功！请关闭此页面！</el-text>
    <el-text v-show="errStatus">微信{{ modelStr }}失败，{{ errMsg }},请先通过手机号注册账户，请关闭此页面。</el-text>
  </div>
</template>

<style scoped></style>
