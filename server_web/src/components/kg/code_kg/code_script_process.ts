import {reactive, ref} from "vue";
import {CurrentKg, get_current_kg_docs} from "@/components/kg/kg_process";
import {ElNotification, genFileId, UploadRawFile} from "element-plus";
import {doc_upload_before_check} from "@/api/kg_center";
import {calculateMD5} from "@/components/kg/doc_process";
import {
    dialog_v_upload_kg_script,
    kg_scripts_ref,
    upload_script_loading
} from "@/components/kg/code_kg/code_kg_process";
export const current_script_tags_form = ref(null)
export const current_script_tags= ref({})
export const current_script_tags_valid_status = ref({})
export const kg_script_data = reactive({
    doc_type: '',
    doc_name: '',
    doc_kg_db_id: '',
    doc_kg_name: '',
    doc_tags:""
        }
)

export async function kg_script_before_upload(file: UploadRawFile){
    kg_script_data.doc_type = CurrentKg.value.kg_type
    kg_script_data.doc_name = file.name
    kg_script_data.doc_kg_db_id = CurrentKg.value.kg_code
    kg_script_data.doc_tags = JSON.stringify(current_script_tags.value)
    // 文件大小不能超过100M
    if (file.size > 100 * 1024 * 1024){
        ElNotification.error({
            title: '系统通知',
            message: '文件大小不能超过100M',
            duration: 5000,
        })
        return false
    }
    if (file.size ==0){
        ElNotification.error({
            title: '系统通知',
            message: "文件内容为空！：" + file.name,
            duration: 5000,
        })
        return false
    }
    let fileSHA256  = ''
    try {
        fileSHA256 = await calculateMD5(file)
    }
    catch (e) {
        ElNotification.error({
            title: '系统通知',
            message: '计算文件MD5值失败' +e,
            duration: 5000,
        })
        return false;
    }
    if (!fileSHA256 ) {
        return false;
    }
    // 计算文件的md5，向后端查询是否已经存在
    let check_res = await doc_upload_before_check({
        kg_code: CurrentKg.value.kg_code,
        doc_name: file.name,
        doc_feature_code: fileSHA256
    })
    kg_scripts_ref.value?.clearFiles()
    file.uid = genFileId()
    kg_scripts_ref.value?.handleStart(file)
    return !check_res.error_status;
}

export async function kg_single_script_on_success(response: any, file: UploadRawFile){
    upload_script_loading.value = false
    if (response.error_status) {
        ElNotification.error({
            title: '系统通知',
            message: '上传错误！'+ response.error_message,
            duration: 3000
        })
        return
    }

    ElNotification.success({
        title: '系统通知',
        message: '上传成功',
        type: 'success',
        duration: 1000
    })
    await get_current_kg_docs(CurrentKg.value.kg_code)
    await kg_scripts_ref.value?.clearFiles()

    dialog_v_upload_kg_script.value = false
}
