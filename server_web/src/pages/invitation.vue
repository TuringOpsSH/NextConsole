<script setup lang="ts">
import { ref, onMounted } from 'vue'
import router from "@/router";
import {accept_invite_friend, get_invite_detail, update_invite_status} from "@/api/user_center";
import {user_info} from "@/components/user_center/user";
import {Users} from "@/types/users";
import {clientFingerprint, getFingerPrint} from "@/components/global/web_socket/web_socket";
import {getInfo} from "@/utils/auth";
const show_flag = true
const reset_width= ref(  window.innerWidth > 768 ? '50%' : '90%')
const props = defineProps ({
  invite_code: {
    type: String,
    default: '',
    required: false
  },
  invite_type:{
    type: String,
    default: 'invite_link',
    required: false
  },
  marketing_code:{
    type: String,
    default: '',
    required: false
  }
})
const invitor = ref<Users>({})
async function router_to_create(){
  // 更新邀请状态
  let params = {
    view_user_id: user_info.value?.user_id,
    view_client_id: clientFingerprint.value,
    invite_view_id: invitor.value?.view_record_id,
    begin_register: true
  }
  let res = await update_invite_status(params)
  router.push({
    name: 'login',
    query: {
      invite_view_id: invitor.value?.view_record_id,
    }
  })
}

async function router_to_add_friend(){
  // 更新邀请状态
  let params = {
    view_user_id: user_info.value?.user_id,
    view_client_id: clientFingerprint.value,
    invite_view_id: invitor.value?.view_record_id,
    begin_add_friend: true
  }
  let res = await update_invite_status(params)
  router.push({
    name: 'login',
    query: {
      invite_view_id: invitor.value?.view_record_id,
    }
  })
}

async function router_to_accept_friend(){
  let params = {
    invite_view_id: invitor.value?.view_record_id,
  }
  let res = await accept_invite_friend(params)
  if (!res.error_status){
    router.push({
      name: 'friends'
    })
  }
}

onMounted(async () => {
  // 加载邀请码详情
  if (!props.invite_code){
    console.log('邀请码为空')
    router.push({
      name: 'next_console_welcome_home'
    })
    return
  }
  user_info.value = await getInfo()
  if( !clientFingerprint.value){
    await getFingerPrint()
  }
  let params = {
    invite_code: props.invite_code,
    invite_type: props.invite_type,
    marketing_code: props.marketing_code,
    view_user_id : user_info.value?.user_id,
    view_client_id: clientFingerprint.value
  }
  let invite_detail_res = await get_invite_detail(params)
  if (!invite_detail_res.error_status){
    invitor.value = invite_detail_res.result

  }

})
</script>

<template>
  <div style="padding: 24px">
    <el-image src="images/logo_text.svg"/>
  </div>
  <el-dialog v-model="show_flag" title="邀请新好友" :width="reset_width" :show-close="false" :modal="false"
             top="150px" :close-on-click-modal="false" :close-on-press-escape="false" >

    <div id="invite-area" v-if="invitor?.user_id">
      <div id="invite-info">
        <div class="std-middle-box">
          <el-avatar :src="invitor?.user_avatar" v-if="invitor?.user_avatar" style="width: 88px;height: 88px"/>
          <el-avatar v-else style="background: #D1E9FF;width: 88px;height: 88px">
            <el-text style="font-weight: 600;color: #1570ef">{{invitor?.user_nick_name_py}}</el-text>
          </el-avatar>
        </div>
        <div class="std-middle-box">
          <el-text style="font-size: 24px;font-weight: 600;color: black">
            {{invitor.user_nick_name}}
          </el-text>
        </div>
      </div>

      <div v-if="user_info?.user_id == invitor?.user_id">
         <el-table :data="invitor.view_records" border height="600">
              <el-table-column type="index" width="50" />
              <el-table-column prop="invite_code" label="邀请码" min-width="180" />
              <el-table-column prop="invite_type" label="邀请类型" min-width="120"/>
              <el-table-column prop="view_user_info" label="查看用户" min-width="180" >
                <template #default="scope">
                  <div class="std-middle-box" style="gap: 4px">
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
              <el-table-column prop="view_client_id" label="查看客户端" min-width="120" />
              <el-table-column prop="create_time" label="查看时间" min-width="180" />
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
      </div>
      <div v-else>
        <div v-if="!user_info?.user_id" id="invite-intro">
          <div class="std-middle-box">
            <el-text style="font-size: 24px;font-weight: 600;color: black">
              邀请您使用NextConsole智能体服务平台
            </el-text>
          </div>
          <div class="std-middle-box">
            <el-text >
              并成为他的好友
            </el-text>
          </div>
          <div class="std-middle-box" style="flex-direction: column;gap: 12px">
            <el-button type="primary" @click="router_to_create()">
              没有账号，接受邀请注册账号
            </el-button>
            <el-button style="margin-left: 0" @click="router_to_add_friend()">
              已有账号，接受邀请成为好友
            </el-button>
          </div>
        </div>
        <div v-else>
          <div v-if="invitor?.is_friend" id="friend-area">
            <div>
              <el-text style="font-size: 20px;font-weight: 400;color: black">
                你们已经是好友了😄
              </el-text>
            </div>
            <div>
              <el-button type="primary" @click="router.push({name: 'next_console_welcome_home'})">
                前往使用NextConsole智能体服务平台
              </el-button>
            </div>
          </div>
          <div v-else id="is_friend_area">
            <div>
              <el-text style="font-size: 20px;font-weight: 400;color: black">
                邀请您成为他的好友
              </el-text>
            </div>
            <div>
              <el-button type="primary" @click="router_to_accept_friend()">
                接受邀请成为好友
              </el-button>
            </div>
          </div>

        </div>
      </div>


    </div>


  </el-dialog>

</template>

<style scoped>
#invite-area{
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 12px;
  justify-content: center;
}
#invite-info{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
.std-middle-box{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
#is_friend_area{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
}
#invite-intro{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
#friend-area{
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
  justify-content: center;
  align-items: center;
}

</style>
