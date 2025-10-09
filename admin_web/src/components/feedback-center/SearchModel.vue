<script setup lang="ts">
import { Search, Setting, HomeFilled } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { adminFavorite, getSessionHistoryMsg, searchSessionLog, searchSessionSourceAPI } from '@/api/feedback_center';
import MessageFlowV2 from '@/components/app-center/app-preview/MessageFlowV2.vue';
import { IMsgQueueItem, ISessionItem } from '@/types/next-console';

const route = useRoute();
const currentIndex = route.path;
const filteredComponents = ref([
  {
    name: 'AI工作台',
    url: '/feedback/search_model'
  }
]);
const currentSessionLogList = ref<ISessionItem[]>([]);
const currentSessionTotal = ref(0);
const currentSessionPageSize = ref(100);
const currentSessionPageNum = ref(1);
const upSessionIconHover = ref(false);
const downSessionIconHover = ref(false);
const currentSessionSource = ref([]);
const sessionLoading = ref(false);
const targetSessionTopic = ref('');
const availableSessionSource = ref([]);
const targetSessionRemark = ref(null);
const targetSessionFavorite = ref(null);
const targetSessionTimeRange = ref('');
const targetSessionUser = ref();
const targetSessionTag = ref('');
const currentSession = ref();
const msgFlowRef = ref();
const viewField = ref([
  '会话id',
  '会话来源',
  '用户id',
  '会话标题',
  'QA数',
  '消耗Token数',
  '更新时间',
  '用户反馈',
  '用户收藏'
]);
const SessionHistoryMsgList = ref<IMsgQueueItem[]>([]);
const SessionTimeRangeShortCuts = [
  {
    text: '上周',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
      return [start, end];
    }
  },
  {
    text: '上个月',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
      return [start, end];
    }
  },
  {
    text: '上季度',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
      return [start, end];
    }
  }
];
const showSessionHistoryMsg = ref(false);
const targetSession = ref<ISessionItem>();
async function handleSizeChange(val: number) {
  currentSessionPageSize.value = val;
  await getSessionLog();
}
async function handleCurrentChange(val: number) {
  currentSessionPageNum.value = val;
  await getSessionLog();
}
async function getSessionLog() {
  const params = {
    page_num: currentSessionPageNum.value,
    page_size: currentSessionPageSize.value
  };
  if (targetSessionRemark.value !== null && targetSessionRemark.value !== '') {
    params['session_remark'] = targetSessionRemark.value;
  }
  if (targetSessionFavorite.value !== null && targetSessionFavorite.value !== '') {
    params['session_favorite'] = targetSessionFavorite.value;
  }
  if (targetSessionTimeRange.value) {
    params['create_start_date'] = formatDateToUTC8(targetSessionTimeRange.value[0]);
    params['create_end_date'] = formatDateToUTC8(targetSessionTimeRange.value[1]);
  }
  if (targetSessionTopic.value !== '') {
    params['session_topic'] = targetSessionTopic.value;
  }
  if (targetSessionTag.value !== '') {
    params['tag'] = targetSessionTag.value;
  }
  if (targetSessionUser.value) {
    params['session_user_id'] = targetSessionUser.value;
  }
  if (currentSessionSource.value) {
    params['session_source'] = currentSessionSource.value.map(item => item.app_code);
  }
  sessionLoading.value = true;
  const res = await searchSessionLog(params);
  if (!res.error_status) {
    currentSessionLogList.value = res.result.data;
    currentSessionTotal.value = res.result.total;
  }
  sessionLoading.value = false;
}
function formatDateToUTC8(date) {
  return new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
    .format(date)
    .replace(/\//g, '-')
    .replace(/,/g, '');
}
async function favoriteHistorySession() {
  if (targetSession.value.admin_session_favorite === 0) {
    targetSession.value.admin_session_favorite = 1;
  } else {
    targetSession.value.admin_session_favorite = 0;
  }

  const params = {
    admin_session_favorite: targetSession.value.admin_session_favorite,
    session_id: targetSession.value.id
  };
  const res = await adminFavorite(params);
  if (!res.error_status) {
    ElMessage.success('操作成功');
    await getSessionLog();
  }
}
async function upCheckTargetSession() {
  // 向上查找上一个session,并且展示,如果没有则提示
  const index = currentSessionLogList.value.indexOf(targetSession.value);
  if (index === 0 && currentSessionPageNum.value === 1) {
    ElMessage.warning('已经是第一个了');
    return;
  }
  if (index === 0 && currentSessionPageNum.value !== 1) {
    currentSessionPageNum.value = currentSessionPageNum.value - 1;
    await getSessionLog();
    targetSession.value = currentSessionLogList.value[currentSessionLogList.value.length - 1];
    return;
  }
  targetSession.value = currentSessionLogList.value[index - 1];
  const params = {
    session_id: targetSession.value.id
  };
  const res = await getSessionHistoryMsg(params);
  if (!res.error_status) {
    SessionHistoryMsgList.value = res.result;
  }
}
async function downCheckTargetSession() {
  // 向下查找下一个session,并且展示,如果没有则提示
  const index = currentSessionLogList.value.indexOf(targetSession.value);
  if (
    index === currentSessionLogList.value.length - 1 &&
    currentSessionPageNum.value === Math.ceil(currentSessionTotal.value / currentSessionPageSize.value)
  ) {
    ElMessage.warning('已经是最后一个了');
    return;
  }
  if (
    index === currentSessionLogList.value.length - 1 &&
    currentSessionPageNum.value !== Math.ceil(currentSessionTotal.value / currentSessionPageSize.value)
  ) {
    currentSessionPageNum.value = currentSessionPageNum.value + 1;
    await getSessionLog();
    targetSession.value = currentSessionLogList.value[0];
    return;
  }
  targetSession.value = currentSessionLogList.value[index + 1];
  const params = {
    session_id: targetSession.value.id
  };
  const res = await getSessionHistoryMsg(params);
  if (!res.error_status) {
    SessionHistoryMsgList.value = res.result;
  }
}
async function showSessionMsg(targetSession: ISessionItem) {
  showSessionHistoryMsg.value = true;
  if (!targetSession) {
    return;
  }
  if (targetSession == currentSession.value) {
    await msgFlowRef.value?.refreshMsgFlow();
    return;
  }
  currentSession.value = targetSession;
}
async function searchSessionSource(query: string) {
  const params = {
    keyword: query
  };
  const res = await searchSessionSourceAPI(params);
  if (!res.error_status) {
    availableSessionSource.value = res.result.data;
  }
}
onMounted(async () => {
  await getSessionLog();
});
</script>

<template>
  <el-container style="height: 100vh">
    <el-header height="61px">
      <div class="next-console-admin-header">
        <div class="component-box">
          <el-menu :default-active="currentIndex" class="el-menu-demo" mode="horizontal" router :ellipsis="false">
            <el-menu-item
              v-for="component in filteredComponents"
              :key="component.url"
              :index="component.url"
              class="menu-header-item"
            >
              <el-icon><HomeFilled /></el-icon>
              <span>{{ component.name }}</span>
            </el-menu-item>
          </el-menu>
        </div>
      </div>
    </el-header>
    <el-main>
      <div class="main-area">
        <div class="condition-area">
          <div class="condition-area-left">
            <el-text class="next-console-font-bold" style="width: 120px"> 会话日志 </el-text>
          </div>
          <div class="condition-area-right">
            <div style="width: 120px">
              <el-select
                v-model="currentSessionSource"
                placeholder="会话来源"
                clearable
                multiple
                filterable
                remote
                value-key="id"
                :remote-method="searchSessionSource"
                @change="getSessionLog"
              >
                <el-option v-for="item in availableSessionSource" :key="item.id" :label="item.app_name" :value="item" />
              </el-select>
            </div>
            <div style="width: 120px">
              <el-input
                v-model="targetSessionUser"
                style="width: 120px"
                placeholder="用户id(数字)"
                clearable
                @change="getSessionLog"
              />
            </div>
            <div style="width: 120px">
              <el-select v-model="targetSessionRemark" placeholder="会话评价" clearable @change="getSessionLog">
                <el-option :value="-1" label="点踩" />
                <el-option :value="0" label="未评价" />
                <el-option :value="1" label="点赞" />
              </el-select>
            </div>
            <div style="width: 120px">
              <el-select v-model="targetSessionFavorite" placeholder="会话收藏" clearable @change="getSessionLog">
                <el-option :value="0" label="未收藏" />
                <el-option :value="1" label="收藏" />
              </el-select>
            </div>
            <div style="width: 380px">
              <el-date-picker
                v-model="targetSessionTimeRange"
                style="width: 350px"
                type="datetimerange"
                :shortcuts="SessionTimeRangeShortCuts"
                range-separator="至"
                start-placeholder="开始时间"
                end-placeholder="截止时间"
                @change="getSessionLog"
              />
            </div>
            <div style="width: 180px">
              <el-input
                v-model="targetSessionTopic"
                placeholder="搜索会话标题"
                :prefix-icon="Search"
                clearable
                @change="getSessionLog"
              />
            </div>
            <div style="width: 180px">
              <el-input
                v-model="targetSessionTag"
                placeholder="搜索会话标签"
                clearable
                :prefix-icon="Search"
                @change="getSessionLog"
              />
            </div>
            <div>
              <el-popover trigger="click" placement="bottom" width="300">
                <template #reference>
                  <el-button size="small" :icon="Setting" circle />
                </template>
                <el-checkbox-group v-model="viewField">
                  <el-checkbox
                    v-for="item in [
                      '会话id',
                      '会话来源',
                      '用户id',
                      '会话标题',
                      'QA数',
                      '消耗Token数',
                      '更新时间',
                      '用户反馈',
                      '用户收藏'
                    ]"
                    :key="item"
                    :value="item"
                  >
                    {{ item }}
                  </el-checkbox>
                </el-checkbox-group>
              </el-popover>
            </div>
          </div>
        </div>
        <div v-loading="sessionLoading" element-loading-text="加载中..." style="margin-top: 12px; width: 100%">
          <el-table :data="currentSessionLogList" show-overflow-tooltip border stripe height="calc(100vh - 200px)">
            <el-table-column type="selection" width="55" />
            <el-table-column v-if="viewField.includes('会话id')" prop="id" label="会话id" width="100" sortable />
            <el-table-column v-if="viewField.includes('会话来源')" prop="session_source" label="会话来源" width="280">
              <template #default="{ row }">
                <div v-if="row.session_source" class="session_source">
                  <div>
                    <el-image v-if="row.session_source.app_icon" :src="row.session_source.app_icon" class="app-icon" />
                  </div>
                  <el-popover width="300px" :content="row.session_source.app_code">
                    <template #reference>
                      {{ row.session_source.app_name }}
                    </template>
                  </el-popover>
                </div>
              </template>
            </el-table-column>
            <el-table-column v-if="viewField.includes('用户id')" prop="user_id" label="用户id" width="100" sortable />
            <el-table-column v-if="viewField.includes('会话标题')" prop="session_topic" label="会话标题" />
            <el-table-column v-if="viewField.includes('QA数')" prop="qa_cnt" label="QA数" min-width="100" sortable />
            <el-table-column
              v-if="viewField.includes('消耗Token数')"
              prop="msg_token_used"
              label="消耗Token数"
              min-width="120"
              sortable
            />
            <el-table-column
              v-if="viewField.includes('更新时间')"
              prop="update_time"
              label="更新时间"
              width="180"
              sortable
            />
            <el-table-column v-if="viewField.includes('用户反馈')" prop="session_remark" label="用户反馈">
              <template #default="{ row }">
                <el-tag v-if="row.session_remark == -1" type="danger" round> 点踩 </el-tag>
                <el-tag v-if="row.session_remark == 0" type="info" round> 未评价 </el-tag>
                <el-tag v-if="row.session_remark == 1" type="success" round> 点赞 </el-tag>
              </template>
            </el-table-column>
            <el-table-column v-if="viewField.includes('用户收藏')" prop="session_favorite" label="用户收藏">
              <template #default="{ row }">
                <el-image
                  v-if="row.session_favorite == 1"
                  style="width: 24px; height: 24px"
                  src="/images/star_icon_yellow.svg"
                />

                <el-image
                  v-else-if="row.session_favorite == 0"
                  style="width: 24px; height: 24px"
                  src="/images/star_icon_grey.svg"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" fixed="right">
              <template #default="{ row }">
                <div style="cursor: pointer" @click="showSessionMsg(row)">
                  <el-image style="width: 20px; height: 20px" src="/images/icon_circle_grey.svg" />
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
      <el-drawer v-model="showSessionHistoryMsg" size="50%">
        <template #header>
          <div
            v-if="targetSession"
            style="
              width: 100%;
              display: flex;
              flex-direction: row;
              justify-content: space-between;
              align-content: center;
            "
          >
            <div class="next-console-div">
              <div>
                <el-text class="next-console-font-bold">{{ targetSession.session_topic }}</el-text>
              </div>
              <div>
                <div style="cursor: pointer" @click="favoriteHistorySession()">
                  <el-image
                    v-if="targetSession.admin_session_favorite == 1"
                    src="/images/star_icon_yellow.svg"
                    style="width: 24px; height: 24px"
                  />
                  <el-image v-else src="/images/star_icon_grey.svg" style="width: 24px; height: 24px" />
                </div>
              </div>
            </div>
            <div class="next-console-div">
              <div
                class="next-console-div"
                @mouseenter="upSessionIconHover = true"
                @mouseleave="upSessionIconHover = false"
                @click="upCheckTargetSession"
              >
                <el-image
                  v-if="upSessionIconHover"
                  src="/images/arrow_up_blue.svg"
                  style="width: 14px; height: 14px; cursor: pointer"
                />

                <el-image v-else src="/images/arrow_up_grey.svg" style="width: 14px; height: 14px; cursor: pointer" />
              </div>
              <div
                class="next-console-div"
                @mouseenter="downSessionIconHover = true"
                @mouseleave="downSessionIconHover = false"
                @click="downCheckTargetSession"
              >
                <el-image
                  v-if="downSessionIconHover"
                  src="/images/arrow_down_blue.svg"
                  style="width: 14px; height: 14px; cursor: pointer"
                />
                <el-image v-else src="/images/arrow_down_grey.svg" style="width: 14px; height: 14px; cursor: pointer" />
              </div>
            </div>
          </div>
        </template>
        <MessageFlowV2
          ref="msgFlowRef"
          :session-code="currentSession.session_code"
          :height="'calc(100vh - 300px)'"
          :debug="true"
          style="width: 100%"
        />
      </el-drawer>
    </el-main>
    <el-footer>
      <div class="kg-pagination">
        <el-pagination
          size="small"
          layout=" total, sizes, prev, pager, next, jumper"
          :total="currentSessionTotal"
          :page-sizes="[50, 100, 200, 500]"
          :page-size="currentSessionPageSize"
          :current-page="currentSessionPageNum"
          @update:page-size="handleSizeChange"
          @update:current-page="handleCurrentChange"
        />
      </div>
    </el-footer>
  </el-container>
</template>

<style scoped>
.el-header {
  --el-header-padding: 0 !important;
}
.main-area {
  height: calc(100vh - 170px);
  width: 100%;
}
.condition-area {
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
}
.condition-area-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}
.condition-area-right {
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: flex-end;
  gap: 8px;
  flex-wrap: wrap;
}
.kg-pagination {
  display: flex;
  justify-content: center;
  align-content: center;
  width: 100%;
  height: 100%;
}
.session_source {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  width: 100%;
  height: 30px;
}
.app-icon {
  width: 24px;
  height: 24px;
}
.app-name-text {
  width: 100px;
  font-size: 14px;
  line-height: 20px;
  font-weight: 400;
  height: 30px;
}
</style>
