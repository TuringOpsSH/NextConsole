import router from "@/router";
import {reactive, ref} from "vue";
import {DataSetMeta} from "@/types/dataset_center";
import {add_dataset, delete_dataset, search_dataset, search_instructions} from "@/api/dataset_center";
import {assistant_instruction} from "@/types/assistant";
import {ElNotification} from "element-plus";
import type { FormInstance, FormRules } from 'element-plus'
export const data_set_list = ref<DataSetMeta[]>([]);
export const data_set_page_num = ref(1)
export const data_set_page_size = ref(10)
export const data_set_page_total = ref(0)
export const data_set_add_form = ref()
export const data_set_add_model = reactive<DataSetMeta>({
    id: 0,
    dataset_name: '',
    dataset_type: '指令',
    dataset_desc: '',
    user_id: null,
    instruction_id:null,
    dataset_status: 0,
    create_time: '',
    update_time: ''

})
export const data_set_instructions_list = ref<assistant_instruction[]>()
export const data_set_add_rules = reactive<FormRules<DataSetMeta>>({
    dataset_name: [
        { required: true, message: '请输入数据集名称', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
    ],
    dataset_type: [
        { required: true, message: '请选择数据集类型', trigger: 'change' }
    ],
    instruction_id: [
        { required: true, message: '请选择指令', trigger: 'change' }
    ]
})

export async function add_new_data_set(){
    await router.push({
        name: 'dataset_add',
        query: {
            "data_set_id": 0
        }
    })
}
export async function cancel_add_new_data_set(){
    data_set_add_model.dataset_name = ''
    data_set_add_model.dataset_desc = ''
    data_set_add_model.dataset_type = '指令'
    data_set_add_model.instruction_id = null
    await router.push({
        name: 'dataset_list',
        query: {
            page_num: data_set_page_num.value,
            page_size: data_set_page_size.value,
        }
    })

}
export async function get_data_set_list(){

    let params = {
        page_num: data_set_page_num.value,
        page_size: data_set_page_size.value,
        order: "create_time",
    }
    let res = await search_dataset(params)
    if (!res.error_status){
        data_set_list.value = res.result.data
        data_set_page_total.value = res.result.total
        await router.push(
            {
                name: 'dataset_list',
                query: {
                    page_num: data_set_page_num.value,
                    page_size: data_set_page_size.value,
                }
            }
        )
    }
}
export async function hand_data_set_size_change(val:number){
    data_set_page_size.value = val
    await get_data_set_list()
}
export async function hand_data_set_page_change(val: number) {
    data_set_page_num.value = val
    await get_data_set_list()
}

export async function edit_data_set_meta(data_set: DataSetMeta){
    console.log(data_set)
    await router.push({
        name: 'dataset_meta',
         params:{
             dataset_id: data_set.id
         }
    })
}
export async function show_data_set_sample_list(data_set: DataSetMeta){
    await router.push({
        name: 'data_sample_list',
        params:{
            dataset_id: data_set.id
        }
    })
}
export async function get_all_available_instructions(){
    let res = await search_instructions({})
    if (!res.error_status) {
        data_set_instructions_list.value = res.result
    }
}
export async function submit_new_data_set_form(data_set_add_form: FormInstance){
    // todo 校验
    if (!data_set_add_form) return
    try {
        let valid_res = await data_set_add_form.validate()
        if (!valid_res) return
    }catch (e) {
        return
    }
    if (!data_set_add_model.instruction_id){
        return
    }
    let params = {
        dataset_name: data_set_add_model.dataset_name,
        dataset_desc: data_set_add_model.dataset_desc,
        dataset_type: data_set_add_model.dataset_type,
        instruction_id: data_set_add_model.instruction_id
    }
    let res = await add_dataset(params)
    if (!res.error_status){
        ElNotification({
            title: '成功',
            message: '数据集创建成功！',
            type: 'success'
        })
        await cancel_add_new_data_set()
    }
}
export async function delete_data_set(data_set: DataSetMeta){
    let params = {
        "dataset_id": data_set.id
    }
    let res = await delete_dataset(params)
    if (!res.error_status){
        ElNotification({
            title: '成功',
            message: '数据集删除成功！',
            type: 'success'
        })
        await get_data_set_list()
    }
}
