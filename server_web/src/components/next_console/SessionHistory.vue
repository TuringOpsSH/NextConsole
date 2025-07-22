<script setup lang="ts">
import {Search} from '@element-plus/icons-vue';
import {ElMessage} from 'element-plus';
import {nextTick, ref, watch} from 'vue';
import {
  delete_session as deleteSession,
  search_qa as searchQa,
  search_session as searchSession,
  update_session as updateSession
} from '@/api/next_console';
import {session_item, session_item as ISessionItem} from '@/types/next_console';
import router from "@/router";


const props = defineProps({
  sessionSource: {
    type: String,
    default: 'next_search'
  }
});
const loadingSession = ref(false);
const sessionSource = ref('next_search');
const searchSessionKeyword = ref('');
const sessionHistoryAll = ref<ISessionItem[]>([]);
const sessionHistoryOneDay = ref<ISessionItem[]>([]);
const sessionHistoryOneWeek = ref<ISessionItem[]>([]);
const sessionHistoryOneMonth = ref<ISessionItem[]>([]);
const sessionHistoryOther = ref<ISessionItem[]>([]);
const allSessionSummaryMaps = ref({});
const historySessionTopicInputRef = ref();
async function getAllSession() {
  // 跳转到所有会话
  let params = {
    fetch_all: true,
    session_topic: searchSessionKeyword.value,
    session_source: 'next_search'
  };
  if (sessionSource.value) {
    params.session_source = sessionSource.value;
  }
  loadingSession.value = true;
  let data = await searchSession(params);
  loadingSession.value = false;
  if (data.error_status) {
    return;
  }
  sessionHistoryAll.value = data.result;
  sessionHistoryOneDay.value = data.result.filter((item: ISessionItem) => calTimeArea(item.update_time) === 0);
  sessionHistoryOneWeek.value = data.result.filter((item: ISessionItem) => calTimeArea(item.update_time) === 1);
  sessionHistoryOneMonth.value = data.result.filter((item: ISessionItem) => calTimeArea(item.update_time) === 2);
  sessionHistoryOther.value = data.result.filter((item: ISessionItem) => calTimeArea(item.update_time) === 3);
  let allSessionId = data.result.map((item: ISessionItem) => item.id);
  let qaData = await searchQa({
    session_id: allSessionId,
    fetch_all: true
  });
  if (qaData.error_status) {
    return;
  }
  let summaryCnt = {};
  for (let item of qaData.result) {
    if (!allSessionSummaryMaps.value[item.session_id]) {
      allSessionSummaryMaps.value[item.session_id] = '';
    }
    if (!summaryCnt[item.session_id]) {
      summaryCnt[item.session_id] = 0;
    }
    if (!item.qa_topic || summaryCnt[item.session_id] > 3) {
      continue;
    }
    allSessionSummaryMaps.value[item.session_id] += '  ' + item.qa_topic;
    summaryCnt[item.session_id] += 1;
  }
  // session_summary 由对应qa_topic 组合而成
  for (let item of sessionHistoryAll.value) {
    item.session_summary = allSessionSummaryMaps.value[item.id];
  }
}
async function historyDeleteSession(item: ISessionItem) {
  let params = {
    session_id: item.id
  };
  let res = await deleteSession(params);
  if (!res.error_status) {
    await getAllSession();
    ElMessage.success('删除成功');
  }
}
async function historyRewriteSessionTopic(item: ISessionItem) {
  let params = {
    session_id: item.id,
    session_topic: item.session_topic
  };
  let res = await updateSession(params);
  if (!res.error_status) {
    await getAllSession();
    ElMessage.success('修改成功');
  }
}
async function focusHistorySessionTopicInput(item: ISessionItem) {
  item.history_is_edit = true;
  // 在渲染完成后聚焦
  await nextTick();
  if (historySessionTopicInputRef.value) {
    historySessionTopicInputRef.value?.[0].focus();
  }
}
async function changeCurrentSession(targetSession: session_item, event: any) {
  if (targetSession.is_edit) {
    return;
  }
  // 拦截点击更多按钮
  if (
      event.target.className.includes('session-more-button') ||
      event.target.className.includes('el-image__inner') ||
      event.target.className.includes('el-image')
  ) {
    return;
  }
  if (targetSession.session_source == 'next_search') {
    await router.push({
      name: 'message_flow',
      params: {
        session_code: targetSession.session_code
      }
    });
  } else {
    await router.push({
      name: 'workbenches',
      params: {
        appCode: targetSession.session_source,
        sessionCode: targetSession.session_code
      }
    });
  }
}
function calTimeArea(updateTime: string) {
  // 计算时间区间，并返回 0：今天，1：本周，2：本月，3：更早
  // 这个时间字符串"2024-01-14 19:27:39"的时间戳
  const targetTime = new Date(updateTime).getTime();

  // 当下时间的时间戳
  const nowTime = new Date().getTime();

  // 计算时间间隔
  const interval = nowTime - targetTime;
  // 一天的时间戳
  if (interval < 86400000) {
    return 0;
  }
  // 一周的时间戳
  if (interval < 86400000 * 7) {
    return 1;
  }
  // 一个月的时间戳
  if (interval < 86400000 * 30) {
    return 2;
  }
  return 3;
}
watch(
  () => props.sessionSource,
  (newVal) => {
    sessionSource.value = newVal;
    getAllSession();
  },
  { immediate: true }
);
</script>

