import { defineStore } from 'pinia';
import { ref } from 'vue';
import { IPersistOptions } from '@/types/resource_type';

export const useResourceStore = defineStore(
  'resource',
  () => {
    const authType = ref<string>();

    return { authType };
  },
  // 开启本地缓存
  {
    persist: {
      storage: sessionStorage, // 指定存储类型（默认 localStorage）
      key: 'resourceStore', // 自定义存储键名（默认使用 Store ID）
      paths: ['authType'] // 缓存哪些数据
    } as IPersistOptions
  }
);
