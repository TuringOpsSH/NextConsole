import {recommend_question_item} from "@/types/next-console";

/**
 * ApifoxModel，ai应用信息表
 */
export interface IAppMeta {
  /**
   * 应用编码，应用编码
   */
  app_code: string;
  /**
   * 应用默认助手，应用默认助手
   */
  app_default_assistant?: number;
  /**
   * 应用描述，应用描述
   */
  app_desc?: string;
  /**
   * 应用图标，应用图标
   */
  app_icon?: string;
  /**
   * 应用名称，应用名称
   */
  app_name?: string;
  /**
   * 应用状态，应用状态
   */
  app_status?: string;
  /**
   * 应用类型，应用类型
   */
  app_type?: string;
  /**
   * 创建时间，创建时间
   */
  create_time?: string;
  /**
   * 自增id，自增id
   */
  id?: number;
  /**
   * 更新时间，更新时间
   */
  update_time?: string;
  /**
   * 应用编码，作者id
   */
  user_id?: number;
  assistant_avatar?: string;
  assistant_prologue?: string;
  assistant_preset_question?: recommend_question_item[];
  [property: string]: any;
}
