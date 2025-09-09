/**
 * AppMetaInfo，ai应用信息表
 */
export interface IAppMetaInfo {
  /**
   * 应用编码，应用编码
   */
  app_code: string;
  /**
   * 应用描述，应用描述
   */
  app_desc: string;
  /**
   * 应用图标，应用图标
   */
  app_icon: string;
  /**
   * 应用名称，应用名称
   */
  app_name: string;
  /**
   * 应用状态，应用状态
   */
  app_status: string;
  /**
   * 应用类型，应用类型
   */
  app_type: string;
  /**
   * 创建时间，创建时间
   */
  create_time: string;
  /**
   * 自增id，自增id
   */
  id: number;
  /**
   * 更新时间，更新时间
   */
  update_time: string;
  /**
   * 应用编码，作者id
   */
  user_id: number;
  [property: string]: any;
}

/**
 * workflow_meta_info，工作流元信息
 */
export interface IWorkflowMetaInfo {
  /**
   * 创建时间
   */
  create_time?: string;
  /**
   * 自增id
   */
  id: number;
  /**
   * 更新时间
   */
  update_time?: string;
  /**
   * 作者id
   */
  user_id?: number;
  /**
   * 工作流编码
   */
  workflow_code: string;
  /**
   * 工作流描述
   */
  workflow_desc: string;
  /**
   * 工作流图标
   */
  workflow_icon: string;
  /**
   * 工作流名称
   */
  workflow_name: string;
  /**
   * 工作流结构
   */
  workflow_schema: string;
  workflow_edit_schema: string;
  /**
   * 工作流状态
   */
  workflow_status: string;
  [property: string]: any;
}

export interface IAgentNode {
  nodeCode: string;
  nodeIcon: string;
  nodeType: string;
  nodeDesc: string;
  nodeName: string;
  nodeInput: string;
  nodeOutput: string;
  nodeModel: string;
  nodeStatus?: string;
  [property: string]: any;
}

/**
 * workflow_node_info
 */
export interface IWorkflowNodeInfo {
  /**
   * 创建时间
   */
  create_time: string;
  /**
   * ID 编号
   */
  id: number;
  /**
   * 节点编号
   */
  node_code: string;
  /**
   * 节点描述
   */
  node_desc: string;
  /**
   * 节点失败策略
   */
  node_failed_solution: string;
  /**
   * 节点失败模板
   */
  node_failed_template: string;
  /**
   * 节点图标
   */
  node_icon: string;
  /**
   * 节点大模型编号
   */
  node_llm_code: string;
  /**
   * 节点大模型参数
   */
  node_llm_params: INodeLlmParams;
  /**
   * 系统提示词变量结构
   */
  node_llm_system_prompt_params_json_schema: string;
  /**
   * 系统提示词模板
   */
  node_llm_system_prompt_template: string;
  /**
   * 用户提示词变量结构
   */
  node_llm_user_prompt_params_json_schema: string;
  /**
   * 用户提示词模板
   */
  node_llm_user_prompt_template: string;
  /**
   * 节点名称
   */
  node_name: string;
  /**
   * 节点输出数据格式
   */
  node_result_format: string;
  /**
   * 节点输出模板
   */
  node_result_template: string;
  /**
   * 节点重试间隔
   */
  node_retry_duration: string;
  /**
   * 节点最大重试次数
   */
  node_retry_max: string;
  node_retry_model?: number;
  /**
   * 节点运行模式
   */
  node_run_model_config: Record<string, unknown>;
  /**
   * 节点状态
   */
  node_status: string;
  /**
   * 节点类型
   */
  node_type: string;
  /**
   * 更新时间
   */
  update_time: string;
  /**
   * 用户id
   */
  user_id: number;
  /**
   * workflow_id
   */
  workflow_id: number;
  node_session_memory_size: number;
  node_deep_memory: boolean;
  node_agent_nickname: string;
  node_agent_avatar: string;
  node_agent_desc: string;
  node_agent_prologue: string;
  node_agent_preset_question: string;
  node_input_params_json_schema?: {
    properties: object;
  };
  node_upstream?: any[];
  node_upstream2?: any[];
  node_downstream?: string;
  node_result_extract_separator?: string;
  node_result_extract_quote?: string;
  node_result_extract_columns?: string;
  node_result_params_json_schema?: object;

