<script setup lang="ts">
import Clipboard from 'clipboard';
import { ElMessage, FormInstance, FormRules, TabsPaneContext } from 'element-plus';
import html2canvas from 'html2canvas';
import QRCode from 'qrcode';
import { reactive, ref, watch } from 'vue';
import { getInviteDetail, refreshInviteCode, sendInviteCodeByEmail } from '@/api/user-center';
import { useUserInfoStore } from '@/stores/user-info-store';
import { IUsers } from '@/types/user-center';
const userInfoStore = useUserInfoStore();
const props = defineProps({
  mode: {
    type: Boolean,
    required: true
  }
});
const emits = defineEmits(['update:mode']);

const localMode = ref(false);
const currentInviteType = ref('invite_link');
const currentInviteUrl = ref('');

const refreshConfirmFlag = ref(false);
const resetWidth = ref(window.innerWidth < 768 ? '90%' : '50%');
const qrcodeCanvas = ref(null);
const captureArea = ref(null);
// 邮件邀请
const emailInviteForm = reactive({
  user_email: ''
});
const emailInviteFormRules = reactive<FormRules>({
  user_email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱', trigger: ['blur', 'change'] }
  ]
});
const emailInviteFormRef = ref<FormInstance>();
// 邀请历史
const inviteHistory = ref([]);
function generateQrcode() {
  const centerImage = new Image();
  centerImage.src = '/images/logo.svg';
  centerImage.onload = () => {
    // 确保图片加载完成后再绘制
    QRCode.toCanvas(
      qrcodeCanvas.value,
      currentInviteUrl.value,
      {
        width: 150, // 设置二维码大小
        margin: 4, // 边距
        errorCorrectionLevel: 'H' // 高纠错级别，便于在中间放置图片
      },
      function (error) {
        if (error) {
          console.error(error);
          return;
        }

        // 在二维码中心绘制图片
        const ctx = qrcodeCanvas.value.getContext('2d');
        const imageSize = 24; // 中间图片的大小
        const position = (qrcodeCanvas.value.width - imageSize) / 2;
        // 绘制白色背景矩形
        ctx.fillStyle = 'white';
        ctx.fillRect(position, position, imageSize * 1.1, imageSize * 1.2 * 1.1);
        // 绘制图片
        ctx.drawImage(centerImage, position, position, imageSize, imageSize * 1.2);
      }
    );
  };
}

function handleClick(tab: TabsPaneContext) {
  if (tab.props.name === 'invite_code') {
    generateQrcode();
  } else if (tab.props.name === 'inviteHistory') {
    getInviteHistory();
  }
}

// 复制邀请二维码
async function copyInviteQrcode() {
  try {
    const canvas = await html2canvas(captureArea.value);
    canvas.toBlob(async blob => {
      // eslint-disable-next-line @typescript-eslint/naming-convention
      const item = new ClipboardItem({ 'image/png': blob });
      await navigator.clipboard.write([item]);
      ElMessage({
        message: '复制成功',
        type: 'success'
      });
    });
  } catch (error) {
    console.error('复制失败', error);
    ElMessage({
      message: '复制失败，请使用保存功能',
      type: 'info'
    });
  }
}
async function saveInviteQrcode() {
  const canvas = await html2canvas(captureArea.value);
  const link = document.createElement('a');
  link.href = canvas.toDataURL('image/png');
  link.download = 'qrcode.png';
  link.click();
}
async function refreshInviteQrcode() {
  let res = await refreshInviteCode({});
  if (!res.error_status) {
    userInfoStore.userInfo.user_invite_code = res.result.user_invite_code;
    ElMessage.success({
      message: '刷新成功',
      duration: 1000
    });
    let VITE_APP_NEXT_CONSOLE_PATH = import.meta.env.VITE_APP_NEXT_CONSOLE_PATH;
    if (import.meta.env.VITE_APP_NODE_ENV === 'private') {
      VITE_APP_NEXT_CONSOLE_PATH = window.location.protocol + '//' + window.location.host + '/';
    }
    currentInviteUrl.value =
      VITE_APP_NEXT_CONSOLE_PATH +
      'invitation?invite_code=' +
      userInfoStore.userInfo.user_invite_code +
      '&invite_type=' +
      currentInviteType.value;
    generateQrcode();
    refreshConfirmFlag.value = false;
  }
}

