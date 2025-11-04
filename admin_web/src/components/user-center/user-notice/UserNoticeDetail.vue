<script setup lang="ts">
import DOMPurify from 'dompurify';
import { ElMessage } from 'element-plus';
import { reactive, ref, watch } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';

import {
  deleteTask,
  getTaskDetail,
  initTask,
  listTaskInstance,
  pauseTask,
  searchNoticeCompany,
  searchNoticeDepartment,
  searchNoticeUser,
  startTask,
  updateTask,
  resumeTask,
  stopTask
} from '@/api/user-notice';
import router from '@/router';
import { ICompany, IDepartment } from '@/types/contacts';
import { ITaskInstance, IUserNoticeTaskInfo, IUsers } from '@/types/user-center';

const props = defineProps({
  taskId: {
    type: Number,
    require: false,
    default: null
  }
});

const currentNoticeTask = reactive<IUserNoticeTaskInfo>({} as IUserNoticeTaskInfo);
const currentNoticeTemplateValid = ref(false);
const previewContent = ref('');
const areaShortcut = ref([]);
const noticeTaskRef = ref(null);
const taskLoading = ref(false);
const loadingText = ref('加载中...');

const areaTargetCompanies = ref<ICompany[]>([]);
const areaTargetDepartments = ref<IDepartment[]>([]);
const areaTargetUsers = ref<IUsers[]>([]);

const areaCompanyOptions = ref<ICompany[]>([]);
const areaDepartmentOptions = ref<IDepartment[]>([]);
const areaUserOptions = ref<IUsers[]>([]);
const refreshInterval = ref(null);
const currentTaskInstances = ref<ITaskInstance[]>([]);

const noticeTaskRules = reactive({
  task_name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  task_desc: [{ required: true, message: '请输入任务描述', trigger: 'blur' }],

  notice_template: [{ validator: validTemplate, trigger: 'blur' }],
  notice_params: [{ validator: validNoticeParams, trigger: 'blur' }],
  notice_type: [{ required: true, message: '请选择通知类型', trigger: 'blur' }],
  plan_begin_time: [{ validator: validPlanTime, trigger: 'blur' }],
  plan_end_time: [{ validator: validPlanTime, trigger: 'blur' }],
  run_now: [{ validator: validRightNow, message: '请选择是否立即执行', trigger: 'blur' }]
});

function validPlanTime(rule: any, value: any, callback: any) {
  if (currentNoticeTask.plan_begin_time && currentNoticeTask.plan_finish_time) {
    if (currentNoticeTask.plan_begin_time > currentNoticeTask.plan_finish_time) {
      return callback(new Error('计划开始时间不能大于计划结束时间'));
    }
  }
  if (!value && !currentNoticeTask.run_now) {
    return callback(new Error('请选择是否立即执行或者计划开始时间'));
  }
  callback();
}

function validRightNow(rule: any, value: any, callback: any) {
  if (!value && !currentNoticeTask.plan_begin_time) {
    return callback(new Error('请选择是否立即执行或者计划开始时间'));
  }
  callback();
}

function validTemplate(rule: any, value: any, callback: any) {
  if (!value) {
    return callback(new Error('请输入通知内容'));
  }
  try {
    const sanitizedContent = DOMPurify.sanitize(currentNoticeTask.notice_template);
    if (!sanitizedContent) {
      throw new Error('内容为空或不合法');
    }
    previewContent.value = sanitizedContent;
    currentNoticeTemplateValid.value = true;
  } catch (e) {
    currentNoticeTemplateValid.value = false;
    return callback(new Error('请输入正确的通知内容'));
  }
  callback();
}

function validNoticeParams(rule: any, value: any, callback: any) {
  if (!value) {
    return callback(new Error('请选择通知范围'));
  }
  // 不能全为空
  if (
    !value.all_user &&
    !value.all_company_user &&
    !value.all_person_user &&
    !value.all_subscribe_email &&
    !value.target_companies?.length &&
    !value.target_departments?.length &&
    !value.target_users?.length
  ) {
    return callback(new Error('请选择通知范围'));
  }
  callback();
}

async function searchCompany(val: string) {
  if (!val) {
    return;
  }
  const params = {
    keyword: val
  };
  const res = await searchNoticeCompany(params);
  if (!res.error_status) {
    areaCompanyOptions.value = res.result.data;
  }
}

