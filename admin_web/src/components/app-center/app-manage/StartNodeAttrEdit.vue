<script setup lang="ts">
import { ArrowDown, ArrowRight, Close, QuestionFilled, Search, SuccessFilled } from '@element-plus/icons-vue';
import { nextTick, ref } from 'vue';
import { nodeUpdate } from '@/api/app-center-api';
import TemplateEditor from '@/components/app-center/app-manage/TemplateEditor.vue';


import { useAppStore } from '@/stores/app-store';
import { useWorkflowStore } from '@/stores/workflow-store';
const appInfoStore = useAppStore();
const workflowStore = useWorkflowStore();
const showModeFlag = ref(false);
async function handleStartNodeChange() {
  nodeUpdate({
    app_code: appInfoStore.currentApp.app_code,
    node_code: workflowStore.currentNodeDetail.node_code,
    node_run_model_config: workflowStore.currentNodeDetail.node_run_model_config
  });
}
</script>

<template>
  <div v-if="workflowStore.currentNodeDetail?.node_type == 'start'" class="config-item">
    <div class="config-head">
      <div class="std-middle-box">
        <el-icon v-if="showModeFlag" class="config-arrow" @click="showModeFlag = false">
          <ArrowDown />
        </el-icon>
        <el-icon v-else class="config-arrow" @click="showModeFlag = true">
          <ArrowRight />
        </el-icon>
      </div>
      <div class="std-middle-box">
        <el-text> 工作流模式 </el-text>
      </div>
      <div>
        <el-tooltip content="配置交互型，任务型等参数">
          <el-icon>
            <QuestionFilled />
          </el-icon>
        </el-tooltip>
      </div>
    </div>
    <div v-show="showModeFlag" class="config-area">
      <div>
        <el-form label-position="top" :model="workflowStore.currentNodeDetail">
          <el-form-item label="跳过用户问题" style="padding: 0 12px">
            <el-switch
              v-model="workflowStore.currentNodeDetail.node_run_model_config.skip_user_question"
              @change="handleStartNodeChange"
            />
          </el-form-item>
        </el-form>
      </div>
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
