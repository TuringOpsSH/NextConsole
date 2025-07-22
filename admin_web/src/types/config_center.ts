export interface UserConfig {
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
export interface SearchResourceType {
  resource_type: string;
  resource_name: string;
  resource_active: boolean;
}
export interface LLMInstance {
  llm_code: string;
  llm_name: string;
  llm_type: string;
  llm_desc: string;
  llm_icon: string;
  llm_status: string;
  llm_is_proxy: boolean;
  support_vis?: boolean;
  support_file?: boolean;
  create_time: string;
  update_time: string;
}
