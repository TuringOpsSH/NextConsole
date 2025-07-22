import {nextTick, ref} from "vue";
import {
    add_kg,
    delete_kg,
    doc_search,
    get_kg_detail,
    kg_ref_build,
    kg_ref_get,
    search_kg_list,
    update_kg
} from "@/api/kg_center";
import {DocMeta, KGMeta, KGRefStatus} from "@/types/kg";
import router from "@/router";
import {ElNotification, genFileId, UploadRawFile} from "element-plus";
import {getToken} from "@/utils/auth";
import {
     current_kg_doc_list,
    CurrentKgDocKeyWord,
    CurrentKgDocRefStatus,
    CurrentKgDocTotal
} from "@/components/kg/doc_process";
import {check_kg_permission} from "@/components/kg/kg_center_base";

export const CurrentKg = ref<KGMeta>({
    kg_json_schema: {
        meta:{
            code: "",
            embedding:[]
        },
        properties:{},
        required:[],
        type: 'object'
    },
    kg_company: "",
    kg_code: null,
    kg_name: null,
    kg_type: null,
    kg_desc: null,
    kg_tags: [],
    kg_public: 0,
    kg_author_id: null,
    kg_author_name: null,
    kg_author_avatar: null,
    kg_icon: null,
    kg_status: '初始化',
    kg_sync_frequency: null,
    kg_url: null,
    rag_factor: 0.75,
    rag_relevant_threshold: 0.25,
    create_time: null,
    update_time: null,
    doc_cnt: 0,
    kg_ref_id:  null,
    kg_ref_status:  null,
    kg_is_chosen: false

})
export const CurrentKeyword = ref('')
export const CurrentKgPublic = ref(-1)
export const CurrentKgList = ref<KGMeta[]>([])
export const CurrentKgDetail = ref('file')
export const CurrentStage = ref('meta')
export const CurrentKgType = ref('file')
export const CurrentKgTotal = ref(0)
export const CurrentKgPageSize = ref(100)
export const CurrentKgPageNum = ref(1)
export const CurrentKgDocPageSize = ref(20)
export const CurrentKgDocPageNum = ref(1)
export const CurrentListKgType = ref('')
export const CurrentKgDocList = ref<DocMeta[]>([])
export const CurrentKgBuildProgress = ref<KGRefStatus>({
    Error: 0, Failure: 0, Pending: 0, Success: 0, Total: 0

})

export const dialog_v_delete_confirm = ref(false)
export const dialog_v_add_kg = ref(false)
export const inputKgTagVisible = ref(false)
export const inputKgTagValue= ref('')
export const InputKgTagRef = ref(null)
export const upload_kg_avatar = ref(null)
export const ValidKgNameError = ref(false)
export const ValidKgNameErrorMsg = ref('')
export const check_kg_ref_progress_interval_id = ref()
export const upload_loading = ref(false)
export const download_loading = ref(false)
export const show_kg_batch_upload_result = ref(false)
export const kg_batch_upload_progress = ref(10)
export async function search_kgs(){
    let params = {

        page_num:CurrentKgPageNum.value,
        page_size: CurrentKgPageSize.value,

    }
    if (CurrentKeyword.value){
        params["kg_name"] = CurrentKeyword.value
        params["kg_desc"] = CurrentKeyword.value
        params["kg_tags"] = [CurrentKeyword.value]

    }
    if (CurrentKgPublic.value !== -1){
        params["kg_public_model"] = CurrentKgPublic.value

    }
    if (CurrentListKgType.value && CurrentListKgType.value !== "All"){
        params["kg_type"] = [CurrentListKgType.value]
    }
    let response = await search_kg_list(params)
    if (!response.error_status){
        CurrentKgList.value = response.result.data
        CurrentKgTotal.value = response.result.total
        await router.push(
            {
                name: 'kg_manage_list',
                query: {
                    page_num: CurrentKgPageNum.value,
                    page_size: CurrentKgPageSize.value
                }
            }
        )
    }
}

export async function get_current_kg(kg_code:string){
    let params = {
        kg_code: kg_code
    }
    let response = await get_kg_detail(params)
    if (!response.error_status){
        CurrentKg.value = response.result
    }
}

export async function switch_delete_dialog(kg:KGMeta){
    CurrentKg.value = kg
    dialog_v_delete_confirm.value = !dialog_v_delete_confirm.value
}

