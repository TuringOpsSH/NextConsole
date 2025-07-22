import {ref} from "vue";
import {assistant_instruction} from "@/types/assistant";
import {get_dataset_sample, search_instructions, upsert_tags} from "@/api/dataset_center";
import {current_data_sample} from "@/components/dataset_center/data_samples";
import {DataSetSampleTagsMap} from "@/types/dataset_center";
import {ElNotification} from "element-plus";

export const current_tags_instruction = ref<assistant_instruction>(null)
export const current_sample_tags = ref<DataSetSampleTagsMap[]>()
export async function get_current_data_sample(dataset_id: number,data_sample_id:number){
    let res = await get_dataset_sample(
        {
            dataset_id: dataset_id,
            data_sample_id: data_sample_id,
            with_tags: true
        }
    );
    if (!res.error_status){
        current_data_sample.value = res.result;
        current_sample_tags.value = current_data_sample.value.tags

        await get_current_tags_instruction()
    }

}

export async function get_current_tags_instruction(){

    let params = {
        instruction_ids: [current_data_sample.value.instruction_id]
    }
    let res = await search_instructions(params)
    if (!res.error_status) {
        if (res.result.length > 0){
            current_tags_instruction.value = res.result[0]
        }
        else {
            current_tags_instruction.value = null
        }
    }
}




export async function update_current_data_sample_tags(){
    let params = {
        dataset_sample_id : current_data_sample.value.id,
        tags: []
    }
    for (let key in current_sample_tags.value){
        params.tags.push(current_sample_tags.value[key])
    }
    let res = await upsert_tags(params)
    if (!res.error_status){
        ElNotification.success({
            title: '提示',
            message: '标签更新成功',
            type: 'success'
        })
    }
}
