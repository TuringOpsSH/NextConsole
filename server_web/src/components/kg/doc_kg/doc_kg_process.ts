import {ElMessage, UploadRawFile} from "element-plus";
import router from "@/router";
import {
    CurrentKg,
    CurrentKgType,
    CurrentStage,
    get_current_kg_docs, upload_loading
} from "@/components/kg/kg_process";
import {kg_doc_list, kg_doc_ref} from "@/components/kg/doc_process";
import {ref} from "vue";
import {sleep} from "@/utils/base";
export const dialog_v_upload_kg_file = ref(false)
export async function turn_on_upload_dialog(){
    if(CurrentKg.value.kg_code){
        dialog_v_upload_kg_file.value = true
    }
    else {
        ElMessage.warning({
            message:'请先完善知识库基础信息！',
            duration: 600
        })
        CurrentStage.value = 'meta'
        await router.replace({
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

export async function turn_off_upload_dialog(){
    dialog_v_upload_kg_file.value = false
    kg_doc_list.value = []
    await get_current_kg_docs(CurrentKg.value.kg_code)

}
export async function upload_dialog_commit(){
    upload_loading.value = true
    await kg_doc_ref.value!.submit() // 提交上传
    // 循环检查上传文件状态，直到所有文件处理完成
    while (upload_loading.value){
        let check_flag = true
        for (let i=0; i<kg_doc_list.value.length; i++){
            if (kg_doc_list.value[i].status !== 'success'){
                check_flag = false
                break
            }
        }
        if (check_flag){
            upload_loading.value = false
            dialog_v_upload_kg_file.value = false
            if (kg_doc_list.value.length){
                ElMessage.success({
                    message: '上传成功',
                    type: 'success',
                    duration: 666
                })
                await get_current_kg_docs(CurrentKg.value.kg_code)
            }

        }
        else {
            await sleep(100)
        }

    }


}
export async function upload_dialog_remove(file: UploadRawFile ){
    kg_doc_ref.value!.handleRemove(file)
}
