import {Graph} from '@antv/x6';
import {ElMessage} from 'element-plus';
import {nextTick, ref} from 'vue';
import {nodeDelete, nodeInit, workflowDetail, workflowUpdate} from '@/api/appCenterApi';
import {currentApp, getWorkFlowSession} from '@/components/appCenter/ts/app-detail';
import {IWorkflowEdgeInfo, IWorkflowMetaInfo, IWorkflowNodeInfo} from '@/types/appCenterType';

export const CurrentEditFlow = ref<IWorkflowMetaInfo>({
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
export const CurrentEditSession = ref();
export const graphWrapper = ref(null);
export const showNodeFlag = ref(false);
// @ts-ignore
export const currentNodeDetail = ref<IWorkflowNodeInfo | null>({});
export const loadingNodeInfo = ref(false);
export const selectedNodes = ref([]);
export const selectedEdges = ref([]);
export const showAgentApp = ref(false);
export const showDeleteNodeConfirm = ref(false);
export const showEdgeFlag = ref(false);
export const loadingEdgeInfo = ref(false);
export const currentEdgeDetail = ref<IWorkflowEdgeInfo | null>({});
export async function initCurrentWorkflowEdit(appCode: string, workflowCode: string, auto = true) {
  // 初始化当前编辑的工作流
  const res = await workflowDetail({
    app_code: appCode,
    workflow_code: workflowCode
  });
  if (!res.error_status) {
    CurrentEditFlow.value = res.result;
    // 初始化画布
    if (graphWrapper.value) {
      if (Object.keys(res.result.workflow_edit_schema).length) {
        await graphWrapper.value.fromJSON(res.result.workflow_edit_schema);
      } else {
        // 清空数据
        graphWrapper.value.fromJSON({});
      }
    }
  }
  // 初始化开始和结束节点
  if (graphWrapper.value) {
    const nodes = graphWrapper.value.getNodes();
    if (nodes.length === 0 && auto) {
      await addStartNode();
      await addEndNode();
    }
  }
  await getWorkFlowSession(CurrentEditFlow.value);
  optimizedLayout();
}
export function optimizedLayout() {
  graphWrapper.value?.centerContent();
}
export async function addStartNode() {
  if (graphWrapper.value) {
    const newPosition = generateNewNodePosition(graphWrapper.value);
    const newNode = await graphWrapper.value.addNode({
      shape: 'custom-vue-node',
      x: newPosition.x,
      y: newPosition.y,
      data: {
        nodeType: 'start',
        nodeDesc: '开始节点',
        nodeName: '开始',
        nodeIcon: 'images/node_start.svg',
        nodeInput: 'string',
        nodeOutput: 'string',
        nodeModel: ''
      }
    });
    // 初始化节点
    const addRes = await nodeInit({
      app_code: currentApp.app_code,
      workflow_code: CurrentEditFlow.value.workflow_code,
      node_code: newNode.id,
      node_type: 'start',
      node_name: '开始',
      node_desc: '开始节点可以获取系统变量与设定工作流输入变量',
      node_icon: 'images/node_start.svg'
    });
    if (addRes.error_status) {
      // 移除节点
      graphWrapper.value.removeNode(newNode);
      return false;
    }
    const graphData = graphWrapper.value.toJSON();
    if (graphData) {
      await workflowUpdate({
        app_code: currentApp.app_code,
        workflow_code: CurrentEditFlow.value.workflow_code,
        workflow_edit_schema: graphData
      });
    }

  }
}
export async function addEndNode() {
  if (graphWrapper.value) {
    const newPosition = generateNewNodePosition(graphWrapper.value);
    const newNode = graphWrapper.value.addNode({
      shape: 'custom-vue-node',
      x: newPosition.x,
      y: newPosition.y,
      data: {
        nodeType: 'end',
        nodeDesc: '结束节点用于标识工作流的最终状态与输出数据',
        nodeName: '结束',
        nodeIcon: 'images/node_end.svg',
        nodeInput: 'string',
        nodeOutput: '返回文本',
        nodeModel: ''
      }
    });
    // 初始化节点
    const addRes = await nodeInit({
      app_code: currentApp.app_code,
      workflow_code: CurrentEditFlow.value.workflow_code,
      node_code: newNode.id,
      node_type: 'end',
      node_name: '结束',
      node_desc: '结束节点用于标识工作流的最终状态与输出数据',
      node_icon: 'images/node_end.svg'
    });
    if (addRes.error_status) {
      // 移除节点
      graphWrapper.value.removeNode(newNode);
      return false;
    }
    const graphData = graphWrapper.value.toJSON();
    if (graphData) {
      await workflowUpdate({
        app_code: currentApp.app_code,
        workflow_code: CurrentEditFlow.value.workflow_code,
        workflow_edit_schema: graphData
      });
    }

  }
}
function generateNewNodePosition(graph: Graph) {
  const nodes = graph.getNodes();
  // 如果图为空，返回画布中央的坐标
  if (nodes.length === 0) {
    const { width, height } =
      graph.options.width && graph.options.height
        ? { width: graph.options.width, height: graph.options.height }
        : { width: 800, height: 600 }; // 默认画布大小
    return {
      x: width / 2,
      y: height / 2
    };
  }
  const lastNode = nodes[nodes.length - 1];
  const lastNodeBBox = lastNode?.getBBox();
  return {
    x: lastNodeBBox?.x + lastNodeBBox?.width + 50,
    y: lastNodeBBox?.y
  };
}
export async function keyboardDeleteNode() {
  if (!selectedNodes.value.length && !selectedEdges.value.length) {
    return;
  }
  if (!graphWrapper.value) {
    return;
  }
  // 开始节点不能删除
  const startNode = graphWrapper.value.getNodes().find(node => node.data.nodeType === 'start');
  if (startNode && selectedNodes.value.includes(startNode)) {
    ElMessage.info('开始节点不能删除');
    return;
  }
  // 结束节点不能删除
  const endNode = graphWrapper.value.getNodes().find(node => node.data.nodeType === 'end');
  if (endNode && selectedNodes.value.includes(endNode)) {
    ElMessage.info('结束节点不能删除');
    return;
  }
  if (selectedNodes.value.length) {
    // 去重
    selectedNodes.value = Array.from(new Set(selectedNodes.value));
    showDeleteNodeConfirm.value = true;
    return;
  }
  // 遍历选中的边
  selectedEdges.value.forEach(edge => {
    // 删除边
    graphWrapper.value.removeEdge(edge);
  });
  selectedEdges.value = [];
  // 保存数据
  const graphData = graphWrapper.value.toJSON();
  if (graphData) {
    workflowUpdate({
      app_code: currentApp.app_code,
      workflow_code: CurrentEditFlow.value.workflow_code,
      workflow_edit_schema: graphData
    });
  }

  ElMessage.success('删除成功');
  showNodeFlag.value = false;
  showEdgeFlag.value = false;
  await nextTick();

}
export async function deleteCurrentNode() {
  const params = {
    app_code: currentApp.app_code,
    workflow_code: CurrentEditFlow.value.workflow_code,
    nodes: []
  };
  for (let i = 0; i < selectedNodes.value.length; i++) {
    params.nodes.push(selectedNodes.value[i].id);
  }
  if (!params.nodes.length) {
    return;
  }
  const res = await nodeDelete(params);
  if (res.error_status) {
    return;
  }
  // 遍历选中的边
  selectedEdges.value.forEach(edge => {
    // 删除边
    graphWrapper.value.removeEdge(edge);
  });
  // 遍历选中的节点
  selectedNodes.value.forEach(node => {
    // 获取与该节点关联的边
    const connectedEdges = graphWrapper.value.getConnectedEdges(node);

    // 删除关联的边
    connectedEdges.forEach((edge: any) => {
      graphWrapper.value.removeEdge(edge);
    });

    // 删除节点
    graphWrapper.value.removeNode(node);
  });

  // 清空选中数组
  selectedNodes.value = [];
  selectedEdges.value = [];

  // 保存数据
  const graphData = graphWrapper.value.toJSON();
  if (graphData) {
    workflowUpdate({
      app_code: currentApp.app_code,
      workflow_code: CurrentEditFlow.value.workflow_code,
      workflow_edit_schema: graphData
    });
  }
  showDeleteNodeConfirm.value = false;
  ElMessage.success('删除成功');
  showNodeFlag.value = false;
  showEdgeFlag.value = false;
  await nextTick();
}

// @ts-ignore
export const agentAppRef = ref();
