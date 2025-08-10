<script setup lang="ts">
import {
  ArrowDown,
  ArrowRight,
  MoreFilled,
  QuestionFilled,
  Setting,
  VideoPause,
  VideoPlay,
  Search,
  Close,
  SuccessFilled,
  WarningFilled
} from '@element-plus/icons-vue';
import { nodeUpdate, workflowUpdate, workflowSearch } from '@/api/appCenterApi';
import { type CSSProperties, onMounted, reactive, ref, nextTick } from 'vue';
import JsonSchemaForm from '@/components/appCenter/JsonSchemaForm.vue';
import TemplateEditor from '@/components/appCenter/TemplateEditor.vue';
import { llmInstanceSearch } from '@/api/config_center';
import { LLMInstance } from '@/types/config_center';
import { currentApp } from '@/components/appCenter/ts/app-detail';
import ResourcesSearch from '@/components/appCenter/appPreview/ResourcesSearch.vue';
import {
  CurrentEditFlow,
  currentNodeDetail,
  deleteCurrentNode,
  graphWrapper,
  loadingNodeInfo,
  showNodeFlag
} from '@/components/appCenter/ts/workflow-edit';
import RefSelect from '@/components/appCenter/refSelect.vue';
import { ElMessage } from 'element-plus';
import { getToken } from '@/utils/auth';
const isResizing = ref(false);
const startX = ref(0);
const startWidth = ref(0);
const nodeDetailWidth = ref(560);
const nodeDetailRef = ref();
const showToolConfigFlag = ref(false);
const showLLMConfigFlag = ref(false);
const showPromptConfigFlag = ref(false);
const showMemoryConfigFlag = ref(false);
const showToolsConfigFlag = ref(false);
const showInputParamsFlag = ref(false);
const showOutputParamsFlag = ref(false);
const showRunParamsFlag = ref(false);
const showLLMConfigForm = ref(false);
const nodeNameEdit = ref(false);
const nodeDescEdit = ref(false);
const allLLMInstanceList = ref<LLMInstance[]>([]);
const showRagConfigFlag = ref(false);
const showRagConfigKgFlag = ref(false);
const showRagConfigRerankFlag = ref(false);
const showRagConfigWebFlag = ref(false);
interface IMark {
  style: CSSProperties;
  label: string;
}
// eslint-disable-next-line @typescript-eslint/naming-convention
type Marks = Record<number, IMark | string>;
const temperatureMarks = reactive<Marks>({
  // eslint-disable-next-line @typescript-eslint/naming-convention
  0: '0-精确',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  1: '1-平衡',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  2: '2-创意'
});
const maxTokensMarks = reactive<Marks>({
  // eslint-disable-next-line @typescript-eslint/naming-convention
  1000: '1k',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  10000: '10k',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  32000: '32k',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  64000: '64k',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  128000: '128k'
});
const topPMarks = reactive<Marks>({
  // eslint-disable-next-line @typescript-eslint/naming-convention
  0: '0',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  0.5: '0.5',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  1: '1'
});
const frequencyPenaltyMarks = reactive<Marks>({
  // eslint-disable-next-line @typescript-eslint/naming-convention
  '-2': '-2',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  0: '0',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  1: '1',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  2: '2'
});
const uploadHeader = {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  Authorization: 'Bearer ' + getToken()
};
const resourcesSearchRef = ref();
const resourceSearchDialogShow = ref(false);
const promptTips = `为Agent设定角色与任务
技巧1：如果需要显示参考资料，可以在系统提示词中添加相关说明。如
请于目标段落给出参考文献标识，参考标识为每段参考资料开头给出的编号，请直接使用
如："
        oralce的最新版本<sup>[1]</sup>是13c，
        mysql的最新版本<sup>[2]</sup>是8.0，
注意：引用参考资料的段落需符合引用规范，请不用标记这个问题以外的参考资料。
如果一个段落参考了多个引用资源，请为每一个资源生成一个sup标签，如：
oralce的最新版本<sup>[1]</sup><sup>[2]</sup>是13c。
答案中不要丢失参考资料文本中的那些具有参考价值的格式化元素，比如markdown里面的图片、视频、表格、代码块等元素。"
技巧2：如果打开显示参考资料，系统将会按照变量定义顺序渲染参考文献。
`
const searchSubWorkflowLoading = ref(false);
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
  if (src == 'node_llm_system_prompt_template') {
    currentNodeDetail.value.node_llm_system_prompt_template = newValue;
    updateNodePrompt();
  } else if (src == 'node_llm_user_prompt_template') {
    currentNodeDetail.value.node_llm_user_prompt_template = newValue;
    updateNodePrompt();
  } else if (src == 'node_result_template') {
    currentNodeDetail.value.node_result_template = newValue;
    updateNodeOutputConfig();
  } else if (src == 'node_failed_template') {
    currentNodeDetail.value.node_failed_template = newValue;
    updateNodeRunConfig();
  } else if (src == 'node_rag_query_template') {
    currentNodeDetail.value.node_rag_query_template = newValue;
    updateNodeRagConfig();
  }
}
async function updateNodeRunConfig() {
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_run_model_config: currentNodeDetail.value.node_run_model_config,
    node_failed_solution: currentNodeDetail.value.node_failed_solution,
    node_retry_max: currentNodeDetail.value.node_retry_max,
    node_retry_duration: currentNodeDetail.value.node_retry_duration,
    node_retry_model: currentNodeDetail.value.node_retry_model,
    node_failed_template: currentNodeDetail.value.node_failed_template,
    node_timeout: currentNodeDetail.value.node_timeout
  });
}
async function updateNodeOutputConfig() {
  if (currentNodeDetail.value.node_result_format === 'text') {
    // @ts-ignore
    currentNodeDetail.value.node_result_params_json_schema.properties = {};
    // @ts-ignore
    currentNodeDetail.value.node_result_params_json_schema.properties['OUTPUT'] = {
      type: 'string',
      value: '',
      ref: '',
      showSubArea: true
    };
  }
  const res = await nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_result_format: currentNodeDetail.value.node_result_format,
    node_result_template: currentNodeDetail.value.node_result_template,
    node_result_params_json_schema: currentNodeDetail.value.node_result_params_json_schema,
    node_result_extract_separator: currentNodeDetail.value.node_result_extract_separator,
    node_result_extract_quote: currentNodeDetail.value.node_result_extract_quote,
    node_result_extract_columns: currentNodeDetail.value.node_result_extract_columns,
    node_enable_message: currentNodeDetail.value.node_enable_message,
    node_message_schema_type: currentNodeDetail.value.node_message_schema_type,
    node_message_schema: currentNodeDetail.value.node_message_schema
  });
  if (!res.error_status) {
    // 更新工作流节点的输出参数
    const currentNode = graphWrapper.value.getCellById(currentNodeDetail.value.node_code);
    currentNode.updateData({
      nodeResultParams: currentNodeDetail.value.node_result_params_json_schema?.ncOrders
    });
    const graphData = graphWrapper.value.toJSON();
    if (graphData) {
      workflowUpdate({
        app_code: currentApp.app_code,
        workflow_code: CurrentEditFlow.value.workflow_code,
        workflow_edit_schema: graphData
      });
    }
  }
}
async function switchLLMInstance(targetLLMInstance: LLMInstance) {
  if (!currentNodeDetail.value.node_llm_params) {
    // @ts-ignore
    currentNodeDetail.value.node_llm_params = {};
  }
  currentNodeDetail.value.node_llm_params.llm_name = targetLLMInstance.llm_name;
  currentNodeDetail.value.node_llm_params.llm_icon = targetLLMInstance.llm_icon;
  currentNodeDetail.value.node_llm_params.llm_desc = targetLLMInstance.llm_desc;
  currentNodeDetail.value.node_llm_params.support_vis = targetLLMInstance.support_vis;
  currentNodeDetail.value.node_llm_params.support_file = targetLLMInstance.support_file;
  const res = await nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_llm_code: targetLLMInstance.llm_code,
    node_llm_params: currentNodeDetail.value.node_llm_params
  });
  if (!res.error_status) {
    currentNodeDetail.value.node_llm_code = targetLLMInstance.llm_code;
    // 更新工作流节点的模型字段
    const currentNode = graphWrapper.value.getCellById(currentNodeDetail.value.node_code);
    currentNode.updateData({
      nodeModel: targetLLMInstance.llm_desc
    });
  }
}
async function updateNodePrompt() {
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_llm_system_prompt_template: currentNodeDetail.value.node_llm_system_prompt_template,
    node_llm_user_prompt_template: currentNodeDetail.value.node_llm_user_prompt_template
  });
}
async function updateNodeMemoryConfig() {
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_session_memory_size: currentNodeDetail.value.node_session_memory_size,
    node_deep_memory: currentNodeDetail.value.node_deep_memory
  });
}
async function updateNodeLLMConfig() {
  if (!currentNodeDetail.value.node_llm_params) {
    // @ts-ignore
    currentNodeDetail.value.node_llm_params = {};
  }
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_llm_params: currentNodeDetail.value.node_llm_params
  });
}
async function updateNodeToolConfig() {
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_tool_api_url: currentNodeDetail.value.node_tool_api_url,
    node_tool_http_method: currentNodeDetail.value.node_tool_http_method,
    node_tool_http_header: currentNodeDetail.value.node_tool_http_header,
    node_tool_http_params: currentNodeDetail.value.node_tool_http_params,
    node_tool_http_body: currentNodeDetail.value.node_tool_http_body,
    node_tool_http_body_type: currentNodeDetail.value.node_tool_http_body_type,
  });
}
async function updateNodeInputConfig() {
  const params = {
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_input_params_json_schema: currentNodeDetail.value.node_input_params_json_schema
  }
  if (currentNodeDetail.value.node_type == 'start') {
    // 输出参数从第六个参数移出自定义参数,
    const invalidKeys = [];
    for (let i = 5; i < currentNodeDetail.value.node_result_params_json_schema.ncOrders.length; i++) {
      invalidKeys.push(currentNodeDetail.value.node_result_params_json_schema.ncOrders[i]);

    }
    for (const key of invalidKeys) {
      delete currentNodeDetail.value.node_result_params_json_schema.properties[key];
      const index = currentNodeDetail.value.node_result_params_json_schema.ncOrders.indexOf(key);
      if (index > -1) {
        currentNodeDetail.value.node_result_params_json_schema.ncOrders.splice(index, 1);
      }
    }
    // merge输入变量到输出参数中
    for (const key of currentNodeDetail.value.node_input_params_json_schema.ncOrders) {
      currentNodeDetail.value.node_result_params_json_schema.ncOrders.push(key);
      currentNodeDetail.value.node_result_params_json_schema.properties[
          key] = currentNodeDetail.value.node_input_params_json_schema.properties[key];
    }
    params["node_result_params_json_schema"] = currentNodeDetail.value.node_result_params_json_schema;
  }
  const res = await nodeUpdate(params);
  if (!res.error_status) {
    // 更新节点入参
    const currentNode = graphWrapper.value.getCellById(currentNodeDetail.value.node_code);
    const nodeParams = currentNodeDetail.value.node_input_params_json_schema?.ncOrders

    currentNode.updateData({
      nodeParams: nodeParams
    });
    const graphData = graphWrapper.value.toJSON();
    if (graphData) {
      workflowUpdate({
        app_code: currentApp.app_code,
        workflow_code: CurrentEditFlow.value.workflow_code,
        workflow_edit_schema: graphData
      });
    }
  }
}
async function initAllLLM() {
  const res = await llmInstanceSearch({
    page_size: 100,
  });
  if (!res.error_status) {
    allLLMInstanceList.value = res.result.data;
  }
}
async function handleAvatarUploadSuccess(res: any) {
  if (!res.error_status) {
    currentNodeDetail.value.node_agent_avatar = res.result.node_agent_avatar;
    updateNodePersonConfig();
  }
}
async function updateNodePersonConfig() {
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_agent_nickname: currentNodeDetail.value.node_agent_nickname,
    node_agent_avatar: currentNodeDetail.value.node_agent_avatar,
    node_agent_desc: currentNodeDetail.value.node_agent_desc,
    node_agent_prologue: currentNodeDetail.value.node_agent_prologue,
    node_agent_preset_question: currentNodeDetail.value.node_agent_preset_question,
    node_rag_web_search: currentNodeDetail.value.node_rag_web_search
  });
}
async function updateNodeRagConfig() {
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_rag_resources: currentNodeDetail.value.node_rag_resources,
    node_rag_query_template: currentNodeDetail.value.node_rag_query_template,
    node_rag_recall_config: currentNodeDetail.value.node_rag_recall_config,
    node_rag_rerank_config: currentNodeDetail.value.node_rag_rerank_config,
    node_rag_web_search_config: currentNodeDetail.value.node_rag_web_search_config,
    node_rag_ref_show: currentNodeDetail.value.node_rag_ref_show,
  });
}
async function updateNodeName() {
  nodeNameEdit.value = false;
  const res = await nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_name: currentNodeDetail.value.node_name
  });
  if (!res.error_status) {
    // 更新工作流节点的名称
    const currentNode = graphWrapper.value.getCellById(currentNodeDetail.value.node_code);
    currentNode.updateData({
      nodeName: currentNodeDetail.value.node_name
    });
    const graphData = graphWrapper.value.toJSON();
    const jsonData = JSON.stringify(graphData, null, 2);
    workflowUpdate({
      app_code: currentApp.app_code,
      workflow_code: CurrentEditFlow.value.workflow_code,
      workflow_edit_schema: jsonData
    });
  }
}
async function updateNodeDesc() {
  nodeDescEdit.value = false;
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_desc: currentNodeDetail.value.node_desc
  });
}
async function removeResource(id: string | number) {
  const targetResource = currentNodeDetail.value.node_rag_resources.find(item => item.id === id);
  if (targetResource) {
    currentNodeDetail.value.node_rag_resources = currentNodeDetail.value.node_rag_resources.filter(
        item => item.id !== id
    );
    nodeUpdate({
      app_code: currentApp.app_code,
      node_code: currentNodeDetail.value.node_code,
      node_rag_resources: currentNodeDetail.value.node_rag_resources
    });
  }
}
function setNodeMessageSchema(msgSchema: any) {
  if (msgSchema.schema_type == 'customize') {
    msgSchema.schema = {
      type: 'object',
      properties: {},
      ncOrders: []
    };
  }
  else if (msgSchema.schema_type == 'messageFlow') {
    if (currentNodeDetail.value.node_type == 'llm') {
      msgSchema.schema = {
        type: 'object',
        properties: {
          content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: {
              nodeCode: currentNodeDetail.value.node_code,
              nodeDesc: currentNodeDetail.value.node_desc,
              nodeIcon: currentNodeDetail.value.node_icon,
              nodeName: currentNodeDetail.value.node_name,
              nodeType: currentNodeDetail.value.node_type,
              refAttrName: 'content',
              refAttrPath: currentNodeDetail.value.node_code + '.content',
              refAttrType: 'string'
            },
            showSubArea: true,
            attrFixed: true,
            description: '输出消息',
            // valueFixed: true
          },
          reasoning_content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: {
              nodeCode: currentNodeDetail.value.node_code,
              nodeDesc: currentNodeDetail.value.node_desc,
              nodeIcon: currentNodeDetail.value.node_icon,
              nodeName: currentNodeDetail.value.node_name,
              nodeType: currentNodeDetail.value.node_type,
              refAttrName: 'reasoning_content',
              refAttrPath: currentNodeDetail.value.node_code + '.reasoning_content',
              refAttrType: 'string'
            },
            showSubArea: true,
            attrFixed: true,
            typeFixed: true,
            description: '推理消息',
            // valueFixed: true
          }
        },
        ncOrders: ['content', 'reasoning_content']
      };
    }
    else {
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
            description: '输出消息',
          },
          reasoning_content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: '',
            showSubArea: true,
            attrFixed: true,
            typeFixed: true,
            description: '推理消息',
          }
        },
        ncOrders: ['content', 'reasoning_content']
      };
    }
  }
  else if (msgSchema.schema_type == 'workflow') {
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
          description: '标题',
        },
        description: {
          type: 'string',
          typeName: 'string',
          value: '',
          ref: '',
          showSubArea: true,
          attrFixed: true,
          typeFixed: true,
          description: '描述',
        }
      },
      ncOrders: ['title', 'description']
    };
  }
  else if (msgSchema.schema_type == 'null') {
    // 从消息结构中移除
    currentNodeDetail.value.node_message_schema = currentNodeDetail.value.node_message_schema.filter(
        item => item.schema_type != 'null'
    );
  }
  else if (msgSchema.schema_type == 'recommendQ') {
    msgSchema.schema = {
      type: 'object',
      properties: {
        questions: {
          items: {
            type: 'string',
            typeName: 'string',
            description: '推荐问题',
          },
          ref: '',
          showSubArea: false,
          type: 'array',
          typeName: 'array',
          value: '',
          attrFixed: true,
          typeFixed: true,
          description: '推荐问题列表',
        }
      },
      ncOrders: ['questions']
    };
  }
  updateNodeOutputConfig();
}
function initNewMessageSchema() {
  if (currentNodeDetail.value.node_type == 'llm') {
    currentNodeDetail.value.node_message_schema.push({
      schema_type: 'messageFlow',
      schema:  {
        type: 'object',
        properties: {
          content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: {
              nodeCode: currentNodeDetail.value.node_code,
              nodeDesc: currentNodeDetail.value.node_desc,
              nodeIcon: currentNodeDetail.value.node_icon,
              nodeName: currentNodeDetail.value.node_name,
              nodeType: currentNodeDetail.value.node_type,
              refAttrName: 'content',
              refAttrPath: currentNodeDetail.value.node_code + '.content',
              refAttrType: 'string'
            },
            showSubArea: true,
            attrFixed: true,
            description: '输出消息',
            // valueFixed: true
          },
          reasoning_content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: {
              nodeCode: currentNodeDetail.value.node_code,
              nodeDesc: currentNodeDetail.value.node_desc,
              nodeIcon: currentNodeDetail.value.node_icon,
              nodeName: currentNodeDetail.value.node_name,
              nodeType: currentNodeDetail.value.node_type,
              refAttrName: 'reasoning_content',
              refAttrPath: currentNodeDetail.value.node_code + '.reasoning_content',
              refAttrType: 'string'
            },
            showSubArea: true,
            attrFixed: true,
            typeFixed: true,
            description: '推理消息',
            // valueFixed: true
          }
        },
        ncOrders: ['content', 'reasoning_content']
      }
    })
  }
  else {
    currentNodeDetail.value.node_message_schema.push({
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
            description: '输出消息',
          },
          reasoning_content: {
            type: 'string',
            typeName: 'string',
            value: '',
            ref: '',
            showSubArea: true,
            attrFixed: true,
            typeFixed: true,
            description: '推理消息',
          }
        },
        ncOrders: ['content', 'reasoning_content']
      }
    })
  }
  updateNodeOutputConfig();
}
async function commitAddChooseResources() {
  resourceSearchDialogShow.value = false;
  const pickResources = resourcesSearchRef.value?.getSelectedResources();
  for (const resource of pickResources) {
    if (!currentNodeDetail.value.node_rag_resources) {
      currentNodeDetail.value.node_rag_resources = [];
    }
    const existingResource = currentNodeDetail.value.node_rag_resources.find(item => item.id === resource.id);
    if (!existingResource) {
      currentNodeDetail.value.node_rag_resources.push(resource);
    }
  }
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_rag_resources: currentNodeDetail.value.node_rag_resources
  });
  resourceSearchDialogShow.value = false;
  await nextTick();
}
function fixResourceIcon(url: string) {
  if (!url.includes('images/') && !url.includes('http')) {
    return 'images/' + url;
  }
  return url;
}
async function updateNodeFileReaderConfig() {
  // 修正目标格式为png时的输出格式
  if (['png', 'jpg'].includes(currentNodeDetail.value.node_file_reader_config?.tgt_format)
  && currentNodeDetail.value.node_result_params_json_schema.ncOrders[0] == 'output_resource'
  ) {
    currentNodeDetail.value.node_input_params_json_schema.properties['input_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输入文档列表',
      items: {
        type: 'object',
        typeName: 'file',
        value: '',
        ref: '',
        showSubArea: true,
        attrFixed: true,
        typeFixed: true,
        description: '输入文档',
        properties: fileSchema,
        ncOrders: ['id', 'name', 'size', 'format', 'icon']
      }
    };
    delete currentNodeDetail.value.node_input_params_json_schema.properties['input_resource'];
    currentNodeDetail.value.node_input_params_json_schema.ncOrders[0] = 'input_resources';

    currentNodeDetail.value.node_result_params_json_schema.properties['output_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输出文档内容',
      items: {
        ncOrders: [
          "id",
          "name",
          "format",
          "size",
          "content",
          "url"
        ],
        properties: {
          content: {
            description: "文件内容",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          },
          "format": {
            "description": "文件名称",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          },
          "id": {
            "description": "文件ID",
            "ref": "",
            "showSubArea": false,
            "type": "integer",
            "typeName": "integer",
            "value": ""
          },
          "name": {
            "description": "文件名称",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          },
          "size": {
            "description": "文件大小",
            "ref": "",
            "showSubArea": false,
            "type": "number",
            "typeName": "number",
            "value": ""
          },
          "url": {
            "description": "文件URL",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          }
        },
        required: [],
        type: "object",
        typeName: "file"
      }
    };
    delete currentNodeDetail.value.node_result_params_json_schema.properties['output_resource'];
    currentNodeDetail.value.node_result_params_json_schema.ncOrders[0] = 'output_resources';
  }

  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_file_reader_config: currentNodeDetail.value.node_file_reader_config
  });
}
async function updateNodeFileSplitterConfig() {
  nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_file_splitter_config: currentNodeDetail.value.node_file_splitter_config
  });
}
async function handleFileReaderModeChange(val:string) {
  // 将input_resources 入参进行处理
  const fileSchema = {
    id: {
      type: 'integer',
      typeName: 'integer',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      valueFixed: true,
      description: '资源ID'
    },
    name: {
      type: 'string',
      typeName: 'string',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      valueFixed: true,
      description: '资源名称'
    },
    size: {
      type: 'number',
      typeName: 'number',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      valueFixed: true,
      description: '资源大小'
    },
    format : {
      type: 'string',
      typeName: 'string',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      valueFixed: true,
      description: '资源格式'
    },
    icon : {
      type: 'string',
      typeName: 'string',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      valueFixed: true,
      description: '资源图标',
      valueFixed: true
    }
  }
  if (val == 'single') {
    currentNodeDetail.value.node_input_params_json_schema.properties['input_resource'] = {
      type: 'object',
      typeName: 'file',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输入文档',
      properties: fileSchema,
      ncOrders: ['id', 'name', 'size', 'format', 'icon']
    };
    delete currentNodeDetail.value.node_input_params_json_schema.properties['input_resources'];
    currentNodeDetail.value.node_input_params_json_schema.ncOrders[0] = 'input_resource';

    currentNodeDetail.value.node_result_params_json_schema.properties['output_resource'] = {
      ncOrders: [
        "id",
        "name",
        "format",
        "size",
        "content",
        "url"
      ],
      properties: {
        content: {
          description: "文件内容",
          ref: "",
          showSubArea: false,
          type: "string",
          typeName: "string",
          value: ""
        },
        format: {
          "description": "文件名称",
          "ref": "",
          "showSubArea": false,
          "type": "string",
          "typeName": "string",
          "value": ""
        },
        id: {
          "description": "文件ID",
          "ref": "",
          "showSubArea": false,
          "type": "integer",
          "typeName": "integer",
          "value": ""
        },
        name: {
          "description": "文件名称",
          "ref": "",
          "showSubArea": false,
          "type": "string",
          "typeName": "string",
          "value": ""
        },
        size: {
          "description": "文件大小",
          "ref": "",
          "showSubArea": false,
          "type": "number",
          "typeName": "number",
          "value": ""
        },
        url: {
          "description": "文件URL",
          "ref": "",
          "showSubArea": false,
          "type": "string",
          "typeName": "string",
          "value": ""
        }
      },
      required: [],
      type: "object",
      typeName: "file"
    };
    delete currentNodeDetail.value.node_result_params_json_schema.properties['output_resources'];
    currentNodeDetail.value.node_result_params_json_schema.ncOrders[0] = 'output_resource';
  }
  else if (val == 'list') {
    currentNodeDetail.value.node_input_params_json_schema.properties['input_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输入文档列表',
      items: {
        type: 'object',
        typeName: 'file',
        value: '',
        ref: '',
        showSubArea: true,
        attrFixed: true,
        typeFixed: true,
        description: '输入文档',
        properties: fileSchema,
        ncOrders: ['id', 'name', 'size', 'format', 'icon']
      }
    };
    delete currentNodeDetail.value.node_input_params_json_schema.properties['input_resource'];
    currentNodeDetail.value.node_input_params_json_schema.ncOrders[0] = 'input_resources';

    currentNodeDetail.value.node_result_params_json_schema.properties['output_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输出文档内容',
      items: {
        ncOrders: [
          "id",
          "name",
          "format",
          "size",
          "content",
          "url"
        ],
        properties: {
          content: {
            description: "文件内容",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          },
          "format": {
            "description": "文件名称",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          },
          "id": {
            "description": "文件ID",
            "ref": "",
            "showSubArea": false,
            "type": "integer",
            "typeName": "integer",
            "value": ""
          },
          "name": {
            "description": "文件名称",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          },
          "size": {
            "description": "文件大小",
            "ref": "",
            "showSubArea": false,
            "type": "number",
            "typeName": "number",
            "value": ""
          },
          "url": {
            "description": "文件URL",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          }
        },
        required: [],
        type: "object",
        typeName: "file"
      }
    };
    delete currentNodeDetail.value.node_result_params_json_schema.properties['output_resource'];
    currentNodeDetail.value.node_result_params_json_schema.ncOrders[0] = 'output_resources';
  }
  updateNodeInputConfig();
  updateNodeOutputConfig();
  updateNodeFileReaderConfig();
}
async function handleFileReaderTargetFormatChange(val:string) {
  if (['png', 'jpg'].includes(val) && currentNodeDetail.value.node_file_reader_config?.src_format == 'pdf'
      &&  currentNodeDetail.value.node_file_reader_config?.engine == 'PyMuPDF') {
    currentNodeDetail.value.node_result_params_json_schema.properties['output_resources'] = {
      type: 'array',
      typeName: 'file-list',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '输出文档内容',
      items: {
        ncOrders: [
          "id",
          "name",
          "format",
          "size",
          "content",
          "url"
        ],
        properties: {
          content: {
            description: "文件内容",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          },
          "format": {
            "description": "文件名称",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          },
          "id": {
            "description": "文件ID",
            "ref": "",
            "showSubArea": false,
            "type": "integer",
            "typeName": "integer",
            "value": ""
          },
          "name": {
            "description": "文件名称",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          },
          "size": {
            "description": "文件大小",
            "ref": "",
            "showSubArea": false,
            "type": "number",
            "typeName": "number",
            "value": ""
          },
          "url": {
            "description": "文件URL",
            "ref": "",
            "showSubArea": false,
            "type": "string",
            "typeName": "string",
            "value": ""
          }
        },
        required: [],
        type: "object",
        typeName: "file"
      }
    };
    delete currentNodeDetail.value.node_result_params_json_schema.properties['output_resource'];
    currentNodeDetail.value.node_result_params_json_schema.ncOrders[0] = 'output_resources';
  }
  updateNodeOutputConfig();
  updateNodeFileReaderConfig()
}
async function searchSubWorkflow(val:string) {
  searchSubWorkflowLoading.value = true;
  const workflow_codes = []
  if (currentNodeDetail.value.node_sub_workflow_config?.target_workflow_code) {
    workflow_codes.push(currentNodeDetail.value.node_sub_workflow_config.target_workflow_code);
  }
  const res = await workflowSearch({
    app_code: currentApp.app_code,
    keyword: val,
    workflow_codes: workflow_codes,
    page_size: 10
  });
  if (!res.error_status) {
    currentNodeDetail.value.subWorkflowOptions = res.result.data;
  }
  searchSubWorkflowLoading.value = false;
}
async function updateNodeSubWorkflowConfig() {
  const pickSubWorkflow = currentNodeDetail.value.subWorkflowOptions.find(
    item => item.workflow_code == currentNodeDetail.value.node_sub_workflow_config.target_workflow_code
  );

  currentNodeDetail.value.node_input_params_json_schema = pickSubWorkflow.workflow_params_schema;
  currentNodeDetail.value.node_result_params_json_schema = pickSubWorkflow.workflow_result_schema;
  currentNodeDetail.value.node_input_params_json_schema.attrFixed = true;
  currentNodeDetail.value.node_result_params_json_schema.attrFixed = true;
  for (let k of currentNodeDetail.value.node_input_params_json_schema.ncOrders) {
    if (currentNodeDetail.value.node_input_params_json_schema.properties[k]) {
      currentNodeDetail.value.node_input_params_json_schema.properties[k].attrFixed = true;
      currentNodeDetail.value.node_input_params_json_schema.properties[k].typeFixed = true;
    }
  }
  for (let k of currentNodeDetail.value.node_result_params_json_schema.ncOrders) {
    if (currentNodeDetail.value.node_result_params_json_schema.properties[k]) {
      currentNodeDetail.value.node_result_params_json_schema.properties[k].attrFixed = true;
      currentNodeDetail.value.node_result_params_json_schema.properties[k].typeFixed = true;
    }
  }
  const res = await nodeUpdate({
    app_code: currentApp.app_code,
    node_code: currentNodeDetail.value.node_code,
    node_sub_workflow_config: currentNodeDetail.value.node_sub_workflow_config,
    node_input_params_json_schema: currentNodeDetail.value.node_input_params_json_schema,
    node_result_params_json_schema: currentNodeDetail.value.node_result_params_json_schema
  });
  if (!res.error_status) {
    currentNodeDetail.value.node_sub_workflow_config.target_workflow_name = pickSubWorkflow.workflow_name;
    // 更新工作流节点的名称
    const currentNode = graphWrapper.value.getCellById(currentNodeDetail.value.node_code);
    currentNode.updateData({
      nodeParams:  currentNodeDetail.value.node_input_params_json_schema?.ncOrders,
      nodeResultParams: currentNodeDetail.value.node_result_params_json_schema?.ncOrders
    });
    const graphData = graphWrapper.value.toJSON();
    workflowUpdate({
      app_code: currentApp.app_code,
      workflow_code: CurrentEditFlow.value.workflow_code,
      workflow_edit_schema: graphData
    });
  }
}
function getSubWorkflowInfo(val: string) {
  return currentNodeDetail.value.subWorkflowOptions?.find(
    item => item.workflow_code == val
  );
}
onMounted(async () => {
  initAllLLM();
});
defineExpose(
  {
    searchSubWorkflow,
  }
)
</script>

