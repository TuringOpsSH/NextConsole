export const SessionStorageKeys = {
  RAFFLE_RETRACT: Symbol('raffle_retract'), // 抽奖是否收缩
  SESSION_CODE: Symbol('session_code'), // 会话code
  ASSISTANT_ACTIVE: Symbol('assistant_active'),
  // 数据源
  SESSION_SOURCE: Symbol('session_source'),
  QUOTE_ID_LIST: Symbol('quote_id_ist'),
  CURRENT_SESSION_ID: Symbol('current_session_id'),
  NO_QA_SESSION_IDS: Symbol('no_qa_session_ids')
} as const;
