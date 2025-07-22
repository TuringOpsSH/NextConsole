import {user_id} from '@/components/user_center/user'
import {getUser} from "@/api/user_center";
import {ref} from "vue";
import {version_get} from "@/api/base";
import {ElNotification} from "element-plus";
export const currentVersion = ref(null);

export function get_current_timestamp() {
    let date = new Date();

    let year = date.getFullYear();

    let month = (date.getMonth() + 1).toString().padStart(2, '0');

    let day = date.getDate().toString().padStart(2, '0');

    let hour = date.getHours().toString().padStart(2, '0');

    let minute = date.getMinutes().toString().padStart(2, '0');

    let second = date.getSeconds().toString().padStart(2, '0');

    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}

// 页面辅助函数
export async function refresh_page(){
    // 重新获取用户信息再刷新页面
    await getUser({
        "user_id": user_id.value
    })
    window.location.reload();
}

export async function get_version() {
    try {
        let res = await version_get();
        currentVersion.value = res.result.version;
    } catch (error) {
        console.error('无法获取版本信息', error);
    }
}

export async function check_version() {
    try {
        let res = await version_get();
        if (res.result.version !== currentVersion.value) {
            ElNotification({
                title: '系统通知',
                message: '发现新版本'+ res.result.version+'，请刷新页面！',
                type: 'success',
                duration: 0,
                showClose: false
            })
        }
    } catch (error) {
        console.error('无法获取版本信息', error);
    }
}


export function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
export function omit_text (text:string, length:number){
    if (text.length > length){
        return text.slice(0, length) + '...'
    }
    return text
}