async function sendInviteEmail() {
  const validRes = await emailInviteFormRef.value?.validate();
  if (!validRes) {
    return;
  }
  let params = {
    user_email: emailInviteForm.user_email
  };
  let res = await sendInviteCodeByEmail(params);
  if (!res.error_status) {
    if (res.error_message) {
      ElMessage.info({
        message: res.error_message,
        duration: 3000
      });
      return;
    }

    ElMessage.success({
      message: '发送成功',
      duration: 3000
    });
  }
}
async function getInviteHistory() {
  let params = {
    invite_code: userInfoStore.userInfo.user_invite_code,
    view_user_id: userInfoStore.userInfo.user_id
  };
  let inviteDetailRes = await getInviteDetail(params);
  if (!inviteDetailRes.error_status) {
    inviteHistory.value = inviteDetailRes.result.view_records;
  }
}
function copyInviteLink() {
  Clipboard.copy(currentInviteUrl.value.trim());
  ElMessage({
    message: '复制成功',
    type: 'success',
    duration: 2000
  });
}
async function refreshInviteLink() {
  const res = await refreshInviteCode({});
  if (!res.error_status) {
    userInfoStore.updateUserInfo({ user_invite_code: res.result.user_invite_code } as IUsers);
    ElMessage.success({
      message: '刷新成功',
      duration: 1000
    });
    let VITE_APP_NEXT_CONSOLE_PATH = import.meta.env.VITE_APP_NEXT_CONSOLE_PATH;
    if (import.meta.env.VITE_APP_NODE_ENV === 'private') {
      VITE_APP_NEXT_CONSOLE_PATH = window.location.protocol + '//' + window.location.host + '/';
    }
    currentInviteUrl.value =
      VITE_APP_NEXT_CONSOLE_PATH +
      'invitation?invite_code=' +
      userInfoStore.userInfo.user_invite_code +
      '&invite_type=' +
      currentInviteType.value;
    refreshConfirmFlag.value = false;
  }
}

watch(
  () => props.mode,
  newVal => {
    localMode.value = newVal;
    currentInviteUrl.value =
      window.location.protocol +
      '//' +
      window.location.host +
      '/invitation?invite_code=' +
      userInfoStore.userInfo.user_invite_code +
      '&invite_type=' +
      currentInviteType.value;
  }
);
</script>

