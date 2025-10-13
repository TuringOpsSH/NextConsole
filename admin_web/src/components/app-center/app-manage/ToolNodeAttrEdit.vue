<script setup lang="ts">
import { ArrowDown, ArrowRight, QuestionFilled } from '@element-plus/icons-vue';
import { ref } from 'vue';
import { nodeUpdate } from '@/api/app-center-api';
import JsonSchemaForm from '@/components/app-center/app-manage/JsonSchemaForm.vue';

import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';
const showToolConfigFlag = ref(false);
const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
async function updateNodeToolConfig() {
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_tool_api_url: workflowStore.currentNodeDetail.node_tool_api_url,
    node_tool_http_method: workflowStore.currentNodeDetail.node_tool_http_method,
    node_tool_http_header: workflowStore.currentNodeDetail.node_tool_http_header,
    node_tool_http_params: workflowStore.currentNodeDetail.node_tool_http_params,
    node_tool_http_body: workflowStore.currentNodeDetail.node_tool_http_body,
    node_tool_http_body_type: workflowStore.currentNodeDetail.node_tool_http_body_type
  });
}
</script>

<template>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'tool'" class="config-item">
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
      <el-form :model="workflowStore.currentNodeDetail" label-position="top">
        <el-form-item prop="node_tool_api_url" label="URL" style="padding: 0 12px">
          <el-input
            v-model="workflowStore.currentNodeDetail.node_tool_api_url"
            placeholder="请输入API地址"
            @blur="updateNodeToolConfig"
          />
        </el-form-item>
        <el-form-item prop="node_tool_http_method" label="Method" style="padding: 0 12px">
          <el-select
            v-model="workflowStore.currentNodeDetail.node_tool_http_method"
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
            :json-schema="workflowStore.currentNodeDetail.node_tool_http_header"
            :value-define="true"
            :node-upstream="workflowStore.currentNodeDetail?.node_upstream"
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
            :json-schema="workflowStore.currentNodeDetail.node_tool_http_params"
            :value-define="true"
            :node-upstream="workflowStore.currentNodeDetail?.node_upstream"
            @update:schema="updateNodeToolConfig"
          />
        </el-form-item>
        <el-form-item prop="node_tool_http_body" label="Body" style="padding: 0 12px">
          <el-row style="width: 100%">
            <el-radio-group v-model="workflowStore.currentNodeDetail.node_tool_http_body_type" @change="updateNodeToolConfig">
              <el-radio value="json">json</el-radio>
              <el-radio value="form-data">form-data</el-radio>
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
            :json-schema="workflowStore.currentNodeDetail.node_tool_http_body"
            :value-define="true"
            :node-upstream="workflowStore.currentNodeDetail?.node_upstream"
            @update:schema="updateNodeToolConfig"
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
