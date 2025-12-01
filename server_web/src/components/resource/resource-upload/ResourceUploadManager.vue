<script setup lang="ts">
import { ElNotification, UploadRequestOptions } from 'element-plus';
import { ref } from 'vue';
import { update_upload_task } from '@/api/resource-api';
import {
  close_upload_manager,
  finish_time_size_map,
  show_close_confirm_flag,
  show_upload_manage_box,
  upload_file_content,
  upload_file_list,
  upload_file_task_list,
  upload_manager_status, upload_size
} from '@/components/resource/resource-upload/resource-upload';
import { IResourceUploadItem } from '@/types/resource-type';
const showUploadFileDetail = ref(true);
async function continueAllUploadTask() {
  // 继续所有上传任务
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status === 'pause') {
      // 更新后端上传任务状态
      let params = {
        task_id: upload_file_task_list.value[i].id,
        task_status: 'uploading'
      };
      await update_upload_task(params);

      upload_file_task_list.value[i].task_status = 'uploading';
      upload_file_content(<UploadRequestOptions>{
        file: upload_file_task_list.value[i].raw_file,
        data: {},
        headers: {}
      });
    }
  }
  upload_manager_status.value = 'uploading';
}
function cleanUploadManager() {
  upload_file_list.value = [];
  // 更新后端上传任务状态
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (
      upload_file_task_list.value[i].task_status !== 'success' &&
      upload_file_task_list.value[i].task_status !== 'error' &&
      upload_file_task_list.value[i].task_status !== 'abort' &&
      upload_file_task_list.value[i].id
    ) {
      let params = {
        task_id: upload_file_task_list.value[i].id,
        task_status: 'abort'
      };
      update_upload_task(params);
    }
  }

  upload_file_task_list.value = [];
  upload_manager_status.value = 'pending';
  show_upload_manage_box.value = false;
  show_close_confirm_flag.value = false;
}
async function removeUploadTask(item: IResourceUploadItem) {
  // 删除上传任务
  let index = upload_file_task_list.value.findIndex(value => value.id === item.id);
  upload_file_task_list.value.splice(index, 1);
  // 更新后端上传任务状态
  let params = {
    task_id: item.id,
    task_status: 'abort'
  };
  update_upload_task(params);
}
async function retryUploadTask(item: IResourceUploadItem) {
  // 重试上传任务
  if (item.task_status === 'error') {
    // 更新后端上传任务状态
    let params = {
      task_id: item.id,
      task_status: 'pending'
    };
    await update_upload_task(params);
    item.task_status = 'pending';
    item.content_finish_idx = -1;
    await upload_file_content(<UploadRequestOptions>{
      file: item.raw_file,
      data: {},
      headers: {}
    });
    // 更新管理器状态
    upload_manager_status.value = 'uploading';
  } else {
    ElNotification.error({
      title: '系统通知',
      message: '任务状态不是错误状态，无法重试',
      duration: 5000
    });
  }
}
async function pauseUploadTask(item: IResourceUploadItem) {
  // 暂停上传任务,修改任务状态为pause
  item.task_status = 'pause';
  item.content_finish_idx -= 1;
  // // console.log(
  //     '触发暂停上传任务',
  //     item.content_finish_idx, item.content_max_idx
  // )
  // 更新后端上传任务状态
  let params = {
    task_id: item.id,
    task_status: 'pause'
  };
  update_upload_task(params);
  // 更新管理器状态：如果所有任务都暂停了，那么管理器状态也为pause
  let allPause = true;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status !== 'pause') {
      allPause = false;
      break;
    }
  }
  if (allPause) {
    upload_manager_status.value = 'pause';
  }
}
async function pauseAllUploadTask() {
  // 暂停所有上传任务
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status !== 'uploading') {
      continue;
    }
    upload_file_task_list.value[i].task_status = 'pause';
    upload_file_task_list.value[i].content_finish_idx -= 1;
    // 更新后端上传任务状态
    let params = {
      task_id: upload_file_task_list.value[i].id,
      task_status: 'pause'
    };
    update_upload_task(params);
  }
  upload_manager_status.value = 'pause';
}

