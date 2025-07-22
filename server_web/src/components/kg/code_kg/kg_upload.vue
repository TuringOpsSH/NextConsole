<script setup lang="ts">

import {
  CurrentKg,
  get_upload_headers,
  kg_batch_upload_progress,
  show_kg_batch_upload_result,
  upload_loading,
} from "@/components/kg/kg_process";
import {
  accept_languages,
  dialog_v_upload_kg_script,
  download_script_kg,
  download_script_template,
  json_editor_vue_ref,
  kg_add_scripts_model,
  kg_batch_script_ref,
  kg_batch_upload_logs,
  kg_exceed_single_script,
  kg_exceed_template,
  kg_script_list,
  kg_scripts_ref,
  pre_check_script_schema,
  script_schema_show,
  switch_script_schema_show,
  turn_off_upload_script_dialog,
  update_button_ref,
  update_script_schema,
  update_script_schema_commit,
  update_script_schema_dialog,
  upload_script_dialog_batch_on_success,
  upload_script_dialog_commit,
  upload_script_dialog_remove,
  upload_script_loading,
  upload_script_template_remove,
} from "@/components/kg/code_kg/code_kg_process";
import {kg_doc_before_upload, kg_doc_data, kg_doc_on_remove} from "@/components/kg/doc_process";
import {api} from "@/api/kg_center";
import {UploadFilled} from "@element-plus/icons-vue";
import {omit_text} from "@/utils/base"
// @ts-ignore
import JsonEditorVue from 'json-editor-vue3'
import {onMounted} from "vue";
import Kg_upload_json_schema_form from "@/components/kg/code_kg/kg_upload_json_schema_form.vue";
import {
  kg_script_before_upload,
  kg_script_data,
  kg_single_script_on_success
} from "@/components/kg/code_kg/code_script_process";

onMounted(
    async () => {

    }
)


</script>

