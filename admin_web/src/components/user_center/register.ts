import {reactive} from "vue";
import {confirm_email} from "@/api/user_center";
import {ElNotification} from "element-plus";
import router from "@/router";
import {loginSave} from "@/utils/auth";

export const registerForm = reactive(
    {
        user_email: '',
        user_nickname:'',
        user_company:'',
        user_area_id:'',
        password: '',
        password2: ''
    }
)

export async function register_code_valid(code :string){
        let res = await confirm_email(
            {
                    email : registerForm.user_email,
                    code : code
            }
        )
        if (!res.error_status){
                if (!res.result?.token){
                        //验证码错误
                        ElNotification({
                                title: '错误',
                                message: '验证码错误',
                                type: 'error',
                                duration: 2000
                        })


                }
                //验证码正确，保存用户数据并跳转
                else {
                        loginSave(res.result)

                        await router.push({
                                name: 'user_activity'
                        })
                }

        }
}
