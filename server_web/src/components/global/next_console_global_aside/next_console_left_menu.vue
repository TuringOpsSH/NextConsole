<script setup lang="ts">
import router from '@/router';
import {user_info} from '@/components/user_center/user';
import {onMounted, ref, watch} from 'vue';
import {getInfo, login_out} from '@/utils/auth';
import {useRoute} from 'vue-router';
import {
  all_system_notice,
  change_notice_type,
  current_system_notice_type,
  get_notice_icon,
  init_system_notice,
  load_more_notice,
  menu_data as menuData,
  set_all_notice_read,
  set_notice_read,
  unread_system_notice,
  user_button_data
} from '@/components/global/next_console_global_aside/menu_data';
import {addNewSession} from '@/components/next_console/messages_flow/sessions';
const route = useRoute();
const showButtonPop = ref();
const noticeWidth = ref('390px');
const activeSlideBarName = ref('');
onMounted(async () => {
  user_info.value = await getInfo(true);
  init_system_notice();
  const activeItem = menuData.find(item => route.path.replace('next_console', '').includes(item.rootName));
  activeSlideBarName.value = activeItem?.rootName;
  if (window.innerWidth < 768) {
    noticeWidth.value = window.innerWidth - 80 + 'px';
  }
});
watch(
    () => route.path,
    newVal => {
      const activeItem = menuData.find(item => newVal.replace('next_console', '').includes(item.rootName));
      activeSlideBarName.value = activeItem?.rootName;
    }
);

async function chooseMenuItem(item) {
  await router.push({ name: item.name });
}

async function callUserButton(item) {
  if (item.new_window) {
    window.open(router.resolve({ name: item.name }).href, '_blank');
  } else {
    await router.push({ name: item.name });
  }

  showButtonPop.value?.hide();
}
</script>

<template>
  <el-container id="next-console-menu">
    <el-header style="padding: 0 !important" height="60px">
      <div id="next-console-logo-box" @click="addNewSession()">
        <el-image src="images/logo.svg" fit="scale-down" style="height: 40px; width: 40px" />
      </div>
    </el-header>
    <el-main style="padding: 0 !important">
      <div id="menu-box">
        <div
            v-for="(item, index) in menuData"
            :key="index"
            class="menu-item"
            :class="{ 'menu-item-active': activeSlideBarName === item.rootName }"
            @click="chooseMenuItem(item)"
        >
          <el-tooltip placement="right" effect="light" :auto-close="3000">
            <template #content>
              <div>
                <el-text
                    class="menu-item-text"
                    :class="{ 'menu-item-text-active': activeSlideBarName === item.rootName }"
                >
                  {{ item.text }}
                </el-text>
              </div>
            </template>
            <div>
              <el-image
                  :src="`images/${activeSlideBarName === item.rootName ? item.active_icon : item.icon}`"
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
              <el-badge :value="unread_system_notice.length" :hidden="!unread_system_notice.length">
                <div class="user-button-box">
                  <el-image src="images/notice_grey.svg" />
                </div>
              </el-badge>
            </div>
          </template>
          <div id="system-notice-area">
            <div id="system-notice-tabs">
              <div
                  class="system-notice-tab"
                  :class="{ 'system-notice-tab-active': current_system_notice_type == 'unread' }"
                  @click="change_notice_type('unread')"
              >
                <el-text
                    class="system-notice-tab-text"
                    :class="{
                    'system-notice-tab-text-active': current_system_notice_type == 'unread'
                  }"
                >
                  未读
                </el-text>
              </div>
              <div
                  class="system-notice-tab"
                  @click="change_notice_type('all')"
                  :class="{
                  'system-notice-tab-active': current_system_notice_type == 'all'
                }"
              >
                <el-text
                    class="system-notice-tab-text"
                    :class="{
                    'system-notice-tab-text-active': current_system_notice_type == 'all'
                  }"
                >
                  全部
                </el-text>
              </div>
            </div>
            <div
                v-if="unread_system_notice.length > 0 && current_system_notice_type == 'unread'"
                id="all-read-button"
                @click="set_all_notice_read()"
            >
              <el-text style="font-weight: 600; font-size: 14px; line-height: 20px; color: #175cd3">
                全部标记为已读
              </el-text>
            </div>
            <el-scrollbar>
              <div style="max-height: 50vh">
                <div v-if="current_system_notice_type == 'unread'" class="notice-queue">
                  <div v-for="(notice, idx) in unread_system_notice" :key="idx" class="notice-area">
                    <div class="std-middle-box" style="width: 40px">
                      <el-avatar
                          :src="get_notice_icon(notice.notice_icon)"
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
                        <div class="std-middle-box" style="cursor: pointer" @click="set_notice_read(notice)">
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
                  <div v-if="!unread_system_notice.length">
                    <el-empty description="暂无未读站内信" />
                  </div>
                </div>
                <div v-else class="notice-queue" v-infinite-scroll="load_more_notice">
                  <div v-for="(notice, idx) in all_system_notice" :key="idx" class="notice-area">
                    <div class="std-middle-box" style="width: 40px">
                      <el-avatar
                          :src="get_notice_icon(notice.notice_icon)"
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
                            @click="set_notice_read(notice)"
                        >
                          <el-text class="set-read-button">标记为已读</el-text>
                        </div>
                        <div class="std-middle-box" style="justify-content: flex-start">
                          <el-text>{{ notice.create_time }}</el-text>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-if="!all_system_notice.length">
                    <el-empty description="暂无站内信" />
                  </div>
                </div>
              </div>
            </el-scrollbar>
          </div>
        </el-popover>

        <el-popover ref="showButtonPop" trigger="click" placement="top-end" width="300px" :hide-after="0">
          <template #reference>
            <div v-if="user_info?.user_id" id="user-avatar">
              <el-avatar v-if="user_info?.user_avatar" :src="user_info?.user_avatar" />
              <el-avatar v-else style="background: #d1e9ff">
                <el-text style="font-weight: 600; color: #1570ef">{{ user_info?.user_nick_name_py }}</el-text>
              </el-avatar>
            </div>
            <div v-else>
              <el-image src="images/empty_avatar.svg" style="width: 24px; height: 24px" />
            </div>
          </template>
          <div id="user-button-area">
            <div id="user-button-info">
              <div class="std-middle-box">
                <el-avatar v-if="user_info?.user_avatar" :src="user_info?.user_avatar" />
                <el-avatar v-else style="background: #d1e9ff">
                  <el-text style="font-weight: 600; color: #1570ef">{{ user_info?.user_nick_name_py }}</el-text>
                </el-avatar>
              </div>
              <div id="user-button-info-head">
                <div class="std-middle-box" style="justify-content: flex-start">
                  <el-text truncated>
                    {{ user_info?.user_nick_name }}
                  </el-text>
                </div>
                <div class="std-middle-box">
                  <el-text truncated>
                    {{ user_info?.user_email }}
                  </el-text>
                </div>
              </div>
            </div>
            <div id="user-button-list">
              <div
                  v-for="(item, index) in user_button_data"
                  :key="index"
                  class="user-button-list-item"
                  @click="callUserButton(item)"
              >
                <div class="std-middle-box">
                  <el-image :src="'images/' + item.icon" class="user-button-icon" />
                </div>
                <div>
                  <el-text>
                    {{ item.text }}
                  </el-text>
                </div>
              </div>
            </div>
            <div id="logo_out_button" @click="login_out">
              <el-image src="images/logout_red.svg" style="width: 20px; height: 20px" />
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