export async function delete_current_kg(){
    if (!CurrentKg.value.kg_code){
        return false
    }
    let params = {
        kg_codes: [CurrentKg.value.kg_code]
    }
    let response = await delete_kg(params)
    if (!response.error_status){
        ElNotification.success({
            title: '系统通知',
            message: '删除知识库成功',
            duration: 600
        })
        dialog_v_delete_confirm.value = false
        for (let i=0; i<CurrentKgList.value.length; i++){
            if (CurrentKgList.value[i].kg_code === CurrentKg.value.kg_code){
                CurrentKgList.value.splice(i, 1)
            }
        }
        CurrentKg.value = {
            kg_json_schema: {
                meta:{
                    code: "",
                    embedding:[]
                },
                properties:{},
                required:[],
                type: 'object'
            },
            kg_company: "",
            kg_author_avatar: "",
            kg_author_name: "",
            kg_is_chosen: false,
            kg_ref_id: "",
            kg_ref_status: "",
            kg_code: null,
            kg_name: null,
            kg_type: null,
            kg_desc: null,
            kg_tags: [],
            kg_public: 0,
            kg_author_id: null,
            kg_icon: null,
            kg_status: '初始化',
            kg_sync_frequency: null,
            kg_url: null,
            rag_factor: 0.75,
            rag_relevant_threshold: 0.25,
            create_time: null,
            update_time: null,
            doc_cnt: 0

        }
    }
}

export async function change_kg_add_stage(step:number){
    let all_stage = ['meta', 'upload', 'rag', 'finish']
    // 找到当前stage的index
    let index = all_stage.indexOf(CurrentStage.value)
    let stage = all_stage[index + step]
    if (CurrentStage.value === 'meta' && step ===1){
        if (!ValidKgMeta()){
            return
        }

        if (!CurrentKg.value.kg_code) {
            // 增加知识库元信息
            let params = {
                kg_name: CurrentKg.value.kg_name,
                kg_type: CurrentKgType.value,
                kg_icon: CurrentKg.value.kg_icon,
                kg_desc: CurrentKg.value.kg_desc,
                kg_tags: CurrentKg.value.kg_tags,
                kg_url: CurrentKg.value.kg_url,
                kg_sync_frequency: CurrentKg.value.kg_sync_frequency,
                rag_factor: CurrentKg.value.rag_factor,
                rag_relevant_threshold: CurrentKg.value.rag_relevant_threshold,
                kg_status: CurrentKg.value.kg_status,
                kg_public: CurrentKg.value.kg_public,
            }
            let response = await add_kg(params)
            if (!response.error_status) {
                CurrentKg.value = response.result
                await router.replace({
                    name: 'kg_manage_add',
                    query: {
                        ...router.currentRoute.value.query, // 保持既有参数
                        kg_code: CurrentKg.value.kg_code
                    }
                })
            } else {
                return
            }
        } else {
            // 更新知识库元信息
            let params = {
                kg_code: CurrentKg.value.kg_code,
                kg_name: CurrentKg.value.kg_name,
                kg_type: CurrentKg.value.kg_type,
                kg_icon: CurrentKg.value.kg_icon,
                kg_desc: CurrentKg.value.kg_desc,
                kg_tags: CurrentKg.value.kg_tags,
                kg_url: CurrentKg.value.kg_url,
                kg_sync_frequency: CurrentKg.value.kg_sync_frequency,
                rag_factor: CurrentKg.value.rag_factor,
                rag_relevant_threshold: CurrentKg.value.rag_relevant_threshold,
                kg_status: CurrentKg.value.kg_status,
                kg_public: CurrentKg.value.kg_public,
            }
            let response = await update_kg(params)
            if (!response.error_status) {
                CurrentKg.value = response.result
                await router.replace({
                    name: 'kg_manage_add',
                    query: {
                        ...router.currentRoute.value.query, // 保持既有参数
                        kg_code: CurrentKg.value.kg_code
                    }
                })
            } else {
                return
            }
        }

    }
    // 切换到下一个stage
    CurrentStage.value = stage
    await router.replace({
        name: 'kg_manage_add',
        query: {
            ...router.currentRoute.value.query, // 保持既有参数
            stage: stage
        }
    })

}

export async function reset_new_kg(){
    // 删除当前知识库元信息
    if (!CurrentKg.value.kg_code){
        return false
    }
    let params = {
        kg_codes: [CurrentKg.value.kg_code]

    }
    let response = await delete_kg(params)
    if (!response.error_status){
        CurrentKg.value = {
            kg_json_schema: {
                meta:{
                    code: "",
                    embedding:[]
                },
                properties:{},
                required:[],
                type: 'object'
            },
            kg_company: "",
            kg_author_avatar: "",
            kg_author_name: "",
            kg_is_chosen: false,
            kg_ref_id: "",
            kg_ref_status: "",
            kg_code: null,
            kg_name: null,
            kg_type: null,
            kg_desc: null,
            kg_tags: [],
            kg_public: 0,
            kg_author_id: null,
            kg_icon: null,
            kg_status: '初始化',
            kg_sync_frequency: null,
            kg_url: null,
            rag_factor: 0.75,
            rag_relevant_threshold: 0.25,
            create_time: null,
            update_time: null,
            doc_cnt: 0
        }
    }
    // 切换到list
    await enter_kg_list()


}

