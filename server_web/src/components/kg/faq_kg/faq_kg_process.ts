import {reactive, ref} from "vue";
import {ElNotification, UploadRawFile, UploadUserFile} from "element-plus";
import {CurrentKg, get_current_kg, kg_batch_upload_progress} from "@/components/kg/kg_process";
import {get_kg_upload_template, kg_ref_build} from "@/api/kg_center";
import {kg_doc_data, search_kg_docs} from "@/components/kg/doc_process";
import {kg_batch_upload_logs} from "@/components/kg/code_kg/code_kg_process";

export const dialog_v_upload_faq = ref(false)
export const kg_batch_faq_ref = ref()
export const kg_faq_list = ref<UploadUserFile[]>([])
export const upload_faq_loading = ref(false)
export const current_faq_data_form = reactive(
    {
        pre_question : '',
    }
)

export async function turn_on_upload_faq_dialog(){
    if (!CurrentKg.value.kg_code) {
        return
    }
    await get_current_kg(CurrentKg.value.kg_code)
    dialog_v_upload_faq.value = true
    kg_faq_list.value = []

}
export async function turn_off_upload_faq_dialog(){
    dialog_v_upload_faq.value = false

}
export async function upload_faq_dialog_batch_commit(){
    if (!current_faq_data_form.pre_question){
        return false
    }
    // 提交批量csv
    upload_faq_loading.value = true
    kg_doc_data.value.pre_question = current_faq_data_form.pre_question
    // 获取提交与解析结果
    await kg_batch_faq_ref.value?.submit()
    // 提交构建任务
    let params2 = {
        kg_db_code: CurrentKg.value.kg_code
    }
    await kg_ref_build(params2)

}
export async function download_faq_template(){
    await get_kg_upload_template({
        kg_code: CurrentKg.value.kg_code
    })

    ElNotification.success({
        title: '系统通知',
        message: '下载成功！',
        duration: 6666
    })
}
export async function upload_faq_dialog_batch_on_success(response: any, file: UploadRawFile){
    upload_faq_loading.value = false
    if (!response.error_status){
        kg_batch_upload_progress.value = response.result.progress
        kg_batch_upload_logs.value = response.result.logs
        ElNotification.success(
            {
                title: "系统通知",
                message:"上传完成",
                duration: 5000
            }
        )

        await search_kg_docs()
    }
    else {
        ElNotification.error({
            title: "系统通知",
            message:"上传失败",
            duration: 5000
        })
    }
}

