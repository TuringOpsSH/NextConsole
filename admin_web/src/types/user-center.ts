import { ICompany, IDepartment } from '@/types/contacts';

export interface IUsers {
  user_id?: string | number;
  user_code?: string;
  user_name?: string;
  user_nick_name: string;
  user_nick_name_py?: string;
  user_email?: string;
  user_phone?: string;
  user_gender?: string;
  user_age?: number;
  user_avatar?: string;
  user_department?: string;
  user_company?: string | null;
  user_account_type?: string;
  user_resource_limit?: number;
  create_time?: string;
  update_time?: string;
  user_expire_time?: string;
  last_login_time?: string;
  user_role?: [string];
  user_status?: string;
  user_source?: string;
  user_wx_nickname?: string;
  user_wx_avatar?: string;
  user_wx_openid?: string;
  user_wx_union_id?: string;
  user_position?: string | null;
  user_area?: string | null;
  user_department_id?: number;
  user_company_id?: number;
  user_invite_code?: string;
  user_point_account?: IUserAccount;
  view_record_id?: number;
  view_records?: Array<any>;
  is_friend?: boolean;
  [property: string]: any;
}

export interface IUserAccount {
  user_id: string;
  account_id: string;
  account_type: string;
  balance: number;
  frozen_balance: number;
  account_status: string;
  create_time: string;
  update_time: string;
  [property: string]: any;
}

export interface IUserTokenSta {
  user_id: string;
  create_time: string;
  update_time: string;
  sta_date: string;
  qa_cnt: number;
  rag_cnt: number;
  msg_token_used_cnt: number;
  msg_token_used_point_cnt: number;
  rag_token_used_cnt: number;
  rag_token_used_point_cnt: number;
  rate_dist: string;
  rate_dist_obj: {
    [key: string]: number;
  };
}

export interface ICouponInfo {
  coupon_id: string;
  coupon_name: string;
  coupon_text: string;
  coupon_desc: string;
  coupon_token_points: number;
  coupon_start_date: string;
  coupon_end_date: string;
  coupon_status: string;
  coupon_type: string;
  coupon_used_cnt_limit: number;
  coupon_used_cnt: number;
  coupon_last_used_time: string;
  create_time: string;
  update_time: string;
}
export interface ISystemNotice {
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
export interface IUserConfig {
  user_id: string | number;
  workbench: {
    model_list: Array<string>;
    message_layout: string;
    search_engine_language: string;
    search_engine_resource: string;
  };
  resources: {
    auto_rag: boolean;
    view_components: string;
  };
  contact: {
    allow_search: boolean;
  };
  system: {
    theme: string;
    language: string;
  };
}
/**
 * user_notice_task_info
 */
export interface IUserNoticeTaskInfo {
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
  task_name: string;
  task_desc: string;
  run_now: boolean;
  plan_begin_time: string;
  plan_finish_time: string;
  notice_params: INoticeParams;
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
  task_progress: string;
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
export interface INoticeParams {
  all_user: boolean;
  all_company_user: boolean;
  all_person_user: boolean;
  all_subscribe_email: boolean;
  target_company: boolean;
  target_department: boolean;
  target_user: boolean;
  target_companies: ICompany[];
  target_departments: IDepartment[];
  target_users: IUsers[];
}
export interface ITaskInstance {
  id: number;
  task_id: number;
  receive_user_id: number;
  task_celery_id: string;
  notice_type: string;
  notice_params: INoticeParams;
  notice_content: string;
  notice_status: string;
  create_time: string;
  update_time: string;
}

export interface ISystemConfig {
  ai: {
    xiaoyi: {
      llm_code: string;
      name: string;
      avatar_url: string;
    };
    embedding: {
      enable: boolean;
      llm_code: string;
      threshold: number;
      topK: number;
    };
    rerank: {
      enable: boolean;
      llm_code: string;
      threshold: number;
      topK: number;
    };
    stt: {
      provider: string;
      xf_api: string;
      xf_api_id: string;
      xf_api_key: string;
      xf_api_secret: string;
    };
  };
  connectors: {
    qywx: [
      {
        domain: string;
        sToken: string;
        sEncodingAESKey: string;
        sCorpID: string;
        corpsecret: string;
        agent_id: string;
      }
    ];
    weixin: [
      {
        domain: string;
        wx_app_id: string;
        wx_app_secret: string;
      }
    ];
  };
  tools: {
    search_engine: {
      provider: string;
      endpoint: string;
      key: string;
    };
    sms: {
      provider: string;
      key_id: string;
      key_secret: string;
      endpoint: string;
      sign_name: string;
      template_code: string;
    };
    email: {
      smtp_server: string;
      smtp_port: 465;
      smtp_user: string;
      smtp_password: string;
      notice_email: string;
    };
    wps: {
      enabled: boolean;
      app_id: string;
      preview: boolean;
      edit: boolean;
    };
  };
  ops: {
    brand: {
      enable: boolean;
      logo_url: string;
      logo_full_url: string;
      brand_name: string;
    };
  };
}
export interface ILLMInstance {
  id: number;
  llm_code: string;
  llm_name: string;
  llm_label: string;
  llm_type: string;
  llm_desc: string;
  llm_icon: string;
  llm_status: string;
  support_vis?: boolean;
  support_file?: boolean;
  stream?: boolean;
  create_time: string;
  update_time: string;
  is_editable?: boolean;
  llm_company?: string;
  llm_is_public?: boolean;
  llm_proxy_url?: string;
  is_std_openai?: boolean;
  llm_api_secret_key?: string;
  max_tokens?: number;
  llm_base_url?: string;
  llm_tags?: string[];
  use_default?: boolean;
  temperature?: number;
  frequency_penalty?: number;
  presence_penalty?: number;
  top_p?: number;
  extra_headers?: Record<string, unknown>;
  extra_body?: Record<string, unknown>;
}
