<script setup lang="ts">
import {getInfo, login_out, setInfo} from "@/utils/auth";
import {
  account_transaction_data, account_transaction_loading,
  beforeAvatarUpload,
  begin_bind_email,
  begin_bind_phone,
  begin_bind_wx,
  bind_new_email,
  bind_new_phone,
  bind_text_code_status,
  bind_text_code_status_phone,
  bind_text_code_time,
  bind_text_code_time_phone, close_account_flag, close_user_account,
  email_bind_form,
  email_bind_form_ref,
  email_bind_rules,
  email_update,
  handleAvatarUploadSuccess,
  phone_bind_form,
  phone_bind_form_ref,
  phone_bind_rules,
  phone_update,
  send_bind_code,
  send_bind_code_phone, show_account_transaction, show_account_transaction_dialog,
  show_invite_dialog,
  user_avatar_upload_header,
  user_info,
  wx_update,
  current_page_num,
  current_page_size, current_transaction_cnt,
  handleSizeChange, handleCurrentChange,
} from "@/components/user_center/user";
import {api, get_support_area, user_update} from "@/api/user_center";
import {onBeforeMount, onUnmounted} from "vue-demi";
import {nextTick, onMounted, ref} from "vue";
import {ElNotification} from "element-plus";
import Reset_password_form from "@/components/user_center/reset_password_form.vue";
import User_invite_dialog from "@/components/user_center/user_invite_dialog.vue";

// 昵称
const nick_name_update = ref(false)
const nick_name_input = ref("")
const nick_name_ref = ref(null)
function begin_update_nick_name() {
  nick_name_update.value = true
  nick_name_input.value = user_info.value.user_nick_name
  nextTick(() => {
    nick_name_ref.value.focus()
  })

}
async function update_user_nick_name(){
  if (nick_name_input.value === user_info.value.user_nick_name){
    nick_name_update.value = false
    return
  }
  let res = await user_update(
      {
        user_nick_name: nick_name_input.value
      }
  )
  if (!res.error_status){
    user_info.value = res.result
    setInfo(res.result)
    nick_name_update.value = false
    ElNotification({
      title: "修改成功",
      message: "昵称修改成功",
      type: "success",
      duration: 3000,

    })
  }
}
// 姓名
const name_update = ref(false)
const name_input = ref("")
const name_ref = ref(null)
function begin_update_name() {
  name_update.value = true
  name_input.value = user_info.value.user_name
  nextTick(() => {
    name_ref.value.focus()
  })

}
async function update_user_name(){
  if (name_input.value === user_info.value.user_name){
    name_update.value = false
    return
  }
  let res = await user_update(
      {
        user_name: name_input.value
      }
  )
  if (!res.error_status){
    user_info.value = res.result
    setInfo(res.result)
    name_update.value = false
    ElNotification({
      title: "修改成功",
      message: "姓名修改成功",
      type: "success",
      duration: 3000,

    })
  }
}
// 企业
const company_update = ref(false)
const company_input = ref("")
const company_ref = ref(null)
function begin_update_company() {
  company_update.value = true
  company_input.value = user_info.value.user_company
  nextTick(() => {
    company_ref.value.focus()
  })

}
async function update_user_company(){
  if (company_input.value === user_info.value.user_company){
    company_update.value = false
    return
  }
  let res = await user_update(
      {
        user_company: company_input.value
      }
  )
  if (!res.error_status){
    user_info.value = res.result
    setInfo(res.result)
    company_update.value = false

    ElNotification({
      title: "修改成功",
      message: "企业修改成功",
      type: "success",
      duration: 3000,

    })
  }
}
// 部门
const department_update = ref(false)
const department_input = ref("")
const department_ref = ref(null)
function begin_update_department() {
  department_update.value = true
  department_input.value = user_info.value.user_department
  nextTick(() => {
    department_ref.value.focus()
  })

}
async function update_user_department(){
  if (department_input.value === user_info.value.user_department){
    department_update.value = false
    return
  }
  let res = await user_update(
      {
        user_department: department_input.value
      }
  )
  if (!res.error_status){
    user_info.value = res.result
    setInfo(res.result)
    department_update.value = false

    ElNotification({
      title: "修改成功",
      message: "部门修改成功",
      type: "success",
      duration: 3000,

    })
  }
}
// 职位
const position_update = ref(false)
const position_input = ref("")
const position_ref = ref(null)
function begin_update_position() {
  position_update.value = true
  position_input.value = user_info.value.user_position
  nextTick(() => {
    position_ref.value.focus()
  })

}
async function update_user_position(){
  if (position_input.value === user_info.value.user_position){
    position_update.value = false
    return
  }
  let res = await user_update(
      {
        user_position: position_input.value
      }
  )
  if (!res.error_status){
    user_info.value = res.result
    setInfo(res.result)
    position_update.value = false

    ElNotification({
      title: "修改成功",
      message: "职位修改成功",
      type: "success",
      duration: 3000,

    })
  }
}
// 区域
const area_update = ref(false)
const area_input = ref("")
const options = ref([])
async function get_all_options(){
  let res = await get_support_area({})
  if (res.error_status){
    return
  }
  options.value = res.result

}
async function begin_update_area() {
  area_update.value = true
  area_input.value = user_info.value.user_area
  await get_all_options()


}
async function update_user_area(){
  if (area_input.value === user_info.value.user_area){
    area_update.value = false
    return
  }
  let res = await user_update(
      {
        user_area: area_input.value
      }
  )
  if (!res.error_status){
    user_info.value = await getInfo(true)
    area_update.value = false

    ElNotification({
      title: "修改成功",
      message: "区域修改成功",
      type: "success",
      duration: 3000,

    })
  }
}

