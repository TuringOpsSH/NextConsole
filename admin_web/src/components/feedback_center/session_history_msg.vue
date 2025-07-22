<script setup lang="ts">
import 'highlight.js/styles/monokai.css';
import { ElMessage } from 'element-plus';
import { nextTick } from 'vue';
import { admin_add_like } from '@/api/feedback_center';
import { showMsgTraceDialog } from '@/components/feedback_center/message_log';
import MsgTrace from '@/components/feedback_center/msg_trace.vue';
import { showPromptTestDialog } from '@/components/feedback_center/prompt_test';
import {
  addSessionTag,
  copy_text,
  handle_tag_close,
  handleSessionTagInputConfirm,
  InputSessionTagRef,
  inputSessionTagValue,
  inputSessionTagVisible,
  loadingSessionHistoryMsg,
  SessionHistoryMsgList,
  targetSession,
  version_turn_left,
  version_turn_right
} from '@/components/feedback_center/session_log';
import { msg_queue_item } from '@/types/next_console';
import { compiledMarkdown } from '@/utils/markdown';
function showSessionTagInput() {
  try {
    if (targetSession.value.tag_list.length >= 8) {
      ElMessage.warning({
        message: '最多添加8个标签',
        type: 'warning',
        duration: 600
      });
      return;
    }
  } catch (e) {}

  inputSessionTagVisible.value = true;
  nextTick(() => {
    InputSessionTagRef.value!.focus();
  });
}
async function adminAddLike(qa: msg_queue_item) {
  let question_id = qa.qa_value.question[0].msg_id;
  let answer_id = qa.qa_value.answer[question_id][0].msg_id;
  if (answer_id === 0) {
    ElMessage.info({
      message: '请过会儿点击，感谢您的支持！',
      duration: 1000
    });

    return false;
  }
  let params = {
    msg_id: qa.qa_value.answer[question_id][0].msg_id,
    admin_msg_remark: 1
  };
  let res = await admin_add_like(params);
  if (!res.error_status) {
    ElMessage.success('操作成功');
    qa.qa_value.answer[question_id][0].msg_remark = 1;
  }
}
async function adminAddDislike(qa: msg_queue_item) {
  let question_id = qa.qa_value.question[0].msg_id;
  let answer_id = qa.qa_value.answer[question_id][0].msg_id;
  if (answer_id === 0) {
    ElMessage.info({
      message: '请过会儿点击，感谢您的支持！',
      duration: 1000
    });
    return false;
  }
  let params = {
    msg_id: qa.qa_value.answer[question_id][0].msg_id,
    admin_msg_remark: -1
  };
  let res = await admin_add_like(params);
  if (!res.error_status) {
    ElMessage.success('操作成功');
    qa.qa_value.answer[question_id][0].msg_remark = -1;
  }
}
</script>

