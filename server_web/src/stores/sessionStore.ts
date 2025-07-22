import { defineStore } from 'pinia';
import { ref } from 'vue';

// eslint-disable-next-line @typescript-eslint/naming-convention
type SessionListFn = () => Promise<void>;

export const useSessionStore = defineStore('session', () => {
  const getLatestSessionListRef = ref<SessionListFn | null>(null);
  const initAppSessionRef = ref<() => Promise<void> | null>(null);
  // 注册函数的方法
  const registerSessionListFn = (fn: SessionListFn) => {
    getLatestSessionListRef.value = fn;
  };
  const registerInitAppSessionFn = (fn: (newVal, keepSession) => Promise<void>) => {
    initAppSessionRef.value = fn;
  }


  return { getLatestSessionListRef, registerSessionListFn, registerInitAppSessionFn, initAppSessionRef };
});
