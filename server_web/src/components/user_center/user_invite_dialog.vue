<script setup lang="ts">

import {
  copy_invite_link,
  current_invite_type, current_invite_url,
  refresh_confirm_flag, refresh_invite_link,
  show_invite_dialog_flag, user_info
} from "@/components/user_center/user";
import {ElMessage, TabsPaneContext, FormInstance, FormRules} from "element-plus";
import {ref, reactive} from "vue";
import html2canvas from "html2canvas";
import QRCode from "qrcode";
import {get_invite_detail, refresh_invite_code, send_invite_code_by_email} from "@/api/user_center";
import {Search} from "@element-plus/icons-vue";
import {clientFingerprint} from "@/components/global/web_socket/web_socket";


const reset_width= ref(window.innerWidth < 768 ? '90%' : '50%' )
const qrcodeCanvas = ref(null)
function generate_qrcode() {
  const centerImage = new Image();
  centerImage.src = 'images/logo.svg';
  centerImage.onload = () => { // 确保图片加载完成后再绘制
    QRCode.toCanvas(
        qrcodeCanvas.value,
        current_invite_url.value,
        {
          width: 150, // 设置二维码大小
          margin: 4,  // 边距
          errorCorrectionLevel: 'H', // 高纠错级别，便于在中间放置图片
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
    )
  }
}

function handleClick(tab: TabsPaneContext, event: Event){
  if (tab.props.name === 'invite_code'){
    generate_qrcode()
  }
  else if (tab.props.name === 'invite_history'){
    get_invite_history()
  }
}

const captureArea = ref(null)
// 复制邀请二维码
async function copy_invite_qrcode(){
  try {
    const canvas = await html2canvas(captureArea.value);
    canvas.toBlob(async (blob) => {
      const item = new ClipboardItem({ 'image/png': blob });
      await navigator.clipboard.write([item]);
      ElMessage({
        message: '复制成功',
        type: 'success'
      });
    });
  } catch (error) {
    console.error('复制失败', error);
  }
}
async function save_invite_qrcode(){
  const canvas = await html2canvas(captureArea.value);
  const link = document.createElement('a');
  link.href = canvas.toDataURL('image/png');
  link.download = 'qrcode.png';
  link.click();
}
async function refresh_invite_qrcode(){
  let res = await refresh_invite_code({})
  if (!res.error_status) {
    user_info.value.user_invite_code = res.result.user_invite_code
    ElMessage.success({
      message: "刷新成功",
      duration: 1000
    })
    let VITE_APP_NEXT_CONSOLE_PATH = import.meta.env.VITE_APP_NEXT_CONSOLE_PATH
    if (import.meta.env.VITE_APP_NODE_ENV === 'private') {
      VITE_APP_NEXT_CONSOLE_PATH = window.location.protocol + "//" + window.location.host + "/"
    }
    current_invite_url.value = VITE_APP_NEXT_CONSOLE_PATH
        +  "#/invitation?invite_code="
        + user_info.value.user_invite_code
        + "&invite_type=" + current_invite_type.value
    generate_qrcode()
    refresh_confirm_flag.value = false
  }
}

// 邮件邀请
const email_invite_form = reactive({
  user_email : ''
})
const email_invite_form_rules = reactive<FormRules>({
  user_email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱', trigger: ['blur', 'change'] }
  ]
})
const emailInviteFormRef = ref<FormInstance>()


async function send_invite_email(){
    let valid_res = await emailInviteFormRef.value?.validate()
    if (!valid_res) {
      return
    }
    let params = {
      user_email: email_invite_form.user_email,
    }
    let res = await send_invite_code_by_email(params)
    if (!res.error_status) {

      if (res.error_message) {
        ElMessage.info({
          message: res.error_message,
          duration: 3000
        })
        return
      }

      ElMessage.success({
        message: "发送成功",
        duration: 3000
      })

    }

}

