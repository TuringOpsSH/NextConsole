<script setup lang="ts">

import {
  CurrentMsgTab,
  showMsgRagTrace,
  showMsgTrace,
  showMsgQaTrace,
  CurrentMsg, CurrentMsgRagTrace, showMsgWorkFlowTrace, CurrentMsgWorkFlowTrace
} from "@/components/feedback_center/message_log";
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css';
</script>

<template>
  <el-dialog v-model="showMsgTrace" title="日志">
    <div style="width: 100% ;display:flex;flex-direction: column; height: 50vh" >
      <div id="msg-trace-head">
        <div class="msg-trace-tab" :class="CurrentMsgTab == 3 ? 'msg-trace-tab-active' :''"
             @click="showMsgWorkFlowTrace"
        >
          <el-text class="msg-trace-tab-text" :class="CurrentMsgTab == 3 ? 'msg-trace-tab-active-text' :''">
            WorkFlow日志
          </el-text>
        </div>
        <div class="msg-trace-tab" :class="CurrentMsgTab == 1 ? 'msg-trace-tab-active' :''"
             @click="showMsgRagTrace"
        >
          <el-text class="msg-trace-tab-text" :class="CurrentMsgTab == 1 ? 'msg-trace-tab-active-text' :''">
            RAG日志
          </el-text>
        </div>
        <div class="msg-trace-tab" :class="CurrentMsgTab == 2 ? 'msg-trace-tab-active' :''"
             @click="showMsgQaTrace"
        >
          <el-text class="msg-trace-tab-text" :class="CurrentMsgTab == 2 ? 'msg-trace-tab-active-text' :''">
            QA日志
          </el-text>
        </div>
      </div>
      <el-scrollbar view-class="width:100%" wrap-class="width:100%">

        <div v-if="CurrentMsgTab == 1">
          <vue-json-pretty v-if="CurrentMsgRagTrace"
                           :showLineNumber="true"
                           :showIcon="true"
                           :data="JSON.parse(JSON.stringify(CurrentMsgRagTrace))"
                           :deep="1"
                           display-data-type />
          <el-empty v-else description="该问题未启用rag"></el-empty>
        </div>
        <div v-else-if="CurrentMsgTab == 2">

          <vue-json-pretty :data="JSON.parse(JSON.stringify(CurrentMsg))"
                           :deep="1"
                           :showLineNumber="true"
                           :showIcon="true"
                           display-data-type />
        </div>
        <div v-else-if="CurrentMsgTab == 3">

          <vue-json-pretty :data="JSON.parse(JSON.stringify(CurrentMsgWorkFlowTrace))"
                           :deep="2"
                           :showLineNumber="true"
                           :showIcon="true"
                           display-data-type />
        </div>
      </el-scrollbar>

    </div>

  </el-dialog>
</template>

<style scoped>
#msg-trace-head{
  width: 100% ;
  display:flex;
  flex-direction: row;
  gap: 6px;
  background-color: #F9FAFB;
  border: 1px solid #EAECF0
}
.msg-trace-tab{
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.msg-trace-tab-active{
  background-color: #FFFFFF;
  box-shadow: 0 1px 2px 0 #1018280F;
}
.msg-trace-tab-text{
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  text-align: left;
  color: #667085;

}
.msg-trace-tab-active-text{
  color: #344054;
}
</style>
