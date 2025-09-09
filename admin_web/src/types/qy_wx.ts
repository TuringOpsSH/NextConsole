import {msg_queue_item} from "@/types/next-console";

export interface task_member{
    id: number,
    staff_code: string,
    staff_name: string,
    staff_avatar: string,
    staff_department: string,
    staff_status: string,
    task_role: string,
    work_model: string,

}

export interface service_ticket {

    id: number,
    ticket_id: string,
    ticket_status: string,
    device_code: string,
    device_type: string,
    task_name: string,
    task_desc: string,
    task_type: string,
    task_source: string,
    task_standard_demands: string,
    task_level: number,
    task_work_model: string,
    task_customer_contract: string,
    task_customer_phone: string,
    task_location: string,
    task_change_manager: string,
    task_change_type: string,
    project_code: string,
    project_name: string,
    task_member_list : task_member[],
    create_time: string,
    update_time: string,
    ticket_show_flag: boolean,
    ticket_edit_flag: boolean,
}

export interface qx_wx_customer {

    id: number,
    weixin_id: number,
    weixin_nickname: string,
    weixin_avatar: string,
    weixin_gender: number,
    customer_company: string,
    customer_department: string,
    customer_area: string,
    customer_region: string,
    customer_maintenance_scope: string,
    customer_comment: string,
    customer_comment_person: string,
    customer_name: string,
    customer_phone: string,
    customer_status: string,
    customer_session_status: number,
    customer_reg_info: msg_queue_item[],
    create_time: string,
    update_time: string,

}

export interface kf_config {
    id: number,
    s_agent_id: string,
    s_corp_id: string,
    s_kf_id: string,

}

export interface kf_account {
    kf_avatar: string,
    kf_desc: string,
    kf_id: string,
    kf_name: string
}


export interface pre_check_record{
    device_sn: string,
    device_type: string,
    device_code: string,
    device_maintain_company: string,
    device_produce_company: string,
    device_begin_time: string,
    device_end_time: string,

}
export interface pre_check_attachment{
    file_id: string,
    file_icon: string,
    file_name: string,
    file_source: string,
    file_size: string,
    file_status: string,

}

export interface customer_info{
    ID:string,
    name: string,
    wx: string,

}
export interface project_info {
    F_Str_ProjectName: string,
    F_Str_ContractNum: string,
    F_Str_ProjectCode: string,
    F_Str_ContractualCustomer: string,
    CustomerAddress: string,
    F_Sel_ProjectManager: string,
    F_Sel_Salesperson: string,
    F_bpm_status: string,
    F_Dt_StartDate: string,
    F_Dt_EndDate: string,
    F_Str_Task_Cnt: number|string,
    F_Str_Task_Cnt_ALL: number,
    all_address_str: string,
    project_info_is_show: boolean |null,
    pre_check_record : [pre_check_record],
    pre_check_attachment: [pre_check_attachment],
    all_customer_info: [customer_info],
}

export interface kf_console_customer{
    open_kf: kf_account,
    customers: qx_wx_customer[],
}

export interface kf_servicer {
    id: string,
    staff_code: string,
    staff_name: string,
    staff_avatar: string,
    staff_department: string,
    staff_status: string,
}
