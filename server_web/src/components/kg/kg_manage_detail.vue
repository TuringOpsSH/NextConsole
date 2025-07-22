<script lang="ts"  setup>
import {onBeforeUnmount, onMounted} from 'vue';
import {ElNotification, ElScrollbar} from "element-plus";

import './kg_center.scss'
import {
  commit_new_kg,
  CurrentKg,
  CurrentKgBuildProgress,
  CurrentKgDetail,
  CurrentKgDocList,
  CurrentKgDocPageNum,
  CurrentKgDocPageSize,
  download_loading,
  enter_kg_list,
  get_current_kg,
  show_kg_build_progress,
  switch_kg_detail_type
} from "@/components/kg/kg_process";
import {
  check_kg_permission,
  handleKgDocCurrentChange,
  handleKgDocSizeChange,
  scrollbarHeight,
} from "@/components/kg/kg_center_base";
import Kg_doc_upload from "@/components/kg/doc_kg/kg_upload.vue";
import Kg_web_upload from "@/components/kg/web_kg/kg_upload.vue";
import Kg_code_upload from "@/components/kg/code_kg/kg_upload.vue"
import Kg_faq_upload from "@/components/kg/faq_kg/kg_upload.vue";
import Kg_detail_file from "@/components/kg/kg_detail_file.vue";
import Kg_detail_meta from "@/components/kg/kg_detail_meta.vue";
import {
  current_kg_doc_list,
  CurrentKgDocKeyWord,
  CurrentKgDocRefStatus,
  CurrentKgDocTotal
} from "@/components/kg/doc_process";

import {user_info} from "@/components/user_center/user";
import {get_user} from "@/api/user_center";
import router from "@/router";
import {doc_search, kg_ref_get} from "@/api/kg_center";

const props = defineProps({
  kg_code: {
    type: String,
    required: true,
    default: null,

  },
  info_type : {
    type: String,
    required: false,
    default: "file",
  },
  page_size: {
    type: String,
    required: false,
    default: "20",
  },
  page_num: {
    type: String,
    required: false,
    default: "1",
  },
  keyword: {
    type: String,
    required: false,
    default: "",
  },
  ref_status: {
    type: Array,
    required: false,
    default: () => [],
  }
});
async function handleResize(){
  scrollbarHeight.value = window.innerHeight - 220

}

async function init_kg_detail(){

  if (check_kg_permission(CurrentKg.value, 'read')){
    let progress_params = {
      kg_db_code: CurrentKg.value.kg_code
    }
    let kg_ref_progress = await kg_ref_get(progress_params)
    if (!kg_ref_progress.error_status){
      CurrentKgBuildProgress.value = kg_ref_progress.result
    }
  }
  let kg_doc_params = {
    doc_kg_db_id: CurrentKg.value.kg_code,
    doc_name: CurrentKgDocKeyWord.value,
    page_size: CurrentKgDocPageSize.value,
    page_num: CurrentKgDocPageNum.value
  }
  let response2 = await doc_search(kg_doc_params)
  if (!response2.error_status){
    CurrentKgDocList.value = response2.result.data
    CurrentKgDocTotal.value = response2.result.total
    current_kg_doc_list.value = response2.result.data

  }

}
onMounted(async () => {
      window.addEventListener('resize', handleResize);
      await handleResize()
      if(!user_info.value){
        user_info.value = (await get_user({})).result
      }
      if(props.kg_code){
        await get_current_kg(props.kg_code)
      }
      else {
        ElNotification({
          title: '错误',
          message: '未找到知识库',
          type: 'error'
        });
        await router.push(
            {
              name: 'kg_manage_list',
              query: {
                page_num: 1,
                page_size: 20,
              }
          }
        )
      }
      CurrentKgDetail.value = props.info_type;
      try {
        CurrentKgDocPageNum.value = parseInt(props.page_num)
        CurrentKgDocPageSize.value = parseInt(props.page_size);
      }catch (e) {
        CurrentKgDocPageNum.value = 1
        CurrentKgDocPageSize.value = 20;
      }

      CurrentKgDocKeyWord.value = props.keyword;
      //@ts-ignore
      CurrentKgDocRefStatus.value = props.ref_status;
      await init_kg_detail()
    }
)
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  }
)

</script>

