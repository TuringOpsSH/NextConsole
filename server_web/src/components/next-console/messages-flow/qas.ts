import {qa_item} from "@/types/next-console";
import {ref} from "vue";
import {current_session} from "@/components/next-console/messages-flow/sessions";
import {user_input} from "@/components/next-console/messages-flow/console_input";
import {create_qa, search_qa} from "@/api/next-console";

export const qa_list = ref<qa_item[]>([])
export const current_qa_id = ref()

export async function add_new_qa() {
    let params = {
        "session_id": current_session.id,
        "qa_topic": user_input.value,
    }
    let data = await create_qa(params)
    qa_list.value.unshift(data.result)
    return data.result
}
export async function get_lasted_qa() {
    // 获取最新qa
    if (!current_session.id){
        qa_list.value = []
        return false
    }
    let params = {
        "session_id": [],
    }
    // for (let i = 0; i < session_list.value.length; i++) {
    //     params.session_id.push(session_list.value[i].id)
    // }
    params.session_id.push(current_session.id)
    let data = await search_qa(params)
    qa_list.value = data.result
}
