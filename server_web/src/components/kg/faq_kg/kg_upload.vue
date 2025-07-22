<script setup lang="ts">

import {
  kg_batch_upload_logs,

  kg_exceed_template,
  upload_script_template_remove,
} from "@/components/kg/code_kg/code_kg_process";
import {onMounted} from "vue";
import {
  current_faq_data_form,
  dialog_v_upload_faq,
  download_faq_template,
  kg_batch_faq_ref,
  kg_faq_list,
  turn_off_upload_faq_dialog,
  upload_faq_dialog_batch_commit,
  upload_faq_dialog_batch_on_success
} from "@/components/kg/faq_kg/faq_kg_process";
import {get_upload_headers, show_kg_batch_upload_result, upload_loading, kg_batch_upload_progress,} from "@/components/kg/kg_process";
import {api} from "@/api/kg_center";
import {kg_doc_before_upload, kg_doc_data, kg_doc_on_remove} from "@/components/kg/doc_process";
import {omit_text} from "@/utils/base";
import {UploadFilled} from "@element-plus/icons-vue";

onMounted(
    async () => {

    }
)


</script>

<template>
<el-dialog v-model="dialog_v_upload_faq" title="FAQ" top="6vh"
             width="80%" :close-on-click-modal="true">
  <div class="script-kg-button" @click="download_faq_template()">
      <div class="std-middle-box">
        <el-image src="images/file_download_02.svg" style="width: 20px;height: 20px"/>
      </div>
      <div class="std-middle-box">
        <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054;">
          下载模板文件
        </el-text>
      </div>
    </div>
  <el-form :model="current_faq_data_form" label-position="top" style="width: 100%"

  >
    <el-form-item required label="问题统一前缀字段"
                  error="必须指定faq对应领域、产品、版本等特征，以提升faq命中"
                  prop="pre_question"

    >
      <el-input v-model="current_faq_data_form.pre_question" placeholder="问题统一前缀字段"
                style="width: 100%"/>
    </el-form-item>

  </el-form>

  <div id="script-kg-upload-box">
    <el-upload
        v-loading="upload_loading"
        element-loading-text="上传中，请稍候。。。"
        ref="kg_batch_faq_ref"
        :limit="1"
        :action="api.kg_batch_upload"
        :multiple="false"
        :show-file-list="true"
        :auto-upload="false"
        :drag="true"
        name="kg_db_doc"
        :before-upload="kg_doc_before_upload"
        :headers="get_upload_headers()"
        :data="kg_doc_data"
        :on-remove="kg_doc_on_remove"
        :on-success="upload_faq_dialog_batch_on_success"
        :on-exceed="kg_exceed_template"
        v-model:file-list="kg_faq_list"
        list-type='text'
        accept=".xlsx"
        style="width: 100%"
    >
      <div>
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      </div>

      <el-button  text>
        <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #175CD3;">
          点击或拖拽上传文档
        </el-text>

      </el-button>
      <div slot="tip" class="el-upload__tip">
        支持
        <el-text style="color: #1570ef">
          XlSX
        </el-text>
        格式
      </div>

      <template #file="{ file }">
        <div class="attachment-file-item-box" >
          <div class="attachment-file-item-left">
            <div class="attachment-file-icon-box">
              <el-image src="images/file_format_html_blue.svg" class="attachment-file-icon"
                        v-if="file.name.toLowerCase().endsWith('.html')"/>
              <el-image src="images/file_format_docx_blue.svg" class="attachment-file-icon"
                        v-else-if="file.name.toLowerCase().endsWith('.docx')"/>
              <el-image src="images/file_format_docx_blue.svg" class="attachment-file-icon"
                        v-else-if="file.name.toLowerCase().endsWith('.doc')"/>
              <el-image src="images/file_format_md.svg" class="attachment-file-icon"
                        v-else-if="file.name.toLowerCase().endsWith('.md')"/>
              <el-image src="images/file_format_txt.svg" class="attachment-file-icon"
                        v-else-if="file.name.toLowerCase().endsWith('.txt')"/>
              <el-image src="images/file_format_pdf.svg" class="attachment-file-icon"
                        v-else-if="file.name.toLowerCase().endsWith('.pdf')"/>
              <el-image src="images/file_format_csv.svg" class="attachment-file-icon"
                        v-else-if="file.name.toLowerCase().endsWith('.csv')"/>
              <el-image src="images/excel.svg" class="attachment-file-icon"
                        v-else-if="file.name.toLowerCase().endsWith('.xlsx') ||
                                file.name.toLowerCase().endsWith('.xls')"/>
              <el-image src="images/file_format_other.svg" class="attachment-file-icon"
                        v-else/>
            </div>
            <div class="attachment-file-meta-box">
              <div>
                <el-tooltip :content="file.name" v-if="file.name.length > 60" effect="light">
                  <el-text>{{omit_text(file.name,60)}}</el-text>
                  <template #content>
                    <div v-text="file.name" style="max-width: 400px;display: flex;flex-wrap: wrap">

                    </div>
                  </template>
                </el-tooltip>
                <el-text v-else>{{file.name}}</el-text>

              </div>
              <div>
                <el-text>
                  {{(file.size/ 1024/ 1024).toFixed(3)}} MB
                </el-text> - <el-text>{{file.status}}</el-text>
              </div>

            </div>
          </div>
          <div class="attachment-file-button-box">
            <el-button style="border:0;padding: 0;" @click="upload_script_template_remove(file)">
              <el-image src="images/file_minus_blue.svg" style="width: 15px;height: 15px"/>
            </el-button>
          </div>
        </div>
      </template>

    </el-upload>
  </div>
  <div id="script-kg-upload-result" v-if="show_kg_batch_upload_result">
    <el-form label-position="top" style="width: 100%">
      <el-form-item label="解析进度">
        <el-progress :percentage="kg_batch_upload_progress" :text-inside="true"
                     :stroke-width="20" style="width: 100%" />
      </el-form-item>
      <el-form-item label="上传日志">
        <el-input resize="none" v-model="kg_batch_upload_logs" readonly type="textarea" :rows="5"
                  style="width: 100%"
        />
      </el-form-item>
    </el-form>
  </div>
    <template #footer>
      <div class="kg-dialog-footer">
        <el-button class="kg-dialog-footer-button" style="background-color: #FFFFFF; border: 1px solid #D0D5DD" @click="turn_off_upload_faq_dialog()">
          <el-text class="kg-button-text" style="color: #344054">
            取消
          </el-text>
        </el-button>
        <el-button class="kg-dialog-footer-button" style="background-color: #1570ef; border: 1px solid #D0D5DD" @click="upload_faq_dialog_batch_commit()">
          <el-text class="kg-button-text" style="color: #FFFFFF">
            上传
          </el-text>
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
#code-bath-upload-box{
  display:flex;
  flex-direction: column;align-items: center;
  justify-content: center;
  gap: 6px;width: 100%
}
#code-schema-switch-box{
  display:flex; flex-direction: row;align-items: center;justify-content: center;gap: 6px
}
#code-schema-label{
  font-size: 14px;font-weight: 600;line-height: 20px;color: #475467;
}
.code-schema-switch-icon{
  width:12px; height: 12px; cursor: pointer
}
#code-schema-json-editor{
  width: 100%; height: 300px; display: flex;flex-direction: row;align-items: flex-start;justify-content: flex-start
}
.script-kg-button{
  width: calc(100% - 30px);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid #D0D5DD;
  box-shadow: 0 1px 2px 0 #1018280D;
}
.script-kg-button:hover{
  background-color: #EFF8FF;
}
.std-middle-box{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
#script-kg-upload-box{
  display: flex;flex-direction: column; justify-content: flex-start;width: 100%
}
#update-confirm-box{
  display: flex;flex-direction: column;justify-content: center;width: 100%;
  gap: 8px;
}
.update-schema-button{
  width: calc(100% - 28px);
  padding: 8px 14px;
  border-radius: 8px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
#script-kg-upload-result{
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>
