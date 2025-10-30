<script setup lang="ts">
import { ArrowDown, ArrowRight, MoreFilled, QuestionFilled, VideoPause, VideoPlay } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { ref, nextTick } from 'vue';
import { nodeCopy, nodeDelete, nodeUpdate, workflowSearch, workflowUpdate } from '@/api/app-center-api';
import AgentNodeAttrEdit from '@/components/app-center/app-manage/AgentNodeAttrEdit.vue';
import FileReaderNodeAttrEdit from '@/components/app-center/app-manage/FileReaderNodeAttrEdit.vue';
import FileSplitterNodeAttrEdit from '@/components/app-center/app-manage/FileSplitterNodeAttrEdit.vue';
import JsonSchemaForm from '@/components/app-center/app-manage/JsonSchemaForm.vue';
import RagNodeAttrEdit from '@/components/app-center/app-manage/RagNodeAttrEdit.vue';
import StartNodeAttrEdit from '@/components/app-center/app-manage/StartNodeAttrEdit.vue';
import SubWorkFlowNodeAttrEdit from '@/components/app-center/app-manage/SubWorkFlowNodeAttrEdit.vue';
import TemplateEditor from '@/components/app-center/app-manage/TemplateEditor.vue';
import ToolNodeAttrEdit from '@/components/app-center/app-manage/ToolNodeAttrEdit.vue';

import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';
const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
const isResizing = ref(false);
const startX = ref(0);
const startWidth = ref(0);
const nodeDetailWidth = ref(620);
const nodeDetailRef = ref();
const showInputParamsFlag = ref(false);
const showOutputParamsFlag = ref(false);
const showRunParamsFlag = ref(false);
const nodeNameEdit = ref(false);
const nodeDescEdit = ref(false);
const searchSubWorkflowLoading = ref(false);
const parallelType = ['llm', 'rag'];

