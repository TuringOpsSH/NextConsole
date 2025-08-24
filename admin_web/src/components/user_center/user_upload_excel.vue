<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue';
import {api, createUserByExcel, createUserByExcelTW} from '@/api/user_manage';
import {
  adminSearchUser,
  user_is_next_console_admin
} from '@/components/user_center/user_manage';
import {
  ElMessage,
  genFileId,
  type UploadInstance,
  type UploadProps,
  type UploadRawFile,
  type UploadUserFile
} from "element-plus";
import {ref, watch} from "vue";
import {getToken} from "@/utils/auth";
const props = defineProps({
  model: {
    type: Boolean,
    required: true,
    default: false
  }
});
const emits = defineEmits(['update:model']);
const localModel = ref(false);
const uploadRef = ref<UploadInstance>();
const userExcelFile = ref<UploadUserFile[]>();
const userExcelFileFlag = ref(false);
const userExcelFileName = ref('待上传');
const userExcelFileProgress = ref(0);
const userExcelFileResult = ref('');
const userExcelFileSize = ref('');
const userExcelFileStatus = ref('');
const dialogRef = ref(null);
const loading = ref(false);
const uploadDisabled = ref(true);
function getUploadHeaders() {
  return {
    Authorization: 'Bearer ' + getToken()
  };
}
function getFileInfo(file) {
  userExcelFileName.value = file.name;
  userExcelFileSize.value = (file.size / 1024).toFixed(2) + 'KB';
  userExcelFileFlag.value = true;
  uploadDisabled.value = false;
}
function handleExcelExceed(files: UploadProps['onExceed']) {
  uploadRef.value.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  uploadRef.value!.handleStart(file);
  userExcelFileProgress.value = 0;
  userExcelFileStatus.value = '';
  userExcelFileResult.value = '';
}
async function downloadUserTemplate() {
  if (user_is_next_console_admin.value) {
    await createUserByExcelTW({ file_name: '天问用户导入模板.xlsx' }, 'get');
    return;
  }
  await createUserByExcel({ file_name: '用户导入模板.xlsx' }, 'get');
}
function uploadUserExcelFile() {
  if (typeof userExcelFile.value === 'undefined') {
    ElMessage.warning('请上传文件！');
    return false;
  }
  uploadRef.value!.submit();
  // uploadRef.value.clearFiles()
}
async function updateUserResult(response, file, fileList) {
  // 在这里处理服务器返回的结果
  loading.value = false;
  if (response.error_status) {
    userExcelFileResult.value = response.error_message;
  } else {
    userExcelFileName.value = '';
    userExcelFileSize.value = '';
    userExcelFileFlag.value = false;
    userExcelFileProgress.value = (response.result.finished_cnt / response.result.total_cnt) * 100;
    if (userExcelFileProgress.value == 100) {
      userExcelFileStatus.value = 'success';
    }
    if (userExcelFileProgress.value < 60 && userExcelFileProgress.value >= 30) {
      userExcelFileStatus.value = 'warning';
    }
    if (userExcelFileProgress.value < 30) {
      userExcelFileStatus.value = 'exception';
    }
    userExcelFileResult.value =
        '总共导入' +
        response.result.total_cnt +
        '条数据，成功导入' +
        response.result.finished_cnt +
        '条数据，失败' +
        response.result.error_cnt +
        '条数据';
    for (let i = 0; i < response.result.trace.length; i++) {
      if (response.result.trace[i]?.error)
        userExcelFileResult.value +=
            '\n错误原因：' + response.result.trace[i]?.error + '，行号：' + response.result.trace[i]?.row_num;
    }
  }

  await adminSearchUser();
  uploadDisabled.value = true;
}
function beginLoading() {
  loading.value = true;
}
function handleDialogClosed() {
  loading.value = false;
  userExcelFileName.value = '待上传';
  userExcelFileSize.value = '';
  userExcelFileFlag.value = false;
  userExcelFileProgress.value = 0;
  userExcelFileStatus.value = '';
  userExcelFileResult.value = '';
  userExcelFile.value = [];
  uploadRef.value?.clearFiles();
  uploadDisabled.value = true;
  emits('update:model', false)
}
watch (
  () => props.model,
  (newVal) => {
    localModel.value = newVal;
  },
  { immediate: true }
);
</script>

<template>
  <el-dialog :ref="dialogRef" title="添加用户" v-model="localModel"
             @closed="handleDialogClosed">
    <div class="next-console-div" style="flex-direction: column" v-loading="loading" element-loading-text="努力导入中">
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
            v-model:file-list="userExcelFile"
            style="width: 100%"
            drag
            method="post"
            :auto-upload="false"
            :limit="1"
            :show-file-list="false"
            :on-change="getFileInfo"
            :headers="getUploadHeaders()"
            :action="user_is_next_console_admin ? api.twadmin_create_user_by_excel : api.admin_create_user_by_excel"
            with-credentials
            :on-exceed="handleExcelExceed"
            accept=".xlsx"
            :on-progress="beginLoading"
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
      <div class="next-console-div-upload" v-show="userExcelFile?.length > 0">
        <div>
          <el-image src="images/xlsx.svg" style="width: 40px; height: 40px" />
        </div>
        <div style="display: flex; flex-direction: column; width: 100%; gap: 4px; justify-content: flex-start">
          <div>
            <el-text>{{ userExcelFileName }}</el-text>
          </div>
          <div>
            <el-text>{{ userExcelFileSize }}</el-text>
          </div>
          <div>
            <el-progress
                :percentage="userExcelFileProgress"
                :status="userExcelFileStatus"
                striped
                striped-flow
                :duration="10"
            />
          </div>
        </div>
        <div v-if="userExcelFileFlag">
          <el-image src="images/check_blue.svg" style="width: 16px; height: 16px" />
        </div>
      </div>
      <div class="next-console-div-upload-result">
        <div class="user_upload_result_title">
          <el-text> 上传结果 </el-text>
        </div>

        <div>
          <el-input v-model="userExcelFileResult" type="textarea" resize="none" readonly :autosize="{ minRows: 5 }" />
        </div>
      </div>
      <div class="user-add-form-header">
        <el-button color="#1570EF" style="border: 1px solid #1570ef; width: 100%" @click="uploadUserExcelFile" :disabled="uploadDisabled">
          <el-text class="user_del_font" style="color: white"> 批量添加 </el-text>
        </el-button>
      </div>
    </div>
  </el-dialog>

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
