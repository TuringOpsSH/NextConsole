export interface session_log_item{
    admin_session_favorite: number,
    admin_session_remark: number,
    assistant_name: string,
    msg_token_used:number,
    qa_cnt: number,
    rag_token_percentage: number,
    session_end_time: string,
    session_favorite: number,
    session_id: number,
    session_remark: number,
    session_topic: string,
    tag_name: string,
    tag_list:string[],
    user_id: string
}

export interface session_history_msg{
    admin_msg_remark: number,
    assistant_id: number,
    create_time: string,
    msg_attachment_list: [
        number
    ],
    msg_content: string,
    msg_del: number,
    msg_format: string,
    msg_id: number,
    msg_inner_content:  {
        content: string,
        role: string
    },
    msg_llm_type: string,
    msg_parent_id: number,
    msg_prompt: [
        {
            content: string,
            role: string
        }
    ],
    msg_remark: number,
    msg_role: string,
    msg_time_used: number,
    msg_token_used: number,
    msg_version: number,
    qa_id: number,
    session_id: number,
    shop_assistant_id: number,
    update_time: string,
    user_id: number
}
