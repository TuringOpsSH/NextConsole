<script setup lang="ts">

import {
  limitNumber,
  limitTextNumber,
  login_text_code_stats, login_text_code_time,
  sendMsgCode,
  user_phone,
  user_text_code, userPhoneBind, userPhoneLogin
} from "@/components/user_center/user";
</script>

<template>
  <div class="login-div2">
    <div class="login-div3">
      <div>
        <el-image src="images/phone_red.svg" style="width: 24px; height: 24px"/>
      </div>
      <div>
        <el-text style="font-size: 16px;font-weight: 600;color: #101828">
          手机号绑定
        </el-text>
      </div>
    </div>
    <div class="login-input-box">
      <el-input placeholder="请输入手机号" v-model="user_phone" clearable inputmode="numeric"
                maxlength="11" @input="limitNumber"
      />
    </div>
    <div class="login-input-box">

      <el-input placeholder="输入验证码" v-model="user_text_code" inputmode="numeric" maxlength="6"
                @input="limitTextNumber" @keydown.enter="userPhoneBind()">
        <template #suffix>

          <el-text style="font-weight: 500;font-size: 14px;color: #175CD3;cursor: pointer" @click="sendMsgCode"
                   v-if="login_text_code_stats">
            获取验证码
          </el-text>
          <el-text v-else style="color: #475467;font-weight: 500;font-size: 14px">
            {{login_text_code_time}}s后再次获取
          </el-text>

        </template>
      </el-input>
    </div>
    <div id="login_button" @click="userPhoneBind()">
      <el-text style="color: white;font-size: 14px;font-weight: 600" >绑定</el-text>
    </div>
  </div>
</template>

<style scoped>
.login-div2{
  display: flex;
  flex-direction: column;
  padding: 0;
  gap: 16px;

  align-items: flex-start;
  justify-content: center;
}
.login-div3{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
#login_button{
  width: calc(100% - 24px);
  border-radius: 8px;
  background-color: #1570ef;
  box-shadow: 0 1px 2px 0 #1018280D;
  border: 1px solid #1570EF;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.login-input-box{
  width: 100%;
}
@media (max-width: 600px) {
  .login-div2{

    width: 100%;
    padding: 0;

  }
  #login_button{
    width: calc(100% - 24px);
  }
}
</style>