async function searchDepartment(val: string) {
  if (!val) {
    return;
  }
  const params = {
    keyword: val
  };
  const res = await searchNoticeDepartment(params);
  if (!res.error_status) {
    areaDepartmentOptions.value = res.result.data;
  }
}

async function searchUser(val: string) {
  if (!val) {
    return;
  }
  const params = {
    keyword: val
  };
  const res = await searchNoticeUser(params);
  if (!res.error_status) {
    areaUserOptions.value = res.result.data;
  }
}

function handleNoticeCompanyChange(val: any) {
  currentNoticeTask.notice_params.target_companies = val;
}

function handleNoticeDepartmentChange(val: any) {
  currentNoticeTask.notice_params.target_departments = val;
}

function handleNoticeUserChange(val: any) {
  currentNoticeTask.notice_params.target_users = val;
}

function handleNoticeAreaChange(val: any) {
  currentNoticeTask.notice_params.all_user = !!val.includes('all_user');
  currentNoticeTask.notice_params.all_company_user = !!val.includes('all_company_user');
  currentNoticeTask.notice_params.all_person_user = !!val.includes('all_person_user');
  currentNoticeTask.notice_params.all_subscribe_email = !!val.includes('all_subscribe_email');
  currentNoticeTask.notice_params.target_company = !!val.includes('target_company');
  currentNoticeTask.notice_params.target_department = !!val.includes('target_department');
  currentNoticeTask.notice_params.target_user = !!val.includes('target_user');
}

async function updateCurrentTask() {
  const validRes = await noticeTaskRef.value?.validate();
  if (!validRes) {
    return;
  }
  const params = {
    task_id: currentNoticeTask.id,
    task_name: currentNoticeTask.task_name,
    task_desc: currentNoticeTask.task_desc,
    plan_begin_time: currentNoticeTask.plan_begin_time,
    plan_finish_time: currentNoticeTask.plan_finish_time,
    notice_template: currentNoticeTask.notice_template,
    notice_params: currentNoticeTask.notice_params,
    notice_type: currentNoticeTask.notice_type,
    run_now: currentNoticeTask.run_now,
    batch_size: currentNoticeTask.task_instance_batch_size
  };
  taskLoading.value = true;
  loadingText.value = '保存中...';
  const res = await updateTask(params);
  if (!res.error_status) {
    ElMessage.success({
      message: '保存成功',
      duration: 6000
    });
    Object.assign(currentNoticeTask, res.result);
  }
  taskLoading.value = false;
  router.push({
    name: 'user_notice_detail',
    query: {
      taskId: currentNoticeTask.id
    }
  });
}

function checkHtmlValid() {
  try {
    const sanitizedContent = DOMPurify.sanitize(currentNoticeTask.notice_template);
    if (!sanitizedContent) {
      throw new Error('内容为空或不合法');
    }
    previewContent.value = sanitizedContent;
    currentNoticeTemplateValid.value = true;
  } catch (e) {
    currentNoticeTemplateValid.value = false;
  }
}

async function initCurrentTask(taskId: number) {
  if (taskId) {
    // @ts-ignore
    const res = await getTaskDetail({
      task_id: taskId
    });
    if (!res.error_status) {
      Object.assign(currentNoticeTask, res.result);
    }
    if (currentNoticeTask.task_status != '新建中') {
      const instances = await listTaskInstance({
        task_id: taskId,
        page_num: 1,
        page_size: currentNoticeTask.task_instance_total
      });
      if (!instances.error_status) {
        currentTaskInstances.value = instances.result.data;
      }
    } else {
      currentTaskInstances.value = [];
    }
  } else {
    const res = await initTask({});
    if (!res.error_status) {
      Object.assign(currentNoticeTask, res.result);
      router.push({
        name: 'user_notice_detail',
        query: {
          task_id: currentNoticeTask.id
        }
      });
    }
  }
  checkHtmlValid();
  // 获取快捷区域
  areaShortcut.value = [];
  if (currentNoticeTask.notice_params.all_user) {
    areaShortcut.value.push('all_user');
  }
  if (currentNoticeTask.notice_params.all_company_user) {
    areaShortcut.value.push('all_company_user');
  }
  if (currentNoticeTask.notice_params.all_person_user) {
    areaShortcut.value.push('all_person_user');
  }
  if (currentNoticeTask.notice_params.all_subscribe_email) {
    areaShortcut.value.push('all_subscribe_email');
  }
  if (currentNoticeTask.notice_params.target_company) {
    areaShortcut.value.push('target_company');
  }
  if (currentNoticeTask.notice_params.target_department) {
    areaShortcut.value.push('target_department');
  }
  if (currentNoticeTask.notice_params.target_user) {
    areaShortcut.value.push('target_user');
  }
  if (currentNoticeTask.notice_params.target_company) {
    areaTargetCompanies.value = currentNoticeTask.notice_params.target_companies;
    areaCompanyOptions.value = currentNoticeTask.notice_params.target_companies;
  }
  if (currentNoticeTask.notice_params.target_department) {
    areaTargetDepartments.value = currentNoticeTask.notice_params.target_departments;
    areaDepartmentOptions.value = currentNoticeTask.notice_params.target_departments;
  }
  if (currentNoticeTask.notice_params.target_user) {
    areaTargetUsers.value = currentNoticeTask.notice_params.target_users;
    areaUserOptions.value = currentNoticeTask.notice_params.target_users;
  }
}