<template>
  <el-dialog
    v-model="localMode"
    title="邀请码"
    :width="resetWidth"
    draggable
    top="15vh"
    @closed="emits('update:mode', false)"
  >
    <el-tabs v-model="currentInviteType" @tab-click="handleClick">
      <el-tab-pane label="邀请链接" name="invite_link">
        <div class="invite-area">
          <div class="user-info-meta-value user-info-meta-value-disabled" style="max-width: 90%">
            <el-text style="width: 100%">
              {{ currentInviteUrl }}
            </el-text>
          </div>
          <div class="std-middle-box">
            <el-button text type="primary" @click="copyInviteLink()"> 复制链接 </el-button>
            <el-button text @click="refreshConfirmFlag = true"> 刷新链接 </el-button>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="邀请二维码" name="invite_code">
        <div class="invite-area">
          <div id="invite-qr-code" ref="captureArea">
            <div class="std-middle-box">
              <div class="std-middle-box">
                <el-avatar v-if="userInfoStore.userInfo?.user_avatar" :src="userInfoStore.userInfo?.user_avatar" />
                <el-avatar v-else style="background: #d1e9ff">
                  <el-text style="font-weight: 600; color: #1570ef">
                    {{ userInfoStore.userInfo?.user_nick_name_py }}
                  </el-text>
                </el-avatar>
              </div>
              <div>
                <el-text>
                  {{ userInfoStore.userInfo?.user_nick_name }}
                </el-text>
              </div>
            </div>
            <div class="std-middle-box">
              <canvas ref="qrcodeCanvas" />
            </div>
            <div class="std-middle-box">
              <el-text>扫描二维码，添加我为好友</el-text>
            </div>
          </div>
          <div class="std-middle-box">
            <el-button text type="primary" @click="saveInviteQrcode"> 保存 </el-button>
            <el-button text type="primary" @click="copyInviteQrcode"> 复制 </el-button>
            <el-button text @click="refreshConfirmFlag = true"> 刷新二维码 </el-button>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="邮件邀请" name="invite_email">
        <div class="invite-area">
          <el-form
            ref="emailInviteFormRef"
            label-position="top"
            style="width: 100%"
            :model="emailInviteForm"
            status-icon
            :rules="emailInviteFormRules"
            :hide-required-asterisk="true"
          >
            <el-form-item prop="user_email" label="收件人">
              <el-input v-model="emailInviteForm.user_email" placeholder="请输入邮箱" @keydown.enter.prevent />
            </el-form-item>
            <el-form-item label="发送内容" style="justify-content: center">
              <div
                class="user-info-meta-value user-info-meta-value-disabled"
                style="flex-direction: column; max-width: 90%"
              >
                <el-text> 主题：和我一起使用NextConsole </el-text>
                <el-divider />
                <el-text style="width: 100%">
                  {{ userInfoStore.userInfo.user_nick_name }}邀请您一起使用NextConsole，赶快点击链接加入吧！<br />
                  {{ currentInviteUrl }}
                </el-text>
              </div>
            </el-form-item>

            <el-form-item>
              <div class="std-middle-box" style="width: 100%">
                <el-button text @click="localMode = false"> 取消 </el-button>
                <el-button type="primary" @click="sendInviteEmail"> 发送 </el-button>
              </div>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>
      <el-tab-pane label="邀请历史" name="inviteHistory">
        <el-table :data="inviteHistory" border height="600">
          <el-table-column type="index" width="50" />
          <el-table-column prop="view_user_info" label="查看用户" min-width="180">
            <template #default="scope">
              <div class="std-middle-box">
                <el-avatar
                  v-if="scope.row?.view_user_info?.user_avatar"
                  :src="scope.row?.view_user_info?.user_avatar"
                  style="width: 32px; height: 32px"
                />
                <el-avatar
                  v-else-if="scope.row?.view_user_info?.user_nick_name_py"
                  style="background: #d1e9ff; width: 32px; height: 32px"
                >
                  <el-text style="font-weight: 600; color: #1570ef">
                    {{ scope.row?.view_user_info?.user_nick_name_py }}
                  </el-text>
                </el-avatar>
                <el-text>{{ scope.row?.view_user_info?.user_nick_name }}</el-text>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="create_time" label="查看时间" min-width="180" />
          <el-table-column prop="invite_code" label="邀请码" min-width="180" />
          <el-table-column prop="invite_type" label="邀请类型" min-width="120" />
          <el-table-column prop="view_client_id" label="查看客户端" min-width="120" />
          <el-table-column prop="marketing_code" label="活动代码" min-width="120" />
          <el-table-column prop="finish_task" label="邀请结果" min-width="120" fixed="right">
            <template #default="scope">
              <div class="std-middle-box" style="width: 100%; gap: 4px; flex-wrap: wrap">
                <el-tag v-if="scope.row.finish_register" type="success">注册成功</el-tag>
                <el-tag v-if="scope.row.finish_add_friend" type="success">添加好友成功</el-tag>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-dialog>
  <el-dialog v-model="refreshConfirmFlag">
    <el-result
      v-if="currentInviteType == 'invite_link'"
      title="刷新邀请链接"
      sub-title="刷新后历史链接将会失效！"
      icon="warning"
    />
    <el-result
      v-if="currentInviteType == 'invite_code'"
      title="刷新邀请二维码"
      sub-title="刷新后历史二维码将会失效！"
      icon="warning"
    />
    <template #footer>
      <div class="std-middle-box">
        <el-button @click="refreshConfirmFlag = false">取 消</el-button>
        <el-button v-if="currentInviteType == 'invite_link'" type="primary" @click="refreshInviteLink">
          刷新链接
        </el-button>
        <el-button v-else-if="currentInviteType == 'invite_code'" type="primary" @click="refreshInviteQrcode">
          刷新二维码
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.std-middle-box {
  display: flex;

  justify-content: center;
  align-items: center;
  height: 100%;
  gap: 12px;
}
.user-info-meta-value {
  display: flex;
  align-items: center;
  border: 1px solid #d0d5dd;
  width: calc(100% - 24px);
  max-width: 420px;
  min-height: 16px;
  box-shadow: 0 1px 2px 0 #1018280d;
  border-radius: 8px;
  padding: 8px 12px;
  gap: 6px;
  margin-left: 6px;
}
.user-info-meta-value-disabled {
  background: #f2f4f7;
  color: #b0bac5;
}
.invite-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  height: 100%;
  align-items: center;
}
</style>
