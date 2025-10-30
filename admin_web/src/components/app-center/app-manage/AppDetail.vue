<script setup lang="ts">
import { ArrowDown, ArrowRight, Close, Edit, Expand, Fold, MoreFilled, Plus } from '@element-plus/icons-vue';
import { ElMessage, genFileId, type UploadInstance, type UploadRawFile } from 'element-plus';
import { defineProps, nextTick, onMounted, reactive, ref, watch } from 'vue';
import {
  api,
  appDetail,
  workflowExport,
  workflowCreate,
  workflowDelete,
  workflowUpdate,
  workflowImport,
  appUpdate,
  workflowRestore
} from '@/api/app-center-api';
import { delete_session as deleteSession, update_session as updateSession } from '@/api/next-console';

import router from '@/router';
import { useAppStore } from '@/stores/app-store';
import { useUserInfoStore } from '@/stores/user-info-store';
import { useWorkflowStore } from '@/stores/workflow-store';
import { IWorkflowMetaInfo, IConfigArea } from '@/types/app-center-type';
import { ISessionItem } from '@/types/next-console';

const prop = defineProps({
  appCode: {
    type: String,
    default: ''
  }
});
interface ISubPage {
  appCode: string;
  pageName: string;
  pageIcon: string;
  pageCode: string;
  pageSource: string;
}
const userInfoStore = useUserInfoStore();
const appInfoStore = useAppStore();
const showNewFlowForm = ref(false);
const currentFlowListDetail = ref(true);
const metaDialogFlag = ref(false);
const openedSubPage = ref<ISubPage[]>([]);
const currentFlowList = ref<IWorkflowMetaInfo[]>([]);
const currentSessionListFlag = ref(true);
const currentAppConfigFlag = ref(true);
const currentSessionTopicInputRef = ref();
const sessionButtonsRef = ref();
const newAppFormRules = {
  app_name: [
    { required: true, message: '请输入应用名称', trigger: 'blur' },
    { message: '应用名称长度不能超过20个字符', trigger: 'blur', max: 20 }
  ],
  app_desc: [{ required: true, message: '请输入应用描述', trigger: 'blur' }],
  app_icon: [{ required: true, message: '请上传应用图标', trigger: 'change' }]
};
const newFlowFormRef = ref(null);
const newFlowFormRules = {
  workflow_name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  workflow_desc: [{ required: true, message: '请输入描述', trigger: 'blur' }],
  workflow_icon: [{ required: true, message: '请输入图标', trigger: 'blur' }]
};
const showDeleteFlowConfirm = ref(false);
const deleteFlow = ref<IWorkflowMetaInfo | null>(null);
const showFlowUpdateForm = ref(false);
const updateFlow = reactive<IWorkflowMetaInfo | null>({
  workflow_schema: '',
  workflow_edit_schema: '',
  workflow_status: '',
  workflow_name: '',
  workflow_desc: '',
  workflow_code: '',
  workflow_icon: '',
  id: 0
});
const FlowUpdateFormRef = ref(null);
const defaultFlow = reactive<IWorkflowMetaInfo>({
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
const showNewWorkFlowUploadForm = ref(false);
const newUploadWorkFlowFormRef = ref(null);
const uploadWorkFlowLoading = ref(false);
const newUploadWorkFlowForm = reactive({
  uploadFileUrl: ''
});
const newUploadWorkFlowFormRules = {
  uploadFileUrl: [{ required: true, message: '请上传工作流文件', trigger: 'blur' }]
};
const uploadRef = ref<UploadInstance>();
const currentAppRef = ref(null);
const currentAppMode = ref('logic');
const currentPage = ref<ISubPage>({
  appCode: '',
  pageCode: '',
  pageName: '',
  pageIcon: '',
  pageSource: ''
});
const showRestoreConfirm = ref(false);
const restoreFlow = ref<IWorkflowMetaInfo | null>(null);
const showSetPanel = ref(true);
const workflowStore = useWorkflowStore();

async function initCurrentApp(appCode: string) {
  if (appCode) {
    const res = await appDetail({
      app_code: appCode
    });
    if (!res.error_status) {
      appInfoStore.updateAppMetaArea(res.result?.meta);
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
async function beginInitWorkFlow() {
  showNewFlowForm.value = true;
  defaultFlow.workflow_name = '';
  defaultFlow.workflow_code = '';
  defaultFlow.workflow_icon = '/images/workflow.svg';
}
async function handleWorkFlowIconUploadSuccess(res: any) {
  if (!res.error_status) {
    defaultFlow.workflow_icon = res.result.workflow_icon;
  }
}
async function beginDeleteWorkFlow(workflow: IWorkflowMetaInfo) {
  showDeleteFlowConfirm.value = true;
  deleteFlow.value = workflow;
}
function beforeAvatarUpload(file: File) {
  const isLt5M = file.size / 1024 / 1024 < 5;
  if (!isLt5M) {
    ElMessage.info('上传头像图片大小不能超过 5MB!');
  }
  return isLt5M;
}
async function routerToPublish() {
  if (appInfoStore.currentApp?.app_code) {
    if (appInfoStore.currentApp.app_status != '已删除') {
      await router.push({
        name: 'publishCreate',
        params: {
          appCode: appInfoStore.currentApp?.app_code
        }
      });
    } else {
      await router.push({
        name: 'publishDetail',
        params: {
          appCode: appInfoStore.currentApp?.app_code
        }
      });
    }
  }
}
async function confirmUpdateWorkflow() {
  const validRes = await FlowUpdateFormRef.value.validate();
  if (!validRes) return;
  showFlowUpdateForm.value = false;
  updateFlow.app_code = appInfoStore.currentApp.app_code;
  const res = await workflowUpdate({
    app_code: appInfoStore.currentApp.app_code,
    workflow_code: updateFlow.workflow_code,
    workflow_name: updateFlow.workflow_name,
    workflow_desc: updateFlow.workflow_desc,
    workflow_icon: updateFlow.workflow_icon
  });
  if (!res.error_status) {
    // 更新列表
    const index = currentFlowList.value.findIndex(item => item.workflow_code === updateFlow.workflow_code);
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
async function newFlowFormSubmit() {
  const validRes = await newFlowFormRef.value.validate();
  if (!validRes) return;
  const params = {
    app_code: appInfoStore.currentApp.app_code,
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
      appCode: appInfoStore.currentApp.app_code,
      workflow_code: res.result.workflow_code,
      workflow_name: res.result.workflow_name,
      workflow_icon: res.result.workflow_icon
    });
    defaultFlow.workflow_desc = '';
  }
}
async function beginUpdateWorkFlow(workflow: IWorkflowMetaInfo) {
  showFlowUpdateForm.value = true;
  Object.assign(updateFlow, workflow);
}
async function confirmDeleteWorkFlow() {
  showDeleteFlowConfirm.value = false;
  closeSubPage({
    appCode: appInfoStore.currentApp.app_code,
    pageCode: deleteFlow.value.workflow_code,
    pageName: deleteFlow.value.workflow_name,
    pageIcon: deleteFlow.value.workflow_icon
  });
  const res = await workflowDelete({
    app_code: appInfoStore.currentApp.app_code,
    workflow_code: deleteFlow.value.workflow_code
  });
  if (!res.error_status) {
    const deleteSubPageIdx = openedSubPage.value.findIndex(item => item.pageCode === deleteFlow.value.flow_code);
    if (deleteSubPageIdx > -1) {
      closeSubPage(openedSubPage.value[deleteSubPageIdx]);
    }
    const res = await appDetail({
      app_code: appInfoStore.currentApp.app_code
    });
    if (!res.error_status) {
      currentFlowList.value = res.result.flows;
    }
    ElMessage.success('删除成功!');
  }
  deleteFlow.value = null;
  workflowStore.showAgentApp = false;
  workflowStore.updateCurrentSessionList([]);
  workflowStore.showNodeFlag = false;
  workflowStore.showEdgeFlag = false;
}
async function setMainWorkflow(workflow: IWorkflowMetaInfo) {
  const res = await workflowUpdate({
    app_code: appInfoStore.currentApp.app_code,
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
async function exportTargetWorkflow(workflow: IWorkflowMetaInfo) {
  const res = await workflowExport({
    app_code: appInfoStore.currentApp.app_code,
    workflow_code: workflow.workflow_code
  });
  if (!res.error_status) {
    const blob = new Blob([JSON.stringify(res.result)], {
      type: 'application/json;charset=utf-8'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${appInfoStore.currentApp.app_code}_${workflow.workflow_code}.json`;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
  }
}
async function handleExceed(files) {
  uploadRef.value!.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  uploadRef.value!.handleStart(file);
  uploadRef.value.submit();
}
async function importTargetWorkflow() {
  const validRes = await newUploadWorkFlowFormRef.value.validate();
  if (!validRes) return;
  uploadWorkFlowLoading.value = true;
  const res = await workflowImport({
    app_code: appInfoStore.currentApp.app_code,
    workflow_schema_url: newUploadWorkFlowForm.uploadFileUrl
  });
  if (!res.error_status) {
    showNewWorkFlowUploadForm.value = false;
    ElMessage.success('导入成功');
    initCurrentApp(appInfoStore.currentApp.app_code);
  } else {
    ElMessage.error('导入失败');
  }
  uploadWorkFlowLoading.value = false;
  newUploadWorkFlowForm.uploadFileUrl = '';
  uploadRef.value!.clearFiles();
}
function closePanel() {
  showSetPanel.value = false;
  router.replace({
    params: {
      ...router.currentRoute.value.params
    },
    query: {
      ...router.currentRoute.value.query,
      showPanel: 'false'
    }
  });
  workflowStore.showNodeFlag = false;
  workflowStore.showEdgeFlag = false;
}
function openPanel() {
  showSetPanel.value = true;
  router.replace({
    params: {
      ...router.currentRoute.value.params
    },
    query: {
      ...router.currentRoute.value.query,
      showPanel: 'true'
    }
  });
}
async function autoOpenFlow() {
  for (let workflow of currentFlowList.value) {
    if (workflow.workflow_is_main) {
      await openWorkFlowEdit(workflow);
      workflowStore.showAgentApp = false;
      return;
    }
  }
  // 如果没有主流程，则打开第一个工作流
  if (currentFlowList.value.length > 0) {
    await openWorkFlowEdit(currentFlowList.value[0]);
    workflowStore.showAgentApp = false;
    return;
  }
  workflowStore.updateCurrentSessionList([]);
  workflowStore.showAgentApp = false;
}
async function focusSessionTopicInput(item: ISessionItem) {
  item.is_edit = true;
  await nextTick();
  currentSessionTopicInputRef.value?.[0].focus();
  for (let i = 0; i < sessionButtonsRef.value.length; i++) {
    sessionButtonsRef.value[i]?.hide();
  }
}
async function panelRewriteSessionTopic(item: ISessionItem) {
  let params = {
    session_id: item.id,
    session_topic: item.session_topic
  };
  let res = await updateSession(params);
  if (!res.error_status) {
    await workflowStore.getWorkFlowSession(workflowStore.currentFlow);
    ElMessage.success('修改成功');
  }
}
async function panelDeleteSession(item: ISessionItem) {
  let params = {
    session_id: item.id
  };
  let res = await deleteSession(params);
  if (!res.error_status) {
    await workflowStore.getWorkFlowSession(workflowStore.currentFlow);
    ElMessage.success('删除成功');
  }
  for (let i = 0; i < sessionButtonsRef.value.length; i++) {
    sessionButtonsRef.value[i]?.hide();
  }
  workflowStore.showAgentApp = false;
}
async function changeTestSession(item: ISessionItem) {
  await appInfoStore.agentAppRef?.changeTestSession(appInfoStore.currentApp.app_code, item.session_code);
  workflowStore.updateCurrentEditSession(item);
  workflowStore.showAgentApp = true;
}
async function handleWorkFlowUploadSuccess(res: any) {
  if (!res.error_status) {
    newUploadWorkFlowForm.uploadFileUrl = res.result.app_flow_schema_url;
  }
}
async function handleAvatarUploadSuccess(res: any) {
  if (!res.error_status) {
    appInfoStore.currentApp.app_icon = res.result.app_icon;
  }
}
async function updateCurrentApp() {
  const validRes = await currentAppRef.value.validate();
  if (!validRes) {
    return;
  }
  const res = await appUpdate(appInfoStore.currentApp);
  if (!res.error_status) {
    appInfoStore.updateAppMetaArea(res.result);
    ElMessage.success('更新成功');
    metaDialogFlag.value = false;
  }
}
async function openSubPage(page: ISubPage) {
  // 加入到已打开的子页面列表
  let findFlag = false;
  openedSubPage.value.forEach(item => {
    if (item.pageCode === page.pageCode) {
      findFlag = true;
    }
  });
  if (!findFlag) {
    openedSubPage.value.push({
      appCode: appInfoStore.currentApp.app_code,
      pageCode: page.pageCode,
      pageName: page.pageName,
      pageIcon: page.pageIcon,
      pageSource: page.pageSource
    });
  }
  workflowStore.currentFlow.workflow_code = page.pageCode;
  // 保存至localstorage
  localStorage.setItem('openedSubPage', JSON.stringify(openedSubPage.value));
  workflowStore.showAgentApp = false;
  workflowStore.showNodeFlag = false;
  workflowStore.showEdgeFlag = false;
  currentPage.value = page;
  if (page.pageSource === 'appConfig') {
    router.push({
      name: 'configEdit',
      params: {
        area: page.pageCode
      }
    });
  } else if (page.pageSource === 'workflow') {
    // 跳转到工作流编辑页面
    await router.push({
      name: 'workflowEdit',
      params: {
        workflowCode: page.pageCode
      }
    });
  }
}
async function closeSubPage(page: ISubPage) {
  // 关闭子页面
  const index = openedSubPage.value.findIndex(item => item.pageCode === page.pageCode);
  openedSubPage.value.splice(index, 1);
  // 保存工作流
  if (currentPage.value?.pageSource == 'workflow' && currentPage.value?.pageCode == page.pageCode) {
    const graphData = workflowStore.graphWrapper?.toJSON();
    if (graphData) {
      workflowUpdate({
        app_code: appInfoStore.currentApp.app_code,
        workflow_code: workflowStore.currentFlow.workflow_code,
        workflow_edit_schema: workflowStore.graphWrapper?.toJSON()
      });
    }
    workflowStore.currentFlow.workflow_code = '';
  }
  // 跳转到上一个页面
  if (openedSubPage.value.length > 0) {
    const targetSubPage = openedSubPage.value[openedSubPage.value.length - 1];
    if (targetSubPage.pageSource == 'workflow') {
      await openSubPage(targetSubPage);
    }
  } else {
    currentPage.value = {
      appCode: '',
      pageCode: '',
      pageName: '',
      pageIcon: '',
      pageSource: ''
    };
    await router.push({
      name: 'appDetail',
      params: {
        app_code: appInfoStore.currentApp.app_code
      }
    });
  }
  localStorage.setItem('openedSubPage', JSON.stringify(openedSubPage.value));
}
async function openWorkFlowEdit(workflow: IWorkflowMetaInfo) {
  // 加入到已打开的子页面列表
  let findFlag = false;
  openedSubPage.value.forEach(item => {
    if (item.pageCode === workflow.workflow_code) {
      findFlag = true;
    }
  });
  if (!findFlag) {
    openedSubPage.value.push({
      appCode: appInfoStore.currentApp.app_code,
      pageCode: workflow.workflow_code,
      pageName: workflow.workflow_name,
      pageIcon: workflow.workflow_icon,
      pageSource: 'workflow'
    });
  }
  // 跳转到子页面
  await router.push({
    name: 'workflowEdit',
    params: {
      workflowCode: workflow.workflow_code
    }
  });
  // 保存至localstorage
  localStorage.setItem('openedSubPage', JSON.stringify(openedSubPage.value));
  // 更新当前编辑的agent
  // 获取测试会话
  await workflowStore.getWorkFlowSession(workflow);
  currentPage.value = {
    appCode: appInfoStore.currentApp.app_code,
    pageCode: workflow.workflow_code,
    pageName: workflow.workflow_name,
    pageIcon: workflow.workflow_icon,
    pageSource: 'workflow'
  };
  workflowStore.showAgentApp = false;
  workflowStore.showNodeFlag = false;
  workflowStore.showEdgeFlag = false;
}
async function addNewTestSession() {
  workflowStore.updateCurrentEditSession(
    await appInfoStore.agentAppRef?.initTestSession(appInfoStore.currentApp.app_code, null)
  );
  workflowStore.showAgentApp = true;
  workflowStore.getWorkFlowSession(workflowStore.currentFlow);
}
function cancelLoadWorkFlow() {
  showNewWorkFlowUploadForm.value = false;
  uploadWorkFlowLoading.value = false;
  newUploadWorkFlowForm.uploadFileUrl = '';
  uploadRef.value!.clearFiles();
}
async function openConfigEdit(area: IConfigArea) {
  let findFlag = false;
  openedSubPage.value.forEach(item => {
    if (item.pageCode === area.area) {
      findFlag = true;
    }
  });
  if (!findFlag) {
    openedSubPage.value.push({
      appCode: appInfoStore.currentApp.app_code,
      pageCode: area.area,
      pageName: area.label,
      pageIcon: area.icon,
      pageSource: 'appConfig'
    });
  }
  await router.push({
    name: 'configEdit',
    params: {
      area: area.area
    }
  });
  // 保存至localstorage
  localStorage.setItem('openedSubPage', JSON.stringify(openedSubPage.value));
  currentPage.value = {
    appCode: appInfoStore.currentApp.app_code,
    pageCode: area.area,
    pageName: area.label,
    pageIcon: area.icon,
    pageSource: 'appConfig'
  };
}
async function initCurrentSubPage() {
  if (router.currentRoute.value.name == 'workflowEdit') {
    currentPage.value = {
      appCode: appInfoStore.currentApp.app_code,
      pageCode: router.currentRoute.value.params.workflowCode as string,
      pageName: workflowStore.currentFlow.workflow_name,
      pageIcon: workflowStore.currentFlow.workflow_icon,
      pageSource: 'workflow'
    };
    // 加入到已打开的子页面列表
    let findFlag = false;
    openedSubPage.value.forEach(item => {
      if (item.pageCode === currentPage.value.pageCode) {
        findFlag = true;
      }
    });
    if (!findFlag) {
      openedSubPage.value.push(currentPage.value);
    }
  } else if (router.currentRoute.value.name == 'configEdit') {
    currentPage.value = {
      appCode: appInfoStore.currentApp.app_code,
      pageCode: router.currentRoute.value.params.area[0],
      pageName: appInfoStore.currentAppConfigArea.label,
      pageIcon: appInfoStore.currentAppConfigArea.icon,
      pageSource: 'appConfig'
    };
  }
}
function beginRestoreWorkflowSchema(workflow) {
  showRestoreConfirm.value = true;
  restoreFlow.value = workflow;
}
async function restoreWorkflowSchema() {
  const res = await workflowRestore({
    app_code: appInfoStore.currentApp.app_code,
    workflow_code: restoreFlow.value.workflow_code
  });
  if (!res.error_status) {
    showRestoreConfirm.value = false;
    ElMessage.success('恢复成功');
    await openWorkFlowEdit(restoreFlow.value);
  } else {
    ElMessage.error('恢复失败');
  }
  restoreFlow.value = null;
}

watch(
  () => prop.appCode,
  async newVal => {
    if (newVal) {
      await initCurrentApp(newVal);
    } else {
      await router.push({
        name: 'appList'
      });
      return;
    }
  },
  { immediate: true }
);
onMounted(async () => {
  if (router.currentRoute.value.query?.showPanel != 'false') {
    openPanel();
  } else {
    closePanel();
  }
  if (router.currentRoute.value.name == 'appDetail') {
    await autoOpenFlow();
  }
  initCurrentSubPage();
});
</script>

<template>
  <el-container>
    <el-header style="padding: 0">
      <div id="app-head">
        <div id="app-head-left">
          <div>
            <el-image :src="appInfoStore.currentApp.app_icon" class="icon-button" />
          </div>
          <div>
            <el-text style="font-size: 20px; max-width: 300px" truncated>
              {{ appInfoStore.currentApp?.app_name }}
            </el-text>
          </div>
          <div>
            <el-button :icon="Edit" text type="primary" @click="metaDialogFlag = true" />
          </div>
        </div>
        <div id="app-head-middle">
          <el-radio-group v-model="currentAppMode">
            <el-radio-button value="logic">业务逻辑</el-radio-button>
            <el-radio-button value="ui" disabled>前端组件</el-radio-button>
          </el-radio-group>
        </div>
        <div id="app-head-right">
          <div>
            <el-button type="primary" @click="routerToPublish()"> 发布应用 </el-button>
          </div>
        </div>
      </div>
    </el-header>
    <el-main style="padding: 0">
      <el-container>
        <el-aside v-if="showSetPanel" width="200px">
          <div id="panel-box">
            <div id="panel-head">
              <div>
                <el-text> 控制面板 </el-text>
              </div>
              <div>
                <el-button text :icon="Expand" class="icon-button" @click="closePanel" />
              </div>
            </div>
            <el-scrollbar>
              <div id="panel-body">
                <div class="panel-item">
                  <div class="panel-item-head">
                    <div class="panel-item-head-left" @click="currentFlowListDetail = !currentFlowListDetail">
                      <div class="std-middle-box">
                        <el-icon v-if="currentFlowListDetail" text class="panel-icon">
                          <ArrowDown />
                        </el-icon>
                        <el-icon v-else text class="panel-icon">
                          <ArrowRight />
                        </el-icon>
                      </div>
                      <div>
                        <el-text class="panel-label"> 流程设计 </el-text>
                      </div>
                    </div>
                    <div class="panel-item-head-right">
                      <el-dropdown>
                        <el-button text :icon="Plus" />
                        <template #dropdown>
                          <el-dropdown-menu>
                            <el-dropdown-item @click="beginInitWorkFlow"> 新建工作流 </el-dropdown-item>
                            <el-dropdown-item @click="showNewWorkFlowUploadForm = true"> 导入工作流 </el-dropdown-item>
                          </el-dropdown-menu>
                        </template>
                      </el-dropdown>
                    </div>
                  </div>
                  <div v-show="currentFlowListDetail" class="panel-item-body">
                    <div
                      v-for="workflow in currentFlowList"
                      :key="workflow.id"
                      class="agent-box"
                      :class="workflow.workflow_code === currentPage?.pageCode ? 'agent-box-active' : ''"
                      @click="openWorkFlowEdit(workflow)"
                    >
                      <el-badge :hidden="!workflow?.workflow_is_main" :offset="[-160, 0]" is-dot>
                        <div class="agent-box-left">
                          <div class="std-middle-box">
                            <el-image :src="workflow.workflow_icon" class="agent-icon" />
                          </div>
                          <el-tooltip :content="workflow.workflow_desc" :show-after="1000" placement="top">
                            <div class="std-middle-box">
                              <el-text truncated style="width: 130px" size="small">
                                {{ workflow.workflow_name }}
                              </el-text>
                            </div>
                          </el-tooltip>
                        </div>
                      </el-badge>

                      <div class="std-middle-box" @click.stop>
                        <el-dropdown trigger="click">
                          <div class="std-middle-box">
                            <el-icon style="cursor: pointer">
                              <MoreFilled />
                            </el-icon>
                          </div>
                          <template #dropdown>
                            <el-dropdown-menu>
                              <el-dropdown-item @click="beginUpdateWorkFlow(workflow)"> 修改 </el-dropdown-item>
                              <el-dropdown-item @click="beginDeleteWorkFlow(workflow)"> 删除 </el-dropdown-item>
                              <el-dropdown-item @click="setMainWorkflow(workflow)"> 设为主流程 </el-dropdown-item>
                              <el-dropdown-item @click="exportTargetWorkflow(workflow)"> 导出 </el-dropdown-item>
                              <el-dropdown-item @click="beginRestoreWorkflowSchema(workflow)"> 恢复 </el-dropdown-item>
                            </el-dropdown-menu>
                          </template>
                        </el-dropdown>
                      </div>
                    </div>
                  </div>
                  <div v-show="!currentFlowList?.length && currentFlowListDetail">
                    <el-empty description="暂无主流程，赶快创建一个吧！" />
                  </div>
                </div>
                <div class="panel-item">
                  <div class="panel-item-head">
                    <div class="panel-item-head-left" @click="currentAppConfigFlag = !currentAppConfigFlag">
                      <div class="std-middle-box">
                        <el-icon v-if="currentAppConfigFlag" text class="panel-icon">
                          <ArrowDown />
                        </el-icon>
                        <el-icon v-else text class="panel-icon">
                          <ArrowRight />
                        </el-icon>
                      </div>
                      <div>
                        <el-text class="panel-label"> 应用配置 </el-text>
                      </div>
                    </div>
                  </div>
                  <div v-show="currentAppConfigFlag" class="panel-item-body">
                    <div
                      v-for="area in appInfoStore.configArea"
                      :key="area.area"
                      class="agent-box"
                      :class="area.area === currentPage?.pageCode ? 'agent-box-active' : ''"
                      @click="openConfigEdit(area)"
                    >
                      <div class="agent-box-left">
                        <div>
                          <el-image :src="area.icon" class="agent-icon" />
                        </div>
                        <div>
                          <el-text> {{ area.label }} </el-text>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-show="currentPage.pageSource == 'workflow'" class="panel-item">
                  <div class="panel-item-head">
                    <div class="panel-item-head-left" @click="currentSessionListFlag = !currentSessionListFlag">
                      <div class="std-middle-box">
                        <el-icon v-if="currentSessionListFlag" text class="panel-icon">
                          <ArrowDown />
                        </el-icon>
                        <el-icon v-else text class="panel-icon">
                          <ArrowRight />
                        </el-icon>
                      </div>
                      <div>
                        <el-text class="panel-label"> 测试会话 </el-text>
                      </div>
                    </div>

                    <div class="panel-item-head-right">
                      <el-button text :icon="Plus" @click="addNewTestSession" />
                    </div>
                  </div>
                  <div v-show="currentSessionListFlag" class="panel-item-body">
                    <div
                      v-for="session in workflowStore.currentSessionList"
                      :key="session.id"
                      class="session-item-box"
                      :class="
                        session.session_code === workflowStore.currentEditSession?.session_code
                          ? 'session-item-box-active'
                          : ''
                      "
                      @click="changeTestSession(session)"
                    >
                      <div v-if="session?.is_edit" style="z-index: 999">
                        <el-input
                          ref="currentSessionTopicInputRef"
                          v-model="session.session_topic"
                          placeholder="请输入会话名称"
                          @change="panelRewriteSessionTopic(session)"
                        />
                      </div>
                      <div v-else class="session-topic-box">
                        <el-text
                          truncated
                          class="session-topic-text"
                          :class="{
                            'session-topic-text-active':
                              workflowStore.currentEditSession?.id == session.id && workflowStore.currentEditSession?.id
                          }"
                        >
                          {{ session?.session_topic }}
                        </el-text>
                      </div>
                      <div
                        v-show="
                          workflowStore.currentEditSession?.id == session.id && workflowStore.currentEditSession?.id
                        "
                        class="session-more-button"
                      >
                        <el-popover ref="sessionButtonsRef" trigger="click">
                          <template #reference>
                            <div class="std-middle-box">
                              <el-icon size="12">
                                <MoreFilled />
                              </el-icon>
                            </div>
                          </template>
                          <div id="session-manage-box">
                            <div class="session-manage-button" @click="focusSessionTopicInput(session)">
                              <div class="std-middle-box">
                                <el-image src="/images/edit_03_grey.svg" class="session-manage-button-icon" />
                              </div>
                              <div class="std-middle-box">
                                <el-text class="session-manage-button-text"> 重命名 </el-text>
                              </div>
                            </div>
                            <el-divider style="margin: 8px 0" />
                            <div class="session-manage-button" @click="panelDeleteSession(session)">
                              <div class="std-middle-box">
                                <el-image src="/images/delete_red.svg" class="session-manage-button-icon" />
                              </div>
                              <div class="std-middle-box">
                                <el-text class="session-manage-button-text" style="color: red"> 删除 </el-text>
                              </div>
                            </div>
                          </div>
                        </el-popover>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </el-scrollbar>
          </div>
        </el-aside>
        <el-main style="padding: 0">
          <el-header style="padding: 0" height="51px">
            <div id="page-router-area">
              <div v-if="!showSetPanel" class="page-router">
                <el-button text :icon="Fold" class="icon-button" @click="openPanel" />
              </div>
              <div
                v-for="item in openedSubPage"
                :key="item.pageCode"
                class="page-router"
                :class="currentPage?.pageCode === item.pageCode ? 'page-router-active' : ''"
                @click="openSubPage(item)"
              >
                <div>
                  <el-image :src="item.pageIcon" class="panel-icon" />
                </div>
                <div>
                  <el-text>
                    {{ item.pageName }}
                  </el-text>
                </div>
                <div v-if="currentPage?.pageCode === item.pageCode" class="close-button">
                  <el-icon class="icon-button" @click.stop="closeSubPage(item)">
                    <Close />
                  </el-icon>
                </div>
              </div>
            </div>
          </el-header>
          <div v-if="router.currentRoute.value.name == 'appDetail'" class="welcome-area">
            <div class="welcome-container">
              <!-- 图标 -->
              <div class="icon">
                <i class="fa-solid fa-robot" />
              </div>
              <!-- 标题 -->
              <h1 class="title">欢迎使用 AI Agent 工作流</h1>
              <!-- 说明 -->
              <p class="description">AI Agent 工作流可以帮助您自动化完成各种任务，提高工作效率。立即开始体验吧！</p>
              <el-button type="primary" class="new-flow-button" @click="beginInitWorkFlow">
                <el-icon><Plus /></el-icon>
                新建工作流
              </el-button>
              <el-button type="primary" class="new-flow-button" @click="showNewWorkFlowUploadForm = true">
                <el-icon><Plus /></el-icon>
                导入工作流
              </el-button>
            </div>
          </div>
          <router-view />
        </el-main>
      </el-container>
    </el-main>
  </el-container>
  <el-dialog v-model="metaDialogFlag" title="编辑应用">
    <el-form ref="currentAppRef" :model="appInfoStore.currentApp" label-position="top" :rules="newAppFormRules">
      <el-form-item label="应用名称" prop="app_name" required>
        <el-input v-model="appInfoStore.currentApp.app_name" @keydown.enter.prevent />
      </el-form-item>
      <el-form-item label="应用描述" prop="app_desc" required>
        <el-input
          v-model="appInfoStore.currentApp.app_desc"
          type="textarea"
          :rows="8"
          show-word-limit
          maxlength="500"
        />
      </el-form-item>
      <el-form-item label="应用图标" prop="app_icon" required>
        <el-upload
          drag
          :show-file-list="false"
          accept=".png, .jpg, .jpeg, .gif, .bmp, .webp"
          name="app_icon"
          :headers="userInfoStore.userHeader"
          :before-upload="beforeAvatarUpload"
          :action="api.app_icon_upload"
          :on-success="handleAvatarUploadSuccess"
          style="min-width: 160px"
        >
          <div v-if="appInfoStore.currentApp.app_icon">
            <el-image :src="appInfoStore.currentApp.app_icon" style="width: 40px; height: 40px" />
          </div>
          <div v-else>
            <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
            <i class="el-icon-upload" />
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </div>
        </el-upload>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="metaDialogFlag = false"> 取消 </el-button>
      <el-button type="primary" @click="updateCurrentApp"> 更新 </el-button>
    </template>
  </el-dialog>
  <el-dialog v-model="showNewFlowForm" title="新建工作流">
    <el-form ref="newFlowFormRef" :model="defaultFlow" label-position="top" :rules="newFlowFormRules">
      <el-form-item label="工作流名称" prop="workflow_name" required>
        <el-input v-model="defaultFlow.workflow_name" placeholder="请输入工作流名称" @keydown.enter.prevent />
      </el-form-item>
      <el-form-item label="工作流描述" prop="workflow_desc" required>
        <el-input
          v-model="defaultFlow.workflow_desc"
          type="textarea"
          :rows="8"
          show-word-limit
          maxlength="500"
          placeholder="请输入工作流描述, 让大模型知道什么情况下进行调用"
        />
      </el-form-item>
      <el-form-item label="工作流图标" prop="workflow_icon" required>
        <el-upload
          drag
          :show-file-list="false"
          accept=".png, .jpg, .jpeg, .gif, .bmp, .webp"
          name="workflow_icon"
          :headers="userInfoStore.userHeader"
          :before-upload="beforeAvatarUpload"
          :action="api.workflow_icon_upload"
          :on-success="handleWorkFlowIconUploadSuccess"
          style="min-width: 160px"
        >
          <div v-if="defaultFlow.workflow_icon">
            <el-image :src="defaultFlow.workflow_icon" style="width: 40px; height: 40px" />
          </div>
          <div v-else>
            <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
            <i class="el-icon-upload" />
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </div>
        </el-upload>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showNewFlowForm = false"> 取消 </el-button>
      <el-button type="primary" @click="newFlowFormSubmit"> 创建 </el-button>
    </template>
  </el-dialog>
  <el-dialog v-model="showDeleteFlowConfirm" title="删除工作流" width="30%">
    <el-result icon="warning" :title="'是否删除工作流：' + deleteFlow?.workflow_name + '？'" />
    <template #footer>
      <el-button @click="showDeleteFlowConfirm = false"> 取消 </el-button>
      <el-button type="danger" @click="confirmDeleteWorkFlow"> 确认 </el-button>
    </template>
  </el-dialog>
  <el-dialog v-model="showFlowUpdateForm" title="修改工作流">
    <el-form ref="FlowUpdateFormRef" :model="updateFlow" label-position="top" :rules="newFlowFormRules">
      <el-form-item label="名称" prop="workflow_name" required>
        <el-input
          v-model="updateFlow.workflow_name"
          :placeholder="'请输入' + updateFlow.workflow_name + '名称'"
          @keydown.enter.prevent
        />
      </el-form-item>
      <el-form-item label="描述" prop="workflow_desc" required>
        <el-input
          v-model="updateFlow.workflow_desc"
          type="textarea"
          :rows="8"
          show-word-limit
          maxlength="500"
          :placeholder="'请输入描述, 让大模型知道什么情况下进行调用'"
        />
      </el-form-item>
      <el-form-item label="图标" prop="workflow_icon" required>
        <el-upload
          drag
          :show-file-list="false"
          accept=".png, .jpg, .jpeg, .gif, .bmp, .webp"
          name="flow_icon"
          :headers="userInfoStore.userHeader"
          :before-upload="beforeAvatarUpload"
          :action="api.workflow_icon_upload"
          :on-success="handleWorkFlowIconUploadSuccess"
          style="min-width: 160px"
        >
          <div v-if="updateFlow.workflow_icon">
            <el-image :src="updateFlow.workflow_icon" style="width: 40px; height: 40px" />
          </div>
          <div v-else>
            <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
            <i class="el-icon-upload" />
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </div>
        </el-upload>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showFlowUpdateForm = false"> 取消 </el-button>
      <el-button type="primary" @click="confirmUpdateWorkflow"> 更新 </el-button>
    </template>
  </el-dialog>
  <el-dialog v-model="showNewWorkFlowUploadForm" title="导入工作流" width="30%">
    <el-form
      ref="newUploadWorkFlowFormRef"
      v-loading="uploadWorkFlowLoading"
      element-loading-text="努力导入中..."
      :model="newUploadWorkFlowForm"
      :rules="newUploadWorkFlowFormRules"
      label-position="top"
    >
      <el-form-item label="上传工作流文件" prop="uploadFileUrl" required>
        <el-upload
          ref="uploadRef"
          drag
          :show-file-list="true"
          accept=".json"
          :limit="1"
          name="workflow_schema"
          :headers="userInfoStore.userHeader"
          :action="api.workflow_upload"
          :on-exceed="handleExceed"
          :on-success="handleWorkFlowUploadSuccess"
          style="min-width: 160px; width: 100%"
        >
          <div>
            <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
            <i class="el-icon-upload" />
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </div>
        </el-upload>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="cancelLoadWorkFlow"> 取消 </el-button>
      <el-button type="primary" @click="importTargetWorkflow"> 确认导入 </el-button>
    </template>
  </el-dialog>
  <el-dialog v-model="showRestoreConfirm" title="恢复工作流" width="30%">
    <el-result
      icon="warning"
      :title="'是否恢复工作流：' + restoreFlow.workflow_name + ',将工作流定义恢复至上一发布版本？'"
    />
    <template #footer>
      <el-button @click="showRestoreConfirm = false"> 取消 </el-button>
      <el-button type="primary" @click="restoreWorkflowSchema"> 确认 </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
#app-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 12px;
  border-bottom: 1px solid #dcdfe6;
  background-color: #f5f7f9;
}
#app-head-left {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  min-width: 400px;
}
#app-head-middle {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: center;
  min-width: 400px;
}
#app-head-right {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
}
.icon-button {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  &:hover {
    background-color: #f0f1f3;
  }
}
#panel-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: calc(100vh - 120px);
  border-right: 1px solid #dcdfe6;
}
#panel-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 12px;
  border-bottom: 1px solid #dcdfe6;
}
#panel-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 6px;
  max-height: calc(100vh - 160px);
}
.panel-item-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
}
.panel-item-head-left {
  cursor: pointer;
  display: flex;
  flex-direction: row;
  gap: 4px;
  width: 100%;
}
.panel-icon {
  width: 12px;
  height: 12px;
}
.panel-label {
  font-weight: 600;
}
.panel-item-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.agent-box {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 6px 8px;
  background-color: #f9fafb;
  width: calc(100% - 16px);
  cursor: pointer;
  border-radius: 6px;
  align-items: center;
}
.agent-box-active {
  background-color: #e6f7ff; /* 浅蓝色背景 */
  border-left: 3px solid #1890ff; /* 左侧高亮色条 */
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1); /* 柔和阴影 */
  transform: translateY(-1px); /* 轻微上浮效果 */
  transition: all 0.2s ease; /* 平滑过渡 */
  font-weight: 500;
  /* 悬停效果增强 */
}
.agent-box:hover {
  background-color: #eff8ff;
}
.agent-box-left {
  display: flex;
  flex-direction: row;
  gap: 6px;
}
.agent-icon {
  width: 20px;
  height: 20px;
}
#page-router-area {
  display: flex;
  flex-direction: row;
  gap: 4px;
  padding: 4px;
  background-color: white;
  min-height: 40px;
  border-bottom: 1px solid #dcdfe6;
}
.page-router {
  display: flex;
  flex-direction: row;
  gap: 4px;
  padding: 8px;
  cursor: pointer;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  &:hover {
    background: rgb(239, 239, 244);
  }
}
.page-router-active {
  background-color: #e6f7ff;
  border-left: 3px solid #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1); /* 柔和阴影 */
  font-weight: 500;
  transform: translateY(-1px);
  transition: all 0.2s ease; /* 平滑过渡 */
  &:hover {
    background: none;
  }
}

.session-topic-box {
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  width: calc(100% - 24px);
}
.session-item-box {
  display: flex;
  flex-direction: row;
  gap: 8px;
  padding: 4px 8px;
  justify-content: space-between;
  align-items: center;
  border-radius: 8px;
  cursor: pointer;
  width: calc(100% - 16px);
  &:hover {
    background-color: #f5f8ff;
  }
  &:active {
    background-color: #d9d9d9;
  }
}
.session-item-box-active {
  background-color: #e6f7ff;
  border-left: 3px solid #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1); /* 柔和阴影 */
  font-weight: 500;
  transform: translateY(-1px);
  transition: all 0.2s ease; /* 平滑过渡 */
}
.session-manage-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  cursor: pointer;
  width: 100%;
  &:hover {
    background-color: #f5f8ff;
  }
  &:active {
    transform: scale(0.95);
  }
}
.session-manage-button-icon {
  width: 16px;
  height: 16px;
}
.session-manage-button-text {
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
  color: #101828;
}
.more-filled {
  cursor: pointer;
  &:focus {
    outline: none;
  }
}
.welcome-area {
  display: flex;
  align-items: center;
  justify-content: center;
  height: calc(100% - 200px);
}
.welcome-container {
  background-color: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.icon {
  font-size: 80px;
  color: #007bff;
  margin-bottom: 20px;
}

.title {
  font-size: 32px;
  color: #333;
  margin-bottom: 10px;
}

.description {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
}
.session-more-button {
  width: 20px;
}
</style>
