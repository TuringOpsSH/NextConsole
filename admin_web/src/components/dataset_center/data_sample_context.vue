<script setup lang="ts">

import {copy_text, version_turn_left, version_turn_right} from "@/components/feedback_center/session_log";
import {compiledMarkdown} from "@/utils/markdown";
import {current_smale_context} from "@/components/dataset_center/data_samples";
</script>

<template>
  <el-scrollbar wrap-class="width:100%" view-class="width:100%">

    <div class="msg-item-box" v-for="(item, index)  in current_smale_context" >

      <div class="msg-item">
        <div v-if="item.qa_value.question.length >0" class="msg-sub-item">

          <div class="msg-item-right">
            <div class="sub-button">
              <div class="send-time">
                <el-text class="send-time-text">
                  {{ item.qa_value.question[0].create_time }}
                </el-text>

              </div>
              <div class="msg-update">
                <div class="msg-update-button-version"
                     v-if="item.qa_value.question.length >1">
                  <el-row>
                    <el-col :span="8" class="version-text-box">
                      <el-button class="version-arrow" @click="version_turn_left(item, 1)">
                        <el-image src="images/version_left.svg" class="version-change-icon"/>
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
                        <el-image src="images/version_right.svg" class="version-change-icon"/>
                      </el-button>
                    </el-col>
                  </el-row>
                </div>
                <el-button-group>
                  <el-button class="msg-update-button"
                             @click="copy_text(item.qa_value.question[0].msg_content)">
                    <el-image src="images/copy.svg" class="msg-update-button-icon"/>
                  </el-button>
                </el-button-group>
              </div>

            </div>
            <div class="msg-content" :style='{
                        backgroundColor: "#D1E9FF" }'

            >
              <div v-html="compiledMarkdown(item.qa_value.question[0].msg_content, 1)"
                   class="assistant-answer" id="{{item.qa_value.question[0].msg_id}}"/>

            </div>
          </div>
        </div>
        <div v-if="item.qa_value.question[0].msg_id in item.qa_value.answer &&
                      item.qa_value.answer[item.qa_value.question[0].msg_id].length >0" class="msg-sub-item">

          <div class="msg-item-right">
            <div class="sub-button">
              <div class="send-time">
                <el-text class="send-time-text">
                  {{ item.qa_value.answer[item.qa_value.question[0].msg_id][0].create_time }}
                </el-text>
              </div>
              <div class="msg-update">

                <div class="msg-update-button-version"
                     v-if="item.qa_value.answer[item.qa_value.question[0].msg_id].length >1">
                  <el-row>
                    <el-col :span="8" class="version-text-box">
                      <el-button class="version-arrow" @click="version_turn_left(item, 2)">
                        <el-image src="images/version_left.svg" class="version-change-icon"/>
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
                        <el-image src="images/version_right.svg" class="version-change-icon"/>
                      </el-button>
                    </el-col>
                  </el-row>
                </div>

                <el-button-group >
                  <el-button class="msg-update-button"
                             @click="copy_text(item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_content)">
                    <el-image src="images/copy.svg" class="msg-update-button-icon"/>
                  </el-button>
                </el-button-group>

              </div>
            </div>

            <div class="msg-content"
                 :style="{ backgroundColor : '#F2F4F7'}">

              <div v-html="compiledMarkdown(
                                        item.qa_value.answer[item.qa_value.question[0].msg_id][0].msg_content,2)"
                   id="answer-markdown"
                   class="assistant-answer"/>

            </div>

          </div>
        </div>

      </div>

    </div>
  </el-scrollbar>

</template>

<style scoped>
  .msg-item-box{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  padding: 0 12px;
  gap: 8px;
  width: calc(100% - 24px);
}
  .assistant-answer{
    width: 100%;
    overflow: auto;
  }
  :deep(.hljs){
    font-size: 14px !important;
    line-height: 21px !important;
  }
  :deep(code ) {
    max-width: 751px;
    padding: 3px 5px  ;
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
  .msg-update-button-version{
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
  .version-arrow{
    width: 16px;
    height: 16px;
    border: 0;

  }
  .version-change-icon{
    width: 16px;
    height: 16px;
  }
  .version-text-box{
    display: flex;
    justify-content: center;


  }
  .version-text{
    font-size: 12px;
    font-weight: 500;
    line-height: 18px;
    color: #101828;
    display: flex;
    justify-content: center;
    align-self: auto;
  }
  .msg-item{
    width: 100%;
  }
</style>
