<script setup lang="ts">

import {
  current_page_num,
  current_page_size,
  current_total, delete_notification,
  get_notification_data,
  handle_num_change,
  handle_search_by_keyword,
  handle_size_change,
  notification_data, pick_status, pick_type,
  search_keyword, search_notification
} from "@/components/user_center/user_notice/user_notification";
import {onMounted} from "vue";
import {Search} from "@element-plus/icons-vue";
import router from "@/router";
import {current_notice_task} from "@/components/user_center/user_notice/user_notice_detail";

const props = defineProps({
  page_size: {
    type: Number,
    default: 50
  },
  page_num: {
    type: Number,
    default: 1
  }
})

onMounted(async() => {
  current_page_num.value = props.page_num;
  current_page_size.value = props.page_size;
  get_notification_data();


})
</script>

<template>
<el-container>
  <el-header>
    <div id="notice-head">
      <div id="notice-head-left">
        <el-text class="next-console-font-bold" style="width: 60px;color: #101828"> 通知任务</el-text>
      </div>
      <div id="notice-head-right">
        <div class="std-middle-box">
          <el-input :prefix-icon="Search" placeholder="搜索名称或者描述"
                    @keydown.enter.prevent="handle_search_by_keyword"
                    @blur="handle_search_by_keyword"
                    @clear="get_notification_data"
                    v-model="search_keyword"
                    clearable
          />
        </div>
        <div class="std-middle-box" style="width: 150px">
          <el-select v-model="pick_status" multiple placeholder="全部状态" collapse-tags clearable
                     @change="search_notification"
          >
            <el-option label="新建中" value="新建中"></el-option>
            <el-option label="待执行" value="待执行"></el-option>
            <el-option label="执行中" value="执行中"></el-option>
            <el-option label="已暂停" value="已暂停"></el-option>
            <el-option label="已完成" value="已完成"></el-option>
            <el-option label="异常" value="异常"></el-option>
            <el-option label="已终止" value="已终止"></el-option>
          </el-select>
        </div>
        <div class="std-middle-box" style="width: 150px">
          <el-select v-model="pick_type" multiple placeholder="全部类型" collapse-tags clearable
                     @change="search_notification"
          >
            <el-option label="站内信" value="站内信"></el-option>
            <el-option label="邮件" value="邮件"></el-option>
          </el-select>
        </div>
        <div class="std-middle-box">
          <el-button type="primary" @click="router.push({'name': 'user_notice_detail'})">
            新建
          </el-button>
        </div>
      </div>
    </div>
  </el-header>
  <el-main style="height: calc(100vh - 170px)" >
    <el-scrollbar >
      <div id="notice-table-area">
        <el-table :data="notification_data" border stripe show-overflow-tooltip>
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="任务ID" sortable />
          <el-table-column prop="user_id" label="创建人" sortable />
          <el-table-column prop="task_name" label="任务名称" sortable />
          <el-table-column prop="task_desc" label="任务描述" sortable />
          <el-table-column prop="notice_type" label="通知类型" sortable />
          <el-table-column prop="task_status" label="任务状态" sortable min-width="100px">
            <template #default="{row}">
              <el-tag v-if="row.task_status === '待执行'" type="info">待执行</el-tag>
              <el-tag v-else-if="row.task_status === '执行中'" type="primary">执行中</el-tag>
              <el-tag v-else-if="row.task_status === '成功'" type="success">成功</el-tag>
              <el-tag v-else-if="row.task_status === '已暂停'" type="warning">已暂停</el-tag>
              <el-tag v-else-if="row.task_status === '已终止'" type="danger">已终止</el-tag>
              <el-tag v-else-if="row.task_status === '异常'" type="danger">异常</el-tag>
              <el-tag v-else type="primary">
                {{ row.task_status }}
              </el-tag>

            </template>
          </el-table-column>
          <el-table-column prop="task_instance_total" label="通知总数" sortable min-width="100px" />
          <el-table-column prop="task_instance_failed" label="通知失败数" sortable min-width="100px" />
          <el-table-column prop="task_progress" label="任务进度" sortable min-width="140px">
            <template #default="{row}">
              <el-progress :percentage="row.task_progress" status="exception"
                           :text-inside="true" :stroke-width="18"
                           v-if="row.task_instance_failed"
              />
              <el-progress :percentage="row.task_progress" status="success"
                           :text-inside="true" :stroke-width="18"
                           v-else-if="row.task_status === '已完成'"
              />

              <el-progress :percentage="row.task_progress" status="warning"
                           :text-inside="true" :stroke-width="18"
                           v-else-if="row.task_status === '已暂停' || row.task_status === '已终止'"
              />
              <el-progress :percentage="row.task_progress"
                           :text-inside="true" :stroke-width="18"
                           v-else
              />
            </template>
          </el-table-column>
          <el-table-column prop="begin_time" label="计划启动时间" sortable   />
          <el-table-column prop="begin_time" label="启动时间" sortable  />
          <el-table-column prop="finish_time" label="完成时间" sortable  />
          <el-table-column prop="update_time" label="操作" fixed min-width="80px">
            <template #default="{row}">
              <el-button type="primary" size="small" @click="router.push({
                name: 'user_notice_detail',
                query: {task_id: row.id}
              })" round>查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-scrollbar>

  </el-main>
  <el-footer>
    <el-pagination
        size="small"
        layout=" total, sizes, prev, pager, next"
        :total="current_total"
        :page-sizes="[10,20,50,100]"
        :page-size="current_page_size"
        :current-page="current_page_num"
        @update:page-size="handle_size_change"
        @update:current-page="handle_num_change"
    />
  </el-footer>
</el-container>
</template>

<style scoped>
.std-middle-box{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  height: 100%;
  gap: 12px;
}
#notice-head{
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  width: 100%;
  height:60px;
  gap: 12px;
}
#notice-head-left{
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  max-width: 100px;
  height: 100%;
  gap: 12px;
}
#notice-head-right{
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: flex-end;
  width: 100%;
  height: 100%;
  gap: 12px;
}
#notice-table-area{
  width: 100%;
  height: 100%;

}
</style>