// 密码
const password_update = ref(false)
function begin_update_password() {
  password_update.value = true
}

// 邮箱


onBeforeMount(async () => {
  // @ts-ignore
  user_info.value = await getInfo(true)
})
const phone_view =ref(false)
const reset_width= ref('50%')
function change_phone_view(){
  if (window.innerWidth < 768){
    phone_view.value = true
    reset_width.value = '90%'
  }
  else {
    phone_view.value = false
    reset_width.value = '50%'
  }
}


onMounted(
    () => {
      window.addEventListener('resize', change_phone_view)
      change_phone_view()
    }
)
onUnmounted(
    () => {
      window.removeEventListener('resize', change_phone_view)
    }
)
</script>

<template>
  <el-container>
    <el-main>
      <el-scrollbar wrap-style="width:100%"
                    view-style="width: 100%;">
        <div id="user_info_main">

          <div id="user_info_box">
            <el-row>
              <el-col :span="24">
                <div class="user_info_headers">
                  <div class="user-info-meta">
                    <div class="user-info-meta-label">
                      <el-text>
                        账号ID
                      </el-text>
                    </div>
                    <div class="user-info-meta-value">
                      <el-text>
                        {{("" + user_info?.user_id).padStart(9, "0")}}
                      </el-text>
                    </div>
                  </div>
                  <el-divider v-if="phone_view"/>
                  <div class="user-info-meta">
                    <div class="user-info-meta-label">
                      <el-text>
                        注册时间
                      </el-text>
                    </div>
                    <div class="user-info-meta-value">
                      <el-text>
                        {{user_info?.create_time}}
                      </el-text>
                    </div>
                  </div>
                  <el-divider v-if="phone_view"/>
                  <div class="user-info-meta">
                    <div class="user-info-meta-label">
                      <el-text>
                        账号类型
                      </el-text>
                    </div>
                    <div class="user-info-meta-value">
                      <el-text>
                        {{user_info?.user_account_type}}
                      </el-text>
                      <el-image src="images/certification.svg" style="width: 18px; height: 18px"
                                v-if="user_info.user_account_type == '企业账号'"/>
                    </div>

                  </div>
                  <el-divider v-if="phone_view"/>
                  <div class="user-info-meta">

                    <el-button type="primary" plain @click="login_out()" style="height: 35px">
                      退出登录
                    </el-button>

                    <el-button type="danger" plain @click="close_account_flag=true" style="height: 35px">
                      注销账号
                    </el-button>
                  </div>
                </div>

              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-divider style="padding: 0!important;">
                  <el-text>
                    基本信息
                  </el-text>
                </el-divider>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    昵称
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12" style="flex-direction: row">
                <div v-if="nick_name_update">
                  <el-input v-model="nick_name_input"
                            @change="update_user_nick_name()"
                            @blur="nick_name_update = false"
                            ref="nick_name_ref"/>
                </div>
                <div class="user-info-meta-value" v-else>
                  <el-text>
                    {{ user_info?.user_nick_name }}
                  </el-text>

                </div>

              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_update_nick_name()" v-if="!nick_name_update" style="margin-left: 12px">
                  <el-text class="button-text">
                    修改
                  </el-text>
                </el-button>
              </el-col>
            </el-row>

            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    头像
                  </el-text>
                </div>
              </el-col>
              <el-col :span="3">
                <div class="std-middle-box">
                  <el-avatar :src="user_info?.user_avatar" v-if="user_info?.user_avatar"/>
                  <el-avatar v-else style="background: #D1E9FF">
                    <el-text style="font-weight: 600;color: #1570ef">{{user_info?.user_nick_name_py}}</el-text>
                  </el-avatar>
                </div>
              </el-col>
              <el-col :span="15">
                <div style="margin-left: 12px">
                  <el-upload
                      drag
                      :show-file-list="false"
                      accept=".png, .jpg, .jpeg, .svg, .gif, .bmp, .webp"
                      :before-upload="beforeAvatarUpload"
                      :action="api.user_avatar_update"
                      :on-success="handleAvatarUploadSuccess"
                      style=" "
                      name="avatar"
                      :headers="user_avatar_upload_header"
                  >
                    <el-avatar src="images/upload_cloud.svg" style="background: #F2F4F7" fit="scale-down"/>

                    <div class="el-upload__text">
                      <em>点击上传</em> <br>

                    </div>
                  </el-upload>
                </div>

              </el-col>
            </el-row>

            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    邮箱
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="user-info-meta-value">
                  <el-text>
                    {{ user_info?.user_email }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_bind_email()"
                           style="margin-left: 12px"
                           v-if="!email_update && user_info?.user_account_type == '个人账号' && !user_info.user_email">
                  <el-text class="button-text">
                    绑定
                  </el-text>
                </el-button>
              </el-col>
            </el-row>

            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    手机
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="user-info-meta-value">
                  <el-text>
                    {{ user_info?.user_phone }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_bind_phone()"
                           style="margin-left: 12px"

                           v-if="!phone_update && !user_info.user_phone">
                  <el-text class="button-text">
                    绑定
                  </el-text>
                </el-button>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    微信
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="user-info-meta-value">
                  <el-text>
                    {{ user_info?.user_wx_nickname }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_bind_wx()"
                           style="margin-left: 12px"

                           v-if="!wx_update  && !user_info.user_wx_union_id">
                  <el-text class="button-text">
                    绑定
                  </el-text>
                </el-button>
              </el-col>
            </el-row>

            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    密码
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="user-info-meta-value">
                  <el-text>
                    *****************
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_update_password()" v-if="!password_update"
                           style="margin-left: 12px"
                >
                  <el-text class="button-text">
                    修改
                  </el-text>
                </el-button>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    邀请码
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="user-info-meta-value">
                  <el-text>
                    {{ user_info?.user_invite_code }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="show_invite_dialog"
                           style="margin-left: 12px"
                >
                  <el-text class="button-text">
                    查看
                  </el-text>
                </el-button>
              </el-col>
            </el-row>
            <el-row> <el-col :span="24"> <el-divider>
              <el-text v-if="user_info.user_account_type == '企业账号'">
                以下信息如需修改，请联系企业管理员
              </el-text>
              <el-text v-else>
                个人信息
              </el-text>

            </el-divider></el-col> </el-row>
            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    姓名
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12" style="flex-direction: row">
                <div v-if="name_update">
                  <el-input v-model="name_input"
                            @change="update_user_name()"
                            @blur="name_update = false"
                            ref="name_ref"/>
                </div>
                <div class="user-info-meta-value" v-else :class="{
                  'user-info-meta-value-disabled': user_info?.user_account_type == '企业账号'
                }">
                  <el-text>
                    {{ user_info?.user_name }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_update_name()"
                           style="margin-left: 12px"
                           v-if="!name_update && user_info?.user_account_type != '企业账号'">
                  <el-text class="button-text">
                    修改
                  </el-text>
                </el-button>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    企业
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12" style="flex-direction: row">
                <div v-if="company_update">
                  <el-input v-model="company_input"
                            @change="update_user_company()"
                            @blur="company_update = false"
                            ref="company_ref"/>
                </div>
                <div class="user-info-meta-value" v-else :class="{
                  'user-info-meta-value-disabled': user_info?.user_account_type == '企业账号'
                }">
                  <el-text>
                    {{ user_info?.user_company }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_update_company()"
                           style="margin-left: 12px"
                           v-if="!company_update && user_info?.user_account_type != '企业账号'">
                  <el-text class="button-text">
                    修改
                  </el-text>
                </el-button>
              </el-col>
            </el-row>

            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    部门
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12" style="flex-direction: row">
                <div v-if="department_update">
                  <el-input v-model="department_input"
                            @change="update_user_department()"
                            @blur="department_update = false"
                            ref="department_ref"/>
                </div>
                <div class="user-info-meta-value" v-else :class="{
                  'user-info-meta-value-disabled': user_info?.user_account_type == '企业账号'
                }">
                  <el-text>
                    {{ user_info?.user_department }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_update_department()"
                           style="margin-left: 12px"
                           v-if="!department_update  && user_info?.user_account_type != '企业账号'">
                  <el-text class="button-text">
                    修改
                  </el-text>
                </el-button>
              </el-col>
            </el-row>

            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    职位
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12" style="flex-direction: row">
                <div v-if="position_update">
                  <el-input v-model="position_input"
                            @change="update_user_position()"
                            @blur="position_update = false"
                            ref="position_ref"/>
                </div>
                <div class="user-info-meta-value" v-else :class="{
                  'user-info-meta-value-disabled': user_info?.user_account_type == '企业账号'
                }">
                  <el-text>
                    {{ user_info?.user_position }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_update_position()" style="margin-left: 12px"
                           v-if="!position_update && user_info?.user_account_type == '个人账号'">
                  <el-text class="button-text">
                    修改
                  </el-text>
                </el-button>
              </el-col>
            </el-row>

            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    区域
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12">
                <div v-if="area_update">
                  <el-cascader
                      v-model="area_input"
                      clearable
                      :show-all-levels="false"
                      placeholder="选择国家/地区"
                      :options="options"
                      filterable
                      @change="update_user_area()"
                      style="width: 100%"
                  />
                </div>
                <div class="user-info-meta-value" v-else :class="{
                  'user-info-meta-value-disabled': user_info?.user_account_type == '企业账号'
                }">
                  <el-text>
                    {{ user_info?.user_area }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="begin_update_area()" style="margin-left: 12px"
                           v-if="!area_update && user_info?.user_account_type == '个人账号'">
                  <el-text class="button-text">
                    修改
                  </el-text>
                </el-button>
              </el-col>
            </el-row>
            <el-row> <el-col :span="24"> <el-divider>
              <el-text>
                账户信息
              </el-text>

            </el-divider></el-col> </el-row>
            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    账户ID
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12">

                <div class="user-info-meta-value" >
                  <el-text>
                    {{ user_info?.user_point_account?.account_id }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">

              </el-col>
            </el-row>
            <el-row>
              <el-col :span="6">
                <div class="user-info-meta-label">
                  <el-text>
                    账户余额
                  </el-text>
                </div>
              </el-col>
              <el-col :span="12">

                <div class="user-info-meta-value" >
                  <el-text>
                    {{ user_info?.user_point_account?.balance }}
                  </el-text>
                </div>
              </el-col>
              <el-col :span="6">
                <el-button text @click="show_account_transaction_dialog"
                           style="margin-left: 12px"
                >
                  <el-text class="button-text">
                    查看
                  </el-text>
                </el-button>
              </el-col>
            </el-row>
          </div>


        </div>
      </el-scrollbar>
    </el-main>
  </el-container>

  <el-footer>

  </el-footer>

  <el-dialog v-model="password_update"  :width="reset_width" top="35vh" style="max-width: 500px">
    <reset_password_form/>
  </el-dialog>
  <el-dialog v-model="email_update" :width="reset_width" title="绑定邮箱" draggable top="35vh" style="max-width: 500px">
    <el-form :model="email_bind_form" ref="email_bind_form_ref" :rules="email_bind_rules">
      <el-form-item prop="user_email">
        <el-input v-model="email_bind_form.user_email" placeholder="请输入邮箱"></el-input>
      </el-form-item>
      <el-form-item prop="user_email_code">
        <el-input v-model="email_bind_form.user_email_code" placeholder="请输入验证码">
          <template #suffix>
            <el-button text @click="send_bind_code" v-if="bind_text_code_status" type="primary">
              获取验证码
            </el-button>
            <el-button text v-else disabled>
              {{bind_text_code_time}}s后再次获取
            </el-button>
          </template>
        </el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="std-middle-box">
        <el-button @click="email_update = false">取 消</el-button>
        <el-button type="primary" @click="bind_new_email">确 定</el-button>
      </div>

    </template>
  </el-dialog>
  <el-dialog v-model="phone_update" :width="reset_width" title="绑定手机" draggable top="35vh" style="max-width: 500px">
    <el-form :model="phone_bind_form" ref="phone_bind_form_ref" :rules="phone_bind_rules">
      <el-form-item prop="user_phone">
        <el-input v-model="phone_bind_form.user_phone" placeholder="请输入手机"></el-input>
      </el-form-item>
      <el-form-item prop="user_email_code">
        <el-input v-model="phone_bind_form.user_phone_code" placeholder="请输入验证码">
          <template #suffix>
            <el-button text @click="send_bind_code_phone" v-if="bind_text_code_status_phone" type="primary">
              获取验证码
            </el-button>
            <el-button text v-else disabled>
              {{bind_text_code_time_phone}}s后再次获取
            </el-button>
          </template>
        </el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="std-middle-box">
        <el-button @click="phone_update = false">取 消</el-button>
        <el-button type="primary" @click="bind_new_phone">确 定</el-button>
      </div>

    </template>
  </el-dialog>
  <el-dialog v-model="wx_update" title="绑定微信" :width="reset_width" draggable top="35vh" style="max-width: 500px">
    <div class="std-middle-box" style="  flex-direction: column;">
      <div id="wx_login_container"/>
      <div style="display:flex;flex-direction: row;align-items: center;justify-content: center; gap: 12px">
        <div style="display:flex;flex-direction: row;align-items: center;justify-content: center">
          <el-image src="images/wx_logo.svg" style="width: 20px; height: 20px"/>
        </div>
        <div>
          <el-text style="font-size: 15px; font-weight: 600;color: #344054">
            微信扫一扫
          </el-text>
        </div>
      </div>
    </div>

  </el-dialog>
  <el-dialog v-model="close_account_flag" title="注销账号" :width="reset_width" draggable top="35vh" style="max-width: 500px">
    <div class="std-middle-box" style="  flex-direction: column;">
      <div>
        <el-result title="注销账号" sub-title="注销账号后，您的账号将无法再次登录，且无法找回，请谨慎操作" icon="warning"></el-result>
      </div>

      <div>
        <el-button text type="danger" @click="close_user_account">确认注销</el-button>
        <el-button text type="primary" @click="close_account_flag=false">我再想想</el-button>
      </div>
    </div>
  </el-dialog>
  <user_invite_dialog/>
  <el-dialog v-model="show_account_transaction" :width="reset_width" title="账户交易记录" draggable top="35vh" >
    <el-table :data="account_transaction_data" border style="width: 100%" v-loading="account_transaction_loading"
              element-loading-text="加载中"
    >
      <el-table-column prop="transaction_id" label="交易ID" width="180">
      </el-table-column>
      <el-table-column prop="create_time" label="发生时间" width="180">
      </el-table-column>
      <el-table-column prop="transaction_type" label="类型" width="180">
      </el-table-column>
      <el-table-column prop="transaction_amount" label="金额" width="180">
      </el-table-column>
      <el-table-column prop="transaction_desc" label="描述" width="180">
      </el-table-column>
      <el-table-column prop="order_id" label="订单ID" width="180">
      </el-table-column>

    </el-table>
    <el-pagination
        :page-sizes="[10, 20, 50, 100]"
        size="small"
        :page-size="current_page_size"
        :current-page="current_page_num"
        :layout="page_model"
        :total="current_transaction_cnt"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
    ></el-pagination>
    <template #footer>
      <div class="std-middle-box">
        <el-button @click="show_account_transaction = false">确 定</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>

#user_info_main{
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  height: calc(100vh - 60px);
  width: 100%;
  gap: 12px;

}
#user_info_box{
  display: flex;
  flex-direction: column;
  margin: 80px;
  width: 100%;
  max-width: 900px;
  gap:24px;


}
.std-middle-box{
  display: flex;

  justify-content: center;
  align-items: center;
  height: 100%;
  gap: 12px;
}
.user-info-meta{
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;

}
.user-info-meta-label{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  min-width: 80px;
  max-width: 160px;
  height: 100%;
}
.user_info_headers{
  display: flex;
  justify-content: flex-start;
  align-items: flex-end;
  gap: 12px;
  width: 100%;

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
.button-text{
  color: #175CD3;
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  margin-left: 12px;
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
@media (max-width: 768px) {
  #user_info_main{
    gap: 0;
  }
  #user_info_box{
    width: 100%;
    max-width: 100%;
    max-height: calc(100vh - 20px);
    margin-top: 20px;
    padding: 20px;

  }
  .user_info_headers{
    flex-direction: column;
    gap: 0;
    align-items: start;
  }

  .user-info-meta-label{
    justify-content: flex-start;
  }
  .user-info-meta-value{
    max-width: calc(100% - 48px);
    overflow: auto;
  }

  .user-info-meta{
    width: calc(100% - 24px);
  }

}
</style>
