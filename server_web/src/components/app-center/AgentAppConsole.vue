<script setup lang="ts">
import {onMounted} from 'vue';
import {
  get_running_progress,
  running_questions,
  user_batch_size,
} from "@/components/next-console/messages-flow/console_input";
import {
  llm_instance_queue,
  search_llm_instance,
} from "@/components/next-console/messages-flow/llm_instance";
import {
  askAgentQuestion,
  audioUrl,
  consoleInput,
  consoleInputInnerRef,
  consoleInputRef,
  handleInputChange,
  handleKeyDown,
  isRecording,
  startRecording,
  stop_agent_question,
  stopRecording,
  userComposition,
  modelListRef,
  switchLlmInstance, getSessionLlmName
} from "@/components/app-center/ts/agent_console";
import {CurrentAgentAppSession} from "@/components/app-center/ts/agent-app";
import {Microphone, VideoPause} from "@element-plus/icons-vue";


onMounted(async () => {
  if (window.innerWidth >= 768){
    consoleInputInnerRef.value.focus()
  }
  // 获取模型列表
  search_llm_instance()


})

</script>

<template>
  <div id="console-input">

    <div id="console-input-box" ref="consoleInputRef">

      <div id="console-input-box-inner">

        <div id="console-input-box-inner-body">
          <div id="input-text-box">
            <el-input placeholder="请输入您想咨询的问题"
                      type="textarea"
                      ref="consoleInputInnerRef"
                      v-model="consoleInput"
                      resize="none"
                      :autosize="{minRows: 3, maxRows: 10}"
                      @keydown.enter.prevent
                      @keydown="handleKeyDown"
                      @compositionend="userComposition=false"
                      @compositionstart="userComposition=true"
                      @input="handleInputChange"
                      input-style="box-shadow: none; border-radius: 8px; border: none;"
                      class="msg-input-textarea"
            />
          </div>

          <div class="input-button" v-if="user_batch_size == 1"
               @click="stop_agent_question()"
               style="background-color: red">
            <el-image src="/images/pause_white.svg" class="input-icon"/>
          </div>
          <el-popover v-else-if="user_batch_size > 1" trigger="hover" width="300px">
            <template #reference>
              <el-badge :value="user_batch_size">
                <div class="input-button" style="background-color: red">
                  <el-image src="/images/pause_white.svg" class="input-icon"/>
                </div>
              </el-badge>
            </template>
            <div v-for="running_question in running_questions" class="running_question_item_box">
              <div class="running-question-idx-box">
                <el-text truncated>
                  第{{ running_question.qa_item_idx + 1 }}个问题
                </el-text>
              </div>
              <div class="running-question-word-cnt-box">
                <el-text>
                  已经输出{{ get_running_progress(running_question) }}个字
                </el-text>
              </div>
              <div class="running-question-stop-button">

                <el-image src="/images/close_red.svg"
                          @click="stop_agent_question(running_question)"/>

              </div>
            </div>
          </el-popover>
          <div class="input-button" v-else @click="askAgentQuestion()">
            <el-image src="/images/send_blue.svg" class="input-icon"/>
          </div>
          <div class="input-button"
               @mousedown.prevent="startRecording(1)"
               @mouseup="stopRecording(2)"
               @touchstart.prevent="startRecording(3)"
               @touchend="stopRecording(4)"
               >
            <div class="recording-box" v-show="isRecording">
              <div class="wave"></div>
              <div class="wave"></div>
              <div class="wave"></div>
            </div>
            <el-tooltip content="语音输入" placement="top" >
              <el-icon class="audio-input-icon" >
                <Microphone class="audio-input-icon"  v-show="!isRecording" />
                <VideoPause class="audio-input-icon" style="color: #c45656" v-show="isRecording" />
              </el-icon>
            </el-tooltip>

          </div>

        </div>
      </div>
    </div>
    <div id="input-tips">
      <div class="std-middle-box">
        <el-text class="msg-tips-text">
          以上内容均由AI生成式模型
        </el-text>
        <el-text class="msg-tips-text">
          {{ getSessionLlmName() || 'DeepSeek-V3' }}
        </el-text>
        <el-popover trigger="click" width="280px" ref="modelListRef">
          <template #reference>
            <div class="std-middle-box">
              <el-image src="/images/arrow_down_grey.svg" class="model-select-icon"/>
            </div>

          </template>
          <el-scrollbar>
            <div class="llm-instance-area">

              <div v-for="(item,idx) in llm_instance_queue" class="llm-instance-item"
                   :class="{
              'llm-instance-item-active': item.llm_code == CurrentAgentAppSession?.session_llm_code
                 }"
                   @click="switchLlmInstance(item)"
              >
                <div class="std-middle-box">
                  <el-avatar :src="item.llm_icon" style="width: 20px;height: 20px;background-color: white"
                             fit="contain"/>
                </div>
                <div class="std-middle-box" style="justify-content: flex-start">
                  <el-text truncated style="font-size: 14px;font-weight: 500;line-height: 20px;color: #344054">
                    {{ item.llm_label }}
                  </el-text>
                </div>
              </div>


            </div>
          </el-scrollbar>
        </el-popover>
        <el-text class="msg-tips-text">
          生成，仅供参考
        </el-text>
      </div>


    </div>
  </div>


