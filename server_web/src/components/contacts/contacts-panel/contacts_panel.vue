<script setup lang="ts">
import { onMounted, ref } from 'vue';
import {
  current_company,
  current_friend_request_cnt,
  init_friend_request_cnt,
  router_to_company_structure,
  router_to_friends,
  router_to_groups_chat,
  switch_panel
} from '@/components/contacts/contacts-panel/contacts_panel';
import UserInviteDialog from '@/components/user-center/UserInviteDialog.vue';
import router from '@/router';
import {get_company_info} from "@/api/contacts";

const showInviteDialogFlag = ref(false);

async function initCurrentCompany() {
  const res = await get_company_info({});
  if (!res.error_status) {
    current_company.value = res.result;
  }
}

onMounted(async () => {
  initCurrentCompany();
  init_friend_request_cnt();
});
</script>

<template>
  <div id="friends_panel_box" @contextmenu.prevent>
    <div id="panel_head">
      <div id="panel_head_left">
        <div class="std-middle-box" style="cursor: pointer" @click="switch_panel()">
          <el-image src="/images/layout_alt.svg" style="width: 16px; height: 16px" />
        </div>
        <div class="std-middle-box" @click="router.push({ name: 'contacts' })">
          <el-text style="font-size: 16px; font-weight: 600; line-height: 24px; color: #101828; cursor: pointer">
            我的通讯录
          </el-text>
        </div>
      </div>
    </div>
    <el-scrollbar>
      <div id="panel_body">
        <div v-if="false" class="contact-type-area" @click="router_to_groups_chat()">
          <div class="contact-type-area-left">
            <div class="std-middle-box">
              <el-image src="/images/group_chat_blue.svg" class="contact-type-icon" />
            </div>
            <div class="std-middle-box">
              <el-text> 群聊 </el-text>
            </div>
          </div>
          <div class="std-middle-box">
            <el-image src="/images/arrow_right_grey.svg" />
          </div>
        </div>
        <el-divider v-if="false" style="margin: 0" />
        <div v-if="current_company?.id" class="contact-type-area" @click="router_to_company_structure()">
          <div class="contact-type-area-left">
            <div class="std-middle-box">
              <el-image
                :src="current_company?.company_logo || '/images/company_default.svg'"
                class="contact-type-icon"
              />
            </div>
            <div class="std-middle-box">
              <el-text>
                {{ current_company?.company_name }}
              </el-text>
            </div>
          </div>
          <div class="std-middle-box">
            <el-image src="/images/arrow_right_grey.svg" />
          </div>
        </div>
        <div v-else class="contact-type-area" @click="router_to_company_structure()">
          <div class="contact-type-area-left">
            <div class="std-middle-box">
              <el-image src="/images/company_default.svg" class="contact-type-icon" />
            </div>
            <div class="std-middle-box">
              <el-text> 企业联系人</el-text>
            </div>
          </div>
          <div class="std-middle-box">
            <el-image src="/images/arrow_right_grey.svg" />
          </div>
        </div>
        <el-divider style="margin: 0" />
        <div class="contact-type-area" @click="router_to_friends()">
          <div class="contact-type-area-left">
            <div class="std-middle-box">
              <el-image src="/images/user_02.svg" class="contact-type-icon" />
            </div>
            <el-badge
              :value="current_friend_request_cnt"
              class="friend-badge"
              :max="99"
              :hidden="!current_friend_request_cnt"
            >
              <div class="std-middle-box" style="padding-right: 12px">
                <el-text> 好友 </el-text>
              </div>
            </el-badge>
          </div>
          <div class="std-middle-box">
            <el-image src="/images/arrow_right_grey.svg" />
          </div>
        </div>

        <div class="contact-type-area" style="justify-content: flex-start" @click="showInviteDialogFlag = true">
          <div class="std-middle-box">
            <el-text style="font-weight: 600; color: #175cd3">+</el-text>
          </div>
          <div class="std-middle-box">
            <el-text style="font-weight: 600; color: #175cd3">邀请好友加入...</el-text>
          </div>
        </div>
      </div>
    </el-scrollbar>
    <UserInviteDialog
      :mode="showInviteDialogFlag"
      @update:mode="
        args => {
          showInviteDialogFlag = args;
        }
      "
    />
  </div>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
}
#friends_panel_box {
  height: 100vh;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 8px -2px #1018281a;
  gap: 4px;
  width: calc(100% - 2px);
}
#panel_head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  gap: 36px;
}
#panel_body {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  width: calc(100% - 24px);
  height: calc(100% - 200px);
}
.contact-type-area {
  display: flex;
  flex-direction: row;
  gap: 4px;
  border-radius: 8px;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px;
  cursor: pointer;
}
.contact-type-area:hover {
  background-color: #f0f0f0;
  border-radius: 8px;
}

.contact-type-area-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.contact-type-icon {
  width: 24px;
  height: 24px;
}
#panel_head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  gap: 36px;
}
#panel_head_left {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: flex-start;
  gap: 4px;
  min-width: 84px;
}
</style>
