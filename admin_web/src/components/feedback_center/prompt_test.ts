import {ref} from "vue";
import {msg_item} from "@/types/next_console";
import {assistant_instruction} from "@/types/assistant";
import {
    add_dataset_sample,
    dryrun_dataset_sample, extract_result,
    get_relate_dataset,
    get_tags,
    search_dataset,
    search_dataset_sample,
    search_instructions,
    update_relate_dataset,
    upsert_tags
} from "@/api/dataset_center";
import {ElMessage, ElNotification} from "element-plus";
import {DataSetMeta, DataSetSample, DataSetSampleTag, DataSetSampleTagsMap} from "@/types/dataset_center";

export const prompt_test_dialog = ref(false)
export const assistant_instructions   = ref<assistant_instruction[]>([])
export const current_question = ref<msg_item>(null)
export const current_assistant_instruction = ref<assistant_instruction>(null)
export const current_assistant_instruction_name = ref("PolicySchedule")
export const current_dry_run_params = ref({})
export const current_dry_run_tags = ref<DataSetSampleTagsMap>({})
export const current_dry_run_result = ref('')
export const current_dry_run_loading = ref(false)
export const current_dry_run_result_extract_loading = ref(false)
export const current_data_sample = ref<DataSetSample> ()
export const current_data_relate_set = ref<DataSetMeta[]>()
export const available_data_set_list = ref<DataSetMeta[]>([])
export const tags_type = ref("history")
export async function showPromptTestDialog(msg:msg_item) {
    // 打开对话框并初始化数据：指令列表
    prompt_test_dialog.value = true
    current_question.value = msg
    // 指令列表
    let params = {}
    let res = await search_instructions(params)
    if (!res.error_status) {
        assistant_instructions.value = res.result
    }
    // 默认指令
    for (let i = 0; i < assistant_instructions.value.length; i++) {
        if (assistant_instructions.value[i].instruction_name === current_assistant_instruction_name.value) {
            await switch_current_assistant_instruction(current_assistant_instruction_name.value)
            break
        }
    }

}
export async function switch_current_assistant_instruction(instruction_name:string){
    let instruction = null;
    for (let i = 0; i < assistant_instructions.value.length; i++) {
        if (assistant_instructions.value[i].instruction_name === instruction_name) {
            instruction = assistant_instructions.value[i]
            break
        }
    }
    current_assistant_instruction.value = instruction
    // 获取dry run参数，并设置参数的默认值
    if (current_assistant_instruction.value?.instruction_params_json_schema) {
        let instruction_params_json_schema = current_assistant_instruction.value.instruction_params_json_schema?.properties
        for (let key in instruction_params_json_schema) {
            current_dry_run_params.value[key] = instruction_params_json_schema[key].default
            current_dry_run_tags.value[key] = {
                id: null,
                data_sample_id: null,
                tag_name: key,
                tag_desc: instruction_params_json_schema[key].title,
                tag_type: instruction_params_json_schema[key].type,
                tag_value_correct: instruction_params_json_schema[key].default,
                tag_value_history: null,
                tag_value_comment: null,
                tag_source: null,
                tag_status: null,
                create_time: null,
                update_time: null,
            }
        }
    }
    // 设置结果的默认值
    if(current_assistant_instruction.value?.instruction_result_json_schema){
        let instruction_result_json_schema = current_assistant_instruction.value.instruction_result_json_schema?.properties
        for (let key in instruction_result_json_schema) {
            current_dry_run_tags.value[key] = {
                    id: null,
                    data_sample_id: null,
                    tag_name: key,
                    tag_desc: instruction_result_json_schema[key].title,
                    tag_type: instruction_result_json_schema[key].type,
                    tag_value_correct: instruction_result_json_schema[key].default,
                    tag_value_history: null,
                    tag_value_comment: null,
                    tag_source: null,
                    tag_status: null,
                    create_time: null,
                    update_time: null,
                }
        }
    }
    // 获取数据集列表
    await get_available_data_set()

    // 获取数据样本,并尝试覆盖默认值
    await get_data_sample()

}
export async function dry_run_instruction(){
    current_dry_run_loading.value = true
    let params = {
        msg_id: current_question.value.msg_id,
        instruction_name: current_assistant_instruction_name.value,
        instruction_params: current_dry_run_params.value
    }
    let res = await dryrun_dataset_sample(params)
    if (!res.error_status) {
        current_dry_run_result.value = res.result
    }
    current_dry_run_loading.value = false
    // 将dry参数的值更新到tags中
    for (let key in current_dry_run_params.value) {
        current_dry_run_tags.value[key].tag_value_history = current_dry_run_params.value[key]
    }

    // 将dry参数的值更新到tags中
    current_dry_run_result_extract_loading.value = true
    let result_params = {
        instruction_id : current_assistant_instruction.value.id,
        instruction_result: res.result
    }
    let instruction_res = await extract_result(result_params)
    if (!instruction_res.error_status) {
        for (let key in instruction_res.result) {
            // 去json_schema 中找到对应的tag_name
            let tag_name = ""
            for (let k in current_assistant_instruction.value.instruction_result_json_schema.properties) {
                if (current_assistant_instruction.value.instruction_result_json_schema.properties[k].title === key) {
                    tag_name = k
                    break
                }
            }
            if (tag_name){
                current_dry_run_tags.value[tag_name].tag_value_history = instruction_res.result[key]
                current_dry_run_tags.value[tag_name].tag_value_correct = instruction_res.result[key]
            }


        }
    }
    current_dry_run_result_extract_loading.value = false
}
export async function get_available_data_set(){
    let params = {}
    let res = await search_dataset(params)
    if (!res.error_status) {
        available_data_set_list.value = res.result.data
    }
}
export async function get_data_sample(){
    let params = {
        msg_id_list: [current_question.value.msg_id],
        instruction_id_list : [current_assistant_instruction.value.id]
    }
    let res = await search_dataset_sample(params)
    if (!res.error_status) {
        if ( res.result.data.length > 0){
            current_data_sample.value = res.result.data[0]
            get_data_relate_set()
            get_data_sample_tags()
        }

        else {
            current_data_sample.value = null
            current_data_relate_set.value = []

        }
    }

}
export async function get_data_relate_set(){
    let params = {
        data_sample_id: current_data_sample.value.id
    }
    let res = await get_relate_dataset(params)
    if (!res.error_status) {
        current_data_relate_set.value = res.result
    }
}
export async function add_new_data_sample(){
    let params = {
        msg_id: current_question.value.msg_id,
        instruction_id: current_assistant_instruction.value.id,
        sample_params: current_dry_run_params.value,
        sample_result: current_dry_run_result.value,
    }
    let res = await add_dataset_sample(params)
    if (!res.error_status) {
        current_data_sample.value = res.result
    }
}
export async function update_data_sample_relations(){
    // 如果没有样本值，则先创建样本数据，
    if (!current_data_sample.value){
        await add_new_data_sample()
    }

    // 更新关联数据集
    let params = {
        data_sample_id: current_data_sample.value.id,
        relate_dataset_ids: []

    }
    for (let i = 0; i < current_data_relate_set.value.length; i++) {
        params.relate_dataset_ids.push(current_data_relate_set.value[i].id)
    }
    let res = await update_relate_dataset(params)
    if(!res.error_status){
        current_data_relate_set.value = res.result
        ElNotification({
            title: '系统通知',
            message: '关联数据集更新成功',
            type: 'success',
            duration: 666
        })
    }
}
export async function update_data_sample_tags(){
    if (!current_data_sample.value){
        await add_new_data_sample()
    }
    let params = {
        dataset_sample_id: current_data_sample.value.id,
        tags: []
    }
    for (let key in current_dry_run_tags.value) {
        let sub_tag= <DataSetSampleTag>{
            tag_name: key,
            tag_desc: current_dry_run_tags.value[key].tag_desc,
            tag_type: current_dry_run_tags.value[key].tag_type,
            tag_value_history: current_dry_run_tags.value[key].tag_value_history,
            tag_value_correct: current_dry_run_tags.value[key].tag_value_correct,
        }
        if (current_dry_run_tags.value[key].id){
            sub_tag.id = current_dry_run_tags.value[key].id
        }
        params.tags.push(sub_tag)
    }
    let res = await upsert_tags(params)
    if (!res.error_status) {
        current_dry_run_tags.value = {}
        for (let i = 0; i < res.result.length; i++) {
            current_dry_run_tags.value[res.result[i].tag_name] = res.result[i]
        }
        ElNotification({
            title: '系统通知',
            message: '标签更新成功',
            type: 'success',
            duration: 666
        })

    }
    await update_data_sample_relations()
}
export async function get_data_sample_tags(){
    let params = {
        dataset_sample_id: current_data_sample.value.id
    }
    let res = await get_tags(params)
    if (!res.error_status) {

        for (let i = 0; i < res.result.length; i++) {
            current_dry_run_tags.value[res.result[i].tag_name] = res.result[i]
        }
    }
}
