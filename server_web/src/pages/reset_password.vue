<script setup lang="ts">

import {valid_user_account} from "@/components/user_center/login";
// 重置密码表单
import {FormRules} from "element-plus";
import {reactive} from "vue";
import Valid_code from "@/components/user_center/valid_code.vue";
import {count_down} from "@/components/user_center/valid_code";
import {
  begin_valid,
  resend_reset_email,
  reset_password,
  resetForm,
  resetFormRef,
  resetFormValid,
  send_reset_email,
} from "@/components/user_center/reset_password";

function validatePass1 (rule: any, value: any, callback: any){
  if (value.includes(' ')) {
    callback(new Error('密码中请勿包含空格!'))
  }
  callback()

}
function validatePass2 (rule: any, value: any, callback: any){
  if (value !== resetForm.password) {
    callback(new Error('请确认两次输入密码一致！'))
  }
  callback()

}
const rules = reactive<FormRules<typeof resetForm>>({
  user_account: [
    { trigger: 'blur', validator: valid_user_account},
  ],
  password: [
    { trigger: 'blur', required: true, message: '请输入密码'},
    { trigger: 'blur', min:6, max:200, message: '长度请保持在6-200之间'},
    { validator: validatePass1, trigger: 'blur'}

  ],
  password2: [
    { trigger: 'blur', required: true, message: '请输入密码'},
    { trigger: 'blur', min:6, max:200, message: '长度请保持在6-200之间'},
    { validator: validatePass2, trigger: 'blur'}
  ],
})


</script>

<template>
  <el-container>
    <el-main>
      <el-scrollbar>
        <div id="reset-aside-box">
          <div id="reset-box">
            <div id="login_logo">
              <el-image src="images/logo_text.svg" fit="fill"/>
            </div>
            <div id="reset-form" >
              <el-form label-position="top" style="width: 100%" ref="resetFormRef"
                       :model="resetForm" status-icon
                       :rules="rules"
                       id="reset-form-inner"
                       :disabled="begin_valid"
              >
                <el-form-item label="账号" prop="user_account">
                  <el-input v-model="resetForm.user_account" placeholder="输入手机号或邮箱" />
                </el-form-item>
                <el-form-item label="新密码" prop="password">
                  <el-input v-model="resetForm.password" placeholder="请输入新密码" type="password" show-password/>
                </el-form-item>
                <el-form-item label="确认密码" prop="password2">
                  <el-input v-model="resetForm.password2" placeholder="请确认新密码" type="password" show-password/>
                </el-form-item>
                <el-form-item>
                  <el-button   @click="send_reset_email" id="reset-button">
                    <div class="std-middle-box">
                      <el-text style="font-size: 14px;font-weight: 600;color: white;line-height: 20px">
                        发送验证码
                      </el-text>
                    </div>
                    <div class="std-middle-box" style="margin-left: 6px">
                      <el-image src="images/login_icon.svg"/>
                    </div>

                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            <div id="reset-valid-box" v-if="resetFormValid">
              <div id="reset-code-info" v-if="resetForm.user_account.includes('@')">
                <el-text>
                  我们向
                </el-text>
                <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #101828">
                  {{resetForm.user_account}}
                </el-text><br/>
                <el-text>
                  发送了一封含验证码的邮件，请查收并输入验证码
                </el-text>
                <br/>
                <el-text>
                  该验证码将在5分钟后失效
                </el-text>
              </div>
              <div id="reset-code-info" v-else>
                <el-text>
                  我们向
                </el-text>
                <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #101828">
                  {{resetForm.user_account}}
                </el-text><br/>
                <el-text>
                  发送了一封含验证码的短信，请查收并输入验证码
                </el-text>
                <br/>
                <el-text>
                  该验证码将在5分钟后失效
                </el-text>
              </div>
              <div id="reset-valid-code">
                <valid_code :valid_code_func="reset_password"/>
              </div>
              <div id="reset-retry-valid-box" v-if="resetForm.user_account.includes('@')">
                <div>
                  <el-text>
                    没有接受到邮件？试试检查垃圾邮件过滤器，或者
                  </el-text>
                </div>
                <div>
                  <el-text v-if="count_down>0 && count_down < 60">
                    {{count_down}}秒后点击
                  </el-text>
                  <el-button type="primary" text @click="resend_reset_email()">

                    重新发送验证邮件

                  </el-button>
                </div>
              </div>
              <div id="reset-retry-valid-box" v-else>
                <div>
                  <el-text>
                    没有接受到短信？
                  </el-text>
                </div>
                <div>
                  <el-text v-if="count_down>0 && count_down < 60">
                    {{count_down}}秒后点击
                  </el-text>
                  <el-button type="primary" text @click="resend_reset_email()">
                    重新发送验证短信
                  </el-button>
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
#reset-aside-box{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
#reset-box{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
  gap: 20px;
  min-width: 350px;
}
#create_account_box{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}
#create-account-button{
  width: calc(100% - 24px);
  display: flex;
  padding: 6px 12px;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  border-radius: 8px;
  background-color: #eff8ff;
  border: 1px solid #B2DDFF;
  cursor: pointer;
}
#create-account-button:hover{
  background-color: #D6EFFF;
}
#reset-button{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-direction: row;
  width: 100%;
  background-color: #1570ef;
  border-radius: 8px;
}
#reset-form{
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 600px;
}
#reset-form-inner{
  width: 100%;
  max-width: 672px;
  display: flex;
  flex-direction: column;
}
#reset-valid-box{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
  gap: 4px;
  width: 100%;
  max-width: 600px;

}
.std-middle-box{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}
.el-main{
  padding: 0 !important;
}
:deep(.el-input__validateIcon) {
  color: green;
}


@media  screen and (max-width: 768px) {

  #reset-valid-box{
    gap: 6px;
    max-width: 80vw;
  }
}
</style>
