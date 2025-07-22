<script lang="ts" setup>
import {nextTick, onMounted} from 'vue'
import {ElInput, ElMessage, ElScrollbar} from "element-plus";
import NextConsole from "@/components/next_console/console/next_console.vue";
import {api, assistant_get, models_search} from "@/api/assistant_center";
import {useRoute, useRouter} from 'vue-router';
import {
  add_assistant_kg,
  assistant_avatar_upload_data,
  assistant_avatar_upload_header,
  assistant_choose,
  assistant_choose_avatar_upload_data,
  assistant_detail_type,
  assistant_model_detail_vis,
  assistant_role_edit_resize_cnt,
  assistant_role_prompt_rows,
  assistant_role_prompt_template,
  assistant_view_model,
  Current_assistant_kg_keyword,
  Current_assistant_kg_list,
  dia_assistant_kg_setting_vis,
  handle_avatar_change,
  handle_exceed,
  handle_tag_close,
  handleInputConfirm,
  InputRef,
  inputValue,
  inputVisible,
  marks,
  model_list,
  pick_assistant_role_edit,
  remove_assistant_kg,
  search_assistant_kg_list,
  show_role_base_info,
  show_role_kg_info,
  show_test_console_flag,
  showInput,
  system_prompt_example_copy,
  system_prompt_example_vis,
  to_do_something,
  upload_avatar,
} from "@/components/assistant/assistant_manage/assistant_manage";
import {
  assistant_delete_vis,
  assistant_deleted,
  assistant_filter, assistant_key_word,
  assistant_order,
  assistantList,
  assistants_cnt,
  change_order,
  change_page,
  current_page_num,
  current_page_size,
  delete_assistants,
  get_assistant_list,
  handle_current_change,
  show_cnt_tag,
  start_assistant,
} from "@/components/assistant/assistant_manage/assistant_list";
import {
  add_new_assistant,
  reset_new_assistant,
  save_new_assistant,
} from "@/components/assistant/assistant_manage/assistant_add";
import {
  assistant_avg_time_Ref,
  assistant_cost_Ref,
  assistant_qa_Ref,
  assistant_remark_Ref,
  assistant_speed_Ref,
  assistant_user_Ref,
  change_publish_way,
  current_publish_way,
  init_metric_chart,
  monitor_time_range,
  publish_assistant,
  reset_current_assistant,
  unpublished_assistant,
  update_assistant_detail,
} from "@/components/assistant/assistant_manage/assistant_detail";


import {Search} from "@element-plus/icons-vue";
import {assistant} from "@/types/assistant";
import {current_assistant} from "@/components/next_console/console/assistant";

const router = useRouter()
const props = defineProps({
  model: {
    type:  Number,
    required: false,
    default: 0
  },
  assistant: {
    type: Number,
    default: null,
    required: false
  },
  info_type : {
    type: Number,
    default: 1,
    required: false
  }
});


async function change_assistant_view_model(model: number, assistant: assistant | null = null,
                                           info_type :number| null = null) {
  // 更新参数
  assistant_view_model.value = model;
  assistant_detail_type.value = info_type
  Object.assign(assistant_choose, assistant)
  // model 0 列表查看模式
  // console.log(model,"fewfew")
  if (model === 0) {
    router.push({
      name: 'assistant_manage',
      query: {
        model: 0
      }
    });
    reset_new_assistant(false)
    await get_assistant_list()
    show_test_console_flag.value = false
  }
  // model 1 详情查看模式
  else if (model === 1) {
    if (assistant_choose.id && assistant_choose.id < 0) {
      ElMessage.info({
        message: '此助手暂不支持查看',
        type: 'info',
        duration: 600
      })
      return
    }
    let res = await assistant_get({
      "id": assistant_choose.id,
    })
    if (!res.error_status) {
      Object.assign(assistant_choose, res.result);
      current_assistant.value = res.result;
      show_test_console_flag.value = true
    }
    router.push({
      name: 'assistant_manage',
      query: {
        ...router.currentRoute.value.query, // 保持既有参数
        model: 1,
        assistant: assistant_choose.id,
        info_type: assistant_detail_type.value
      }
    });
    if (assistant_detail_type.value === 1) {
      await init_metric_chart()
    }

    else if (assistant_detail_type.value === 3) {
      await search_assistant_kg_list()
    }

  }
  // model 2 新增助手模式
  else if (model === 2 ){
    router.push({
      name: 'assistant_manage',
      query: {
        ...router.currentRoute.value.query, // 保持既有参数
        model: assistant_view_model.value,
        assistant: assistant_choose.id,
      }
    });
    show_test_console_flag.value = false
    await search_assistant_kg_list()
    return
  }

}

async function add_assistant_function() {
  to_do_something()
}


function omit_assistant_desc(assistant_desc:string ,n = 12){
  if (assistant_desc.length > n){
    return assistant_desc.slice(0,n) + '...'
  }
  return assistant_desc
}


async function handleResize(){
  assistant_role_prompt_rows.value= Math.round((window.innerHeight -180) /21.25) + 1;
  assistant_role_edit_resize_cnt.value += 1
  await nextTick()
}




onMounted(async () => {
  // 监听窗口变化

  window.addEventListener('resize', handleResize);
  await handleResize()
  // 载入助手列表
  await get_assistant_list()
  // 载入模型列表
  let res = await models_search({})
  if (!res.error_status) {
    model_list.value = res.result.data
  }
  // 载入路径参数
  assistant_view_model.value = props.model
  assistant_detail_type.value = props.info_type
  if (props.assistant) {
    let res = await assistant_get({
      "id": props.assistant,
    })
    if (!res.error_status) {
      Object.assign(assistant_choose, res.result);
    }
  }
  // 进入指定模式
  await change_assistant_view_model(assistant_view_model.value, assistant_choose, assistant_detail_type.value)
})


</script>
<template>
  <div class="assistant-center">

    <div class="assistant-list">
      <div class="assistant-list-header">
        <div class="step-router">
          <el-button class="step-button" style="height: 40px"
                     @click="change_assistant_view_model(0)"
                     :disabled = "assistant_view_model === 0"
          >
            <el-image v-if="assistant_view_model !== 0" src="images/arrow_left_black.svg"
                      style="width: 14px;height: 14px"/>
            <el-image v-else src="images/arrow_left_grey.svg" style="width: 14px;height: 14px"/>
          </el-button>
          <el-button class="step-button" style="height: 40px" disabled>
            <el-image src="images/arrow_right_grey.svg" style="width: 14px;height: 14px"/>
          </el-button>
          <div v-if="assistant_view_model === 2" style="display: flex;align-items: center;padding: 0 12px">
            <el-text style="font-size: 16px;font-weight: 600;line-height: 24px; color: #101828">
              新增助手
            </el-text>
          </div>
          <div v-if="assistant_view_model === 1 && assistant_choose"
               style="display: flex;align-items: center;padding: 0 12px;gap: 8px">
            <el-avatar :src="assistant_choose.assistant_avatar_url ? assistant_choose.assistant_avatar_url : assistant_choose.assistant_avatar"/>

            <el-tooltip v-if="assistant_choose.assistant_name.length > 5" effect="light">

              <el-text style="margin-left: 8px;font-size: 16px;font-weight: 600;line-height: 24px;">

                {{ omit_assistant_desc(assistant_choose.assistant_name, 5) }}
              </el-text>
              <template #content>
                <div v-text="assistant_choose.assistant_name" style="max-width: 400px;display: flex;flex-wrap: wrap">

                </div>
              </template>
            </el-tooltip>
            <el-text v-else style="margin-left: 8px;font-size: 16px;font-weight: 600;line-height: 24px;">
              {{ assistant_choose.assistant_name }}
            </el-text>
          </div>
        </div>
        <div class="order-button" v-if="assistant_view_model === 0">
          <el-button :class="assistant_order === 'create_time' ? 'order-button-left' : 'order-button-default'"
                     @click="change_order('create_time')">
            <el-image src="images/green_dot.svg"
                      v-if="assistant_order === 'create_time'"
                      style="display: flex;align-items: center;margin: 0 6px 0 6px;"
            />
            <el-text>最近添加</el-text>
          </el-button>
          <el-button :class="assistant_order === 'call_cnt' ? 'order-button-right' : 'order-button-default'"
                     @click="change_order('call_cnt')">
            <el-image src="images/green_dot.svg"
                      v-if="assistant_order === 'call_cnt'"
                      style="display: flex;align-items: center;margin: 0 6px 0 6px;"
            />
            <el-text>最大调用</el-text>
          </el-button>
        </div>
        <div class="assistant-edit-step" v-if="assistant_view_model === 2">
          <el-button text style="height: 100%"
                     :class="pick_assistant_role_edit ? 'assistant-role-button-picked' :'' "
                     @click="pick_assistant_role_edit=true"
          >
            <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #667085;">
              角色设置
            </el-text>
          </el-button>
          <el-button text v-for="(item,index) in assistant_choose.assistant_function_lists" style="height: 100%"


          >
            <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #667085;">
              指令{{ index + 1 }}
            </el-text>
          </el-button>
          <el-button text @click="add_assistant_function" style="height: 100%">
            <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #667085;">
              +添加任务指令
            </el-text>
          </el-button>

        </div>
        <div class="assistant-author-info" v-if="assistant_view_model === 1 && assistant_choose">
          <div>
            <el-text>创建者 {{ assistant_choose.assistant_author_name}}  </el-text>
          </div>

          <div>
            <el-text>创建时间 {{ assistant_choose.create_time}}</el-text>
          </div>
        </div>
        <div class="assistant-detail-info-button-box" v-if="assistant_view_model === 1">
          <el-button style="box-shadow: 0 1px 2px 0 #1018280D; background: #FFFFFF;
        height: 40px; border-radius: 8px; padding: 10px 16px 10px 16px;" @click="reset_current_assistant">
            <el-image src="images/retry.svg"/>
            <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054;
          margin-left: 8px;
