import mitt from 'mitt';

// 定义所有事件类型及其参数
type TEventTypes = {
  [eventKeys.SIDEBAR.REFRESH_SESSION_LIST]: void; // 无参数事件
  [eventKeys.SIDEBAR.CHANGE_SESSION]: { sessionId: number; sessionCode: string; taskId: string }; // 带参数事件
  // 可扩展其他事件...
};

// 创建强类型化的 Mitt 实例
export const emitter = mitt<TEventTypes>();

// 统一管理事件键名（避免硬编码）
export const eventKeys = {
  SIDEBAR: {
    REFRESH_SESSION_LIST: 'refresh-session-list',
    CHANGE_SESSION: 'change-session'
  }
} as const; // as const 确保键名为字面量类型