<template>
  <div id="all_session_main">
    <div id="session_history_title">
      <div class="std-middle-box" style="width: 160px">
        <el-text id="session_history_title_text">会话历史</el-text>
      </div>

      <el-input
          v-model="searchSessionKeyword"
          :prefix-icon="Search"
          placeholder="搜索会话主题"
          clearable
          style="max-width: calc(100% - 200px)"
          @change="getAllSession()"
      />
    </div>
    <el-scrollbar>
      <div id="session_list" v-loading="loadingSession" element-loading-text="记忆加载中...">
        <div v-if="sessionHistoryOneDay?.length" id="in_one_day" class="session-time-type-box">
          <div class="session-time-type">
            <el-text>今天</el-text>
          </div>
          <div v-for="item in sessionHistoryOneDay" :key="item.id">
            <div class="session-topic-box">
              <el-input
                  v-if="item?.history_is_edit"
                  ref="historySessionTopicInputRef"
                  v-model="item.session_topic"
                  clearable
                  @blur="historyRewriteSessionTopic(item)"
                  @keydown.enter="historyRewriteSessionTopic(item)"
              />
              <el-text v-else class="session-topic-text" truncated @click="changeCurrentSession(item, $event)">
                {{ item.session_topic }}
              </el-text>
            </div>
            <div class="session-info-box">
              <div class="session-summary-box">
                <el-text class="session-summary-text" truncated>
                  {{ item?.session_summary }}
                </el-text>
                <div class="session-manage-box">
                  <el-popover trigger="click">
                    <template #reference>
                      <el-image src="images/dot_list_grey.svg" />
                    </template>
                    <div class="session-manage-button" @click="focusHistorySessionTopicInput(item)">
                      <div class="std-middle-box">
                        <el-image src="images/edit_03_grey.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text"> 重命名 </el-text>
                      </div>
                    </div>
                    <div class="session-manage-button" @click="historyDeleteSession(item)">
                      <div class="std-middle-box">
                        <el-image src="images/delete_red.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text" style="color: red"> 删除 </el-text>
                      </div>
                    </div>
                  </el-popover>
                </div>
              </div>

              <div class="session-update-box">
                <el-text class="session-update-time-text">上次更新时间: {{ item.update_time }}</el-text>
              </div>
            </div>
          </div>
        </div>
        <el-divider v-if="sessionHistoryOneDay?.length" />
        <div v-if="sessionHistoryOneWeek?.length" id="in_seven_days" class="session-time-type-box">
          <div class="session-time-type">
            <el-text>一周内</el-text>
          </div>
          <div v-for="item in sessionHistoryOneWeek" :key="item.id">
            <div class="session-topic-box">
              <el-input
                  v-if="item?.history_is_edit"
                  ref="historySessionTopicInputRef"
                  v-model="item.session_topic"
                  clearable
                  @blur="historyRewriteSessionTopic(item)"
                  @keydown.enter="historyRewriteSessionTopic(item)"
              />
              <el-text v-else class="session-topic-text" truncated @click="changeCurrentSession(item, $event)">
                {{ item.session_topic }}
              </el-text>
            </div>
            <div class="session-info-box">
              <div class="session-summary-box">
                <el-text class="session-summary-text" truncated>
                  {{ item?.session_summary }}
                </el-text>
                <div class="session-manage-box">
                  <el-popover trigger="click">
                    <template #reference>
                      <el-image src="images/dot_list_grey.svg" />
                    </template>
                    <div class="session-manage-button" @click="focusHistorySessionTopicInput(item)">
                      <div class="std-middle-box">
                        <el-image src="images/edit_03_grey.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text"> 重命名 </el-text>
                      </div>
                    </div>
                    <div class="session-manage-button" @click="historyDeleteSession(item)">
                      <div class="std-middle-box">
                        <el-image src="images/delete_red.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text" style="color: red"> 删除 </el-text>
                      </div>
                    </div>
                  </el-popover>
                </div>
              </div>

              <div class="session-update-box">
                <el-text class="session-update-time-text">上次更新时间: {{ item.update_time }}</el-text>
              </div>
            </div>
          </div>
        </div>
        <el-divider v-if="sessionHistoryOneWeek?.length" />
        <div v-if="sessionHistoryOneMonth?.length" id="in_one_month" class="session-time-type-box">
          <div class="session-time-type">
            <el-text>一月内</el-text>
          </div>
          <div v-for="item in sessionHistoryOneMonth" :key="item.id">
            <div class="session-topic-box">
              <el-input
                  v-if="item?.history_is_edit"
                  ref="historySessionTopicInputRef"
                  v-model="item.session_topic"
                  clearable
                  @blur="historyRewriteSessionTopic(item)"
                  @keydown.enter="historyRewriteSessionTopic(item)"
              />
              <el-text v-else class="session-topic-text" truncated @click="changeCurrentSession(item, $event)">
                {{ item.session_topic }}
              </el-text>
            </div>
            <div class="session-info-box">
              <div class="session-summary-box">
                <el-text class="session-summary-text" truncated>
                  {{ item?.session_summary }}
                </el-text>
                <div class="session-manage-box">
                  <el-popover trigger="click">
                    <template #reference>
                      <el-image src="images/dot_list_grey.svg" />
                    </template>
                    <div class="session-manage-button" @click="focusHistorySessionTopicInput(item)">
                      <div class="std-middle-box">
                        <el-image src="images/edit_03_grey.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text"> 重命名 </el-text>
                      </div>
                    </div>
                    <div class="session-manage-button" @click="historyDeleteSession(item)">
                      <div class="std-middle-box">
                        <el-image src="images/delete_red.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text" style="color: red"> 删除 </el-text>
                      </div>
                    </div>
                  </el-popover>
                </div>
              </div>

              <div class="session-update-box">
                <el-text class="session-update-time-text">上次更新时间: {{ item.update_time }}</el-text>
              </div>
            </div>
          </div>
        </div>
        <el-divider v-if="sessionHistoryOneMonth?.length" />
        <div v-if="sessionHistoryOther?.length" id="other_time_rage" class="session-time-type-box">
          <div class="session-time-type">
            <el-text>更早</el-text>
          </div>
          <div v-for="item in sessionHistoryOther" :key="item.id">
            <div class="session-topic-box">
              <el-input
                  v-if="item?.history_is_edit"
                  ref="historySessionTopicInputRef"
                  v-model="item.session_topic"
                  clearable
                  @blur="historyRewriteSessionTopic(item)"
                  @keydown.enter="historyRewriteSessionTopic(item)"
              />
              <el-text v-else class="session-topic-text" truncated @click="changeCurrentSession(item, $event)">
                {{ item.session_topic }}
              </el-text>
            </div>
            <div class="session-info-box">
              <div class="session-summary-box">
                <el-text class="session-summary-text" truncated>
                  {{ item?.session_summary }}
                </el-text>
                <div class="session-manage-box">
                  <el-popover trigger="click">
                    <template #reference>
                      <el-image src="images/dot_list_grey.svg" />
                    </template>
                    <div class="session-manage-button" @click="focusHistorySessionTopicInput(item)">
                      <div class="std-middle-box">
                        <el-image src="images/edit_03_grey.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text"> 重命名 </el-text>
                      </div>
                    </div>
                    <div class="session-manage-button" @click="historyDeleteSession(item)">
                      <div class="std-middle-box">
                        <el-image src="images/delete_red.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text" style="color: red"> 删除 </el-text>
                      </div>
                    </div>
                  </el-popover>
                </div>
              </div>

              <div class="session-update-box">
                <el-text class="session-update-time-text">上次更新时间: {{ item.update_time }}</el-text>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!sessionHistoryAll?.length">
          <el-empty description="未找到相关结果~" />
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
  min-width: 24px;
  min-height: 24px;
}
#all_session_main {
  width: 100%;
  height: 100vh;
  background: #ffffff;
  display: flex;
  flex-direction: column;
}
#session_history_title {
  display: flex;
  justify-content: flex-start;
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
}
#session_history_title_text {
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
}
#session_list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px 40px;
  height: calc(100vh - 180px);
}
.session-time-type-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.session-time-type {
  font-size: 14px;
  font-weight: 600;
  line-height: 24px;
}
.session-topic-box {
  padding: 10px;
  border-radius: 4px;
}

.session-topic-text {
  font-size: 18px;
  font-weight: 700;
  line-height: 32px;
  color: black;
  cursor: pointer;
}
.session-topic-text:hover {
  color: #1570ef;
}
.session-topic-text:active {
  color: #3a88f7;
  transform: scale(0.95);
}
.session-summary-box {
  display: flex;
  flex-direction: row;
  gap: 4px;
  padding: 10px;
  width: calc(100% - 30px);
  height: 40px;
  border-radius: 4px;
  background: #f5f5f5;
  justify-content: space-between;
}
.session-summary-text {
  width: calc(100% - 70px);
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  color: #666666;
}
.session-info-box {
  flex-direction: row;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
}
.session-update-box {
  display: flex;
  flex-direction: row-reverse;
  padding: 10px;
}

.session-update-time-text {
  font-size: 12px;
  font-weight: 400;
  line-height: 20px;
  color: #666666;
}
.session-manage-box {
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 30px;
}
.session-manage-button {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 4px;
  padding: 4px;
  border-radius: 4px;
  cursor: pointer;
}
.session-manage-button:hover {
  background: #f5f5f5;
}
.session-manage-button:active {
  transform: scale(0.95);
}
.session-manage-button-text {
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
  color: #101828;
}
</style>

