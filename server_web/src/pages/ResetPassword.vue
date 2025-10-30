<script setup lang="ts">
// 重置密码表单
import CryptoJS from 'crypto-js';
import { FormRules, ElMessage, FormInstance } from 'element-plus';
import { reactive, ref } from 'vue';

import { resetAccountPassword, validResetPasswordCode } from '@/api/user-center';
import ValidCode from '@/components/user-center/ValidCode.vue';
import router from '@/router';
const resetForm = reactive({
  user_account: '',
  user_valid_code: '',
  password: '',
  password2: ''
});
const resetFormRef = ref<FormInstance>();
const rules = reactive<FormRules<typeof resetForm>>({
  user_account: [{ trigger: 'blur', validator: validUserAccount }],
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
const resetFormValid = ref(false);
const beginValid = ref(false);
let countDownInterval = null;
const countDown = ref(60);
function validatePass1(rule: any, value: any, callback: any) {
  if (value.includes(' ')) {
    callback(new Error('密码中请勿包含空格!'));
  }
  callback();
}
function validatePass2(rule: any, value: any, callback: any) {
  if (value !== resetForm.password) {
    callback(new Error('请确认两次输入密码一致！'));
  }
  callback();
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
async function resendResetEmail() {
  if (countDown.value > 0) {
    return;
  }
  let res = await resetAccountPassword({
    user_account: resetForm.user_account,
    new_password: CryptoJS.SHA256(resetForm.password.trim()).toString()
  });
  if (!res.error_status) {
    ElMessage({
      message: '验证码已发送',
      type: 'success',
      duration: 3000
    });
  }
  countDown.value = 60;
  countDownStart();
}
async function sendResetEmail() {
  if (!resetFormValid.value) {
    resetFormValid.value = await resetFormRef.value?.validate();
  }
  if (!resetFormValid.value) {
    return;
  }
  // 发送重置密码验证码

  let res = await resetAccountPassword({
    user_account: resetForm.user_account,
    new_password: CryptoJS.SHA256(resetForm.password.trim()).toString()
  });
  if (!res.error_status) {
    beginValid.value = true;
    ElMessage({
      message: '验证码已发送',
      type: 'success',
      duration: 3000
    });
    countDownStart();
  }
}
async function resetPassword(code: string) {
  let res = await validResetPasswordCode({
    user_account: resetForm.user_account,
    code: code
  });
  if (!res.error_status) {
    ElMessage({
      message: '密码重置成功，请重新登录',
      type: 'success',
      duration: 3000
    });
    resetForm.user_account = '';
    resetForm.password = '';
    resetForm.password2 = '';
    resetForm.user_valid_code = '';
    beginValid.value = false;
    router.push({
      name: 'login'
    });
  }
}
function countDownStart() {
  countDownInterval = setInterval(() => {
    countDown.value -= 1;
    if (countDown.value === 0) {
      clearInterval(countDownInterval);
    }
  }, 1000);
}
</script>

<template>
  <el-container>
    <el-main>
      <el-scrollbar>
        <div id="reset-aside-box">
          <div id="reset-box">
            <div id="login_logo">
              <el-image src="/images/logo_text.svg" fit="fill" />
            </div>
            <div id="reset-form">
              <el-form
                id="reset-form-inner"
                ref="resetFormRef"
                label-position="top"
                style="width: 100%"
                :model="resetForm"
                status-icon
                :rules="rules"
                :disabled="beginValid"
              >
                <el-form-item label="账号" prop="user_account">
                  <el-input v-model="resetForm.user_account" placeholder="输入手机号或邮箱" />
                </el-form-item>
                <el-form-item label="新密码" prop="password">
                  <el-input v-model="resetForm.password" placeholder="请输入新密码" type="password" show-password />
                </el-form-item>
                <el-form-item label="确认密码" prop="password2">
                  <el-input v-model="resetForm.password2" placeholder="请确认新密码" type="password" show-password />
                </el-form-item>
                <el-form-item>
                  <el-button id="reset-button" @click="sendResetEmail">
                    <div class="std-middle-box">
                      <el-text style="font-size: 14px; font-weight: 600; color: white; line-height: 20px">
                        发送验证码
                      </el-text>
                    </div>
                    <div class="std-middle-box" style="margin-left: 6px">
                      <el-image src="/images/login_icon.svg" />
                    </div>
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            <div v-if="resetFormValid" id="reset-valid-box">
              <div v-if="resetForm.user_account.includes('@')" id="reset-code-info">
                <el-text> 我们向 </el-text>
                <el-text style="font-size: 14px; font-weight: 600; line-height: 20px; color: #101828">
                  {{ resetForm.user_account }}
                  ><br />
                  <el-text> 发送了一封含验证码的邮件，请查收并输入验证码 </el-text>
                  <br />
                  <el-text> 该验证码将在5分钟后失效 </el-text>
                </el-text>
              </div>
              <div v-else id="reset-code-info">
                <el-text> 我们向 </el-text>
                <el-text style="font-size: 14px; font-weight: 600; line-height: 20px; color: #101828">
                  {{ resetForm.user_account }}
                  <br />
                  <el-text> 发送了一封含验证码的短信，请查收并输入验证码 </el-text>
                  <br />
                  <el-text> 该验证码将在5分钟后失效 </el-text>
                </el-text>
              </div>
              <div id="reset-valid-code">
                <ValidCode :valid-code-func="resetPassword" />
              </div>
              <div v-if="resetForm.user_account.includes('@')" id="reset-retry-valid-box">
                <div>
                  <el-text> 没有接受到邮件？试试检查垃圾邮件过滤器，或者 </el-text>
                </div>
                <div>
                  <el-text v-if="countDown > 0 && countDown < 60"> {{ countDown }}秒后点击 </el-text>
                  <el-button type="primary" text @click="resendResetEmail"> 重新发送验证邮件 </el-button>
                </div>
              </div>
              <div v-else id="reset-retry-valid-box">
                <div>
                  <el-text> 没有接受到短信？ </el-text>
                </div>
                <div>
                  <el-text v-if="countDown > 0 && countDown < 60"> {{ countDown }}秒后点击 </el-text>
                  <el-button type="primary" text @click="resendResetEmail"> 重新发送验证短信 </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-scrollbar>
    </el-main>
  </el-container>
</template>

<style scoped>
#reset-aside-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
#reset-box {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
  gap: 20px;
  min-width: 350px;
}
#create_account_box {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}
#create-account-button {
  width: calc(100% - 24px);
  display: flex;
  padding: 6px 12px;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  border-radius: 8px;
  background-color: #eff8ff;
  border: 1px solid #b2ddff;
  cursor: pointer;
}
#create-account-button:hover {
  background-color: #d6efff;
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
#reset-form {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 600px;
}
#reset-form-inner {
  width: 100%;
  max-width: 672px;
  display: flex;
  flex-direction: column;
}
#reset-valid-box {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
  gap: 4px;
  width: 100%;
  max-width: 600px;
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

@media screen and (max-width: 768px) {
  #reset-valid-box {
    gap: 6px;
    max-width: 80vw;
  }
}
</style>
