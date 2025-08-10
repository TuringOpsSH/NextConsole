<script setup lang="ts">
import { ref } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import ConsoleInput from '@/components/next_console/messages_flow/ConsoleInput.vue';
import MessageFlowV2 from '@/components/next_console/messages_flow/MessageFlowV2.vue';
import { consoleInputRef } from '@/components/next_console/messages_flow/console_input';
import { msgFlowRef } from '@/components/next_console/messages_flow/message_flow';
import { close_upload_manager } from '@/components/resource/resource_upload/resource_upload';
import router from '@/router';
const props = defineProps({
  sessionCode: {
    type: String,
    default: '',
    required: false
  }
});
const showScrollbarButton = ref(window.innerWidth >= 768);
const consoleInputHeight = ref(150);
const chooseModel = ref(false);
const chooseMsgCnt = ref(0);
const chooseMsgAll = ref(false);
const chooseMsgMiddle = ref(false);
function turnOffMsgChooseModel() {
  // 关闭消息流选择模式
  msgFlowRef.value?.turnOffMsgChooseModel();
  chooseModel.value = false;
  chooseMsgCnt.value = 0;
}

async function handleMsgFlowReady() {
  if (router.currentRoute.value.query?.auto_ask && localStorage.getItem('nc_new_ask_question')) {
    await consoleInputRef.value?.askQuestion('refresh');
  }
}
function handleMsgSelectModel(args) {
  chooseMsgCnt.value = msgFlowRef.value?.turnOnMsgChooseModel(args);
  chooseModel.value = true;
  chooseMsgAll.value = true;
  chooseMsgMiddle.value = false;
}
function handleMsgSelectChange(args) {
  chooseMsgCnt.value = args?.chooseMsgCnt;
  chooseMsgAll.value = args?.chooseMsgAll;
  chooseMsgMiddle.value = args?.chooseMsgMiddle;
}
function changeMsgSelectAll() {
  if (chooseMsgAll.value) {
    chooseMsgCnt.value = msgFlowRef.value?.turnOnMsgChooseModel();
    chooseMsgAll.value = true;
    chooseMsgMiddle.value = false;
  } else {
    chooseMsgCnt.value = msgFlowRef.value?.unSelectMessages();
    chooseMsgAll.value = false;
    chooseMsgCnt.value = 0;
    chooseMsgMiddle.value = false;
  }
}
onBeforeRouteLeave((to, from, next) => {
  close_upload_manager();
  next();
});
</script>

<template>
  <el-container>
    <MessageFlowV2
      ref="msgFlowRef"
      :session-code="props.sessionCode"
      :height="'calc(100vh - ' + consoleInputHeight + 'px)'"
      @click-recommend-question="data => consoleInputRef?.clickRecommendQuestion(data)"
      @ready="async args => await handleMsgFlowReady()"
      @select-msg="data => handleMsgSelectChange(data)"
    />
    <el-footer :height="consoleInputHeight.toString() + 'px'">
      <ConsoleInput
        v-if="!chooseModel"
        ref="consoleInputRef"
        :session-code="props.sessionCode"
        :height="consoleInputHeight.toString() + 'px'"
        @begin-answer="data => msgFlowRef.beginAnswer(data)"
        @update-answer="newMsg => msgFlowRef.updateAnswer(newMsg)"
        @finish-answer="args => msgFlowRef?.finishAnswer(args)"
        @stop-answer="args => msgFlowRef?.stopAnswer(args)"
        @turn-on-msg-choose-model="args => handleMsgSelectModel(args)"
        @height-change="args => (consoleInputHeight = args.newHeight)"
      />
      <div v-else class="std-middle-box" style="height: 120px; width: 100%">
        <div id="choose-model-area">
          <div class="std-middle-box">
            <el-checkbox v-model="chooseMsgAll" :indeterminate="chooseMsgMiddle" @change="changeMsgSelectAll">
              <el-text> 当前已选中 </el-text>
              <el-text v-if="!showScrollbarButton">
                <br />
              </el-text>
              <el-text> {{ chooseMsgCnt }} 条消息 </el-text>
              <el-text v-if="!showScrollbarButton">
                <br />
              </el-text>

            </el-checkbox>
          </div>
          <div class="std-middle-box" style="flex-direction: row; gap: 4px">
            <div>
              <el-button size="small" @click="turnOffMsgChooseModel"> 取消 </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-footer>
  </el-container>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
#choose-model-area {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  width: calc(100% - 24px);
  max-width: 900px;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
}

@media (width<768px) {
  #choose-model-area {
    padding: 8px;
    gap: 6px;
  }
}
</style>
