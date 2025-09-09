<script setup lang="ts">
import CryptoJS from 'crypto-js';
import { ElMessage, FormInstance, FormRules } from 'element-plus';
import { onMounted, reactive, ref, computed } from 'vue';
import { generateTextCode, getWxConfig, loginByCode, loginByPassword } from '@/api/user-center';
import HomeFooter from '@/components/user-center/HomeFooter.vue';
import router from '@/router';
import { useUserConfigStore } from '@/stores/userConfigStore';
import { useUserInfoStore } from '@/stores/userInfoStore';

const LocalLoginType = ref('code');
const nodeEnv = import.meta.env.VITE_APP_NODE_ENV;
const rules = reactive<FormRules<typeof loginForm>>({
  user_account: [{ validator: validUserAccount, trigger: 'blur' }],
  user_password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
});
const contractFormRef = ref();
const loginForm = reactive({
  user_account: '',
  user_password: '',
  session_30_flag: true
});
const loginFormValid = ref(false);
const loginFormRef = ref<FormInstance>();
const acceptContractForm = reactive({
  accept_contract: false
});
// 账号登录表单
const contractRules = reactive<FormRules>({
  accept_contract: [{ validator: acceptContractCheck, trigger: 'change' }]
});
const codeLoginFormRef = ref<FormInstance>();
const codeLoginForm = reactive({
  user_account: '',
  text_code: '',
  session_30_flag: true
});
const codeLoginRules = reactive<FormRules<typeof codeLoginForm>>({
  user_account: [{ validator: validUserAccount, trigger: 'blur' }],
  text_code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { pattern: /^\d{6}$/, message: '请输入正确的验证码', trigger: 'blur' }
  ]
});
const loginTextCodeStats = ref(true);
const loginTextCodeTime = ref(60);
const LocalInviteViewId = ref();
const inviteModel = ref(false);
const userInfoStore = useUserInfoStore();
const userConfigStore = useUserConfigStore();
function changeLoginType(type: string) {
  LocalLoginType.value = type;
  router.push({
    name: 'login',
    query: {
      login_type: type,
      invite_view_id: LocalInviteViewId.value
    }
  });
}
function acceptContractCheck(rule: any, value: any, callback: any) {
  // 必须勾选协议
  if (!value) {
    callback(new Error('请先同意并勾选协议'));
  } else {
    callback();
  }
}
async function codeLogin() {
  // 校验表单合法性
  let phoneValidRes = await codeLoginFormRef.value?.validate();
  if (!phoneValidRes) {
    return;
  }
  // 检验合同是否勾选
  let contractValidRes = await contractFormRef.value?.validate();
  if (!contractValidRes) {
    return;
  }
  let res = await loginByCode({
    user_account: codeLoginForm.user_account,
    text_code: codeLoginForm.text_code,
    session_30_flag: codeLoginForm.session_30_flag,
    invite_view_id: LocalInviteViewId.value
  });
  if (!res.error_status) {
    userInfoStore.updateUserInfo(res.result?.userinfo);
    userInfoStore.token = res.result?.token;
    userInfoStore.expireTime = res.result?.expire_time;
    // 如果有被拦截的页面，登录成功后跳转到拦截页面
    const redirect = sessionStorage.getItem('redirectRoute');
    if (redirect) {
      const route = JSON.parse(redirect); // 将字符串解析为对象
      router.push(route); // 使用完整的路由对象
      sessionStorage.removeItem('redirectRoute');
      return;
    }
    router.push({ name: 'next_console_welcome_home' });
  }
}
async function sendMsgCode() {
  if (!loginTextCodeStats.value) {
    // console.log('正在发送中')
    return;
  }
  // 校验账号格式
  let accountValidRes = await codeLoginFormRef.value?.validateField('user_account');
  if (!accountValidRes) {
    // console.log(accountValidRes)
    return;
  }
  // 发送验证码
  let data = {};
  if (codeLoginForm.user_account.includes('@')) {
    data = {
      user_email: codeLoginForm.user_account
    };
  } else {
    data = {
      user_phone: codeLoginForm.user_account
    };
  }
  let res = await generateTextCode(data);

  // 发送成功后倒计时
  if (!res.error_status) {
    loginTextCodeStats.value = false;
    ElMessage.success({
      message: '发送成功',
      duration: 1000
    });
    let time = loginTextCodeTime.value;
    let interval = setInterval(() => {
      time--;
      loginTextCodeTime.value = time;
      if (time === 0) {
        clearInterval(interval);
        loginTextCodeTime.value = 60;
        loginTextCodeStats.value = true;
      }
    }, 1000);
  }
}
async function resetPassword() {
  router.push({ name: 'reset_password' });
}
async function login() {
  loginForm.user_account = loginForm.user_account.trim();
  if (!loginFormValid.value) {
    loginFormValid.value = await loginFormRef.value?.validate();
  }
  if (!loginFormValid.value) {
    return;
  }
  // 检验合同是否勾选
  let contractValidRes = await contractFormRef.value?.validate();
  if (!contractValidRes) {
    return;
  }
  let res = await loginByPassword({
    user_account: loginForm.user_account,
    user_password: CryptoJS.SHA256(loginForm.user_password.trim()).toString(),
    session_30_flag: loginForm.session_30_flag,
    invite_view_id: LocalInviteViewId.value
  });
  if (!res.error_status) {
    userInfoStore.updateUserInfo(res.result?.userinfo);
    userInfoStore.token = res.result?.token;
    userInfoStore.expireTime = res.result?.expire_time;
    // 如果有被拦截的页面，登录成功后跳转到拦截页面
    const redirect = sessionStorage.getItem('redirectRoute');
    if (redirect) {
      const route = JSON.parse(redirect); // 将字符串解析为对象
      router.push(route); // 使用完整的路由对象
      sessionStorage.removeItem('redirectRoute');
      return;
    }
    router.push({ name: 'next_console_welcome_home' });
  }
}
async function initWxLogin() {
  // 确保 WxLogin 已经加载

  let state = 'login';
  if (LocalInviteViewId.value !== null && LocalInviteViewId.value !== undefined && LocalInviteViewId.value !== '') {
    state = 'login_' + LocalInviteViewId.value;
  }
  const wxConfig = await getWxConfig({
    domain: window.location.hostname
  });
  if (wxConfig.error_status || !wxConfig.result?.wx_app_id) {
    return;
  }
  let redirectUrl = window.location.protocol + '//' + window.location.hostname + '/login/wx_login';
  //@ts-ignore
  if (typeof WxLogin !== 'undefined') {
    //@ts-ignore
    new WxLogin({
      self_redirect: false,
      id: 'wx_login_container',
      appid: wxConfig.result?.wx_app_id,
      scope: 'snsapi_login',
      redirect_uri: encodeURIComponent(redirectUrl),
      state: state,
      style: 'black',
      href: 'data:text/css;base64,LmltcG93ZXJCb3gge3dpZHRoOiAxMjhweH0NCi5pbXBvd2VyQm94IC5xcmNvZGUge3dpZHRoOiAxMjNweDt9DQouaW1wb3dlckJveCAudGl0bGUge2Rpc3BsYXk6IG5vbmV9DQouaW1wb3dlckJveCAuaW5mbyB7ZGlzcGxheTogbm9uZX0NCi5pbXBvd2VyQm94IC53cnBfY29kZSB7d2lkdGg6IDEyOHB4fQ0KDQoNCg=='
    });
    let container = document.getElementById('wx_login_container');
    const iframe = container.querySelector('iframe');
    iframe.width = '128px';
    iframe.height = '140px';
  }
}
function validUserAccount(rule: any, value: any, callback: any) {
  const phonePattern = /^1[3456789]\d{9}$/;
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (inviteModel.value) {
    if (!value) {
      return callback(new Error('请输入手机号'));
    }
    if (phonePattern.test(value)) {
      callback();
    } else {
      callback(new Error('请输入正确的手机号'));
    }
  }
  if (!value) {
    return callback(new Error('请输入手机号或者邮箱'));
  }
  if (phonePattern.test(value) || emailPattern.test(value)) {
    callback();
  } else {
    callback(new Error('请输入正确的手机号或者邮箱'));
  }
}
const logoUrl = computed(() => getMainLogo());
function getMainLogo() {
  if (userConfigStore.systemConfig?.ops?.brand?.enable && userConfigStore.systemConfig.ops.brand.logo_full_url) {
    return userConfigStore.systemConfig.ops.brand.logo_full_url;
  }
  return '/images/logo_text.svg';
}
onMounted(async () => {
  // 动态加载 wxLogin.js 脚本
  const script = document.createElement('script');
  script.src = 'https://res.wx.qq.com/connect/zh_CN/htmledition/js/wxLogin.js';
  script.onload = () => initWxLogin(); // 确保脚本加载完毕后再初始化微信登录
  document.body.appendChild(script);
  if (nodeEnv == 'private') {
    LocalLoginType.value = 'password';
  }
});
</script>

