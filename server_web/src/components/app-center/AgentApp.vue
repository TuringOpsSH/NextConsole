<script setup lang="ts">
import {computed, onBeforeUnmount, onMounted, ref} from "vue";
import 'highlight.js/styles/stackoverflow-light.min.css';
import AgentAppConsole from "@/components/app-center/AgentAppConsole.vue";
import {Picture as IconPicture} from '@element-plus/icons-vue'
import {
  add_dislike,
  add_like,
  copy_answer,
  copy_question,
  get_msg_item_answer_create_time,
  msg_recommend_question,
  switch_answer_length,
  tooltipStyle,
} from "@/components/next-console/messages-flow/message_flow";
import {console_input_height} from "@/components/next-console/messages-flow/console_input";
import {
  open_reference,
  retry_get_icon,
  show_reference_drawer_fn
} from "@/components/next-console/messages-flow/reference_drawer";
import Reference_drawer from "@/components/next-console/messages-flow/reference_drawer.vue";
import Simple_progress from "@/components/next-console/messages-flow/simple_progress.vue";
import {
  AgentAppMsgFlow,
  agentFlowBoxRef,
  AgentFlowScrollbarRef,
  clickRecommendQuestion, CurrentAgentApp,
  CurrentAgentAppSession,
  CurrentAgentReference, currentGraphConfigs,
  getAgentApp,
  getAgentAppSession,
  handleScroll,
  initAgentAppMsg,
  initAgentAppQas,
  LoadingStatus,
  QAWorkFlowMap,
  scrollToBottom,
  scrollToFlag,
  scrollToQA,
  scrollToTop, sessionAttachData
} from "@/components/app-center/ts/agent-app";
import {
  askAgentQuestion,
  consoleInput,
  currentSupDetail,
  showSupDetail,
  showSupDetailFlag
} from "@/components/app-center/ts/agent_console";
import AgentGraph from "@/components/app-center/AgentGraph.vue";
import {useUserInfoStore} from "@/stores/userInfoStore";

const props = defineProps({
  app_code: {
    type: String,
    required: true
  },
  session_code: {
    type: String,
    required: false
  }})
const userInfoStore = useUserInfoStore()
const show_scrollbar_button = ref(window.innerWidth >= 768)
const mainStyle = computed(() => ({
  height: `calc(100vh - ${console_input_height.value}px)`,
  padding: '0 !important',
}));
function add_custom_style(){
  const appElements = document.querySelectorAll('#app');
  appElements.forEach((element) => {
    // 将每个元素的背景颜色设置为透明
    element.style.backgroundColor = 'transparent';
  });
}
function remove_custom_style(){
  const appElements = document.querySelectorAll('#app');
  appElements.forEach((element) => {
    // 将每个元素的背景颜色设置为透明
    element.style.backgroundColor = 'white';
  });
}
function sendMessageToParent(data) {
  window.parent.postMessage(data, '*'); // '*' 表示不限制目标域名
}

// 监听来自主页面的消息
window.addEventListener('message', (event) => {
  if (event.data.type === 'echo') {
    // 收到消息后，向主页面回复一条消息
    sendMessageToParent(event.data)
    sessionAttachData.value = event.data.data
  } else if (event.data.type === 'question') {
    const question = event.data.data?.[0]?.content;
    if (question) {
      consoleInput.value = question;
      askAgentQuestion();
    }
  }
});

onMounted(async ()=>{
  // 初始化应用信息
  LoadingStatus.value = true
  await getAgentApp( props.app_code )
  // 初始化会话信息
  await getAgentAppSession( props.app_code, props.session_code )
  await initAgentAppQas( props.app_code, props.session_code )
  // 有会话，则加载会话的消息
  await initAgentAppMsg( props.app_code, props.session_code )
  LoadingStatus.value = false
  add_custom_style()

})
onBeforeUnmount(() => {
  remove_custom_style()
})
</script>

