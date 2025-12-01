<script setup lang="ts">
import { ArrowDown, ArrowRight, QuestionFilled } from '@element-plus/icons-vue';
import { ref } from 'vue';
import { nodeUpdate } from '@/api/app-center-api';
import JsonSchemaForm from '@/components/app-center/app-manage/JsonSchemaForm.vue';
import TemplateEditor from '@/components/app-center/app-manage/TemplateEditor.vue';
import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';
const showCastConfigFlag = ref(false);
const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
const castOptions = [
  {
    label: '文本',
    value: 'string'
  },
  {
    label: '对象',
    value: 'object'
  }
];
async function updateNodeCastConfig() {

  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_variable_cast_config: workflowStore.currentNodeDetail.node_variable_cast_config,
    node_result_params_json_schema: workflowStore.currentNodeDetail.node_result_params_json_schema
  });
}
async function handleCastTypeChange(value: string) {
  if (value == 'string') {
    workflowStore.currentNodeDetail.node_result_params_json_schema = {
      type: 'object',
      properties: {
        content: {
          type: 'string',
          typeName: 'string',
          description: '转换后内容',
          attrFixed: true,
          typeFixed: true,
          valueFixed: true
        }
      },
      ncOrders: ['content'],
      attrFixed: true,
      typeFixed: true,
      valueFixed: true
    };
  } else if (value == 'object') {
    // @ts-ignore
    workflowStore.currentNodeDetail.node_result_params_json_schema =
        workflowStore.currentNodeDetail.node_variable_cast_config.cast_schema;
  }
  await updateNodeCastConfig();
}

async function handleTemplateChange(value: string) {
  workflowStore.currentNodeDetail.node_variable_cast_config.string_template = value;
  await updateNodeCastConfig();
}
</script>

<template>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'variable_cast'" class="config-item">
    <div class="config-head">
      <div class="std-middle-box">
        <el-icon v-if="showCastConfigFlag" class="config-arrow" @click="showCastConfigFlag = false">
          <ArrowDown />
        </el-icon>
        <el-icon v-else class="config-arrow" @click="showCastConfigFlag = true">
          <ArrowRight />
        </el-icon>
      </div>
      <div class="std-middle-box">
        <el-text> 变量转换设置 </el-text>
      </div>
      <div>
        <el-tooltip content="将单变量或者多变量进行类型转换和聚合操作">
          <el-icon>
            <QuestionFilled />
          </el-icon>
        </el-tooltip>
      </div>
    </div>
    <div v-show="showCastConfigFlag" class="config-area">
      <el-form :model="workflowStore.currentNodeDetail" label-position="top">
        <el-form-item prop="node_variable_cast_config.cast_type" label="转换类型" style="padding: 0 12px">
          <el-segmented
            v-model="workflowStore.currentNodeDetail.node_variable_cast_config.cast_type"
            :options="castOptions"
            @change="handleCastTypeChange"
          />
        </el-form-item>
        <el-form-item
          v-if="workflowStore.currentNodeDetail.node_variable_cast_config.cast_type == 'string'"
          prop="node_variable_cast_config.string_template"
          label="输出模板"
          style="padding: 0 12px"
        >
          <TemplateEditor
            :value="workflowStore.currentNodeDetail.node_variable_cast_config.string_template"
            style="width: 100%"
            placeholder="请输入输出模板，如：请问天气如何。可以通过/ 唤出上游变量列表"
            :node="workflowStore.currentNodeDetail"
            @update:value="newValue => handleTemplateChange(newValue)"
          />
        </el-form-item>
        <el-form-item
          v-if="workflowStore.currentNodeDetail.node_variable_cast_config.cast_type == 'object'"
          prop="node_variable_cast_config.cast_schema"
          label="输出变量"
          style="padding: 0 12px"
        >
          <JsonSchemaForm
            :json-schema="workflowStore.currentNodeDetail.node_variable_cast_config.cast_schema"
            :node-upstream="workflowStore.currentNodeDetail?.nodeSelf"
            :value-define="true"
            @update:schema="
              newSchema => {
                workflowStore.currentNodeDetail.node_variable_cast_config.cast_schema = newSchema;
                updateNodeCastConfig();
              }
            "
          />
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
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
</style>
