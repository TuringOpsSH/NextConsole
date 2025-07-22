<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue';
import { api } from '@/api/user_manage';
import {
  downloadUserTemplate,
  get_upload_headers,
  getFileInfo,
  handleExcelExceed,
  showAddUserDialogFlag,
  updateUserResult,
  uploadRef,
  uploadUserExcelFile,
  user_excel_file,
  user_excel_file_flag,
  user_excel_file_name,
  user_excel_file_progress,
  user_excel_file_result,
  user_excel_file_size,
  user_excel_file_status,
  user_is_next_console_admin
} from '@/components/user_center/user_manage';
</script>

<template>
  <div class="next-console-div" style="flex-direction: column">
    <div class="next-console-div-download" style="padding: 8px 0; width: 100%" @click="downloadUserTemplate">
      <div>
        <el-image src="images/download_01_grey.svg" style="width: 20px; height: 20px" />
      </div>
      <div style="margin-left: 8px">
        <el-text class="next-console-font-bold" style="color: #344054">下载用户模板文件</el-text>
      </div>
    </div>

    <div class="next-console-div-download" style="padding: 0; width: 100%">
      <el-upload
        ref="uploadRef"
        v-model:file-list="user_excel_file"
        style="width: 100%"
        drag
        method="post"
        :auto-upload="false"
        :limit="1"
        :show-file-list="false"
        :on-change="getFileInfo"
        :headers="get_upload_headers()"
        :action="user_is_next_console_admin ? api.twadmin_create_user_by_excel : api.admin_create_user_by_excel"
        with-credentials
        :on-exceed="handleExcelExceed"
        accept=".xlsx"
        :on-success="updateUserResult"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          <em>点击上传</em>或者<em>拖拽文件到此处上传</em>
          <br />
          <el-text>支持xlsx文件</el-text>
        </div>
      </el-upload>
    </div>
    <div class="next-console-div-upload">
      <div>
        <el-image src="images/csv_green.svg" style="width: 40px; height: 40px" />
      </div>
      <div style="display: flex; flex-direction: column; width: 100%; gap: 4px; justify-content: flex-start">
        <div>
          <el-text>{{ user_excel_file_name }}</el-text>
        </div>
        <div>
          <el-text>{{ user_excel_file_size }}</el-text>
        </div>
        <div>
          <el-progress
            :percentage="user_excel_file_progress"
            :status="user_excel_file_status"
            striped
            striped-flow
            :duration="10"
          />
        </div>
      </div>
      <div v-if="user_excel_file_flag">
        <el-image src="images/check_blue.svg" style="width: 16px; height: 16px" />
      </div>
    </div>
    <div class="next-console-div-upload-result">
      <div class="user_upload_result_title">
        <el-text> 上传结果 </el-text>
      </div>

      <div>
        <el-input v-model="user_excel_file_result" type="textarea" resize="none" disabled :autosize="{ minRows: 5 }" />
      </div>
    </div>
    <div class="user-add-form-header">
      <el-button color="white" style="width: 100%; border: 1px solid #d0d5dd" @click="showAddUserDialogFlag = false">
        <el-text class="user_del_font" style="color: #344054"> 取 消 </el-text>
      </el-button>
      <el-button color="#1570EF" style="border: 1px solid #1570ef; width: 100%" @click="uploadUserExcelFile">
        <el-text class="user_del_font" style="color: white"> 确 认 </el-text>
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.next-console-div-download {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 12px 16px;
  border: 1px solid #d0d5dd;
  box-shadow: 0 1px 2px 0 #1018280d;
  border-radius: 8px;
  width: 90%;
}
.next-console-div-download:hover {
  background-color: whitesmoke;
  opacity: 0.5;
  cursor: pointer;
}
.next-console-div-upload {
  display: flex;
  flex-direction: row;
  border-radius: 12px;
  border: 1px solid #eaecf0;
  padding: 16px;
  width: calc(100% - 32px);
  justify-content: space-between;
  gap: 12px;
}
.user_upload_result_title {
  margin-top: 15px;
}
.next-console-div-upload-result {
  display: flex;
  flex-direction: column;
  gap: 6px;
  justify-content: flex-start;
  width: 100%;
}
.user-add-form-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 24px;
  padding: 16px;
  width: calc(100% - 32px);
}
.user_del_font {
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  text-align: left;
}
</style>
