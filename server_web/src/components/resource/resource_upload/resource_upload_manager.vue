<script setup lang="ts">

import {
  clean_upload_manager,
  close_upload_manager,
  continue_all_upload_task,
  continue_upload_task,
  get_success_upload_size,
  get_success_upload_task,
  get_upload_speed,
  get_upload_task_progress,
  pause_all_upload_task,
  pause_upload_task,
  remove_upload_task,
  retry_upload_task,
  show_close_confirm_flag,
  show_upload_file_detail,
  show_upload_manage_box,
  upload_file_task_list,
  upload_manager_status
} from "@/components/resource/resource_upload/resource_upload";
import Resource_view_tree from "@/components/resource/resource_tree/resource_view_tree.vue";
</script>

<template>
  <div id="upload_manager" v-show="show_upload_manage_box">
    <div id="upload_header">
      <div id="upload_header_left">
        <div id="upload_status_icon">
          <el-image src="/images/upload_blue.svg" style="width: 20px;height: 20px;"/>
        </div>
        <div id="upload_status_text" v-show="upload_manager_status == 'uploading'">
          <el-text>上传中 {{get_success_upload_task()}}/{{upload_file_task_list.length}}</el-text>
        </div>
        <div id="upload_status_text" v-show="upload_manager_status == 'pending'">
          <el-text>上传中 0/{{upload_file_task_list.length}}</el-text>
        </div>
        <div id="upload_status_text" v-show="upload_manager_status == 'pause'">
          <el-text type="warning">全部暂停</el-text>
        </div>
        <div id="upload_status_text" v-show="upload_manager_status == 'success'">
          <el-text type="success">全部上传成功</el-text>
        </div>
      </div>
      <div id="upload_header_right">
        <div class="upload_button" @click="show_upload_file_detail = !show_upload_file_detail">
          <el-image src="/images/triangle_down_blue.svg" style="width: 20px;height: 20px;"
                    v-show="show_upload_file_detail"/>
          <el-image src="/images/triangle_right_grey.svg" style="width: 20px;height: 20px;"
                    v-show="!show_upload_file_detail"/>
        </div>
        <div  class="upload_button" @click="close_upload_manager()">
          <el-image src="/images/close_grey.svg" style="width: 20px;height: 20px;"/>
        </div>
      </div>
    </div>
    <div id="upload_status" v-show="show_upload_file_detail">
      <div id="upload_status_left">
        <el-text v-show="upload_manager_status== 'pause'">
          已上传 {{get_success_upload_task()}}/{{upload_file_task_list.length}} 个任务
        </el-text>
        <el-text v-show="upload_manager_status== 'success'">

          已上传 {{get_success_upload_task()}} 个任务, 共 {{get_success_upload_size()}}MB
        </el-text>
        <el-text v-show="upload_manager_status== 'uploading'">
          速度： {{get_upload_speed()}} MB/s
        </el-text>
      </div>
      <div id="upload_status_right">
        <div class="upload_button" v-show="upload_manager_status == 'uploading'" @click="pause_all_upload_task()">
          <el-text>全部暂停</el-text>
        </div>
        <div class="upload_button" v-show="upload_manager_status == 'pause'" @click="continue_all_upload_task()">
          <el-text>全部继续</el-text>
        </div>
      </div>

    </div>
    <el-scrollbar wrap-style="width : 100%" view-style="width : 100%" style="width: 100%">
      <div id="upload_queue" v-show="show_upload_file_detail">

          <div v-for="item in upload_file_task_list" class="upload-task-item">
            <div class="upload-task-left">
              <div class="upload-task-icon">
                <img :src="item?.task_icon" alt="" class="resource-icon"/>
              </div>
              <div class="upload-task-meta">
                <div class="upload-task-name">
                  <el-text truncated>{{item?.resource_name}}</el-text>
                </div>
                <div class="upload-task-progress-box">
                  <el-text class="upload-task-progress-text">
                    {{
                      get_upload_task_progress(item)
                    }} MB / {{
                      parseFloat(item.resource_size_in_mb.toFixed(4))
                    }}MB
                  </el-text>

                </div>
              </div>
            </div>
            <div class="upload-task-right">

              <div v-show="item.task_status == 'uploading'" class="upload-task-right-button-area">
                <el-progress :percentage="get_upload_task_progress(item, 'progress')" type="circle" :width="40"/>
                <div class="upload-button" @click="pause_upload_task(item)">
                  <el-image src="/images/pause_blue.svg" class="upload-button-icon"/>
                </div>
              </div>

              <div v-show="item.task_status == 'success'" class="upload-task-right-button-area">
                <el-image src="/images/success_grey.svg" class="upload-button-icon"/>
              </div>
              <div v-show="item.task_status != 'uploading' && item.task_status != 'success'"
                   class="upload-task-right-button-area">
                <el-tooltip v-if="item.task_status == 'error'" content="文件为空，无法上传">
                  <el-image src="/images/notice_error_small.svg"  class="upload-button-icon"></el-image>
                </el-tooltip>
                <div class="upload-button" v-show="item.task_status != 'success'" @click="remove_upload_task(item)">
                  <el-image src="/images/close_grey.svg" class="upload-button-icon"/>
                </div>
                <div class="upload-button" v-show="item.task_status == 'error'" @click="retry_upload_task(item)">
                  <el-image src="/images/retry_grey.svg" class="upload-button-icon"/>
                </div>
                <div class="upload-button" v-show="item.task_status == 'pause'" @click="continue_upload_task(item)">
                  <el-image src="/images/continue.svg" class="upload-button-icon"/>
                </div>

              </div>

            </div>
          </div>





      </div>
    </el-scrollbar>
  </div>

  <el-dialog v-model="show_close_confirm_flag" style="max-width: 400px" top="40vh"
             :close-on-click-modal="false">
    <div id="upload_close_confirm_box">
      <div>
        <el-text id="close_confirm_text">仍有任务未完成，确认关闭上传管理器？</el-text>
      </div>
      <div id="upload_close_confirm_button_box">

        <el-button @click="show_close_confirm_flag = false" style="width: 120px">取消</el-button>
        <el-button @click="clean_upload_manager()" style="width: 120px" type="primary">确认</el-button>
      </div>
    </div>



  </el-dialog>
