<script setup lang="ts">

import {begin_valid, resetForm, resetFormRef, resetFormValid,} from "@/components/user_center/reset_password";
import {reactive} from "vue";
import {ElNotification, FormRules} from "element-plus";
import {user_update} from "@/api/user_center";
import CryptoJS from "crypto-js";
import {logout} from "@/utils/auth";
import router from "@/router";

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
async function reset_user_password(){
  if (!resetFormValid.value){
    await resetFormRef.value.validate((valid, fields) => {
      resetFormValid.value = valid;
    })
  }
  if (!resetFormValid.value){
    return
  }
  let res = await user_update(
      {
        user_password: CryptoJS.SHA256(resetForm.password.trim()).toString(),
      }
  )
  if ( !res.error_status){
    ElNotification({
      title: "修改成功",
      message: "密码修改成功，请重新登陆！",
      type: "success",
      duration: 3000,
    })
    logout()
    router.push("/login")
  }
}

</script>

<template>
  <div id="reset-form" >
    <el-form label-position="top" style="width: 100%" ref="resetFormRef"
             :model="resetForm" status-icon
             :rules="rules"
             id="reset-form-inner"
             :disabled="begin_valid"
    >

      <el-form-item label="新密码" prop="password">
        <el-input v-model="resetForm.password" placeholder="请输入新密码" type="password" show-password />
      </el-form-item>
      <el-form-item label="确认密码" prop="password2">
        <el-input v-model="resetForm.password2" placeholder="请确认新密码" type="password" show-password/>
      </el-form-item>
      <el-form-item>
        <el-button   @click="reset_user_password()" id="reset-button">
          <div class="std-middle-box">
            <el-text style="font-size: 14px;font-weight: 600;color: white;line-height: 20px">
              重置密码
            </el-text>
          </div>
          <div class="std-middle-box" style="margin-left: 6px">
            <el-image src="images/login_icon.svg"/>
          </div>

        </el-button>
      </el-form-item>
    </el-form>
  </div>

</template>

<style scoped>
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
</style>
