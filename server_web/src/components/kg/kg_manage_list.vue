<script lang="ts"  setup>
import {onBeforeUnmount, onMounted} from 'vue';
import {ElInput, ElScrollbar} from "element-plus";
import {Search} from "@element-plus/icons-vue";

import './kg_center.scss'
import {
  CurrentKeyword,
  CurrentKg,
  CurrentKgList,
  CurrentKgPageNum,
  CurrentKgPageSize,
  CurrentKgPublic,
  CurrentKgTotal,
  CurrentKgType,
  CurrentListKgType,
  delete_current_kg,
  dialog_v_add_kg,
  dialog_v_delete_confirm,
  enter_kg_add,
  enter_kg_detail,
  search_kgs,
  switch_delete_dialog,
} from "@/components/kg/kg_process";
import {check_kg_permission, isAdmin, scrollbarHeight,} from "@/components/kg/kg_center_base";
import router from "@/router";
import {user_info} from "@/components/user_center/user";
import {get_user} from "@/api/user_center";
import {omit_text} from "@/utils/base"
const props = defineProps({

  page_num: {
    type: String,
    required: false,
    default: '1'
  },
  page_size: {
    type: String,
    required: false,
    default: '20'
  }
});
async function handleResize(){
  scrollbarHeight.value = window.innerHeight - 220

}
async function handleSizeChange  (val: number)   {
  CurrentKgPageSize.value = val
  await router.push({
    query: {

      page_size: val,
      page_num: CurrentKgPageNum.value}})
  await search_kgs()

}
async function handleCurrentChange(val: number) {
  CurrentKgPageNum.value = val
  await router.push({query: {
    page_size: CurrentKgPageSize.value, page_num: val}})
  await search_kgs()

}

onMounted(async () => {
      window.addEventListener('resize', handleResize);
      await handleResize()
      if(!user_info.value){
        user_info.value = (await get_user({})).result
      }
      isAdmin.value = user_info.value?.user_role.includes('admin')
          || user_info.value?.user_role.includes('super_admin')
          || user_info.value?.user_role.includes('next_console_admin')

      if (props.page_num){
        try {
          CurrentKgPageNum.value = parseInt(props.page_num)
        } catch (e) {
          CurrentKgPageNum.value = 1
        }

      }
      if (props.page_size){
        try {
          CurrentKgPageSize.value = parseInt(props.page_size)
        } catch (e) {
          CurrentKgPageSize.value = 20
        }
      }
       await search_kgs()
    }
)
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  }
)

</script>

