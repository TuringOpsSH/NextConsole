import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import { IAppMetaInfo, IConfigArea } from '@/types/app-center-type';

export const useAppStore = defineStore('appStore', () => {
  const currentApp = reactive<IAppMetaInfo>({
    app_code: '',
    app_desc: '',
    app_icon: '',
    app_name: '',
    app_status: '',
    app_type: '',
    app_config: {},
    create_time: '',
    id: 0,
    update_time: '',
    user_id: 0
  });
  const configArea = <IConfigArea[]>[
    {
      area: 'welcome',
      name: 'configEdit',
      label: '欢迎页',
      icon: '/images/welcome.svg'
    },
    {
      area: 'params',
      name: 'configEdit',
      label: '应用参数',
      icon: '/images/params.svg'
    }
  ];
  const agentAppRef = ref(null);
  const currentAppConfigArea = reactive<IConfigArea>({
    area: 'welcome',
    name: 'configEdit',
    label: '欢迎页配置',
    icon: '/images/welcome.svg'
  });
  function updateAppConfigArea(newArea: IConfigArea) {
    Object.assign(currentAppConfigArea, newArea);
  }
  function updateAppMetaArea(newApp: IAppMetaInfo) {
    Object.assign(currentApp, newApp);
  }
  function updateAgentAppRef(newRef: any) {
    agentAppRef.value = newRef;
  }
  return {
    currentApp,
    agentAppRef,
    configArea,
    currentAppConfigArea,
    updateAppConfigArea,
    updateAppMetaArea,
    updateAgentAppRef
  };
});