<template>
<el-container>
  <el-main :style="mainStyle" >
    <el-scrollbar v-loading="LoadingStatus"
                  element-loading-text="记忆加载中..."
                  @scroll.native="handleScroll"
                  ref="AgentFlowScrollbarRef"
                  wrap-style="width: 100%;"
                  view-style="width: 100%;height: 100%;"
    >
      <el-row style="width: 100%">
        <el-col :span="2" :xs="1"/>
        <el-col :span="20" :xs="22">
          <div id="message-flow-box" ref="agentFlowBoxRef">
            <div style="margin-bottom: 20px">
              <div class="msg-flow-answer-box" >
                <div class="msg-flow-answer-avatar" >
                  <el-avatar :src="CurrentAgentApp.assistant_avatar" shape="square" style="background: none"/>
                </div>
                <div class="msg-flow-answer-content" >
                  <div class="msg-flow-answer-inner"  >
                    <div v-html="CurrentAgentApp?.assistant_prologue"
                         style="width: 100%" />
                  </div>
                </div>
              </div>
              <div class="msg-flow-footer-box">
                <div class="msg-flow-recommend-area">
                  <div class="msg-flow-recommend-box" @click="clickRecommendQuestion(sub_question)"
                       v-for="(sub_question,index) in CurrentAgentApp?.assistant_preset_question">
                    <el-text>
                      {{sub_question?.recommend_question}}
                    </el-text>
                    <div class="relate-question-button" >
                      <el-image src="/images/arrow_right_grey.svg" style="width: 12px;height: 12px"/>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-for="(item,idx) in AgentAppMsgFlow" class="msg-flow-qa-box"
                 @mouseleave="item.show_button_question_area = false; item.show_button_answer_area = false"
            >
              <div class="msg-flow-question-box"
                   @mouseenter="item.show_button_question_area = true">
                <div class="msg-flow-question-content">
                  <div class="msg-question-head-button-area"
                  >
                    <div class="question-create-time-box">
                      <el-text class="msg-tips-text" style="min-width: 125px">
                        {{item?.qa_value.question[0].create_time}}
                      </el-text>

                    </div>
                    <div class="question-button-box" >
                      <div class="question-button" @click="copy_question(item)">
                        <el-image class="question-button-icon" src="/images/copy.svg"/>
                      </div>

                    </div>
                  </div>
                  <el-text class="question-content-text">
                    {{item?.qa_value.question[0].msg_content}}
                  </el-text>
                </div>
                <div class="msg-flow-question-avatar">
                  <el-avatar v-if="userInfoStore.userInfo?.user_avatar" :src="userInfoStore.userInfo?.user_avatar" style="background-color: white"/>
                  <el-avatar v-else style="background: #D1E9FF; cursor: pointer">
                    <el-text style="font-weight: 600;color: #1570ef">
                      {{userInfoStore.userInfo?.user_nick_name_py}}
                    </el-text>
                  </el-avatar>

                </div>
              </div>
              <div class="msg-flow-answer-box"
                   @mouseenter="item.show_button_answer_area = true">
                <div class="msg-flow-answer-avatar" >
                  <el-avatar :src="CurrentAgentApp.assistant_avatar"
                             shape="square"
                             :style="'margin-top: ' + (QAWorkFlowMap?.[item.qa_id]?.length ? '0' : '20px')"
                             style="background: none"
                  />
                </div>

                <div class="msg-flow-answer-content" >

                  <div class="msg-flow-workflow-box" v-if="QAWorkFlowMap?.[item.qa_id]?.length">

                    <div v-show="item?.qa_workflow_open" class="open-workflow-area" >

                      <div class="open-workflow-head">
                        <div class="open-workflow-head-left">
                          <div class="std-middle-box">
                            <el-text style="  min-width: 60px;">工作流</el-text>
                          </div>
                          <simple_progress v-if="!item.qa_finished"/>
                        </div>
                        <div class="open-workflow-head-right">
                          <div class="std-middle-box">
                            <el-image src="/images/arrow_up_grey2.svg" @click="item.qa_workflow_open = false"
                                      style="width: 20px;height: 20px;cursor: pointer"/>
                          </div>
                        </div>
                      </div>
                      <el-scrollbar>
                        <div class="workflow-list">
                          <div v-for="sub_workflow in QAWorkFlowMap[item.qa_id]" class="sub-workflow-area">
                            <div class="sub-workflow-head">
                              <div class="std-middle-box">
                                <el-image src="/images/task_status.svg" style="width: 16px;height: 16px"
                                          v-show="sub_workflow.task_status != 'finished'"
                                />
                                <el-image src="/images/task_status_ok.svg" style="width: 16px;height: 16px"
                                          v-show="sub_workflow.task_status == 'finished'"
                                />
                              </div>
                              <div class="std-middle-box">
                                <el-text>{{sub_workflow.task_type}}</el-text>
                              </div>
                            </div>
                            <div class="sub-workflow-show-info" v-if="sub_workflow.task_type=='网页解析'"
                                 v-for="(img_item,idx) in sub_workflow?.task_params"
                            >
                              <div class="std-middle-box" >
                                <el-image fit="cover" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2"
                                          :preview-src-list="[img_item?.resource_show_url]" :initial-index="0"
                                          :alt="img_item?.resource_source_url"
                                          :src="img_item?.resource_show_url" style="width: 24px;height: 24px">
                                  <template #error>
                                    <el-icon><icon-picture /></el-icon>
                                  </template>
                                </el-image>
                              </div>


                            </div>
                            <div class="sub-workflow-show-info" v-else-if="sub_workflow.task_type=='图像识别'"
                                 v-for="(img_item,idx) in sub_workflow?.task_params"
                            >
                              <div class="std-middle-box" >
                                <el-image fit="cover" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2"
                                          :preview-src-list="sub_workflow?.task_params" :initial-index="0"
                                          :src="img_item" style="width: 24px;height: 24px">
                                  <template #error>
                                    <el-icon><icon-picture /></el-icon>
                                  </template>
                                </el-image>
                              </div>


                            </div>
                            <div class="sub-workflow-show-info" v-else>

                              <el-tooltip :content="sub_workflow.task_label" effect="light">
                                <el-text truncated style="max-width: 100%;">
                                  {{sub_workflow.task_label}}
                                </el-text>
                              </el-tooltip>
                            </div>
                          </div>
                        </div>
                      </el-scrollbar>
                    </div>
                    <div v-show="!item?.qa_workflow_open" class="close-workflow-area">
                      <div class="close-workflow-area-left">
                        <div class="std-middle-box">
                          <el-image src="/images/ok_green.svg" style="width: 20px;height: 20px"
                                    v-show="item?.qa_finished"
                          />
                          <el-image src="/images/ok_grey.svg" style="width: 20px;height: 20px"
                                    v-show="!(item?.qa_finished)" />
                        </div>
                        <div class="std-middle-box">
                          <el-text style="font-weight: 500;font-size: 14px;line-height: 20px;color: #101828">
                            工作流</el-text>
                        </div>
                      </div>
                      <div class="close-workflow-area-right">
                        <div class="std-middle-box">
                          <el-image src="/images/arrow_down_grey2.svg"
                                    style="width: 20px;height: 20px; cursor: pointer "
                                    @click="item.qa_workflow_open = true"
                          />
                        </div>

                      </div>
                    </div>

                  </div>
                  <div class="msg-flow-graph-box" v-if="currentGraphConfigs?.[item.qa_value.question[0]?.msg_id]?.sql">
                    <AgentGraph :msg-id="item.qa_value.question[0]?.msg_id"
                                :sql ="currentGraphConfigs?.[item.qa_value.question[0]?.msg_id]?.sql"
                                :raw-data ="currentGraphConfigs?.[item.qa_value.question[0]?.msg_id]?.raw_data"
                                :columns = "currentGraphConfigs?.[item.qa_value.question[0]?.msg_id]?.columns"
                                :options="currentGraphConfigs?.[item.qa_value.question[0]?.msg_id]?.options"
                                :pane="currentGraphConfigs?.[item.qa_value.question[0]?.msg_id]?.pane"
                    />
                  </div>

                  <div class="msg-flow-answer-inner"
                       :class="{'msg-flow-answer-inner-short': item?.short_answer}"

                  >

                    <div v-html="sub_finish_msg"
                         style="width: 100%"
                         v-for="(sub_finish_msg,idx) in item.qa_value.answer[
                                                          item.qa_value.question[0]?.msg_id
                                                          ]?.[0]?.msg_content_finish_html"
                         @mouseover="showSupDetail(item, $event)"

                    />
                    <simple_progress v-if="item?.qa_finished==false && !item?.qa_workflow_open"/>
                    <div v-if="item.qa_value.answer[
                                                          item.qa_value.question[0]?.msg_id
                                                          ]?.[0]?.msg_is_cut_off">
                      <el-text style="color: #c8cad9;font-size: 12px">
                        此回答已停止
                      </el-text>
                    </div>


                  </div>


                </div>
                <div class="msg-answer-right-button-area"
                     v-if="show_scrollbar_button"
                     v-show="item.show_button_answer_area == true || item?.short_answer">

                  <div class="answer-button-box">
                    <div class="answer-button" @click="switch_answer_length(item)">
                      <el-image  src="/images/arrow_down_grey.svg"
                                 v-if="item?.short_answer"/>
                      <el-image class="answer-button-icon" src="/images/arrow_up_grey.svg"
                                v-else/>

                    </div>

                  </div>
                </div>
              </div>
              <div class="msg-flow-footer-box">
                <div class="msg-flow-answer-button-area" >
                  <div class="msg-flow-answer-button-area-left">
                    <div v-show="CurrentAgentReference?.[item.qa_value.question?.[0]?.msg_id]"
                         @click="show_reference_drawer_fn(CurrentAgentReference?.[item.qa_value.question?.[0]?.msg_id])">
                      <el-text class="reference-link-text">
                        参考来源
                      </el-text>
                    </div>
                    <div class="reference-link-box">
                      <el-text class="reference-link-cnt">
                        {{CurrentAgentReference?.[item.qa_value.question?.[0]?.msg_id]?.length}}
                      </el-text>

                    </div>
                    <el-divider direction="vertical"
                                v-show="CurrentAgentReference?.[item.qa_value.question?.[0]?.msg_id]"/>
                    <div class="answer-create-time-box"  >
                      <el-text class="msg-tips-text">
                        {{get_msg_item_answer_create_time(item)}}
                      </el-text>
                    </div>
                  </div>
                  <div  class="msg-flow-answer-button-area-right">
                    <div class="msg-flow-answer-button" @click="copy_answer(item)">
                      <div class="msg-flow-answer-button-icon-box">
                        <el-image class="msg-flow-answer-button-icon"
                                  src="/images/copy.svg"/>
                      </div>

                    </div>
                    <div class="msg-flow-answer-button" @click="add_like(item)" v-if="false">
                      <div class="msg-flow-answer-button-icon-box">
                        <el-image class="msg-flow-answer-button-icon" src="/images/collect_green.svg"
                                  v-if="item?.qa_value?.answer?.[
                                     item?.qa_value?.question?.[0]?.msg_id
                                     ]?.[0]?.msg_remark == 1"/>
                        <el-image class="msg-flow-answer-button-icon" src="/images/collect_grey.svg" v-else/>
                      </div>
                    </div>
                    <div class="msg-flow-answer-button" @click="add_dislike(item)">
                      <div class="msg-flow-answer-button-icon-box">
                        <el-image class="msg-flow-answer-button-icon" src="/images/thumbs_down_red.svg"
                                  v-if="item?.qa_value?.answer?.[
                                     item?.qa_value?.question?.[0]?.msg_id
                                     ]?.[0]?.msg_remark == -1"/>
                        <el-image class="msg-flow-answer-button-icon" src="/images/thumbs_down_grey.svg" v-else/>
                      </div>
                    </div>
                  </div>


                </div>
                <div class="msg-flow-recommend-area" v-show="item?.qa_finished">
                  <div class="msg-flow-recommend-box" @click="clickRecommendQuestion(sub_question)"
                       v-for="(sub_question,index) in msg_recommend_question?.[item?.qa_value.question?.[0]?.msg_id]">
                    <el-text>
                      {{sub_question.recommend_question}}
                    </el-text>
                    <div class="relate-question-button" >
                      <el-image src="/images/arrow_right_grey.svg" style="width: 12px;height: 12px"/>
                    </div>
                  </div>

                </div>
              </div>
            </div>
          </div>

        </el-col>
        <el-col :span="2" :xs="1"/>
      </el-row>
    </el-scrollbar>
    <div class="to-bottom-box" v-show="scrollToFlag && CurrentAgentAppSession?.id && show_scrollbar_button"
         @click="scrollToQA(1)" @dblclick="scrollToBottom()"
    >
      <el-button class="to-top-button" >
        <el-image src="/images/to_bottom.svg" class="to-top-button-icon"/>
      </el-button>
    </div>
    <div class="to-top-box" v-show="scrollToFlag && CurrentAgentAppSession?.id && show_scrollbar_button"
         @click="scrollToQA(-1)"
         @dblclick="scrollToTop()" >
      <el-button class="to-top-button">
        <el-image src="/images/to_top.svg" class="to-top-button-icon"/>
      </el-button>
    </div>
    <reference_drawer :enable-view="false"/>

    <div v-if="showSupDetailFlag" :style="tooltipStyle" id="sup_detail_box" @mouseleave="showSupDetailFlag=false">

      <div class="reference-title">
        <div class="std-middle-box">
          <el-image :src="currentSupDetail?.resource_icon" v-if="currentSupDetail?.resource_icon"
                    :id="currentSupDetail?.resource_icon"
                    @error="retry_get_icon(currentSupDetail)" class="reference-img">
            <template #error>
              <div class="image-slot">
                <el-icon><icon-picture /></el-icon>
              </div>
            </template>
          </el-image>
        </div>
        <div class="std-middle-box">
          <el-text truncated class="reference-site-name">
            {{currentSupDetail?.resource_name}}
          </el-text>
        </div>
      </div>
      <div class="reference-name">
        <el-text truncated class="reference-name-text" @click="">
          {{currentSupDetail?.resource_title}}
        </el-text>
      </div>
      <div class="reference-text-box" v-show="currentSupDetail?.source_type=='webpage'">
        <el-text truncated class="reference-text"  >
          {{currentSupDetail?.ref_text}}
        </el-text>
      </div>

    </div>

  </el-main>
  <el-footer :height="console_input_height.toString()+'px'">
    <AgentAppConsole />

  </el-footer>
