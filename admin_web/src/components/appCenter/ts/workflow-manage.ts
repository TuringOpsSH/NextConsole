import { ElMessage } from 'element-plus';
import { reactive, ref } from 'vue';
import { appDetail, workflowCreate, workflowDelete, workflowUpdate } from '@/api/appCenterApi';
import { closeSubPage, currentApp, openedSubPage, openWorkFlowEdit } from '@/components/appCenter/ts/app-detail';
import { IWorkflowMetaInfo } from '@/types/appCenterType';

export const showNewFlowForm = ref(false);
export const currentFlowList = ref<IWorkflowMetaInfo[]>([]);
export const currentFlowListDetail = ref(true);

export const newFlowFormRef = ref(null);
export const newFlowFormRules = {
  workflow_name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  workflow_desc: [{ required: true, message: '请输入描述', trigger: 'blur' }],
  workflow_icon: [{ required: true, message: '请输入图标', trigger: 'blur' }]
};
export const showDeleteFlowConfirm = ref(false);
export const deleteFlow = ref<IWorkflowMetaInfo | null>(null);
export const showFlowUpdateForm = ref(false);
export const updateFlow = reactive<IWorkflowMetaInfo | null>({
  workflow_schema: '',
  workflow_edit_schema: '',
  workflow_status: '',
  workflow_name: '',
  workflow_desc: '',
  workflow_code: '',
  workflow_icon: '',
  id: 0
});
export const FlowUpdateFormRef = ref(null);
export const defaultFlow = reactive<IWorkflowMetaInfo>({
  user_id: 0,
  workflow_schema: '',
  workflow_edit_schema: '',
  workflow_status: '',
  workflow_name: '',
  workflow_desc: '',
  workflow_code: '',
  workflow_icon: '',
  id: 0
});
// eslint-disable-next-line @typescript-eslint/naming-convention
export async function beginInitWorkFlow() {
  showNewFlowForm.value = true;
  defaultFlow.workflow_name = '';
  defaultFlow.workflow_code = '';
  defaultFlow.workflow_icon = 'images/workflow.svg';
}
export async function handleWorkFlowIconUploadSuccess(res: any) {
  if (!res.error_status) {
    defaultFlow.workflow_icon = res.result.workflow_icon;
  }
}

export async function newFlowFormSubmit() {
  const validRes = await newFlowFormRef.value.validate();
  if (!validRes) return;
  const params = {
    app_code: currentApp.app_code,
    workflow_name: defaultFlow.workflow_name,
    workflow_icon: defaultFlow.workflow_icon,
    workflow_desc: defaultFlow.workflow_desc,
    workflow_is_main: currentFlowList.value.length === 0
  };
  const res = await workflowCreate(params);
  if (!res.error_status) {
    showNewFlowForm.value = false;
    currentFlowList.value.push(res.result);
    // @ts-ignore
    await openWorkFlowEdit({
      appCode: currentApp.app_code,
      workflow_code: res.result.workflow_code,
      workflow_name: res.result.workflow_name,
      workflow_icon: res.result.workflow_icon
    });
  }
}

export async function beginUpdateWorkFlow(workflow: IWorkflowMetaInfo) {
  showFlowUpdateForm.value = true;
  Object.assign(updateFlow, workflow);
}
export async function beginDeleteWorkFlow(workflow: IWorkflowMetaInfo) {
  showDeleteFlowConfirm.value = true;
  deleteFlow.value = workflow;
}
export async function confirmDeleteWorkFlow() {
  showDeleteFlowConfirm.value = false;
  closeSubPage({
    appCode: currentApp.app_code,
    pageCode: deleteFlow.value.workflow_code,
    pageName: deleteFlow.value.workflow_name,
    pageIcon: deleteFlow.value.workflow_icon
  });
  const res = await workflowDelete({
    app_code: currentApp.app_code,
    workflow_code: deleteFlow.value.workflow_code
  });
  if (!res.error_status) {
    const deleteSubPageIdx = openedSubPage.value.findIndex(item => item.pageCode === deleteFlow.value.flow_code);
    if (deleteSubPageIdx > -1) {
      closeSubPage(openedSubPage.value[deleteSubPageIdx]);
    }
    const res = await appDetail({
      app_code: currentApp.app_code
    });
    if (!res.error_status) {
      currentFlowList.value = res.result.flows;
    }
    ElMessage.success('删除成功!');
  }
  deleteFlow.value = null;
}

export async function confirmUpdateWorkflow() {
  const validRes = await FlowUpdateFormRef.value.validate();
  if (!validRes) return;
  showFlowUpdateForm.value = false;
  updateFlow.app_code = currentApp.app_code;
  const res = await workflowUpdate(updateFlow);
  if (!res.error_status) {
    // 更新列表
    const index = currentFlowList.value.findIndex(item => item.flow_code === updateFlow.flow_code);
    currentFlowList.value[index] = res.result;
    // 更新标签页
    openedSubPage.value.forEach(item => {
      if (item.pageCode === updateFlow.workflow_code) {
        item.pageName = res.result.workflow_name;
        item.pageIcon = res.result.workflow_icon;
      }
    });
    // 初始化UpdateWorkflow
    updateFlow.workflow_name = '';
    updateFlow.workflow_desc = '';
    updateFlow.workflow_icon = '';
    ElMessage.success('更新成功!');
  }
}
export async function setMainWorkflow(workflow: IWorkflowMetaInfo) {
  const res = await workflowUpdate({
    app_code: currentApp.app_code,
    workflow_code: workflow.workflow_code,
    workflow_is_main: true
  });
  if (!res.error_status) {
    currentFlowList.value.forEach(item => {
      item.workflow_is_main = false;
    });
    workflow.workflow_is_main = true;
    ElMessage.success('设置成功!');
  }
}
