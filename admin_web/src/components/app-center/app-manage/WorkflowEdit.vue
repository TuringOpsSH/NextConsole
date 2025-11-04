<script setup lang="ts">
import { Graph } from '@antv/x6';
import { Export } from '@antv/x6-plugin-export';
import { Keyboard } from '@antv/x6-plugin-keyboard';
import { Snapline } from '@antv/x6-plugin-snapline';
import { getTeleport, register } from '@antv/x6-vue-shape';
import { Bell, MagicStick, Plus, VideoPlay, Connection, Lock, Unlock } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { defineProps, onMounted, ref, watch, nextTick } from 'vue';
import {
  nodeDelete,
  nodeDetail,
  nodeInit,
  nodeSearch,
  workflowCheck,
  workflowDetail,
  workflowUpdate
} from '@/api/app-center-api';
import WorkFlowEdgeEdit from '@/components/app-center/app-manage/WorkFlowEdgeEdit.vue';
import WorkFlowNodeEdit from '@/components/app-center/app-manage/WorkFlowNodeEdit.vue';
import WorkflowNode from '@/components/app-center/app-manage/WorkflowNode.vue';
import AgentApp from '@/components/app-center/app-preview/AgentApp.vue';

import router from '@/router';
import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';

const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
register({
  shape: 'custom-vue-node',
  width: 300,
  height: 100,
  component: WorkflowNode,
  ports: {
    groups: {
      top: {
        position: 'left',
        attrs: {
          circle: {
            r: 4,
            magnet: true,
            stroke: '#31d0c6',
            strokeWidth: 2,
            fill: '#fff'
          }
        }
      },
      bottom: {
        position: 'right',
        attrs: {
          circle: {
            r: 4,
            magnet: true,
            stroke: '#31d0c6',
            strokeWidth: 2,
            fill: '#fff'
          }
        }
      }
    },
    items: [
      {
        group: 'top'
      },
      {
        group: 'bottom'
      }
    ]
  }
});
const TeleportContainer = getTeleport();
const props = defineProps({
  workflowCode: {
    type: String,
    default: ''
  },
  appCode: {
    type: String,
    default: ''
  }
});
const workflowAlters = ref([]);
const alterRef = ref(null);
const agentAppRef = ref(null);
const globalRouter = ref('metro');
// 定义颜色常量
const SELECTED_COLOR = '#ADD8E6'; // 淡蓝色，可根据需要调整
const UNSELECTED_COLOR = 'black';
// 定义过渡效果时间
const TRANSITION_DURATION = '0.3s';
// 定义选中边的样式
const selectedEdgeStyle = {
  stroke: SELECTED_COLOR,
  strokeWidth: 4,
  filter: `drop-shadow(0 0 5px ${SELECTED_COLOR})`, // 模拟光晕效果
  transition: `stroke ${TRANSITION_DURATION}, stroke-width ${TRANSITION_DURATION}, filter ${TRANSITION_DURATION}`
};
const unselectedEdgeStyle = {
  stroke: UNSELECTED_COLOR,
  strokeWidth: 1,
  filter: 'none',
  transition: `stroke ${TRANSITION_DURATION}, stroke-width ${TRANSITION_DURATION}, filter ${TRANSITION_DURATION}`
};
const workflowNodeRef = ref(null);
const graphLock = ref(false);
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
async function addAgentNode(nodeType: string) {
  if (workflowStore.graphWrapper) {
    const newPosition = generateNewNodePosition(workflowStore.graphWrapper);
    const data = {
      nodeInput: 'string',
      nodeOutput: 'string',
      nodeModel: '',
      nodeIcon: '/images/node_llm.svg',
      nodeType: 'llm',
      nodeDesc: '通过大语言模型构建Agent，智能生成回复',
      nodeName: 'Agent节点'
    };
    if (nodeType == 'tool') {
      data.nodeIcon = '/images/node_api.svg';
      data.nodeType = 'tool';
      data.nodeDesc = '通过api调用外部工具，扩展Agent能力';
      data.nodeName = '工具调用';
    } else if (nodeType == 'rag') {
      data.nodeIcon = '/images/node_rag.svg';
      data.nodeType = 'rag';
      data.nodeDesc = '通过调用外部知识，扩展Agent能力';
      data.nodeName = '知识调用';
    } else if (nodeType == 'file_reader') {
      data.nodeIcon = '/images/node_file_reader.svg';
      data.nodeType = 'file_reader';
      data.nodeDesc = '读取文件为指定格式，供Agent使用';
      data.nodeName = '文件阅读';
    } else if (nodeType == 'file_splitter') {
      data.nodeIcon = '/images/node_file_splitter.svg';
      data.nodeType = 'file_splitter';
      data.nodeDesc = '将文本切分段落，供Agent使用';
      data.nodeName = '文本切分';
    } else if (nodeType == 'workflow') {
      data.nodeIcon = '/images/node_flow.svg';
      data.nodeType = 'workflow';
      data.nodeDesc = '调用执行其他工作流';
      data.nodeName = '工作流节点';
    }
    const newNode = workflowStore.graphWrapper.addNode({
      shape: 'custom-vue-node',
      x: newPosition.x,
      y: newPosition.y,
      data: data
    });
    // 初始化节点
    const addRes = await nodeInit({
      app_code: appInfoStore.currentApp.app_code,
      workflow_code: workflowStore.currentFlow.workflow_code,
      node_code: newNode.id,
      node_type: nodeType,
      node_name: data.nodeName,
      node_desc: data.nodeDesc,
      node_icon: data.nodeIcon,
      node_llm_code: ''
    });
    if (addRes.error_status) {
      // 移除节点
      workflowStore.graphWrapper.removeNode(newNode);
      return false;
    }
    workflowStore.graphWrapper.centerCell(newNode);
    const graphData = workflowStore.graphWrapper.toJSON();
    if (graphData) {
      workflowUpdate({
        app_code: appInfoStore.currentApp.app_code,
        workflow_code: workflowStore.currentFlow.workflow_code,
        workflow_edit_schema: graphData
      });
    }
  }
}
function optimizedLayout() {
  workflowStore.graphWrapper?.centerContent();
}
async function runWorkflow() {
  const res = await preCheckWorkflow();
  if (!res) {
    ElMessage.warning({
      message: '工作流配置不完整，请检查工作流配置',
      duration: 2000
    });
    return;
  }
  workflowStore.updateCurrentEditSession(
    await appInfoStore.agentAppRef?.initTestSession(appInfoStore.currentApp.app_code, true)
  );
  workflowStore.showAgentApp = true;
  workflowStore.getWorkFlowSession(workflowStore.currentFlow);
}
async function preCheckWorkflow() {
  // 检查工作流合法性，提醒用户修改
  // rule1: 开始节点与结束节点必须联通
  let newWorkflowAlters = [];
  const startNode = workflowStore.graphWrapper.getNodes().filter(node => node.data.nodeType === 'start');
  const endNode = workflowStore.graphWrapper.getNodes().filter(node => node.data.nodeType === 'end');
  if (!startNode?.length || !endNode.length) {
    return;
  }
  const shortestPath = workflowStore.graphWrapper.getShortestPath(startNode[0], endNode[0], {
    directed: true
  });
  if (!shortestPath?.length) {
    // 存在已有告警则跳过
    newWorkflowAlters.push({
      id: 'alter1',
      title: `工作流${workflowStore.currentFlow.workflow_name}不完整:开始节点与结束节点未联通`,
      type: 'error'
    });
  }
  // rule2: 工作流中必须有开始节点和结束节点
  if (startNode.length === 0 || endNode.length === 0) {
    newWorkflowAlters.push({
      id: 'alter2',
      title: `初始化异常:工作流${workflowStore.currentFlow.workflow_name}：必须有开始节点和结束节点，请创建新工作流`,
      type: 'error'
    });
  }
  // rule3: 工作流中不建议存在不可达节点
  const rootNodes = workflowStore.graphWrapper.getRootNodes();
  if (rootNodes.length > 1) {
    newWorkflowAlters.push({
      id: 'alter3',
      title: `工作流${workflowStore.currentFlow.workflow_name}：存在孤立节点，请检查工作流配置`,
      type: 'info'
    });
  }
  if (!appInfoStore.currentApp.app_code) {
    newWorkflowAlters.push({
      id: 'alter4',
      title: `应用信息获取异常，请重新进入该页面`,
      type: 'error'
    });
  }
  const res = await workflowCheck({
    app_code: appInfoStore.currentApp.app_code,
    workflow_code: workflowStore.currentFlow.workflow_code
  });
  if (!res.error_status) {
    for (let i of res.result) {
      newWorkflowAlters.push(i);
    }
    if (!res.result.length) {
      newWorkflowAlters = [];
    }
  }
  // 按照告警级别排序
  newWorkflowAlters.sort((a, b) => {
    const priority = { error: 3, warning: 2, info: 1 };
    return priority[b.type] - priority[a.type];
  });
  workflowAlters.value = newWorkflowAlters;
  // 如果存在error，则不允许试运行
  return !newWorkflowAlters?.some(alter => alter.type === 'error');
}
function handleClickBlank() {
  workflowStore.showNodeFlag = false;
  workflowStore.showEdgeFlag = false;
  workflowStore.showAgentApp = false;
  // 取消点边的选中
  // 取消节点的选中
  workflowStore.selectedNodes = [];
  // 取消边的选中
  workflowStore.selectedEdges.forEach(edge => {
    edge.setAttrs({ line: unselectedEdgeStyle });
  });
  workflowStore.selectedEdges = [];
  // 保存数据
  const graphData = workflowStore.graphWrapper.toJSON();
  if (graphData) {
    workflowUpdate({
      app_code: appInfoStore.currentApp.app_code,
      workflow_code: workflowStore.currentFlow.workflow_code,
      workflow_edit_schema: graphData
    });
  }
  preCheckWorkflow();
}
function handleClickNode(node: any, e) {
  highlightNode(node, e);
  workflowStore.showAgentApp = false;
  workflowStore.showEdgeFlag = false;
  showNodeDetail(node);
}
function handleClickEdge(edge: any, e) {
  highlightEdge(edge, e);
  workflowStore.showNodeFlag = false;
  workflowStore.showAgentApp = false;
  showEdgeDetail(edge);
}
function highlightEdge(edge: any, e) {
  const isCtrlPressed = e.ctrlKey;

  if (isCtrlPressed) {
    // 如果按下 Ctrl 键，进行多选操作
    if (workflowStore.selectedEdges.includes(edge)) {
      // 如果边已经选中，取消选中
      edge.setAttrs({ line: unselectedEdgeStyle });
      workflowStore.selectedEdges = workflowStore.selectedEdges.filter(ed => ed !== edge);
    } else {
      // 如果边未选中，选中该边
      edge.setAttrs({ line: selectedEdgeStyle });
      workflowStore.selectedEdges.push(edge);
    }
  } else {
    // 如果没有按下 Ctrl 键，取消其他选中的边
    workflowStore.selectedEdges.forEach(ed => {
      ed.setAttrs({ line: unselectedEdgeStyle });
    });
    workflowStore.selectedEdges = [edge];
    edge.setAttrs({ line: selectedEdgeStyle });
  }
}
async function searchNodeUpstream(nodeId: string) {
  const cell = workflowStore.graphWrapper.getCellById(nodeId);
  const predecessors = workflowStore.graphWrapper.getPredecessors(cell, {
    breadthFirst: true,
    deep: true
  });
  // 倒序
  predecessors.reverse();
  // 获取前序节点信息
  const params = {
    app_code: appInfoStore.currentApp.app_code,
    workflow_code: workflowStore.currentFlow.workflow_code,
    node_code: [],
    fetch_all: true
  };
  predecessors.forEach((item: any) => {
    params.node_code.push(item.id);
  });
  const res = await nodeSearch(params);
  if (res.error_status) {
    return;
  }
  const nodeIdMap = {};
  res.result.data.forEach((item: any) => {
    nodeIdMap[item.node_code] = item;
  });
  const nodeUpstream = [];
  for (let i = 0; i < predecessors.length; i++) {
    const predecessorNode = predecessors[i];
    nodeUpstream.push({
      nodeCode: predecessorNode.id,
      nodeName: predecessorNode.data.nodeName,
      nodeIcon: predecessorNode.data.nodeIcon,
      nodeType: predecessorNode.data.nodeType,
      nodeDesc: predecessorNode.data.nodeDesc,
      nodeResultFormat: nodeIdMap?.[predecessorNode.id]?.node_result_format,
      nodeResultJsonSchema: nodeIdMap?.[predecessorNode.id]?.node_result_params_json_schema,
      nodeResultExtractColumns: nodeIdMap?.[predecessorNode.id]?.node_result_extract_columns
    });
  }
  return nodeUpstream;
}
async function showEdgeDetail(edge: any) {
  workflowStore.showEdgeFlag = true;
  workflowStore.loadingEdgeInfo = true;
  if (!edge.getData()) {
    edge.setData({
      edge_icon: '/images/edge.svg',
      edge_name: '关系',
      edge_desc: '通过配置关系上的条件，控制工作流的流向',
      edge_type: '充分',
      edge_code: edge.id,
      edge_condition_type: 'or',
      edge_conditions: []
    });
    edge.prop('labels', ['充分']);
    const graphData = workflowStore.graphWrapper.toJSON();
    if (graphData) {
      workflowUpdate({
        app_code: appInfoStore.currentApp.app_code,
        workflow_code: workflowStore.currentFlow.workflow_code,
        workflow_edit_schema: graphData
      });
    }
  }
  // 补充前序节点信息
  workflowStore.updateCurrentEditEdgeDetail(edge.getData());
  workflowStore.currentEdgeDetail['node_upstream'] = await searchNodeUpstream(edge.id);
  workflowStore.currentEdgeDetail['routerName'] = edge.getRouter()?.name || 'normal';
  workflowStore.loadingEdgeInfo = false;
}
function highlightNode(node, e) {
  const isCtrlPressed = e.ctrlKey;
  if (isCtrlPressed) {
    // 如果按下 Ctrl 键，进行多选操作
    if (workflowStore.selectedNodes.includes(node)) {
      // 如果节点已经选中，取消选中
      workflowStore.selectedNodes = workflowStore.selectedNodes.filter(n => n !== node);
    } else {
      // 如果节点未选中，选中该节点
      workflowStore.selectedNodes.push(node);
    }
  } else {
    // 如果没有按下 Ctrl 键，取消其他选中的节点
    workflowStore.selectedNodes = [node];
  }

  // 高亮关联的边
  workflowStore.graphWrapper.getEdges().forEach(edge => {
    const sourceNode = edge.getSourceNode();
    const targetNode = edge.getTargetNode();
    if (workflowStore.selectedNodes.some(n => n === sourceNode || n === targetNode)) {
      edge.setAttrs({ line: selectedEdgeStyle });
      // 如果不在选中边列表中则加入
      if (!workflowStore.selectedEdges.includes(edge)) {
        workflowStore.selectedEdges.push(edge);
      }
    } else {
      edge.setAttrs({ line: unselectedEdgeStyle });
    }
  });
}
async function showNodeDetail(node: any) {
  workflowStore.showNodeFlag = true;
  workflowStore.loadingNodeInfo = true;
  const nodeRes = await nodeDetail({
    app_code: appInfoStore.currentApp.app_code,
    agent_code: workflowStore.currentFlow.agent_code,
    agent_type: workflowStore.currentFlow.agent_type,
    node_code: node.id
  });
  if (!nodeRes.error_status) {
    workflowStore.updateCurrentEditNodeDetail(nodeRes.result);
  }
  // 补充前序节点信息
  workflowStore.currentNodeDetail['node_upstream'] = await searchNodeUpstream(node.id);
  workflowStore.currentNodeDetail['nodeSelf'] = [
    {
      nodeCode: workflowStore.currentNodeDetail.node_code,
      nodeName: workflowStore.currentNodeDetail.node_name,
      nodeIcon: workflowStore.currentNodeDetail.node_icon,
      nodeType: workflowStore.currentNodeDetail.node_type,
      nodeDesc: workflowStore.currentNodeDetail.node_desc,
      nodeResultFormat: workflowStore.currentNodeDetail.node_result_format,
      nodeResultJsonSchema: workflowStore.currentNodeDetail.node_input_params_json_schema
    }
  ];
  workflowStore.currentNodeDetail['node_upstream2'] = await searchNodeUpstream(node.id);
  workflowStore.currentNodeDetail['node_upstream2'].push({
    nodeCode: workflowStore.currentNodeDetail.node_code,
    nodeName: workflowStore.currentNodeDetail.node_name,
    nodeIcon: workflowStore.currentNodeDetail.node_icon,
    nodeType: workflowStore.currentNodeDetail.node_type,
    nodeDesc: workflowStore.currentNodeDetail.node_desc,
    nodeResultFormat: workflowStore.currentNodeDetail.node_result_format,
    nodeResultJsonSchema: workflowStore.currentNodeDetail.node_result_params_json_schema
  });
  if (workflowStore.currentNodeDetail.node_type == 'workflow') {
    await workflowNodeRef.value?.searchSubWorkflow();
  }
  workflowStore.loadingNodeInfo = false;
}