</template>

<style scoped>
#upload_manager{
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
  box-shadow:  0 2px 12px 0 rgba(0,0,0,0.1);
  z-index: 999;
  background-color: white;
}
#upload_header{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width:  calc(100% - 20px);
  padding: 10px;
  border-bottom: 1px solid #ebeef5;

}
#upload_header_left{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  padding: 10px;
  gap: 10px;
}
#upload_header_right{
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  padding: 10px;
}
.upload_button{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
#upload_status{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: calc( 100% - 20px);
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
  background-color:  #f0f0f0;
}
#upload_status_left{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}
#upload_status_right{
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}
#upload_queue{
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  width: calc( 100% - 20px);
  padding: 10px;
  gap: 10px;
  max-height: 300px;
}
.upload-task-item{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
  width: calc(100% - 20px);
}
.upload-task-left{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}
#upload_close_confirm_box{
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 10px;
  padding: 10px;
  width: calc(100% - 20px);
}
#upload_close_confirm_button_box{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 10px;
  width: calc(100% - 20px);
}
#close_confirm_text{
  color:  #101828;
  text-align: center;

  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 24px;
}
.upload-task-progress-text{
  font-weight: 300;
  font-size: 12px;
  line-height: 14px;
  color: #606266;
}
.upload-task-icon{
  width: 24px;
  height: 24px;
}
.upload-button{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.upload-button-icon{
  width: 16px;
  height: 16px;
}
.upload-task-right-button-area{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;

}
.upload-task-meta{
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 2px;
}
.upload-task-name{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
.upload-task-progress-box{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
.resource-icon{
  width: 22px;
  height: 22px;
  margin-right: 4px;
}
@media (width < 768px) {
  #upload_manager{
    width: 300px;
    min-width: 200px;
  }
}
</style>