</template>

<style scoped>

.msg-input-textarea :deep(.el-textarea__inner::-webkit-scrollbar) {
  width: 4px;
  height: 6px;
}

.msg-input-textarea :deep(.el-textarea__inner::-webkit-scrollbar-thumb) {
  border-radius: 3px;
  -moz-border-radius: 3px;
  -webkit-border-radius: 3px;
  background-color: #c3c3c3;
}

.msg-input-textarea :deep(.el-textarea__inner::-webkit-scrollbar-track) {
  background-color: transparent;
}

#console-input {
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 100%;
}

#console-input-box {
  width: 100%;
  max-width: 900px;
  display: flex;
  flex-direction: row;
  gap: 4px;
  box-shadow: 0 1px 2px 0 #1018280D;
  border-radius: 24px;
  padding: 4px;
  background-color: #f3f4f6;
  position: relative;
}

#console-input-box-inner {
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  border: 1px solid #D0D5DD;
  background-color: white;
  box-shadow: 0 1px 2px 0 #1018280D;
  gap: 4px;
  width: 100%;
  align-items: center;

}

#console-input-box-inner-body {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px;
  width: calc(100% - 24px);
}

.input-button {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 4px;
}

.input-button:hover {
  background-color: #F3F4F6;
}

.input-button:active {
  transform: scale(0.95);
}

#input-text-box {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.input-icon {
  width: 32px;
  height: 32px;
}
.audio-input-icon{
  width: 42px;
  height: 42px;
}
.msg-tips-text {
  font-size: 12px;
  line-height: 18px;
  font-weight: 400;
  color: #475467;
}

.running_question_item_box {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-bottom: 1px solid #D0D5DD;
}

.running-question-idx-box {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  background-color: #F3F4F6;
  padding: 4px;
}

.running-question-word-cnt-box {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  background-color: #F3F4F6;
  padding: 4px;
}

.running-question-stop-button {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 4px;
  background-color: #F3F4F6;
  padding: 4px;
  width: 24px;
  height: 24px;
}

.running-question-stop-button:hover {
  background-color: #F3F4F6;
}

.running-question-stop-button:active {
  transform: scale(0.95);
}

#input-tips {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 8px;
  border-radius: 8px;
  gap: 4px;
  height: 20px;
}

.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
}

#console-input-buttons {
  position: absolute;
  left: 20px;
  top: -30px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
}

.console-button-icon {
  width: 12px;
  height: 12px;
}

.console-button-text {
  font-weight: 500;
  font-size: 12px;
  line-height: 18px;
  color: #344054;
}

.console-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: #FFFFFF;
  gap: 4px;
  border: 1px solid #D0D5DD;

}

.console-button:hover {
  background-color: #EFF8FF;
  border: 1px solid #2E90FA;
  cursor: pointer;

}

#console-input-box-inner-head {
  width: 100%;
}

#ai_search {
  display: flex;
  flex-direction: column;
  max-height: 90px;
  width: 100%;
}

#ai_search_head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  width: calc(100% - 32px);
  height: 20px;
  background: #F5F5F4;
  border-radius: 20px 20px 0 0;
}

