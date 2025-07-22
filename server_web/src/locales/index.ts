import { createI18n } from 'vue-i18n';
import en from './en';
import { zh } from './zh';

// 按模块合并语言包
const messages = {
  en,
  zh
};

// 创建 i18n 实例（支持 TS 类型推导）
export const i18n = createI18n({
  legacy: false, // 启用 Composition API 模式
  locale: 'zh', // 默认语言
  fallbackLocale: 'en',
  messages,
  globalInjection: true // 启用全局 $t 方法（TS 需额外处理）
});
