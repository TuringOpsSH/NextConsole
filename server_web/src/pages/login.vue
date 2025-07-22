<script setup lang="ts">
import {onMounted, ref} from "vue";
import router from "@/router";
import {initWxLogin,} from "@/components/user_center/user";
import {
  login, login_text_code_stats, login_text_code_time,
  loginForm,
  loginFormRef, code_login,
  code_login_form,
  code_login_rules,
  codeLoginFormRef,
  contract_form_ref,
  reset_password,
  rules, sendMsgCode, accept_contract_form, contract_rules, invite_view_id, invite_model
} from "@/components/user_center/login";
import {valid_invite_api} from "@/api/contacts";
import HomeFooter from "@/components/user_center/homeFooter.vue";

const props = defineProps({
  login_type:{
    type: String,
    required: false,
    default: 'code'
  },
  invite_view_id: {
    type: String,
    default: '',
    required: false
  }
})
const login_type = ref('code')

// 账号登录表单

function change_login_type(type: string){
  login_type.value = type
  router.push({name: 'login',
    query: {
      login_type: type,
      invite_view_id: invite_view_id.value
    }})
}

async function valid_invite(){
  if (invite_view_id.value){
    let res = await valid_invite_api({
      invite_id: invite_view_id.value
    })
    if (!res.error_status && res.result?.valid &&!res.result?.homepage){
      invite_model.value = true
    }

  }
}
onMounted(
    async () => {
      login_type.value = props.login_type
      invite_view_id.value = props.invite_view_id
      if (invite_view_id.value){
        await valid_invite()
      }
      // 动态加载 wxLogin.js 脚本
      const script = document.createElement('script');
      script.src = 'https://res.wx.qq.com/connect/zh_CN/htmledition/js/wxLogin.js';
      script.onload = () => initWxLogin(); // 确保脚本加载完毕后再初始化微信登录
      document.body.appendChild(script);

    }
)

</script>