<template>
  <el-container style="height: calc(100vh - 240px)">
    <el-main>
      <el-scrollbar
        v-loading="loadingSessionHistoryMsg"
        element-loading-text="加载中..."
        wrap-class="width:100%"
        view-class="width:100%"
      >
        <div v-for="(item, index) in SessionHistoryMsgList" class="msg-item-box">
          <div class="msg-item">
            <div v-if="item.qa_value.question.length > 0" class="msg-sub-item">
              <div class="msg-item-right">
                <div class="sub-button">
                  <div class="send-time">
                    <el-text class="send-time-text">
                      {{ item.qa_value.question[0].create_time }}
                    </el-text>
                  </div>
                  <div class="msg-update">
                    <div v-if="item.qa_value.question.length > 1" class="msg-update-button-version">
                      <el-row>
                        <el-col :span="8" class="version-text-box">
                          <el-button class="version-arrow" @click="version_turn_left(item, 1)">
                            <el-image src="images/version_left.svg" class="version-change-icon" />
                          </el-button>
                        </el-col>
                        <el-col :span="8" class="version-text-box">
                          <el-text class="version-text">
                            {{ item.qa_value.question[0].msg_version + 1 }}/
                            {{ item.qa_value.question.length }}
                          </el-text>
                        </el-col>
                        <el-col :span="8" class="version-text-box">
                          <el-button class="version-arrow" @click="version_turn_right(item, 1)">
                            <el-image src="images/version_right.svg" class="version-change-icon" />
                          </el-button>
                        </el-col>
                      </el-row>
                    </div>
                    <el-button-group>
                      <el-button class="msg-update-button" @click="copy_text(item.qa_value.question[0].msg_content)">
                        <el-image src="images/copy.svg" class="msg-update-button-icon" />
                      </el-button>
                      <el-button class="msg-update-button" @click="showMsgTraceDialog(item.qa_value.question[0])">
                        <el-image
                          src="images/icon_circle_grey.svg"
                          style="width: 16px; height: 16px"
                          class="msg-update-button-icon"
                        />
                      </el-button>
                      <el-button class="msg-update-button" @click="showPromptTestDialog(item.qa_value.question[0])">
                        <el-image
                          src="images/target_04.svg"
                          style="width: 16px; height: 16px"
                          class="msg-update-button-icon"
                        />
                      </el-button>
                    </el-button-group>
                  </div>
                </div>
                <div class="msg-content" :style="{ backgroundColor: '#d1E9ff' }">
                  <div
                    id="{{item.qa_value.question[0].msg_id}}"
                    class="assistant-answer"
                    v-html="compiledMarkdown(item.qa_value.question[0].msg_content, 1)"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          <div
            v-if="
              item.qa_value.question[0].msg_id in item.qa_value.answer &&
              item.qa_value.answer[item.qa_value.question[0].msg_id].length > 0
            "
            class="msg-sub-item"
          >
            <div class="msg-item-right">
              <div class="sub-button">
                <div class="send-time">
                  <el-text class="send-time-text">
                    {{ item.qa_value.answer[item.qa_value.question[0].msg_id][0].create_time }}
                  </el-text>
                </div>
                <div class="msg-update">
                  <div
                    v-if="item.qa_value.answer[item.qa_value.question[0].msg_id].length > 1"
                    class="msg-update-button-version"
                  >
                    <el-row>
                      <el-col :span="8" class="version-text-box">
                        <el-button class="version-arrow" @click="version_turn_left(item, 2)">
                          <el-image src="images/version_left.svg" class="version-change-icon" />
                        </el-button>
                      </el-col>
                      <el-col :span="8" class="version-text-box">
                        <el-text class="version-text">
                          {{ item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_version + 1 }}/
                          {{ item.qa_value.answer[item.qa_value.question[0].msg_id].length }}
                        </el-text>
                      </el-col>
                      <el-col :span="8" class="version-text-box">
                        <el-button class="version-arrow" @click="version_turn_right(item, 2)">
                          <el-image src="images/version_right.svg" class="version-change-icon" />
                        </el-button>
                      </el-col>
                    </el-row>
                  </div>

                  <el-button-group style="min-width: 60px">
                    <el-button
                      class="msg-update-button"
                      @click="copy_text(item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_content)"
                    >
                      <el-image src="images/copy.svg" class="msg-update-button-icon" />
                    </el-button>

                    <el-button
                      class="msg-update-button"
                      @click="showMsgTraceDialog(item.qa_value.answer[item.qa_value.question[0].msg_id][0])"
                    >
                      <el-image
                        src="images/icon_circle_grey.svg"
                        style="width: 16px; height: 16px"
                        class="msg-update-button-icon"
                      />
                    </el-button>

                    <el-button class="msg-update-button" @click="adminAddLike(item)">
                      <el-image
                        v-if="item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_remark != 1"
                        src="images/add_like.svg"
                        class="msg-update-button-icon"
                      />
                      <el-image
                        v-if="item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_remark == 1"
                        src="images/add_like_click.svg"
                        class="msg-update-button-icon"
                      />
                    </el-button>
                    <el-button class="msg-update-button" @click="adminAddDislike(item)">
                      <el-image
                        v-if="item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_remark != -1"
                        src="images/add_dislike.svg"
                        class="msg-update-button-icon"
                      />
                      <el-image
                        v-if="item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_remark == -1"
                        src="images/add_dislike_click.svg"
                        class="msg-update-button-icon"
                      />
                    </el-button>
                  </el-button-group>
                </div>
              </div>

              <div class="msg-content" :style="{ backgroundColor: '#F2F4F7' }">
                <div
                  id="answer-markdown"
                  class="assistant-answer"
                  v-html="compiledMarkdown(item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_content, 2)"
                ></div>
              </div>
            </div>
          </div>
        </div>
        <MsgTrace />
      </el-scrollbar>
    </el-main>
    <el-footer>
      <div>
        <div class="kg-add-tags-value">
          <el-tag
            v-for="tag in targetSession.tag_list"
            :key="tag"
            :closable="true"
            :disable-transitions="false"
            style="margin: 2px"
            @close="handle_tag_close(tag)"
          >
            {{ tag }}
          </el-tag>
          <el-input
            v-if="inputSessionTagVisible"
            ref="InputSessionTagRef"
            v-model="inputSessionTagValue"
            style="width: 100px; height: 20px; margin-top: 8px"
            size="small"
            @keyup.enter="handleSessionTagInputConfirm"
            @blur="handleSessionTagInputConfirm"
          />
          <el-button v-else class="button-new-tag" size="small" style="margin-top: 8px" @click="showSessionTagInput">
            + 新标签
          </el-button>
        </div>
        <div style="width: 100%; margin: 20px 0">
          <el-button
            style="width: 100%; background-color: #1570ef; border: 1px solid #1570ef; border-radius: 8px"
            @click="addSessionTag"
          >
            <el-text style="font-size: 16px; font-weight: 600; line-height: 24px; text-align: left; color: #ffffff">
              确认
            </el-text>
          </el-button>
        </div>
      </div>
    </el-footer>
  </el-container>