async function changeAllEdgeRouter(name: string) {
  const allEdges = workflowStore.graphWrapper?.getEdges();
  allEdges.forEach(edge => {
    edge.setRouter({ name: name });
  });
  const graphData = workflowStore.graphWrapper.toJSON();
  if (graphData) {
    await workflowUpdate({
      app_code: appInfoStore.currentApp.app_code,
      workflow_code: workflowStore.currentFlow.workflow_code,
      workflow_edit_schema: graphData
    });
  }
  ElMessage.success('已成功更新了所有边的路由~');
}
async function switchGraphLock() {
  graphLock.value = !graphLock.value;
  if (workflowStore.graphWrapper.options.interacting) {
    workflowStore.graphWrapper.options.interacting = false;
  } else {
    workflowStore.graphWrapper.options.interacting = true;
  }
  if (graphLock.value) {
    workflowStore.graphWrapper.disablePanning();
    workflowStore.graphWrapper.disableMouseWheel();
  } else {
    workflowStore.graphWrapper.enablePanning();
    workflowStore.graphWrapper.enableMouseWheel();
  }
}
async function addStartNode() {
  if (workflowStore.graphWrapper) {
    const newPosition = generateNewNodePosition(workflowStore.graphWrapper);
    const newNode = await workflowStore.graphWrapper.addNode({
      shape: 'custom-vue-node',
      x: newPosition.x,
      y: newPosition.y,
      data: {
        nodeType: 'start',
        nodeDesc: '开始节点',
        nodeName: '开始',
        nodeIcon: '/images/node_start.svg',
        nodeInput: 'string',
        nodeOutput: 'string',
        nodeModel: ''
      }
    });
    // 初始化节点
    const addRes = await nodeInit({
      app_code: appInfoStore.currentApp.app_code,
      workflow_code: workflowStore.currentFlow.workflow_code,
      node_code: newNode.id,
      node_type: 'start',
      node_name: '开始',
      node_desc: '开始节点可以获取系统变量与设定工作流输入变量',
      node_icon: '/images/node_start.svg'
    });
    if (addRes.error_status) {
      // 移除节点
      workflowStore.graphWrapper.removeNode(newNode);
      return false;
    }
    const graphData = workflowStore.graphWrapper.toJSON();
    if (graphData) {
      await workflowUpdate({
        app_code: appInfoStore.currentApp.app_code,
        workflow_code: workflowStore.currentFlow.workflow_code,
        workflow_edit_schema: graphData
      });
    }
  }
}
async function addEndNode() {
  if (workflowStore.graphWrapper) {
    const newPosition = generateNewNodePosition(workflowStore.graphWrapper);
    const newNode = workflowStore.graphWrapper.addNode({
      shape: 'custom-vue-node',
      x: newPosition.x,
      y: newPosition.y,
      data: {
        nodeType: 'end',
        nodeDesc: '结束节点用于标识工作流的最终状态与输出数据',
        nodeName: '结束',
        nodeIcon: '/images/node_end.svg',
        nodeInput: 'string',
        nodeOutput: '返回文本',
        nodeModel: ''
      }
    });
    // 初始化节点
    const addRes = await nodeInit({
      app_code: appInfoStore.currentApp.app_code,
      workflow_code: workflowStore.currentFlow.workflow_code,
      node_code: newNode.id,
      node_type: 'end',
      node_name: '结束',
      node_desc: '结束节点用于标识工作流的最终状态与输出数据',
      node_icon: '/images/node_end.svg'
    });
    if (addRes.error_status) {
      // 移除节点
      workflowStore.graphWrapper.removeNode(newNode);
      return false;
    }
    const graphData = workflowStore.graphWrapper.toJSON();
    if (graphData) {
      await workflowUpdate({
        app_code: appInfoStore.currentApp.app_code,
        workflow_code: workflowStore.currentFlow.workflow_code,
        workflow_edit_schema: graphData
      });
    }
  }
}
async function initCurrentWorkflowEdit(appCode: string, workflowCode: string, auto = true) {
  // 初始化当前编辑的工作流
  const res = await workflowDetail({
    app_code: appCode,
    workflow_code: workflowCode
  });
  if (!res.error_status) {
    workflowStore.updateCurrentFlow(res.result);
    // 初始化画布
    if (workflowStore.graphWrapper) {
      if (Object.keys(res.result.workflow_edit_schema).length) {
        await workflowStore.graphWrapper.fromJSON(res.result.workflow_edit_schema);
      } else {
        // 清空数据
        workflowStore.graphWrapper.fromJSON({});
      }
    }
  }
  // 初始化开始和结束节点
  if (workflowStore.graphWrapper) {
    const nodes = workflowStore.graphWrapper.getNodes();
    if (nodes.length === 0 && auto) {
      await addStartNode();
      await addEndNode();
    }
  }
  await workflowStore.getWorkFlowSession(workflowStore.currentFlow);
  optimizedLayout();
}
async function keyboardDeleteNode() {
  if (!workflowStore.selectedNodes.length && !workflowStore.selectedEdges.length) {
    return;
  }
  if (!workflowStore.graphWrapper) {
    return;
  }
  // 开始节点不能删除
  const startNode = workflowStore.graphWrapper.getNodes().find(node => node.data.nodeType === 'start');
  if (startNode && workflowStore.selectedNodes.includes(startNode)) {
    ElMessage.info('开始节点不能删除');
    return;
  }
  // 结束节点不能删除
  const endNode = workflowStore.graphWrapper.getNodes().find(node => node.data.nodeType === 'end');
  if (endNode && workflowStore.selectedNodes.includes(endNode)) {
    ElMessage.info('结束节点不能删除');
    return;
  }
  if (workflowStore.selectedNodes.length) {
    // 去重
    workflowStore.selectedNodes = Array.from(new Set(workflowStore.selectedNodes));
    workflowStore.showDeleteNodeConfirm = true;
    return;
  }
  // 遍历选中的边
  workflowStore.selectedEdges.forEach(edge => {
    // 删除边
    workflowStore.graphWrapper.removeEdge(edge);
  });
  workflowStore.selectedEdges = [];
  // 保存数据
  const graphData = workflowStore.graphWrapper.toJSON();
  if (graphData) {
    workflowUpdate({
      app_code: appInfoStore.currentApp.app_code,
      workflow_code: workflowStore.currentFlow.workflow_code,
      workflow_edit_schema: graphData
    });
  }

  ElMessage.success('删除成功');
  workflowStore.showNodeFlag = false;
  workflowStore.showEdgeFlag = false;
  await nextTick();
}
async function deleteCurrentNode() {
  const params = {
    app_code: appInfoStore.currentApp.app_code,
    workflow_code: workflowStore.currentFlow.workflow_code,
    nodes: []
  };
  for (let i = 0; i < workflowStore.selectedNodes.length; i++) {
    params.nodes.push(workflowStore.selectedNodes[i].id);
  }
  if (!params.nodes.length) {
    return;
  }
  const res = await nodeDelete(params);
  if (res.error_status) {
    return;
  }
  // 遍历选中的边
  workflowStore.selectedEdges.forEach(edge => {
    // 删除边
    workflowStore.graphWrapper.removeEdge(edge);
  });
  // 遍历选中的节点
  workflowStore.selectedNodes.forEach(node => {
    // 获取与该节点关联的边
    const connectedEdges = workflowStore.graphWrapper.getConnectedEdges(node);

    // 删除关联的边
    connectedEdges.forEach((edge: any) => {
      workflowStore.graphWrapper.removeEdge(edge);
    });

    // 删除节点
    workflowStore.graphWrapper.removeNode(node);
  });

  // 清空选中数组
  workflowStore.selectedNodes = [];
  workflowStore.selectedEdges = [];

  // 保存数据
  const graphData = workflowStore.graphWrapper.toJSON();
  if (graphData) {
    workflowUpdate({
      app_code: appInfoStore.currentApp.app_code,
      workflow_code: workflowStore.currentFlow.workflow_code,
      workflow_edit_schema: graphData
    });
  }
  workflowStore.showDeleteNodeConfirm = false;
  ElMessage.success('删除成功');
  workflowStore.showNodeFlag = false;
  workflowStore.showEdgeFlag = false;
  await nextTick();
}

