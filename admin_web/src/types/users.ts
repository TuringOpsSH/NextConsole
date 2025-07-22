import {Company, Department} from "@/types/contacts";

export interface Users{
    user_id?: string|number,
    user_code?: string ,
    user_name?: string,
    user_nick_name?: string,
    user_nick_name_py?: string,
    user_email?: string,
    user_phone?: string,
    user_gender?: string,
    user_age?: number,
    user_avatar?: string,
    user_department?: string,
    user_company?: string | null,
    user_account_type?: string,
    user_resource_limit?: number,
    create_time?: string,
    update_time?: string,
    user_expire_time?: string,
    last_login_time?: string,
    user_role?: [string],
    user_status?: string,
    user_source?: string,
    user_wx_nickname?: string,
    user_wx_avatar?: string,
    user_wx_openid?: string,
    user_wx_union_id?: string,
    user_position?: string | null,
    user_area?: string | null,
    user_department_id?: number,
    user_company_id?: number,
    [property: string]: any;
}

export interface UserAccount{
    user_id: string,
    create_time: string,
    update_time: string,
    token_used_point_cnt_cycle: number,
    token_used_point_cnt_cycle_str: string | null,
    token_used_point_cnt_total: number,
    token_point_bal: number,
    token_point_fix_bal: number,
}

export interface UserTokenSta{
    user_id: string,
    create_time: string,
    update_time: string,
    sta_date: string,
    qa_cnt: number,
    rag_cnt: number,
    msg_token_used_cnt: number,
    msg_token_used_point_cnt: number,
    rag_token_used_cnt: number,
    rag_token_used_point_cnt: number,
    rate_dist: string,
    rate_dist_obj: {
        [key: string]: number,

    }

}

export interface CouponInfo{
    coupon_id: string,
    coupon_name: string,
    coupon_text: string,
    coupon_desc: string,
    coupon_token_points: number,
    coupon_start_date: string,
    coupon_end_date: string,
    coupon_status: string,
    coupon_type: string,
    coupon_used_cnt_limit: number,
    coupon_used_cnt: number,
    coupon_last_used_time: string,
    create_time: string,
    update_time: string,

}
export interface SystemNotice{
    /**
     * 创建时间，创建时间
     */
    create_time: string;
    /**
     * ID 编号，ID 编号
     */
    id: string;
    /**
     * 通知内容，通知内容
     */
    notice_content: string;
    /**
     * 通知图标，通知图标
     */
    notice_icon: string;
    /**
     * 通知等级，通知等级
     */
    notice_level: string;
    /**
     * 通知状态，通知状态
     */
    notice_status: string;
    /**
     * 通知标题，通知标题
     */
    notice_title: string;
    /**
     * 通知类型，通知图标
     */
    notice_type: string;
    /**
     * 更新时间，更新时间
     */
    update_time: string;
    /**
     * 用户id，用户id
     */
    user_id: string;
}

/**
 * user_notice_task_info
 */
export interface user_notice_task_info {
    /**
     * 任务开始时间，任务开始时间
     */
    begin_time: string;
    /**
     * 创建时间，创建时间
     */
    create_time: string;
    /**
     * 任务完成时间，任务完成时间
     */
    finish_time: string;
    /**
     * ID 编号，ID 编号
     */
    id: number;
    /**
     * 通知变量，通知变量
     */
    task_name:string;
    task_desc:string;
    run_now: boolean;
    plan_begin_time:string;
    plan_finish_time:string;
    notice_params: notice_params;
    /**
     * 通知模版，通知模版
     */
    notice_template: string;
    /**
     * 通知类型，通知类型
     */
    notice_type: string;
    /**
     * 任务进度，任务进度
     */
    task_instance_batch_size: number;
    task_instance_total: number;
    task_instance_success: number;
    task_instance_failed: number;
    task_progress:string;
    /**
     * 任务状态，任务状态
     */
    task_status: string;
    /**
     * 更新时间，更新时间
     */
    update_time: string;
    /**
     * 用户id，用户id
     */
    user_id: number;
    [property: string]: any;
}
export interface notice_params{
    all_user: boolean,
    all_company_user: boolean,
    all_person_user: boolean,
    all_subscribe_email: boolean,
    target_company: boolean,
    target_department: boolean,
    target_user: boolean,
    target_companies: Company[],
    target_departments: Department[],
    target_users: Users[],
}

export interface task_instance{
    id: number,
    task_id: number,
    receive_user_id: number,
    task_celery_id: string,
    notice_type: string,
    notice_params: notice_params,
    notice_content: string,
    notice_status: string,
    create_time: string,
    update_time: string,
}
