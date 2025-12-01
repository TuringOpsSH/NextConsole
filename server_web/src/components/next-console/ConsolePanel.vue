<script setup lang="ts">
import { ArrowDown, ArrowUp, Memo } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { nextTick, onMounted, ref, watch } from 'vue';
import { onBeforeMount } from 'vue-demi';
import { appSearch } from '@/api/app-center';
import { delete_session, search_session, update_session } from '@/api/next-console';
import { session_history_top5 } from '@/components/next-console/messages-flow/sessions';
import router from '@/router';
import { useSessionStore } from '@/stores/sessionStore';
import { useUserConfigStore } from '@/stores/user-config-store';
import { useUserInfoStore } from '@/stores/user-info-store';
import { ISessionItem } from '@/types/next-console';
const sessionStore = useSessionStore();
const userInfoStore = useUserInfoStore();
const userConfigStore = useUserConfigStore();
const showSidebar = ref(true);
const appAreaExpand = ref(true);
const panelWidth = ref('200px');
const currentSessionTopicInputRef = ref();
const sessionButtonsRef = ref(null);
const defaultApp = {
  app_code: 'next_search',
  app_name: userConfigStore.systemConfig?.ai?.xiaoyi?.name || '小亦助手',
  app_icon: userConfigStore.systemConfig?.ai?.xiaoyi?.avatar_url || '/images/logo.svg'
};
const currentApp = ref({
  app_code: 'next_search',
  app_name: '小亦助手',
  app_icon: '/images/logo.svg'
});
const currentAppList = ref([]);
const currentSession = ref<ISessionItem>({
  id: 0,
  session_source: 'next_search',
  session_code: ''
});
const newSessionLoading = ref(false);
async function toAllSession() {
  await router.push({
    name: 'session_history',
    params: {
      sessionSource: currentApp.value?.app_code
    }
  });
  if (window.innerWidth < 768) {
    panelWidth.value = '0px';
  }
}
function switchPanel() {
  showSidebar.value = !showSidebar.value;
  if (panelWidth.value === '0px') {
    if (window.innerWidth < 768) {
      // 手机端
      panelWidth.value = window.innerWidth - 60 + 'px';
    } else {
      panelWidth.value = '200px';
    }
    router.replace({ query: { ...router.currentRoute.value.query, show_panel: 'true' } });
  } else {
    panelWidth.value = '0px';
    router.replace({ query: { ...router.currentRoute.value.query, show_panel: 'false' } });
  }
}
async function panelRewriteSessionTopic(item: ISessionItem) {
  let params = {
    session_id: item.id,
    session_topic: item.session_topic
  };
  let res = await update_session(params);
  if (!res.error_status) {
    await getLastedSession();
    ElMessage.success('修改成功');
  }
}
async function panelDeleteSession(item: ISessionItem) {
  let params = {
    session_id: item.id
  };
  let res = await delete_session(params);
  if (!res.error_status) {
    if (item.session_source == 'next_search') {
      router.push({
        name: 'next_console_welcome_home'
      });
    } else {
      router.push({
        name: 'workbenches',
        params: {
          appCode: item.session_source,
          sessionCode: null
        }
      });
    }
    await getLastedSession();
    ElMessage.success('删除成功');
  }
  for (let i = 0; i < sessionButtonsRef.value.length; i++) {
    sessionButtonsRef.value[i]?.hide();
  }
}
async function focusSessionTopicInput(item: ISessionItem) {
  item.is_edit = true;
  // 在渲染完成后聚焦
  nextTick().then(() => {
    if (currentSessionTopicInputRef.value) {
      currentSessionTopicInputRef.value?.[0].focus();
      for (let i = 0; i < sessionButtonsRef.value.length; i++) {
        sessionButtonsRef.value[i]?.hide();
      }
    }
  });
}
async function switchAppArea() {
  appAreaExpand.value = !appAreaExpand.value;
}
async function getLastedSession() {
  // 获取最新session，并填充至session-list
  const params = {
    page_num: 1,
    page_size: 30,
    session_source: currentApp.value?.app_code
  };
  const data = await search_session(params);
  session_history_top5.value = data.result;
  for (let i = 0; i < session_history_top5.value.length; i++) {
    if (session_history_top5.value[i].session_code == router.currentRoute.value.params?.sessionCode) {
      currentSession.value = session_history_top5.value[i];
      break;
    }
  }
}
async function changeCurrentSession(targetSession: ISessionItem, event: any) {
  if (targetSession?.is_edit) {
    return;
  }
  // 拦截点击更多按钮
  if (
    event &&
    (event.target.className.includes('session-more-button') ||
      event.target.className.includes('el-image__inner') ||
      event.target.className.includes('el-image'))
  ) {
    return;
  }
  currentSession.value = targetSession;
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
async function toAppArea(app: any) {
  currentApp.value = app;
  await getLastedSession();
  try {
    if (session_history_top5.value?.length) {
      await changeCurrentSession(session_history_top5.value[0], null);
    } else {
      if (app.app_code == 'next_search') {
        router.push({
          name: 'next_console_welcome_home'
        });
      } else {
        router.push({
          name: 'workbenches',
          params: {
            appCode: app.app_code,
            sessionCode: null
          }
        });
        // 自动创建新会话
        currentSession.value.session_source = app.app_code;
      }
    }
  } catch (e) {
    console.log(e);
  }
}
async function refreshAppList() {
  const res = await appSearch({
    page_size: 50
  });
  if (!res.error_status) {
    currentAppList.value = res.result.data;
  }
  for (let app of currentAppList.value) {
    if (app.app_code == router.currentRoute.value.params?.appCode) {
      currentApp.value = app;
      currentSession.value.session_source = app.app_code;
      break;
    }
  }
}
async function addNewSession() {
  // 清空当前会话
  if (newSessionLoading.value) {
    ElMessage.info('正在新建会话，请稍候...');
    return;
  }
  if (currentSession.value.session_source == 'next_search' || !currentSession.value) {
    if (router.currentRoute.value.name == 'next_console_welcome_home') {
      ElMessage.success('已经为最新会话啦');
      return;
    }
    await router.push({ name: 'next_console_welcome_home' });
  } else {
    if (router.currentRoute.value.name == 'workbenches') {
      newSessionLoading.value = true;
      if (sessionStore.initAppSessionRef) {
        currentSession.value = await sessionStore.initAppSessionRef(currentApp.value?.app_code, null);
      }
      setTimeout(() => {
        newSessionLoading.value = false;
      }, 5000);
    }
  }
}
defineExpose({
  switchPanel,
  showSidebar,
  panelWidth,
  getLastedSession
});
sessionStore.registerSessionListFn(getLastedSession);
onBeforeMount(() => {
  // 初始化时检查是否需要显示侧边栏
  if (router.currentRoute.value.query.show_panel === 'false') {
    showSidebar.value = false;
    panelWidth.value = '0px';
  } else {
    showSidebar.value = true;
    panelWidth.value = '200px';
  }
  if (router.currentRoute.value.params?.appCode) {
    // @ts-ignore
    currentApp.value.app_code = router.currentRoute.value.params.appCode;
  }
  if (router.currentRoute.value.params?.session_code) {
    currentSession.value.session_code = router.currentRoute.value.params.session_code as string;
  }
});
onMounted(async () => {
  // 检查是否登录
  try {
    if (userInfoStore.token) {
      await refreshAppList();
      await getLastedSession();
    }
  } catch (e) {
    console.error('🚀ConsolePanel.vue', e);
  }
});
watch(
  () => router.currentRoute.value.params?.session_code,
  newCode => {
    if (newCode) {
      currentSession.value.session_code = newCode as string;
    }
  },
  { immediate: true }
);
</script>

<template>
  <div v-show="showSidebar" id="console_panel_box">
    <div id="panel-head">
      <div>
        <el-text style="font-size: 16px; line-height: 24px; font-weight: 600; color: #101828; cursor: default">
          AI 工作台
        </el-text>
      </div>
      <div id="layout_button" @click="switchPanel">
        <el-tooltip effect="light" :content="$t('closeSidebar')" placement="right" :show-after="1500">
          <el-icon>
            <Memo />
          </el-icon>
        </el-tooltip>
      </div>
    </div>
    <div id="app-area">
      <div id="app-area-head">
        <div id="app-area-head-left">
          <div class="app-type-button">
            <el-text class="panel-sub-title">个人应用</el-text>
          </div>
          <el-divider direction="vertical" />
          <div class="app-type-button">
            <el-text class="panel-sub-title">团队应用</el-text>
          </div>
        </div>
        <div class="app-type-button">
          <el-icon v-if="appAreaExpand" @click="switchAppArea">
            <ArrowUp />
          </el-icon>
          <el-icon v-else @click="switchAppArea">
            <ArrowDown />
          </el-icon>
        </div>
      </div>
      <el-scrollbar>
        <div v-show="appAreaExpand" id="app-area-body">
          <div
            class="app-button"
            :class="currentApp?.app_code === defaultApp.app_code ? 'app-button-pick' : ''"
            @click="toAppArea(defaultApp)"
          >
            <div class="std-middle-box">
              <el-image :src="defaultApp.app_icon" class="app-icon" />
            </div>
            <div>
              <el-text style="color: #101828" truncated size="small">{{ defaultApp.app_name }}</el-text>
            </div>
          </div>
          <div
            v-for="app in currentAppList"
            :key="app.app_code"
            class="app-button"
            :class="currentApp?.app_code === app?.app_code ? 'app-button-pick' : ''"
            @click="toAppArea(app)"
          >
            <div class="std-middle-box">
              <el-image :src="app.app_icon" class="app-icon" />
            </div>
            <div>
              <el-text style="color: #101828; width: 120px" truncated size="small">
                {{ app.app_name }}
              </el-text>
            </div>
          </div>
        </div>
      </el-scrollbar>
      <div v-show="appAreaExpand" id="app-area-foot">
        <el-text style="font-size: 12px; cursor: not-allowed">查看全部应用</el-text>
      </div>
    </div>
    <div id="foot-area">
      <div id="add-session-button" @click="addNewSession()">
        <div class="std-middle-box">
          <el-image id="add-session-button-icon" src="/images/plus_circle_white.svg" />
        </div>
        <div>
          <el-text id="add-session-button-text">新建会话</el-text>
        </div>
      </div>
    </div>
    <div id="panel-body">
      <div id="session-history-area">
        <div id="session-history-title">
          <div>
            <el-text class="panel-sub-title">会话历史</el-text>
          </div>
        </div>
        <el-scrollbar>
          <div
            class="session-history-list"
            :style="{ 'max-height': appAreaExpand ? 'calc(100vh - 510px)' : 'calc(100vh - 230px)' }"
          >
            <div
              v-for="item in session_history_top5"
              :key="item.id"
              class="session-item-box"
              :class="{
                'session-item-box-active':
                  currentSession?.session_code == item.session_code && currentSession?.session_code
              }"
              @click="changeCurrentSession(item, $event)"
            >
              <div v-if="item?.is_edit" style="z-index: 999">
                <el-input
                  ref="currentSessionTopicInputRef"
                  v-model="item.session_topic"
                  placeholder="请输入会话名称"
                  @change="panelRewriteSessionTopic(item)"
                />
              </div>
              <div v-else class="session-topic-box">
                <el-text
                  truncated
                  class="session-topic-text"
                  :class="{
                    'session-topic-text-active':
                      currentSession?.session_code == item.session_code && currentSession?.session_code
                  }"
                >
                  {{ item?.session_topic }}
                </el-text>
              </div>
              <div
                v-show="currentSession?.session_code == item.session_code && currentSession?.session_code"
                class="std-middle-box session-more-button"
              >
                <el-popover ref="sessionButtonsRef" trigger="click">
                  <template #reference>
                    <div class="std-middle-box">
                      <el-image src="/images/dot_list_grey.svg" />
                    </div>
                  </template>
                  <div id="session-manage-box">
                    <div class="session-manage-button" @click="focusSessionTopicInput(item)">
                      <div class="std-middle-box">
                        <el-image src="/images/edit_03_grey.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text"> 重命名 </el-text>
                      </div>
                    </div>
                    <el-divider style="margin: 8px 0" />
                    <div class="session-manage-button" @click="panelDeleteSession(item)">
                      <div class="std-middle-box">
                        <el-image src="/images/delete_red.svg" class="session-manage-button-icon" />
                      </div>
                      <div class="std-middle-box">
                        <el-text class="session-manage-button-text" style="color: red"> 删除 </el-text>
                      </div>
                    </div>
                  </div>
                </el-popover>
              </div>
            </div>
          </div>
        </el-scrollbar>
        <div
          v-if="session_history_top5?.length"
          id="more-session-button"
          class="session-item-box"
          @click="toAllSession"
        >
          <el-text style="font-size: 12px"> 查看全部记录...</el-text>
        </div>
        <div v-if="!session_history_top5?.length">
          <el-empty description="暂无会话记录" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
}