<template>
  <div
      v-show="showNodeFlag"
      id="agent-node-detail-box"
      ref="nodeDetailRef"
      v-loading="loadingNodeInfo"
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
                <el-image class="agent-node-icon" :src="currentNodeDetail?.node_icon" />
              </div>
              <div v-show="!nodeNameEdit" class="std-middle-box" @dblclick="nodeNameEdit = true">
                <el-text class="agent-node-name"> {{ currentNodeDetail?.node_name }} </el-text>
              </div>
              <div v-show="nodeNameEdit" class="std-middle-box">
                <el-input v-model="currentNodeDetail.node_name" @blur="updateNodeName()" />
              </div>
            </div>
            <div id="node-detail-head-right">
              <div class="std-middle-box">
                <el-tooltip content="测试运行" effect="light" placement="top">
                  <el-button v-if="currentNodeDetail?.node_status == '运行中'" text :icon="VideoPause" disabled />
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
                      <el-dropdown-item divided disabled>创建副本</el-dropdown-item>
                      <el-dropdown-item divided @click="deleteCurrentNode">删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>
          <div v-show="!nodeDescEdit" class="std-left-box" style="min-height: 20px" @dblclick="nodeDescEdit = true">
            <el-text> {{ currentNodeDetail?.node_desc }}</el-text>
          </div>
          <div v-show="nodeDescEdit" class="std-left-box">
            <el-input v-model="currentNodeDetail.node_desc" @blur="updateNodeDesc" />
          </div>
        </div>
        <div v-if="!['tool', 'end'].includes(currentNodeDetail?.node_type)" class="config-item">
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
              <el-tooltip :content="currentNodeDetail?.node_type == 'start' ? '配置工作流输入变量，请不要与系统变量命名冲突~' :'配置节点输入变量'">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showInputParamsFlag" class="config-area">
            <el-form :model="currentNodeDetail" label-position="top" style="padding: 12px">
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
                    :jsonSchema="currentNodeDetail.node_input_params_json_schema"
                    :value-define="true"
                    :require-define="true"
                    :node-upstream="currentNodeDetail?.node_upstream"
                    @update:schema="updateNodeInputConfig"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'llm'" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showPromptConfigFlag" class="config-arrow" @click="showPromptConfigFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showPromptConfigFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 提示词 </el-text>
            </div>
            <div>
              <el-tooltip>
                <template #content>
                  <div style="max-width: 600px">
                    {{promptTips}}
                  </div>
                </template>
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showPromptConfigFlag" class="config-area">
            <el-form :model="currentNodeDetail" label-position="top" style="padding: 12px">
              <el-form-item prop="node_llm_system_prompt_template" label="系统提示词">
                <TemplateEditor
                    id="node_llm_system_prompt_template"
                    :value="currentNodeDetail.node_llm_system_prompt_template"
                    style="width: 100%"
                    placeholder="请输入系统提示词，如：你是一个AI助手。可以通过/ 唤出上游变量列表"
                    :node="currentNodeDetail"
                    @update:value="newValue => handleTemplateChange(newValue, 'node_llm_system_prompt_template')"
                />
              </el-form-item>
              <el-form-item prop="node_llm_user_prompt_template" label="用户提示词">
                <TemplateEditor
                    id="node_llm_user_prompt_template"
                    :value="currentNodeDetail.node_llm_user_prompt_template"
                    style="width: 100%"
                    placeholder="请输入用户提示词，如：请问天气如何。可以通过/ 唤出上游变量列表"
                    :node="currentNodeDetail"
                    @update:value="newValue => handleTemplateChange(newValue, 'node_llm_user_prompt_template')"
                />
              </el-form-item>
              <el-form-item label="显示参考资料" style="padding: 0 12px">
                <el-switch
                    v-model="currentNodeDetail.node_rag_ref_show"
                    active-text="提供"
                    inactive-text="隐藏"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'llm'" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showLLMConfigFlag" class="config-arrow" @click="showLLMConfigFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showLLMConfigFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 基础模型 </el-text>
            </div>
            <div>
              <el-tooltip content="选择一个合适的基础模型来完成问答，可前往模型管理页面新增模型">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showLLMConfigFlag" class="config-area">
            <div class="std-left-box">
              <div class="std-middle-box" style="width: 100%">
                <el-popover trigger="click" width="320">
                  <template #reference>
                    <el-input v-model="currentNodeDetail.node_llm_params.llm_desc" readonly style="cursor: pointer">
                      <template #prefix>
                        <el-image
                            v-if="currentNodeDetail.node_llm_params.llm_icon"
                            :src="currentNodeDetail.node_llm_params.llm_icon"
                            class="config-llm-icon"
                        />
                      </template>
                      <template #suffix>
                        <el-icon class="config-llm-icon">
                          <ArrowDown />
                        </el-icon>
                      </template>
                    </el-input>
                  </template>
                  <el-scrollbar>
                    <div class="llm-instance-area">
                      <div
                          v-for="(item, idx) in allLLMInstanceList"
                          :key="idx"
                          class="llm-instance-item"
                          :class="{ 'llm-instance-item-active': item.llm_code == currentNodeDetail?.node_llm_code }"
                          @click="switchLLMInstance(item)"
                      >
                        <div class="std-middle-box">
                          <el-avatar
                              :src="item.llm_icon"
                              style="width: 20px; height: 20px; background-color: white"
                              fit="contain"
                          />
                        </div>
                        <div class="std-middle-box" style="justify-content: flex-start">
                          <el-text
                              truncated
                              style="font-size: 14px; font-weight: 500; line-height: 20px; color: #344054"
                          >
                            {{ item.llm_desc }}
                          </el-text>
                        </div>
                      </div>
                    </div>
                  </el-scrollbar>
                </el-popover>
              </div>
              <div class="std-middle-box">
                <el-icon class="config-item" style="cursor: pointer" @click="showLLMConfigForm = true">
                  <Setting />
                </el-icon>
              </div>
            </div>
            <div class="std-left-box">
              <el-form style="width: 100%">
                <el-form-item prop="stream" label="流式输出">
                  <el-switch v-model="currentNodeDetail.node_llm_params.stream" @change="updateNodeLLMConfig" />
                </el-form-item>
                <el-form-item v-show="currentNodeDetail.node_llm_params.support_vis" label="视觉能力">
                  <el-switch v-model="currentNodeDetail.node_llm_params.enable_visual" @change="updateNodeLLMConfig" />
                </el-form-item>
                <el-form-item
                    v-show="
                    currentNodeDetail.node_llm_params.support_vis && currentNodeDetail.node_llm_params?.enable_visual
                  "
                    label="图片输入"
                    label-position="top"
                >
                  <JsonSchemaForm
                      style="margin-left: 24px"
                      :jsonSchema="currentNodeDetail.node_llm_params.visual_schema"
                      :value-define="true"
                      :node-upstream="currentNodeDetail?.nodeSelf"
                      :is-parent="false"
                      @update:schema="updateNodeLLMConfig"
                  />
                </el-form-item>
                <el-form-item v-show="currentNodeDetail.node_llm_params.support_file" label="文件阅读能力">
                  <el-switch v-model="currentNodeDetail.node_llm_params.enable_file" @change="updateNodeLLMConfig" />
                </el-form-item>
                <el-form-item
                    v-show="
                    currentNodeDetail.node_llm_params.support_file &&
                    currentNodeDetail.node_llm_params?.enable_file
                  "
                    label="文件输入"
                >
                  <RefSelect
                      :up-stream-nodes="currentNodeDetail.node_upstream"
                      :ref-value="currentNodeDetail.node_llm_params.file_ref"
                      style="width: 100%"
                      @update:ref="
                      result => {
                        currentNodeDetail.node_llm_params.file_ref = result;
                        updateNodeLLMConfig();
                      }
                    "
                  />
                </el-form-item>
                <el-form-item prop="response_format" label="输出格式">
                  <el-select v-model="currentNodeDetail.node_llm_params.response_format" @change="updateNodeLLMConfig">
                    <el-option value="text" label="text" />
                    <el-option value="json" label="json" />
                  </el-select>
                </el-form-item>
                <el-form-item prop="stop" label="停止词">
                  <el-select
                      v-model="currentNodeDetail.node_llm_params.stop"
                      multiple
                      clearable
                      allow-create
                      filterable
                      default-first-option
                      :multiple-limit="8"
                      placeholder="请输入停止词"
                      @change="updateNodeLLMConfig"
                  />
                </el-form-item>
              </el-form>
            </div>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'llm'" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showMemoryConfigFlag" class="config-arrow" @click="showMemoryConfigFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showMemoryConfigFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 记忆 </el-text>
            </div>
            <div>
              <el-tooltip content="为Agent配置合适的记忆模式和专业知识，来增强理解与问答能力">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showMemoryConfigFlag" class="config-area">
            <el-form :model="currentNodeDetail" label-position="top" style="padding: 12px">
              <el-form-item prop="node_session_memory_size" label="会话记忆长度">
                <el-input-number
                    v-model="currentNodeDetail.node_session_memory_size"
                    :min="0"
                    @change="updateNodeMemoryConfig"
                />
              </el-form-item>
              <el-form-item prop="node_session_memory_size" label="深度记忆">
                <el-switch v-model="currentNodeDetail.node_deep_memory" @change="updateNodeMemoryConfig" />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="false" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showToolsConfigFlag" class="config-arrow" @click="showToolsConfigFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showToolsConfigFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 工具 </el-text>
            </div>
            <div>
              <el-tooltip content="为Agent配置合适的工具，来扩展能力边界">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showToolsConfigFlag" class="config-area"></div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'tool'" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showToolConfigFlag" class="config-arrow" @click="showToolConfigFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showToolConfigFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> API设置 </el-text>
            </div>
            <div>
              <el-tooltip content="工具调用方式的配置信息">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showToolConfigFlag" class="config-area">
            <el-form :model="currentNodeDetail" label-position="top">
              <el-form-item prop="node_tool_api_url" label="URL" style="padding: 0 12px">
                <el-input
                    v-model="currentNodeDetail.node_tool_api_url"
                    placeholder="请输入API地址"
                    @blur="updateNodeToolConfig"
                />
              </el-form-item>
              <el-form-item prop="node_tool_http_method" label="Method" style="padding: 0 12px">
                <el-select
                    v-model="currentNodeDetail.node_tool_http_method"
                    placeholder="请选择请求方法类型"
                    @change="updateNodeToolConfig"
                >
                  <el-option value="GET" label="GET" />
                  <el-option value="POST" label="POST" />
                  <el-option value="PUT" label="PUT" />
                  <el-option value="DELETE" label="DELETE" />
                  <el-option value="PATCH" label="PATCH" />
                  <el-option value="HEAD" label="HEAD" />
                  <el-option value="OPTIONS" label="OPTIONS" />
                </el-select>
              </el-form-item>
              <el-form-item prop="node_tool_http_header" label="Header" style="padding: 0 12px">
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
                    :jsonSchema="currentNodeDetail.node_tool_http_header"
                    :value-define="true"
                    :node-upstream="currentNodeDetail?.node_upstream"
                    @update:schema="updateNodeToolConfig"
                />
              </el-form-item>
              <el-form-item prop="node_tool_http_params" label="Query" style="padding: 0 12px">
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
                    :jsonSchema="currentNodeDetail.node_tool_http_params"
                    :value-define="true"
                    :node-upstream="currentNodeDetail?.node_upstream"
                    @update:schema="updateNodeToolConfig"
                />
              </el-form-item>
              <el-form-item prop="node_tool_http_body" label="Body" style="padding: 0 12px">
                <el-row style="width: 100%">
                  <el-radio-group v-model="currentNodeDetail.node_tool_http_body_type" @change="updateNodeToolConfig">
                    <el-radio value="json" >json</el-radio>
                    <el-radio value="form-data" >form-data</el-radio>
                  </el-radio-group>
                </el-row>
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
                    :jsonSchema="currentNodeDetail.node_tool_http_body"
                    :value-define="true"
                    :node-upstream="currentNodeDetail?.node_upstream"
                    @update:schema="updateNodeToolConfig"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'rag'" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showRagConfigKgFlag" class="config-arrow" @click="showRagConfigKgFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showRagConfigKgFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 知识库选择 </el-text>
            </div>
            <div>
              <el-tooltip content="配置知识来源">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showRagConfigKgFlag" class="config-area">

            <div>
              <el-form label-position="top">
                <el-form-item label="查询语句" style="padding: 0 12px">
                  <TemplateEditor
                      id="node_rag_query_template"
                      :value="currentNodeDetail.node_rag_query_template"
                      style="width: 100%"
                      placeholder="请输入需要查询知识的语句，如选择系统变量USER_INPUT"
                      :node="currentNodeDetail"
                      @update:value="newValue => handleTemplateChange(newValue, 'node_rag_query_template')"
                  />
                </el-form-item>
                <el-form-item label="召回知识库" style="padding: 0 12px">
                  <div class="rag-area">
                    <div class="rag-title">
                      <el-button :icon="Search" round @click="resourceSearchDialogShow = true" style="width: 100%">
                        搜索知识库
                      </el-button>
                    </div>
                    <div class="rag-body">
                      <div v-for="item in currentNodeDetail?.node_rag_resources" :key="item.id" class="resource-item">
                        <div class="resource-item-left">
                          <div class="resource-status">
                            <el-icon style="color: green">
                              <SuccessFilled />
                            </el-icon>
                          </div>
                          <div class="resource-icon">
                            <el-image :src="fixResourceIcon(item?.resource_icon)" />
                          </div>
                          <div class="resource-title">
                            <el-text truncated>
                              {{ item?.resource_name }}
                            </el-text>
                          </div>
                        </div>
                        <div class="resource-remove">
                          <el-button :icon="Close" round @click="removeResource(item?.id)" />
                        </div>
                      </div>
                    </div>
                  </div>
                </el-form-item>

              </el-form>

            </div>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'rag'" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showRagConfigFlag" class="config-arrow" @click="showRagConfigFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showRagConfigFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 召回设置 </el-text>
            </div>
            <div>
              <el-tooltip content="调用向量模型匹配最佳参考知识">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showRagConfigFlag" class="config-area">
            <el-form :model="currentNodeDetail" label-position="top">
              <el-form-item label="相似度度量方法" style="padding: 0 12px">
                <el-select
                    v-model="currentNodeDetail.node_rag_recall_config.recall_similarity"
                    @change="updateNodeRagConfig">
                  <el-option value="ip" label="最大内积" />
                  <el-option value="cosine" label="余弦相似度" />
                </el-select>
              </el-form-item>
              <el-form-item label="召回阈值" style="padding: 0 12px">
                <el-slider
                    v-model="currentNodeDetail.node_rag_recall_config.recall_threshold"
                    show-input
                    :show-input-controls="false"
                    :min="0"
                    :max="1"
                    :step="0.01"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
              <el-form-item label="最大召回数" style="padding: 0 12px">
                <el-input-number
                    v-model="currentNodeDetail.node_rag_recall_config.recall_k"
                    :min="1"
                    :max="500"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'rag'" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showRagConfigRerankFlag" class="config-arrow" @click="showRagConfigRerankFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showRagConfigRerankFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text> 重排序设置 </el-text>
            </div>
            <div>
              <el-tooltip content="调用重排序模型对召回结果进行精排序">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showRagConfigRerankFlag" class="config-area">
            <el-form :model="currentNodeDetail" label-position="top">
              <el-form-item label="启用重排序" style="padding: 0 12px">
                <el-switch
                    v-model="currentNodeDetail.node_rag_rerank_config.rerank_enabled"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
              <el-form-item label="文档中生成的最大块数" style="padding: 0 12px">
                <el-input-number
                    v-model="currentNodeDetail.node_rag_rerank_config.max_chunk_per_doc"
                    :disabled="!currentNodeDetail.node_rag_rerank_config.rerank_enabled"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
              <el-form-item label="标记重叠数量" style="padding: 0 12px">
                <el-input-number
                    v-model="currentNodeDetail.node_rag_rerank_config.overlap_tokens"
                    :min="1"
                    :max="80"
                    :disabled="!currentNodeDetail.node_rag_rerank_config.rerank_enabled"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
              <el-form-item label="召回阈值" style="padding: 0 12px">
                <el-slider
                    v-model="currentNodeDetail.node_rag_rerank_config.rerank_threshold"
                    :disabled="!currentNodeDetail.node_rag_rerank_config.rerank_enabled"
                    show-input
                    :show-input-controls="false"
                    :min="0"
                    :max="1"
                    :step="0.01"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
              <el-form-item label="最大召回数" style="padding: 0 12px">
                <el-input-number
                    v-model="currentNodeDetail.node_rag_rerank_config.rerank_k"
                    :disabled="!currentNodeDetail.node_rag_rerank_config.rerank_enabled"
                    :min="1"
                    :max="500"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'rag'" class="config-item">
          <div class="config-head">
            <div class="std-middle-box">
              <el-icon v-if="showRagConfigWebFlag" class="config-arrow" @click="showRagConfigWebFlag = false">
                <ArrowDown />
              </el-icon>
              <el-icon v-else class="config-arrow" @click="showRagConfigWebFlag = true">
                <ArrowRight />
              </el-icon>
            </div>
            <div class="std-middle-box">
              <el-text class="config-head-text"> 联网搜索设置 </el-text>
            </div>
            <div>
              <el-tooltip content="调用搜索引擎补充实时网页数据">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showRagConfigWebFlag" class="config-area">
            <el-form :model="currentNodeDetail" label-position="top">
              <el-form-item label="启用联网搜索" style="padding: 0 12px">
                <el-switch
                    v-model="currentNodeDetail.node_rag_web_search_config.search_engine_enhanced"
                    @change="updateNodeRagConfig" />
              </el-form-item>
              <el-form-item label="最大返回网页数" style="padding: 0 12px">
                <el-input-number
                    v-model="currentNodeDetail.node_rag_web_search_config.num"
                    :disabled="!currentNodeDetail.node_rag_web_search_config.search_engine_enhanced"
                    :min="1"
                    :max="50"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
              <el-form-item label="最大超时" style="padding: 0 12px">
                <el-slider
                    v-model="currentNodeDetail.node_rag_web_search_config.timeout"
                    :disabled="!currentNodeDetail.node_rag_web_search_config.search_engine_enhanced"
                    :min="1"
                    :max="60"
                    show-input
                    :show-input-controls="false"
                    :step="1"
                    @change="updateNodeRagConfig"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'file_reader'" class="config-item">
          <div class="config-area">
            <el-form :model="currentNodeDetail" label-position="top">
              <el-form-item prop="mode" label="模式" style="padding: 0 12px">
                <el-radio-group
                    v-model="currentNodeDetail.node_file_reader_config.mode"
                    @change="handleFileReaderModeChange"
                >
                  <el-radio value="single">单文件</el-radio>
                  <el-radio value="list">文件列表</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item prop="src_format" label="来源格式" style="padding: 0 12px">
                <el-select
                  v-model="currentNodeDetail.node_file_reader_config.src_format"
                  filterable
                  allow-create
                  placeholder="请选择或输入来源格式"
                  @change="updateNodeFileReaderConfig"
                >
                  <el-option value="pdf" label="pdf" />
                  <el-option value="docx" label="docx" />
                  <el-option value="doc" label="doc" />
                  <el-option value="pptx" label="pptx" />
                  <el-option value="xlsx" label="xlsx" />
                  <el-option value="xls" label="xls" />
                  <el-option value="未知" label="未知" />
                </el-select>
              </el-form-item>
              <el-form-item prop="tat_format" label="目标格式" style="padding: 0 12px">
                <el-select
                    v-model="currentNodeDetail.node_file_reader_config.tgt_format"
                    filterable
                    allow-create
                    placeholder="请选择或输入目标格式"
                    @change="handleFileReaderTargetFormatChange"
                >
                  <el-option value="pdf" label="pdf" />
                  <el-option value="text" label="text" />
                  <el-option value="png" label="png" />
                  <el-option value="jpg" label="jpg" />
                  <el-option value="markdown" label="markdown" />
                  <el-option value="html" label="html" />
                </el-select>
              </el-form-item>
              <el-form-item prop="engine" label="处理引擎" style="padding: 0 12px">
                <el-select
                    v-model="currentNodeDetail.node_file_reader_config.engine"
                    filterable
                    placeholder="请选择处理引擎"
                    @change="updateNodeFileReaderConfig"
                >
                  <el-option value="pandoc" label="pandoc" />
                  <el-option value="PyMuPDF" label="PyMuPDF" />
                  <el-option value="openpyxl" label="openpyxl" />
                  <el-option value="python-pptx" label="python-pptx" />
                  <el-option value="html2text" label="html2text" />
                  <el-option value="liboffice" label="liboffice" disabled/>
                  <el-option value="tika" label="tika" disabled/>
                </el-select>
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'file_splitter'" class="config-item">
          <div class="config-area">
            <el-form :model="currentNodeDetail" label-position="top">
              <el-form-item prop="method" label="切分方法" style="padding: 0 12px">
                <el-select
                    v-model="currentNodeDetail.node_file_splitter_config.method"
                    placeholder="请选择切分方法"
                    @change="updateNodeFileSplitterConfig"
                >
                  <el-option value="length" label="长度" />
                  <el-option value="symbol" label="分隔符" />
                  <el-option value="layout" label="布局结构" disabled/>
                </el-select>
              </el-form-item>
              <el-form-item prop="method" label="分块基础大小" style="padding: 0 12px">
                <el-input-number v-model="currentNodeDetail.node_file_splitter_config.chunk_size"
                                :min="1"
                                :max="10000" placeholder="请选择分块基础大小" :precision="0"
                                 style="width: 100%"
                                @change="updateNodeFileSplitterConfig"
                />
              </el-form-item>
              <el-form-item prop="chunk_overlap" label="分块重叠值" style="padding: 0 12px"
                            v-show="currentNodeDetail.node_file_splitter_config.method == 'length'">
                <el-input-number
                    v-model="currentNodeDetail.node_file_splitter_config.length_config.chunk_overlap"
                    :min="0"
                    :max="currentNodeDetail.node_file_splitter_config.chunk_size"
                    placeholder="请选择分块重叠值，值越大分段上下文重叠区域越大" :precision="0"
                    style="width: 100%"
                    @change="updateNodeFileSplitterConfig"
                />
              </el-form-item>
              <el-form-item prop="separators" label="分隔符" style="padding: 0 12px"
                            v-show="currentNodeDetail.node_file_splitter_config.method == 'symbol'"
              >
                <el-input
                    v-model="currentNodeDetail.node_file_splitter_config.symbol_config.separators"
                    placeholder="请输入分隔符"
                    @change="updateNodeFileSplitterConfig"
                />
              </el-form-item>
              <el-form-item prop="keep_separator" label="保留分隔符" style="padding: 0 12px"
                            v-show="currentNodeDetail.node_file_splitter_config.method == 'symbol'"
              >
                <el-switch
                    v-model="currentNodeDetail.node_file_splitter_config.symbol_config.keep_separator"
                    @change="updateNodeFileSplitterConfig"
                />
              </el-form-item>
              <el-form-item prop="merge_chunks" label="合并小于基础长度的小分块" style="padding: 0 12px"
                            v-show="currentNodeDetail.node_file_splitter_config.method == 'symbol'"
              >
                <el-switch
                    v-model="currentNodeDetail.node_file_splitter_config.symbol_config.merge_chunks"
                    @change="updateNodeFileSplitterConfig"
                />
              </el-form-item>
              <el-form-item prop="merge_chunks" label="合并小于基础长度的小分块" style="padding: 0 12px"
                            v-show="currentNodeDetail.node_file_splitter_config.method == 'layout'"
              >
                <el-switch
                    v-model="currentNodeDetail.node_file_splitter_config.layout_config.merge_chunks"
                    @change="updateNodeFileSplitterConfig"
                />
              </el-form-item>
              <el-form-item prop="preserve_structures" label="保留元素结构" style="padding: 0 12px"
                            v-show="currentNodeDetail.node_file_splitter_config.method == 'layout'"
              >
                <el-select multiple
                    v-model="currentNodeDetail.node_file_splitter_config.layout_config.preserve_structures"
                    @change="updateNodeFileSplitterConfig"
                >
                  <el-option value="paragraph" label="段落" />
                  <el-option value="heading" label="标题" />
                  <el-option value="list" label="列表" />
                  <el-option value="table" label="表格" />
                  <el-option value="code" label="代码块" />
                </el-select>
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="currentNodeDetail?.node_type == 'workflow'" class="config-item">
          <div class="config-area">
            <el-form :model="currentNodeDetail" label-position="top">
              <el-form-item prop="target_workflow_code" label="目标工作流" style="padding: 0 12px">
                <el-select
                    v-model="currentNodeDetail.node_sub_workflow_config.target_workflow_code"
                    placeholder="请搜索子工作流"
                    @change="updateNodeSubWorkflowConfig"
                    filterable
                    remote
                    :loading="searchSubWorkflowLoading"
                    :remote-method="searchSubWorkflow"
                >
                  <template #label="{ label, value }">
                    <div class="std-middle-box" style="justify-content: flex-start; gap: 4px">
                      <div class="std-middle-box">
                        <el-image :src="getSubWorkflowInfo(value)?.workflow_icon"
                                  style="width: 16px;height: 16px;border-radius: 20%" />
                      </div>
                      <div>
                        <el-tooltip :content="getSubWorkflowInfo(value)?.workflow_desc" :show-after="1000">
                          <el-text>{{label}}</el-text>
                        </el-tooltip>
                      </div>
                    </div>
                  </template>
                  <el-option
                      v-for="item in currentNodeDetail.subWorkflowOptions"
                      :key="item.id"
                      :label="item.workflow_name"
                      :value="item.workflow_code"
                  >

                    <div class="std-middle-box" style="justify-content: flex-start; gap: 4px">
                      <div class="std-middle-box">
                        <el-image :src="item.workflow_icon" style="width: 16px;height: 16px;border-radius: 20%" />
                      </div>
                      <div>
                        <el-tooltip :content="item.workflow_desc" :show-after="1000">
                          <el-text>{{item.workflow_name}}</el-text>
                        </el-tooltip>
                      </div>
                    </div>
                  </el-option>
                </el-select>
              </el-form-item>

            </el-form>
          </div>
        </div>
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
              <el-tooltip content="配置结果的解析格式、配置结果输出至消息流">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-show="showOutputParamsFlag" class="config-area">
            <el-form
                :model="currentNodeDetail"
                label-position="top"
                style="padding: 12px"
                require-asterisk-position="right"
            >
              <el-form-item prop="node_result_format" label="数据格式">
                <el-select
                    v-model="currentNodeDetail.node_result_format"
                    :disabled="['start', 'rag', 'llm', 'file_reader', 'file_splitter', 'workflow', 'end'].includes(
                        currentNodeDetail?.node_type)"
                    @change="updateNodeOutputConfig"
                >
                  <el-option value="text" label="text" />
                  <el-option value="json" label="json" />
                </el-select>
              </el-form-item>
              <el-form-item
                  v-show="currentNodeDetail?.node_result_format == 'table'"
                  prop="node_result_extract_separator"
                  label="分隔符"
              >
                <el-input
                    v-model="currentNodeDetail.node_result_extract_separator"
                    :maxlength="1"
                    @blur="updateNodeOutputConfig"
                />
              </el-form-item>
              <el-form-item
                  v-show="currentNodeDetail?.node_result_format == 'table'"
                  prop="node_result_extract_quote"
                  label="引用符"
              >
                <el-input
                    v-model="currentNodeDetail.node_result_extract_quote"
                    :maxlength="1"
                    @blur="updateNodeOutputConfig"
                />
              </el-form-item>
              <el-form-item
                  v-show="currentNodeDetail?.node_result_format == 'table'"
                  prop="node_result_extract_columns"
                  label="列名"
              >
                <el-select
                    v-model="currentNodeDetail.node_result_extract_columns"
                    multiple
                    allow-create
                    filterable
                    placeholder="请输入列名"
                    @blur="updateNodeOutputConfig"
                />
              </el-form-item>
              <el-form-item
                  v-if="currentNodeDetail.node_result_format == 'json'"
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
                    :jsonSchema="currentNodeDetail.node_result_params_json_schema"
                    :value-define="currentNodeDetail.node_type == 'end'"
                    :node-upstream="currentNodeDetail?.node_upstream"
                    :read-only="['start', 'rag', 'file_reader'].includes(currentNodeDetail?.node_type)"
                    :is-parent="!['llm'].includes(currentNodeDetail?.node_type)"
                    @update:schema="updateNodeOutputConfig"
                />
              </el-form-item>
              <el-form-item
                  v-else-if="currentNodeDetail.node_result_format == 'text'"
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
                <JsonSchemaForm :jsonSchema="currentNodeDetail.node_result_params_json_schema" :read-only="true" />
              </el-form-item>
              <el-form-item
                  v-show="!['start'].includes(currentNodeDetail?.node_type)"
                  prop="node_enable_message"
                  label="输出至消息流（用户可见）"
                  label-position="left"
                  required
              >
                <el-switch v-model="currentNodeDetail.node_enable_message" @change="updateNodeOutputConfig" />
              </el-form-item>
              <div v-show="currentNodeDetail.node_enable_message" class="node-message-list">

                <el-button type="primary" round @click="initNewMessageSchema">新增输出消息</el-button>
                <div v-for="(msgSchema, idx) in currentNodeDetail.node_message_schema" :key="idx">
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
                      :jsonSchema="msgSchema.schema"
                      :value-define="true"
                      :node-upstream="currentNodeDetail?.node_upstream2"
                      @update:schema="updateNodeOutputConfig"
                  />
                </div>
              </div>
            </el-form>
          </div>
        </div>
        <div v-if="!['start'].includes(currentNodeDetail?.node_type)" class="config-item">
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
              <el-tooltip content="配置节点运行策略">
                <el-icon>
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
          </div>
          <div v-if="showRunParamsFlag" class="config-area">
            <el-form :model="currentNodeDetail" label-position="top" style="padding: 12px">
              <el-form-item label="运行方式" prop="node_run_model">
                <el-radio-group v-model="currentNodeDetail.node_run_model_config.node_run_model"
                                @change="updateNodeRunConfig">
                  <el-radio-button value="sync" >默认</el-radio-button>
                  <el-radio-button value="parallel" >并行</el-radio-button>
                  <el-radio-button value="async" disabled >异步</el-radio-button>
                  <el-radio-button value="loop" disabled >循环</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item v-show="currentNodeDetail.node_run_model_config.node_run_model == 'parallel'"
                            label="并行属性" prop="parallel_attr">
                <el-select v-model="currentNodeDetail.node_run_model_config.parallel_attr"
                           @change="updateNodeRunConfig">
                  <el-option
                      v-for="(value, key) in currentNodeDetail.node_input_params_json_schema.properties"
                      :key="key"
                      :value="key"
                      :label="key + ' <' + (value?.type || '')  + '>'"
                      :disabled="!value?.type?.includes('array')"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="运行超时（秒）" prop="node_timeout">
                <el-input-number
                    v-model="currentNodeDetail.node_timeout"
                    :min="0"
                    :max="600"
                    @change="updateNodeRunConfig"
                />
              </el-form-item>
              <el-form-item label="失败策略" prop="node_failed_solution">
                <el-radio-group v-model="currentNodeDetail.node_failed_solution" @change="updateNodeRunConfig">
                  <el-radio-button v-show="currentNodeDetail.node_type != 'end'" label="重试" value="retry" />
                  <el-radio-button value="exit" >退出</el-radio-button>
                  <el-radio-button value="catch" >异常处理</el-radio-button>
                  <el-radio-button value="pass" >跳过</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item v-show="currentNodeDetail.node_failed_solution == 'retry'" label="最大重试次数">
                <el-input-number
                    v-model="currentNodeDetail.node_retry_max"
                    :max="3"
                    :min="0"
                    @change="updateNodeRunConfig"
                />
              </el-form-item>
              <el-form-item v-show="currentNodeDetail.node_failed_solution == 'retry'" label="重试间隔（毫秒）">
                <el-input-number
                    v-model="currentNodeDetail.node_retry_duration"
                    :min="0"
                    @change="updateNodeRunConfig"
                />
              </el-form-item>
              <el-form-item v-show="currentNodeDetail.node_failed_solution == 'retry'" label="重试后策略">
                <el-radio-group v-model="currentNodeDetail.node_retry_model" @change="updateNodeRunConfig">
                  <el-radio label="退出" :value="1" >退出</el-radio>
                  <el-radio label="异常处理" :value="2">异常处理</el-radio>
                  <el-radio label="跳过" :value="3">跳过</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item v-show="currentNodeDetail.node_failed_solution == 'catch'" label="异常输出结果">
                <TemplateEditor
                    id="node_failed_template"
                    style="width: 100%"
                    :value="currentNodeDetail.node_failed_template"
                    placeholder="请输入异常情况下的默认结果模板,可以通过/ 搜索上游变量，渲染结果将作为输出变量重新进行校验和消息输出"
                    :node="currentNodeDetail"
                    @update:value="newValue => handleTemplateChange(newValue, 'node_failed_template')"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </el-scrollbar>
  </div>
  <el-drawer v-model="showLLMConfigForm" title="模型配置" size="50vw">
    <el-scrollbar>
      <div class="std-middle-box">
        <el-form :model="currentNodeDetail.node_llm_params" label-position="top" style="width: 100%; padding: 12px">
          <el-form-item prop="use_default" label="使用默认配置" style="height: 80px">
            <el-switch v-model="currentNodeDetail.node_llm_params.use_default" @change="updateNodeLLMConfig" />
          </el-form-item>
          <el-form-item prop="temperature" label="温度" style="height: 80px">
            <el-slider
                v-model="currentNodeDetail.node_llm_params.temperature"
                :min="0"
                :max="2"
                :step="0.1"
                :marks="temperatureMarks"
                style="margin: 0 24px"
                show-input
                :show-input-controls="false"
                :disabled="currentNodeDetail.node_llm_params.use_default"
                @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="frequency_penalty" label="频率惩罚" style="height: 80px">
            <el-slider
                v-model="currentNodeDetail.node_llm_params.frequency_penalty"
                :min="-2"
                :max="2"
                :step="0.1"
                :marks="frequencyPenaltyMarks"
                style="margin: 0 24px"
                show-input
                :show-input-controls="false"
                :disabled="currentNodeDetail.node_llm_params.use_default"
                @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="top_p" label="核采样" style="height: 80px">
            <el-slider
                v-model="currentNodeDetail.node_llm_params.top_p"
                :min="0"
                :max="1"
                :step="0.1"
                :marks="topPMarks"
                style="margin: 0 24px"
                show-input
                :show-input-controls="false"
                :disabled="currentNodeDetail.node_llm_params.use_default"
                @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="presence_penalty" label="出现惩罚" style="height: 80px">
            <el-slider
                v-model="currentNodeDetail.node_llm_params.presence_penalty"
                :min="-2"
                :max="2"
                :step="0.1"
                :marks="frequencyPenaltyMarks"
                style="margin: 0 24px"
                show-input
                :show-input-controls="false"
                :disabled="currentNodeDetail.node_llm_params.use_default"
                @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="max_tokens" label="最大输出token" style="height: 80px">
            <el-slider
                v-model="currentNodeDetail.node_llm_params.max_tokens"
                :min="1"
                :max="16000"
                :step="1"
                :marks="maxTokensMarks"
                style="margin: 0 24px"
                show-input
                :show-input-controls="false"
                :disabled="currentNodeDetail.node_llm_params.use_default"
                @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="extra_body" label="额外Body参数" style="height: 80px">
            <JsonSchemaForm
                :jsonSchema="currentNodeDetail.node_llm_params.extra_body_schema"
                :value-define="true"
                :node-upstream="currentNodeDetail?.node_upstream"
                @update:schema="newSchema => {
                  currentNodeDetail.node_llm_params.extra_body_schema = newSchema;
                  updateNodeLLMConfig();
                }"
            />
          </el-form-item>
        </el-form>
      </div>
    </el-scrollbar>
  </el-drawer>
  <ResourcesSearch
      v-if="currentNodeDetail.node_type == 'rag'"
      ref="resourcesSearchRef"
      :model="resourceSearchDialogShow"
      @close="resourceSearchDialogShow = false"
      @commit="
      args => {
        commitAddChooseResources();
      }
    "
  />
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
.agent-node-option {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: space-between;
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
.config-llm-icon {
  width: 12px;
  height: 12px;
}
.llm-instance-area {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 300px;
}
.llm-instance-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  border-radius: 8px;
  padding: 6px 8px;
  margin-right: 10px;
  cursor: pointer;
  background: #ffffff;
}
.llm-instance-item:hover {
  background: #eff8ff;
}
.llm-instance-item-active {
  background: #eff8ff;
}
.config-area {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.rag-area {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}
.rag-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.resource-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
  width: calc(100% - 24px);
  height: 40px;
  padding: 4px 12px;
  background-color: #eff8ff;
  border-radius: 8px;
}
.resource-item-left {
  display: flex;
  flex-direction: row;
  gap: 8px;
}
.resource-icon {
  width: 24px;
  height: 24px;
}
.node-message-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
