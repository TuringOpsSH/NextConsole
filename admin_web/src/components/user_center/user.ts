import {reactive, ref} from "vue";
import {Users} from "@/types/users";
import {ElMessage, FormRules} from "element-plus";
import {getToken} from "@/utils/auth";
import {valid_user_account} from "@/components/user_center/login";
import {bind_new_phone_api, reset_new_email, valid_new_phone_api, valid_reset_email_code} from "@/api/user_center";
//@ts-ignore
export const user_info = ref<Users>({
    user_resource_limit: 0,
    user_id: null,
    user_code: null ,
    user_name: null,
    user_nick_name: null,
    user_nick_name_py: 'null',
    user_email: null,
    user_phone: null,
    user_gender: null,
    user_age: null,
    user_avatar: null,
    user_department: null,
    user_company: null,
    user_account_type: null,
    create_time: null,
    update_time: null,
    user_expire_time: null,
    last_login_time: null,
    user_role: null,
    user_status: null,
    user_source: null,
    user_wx_nickname: null,
    user_wx_avatar: null,
    user_wx_openid: null,
    user_wx_union_id: null,
    user_position: null,
    user_department_id: null,
    user_company_id: null,
})
export const user_id = ref(0)

export function beforeAvatarUpload(file: File){

    const isLt5M = file.size / 1024 / 1024 < 5

    if (!isLt5M) {
        ElMessage.error('上传头像图片大小不能超过 5MB!')
    }
    return  isLt5M
}
export async function handleAvatarUploadSuccess(res: any, file: any){
    user_info.value.user_avatar = URL.createObjectURL(file.raw)
    ElMessage.success('上传成功')

}
export const user_avatar_upload_header = {
    Authorization: 'Bearer ' + getToken()
}


export function initWxLogin() {
    // 确保 WxLogin 已经加载
    let redirect_url = import.meta.env.VITE_APP_NEXT_CONSOLE_PATH + "#/login/wx_login"
    if (import.meta.env.VITE_APP_NODE_ENV === 'private') {
        redirect_url = window.location.protocol + "//" + window.location.host + "/#/login/wx_login"
    }
    console.log(redirect_url)
    //@ts-ignore
    if (typeof WxLogin !== 'undefined') {
        //@ts-ignore
        const obj = new WxLogin({
            self_redirect: false,
            id: "wx_login_container",
            appid: import.meta.env.VITE_APP_CORP_ID,
            scope: "snsapi_login",
            redirect_uri: encodeURIComponent(redirect_url),
            state: "login",
            style: "black",
            href: "data:text/css;base64,LmltcG93ZXJCb3gge3dpZHRoOiAxMjhweH0NCi5pbXBvd2VyQm94IC5xcmNvZGUge3dpZHRoOiAxMjNweDt9DQouaW1wb3dlckJveCAudGl0bGUge2Rpc3BsYXk6IG5vbmV9DQouaW1wb3dlckJveCAuaW5mbyB7ZGlzcGxheTogbm9uZX0NCi5pbXBvd2VyQm94IC53cnBfY29kZSB7d2lkdGg6IDEyOHB4fQ0KDQoNCg=="

        });
        let container = document.getElementById("wx_login_container")
        const iframe = container.querySelector('iframe');
        iframe.width = "128px";
        iframe.height = "140px";
    }
}


// 邮箱绑定
export const email_update = ref(false)
export const email_bind_form = reactive({
    user_email: "",
    user_email_code: ""
})
export const email_bind_form_ref = ref()
export const  email_bind_rules = reactive<FormRules<typeof email_bind_form>>({
    user_email: [
        {validator: valid_user_account, trigger: 'blur' }
    ],
    user_email_code: [
        { required: true, message: '请输入验证码', trigger: 'blur' },
        { pattern: /^\d{6}$/, message: '请输入正确的验证码', trigger: 'blur' }
    ]
})

export const bind_text_code_status = ref(true)
export const bind_text_code_time = ref(60)

export function begin_bind_email(){
    email_update.value = true


}
export async function send_bind_code(){
    if (!bind_text_code_status.value){
        // console.log('正在发送中')
        return
    }
    // 校验账号格式
    let account_valid_res = await email_bind_form_ref.value?.validateField('user_email')
    if (!account_valid_res){
        // console.log(account_valid_res)
        return
    }
    // 发送验证码
    let data = {
        new_email: email_bind_form.user_email
    }
    let res = await reset_new_email(data)
    if (!res.error_status) {
        bind_text_code_status.value = false
        ElMessage.success({
                message: "发送成功",
                duration: 1000
            }
        )
        let timer = setInterval(() => {
            bind_text_code_time.value--
            if (bind_text_code_time.value === 0){
                bind_text_code_status.value = true
                bind_text_code_time.value = 60
                clearInterval(timer)
            }
        }, 1000)
    }

}
export async function bind_new_email(){

    let res = await valid_reset_email_code({
        new_email: email_bind_form.user_email,
        code: email_bind_form.user_email_code
    })
    if (!res.error_status){
        ElMessage.success({
            message: "绑定成功",
            duration: 1000
        })
        email_update.value = false
        user_info.value.user_email = email_bind_form.user_email
    }
}

