<script setup lang="ts">
import { Search } from '@element-plus/icons-vue';
import { onMounted, ref } from 'vue';

import { listTask, searchTask } from '@/api/user-notice';
import router from '@/router';
import { IUserNoticeTaskInfo } from '@/types/user-center';

const props = defineProps({
  pageSize: {
    type: Number,
    default: 50
  },
  pageNum: {
    type: Number,
    default: 1
  }
});

const notificationData = ref<IUserNoticeTaskInfo[]>([]);
const currentPageNum = ref(1);
const currentPageSize = ref(10);
const currentTotal = ref(0);
const searchKeyword = ref('');
const pickStatus = ref([]);
const pickType = ref([]);

async function getNotificationData() {
  // 获取通知列表
  // @ts-ignore
  const res = await listTask({
    page_num: currentPageNum.value,
    page_size: currentPageSize.value
  });
  if (!res.error_status) {
    notificationData.value = res.result.data;
    currentTotal.value = res.result.total;
  }
}
async function handleSizeChange(val: number) {
  currentPageSize.value = val;
  await getNotificationData();
}
async function handleNumChange(val: number) {
  currentPageNum.value = val;
  await getNotificationData();
}

async function handleSearchByKeyword() {
  if (!searchKeyword.value) {
    return;
  }
  await searchNotification();
}

async function searchNotification() {
  const params = {
    keyword: searchKeyword.value,
    fetch_all: true,
    task_status: pickStatus.value,
    notice_type: pickType.value
  };
  const res = await searchTask(params);
  if (!res.error_status) {
    notificationData.value = res.result.data;
    currentTotal.value = res.result.total;
  }
}
function getTaskProgressStatus(status: string) {
  switch (status) {
    case '待执行':
      return 'info';
    case '执行中':
      return 'primary';
    case '已完成':
      return 'success';
    case '已暂停':
      return 'warning';
    case '已终止':
      return 'warning';
    case '异常':
      return 'danger';
    default:
      return 'primary';
  }
}
onMounted(async () => {
  currentPageNum.value = props.pageNum;
  currentPageSize.value = props.pageSize;
  getNotificationData();
});
</script>

<template>
  <el-container>
    <el-header>
      <div id="notice-head">
        <div id="notice-head-left">
          <el-text class="next-console-font-bold" style="width: 60px; color: #101828"> 通知任务</el-text>
        </div>
        <div id="notice-head-right">
          <div class="std-middle-box">
            <el-input
              v-model="searchKeyword"
              :prefix-icon="Search"
              placeholder="搜索名称或者描述"
              clearable
              @keydown.enter.prevent="handleSearchByKeyword"
              @blur="handleSearchByKeyword"
              @clear="getNotificationData"
            />
          </div>
          <div class="std-middle-box" style="width: 150px">
            <el-select
              v-model="pickStatus"
              multiple
              placeholder="全部状态"
              collapse-tags
              clearable
              @change="searchNotification"
            >
              <el-option label="新建中" value="新建中" />
              <el-option label="待执行" value="待执行" />
              <el-option label="执行中" value="执行中" />
              <el-option label="已暂停" value="已暂停" />
              <el-option label="已完成" value="已完成" />
              <el-option label="异常" value="异常" />
              <el-option label="已终止" value="已终止" />
            </el-select>
          </div>
          <div class="std-middle-box" style="width: 150px">
            <el-select
              v-model="pickType"
              multiple
              placeholder="全部类型"
              collapse-tags
              clearable
              @change="searchNotification"
            >
              <el-option label="站内信" value="站内信" />
              <el-option label="邮件" value="邮件" />
            </el-select>
          </div>
          <div class="std-middle-box">
            <el-button type="primary" @click="router.push({ name: 'user_notice_detail' })"> 新建 </el-button>
          </div>
        </div>
      </div>
    </el-header>
    <el-main style="height: calc(100vh - 170px)">
      <el-scrollbar>
        <div id="notice-table-area">
          <el-table :data="notificationData" border stripe show-overflow-tooltip>
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="任务ID" sortable />
            <el-table-column prop="user_id" label="创建人" sortable />
            <el-table-column prop="task_name" label="任务名称" sortable />
            <el-table-column prop="task_desc" label="任务描述" sortable />
            <el-table-column prop="notice_type" label="通知类型" sortable />
            <el-table-column prop="task_status" label="任务状态" sortable min-width="100px">
              <template #default="{ row }">
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
            <el-table-column prop="instance_count" label="实例总数" sortable min-width="100px" />
            <el-table-column prop="failed_count" label="失败数" sortable min-width="100px" />
            <el-table-column prop="task_progress" label="任务进度" sortable min-width="140px">
              <template #default="{ row }">
                <el-progress
                  :percentage="row.task_progress"
                  :status="getTaskProgressStatus(row.task_status)"
                  :text-inside="true"
                  :stroke-width="18"
                />
              </template>
            </el-table-column>
            <el-table-column prop="begin_time" label="计划启动时间" sortable />
            <el-table-column prop="begin_time" label="启动时间" sortable />
            <el-table-column prop="finish_time" label="完成时间" sortable />
            <el-table-column prop="update_time" label="操作" fixed min-width="80px">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  size="small"
                  round
                  @click="
                    router.push({
                      name: 'user_notice_detail',
                      query: { taskId: row.id }
                    })
                  "
                >
                  查看
                </el-button>
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
        :total="currentTotal"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="currentPageSize"
        :current-page="currentPageNum"
        @update:page-size="handleSizeChange"
        @update:current-page="handleNumChange"
      />
    </el-footer>
  </el-container>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  height: 100%;
  gap: 12px;
}
#notice-head {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  width: calc(100% - 32px);
  height: 60px;
  gap: 12px;
  padding: 12px;
}
#notice-head-left {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  max-width: 100px;
  height: 100%;
  gap: 12px;
}
#notice-head-right {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: flex-end;
  width: 100%;
  height: 100%;
  gap: 16px;
}
#notice-table-area {
  width: 100%;
  height: 100%;
}
</style>
