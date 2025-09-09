<script setup lang="ts">
import { VideoPlay, VideoPause, MoreFilled } from '@element-plus/icons-vue';
import { inject, ref, onMounted } from 'vue';
const getNode = inject('getNode') as () => any;
const nodeData = ref<IAgentNode>({
  nodeInput: '',
  nodeOutput: '',
  nodeModel: '',
  nodeIcon: '',
  nodeName: '',
  nodeType: '',
  nodeDesc: '',
  nodeStatus: '',
  nodeCode: ''
});
let node = null;
onMounted(() => {
  node = getNode();
  nodeData.value = node.data;
  node.on('change:data', ({ current }) => {
    nodeData.value = current;
  });
});
import { keyboardDeleteNode, selectedNodes } from '@/components/app-center/ts/workflow-edit';
import { IAgentNode } from '@/types/appCenterType';
function SingleDeleteNode(node) {
  selectedNodes.value.push(node);
  keyboardDeleteNode();
}
</script>

<template>
  <div class="agent-node" :class="selectedNodes.includes(node) ? 'agent-node-selected' : ''">
    <div class="agent-head">
      <div class="agent-head-left">
        <div class="std-middle-box">
          <img class="agent-node-icon" :src="nodeData?.nodeIcon" />
        </div>
        <div class="std-middle-box">
          <el-text class="agent-node-name">
            {{ nodeData?.nodeName }}
          </el-text>
        </div>
      </div>
      <div class="agent-head-right">
        <div class="std-middle-box">
          <el-tooltip content="测试运行" effect="light" placement="top">
            <VideoPause v-if="nodeData?.nodeStatus == '运行中'" class="agent-node-svg" style="" />
            <VideoPlay v-else class="agent-node-svg" />
          </el-tooltip>
        </div>
        <div class="std-middle-box">
          <el-dropdown>
            <MoreFilled class="agent-node-svg" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item divided disabled>创建副本</el-dropdown-item>
                <el-dropdown-item divided @click="SingleDeleteNode(node)">删除</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>
    <div class="agent-body">
      <div class="agent-body-row">
        <div class="std-middle-box">
          <el-text class="agent-body-row-name"> 输入 </el-text>
        </div>
        <div v-if="nodeData?.nodeParams?.length > 0" class="params-tag-area">
          <el-tag v-for="param in nodeData.nodeParams" :key="param">
            {{ param }}
          </el-tag>
        </div>
        <div v-else class="std-middle-box">
          <el-text>{{ nodeData?.nodeInput }}</el-text>
        </div>
      </div>
      <div class="agent-body-row">
        <div class="agent-body-row-name">
          <el-text> 输出 </el-text>
        </div>
        <div v-if="nodeData?.nodeResultParams?.length > 0" class="params-tag-area">
          <el-tag v-for="param in nodeData.nodeResultParams" :key="param">
            {{ param }}
          </el-tag>
        </div>
        <div v-else>
          <el-text>{{ nodeData?.nodeOutput }}</el-text>
        </div>
      </div>
      <div v-if="nodeData?.nodeType == 'llm'" class="agent-body-row">
        <div class="agent-body-row-name">
          <el-text> 模型 </el-text>
        </div>
        <div>
          <el-text>{{ nodeData?.nodeModel }}</el-text>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: center;
}
.agent-node {
  background-color: white;
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  padding: 4px;
  box-shadow:
    0 4px 8px rgba(0, 0, 0, 0.1),
    0 6px 20px rgba(0, 0, 0, 0.1); /* 阴影效果 */
}
.agent-node-selected {
  border: 1px solid #409eff;
}
.agent-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}
.agent-head-left {
  display: flex;
  flex-direction: row;
  gap: 12px;
  padding: 6px;
}
.agent-head-right {
  display: flex;
  flex-direction: row;
}

.agent-node-name {
  font-size: 16px;
}
.agent-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 6px;
}

.agent-node-icon {
  width: 24px;
  height: 24px;
}
.agent-body-row {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 12px;
}
.agent-body-row-name {
  font-size: 14px;
  font-weight: bold;
}
.params-tag-area {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 4px;
}
.agent-node-svg {
  width: 1em;
  height: 1em;
  margin-right: 8px;
  cursor: pointer;
  &:focus {
    outline: none !important;
  }
}
</style>