  node_tool_api_url?: string;
  node_tool_http_method?: string;
  node_tool_http_header?: object;
  node_tool_http_params?: object;
  node_tool_http_body?: object;
  node_tool_http_body_type?: string;
  node_rag_resources?: any[];
  node_rag_web_search?: boolean;
  node_timeout?: number;
  enable_file?: boolean;
  node_enable_message?: boolean;
  node_message_schema?: any[];
  node_message_schema_type?: string;
  node_rag_ref_show?: boolean;
  node_file_reader_config?: IFileReaderConfig;
  node_file_splitter_config?: IFileSplitterConfig;
  node_sub_workflow_config?: IWorkflowConfig;
  subWorkflowOptions?: IWorkflowMetaInfo[];
  [property: string]: any;
}

/**
 * 节点大模型参数
 */
export interface INodeLlmParams {
  llm_name?: string;
  llm_icon?: string;
  llm_desc?: string;
  /**
   * 使用什么样的采样温度，在0到2之间。较高的值（如0.8）将使输出更加随机，而较低的值（例如0.2）将使其更加集中和确定。
   */
  temperature: number;
  /**
   * 介于-2.0和2.0之间的数字。正值会根据到目前为止新标记在文本中的现有频率对其进行惩罚，从而降低模型逐字重复同一行的可能性。
   */
  frequency_penalty: number;
  /**
   * 一种替代温度采样的方法，称为核采样，其中模型考虑了具有top_p概率质量的标记的结果。因此，0.1意味着只考虑包含前10%概率质量的令牌。
   * 我们通常建议改变这个或温度，但不要两者都改变。
   */
  top_p: number;
  /**
   * 介于-2.0和2.0之间的数字。正值根据新标记是否出现在文本中来惩罚它们，从而增加了模型谈论新主题的可能性。
   */
  presence_penalty: string;

  /**
   * 输入令牌和生成令牌的总长度受模型上下文长度的限制。用于计数令牌的示例Python代码。
   */
  max_tokens: string;
  /**
   * 响应格式
   */
  response_format: string;
  /**
   * 一个 string 或最多包含 8 个 string 的 list，在遇到这些词时，API 将停止生成更多的 token。
   */
  stop: string;
  /**
   * 如果设置为 True，将会以 SSE（server-sent events）的形式以流式发送消息增量。消息流以 data: [DONE] 结尾。
   */
  stream: string;
  /**
   * 开启视觉能力
   */
  support_vis: boolean;
  enable_visual: boolean;
  visual_ref: Record<string, unknown>;
  support_file: boolean;
  enable_file: boolean;
  file_ref: Record<string, unknown>;
  use_default?: boolean;
  extra_body_schema?: object;
  [property: string]: any;
}
export interface IWorkflowEdgeInfo {
  edge_code?: string;
  edge_icon?: string;
  edge_name?: string;
  edge_desc?: string;
  edge_type?: string;
  edge_condition_type?: string;
  edge_conditions?: IWorkflowEdgeCondition[];
  routerName?: string;
  node_upstream?: any;
}
export interface IWorkflowEdgeCondition {
  src_node: Record<string, unknown>;
  operator: string;
  tgt_node: Record<string, unknown>;
}
export interface IFileReaderConfig{
  input_resources: object;
  src_format: string;
  engine: string;
  tgt_format: string;
}
export interface IFileSplitterConfig{
  method: string;
  chunk_size: number;
  length_config: Record<string, unknown>;
  symbol_config: Record<string, unknown>;
  layout_config: Record<string, unknown>;
}
export interface IWorkflowConfig {
  target_workflow_code: string;
}
