<script setup lang="ts">
// 定义属性
import {onMounted, ref} from 'vue';
import {wx_register} from "@/api/user_center";
import {getToken, setToken} from "@/utils/auth";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus";

const props = defineProps({
  code: {
    type:  String,
    required: true,
    default: null
  },
  state: {
    type: String,
    default: true,
    required: false
  }
});
const code = ref(null);
const state = ref(null);
const model_str = ref(null);
const router = useRouter();
const loading = ref(true);
const err_status = ref(false);
const err_msg  =ref('')

onMounted(() => {
  code.value = props.code;
  state.value = props.state;
  if (state.value == "register") {
    model_str.value = "自动注册";
  } else if (state.value == 'login' || state.value.includes('login')) {
    model_str.value = '自动登录';
  }
  else if (state.value=="bind"){
    model_str.value = "自动绑定";
  }
  else if (state.value=="update"){
    model_str.value = "自动更新";
  }
  else {
    router.push({path: '/403'});
    return;
  }


  let params = {
    code: code.value,
    state: state.value
  }
  if (state.value == "bind" || state.value == "update") {
    params["token"] = getToken()
  }
  wx_register(params).then(res => {
    if (!res.error_status) {
      const { token, userinfo } = res.result;
      setToken(token);
      // setInfo(userinfo)
      ElMessage.success(model_str.value + '成功！');
      if (state.value == 'register' || state.value == 'login' || state.value.includes('login')) {
        const redirect = sessionStorage.getItem('redirectRoute');
        if (redirect) {
          const route = JSON.parse(redirect); // 将字符串解析为对象
          router.push(route); // 使用完整的路由对象
          sessionStorage.removeItem('redirectRoute');
          return;
        }
        router.push({
          name: 'next_console_welcome_home'
        });
      } else if (state.value == 'bind' || state.value == 'update') {
        loading.value = false;
        // 更新用户信息
      }
    } else {
      if (res.error_code == 1004) {
        loading.value = false;
        err_msg.value = res.error_message;
        err_status.value = true;
        return;
      }

      router.push({ path: '/403' });
    }
  });
});

</script>

<template>
<div style="width: 100%;height: 100%; display: flex;justify-content: center;align-items: center">

  <el-text v-show="loading && !err_status">微信{{model_str}}中，请稍候。。。</el-text>
  <el-text v-show="!loading && !err_status">恭喜微信{{model_str}}成功！请关闭此页面！</el-text>
  <el-text v-show="err_status">微信{{model_str}}失败，{{err_msg}},请先通过手机号注册账户，请关闭此页面。</el-text>
</div>
</template>

<style scoped>

</style>
