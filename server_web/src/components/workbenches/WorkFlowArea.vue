<script setup lang="ts">
import { Picture as IconPicture } from '@element-plus/icons-vue';
import { onMounted, ref, watch } from 'vue';
import SimpleProgress from './SimpleProgress.vue';
import { workflow_task_item } from '@/types/next_console';
const props = defineProps({
  workflowTask: {
    type: Array as () => workflow_task_item[],
    default: () => []
  },
  qaWorkflowOpen: {
    type: Boolean,
    default: false
  },
  qaFinished: {
    type: Boolean,
    default: false
  }
});
const localQaWorkflowOpen = ref(false);
const localQaFinished = ref(false);
const workflowTask = ref<workflow_task_item[]>([]);
onMounted(() => {
  localQaWorkflowOpen.value = props.qaWorkflowOpen;
  localQaFinished.value = props.qaFinished;
  workflowTask.value = props.workflowTask;
});
watch(
    () => props.workflowTask,
    newVal => {
      workflowTask.value = newVal;
    }
);
watch(
    () => props.qaFinished,
    newVal => {
      localQaFinished.value = newVal;
    }
);
watch(
    () => props.qaWorkflowOpen,
    newVal => {
      localQaWorkflowOpen.value = newVal;
    }
)
</script>

<template>
  <div v-if="workflowTask?.length" class="msg-flow-workflow-box">
    <div v-show="localQaWorkflowOpen" class="open-workflow-area">
      <div class="open-workflow-head">
        <div class="open-workflow-head-left">
          <div class="std-middle-box">
            <el-text style="min-width: 60px">工作流</el-text>
          </div>
          <SimpleProgress v-if="!localQaFinished" />
        </div>
        <div class="open-workflow-head-right">
          <div class="std-middle-box">
            <el-image
                src="images/arrow_up_grey2.svg"
                style="width: 20px; height: 20px; cursor: pointer"
                @click="localQaWorkflowOpen = false"
            />
          </div>
        </div>
      </div>
      <el-scrollbar>
        <div class="open-workflow-list">
          <div v-for="sub_workflow in workflowTask" class="sub-workflow-area">
            <div class="sub-workflow-head">
              <div class="std-middle-box">
                <el-image
                    v-show="sub_workflow.task_status != 'finished'"
                    src="images/task_status.svg"
                    style="width: 16px; height: 16px"
                />
                <el-image
                    v-show="sub_workflow.task_status == 'finished'"
                    src="images/task_status_ok.svg"
                    style="width: 16px; height: 16px"
                />
              </div>
              <div class="std-middle-box">
                <el-text>{{ sub_workflow.task_type }}</el-text>
              </div>
            </div>
            <div v-if="sub_workflow.task_type == '资料检索'" class="sub-workflow-show-info">
              <el-text truncated style="max-width: 100%">
                {{ sub_workflow.task_params?.user_params?.query_text }}
              </el-text>
            </div>
            <div
                v-for="(img_item, idx) in sub_workflow?.task_params"
                v-else-if="sub_workflow.task_type == '网页解析'"
                class="sub-workflow-show-info"
            >
              <div class="std-middle-box">
                <el-image
                    fit="cover"
                    :zoom-rate="1.2"
                    :max-scale="7"
                    :min-scale="0.2"
                    :preview-src-list="[img_item?.resource_show_url]"
                    :initial-index="0"
                    :alt="img_item?.resource_source_url"
                    :src="img_item?.resource_show_url"
                    style="width: 24px; height: 24px"
                >
                  <template #error>
                    <el-icon><IconPicture /></el-icon>
                  </template>
                </el-image>
              </div>
            </div>
            <div
                v-for="(img_item, idx) in sub_workflow?.task_params"
                v-else-if="sub_workflow.task_type == '图像识别'"
                class="sub-workflow-show-info"
            >
              <div class="std-middle-box">
                <el-image
                    fit="cover"
                    :zoom-rate="1.2"
                    :max-scale="7"
                    :min-scale="0.2"
                    :preview-src-list="sub_workflow?.task_params"
                    :initial-index="0"
                    :src="img_item"
                    style="width: 24px; height: 24px"
                >
                  <template #error>
                    <el-icon><IconPicture /></el-icon>
                  </template>
                </el-image>
              </div>
            </div>
            <div v-else-if="sub_workflow.task_type == '会话命名'" class="sub-workflow-show-info">
              <el-text truncated style="max-width: 100%">
                {{ sub_workflow.task_result }}
              </el-text>
            </div>
            <div v-else class="sub-workflow-show-info">
              <el-text truncated style="max-width: 100%">
                {{ sub_workflow.task_result }}
              </el-text>
            </div>
          </div>
        </div>
      </el-scrollbar>
    </div>
    <div v-show="!localQaWorkflowOpen" class="close-workflow-area">
      <div class="close-workflow-area-left">
        <div class="std-middle-box">
          <el-image v-show="localQaFinished" src="images/ok_green.svg" style="width: 20px; height: 20px" />
          <el-image v-show="!localQaFinished" src="images/ok_grey.svg" style="width: 20px; height: 20px" />
        </div>
        <div class="std-middle-box" style="width: 60px">
          <el-text style="font-weight: 500; font-size: 14px; line-height: 20px; color: #101828; min-width: 60px">
            工作流
          </el-text>
        </div>
        <SimpleProgress v-show="!localQaFinished" />
      </div>
      <div class="close-workflow-area-right">
        <div class="std-middle-box">
          <el-image
              src="images/arrow_down_grey2.svg"
              style="width: 20px; height: 20px; cursor: pointer"
              @click="localQaWorkflowOpen = true"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