export async function commit_new_kg(jump_flag:boolean = true, is_rebuild_all:boolean = false){
    if (!CurrentKg.value.kg_code){
        return
    }
    CurrentKg.value.kg_status = '构建中'
    let params = {
        kg_code: CurrentKg.value.kg_code,
        kg_name: CurrentKg.value.kg_name,
        kg_desc: CurrentKg.value.kg_desc,
        kg_tags: CurrentKg.value.kg_tags,
        kg_public: CurrentKg.value.kg_public,
        kg_icon: CurrentKg.value.kg_icon,
        kg_status: CurrentKg.value.kg_status,
        kg_url: CurrentKg.value.kg_url,
        kg_sync_frequency: CurrentKg.value.kg_sync_frequency,
        rag_factor: CurrentKg.value.rag_factor,
        rag_relevant_threshold: CurrentKg.value.rag_relevant_threshold,

    }
    let response = await update_kg(params)
    if (!response.error_status){
        CurrentKg.value = response.result
    }
    // 提交构建任务
    if (is_rebuild_all || CurrentKg.value.kg_type=='script' || CurrentKg.value.kg_type=='faq'){
        let params2 = {
            kg_db_code: CurrentKg.value.kg_code
        }
        let response2 = await kg_ref_build(params2)
        if (!response2.error_status){
            ElNotification.success({
                title:'系统通知',
                message: '更新知识库配置成功！',
                type: 'success',
                duration: 600
            })
        }
    }

    // 切换到list
    if(jump_flag){
        await enter_kg_list()
    }

}

export function handle_tag_close(tag:string){
    // @ts-ignore
    let index = CurrentKg.value.kg_tags.indexOf(tag)
    CurrentKg.value.kg_tags.splice(index, 1)
}


export function handleKgTagInputConfirm() {
    if (inputKgTagValue.value) {
        if (inputKgTagValue.value.length > 100) {
            ElNotification.warning({
                title:"系统通知",
                message: '标签过长！请不要超过100个字符',
                duration: 600
            })
            return
        }
        // @ts-ignore
        CurrentKg.value.kg_tags.push(inputKgTagValue.value)

    }
    inputKgTagVisible.value = false
    inputKgTagValue.value = ''
}

export async function showKgTagInput() {
    try{
        if  ( CurrentKg.value.kg_tags.length >= 8) {
            ElNotification.warning({
                title:'系统通知',
                message: '最多添加8个标签',
                type: 'warning',
                duration: 600
            })
            return
        }
    } catch (e) {

    }
    

    inputKgTagVisible.value = true
    await nextTick(() => {
        InputKgTagRef.value?.focus()
    })
}

export function get_upload_headers(){
    return {
        Authorization: 'Bearer ' + getToken()
    }
}
export function handle_upload_kg_avatar(res:any){

    CurrentKg.value.kg_icon = res.result
}
export function handle_upload_kg_avatar_exceed(files: File[]){
    upload_kg_avatar.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    upload_kg_avatar.value!.handleStart(file)
    upload_kg_avatar.value!.submit()

}

export function ValidKgMeta(){

    if (!CurrentKg.value.kg_name){
        ValidKgNameError.value = true
        ValidKgNameErrorMsg.value = '请输入知识库名称'
        return false
    }
    if (CurrentKg.value.kg_name.length > 200){
        ValidKgNameError.value = true
        ValidKgNameErrorMsg.value = '知识库名称过长！请不要超过200个字符！'
        return false
    }
    ValidKgNameError.value = false


    return true
}
export async function get_current_kg_docs(kg_code:string){
    let params = {
        doc_kg_db_id: kg_code,
        page_num: CurrentKgDocPageNum.value,
        page_size: CurrentKgDocPageSize.value,
    }
    if (CurrentKgDocKeyWord.value){
        params["doc_name"] = CurrentKgDocKeyWord.value
    }
    let response = await doc_search(params)
    if (!response.error_status && response.result.data.length){
        CurrentKgDocList.value = response.result.data
        current_kg_doc_list.value = response.result.data
        CurrentKgDocTotal.value = response.result.total
    }
}

