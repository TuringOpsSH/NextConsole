<script setup lang="ts">
import { ref } from 'vue';
import { nodeUpdate, workflowSearch, workflowUpdate } from '@/api/app-center-api';

import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';
const searchSubWorkflowLoading = ref(false);
const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
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
async function updateNodeSubWorkflowConfig() {
  const pickSubWorkflow = workflowStore.currentNodeDetail.subWorkflowOptions.find(
    item => item.workflow_code == workflowStore.currentNodeDetail.node_sub_workflow_config.target_workflow_code
  );

  workflowStore.currentNodeDetail.node_input_params_json_schema = pickSubWorkflow.workflow_params_schema;
  workflowStore.currentNodeDetail.node_result_params_json_schema = pickSubWorkflow.workflow_result_schema;
  workflowStore.currentNodeDetail.node_input_params_json_schema.attrFixed = true;
  workflowStore.currentNodeDetail.node_result_params_json_schema.attrFixed = true;
  for (let k of workflowStore.currentNodeDetail.node_input_params_json_schema.ncOrders) {
    if (workflowStore.currentNodeDetail.node_input_params_json_schema.properties[k]) {
      workflowStore.currentNodeDetail.node_input_params_json_schema.properties[k].attrFixed = true;
      workflowStore.currentNodeDetail.node_input_params_json_schema.properties[k].typeFixed = true;
    }
  }
  for (let k of workflowStore.currentNodeDetail.node_result_params_json_schema.ncOrders) {
    if (workflowStore.currentNodeDetail.node_result_params_json_schema.properties[k]) {
      workflowStore.currentNodeDetail.node_result_params_json_schema.properties[k].attrFixed = true;
      workflowStore.currentNodeDetail.node_result_params_json_schema.properties[k].typeFixed = true;
    }
  }
  const res = await nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_sub_workflow_config: workflowStore.currentNodeDetail.node_sub_workflow_config,
    node_input_params_json_schema: workflowStore.currentNodeDetail.node_input_params_json_schema,
    node_result_params_json_schema: workflowStore.currentNodeDetail.node_result_params_json_schema
  });
  if (!res.error_status) {
    workflowStore.currentNodeDetail.node_sub_workflow_config.target_workflow_name = pickSubWorkflow.workflow_name;
    // 更新工作流节点的名称
    const currentNode = workflowStore.graphWrapper.getCellById(workflowStore.currentNodeDetail.node_code);
    currentNode.updateData({
      nodeParams: workflowStore.currentNodeDetail.node_input_params_json_schema?.ncOrders,
      nodeResultParams: workflowStore.currentNodeDetail.node_result_params_json_schema?.ncOrders
    });
    const graphData = workflowStore.graphWrapper.toJSON();
    workflowUpdate({
      app_code: appInfoStore.currentApp.app_code,
      workflow_code: workflowStore.currentFlow.workflow_code,
      workflow_edit_schema: graphData
    });
  }
}
function getSubWorkflowInfo(val: string) {
  return workflowStore.currentNodeDetail.subWorkflowOptions?.find(item => item.workflow_code == val);
}
</script>

<template>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'workflow'" class="config-item">
    <div class="config-area">
      <el-form :model="workflowStore.currentNodeDetail" label-position="top">
        <el-form-item prop="target_workflow_code" label="目标工作流" style="padding: 0 12px">
          <el-select
            v-model="workflowStore.currentNodeDetail.node_sub_workflow_config.target_workflow_code"
            placeholder="请搜索子工作流"
            filterable
            remote
            :loading="searchSubWorkflowLoading"
            :remote-method="searchSubWorkflow"
            @change="updateNodeSubWorkflowConfig"
          >
            <template #label="{ label, value }">
              <div class="std-middle-box" style="justify-content: flex-start; gap: 4px">
                <div class="std-middle-box">
                  <el-image
                    :src="getSubWorkflowInfo(value)?.workflow_icon"
                    style="width: 16px; height: 16px; border-radius: 20%"
                  />
                </div>
                <div>
                  <el-tooltip :content="getSubWorkflowInfo(value)?.workflow_desc" :show-after="1000">
                    <el-text>{{ label }}</el-text>
                  </el-tooltip>
                </div>
              </div>
            </template>
            <el-option
              v-for="item in workflowStore.currentNodeDetail.subWorkflowOptions"
              :key="item.id"
              :label="item.workflow_name"
              :value="item.workflow_code"
            >
              <div class="std-middle-box" style="justify-content: flex-start; gap: 4px">
                <div class="std-middle-box">
                  <el-image :src="item.workflow_icon" style="width: 16px; height: 16px; border-radius: 20%" />
                </div>
                <div>
                  <el-tooltip :content="item.workflow_desc" :show-after="1000">
                    <el-text>{{ item.workflow_name }}</el-text>
                  </el-tooltip>
                </div>
              </div>
            </el-option>
          </el-select>
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
.config-area {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