">重置</el-text>
          </el-button>


          <el-popconfirm title="确定要更新该助手的所有配置么?" confirm-button-text="确定"
                         cancel-button-text="取消" @confirm="update_assistant_detail">
            <template #reference>

              <el-button style="background: #1570ef;height: 40px; border-radius: 8px; padding: 10px 16px 10px 16px;
            box-shadow: 0 1px 2px 0 #1018280D; margin-left: 12px
">
                <el-image src="images/refresh_white.svg"/>
                <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #FFFFFF;
          margin-left: 8px;
">更新</el-text>
              </el-button>
            </template>
          </el-popconfirm>
        </div>
        <div class="right-button-box" v-if="assistant_view_model === 0">
          <el-input @change="get_assistant_list" v-model="assistant_key_word" :prefix-icon="Search"
                    placeholder="搜索助手"
                    style="width: 200px;height: 40px"
                    clearable
          />
          <el-select v-model="assistant_filter" style="width: 164px;height: 40px" @change="get_assistant_list"
                     clearable
          >
            <el-option label="全部"  value></el-option>
            <el-option label="仅显示已启用助手" value="1"></el-option>
            <el-option label="未启用" value="0"></el-option>
          </el-select>
          <el-button type="primary" style="background: #1570EF;gap: 8px;border-radius: 8px;height: 40px"
                     @click="change_assistant_view_model(2)">
            <el-image src="images/user_plus.svg"/>
            <el-text style="color: #FFFFFF;
                  font-size: 14px;
                  font-weight: 600;
                  line-height: 20px;
                  margin-left: 8px;
                  ">新增助手
            </el-text>
          </el-button>

        </div>
        <div class="assistant-edit-button-box" v-if="assistant_view_model === 2">
          <el-button style="width: 88px;height: 40px;border-radius: 8px;" @click="reset_new_assistant">
            <el-image src="images/retry.svg" style="width: 20px;height: 20px;margin-right: 6px"/>
            <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054;">重置</el-text>
          </el-button>
          <el-button style="margin-left: 12px;border-radius: 8px;
            background: #1570EF;border: 0;width: 88px;
            height: 40px;box-shadow: 0 1px 2px 0 #1018280D;" @click="save_new_assistant"
                     v-if="assistant_choose.id"
          >
            <el-image src="images/save_white.svg" style="width: 20px;height: 20px;margin-right: 6px"/>
            <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #FFFFFF;">保存</el-text>
          </el-button>
          <el-button style="margin-left: 12px;border-radius: 8px;
            background: #1570EF;border: 0;width: 88px;
            height: 40px;box-shadow: 0 1px 2px 0 #1018280D;" @click="add_new_assistant" v-else>
            <el-image src="images/send.svg" style="width: 20px;height: 20px;margin-right: 6px"/>
            <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #FFFFFF;">创建</el-text>
          </el-button>
        </div>
      </div>
      <el-scrollbar class="my-scrollbar">
        <div v-if="assistant_view_model === 2" class="assistant-add-body">

          <div class="assistant-role-edit-box">
            <div class="assistant-role-edit-header">
              <div>
                <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">
                  提示词
                </el-text>
              </div>
              <div>
                <el-button style="border-radius: 8px" @click="system_prompt_example_vis = true">
                  <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054">示例</el-text>
                </el-button>
                <el-button style="margin-left: 16px;border-radius: 8px" @click="to_do_something">
                  <el-image src="images/cpu.svg"/>
                  <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054;
                        margin-left: 8px;" >
                    AI优化
                  </el-text>
                </el-button>
                <el-dialog v-model="system_prompt_example_vis" title="示例" :modal="false"
                           width="640px" top="10vh">

                  <el-input v-model="assistant_role_prompt_template" disabled
                            type="textarea"
                            :autosize="{ minRows: 40, maxRows: 40 }"
                  />
                  <template #footer>
                    <div style="width: 100%; display: flex;justify-content: space-between;gap: 8px">
                      <el-button @click="system_prompt_example_copy"
                                 style="border: 1px solid #D0D5DD;
                                       box-shadow: 0 1px 2px 0 #1018280D;
                                        border-radius: 8px;
                                        padding: 10px 18px 10px 18px;
                                        width: 100%;

  ">
                        <el-image src="images/copy.svg"></el-image>
                        <el-text style="
                              margin-left: 8px;
                              font-size: 16px;
                              font-weight: 600;
                              line-height: 24px;">复制
                        </el-text>
                      </el-button>
                      <el-button @click="system_prompt_example_vis = false"
                                 style="
                                       border: 1px solid #1570EF;
                                       background: #1570EF;
                                       box-shadow: 0 1px 2px 0 #1018280D;
                                        border-radius: 8px;
                                        padding: 10px 18px 10px 18px;
                                        width: 100%;
  "
                      >
                        <el-text style="color: #FFFFFF;font-size: 16px;
                              font-weight: 600;
                              line-height: 24px;
                              ">确 定
                        </el-text>
                      </el-button>
                    </div>
                  </template>
                </el-dialog>
              </div>
            </div>
            <div class="assistant-role-edit-body">

              <el-input type="textarea" v-model="assistant_choose.assistant_role_prompt"
                        class="assistant-role-edit-area"
                        :autosize = "{ minRows: assistant_role_prompt_rows, maxRows: assistant_role_prompt_rows }"
                        :placeholder="assistant_role_prompt_template"
                        :key="assistant_role_edit_resize_cnt"

              />

            </div>
          </div>

          <div class="assistant-role-setting-box" v-if="pick_assistant_role_edit">
            <div class="assistant-role-edit-header">
              <div>
                <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">
                  设置
                </el-text>
              </div>
              <div>
                <el-button style="border-radius: 8px;background: #EFF8FF;border: 1px solid #1570EF; gap: 8px;
                    display: flex;justify-content: space-between"
                           @click="assistant_model_detail_vis=true">
                  <el-image src="images/deep_seek_logo.png" style="margin-right: 4px;width: 24px;height: 24px;
                  background-color: #EFF8FF"/>
                  <el-text style="margin-right: 4px"> {{ assistant_choose.assistant_model_name }}</el-text>
                  <el-tag style="margin-right: 4px;border-radius: 16px;border: 1px solid #B2DDFF">
                    chat
                  </el-tag>
                  <el-image src="images/parent_component.svg"/>
                </el-button>
                <el-dialog v-model="assistant_model_detail_vis" :modal="false" width="500px">
                  <div class="model-detail-box">
                    <el-text style="margin-right: 20px">模型类型</el-text>
                    <div style="flex: 1">
                      <el-select v-model="assistant_choose.assistant_model_name" style="width: 100%;">
                        <el-option v-for="model in model_list" :value="model.llm_name"/>

                      </el-select>
                    </div>
                  </div>
                  <div class="model-detail-box">
                    <el-text style="margin-right: 20px">模型温度</el-text>
                    <div style="flex: 1">
                      <el-slider v-model="assistant_choose.assistant_model_temperature" :step="0.1"
                                 :max="2"
                                 :marks="marks"
                      />
                    </div>
                  </div>
                </el-dialog>
              </div>
            </div>
            <div class="assistant-role-edit-body">
              <div class="assistant-role-base-info-box">
                <div class="role-base-info-label">
                  <el-button @click="show_role_base_info = !show_role_base_info" v-if="show_role_base_info"
                             style="display: flex;align-items: center;width: 24px;height: 24px;background: #F9FAFB;
                           border: 0; " >
                    <el-image src="images/arrow_down.svg"  style="width: 24px;height: 8px"/>
                  </el-button>
                  <el-button @click="show_role_base_info = !show_role_base_info" v-else
                             style="display: flex;align-items: center;width: 24px;height: 24px"
                             text
                  >
                    <el-image src="images/chevron-right.svg" style="width: 8px;height: 24px"/>
                  </el-button>
                  <el-text style="margin-left: 6px;font-weight: 500;line-height: 24px;color: #101828">基础信息</el-text>
                </div>
                <div class="role-base-info-body" v-if="show_role_base_info">
                  <div>
                    <div style="margin-bottom: 6px">
                      <el-text>助手编号</el-text>
                    </div>
                    <el-input v-model="assistant_choose.id" disabled/>
                  </div>
                  <div>
                    <div style="margin-bottom: 6px">
                      <el-text>助手名称</el-text>
                    </div>
                    <el-input v-model="assistant_choose.assistant_name"/>
                  </div>
                  <div>
                    <div style="margin-bottom: 6px">
                      <el-text>助手描述</el-text>
                    </div>
                    <el-input v-model="assistant_choose.assistant_desc" type="textarea"
                              :autosize="{ minRows: 5, maxRows: 5 }"
                              class="assistant-desc-input-textarea"
                              placeholder="请输入简单易懂的能力描述"/>
                  </div>
                  <div>
                    <div style="margin-bottom: 6px">
                      <el-text>助手脑容量</el-text>
                    </div>
                    <el-slider v-model="assistant_choose.assistant_memory_size"
                               :step="1"
                               show-stops :max="10"/>
                  </div>
                  <div style="display: flex;flex-direction: row;padding: 8px;
                       justify-content: space-between;align-items: center;border-bottom: 1px solid #D0D5DD">
                    <div style="display: flex;align-items: center">
                      <div style="margin-right: 12px">
                        <el-text>头像</el-text>
                      </div>
                      <el-avatar :src="assistant_choose.assistant_avatar_url ? assistant_choose.assistant_avatar_url : assistant_choose.assistant_avatar"/>
                    </div>
                    <div style="display: flex;flex-direction: row">
                      <el-upload
                          ref="upload_avatar"
                          :action="api.assistant_avatar_upload"
                          :auto-upload="false"
                          :on-change="handle_avatar_change"
                          :show-file-list="false"
                          :limit="1"
                          :on-exceed="handle_exceed"
                          name="avatar"
                          :headers="assistant_avatar_upload_header"
                          :data="assistant_avatar_upload_data"


                      >

                        <template #trigger>
                          <el-button text style="padding: 12px">
                            <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color:#475467">
                              上传
                            </el-text>
                          </el-button>
                        </template>
                      </el-upload>
                      <el-button text style="padding: 12px" @click="to_do_something">
                        <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color:#175CD3">
                          AI 生成
                        </el-text>
                      </el-button>
                    </div>
                  </div>
                  <div>
                    <div style="margin-bottom: 6px">
                      <el-text>检索标签</el-text>
                    </div>

                    <div style="height: 100px;
                           border: 1px solid #D0D5DD;box-shadow: 0 1px 2px 0 #1018280D;border-radius: 8px;
                           padding: 12px 16px;
                           gap: 8px;