const resultMergeOptions = ref([
  { label: '默认', value: 'list' },
  { label: '去重', value: 'set' }
]);
function handleOverNodeDetail(event) {
  const rect = nodeDetailRef.value.getBoundingClientRect();
  const leftBorderWidth = 10; // 左侧边框可触发拖拉的宽度范围
  if (event.clientX >= rect.left && event.clientX <= rect.left + leftBorderWidth) {
    nodeDetailRef.value.style.cursor = 'ew-resize';
  } else {
    nodeDetailRef.value.style.cursor = 'default';
  }
}
const onMouseDown = event => {
  const rect = nodeDetailRef.value.getBoundingClientRect();
  const leftBorderWidth = 10; // 左侧边框可触发拖拉的宽度范围
  if (event.clientX >= rect.left && event.clientX <= rect.left + leftBorderWidth) {
    isResizing.value = true;
    startX.value = event.clientX;
    startWidth.value = nodeDetailWidth.value;
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    nodeDetailRef.value.style.cursor = 'ew-resize';
  }
};
const onMouseMove = event => {
  if (isResizing.value) {
    const deltaX = event.clientX - startX.value;
    nodeDetailWidth.value = startWidth.value - deltaX;
    // 可设置最小宽度限制
    if (nodeDetailWidth.value < 300) {
      nodeDetailWidth.value = 300;
    }
  }
};
const onMouseUp = () => {
  if (isResizing.value) {
    isResizing.value = false;
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
    const rect = nodeDetailRef.value.getBoundingClientRect();
    const leftBorderWidth = 10;
    // @ts-ignore
    const mouseX = event.clientX;
    if (mouseX >= rect.left && mouseX <= rect.left + leftBorderWidth) {
      nodeDetailRef.value.style.cursor = 'ew-resize';
    } else {
      nodeDetailRef.value.style.cursor = 'default';
    }
  }
};
const onMouseLeave = () => {
  nodeDetailRef.value.style.cursor = 'default';
};
async function handleTemplateChange(newValue, src = '') {
  if (src == 'node_result_template') {
    workflowStore.currentNodeDetail.node_result_template = newValue;
    updateNodeOutputConfig();
  } else if (src == 'node_failed_template') {
    workflowStore.currentNodeDetail.node_failed_template = newValue;
    updateNodeRunConfig();
  }
}
async function updateNodeRunConfig() {
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_run_model_config: workflowStore.currentNodeDetail.node_run_model_config,
    node_failed_solution: workflowStore.currentNodeDetail.node_failed_solution,
    node_retry_max: workflowStore.currentNodeDetail.node_retry_max,
    node_retry_duration: workflowStore.currentNodeDetail.node_retry_duration,
    node_retry_model: workflowStore.currentNodeDetail.node_retry_model,
    node_failed_template: workflowStore.currentNodeDetail.node_failed_template,
    node_timeout: workflowStore.currentNodeDetail.node_timeout
  });
}
async function updateNodeOutputConfig() {
  if (workflowStore.currentNodeDetail.node_result_format === 'text') {
    // @ts-ignore
    workflowStore.currentNodeDetail.node_result_params_json_schema.properties = {};
    // @ts-ignore
    workflowStore.currentNodeDetail.node_result_params_json_schema.properties['OUTPUT'] = {
      type: 'string',
      value: '',
      ref: '',
      showSubArea: true
    };
  }
  const res = await nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_result_format: workflowStore.currentNodeDetail.node_result_format,
    node_result_template: workflowStore.currentNodeDetail.node_result_template,
    node_result_params_json_schema: workflowStore.currentNodeDetail.node_result_params_json_schema,
    node_result_extract_separator: workflowStore.currentNodeDetail.node_result_extract_separator,
    node_result_extract_quote: workflowStore.currentNodeDetail.node_result_extract_quote,
    node_result_extract_columns: workflowStore.currentNodeDetail.node_result_extract_columns,
    node_enable_message: workflowStore.currentNodeDetail.node_enable_message,
    node_message_schema_type: workflowStore.currentNodeDetail.node_message_schema_type,
    node_message_schema: workflowStore.currentNodeDetail.node_message_schema
  });
  if (!res.error_status) {
    // 更新工作流节点的输出参数
    const currentNode = workflowStore.graphWrapper.getCellById(workflowStore.currentNodeDetail.node_code);
    currentNode.updateData({
      nodeResultParams: workflowStore.currentNodeDetail.node_result_params_json_schema?.ncOrders
    });
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
async function updateNodeInputConfig() {
  const params = {
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_input_params_json_schema: workflowStore.currentNodeDetail.node_input_params_json_schema
  };
  if (workflowStore.currentNodeDetail.node_type == 'start') {
    // 输出参数从第六个参数移出自定义参数,
    const invalidKeys = [];
    for (let i = 5; i < workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders.length; i++) {
      invalidKeys.push(workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders[i]);
    }
    for (const key of invalidKeys) {
      delete workflowStore.currentNodeDetail.node_result_params_json_schema.properties[key];
      const index = workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders.indexOf(key);
      if (index > -1) {
        workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders.splice(index, 1);
      }
    }
    // merge输入变量到输出参数中
    for (const key of workflowStore.currentNodeDetail.node_input_params_json_schema.ncOrders) {
      workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders.push(key);
      workflowStore.currentNodeDetail.node_result_params_json_schema.properties[key] =
        workflowStore.currentNodeDetail.node_input_params_json_schema.properties[key];
    }
    params['node_result_params_json_schema'] = workflowStore.currentNodeDetail.node_result_params_json_schema;
  }
  const res = await nodeUpdate(params);
  if (!res.error_status) {
    // 更新节点入参
    const currentNode = workflowStore.graphWrapper.getCellById(workflowStore.currentNodeDetail.node_code);
    const nodeParams = workflowStore.currentNodeDetail.node_input_params_json_schema?.ncOrders;

    currentNode.updateData({
      nodeParams: nodeParams
    });
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
async function updateNodeName() {
  nodeNameEdit.value = false;
  const res = await nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_name: workflowStore.currentNodeDetail.node_name
  });
  if (!res.error_status) {
    // 更新工作流节点的名称
    const currentNode = workflowStore.graphWrapper.getCellById(workflowStore.currentNodeDetail.node_code);
    currentNode.updateData({
      nodeName: workflowStore.currentNodeDetail.node_name
    });
    const graphData = workflowStore.graphWrapper.toJSON();
    const jsonData = JSON.stringify(graphData, null, 2);
    workflowUpdate({
      app_code: appInfoStore.currentApp.app_code,
      workflow_code: workflowStore.currentFlow.workflow_code,
      workflow_edit_schema: jsonData
    });
  }
}
async function updateNodeDesc() {
  nodeDescEdit.value = false;
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_desc: workflowStore.currentNodeDetail.node_desc
  });
}
function setNodeMessageSchema(msgSchema: any) {
  if (msgSchema.schema_type == 'customize') {
    msgSchema.schema = {
      type: 'object',
      properties: {},
      ncOrders: []
    };
  } else if (msgSchema.schema_type == 'messageFlow') {
    if (workflowStore.currentNodeDetail.node_type == 'llm') {
      msgSchema.schema = {
        type: 'object',
        properties: {
          content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: {
              nodeCode: workflowStore.currentNodeDetail.node_code,
              nodeDesc: workflowStore.currentNodeDetail.node_desc,
              nodeIcon: workflowStore.currentNodeDetail.node_icon,
              nodeName: workflowStore.currentNodeDetail.node_name,
              nodeType: workflowStore.currentNodeDetail.node_type,
              refAttrName: 'content',
              refAttrPath: workflowStore.currentNodeDetail.node_code + '.content',
              refAttrType: 'string'
            },
            showSubArea: true,
            attrFixed: true,
            description: '输出消息'
            // valueFixed: true
          },
          reasoning_content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: {
              nodeCode: workflowStore.currentNodeDetail.node_code,
              nodeDesc: workflowStore.currentNodeDetail.node_desc,
              nodeIcon: workflowStore.currentNodeDetail.node_icon,
              nodeName: workflowStore.currentNodeDetail.node_name,
              nodeType: workflowStore.currentNodeDetail.node_type,
              refAttrName: 'reasoning_content',
              refAttrPath: workflowStore.currentNodeDetail.node_code + '.reasoning_content',
              refAttrType: 'string'
            },
            showSubArea: true,
            attrFixed: true,
            typeFixed: true,
            description: '推理消息'
            // valueFixed: true
          }
        },
        ncOrders: ['content', 'reasoning_content']
      };
    } else {
      msgSchema.schema = {
        type: 'object',
        properties: {
          content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: '',
            showSubArea: true,
            attrFixed: true,
            typeFixed: true,
            description: '输出消息'
          },
          reasoning_content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: '',
            showSubArea: true,
            attrFixed: true,
            typeFixed: true,
            description: '推理消息'
          }
        },
        ncOrders: ['content', 'reasoning_content']
      };
    }
  } else if (msgSchema.schema_type == 'workflow') {
    msgSchema.schema = {
      type: 'object',
      properties: {
        title: {
          type: 'string',
          typeName: 'string',
          value: '',
          ref: '',
          showSubArea: true,
          attrFixed: true,
          typeFixed: true,
          description: '标题'
        },
        description: {
          type: 'string',
          typeName: 'string',
          value: '',
          ref: '',
          showSubArea: true,
          attrFixed: true,
          typeFixed: true,
          description: '描述'
        }
      },
      ncOrders: ['title', 'description']
    };
  } else if (msgSchema.schema_type == 'null') {
    // 从消息结构中移除
    workflowStore.currentNodeDetail.node_message_schema = workflowStore.currentNodeDetail.node_message_schema.filter(
      item => item.schema_type != 'null'
    );
  } else if (msgSchema.schema_type == 'recommendQ') {
    msgSchema.schema = {
      type: 'object',
      properties: {
        questions: {
          items: {
            type: 'string',
            typeName: 'string',
            description: '推荐问题'
          },
          ref: '',
          showSubArea: false,
          type: 'array',
          typeName: 'array',
          value: '',
          attrFixed: true,
          typeFixed: true,
          description: '推荐问题列表'
        }
      },
      ncOrders: ['questions']
    };
  }
  updateNodeOutputConfig();
}
function initNewMessageSchema() {
  if (workflowStore.currentNodeDetail.node_type == 'llm') {
    workflowStore.currentNodeDetail.node_message_schema.push({
      schema_type: 'messageFlow',
      schema: {
        type: 'object',
        properties: {
          content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: {
              nodeCode: workflowStore.currentNodeDetail.node_code,
              nodeDesc: workflowStore.currentNodeDetail.node_desc,
              nodeIcon: workflowStore.currentNodeDetail.node_icon,
              nodeName: workflowStore.currentNodeDetail.node_name,
              nodeType: workflowStore.currentNodeDetail.node_type,
              refAttrName: 'content',
              refAttrPath: workflowStore.currentNodeDetail.node_code + '.content',
              refAttrType: 'string'
            },
            showSubArea: true,
            attrFixed: true,
            description: '输出消息'
            // valueFixed: true
          },
          reasoning_content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: {
              nodeCode: workflowStore.currentNodeDetail.node_code,
              nodeDesc: workflowStore.currentNodeDetail.node_desc,
              nodeIcon: workflowStore.currentNodeDetail.node_icon,
              nodeName: workflowStore.currentNodeDetail.node_name,
              nodeType: workflowStore.currentNodeDetail.node_type,
              refAttrName: 'reasoning_content',
              refAttrPath: workflowStore.currentNodeDetail.node_code + '.reasoning_content',
              refAttrType: 'string'
            },
            showSubArea: true,
            attrFixed: true,
            typeFixed: true,
            description: '推理消息'
            // valueFixed: true
          }
        },
        ncOrders: ['content', 'reasoning_content']
      }
    });
  } else {
    workflowStore.currentNodeDetail.node_message_schema.push({
      schema_type: 'messageFlow',
      schema: {
        type: 'object',
        properties: {
          content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: '',
            showSubArea: true,
            attrFixed: true,
            description: '输出消息'
          },
          reasoning_content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: '',
            showSubArea: true,
            attrFixed: true,
            typeFixed: true,
            description: '推理消息'
          }
        },
        ncOrders: ['content', 'reasoning_content']
      }
    });
  }
  updateNodeOutputConfig();
}