<template>
  <el-container>
    <el-main>
      <el-scrollbar>
        <div id="login-aside-box">
          <div id="login_box">
            <div id="login_logo">
              <el-image :src="logoUrl" fit="fill" />
              <el-text style="margin-top: 16px">智能科技创造美好未来</el-text>
            </div>
            <div class="std-middle-box" style="width: 100%; gap: 16px">
              <div
                class="login-type-area"
                :class="{ 'login-type-area-active': LocalLoginType === 'code' }"
                @click="changeLoginType('code')"
              >
                <el-text class="login-type-text" :class="{ 'login-type-text-active': LocalLoginType === 'code' }">
                  验证码登录
                </el-text>
              </div>
              <div
                v-show="nodeEnv != 'private'"
                class="login-type-area"
                :class="{ 'login-type-area-active': LocalLoginType === 'qr_code' }"
                @click="changeLoginType('qr_code')"
              >
                <el-text class="login-type-text" :class="{ 'login-type-text-active': LocalLoginType === 'qr_code' }">
                  扫码登录
                </el-text>
              </div>
              <div
                class="login-type-area"
                :class="{ 'login-type-area-active': LocalLoginType === 'password' }"
                @click="changeLoginType('password')"
              >
                <el-text class="login-type-text" :class="{ 'login-type-text-active': LocalLoginType === 'password' }">
                  密码登录
                </el-text>
              </div>
            </div>
            <div v-show="LocalLoginType === 'code'" class="login_form">
              <el-form
                ref="codeLoginFormRef"
                label-position="top"
                style="width: 100%"
                :model="codeLoginForm"
                status-icon
                :rules="codeLoginRules"
                :hide-required-asterisk="true"
              >
                <el-form-item prop="user_account">
                  <el-input v-if="inviteModel" v-model="codeLoginForm.user_account" placeholder="请输入手机号" />
                  <el-input v-else v-model="codeLoginForm.user_account" placeholder="请输入手机号或者邮箱" />
                </el-form-item>
                <el-form-item prop="text_code" :show-message="false">
                  <el-input v-model="codeLoginForm.text_code" placeholder="请输入验证码">
                    <template #suffix>
                      <el-button v-if="loginTextCodeStats" text type="primary" @click="sendMsgCode">
                        获取验证码
                      </el-button>
                      <el-button v-else text disabled> {{ loginTextCodeTime }}s后再次获取 </el-button>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item>
                  <div
                    style="display: flex; flex-direction: row; align-items: center; justify-content: center; width: 95%"
                  >
                    <el-checkbox v-model="codeLoginForm.session_30_flag"> 30天内自动登录 </el-checkbox>
                  </div>
                </el-form-item>
                <el-form-item>
                  <el-button id="login-button" @click="codeLogin">
                    <div class="std-middle-box">
                      <el-text style="font-size: 14px; font-weight: 600; color: white; line-height: 20px">
                        登 录
                      </el-text>
                    </div>
                    <div class="std-middle-box" style="margin-left: 6px">
                      <el-image src="/images/login_icon.svg" />
                    </div>
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            <div v-show="LocalLoginType === 'qr_code'" class="login_form">
              <div id="wx_login_container" />
              <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 12px">
                <div style="display: flex; flex-direction: row; align-items: center; justify-content: center">
                  <el-image src="/images/wx_logo.svg" style="width: 20px; height: 20px" />
                </div>
                <div>
                  <el-text style="font-size: 15px; font-weight: 600; color: #344054"> 微信扫一扫 </el-text>
                </div>
              </div>
              <div v-if="!acceptContractForm.accept_contract" class="mask-layer">
                <el-text> 请先同意并勾选下方的用户协议和隐私政策 </el-text>
              </div>
            </div>
            <div v-show="LocalLoginType === 'password'" class="login_form">
              <el-form
                ref="loginFormRef"
                label-position="top"
                style="width: 100%"
                :model="loginForm"
                status-icon
                :rules="rules"
                :hide-required-asterisk="true"
              >
                <el-form-item prop="user_account">
                  <el-input v-model="loginForm.user_account" placeholder="输入手机或者邮箱" />
                </el-form-item>
                <el-form-item prop="user_password">
                  <el-input v-model="loginForm.user_password" show-password type="password" placeholder="输入密码" />
                </el-form-item>
                <el-form-item>
                  <div
                    style="
                      display: flex;
                      flex-direction: row;
                      align-items: center;
                      justify-content: space-between;
                      width: 95%;
                    "
                  >
                    <div>
                      <el-button text type="primary" @click="resetPassword">找回密码</el-button>
                    </div>
                    <div>
                      <el-checkbox v-model="loginForm.session_30_flag"> 30天内自动登录 </el-checkbox>
                    </div>
                  </div>
                </el-form-item>
                <el-form-item>
                  <el-button id="login-button" @click="login">
                    <div class="std-middle-box">
                      <el-text style="font-size: 14px; font-weight: 600; color: white; line-height: 20px">
                        登 录
                      </el-text>
                    </div>
                    <div class="std-middle-box" style="margin-left: 6px">
                      <el-image src="/images/login_icon.svg" />
                    </div>
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            <div class="std-middle-box std-contract-check" style="gap: 8px">
              <div class="std-middle-box">
                <el-form ref="contractFormRef" :model="acceptContractForm" :rules="contractRules">
                  <el-form-item prop="accept_contract" class="contract-check">
                    <el-checkbox v-model="acceptContractForm.accept_contract" style="height: auto" />
                  </el-form-item>
                </el-form>
              </div>

              <div>
                <el-text>我已阅读并同意图灵天问的</el-text>
                <el-link
                  type="primary"
                  underline
                  @click="
                    router.push({
                      name: 'contract'
                    })
                  "
                >
                  《用户协议》
                </el-link>
                <el-text> 和 </el-text>
                <el-link type="primary" underline @click="router.push({ name: 'privacy_policy' })">
                  《隐私政策》
                </el-link>
                <br />
                <el-text v-if="LocalLoginType != 'password'"> 新用户首次登录会自动创建账号 </el-text>
              </div>
            </div>
          </div>
        </div>
      </el-scrollbar>
    </el-main>
    <el-footer height="60px">
      <HomeFooter />
    </el-footer>
  </el-container>
</template>

<style scoped>
#login-aside-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 60px);
}
#login_box {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
  gap: 16px;
  max-width: 400px;
}
.login_form {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  height: 200px;
  position: relative;
}
#login-button {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-direction: row;
  width: 100%;
  background-color: #1570ef;
  border-radius: 8px;
}

.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}
.el-main {
  padding: 0 !important;
}
:deep(.el-input__validateIcon) {
  color: green;
}
#login_logo {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}
.login-type-area {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px;
  cursor: pointer;
  border-bottom: 2px solid white;
}
.login-type-area-active {
  border-bottom: 2px solid #175cd3;
}
.login-type-text {
  font-weight: 600;
  font-size: 14px;
  line-height: 20px;
  color: #667085;
}
.login-type-text-active {
  color: #175cd3;
}
.contract-check :deep(.el-form-item__content) {
  .el-form-item__error {
    width: 120px !important;
    margin-top: 20px;
  }
}
.mask-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8); /* 背景颜色和透明度 */
  backdrop-filter: blur(5px); /* 模糊效果 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10; /* 确保遮罩层在最上层 */
}
.std-contract-check {
  align-items: flex-start;
  :deep(.el-checkbox) {
    height: auto;
    padding-top: 4px;
  }
}
</style>