<template>
  <el-container>
    <el-main>
      <el-scrollbar>
        <div id="login-aside-box">

          <div id="login_box">
            <div id="login_logo">
              <el-image src="images/logo_text.svg" fit="fill" />
              <el-text style="margin-top: 16px">智能科技创造美好未来</el-text>
            </div>
            <div class="std-middle-box" style="width: 100%; gap: 16px">
              <div class="login-type-area" @click="change_login_type('code')"
                   :class="{ 'login-type-area-active': login_type === 'code'  }" >
                <el-text class="login-type-text"
                         :class="{ 'login-type-text-active': login_type === 'code' }">
                  验证码登录
                </el-text>
              </div>
              <div class="login-type-area" @click="change_login_type('qr_code')"
                   :class="{'login-type-area-active': login_type === 'qr_code'}">
                <el-text class="login-type-text"
                         :class="{'login-type-text-active': login_type === 'qr_code'}">
                  扫码登录
                </el-text>
              </div>
              <div class="login-type-area" @click="change_login_type('password')"
                   :class="{'login-type-area-active': login_type === 'password'}"
              >
                <el-text class="login-type-text"
                         :class="{'login-type-text-active': login_type === 'password'}">
                  密码登录
                </el-text>
              </div>

            </div>
            <div class="login_form" v-show="login_type === 'code'">
              <el-form label-position="top" style="width: 100%" ref="codeLoginFormRef" :model="code_login_form" status-icon
                       :rules="code_login_rules" :hide-required-asterisk="true">
                <el-form-item prop="user_account">
                  <el-input v-model="code_login_form.user_account" placeholder="请输入手机号" v-if="invite_model"/>
                  <el-input v-model="code_login_form.user_account" placeholder="请输入手机号或者邮箱" v-else/>
                </el-form-item>
                <el-form-item prop="text_code" :show-message="false">
                  <el-input v-model="code_login_form.text_code" placeholder="请输入验证码" >
                    <template #suffix>
                      <el-button text @click="sendMsgCode" v-if="login_text_code_stats" type="primary">
                        获取验证码
                      </el-button>
                      <el-button text v-else disabled>
                        {{login_text_code_time}}s后再次获取
                      </el-button>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item >
                  <div style="display: flex;flex-direction: row; align-items: center;
                  justify-content: center;width: 95%">
                    <el-checkbox  v-model="code_login_form.session_30_flag" >
                      30天内自动登录
                    </el-checkbox>
                  </div>


                </el-form-item>
                <el-form-item>
                  <el-button   @click="code_login" id="login-button">
                    <div class="std-middle-box">
                      <el-text style="font-size: 14px;font-weight: 600;color: white;line-height: 20px">
                        登 录
                      </el-text>
                    </div>
                    <div class="std-middle-box" style="margin-left: 6px">
                      <el-image src="images/login_icon.svg"/>
                    </div>

                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            <div class="login_form" v-show="login_type === 'qr_code'" >

              <div id="wx_login_container" />
              <div style="display:flex;flex-direction: row;align-items: center;justify-content: center; gap: 12px">
                <div style="display:flex;flex-direction: row;align-items: center;justify-content: center">
                  <el-image src="images/wx_logo.svg" style="width: 20px; height: 20px"/>
                </div>
                <div>
                  <el-text style="font-size: 15px; font-weight: 600;color: #344054">
                    微信扫一扫
                  </el-text>
                </div>
              </div>
              <div v-if="!accept_contract_form.accept_contract" class="mask-layer">
                <el-text>
                  请先同意并勾选下方的用户协议和隐私政策
                </el-text>

              </div>
            </div>
            <div class="login_form" v-show="login_type === 'password'">
              <el-form label-position="top" style="width: 100%" ref="loginFormRef" :model="loginForm" status-icon
                       :rules="rules" :hide-required-asterisk="true">
                <el-form-item  prop="user_account">
                  <el-input v-model="loginForm.user_account" placeholder="输入手机或者邮箱" />
                </el-form-item>
                <el-form-item  prop="user_password">
                  <el-input v-model="loginForm.user_password" show-password type="password" placeholder="输入密码"

                  />
                </el-form-item>
                <el-form-item >
                  <div style="display: flex;flex-direction: row;
                  align-items: center;
                  justify-content: space-between;width: 95%">
                    <div>
                      <el-button text @click="reset_password" type="primary">找回密码</el-button>
                    </div>
                    <div>
                      <el-checkbox  v-model="loginForm.session_30_flag" >
                        30天内自动登录
                      </el-checkbox>
                    </div>
                  </div>


                </el-form-item>
                <el-form-item>
                  <el-button @click="login" id="login-button">
                    <div class="std-middle-box">
                      <el-text style="font-size: 14px;font-weight: 600;color: white;line-height: 20px">
                        登 录
                      </el-text>
                    </div>
                    <div class="std-middle-box" style="margin-left: 6px">
                      <el-image src="images/login_icon.svg"/>
                    </div>

                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            <div class="std-middle-box std-contract-check" style="gap: 8px">
              <div class="std-middle-box">
                <el-form :model="accept_contract_form" :rules="contract_rules" ref="contract_form_ref">
                  <el-form-item prop="accept_contract" class="contract-check">
                    <el-checkbox v-model="accept_contract_form.accept_contract" style="height: auto"/>
                  </el-form-item>

                </el-form>
              </div>

              <div  >
                <el-text>我已阅读并同意图灵天问的</el-text>
                <el-link type="primary" underline @click="router.push({
                  name: 'contract'
                })">《用户协议》</el-link>
                <el-text>
                  和
                </el-text>
                <el-link type="primary" underline @click="router.push(
                  {name: 'privacy_policy'}
                )">《隐私政策》</el-link>
                <br/>
                <el-text v-if="login_type !='password'">
                  新用户首次登录会自动创建账号
                </el-text>
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
#login-aside-box{
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc( 100vh - 60px);
}
#login_box{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
  gap: 16px;
  max-width: 400px;
}
.login_form{
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  height: 200px;
  position: relative;
}
#login-button{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-direction: row;
  width: 100%;
  background-color: #1570ef;
  border-radius: 8px;
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
#login_logo{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}
.login-type-area{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px;
  cursor: pointer;
  border-bottom: 2px solid white;
}
.login-type-area-active{
  border-bottom: 2px solid #175CD3;
}
.login-type-text{
  font-weight: 600;
  font-size: 14px;
  line-height: 20px;
  color: #667085;
}
.login-type-text-active{
  color: #175CD3;
}
.contract-check :deep(.el-form-item__content){
  .el-form-item__error{
    width: 120px !important;
    margin-top: 20px;
  }
}
.mask-layer{
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