async function searchSubWorkflow(val: string) {
  searchSubWorkflowLoading.value = true;
  const workflowCodes = [];
  if (workflowStore.currentNodeDetail.node_sub_workflow_config?.target_workflow_code) {
    workflowCodes.push(workflowStore.currentNodeDetail.node_sub_workflow_config.target_workflow_code);
  }
  const res = await workflowSearch({
    app_code: appInfoStore.currentApp.app_code,
    keyword: val,
    workflow_codes: workflowCodes,
    page_size: 10
  });
  if (!res.error_status) {
    workflowStore.currentNodeDetail.subWorkflowOptions = res.result.data;
  }
  searchSubWorkflowLoading.value = false;
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

async function addCopy() {
  // 新增节点副本
  if (!workflowStore.graphWrapper) {
    return;
  }
  const res = await nodeCopy({
    node_code: workflowStore.currentNodeDetail.node_code
  });
  if (!res.error_status) {
    // 重新加载工作流数据
    ElMessage.success('创建副本成功');
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
}

defineExpose({
  searchSubWorkflow
});
</script>

<template>
  <div
    v-show="workflowStore.showNodeFlag"
    id="agent-node-detail-box"
    ref="nodeDetailRef"
    v-loading="workflowStore.loadingNodeInfo"
    element-loading-text="加载中..."
    :style="{ width: nodeDetailWidth + 'px' }"
    @mousemove="handleOverNodeDetail"
    @mousedown="onMouseDown"
    @mouseup="onMouseUp"
    @mouseleave="onMouseLeave"
  >
    <el-scrollbar style="width: 100%">
      <div id="agent-node-detail">
        <div id="node-detail-head">
          <div id="node-detail-head-top">
            <div id="node-detail-head-left">
              <div class="std-middle-box">
                <el-image class="agent-node-icon" :src="workflowStore.currentNodeDetail?.node_icon" />
              </div>
              <div v-show="!nodeNameEdit" class="std-middle-box" @dblclick="nodeNameEdit = true">
                <el-text class="agent-node-name"> {{ workflowStore.currentNodeDetail?.node_name }} </el-text>
              </div>
              <div v-show="nodeNameEdit" class="std-middle-box">
                <el-input v-model="workflowStore.currentNodeDetail.node_name" @blur="updateNodeName()" />
              </div>
            </div>
            <div id="node-detail-head-right">
              <div class="std-middle-box">
                <el-tooltip content="测试运行" effect="light" placement="top">
                  <el-button
                    v-if="workflowStore.currentNodeDetail?.node_status == '运行中'"
                    text
                    :icon="VideoPause"
                    disabled
                  />
                  <el-button v-else text :icon="VideoPlay" disabled />
                </el-tooltip>
              </div>
              <div class="std-middle-box">
                <el-dropdown>
                  <div class="std-middle-box">
                    <el-icon size="small" style="cursor: pointer">
                      <MoreFilled />
                    </el-icon>
                  </div>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item divided @click="addCopy">创建副本</el-dropdown-item>
                      <el-dropdown-item divided @click="deleteCurrentNode">删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>
          <div v-show="!nodeDescEdit" class="std-left-box" style="min-height: 20px" @dblclick="nodeDescEdit = true">
            <el-text> {{ workflowStore.currentNodeDetail?.node_desc }}</el-text>
          </div>
          <div v-show="nodeDescEdit" class="std-left-box">
            <el-input v-model="workflowStore.currentNodeDetail.node_desc" @blur="updateNodeDesc" />
          </div>
        </div>
        <div v-if="!['tool', 'end'].includes(workflowStore.currentNodeDetail?.node_type)" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showInputParamsFlag" class="config-arrow" @click="showInputParamsFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showInputParamsFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 输入参数 </el-text>
            </div>
            <div>
              <el-tooltip
                :content="
                  workflowStore.currentNodeDetail?.node_type == 'start'
                    ? '配置工作流输入变量，请不要与系统变量命名冲突~'
                    : '配置节点输入变量'
                "
                placement="top"
              >
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showInputParamsFlag" class="config-area">
            <el-form :model="workflowStore.currentNodeDetail" label-position="top" style="padding: 12px">
              <el-form-item prop="node_input_params_json_schema">
                <el-row style="width: 100%">
                  <el-col :span="4">
                    <el-text type="info" size="small"> 变量名称 </el-text>
                  </el-col>
                  <el-col :span="4">
                    <el-text type="info" size="small"> 变量描述 </el-text>
                  </el-col>
                  <el-col :span="8">
                    <el-text type="info" size="small"> 变量类型 </el-text>
                  </el-col>
                  <el-col :span="8">
                    <el-text type="info" size="small"> 变量取值 </el-text>
                  </el-col>
                </el-row>
                <JsonSchemaForm
                  :json-schema="workflowStore.currentNodeDetail.node_input_params_json_schema"
                  :value-define="true"
                  :require-define="true"
                  :node-upstream="workflowStore.currentNodeDetail?.node_upstream"
                  @update:schema="updateNodeInputConfig"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <StartNodeAttrEdit />
        <AgentNodeAttrEdit />
        <ToolNodeAttrEdit />
        <RagNodeAttrEdit />
        <FileReaderNodeAttrEdit
          @update-node-input-config="updateNodeInputConfig"
          @update-node-output-config="updateNodeOutputConfig"
        />
        <FileSplitterNodeAttrEdit
          @update-node-input-config="updateNodeInputConfig"
          @update-node-output-config="updateNodeOutputConfig"
        />
        <SubWorkFlowNodeAttrEdit />
        <div class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showOutputParamsFlag" class="config-arrow" @click="showOutputParamsFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showOutputParamsFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 输出设置 </el-text>
            </div>
            <div>
              <el-tooltip content="配置结果的解析格式、配置结果输出至消息流" placement="top">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showOutputParamsFlag" class="config-area">
            <el-form
              :model="workflowStore.currentNodeDetail"
              label-position="top"
              style="padding: 12px"
              require-asterisk-position="right"
            >
              <el-form-item prop="node_result_format" label="数据格式">
                <el-select
                  v-model="workflowStore.currentNodeDetail.node_result_format"
                  :disabled="
                    ['start', 'rag', 'llm', 'file_reader', 'file_splitter', 'workflow', 'end'].includes(
                      workflowStore.currentNodeDetail?.node_type
                    )
                  "
                  @change="updateNodeOutputConfig"
                >
                  <el-option value="text" label="text" />
                  <el-option value="json" label="json" />
                </el-select>
              </el-form-item>
              <el-form-item
                v-show="workflowStore.currentNodeDetail?.node_result_format == 'table'"
                prop="node_result_extract_separator"
                label="分隔符"
              >
                <el-input
                  v-model="workflowStore.currentNodeDetail.node_result_extract_separator"
                  :maxlength="1"
                  @blur="updateNodeOutputConfig"
                />
              </el-form-item>
              <el-form-item
                v-show="workflowStore.currentNodeDetail?.node_result_format == 'table'"
                prop="node_result_extract_quote"
                label="引用符"
              >
                <el-input
                  v-model="workflowStore.currentNodeDetail.node_result_extract_quote"
                  :maxlength="1"
                  @blur="updateNodeOutputConfig"
                />
              </el-form-item>
              <el-form-item
                v-show="workflowStore.currentNodeDetail?.node_result_format == 'table'"
                prop="node_result_extract_columns"
                label="列名"
              >
                <el-select
                  v-model="workflowStore.currentNodeDetail.node_result_extract_columns"
                  multiple
                  allow-create
                  filterable
                  placeholder="请输入列名"
                  @blur="updateNodeOutputConfig"
                />
              </el-form-item>
              <el-form-item
                v-if="workflowStore.currentNodeDetail.node_result_format == 'json'"
                prop="node_result_params_json_schema"
                label="输出变量"
              >
                <el-row style="width: 100%">
                  <el-col :span="8">
                    <el-text type="info" size="small"> 变量名称 </el-text>
                  </el-col>
                  <el-col :span="4">
                    <el-text type="info" size="small"> 变量描述 </el-text>
                  </el-col>
                  <el-col :span="12">
                    <el-text type="info" size="small"> 变量类型 </el-text>
                  </el-col>
                </el-row>
                <JsonSchemaForm
                  :json-schema="workflowStore.currentNodeDetail.node_result_params_json_schema"
                  :value-define="workflowStore.currentNodeDetail.node_type == 'end'"
                  :node-upstream="workflowStore.currentNodeDetail?.node_upstream"
                  :read-only="['start', 'rag', 'file_reader'].includes(workflowStore.currentNodeDetail?.node_type)"
                  @update:schema="updateNodeOutputConfig"
                />
              </el-form-item>
              <el-form-item
                v-else-if="workflowStore.currentNodeDetail.node_result_format == 'text'"
                prop="node_result_params_json_schema"
                label="输出变量"
              >
                <el-row style="width: 100%">
                  <el-col :span="8">
                    <el-text type="info" size="small"> 变量名称 </el-text>
                  </el-col>
                  <el-col :span="4">
                    <el-text type="info" size="small"> 变量描述 </el-text>
                  </el-col>
                  <el-col :span="12">
                    <el-text type="info" size="small"> 变量类型 </el-text>
                  </el-col>
                </el-row>
                <JsonSchemaForm
                  :json-schema="workflowStore.currentNodeDetail.node_result_params_json_schema"
                  :read-only="true"
                />
              </el-form-item>
              <el-form-item
                v-show="!['start'].includes(workflowStore.currentNodeDetail?.node_type)"
                prop="node_enable_message"
                label="输出至消息流（用户可见）"
                label-position="left"
                required
              >
                <el-switch
                  v-model="workflowStore.currentNodeDetail.node_enable_message"
                  @change="updateNodeOutputConfig"
                />
              </el-form-item>
              <div v-show="workflowStore.currentNodeDetail.node_enable_message" class="node-message-list">
                <el-button type="primary" round @click="initNewMessageSchema">新增输出消息</el-button>
                <div v-for="(msgSchema, idx) in workflowStore.currentNodeDetail.node_message_schema" :key="idx">
                  <el-form-item prop="node_message_schema" label="输出消息格式" label-position="left">
                    <el-select v-model="msgSchema.schema_type" @change="setNodeMessageSchema(msgSchema)">
                      <el-option value="messageFlow" label="消息流" />
                      <el-option value="workflow" label="工作流" />
                      <el-option value="recommendQ" label="推荐问题" />
                      <el-option value="echarts" label="数据图表" disabled />
                      <el-option value="customize" label="自定义" />
                      <el-option value="null" label="空" />
                    </el-select>
                  </el-form-item>
                  <el-row style="width: 100%">
                    <el-col :span="4">
                      <el-text type="info" size="small"> 变量名称 </el-text>
                    </el-col>
                    <el-col :span="4">
                      <el-text type="info" size="small"> 变量描述 </el-text>
                    </el-col>
                    <el-col :span="6">
                      <el-text type="info" size="small"> 变量类型 </el-text>
                    </el-col>
                    <el-col :span="6">
                      <el-text type="info" size="small"> 变量取值 </el-text>
                    </el-col>
                  </el-row>
                  <JsonSchemaForm
                    style="margin-top: 40px"
                    :json-schema="msgSchema.schema"
                    :value-define="true"
                    :node-upstream="workflowStore.currentNodeDetail?.node_upstream2"
                    @update:schema="updateNodeOutputConfig"
                  />
                </div>
              </div>
            </el-form>
          </div>
        </div>
        <div class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showRunParamsFlag" class="config-arrow" @click="showRunParamsFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showRunParamsFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 运行设置 </el-text>
            </div>
            <div>
              <el-tooltip content="配置节点运行策略" placement="top">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-if="showRunParamsFlag" class="config-area">
            <el-form :model="workflowStore.currentNodeDetail" label-position="top" style="padding: 12px">
              <el-form-item label="运行方式" prop="node_run_model">
                <el-radio-group
                  v-model="workflowStore.currentNodeDetail.node_run_model_config.node_run_model"
                  @change="updateNodeRunConfig"
                >
                  <el-radio-button value="sync">默认</el-radio-button>
                  <el-radio-button
                    value="parallel"
                    :disabled="!parallelType.includes(workflowStore.currentNodeDetail.node_type)"
                  >
                    并行
                  </el-radio-button>
                  <el-radio-button value="async" disabled>异步</el-radio-button>
                  <el-radio-button value="loop" disabled>循环</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item
                v-show="workflowStore.currentNodeDetail.node_run_model_config.node_run_model == 'parallel'"
                label="并行属性"
                prop="parallel_attr"
              >
                <el-select
                  v-model="workflowStore.currentNodeDetail.node_run_model_config.parallel_attr"
                  @change="updateNodeRunConfig"
                >
                  <el-option
                    v-for="(value, key) in workflowStore.currentNodeDetail.node_input_params_json_schema.properties"
                    :key="key"
                    :value="key"
                    :label="key + ' <' + (value?.type || '') + '>'"
                    :disabled="!value?.type?.includes('array')"
                  />
                </el-select>
              </el-form-item>
              <el-form-item
                v-show="workflowStore.currentNodeDetail.node_run_model_config.node_run_model == 'parallel'"
                label="结果汇总模式"
                prop="result_merge_model"
              >
                <el-segmented
                  v-model="workflowStore.currentNodeDetail.node_run_model_config.result_merge_model"
                  block
                  :options="resultMergeOptions"
                  @change="updateNodeRunConfig"
                />
              </el-form-item>
              <el-form-item label="运行超时（秒）" prop="node_timeout">
                <el-input-number
                  v-model="workflowStore.currentNodeDetail.node_timeout"
                  :min="0"
                  :max="600"
                  @change="updateNodeRunConfig"
                />
              </el-form-item>
              <el-form-item label="失败策略" prop="node_failed_solution">
                <el-radio-group
                  v-model="workflowStore.currentNodeDetail.node_failed_solution"
                  @change="updateNodeRunConfig"
                >
                  <el-radio-button
                    v-show="workflowStore.currentNodeDetail.node_type != 'end'"
                    label="重试"
                    value="retry"
                  />
                  <el-radio-button value="exit">退出</el-radio-button>
                  <el-radio-button value="catch">异常处理</el-radio-button>
                  <el-radio-button value="pass">跳过</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item
                v-show="workflowStore.currentNodeDetail.node_failed_solution == 'retry'"
                label="最大重试次数"
              >
                <el-input-number
                  v-model="workflowStore.currentNodeDetail.node_retry_max"
                  :max="3"
                  :min="0"
                  @change="updateNodeRunConfig"
                />
              </el-form-item>
              <el-form-item
                v-show="workflowStore.currentNodeDetail.node_failed_solution == 'retry'"
                label="重试间隔（毫秒）"
              >
                <el-input-number
                  v-model="workflowStore.currentNodeDetail.node_retry_duration"
                  :min="0"
                  @change="updateNodeRunConfig"
                />
              </el-form-item>
              <el-form-item v-show="workflowStore.currentNodeDetail.node_failed_solution == 'retry'" label="重试后策略">
                <el-radio-group
                  v-model="workflowStore.currentNodeDetail.node_retry_model"
                  @change="updateNodeRunConfig"
                >
                  <el-radio label="退出" :value="1">退出</el-radio>
                  <el-radio label="异常处理" :value="2">异常处理</el-radio>
                  <el-radio label="跳过" :value="3">跳过</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item
                v-show="workflowStore.currentNodeDetail.node_failed_solution == 'catch'"
                label="异常输出结果"
              >
                <TemplateEditor
                  id="node_failed_template"
                  style="width: 100%"
                  :value="workflowStore.currentNodeDetail.node_failed_template"
                  placeholder="请输入异常情况下的默认结果模板,可以通过/ 搜索上游变量，渲染结果将作为输出变量重新进行校验和消息输出"
                  :node="workflowStore.currentNodeDetail"
                  @update:value="newValue => handleTemplateChange(newValue, 'node_failed_template')"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}
.std-left-box {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-direction: row;
  width: 100%;
}
#agent-node-detail-box {
  position: fixed;
  top: 140px;
  right: 20px;
  height: calc(100vh - 200px);
  background: white;
  z-index: 999;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  box-shadow:
    0 4px 8px rgba(0, 0, 0, 0.1),
    0 6px 20px rgba(0, 0, 0, 0.1); /* 阴影效果 */
}
#agent-node-detail {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 6px;
  max-height: calc(100vh - 240px);
}
.agent-node-icon {
  width: 24px;
  height: 24px;
}
#node-detail-head {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: center;
  justify-content: space-between;
  padding: 6px;
  border-bottom: 1px solid #f0f0f0;
}
#node-detail-head-top {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}
#node-detail-head-left {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: center;
}
#node-detail-head-right {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: center;
}
.config-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 6px;
  border-bottom: 1px solid #f0f0f0;
}
.config-head {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: flex-start;
  padding: 6px;
}
.config-arrow {
  cursor: pointer;
  width: 12px;
  height: 12px;
}
.config-area {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.node-message-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
