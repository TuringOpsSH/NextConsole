import {ResourceItem} from "@/types/resource-type";

export interface SupportTicket{
    actions_token?: string;
    close_time?: string;
    consult_outline?: string;
    consult_topic?: string;
    contact_information?: string;
    contact_person?: string;
    create_time: string;
    delete_time?: string;
    finish_time?: string;
    hardware_desc?: string;
    hardware_status?: string;
    id: number;
    installation_media_status?: string;
    key_measurements?: string;
    os_type?: string;
    os_version?: string;
    product_name?: string;
    product_type?: string;
    product_version?: string;
    requirements?: string;
    service_type?: string;
    special_requirements?: string;
    start_time?: string;
    support_channel?: string[];
    trace_logs?: string;
    ticket_code?: string;
    ticket_deadline?: string;
    ticket_desc: string;
    ticket_evaluation?: string;
    ticket_level?: number;
    ticket_price?: string;
    ticket_priority?: number;
    ticket_score?: number;
    ticket_session_id?: number;
    ticket_source?: string;
    ticket_status?: string;
    ticket_title: string;
    ticket_type?: string;
    update_time?: string;
    user_id: number;
    is_selected?: boolean;
    token_actions?: string;
    has_new_msg?: boolean;
    attachment_list?: SupportTicketAttachment[];
    ticket_deliver?: SupportTicketAttachment[];
}
export interface SupportTicketOption{
    id: number;
    source_field: string;
    option_status: string;
    option_data_type: string;
    option_label: string;
    option_value: string;
    option_desc: string;
    option_sort: number;
    create_time: string;
    update_time: string;
}
export type SupportTicketOptions = Record<string, SupportTicketOption[]>
export interface SupportTicketChange{
    id: number;
    circular_type: string;
    create_time: string;
    ticket_id: number;
    update_time:string;
    user_nick_name?:string;
    user_avatar?:string;
    column_comment?:string;
    column_type?: string;
    update_field_new_value?: string;
    update_field_old_value?: string;

}
export interface SupportTicketMessage{
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
    msg_content_finish_html?: string[] | null,
    msg_token_used: number | null,
    msg_time_used: number | null,
    msg_remark: number | null,
    msg_del: number | null,
    msg_version :number | null,
    msg_parent_id :number | null,
    msg_reference_finish: boolean | null,
    attachment_list?: SupportTicketAttachment[];
    create_time: string | null,
    update_time: string | null,

}
export interface SupportTicketAttachment{
    ticket_id: number
    ticket_code:string
    session_id:number
    qa_id:number
    msg_id:number
    user_id:number
    id:number
    resource_type:string
    resource_name:string
    resource_icon:string
    resource_url:string
    resource_size:number
    resource_desc:string
    resource_feature_code:string
    resource_status:string
    create_time:string
    update_time:string
}