async function continueUploadTask(item: IResourceUploadItem) {
  // 更新后端上传任务状态
  let params = {
    task_id: item.id,
    task_status: 'uploading'
  };
  await update_upload_task(params);
  // 继续上传任务,修改任务状态为uploading，然后继续上传
  item.task_status = 'uploading';
  // // console.log(
  //     '触发继续上传任务',
  //     item.content_finish_idx, item.content_max_idx
  // )
  upload_file_content(<UploadRequestOptions>{
    file: item.raw_file,
    data: {},
    headers: {}
  });
  // 更新管理器状态
  upload_manager_status.value = 'uploading';
}
function getUploadSpeed() {
  // 获取上传速度: 3s内上传的文件大小
  let currentTime = Date.now();
  let lastTime = currentTime - 3000;
  let finishUploadSizeIn = 0;
  for (let key in finish_time_size_map.value) {
    if (parseInt(key) > lastTime) {
      finishUploadSizeIn += finish_time_size_map.value[key];
    }
  }
  return parseFloat((finishUploadSizeIn / 1024 / 1024 / 3).toFixed(2));
}

function getUploadTaskProgress(item: IResourceUploadItem, output: string = 'number') {
  // 获取上传任务进度,以MB为单位或者以比例返回
  if (item.content_finish_idx === -1) {
    return 0;
  }
  if (output === 'number') {
    if (item.task_status === 'success') {
      return parseFloat(item.resource_size_in_mb.toFixed(4));
    }
    return item.content_finish_idx * upload_size.value;
  }
  let progress = Math.floor(((item.content_finish_idx * upload_size.value) / item.resource_size_in_mb) * 100);
  return parseFloat(progress.toFixed(4));
}
function getSuccessUploadSize() {
  // 获取已经上传成功的文件大小
  let size = 0;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status === 'success') {
      size += upload_file_task_list.value[i].resource_size_in_mb;
    }
  }
  return parseFloat(size.toFixed(4));
}
function getSuccessUploadTask() {
  // 获取已经上传成功的文件数量
  let count = 0;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (upload_file_task_list.value[i].task_status === 'success') {
      count++;
    }
  }
  return count;
}
</script>

