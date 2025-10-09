import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ISystemNotice } from '@/types/user-center';

export const useSystemNoticeStore = defineStore(
  'systemNotice',
  () => {
    const unreadSystemNotice = ref<ISystemNotice[]>([]);

    function addNewNotice(data) {
      unreadSystemNotice.value.unshift(data);
    }
    function updateSystemNotice(data) {
      unreadSystemNotice.value = data;
    }
    function $reset() {
      unreadSystemNotice.value = [];
    }
    return { unreadSystemNotice, updateSystemNotice, addNewNotice, $reset };
  },
  {
    persist: true // 启用持久化
  }
);
