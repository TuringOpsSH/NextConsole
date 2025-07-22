import {ref} from "vue";
import {llmInstanceSearch} from "@/api/config_center";
import {LLMInstance} from "@/types/config_center";
import {current_session} from "@/components/next_console/messages_flow/sessions";
import {update_session} from "@/api/next_console";
import {ElMessage} from "element-plus";
// import {model_list_Ref} from "@/components/next_console/messages_flow/console_input";

export const llm_instance_queue = ref<LLMInstance[]>([]);
export async function search_llm_instance() {
    let data = await llmInstanceSearch({})
    if (!data.error_status){
        llm_instance_queue.value = data.result.data
    }

}
export async function  switch_llm_instance(item:LLMInstance){
    // 切换llm_instance
    // welcome界面
    if (!current_session?.id){

        current_session.session_llm_code = item.llm_code
        // model_list_Ref.value?.hide()
        ElMessage.success("切换成功!")
        // // console.log('item', item.llm_code, current_session.session_llm_code)
        return
    }
    let params = {
        session_id : current_session.id,
        session_llm_code: item.llm_code,
    }
    let data = await update_session(params)
    if (!data.error_status){
        current_session.session_llm_code = item.llm_code
        // model_list_Ref.value?.hide()
        ElMessage.success("切换成功!")
    }
}

export function get_session_llm_name(){
    let current_llm_name = '火山引擎/DeepSeek-V3'
    if (current_session.session_llm_code){
        for (let i = 0; i < llm_instance_queue.value.length; i++) {
            if (llm_instance_queue.value[i].llm_code === current_session.session_llm_code){
                current_llm_name = llm_instance_queue.value[i].llm_desc
                if (window.innerWidth < 768){
                    current_llm_name = llm_instance_queue.value[i].llm_type
                }
                break
            }
        }
    }
    return current_llm_name
}