</el-container>
</template>

<style scoped>
html, body {
  background-color: transparent !important;
}

#app {
  background: transparent !important;
}
:deep(.hljs){
  font-size: 14px !important;
  line-height: 21px !important;
}
:deep(code ) {
  max-width: 751px;
  margin: 3px 5px  ;
  border-radius: 6px  ;
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
#message-flow-box{
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
  margin-top: 24px;
  position: relative;
}
.to-bottom-box{
  position: fixed;
  bottom: 200px;
  z-index: 999;
  right: 20px
}
.to-top-button{
  width: 40px;
  height: 40px;
  border: 1px solid #EAECF0;
  box-shadow: 0 1px 2px 0 #1018280D;
  border-radius: 20px;
}
.to-top-button-icon{
  width: 20px;
  height: 20px;

}
.to-top-box{
  position: fixed;
  top: 20px;
  z-index: 999;
  right: 20px ;
}
.msg-flow-qa-box{
  display: flex;
  flex-direction: column;
  padding: 16px 0;
  gap: 16px;
  align-items: flex-start;
  justify-content: center;
  width: 100%;
}
.msg-tips-text{
  font-weight: 400;
  font-size: 12px;
  line-height: 20px;
  color: #475467
}
.msg-flow-question-box{
  display: flex;
  flex-direction: row;
  gap: 12px;
  width: 100%;
  justify-content: flex-end;
  position: relative;
}
.msg-flow-question-content{
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: calc(100% - 130px);
  align-items: flex-end;
  justify-content: center;
  background: rgb(209, 233, 255);
  padding: 8px 12px;
  border-radius: 8px;
  position: relative;
}
.msg-question-head-button-area{
  position: absolute;
  top: -28px;
  right: 0;
  display: flex;
  flex-direction: row-reverse;
  justify-content: flex-start;
  width: 100%;
  align-items: center;
  gap: 6px;

}
.question-button-box{
  display: flex;
  flex-direction: row;
  gap: 8px;


}
.question-button{
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px;

}
.question-button:hover{
  background: #F0F9FF;
}
.question-button:active{
  background: #D9D9D9;
  transform: scale(0.95);
}
.question-button-icon{
  width: 20px;
  height: 20px;
}
.question-create-time-box{
  display: flex;
  flex-direction: row;
  gap: 8px;
}