</template>

<style scoped>
.assistant-answer {
  width: 100%;
  overflow: auto;
}

:deep(.hljs) {
  font-size: 14px !important;
  line-height: 21px !important;
}
:deep(code) {
  max-width: 751px;
  padding: 3px 5px;
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
.kg-add-tags-value {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 2px;
  border: 1px solid #d0d5dd;
  box-shadow: 0 1px 2px 0 #1018280d;
  height: 120px;
  border-radius: 8px;
  padding: 12px;
  width: calc(100% - 24px);
}
.sub-button {
  width: 100%;
  height: 24px;
  display: flex;
  justify-content: space-between; /* 元素在两边 */
  margin: 4px 0 4px 0 !important;
}
.send-time {
  min-width: 130px;
  height: 100%;
  display: flex;
  align-items: center;
}
.send-time-text {
  font-size: 12px;
  font-weight: 400;
  line-height: 18px;
  color: #475467;
}
.msg-update {
  min-width: 60px;
  display: flex;
  justify-content: right;
}
.msg-update-button {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  padding: 2px;
  gap: 8px;
  border: 0;
}
.msg-update-button-version {
  min-width: 80px;
  height: 24px;
  border-radius: 4px;
  padding: 2px;
  gap: 8px;
  border: 0;
  display: flex;
  justify-content: right;
  align-content: center;
}
.msg-update-button-icon {
  width: 20px;
  height: 20px;
}
.version-arrow {
  width: 16px;
  height: 16px;
  border: 0;
}
.version-change-icon {
  width: 16px;
  height: 16px;
}
.version-text-box {
  display: flex;
  justify-content: center;
}
.version-text {
  font-size: 12px;
  font-weight: 500;
  line-height: 18px;
  color: #101828;
  display: flex;
  justify-content: center;
  align-self: auto;
}
</style>