const target_user_phone = ref('')
async function send_invite_sms(){
  if (!target_user_phone.value) {
    ElMessage.info({
      message: "请输入邀请手机号",
      duration: 1000
    })
    return
  }

    ElMessage.success({
      message: "发送成功",
      duration: 1000
    })
}

// 邀请历史
const invite_history = ref([])
async function get_invite_history(){
  let params = {
    invite_code: user_info.value.user_invite_code,
    view_user_id : user_info.value.user_id
  }
  let invite_detail_res = await get_invite_detail(params)
  if (!invite_detail_res.error_status){
    invite_history.value = invite_detail_res.result.view_records
  }
}


</script>

<template>
  <el-dialog v-model="show_invite_dialog_flag" title="邀请码" :width="reset_width" draggable top="15vh">
    <el-tabs v-model="current_invite_type"  @tab-click="handleClick">
      <el-tab-pane label="邀请链接" name="invite_link">
        <div class="invite-area">
          <div class="user-info-meta-value user-info-meta-value-disabled" style="max-width: 90%">
            <el-text style="width: 100%">
              {{current_invite_url}}
            </el-text>
          </div>
          <div class="std-middle-box">

            <el-button text  @click="copy_invite_link()" type="primary">
              复制链接
            </el-button>
            <el-button text @click="refresh_confirm_flag=true">
              刷新链接
            </el-button>

          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="邀请二维码" name="invite_code">
        <div class="invite-area">
          <div id="invite-qr-code" ref="captureArea">
            <div  class="std-middle-box">
              <div class="std-middle-box">
                <el-avatar :src="user_info?.user_avatar" v-if="user_info?.user_avatar"/>
                <el-avatar v-else style="background: #D1E9FF">
                  <el-text style="font-weight: 600;color: #1570ef">{{user_info?.user_nick_name_py}}</el-text>
                </el-avatar>
              </div>
              <div>
                <el-text>
                  {{user_info?.user_nick_name}}
                </el-text>
              </div>

            </div>
            <div class="std-middle-box">
              <canvas ref="qrcodeCanvas"></canvas>
            </div>
            <div class="std-middle-box">
              <el-text>扫描二维码，添加我为好友</el-text>
            </div>
          </div>
          <div class="std-middle-box">
            <el-button text type="primary" @click="save_invite_qrcode">
              保存
            </el-button>
            <el-button text type="primary" @click="copy_invite_qrcode">
              复制
            </el-button>
            <el-button text @click="refresh_confirm_flag = true">
              刷新二维码
            </el-button>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="邮件邀请" name="invite_email">
        <div class="invite-area">


          <el-form label-position="top" style="width: 100%" ref="emailInviteFormRef" :model="email_invite_form" status-icon
                   :rules="email_invite_form_rules" :hide-required-asterisk="true">
            <el-form-item prop="user_email" label="收件人">
              <el-input v-model="email_invite_form.user_email" placeholder="请输入邮箱"
                        @keydown.enter.prevent/>
            </el-form-item>
            <el-form-item label="发送内容" style="justify-content: center">
              <div class="user-info-meta-value user-info-meta-value-disabled" style="flex-direction: column;max-width: 90%">
                <el-text>
                  主题：和我一起使用NextConsole
                </el-text>
                <el-divider/>
                <el-text style="width: 100%">
                  {{user_info.user_nick_name}}邀请您一起使用NextConsole，赶快点击链接加入吧！<br/>
                  {{current_invite_url}}
                </el-text>
              </div>
            </el-form-item>

            <el-form-item>
              <div class="std-middle-box" style="width: 100%">
                <el-button text @click="show_invite_dialog_flag=false">
                  取消
                </el-button>
                <el-button type="primary" @click="send_invite_email()">
                  发送
                </el-button>
              </div>

            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>
      <el-tab-pane label="短信邀请" name="invite_sms" v-if="false">
        <div class="invite-area">
          <div class="std-middle-box" style="width: 100%;justify-content: flex-start">
            <el-text>
              收件人：
            </el-text>
          </div>
          <div class="std-middle-box" style="width: 100%;justify-content: flex-start">
            <el-input v-model="target_user_phone" :suffix-icon="Search" placeholder="请输入邀请手机"/>
          </div>
          <div class="std-middle-box" style="width: 100%;justify-content: flex-start">
            <el-text>
              发送内容：
            </el-text>
          </div>
          <div class="user-info-meta-value user-info-meta-value-disabled" style="flex-direction: column">

            <el-text>
              {{user_info.user_nick_name}}邀请您一起使用NextConsole，赶快点击链接加入吧！<br/>
              {{current_invite_url}}
            </el-text>
          </div>
          <div class="std-middle-box">
            <el-button text @click="show_invite_dialog_flag=false">
              取消
            </el-button>
            <el-button type="primary" @click="send_invite_sms()" disabled>
              发送
            </el-button>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="邀请历史" name="invite_history">
        <el-table :data="invite_history" border height="600">
              <el-table-column type="index" width="50" />
          <el-table-column prop="view_user_info" label="查看用户" min-width="180" >
            <template #default="scope">
              <div class="std-middle-box">
                <el-avatar :src="scope.row?.view_user_info?.user_avatar"
                           v-if="scope.row?.view_user_info?.user_avatar" style="width: 32px;height: 32px"/>
                <el-avatar v-else-if="scope.row?.view_user_info?.user_nick_name_py"
                           style="background: #D1E9FF;width: 32px;height: 32px">
                  <el-text style="font-weight: 600;color: #1570ef">
                    {{scope.row?.view_user_info?.user_nick_name_py}}
                  </el-text>
                </el-avatar>
                <el-text>{{scope.row?.view_user_info?.user_nick_name}}</el-text>
              </div>

            </template>
          </el-table-column>
          <el-table-column prop="create_time" label="查看时间" min-width="180" />
              <el-table-column prop="invite_code" label="邀请码" min-width="180" />
              <el-table-column prop="invite_type" label="邀请类型" min-width="120"/>
              <el-table-column prop="view_client_id" label="查看客户端" min-width="120" />
              <el-table-column prop="marketing_code" label="活动代码" min-width="120" />
              <el-table-column prop="finish_task" label="邀请结果" min-width="120" fixed="right">
                <template #default="scope">
                  <div class="std-middle-box" style="width: 100%;gap: 4px;flex-wrap: wrap">
                    <el-tag v-if="scope.row.finish_register" type="success">注册成功</el-tag>
                    <el-tag v-if="scope.row.finish_add_friend" type="success">添加好友成功</el-tag>
                  </div>

                </template>
              </el-table-column>
            </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-dialog>
  <el-dialog v-model="refresh_confirm_flag">
    <el-result title="刷新邀请链接" sub-title="刷新后历史链接将会失效！" icon="warning"
               v-if="current_invite_type=='invite_link'" />
    <el-result title="刷新邀请二维码" sub-title="刷新后历史二维码将会失效！" icon="warning"
               v-if="current_invite_type=='invite_code'" />
    <template #footer>
      <div class="std-middle-box">
        <el-button @click="refresh_confirm_flag = false">取 消</el-button>
        <el-button type="primary" @click="refresh_invite_link" v-if="current_invite_type=='invite_link'">
          刷新链接
        </el-button>
        <el-button type="primary" @click="refresh_invite_qrcode" v-else-if="current_invite_type=='invite_code'">
          刷新二维码
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.std-middle-box{
  display: flex;

  justify-content: center;
  align-items: center;
  height: 100%;
  gap: 12px;
}
.user-info-meta-value{
  display: flex;
  align-items: center;
  border: 1px solid #D0D5DD;
  width: calc(100% - 24px);
  max-width: 420px;
  min-height: 16px;
  box-shadow: 0 1px 2px 0 #1018280D;
  border-radius: 8px;
  padding: 8px 12px;
  gap: 6px;
  margin-left: 6px;

}
.user-info-meta-value-disabled{
  background: #F2F4F7;
  color: #B0BAC5;
}
.invite-area{
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  height: 100%;
  align-items: center;
}
</style>