#console_panel_box {
  height: 100vh;
  background-color: #f7f7fa;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #eaecf0;
}

#panel-head {
  border-bottom: 1px solid #eaecf0;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 16px;
  background-color: #ffffff;
}

#layout_button {
  cursor: pointer;
  height: 100%;
  display: flex;
  align-items: center;
}

#panel-body {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  height: 100%;
}

#more-session-button {
  cursor: pointer;
}

#add-session-button {
  cursor: pointer;
  background-color: #1570ef;
  display: flex;
  box-shadow: 0 1px 2px 0 #1018280d;
  padding: 8px 12px;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  gap: 8px;
  width: 100%;
}

#add-session-button:hover {
  background-color: #3a88f7;
}

#add-session-button:active {
  transform: scale(0.95);
}

#add-session-button-icon {
  width: 20px;
  height: 20px;
}

#add-session-button-text {
  color: white;
  font-size: 14px;
  line-height: 20px;
  font-weight: 600;
}

#app-area {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 0;
}

#app-area-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 4px 8px;
}

#app-area-head-left {
  display: flex;
  flex-direction: row;
  gap: 8px;
}

.app-type-button {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

#session-history-title {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: flex-start;
}

#session-history-area {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: calc(100% - 16px);
  padding: 0 8px;
  justify-content: space-between;
  height: 100%;
}

