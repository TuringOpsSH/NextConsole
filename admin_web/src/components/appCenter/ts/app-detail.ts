import { reactive, ref } from 'vue';
import { appDetail } from '@/api/appCenterApi';
import { search_session as searchSession } from '@/api/next_console';
import { IAppMetaInfo, IWorkflowMetaInfo } from '@/types/appCenterType';
import { session_item as ISessionItem } from '@/types/next_console';

export interface ISubPage {
  appCode: string;
  pageName: string;
  pageIcon: string;
  pageCode: string;
  pageSource: string;
}
export const currentApp = reactive<IAppMetaInfo>({
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
export const currentFlowList = ref<IWorkflowMetaInfo[]>([]);
export const showSetPanel = ref(true);
export const currentSessionList = ref<ISessionItem[]>([]);
export const openedSubPage = ref<ISubPage[]>([]);
export async function initCurrentApp(appCode: string) {
  if (appCode) {
    const res = await appDetail({
      app_code: appCode
    });
    if (!res.error_status) {
      Object.assign(currentApp, res.result?.meta);
      currentFlowList.value = res.result.flows;
    }
  }
  // 从localstorage中获取已打开的本应用的子页面
  const openedSubPageStr = localStorage.getItem('openedSubPage');
  if (openedSubPageStr) {
    const openObj = JSON.parse(openedSubPageStr);
    openedSubPage.value = openObj.filter((item: ISubPage) => item.appCode === appCode);
  }
}
export async function getWorkFlowSession(workflow: IWorkflowMetaInfo) {
  const params = {
    session_task_id: workflow.workflow_code,
    session_status: ['测试']
  };
  if (!workflow.workflow_is_main) {
    params.session_task_id = workflow.workflow_code;
  }
  const res = await searchSession(params);
  if (!res.error_status) {
    currentSessionList.value = res.result;
  }
}
