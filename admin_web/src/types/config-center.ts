export interface IUserConfig {
  id: number;
  user_id: number;
  open_query_agent: boolean;
  resource_table_show_fields: string;
  resource_auto_rag: boolean;
  resource_shortcut_types: string;
  search_engine_language_type: string;
  search_engine_resource_type: string;
  config_status: string;
  create_time: string;
  update_time: string;
}
export interface ISearchResourceType {
  resource_type: string;
  resource_name: string;
  resource_active: boolean;
}
export interface ILLMInstance {
  id: number;
  user_id?: number;
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
  llm_authors?: any[];
  author?: {
    user_id: number;
    user_nick_name: string;
    user_avatar: string;
    user_nick_name_py?: string;
  };
  access?: string[];
}
export interface ISupplier {
  id: number;
  supplier_code: string;
  supplier_name: string;
  supplier_desc: string;
  supplier_icon: string;
  supplier_website: string;
  supplier_models: ILLMInstance[];
  supplier_api_url: string;
  supplier_status: string;
  create_time: string;
  update_time: string;
}