<template>
  <el-dialog v-model="dialog_v_upload_kg_script" title="上传代码脚本" top="6vh"
             width="80%" :close-on-click-modal="true">
    <el-tabs v-model="kg_add_scripts_model">
      <el-tab-pane label="批量上传" name="csv" >
        <div id="code-bath-upload-box">
          <el-divider>
            <div id="code-schema-switch-box">
              <el-text id="code-schema-label">
                脚本管理字段schema
              </el-text>
              <el-image src="images/chevron_down_grey.svg"
                        class="code-schema-switch-icon"
                        v-if = "!script_schema_show"
                        @click="switch_script_schema_show()"/>
              <el-image src="images/chevron_up_grey.svg"
                        class="code-schema-switch-icon"
                        v-else
                        @click="switch_script_schema_show()"/>
            </div>

          </el-divider>
          <div id="code-schema-json-editor" v-if="script_schema_show" >
            <json-editor-vue   v-model="CurrentKg.kg_json_schema"
                               ref="json_editor_vue_ref"
                               @validationError="pre_check_script_schema"
                               style="width: 100%; height: 280px"/>
          </div>
          <el-form :model="CurrentKg.kg_json_schema.meta" label-position="top" style="width: 100%"
                   v-if="CurrentKg.kg_json_schema" require-asterisk-position="right"
          >
            <el-form-item required label="指定语义检索字段" error="必须勾选语义检索字段，用于后续查询" prop="embedding">
              <el-checkbox-group v-model="CurrentKg.kg_json_schema.meta.embedding">
                <el-checkbox v-for="(property, key) in CurrentKg.kg_json_schema.properties" :label="key"
                              size="small"
                >
                  {{property.description}}
                </el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item required label="指定代码字段" error="必须勾选代码字段，用于构建索引" prop="code">
              <el-radio-group size="small" v-model="CurrentKg.kg_json_schema.meta.code">
                <el-radio v-for="(property, key) in CurrentKg.kg_json_schema.properties" :label="key"

                >
                  {{property.description}}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
          <div class="script-kg-button" @click="update_script_schema()" ref="update_button_ref">
            <div class="std-middle-box">
              <el-image src="images/save.svg" style="width: 20px;height: 20px"/>
            </div>
            <div class="std-middle-box">
              <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054;">
                保存schema更新
              </el-text>
            </div>
          </div>
          <el-dialog v-model="update_script_schema_dialog" title="更新schema">
             <div id="update-confirm-box">
               <div>
                 <el-result
                     icon="warning"
                     title="注意！更新schema会删除所有已有脚本！"
                     sub-title="建议下载已有脚本库进行备份，并按照最新schema重新上传！"
                 />
               </div>
               <div>
                 <div class="update-schema-button" style="background-color: red" @click="download_script_kg">
                   <div class="std-middle-box">
                     <el-image src="images/download_02_white.svg" style="width: 15px; height: 15px"/>
                   </div>
                   <div class="std-middle-box">
                     <el-text style="color: white;font-weight: 600;font-size: 14px;line-height: 20px">
                       下载备份所有脚本
                     </el-text>
                   </div>
                 </div>
               </div>
             </div>
              <template #footer>
                <div class="std-middle-box">
                  <div class="update-schema-button" style="background-color: white;border: 1px solid #D0D5DD;gap: 6px"
                       @click="update_script_schema_dialog=false">
                    <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054">
                      取消
                    </el-text>
                  </div>
                  <div class="update-schema-button" style="background-color: #1570ef"
                       @click="update_script_schema_commit()">
                    <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: white">
                      确认
                    </el-text>
                  </div>
                </div>
              </template>
          </el-dialog>
          <div class="script-kg-button" @click="download_script_template()">
            <div class="std-middle-box">
              <el-image src="images/file_download_02.svg" style="width: 20px;height: 20px"/>
            </div>
            <div class="std-middle-box">
              <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #344054;">
                下载模板文件
              </el-text>
            </div>
          </div>
          <div id="script-kg-upload-box">
            <el-upload
                v-loading="upload_loading"
                element-loading-text="上传中，请稍候。。。"
                ref="kg_batch_script_ref"
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
                :on-success="upload_script_dialog_batch_on_success"
                :on-exceed="kg_exceed_template"
                v-model:file-list="kg_script_list"
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
        </div>
      </el-tab-pane>
      <el-tab-pane label="单文件上传" name="file">

        <el-upload
            v-loading="upload_script_loading"
            element-loading-text="上传中，请稍候。。。"
            ref="kg_scripts_ref"
            :action="api.doc_upload"
            :multiple="false"
            :show-file-list="true"
            :auto-upload="false"
            :drag="true"
            :limit="1"
            name="kg_db_doc"
            :before-upload="kg_script_before_upload"
            :headers="get_upload_headers()"
            :data="kg_script_data"
            :on-remove="kg_doc_on_remove"
            :on-success="kg_single_script_on_success"
            :on-exceed="kg_exceed_single_script"
            v-model:file-list="kg_script_list"
            list-type='text'
            :accept='accept_languages'

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
              常见代码文件格式
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
                  <el-image src="images/file_format_xlsx.svg" class="attachment-file-icon"
                            v-else-if="file.name.toLowerCase().endsWith('.xlsx')"/>
                  <el-image src="images/file_format_xls.svg" class="attachment-file-icon"
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
                <el-button style="border:0;padding: 0;" @click="upload_script_dialog_remove(file)">
                  <el-image src="images/file_minus_blue.svg" style="width: 15px;height: 15px"/>
                </el-button>
              </div>
            </div>
          </template>

        </el-upload>
        <kg_upload_json_schema_form/>
      </el-tab-pane>
    </el-tabs>
    <template #footer>
      <div class="kg-dialog-footer">
        <el-button class="kg-dialog-footer-button" style="background-color: #FFFFFF; border: 1px solid #D0D5DD" @click="turn_off_upload_script_dialog()">
          <el-text class="kg-button-text" style="color: #344054">
            取消
          </el-text>
        </el-button>
        <el-button class="kg-dialog-footer-button" style="background-color: #1570ef; border: 1px solid #D0D5DD" @click="upload_script_dialog_commit()">
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
