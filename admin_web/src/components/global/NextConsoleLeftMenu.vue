<script setup lang="ts">
import { onMounted, ref, reactive, computed } from 'vue';
import { useRoute } from 'vue-router';
import { domainGet } from '@/api/base';
import { getSystemNotices, getUser, setSystemNoticesRead } from '@/api/user-center';
import router from '@/router';
import { useSystemNoticeStore } from '@/stores/systemNoticeStore';
import { useUserConfigStore } from '@/stores/userConfigStore';
import { useUserInfoStore } from '@/stores/userInfoStore';
import { ISystemNotice } from '@/types/user-center';

const showButtonPop = ref();
const noticeWidth = ref('390px');
const activeSlideBarName = ref('');
const userInfoStore = useUserInfoStore();
const userConfigStore = useUserConfigStore();
const menuData = reactive([
  {
    icon: 'presentation_chart_02_grey.svg',
    active_icon: 'presentation_chart_02_blue.svg',
    text: '监控中心',
    is_active: false,
    name: 'user_activity',
    rootName: 'dashboard'
  },
  {
    icon: 'heart_circle_grey.svg',
    active_icon: 'heart_circle_blue.svg',
    text: '反馈中心',
    is_active: false,
    name: 'search_model',
    rootName: 'feedback'
  },
  {
    icon: 'user_01_grey.svg',
    active_icon: 'user_01_blue.svg',
    text: '用户管理',
    is_active: false,
    name: 'user_center',
    rootName: 'user_center'
  },
  {
    icon: 'app_center_grey.svg',
    active_icon: 'app_center_blue.svg',
    text: 'AI应用工厂',
    is_active: false,
    name: 'appCenter',
    rootName: 'appCenter'
  }
]);
const route = useRoute();
const menuLogo = computed(() => {
  if (userConfigStore.systemConfig?.ops?.brand?.enable) {
    return userConfigStore.systemConfig.ops.brand.logo_url;
  }
  return '/images/logo.svg';
});
const userButtonData = reactive([
  {
    icon: '/images/user_center.svg',
    active_icon: '/images/console_blue.svg',
    text: '用户中心',
    is_active: false,
    name: 'next_console_user_info',
    new_window: false
  },
  {
    icon: menuLogo,
    active_icon: menuLogo,
    text: '服务端',
    is_active: false,
    url: '',
    name: 'server_app',
    new_window: true
  },
  {
    icon: '/images/book-open.svg',
    active_icon: '/images/logo.svg',
    text: '使用文档',
    is_active: false,
    url: 'https://docs.nextconsole.cn',
    name: 'contract',
    new_window: true
  },
  {
    icon: '/images/privacy.svg',
    active_icon: '/images/privacy.svg',
    text: '隐私说明',
    is_active: false,
    name: 'privacy_policy',
    new_window: true
  },
  {
    icon: '/images/documents.svg',
    active_icon: '/images/documents.svg',
    text: '用户协议',
    is_active: false,
    name: 'contract',
    new_window: true
  }
]);
const currentSystemNoticeType = ref('unread');
const unreadNotice = useSystemNoticeStore();
const allSystemNotice = ref<ISystemNotice[]>([]);
const currentPageSize = ref(50);
const currentPageNum = ref(1);

async function chooseMenuItem(item) {
  activeSlideBarName.value = item.rootName;
  await router.push({ name: item.name });
}

async function callUserButton(item) {
  if (item.new_window) {
    if (item?.url) {
      window.open(item.url, '_blank');
      return;
    }
    if (item?.name == 'admin_app') {
      const res = await domainGet();
      const adminDomain = res.result.admin_domain;
      window.open(adminDomain, '_blank');
      return;
    }
    window.open(router.resolve({ name: item.name }).href, '_blank');
  } else {
    await router.push({ name: item.name });
  }

  showButtonPop.value?.hide();
}

function logOut() {
  userInfoStore.$reset();
  router.push({ name: 'login' });
}

async function initSystemNotice() {
  const params = {
    fetch_all: true,
    status: '未读'
  };
  const res = await getSystemNotices(params);
  unreadNotice.updateSystemNotice(res.result);
}

