<script setup lang="ts">
import Clipboard from 'clipboard';
import CryptoJS from 'crypto-js';
import { ElMessage, FormRules, FormInstance } from 'element-plus';
import { nextTick, onMounted, reactive, ref, watch } from 'vue';
import {
  api,
  bindNewPhoneApi,
  closeUser,
  getSupportArea,
  getWxConfig,
  listPointTransaction,
  refreshToken,
  resetNewEmail,
  userUpdate,
  validNewPhoneApi,
  validResetEmailCode
} from '@/api/user-center';
import GeneralConfig from '@/components/user-center/GeneralConfig.vue';
import SystemConfig from '@/components/user-center/SystemConfig.vue';
import UserInviteDialog from '@/components/user-center/UserInviteDialog.vue';
import router from '@/router';
import { useUserInfoStore } from '@/stores/user-info-store';
import { IPointTransaction, IUsers } from '@/types/user-center';

const props = defineProps({
  // 是否显示用户信息
  tab: {
    type: String,
    default: 'base'
  }
});
const currentTab = ref('base');
const userInfoStore = useUserInfoStore();

const phoneView = ref(false);
const resetWidth = ref('50%');
const localUserInfo = reactive({
  user_nick_name: '',
  user_email: '',
  password: '',
  password2: '',
  user_valid_code: '',
  user_phone: '',
  user_phone_code: '',
  user_name: '',
  user_company: '',
  user_department: '',
  user_position: '',
  user_area: '',
  expire_time: ''
});
const localUpdateStatus = reactive({
  user_nick_name: false,
  user_email: false,
  close_account: false,
  password: false,
  phone: false,
  user_name: false,
  user_company: false,
  user_department: false,
  user_position: false,
  user_area: false,
  user_wx: false,
  expire_time: false
});
const nickNameRef = ref(null);
// 邮箱
const emailBindFormRef = ref();
const emailBindRules = reactive<FormRules<typeof emailBindForm>>({
  user_email: [{ validator: validUserAccount, trigger: 'blur' }],
  user_email_code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { pattern: /^\d{6}$/, message: '请输入正确的验证码', trigger: 'blur' }
  ]
});
const emailBindForm = reactive({
  user_email: '',
  user_email_code: ''
});
const bindTextCodeStatus = ref(true);
const bindTextCodeTime = ref(60);
// 密码
const passwordRules = reactive<FormRules>({
  password: [
    { trigger: 'blur', required: true, message: '请输入密码' },
    { trigger: 'blur', min: 6, max: 200, message: '长度请保持在6-200之间' },
    { validator: validatePass1, trigger: 'blur' }
  ],
  password2: [
    { trigger: 'blur', required: true, message: '请输入密码' },
    { trigger: 'blur', min: 6, max: 200, message: '长度请保持在6-200之间' },
    { validator: validatePass2, trigger: 'blur' }
  ]
});
const resetFormRef = ref<FormInstance>();
// 手机
const phoneBindFormRef = ref();
const phoneBindRules = reactive<FormRules>({
  user_phone: [{ validator: validUserAccount, trigger: 'blur' }],
  user_phone_code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { pattern: /^\d{6}$/, message: '请输入正确的验证码', trigger: 'blur' }
  ]
});
const bindTextCodeStatusPhone = ref(true);
const bindTextCodeTimePhone = ref(60);
const showInviteDialogFlag = ref(false);
// 个人积分账户
const showAccountTransaction = ref(false);
const accountTransactionLoading = ref(false);
const accountTransactionData = ref<IPointTransaction[]>([]);
const currentPageNum = ref(1);
const currentPageSize = ref(10);
const currentTransactionCnt = ref(0);
// 企业信息
const nameRef = ref(null);
const companyRef = ref(null);
const departmentRef = ref(null);
const positionRef = ref(null);
const areaOptions = ref([]);
const shortcuts = [
  {
    text: '一周',
    value: () => {
      const date = new Date();
      date.setDate(date.getDate() + 7);
      return date;
    }
  },
  {
    text: '一个月',
    value: () => {
      const date = new Date();
      date.setMonth(date.getMonth() + 1);
      return date;
    }
  },
  {
    text: '一个季度',
    value: () => {
      const date = new Date();
      date.setMonth(date.getMonth() + 3);
      return date;
    }
  },
  {
    text: '一年',
    value: () => {
      const date = new Date();
      date.setFullYear(date.getFullYear() + 1);
      return date;
    }
  }
];
function changePhoneView() {
  if (window.innerWidth < 768) {
    phoneView.value = true;
    resetWidth.value = '90%';
  } else {
    phoneView.value = false;
    resetWidth.value = '50%';
  }
}
async function handleTabChange(tab: any) {
  await router.replace({ query: { tab: tab } });
}
function logOut() {
  userInfoStore.$reset();
  router.push({ name: 'login' });
}
async function closeUserAccount() {
  let res = await closeUser({});
  if (!res.error_status) {
    ElMessage.success({
      message: '注销成功',
      duration: 1000
    });
    logOut();
  }
}
function beginUpdateNickName() {
  localUpdateStatus.user_nick_name = true;
  localUserInfo.user_nick_name = userInfoStore.userInfo.user_nick_name;
  nextTick(() => {
    nickNameRef.value.focus();
  });
}
async function updateUserNickName() {
  if (localUserInfo.user_nick_name === userInfoStore.userInfo.user_nick_name) {
    localUpdateStatus.user_nick_name = false;
    return;
  }
  let res = await userUpdate({
    user_nick_name: localUserInfo.user_nick_name
  });
  if (!res.error_status) {
    userInfoStore.updateUserInfo(res.result);
    localUpdateStatus.user_nick_name = false;
    ElMessage({
      message: '昵称修改成功',
      type: 'success',
      duration: 3000
    });
  }
}
function beforeAvatarUpload(file: File) {
  const isLt5M = file.size / 1024 / 1024 < 5;

  if (!isLt5M) {
    ElMessage.error('上传头像图片大小不能超过 5MB!');
  }
  return isLt5M;
}
async function handleAvatarUploadSuccess(res: any) {
  if (!res.error_status) {
    userInfoStore.updateUserInfo({
      user_avatar: res.result.user_avatar
    } as IUsers);
    ElMessage.success('上传成功');
  }
}
async function sendBindCode() {
  if (!bindTextCodeStatus.value) {
    // console.log('正在发送中')
    return;
  }
  // 校验账号格式
  let accountValidRes = await emailBindFormRef.value?.validateField('user_email');
  if (!accountValidRes) {
    return;
  }
  // 发送验证码
  let data = {
    new_email: emailBindForm.user_email
  };
  let res = await resetNewEmail(data);
  if (!res.error_status) {
    bindTextCodeStatus.value = false;
    ElMessage.success({
      message: '发送成功',
      duration: 1000
    });
    let timer = setInterval(() => {
      bindTextCodeTime.value--;
      if (bindTextCodeTime.value === 0) {
        bindTextCodeStatus.value = true;
        bindTextCodeTime.value = 60;
        clearInterval(timer);
      }
    }, 1000);
  }
}
async function bindNewEmail() {
  let res = await validResetEmailCode({
    new_email: emailBindForm.user_email,
    code: emailBindForm.user_email_code
  });
  if (!res.error_status) {
    ElMessage.success({
      message: '绑定成功',
      duration: 1000
    });
    localUpdateStatus.user_email = false;
    userInfoStore.updateUserInfo({ user_email: emailBindForm.user_email } as IUsers);
  }
}
function validatePass1(rule: any, value: any, callback: any) {
  if (value.includes(' ')) {
    callback(new Error('密码中请勿包含空格!'));
  }
  callback();
}
function validatePass2(rule: any, value: any, callback: any) {
  if (value !== localUserInfo.password) {
    callback(new Error('请确认两次输入密码一致！'));
  }
  callback();
}
async function resetUserPassword() {
  const validRes = await resetFormRef.value.validate();
  if (!validRes) {
    return;
  }
  let res = await userUpdate({
    user_password: CryptoJS.SHA256(localUserInfo.password.trim()).toString()
  });
  if (!res.error_status) {
    ElMessage({
      message: '密码修改成功，请重新登陆！',
      type: 'success',
      duration: 3000
    });
    logOut();
  }
}
function validUserAccount(rule: any, value: any, callback: any) {
  const phonePattern = /^1[3456789]\d{9}$/;
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!value) {
    return callback(new Error('请输入手机号或者邮箱'));
  }
  if (phonePattern.test(value) || emailPattern.test(value)) {
    callback();
  } else {
    callback(new Error('请输入正确的手机号或者邮箱'));
  }
}
async function sendBindCodePhone() {
  if (!bindTextCodeStatusPhone.value) {
    // console.log('正在发送中')
    return;
  }
  // 校验账号格式
  let accountValidRes = await phoneBindFormRef.value?.validateField('user_phone');
  if (!accountValidRes) {
    return;
  }
  // 发送验证码
  let data = {
    new_phone: localUserInfo.user_phone
  };
  let res = await bindNewPhoneApi(data);
  if (!res.error_status) {
    bindTextCodeStatusPhone.value = false;
    ElMessage.success({
      message: '发送成功',
      duration: 1000
    });
    let timer = setInterval(() => {
      bindTextCodeTimePhone.value--;
      if (bindTextCodeTimePhone.value === 0) {
        bindTextCodeStatusPhone.value = true;
        bindTextCodeTimePhone.value = 60;
        clearInterval(timer);
      }
    }, 1000);
  }
}
async function bindNewPhone() {
  const validRes = await phoneBindFormRef.value?.validate();
  if (!validRes) {
    return;
  }
  let res = await validNewPhoneApi({
    new_phone: localUserInfo.user_phone,
    code: localUserInfo.user_phone_code
  });
  if (!res.error_status) {
    ElMessage.success({
      message: '绑定成功',
      duration: 1000
    });
    localUpdateStatus.phone = false;
    userInfoStore.updateUserInfo({ user_phone: localUserInfo.user_phone } as IUsers);
  }
}
async function showAccountTransactionDialog() {
  showAccountTransaction.value = true;
  accountTransactionLoading.value = true;
  const res = await listPointTransaction({
    page_num: currentPageNum.value,
    page_size: currentPageSize.value
  });
  if (!res.error_status) {
    accountTransactionData.value = res.result.data;
    currentTransactionCnt.value = res.result.total;
  }
  accountTransactionLoading.value = false;
}
async function handleCurrentChange(val: number) {
  currentPageNum.value = val;
  showAccountTransactionDialog();
}
async function handleSizeChange(val: number) {
  currentPageSize.value = val;
  showAccountTransactionDialog();
}
function beginUpdateName() {
  localUpdateStatus.user_name = true;
  localUserInfo.user_name = userInfoStore.userInfo.user_name;
  nextTick(() => {
    nameRef.value.focus();
  });
}
async function updateUserName() {
  if (localUserInfo.user_name === userInfoStore.userInfo.user_name) {
    localUpdateStatus.user_name = false;
    return;
  }
  let res = await userUpdate({
    user_name: localUserInfo.user_name
  });
  if (!res.error_status) {
    userInfoStore.updateUserInfo({ user_name: localUserInfo.user_name } as IUsers);
    localUpdateStatus.user_name = false;
    ElMessage({
      message: '姓名修改成功',
      type: 'success',
      duration: 3000
    });
  }
}
function beginUpdateCompany() {
  localUpdateStatus.user_company = true;
  localUserInfo.user_company = userInfoStore.userInfo.user_company;
  nextTick(() => {
    companyRef.value.focus();
  });
}
async function updateUserCompany() {
  if (localUserInfo.user_company === userInfoStore.userInfo.user_company) {
    localUpdateStatus.user_company = false;
    return;
  }
  let res = await userUpdate({
    user_company: localUserInfo.user_company
  });
  if (!res.error_status) {
    userInfoStore.updateUserInfo({ user_company: localUserInfo.user_company } as IUsers);
    localUpdateStatus.user_company = false;
    ElMessage({
      message: '企业修改成功',
      type: 'success',
      duration: 3000
    });
  }
}
function beginUpdateDepartment() {
  localUpdateStatus.user_department = true;
  localUserInfo.user_department = userInfoStore.userInfo.user_department;
  nextTick(() => {
    departmentRef.value.focus();
  });
}
async function updateUserDepartment() {
  if (localUserInfo.user_department === userInfoStore.userInfo.user_department) {
    localUpdateStatus.user_department = false;
    return;
  }
  let res = await userUpdate({
    user_department: localUserInfo.user_department
  });
  if (!res.error_status) {
    userInfoStore.updateUserInfo({ user_department: localUserInfo.user_department } as IUsers);
    localUpdateStatus.user_department = false;
    ElMessage({
      message: '部门修改成功',
      type: 'success',
      duration: 3000
    });
  }
}
function beginUpdatePosition() {
  localUpdateStatus.user_position = true;
  localUserInfo.user_position = userInfoStore.userInfo.user_position;
  nextTick(() => {
    positionRef.value.focus();
  });
}
async function updateUserPosition() {
  if (localUserInfo.user_position === userInfoStore.userInfo.user_position) {
    localUpdateStatus.user_position = false;
    return;
  }
  let res = await userUpdate({
    user_position: localUserInfo.user_position
  });
  if (!res.error_status) {
    userInfoStore.updateUserInfo({ user_position: localUserInfo.user_position } as IUsers);
    localUpdateStatus.user_position = false;
    ElMessage({
      message: '职位修改成功',
      type: 'success',
      duration: 3000
    });
  }
}
async function beginUpdateArea() {
  localUpdateStatus.user_area = true;
  localUserInfo.user_area = userInfoStore.userInfo.user_area;
  let res = await getSupportArea({});
  if (res.error_status) {
    return;
  }
  areaOptions.value = res.result;
}
async function updateUserArea() {
  if (localUserInfo.user_area === userInfoStore.userInfo.user_area) {
    localUpdateStatus.user_area = false;
    return;
  }
  let res = await userUpdate({
    user_area: localUserInfo.user_area
  });
  if (!res.error_status) {
    userInfoStore.updateUserInfo({ user_area: localUserInfo.user_area } as IUsers);
    localUpdateStatus.user_area = false;
    ElMessage({
      message: '区域修改成功',
      type: 'success',
      duration: 3000
    });
  }
}
function copyToken() {
  // 复制到剪贴板
  Clipboard.copy(userInfoStore.token);
  ElMessage({
    message: 'API-KEY已复制到剪贴板',
    type: 'success',
    duration: 3000
  });
}
function beginUpdateExpireTime() {
  localUpdateStatus.expire_time = true;
  localUserInfo.expire_time = userInfoStore.expireTime;
}
async function refreshUserToken() {
  const params = {
    expire_time: localUserInfo.expire_time
  };
  let res = await refreshToken(params);
  if (!res.error_status) {
    userInfoStore.expireTime = res.result.expire_time;
    userInfoStore.token = res.result.token;
    localUpdateStatus.expire_time = false;
    ElMessage({
      message: '失效时间刷新成功',
      type: 'success',
      duration: 3000
    });
  }
}
async function beginBindWx() {
  localUpdateStatus.user_wx = true;
  const script = document.createElement('script');
  script.src = 'https://res.wx.qq.com/connect/zh_CN/htmledition/js/wxLogin.js';
  script.onload = () => initWxBind(); // 确保脚本加载完毕后再初始化微信登录
  document.body.appendChild(script);
}
async function initWxBind() {
  const wxConfig = await getWxConfig({
    domain: window.location.hostname
  });
  if (wxConfig.error_status || !wxConfig.result?.wx_app_id) {
    return;
  }
  let redirectUrl = window.location.protocol + '//' + window.location.hostname + '/login/wx_login';
  // @ts-ignore
  if (typeof WxLogin !== 'undefined') {
    new WxLogin({
      self_redirect: false,
      id: 'wx_login_container',
      appid: wxConfig.result?.wx_app_id,
      scope: 'snsapi_login',
      redirect_uri: encodeURIComponent(redirectUrl),
      state: 'bind',
      style: 'black',
      href: 'data:text/css;base64,LmltcG93ZXJCb3gge3dpZHRoOiAxMjhweH0NCi5pbXBvd2VyQm94IC5xcmNvZGUge3dpZHRoOiAxMjNweDt9DQouaW1wb3dlckJveCAudGl0bGUge2Rpc3BsYXk6IG5vbmV9DQouaW1wb3dlckJveCAuaW5mbyB7ZGlzcGxheTogbm9uZX0NCi5pbXBvd2VyQm94IC53cnBfY29kZSB7d2lkdGg6IDEyOHB4fQ0KDQoNCg=='
    });
    let container = document.getElementById('wx_login_container');
    const iframe = container.querySelector('iframe');
    iframe.width = '128px';
    iframe.height = '140px';
  }
}