onMounted(async () => {
  if (!props.workflowCode) {
    await router.push({ name: 'appCenter' });
    return;
  }
  workflowStore.updateGraphWrapper(
    new Graph({
      container: document.getElementById('container'),
      autoResize: true,
      background: {
        color: '#F2F7FA'
      },
      panning: true,
      mousewheel: true,
      grid: {
        visible: true,
        type: 'dot',
        args: {
          color: '#a0a0a0', // 网点颜色
          thickness: 1, // 网点大小
          size: 10 // 网格大小 10px
        }
      },
      connecting: {
        snap: true,
        allowBlank: false, // 允许连接到空白处
        allowLoop: false,
        allowNode: false
      }
    })
  );
  // 对齐线
  workflowStore.graphWrapper.use(
    new Snapline({
      enabled: true
    })
  );
  // 框选
  // workflowStore.graphWrapper.use(
  //   new Selection({
  //     enabled: true,
  //   }),
  // )
  // 导出
  workflowStore.graphWrapper.use(new Export());
  // 快捷键
  workflowStore.graphWrapper.use(
    new Keyboard({
      enabled: true
    })
  );
  // 退格事件
  workflowStore.graphWrapper.bindKey('delete', () => {
    keyboardDeleteNode();
  });
  workflowStore.graphWrapper.bindKey('Backspace', () => {
    keyboardDeleteNode();
  });

  // 新增边响应事件
  workflowStore.graphWrapper.on('edge:connected', ({ isNew, edge }) => {
    if (isNew) {
      // 设置边的 router 为 manhattan
      edge.setRouter({ name: 'normal' });
      edge.setData({
        edge_icon: '/images/edge.svg',
        edge_name: '关系',
        edge_desc: '通过配置关系上的条件，控制工作流的流向',
        edge_type: '默认',
        edge_code: edge.id,
        edge_condition_type: 'or',
        edge_conditions: []
      });
      edge.prop('labels', ['默认']);
    }
    const graphData = workflowStore.graphWrapper.toJSON();
    if (graphData) {
      workflowUpdate({
        app_code: appInfoStore.currentApp.app_code,
        workflow_code: workflowStore.currentFlow.workflow_code,
        workflow_edit_schema: graphData
      });
    }
  });
  // 单击节点事件
  workflowStore.graphWrapper.on('node:click', ({ node, e }) => {
    handleClickNode(node, e);
  });
  // 单击边事件
  workflowStore.graphWrapper.on('edge:click', ({ edge, e }) => {
    handleClickEdge(edge, e);
  });
  // 单击空白事件
  workflowStore.graphWrapper.on('blank:click', () => {
    handleClickBlank();
  });
  appInfoStore.updateAgentAppRef(agentAppRef.value);
});
watch(
  () => props.workflowCode,
  async newVal => {
    if (newVal) {
      await initCurrentWorkflowEdit(props.appCode, newVal, false);
      preCheckWorkflow();
    }
  },
  { immediate: true }
);
defineExpose({
  initCurrentWorkflowEdit,
  preCheckWorkflow
});
</script>