export function show_kg_build_progress(){
    if (!CurrentKgBuildProgress.value.Success || !CurrentKgBuildProgress.value.Total){
        return 0
    }
    return Math.round((CurrentKgBuildProgress.value.Success/CurrentKgBuildProgress.value.Total)*100)
}

export async function check_kg_ref_progress(){

    if (!CurrentKg.value.kg_code){
        return false
    }
    let params = {
        kg_db_code: CurrentKg.value.kg_code
    }
    let response = await kg_ref_get(params)
    if (!response.error_status){
        CurrentKgBuildProgress.value = response.result

        let params = {
            page_size: CurrentKgDocPageSize.value,
            page_num: CurrentKgDocPageNum.value,
            doc_kg_db_id: CurrentKg.value.kg_code
        }
        if (CurrentKgDocKeyWord.value){

            params["doc_name"]= CurrentKgDocKeyWord.value
        }
        if (CurrentKgDocRefStatus !== null){
            params["doc_ref_status"] = CurrentKgDocRefStatus.value
        }
        if (!CurrentKg.value.kg_code){
            return false
        }
        let res = await doc_search(params)
        if (!res.error_status){

            CurrentKgDocTotal.value = res.result.total
            // 只更新文档的构建状态
            for (let i=0; i<res.result.data.length; i++){
                for (let j=0; j<current_kg_doc_list.value.length; j++){
                    if (current_kg_doc_list.value[j].doc_id === res.result.data[i].doc_id){
                        current_kg_doc_list.value[j].doc_ref_status = res.result.data[i].doc_ref_status
                    }
                }
            }
        }
    }
}
export async function enter_kg_list(){

    await router.push({
        name: 'kg_manage_list',
        query: {
            page_num: CurrentKgPageNum.value,
            page_size: CurrentKgPageSize.value
        }
    })

}
export async function enter_kg_detail(kg:KGMeta|null = null, info_type:string|null = null){
    if(!kg || !kg.kg_code){
        return false
    }
    if (!info_type){
        info_type = 'file'
    }

    // 必须是自己的知识库才需要调用
    if (check_kg_permission(kg, 'read')){
        let progress_params = {
            kg_db_code: kg.kg_code
        }
        let kg_ref_progress = await kg_ref_get(progress_params)
        if (!kg_ref_progress.error_status){
            CurrentKgBuildProgress.value = kg_ref_progress.result
        }
    }
    await get_current_kg(kg.kg_code)
    let kg_doc_params = {
        doc_kg_db_id: kg.kg_code,
        doc_name: CurrentKgDocKeyWord.value,
        page_size: CurrentKgDocPageSize.value,
        page_num: CurrentKgDocPageNum.value
    }
    let response2 = await doc_search(kg_doc_params)
    if (!response2.error_status){
        CurrentKgDocList.value = response2.result.data
        CurrentKgDocTotal.value = response2.result.total
        current_kg_doc_list.value = response2.result.data

    }
    CurrentKgDetail.value = info_type

    await router.push({
        name: 'kg_manage_detail',
        params: {
            kg_code: CurrentKg.value.kg_code
        },
        query: {
            info_type: info_type
        }
    })

}
export async function switch_kg_detail_type(type:string){
    CurrentKgDetail.value = type
    await router.replace({
        name: 'kg_manage_detail',
        params:{
          ...router.currentRoute.value.params
        },
        query: {
            ...router.currentRoute.value.query, // 保留当前的 query 参数
            info_type: type
        }
    });
}
export async function enter_kg_add(){
    dialog_v_add_kg.value=false
    CurrentKg.value = {
        kg_json_schema: {
            meta:{
                code: "",
                embedding:[]
            },
            properties:{},
            required:[],
            type: 'object'
        },
        kg_company: "",
        kg_author_avatar: "",
        kg_author_name: "",
        kg_is_chosen: false,
        kg_ref_id: "",
        kg_ref_status: "",
        kg_code: null,
        kg_name: null,
        kg_type: null,
        kg_desc: null,
        kg_tags: [],
        kg_public: 0,
        kg_author_id: null,
        kg_icon: null,
        kg_status: '初始化',
        kg_sync_frequency: null,
        kg_url: null,
        rag_factor: 0.75,
        rag_relevant_threshold: 0.25,
        create_time: null,
        update_time: null,
        doc_cnt: 0

    }
    CurrentKgDocList.value = []
    CurrentStage.value = 'meta'
    await router.push({
        name: 'kg_manage_add',
        query: {
            kg_type: CurrentKgType.value,
            stage: CurrentStage.value,
        }
    })
}
