import { defineStore } from 'pinia';
import { ref, reactive, computed } from 'vue';
import { IAppMeta } from '@/types/app';

export const useAppInfoStore = defineStore(
  'app-info-store',
  () => {
    const appInfo = reactive<IAppMeta>({
      app_code: ''
    });
    const sessionCode = ref('');
    const taskCode = ref('');
    const workflowParams = ref({});
    const attachments = ref([]);
    const question = ref('');
    function updateAppInfo(appInfo: IAppMeta) {
      Object.assign(appInfo, appInfo);
    }
    function updateWorkflowParams(params: object) {
      workflowParams.value = params;
    }
    function updateAttachments(params: []) {
      attachments.value = params;
    }
    return {
      appInfo,
      sessionCode,
      taskCode,
      workflowParams,
      attachments,
      question,
      updateAppInfo,
      updateWorkflowParams,
      updateAttachments
    };
  },
  {
    persist: true // 启用持久化
  }
);
