<script setup lang="ts">

import {
  check_kg_ref_progress,
  check_kg_ref_progress_interval_id,
  CurrentKg,
  upload_loading,
} from "@/components/kg/kg_process";
import {
  turn_on_upload_website_dialog,
} from "@/components/kg/web_kg/web_kg_process";
import {
  turn_on_upload_dialog,
} from "@/components/kg/doc_kg/doc_kg_process";
import {InfoFilled, Search, WarningFilled} from "@element-plus/icons-vue";
import {
  batch_switch_kg_doc_status,
  current_kg_doc_list,
  CurrentKgDocKeyWord,
  CurrentKgDocRefStatus,
  download_kg_doc,
  handleKgDocSelectionChange,
  kg_doc_batch_rebuild,
  kg_doc_on_remove,
  kg_doc_rebuild,
  search_kg_docs,
  switch_kg_doc_status
} from "@/components/kg/doc_process";
import {omit_text} from '@/utils/base'
import {check_kg_permission, scrollbarHeight} from "@/components/kg/kg_center_base";
import {onBeforeUnmount, onMounted} from "vue";
import {turn_on_upload_script_dialog} from "@/components/kg/code_kg/code_kg_process";
import {turn_on_upload_faq_dialog} from "@/components/kg/faq_kg/faq_kg_process";


onMounted(async () => {

  // 轮询知识库构建进度
  //@ts-ignore
  check_kg_ref_progress_interval_id.value = setInterval(check_kg_ref_progress, 6666)

})
onBeforeUnmount(() => {
      clearInterval(check_kg_ref_progress_interval_id.value)

    }
)
</script>