:deep(.hljs) {
  font-size: 14px !important;
  line-height: 21px !important;
}
:deep(code) {
  max-width: 751px;
  margin: 3px 5px;
  border-radius: 6px;
  font-size: 14px !important;
  line-height: 21px !important;
  white-space: pre-wrap;
  overflow: auto;
}
:deep(code:not([class])) {
  background: rgba(0, 0, 0, 0.06);
}
:deep(pre:not([class])) {
  background: rgba(0, 0, 0, 0.06);
  overflow: auto;
  white-space: pre-wrap;
}
:deep(pre:not([class]) code:not([class])) {
  background: transparent;
}
sup {
  border-radius: 4px;
  background: #f9f9f9 !important;
  /* 添加其他样式属性 */
}

.std-middle-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.msg-flow-workflow-box {
  width: 100%;
}
.open-workflow-head-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.close-workflow-area {
  min-width: 144px;
  padding: 6px 12px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #f2f4f7;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.close-workflow-area-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
}
.open-workflow-area {
  border: 1px solid #d0d5dd;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  width: calc(100% - 24px);
  max-height: 160px;
  overflow: hidden;
}
.open-workflow-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.sub-workflow-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.sub-workflow-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  min-width: 80px;
}
.sub-workflow-show-info {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  padding: 4px 8px;
  background-color: #f9f9fb;
  gap: 16px;
  max-width: calc(100% - 16px);
}
.open-workflow-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 120px;
}
@media (width<768px) {
  #message-flow-box {
    gap: 0;
  }
  .msg-flow-qa-box {
    padding: 8px 0;
    gap: 8px;
  }
  .msg-flow-question-box {
    gap: 4px;
  }
  .question-button-icon {
    width: 14px;
    height: 14px;
  }
  .msg-flow-question-content {
    max-width: calc(100% - 72px);
  }
  .question-content-text {
    font-size: 14px;
    line-height: 20px;
  }
  .msg-flow-answer-button-area {
    top: -10px;
    left: 0;
    width: 100%;
  }
  .msg-flow-answer-button-icon {
    width: 14px;
    height: 14px;
  }
  .msg-flow-answer-box {
    gap: 4px;
  }
  .msg-flow-answer-content {
    width: calc(100% - 50px);
    padding: 0;
  }
  :deep(.hljs) {
    font-size: 14px !important;
    line-height: 20px !important;
  }
  :deep(p) {
    font-size: 14px !important;
    line-height: 20px !important;
  }
  :deep(li) {
    font-size: 14px !important;
    line-height: 20px !important;
  }
  .open-workflow-area {
    gap: 6px;
    padding: 8px;
  }
  .sub-workflow-area {
    overflow: scroll;
  }
  .msg-check-box {
    position: absolute;
    left: -12px;
  }
  #choose-model-area {
    padding: 8px;
    gap: 6px;
  }
}
</style>