#ai_search_head_left {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
}

#ai_search_head_right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;

}

.console-button-text2 {
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  color: #344054;
}

#ai_search_body {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 0 16px;
  padding: 8px 0;
  gap: 10px;
  border-bottom: 1px solid #D0D5DD;
}

.search-research-type {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  border-radius: 6px;
  background-color: #f9f9f9;
  cursor: pointer;

}

.search-research-type-active {
  background-color: #EFF8FF;
  border: 1px solid #2E90FA;
}

.search-research-type-text {
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  color: #344054;

}

.search-research-type-text-active {

  color: #175CD3;
}

.console-button-active {
  border: none;
  background-color: #EFF8FF;
}

.console-button-text-active {
  color: #175CD3;
}

#ai_image_body {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin: 0 16px;
  padding: 8px 0;
  gap: 10px;
  border-bottom: 1px solid #D0D5DD;
}

#ai_image_head_right {
  max-width: 200px;
  display: flex;
  flex-direction: row;
  gap: 8px;
}

#ai_image_body_left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;

}

#ai_image_body_left_bg {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  padding: 6px 8px;
  border-radius: 8px;
  background: #EFF8FF;
}

.ai_image_item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 6px;
  border-radius: 6px;
  cursor: pointer;
  background: #FFFFFF;
  margin-bottom: 6px;
}

.llm-instance-area {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 200px;

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
  background: #FFFFFF
}

.llm-instance-item:hover {
  background: #EFF8FF;
}

.llm-instance-item-active {
  background: #EFF8FF;
}

#upload-box {
  position: fixed;
  bottom: 250px;
  right: 380px;
  max-width: 200px;
  z-index: 99;
}

.ai_file_item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  padding: 2px 6px;
  border-radius: 6px;
  background-color: #FFFFFF;
  border: 1px solid #D0D5DD;
  box-shadow: 0 1px 2px 0 #1018280D;
  margin-bottom: 6px;
}

#ai_file_body_left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;

}

#ai_file_body_left_bg {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  padding: 6px 8px;
  border-radius: 8px;
  background: #EFF8FF;
}

.highlight-resource-keyword {
  background: yellow;
}

.msg-ticket-text {
  font-size: 12px;
  line-height: 18px;
  font-weight: 400;
  color: #475467;
  cursor: pointer;
}

.msg-ticket-text:hover {
  color: #175CD3;
}
.model-select-icon{
  width: 16px;
  height: 16px;
  cursor: pointer;
}
.rag-icon{
  width: 20px;
  height: 20px;
}
/* 录音盒子样式 */
.recording-box {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  z-index: 2;
}

/* 波纹样式 */
.wave {
  position: absolute;
  width: 40px;
  height: 40px;
  border: 2px solid rgba(0, 123, 255, 0.7);
  border-radius: 50%;
  opacity: 0;
  animation: wave-animation 1.5s linear infinite;
}

/* 第二个波纹延迟动画 */
.wave:nth-child(2) {
  animation-delay: 0.5s;
}

/* 第三个波纹延迟动画 */
.wave:nth-child(3) {
  animation-delay: 1s;
}

/* 波纹动画关键帧 */
@keyframes wave-animation {
  0% {
    transform: scale(0.2);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}
@media (width < 768px) {
  .console-button-text{
    visibility: hidden;
    width: 0;
    height: 24px;
  }
  .msg-tips-text{
    font-size: 8px;
    line-height: 14px;
  }
  #console-input-buttons{
    top: -34px
  }
  .console-button{
    gap: 0;
    padding: 2px 6px;
  }
  .rag-icon{
    width: 14px;
    height: 14px;
  }
  .console-button-text2{
    font-size: 12px;
    line-height: 16px;
  }
  .model-select-icon{
    width: 12px;
    height: 12px;
  }
  .el-divider--vertical{
    margin: 0;
  }
  #input-tips{
    padding: 2px;
  }
  #console-input-box-inner-body{
    padding: 0;
  }
  #upload-box {
    position: fixed;
    bottom: 250px;
    left: 60px;
    max-width: 200px;
    z-index: 99;
  }
}
</style>
