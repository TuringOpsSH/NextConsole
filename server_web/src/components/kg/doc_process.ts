import {ref} from "vue";
import {ElMessage, ElNotification, UploadRawFile, UploadUserFile} from "element-plus";
import {
    CurrentKg,
    CurrentKgDocList,
    CurrentKgDocPageNum,
    CurrentKgDocPageSize,
    download_loading
} from "@/components/kg/kg_process";
import {
    api,
    doc_batch_rebuild,
    doc_batch_switch,
    doc_content,
    doc_delete,
    doc_download,
    doc_rebuild,
    doc_search,
    doc_update,
    doc_upload_before_check, kg_ref_build
} from "@/api/kg_center";
import {DocMeta} from "@/types/kg";
import request from "@/utils/request";
// @ts-ignore
import mammoth from "mammoth";
import router from "@/router";
// 将Markdown转换为HTML

export const kg_doc_ref = ref(null)
export const kg_doc_data = ref({
    doc_type: '',
    doc_name: '',
    doc_kg_db_id: '',
    doc_kg_name: '',
    pre_question : ''
    }
)
export const doc_preview_loading = ref(false)
export const kg_doc_list = ref<UploadUserFile[]>([])
export const current_kg_doc_list = ref<DocMeta[]>([])

export const CurrentKgDocKeyWord= ref('')
export const CurrentPreviewDoc = ref<DocMeta>()