<template>
  <el-container>
    <el-header style="padding: 0 !important;" height="53px">
      <el-scrollbar>
        <div class="kg-op-header">

        <div class="kg-op-header-left">


            <div class="kg-op-step">
              <div>
                <el-button class="kg-op-step-button" @click="enter_kg_list()">
                  <el-image src="images/arrow_left_black.svg" style="width: 14px;height: 14px"/>
                </el-button>

              </div>
              <div>
                <el-button disabled class="kg-op-step-button">
                  <el-image src="images/arrow_right_grey.svg" style="width: 14px;height: 14px"/>
                </el-button>
              </div>
            </div>
            <div class="kg-name-box" v-if="CurrentKg  ">
              <div style="display: flex;align-items: center;justify-content: center">
                <el-text style=" font-size: 16px;font-weight: 600;line-height: 24px;text-align: left;color: #101828;">
                  {{CurrentKg.kg_name}}
                </el-text>
              </div>
              <div  style="display: flex;align-items: center;justify-content: center">
                <el-avatar :src="CurrentKg.kg_icon ? CurrentKg.kg_icon : 'images/kg_default_icon.svg'"
                           style="background: #FFFFFF; margin-left: 12px;width: 32px;height: 32px"/>
              </div>


            </div>


        </div>
        <div class="kg-op-header-middle">
          <div class="kg-op-status-info-item" >
            <el-text style="white-space: nowrap;" v-if="CurrentKg.kg_type=='file'">类型： 文档库 </el-text>
            <el-text style="white-space: nowrap;" v-else-if="CurrentKg.kg_type=='website'">类型： 网页库 </el-text>
            <el-text style="white-space: nowrap;" v-else-if="CurrentKg.kg_type=='script'">类型： 脚本库 </el-text>
            <el-text style="white-space: nowrap;" v-else-if="CurrentKg.kg_type=='faq'">类型： FAQ </el-text>
          </div>
          <div class="kg-op-status-info-item" >
            <el-text style="white-space: nowrap;">状态： {{CurrentKg.kg_status}} </el-text>
          </div>
          <div class="kg-op-status-info-item">
            <el-text style="white-space: nowrap;">构建进度:</el-text>
            <el-progress :percentage="show_kg_build_progress()"
                         type="line" style="width: 100px"/>
          </div>
          <div class="kg-op-status-info-item" >

            <el-text style="white-space: nowrap;">作者： {{CurrentKg.kg_author_name}} </el-text>
          </div>
          <div class="kg-op-status-info-item">
            <el-text style="white-space: nowrap;">文档数： {{CurrentKg.doc_cnt}}</el-text>
          </div>
        </div>
        <div class="kg-op-header-right">

          <div class="kg-op-header-get-box" >

            <div>
              <el-popconfirm title="确定要更新该知识库的所有配置么?" confirm-button-text="确定"
                             cancel-button-text="取消" @confirm="commit_new_kg(false, true)"
                             v-if="check_kg_permission(CurrentKg) && CurrentKgDetail==='meta'">


                <template #reference>

                  <el-button  style="background-color: #1570ef; border: 1px solid #1570EF">
                    <el-image src="images/refresh_white.svg" style="width: 16px;height: 16px;margin-right: 8px"/>
                    <el-text style="font-size: 14px;font-weight: 600;line-height: 20px; color: #FFFFFF">更新</el-text>
                  </el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>

        </div>
      </div>
      </el-scrollbar>
    </el-header>
    <el-main style="height: calc(100vh - 180px)">
      <el-scrollbar   v-loading="download_loading" element-loading-text="下载中，请稍等..."
                      view-style="width: 100%;" wrap-style="width: 100%;"
      >
        <div class="kg-main-box-detail" >
          <div class="kg-main-box-detail-head">
            <div class="kg-main-box-detail-model"
                 :class="CurrentKgDetail=='file' ? 'kg-main-box-detail-model-chosen':''"
                 @click="switch_kg_detail_type('file')">
              <el-text>文档</el-text>
            </div>
            <div class="kg-main-box-detail-model"
                 :class="CurrentKgDetail=='rag' ? 'kg-main-box-detail-model-chosen':''"
                 @click="switch_kg_detail_type('rag')">
              <el-text>召回测试</el-text>
            </div>
            <div class="kg-main-box-detail-model"
                 :class="CurrentKgDetail=='meta' ? 'kg-main-box-detail-model-chosen':''"
                 @click="switch_kg_detail_type('meta')">
              <el-text>设置</el-text>
            </div>
          </div>
          <div class="kg-main-box-detail-body">
            <kg_detail_file v-if="CurrentKgDetail == 'file'" />
            <div v-else-if="CurrentKgDetail == 'rag'">
              <el-empty description="即将上线，敬请期待！"></el-empty>
            </div>
            <kg_detail_meta v-else-if="CurrentKgDetail == 'meta'"  />
          </div>

        </div>
      </el-scrollbar>
    </el-main>

    <el-footer height="48px">
      <div class="kg-pagination" >

        <el-pagination
            :small="true"
            layout=" total, sizes, prev, pager, next"
            :total="CurrentKgDocTotal"
            :page-size="CurrentKgDocPageSize"
            :current-page="CurrentKgDocPageNum"
            :page-sizes="[20, 50, 100, 200, 1000]"
            @update:page-size="handleKgDocSizeChange"
            @update:current-page="handleKgDocCurrentChange"
        />
      </div>
    </el-footer>
  </el-container>

  <kg_doc_upload/>
  <Kg_web_upload/>
  <Kg_code_upload/>
  <Kg_faq_upload/>
</template>

<style scoped>

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

.kg-op-header{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  border-bottom: 1px solid #D0D5DD;
  width: calc(100% - 24px);

}
.kg-op-header-left{
  min-width: 280px;
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: flex-start;

}
.kg-op-header-middle{
  min-width: 480px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.kg-op-header-right{
  width: 150px;
}
</style>