.msg-flow-answer-box{
  display: flex;
  flex-direction: row;
  gap: 12px;
  width: 100%;
  justify-content: flex-start;
  position: relative;
}
.msg-flow-answer-content{
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: calc(100% - 130px);
  align-items: flex-start;
  justify-content: center;
  padding: 0 12px;
  border-radius: 8px;
  position: relative;
  background-color: white;
  height: 100%;
}
.msg-flow-answer-inner{
  display: flex;
  flex-direction: column;
  position: relative;
  width: 100%;
  align-items: flex-start;
  justify-content: space-between;
  overflow: hidden;

}
.msg-flow-answer-inner-short{
  max-height: 300px;
  position: relative;

}
.msg-flow-answer-inner-short::after{
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 80px; /* 羽化的高度 */
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 1));
  pointer-events: none; /* 确保不影响交互 */

}
.msg-answer-right-button-area{

  display: flex;
  flex-direction: row-reverse;
  justify-content: space-between;
  align-items: flex-start;
  z-index: 40;
}
.answer-button-box{
  display: flex;
  flex-direction: row;
  gap: 8px;
}
.answer-button{
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px;
  padding: 4px;
}
.answer-button:hover{
  background: #F0F9FF;
}
.answer-button:active{
  background: #D9D9D9;
  transform: scale(0.95);
}
.answer-button-icon {
  width: 12px;
  height: 12px;
}
.msg-flow-footer-box{
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  justify-content: flex-start;
  position: relative;
}
.msg-flow-answer-button-area{
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
  position: absolute;
  top: -15px;
  left: 50px;
  width: calc(100% - 100px);
}
.msg-flow-answer-button{
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.msg-flow-answer-button-icon-box{
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 4px;

}
.msg-flow-answer-button-icon{
  width: 20px;
  height: 20px;
}
.msg-flow-recommend-area{
  margin-top: 16px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 8px;
  margin-left: 50px;
  margin-right: 50px;
}
.msg-flow-recommend-box{
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  justify-content: center;
  padding: 4px 8px;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
}
.msg-flow-recommend-box:hover{
  background-color: #F0F9FF;
}
.msg-flow-recommend-box:active{
  background-color: #D9D9D9;
  transform: scale(0.95);

}
.reference-link-text{
  font-size: 12px;
  font-weight: 400;
  cursor: pointer;
  line-height: 20px;
  color: #1570ef
}
.reference-link-box{
  background-color: #F2F4f7;
  padding: 0 4px;
  border-radius: 3px;
}
.reference-link-cnt{
  font-size: 12px;
  font-weight: 500;
  line-height: 18px;
  color: #34495e
}
.msg-flow-answer-button-area-left{
  display: flex;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  justify-content: flex-start;
}
.msg-flow-answer-button-area-right{
  display: flex;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  justify-content: flex-start;
}
sup {
  border-radius: 4px;
  background: #f9f9f9 !important;
  /* 添加其他样式属性 */
}
#sup_detail_box{
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px 12px;
  background: #FFFFFF;
  border-radius: 8px;
  position: absolute;
  z-index: 999;
  top: 0;
  left: 0;
  width: 300px;
  max-height: 100px;
  box-shadow: 0 12px 16px -4px #10182814;


}

