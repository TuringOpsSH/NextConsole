import {assistant_delete, assistant_search, assistant_update} from "@/api/assistant_center";
import {ElMessage} from "element-plus";
import {nextTick, ref} from "vue";
import {assistant} from "@/types/assistant";

export const assistant_key_word = ref('') // 搜索关键字
export const assistantList = ref<Array<assistant>>([])
export const assistants_cnt = ref(0)

export const current_page_num = ref(1);
export const current_page_size = ref(20);
export const assistant_order = ref('create_time');

export const assistant_filter = ref();
export const assistant_delete_vis = ref(false)
export const assistant_deleted = ref<assistant>(
    {
        assistant_publish_shop_id: null,
        comments: undefined,
        assistant_author_avatar: "",
        assistant_author_id: "",
        assistant_author_name: "",
        id: null,
        assistant_name: '',
        assistant_desc: '',
        assistant_status: '创建',
        assistant_tags: [],
        assistant_role_prompt: '',
        assistant_avatar: 'images/logo.svg',
        assistant_language: '中文',
        assistant_voice: '',
        assistant_memory_size: 4,
        assistant_model_name: 'deepseek-chat',
        assistant_model_type: 'chat',
        assistant_model_temperature: 1,
        assistant_model_icon: 'images/openai.svg',
        create_time: '',
        update_time: '',
        assistant_knowledge_base: [],
        assistant_function_lists: [],
        assistant_source: 1,
        authority_create_time: "",
        authority_value: 0,
        assistant_is_start: false,
        call_cnt: 0,
        is_shop_assistant: false,
        rag_factor: 0.75,
        rag_miss: 1,
        rag_miss_answer: "对不起，没有从知识库中找到相关信息！",
        rag_relevant_threshold: 0.25,
        assistant_avatar_url: '',

    })
export const show_cnt_tag = ref(false);
export async function start_assistant(assistant: assistant) {
    let params = {
        "id": assistant.id,
        "operate_type": assistant.assistant_is_start ?  "start": "stop",
    }
    let res = await assistant_update(params)
    if (!res.error_status) {
        let msg = assistant.assistant_is_start ? '启用成功！' : '停用成功！'
        ElMessage.success({
            message: msg,
            type: 'success',
            duration: 600
        })
    }

}

export async function handle_current_change(val: number) {
    current_page_num.value = val;
    await get_assistant_list()

}



export async function change_order(order: string) {
    assistant_order.value = order;
    show_cnt_tag.value = order === 'call_cnt';
    await get_assistant_list()

}

export async function get_assistant_list() {
    let params = {
        "page_num": current_page_num.value,
        "page_size": current_page_size.value,
        'order': assistant_order.value,
        'assistant_is_start': assistant_filter.value,
    }
    if (assistant_key_word.value) {
        params["assistant_name"] = assistant_key_word.value
        params["assistant_desc"] = assistant_key_word.value
        params["assistant_tags"] = assistant_key_word.value
    }
    let res = await assistant_search(params)
    if (!res.error_status) {
        assistantList.value = res.result.data
        assistants_cnt.value = res.result.cnt
    }
}
export async function delete_assistants() {
    let params = {
        "assistant_ids": [assistant_deleted.value.id],
    }
    let res = await assistant_delete(params)
    if (!res.error_status) {
        ElMessage.success({
            message: '删除成功',
            type: 'success',
            duration: 600
        })
        for (let i = 0; i < assistantList.value.length; i++) {
            if (assistantList.value[i].id === assistant_deleted.value.id) {
                assistantList.value.splice(i, 1)
                break
            }
        }
        assistants_cnt.value -= 1
        assistant_delete_vis.value = false
        await nextTick()
    }
}


export async function change_page(step: number) {
    let max_page = Math.ceil(assistants_cnt.value / current_page_size.value)
    if (current_page_num.value + step > max_page || current_page_num.value + step < 1) {
        ElMessage.info({
            message: '到头啦！',
            type: 'info',
            duration: 600
        })
        return
    }
    current_page_num.value += step;
    await get_assistant_list()
    await nextTick()

}