<template>
  <div class="kg-main-box-detail-body">
    <el-container>
      <el-header style="display: flex;flex-direction: row;justify-content: space-between ; align-items: center;gap: 16px; padding: 16px 24px !important;border-bottom: 1px solid #EAECF0;">
        <div>
          <el-text class="next-console-text-bold">
            文档素材
          </el-text>
        </div>
        <div style="display: flex;align-items: center;justify-content: center;gap: 6px;flex-direction: row">
          <div>
            <el-input :prefix-icon="Search" placeholder="搜索文档" v-model="CurrentKgDocKeyWord"
                      @change="search_kg_docs()" clearable
            />

          </div>
          <div>
            <el-select v-model="CurrentKgDocRefStatus" clearable placeholder="构建状态"
                       style="width: 160px" multiple collapse-tags
                      @change="search_kg_docs()"
            >
              <el-option value="All" label="所有构建状态" />
              <el-option value="Success" label="成功" />
              <el-option value="Failure" label="失败" />
              <el-option value="Error" label="异常" />
              <el-option value="Processing" label="构建中" />
              <el-option value="Pending" label="排队中" />
              <el-option value="Downloading" label="下载中" />
              <el-option value="DownloadFailed" label="下载失败"/>
              <el-option value="Stop" label="未启动" />
            </el-select>

          </div>
          <div>
            <el-popover trigger="click" v-if="check_kg_permission(CurrentKg)">
              <template #reference>
                <el-button style="display: flex;flex-direction: row;align-items: center;gap: 4px">
                  <div>
                    <el-text class="next-console-text-bold">批量操作</el-text>
                  </div>
                  <div style="margin-left: 4px;">
                    <el-image src="images/dots_horizontal_grey.svg" style="width: 16px;height: 16px"/>
                  </div>

                </el-button>
              </template>
              <div style="display: flex;flex-direction: column; align-items: center;justify-content: center;gap: 6px">
                <el-button class="kg-file-batch-button" @click="batch_switch_kg_doc_status('正常')">
                  <div>
                    <el-image src="images/eye_grey.svg" class="kg-file-batch-icon"/>
                  </div>
                  <div>
                    <el-text class="next-console-text-bold">启用</el-text>
                  </div>
                </el-button>
                <el-button class="kg-file-batch-button" @click="batch_switch_kg_doc_status('停用')">
                  <div >
                    <el-image src="images/eye_off_grey.svg" class="kg-file-batch-icon"/>
                  </div>
                  <div>
                    <el-text class="next-console-text-bold">停用</el-text>
                  </div>
                </el-button>
                <el-button class="kg-file-batch-button" @click="kg_doc_batch_rebuild" >
                  <div>
                    <el-image src="images/retry_cw_01.svg" class="kg-file-batch-icon"/>
                  </div>
                  <div>
                    <el-text class="next-console-text-bold">重新构建</el-text>
                  </div>
                </el-button>
                <el-popconfirm title="确定要批量删除文件么?" confirm-button-text="确定"
                               :icon="WarningFilled"
                               icon-color="red"
                               cancel-button-text="取消"
                               @confirm="batch_switch_kg_doc_status('删除')">
                  <template #reference>
                    <el-button class="kg-file-batch-button">
                      <div>
                        <el-image src="images/trash_01_grey.svg" class="kg-file-batch-icon"/>
                      </div>
                      <div>
                        <el-text class="next-console-text-bold">删除</el-text>
                      </div>
                    </el-button>
                  </template>
                </el-popconfirm>

              </div>
            </el-popover>
          </div>
          <div>
            <el-button @click="turn_on_upload_dialog" style="background-color: #1570ef"
                       v-if="check_kg_permission(CurrentKg) && CurrentKg.kg_type=='file'">
              <el-text class="next-console-text-bold" style="color: #FFFFFF">上传文档</el-text>
            </el-button>
            <el-button @click="turn_on_upload_website_dialog" style="background-color: #1570ef"
                       v-else-if="check_kg_permission(CurrentKg) && CurrentKg.kg_type=='website'">
              <el-text class="next-console-text-bold" style="color: #FFFFFF">选择站点</el-text>
            </el-button>
            <el-button @click="turn_on_upload_script_dialog" style="background-color: #1570ef"
                       v-else-if="check_kg_permission(CurrentKg) && CurrentKg.kg_type=='script'">
              <el-text class="next-console-text-bold" style="color: #FFFFFF">上传脚本</el-text>
            </el-button>
            <el-button @click="turn_on_upload_faq_dialog" style="background-color: #1570ef"
                       v-else-if="check_kg_permission(CurrentKg) && CurrentKg.kg_type=='faq'">
              <el-text class="next-console-text-bold" style="color: #FFFFFF">上传FAQ</el-text>
            </el-button>
          </div>
        </div>
      </el-header>
      <el-main style="width: 100%;height: 100%;display: flex;align-items: center;justify-content: center">
        <div style="width: 100%;height: 100%;display: flex;align-items: center;justify-content: center">
          <el-table :data="current_kg_doc_list"   :max-height="scrollbarHeight - 80"
                    :height = "scrollbarHeight - 80"
                    :stripe="true"
                    @selection-change="handleKgDocSelectionChange"
                    v-loading="upload_loading"
                    element-loading-text="文档新增中。。。"
                    style="width: 100%"
                    :highlight-current-row="true"
          >
            <el-table-column type="selection" width="30"/>
            <el-table-column prop="doc_id" label="素材ID" width="360"/>

            <el-table-column prop="doc_name"  :show-overflow-tooltip="true"
                             :label="CurrentKg.kg_type === 'faq' ? '问题' : '文档名称'"
            />
            <el-table-column prop="doc_desc"  :show-overflow-tooltip="true"
                             :label="CurrentKg.kg_type === 'faq' ? '问题标签' : '文档描述'"
            />
            <el-table-column prop="doc_size" label="文档大小" sortable width="120"
                             v-if="CurrentKg.kg_type==='file'">
              <template #default="{row}">
                <el-text>{{row.doc_size}} MB</el-text>
              </template>
            </el-table-column>
            <el-table-column prop="doc_format" label="文档格式" width="120"  v-if="CurrentKg.kg_type==='file'"/>
            <el-table-column prop="doc_url" label="素材源"  v-if="CurrentKg.kg_type==='website'"
                             :show-overflow-tooltip="true"/>
            <el-table-column prop="create_time" label="添加时间" sortable width="180" />
            <el-table-column prop="doc_ref_id" label="索引ID" sortable width="180" />
            <el-table-column prop="doc_ref_status" sortable label="构建状态" width="120" >
              <template #default="{row}">
                <el-tag v-if="row.doc_ref_status === 'Success'" type="success" round>
                  成功
                </el-tag>
                <el-tag v-else-if="row.doc_ref_status === 'Processing'"
                        round >
                  构建中
                </el-tag>
                <el-tag v-else-if="row.doc_ref_status === 'Pending'"
                        round >
                  排队中
                </el-tag>
                <el-tag v-else-if=" row.doc_ref_status === 'Failure'"
                         type="warning" round>
                  失败
                </el-tag>
                <el-tag v-else-if="row.doc_ref_status === 'Error'"
                        type="danger" round>
                  异常
                </el-tag>
                <el-tag v-else-if="row.doc_ref_status === 'Downloading'"
                        round>
                  下载中
                </el-tag>
                <el-tag v-else-if="row.doc_ref_status === 'DownloadFailed'"
                        round>
                  下载失败
                </el-tag>
                <el-tag v-else type="info" round>
                  未启动
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column fixed="right" label="操作" width="120" >
              <template #default="{row}">
                <div style="display: flex;align-items: center;justify-content: flex-start;gap: 6px">
                  <el-switch v-model="row.doc_status"
                             active-value="正常"
                             inactive-value="停用"
                             size="small"
                             v-if="check_kg_permission(CurrentKg)"
                             @change = "switch_kg_doc_status(row)"
                  />
                  <el-popconfirm title="确定要删除该文件么?" confirm-button-text="确定"
                                 v-if="check_kg_permission(CurrentKg)"
                                 cancel-button-text="取消" @confirm="kg_doc_on_remove(row)">
                    <template #reference>

                      <el-image src="images/trash_01_grey.svg" style="cursor: pointer;background-color: transparent"
                                class="next-console-image"/>

                    </template>
                  </el-popconfirm>
                  <el-popconfirm title="确定要重新索引该文件么?" confirm-button-text="确定"
                                 v-if="check_kg_permission(CurrentKg) && CurrentKg.kg_type!='script'"
                                 cancel-button-text="取消" @confirm="kg_doc_rebuild(row)">
                    <template #reference>

                      <el-image src="images/refresh_grey.svg" style="cursor: pointer;background-color: transparent"
                                class="next-console-image"/>

                    </template>
                  </el-popconfirm>
                  <el-popconfirm title="请严格遵守公司的数据安全制度，该下载文件仅供个人查阅，禁止外传！"
                                 :icon="InfoFilled"
                                 confirm-button-text="我已知晓，确定下载"
                                 width="300px"
                                  v-if="check_kg_permission(CurrentKg)  "
                                 cancel-button-text="取消" @confirm="download_kg_doc(row)">
                    <template #reference>

                      <el-image src="images/download.svg" style="cursor: pointer;background-color: transparent"
                                class="next-console-image"/>

                    </template>
                  </el-popconfirm>

                </div>

              </template>
            </el-table-column>
          </el-table>
        </div>


      </el-main>
    </el-container>

  </div>
</template>

<style scoped>
.kg-file-batch-button{
  width: 100%;
  margin-left: 0 !important;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  border: 0;

}
.kg-file-batch-icon{
  width: 20px;
  height: 20px;
  margin-right: 12px;
}

</style>