function getNoticeIcon(noticeIconUrl: string) {
  if (!noticeIconUrl) {
    return '';
  }
  if (noticeIconUrl.startsWith('http')) {
    return noticeIconUrl;
  }
  if (noticeIconUrl.startsWith('/images/')) {
    return noticeIconUrl;
  }
  if (noticeIconUrl.includes('data:image')) {
    return noticeIconUrl;
  }

  return '/images/' + noticeIconUrl;
}
async function changeNoticeType(targetType: string = 'unread') {
  currentSystemNoticeType.value = targetType;
  if (targetType == 'unread') {
    const params = {
      fetch_all: true,
      status: '未读'
    };
    const res = await getSystemNotices(params);
    unreadNotice.updateSystemNotice(res.result);
  } else {
    const params = {
      page_size: 50,
      page_num: 1
    };
    const res = await getSystemNotices(params);
    allSystemNotice.value = res.result;
  }
}

async function setNoticeRead(notice: ISystemNotice) {
  const params = {
    notice_id: notice.id
  };
  const res = await setSystemNoticesRead(params);
  if (!res.error_status) {
    notice.notice_status = '已读';
    // 更新消息队列
    if (currentSystemNoticeType.value == 'unread') {
      await changeNoticeType(currentSystemNoticeType.value);
    }
  }
}

async function setAllNoticeRead() {
  const params = {
    read_all: true
  };
  const res = await setSystemNoticesRead(params);
  if (!res.error_status) {
    unreadNotice.updateSystemNotice([]);
  }
}

async function loadMoreNotice() {
  currentPageNum.value += 1;
  const params = {
    page_size: currentPageSize.value,
    page_num: currentPageNum.value
  };
  const res = await getSystemNotices(params);
  for (const notice of res.result) {
    // 只添加不重复的消息
    let isExist = false;
    for (const existNotice of allSystemNotice.value) {
      if (existNotice.id == notice.id) {
        isExist = true;
        break;
      }
    }
    if (!isExist) {
      allSystemNotice.value.push(notice);
    }
  }
}

onMounted(async () => {
  const res = await getUser({});
  if (res.error_status) {
    userInfoStore.$reset();
    router.push({ name: 'login' });
  }
  userInfoStore.updateUserInfo(res.result);
  initSystemNotice();
  const activeItem = menuData.find(item => route.path.replace('next-console', '').includes(item.rootName));
  activeSlideBarName.value = activeItem?.rootName;
  if (window.innerWidth < 768) {
    noticeWidth.value = window.innerWidth - 80 + 'px';
  }
});
</script>

