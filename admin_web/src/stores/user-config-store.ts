import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import { IResourceItem } from '@/types/resource-type';
import { ISystemConfig, IUserConfig } from '@/types/user-center';

export const useUserConfigStore = defineStore(
  'userConfig',
  () => {
    const userConfig = reactive<IUserConfig>({
      user_id: null,
      workbench: {
        model_list: [],
        message_layout: 'default',
        search_engine_language: 'zh',
        search_engine_resource: 'search',
        session_resources_list: [
          {
            resource_id: -1,
            resource_icon: 'all_resource.svg',
            resource_name: '全部资源'
          } as IResourceItem
        ]
      },
      contact: {
        allow_search: true
      },
      system: {
        theme: 'light',
        language: '中文'
      }
    });
    const systemConfig = reactive<ISystemConfig>({} as ISystemConfig);
    const systemVersion = ref('');
    function updateUserConfig(config: Partial<IUserConfig>) {
      Object.assign(userConfig, config);
    }
    function updateSystemConfig(config: Partial<ISystemConfig>) {
      Object.assign(systemConfig, config);
    }
    function $reset() {
      Object.assign(userConfig, {
        user_id: null,
        workbench: {
          model_list: [],
          message_layout: 'default',
          search_engine_language: 'zh',
          search_engine_resource: 'search'
        },
        resources: {
          auto_rag: true,
          view_components: 'pdf'
        },
        contact: {
          allow_search: true
        },
        system: {
          theme: 'light',
          language: '中文'
        }
      });
    }
    return { userConfig, systemVersion, systemConfig, updateUserConfig, updateSystemConfig, $reset };
  },
  {
    persist: true // 启用持久化
  }
);
