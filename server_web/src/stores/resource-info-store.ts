import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useResourceInfoStore = defineStore(
  'resourceInfo',
  () => {
    const currentResourceUsage = ref(0);
    const currentResourceUsagePercent = ref(0);
    const uploadFileList = ref([]);
    return { currentResourceUsage, currentResourceUsagePercent, uploadFileList };
  },
  {
    persist: true // 启用持久化
  }
);