watch(
  () => props.tab,
  newVal => {
    if (newVal != currentTab.value && newVal) {
      currentTab.value = newVal;
    }
  },
  { immediate: true }
);
onMounted(async () => {
  Object.assign(localUserInfo, userInfoStore.userInfo);
  areaOptions.value = (await getSupportArea({})).result;
  for (let area of areaOptions.value) {
    if (area.id === userInfoStore.userInfo.user_area) {
      localUserInfo.user_area = area;
      break;
    }
  }
  changePhoneView();
});
</script>

<template>
  <el-container>
    <el-main>
      <el-tabs v-model="currentTab" tab-position="left" @tab-change="handleTabChange">
        <el-tab-pane name="base" label="基本信息">
          <el-scrollbar>
            <div class="user_info_main">
              <div class="user_info_box">
                <el-descriptions title="基础信息" border>
                  <el-descriptions-item label="账号ID">
                    <el-text>
                      {{ ('' + userInfoStore.userInfo.user_id).padStart(9, '0') }}
                    </el-text>
                  </el-descriptions-item>
                  <el-descriptions-item label="账号类型">
                    <div style="display: flex; gap: 4px">
                      <el-text>
                        {{ userInfoStore.userInfo?.user_account_type }}
                      </el-text>
                      <el-image
                        v-if="userInfoStore.userInfo.user_account_type == '企业账号'"
                        src="/images/certification.svg"
                        style="width: 18px; height: 18px"
                      />
                    </div>
                  </el-descriptions-item>
                  <el-descriptions-item label="注册时间">
                    <el-text>
                      {{ userInfoStore.userInfo.create_time }}
                    </el-text>
                  </el-descriptions-item>
                  <el-descriptions-item label="账户ID">
                    <el-text>
                      {{ userInfoStore.userInfo?.user_point_account?.account_id }}
                    </el-text>
                  </el-descriptions-item>
                  <el-descriptions-item label="角色" class-name="">
                    <div class="role-area">
                      <el-tag v-for="role in userInfoStore.userInfo.user_role" :key="role">
                        {{ userInfoStore.translateUserRole(role) }}
                      </el-tag>
                    </div>
                  </el-descriptions-item>
                </el-descriptions>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 头像 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="3">
                    <div class="std-middle-box">
                      <el-avatar
                        v-if="userInfoStore.userInfo?.user_avatar"
                        :src="userInfoStore.userInfo?.user_avatar"
                        class="assistant-avatar"
                      />
                      <el-avatar v-else style="background: #d1e9ff">
                        <el-text style="font-weight: 600; color: #1570ef">
                          {{ userInfoStore.userInfo?.user_nick_name_py }}
                        </el-text>
                      </el-avatar>
                    </div>
                  </el-col>
                  <el-col :span="9">
                    <div style="margin-left: 12px">
                      <el-upload
                        drag
                        :show-file-list="false"
                        accept=".png, .jpg, .jpeg, .svg, .gif, .bmp, .webp"
                        :before-upload="beforeAvatarUpload"
                        :action="api.user_avatar_update"
                        :on-success="handleAvatarUploadSuccess"
                        style=""
                        name="avatar"
                        :headers="userInfoStore.userHeader"
                      >
                        <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />

                        <div class="el-upload__text"><em>点击上传</em> <br /></div>
                      </el-upload>
                    </div>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 昵称 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12" style="flex-direction: row">
                    <div v-if="localUpdateStatus.user_nick_name">
                      <el-input
                        ref="nickNameRef"
                        v-model="localUserInfo.user_nick_name"
                        @change="updateUserNickName"
                        @blur="localUpdateStatus.user_nick_name = false"
                      />
                    </div>
                    <div v-else class="user-info-meta-value">
                      <el-text>
                        {{ userInfoStore.userInfo?.user_nick_name }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="!localUpdateStatus.user_nick_name"
                      text
                      style="margin-left: 12px"
                      @click="beginUpdateNickName"
                    >
                      <el-text class="button-text"> 修改 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 邮箱 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="user-info-meta-value">
                      <el-text>
                        {{ userInfoStore.userInfo.user_email }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="
                        !localUpdateStatus.user_email &&
                        userInfoStore.userInfo?.user_account_type == '个人账号' &&
                        !userInfoStore.userInfo.user_email
                      "
                      text
                      style="margin-left: 12px"
                      @click="localUpdateStatus.user_email = true"
                    >
                      <el-text class="button-text"> 绑定 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 手机 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="user-info-meta-value">
                      <el-text>
                        {{ userInfoStore.userInfo?.user_phone }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="!localUpdateStatus.phone && !userInfoStore.userInfo.user_phone"
                      text
                      style="margin-left: 12px"
                      @click="localUpdateStatus.phone = true"
                    >
                      <el-text class="button-text"> 绑定 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 微信 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="user-info-meta-value">
                      <el-text>
                        {{ userInfoStore.userInfo?.user_wx_nickname }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="!localUpdateStatus.user_wx && !userInfoStore.userInfo.user_wx_union_id"
                      text
                      style="margin-left: 12px"
                      @click="beginBindWx"
                    >
                      <el-text class="button-text"> 绑定 </el-text>
                    </el-button>
                  </el-col>
                </el-row>

                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 密码 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="user-info-meta-value">
                      <el-text> ***************** </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="!localUpdateStatus.password"
                      text
                      style="margin-left: 12px"
                      @click="localUpdateStatus.password = true"
                    >
                      <el-text class="button-text"> 修改 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 邀请码 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="user-info-meta-value">
                      <el-text>
                        {{ userInfoStore.userInfo?.user_invite_code }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button text style="margin-left: 12px" @click="showInviteDialogFlag = true">
                      <el-text class="button-text"> 查看 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 账户余额 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="user-info-meta-value">
                      <el-text>
                        {{ userInfoStore.userInfo?.user_point_account?.balance }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button text style="margin-left: 12px" @click="showAccountTransactionDialog">
                      <el-text class="button-text"> 查看 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> API-KEY </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="user-info-meta-value">
                      <el-text truncated>
                        {{ userInfoStore.token }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button text style="margin-left: 12px" @click="copyToken">
                      <el-text class="button-text"> 复制 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 失效时间 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="user-info-meta-value">
                      <el-text>
                        {{ userInfoStore.expireTime }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button text style="margin-left: 12px" @click="beginUpdateExpireTime">
                      <el-text class="button-text"> 刷新 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6" />
                  <el-col :span="12">
                    <el-button type="primary" plain style="height: 35px" @click="logOut()"> 退出登录 </el-button>
                    <el-button type="danger" plain style="height: 35px" @click="localUpdateStatus.close_account = true">
                      注销账号
                    </el-button>
                  </el-col>
                </el-row>
              </div>
            </div>
          </el-scrollbar>
        </el-tab-pane>
        <el-tab-pane name="setting" label="通用设置">
          <GeneralConfig />
        </el-tab-pane>
        <el-tab-pane name="company" label="企业信息">
          <el-scrollbar>
            <div class="user_info_main">
              <div class="user_info_box">
                <el-row v-if="userInfoStore.userInfo.user_account_type == '企业账号'">
                  <el-col :span="24">
                    <el-divider>
                      <el-text> 以下信息如需修改，请联系企业管理员 </el-text>
                    </el-divider>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 姓名 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12" style="flex-direction: row">
                    <div v-if="localUpdateStatus.user_name">
                      <el-input
                        ref="nameRef"
                        v-model="localUserInfo.user_name"
                        @change="updateUserName"
                        @blur="localUpdateStatus.user_name = false"
                      />
                    </div>
                    <div
                      v-else
                      class="user-info-meta-value"
                      :class="{
                        'user-info-meta-value-disabled': userInfoStore.userInfo?.user_account_type == '企业账号'
                      }"
                    >
                      <el-text>
                        {{ userInfoStore.userInfo?.user_name }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="!localUpdateStatus.user_name && userInfoStore.userInfo?.user_account_type != '企业账号'"
                      text
                      style="margin-left: 12px"
                      @click="beginUpdateName"
                    >
                      <el-text class="button-text"> 修改 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 企业 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12" style="flex-direction: row">
                    <div v-if="localUpdateStatus.user_company">
                      <el-input
                        ref="companyRef"
                        v-model="localUserInfo.user_company"
                        @change="updateUserCompany"
                        @blur="localUpdateStatus.user_company = false"
                      />
                    </div>
                    <div
                      v-else
                      class="user-info-meta-value"
                      :class="{
                        'user-info-meta-value-disabled': userInfoStore.userInfo?.user_account_type == '企业账号'
                      }"
                    >
                      <el-text>
                        {{ userInfoStore.userInfo?.user_company }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="!localUpdateStatus.user_company && userInfoStore.userInfo?.user_account_type != '企业账号'"
                      text
                      style="margin-left: 12px"
                      @click="beginUpdateCompany"
                    >
                      <el-text class="button-text"> 修改 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 部门 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12" style="flex-direction: row">
                    <div v-if="localUpdateStatus.user_department">
                      <el-input
                        ref="departmentRef"
                        v-model="localUserInfo.user_department"
                        @change="updateUserDepartment"
                        @blur="localUpdateStatus.user_department = false"
                      />
                    </div>
                    <div
                      v-else
                      class="user-info-meta-value"
                      :class="{
                        'user-info-meta-value-disabled': userInfoStore.userInfo?.user_account_type == '企业账号'
                      }"
                    >
                      <el-text>
                        {{ userInfoStore.userInfo?.user_department }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="
                        !localUpdateStatus.user_department && userInfoStore.userInfo?.user_account_type != '企业账号'
                      "
                      text
                      style="margin-left: 12px"
                      @click="beginUpdateDepartment"
                    >
                      <el-text class="button-text"> 修改 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 职位 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12" style="flex-direction: row">
                    <div v-if="localUpdateStatus.user_position">
                      <el-input
                        ref="positionRef"
                        v-model="localUserInfo.user_position"
                        @change="updateUserPosition"
                        @blur="localUpdateStatus.user_position = false"
                      />
                    </div>
                    <div
                      v-else
                      class="user-info-meta-value"
                      :class="{
                        'user-info-meta-value-disabled': userInfoStore.userInfo?.user_account_type == '企业账号'
                      }"
                    >
                      <el-text>
                        {{ userInfoStore.userInfo?.user_position }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="!localUpdateStatus.user_position && userInfoStore.userInfo?.user_account_type == '个人账号'"
                      text
                      style="margin-left: 12px"
                      @click="beginUpdatePosition"
                    >
                      <el-text class="button-text"> 修改 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <div class="user-info-meta-label">
                      <el-text> 区域 </el-text>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div v-if="localUpdateStatus.user_area">
                      <el-cascader
                        v-model="localUserInfo.user_area"
                        clearable
                        :show-all-levels="false"
                        placeholder="选择国家/地区"
                        :options="areaOptions"
                        filterable
                        style="width: 100%"
                        @change="updateUserArea"
                      />
                    </div>
                    <div
                      v-else
                      class="user-info-meta-value"
                      :class="{
                        'user-info-meta-value-disabled': userInfoStore.userInfo?.user_account_type == '企业账号'
                      }"
                    >
                      <el-text>
                        {{ userInfoStore.userInfo?.user_area }}
                      </el-text>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      v-if="!localUpdateStatus.user_area && userInfoStore.userInfo?.user_account_type == '个人账号'"
                      text
                      style="margin-left: 12px"
                      @click="beginUpdateArea"
                    >
                      <el-text class="button-text"> 修改 </el-text>
                    </el-button>
                  </el-col>
                </el-row>
              </div>
            </div>
          </el-scrollbar>
        </el-tab-pane>
        <el-tab-pane
          v-if="userInfoStore.userInfo?.user_role?.includes('next_console_admin')"
          name="platform"
          label="系统设置"
        >
          <SystemConfig />
        </el-tab-pane>
      </el-tabs>
    </el-main>
  </el-container>

  <el-footer height="20px" />

  <el-dialog v-model="localUpdateStatus.password" :width="resetWidth" top="35vh" style="max-width: 500px">
    <el-form
      id="reset-form-inner"
      ref="resetFormRef"
      label-position="top"
      style="width: 100%"
      :model="localUserInfo"
      status-icon
      :rules="passwordRules"
    >
      <el-form-item label="新密码" prop="password">
        <el-input v-model="localUserInfo.password" placeholder="请输入新密码" type="password" show-password />
      </el-form-item>
      <el-form-item label="确认密码" prop="password2">
        <el-input v-model="localUserInfo.password2" placeholder="请确认新密码" type="password" show-password />
      </el-form-item>
      <el-form-item>
        <el-button id="reset-button" @click="resetUserPassword">
          <div class="std-middle-box">
            <el-text style="font-size: 14px; font-weight: 600; color: white; line-height: 20px"> 重置密码 </el-text>
          </div>
          <div class="std-middle-box" style="margin-left: 6px">
            <el-image src="/images/login_icon.svg" />
          </div>
        </el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog
    v-model="localUpdateStatus.user_email"
    :width="resetWidth"
    title="绑定邮箱"
    draggable
    top="35vh"
    style="max-width: 500px"
  >
    <el-form ref="emailBindFormRef" :model="emailBindForm" :rules="emailBindRules">
      <el-form-item prop="user_email">
        <el-input v-model="emailBindForm.user_email" placeholder="请输入邮箱" />
      </el-form-item>
      <el-form-item prop="user_email_code">
        <el-input v-model="emailBindForm.user_email_code" placeholder="请输入验证码">
          <template #suffix>
            <el-button v-if="bindTextCodeStatus" text type="primary" @click="sendBindCode"> 获取验证码 </el-button>
            <el-button v-else text disabled> {{ bindTextCodeTime }}s后再次获取 </el-button>
          </template>
        </el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="std-middle-box">
        <el-button @click="localUpdateStatus.user_email = false">取 消</el-button>
        <el-button type="primary" @click="bindNewEmail">确 定</el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog
    v-model="localUpdateStatus.phone"
    :width="resetWidth"
    title="绑定手机"
    draggable
    top="35vh"
    style="max-width: 500px"
  >
    <el-form ref="phoneBindFormRef" :model="localUserInfo" :rules="phoneBindRules">
      <el-form-item prop="user_phone">
        <el-input v-model="localUserInfo.user_phone" placeholder="请输入手机" />
      </el-form-item>
      <el-form-item prop="user_phone_code">
        <el-input v-model="localUserInfo.user_phone_code" placeholder="请输入验证码">
          <template #suffix>
            <el-button v-if="bindTextCodeStatusPhone" text type="primary" @click="sendBindCodePhone">
              获取验证码
            </el-button>
            <el-button v-else text disabled> {{ bindTextCodeTimePhone }}s后再次获取 </el-button>
          </template>
        </el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="std-middle-box">
        <el-button @click="localUpdateStatus.phone = false">取 消</el-button>
        <el-button type="primary" @click="bindNewPhone">确 定</el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog
    v-model="localUpdateStatus.user_wx"
    title="绑定微信"
    :width="resetWidth"
    draggable
    top="35vh"
    style="max-width: 500px"
  >
    <div class="std-middle-box" style="flex-direction: column">
      <div id="wx_login_container" />
      <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 12px">
        <div style="display: flex; flex-direction: row; align-items: center; justify-content: center">
          <el-image src="/images/wx_logo.svg" style="width: 20px; height: 20px" />
        </div>
        <div>
          <el-text style="font-size: 15px; font-weight: 600; color: #344054"> 微信扫一扫 </el-text>
        </div>
      </div>
    </div>
  </el-dialog>
  <el-dialog
    v-model="localUpdateStatus.close_account"
    title="注销账号"
    :width="resetWidth"
    draggable
    top="35vh"
    style="max-width: 500px"
  >
    <div class="std-middle-box" style="flex-direction: column">
      <div>
        <el-result
          title="注销账号"
          sub-title="注销账号后，您的账号将无法再次登录，且无法找回，请谨慎操作"
          icon="warning"
        />
      </div>

      <div>
        <el-button text type="danger" @click="closeUserAccount">确认注销</el-button>
        <el-button text type="primary" @click="localUpdateStatus.close_account = false">我再想想</el-button>
      </div>
    </div>
  </el-dialog>
  <UserInviteDialog :mode="showInviteDialogFlag" @update:mode="args => (showInviteDialogFlag = args)" />
  <el-dialog v-model="showAccountTransaction" :width="resetWidth" title="账户交易记录" draggable top="35vh">
    <el-table
      v-loading="accountTransactionLoading"
      :data="accountTransactionData"
      border
      style="width: 100%"
      element-loading-text="加载中"
    >
      <el-table-column prop="transaction_id" label="交易ID" width="180" />
      <el-table-column prop="create_time" label="发生时间" width="180" />
      <el-table-column prop="transaction_type" label="类型" width="180" />
      <el-table-column prop="transaction_amount" label="金额" width="180" />
      <el-table-column prop="transaction_desc" label="描述" width="180" />
      <el-table-column prop="order_id" label="订单ID" width="180" />
    </el-table>
    <el-pagination
      :page-sizes="[10, 20, 50, 100]"
      size="small"
      :page-size="currentPageSize"
      :current-page="currentPageNum"
      layout="prev, pager, next, jumper, ->, total"
      :total="currentTransactionCnt"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
    <template #footer>
      <div class="std-middle-box">
        <el-button @click="showAccountTransaction = false">确 定</el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="localUpdateStatus.expire_time" title="刷新API-KEY" draggable top="35vh" style="max-width: 500px">
    <div class="std-middle-box" style="flex-direction: column; gap: 12px">
      <el-form-item label-position="left" label="失效日期">
        <el-date-picker
          v-model="localUserInfo.expire_time"
          type="datetime"
          placeholder="选择失效日期"
          :shortcuts="shortcuts"
          format="YYYY-MM-DD HH:mm:ss"
          value-format="YYYY-MM-DD HH:mm:ss"
          date-format="MMM DD, YYYY"
          time-format="HH:mm"
        />
      </el-form-item>
      <div>
        <el-text> 确认刷新API-KEY？ </el-text>
      </div>
      <div>
        <el-button @click="localUpdateStatus.expire_time = false">取 消</el-button>
        <el-button type="primary" @click="refreshUserToken">确 定</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
.user_info_main {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
  height: calc(100vh - 40px);
  gap: 12px;
}
.user_info_box {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 900px;
  gap: 24px;
}
.std-middle-box {
  display: flex;

  justify-content: center;
  align-items: center;
  height: 100%;
  gap: 12px;
}
.user-info-meta {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
}
.user-info-meta-label {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  min-width: 80px;
  max-width: 160px;
  height: 100%;
}
.user_info_headers {
  display: flex;
  justify-content: flex-start;
  align-items: flex-end;
  gap: 12px;
  width: 100%;
}
.user-info-meta-value {
  display: flex;
  align-items: center;
  border: 1px solid #d0d5dd;
  width: calc(100% - 24px);
  max-width: 420px;
  min-height: 16px;
  box-shadow: 0 1px 2px 0 #1018280d;
  border-radius: 8px;
  padding: 8px 12px;
  gap: 6px;
  margin-left: 6px;
}
.button-text {
  color: #175cd3;
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  margin-left: 12px;
}
.user-info-meta-value-disabled {
  background: #f2f4f7;
  color: #b0bac5;
}
.invite-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  height: 100%;
  align-items: center;
}
#reset-button {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-direction: row;
  width: 100%;
  background-color: #1570ef;
  border-radius: 8px;
}
.form-item-box {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  padding: 24px;
  background: #ffffff;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease-in-out;
}

.assistant-avatar {
  width: 148px;
  height: 148px;
  border-radius: 40px;
}
.role-area {
  display: flex;
  gap: 4px;
}
@media (max-width: 768px) {
  .user_info_main {
    gap: 0;
  }
  .user_info_box {
    width: 100%;
    max-width: 100%;
    max-height: calc(100vh - 20px);
    margin-top: 20px;
    padding: 20px;
  }
  .user_info_headers {
    flex-direction: column;
    gap: 0;
    align-items: start;
  }

  .user-info-meta-label {
    justify-content: flex-start;
  }
  .user-info-meta-value {
    max-width: calc(100% - 48px);
    overflow: auto;
  }

  .user-info-meta {
    width: calc(100% - 24px);
  }
}
</style>
