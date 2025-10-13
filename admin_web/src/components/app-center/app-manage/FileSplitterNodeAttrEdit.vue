<script setup lang="ts">
import { nodeUpdate } from '@/api/app-center-api';
import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';
const emits = defineEmits(['updateNodeInputConfig', 'updateNodeOutputConfig']);
const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
async function updateNodeFileSplitterConfig() {
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_file_splitter_config: workflowStore.currentNodeDetail.node_file_splitter_config
  });
}
async function handleFileSplitterModeChange(val: string) {
  // 将input_resources 入参进行处理

  if (val == 'single') {
    workflowStore.currentNodeDetail.node_input_params_json_schema.properties['content'] = {
      type: 'string',
      typeName: 'string',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '文本'
    };
    delete workflowStore.currentNodeDetail.node_input_params_json_schema.properties['contents'];
    workflowStore.currentNodeDetail.node_input_params_json_schema.ncOrders[0] = 'content';
  } else if (val == 'list') {
    workflowStore.currentNodeDetail.node_input_params_json_schema.properties['contents'] = {
      type: 'array',
      typeName: 'array[string]',
      value: '',
      ref: '',
      showSubArea: true,
      attrFixed: true,
      typeFixed: true,
      description: '文本列表',
      items: {
        type: 'string',
        typeName: 'string',
        value: '',
        ref: '',
        showSubArea: true,
        attrFixed: true,
        typeFixed: true,
        description: '文本'
      }
    };
    delete workflowStore.currentNodeDetail.node_input_params_json_schema.properties['content'];
    workflowStore.currentNodeDetail.node_input_params_json_schema.ncOrders[0] = 'contents';
  }
  emits('updateNodeInputConfig');
  emits('updateNodeOutputConfig');
  updateNodeFileSplitterConfig();
}
</script>

<template>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'file_splitter'" class="config-item">
    <div class="config-area">
      <el-form :model="workflowStore.currentNodeDetail" label-position="top">
        <el-form-item prop="mode" label="模式" style="padding: 0 12px">
          <el-radio-group
            v-model="workflowStore.currentNodeDetail.node_file_splitter_config.mode"
            @change="handleFileSplitterModeChange"
          >
            <el-radio value="single">单文本</el-radio>
            <el-radio value="list">文本列表</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item prop="method" label="切分方法" style="padding: 0 12px">
          <el-select
            v-model="workflowStore.currentNodeDetail.node_file_splitter_config.method"
            placeholder="请选择切分方法"
            @change="updateNodeFileSplitterConfig"
          >
            <el-option value="length" label="长度" />
            <el-option value="symbol" label="分隔符" />
            <el-option value="layout" label="布局结构" disabled />
          </el-select>
        </el-form-item>
        <el-form-item prop="method" label="分块基础大小" style="padding: 0 12px">
          <el-input-number
            v-model="workflowStore.currentNodeDetail.node_file_splitter_config.chunk_size"
            :min="1"
            :max="60000"
            placeholder="请选择分块基础大小"
            :precision="0"
            style="width: 100%"
            @change="updateNodeFileSplitterConfig"
          />
        </el-form-item>
        <el-form-item
          v-show="workflowStore.currentNodeDetail.node_file_splitter_config.method == 'length'"
          prop="chunk_overlap"
          label="分块重叠值"
          style="padding: 0 12px"
        >
          <el-input-number
            v-model="workflowStore.currentNodeDetail.node_file_splitter_config.length_config.chunk_overlap"
            :min="0"
            :max="workflowStore.currentNodeDetail.node_file_splitter_config.chunk_size"
            placeholder="请选择分块重叠值，值越大分段上下文重叠区域越大"
            :precision="0"
            style="width: 100%"
            @change="updateNodeFileSplitterConfig"
          />
        </el-form-item>
        <el-form-item
          v-show="workflowStore.currentNodeDetail.node_file_splitter_config.method == 'symbol'"
          prop="separators"
          label="分隔符"
          style="padding: 0 12px"
        >
          <el-input
            v-model="workflowStore.currentNodeDetail.node_file_splitter_config.symbol_config.separators"
            placeholder="请输入分隔符"
            @change="updateNodeFileSplitterConfig"
          />
        </el-form-item>
        <el-form-item
          v-show="workflowStore.currentNodeDetail.node_file_splitter_config.method == 'symbol'"
          prop="keep_separator"
          label="保留分隔符"
          style="padding: 0 12px"
        >
          <el-switch
            v-model="workflowStore.currentNodeDetail.node_file_splitter_config.symbol_config.keep_separator"
            @change="updateNodeFileSplitterConfig"
          />
        </el-form-item>
        <el-form-item
          v-show="workflowStore.currentNodeDetail.node_file_splitter_config.method == 'symbol'"
          prop="merge_chunks"
          label="合并小于基础长度的小分块"
          style="padding: 0 12px"
        >
          <el-switch
            v-model="workflowStore.currentNodeDetail.node_file_splitter_config.symbol_config.merge_chunks"
            @change="updateNodeFileSplitterConfig"
          />
        </el-form-item>
        <el-form-item
          v-show="workflowStore.currentNodeDetail.node_file_splitter_config.method == 'layout'"
          prop="merge_chunks"
          label="合并小于基础长度的小分块"
          style="padding: 0 12px"
        >
          <el-switch
            v-model="workflowStore.currentNodeDetail.node_file_splitter_config.layout_config.merge_chunks"
            @change="updateNodeFileSplitterConfig"
          />
        </el-form-item>
        <el-form-item
          v-show="workflowStore.currentNodeDetail.node_file_splitter_config.method == 'layout'"
          prop="preserve_structures"
          label="保留元素结构"
          style="padding: 0 12px"
        >
          <el-select
            v-model="workflowStore.currentNodeDetail.node_file_splitter_config.layout_config.preserve_structures"
            multiple
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
</template>

<style scoped>
.config-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 6px;
  border-bottom: 1px solid #f0f0f0;
}

.config-area {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