export const CurrentKgDocTotal = ref(0)
export const CurrentKgDocRefStatus = ref<string[]>()
export const multipleKgDocSelection = ref<DocMeta[]>([])
export async function calculateMD5(file: UploadRawFile): Promise<string> {
    const arrayBuffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
export async function kg_doc_before_upload(file: UploadRawFile){
    kg_doc_data.value.doc_type = CurrentKg.value.kg_type
    kg_doc_data.value.doc_name = file.name
    kg_doc_data.value.doc_kg_db_id = CurrentKg.value.kg_code
    kg_doc_data.value.doc_kg_name = CurrentKg.value.kg_name
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

    return !check_res.error_status;



}
export async function kg_doc_on_remove(file: UploadRawFile | DocMeta){
    //@ts-ignore
    if (!file.doc_id || file.doc_status === '删除'){
        return
    }
    let params = {
        // @ts-ignore
        delete_docs: [file.doc_id]
    }
    let res = await doc_delete(params)
    if (!res.error_status){
        // 删除成功
        // @ts-ignore
        file.doc_status = 'deleted'
        ElNotification.success({
            title: "系统消息",
            message: '删除成功' ,
            duration: 3000
        })
        for (let i = 0; i < kg_doc_list.value.length; i++){
            // @ts-ignore
            if (kg_doc_list.value[i].doc_id === file.doc_id){
                kg_doc_list.value.splice(i, 1)
                break
            }
        }
        for (let i = 0; i < current_kg_doc_list.value.length; i++){
            // @ts-ignore
            if (current_kg_doc_list.value[i].doc_id === file.doc_id){
                current_kg_doc_list.value.splice(i, 1)
                break
            }
        }
        CurrentKgDocTotal.value -= 1
        // 删除预览文档
        // @ts-ignore
        if (CurrentPreviewDoc.value && CurrentPreviewDoc.value.doc_id === file.doc_id){
            CurrentPreviewDoc.value = null
        }

    }
}

export async function kg_doc_on_success(response: any, file: UploadRawFile){
    if (!response.error_status){
        // 上传成功
        // @ts-ignore
        file.doc_id = response.result.doc_id
        current_kg_doc_list.value.push(response.result)
    }
}

export async function search_kg_docs(){

    let params = {
        page_size: CurrentKgDocPageSize.value,
        page_num: CurrentKgDocPageNum.value,
        doc_kg_db_id: CurrentKg.value.kg_code
    }
    if (CurrentKgDocKeyWord.value){

        params["doc_name"]= CurrentKgDocKeyWord.value
    }
    if (CurrentKgDocRefStatus !== null){
        params["doc_ref_status"] =  CurrentKgDocRefStatus.value

    }
    let res = await doc_search(params)
    if (!res.error_status){
        CurrentKgDocList.value = res.result.data
        current_kg_doc_list.value = res.result.data
        CurrentKgDocList.value = res.result.data
        CurrentKgDocTotal.value = res.result.total
    }
    await router.replace(
        {
            params: {
                ...router.currentRoute.value.params,
            },
            query: {
                page_size: CurrentKgDocPageSize.value,
                page_num: CurrentKgDocPageNum.value,
                keyword: CurrentKgDocKeyWord.value,
                ref_status: CurrentKgDocRefStatus.value
            }
        }

    )

}


export async function download_kg_doc(doc: DocMeta) {
    download_loading.value = true
    let params = {
        doc_id: doc.doc_id,
    }
    await doc_download(params)
    download_loading.value = false
}

export async function change_current_preview_doc(doc: DocMeta){
    for (let i = 0; i < current_kg_doc_list.value.length; i++){
        current_kg_doc_list.value[i].is_chosen = false
    }
    doc.is_chosen = true
    doc_preview_loading.value= true
    // text,md,html
    if (doc.doc_format === 'txt' || doc.doc_format === 'md'
        || doc.doc_format === 'html' || doc.doc_format=== 'code' || doc.doc_format=== 'faq'
    )
    {
        if (!doc.doc_id){
            return false
        }
        let params = {
            doc_id: doc.doc_id
        }
        let res = await doc_content(params)
        if (!res.error_status) {
            doc.doc_content = res.result

        }
    }
    else if (doc.doc_format === 'pdf'  ) {
        let params = {
            doc_id: doc.doc_id
        }
        const blob: Blob = await request(
            {
                url:api.doc_download,
                data:params,
                responseType: 'blob'
            }) as Blob; // 这里使用类型断言
        doc.doc_url = window.URL.createObjectURL(blob)
    }
    else if (doc.doc_format === 'docx' || doc.doc_format === 'doc') {
        let params = {
            doc_id: doc.doc_id
        }
        const blob: Blob = await request(
            {
                url:api.doc_download,
                data:params,
                responseType: 'blob'
            }) as Blob; // 这里使用类型断言
         try {
             // @ts-ignore
             doc.doc_content = (await mammoth.convertToHtml({arrayBuffer: blob})).value
         }catch (e){
             doc.doc_content = '此文件格式暂不支持预览，请下载查看'
         }
    }
    else {
        ElNotification.warning(
            {
                title: "系统通知",
                message:"暂不支持此类格式文件的预览！",
                duration: 2000,

            }
        )
    }
    CurrentPreviewDoc.value = doc
    doc_preview_loading.value = false
}

export async function switch_kg_doc_status(doc: DocMeta){
    let params = {
        doc_id: doc.doc_id,
        doc_status: doc.doc_status
    }
    let res = await doc_update(params)
    if (!res.error_status){
        doc.doc_status = params.doc_status
    }
}



export function handleKgDocSelectionChange(val: DocMeta[]){
    multipleKgDocSelection.value = val
}
export async function batch_switch_kg_doc_status(target_status: string){
    // 批量修改选中文档状态
    if (multipleKgDocSelection.value.length === 0){
        ElNotification.info({
            title: "系统消息",
            message: '请先选择文档' ,
            duration: 3000
        })
        return
    }
    let doc_ids = []
    for (let i = 0; i < multipleKgDocSelection.value.length; i++){
        doc_ids.push(multipleKgDocSelection.value[i].doc_id)
    }
    let params = {
        doc_ids: doc_ids,
        doc_status: target_status

    }
    let res = await doc_batch_switch(params)
    if (!res.error_status){
        ElMessage.success({
            message: '批量修改成功',
            type: 'success',
            duration: 666
        })
        await search_kg_docs()
    }
}
export async function kg_doc_rebuild(doc: DocMeta) {
    let params = {
        doc_id: doc.doc_id
    }
    let res = await doc_rebuild(params)
    if (!res.error_status){
        ElNotification.success({
            title: '系统通知',
            message: '重建任务已提交，请耐心等待构建完成！',
            type: 'success',
            duration: 3666
        })
    }
    // 更新current_doc_list
    for (let i = 0; i < current_kg_doc_list.value.length; i++){
        if (current_kg_doc_list.value[i].doc_id === doc.doc_id){
            current_kg_doc_list.value[i] = res.result
            break
        }
    }
}
export async function kg_doc_batch_rebuild(){
    // 批量修改选中文档状态
    if (multipleKgDocSelection.value.length === 0){
        ElMessage.info('请先选择文档')
        return
    }
    let doc_ids = []
    for (let i = 0; i < multipleKgDocSelection.value.length; i++){
        doc_ids.push(multipleKgDocSelection.value[i].doc_id)
    }
    let params = {
        doc_ids: doc_ids,
    }
    let res = await doc_batch_rebuild(params)
    if (!res.error_status){
        ElNotification.success({
            title: '系统通知',
            message: '批量重建任务已提交，请耐心等待构建完成！',
            type: 'success',
            duration: 3666
        })
        await search_kg_docs()
    }
}