<template>
  <el-container>
    <el-header style="padding: 0 !important;" height="67px">

      <div class="kg-op-header">
        <div class="kg-op-header-left">
          <div class="kg-op-step">
            <div>
              <el-button disabled class="kg-op-step-button">
                <el-image src="images/arrow_left_grey.svg" style="width: 14px;height: 14px"/>
              </el-button>

            </div>
            <div>
              <el-button disabled class="kg-op-step-button">
                <el-image src="images/arrow_right_grey.svg" style="width: 14px;height: 14px"/>
              </el-button>
            </div>
          </div>
        </div>

        <div class="kg-op-header-right">
          <div class="kg-op-header-list-box">
            <div class="kg-op-header-search" style="width: 150px">
              <el-input placeholder="搜索知识库" v-model="CurrentKeyword" @change="search_kgs"
                        :prefix-icon="Search" style="width: 150px" clearable>
              </el-input>
            </div>
            <div class="kg-op-header-search" style="width: 100px" >
              <el-select v-model="CurrentListKgType" @change="search_kgs" style="width: 100px"
                         clearable
                         placeholder="类型"
              >
                <el-option label="全部" value="All"/>
                <el-option label="离线文档" value="file"/>
                <el-option label="在线站点" value="website"/>
                <el-option label="脚本代码库" value="script"/>
                <el-option label="FAQ" value="faq"/>
              </el-select>
            </div>
            <div class="kg-op-header-search" style="width: 100px" >
              <el-select v-model="CurrentKgPublic" @change="search_kgs" style="width: 100px"
                         clearable
              >
                <el-option label="全部" :value="-1"/>
                <el-option label="个人" :value="0"/>
                <el-option label="团队公开" :value="1"/>
                <el-option label="团队成员" :value="2" v-if="isAdmin"/>
              </el-select>
            </div>
            <div class="kg-op-header-create">
              <el-button @click="dialog_v_add_kg=true" class="kg-add-button">
                <div>
                  <el-image src="images/folder_plus_white.svg" style="width: 20px;height: 20px"/>
                </div>
                <div style="margin-left: 8px">
                  <el-text class="kg-button-text">新增知识库</el-text>
                </div>

              </el-button>
            </div>
          </div>
        </div>
      </div>

    </el-header>

    <el-main style="height: calc(100vh - 180px)">
        <el-scrollbar >
        <div class="kg-main-box" >
          <div class="kg-main-box-list" >
            <div v-for="(kg,_) in CurrentKgList" class="kg-card">
              <div class="kg-card-body">
                <div class="kg-card-body-info">
                  <div class="kg-card-body-info-left">
                    <div>
                      <el-avatar :src="kg.kg_icon ? kg.kg_icon : 'images/kg_default_icon.svg'"
                                 style="background: #FFFFFF"
                      />
                    </div>
                    <div class="kg-card-body-info-middle">
                      <div>
                        <el-tooltip :content="kg.kg_name" v-if="kg.kg_name.length > 20" effect="light">
                          <el-text>{{omit_text(kg.kg_name,20)}}</el-text>
                          <template #content>
                            <div v-text="kg.kg_name" style="max-width: 400px;
                            display: flex;flex-wrap: wrap">

                            </div>
                          </template>
                        </el-tooltip>
                        <el-text v-else>{{kg.kg_name}}</el-text>
                      </div>
                      <div style="display:flex;flex-direction: row;align-items: center;justify-content: center;gap: 8px">
                        <div>
                          <el-text>{{kg.create_time}}</el-text>
                        </div>

                        <div
                            style="display:flex;flex-direction: row;align-items: center;justify-content: center;gap: 4px">
                          <div style="width: 16px;height: 16px;">
                            <el-avatar :src="kg.kg_author_avatar" style="width: 16px;height: 16px;background-color: #FFFFFF"/>
                          </div>
                          <div>
                            <el-tooltip v-if="kg.kg_author_name && kg.kg_author_name.length > 3" effect="light">
                              <el-text style="font-size: 14px;font-weight: 400;line-height: 20px;color: #475467;">
                                {{omit_text(kg.kg_author_name,3)}}
                              </el-text>
                              <template #content>
                                <div v-text="kg.kg_author_name" style="max-width: 400px;display: flex;flex-wrap: wrap"/>
                              </template>
                            </el-tooltip>
                            <el-text v-else style="font-size: 14px;font-weight: 400;line-height: 20px;color: #475467;">
                              {{kg.kg_author_name}}
                            </el-text>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="kg-card-body-info-left">
                    <div v-if="check_kg_permission(kg,'write')">
                      <el-button class="kg-op-step-button" @click="switch_delete_dialog(kg)">
                        <el-image src="images/trash_01_grey.svg"
                                  style="width: 20px; height: 20px"/>
                      </el-button>
                    </div>
                  </div>
                </div>
                <div class="kg-card-body-sub-info">
                  <el-tooltip v-if="kg.kg_desc && kg.kg_desc.length > 32" effect="light">
                    <el-text>{{omit_text(kg.kg_desc,32)}}</el-text>
                    <template #content>
                      <div v-text="kg.kg_desc" style="max-width: 400px;display: flex;flex-wrap: wrap"/>
                    </template>
                  </el-tooltip>
                  <el-text v-else>{{kg.kg_desc}}</el-text>
                </div>
              </div>
              <div class="kg-card-foot">
                <div class="kg-card-foot-left">
                  <div class="kg-card-foot-col">
                    <div>
                      <el-image src="images/file_06_grey.svg" class="kg-card-foot-col-icon"/>
                    </div>
                    <div style="display: flex;width: 100%">
                      <el-text class="kg-card-foot-col-text">{{ kg.doc_cnt }}文档</el-text>
                    </div>


                  </div>
                  <!--          <div class="kg-card-foot-col">-->
                  <!--            <div>-->
                  <!--              <el-image src="images/file_07_grey.svg" class="kg-card-foot-col-icon"/>-->
                  <!--            </div>-->
                  <!--            <div style="display: flex;width: 100%">-->
                  <!--              <el-text class="kg-card-foot-col-text">0 千字符</el-text>-->
                  <!--            </div>-->
                  <!--          </div>-->
                  <!--          <div class="kg-card-foot-col">-->
                  <!--            <el-image src="images/quote_06_grey.svg" class="kg-card-foot-col-icon"/>-->
                  <!--            <el-text class="kg-card-foot-col-text">0 引用</el-text>-->
                  <!--          </div>-->
                </div>
                <div class="kg-card-foot-right">
                  <el-button text @click="enter_kg_detail(kg, 'file')">
                    <el-text class="kg-card-enter-text">查看</el-text>
                  </el-button>

                </div>
              </div>
            </div>
            <div class="kg-empty-box" v-if="!CurrentKgList.length">
              <el-empty :description="CurrentKeyword ? '暂无搜索结果' :'还没有知识库，来创建一个吧！'"></el-empty>
            </div>
          </div>
          </div>
        </el-scrollbar>
      </el-main>

    <el-footer height="48px">
      <div class="kg-pagination" >
        <el-pagination
            layout=" total, sizes, prev, pager, next"
            :total="CurrentKgTotal"
            :small="true"
            :page-sizes="[20, 50, 100, 200, 1000]"
            :page-size="CurrentKgPageSize"
            :current-page="CurrentKgPageNum"
            @update:page-size="handleSizeChange"
            @update:current-page="handleCurrentChange"
        />

      </div>
    </el-footer>
  </el-container>
  <el-dialog v-model="dialog_v_delete_confirm" title="删除确认" style="max-width: 600px">
  <div>
    <el-text>删除知识库 {{CurrentKg.kg_name}} ?此操作不可修复！</el-text>
  </div>
  <template #footer>
    <div class="kg-dialog-footer">
      <el-button class="kg-dialog-footer-button" style="background-color: #FFFFFF;
      border: 1px solid #D0D5DD"
                 @click="dialog_v_delete_confirm=false">
        <el-text class="kg-button-text" style="color: #344054">
          取消
        </el-text>
      </el-button>
      <el-button class="kg-dialog-footer-button"
                 @click="delete_current_kg()">
        <el-text class="kg-button-text" >
          确认
        </el-text>
      </el-button>
    </div>

  </template>