">
                      <el-tag
                          v-for="tag in assistant_choose.assistant_tags"
                          :key="tag"
                          closable
                          :disable-transitions="false"
                          @close="handle_tag_close(tag)"
                          style="margin: 8px"
                      >
                        {{ tag }}
                      </el-tag>
                      <el-input
                          v-if="inputVisible"
                          ref="InputRef"
                          v-model="inputValue"
                          style="width: 100px"
                          size="small"
                          @keyup.enter="handleInputConfirm"
                          @blur="handleInputConfirm"
                      />
                      <el-button v-else class="button-new-tag" size="small" @click="showInput">
                        + 新标签
                      </el-button>
                    </div>
                  </div>
                </div>
              </div>
              <div class="assistant-role-kg-info-box">
                <div class="assistant-role-kg-info-label">
                  <div style="display: flex;flex-direction: row;">
                    <el-button @click="show_role_kg_info = !show_role_kg_info" v-if="show_role_kg_info"
                               style="display: flex;align-items: center;width: 24px;height: 24px;background: #F9FAFB;
                           border: 0; " >
                      <el-image src="images/arrow_down.svg"  style="width: 24px;height: 8px"/>
                    </el-button>
                    <el-button @click="show_role_kg_info = !show_role_kg_info" v-else
                               style="display: flex;align-items: center;width: 24px;height: 24px"
                               text
                    >
                      <el-image src="images/chevron-right.svg" style="width: 8px;height: 24px"/>
                    </el-button>
                    <el-text style="margin-left: 6px;font-weight: 500;line-height: 24px;color: #101828">知识库</el-text>
                  </div>
                  <div style="display: flex;flex-direction: row;align-items: center;justify-content: space-between">
                    <el-image src="images/settings_01_grey.svg" style="width: 20px;height: 20px;cursor: pointer"
                              @click="dia_assistant_kg_setting_vis = true"
                    />
                    <el-popover placement="bottom" :width="520" trigger="click">
                      <template #reference>
                        <el-button text>
                          <el-text style="color:#175CD3;font-size: 24px">+</el-text>
                        </el-button>
                      </template>
                      <el-input :prefix-icon="Search" v-model="Current_assistant_kg_keyword"
                                @change="search_assistant_kg_list"
                      />
                      <div style="margin: 12px">
                        <el-text v-if="!Current_assistant_kg_keyword">
                          最近添加
                        </el-text>
                        <el-text v-else>
                          搜索结果
                        </el-text>
                      </div>

                      <el-table :data="Current_assistant_kg_list" :show-header="false"
                                tooltip-effect="light" :show-overflow-tooltip="true"
                                @row-click="add_assistant_kg"
                                >
                        <el-table-column width="50" property="kg_icon" label="图标" >
                          <template #default="{row}">
                            <el-avatar :src="row.kg_icon ? row.kg_icon: 'images/kg_default_icon.svg'"
                                       style="width: 24px;height: 24px"/>
                          </template>
                        </el-table-column>
                        <el-table-column width="120" property="create_time" label="创建时间" />
                        <el-table-column width="150" property="kg_name" label="名称" />
                        <el-table-column width="150" property="kg_desc" label="描述" />
                      </el-table>
                    </el-popover>

                  </div>
                </div>
                <div class="kg_list" v-if="show_role_kg_info">
                  <div v-for="(kg,_) in assistant_choose.assistant_knowledge_base" class="kg_item">
                    <div>
                      <el-text>{{kg.kg_name}}</el-text>
                    </div>
                    <div>
                      <el-popconfirm title="确定要移除该知识库么?" confirm-button-text="确定"
                                     cancel-button-text="取消" @confirm="remove_assistant_kg(kg)">
                        <template #reference>
                          <el-button style="background: #F9FAFB;border: 0" >
                            <el-image src="images/delete.svg"/>
                          </el-button>
                        </template>
                      </el-popconfirm>

                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="assistant-function-setting-box" v-else>
            <div class="assistant-role-edit-header">
              <div>
                <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">
                  提示词
                </el-text>
              </div>
              <div>
                <el-button style="border-radius: 8px">
                  <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054">示例</el-text>
                </el-button>
                <el-button style="margin-left: 16px;border-radius: 8px">
                  <el-image src="images/cpu.svg"/>
                  <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054;
                      margin-left: 8px;">
                    AI优化
                  </el-text>
                </el-button>
              </div>
            </div>

            <div class="assistant-role-edit-body">

              <el-input type="textarea" v-model="assistant_choose.assistant_role_prompt"
                        class="assistant-role-edit-area"
                        autosize

              />

            </div>
          </div>
          <div class="assistant-test-box">
            <div class="assistant-test-header">
              <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">
                调试
              </el-text>
            </div>
            <div class="assistant-test-body" >

              <NextConsole v-if="show_test_console_flag"
                           :test_model="true"
                           :test_assistant="assistant_choose"
              />

            </div>


          </div>
        </div>
        <div v-else-if="assistant_view_model === 1" class="assistant-detail-box">
            <div class="detail-tabs-head">
              <div class="detail-tab" @click="change_assistant_view_model(1,assistant_choose,1)"
                   :class="assistant_detail_type==1 ? 'detail-tab-activate': ''">
                  <el-text class="detail-tab-text" :class="assistant_detail_type==1 ? 'detail-tab-text-activate': ''">
                    概览信息
                  </el-text>
              </div>
              <div class="detail-tab" @click="change_assistant_view_model(1,assistant_choose,2)"
                   :class="assistant_detail_type==2 ? 'detail-tab-activate': ''">
                <el-text class="detail-tab-text" :class="assistant_detail_type==2 ? 'detail-tab-text-activate': ''">
                  助手发布
                </el-text>
              </div>
              <div class="detail-tab" @click="change_assistant_view_model(1,assistant_choose,3)"
                   :class="assistant_detail_type==3 ? 'detail-tab-activate': ''">
                <el-text class="detail-tab-text" :class="assistant_detail_type==3 ? 'detail-tab-text-activate': ''">
                  角色设置
                </el-text>
              </div>
            </div>
            <div class="detail-tab-content" v-if="assistant_detail_type===1">
              <div class="assistant-monitor-box">
                <div class="assistant-monitor-header">
                  <div>
                    <el-text style=" font-size: 16px;font-weight: 600;line-height: 24px;color: #101828">统计趋势图</el-text>
                  </div>
                  <div>
                    <el-select v-model="monitor_time_range" @change="init_metric_chart">
                      <el-option label="最近7天" :value=7></el-option>
                      <el-option label="最近30天" :value=30></el-option>
                      <el-option label="最近90天" :value=90></el-option>
                    </el-select>
                  </div>
                </div>
                <div class="assistant-monitor-body" >
                  <div ref="assistant_qa_Ref" style="width: 600px; height: 400px;"/>
                  <div ref="assistant_user_Ref" style="width: 600px; height: 400px;"/>
                  <div ref="assistant_avg_time_Ref" style="width: 600px; height: 400px;"/>
                  <div ref="assistant_speed_Ref" style="width: 600px; height: 400px;"/>
                  <div ref="assistant_remark_Ref" style="width: 600px; height: 400px;"/>
                  <div ref="assistant_cost_Ref" style="width: 600px; height: 400px;"/>

                </div>
              </div>
            </div>
            <div class="detail-tab-content" v-else-if="assistant_detail_type===2">
              <div class="assistant-publish-box">
                <div class="assistant-publish-left">
                  <div class="assistant-publish-left-head">
                    <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #101828">
                      发布渠道
                    </el-text>
                  </div>
                  <div class="assistant-publish-left-body">
                    <div class="assistant-publish-way-box"
                         :class="current_publish_way == 'NextConsole' ? 'assistant-publish-way-box-activate':''"
                         @click="change_publish_way('NextConsole')"
                    >
                      <div>
                        <el-avatar src="images/logo.svg"/>
                      </div>
                      <div>
                        <div>
                          <el-text class="assistant-publish-way-name">
                            NextConsole
                          </el-text>
                        </div>
                        <div>
                          <el-text class="assistant-publish-way-desc">
                            管理助手在NextConsole上的发布
                          </el-text>
                        </div>
                      </div>
                    </div>
                    <div class="assistant-publish-way-box"
                         :class="current_publish_way == 'WEB' ? 'assistant-publish-way-box-activate':''"
                         @click="change_publish_way('WEB')">
                      <div>
                        <el-avatar src="images/web_app_logo.svg"/>
                      </div>
                      <div>
                        <div>
                          <el-text class="assistant-publish-way-name">
                            WEB应用
                          </el-text>
                        </div>
                        <div>
                          <el-text class="assistant-publish-way-desc">
                            将助手发布为一个独立的WEB应用
                          </el-text>
                        </div>
                      </div>
                    </div>
                    <div class="assistant-publish-way-box"
                         :class="current_publish_way == 'IFRAME' ? 'assistant-publish-way-box-activate':''"
                         @click="change_publish_way('IFRAME')">
                      <div>
                        <el-avatar src="images/iframe_logo.svg"/>
                      </div>
                      <div>
                        <div>
                          <el-text class="assistant-publish-way-name">
                            IFRAME调用
                          </el-text>
                        </div>
                        <div>
                          <el-text class="assistant-publish-way-desc">
                            将助手嵌入到其他应用中
                          </el-text>
                        </div>
                      </div>
                    </div>
                    <div class="assistant-publish-way-box"
                         :class="current_publish_way == 'API' ? 'assistant-publish-way-box-activate':''"
                         @click="change_publish_way('API')">
                      <div>
                        <el-avatar src="images/api_logo.svg"/>
                      </div>
                      <div>
                        <div>
                          <el-text class="assistant-publish-way-name">
                            API 应用
                          </el-text>
                        </div>
                        <div>
                          <el-text class="assistant-publish-way-desc">
                            对外提供API接口
                          </el-text>
                        </div>
                      </div>
                    </div>
                    <div class="assistant-publish-way-box"
                         :class="current_publish_way == 'qy_wx' ? 'assistant-publish-way-box-activate':''"
                         @click="change_publish_way('qy_wx')">
                      <div>
                        <el-avatar src="images/qy_wx_logo.svg"/>
                      </div>
                      <div>
                        <div>
                          <el-text class="assistant-publish-way-name">
                            企业微信
                          </el-text>
                        </div>
                        <div>
                          <el-text class="assistant-publish-way-desc">
                            将助手发布至企业微信
                          </el-text>
                        </div>
                      </div>
                    </div>
                    <div class="assistant-publish-way-box"
                         :class="current_publish_way == 'feishu' ? 'assistant-publish-way-box-activate':''"
                         @click="change_publish_way('feishu')">
                      <div>
                        <el-avatar src="images/feishu_logo.svg"/>
                      </div>
                      <div>
                        <div>
                          <el-text class="assistant-publish-way-name">
                            飞书
                          </el-text>
                        </div>
                        <div>
                          <el-text class="assistant-publish-way-desc">
                            将助手发布至飞书
                          </el-text>
                        </div>
                      </div>
                    </div>
                    <div class="assistant-publish-way-box"
                         :class="current_publish_way == 'ding_ding' ? 'assistant-publish-way-box-activate':''"
                         @click="change_publish_way('ding_ding')">
                      <div>
                        <el-avatar src="images/ding_ding_logo.svg"/>
                      </div>
                      <div>
                        <div>
                          <el-text class="assistant-publish-way-name">
                            钉钉
                          </el-text>
                        </div>
                        <div>
                          <el-text class="assistant-publish-way-desc">
                            将助手发布至钉钉
                          </el-text>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="assistant-publish-right">

                  <div v-if ="current_publish_way=='NextConsole'">
                    <div v-if="!assistant_choose.assistant_publish_shop_id" class="assistant-publish-area">
                      <div style="display: flex;flex-direction: column">
                        <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #101828">
                          助手发布
                        </el-text>
                        <el-text style="font-size: 14px;font-weight: 400;line-height: 20px;color: #475467">
                          您可以将助手发布到助手商店，分享给其他人使用
                        </el-text>
                      </div>

                      <div style="display: flex;align-content: center;justify-content: center">
                        <el-button style="border-radius: 8px;width: 150px; height: 45px;
                     background: #1570ef;padding: 10px 18px;border: 1px solid #1570EF"
                                   @click="publish_assistant"
                        >
                          <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #FFFFFF;">
                            发布至助手商店
                          </el-text>
                        </el-button>
                      </div>
                    </div>
                    <div v-else class="assistant-publish-area">
                      <div style="display: flex;flex-direction: column">
                        <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #101828">
                          助手下线
                        </el-text>
                        <el-text style="font-size: 14px;font-weight: 400;line-height: 20px;color: #475467">
                          从助手商店下线，其他人将无法继续使用！
                        </el-text>
                      </div>
                      <div  style="display: flex;align-content: center;justify-content: center">
                        <el-button style="border-radius: 8px;width: 150px; height: 45px;
                     background: #D92D20;padding: 10px 18px;border: 1px solid #D92D20"
                                   @click="unpublished_assistant"
                        >

                          <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #FFFFFF;">
                            从助手商店下线
                          </el-text>
                        </el-button>
                      </div>
                    </div>
                  </div>
                  <div v-else>
                    <el-empty description="火热开发中，敬请期待"/>
                  </div>

                </div>
              </div>
            </div>
            <div class="detail-tab-content" v-else-if="assistant_detail_type===3">
              <div class="assistant-add-body" v-if="assistant_choose">

                <div class="assistant-role-edit-box">
                  <div class="assistant-role-edit-header">
                    <div>
                      <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">
                        提示词
                      </el-text>
                    </div>
                    <div>
                      <el-button style="border-radius: 8px" @click="system_prompt_example_vis=true">
                        <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054">示例</el-text>
                      </el-button>
                      <el-button style="margin-left: 16px;border-radius: 8px">
                        <el-image src="images/cpu.svg"/>
                        <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054;
                        margin-left: 8px;" @click="to_do_something">
                          AI优化
                        </el-text>
                      </el-button>
                      <el-dialog v-model="system_prompt_example_vis" title="示例" :modal="false"
                                 width="640px" top="10vh">

                        <el-input v-model="assistant_role_prompt_template" disabled
                                  type="textarea"
                                  :autosize="{ minRows: 40, maxRows: 40 }"
                        />
                        <template #footer>
                          <div style="width: 100%; display: flex;justify-content: space-between;gap: 8px">
                            <el-button @click="system_prompt_example_copy"
                                       style="border: 1px solid #D0D5DD;
                                       box-shadow: 0 1px 2px 0 #1018280D;
                                        border-radius: 8px;
                                        padding: 10px 18px 10px 18px;
                                        width: 100%;

  ">
                              <el-image src="images/copy.svg"></el-image>
                              <el-text style="
                              margin-left: 8px;
                              font-size: 16px;
                              font-weight: 600;
                              line-height: 24px;">复制
                              </el-text>
                            </el-button>
                            <el-button @click="system_prompt_example_vis = false"
                                       style="
                                       border: 1px solid #1570EF;
                                       background: #1570EF;
                                       box-shadow: 0 1px 2px 0 #1018280D;
                                        border-radius: 8px;
                                        padding: 10px 18px 10px 18px;
                                        width: 100%;
  "
                            >
                              <el-text style="color: #FFFFFF;font-size: 16px;
                              font-weight: 600;
                              line-height: 24px;
                              ">确 定
                              </el-text>
                            </el-button>
                          </div>
                        </template>
                      </el-dialog>
                    </div>
                  </div>
                  <div class="assistant-role-edit-body">

                    <el-input type="textarea" v-model="assistant_choose.assistant_role_prompt"
                              class="assistant-role-edit-area"
                              :autosize = "{ minRows: assistant_role_prompt_rows, maxRows: assistant_role_prompt_rows }"
                              :placeholder="assistant_role_prompt_template"
                              :key="assistant_role_edit_resize_cnt"

                    />

                  </div>
                </div>

                <div class="assistant-role-setting-box" v-if="pick_assistant_role_edit">
                  <div class="assistant-role-edit-header">
                    <div>
                      <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">
                        设置
                      </el-text>
                    </div>
                    <div>
                      <el-button style="border-radius: 8px;background: #EFF8FF;border: 1px solid #1570EF; gap: 8px;
                    display: flex;justify-content: space-between"
                                 @click="assistant_model_detail_vis=true">
                        <el-image src="images/openai.svg" style="margin-right: 4px"/>
                        <el-text style="margin-right: 4px"> {{ assistant_choose.assistant_model_name }}</el-text>
                        <el-tag style="margin-right: 4px;border-radius: 16px;border: 1px solid #B2DDFF">
                          chat
                        </el-tag>
                        <el-image src="images/parent_component.svg"/>
                      </el-button>
                      <el-dialog v-model="assistant_model_detail_vis" :modal="false" width="500px">
                        <div class="model-detail-box">
                          <el-text style="margin-right: 20px">模型类型</el-text>
                          <div style="flex: 1">
                            <el-select v-model="assistant_choose.assistant_model_name" style="width: 100%;">
                              <el-option v-for="model in model_list" :value="model.llm_name"/>

                            </el-select>
                          </div>
                        </div>
                        <div class="model-detail-box">
                          <el-text style="margin-right: 20px">模型温度</el-text>
                          <div style="flex: 1">
                            <el-slider v-model="assistant_choose.assistant_model_temperature" :step="0.1"
                                       :max="2"
                                       :marks="marks"
                            />
                          </div>
                        </div>
                      </el-dialog>
                    </div>
                  </div>
                  <div class="assistant-role-edit-body">
                    <div class="assistant-role-base-info-box">
                      <div class="role-base-info-label">
                        <el-button @click="show_role_base_info = !show_role_base_info" v-if="show_role_base_info"
                                   style="display: flex;align-items: center;width: 24px;height: 24px;background: #F9FAFB;
                           border: 0; " >
                          <el-image src="images/arrow_down.svg"  style="width: 24px;height: 8px"/>
                        </el-button>
                        <el-button @click="show_role_base_info = !show_role_base_info" v-else
                                   style="display: flex;align-items: center;width: 24px;height: 24px"
                                   text
                        >
                          <el-image src="images/chevron-right.svg" style="width: 8px;height: 24px"/>
                        </el-button>
                        <el-text style="margin-left: 6px;font-weight: 500;line-height: 24px;color: #101828">基础信息</el-text>
                      </div>
                      <div class="role-base-info-body" v-if="show_role_base_info">
                        <div>
                          <div style="margin-bottom: 6px">
                            <el-text>助手编号</el-text>
                          </div>
                          <el-input v-model="assistant_choose.id" disabled/>
                        </div>
                        <div>
                          <div style="margin-bottom: 6px">
                            <el-text>助手名称</el-text>
                          </div>
                          <el-input v-model="assistant_choose.assistant_name"/>
                        </div>
                        <div>
                          <div style="margin-bottom: 6px">
                            <el-text>助手描述</el-text>
                          </div>
                          <el-input v-model="assistant_choose.assistant_desc" type="textarea"
                                    :autosize="{ minRows: 5, maxRows: 5 }"
                                    class="assistant-desc-input-textarea"
                                    placeholder="请输入简单易懂的能力描述"/>
                        </div>
                        <div>
                          <div style="margin-bottom: 6px">
                            <el-text>助手脑容量</el-text>
                          </div>
                          <el-slider v-model="assistant_choose.assistant_memory_size"
                                     :step="1"
                                     show-stops :max="10"/>
                        </div>
                        <div style="display: flex;flex-direction: row;padding: 8px;
                       justify-content: space-between;align-items: center;border-bottom: 1px solid #D0D5DD">
                          <div style="display: flex;align-items: center">
                            <div style="margin-right: 12px">
                              <el-text>头像</el-text>
                            </div>
                            <el-avatar :src="assistant_choose.assistant_avatar_url ? assistant_choose.assistant_avatar_url : assistant_choose.assistant_avatar"/>
                          </div>
                          <div style="display: flex;flex-direction: row">
                            <el-upload
                                ref="upload_avatar"
                                :action="api.assistant_avatar_upload"
                                :auto-upload="false"
                                :on-change="handle_avatar_change"
                                :show-file-list="false"
                                :limit="1"
                                :on-exceed="handle_exceed"
                                name="avatar"
                                :headers="assistant_avatar_upload_header"
                                :data="assistant_choose_avatar_upload_data"


                            >

                              <template #trigger>
                                <el-button text style="padding: 12px">
                                  <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color:#475467">
                                    上传
                                  </el-text>
                                </el-button>
                              </template>
                            </el-upload>
                            <el-button text style="padding: 12px" @click="to_do_something">
                              <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color:#175CD3">
                                AI 生成
                              </el-text>
                            </el-button>
                          </div>
                        </div>
                        <div>
                          <div style="margin-bottom: 6px">
                            <el-text>检索标签</el-text>
                          </div>

                          <div style="height: 100px;
                           border: 1px solid #D0D5DD;box-shadow: 0 1px 2px 0 #1018280D;border-radius: 8px;
                           padding: 12px 16px;
                           gap: 8px;
