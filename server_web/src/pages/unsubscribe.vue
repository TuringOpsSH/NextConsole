<script setup lang="ts">
import router from "@/router";
import {ElMessage} from "element-plus";
import {cancel_subscribe_api} from "@/api/contacts";
import {user_info} from "@/components/user_center/user";
import {onMounted} from "vue";
import {getInfo} from "@/utils/auth";

const vis_flag=  true
function handleClose(){
  router.push({
    name: 'next_console_welcome_home'
  })
}
async function handleUnsubscribe(){
  // 更新邀请状态
  let params = {
    email: user_info.value.user_email,
  }
  let res = await cancel_subscribe_api(params)
  if (!res.error_status){
    ElMessage.success('取消订阅成功!')
    router.push({
      name: 'next_console_welcome_home'
    })
  }
}
const phone_view = window.innerWidth < 768
onMounted(async () => {
  // 加载邀请码详情
  user_info.value = await getInfo()
})
</script>

<template>
  <el-container>
    <el-main style="padding: 0 !important;">


      <el-dialog v-model="vis_flag" :modal="false" @close="router.push({name: 'next_console_welcome_home'})"
                 :close-on-click-modal="false" :close-on-press-escape="false" :fullscreen="phone_view"
      >
          <div id="main_area">
            <div style="padding: 24px">
              <el-image src="images/logo_text.svg"/>
            </div>
            <div v-if="user_info?.user_email">
              <el-text>尊敬的用户：{{user_info.user_email}}</el-text>
            </div>
            <div v-else>
              <el-text>尊敬的用户：{{user_info.user_nick_name}}</el-text>
            </div>
            <div v-if="user_info?.user_email">
              <el-text type="danger" size="large">
                是否取消订阅NextConsole的最新产品信息邮件？
              </el-text>
              <br/>
              <br/>
              <el-text type="info">
                退订后您将无法收到平台的最新促销活动、折扣信息等。
              </el-text>
            </div>
            <div v-else>
              <el-empty description="暂无订阅数据"/>
            </div>
            <div v-if="user_info?.user_email">
              <el-button type="primary" @click="handleUnsubscribe">确认取消</el-button>
              <el-button @click="handleClose">暂不取消</el-button>
            </div>
          </div>

        </el-dialog>



    </el-main>
  </el-container>

</template>

<style scoped>
#main_area {

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

</style>