</el-dialog>
  <el-dialog v-model="dialog_v_add_kg" title="新增知识库" style="max-width: 600px;min-width: 500px">
    <el-scrollbar wrap-style="width: 100%;" view-style="width: 100%">
      <div class="kg-add-model-area">

        <el-radio-group v-model="CurrentKgType" class="kg-add-model-box" >
          <el-radio class="kg-add-model" label="file">
            <div class="kg-add-model-desc">
              <div class="kg-add-model-icon">
                <el-avatar src="images/kg_add_file.svg"/>
              </div>
              <div class="kg-add-model-name">
                <div style="display:flex;flex-wrap: wrap;width: 100%">
                  <el-text class="kg-add-model-text">离线文档导入</el-text>
                </div>
                <div style="display:flex;flex-wrap: wrap;width: 100%">
                  <el-text class="kg-add-model-text">支持TXT、Markdown、PDF、Word、HTML等文件</el-text>
                </div>
              </div>
            </div>


          </el-radio>
          <el-radio class="kg-add-model" label="website">
            <div class="kg-add-model-desc">
              <div class="kg-add-model-icon">
                <el-avatar src="images/kg_add_website.svg"/>
              </div>
              <div class="kg-add-model-name">
                <div>
                  <el-text class="kg-add-model-text">在线web站点导入</el-text>
                </div>
                <div>
                  <el-text class="kg-add-model-text">支持对Web站点的文档进行在线同步</el-text>
                </div>
              </div>
            </div>


          </el-radio>
          <el-radio class="kg-add-model" label="script">
            <div class="kg-add-model-desc">
              <div class="kg-add-model-icon">
                <el-avatar src="images/kg_add_script.svg"/>
              </div>
              <div class="kg-add-model-name">
                <div>
                  <el-text class="kg-add-model-text">代码脚本导入</el-text>
                </div>
                <div>
                  <el-text class="kg-add-model-text">支持各类常见代码脚本语言</el-text>
                </div>
              </div>
            </div>


          </el-radio>
          <el-radio class="kg-add-model" label="faq">
            <div class="kg-add-model-desc">
              <div class="kg-add-model-icon">
                <el-avatar src="images/kg_add_rag.svg"/>
              </div>
              <div class="kg-add-model-name">
                <div>
                  <el-text class="kg-add-model-text">FAQ</el-text>
                </div>
                <div>
                  <el-text class="kg-add-model-text">第一优先级引用该问答对知识库进行回答</el-text>
                </div>
              </div>
            </div>


          </el-radio>
        </el-radio-group>

      </div>
      </el-scrollbar>
      <template #footer>
        <div class="kg-dialog-footer">
          <el-button class="kg-dialog-footer-button" style="background-color: #FFFFFF;
        border: 1px solid #D0D5DD"
                     @click="dialog_v_add_kg=false">
            <el-text class="kg-button-text" style="color: #344054">
              取消
            </el-text>
          </el-button>
          <el-button class="kg-dialog-footer-button"
                     @click="enter_kg_add()">

            <el-text class="kg-button-text" >
              确认
            </el-text>
          </el-button>
        </div>
      </template>
  </el-dialog>
</template>

<style scoped>
.el-header {
  padding: 0 !important;
}
.el-menu--horizontal.el-menu{
  border-bottom: 0;
}
.kg-pagination{
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.el-button {
  margin-left: 0;
}


.kg-add-meta-item-value-textarea :deep(.el-textarea__inner::-webkit-scrollbar){
  width: 6px ;
  height: 6px ;
}
.kg-add-meta-item-value-textarea :deep(.el-textarea__inner::-webkit-scrollbar-thumb) {
  border-radius: 3px ;
  -moz-border-radius: 3px ;
  -webkit-border-radius: 3px ;
  background-color: #c3c3c3 ;
}
.kg-add-meta-item-value-textarea :deep(.el-textarea__inner::-webkit-scrollbar-track) {
  background-color: transparent ;
}
.kg-op-header-left{
  width: 120px;

}
.kg-op-header{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  border-bottom: 1px solid #D0D5DD;
  width: calc(100% - 24px);

}
.kg-empty-box {
  width: 100%; height: 50vh;display: flex;align-items: center;justify-content: center
}
.kg-op-header-right{
  width: 520px;
}
</style>