async function startNoticeTask() {
  await updateCurrentTask();
  const res = await noticeTaskRef.value?.validate();
  if (!res) {
    return;
  }
  checkHtmlValid();
  if (!currentNoticeTemplateValid.value) {
    return;
  }
  taskLoading.value = true;
  loadingText.value = '任务提交中...';
  const params = {
    task_id: currentNoticeTask.id
  };
  const taskRes = await startTask(params);
  if (!res.error_status) {
    Object.assign(currentNoticeTask, taskRes.result);
  }
  ElMessage.success({
    message: '任务提交成功！',
    duration: 3000
  });
  taskLoading.value = false;
  // 开始刷新任务详情
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value);
  }
  refreshInterval.value = setInterval(refreshTaskDetail, 2000);
}

async function deleteCurrentTask() {
  if (currentNoticeTask.task_status == '执行中') {
    ElMessage.warning({
      message: '运行中的任务不能删除！请先暂停或者终止',
      duration: 5000
    });
    return;
  }
  const res = await deleteTask({
    task_id: currentNoticeTask.id
  });
  if (!res.error_status) {
    ElMessage.success({
      message: '删除成功',
      duration: 3000
    });
    currentNoticeTask.id = null;
  }
  await router.push({ name: 'user_notification_list' });
}

async function pauseNoticeTask() {
  const res = await pauseTask({
    task_id: currentNoticeTask.id
  });
  if (!res.error_status) {
    if (res.error_message) {
      ElMessage.warning({
        message: res.error_message,
        duration: 3000
      });
    }
    Object.assign(currentNoticeTask, res.result);
    if (refreshInterval.value) {
      clearInterval(refreshInterval.value);
    }
  }
}

async function resumeNoticeTask() {
  const res = await resumeTask({
    task_id: currentNoticeTask.id
  });
  if (!res.error_status) {
    Object.assign(currentNoticeTask, res.result);
    if (refreshInterval.value) {
      clearInterval(refreshInterval.value);
    }
    refreshInterval.value = setInterval(refreshTaskDetail, 2000);
  }
}

async function stopNoticeTask() {
  const res = await stopTask({
    task_id: currentNoticeTask.id
  });
  if (!res.error_status) {
    Object.assign(currentNoticeTask, res.result);
  }
}
async function refreshTaskDetail() {
  if (currentNoticeTask?.task_status != '执行中' && refreshInterval.value) {
    clearInterval(refreshInterval.value);
    return;
  }
  const res = await getTaskDetail({
    task_id: currentNoticeTask.id
  });
  if (!res.error_status) {
    currentNoticeTask.task_status = res.result.task_status;
    currentNoticeTask.task_progress = res.result.task_progress;
    currentNoticeTask.begin_time = res.result.begin_time;
    currentNoticeTask.finish_time = res.result.finish_time;
    currentNoticeTask.task_instance_total = res.result.task_instance_total;
    currentNoticeTask.task_instance_success = res.result.task_instance_success;
    currentNoticeTask.task_instance_failed = res.result.task_instance_failed;
  }
}