.session-item-box {
  display: flex;
  flex-direction: row;
  gap: 8px;
  padding: 4px;
  justify-content: space-between;
  align-items: center;
  border-radius: 8px;
  cursor: pointer;
}

.session-item-box:hover {
  background-color: #f5f8ff;
}

.session-item-box:active {
  background-color: #d9d9d9;
}

.session-item-box-active {
  background-color: #eff6ff;
  border: 1px solid #3b82f6;
}

.session-topic-box {
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  width: calc(100% - 4px);
}

.session-topic-text {
  font-size: 12px;
  line-height: 18px;
  font-weight: 500;
  color: #101828;
}

.session-topic-text-active {
  font-weight: 600;
}

#session-manage-box {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 2px;
  background-color: white;
  border-radius: 8px;
}

.session-manage-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  cursor: pointer;
  width: 100%;
}

.session-manage-button:hover {
  background-color: #f5f8ff;
}

.session-manage-button-icon {
  width: 16px;
  height: 16px;
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

#app-area-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 8px;
  max-height: 200px;
}

.app-button {
  display: inline-flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 6px;
  height: 36px;
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background-color: #ffffff;
  cursor: pointer;
  font-family: 'Segoe UI', sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.app-button :hover {
  background-color: #f9fafb;
  border-color: #9ca3af;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.app-button :active {
  transform: scale(0.98);
}
.app-button-pick {
  background-color: #eff6ff;
  border-color: #3b82f6;
  color: #1d4ed8;
}
.app-button-pick :hover {
  background-color: #dbeafe;
  border-color: #2563eb;
}
.app-icon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
}
.panel-sub-title {
  font-size: 12px;
  cursor: not-allowed;
}

.session-more-button:hover {
  background-color: rgb(209, 233, 255);
  border-radius: 4px;
  z-index: 2;
}
#app-area-foot {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  padding: 8px;
}
#foot-area {
  display: flex;
  flex-direction: row;
  gap: 8px;
  width: calc(100% - 16px);
  align-items: center;
  justify-content: center;
  padding: 8px 8px;
  border-top: 1px solid #d0d5dd;
}
.session-history-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  height: 100%;
}
</style>
