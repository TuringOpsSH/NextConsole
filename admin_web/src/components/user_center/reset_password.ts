import {reset_account_password, valid_reset_password_code} from "@/api/user_center";
import {ElNotification, FormInstance} from "element-plus";
import router from "@/router";
import {reactive, ref} from "vue";
import CryptoJS from "crypto-js";
import {count_down, count_down_start} from "@/components/user_center/valid_code";
import {logout} from "@/utils/auth";

export const resetForm = reactive(
    {
        user_account: '',
        user_valid_code:'',
        password: '',
        password2: ''
    }
)
export const resetFormValid = ref(false)
export const begin_valid = ref(false)
export const resetFormRef = ref<FormInstance>()

export async function send_reset_email(){
    if (!resetFormValid.value){
        resetFormValid.value = await resetFormRef.value?.validate( )
    }
    if (!resetFormValid.value){
        return
    }
    // 发送重置密码验证码

    let res = await reset_account_password(
        {
            user_account : resetForm.user_account,
            new_password: CryptoJS.SHA256(resetForm.password.trim()).toString(),
        }

    )
    if (!res.error_status){
        begin_valid.value = true
        ElNotification({
            title: '成功',
            message: '验证码已发送',
            type: 'success',
            duration: 3000
        })
        count_down_start()

    }

}
export async function resend_reset_email(){
    if (count_down.value > 0){
        return
    }
    let res = await reset_account_password(
        {
            user_account : resetForm.user_account,
            new_password: CryptoJS.SHA256(resetForm.password.trim()).toString(),
        }

    )
    if (!res.error_status){
        ElNotification({
            title: '成功',
            message: '验证码已发送',
            type: 'success',
            duration: 3000
        })

    }
    count_down.value = 60
    count_down_start()
}
export async function reset_password(code :string){
    let res = await valid_reset_password_code(
        {
            user_account : resetForm.user_account,
            code : code
        }
    )
    if (!res.error_status){


        ElNotification({
            title: '成功',
            message: '密码重置成功，请重新登录',
            type: 'success',
            duration: 3000
        })
        resetForm.user_account = ''
        resetForm.password = ''
        resetForm.password2 = ''
        resetForm.user_valid_code = ''
        begin_valid.value = false
        logout()
        router.push({
            'name': 'login'
        })

    }


}
