<script setup lang="ts">
import {omit_text} from "@/utils/base"
import {get_upload_headers, upload_loading} from "@/components/kg/kg_process";
import {
  dialog_v_upload_kg_file,
  turn_off_upload_dialog,
  upload_dialog_commit,
  upload_dialog_remove
} from "@/components/kg/doc_kg/doc_kg_process"
import {api} from "@/api/kg_center";
import {
  kg_doc_before_upload,
  kg_doc_data,
  kg_doc_list,
  kg_doc_on_remove,
  kg_doc_on_success,
  kg_doc_ref
} from "@/components/kg/doc_process";
import {UploadFilled} from "@element-plus/icons-vue";
</script>

<template>
  <el-dialog v-model="dialog_v_upload_kg_file" title="上传离线文档"
             :close-on-click-modal="false"
             :fullscreen="false"
             @close="turn_off_upload_dialog">

    <div style="display: flex;flex-direction: column; justify-content: flex-start">
      上传文档
      <el-upload
          v-loading="upload_loading"
          element-loading-text="上传中，请稍候。。。"
          ref="kg_doc_ref"
          :action="api.doc_upload"
          :multiple="true"
          :show-file-list="true"
          :auto-upload="false"
          :drag="true"
          name="kg_db_doc"
          :before-upload="kg_doc_before_upload"
          :headers="get_upload_headers()"
          :data="kg_doc_data"
          :on-remove="kg_doc_on_remove"
          :on-success="kg_doc_on_success"
          v-model:file-list="kg_doc_list"
          list-type='text'
          accept=".html, .htm, .docx, .doc, .md, .txt, .pdf, .rtf, .xml, .xls, .xlsx, .ppt, .pptx, .one, .odf, .odt, .ods, .odp, .eml, .msg, .epub, .mobi, .tex"

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
            HTML、DOCX、DOC、Markdown、PDF、TXT、Excel、PPT
          </el-text>
          等常见文档格式
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
                <el-image src="images/excel.svg" class="attachment-file-icon"
                          v-else-if="file.name.toLowerCase().endsWith('.xlsx')"/>
                <el-image src="images/excel.svg" class="attachment-file-icon"
                          v-else-if="file.name.toLowerCase().endsWith('.xls')"/>
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
              <el-button style="border:0;padding: 0;" @click="upload_dialog_remove(file)">
                <el-image src="images/file_minus_blue.svg" style="width: 15px;height: 15px"/>
              </el-button>
            </div>
          </div>
        </template>

      </el-upload>
    </div>
    <template #footer>
      <div class="kg-dialog-footer">
        <el-button class="kg-dialog-footer-button" style="background-color: #FFFFFF;
      border: 1px solid #D0D5DD"
                   @click="turn_off_upload_dialog">
          <el-text class="kg-button-text" style="color: #344054">
            取消
          </el-text>
        </el-button>
        <el-button class="kg-dialog-footer-button" style="background-color: #1570ef;
      border: 1px solid #D0D5DD"
                   @click="upload_dialog_commit">
          <el-text class="kg-button-text" style="color: #FFFFFF">
            上传
          </el-text>
        </el-button>


      </div>
    </template>

  </el-dialog>
</template>

<style scoped>

</style>