<template>
  <el-container id="next-console-menu">
    <el-header style="padding: 0 !important" height="60px">
      <div id="next-console-logo-box">
        <el-image :src="menuLogo" fit="scale-down" style="height: 40px; width: 40px" />
      </div>
    </el-header>
    <el-main style="padding: 0 !important">
      <div id="menu-box">
        <div
          v-for="item in menuData"
          :key="item.text"
          class="menu-item"
          :class="{ 'menu-item-active': activeSlideBarName === item.rootName }"
          @click="chooseMenuItem(item)"
        >
          <el-tooltip placement="right" effect="light" :auto-close="3000">
            <template #content>
              <div>
                <el-text class="menu-item-text" :class="{ 'menu-item-text-active': item.is_active === true }">
                  {{ item.text }}
                </el-text>
              </div>
            </template>
            <div>
              <el-image
                :src="`/images/${activeSlideBarName === item.rootName ? item.active_icon : item.icon}`"
                class="menu-icon"
              />
            </div>
          </el-tooltip>
        </div>
      </div>
    </el-main>
    <el-footer height="200px" style="padding: 0 !important">
      <div id="next-console-user-box">
        <el-popover trigger="click" placement="right-end" :width="noticeWidth" :hide-after="0">
          <template #reference>
            <div id="user-button-group">
              <el-badge
                :value="unreadNotice.unreadSystemNotice.length"
                :hidden="!unreadNotice.unreadSystemNotice.length"
              >
                <div class="user-button-box">
                  <el-image src="/images/notice_grey.svg" />
                </div>
              </el-badge>
            </div>
          </template>
          <div id="system-notice-area">
            <div id="system-notice-tabs">
              <div
                class="system-notice-tab"
                :class="{ 'system-notice-tab-active': currentSystemNoticeType == 'unread' }"
                @click="changeNoticeType('unread')"
              >
                <el-text
                  class="system-notice-tab-text"
                  :class="{
                    'system-notice-tab-text-active': currentSystemNoticeType == 'unread'
                  }"
                >
                  未读
                </el-text>
              </div>
              <div
                class="system-notice-tab"
                :class="{
                  'system-notice-tab-active': currentSystemNoticeType == 'all'
                }"
                @click="changeNoticeType('all')"
              >
                <el-text
                  class="system-notice-tab-text"
                  :class="{
                    'system-notice-tab-text-active': currentSystemNoticeType == 'all'
                  }"
                >
                  全部
                </el-text>
              </div>
            </div>
            <div
              v-if="unreadNotice.unreadSystemNotice.length > 0 && currentSystemNoticeType == 'unread'"
              id="all-read-button"
              @click="setAllNoticeRead"
            >
              <el-text style="font-weight: 600; font-size: 14px; line-height: 20px; color: #175cd3">
                全部标记为已读
              </el-text>
            </div>
            <el-scrollbar>
              <div style="max-height: 50vh">
                <div v-if="currentSystemNoticeType == 'unread'" class="notice-queue">
                  <div v-for="(notice, idx) in unreadNotice.unreadSystemNotice" :key="idx" class="notice-area">
                    <div class="std-middle-box" style="width: 40px">
                      <el-avatar
                        :src="getNoticeIcon(notice.notice_icon)"
                        style="width: 38px; height: 38px; background-color: white"
                      />
                    </div>
                    <div class="notice-right">
                      <div>
                        <el-text class="notice-title">
                          {{ notice.notice_title }}
                        </el-text>
                      </div>
                      <div v-html="notice.notice_content" />
                      <div class="notice-mark">
                        <div class="std-middle-box" style="cursor: pointer" @click="setNoticeRead(notice)">
                          <el-text class="set-read-button"> 标记为已读 </el-text>
                        </div>
                        <div class="std-middle-box" style="justify-content: flex-start">
                          <el-text style="width: 160px">
                            {{ notice.create_time }}
                          </el-text>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-if="!unreadNotice.unreadSystemNotice.length">
                    <el-empty description="暂无未读站内信" />
                  </div>
                </div>
                <div v-else v-infinite-scroll="loadMoreNotice" class="notice-queue">
                  <div v-for="(notice, idx) in allSystemNotice" :key="idx" class="notice-area">
                    <div class="std-middle-box" style="width: 40px">
                      <el-avatar
                        :src="getNoticeIcon(notice.notice_icon)"
                        style="width: 38px; height: 38px; background-color: white"
                      />
                    </div>
                    <div class="notice-right">
                      <div>
                        <el-text class="notice-title">
                          {{ notice.notice_title }}
                        </el-text>
                      </div>
                      <div v-html="notice.notice_content" />
                      <div class="notice-mark">
                        <div
                          v-if="notice.notice_status == '未读'"
                          class="std-middle-box"
                          style="cursor: pointer; width: 120px"
                          @click="setNoticeRead(notice)"
                        >
                          <el-text class="set-read-button">标记为已读</el-text>
                        </div>
                        <div class="std-middle-box" style="justify-content: flex-start">
                          <el-text>{{ notice.create_time }}</el-text>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-if="!allSystemNotice.length">
                    <el-empty description="暂无站内信" />
                  </div>
                </div>
              </div>
            </el-scrollbar>
          </div>
        </el-popover>

        <el-popover ref="showButtonPop" trigger="click" placement="top-end" width="300px" :hide-after="0">
          <template #reference>
            <div v-if="userInfoStore.userInfo.user_id" id="user-avatar">
              <el-avatar v-if="userInfoStore.userInfo?.user_avatar" :src="userInfoStore.userInfo.user_avatar" />
              <el-avatar v-else style="background: #d1e9ff">
                <el-text style="font-weight: 600; color: #1570ef">
                  {{ userInfoStore.userInfo.user_nick_name_py }}
                </el-text>
              </el-avatar>
            </div>
            <div v-else>
              <el-image src="/images/empty_avatar.svg" style="width: 24px; height: 24px" />
            </div>
          </template>
          <div id="user-button-area">
            <div id="user-button-info">
              <div class="std-middle-box">
                <el-avatar v-if="userInfoStore.userInfo?.user_avatar" :src="userInfoStore.userInfo?.user_avatar" />
                <el-avatar v-else style="background: #d1e9ff">
                  <el-text style="font-weight: 600; color: #1570ef">
                    {{ userInfoStore.userInfo?.user_nick_name_py }}
                  </el-text>
                </el-avatar>
              </div>
              <div id="user-button-info-head">
                <div class="std-middle-box" style="justify-content: flex-start">
                  <el-text truncated>
                    {{ userInfoStore.userInfo?.user_nick_name }}
                  </el-text>
                </div>
                <div class="std-middle-box">
                  <el-text truncated>
                    {{ userInfoStore.userInfo?.user_email }}
                  </el-text>
                </div>
              </div>
            </div>
            <div id="user-button-list">
              <div
                v-for="(item, index) in userButtonData"
                :key="index"
                class="user-button-list-item"
                @click="callUserButton(item)"
              >
                <div class="std-middle-box">
                  <el-image :src="item.icon" class="user-button-icon" />
                </div>
                <div>
                  <el-text>
                    {{ item.text }}
                  </el-text>
                </div>
              </div>
            </div>
            <div id="logo_out_button" @click="logOut">
              <el-image src="/images/logout_red.svg" style="width: 20px; height: 20px" />
              <el-text type="primary">退出登录</el-text>
            </div>
          </div>
        </el-popover>
      </div>
    </el-footer>
  </el-container>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