">
                            <el-tag
                                v-for="tag in assistant_choose.assistant_tags"
                                :key="tag"
                                closable
                                :disable-transitions="false"
                                @close="handle_tag_close(tag)"
                                style="margin: 8px"
                            >
                              {{ tag }}
                            </el-tag>
                            <el-input
                                v-if="inputVisible"
                                ref="InputRef"
                                v-model="inputValue"
                                style="width: 100px"
                                size="small"
                                @keyup.enter="handleInputConfirm"
                                @blur="handleInputConfirm"
                            />
                            <el-button v-else class="button-new-tag" size="small" @click="showInput">
                              + 新标签
                            </el-button>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="assistant-role-kg-info-box">
                      <div class="assistant-role-kg-info-label">
                        <div style="display: flex;flex-direction: row;">
                          <el-button @click="show_role_kg_info = !show_role_kg_info" v-if="show_role_kg_info"
                                     style="display: flex;align-items: center;width: 24px;height: 24px;background: #F9FAFB;
                           border: 0; " >
                            <el-image src="images/arrow_down.svg"  style="width: 24px;height: 8px"/>
                          </el-button>
                          <el-button @click="show_role_kg_info = !show_role_kg_info" v-else
                                     style="display: flex;align-items: center;width: 24px;height: 24px"
                                     text
                          >
                            <el-image src="images/chevron-right.svg" style="width: 8px;height: 24px"/>
                          </el-button>
                          <el-text style="margin-left: 6px;font-weight: 500;line-height: 24px;color: #101828">知识库</el-text>
                        </div>
                        <div style="display: flex;flex-direction: row;align-items: center;justify-content: space-between">
                          <el-image src="images/settings_01_grey.svg" style="width: 20px;height: 20px;cursor: pointer"
                                    @click="dia_assistant_kg_setting_vis = true"
                          />
                          <el-popover placement="bottom" :width="520" trigger="click">
                            <template #reference>
                              <el-button text>
                                <el-text style="color:#175CD3;font-size: 24px">+</el-text>
                              </el-button>
                            </template>
                            <el-input :prefix-icon="Search" v-model="Current_assistant_kg_keyword"
                                      @change="search_assistant_kg_list"
                            />
                            <div style="margin: 12px">
                              <el-text v-if="!Current_assistant_kg_keyword">
                                最近添加
                              </el-text>
                              <el-text v-else>
                                搜索结果
                              </el-text>
                            </div>

                            <el-table :data="Current_assistant_kg_list" :show-header="false"
                                      tooltip-effect="light" :show-overflow-tooltip="true"
                                      @row-click="add_assistant_kg"
                            >
                              <el-table-column width="50" property="kg_icon" label="图标" >
                                <template #default="{row}">
                                  <el-avatar :src="row.kg_icon ? row.kg_icon: 'images/kg_default_icon.svg'"
                                             style="width: 24px;height: 24px"/>
                                </template>
                              </el-table-column>
                              <el-table-column width="120" property="create_time" label="创建时间" />
                              <el-table-column width="150" property="kg_name" label="名称" />
                              <el-table-column width="150" property="kg_desc" label="描述" />
                            </el-table>
                          </el-popover>

                        </div>
                      </div>
                      <div class="kg_list" v-if="show_role_kg_info">
                        <div v-for="(kg,_) in assistant_choose.assistant_knowledge_base" class="kg_item">
                          <div>
                            <el-text>{{kg.kg_name}}</el-text>
                          </div>
                          <div>
                            <el-popconfirm title="确定要移除该知识库么?" confirm-button-text="确定"
                                           cancel-button-text="取消" @confirm="remove_assistant_kg(kg)">
                              <template #reference>
                                <el-button style="background: #F9FAFB;border: 0" >
                                  <el-image src="images/delete.svg"/>
                                </el-button>
                              </template>
                            </el-popconfirm>

                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="assistant-function-setting-box" v-else>
                  <div class="assistant-role-edit-header">
                    <div>
                      <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">
                        提示词
                      </el-text>
                    </div>
                    <div>
                      <el-button style="border-radius: 8px">
                        <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054">示例</el-text>
                      </el-button>
                      <el-button style="margin-left: 16px;border-radius: 8px">
                        <el-image src="images/cpu.svg"/>
                        <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054;
                      margin-left: 8px;">
                          AI优化
                        </el-text>
                      </el-button>
                    </div>
                  </div>

                  <div class="assistant-role-edit-body">

                    <el-input type="textarea" v-model="assistant_choose.assistant_role_prompt"
                              class="assistant-role-edit-area"
                              autosize

                    />

                  </div>
                </div>
                <div class="assistant-test-box">
                  <div class="assistant-test-header">
                    <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">
                      调试
                    </el-text>
                  </div>
                  <div class="assistant-test-body" >

                    <NextConsole v-if="show_test_console_flag"
                                 :test_model="true"
                                 :test_assistant="assistant_choose"
                    />

                  </div>


                </div>
              </div>
            </div>
        </div>
        <div v-else-if="assistant_view_model === 0" class="assistant-list-body">
          <div class="assistant-card" v-for="(item , index) in assistantList">
            <div class="assistant-card-head">
              <div class="assistant-card-info">
                <el-avatar :src="item.assistant_avatar" style="width: 40px;height: 40px"/>
                <div style="flex: 1">


                  <el-tooltip v-if="item.assistant_name.length > 5" effect="light">

                    <el-text style="margin-left: 8px;font-size: 16px;font-weight: 600;line-height: 24px;">

                      {{ omit_assistant_desc(item.assistant_name, 5) }}
                    </el-text>
                    <template #content>
                      <div v-text="item.assistant_name" style="max-width: 400px;display: flex;flex-wrap: wrap">

                      </div>
                    </template>
                  </el-tooltip>
                  <el-text v-else style="margin-left: 8px;font-size: 16px;font-weight: 600;line-height: 24px;">
                    {{ item.assistant_name }}
                  </el-text>

                  <el-text v-if="show_cnt_tag"
                           style="margin-left: 8px;  font-size: 14px; font-weight: 400; line-height: 20px;">
                    {{ item.call_cnt }}
                  </el-text>
                  <el-text v-else style="margin-left: 8px;  font-size: 14px; font-weight: 400; line-height: 20px;">
                    {{item.authority_create_time.split(' ')[0]}}
                  </el-text>

                  <br>
                  <el-tooltip v-if="item.assistant_desc.length > 8" effect="light">

                    <el-text style="margin-left: 8px;  font-size: 14px; font-weight: 400; line-height: 20px;"
                    >
                      {{ omit_assistant_desc(item.assistant_desc,8) }}
                    </el-text>
                    <template #content>
                      <div v-text="item.assistant_desc" style="max-width: 400px;display: flex;flex-wrap: wrap">

                      </div>
                    </template>
                  </el-tooltip>
                  <el-text style="margin-left: 8px;  font-size: 14px; font-weight: 400; line-height: 20px;"
                           v-else
                  >
                    {{ item.assistant_desc }}
                  </el-text>


                </div>
                <div>
                  <el-switch v-model="item.assistant_is_start"
                             style="--el-switch-on-color: #1570EF"
                             @change="start_assistant(item)"
                  >

                  </el-switch>
                </div>

              </div>

              <div class="assistant-card-tag" style="width: 100%;">

                <el-tag v-for="(tag , index) in item.assistant_tags.slice(0, 3)" :key="index" style="margin-right: 8px;">
                  {{ tag }}
                </el-tag>


              </div>

            </div>
            <div class="assistant-card-footer">
              <el-button text class="assistant-card-footer-button" @click="
              assistant_deleted=item;
              assistant_delete_vis=true;"
                         v-if="item.id >0"
              >
                <el-text class="button-text">删除</el-text>
              </el-button>
              <el-button text color="#175CD3" class="assistant-card-footer-button"
                         v-if="item.id >0"
                         @click="change_assistant_view_model(1, item, 1)">
                <el-text style="color: #175CD3;" class="button-text">查看</el-text>
              </el-button>
            </div>

          </div>
          <div class="assistant-delete-confirm-box">
            <el-dialog v-model="assistant_delete_vis" width="480px" >
              <template #header>
                <el-text style="font-size: 18px;font-weight: 600;line-height: 28px;color: #101828">删除确认</el-text><br>
                <el-text>是否确认删除，删除操作不可逆</el-text>
              </template>
              <template #footer>
                <div style="display: flex;flex-direction: row;gap: 12px; height: 70px;
              align-items: center">
                  <el-button @click="assistant_delete_vis=false" style="
              width: 210px;height:44px;border-radius: 8px;gap: 8px; padding: 10px 18px 10px 18px;
              border: 1px solid #D0D5DD;box-shadow: 0 1px 2px 0 #1018280D;">
                    <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #344054">取消</el-text>
                  </el-button>
                  <el-button @click="delete_assistants" style="
              background: #D92D20;width: 210px;height:44px;border-radius: 8px;gap: 8px; padding: 10px 18px 10px 18px;
              border: 1px solid #D92D20;box-shadow: 0 1px 2px 0 #1018280D;">
                    <el-text style="font-size: 16px;font-weight: 600;line-height: 24px;color: #FFFFFF">删除</el-text>
                  </el-button>
                </div>
              </template>

            </el-dialog>
          </div>
          <div  v-if="!assistantList.length" style="width: 100%;height: 50vh;flex-grow: 1;
          display: flex;align-items: center;justify-content: center">
            <el-empty
                      :description="assistant_key_word ? '暂无搜索结果': '还没有自建助手，赶快来创建一个吧！'"/>
          </div>

        </div>

      </el-scrollbar>
      <div class="assistant-list-footer" v-if="!assistant_view_model">
        <div class="assistant-list-footer-box">
          <el-button class="assistant-footer-button" @click="change_page(-1)">
            <el-image src="images/arrow_left_black.svg" style="margin-right: 8px"/>
            上一页
          </el-button>
          <el-pagination
              :total="assistants_cnt"
              layout="pager,total"
              :page-size="current_page_size"
              v-model:current-page="current_page_num"
              @current-change="handle_current_change"
          />
          <el-button class="assistant-footer-button" @click="change_page(1)">
            下一页
            <el-image src="images/arrow_right_black.svg" style="margin-left: 8px"/>
          </el-button>
        </div>
      </div>

    </div>
  </div>
  <el-dialog class="assistant-kg-setting" :modal="false" :close-on-click-modal="false"
             :width="600" top="50vh"
             v-model="dia_assistant_kg_setting_vis">
    <template #header>
      <div style="border-bottom: #EAECF0 1px solid;padding: 20px 0">
        <el-text class="next-console-text-bold">助手知识库检索设置</el-text>
      </div>

    </template>

    <div class="kg-main-box-detail-rag-area" style="gap: 20px">
      <div  style="width: 140px">
        <el-text>检索设置</el-text>
      </div>
      <div  >
        <div>
          <div>
            <el-text>混合检索系数（0代表完全偏向字符关键词检索，1代表完全偏向语义相似度检索）</el-text>
            <el-slider v-model="assistant_choose.rag_factor"
                       :max="1" :step="0.01"
            />
          </div>
        </div>
        <div>
          <div>
            <el-text>最小语义相关度系数（低于这个阈值代表检索到的文本与问题无关）</el-text>
            <el-slider v-model="assistant_choose.rag_relevant_threshold"
                       :max="1" :step="0.01"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="kg-main-box-detail-rag-area" style="gap: 20px;" >
      <div  style="width: 140px">
        <el-text>不相关托底方案</el-text>
      </div>
      <div style="width: 100%">
        <el-radio-group v-model="assistant_choose.rag_miss">
          <el-radio :label="1">大模型托底回答</el-radio>
          <el-radio :label="0">自定义托底回答</el-radio>
        </el-radio-group>
        <div v-if="assistant_choose.rag_miss===0">
          <el-input type="textarea" v-model="assistant_choose.rag_miss_answer"
                    :autosize = "{ minRows: 5, maxRows: 5 }"
                    resize="none"
                    placeholder="请输入自定义托底回答"/>
        </div>
      </div>

    </div>

    <template #footer>

      <div class="kg-dialog-footer">

        <el-button class="kg-dialog-footer-button"
                   @click="dia_assistant_kg_setting_vis=false">
          <el-text class="kg-button-text" >
            确认
          </el-text>
        </el-button>
      </div>
    </template>
  </el-dialog>