// 手机绑定
export const phone_update = ref(false)
export const phone_bind_form = reactive({
    user_phone: "",
    user_phone_code: ""
})
export const phone_bind_form_ref = ref()
export const  phone_bind_rules = reactive<FormRules<typeof phone_bind_form>>({
    user_phone: [
        {validator: valid_user_account, trigger: 'blur' }
    ],
    user_phone_code: [
        { required: true, message: '请输入验证码', trigger: 'blur' },
        { pattern: /^\d{6}$/, message: '请输入正确的验证码', trigger: 'blur' }
    ]
})
export const bind_text_code_status_phone = ref(true)
export const bind_text_code_time_phone = ref(60)
export function begin_bind_phone(){
    phone_update.value = true
}
export async function send_bind_code_phone(){
    if (!bind_text_code_status_phone.value){
        // console.log('正在发送中')
        return
    }
    // 校验账号格式
    let account_valid_res = await phone_bind_form_ref.value?.validateField('user_phone')
    if (!account_valid_res){
        // console.log(account_valid_res)
        return
    }
    // 发送验证码
    let data = {
        new_phone: phone_bind_form.user_phone
    }
    let res = await bind_new_phone_api(data)
    if (!res.error_status) {
        bind_text_code_status_phone.value = false
        ElMessage.success({
                message: "发送成功",
                duration: 1000
            }
        )
        let timer = setInterval(() => {
            bind_text_code_time_phone.value--
            if (bind_text_code_time_phone.value === 0){
                bind_text_code_status_phone.value = true
                bind_text_code_time_phone.value = 60
                clearInterval(timer)
            }
        }, 1000)
    }

}
export async function bind_new_phone(){
    let res = await valid_new_phone_api({
        new_phone: phone_bind_form.user_phone,
        code: phone_bind_form.user_phone_code
    })
    if (!res.error_status){
        ElMessage.success({
            message: "绑定成功",
            duration: 1000
        })
        phone_update.value = false
        user_info.value.user_phone = phone_bind_form.user_phone
    }
}


// 微信绑定
export const wx_update = ref(false)
export async function init_wx_bind(){
    // 确保 WxLogin 已经加载
    let VITE_APP_NEXT_CONSOLE_PATH = import.meta.env.VITE_APP_NEXT_CONSOLE_PATH
    if (import.meta.env.VITE_APP_NODE_ENV === 'private') {
        VITE_APP_NEXT_CONSOLE_PATH = window.location.protocol + "//" + window.location.host + "/"
    }
    let redirect_url = VITE_APP_NEXT_CONSOLE_PATH + "#/login/wx_login"
    // @ts-ignore
    if (typeof WxLogin !== 'undefined') {

        //@ts-ignore
        const obj = new WxLogin({
            self_redirect: false,
            id: "wx_login_container",
            appid: import.meta.env.VITE_APP_CORP_ID,
            scope: "snsapi_login",
            redirect_uri: encodeURIComponent(redirect_url),
            state: "bind",
            style: "black",
            href: "data:text/css;base64,LmltcG93ZXJCb3gge3dpZHRoOiAxMjhweH0NCi5pbXBvd2VyQm94IC5xcmNvZGUge3dpZHRoOiAxMjNweDt9DQouaW1wb3dlckJveCAudGl0bGUge2Rpc3BsYXk6IG5vbmV9DQouaW1wb3dlckJveCAuaW5mbyB7ZGlzcGxheTogbm9uZX0NCi5pbXBvd2VyQm94IC53cnBfY29kZSB7d2lkdGg6IDEyOHB4fQ0KDQoNCg=="

        });
        let container = document.getElementById("wx_login_container")
        const iframe = container.querySelector('iframe');
        iframe.width = "128px";
        iframe.height = "140px";
    }
}
export async function begin_bind_wx(){
    wx_update.value = true
    const script = document.createElement('script');
    script.src = 'https://res.wx.qq.com/connect/zh_CN/htmledition/js/wxLogin.js';
    script.onload = () => init_wx_bind(); // 确保脚本加载完毕后再初始化微信登录
    document.body.appendChild(script);


}