watch(
  () => props.taskId,
  async newTaskId => {
    await initCurrentTask(newTaskId);
    if (currentNoticeTask.task_status === '执行中') {
      // 开始刷新任务详情
      if (refreshInterval.value) {
        clearInterval(refreshInterval.value);
      }
      refreshInterval.value = setInterval(refreshTaskDetail, 2000);
    }
  },
  { immediate: true }
);
onBeforeRouteLeave(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value);
  }
});
</script>

<template>
  <el-container>
    <el-header>
      <div id="detail-header-area">
        <div id="detail-header-left">
          <div>
            <el-text class="next-console-font-bold" style="width: 60px; color: #101828"> 任务详情</el-text>
          </div>
        </div>
        <div id="detail-header-right">
          <div>
            <el-button type="primary" round @click="router.push({ name: 'user_notification_list' })"> 返回 </el-button>
          </div>
          <div v-if="currentNoticeTask.task_status == '新建中'">
            <el-button type="primary" round @click="updateCurrentTask"> 保存 </el-button>
          </div>
          <div v-if="currentNoticeTask.task_status == '新建中'">
            <el-button type="success" round @click="startNoticeTask"> 启动 </el-button>
          </div>
          <div v-else-if="currentNoticeTask.task_status == '执行中'">
            <el-button type="info" round @click="pauseNoticeTask"> 暂停 </el-button>
          </div>
          <div v-else-if="currentNoticeTask.task_status == '已暂停'">
            <el-button type="info" round @click="resumeNoticeTask"> 恢复 </el-button>
          </div>
          <div v-if="!['新建中', '已终止', '已完成'].includes(currentNoticeTask.task_status)">
            <el-button type="warning" round @click="stopNoticeTask"> 终止 </el-button>
          </div>
          <div v-if="['新建中', '已终止', '已完成'].includes(currentNoticeTask.task_status)">
            <el-popconfirm title="删除后不可找回，是否继续？" @confirm="deleteCurrentTask">
              <template #reference>
                <el-button type="danger" round> 删除 </el-button>
              </template>
            </el-popconfirm>
          </div>
        </div>
      </div>
    </el-header>
    <el-main>
      <el-scrollbar style="height: calc(100vh - 200px)">
        <div id="notice-detail-area" v-loading="taskLoading" :element-loading-text="loadingText">
          <el-form label-position="top" inline style="max-width: 925px">
            <el-form-item label="编号" prop="id">
              <el-input v-model="currentNoticeTask.id" readonly />
            </el-form-item>
            <el-form-item label="创建用户" prop="user_id">
              <el-input v-model="currentNoticeTask.user_id" readonly />
            </el-form-item>
            <el-form-item label="状态" prop="task_status">
              <el-input v-model="currentNoticeTask.task_status" readonly />
            </el-form-item>
            <el-form-item label="创建时间">
              <el-input v-model="currentNoticeTask.create_time" readonly />
            </el-form-item>
            <el-form-item label="更新时间">
              <el-input v-model="currentNoticeTask.update_time" readonly />
            </el-form-item>
            <el-form-item label="启动时间">
              <el-input v-model="currentNoticeTask.begin_time" readonly />
            </el-form-item>
            <el-form-item label="完成时间">
              <el-input v-model="currentNoticeTask.finish_time" readonly />
            </el-form-item>
            <el-form-item label="通知总数">
              <el-input v-model="currentNoticeTask.task_instance_total" readonly />
            </el-form-item>
            <el-form-item label="任务进度" style="width: 100%">
              <el-progress
                v-if="currentNoticeTask.task_instance_failed"
                :percentage="currentNoticeTask.task_progress"
                status="exception"
                :text-inside="true"
                :stroke-width="18"
                style="width: 100%"
              />
              <el-progress
                v-else-if="currentNoticeTask.task_status === '已完成'"
                :percentage="currentNoticeTask.task_progress"
                status="success"
                :text-inside="true"
                :stroke-width="18"
                style="width: 100%"
              />

              <el-progress
                v-else-if="currentNoticeTask.task_status === '已暂停' || currentNoticeTask.task_status === '已终止'"
                :percentage="currentNoticeTask.task_progress"
                status="warning"
                :text-inside="true"
                :stroke-width="18"
                style="width: 100%"
              />
              <el-progress
                v-else-if="currentNoticeTask.task_status === '执行中'"
                :percentage="currentNoticeTask.task_progress"
                :text-inside="true"
                :stroke-width="18"
                style="width: 100%"
              />
              <el-text v-else> 暂无进度 </el-text>
            </el-form-item>
          </el-form>
          <el-form
            ref="noticeTaskRef"
            :model="currentNoticeTask"
            label-position="top"
            style="max-width: 925px; width: 100%"
            :rules="noticeTaskRules"
          >
            <el-form-item label="通知主题" prop="task_name" required>
              <el-input v-model="currentNoticeTask.task_name" :disabled="currentNoticeTask.task_status != '新建中'" />
            </el-form-item>
            <el-form-item label="描述" required prop="task_desc">
              <el-input v-model="currentNoticeTask.task_desc" :disabled="currentNoticeTask.task_status != '新建中'" />
            </el-form-item>
            <el-form-item label="通知类型" required prop="notice_type">
              <el-select v-model="currentNoticeTask.notice_type" :disabled="currentNoticeTask.task_status != '新建中'">
                <el-option value="站内信" label="站内信" />
                <el-option value="邮件" label="邮件" />
              </el-select>
            </el-form-item>
            <el-form-item label="立刻运行" prop="run_now">
              <el-checkbox v-model="currentNoticeTask.run_now" :disabled="currentNoticeTask.task_status != '新建中'" />
            </el-form-item>
            <el-form-item v-if="!currentNoticeTask.run_now" label="计划开始时间" prop="plan_begin_time">
              <el-date-picker
                v-model="currentNoticeTask.plan_begin_time"
                type="datetime"
                placeholder="选择日期时间"
                :disabled="currentNoticeTask.task_status != '新建中' || currentNoticeTask.run_now"
                style="width: 100%"
              />
            </el-form-item>
            <el-form-item v-if="!currentNoticeTask.run_now" label="计划完成时间" prop="plan_finish_time">
              <el-date-picker
                v-model="currentNoticeTask.plan_finish_time"
                type="datetime"
                placeholder="选择日期时间"
                :disabled="currentNoticeTask.task_status != '新建中' || currentNoticeTask.run_now"
                style="width: 100%"
              />
            </el-form-item>
            <el-form-item label="任务事务大小" prop="task_instance_batch_size">
              <el-input-number
                v-model="currentNoticeTask.task_instance_batch_size"
                :min="1"
                :max="1000"
                :step="10"
                :disabled="currentNoticeTask.task_status != '新建中'"
              />
            </el-form-item>
            <el-form-item label="通知模板(html)" required prop="notice_template">
              <el-row style="width: 100%">
                <el-col :span="10">
                  <div class="std-middle-box">
                    <el-input
                      v-model="currentNoticeTask.notice_template"
                      type="textarea"
                      :rows="12"
                      :disabled="currentNoticeTask.task_status != '新建中'"
                      @blur="checkHtmlValid"
                    />
                  </div>
                </el-col>
                <el-col :span="4">
                  <div class="std-middle-box">
                    <el-text> 预览区域 </el-text>
                  </div>
                </el-col>
                <el-col :span="10">
                  <div id="preview-area">
                    <div v-if="currentNoticeTemplateValid" v-html="currentNoticeTask.notice_template" />
                    <div v-else>
                      <el-text>模板内容不合法</el-text>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </el-form-item>
            <el-form-item label="通知范围(取并集)" prop="notice_params">
              <div id="notice-area">
                <el-checkbox-group
                  v-model="areaShortcut"
                  :disabled="currentNoticeTask.task_status != '新建中'"
                  @change="handleNoticeAreaChange"
                >
                  <el-checkbox label="所有用户" value="all_user" />
                  <el-checkbox label="所有企业用户" value="all_company_user" />
                  <el-checkbox label="所有个人用户" value="all_person_user" />
                  <el-checkbox
                    v-if="currentNoticeTask.notice_type == '邮件'"
                    label="所有订阅邮箱"
                    value="all_subscribe_email"
                  />
                  <el-checkbox label="指定公司" value="target_company" />
                  <el-checkbox label="指定部门" value="target_department" />
                  <el-checkbox label="指定用户" value="target_user" />
                </el-checkbox-group>

                <el-select
                  v-show="areaShortcut.includes('target_company')"
                  v-model="areaTargetCompanies"
                  multiple
                  placeholder="请搜索后选择公司"
                  :disabled="currentNoticeTask.task_status != '新建中'"
                  collapse-tags
                  clearable
                  :remote-method="searchCompany"
                  remote
                  filterable
                  value-key="id"
                  :max-collapse-tags="3"
                  @change="handleNoticeCompanyChange"
                >
                  <el-option
                    v-for="item in areaCompanyOptions"
                    :key="item.id"
                    :label="item.company_name"
                    :value="item"
                  />
                </el-select>
                <el-select
                  v-show="areaShortcut.includes('target_department')"
                  v-model="areaTargetDepartments"
                  multiple
                  placeholder="请搜索后选择部门"
                  :disabled="currentNoticeTask.task_status != '新建中'"
                  collapse-tags
                  clearable
                  :remote-method="searchDepartment"
                  remote
                  filterable
                  value-key="id"
                  :max-collapse-tags="3"
                  @change="handleNoticeDepartmentChange"
                >
                  <el-option
                    v-for="item in areaDepartmentOptions"
                    :key="item.id"
                    :label="item.department_name"
                    :value="item"
                  />
                </el-select>
                <el-select
                  v-show="areaShortcut.includes('target_user')"
                  v-model="areaTargetUsers"
                  multiple
                  placeholder="请搜索后选择用户"
                  :disabled="currentNoticeTask.task_status != '新建中'"
                  collapse-tags
                  clearable
                  :remote-method="searchUser"
                  remote
                  filterable
                  :max-collapse-tags="3"
                  value-key="user_id"
                  @change="handleNoticeUserChange"
                >
                  <el-option
                    v-for="item in areaUserOptions"
                    :key="item.user_id"
                    :label="item.user_nick_name"
                    :value="item"
                  />
                </el-select>
              </div>
            </el-form-item>
          </el-form>
          <el-divider> 通知实例列表 </el-divider>
          <el-scrollbar>
            <div style="width: 100%; max-height: 600px">
              <el-table :data="currentTaskInstances" stripe>
                <el-table-column type="selection" width="55" />
                <el-table-column prop="id" label="通知ID" sortable />
                <el-table-column prop="receive_user_id" label="用户ID" sortable />
                <el-table-column prop="task_celery_id" label="celery-ID" sortable min-width="240px" />
                <el-table-column prop="notice_type" label="通知类型" sortable />
                <el-table-column prop="notice_status" label="通知状态" sortable>
                  <template #default="{ row }">
                    <el-tag v-if="row.notice_status === '新建中'" type="info">新建中</el-tag>
                    <el-tag v-else-if="row.notice_status === '待执行'" type="info">待执行</el-tag>
                    <el-tag v-else-if="row.notice_status === '执行中'" type="primary">执行中</el-tag>
                    <el-tag v-else-if="row.notice_status === '成功'" type="success">成功</el-tag>
                    <el-tag v-else-if="row.notice_status === '已暂停'" type="warning">已暂停</el-tag>
                    <el-tag v-else-if="row.notice_status === '已终止'" type="danger">已终止</el-tag>
                    <el-tag v-else-if="row.notice_status === '异常'" type="danger">异常</el-tag>
                    <el-tag v-else type="primary">
                      {{ row.notice_status }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="create_time" label="通知时间" sortable min-width="200px" />
                <el-table-column prop="update_time" label="更新时间" sortable min-width="200px" />
                <el-table-column fixed label="操作" min-width="200px">
                  <template #default="{ row }">
                    <el-button v-if="!['已通知', '排队中'].includes(row.notice_status)" disabled type="primary">
                      重发
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-scrollbar>
        </div>
      </el-scrollbar>
    </el-main>
    <el-footer />
  </el-container>
</template>

<style scoped>
.std-middle-box {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
#detail-header-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  height: 100%;
  width: calc(100% - 32px);
  padding: 16px;
}
#detail-header-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  height: 100%;
  width: 100%;
}
#detail-header-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  height: 100%;
  width: 100%;
}
#notice-detail-area {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
#preview-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border: 1px solid #ddd; /* 边框颜色和宽度 */
  border-radius: 4px; /* 圆角 */

  background-color: #f9f9f9; /* 背景色 */
}
#notice-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}
</style>
