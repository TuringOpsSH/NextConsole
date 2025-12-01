<script setup lang="ts">
import { ArrowDown, ArrowRight, QuestionFilled, Setting } from '@element-plus/icons-vue';
import { type CSSProperties, watch, reactive, ref } from 'vue';
import { nodeUpdate } from '@/api/app-center-api';
import { llmInstanceSearch } from '@/api/config-center';
import JsonSchemaForm from '@/components/app-center/app-manage/JsonSchemaForm.vue';
import RefSelect from '@/components/app-center/app-manage/RefSelect.vue';
import TemplateEditor from '@/components/app-center/app-manage/TemplateEditor.vue';
import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';
import { ILLMInstance } from '@/types/config-center';
const showPromptConfigFlag = ref(false);
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
`;
const showLLMConfigFlag = ref(false);
const allLLMInstanceList = ref<ILLMInstance[]>([]);
const showLLMConfigForm = ref(false);
const showMemoryConfigFlag = ref(false);
const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
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
const currentLLMInstance = ref<ILLMInstance | null>(null);
async function handleTemplateChange(newValue, src = '') {
  if (src == 'node_llm_system_prompt_template') {
    workflowStore.currentNodeDetail.node_llm_system_prompt_template = newValue;
    updateNodePrompt();
  } else if (src == 'node_llm_user_prompt_template') {
    workflowStore.currentNodeDetail.node_llm_user_prompt_template = newValue;
    updateNodePrompt();
  }
}
async function updateNodePrompt() {
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_llm_system_prompt_template: workflowStore.currentNodeDetail.node_llm_system_prompt_template,
    node_llm_user_prompt_template: workflowStore.currentNodeDetail.node_llm_user_prompt_template
  });
}
async function updateNodeMemoryConfig() {
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_session_memory_size: workflowStore.currentNodeDetail.node_session_memory_size,
    node_deep_memory: workflowStore.currentNodeDetail.node_deep_memory
  });
}
async function updateNodeLLMConfig() {
  if (!workflowStore.currentNodeDetail.node_llm_params) {
    // @ts-ignore
    workflowStore.currentNodeDetail.node_llm_params = {};
  }
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_llm_params: workflowStore.currentNodeDetail.node_llm_params
  });
}
async function updateNodeRagConfig() {
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_rag_resources: workflowStore.currentNodeDetail.node_rag_resources,
    node_rag_query_template: workflowStore.currentNodeDetail.node_rag_query_template,
    node_rag_recall_config: workflowStore.currentNodeDetail.node_rag_recall_config,
    node_rag_rerank_config: workflowStore.currentNodeDetail.node_rag_rerank_config,
    node_rag_web_search_config: workflowStore.currentNodeDetail.node_rag_web_search_config,
    node_rag_ref_show: workflowStore.currentNodeDetail.node_rag_ref_show
  });
}
async function switchLLMInstance() {
  if (!workflowStore.currentNodeDetail.node_llm_params) {
    // @ts-ignore
    workflowStore.currentNodeDetail.node_llm_params = {};
  }
  workflowStore.currentNodeDetail.node_llm_params.llm_name = currentLLMInstance.value?.llm_name;
  workflowStore.currentNodeDetail.node_llm_params.llm_icon = currentLLMInstance.value?.llm_icon;
  workflowStore.currentNodeDetail.node_llm_params.llm_desc = currentLLMInstance.value?.llm_desc;
  workflowStore.currentNodeDetail.node_llm_params.support_vis = currentLLMInstance.value?.support_vis;
  workflowStore.currentNodeDetail.node_llm_params.support_file = currentLLMInstance.value?.support_file;
  const res = await nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_llm_code: currentLLMInstance.value?.llm_code,
    node_llm_params: workflowStore.currentNodeDetail.node_llm_params
  });
  if (!res.error_status) {
    workflowStore.currentNodeDetail.node_llm_code = currentLLMInstance.value?.llm_code;
    // 更新工作流节点的模型字段
    const currentNode = workflowStore.graphWrapper.getCellById(workflowStore.currentNodeDetail.node_code);
    currentNode.updateData({
      nodeModel: currentLLMInstance.value?.llm_label
    });
  }
}
async function searchLLM(key: string) {
  const res = await llmInstanceSearch({
    fetch_all: true,
    keyword: key
  });
  if (!res.error_status) {
    allLLMInstanceList.value = res.result.data;
  }
  if (workflowStore.currentNodeDetail.node_llm_code) {
    const currentLLM = allLLMInstanceList.value.find(
      item => item.llm_code == workflowStore.currentNodeDetail.node_llm_code
    );
    if (currentLLM) {
      currentLLMInstance.value = currentLLM;
    }
  }
}
watch(
  () => workflowStore.currentNodeDetail.node_llm_code,
  () => {
    searchLLM('');
  },
  { immediate: true }
);
</script>

<template>
  <div>
    <div v-if="workflowStore.currentNodeDetail?.node_type == 'llm'" class="config-item">
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
                {{ promptTips }}
              </div>
            </template>
            <el-icon>
              <QuestionFilled />
            </el-icon>
          </el-tooltip>
        </div>
      </div>
      <div v-show="showPromptConfigFlag" class="config-area">
        <el-form :model="workflowStore.currentNodeDetail" label-position="top" style="padding: 12px">
          <el-form-item prop="node_llm_system_prompt_template" label="系统提示词">
            <TemplateEditor
              id="node_llm_system_prompt_template"
              :value="workflowStore.currentNodeDetail.node_llm_system_prompt_template"
              style="width: 100%"
              placeholder="请输入系统提示词，如：你是一个AI助手。可以通过/ 唤出上游变量列表"
              :node="workflowStore.currentNodeDetail"
              @update:value="newValue => handleTemplateChange(newValue, 'node_llm_system_prompt_template')"
            />
          </el-form-item>
          <el-form-item prop="node_llm_user_prompt_template" label="用户提示词">
            <TemplateEditor
              id="node_llm_user_prompt_template"
              :value="workflowStore.currentNodeDetail.node_llm_user_prompt_template"
              style="width: 100%"
              placeholder="请输入用户提示词，如：请问天气如何。可以通过/ 唤出上游变量列表"
              :node="workflowStore.currentNodeDetail"
              @update:value="newValue => handleTemplateChange(newValue, 'node_llm_user_prompt_template')"
            />
          </el-form-item>
          <el-form-item label="显示参考资料" style="padding: 0 12px">
            <el-switch
              v-model="workflowStore.currentNodeDetail.node_rag_ref_show"
              active-text="提供"
              inactive-text="隐藏"
              @change="updateNodeRagConfig"
            />
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div v-if="workflowStore.currentNodeDetail?.node_type == 'llm'" class="config-item">
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
          <el-select
            v-model="currentLLMInstance"
            value-key="llm_code"
            remote
            :remote-method="searchLLM"
            filterable
            placeholder="选择基础模型"
            style="width: 100%"
            @change="switchLLMInstance"
          >
            <template #label="{ value }">
              <div class="llm-instance-item">
                <div class="std-middle-box">
                  <el-avatar
                    :src="value.llm_icon"
                    style="width: 20px; height: 20px; background-color: white"
                    fit="contain"
                  />
                </div>
                <div class="std-middle-box" style="justify-content: flex-start">
                  <el-text truncated style="font-size: 14px; font-weight: 500; line-height: 20px; color: #344054">
                    {{ value.llm_label }}
                  </el-text>
                </div>
              </div>
            </template>
            <el-option v-for="(item, idx) in allLLMInstanceList" :key="idx" :value="item">
              <div class="llm-instance-item">
                <div class="std-middle-box">
                  <el-avatar
                    :src="item.llm_icon"
                    style="width: 20px; height: 20px; background-color: white"
                    fit="contain"
                  />
                </div>
                <div class="std-middle-box" style="justify-content: flex-start">
                  <el-text truncated style="font-size: 14px; font-weight: 500; line-height: 20px; color: #344054">
                    {{ item.llm_label }}
                  </el-text>
                </div>
              </div>
            </el-option>
          </el-select>
          <div class="std-middle-box">
            <el-icon class="config-item" style="cursor: pointer" @click="showLLMConfigForm = true">
              <Setting />
            </el-icon>
          </div>
        </div>

        <div class="std-left-box">
          <el-form style="width: 100%">
            <el-form-item prop="stream" label="流式输出">
              <el-switch
                v-model="workflowStore.currentNodeDetail.node_llm_params.stream"
                @change="updateNodeLLMConfig"
              />
            </el-form-item>
            <el-form-item v-if="workflowStore.currentNodeDetail.node_llm_params.support_vis" label="视觉能力">
              <el-switch
                v-model="workflowStore.currentNodeDetail.node_llm_params.enable_visual"
                @change="updateNodeLLMConfig"
              />
            </el-form-item>
            <el-form-item
              v-if="
                workflowStore.currentNodeDetail.node_llm_params.support_vis &&
                workflowStore.currentNodeDetail.node_llm_params?.enable_visual
              "
              label="图片输入"
              label-position="top"
            >
              <JsonSchemaForm
                style="margin-left: 24px"
                :json-schema="workflowStore.currentNodeDetail.node_llm_params.visual_schema"
                :value-define="true"
                :node-upstream="workflowStore.currentNodeDetail?.nodeSelf"
                :is-parent="false"
                @update:schema="updateNodeLLMConfig"
              />
            </el-form-item>
            <el-form-item v-if="workflowStore.currentNodeDetail.node_llm_params.support_file" label="文件阅读能力">
              <el-switch
                v-model="workflowStore.currentNodeDetail.node_llm_params.enable_file"
                @change="updateNodeLLMConfig"
              />
            </el-form-item>
            <el-form-item
              v-if="
                workflowStore.currentNodeDetail.node_llm_params.support_file &&
                workflowStore.currentNodeDetail.node_llm_params?.enable_file
              "
              label="文件输入"
            >
              <RefSelect
                :up-stream-nodes="workflowStore.currentNodeDetail.node_upstream"
                :ref-value="workflowStore.currentNodeDetail.node_llm_params.file_ref"
                style="width: 100%"
                @update:ref="
                  result => {
                    workflowStore.currentNodeDetail.node_llm_params.file_ref = result;
                    updateNodeLLMConfig();
                  }
                "
              />
            </el-form-item>
            <el-form-item prop="response_format" label="输出格式">
              <el-select
                v-model="workflowStore.currentNodeDetail.node_llm_params.response_format"
                @change="updateNodeLLMConfig"
              >
                <el-option value="text" label="text" />
                <el-option value="json" label="json" />
              </el-select>
            </el-form-item>
            <el-form-item prop="stop" label="停止词">
              <el-select
                v-model="workflowStore.currentNodeDetail.node_llm_params.stop"
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
    <div v-if="workflowStore.currentNodeDetail?.node_type == 'llm'" class="config-item">
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
        <el-form :model="workflowStore.currentNodeDetail" label-position="top" style="padding: 12px">
          <el-form-item prop="node_session_memory_size" label="会话记忆长度">
            <el-input-number
              v-model="workflowStore.currentNodeDetail.node_session_memory_size"
              :min="0"
              @change="updateNodeMemoryConfig"
            />
          </el-form-item>
          <el-form-item prop="node_session_memory_size" label="深度记忆">
            <el-switch v-model="workflowStore.currentNodeDetail.node_deep_memory" @change="updateNodeMemoryConfig" />
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
  <el-drawer v-model="showLLMConfigForm" title="模型配置" size="50vw" resizable>
    <el-scrollbar>
      <div class="std-middle-box">
        <el-form
          :model="workflowStore.currentNodeDetail.node_llm_params"
          label-position="top"
          style="width: 100%; padding: 12px"
        >
          <el-form-item prop="use_default" label="使用默认配置" style="height: 80px">
            <el-switch
              v-model="workflowStore.currentNodeDetail.node_llm_params.use_default"
              @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="temperature" label="温度" style="height: 80px">
            <el-slider
              v-model="workflowStore.currentNodeDetail.node_llm_params.temperature"
              :min="0"
              :max="2"
              :step="0.1"
              :marks="temperatureMarks"
              style="margin: 0 24px"
              show-input
              :show-input-controls="false"
              :disabled="workflowStore.currentNodeDetail.node_llm_params.use_default"
              @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="frequency_penalty" label="频率惩罚" style="height: 80px">
            <el-slider
              v-model="workflowStore.currentNodeDetail.node_llm_params.frequency_penalty"
              :min="-2"
              :max="2"
              :step="0.1"
              :marks="frequencyPenaltyMarks"
              style="margin: 0 24px"
              show-input
              :show-input-controls="false"
              :disabled="workflowStore.currentNodeDetail.node_llm_params.use_default"
              @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="top_p" label="核采样" style="height: 80px">
            <el-slider
              v-model="workflowStore.currentNodeDetail.node_llm_params.top_p"
              :min="0"
              :max="1"
              :step="0.1"
              :marks="topPMarks"
              style="margin: 0 24px"
              show-input
              :show-input-controls="false"
              :disabled="workflowStore.currentNodeDetail.node_llm_params.use_default"
              @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="presence_penalty" label="出现惩罚" style="height: 80px">
            <el-slider
              v-model="workflowStore.currentNodeDetail.node_llm_params.presence_penalty"
              :min="-2"
              :max="2"
              :step="0.1"
              :marks="frequencyPenaltyMarks"
              style="margin: 0 24px"
              show-input
              :show-input-controls="false"
              :disabled="workflowStore.currentNodeDetail.node_llm_params.use_default"
              @change="updateNodeLLMConfig"
            />
          </el-form-item>
          <el-form-item prop="max_tokens" label="最大输出token" style="height: 80px">
            <el-slider
              v-model="workflowStore.currentNodeDetail.node_llm_params.max_tokens"
              :min="1"
              :max="16000"
              :step="1"
              :marks="maxTokensMarks"
              style="margin: 0 24px"
              show-input
              :show-input-controls="false"
              :disabled="workflowStore.currentNodeDetail.node_llm_params.use_default"
              @change="updateNodeLLMConfig"
            />
          </el-form-item>

          <el-form-item prop="extra_body" label="额外Body参数" style="height: 80px">
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
              :json-schema="workflowStore.currentNodeDetail.node_llm_params.extra_body_schema"
              :value-define="true"
              :node-upstream="workflowStore.currentNodeDetail?.node_upstream"
              @update:schema="
                newSchema => {
                  workflowStore.currentNodeDetail.node_llm_params.extra_body_schema = newSchema;
                  updateNodeLLMConfig();
                }
              "
            />
          </el-form-item>
        </el-form>
      </div>
    </el-scrollbar>
  </el-drawer>
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
}
.config-area {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
