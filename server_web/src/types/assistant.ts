import {KGMeta} from "@/types/kg";

export interface comment {
    id: number,
    comment_content: string,
    comment_level: number,
    create_time: string,
    update_time: string,
    user_id: number,
    assistant_id: number,
    user_avatar: string,
    user_name: string,

}


export interface assistant {
    id: number,
    assistant_name: string,
    assistant_desc: string,
    assistant_status: string,
    assistant_source: number,
    assistant_tags: Array<string>,
    assistant_role_prompt: string,
    assistant_avatar: string,
    assistant_avatar_url : string | null,
    assistant_language: string,
    assistant_voice: string,
    assistant_memory_size: number,
    assistant_model_name: string,
    assistant_model_type: string,
    assistant_model_temperature: number,
    assistant_model_icon: string,
    assistant_publish_shop_id: number| null,
    create_time: string,
    update_time: string,
    assistant_author_id: string,
    assistant_author_name: string,
    assistant_author_avatar: string,
    authority_value: number,
    assistant_is_start: boolean,
    authority_create_time: string,
    call_cnt: number,
    assistant_knowledge_base: Array<KGMeta> |null,
    rag_miss : number |null,
    rag_miss_answer: string |null,
    rag_factor : number |null,
    rag_relevant_threshold : number | null,
    assistant_function_lists: Array<object>,
    comments: Array<comment> | null,
    is_shop_assistant: boolean | null,
    assistant_title: string | null,
}


export interface shop_assistant {
    id: number,
    assistant_name: string,
    assistant_desc: string,
    assistant_status: string,
    assistant_source: number,
    assistant_tags: Array<string>,
    assistant_role_prompt: string,
    assistant_avatar: string,
    assistant_avatar_url : string | null,
    assistant_language: string,
    assistant_voice: string,
    assistant_memory_size: number,
    assistant_model_name: string,
    assistant_model_type: string,
    assistant_model_temperature: number,
    assistant_model_icon: string,
    assistant_publish_shop_id: number| null,
    create_time: string,
    update_time: string,
    assistant_author_id: string,
    assistant_author_name: string,
    assistant_author_avatar: string,
    authority_value: number,
    assistant_is_start: boolean,
    authority_create_time: string,
    call_cnt: number,
    assistant_knowledge_base: Array<KGMeta> |null,
    rag_miss : number |null,
    rag_miss_answer: string |null,
    rag_factor : number |null,
    rag_relevant_threshold : number | null,
    assistant_function_lists: Array<object>,
    comments: Array<comment> | null,
    docs_cnt: number | null,
    tools_cnt: number | null,
    commands_cnt: number | null,
    avg_level: number | null,
    subscribe_rank: number | null,
    subscribe_range: number | null,
    is_shop_assistant: boolean | null,
}