<template>
  <el-container>
    <el-main style="padding: 0">
      <el-scrollbar>
        <div id="edit-area">
          <div id="container" />
          <TeleportContainer />
          <div v-if="graphLock" class="lock-area" />
          <div id="operation-panel">
            <div id="panel-left">
              <div class="std-middle-box">
                <div v-if="!graphLock">
                  <el-tooltip content="锁定画布" placement="top">
                    <el-icon class="panel-icon" @click="switchGraphLock">
                      <Unlock />
                    </el-icon>
                  </el-tooltip>
                </div>
                <div v-else>
                  <el-tooltip content="解锁画布" placement="top">
                    <el-icon class="panel-icon" color="#409eff" @click="switchGraphLock">
                      <Lock />
                    </el-icon>
                  </el-tooltip>
                </div>
              </div>
              <div class="std-middle-box">
                <el-popover placement="top" trigger="click" width="400" title="连线路由">
                  <template #reference>
                    <el-icon class="panel-icon">
                      <Connection />
                    </el-icon>
                  </template>
                  <el-radio-group v-model="globalRouter" size="small" @change="changeAllEdgeRouter">
                    <el-radio-button value="normal"> 普通 </el-radio-button>
                    <el-radio-button value="orth"> 正交 </el-radio-button>
                    <el-radio-button value="oneSide"> 受限正交 </el-radio-button>
                    <el-radio-button value="manhattan"> 智能正交 </el-radio-button>
                    <el-radio-button value="metro"> 地铁 </el-radio-button>
                    <el-radio-button value="er"> 实体关系 </el-radio-button>
                  </el-radio-group>
                </el-popover>
              </div>
              <div class="std-middle-box">
                <el-tooltip content="优化布局" placement="top">
                  <el-icon class="panel-icon" @click="optimizedLayout">
                    <MagicStick />
                  </el-icon>
                </el-tooltip>
              </div>
              <el-dropdown placement="top" size="small" trigger="click">
                <div class="add-node-button">
                  <div class="std-middle-box">
                    <el-icon style="color: #409eff">
                      <Plus />
                    </el-icon>
                  </div>
                  <div class="std-middle-box">
                    <el-text style="color: #409eff; min-width: 70px"> 添加节点 </el-text>
                  </div>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item divided @click="addAgentNode('llm')">
                      <div class="agent-node-option">
                        <div class="std-middle-box">
                          <el-image src="/images/node_llm.svg" class="agent-node-icon" />
                        </div>
                        <div>
                          <el-text> Agent节点 </el-text>
                        </div>
                      </div>
                    </el-dropdown-item>
                    <el-dropdown-item divided @click="addAgentNode('tool')">
                      <div class="agent-node-option">
                        <div class="std-middle-box">
                          <el-image src="/images/node_api.svg" class="agent-node-icon" />
                        </div>
                        <div>
                          <el-text> 工具调用 </el-text>
                        </div>
                      </div>
                    </el-dropdown-item>
                    <el-dropdown-item divided @click="addAgentNode('rag')">
                      <div class="agent-node-option">
                        <div class="std-middle-box">
                          <el-image src="/images/node_rag.svg" class="agent-node-icon" />
                        </div>
                        <div>
                          <el-text> 知识调用 </el-text>
                        </div>
                      </div>
                    </el-dropdown-item>
                    <el-dropdown-item divided @click="addAgentNode('file_reader')">
                      <div class="agent-node-option">
                        <div class="std-middle-box">
                          <el-image src="/images/node_file_reader.svg" class="agent-node-icon" />
                        </div>
                        <div>
                          <el-text> 文件阅读 </el-text>
                        </div>
                      </div>
                    </el-dropdown-item>
                    <el-dropdown-item divided @click="addAgentNode('file_splitter')">
                      <div class="agent-node-option">
                        <div class="std-middle-box">
                          <el-image src="/images/node_file_splitter.svg" class="agent-node-icon" />
                        </div>
                        <div>
                          <el-text> 文本切分 </el-text>
                        </div>
                      </div>
                    </el-dropdown-item>
                    <el-dropdown-item divided @click="addAgentNode('workflow')">
                      <div class="agent-node-option">
                        <div class="std-middle-box">
                          <el-image src="/images/node_flow.svg" class="agent-node-icon" />
                        </div>
                        <div>
                          <el-text> 工作流节点 </el-text>
                        </div>
                      </div>
                    </el-dropdown-item>
                    <el-dropdown-item divided disabled>
                      <div class="agent-node-option">
                        <div class="std-middle-box">
                          <el-image src="/images/node_params.svg" class="agent-node-icon" />
                        </div>
                        <div>
                          <el-text> 变量转换 </el-text>
                        </div>
                      </div>
                    </el-dropdown-item>
                    <el-dropdown-item divided disabled>
                      <div class="agent-node-option">
                        <div class="std-middle-box">
                          <el-image src="/images/node_python.svg" class="agent-node-icon" />
                        </div>
                        <div>
                          <el-text> python执行 </el-text>
                        </div>
                      </div>
                    </el-dropdown-item>
                    <el-dropdown-item divided disabled>
                      <div class="agent-node-option">
                        <div class="std-middle-box">
                          <el-image src="/images/node_app.svg" class="agent-node-icon" />
                        </div>
                        <div>
                          <el-text> 插件调用 </el-text>
                        </div>
                      </div>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            <div id="panel-right">
              <div class="std-middle-box">
                <el-popover ref="alterRef" width="600" :show-after="400">
                  <template #reference>
                    <el-badge :value="workflowAlters?.length" :show-zero="false">
                      <el-icon>
                        <Bell class="panel-icon" :style="{ color: workflowAlters?.length ? 'red' : 'green' }" />
                      </el-icon>
                    </el-badge>
                  </template>
                  <el-scrollbar>
                    <div v-if="workflowAlters?.length" class="alter-list">
                      <el-alert
                        v-for="alter in workflowAlters"
                        :key="alter.id"
                        :title="alter.title"
                        :type="alter.type"
                        show-icon
                        effect="light"
                        :closable="false"
                        style="min-height: 40px"
                      />
                    </div>
                    <div v-else>
                      <el-alert
                        title="工作流配置正常"
                        description="点击试运行按钮，测试工作流是否正常运行"
                        show-icon
                        :closable="false"
                        type="success"
                      />
                    </div>
                  </el-scrollbar>
                </el-popover>
              </div>
              <div class="add-node-button" style="padding: 6px" @click="runWorkflow">
                <div class="std-middle-box">
                  <el-icon size="large" style="color: green">
                    <VideoPlay />
                  </el-icon>
                </div>
                <div class="std-middle-box">
                  <el-text size="large" style="color: green; min-width: 60px"> 试运行 </el-text>
                </div>
              </div>
            </div>
          </div>
        </div>
        <WorkFlowNodeEdit ref="workflowNodeRef" />
        <WorkFlowEdgeEdit />
        <AgentApp
          ref="agentAppRef"
          :app-code="appInfoStore.currentApp.app_code"
          :show="workflowStore.showAgentApp"
          :workflow-code="workflowStore.currentFlow.workflow_code"
        />
        <el-dialog v-model="workflowStore.showDeleteNodeConfirm" title="删除节点" style="max-width: 500px">
          <el-result
            :title="
              workflowStore.selectedNodes?.length > 1 ? `删除${workflowStore.selectedNodes?.length}个节点` : '删除节点'
            "
            :sub-title="
              workflowStore.selectedNodes?.length > 1
                ? '确定要删除这些节点吗？此操作不可恢复'
                : '确定要删除该节点吗？此操作不可恢复'
            "
            icon="warning"
          />
          <template #footer>
            <el-button text type="primary" @click="workflowStore.showDeleteNodeConfirm = false"> 取消 </el-button>
            <el-button type="danger" @click="deleteCurrentNode"> 删除 </el-button>
          </template>
        </el-dialog>
      </el-scrollbar>
    </el-main>
  </el-container>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}
#edit-area {
  width: 100%;
  min-width: calc(100vw - 520px);
  height: 100%;
  min-height: calc(100vh - 160px);
  position: relative;
}
#operation-panel {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  flex-direction: row;
  gap: 24px;
}
#panel-left {
  display: flex;
  flex-direction: row;
  gap: 12px;
  background: white;
  border-radius: 8px;
  padding: 6px;
}
#panel-right {
  display: flex;
  flex-direction: row;
  gap: 12px;
  border-radius: 8px;
  background-color: white;
  padding: 6px;
}
.add-node-button {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: space-between;
  padding: 6px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  background-color: #f0f9ff;
  cursor: pointer;
  &:focus {
    outline: none;
  }
}
.agent-node-icon {
  width: 24px;
  height: 24px;
}
.agent-node-option {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: space-between;
}
.panel-icon {
  width: 20px;
  height: 20px;
  cursor: pointer;
  &:hover {
    color: #409eff;
  }
}
.alter-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 40vh;
}
.lock-area {
  position: fixed;
  z-index: 999;
  width: 100vw;
  height: calc(100vh - 200px);
  top: 120px;
}
</style>