</template>

<style scoped>

.assistant-center{
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.detail-tabs-head{
  max-height: 44px;
  border: 1px solid #EAECF0;
  background-color: #f9fafb;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap:8px;
  padding: 8px 24px;

}
.detail-tab{
  width: 92px;
  height: 44px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.detail-tab-activate{
  background-color: #FFFFFF;
  box-shadow: 0 1px 3px 0 #1018281A;

}
.detail-tab-text{

  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  text-align: left;
  color: #667085;
}
.detail-tab-text-activate{
  color: #344054;
}

.assistant-role-edit-area :deep(.el-textarea__inner) {
  font-size: 16px;
  font-weight: 500;
  line-height: 21px;
  color: #067647;
  box-shadow: 0 0 0 0;
  resize: none;
}
.assistant-role-edit-area :deep(.el-textarea__inner::-webkit-scrollbar){
  width: 6px ;
  height: 6px ;
}
.assistant-role-edit-area :deep(.el-textarea__inner::-webkit-scrollbar-thumb) {
  border-radius: 3px ;
  -moz-border-radius: 3px ;
  -webkit-border-radius: 3px ;
  background-color: #c3c3c3 ;
}
.assistant-role-edit-area :deep(.el-textarea__inner::-webkit-scrollbar-track) {
  background-color: transparent ;
}



.msg-input :deep(.el-textarea__inner) {
  resize: none;
}




.role-base-info-body :deep(.el-textarea__inner) {
  resize: none;
}


.el-textarea :deep(.el-textarea__inner) {
  resize: none;
}

.el-avatar {
  --el-avatar-bg-color: #FFFFFF !important;
}
.assistant-delete-confirm-box :deep(.el-dialog__body) {
  padding: 0 !important;
}


.assistant-desc-input-textarea :deep(.el-textarea__inner::-webkit-scrollbar){
  width: 6px ;
  height: 6px ;
}


.assistant-desc-input-textarea :deep(.el-textarea__inner::-webkit-scrollbar-thumb) {
  border-radius: 3px ;
  -moz-border-radius: 3px ;
  -webkit-border-radius: 3px ;
  background-color: #c3c3c3 ;
}
.assistant-desc-input-textarea :deep(.el-textarea__inner::-webkit-scrollbar-track) {
  background-color: transparent ;
}

.assistant-desc-input-textarea :deep(.el-input__count){
  background: none;
  bottom: -20px;
  right: 80px;
}
.assistant-detail-tab :deep(.el-tabs__content){
  padding: 0;
}

.assistant-monitor-header{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  border-bottom: 1px solid #D0D5DD;


}

.assistant-list {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.assistant-list-header {
  height: 40px;
  border-bottom: 1px solid #D0D5DD;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px 12px 24px;
}

.step-router {

  height: 40px;
  display: flex;
  flex-direction: row;

}

.step-button {
  border: 0;
}

.el-button {
  margin-left: 0;
}

.order-button {
  border: 1px solid #D0D5DD;
  box-shadow: 0 1px 2px 0 #1018280D;
  border-radius: 8px;

}

.order-button-left {
  border-width: 0 1px 0 0;
  border-radius: 8px;
  background: #F9FAFB;
  height: 40px
}

.order-button-right {
  border-width: 0 0 0 1px;
  border-radius: 8px;
  background: #F9FAFB;
  height: 40px
}

.order-button-default {
  border: 0;
  border-radius: 8px;
  height: 40px
}

.right-button-box {
  width: 500px;
  height: 56px;
  gap: 8px;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.el-select :deep(.el-input--suffix) {
  height: 40px;
}

.assistant-list-body {
  flex: 1;
  display: flex;
  gap: 16px;
  padding: 16px;
  flex-wrap: wrap;
  align-content: flex-start;
  margin: 0 24px;
}

.assistant-card {
  width: 350px;
  min-width: 250px;
  border: 1px solid #D0D5DD;
  box-shadow: 0 1px 2px 0 #1018280D;
  border-radius: 12px;
  background-color: #FFFFFF;
}

.assistant-card-head {
  height: 94px;
  padding: 24px;
  gap: 24px;
  display: flex;
  flex-direction: column;
}

.assistant-card-info {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  justify-content: space-between;

}
.assistant-card-head:hover {
  border-bottom: 1px solid #D0D5DD;
}

.assistant-card-footer {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  border-top: 1px solid #EAECF0;
  padding: 0;
}

.assistant-list-footer {
  height: 80px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.assistant-list-footer-box {
  width: 100%;
  margin: 0 24px;
  border-top: 1px solid #D0D5DD;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 0 16px 0
}

.assistant-card-footer-button {
  width: 80px;
  height: 50px;
  border-radius: 16px;

}

.el-pagination :deep(.is-active) {
  background: #F9FAFB
}

.button-text {

  font-size: 14px;
  font-weight: 600;
  line-height: 20px;

  text-align: left;
  color: #475467;
}

.assistant-footer-button {
  border: 1px solid #D0D5DD;
  box-shadow: 0 1px 2px 0 #1018280D;
  display: flex;
  justify-content: space-between;
  background: #FFFFFF;

}

.assistant-edit-step {
  height: 44px;
  border: 1px solid #EAECF0;
  background: #EAECF0;
  display: flex;
  align-items: center;
}

.assistant-role-button-picked {
  background: #FFFFFF;

}

.assistant-function-button-picked {
  background: #FFFFFF;
  box-shadow: 0 1px 2px 0 #1018280F;


}

.assistant-add-body {
  flex: 1;
  display: flex;
  flex-direction: row;
  height: 100%;


}

.assistant-role-edit-box {
  min-width: 400px;
  width: 600px;
  height: 100%;
  border-right: 1px solid #D0D5DD;
  display: flex;
  flex-direction: column;
  overflow-y: hidden;
}

.assistant-role-edit-header {
  display: flex;
  justify-content: space-between;
  padding: 10px 16px 10px 16px;
  border-bottom: 1px solid #D0D5DD;
}

.assistant-role-setting-box {
  min-width: 400px;
  width: 600px;
  border-right: 1px solid #D0D5DD;
}

.assistant-function-setting-box {
  width: 600px;
}

.assistant-test-box {
  width: 600px;
  min-width: 600px;
  flex: 1;
}
.assistant-role-base-info-box {
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid #D0D5DD
}

.role-base-info-label {
  background: #F9FAFB;
  padding: 12px 16px 12px 16px;
  height: 24px;
  display: flex;
  align-items: center;
  flex-direction: row;
}

.role-base-info-body {
  padding: 12px 16px 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.assistant-role-kg-info-label {
  background: #F9FAFB;
  padding: 12px 16px 12px 16px;
  height: 24px;
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: space-between;
}

.kg_list {
  padding: 12px 16px 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.kg_item {
  background: #F9FAFB;
  padding: 8px 12px 8px 12px;
  display: flex;
  justify-content: space-between;
}

.assistant-test-header {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px 12px 16px;
  border-bottom: 1px solid #D0D5DD;

}

.assistant-test-body {

  padding: 12px 16px 12px 16px;
  display: flex;
  flex: 1;
  flex-direction: column;


}

.assistant-test-footer {
  border-top: 1px solid #D0D5DD;
  padding: 12px;
  height: 56px;
  display: flex;
  justify-content: center;
  align-items: center;
}



.assistant-author-info{
  display: flex;
  flex-direction: row;
  gap: 24px;
}
.assistant-detail-info-button-box{
  display: flex;
  flex-direction: row;
  gap: 16px;

}

.model-detail-box {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 16px 24px 16px 24px;
  border-bottom: 1px solid #EAECF0;

}

.assistant-monitor-box{

}

.assistant-monitor-body{
  display: flex;
  flex-direction: row;
  gap: 16px;
  padding: 16px;
  flex-wrap: wrap;
  align-content: flex-start;
  margin: 0 24px;
}
.assistant-publish-box{
  display: flex;
  flex-direction: row;
  height: calc( 100vh - 170px);


}
.assistant-publish-left{
  width: 20%;
  height: 100%;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #EAECF0


}
.assistant-publish-left-head{
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 12px 24px;
  border-width: 1px 0 1px 0;

  border-style: solid;

  border-color: #EAECF0;
}

.assistant-publish-left-body{
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px 16px;
  flex-wrap: wrap;
  align-content: flex-start;
  flex-grow: 1;


}

.assistant-publish-way-box{
  display: flex;
  flex-direction: row;
  gap: 4px;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #EAECF0;
  background-color: #FFFFFF;
  width: calc(100% - 32px);

}
.assistant-publish-way-box:hover{
  border: 1px solid #2E90FA;
  background-color: #EFF8FF;
  cursor: pointer;

}

.assistant-publish-way-box-activate{

  border: 1px solid #2E90FA;
  background-color: #EFF8FF;

}
.assistant-publish-way-name{
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  letter-spacing: 0;
  text-align: left;
  color: #344054;
}
.assistant-publish-way-desc{

  font-size: 12px;
  font-weight: 400;
  line-height: 18px;
  letter-spacing: 0;
  text-align: left;
  color: #475467;

}
.assistant-publish-right{
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80%;
}

.assistant-publish-area{
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-content: center;
  justify-content: center;

}


</style>
