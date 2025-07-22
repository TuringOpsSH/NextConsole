<script setup lang="ts">
import {
  currentEdgeDetail,
  CurrentEditFlow,
  graphWrapper,
  loadingEdgeInfo,
  showEdgeFlag
} from '@/components/appCenter/ts/workflow-edit';
import { ref } from 'vue';
import { Minus } from '@element-plus/icons-vue';
import { workflowUpdate } from '@/api/appCenterApi';
import { currentApp } from '@/components/appCenter/ts/app-detail';
import RefSelect from '@/components/appCenter/refSelect.vue';

const isResizing = ref(false);
const startX = ref(0);
const startWidth = ref(0);
const edgeDetailWidth = ref(560);
const edgeDetailRef = ref();
const showEdgeConfigFlag = ref(true);
function handleOverEdgeDetail(event) {
  const rect = edgeDetailRef.value.getBoundingClientRect();
  const leftBorderWidth = 10; // 左侧边框可触发拖拉的宽度范围
  if (event.clientX >= rect.left && event.clientX <= rect.left + leftBorderWidth) {
    edgeDetailRef.value.style.cursor = 'ew-resize';
  } else {
    edgeDetailRef.value.style.cursor = 'default';
  }
}
const onMouseDown = event => {
  const rect = edgeDetailRef.value.getBoundingClientRect();
  const leftBorderWidth = 10; // 左侧边框可触发拖拉的宽度范围
  if (event.clientX >= rect.left && event.clientX <= rect.left + leftBorderWidth) {
    isResizing.value = true;
    startX.value = event.clientX;
    startWidth.value = edgeDetailWidth.value;
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    edgeDetailRef.value.style.cursor = 'ew-resize';
  }
};
const onMouseMove = event => {
  if (isResizing.value) {
    const deltaX = event.clientX - startX.value;
    edgeDetailWidth.value = startWidth.value - deltaX;
    // 可设置最小宽度限制
    if (edgeDetailWidth.value < 300) {
      edgeDetailWidth.value = 300;
    }
  }
};
const onMouseUp = () => {
  if (isResizing.value) {
    isResizing.value = false;
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
    const rect = edgeDetailRef.value.getBoundingClientRect();
    const leftBorderWidth = 10;
    // @ts-ignore
    const mouseX = event.clientX;
    if (mouseX >= rect.left && mouseX <= rect.left + leftBorderWidth) {
      edgeDetailRef.value.style.cursor = 'ew-resize';
    } else {
      edgeDetailRef.value.style.cursor = 'default';
    }
  }
};
const onMouseLeave = () => {
  edgeDetailRef.value.style.cursor = 'default';
};
async function updateEdgeConfig() {
  const currentEdge = graphWrapper.value.getCellById(currentEdgeDetail.value.edge_code);
  currentEdge.updateData({
    edge_type: currentEdgeDetail.value.edge_type,
    edge_condition_type: currentEdgeDetail.value.edge_condition_type,
    edge_conditions: currentEdgeDetail.value.edge_conditions
  });
  currentEdge.prop('labels', [currentEdgeDetail.value.edge_type]);
  const graphData = graphWrapper.value.toJSON();
  const jsonData = JSON.stringify(graphData, null, 2);
  workflowUpdate({
    app_code: currentApp.app_code,
    workflow_code: CurrentEditFlow.value.workflow_code,
    workflow_edit_schema: jsonData
  });
}
async function addEdgeCondition() {
  const currentEdge = graphWrapper.value.getCellById(currentEdgeDetail.value.edge_code);
  if (!currentEdgeDetail.value?.edge_conditions) {
    currentEdgeDetail.value.edge_conditions = [];
  }
  currentEdgeDetail.value.edge_conditions.push({
    src_node: null,
    operator: '==',
    tgt_node: null
  });
  currentEdge.updateData({
    edge_conditions: currentEdgeDetail.value.edge_conditions
  });
  const graphData = graphWrapper.value.toJSON();
  const jsonData = JSON.stringify(graphData, null, 2);
  workflowUpdate({
    app_code: currentApp.app_code,
    workflow_code: CurrentEditFlow.value.workflow_code,
    workflow_edit_schema: jsonData
  });
}
async function deleteEdgeCondition(idx: number) {
  const currentEdge = graphWrapper.value.getCellById(currentEdgeDetail.value.edge_code);
  if (currentEdgeDetail.value?.edge_conditions) {
    currentEdgeDetail.value.edge_conditions.splice(idx, 1);
    currentEdge.updateData({
      edge_conditions: currentEdgeDetail.value.edge_conditions
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
async function updateEdgeCondition(idx: number, type: string, newValue) {
  const currentEdge = graphWrapper.value.getCellById(currentEdgeDetail.value.edge_code);
  if (currentEdgeDetail.value?.edge_conditions) {
    currentEdgeDetail.value.edge_conditions[idx][type] = newValue;
    currentEdge.updateData({
      edge_conditions: currentEdgeDetail.value.edge_conditions
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
</script>

<template>
  <div
      v-show="showEdgeFlag"
      id="agent-edge-detail-box"
      ref="edgeDetailRef"
      v-loading="loadingEdgeInfo"
      element-loading-text="加载中..."
      :style="{ width: edgeDetailWidth + 'px' }"
      @mousemove="handleOverEdgeDetail"
      @mousedown="onMouseDown"
      @mouseup="onMouseUp"
      @mouseleave="onMouseLeave"
  >
    <el-scrollbar style="width: 100%">
      <div id="agent-edge-detail">
        <div id="edge-detail-head">
          <div id="edge-detail-head-top">
            <div id="edge-detail-head-left">
              <div class="std-middle-box">
                <el-image class="agent-edge-icon" :src="currentEdgeDetail?.edge_icon" />
              </div>
              <div class="std-middle-box">
                <el-text class="agent-node-name"> {{ currentEdgeDetail?.edge_name }} </el-text>
              </div>
            </div>
          </div>
          <div class="std-left-box">
            <el-text> {{ currentEdgeDetail?.edge_desc }}</el-text>
          </div>
        </div>
        <div class="config-item">
          <div v-show="currentEdgeDetail" class="config-area">
            <el-form :model="currentEdgeDetail" label-position="top" style="padding: 12px">
              <el-form-item prop="edge_type" label="关系种类">
                <el-radio-group v-model="currentEdgeDetail.edge_type" @change="updateEdgeConfig">
                  <el-radio label="充分" value="充分" />
                  <el-radio label="必要" value="必要" />
                  <el-radio label="默认" value="默认" />
                </el-radio-group>
              </el-form-item>
              <el-form-item prop="edge_condition_type" label="条件连接类型">
                <el-radio-group v-model="currentEdgeDetail.edge_condition_type" @change="updateEdgeConfig">
                  <el-radio label="or" value="or" />
                  <el-radio label="and" value="and" />
                </el-radio-group>
              </el-form-item>
              <el-form-item prop="edge_conditions" label="条件列表">
                <div class="condition-item-box">
                  <div v-for="(item, idx) in currentEdgeDetail?.edge_conditions" :key="idx" class="condition-item">
                    <div class="condition-src-item">
                      <RefSelect
                          :up-stream-nodes="currentEdgeDetail.node_upstream"
                          :ref-value="currentEdgeDetail.edge_conditions[idx].src_node"
                          @update:ref="result => updateEdgeCondition(idx, 'src_node', result)"
                      />
                    </div>
                    <div class="condition-operator-box">
                      <el-select v-model="currentEdgeDetail.edge_conditions[idx].operator" @change="updateEdgeConfig">
                        <el-option label="等于" value="==" />
                        <el-option label="不等于" value="!=" />
                        <el-option label="大于" value=">" />
                        <el-option label="小于" value="<" />
                        <el-option label="大于等于" value=">=" />
                        <el-option label="小于等于" value="<=" />
                        <el-option label="包含于(in)" value="in" />
                        <el-option label="不包含(not in)" value="not in" />
                        <el-option label="为空" value="is null" />
                        <el-option label="不为空" value="not null" />
                      </el-select>
                    </div>
                    <div
                        v-show="!['is null', 'not null'].includes(currentEdgeDetail.edge_conditions[idx]?.operator)"
                        class="condition-src-item"
                    >
                      <RefSelect
                          :up-stream-nodes="currentEdgeDetail.node_upstream"
                          :ref-value="currentEdgeDetail.edge_conditions[idx].tgt_node"
                          @update:ref="result => updateEdgeCondition(idx, 'tgt_node', result)"
                      />
                    </div>
                    <div>
                      <el-button :icon="Minus" round @click="deleteEdgeCondition(idx)" />
                    </div>
                  </div>
                </div>
                <div class="condition-add">
                  <el-button type="primary" @click="addEdgeCondition">添加条件</el-button>
                </div>
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
#agent-edge-detail-box {
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
#agent-edge-detail {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 6px;
  max-height: calc(100vh - 240px);
}
#edge-detail-head {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: center;
  justify-content: space-between;
  padding: 6px;
  border-bottom: 1px solid #f0f0f0;
}
#edge-detail-head-top {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}
#edge-detail-head-left {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: center;
}
.agent-edge-icon {
  width: 24px;
  height: 24px;
}
.config-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 6px;
  border-bottom: 1px solid #f0f0f0;
}
.condition-item-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}
.condition-item {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
}
.condition-operator-box {
  min-width: 120px;
}
.condition-add {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin-top: 12px;
  width: 100%;
}
.condition-src-item {
  width: 100%;
}
</style>
