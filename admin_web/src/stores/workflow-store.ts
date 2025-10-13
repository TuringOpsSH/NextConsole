import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import { search_session as searchSession } from '@/api/next-console';

import { IWorkflowMetaInfo, IWorkflowNodeInfo, IWorkflowEdgeInfo } from '@/types/app-center-type';
import { ISessionItem } from '@/types/next-console';

export const useWorkflowStore = defineStore('workFlow', () => {
  const graphWrapper = ref(null);
  const currentFlow = reactive<IWorkflowMetaInfo>({
    workflow_code: '',
    workflow_desc: '',
    workflow_icon: '',
    workflow_name: '',
    workflow_schema: '',
    workflow_edit_schema: '',
    workflow_status: '',
    id: 0,
    create_time: '',
    update_time: ''
  });
  const currentSessionList = ref<ISessionItem[]>([]);
  const currentEditSession = reactive<ISessionItem>({
    id: 0,
    session_code: ''
  });
  const showNodeFlag = ref(false);
  const showEdgeFlag = ref(false);
  const showAgentApp = ref(false);
  const loadingNodeInfo = ref(false);
  const loadingEdgeInfo = ref(false);
  const showDeleteNodeConfirm = ref(false);
  const selectedNodes = ref<any[]>([]);
  const selectedEdges = ref<any[]>([]);
  const currentNodeDetail = reactive<Partial<IWorkflowNodeInfo | null>>({
    node_id: ''
  });
  const currentEdgeDetail = reactive<IWorkflowEdgeInfo | null>({});
  function updateCurrentSessionList(newList: ISessionItem[]) {
    currentSessionList.value = newList;
  }

  async function getWorkFlowSession(workflow: IWorkflowMetaInfo) {
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

  function updateCurrentFlow(newFlow: IWorkflowMetaInfo) {
    Object.assign(currentFlow, newFlow);
  }

  function updateCurrentEditSession(newSession: ISessionItem) {
    Object.assign(currentEditSession, newSession);
  }

  function updateCurrentEditNodeDetail(newNodeDetail: IWorkflowNodeInfo) {
    Object.assign(currentNodeDetail, newNodeDetail);
  }
  function updateCurrentEditEdgeDetail(newEdgeDetail: IWorkflowEdgeInfo) {
    Object.assign(currentEdgeDetail, newEdgeDetail);
  }

  function updateGraphWrapper(wrapper: any) {
    graphWrapper.value = wrapper;
  }

  return {
    graphWrapper,
    currentFlow,
    currentSessionList,
    currentEditSession,
    showNodeFlag,
    showEdgeFlag,
    showAgentApp,
    loadingNodeInfo,
    loadingEdgeInfo,
    showDeleteNodeConfirm,
    selectedNodes,
    selectedEdges,
    currentNodeDetail,
    currentEdgeDetail,
    updateCurrentSessionList,
    getWorkFlowSession,
    updateCurrentFlow,
    updateCurrentEditSession,
    updateCurrentEditNodeDetail,
    updateCurrentEditEdgeDetail,
    updateGraphWrapper
  };
});
