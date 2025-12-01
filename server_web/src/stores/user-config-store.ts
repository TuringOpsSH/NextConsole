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
    const systemConfig = reactive<ISystemConfig>({
      ai: {
        stt: { provider: '', xf_api: '', xf_api_id: '', xf_api_key: '', xf_api_secret: '' },
        xiaoyi: { avatar_url: '', llm_code: '', name: '' }
      },
      resources: {
        download: { max_count: 100, cool_time: 7200 },
        auto_rag: true,
        embedding: { enable: false, llm_code: '', threshold: 0, topK: 0 },
        rerank: { enable: false, llm_code: '', threshold: 0, topK: 0 }
      },
      connectors: {
        qywx: [{ agent_id: '', corpsecret: '', domain: '', sCorpID: '', sEncodingAESKey: '', sToken: '' }],
        weixin: [{ domain: '', wx_app_id: '', wx_app_secret: '' }]
      },
      ops: {
        server: {
          domain: '',
          admin_domain: '',
          bucket_size: 0,
          data_dir: '',
          download_dir: '',
          jwt_access_token_expires: 0,
          timezone: '',
          log_dir: '',
          log_file: '',
          log_level: '',
          log_max_size: 0,
          log_backup_count: 0,
          db_type: '',
          db_user: '',
          db_host: '',
          db_port: '',
          redis_host: '',
          redis_port: 0,
          redis_username: '',
          next_console_channel: 0,
          websocket_channel: 0,
          celery_broker_channel: 0,
          celery_result_channel: 0,
          worker_concurrency: 0,
          task_timeout: 0
        },
        brand: { brand_name: '', enable: false, logo_full_url: '', logo_url: '' }
      },
      tools: {
        email: { notice_email: '', smtp_password: '', smtp_port: 465, smtp_server: '', smtp_user: '' },
        search_engine: { endpoint: '', key: '', provider: '' },
        sms: { endpoint: '', key_id: '', key_secret: '', provider: '', sign_name: '', template_code: '' },
        wps: { app_id: '', edit: false, enabled: false, preview: false }
      }
    } as ISystemConfig);
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
          search_engine_resource: 'search',
          session_resources_list: [
            {
              resource_id: -1,
              resource_icon: 'all_resource.svg',
              resource_name: '全部资源'
            } as IResourceItem
          ]
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
