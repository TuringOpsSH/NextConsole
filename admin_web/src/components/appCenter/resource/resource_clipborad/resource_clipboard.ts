import {search_resource_object} from "@/api/resource_api";
import {ElMessage, ElNotification} from "element-plus";
import {ResourceItem} from "@/types/resource_type";
import {ref} from "vue";
export const resource_clipboard = ref(null)
export const current_resource_clipboard = ref<ResourceItem[]>([])
export const current_paste_resource = ref<ResourceItem>()
export const paste_resource_dialog = ref(false)
export async function push_to_clipboard(resource_list: number[], is_share = false){
    let res = null
    if (is_share){
        res = await search_resource_object({
            resource_list: resource_list,
            resource_source: [],
            is_global: true
        })
    }
    else {
        res = await search_resource_object({
            resource_list: resource_list,
            resource_source: [],
            is_global: true
        })
    }

    if (!res.error_status){
        current_resource_clipboard.value = res.result.data
        ElMessage.success(
            {
                message: '资源已加入粘贴板！',
                type: 'success',
                duration: 2000
            }
        )
    }
    // 保存至本地存储
    localStorage.setItem('resource_clipboard', JSON.stringify(current_resource_clipboard.value))

}
export function remove_copy_resource(idx:number){
    current_resource_clipboard.value.splice(idx, 1)
    ElMessage.success(
        {
            message: '资源已移出粘贴板！',
            type: 'success',
            duration: 2000
        }
    )
    // 保存至本地存储
    localStorage.setItem('resource_clipboard', JSON.stringify(current_resource_clipboard.value))

}
export async function paste_resource_confirm( ){

}

export async function paste_resource(){

}

export function clean_all_clipboard(){
    current_resource_clipboard.value = []
    ElMessage.success(
        {
            message: '粘贴板已清空！',
            type: 'success',
            duration: 2000
        }
    )
    resource_clipboard.value?.hide()
    // 保存至本地存储
    localStorage.setItem('resource_clipboard', JSON.stringify(current_resource_clipboard.value))
}
export function init_clipboard(){
    if (!current_resource_clipboard.value?.length){
        let clipboard = localStorage.getItem('resource_clipboard')
        if (clipboard){
            current_resource_clipboard.value = JSON.parse(clipboard)
        }
    }
}