<template>
  <div v-show="show_upload_manage_box" id="upload_manager">
    <div id="upload_header">
      <div id="upload_header_left">
        <div id="upload_status_icon">
          <el-image src="/images/upload_blue.svg" style="width: 20px; height: 20px" />
        </div>
        <div v-if="upload_manager_status == 'uploading'" id="upload_status_text">
          <el-text>上传中 {{ getSuccessUploadTask() }}/{{ upload_file_task_list.length }}</el-text>
        </div>
        <div v-if="upload_manager_status == 'pending'" id="upload_status_text">
          <el-text>上传中 0/{{ upload_file_task_list.length }}</el-text>
        </div>
        <div v-if="upload_manager_status == 'pause'" id="upload_status_text">
          <el-text type="warning">全部暂停</el-text>
        </div>
        <div v-if="upload_manager_status == 'success'" id="upload_status_text">
          <el-text type="success">全部上传成功</el-text>
        </div>
      </div>
      <div id="upload_header_right">
        <div class="upload_button" @click="showUploadFileDetail = !showUploadFileDetail">
          <el-image
            v-if="showUploadFileDetail"
            src="/images/triangle_down_blue.svg"
            style="width: 20px; height: 20px"
          />
          <el-image
            v-if="!showUploadFileDetail"
            src="/images/triangle_right_grey.svg"
            style="width: 20px; height: 20px"
          />
        </div>
        <div class="upload_button" @click="close_upload_manager()">
          <el-image src="/images/close_grey.svg" style="width: 20px; height: 20px" />
        </div>
      </div>
    </div>
    <div v-if="showUploadFileDetail" id="upload_status">
      <div id="upload_status_left">
        <el-text v-if="upload_manager_status == 'pause'">
          已上传 {{ getSuccessUploadTask() }}/{{ upload_file_task_list.length }} 个任务
        </el-text>
        <el-text v-if="upload_manager_status == 'success'">
          已上传 {{ getSuccessUploadTask() }} 个任务, 共 {{ getSuccessUploadSize() }}MB
        </el-text>
        <el-text v-if="upload_manager_status == 'uploading'"> 速度： {{ getUploadSpeed() }} MB/s </el-text>
      </div>
      <div id="upload_status_right">
        <div v-if="upload_manager_status == 'uploading'" class="upload_button" @click="pauseAllUploadTask">
          <el-text>全部暂停</el-text>
        </div>
        <div v-if="upload_manager_status == 'pause'" class="upload_button" @click="continueAllUploadTask">
          <el-text>全部继续</el-text>
        </div>
      </div>
    </div>
    <el-scrollbar wrap-style="width : 100%" view-style="width : 100%" style="width: 100%">
      <div v-if="showUploadFileDetail" id="upload_queue">
        <div v-for="item in upload_file_task_list" :key="item.id" class="upload-task-item">
          <div class="upload-task-left">
            <div class="upload-task-icon">
              <img :src="item?.task_icon" alt="" class="resource-icon" />
            </div>
            <div class="upload-task-meta">
              <div class="upload-task-name">
                <el-text truncated>{{ item?.resource_name }}</el-text>
              </div>
              <div class="upload-task-progress-box">
                <el-text class="upload-task-progress-text">
                  {{ getUploadTaskProgress(item) }} MB / {{ parseFloat(item.resource_size_in_mb.toFixed(4)) }}MB
                </el-text>
              </div>
            </div>
          </div>
          <div class="upload-task-right">
            <div v-if="item.task_status == 'uploading'" class="upload-task-right-button-area">
              <el-progress :percentage="getUploadTaskProgress(item, 'progress')" type="circle" :width="40" />
              <div class="upload-button" @click="pauseUploadTask(item)">
                <el-image src="/images/pause_blue.svg" class="upload-button-icon" />
              </div>
            </div>

            <div v-if="item.task_status == 'success'" class="upload-task-right-button-area">
              <el-image src="/images/success_grey.svg" class="upload-button-icon" />
            </div>
            <div
              v-if="item.task_status != 'uploading' && item.task_status != 'success'"
              class="upload-task-right-button-area"
            >
              <el-tooltip v-if="item.task_status == 'error'" content="文件为空，无法上传">
                <el-image src="/images/notice_error_small.svg" class="upload-button-icon" />
              </el-tooltip>
              <div v-if="item.task_status != 'success'" class="upload-button" @click="removeUploadTask(item)">
                <el-image src="/images/close_grey.svg" class="upload-button-icon" />
              </div>
              <div v-if="item.task_status == 'error'" class="upload-button" @click="retryUploadTask(item)">
                <el-image src="/images/retry_grey.svg" class="upload-button-icon" />
              </div>
              <div v-if="item.task_status == 'pause'" class="upload-button" @click="continueUploadTask(item)">
                <el-image src="/images/continue.svg" class="upload-button-icon" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-scrollbar>
  </div>

  <el-dialog v-model="show_close_confirm_flag" style="max-width: 400px" top="40vh" :close-on-click-modal="false">
    <div id="upload_close_confirm_box">
      <div>
        <el-text id="close_confirm_text">仍有任务未完成，确认关闭上传管理器？</el-text>
      </div>
      <div id="upload_close_confirm_button_box">
        <el-button style="width: 120px" @click="show_close_confirm_flag = false">取消</el-button>
        <el-button style="width: 120px" type="primary" @click="cleanUploadManager">确认</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
#upload_manager {
  display: flex;
  max-width: 900px;
  min-width: 500px;
  max-height: 500px;
  width: calc(100% - 20px);
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  border: 1px solid #ebeef5;
  border-radius: 5px;
  margin: 10px;
  padding: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 999;
  background-color: white;
}
#upload_header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: calc(100% - 20px);
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
}
#upload_header_left {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  padding: 10px;
  gap: 10px;
}
#upload_header_right {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  padding: 10px;
}
.upload_button {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
#upload_status {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: calc(100% - 20px);
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
  background-color: #f0f0f0;
}
#upload_status_left {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}
#upload_status_right {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}
#upload_queue {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  width: calc(100% - 20px);
  padding: 10px;
  gap: 10px;
  max-height: 300px;
}
.upload-task-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
  width: calc(100% - 20px);
}
.upload-task-left {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}
#upload_close_confirm_box {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 10px;
  padding: 10px;
  width: calc(100% - 20px);
}
#upload_close_confirm_button_box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 10px;
  width: calc(100% - 20px);
}
#close_confirm_text {
  color: #101828;
  text-align: center;

  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 24px;
}
.upload-task-progress-text {
  font-weight: 300;
  font-size: 12px;
  line-height: 14px;
  color: #606266;
}
.upload-task-icon {
  width: 24px;
  height: 24px;
}
.upload-button {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.upload-button-icon {
  width: 16px;
  height: 16px;
}
.upload-task-right-button-area {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}
.upload-task-meta {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 2px;
}
.upload-task-name {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
.upload-task-progress-box {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
.resource-icon {
  width: 22px;
  height: 22px;
  margin-right: 4px;
}
@media (width < 768px) {
  #upload_manager {
    width: 300px;
    min-width: 200px;
  }
}
</style>
