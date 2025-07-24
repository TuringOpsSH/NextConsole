import {assistant} from "@/types/assistant";

export interface session_item{
    id: number,
    session_code?: string | null,
    user_id?: number,
    session_topic?: string,
    session_status?: string,
    session_remark?: number,
    session_vis?: number,
    session_favorite?: number,
    session_like_cnt?: number,
    session_dislike_cnt?: number,
    session_share_cnt?: number,
    session_update_cnt?: number,
    session_assistant_id?: number|null,
    session_assistant_name?: string|null,
    session_assistant_desc?: string|null,
    session_assistant_avatar?: string |null,
    session_shop_assistant_id?: number|null,
    session_shop_assistant_name?: string|null,
    session_shop_assistant_desc?: string|null,
    session_shop_assistant_avatar?: string |null,
    session_task_id?: string |null,
    session_source?: string |null,
    session_task_type?: string |null,
    session_search_engine_switch?: boolean |null,
    session_search_engine_resource_type?: string |null,
    session_search_engine_language_type?: object |null,
    session_local_resource_switch?: boolean | null,
    session_local_resource_use_all?: boolean | null,
    session_attachment_image_switch?: boolean | null,
    session_attachment_file_switch?: boolean | null,
    session_attachment_webpage_switch?: boolean | null,
    session_llm_code?: string | null,
    create_time?: string,
    update_time?: string,
    is_edit?: boolean | null,
    history_is_edit?: boolean | null,
    session_summary?: string | null,
    session_customer_score?: number | null,
    session_customer_evaluation?: string | null,
    session_evaluation_close?:boolean | null,
    session_stream?: boolean | null,
    session_task_params_schema?: Record<string, unknown>;
    session_task_params?: Record<string, unknown>;
}
export interface qa_item{
    qa_id: number,
    user_id: number,
    session_id: number,
    qa_del: number,
    qa_status: string,
    qa_topic: string,
    create_time: string,
    update_time: string,
}
export interface msg_item{
    msg_id: number | null,
    user_id: number | null,
    session_id: number | null,
    qa_id: number | null,
    assistant_id: number| null,
    shop_assistant_id: number | null,
    msg_format: string | null,
    msg_llm_type: string | null,
    msg_role: string | null,
    msg_prompt: string | null,
    msg_content : string | null,
    msg_content_finish_html: string[] | null,
    msg_token_used: number | null,
    msg_time_used: number | null,
    msg_remark: number | null,
    msg_del: number | null,
    msg_version :number | null,
    msg_parent_id :number | null,
    msg_reference_finish: boolean | null,
    attachment_list?: SessionAttachment[] | null,
    create_time: string | null,
    update_time: string | null,
    assistant_avatar?: string | null,
    msg_is_selected?: boolean | null,
    assistant_name?: string | null,
    assistant_title?: string | null,
    assistant_desc?: string | null,
    assistant_tags?: string [] | null,
    msg_reason_content_finish_html?: string[] | null,
}
export interface msg_queue_item {
    qa_id: number,
    qa_status?: string,
    qa_value: {
        question: msg_item[],
        answer: {
            [key: number] : msg_item[]
        }
    },
    qa_topic?: string,
    qa_share_picked?: number,
    qa_workflow_open?: boolean,
    qa_is_cut_off?: boolean,
    show_button_question_area?: boolean | null,
    show_button_answer_area?: boolean | null,
    short_answer?: boolean | null,
    qa_finished?: boolean | null,
    qa_assistant?: assistant | null,
    qa_is_last?: boolean | null,
    session_id?: number | null,
}
export interface reference_item{
    resource_id:  string | number,
    resource_icon: string,
    resource_name: string,
    resource_title: string,
    ref_text: string,
    source_type: string,
}
export interface recommend_question_item {
    id: number,
    msg_id: number,
    msg_content: string,
    recommend_question: string,
    is_click:number,
    create_time: string,
    update_time: string,

}
export interface reference_map{
    [key: number]: reference_item[]
}
export interface recommend_question_map{
    [key: number]: recommend_question_item[]
}
export interface running_question_meta {
    qa_item_idx: number,
    begin_time : number,
    end_time : number | null,
    status: string | null,
    abort_controller: AbortController | null,

}
export interface workflow_task_item{
    session_id?: number ,
    qa_id: number | null,
    msg_id: number | null,
    task_id: number | null,
    task_type: string | null,
    task_instruction: string | null,
    task_params: {
        system_params: {
            message_text: string,
        },
        user_params: {
            query_text: string,
        },

    }   ,
    task_result: string| null,
    task_create_time: string| null,
    task_begin_time: string| null,
    task_update_time: string| null,
    task_end_time: string| null,
    task_status: string| null,
}
export interface workflow_task_map{
    [key: number]: workflow_task_item[]
}
export interface session_attachment_relation{
    id: number,
    session_id: number,
    qa_id: number,
    msg_id: number,
    resource_id: number,
    attachment_source: string,
    rel_status: string,
    create_time: string,
    update_time: string,
}
export interface SessionAttachment{
    session_id?:number
    qa_id?:number
    msg_id?:number
    user_id?:number
    id?:number
    resource_type:string
    resource_name:string
    resource_icon:string
    resource_url:string
    resource_size:number
    resource_desc:string
    resource_format?:string
    resource_feature_code:string
    resource_status:string
    create_time:string
    update_time:string
}
