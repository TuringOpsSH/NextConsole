import router from "@/router";
import {ref} from "vue";
import {DataSetSample, DataSetSampleTagFilter, TagFilter} from "@/types/dataset_center";
import {
    delete_dataset_sample, download_dataset_sample,
    get_data_sample_context_msg,
    get_dataset,
    search_dataset_sample
} from "@/api/dataset_center";
import {ElNotification} from "element-plus";
import {json_schema} from "@/types/assistant";
import {get_current_data_sample} from "@/components/dataset_center/data_sample_tags";
import {msg_queue_item} from "@/types/next_console";

export const data_set_sample_list = ref<DataSetSample[]>([]);
export const data_set_sample_page_num = ref(1)
export const data_set_sample_page_size = ref(1000)
export const data_set_sample_page_total = ref(0)
export const current_data_set_id = ref(0)
export const current_params_json_schema = ref<json_schema>()
export const current_result_json_schema = ref<json_schema>()
export const current_sample_key_work = ref('')
export const current_tags_filter = ref<DataSetSampleTagFilter>({})
export const current_data_sample = ref<DataSetSample>({
    msg_content: "",
    session_id: 0, user_id: 0, user_name: "",
    id: 0,
    msg_id: 0,
    instruction_id: 0,
    sample_desc: '',
    sample_model_name: '',
    sample_params: {},
    sample_prompt: '',
    sample_result: '',
    sample_status: '',
    create_time: '',
    update_time: '',
    tags:  null
})
export const show_target_data_sample_drawer = ref(false)
export const data_sample_detail_loading = ref(false)
export const current_smale_detail_model = ref('sample')
export const current_smale_context = ref<msg_queue_item[]>([])
export const current_selected_data_samples = ref<DataSetSample[]>()
export const download_loading = ref(false)
export async function get_data_set_sample_list(){
    if (!current_data_set_id.value){
        ElNotification.warning({
            title: '提示',
            message: '请先选择数据集',
            type: 'warning'
        })
        await router.push(
            {
                name: 'dataset_list',
                query: {
                    page_num: 1,
                    page_size: 1000,
                }
            }
        )
    }
    let params = {
        data_set_id: current_data_set_id.value,
        page_num: data_set_sample_page_num.value,
        page_size: data_set_sample_page_size.value,
        msg_key_word: current_sample_key_work.value,
        with_tags: true,
        tags_filter: current_tags_filter.value
    }
    let res = await search_dataset_sample(params)
    if (!res.error_status){
        data_set_sample_list.value = res.result.data
        data_set_sample_page_total.value = res.result.total
        router.push(
            {
                name: 'data_sample_list',
                params:{
                    dataset_id: current_data_set_id.value
                },
                query: {
                    page_num: data_set_sample_page_num.value,
                    page_size: data_set_sample_page_size.value,
                }
            }
        )
    }

}
export async function hand_data_set_size_change(val:number){
    data_set_sample_page_size.value = val
    await get_data_set_sample_list()
}
export async function hand_data_set_page_change(val: number) {
    data_set_sample_page_num.value = val
    await get_data_set_sample_list()
}
export async function get_data_set_tag_json_schema(){
    let res = await get_dataset(
        {
            dataset_id: current_data_set_id.value
        }
    )
    if (!res.error_status){
        current_params_json_schema.value = res.result.params_json_schema
        current_result_json_schema.value = res.result.result_json_schema
        for (let key in current_result_json_schema.value.properties){
            current_tags_filter.value[key] = {
                tag_name: key,
                tag_value_history: [],
                tag_value_correct: [],
                tag_result: []
            }
        }
    }
}
export async function show_data_set_sample_meta(row: DataSetSample){
    show_target_data_sample_drawer.value = true
    data_sample_detail_loading.value = true
    await get_current_data_sample(current_data_set_id.value, row.id)
    await get_data_sample_context()
    data_sample_detail_loading.value = false

}
export async function delete_data_set_samples(row:DataSetSample){
    let params = {
        data_sample_id_list: [row.id]
    }
    let res = await delete_dataset_sample(params)
    if (!res.error_status){
        ElNotification.success({
            title: '提示',
            message: '删除成功',
            type: 'success'
        })
        await get_data_set_sample_list()
    }
}
export async function check_next_data_sample(direction:number){
     // 找到当前数据样本的下一个数据样本的id
    if (!current_data_sample.value.id){
        ElNotification.warning({
            title: '提示',
            message: '请先选择数据样本',
            type: 'warning'
        })
        return
    }
    let index = data_set_sample_list.value.findIndex(item => item.id === current_data_sample.value.id)

    index = index + direction
    if (index < 0 ){
        ElNotification.warning({
            title: '提示',
            message: '已经是第一个数据样本',
            type: 'warning'
        })

        return
    }
    if (index >= data_set_sample_list.value.length){
        ElNotification.warning({
            title: '提示',
            message: '已经是最后一个数据样本',
            type: 'warning'
        })
        return
    }
    let next_data_sample = data_set_sample_list.value[index]
    await show_data_set_sample_meta(next_data_sample)

}
export async function get_data_sample_context(){
    if (!current_data_sample.value.id){
        return
    }
    let params = {
            data_sample_id: current_data_sample.value.id
    }
    let res = await get_data_sample_context_msg(params)
    if (!res.error_status){
        current_smale_context.value = res.result
    }
}
export function get_all_selected_data_samples(val: DataSetSample[]){
    current_selected_data_samples.value = val
}
export async function batch_download_data_samples(){
    // 获取所有勾选的数据
    if (!current_selected_data_samples.value?.length){
        ElNotification.warning({
            title:"系统通知",
            message:"请先勾选需要删除的样本！",
            duration:666
        })
        return
    }
    let params = {
        data_sample_id_list : []
    }
    for (let i = 0; i< current_selected_data_samples.value.length; i++){
        params.data_sample_id_list.push(
            current_selected_data_samples.value[i].id
        )

    }
    download_loading.value = true
    await download_dataset_sample(params)
    ElNotification.success(
        {
            title:"系统通知",
            message:"下载成功！",
            duration:666
        }
    )
    download_loading.value = false
}
export async function batch_delete_data_samples(){
    if (!current_selected_data_samples.value?.length){
        ElNotification.warning({
            title:"系统通知",
            message:"请先勾选需要删除的样本！",
            duration:666
        })
        return
    }
    let params = {
        data_sample_id_list : []
    }
    for (let i = 0; i< current_selected_data_samples.value.length; i++){
        params.data_sample_id_list.push(
            current_selected_data_samples.value[i].id
        )

    }
    let res = await delete_dataset_sample(params)
    if (!res.error_status){
        await get_data_set_sample_list()
        ElNotification.success(
            {
                title:"系统通知",
                message:"删除成功！",
                duration:666
            }
        )
    }


}
