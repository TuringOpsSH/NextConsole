import router from "@/router";
import { reactive, ref } from "vue";
import CryptoJS from "crypto-js";
import {FormInstance, FormRules, ElMessage} from "element-plus";
import {generate_text_code,  login_by_code, login_by_password} from "@/api/user_center";
import {loginSave} from "@/utils/auth";
export async function begin_create_account(){
    await router.push({name: 'register'})
}
// 协议勾选表单
export const accept_contract_form = reactive({
    accept_contract: false
})
export const contract_form_ref = ref()
export const contract_rules = reactive<FormRules>({
      accept_contract: [

          { validator: accept_contract_check, trigger: 'change' }

      ]
  }
)
export function accept_contract_check(rule: any, value: any, callback: any){
    // 必须勾选协议
    if (!value){
        callback(new Error('请先同意并勾选协议'))
    } else {
        callback()
    }
}


// 账号登录表单
export const loginFormValid = ref(false)
export const loginFormRef = ref<FormInstance>()
export const loginForm = reactive(
  {
      user_account: '',
      user_password: '',
      session_30_flag: true
  }
)
export const rules = reactive<FormRules<typeof loginForm>>({

    user_account: [
        {validator: valid_user_account, trigger: 'blur' }
    ],
    user_password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
    ]

})
export async function login(){
    loginForm.user_account = loginForm.user_account.trim()
    if (!loginFormValid.value){
        loginFormValid.value = await loginFormRef.value?.validate()
    }
    if (!loginFormValid.value){
        return
    }
    // 检验合同是否勾选
    let contract_valid_res = await contract_form_ref.value?.validate()
    if (!contract_valid_res){
        return
    }
    let res = await login_by_password(
      {
          user_account: loginForm.user_account,
          user_password: CryptoJS.SHA256( loginForm.user_password.trim()).toString(),
          session_30_flag: loginForm.session_30_flag,
          invite_view_id: invite_view_id.value
      }
    )
    if (!res.error_status){
        loginSave(res.result)
        // 如果有被拦截的页面，登录成功后跳转到拦截页面
        const redirect = sessionStorage.getItem('redirectRoute')
        if (redirect){
            const route = JSON.parse(redirect); // 将字符串解析为对象
            router.push(route); // 使用完整的路由对象
            sessionStorage.removeItem('redirectRoute')
            return
        }
        router.push({name: 'appCenter'})
    }
}
export async function reset_password(){
    router.push({name: 'reset_password'})
}



// 验证码登录表单
export const codeLoginFormRef = ref<FormInstance>()
export const code_login_form = reactive({
    user_account: '',
    text_code: '',
    session_30_flag: true
})
export const code_login_rules = reactive<FormRules<typeof code_login_form>>({
    user_account: [
        {validator: valid_user_account, trigger: 'blur' }
    ],
    text_code: [
        { required: true, message: '请输入验证码', trigger: 'blur' },
        { pattern: /^\d{6}$/, message: '请输入正确的验证码', trigger: 'blur' }
    ]
})
export const login_text_code_stats = ref(true)
export const login_text_code_time = ref(60)
export function valid_user_account(rule: any, value: any, callback: any){
    const phonePattern = /^1[3456789]\d{9}$/
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (invite_model.value){
        if (!value) {
            return callback(new Error('请输入手机号'))
        }
        if (phonePattern.test(value)) {
            callback()
        } else {
            callback(new Error('请输入正确的手机号'))
        }
    }
    if (!value) {
        return callback(new Error('请输入手机号或者邮箱'))
    }
    if (phonePattern.test(value) || emailPattern.test(value)) {
        callback()
    } else {
        callback(new Error('请输入正确的手机号或者邮箱'))
    }
}
export async function sendMsgCode(){
    if (!login_text_code_stats.value){
        // console.log('正在发送中')
        return
    }
    // 校验账号格式
    let account_valid_res = await codeLoginFormRef.value?.validateField('user_account')
    if (!account_valid_res){
        // console.log(account_valid_res)
        return
    }
    // 发送验证码
    let data = {}
    if( code_login_form.user_account.includes('@')){
        data = {
            user_email: code_login_form.user_account
        }
    }
    else {
        data = {
            user_phone: code_login_form.user_account
        }
    }
    let res = await generate_text_code(data)

    // 发送成功后倒计时
    if (!res.error_status) {
        login_text_code_stats.value = false
        ElMessage.success({
              message: "发送成功",
              duration: 1000
          }
        )
        let time = login_text_code_time.value
        let interval = setInterval(() => {
            time--
            login_text_code_time.value = time
            if (time === 0) {
                clearInterval(interval)
                login_text_code_time.value = 60
                login_text_code_stats.value = true
            }
        }, 1000)
    }
}
export async function code_login(){
    // 校验表单合法性
    let phone_valid_res = await codeLoginFormRef.value?.validate()
    if (!phone_valid_res){
        return
    }
    // 检验合同是否勾选
    let contract_valid_res = await contract_form_ref.value?.validate()
    if (!contract_valid_res){
        return
    }
    let res = await login_by_code(
      {
          user_account: code_login_form.user_account,
          text_code: code_login_form.text_code,
          session_30_flag: code_login_form.session_30_flag,
          invite_view_id: invite_view_id.value
      }
    )
    if (!res.error_status){
        loginSave(res.result)
        // 如果有被拦截的页面，登录成功后跳转到拦截页面
        const redirect = sessionStorage.getItem('redirectRoute')
        if (redirect){
            const route = JSON.parse(redirect); // 将字符串解析为对象
            router.push(route); // 使用完整的路由对象
            sessionStorage.removeItem('redirectRoute')
            return
        }
        router.push({name: 'appCenter'})
    }
}


// 邀请码登录相关
export const invite_view_id = ref()
export const invite_model = ref(false)










