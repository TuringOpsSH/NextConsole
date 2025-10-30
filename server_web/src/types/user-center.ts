import { ResourceItem } from '@/types/resource-type';

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

export interface IPointTransaction {
  id: number;
  transaction_id: string;
  account_id: string;
  transaction_type: string;
  transaction_amount: number;
  transaction_status: string;
  order_id: string;
  transaction_desc: string;
  create_time: string;
  update_time: string;
}

export interface IUserConfig {
  user_id: string | number;
  workbench: {
    model_list: Array<string>;
    message_layout: string;
    search_engine_language: string;
    search_engine_resource: string;
    session_resources_list: Array<ResourceItem>;
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

export interface ISearchResourceType {
  resource_type: string;
  resource_name: string;
  resource_active: boolean;
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
