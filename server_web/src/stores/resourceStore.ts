import { defineStore } from 'pinia';
import { ref } from 'vue';
import { IPersistOptions } from '@/types/resource-type';

export const useResourceStore = defineStore(
  'resource',
  () => {
    const authType = ref<string>();

    return { authType };
  },
  // 开启本地缓存
  {
    persist: {
      key: 'resourceStore', // 自定义存储键名（默认使用 Store ID）
      paths: ['authType'] // 缓存哪些数据
    } as IPersistOptions
  }
);