#next-console-menu {
  height: 100vh;
  width: 100%;
  background: #fcfcfd;
  overflow: hidden;
  border-right: 1px solid #eaecf0;
}
#next-console-logo-box {
  display: flex;
  background: #fcfcfd;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  padding: 8px;
  gap: 6px;
  cursor: pointer;
}
#user-avatar {
  cursor: pointer;
}
#next-console-user-box {
  display: flex;
  flex-direction: column;
  padding: 24px 0;
  gap: 24px;
  align-items: center;
  height: calc(100% - 48px);
  background-color: #fcfcfd;
  justify-content: flex-end;
}
#user-button-group {
  display: flex;
  flex-direction: column;
  padding: 0 12px;
  gap: 8px;
  cursor: pointer;
}
#menu-box {
  padding: 8px 0;
  height: calc(100% - 132px);
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.menu-item {
  width: 28px;
  padding: 6px 8px;
  cursor: pointer;
  border-radius: 8px;
  background-color: #fcfcfd;
  display: flex;
  gap: 12px;
  flex-direction: row;
  align-content: center;
  justify-content: center;
}
.menu-item:hover {
  background-color: #eff8ff;
}
.menu-item-active {
  background-color: #eff8ff;
  transform: scale(0.95);
}
.menu-icon {
  width: 24px;
  height: 24px;
}
.menu-item-text {
  font-size: 14px;
  font-weight: 500;
  line-height: 24px;
  color: #101828;
}
.menu-item-text-active {
  color: #409eff;
}
#user-button-area {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
#user-button-info-head {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: calc(100% - 42px);
}
#user-button-info {
  display: flex;
  flex-direction: row;
  gap: 8px;
  background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
  padding: 8px;
}
#user-button-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 8px;
}

#logo_out_button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px;
  border-radius: 8px;
  background-color: #fcfcfd;
  cursor: pointer;
}
#logo_out_button:hover {
  background-color: #ffffff;
}
#logo_out_button:active {
  background-color: #fcfcfd;
  transform: scale(0.95);
}
.user-button-list-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;

  gap: 8px;
  padding: 8px;
  border-radius: 8px;
  background-color: #fcfcfd;
  cursor: pointer;
}
.user-button-list-item:hover {
  background-color: #ffffff;
}
.user-button-list-item:active {
  background-color: #fcfcfd;
  transform: scale(0.95);
}
.user-button-icon {
  width: 28px;
  height: 28px;
}
#system-notice-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 4px;
}
#system-notice-tabs {
  display: flex;
  flex-direction: row;
  background-color: #f9fafb;
  border: 1px solid #eaecf0;
  border-radius: 8px;
  align-content: center;
  justify-content: space-between;
  gap: 8px;
  padding: 4px;
}
.system-notice-tab {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 6px;
  width: calc(100% - 24px);
}
.system-notice-tab-active {
  background-color: white;
  box-shadow: 0 1px 3px 0 #1018281a;
}

.system-notice-tab-text {
  font-weight: 600;
  font-size: 14px;
  line-height: 20px;
  color: #667085;
}
.system-notice-tab-text-active {
  color: #344054;
}
#all-read-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border-radius: 8px;
  background-color: #eff8ff;
  border: 1px solid #b2ddff;
  cursor: pointer;
  box-shadow: 0 1px 2px 0 #1018280d;
}
.notice-queue {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.notice-area {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  border: 1px solid #eaecf0;
  padding: 16px;
  gap: 16px;
}
.notice-right {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}
.notice-title {
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  color: #101828;
}
.set-read-button {
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  color: #175cd3;
  width: 80px;
}
.notice-mark {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}
@media (width< 768px) {
  .notice-mark {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }
}
</style>