.std-middle-box{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.reference-title{
  display: flex;
  flex-direction: row;
  gap: 4px;
}
.reference-img{
  width: 16px;
  height: 16px;
}
.reference-site-name{
  font-weight: 400;
  font-size: 12px;
  line-height: 18px;
  color: #475467;
  max-width: 260px;
}
.reference-name-text{
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  color: #101828;
  cursor: pointer;
}
.reference-name-text:hover{
  color: #1570ef;
}
.reference-text-box{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  flex-wrap: wrap;
  width: 100%;
}
.reference-text{
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #667085;

}
.msg-flow-workflow-box{
  width: 100%;
}
.open-workflow-head-left{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;

}
.close-workflow-area{
  min-width: 144px;
  padding: 6px 12px;
  background: #f9fAFB;
  border-radius: 8px;
  border: 1px solid #F2F4F7;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.close-workflow-area-left{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
}
.open-workflow-area{
  border: 1px solid #D0D5DD;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  width: calc(100% - 24px);
  max-height: 160px;
  overflow: hidden;
}
.open-workflow-head{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.sub-workflow-area{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;

}
.sub-workflow-head{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  min-width: 80px;
}
.sub-workflow-show-info{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  padding: 4px 8px;
  background-color: #f9f9fB;
  gap: 16px;
  max-width: calc(100% - 136px);
  border-radius: 8px;

}
.msg-check-box{
  position: absolute;
  left: -30px;
  top: 10px;
}
#choose-model-area{
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  width: calc(100% - 24px);
  max-width: 900px;
  padding: 12px;
  background: #F9F9F9;
  border-radius: 8px;
}
.question-content-text{
  font-size: 16px; font-weight: 400;line-height: 24px;color: #101828;
  width: 100%;white-space: pre-line;
}
.msg-flow-graph-box{
  width: 100%;
  height: 100%;
  max-height: 450px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-items: center;
}
.workflow-list{
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 100px;
}
/* 通过穿透语法覆盖父级样式 */

@media (width<768px) {
  #message-flow-box{
    gap: 0;
  }
  .msg-flow-qa-box{
    padding: 8px 0;
    gap: 8px;
  }
  .msg-flow-question-box{
    gap: 4px;
  }
  .question-button-icon{
    width: 14px;
    height: 14px;
  }
  .msg-flow-question-content{
    max-width: calc(100% - 72px);

  }
  .question-content-text{
    font-size: 14px;
    line-height: 20px;
  }
  .msg-flow-answer-button-area{
    top: -10px;
    left: 0;
    width: 100%;
  }
  .msg-flow-answer-button-icon{
    width: 14px;
    height: 14px;
  }
  .msg-flow-answer-box{
    gap: 4px;
  }
  .msg-flow-answer-content{
    width: calc(100% - 50px);
  }
  :deep(.hljs){
    font-size: 14px !important;
    line-height: 20px !important;
  }
  :deep(p){
    font-size: 14px !important;
    line-height: 20px !important;
  }
  :deep(li){
    font-size: 14px !important;
    line-height: 20px !important;

  }
  .open-workflow-area{

    gap: 6px;
    padding: 8px;

  }
  .msg-check-box{
    position: absolute;
    left: -12px;


  }
  #choose-model-area{
    padding: 8px;
    gap: 6px;
  }




}
</style>
