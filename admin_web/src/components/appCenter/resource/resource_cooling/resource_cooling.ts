import { ref } from 'vue'
import router from "@/router";
import {resource_cooing_record_detail, resource_cooling_record_update} from "@/api/resource_api";
import { ElMessage } from 'element-plus';
import {ResourceDownloadCoolingRecord, ResourceItem} from "@/types/resource_type";
import {Users} from "@/types/users";


export const cool_record_dialog = ref(true)
export const current_cooling_user = ref<Users>({})
export const current_cool_record = ref<ResourceDownloadCoolingRecord>({ })
export const cooling_resource = ref<ResourceItem>({})
export async function init_cooling_record(cooling_id: number) {
    cool_record_dialog.value = true
    console.log('init_cooling_record', cooling_id)
    let params = {
        'cooling_id': cooling_id
    }
    let res = await resource_cooing_record_detail(params)
    if (!res.error_status){
        current_cool_record.value = res.result.cooling_record
        current_cooling_user.value = res.result.cooling_user
        cooling_resource.value = res.result.cooling_resource
    } else {
        current_cool_record.value = null
    }
}

export async function exit_cooling_page(){
    cool_record_dialog.value = false
    await router.push({
        'name': 'resource_share'
    })
}

export async function update_cooling_limit(){
    let params = {
        cooling_id: current_cool_record.value.id,
        cooling_limit: current_cool_record.value.author_allow_cnt,
    }
    console.log('update_cooling_limit', params)
    let res = await resource_cooling_record_update(params)
    if (!res.error_status){
        current_cool_record.value = res.result
        ElMessage.success('更新成功')
    }

}