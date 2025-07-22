import {ElMessage} from "element-plus";
import router from "@/router";
import {
    CurrentKg, CurrentKgDocList,
    CurrentKgType,
    CurrentStage,
    upload_loading
} from "@/components/kg/kg_process";
import {add_kg_db_website} from "@/api/kg_center";
import {current_kg_doc_list, CurrentKgDocTotal} from "@/components/kg/doc_process";
import {ref} from "vue";
export const dialog_v_upload_kg_website = ref(false)
export const CurrentWebSiteError = ref(false)
export const CurrentWebSiteErrorMsg = ref('')
export const CurrentWebSiteViewModel = ref(true)

export async function turn_on_upload_website_dialog(){
    if(CurrentKg.value.kg_code){
        dialog_v_upload_kg_website.value = true
    }
    else {
        ElMessage.warning({
            message:'请先完善知识库基础信息！',
            duration: 600
        })
        CurrentStage.value = 'meta'
        await router.push({
            name: 'kg_manage_add',
            query: {
                ...router.currentRoute.value.query, // 保持既有参数
                stage: CurrentStage.value,
                kg_code: CurrentKg.value.kg_code,
                kg_type: CurrentKgType.value

            }
        })
    }

}
export async function turn_off_upload_website_dialog(){
    if (!CurrentWebSiteError.value){
        dialog_v_upload_kg_website.value = false
        upload_loading.value = true
        // 获取网站所有链接
        let res = await add_kg_db_website({
            kg_code : CurrentKg.value.kg_code,
            kg_name : CurrentKg.value.kg_name,
            site_url: CurrentKg.value.kg_url,
            navi_selector: '',
            method: '',

        })
        if (!res.error_status) {
            CurrentKgDocList.value = res.result
            current_kg_doc_list.value = res.result
            CurrentKgDocList.value = res.result
            CurrentKgDocTotal.value = res.result.length

            // await search_kg_docs();


        }
    }
    upload_loading.value = false

}

export async function validate_web_url(url:string){
    // 验证URL基础格式
    const urlRegex = /^(https?:\/\/)?([a-z\d-]+\.)*[a-z\d-]+\.[a-z]{2,}(\/.*)?$/i;
    CurrentWebSiteErrorMsg.value = '';
    CurrentWebSiteError.value = false;
    if (!urlRegex.test(url)) {
        CurrentWebSiteErrorMsg.value = '请输入正确的URL';
        CurrentWebSiteError.value= true;
        return false;
    }
}
