<script setup lang="ts">
import { Check, Close, Search } from '@element-plus/icons-vue';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';
import { defineProps, watch, ref, onMounted } from 'vue';
import {
  accessAuthor,
  accessSearch,
  publishSearch,
  accessUnAuthor,
  runningStatus,
  publishExport
} from '@/api/app-center-api';
import { getAllCompany, searchDepartments } from '@/api/dashboard';
import { adminSearchUserAPI, twadminSearchUser } from '@/api/user-manage';
import router from '@/router';
import { useUserInfoStore } from '@/stores/user-info-store';
const prop = defineProps({
  appCode: {
    type: String,
    default: ''
  },
  viewTab: {
    type: String,
    default: 'history'
  },
  accessType: {
    type: String,
    default: 'user'
  }
});
interface IAppPublishRecord {
  id: number;
  app_code: string;
  publish_code: string;
  publish_config: string;
  publish_desc?: string;
  publish_name: string;
  publish_status: string;
  publish_version: number;
  create_time: string;
  update_time: string;
  user_id: number;
  workflow_code?: string;
  [property: string]: any;
}
const currentViewType = ref('history');
const currentAppCode = ref('');
const currentPublishList = ref<IAppPublishRecord[]>([]);
const currentPageNum = ref(1);
const currentPageSize = ref(50);
const currentTotal = ref(0);
const accessUsers = ref<any[]>([]);
const accessObjectKeyword = ref('');
const allAccessUser = ref(false);
const accessDepartments = ref<any[]>([]);
const accessCompanies = ref<any[]>([]);
const currentAccessPageNum = ref(1);
const currentAccessPageSize = ref(50);
const currentAccessTotal = ref(0);
const currentAccessObject = ref('user');
const userInfoStore = useUserInfoStore();
const showAccessBatchFlag = ref(false);
const showAccessBatchTitle = ref('');
const showAccessBatchSubTitle = ref('');
const showSearchNewUser = ref(false);
const searchNewUserData = ref([]);
const searchNewUserKeyword = ref('');
const searchNewUserLoading = ref(false);
const searchNewUserTotal = ref(0);
const searchNewUserPageNum = ref(1);
const searchNewUserPageSize = ref(100);
const searchNewUserRef = ref(null);
const showSearchNewDepartment = ref(false);
const searchNewDepartmentData = ref([]);
const searchNewDepartmentKeyword = ref('');
const searchNewDepartmentLoading = ref(false);
const searchNewDepartmentTotal = ref(0);
const searchNewDepartmentPageNum = ref(1);
const searchNewDepartmentPageSize = ref(100);
const searchNewDepartmentRef = ref(null);
const showSearchNewCompany = ref(false);
const searchNewCompanyData = ref([]);
const searchNewCompanyLoading = ref(false);
const searchNewCompanyRef = ref(null);
const currentTimeRange = ref(60 * 24);
let userCountGraph = null;
let sessionCountGraph = null;
let qaCountGraph = null;
let attachmentCountGraph = null;
async function handlePageChange(pageNum: number): Promise<void> {
  currentPageNum.value = pageNum;
  refreshPublishList();
}
async function handlePageSizeChange(pageSize: number): Promise<void> {
  currentPageSize.value = pageSize;
  refreshPublishList();
}
async function refreshPublishList() {
  const params = {
    app_code: currentAppCode.value,
    page_num: currentPageNum.value,
    page_size: currentPageSize.value
  };
  const res = await publishSearch(params);
  if (!res.error_status) {
    currentPublishList.value = res.result.data;
    currentTotal.value = res.result.total;
  }
}
async function handleChangeModel(tabName: string) {
  router.replace({
    query: {
      ...router.currentRoute.value.query,
      viewTab: tabName,
      accessType: currentAccessObject.value
    }
  });
}
async function refreshAccess() {
  const params = {
    app_code: currentAppCode.value,
    access_object: currentAccessObject.value,
    access_keyword: accessObjectKeyword.value,
    page_num: currentAccessPageNum.value,
    page_size: currentAccessPageSize.value
  };
  const res = await accessSearch(params);
  if (!res.error_status) {
    if (currentAccessObject.value == 'user') {
      accessUsers.value = res.result.data;
      let findFlag = false;
      for (let access of accessUsers.value) {
        if (access.user_id == -1) {
          findFlag = true;
        }
      }
      allAccessUser.value = findFlag;
    } else if (currentAccessObject.value == 'department') {
      accessDepartments.value = res.result.data;
    } else if (currentAccessObject.value == 'company') {
      accessCompanies.value = res.result.data;
    }
    currentAccessTotal.value = res.result.total;
    currentAccessPageNum.value = res.result.page_num;
    currentAccessPageSize.value = res.result.page_size;
  }
}
async function handleAccessPageChange(pageNum: number): Promise<void> {
  currentAccessPageNum.value = pageNum;
  refreshAccess();
}
async function handleAccessPageSizeChange(pageSize: number): Promise<void> {
  currentAccessPageSize.value = pageSize;
  refreshAccess();
}
async function handleAccessObjectChange(tabName: string) {
  currentAccessObject.value = tabName;
  refreshAccess();
  router.replace({
    query: {
      ...router.currentRoute.value.query,
      viewTab: currentViewType.value,
      accessType: currentAccessObject.value
    }
  });
}
async function handleAccessBatchSwitch() {
  showAccessBatchFlag.value = true;
  if (currentAccessObject.value == 'user') {
    if (allAccessUser.value) {
      showAccessBatchTitle.value = '取消授权给全部平台用户';
      showAccessBatchSubTitle.value = '确认取消此应用给全部平台用户的使用权限？请谨慎操作！';
    } else {
      showAccessBatchTitle.value = '应用授权给全部平台用户';
      showAccessBatchSubTitle.value = '确认将此应用授权给全部平台用户？请谨慎操作！';
    }
  }
  return false;
}
async function changeAccessBatchStatus() {
  if (currentAccessObject.value == 'user') {
    if (allAccessUser.value) {
      // 取消授权
      const res = await accessUnAuthor({
        app_code: currentAppCode.value,
        user_list: [-1]
      });
      if (!res.error_status) {
        allAccessUser.value = false;
        ElMessage.success('取消授权成功！');
        refreshAccess();
      }
    } else {
      // 授权
      const res = await accessAuthor({
        app_code: currentAppCode.value,
        user_list: [-1]
      });
      if (!res.error_status) {
        allAccessUser.value = true;
        ElMessage.success('授权成功！');
      }
    }
  }
  showAccessBatchFlag.value = false;
}
async function removeUserAccess(userId: number) {
  const res = await accessUnAuthor({
    app_code: currentAppCode.value,
    user_list: [userId]
  });
  if (!res.error_status) {
    ElMessage.success('取消授权成功！');
    refreshAccess();
  }
}
async function closeSearchNewUser() {
  showSearchNewUser.value = false;
}
async function searchNewAccessUser() {
  const params = {
    is_archive: 0,
    search_text: searchNewUserKeyword.value,
    page_num: searchNewUserPageNum.value,
    page_size: searchNewUserPageSize.value
  };
  searchNewUserLoading.value = true;
  let res = null;
  if (userInfoStore.userInfo?.user_role?.includes('next_console_admin')) {
    res = await twadminSearchUser(params);
  } else {
    res = await adminSearchUserAPI(params);
  }
  if (res && !res?.error_status) {
    searchNewUserData.value = res.result.data;
    searchNewUserTotal.value = res.result.total;
  } else {
    searchNewUserData.value = [];
    searchNewUserTotal.value = 0;
  }
  searchNewUserLoading.value = false;
}
async function addNewUserAccess() {
  if (!searchNewUserRef.value) {
    return;
  }
  const selectNewUser = searchNewUserRef.value?.getSelectionRows();
  if (!selectNewUser || selectNewUser.length == 0) {
    ElMessage.info('请至少选择一个用户！');
    return;
  }
  const authorRes = await accessAuthor({
    app_code: currentAppCode.value,
    user_list: selectNewUser.map((item: any) => item?.user_id)
  });
  if (!authorRes.error_status) {
    ElMessage.success('授权成功！');
    refreshAccess();
  }
  showSearchNewUser.value = false;
}
async function handleNewUserPageChange(pageNum: number) {
  searchNewUserPageNum.value = pageNum;
  searchNewAccessUser();
}
async function handleNewUserPageSizeChange(pageSize: number) {
  searchNewUserPageSize.value = pageSize;
  searchNewAccessUser();
}
async function removeDepartmentAccess(departmentId: number) {
  const res = await accessUnAuthor({
    app_code: currentAppCode.value,
    department_list: [departmentId]
  });
  if (!res.error_status) {
    ElMessage.success('取消授权成功！');
    refreshAccess();
  }
}
async function searchNewAccessDepartment() {
  searchNewDepartmentLoading.value = true;
  const searchRes = await searchDepartments({
    search_text: searchNewDepartmentKeyword.value,
    page_num: searchNewDepartmentPageNum.value,
    page_size: searchNewDepartmentPageSize.value
  });
  if (!searchRes.error_status) {
    searchNewDepartmentData.value = searchRes.result.data;
    searchNewDepartmentTotal.value = searchRes.result.total;
  } else {
    searchNewDepartmentData.value = [];
    searchNewDepartmentTotal.value = 0;
  }
  searchNewDepartmentLoading.value = false;
}
async function handleNewDepartmentPageSizeChange(pageSize: number) {
  searchNewDepartmentPageSize.value = pageSize;
  searchNewAccessDepartment();
}
async function handleNewDepartmentPageChange(pageNum: number) {
  searchNewDepartmentPageNum.value = pageNum;
  searchNewAccessDepartment();
}
async function addNewDepartmentAccess() {
  if (!searchNewDepartmentRef.value) {
    return;
  }
  const selectNewDepartment = searchNewDepartmentRef.value?.getSelectionRows();
  if (!selectNewDepartment || selectNewDepartment.length == 0) {
    ElMessage.info('请至少选择一个部门！');
    return;
  }
  const authorRes = await accessAuthor({
    app_code: currentAppCode.value,
    department_list: selectNewDepartment.map((item: any) => item?.id)
  });
  if (!authorRes.error_status) {
    ElMessage.success('授权成功！');
    refreshAccess();
  }
}
async function removeCompanyAccess(companyId: number) {
  const res = await accessUnAuthor({
    app_code: currentAppCode.value,
    company_list: [companyId]
  });
  if (!res.error_status) {
    ElMessage.success('取消授权成功！');
    refreshAccess();
  }
}
async function SearchNewCompany() {
  showSearchNewCompany.value = true;
  searchNewCompanyLoading.value = true;
  const searchRes = await getAllCompany({});
  if (!searchRes.error_status) {
    searchNewCompanyData.value = searchRes.result;
  } else {
    searchNewCompanyData.value = [];
  }
  searchNewCompanyLoading.value = false;
}
async function addNewCompanyAccess() {
  if (!searchNewCompanyRef.value) {
    return;
  }
  const selectNewCompany = searchNewCompanyRef.value?.getSelectionRows();
  if (!selectNewCompany || selectNewCompany.length == 0) {
    ElMessage.info('请至少选择一个公司！');
    return;
  }
  const authorRes = await accessAuthor({
    app_code: currentAppCode.value,
    company_list: selectNewCompany.map((item: any) => item?.id)
  });
  if (!authorRes.error_status) {
    ElMessage.success('授权成功！');
    refreshAccess();
  }
  showSearchNewCompany.value = false;
}
async function refreshRunningStatus() {
  refreshUserCount();
  refreshSessionCount();
  refreshQACount();
  refreshAttachmentCount();
}
function getGraphSize() {
  const graphWidth = (window.innerWidth - 480) / 3;
  let graphHeight = (window.innerHeight - 333) / 3;
  if (graphHeight < 300) {
    graphHeight = 300;
  }
  return { width: graphWidth, height: graphHeight };
}
async function refreshUserCount() {
  const graphSize = getGraphSize();
  const res = await runningStatus({
    app_code: currentAppCode.value,
    index_type: 'user_count',
    time_range: currentTimeRange.value
  });
  if (!res.error_status) {
    if (!userCountGraph && document.getElementById('app-user')) {
      userCountGraph = echarts.init(document.getElementById('app-user'), null, {
        width: graphSize.width,
        height: graphSize.height
      });
    }
    userCountGraph?.setOption({
      title: {
        text: res.result.data,
        subtext: '使用用户数',
        left: 'center',
        top: 'center',
        textStyle: {
          fontSize: 60,
          fontWeight: 'bold',
          color: '#5470c6'
        }
      }
    });
  }
}
async function refreshSessionCount() {
  const graphSize = getGraphSize();
  const res = await runningStatus({
    app_code: currentAppCode.value,
    index_type: 'session_count',
    time_range: currentTimeRange.value
  });
  if (!res.error_status) {
    if (!sessionCountGraph && document.getElementById('app-session-cnt')) {
      sessionCountGraph = echarts.init(document.getElementById('app-session-cnt'), null, {
        width: graphSize.width,
        height: graphSize.height
      });
    }
    sessionCountGraph?.setOption({
      title: {
        text: res.result.data,
        subtext: '会话总数',
        left: 'center',
        top: 'center',
        textStyle: {
          fontSize: 60,
          fontWeight: 'bold',
          color: '#5470c6'
        }
      }
    });
  }
}
async function refreshQACount() {
  const graphSize = getGraphSize();
  const res = await runningStatus({
    app_code: currentAppCode.value,
    index_type: 'qa_count',
    time_range: currentTimeRange.value
  });
  if (!res.error_status) {
    if (!qaCountGraph && document.getElementById('app-qa-cnt')) {
      qaCountGraph = echarts.init(document.getElementById('app-qa-cnt'), null, {
        width: graphSize.width,
        height: graphSize.height
      });
    }
    qaCountGraph?.setOption({
      title: {
        text: res.result.data,
        subtext: '问答总数',
        left: 'center',
        top: 'center',
        textStyle: {
          fontSize: 60,
          fontWeight: 'bold',
          color: '#5470c6'
        }
      }
    });
  }
}
async function refreshAttachmentCount() {
  const graphSize = getGraphSize();
  const res = await runningStatus({
    app_code: currentAppCode.value,
    index_type: 'attachment_count',
    time_range: currentTimeRange.value
  });
  if (!res.error_status) {
    if (!attachmentCountGraph && document.getElementById('app-attachment-cnt')) {
      attachmentCountGraph = echarts.init(document.getElementById('app-attachment-cnt'), null, {
        width: graphSize.width,
        height: graphSize.height
      });
    }
    attachmentCountGraph?.setOption({
      title: {
        text: res.result.data,
        subtext: '附件总数',
        left: 'center',
        top: 'center',
        textStyle: {
          fontSize: 60,
          fontWeight: 'bold',
          color: '#5470c6'
        }
      }
    });
  }
}
async function exportTargetVersion(publishRecord: IAppPublishRecord) {
  const res = await publishExport({
    app_code: currentAppCode.value,
    publish_id: publishRecord.id
  });
  if (!res.error_status) {
    const blob = new Blob([JSON.stringify(res.result)], {
      type: 'application/json;charset=utf-8'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentAppCode.value}_${publishRecord.publish_version}.json`;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
  }
}
watch(
  () => prop.appCode,
  newVal => {
    if (newVal) {
      currentAppCode.value = newVal;
    } else {
      currentAppCode.value = '';
    }
  },
  { immediate: true }
);
watch(
  () => prop.viewTab,
  newVal => {
    if (newVal) {
      currentViewType.value = newVal;
    }
    if (currentViewType.value == 'history') {
      refreshPublishList();
    } else if (currentViewType.value == 'author') {
      refreshAccess();
    } else if (currentViewType.value == 'running') {
      refreshRunningStatus();
    }
  },
  { immediate: true }
);
onMounted(async () => {
  if (prop.accessType) {
    currentAccessObject.value = prop.accessType;
    if (currentViewType.value == 'author') {
      refreshAccess();
    }
  }
});
</script>

<template>
  <el-container>
    <el-main style="height: calc(100vh - 130px)">
      <el-tabs :model-value="currentViewType" tab-position="left" @tab-change="handleChangeModel">
        <el-tab-pane label="基本信息" name="base" />
        <el-tab-pane label="发布历史" name="history">
          <el-table :data="currentPublishList" stripe border style="width: 100%" height="calc(100vh - 230px)">
            <el-table-column prop="id" label="发布ID" width="120" sortable />
            <el-table-column prop="publish_code" label="发布编号" width="320" />
            <el-table-column prop="user_id" label="发布者" width="120" sortable />
            <el-table-column prop="publish_name" label="发布名称" width="240" sortable />
            <el-table-column prop="publish_desc" label="发布描述" min-width="180" sortable />
            <el-table-column prop="publish_version" label="发布版本" min-width="180" sortable>
              <template #default="{ row }">
                <el-tag
                  v-if="row.publish_version || row.publish_version == 0"
                  :type="row?.publish_is_prod ? 'success' : 'info'"
                >
                  {{ row.publish_version }}
                </el-tag>
                <el-tag v-else type="warning">无版本</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="publish_status" label="状态" width="120" sortable />
            <el-table-column prop="create_time" label="创建时间" width="180" sortable />
            <el-table-column prop="update_time" label="更新时间" width="180" sortable />
            <el-table-column prop="manage" label="操作" width="120" fixed>
              <template #default="{ row }">
                <el-button text type="primary" @click="exportTargetVersion(row)">导出</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="运行情况" name="running">
          <div class="running-status-condition">
            <el-form-item label="时间范围">
              <el-select v-model="currentTimeRange" @change="refreshRunningStatus">
                <el-option label="最近1小时" :value="60" />
                <el-option label="最近6小时" :value="360" />
                <el-option label="最近12小时" :value="720" />
                <el-option label="最近24小时" :value="1440" />
                <el-option label="最近7天" :value="10080" />
                <el-option label="最近30天" :value="43200" />
              </el-select>
            </el-form-item>
          </div>
          <el-scrollbar>
            <div class="running-status-area">
              <div id="app-user" class="running-graph" />
              <div id="app-session-cnt" class="running-graph" />
              <div id="app-qa-cnt" class="running-graph" />
              <div id="app-attachment-cnt" class="running-graph" />
              <div id="app-attachment" class="running-graph" />
              <div id="app-token" class="running-graph" />
              <div id="app-time" class="running-graph" />
              <div id="app-success-rate" class="running-graph" />
            </div>
          </el-scrollbar>
        </el-tab-pane>
        <el-tab-pane label="授权管理" name="author" @tab-change="handleChangeModel">
          <el-tabs
            :model-value="currentAccessObject"
            tab-position="top"
            type="border-card"
            @tab-change="handleAccessObjectChange"
          >
            <el-tab-pane label="用户授权" name="user">
              <div class="access-head-area">
                <div class="access-head-left">
                  <el-form-item label="授权给全部用户" label-position="left" style="margin-bottom: 0">
                    <el-switch
                      v-if="userInfoStore.userInfo?.user_role?.includes('next_console_admin')"
                      v-model="allAccessUser"
                      inline-prompt
                      :active-icon="Check"
                      :inactive-icon="Close"
                      :before-change="handleAccessBatchSwitch"
                    />
                  </el-form-item>
                  <el-form-item style="margin-bottom: 0">
                    <el-input
                      v-model="accessObjectKeyword"
                      :prefix-icon="Search"
                      clearable
                      placeholder="搜索已授权用户"
                      @keydown.enter.prevent="refreshAccess"
                      @click="refreshAccess"
                      @clear="refreshAccess"
                    />
                  </el-form-item>
                </div>
                <div class="access-head-right">
                  <el-button
                    type="primary"
                    @click="
                      showSearchNewUser = true;
                      searchNewAccessUser();
                    "
                  >
                    新增用户授权
                  </el-button>
                </div>
              </div>
              <el-table
                v-show="!allAccessUser"
                :data="accessUsers"
                stripe
                border
                style="width: 100%"
                height="calc(100vh - 320px)"
              >
                <el-table-column type="selection" width="55" />
                <el-table-column prop="id" label="授权ID" width="120" sortable />
                <el-table-column prop="user_id" label="用户ID" width="120" sortable />
                <el-table-column prop="user_code" label="用户编号" width="240" sortable />
                <el-table-column prop="user_nick_name" label="用户昵称" min-width="180" sortable />
                <el-table-column prop="create_time" label="创建时间" width="180" sortable />
                <el-table-column prop="update_time" label="更新时间" width="180" sortable />
                <el-table-column prop="manage" label="操作" width="180">
                  <template #default="{ row }">
                    <el-popconfirm
                      title="确认移除权限？移除后该用户无法继续使用该应用！"
                      @confirm="removeUserAccess(row.user_id)"
                    >
                      <template #reference>
                        <el-button text type="danger">取消授权</el-button>
                      </template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
              <div v-show="allAccessUser" class="access-all-area">
                <h3 class="access-all-text">此应用已经授权给平台所有用户！</h3>
              </div>
            </el-tab-pane>
            <el-tab-pane label="部门授权" name="department">
              <div class="access-head-area">
                <div class="access-head-left">
                  <el-form-item style="margin-bottom: 0">
                    <el-input
                      v-model="accessObjectKeyword"
                      :prefix-icon="Search"
                      placeholder="搜索已授权部门"
                      clearable
                      @keydown.enter.prevent="refreshAccess"
                      @click="refreshAccess"
                      @clear="refreshAccess"
                    />
                  </el-form-item>
                </div>
                <div class="access-head-right">
                  <el-button
                    type="primary"
                    @click="
                      showSearchNewDepartment = true;
                      searchNewAccessDepartment();
                    "
                  >
                    新增部门授权
                  </el-button>
                </div>
              </div>
              <el-table :data="accessDepartments" stripe border style="width: 100%" height="calc(100vh - 320px)">
                <el-table-column type="selection" width="55" />
                <el-table-column prop="id" label="授权ID" width="120" sortable />
                <el-table-column prop="department_id" label="部门ID" width="120" sortable />
                <el-table-column prop="department_code" label="部门编号" width="240" sortable />
                <el-table-column prop="department_name" label="部门名称" min-width="180" sortable />
                <el-table-column prop="department_desc" label="部门描述" min-width="180" sortable />
                <el-table-column prop="create_time" label="创建时间" width="180" sortable />
                <el-table-column prop="update_time" label="更新时间" width="180" sortable />
                <el-table-column prop="manage" label="操作" width="180">
                  <template #default="{ row }">
                    <el-popconfirm
                      title="确认移除权限？移除后该部门下所有用户无法继续使用该应用！"
                      @confirm="removeDepartmentAccess(row.department_id)"
                    >
                      <template #reference>
                        <el-button text type="danger">取消授权</el-button>
                      </template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane
              v-if="userInfoStore.userInfo?.user_role?.includes('next_console_admin')"
              label="企业授权"
              name="company"
            >
              <div class="access-head-area">
                <div class="access-head-left">
                  <el-form-item style="margin-bottom: 0">
                    <el-input
                      v-model="accessObjectKeyword"
                      :prefix-icon="Search"
                      placeholder="搜索已授权公司"
                      clearable
                      @keydown.enter.prevent="refreshAccess"
                      @click="refreshAccess"
                      @clear="refreshAccess"
                    />
                  </el-form-item>
                </div>
                <div class="access-head-right">
                  <el-button type="primary" @click="SearchNewCompany">新增公司授权</el-button>
                </div>
              </div>
              <el-table :data="accessCompanies" stripe border style="width: 100%" height="calc(100vh - 320px)">
                <el-table-column type="selection" width="55" />
                <el-table-column prop="id" label="授权ID" width="120" sortable />
                <el-table-column prop="company_id" label="公司ID" width="120" sortable />
                <el-table-column prop="company_code" label="公司编号" width="240" sortable />
                <el-table-column prop="company_name" label="公司名称" min-width="180" sortable />
                <el-table-column prop="create_time" label="创建时间" width="180" sortable />
                <el-table-column prop="update_time" label="更新时间" width="180" sortable />
                <el-table-column prop="manage" label="操作" width="180">
                  <template #default="{ row }">
                    <el-popconfirm
                      title="确认移除权限？移除后该公司下所有用户可能无法继续使用该应用！"
                      @confirm="removeCompanyAccess(row.company_id)"
                    >
                      <template #reference>
                        <el-button text type="danger">取消授权</el-button>
                      </template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
      </el-tabs>
    </el-main>
    <el-footer height="40px">
      <el-pagination
        v-show="currentViewType == 'history'"
        background
        size="small"
        layout=" total, sizes, prev, pager, next"
        :total="currentTotal"
        :page-size="currentPageSize"
        :current-page="currentPageNum"
        @update:page-size="handlePageSizeChange"
        @update:current-page="handlePageChange"
      />
      <el-pagination
        v-show="currentViewType == 'author'"
        background
        size="small"
        layout=" total, sizes, prev, pager, next"
        :total="currentAccessTotal"
        :page-size="currentAccessPageSize"
        :current-page="currentAccessPageNum"
        @update:page-size="handleAccessPageSizeChange"
        @update:current-page="handleAccessPageChange"
      />
    </el-footer>
  </el-container>
  <el-dialog v-model="showAccessBatchFlag" title="批量授权确认">
    <el-result :title="showAccessBatchTitle" icon="warning" :sub-title="showAccessBatchSubTitle" />
    <template #footer>
      <el-button text @click="showAccessBatchFlag = false">取消</el-button>
      <el-button text type="primary" @click="changeAccessBatchStatus">确认</el-button>
    </template>
  </el-dialog>
  <el-dialog v-model="showSearchNewUser" title="搜索待授权用户" width="80vw">
    <div class="search-new-user">
      <el-input
        v-model="searchNewUserKeyword"
        :prefix-icon="Search"
        placeholder="搜索待授权用户"
        clearable
        @click="searchNewAccessUser"
        @clear="searchNewAccessUser"
        @keydown.enter.prevent="searchNewAccessUser"
      />
      <el-table ref="searchNewUserRef" v-loading="searchNewUserLoading" :data="searchNewUserData" border height="40vh">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="user_id" label="用户ID" width="120" sortable />
        <el-table-column prop="user_code" label="用户编号" width="240" sortable />
        <el-table-column prop="user_nick_name" label="用户昵称" min-width="180" sortable />
        <el-table-column prop="user_email" label="用户邮箱" min-width="180" sortable />
        <el-table-column prop="user_phone" label="用户手机号" min-width="180" sortable />
      </el-table>
      <el-pagination
        background
        size="small"
        layout=" total, sizes, prev, pager, next"
        :total="searchNewUserTotal"
        :page-size="searchNewUserPageSize"
        :current-page="searchNewUserPageNum"
        @update:page-size="handleNewUserPageSizeChange"
        @update:current-page="handleNewUserPageChange"
      />
    </div>
    <template #footer>
      <el-button type="info" @click="closeSearchNewUser">取消</el-button>
      <el-popconfirm title="确认为这些用户添加权限？" @confirm="addNewUserAccess">
        <template #reference>
          <el-button type="primary">确认</el-button>
        </template>
      </el-popconfirm>
    </template>
  </el-dialog>
  <el-dialog v-model="showSearchNewDepartment" title="搜索待授权部门" width="80vw">
    <div class="search-new-user">
      <el-input
        v-model="searchNewDepartmentKeyword"
        :prefix-icon="Search"
        placeholder="搜索待授权部门"
        clearable
        @click="searchNewAccessDepartment"
        @clear="searchNewAccessDepartment"
        @keydown.enter.prevent="searchNewAccessDepartment"
      />
      <el-table
        ref="searchNewDepartmentRef"
        v-loading="searchNewDepartmentLoading"
        :data="searchNewDepartmentData"
        border
        height="40vh"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="company_id" label="公司ID" min-width="120" sortable />
        <el-table-column prop="id" label="部门ID" width="120" sortable />
        <el-table-column prop="department_code" label="部门编号" width="240" sortable />
        <el-table-column prop="department_name" label="部门名称" min-width="180" sortable />
        <el-table-column prop="department_desc" label="部门描述" min-width="180" sortable />
        <el-table-column prop="create_time" label="创建时间" width="180" sortable />
        <el-table-column prop="update_time" label="更新时间" width="180" sortable />
      </el-table>
      <el-pagination
        background
        size="small"
        layout=" total, sizes, prev, pager, next"
        :total="searchNewDepartmentTotal"
        :page-size="searchNewDepartmentPageSize"
        :current-page="searchNewDepartmentPageNum"
        @update:page-size="handleNewDepartmentPageSizeChange"
        @update:current-page="handleNewDepartmentPageChange"
      />
    </div>
    <template #footer>
      <el-button type="info" @click="searchNewDepartmentLoading = false">取消</el-button>
      <el-popconfirm title="确认为这些部门添加权限？" @confirm="addNewDepartmentAccess">
        <template #reference>
          <el-button type="primary">确认</el-button>
        </template>
      </el-popconfirm>
    </template>
  </el-dialog>
  <el-dialog v-model="showSearchNewCompany" title="搜索待授权公司" width="80vw">
    <div class="search-new-user">
      <el-table
        ref="searchNewCompanyRef"
        v-loading="searchNewCompanyLoading"
        :data="searchNewCompanyData"
        border
        height="40vh"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="公司ID" width="120" sortable />
        <el-table-column prop="company_code" label="公司编号" width="240" sortable />
        <el-table-column prop="company_name" label="公司名称" min-width="180" sortable />
        <el-table-column prop="company_desc" label="公司简介" min-width="180" sortable />
        <el-table-column prop="company_scale" label="公司规模" min-width="180" sortable />
        <el-table-column prop="company_type" label="公司类型" min-width="180" sortable />
        <el-table-column prop="company_country" label="所在国家" min-width="180" sortable />
        <el-table-column prop="company_area" label="公司地区" min-width="180" sortable />
        <el-table-column prop="company_address" label="公司地址" min-width="180" sortable />
        <el-table-column prop="company_industry" label="公司行业" min-width="180" sortable />
        <el-table-column prop="company_status" label="公司状态" min-width="180" sortable />
        <el-table-column prop="company_website" label="公司网址" min-width="180" sortable />
        <el-table-column prop="company_phone" label="公司电话" min-width="180" sortable />
        <el-table-column prop="create_time" label="创建时间" min-width="180" sortable />
        <el-table-column prop="update_time" label="更新时间" min-width="180" sortable />
      </el-table>
    </div>
    <template #footer>
      <el-button type="info" @click="showSearchNewCompany = false">取消</el-button>
      <el-popconfirm title="确认为这些用户添加权限？" @confirm="addNewCompanyAccess">
        <template #reference>
          <el-button type="primary">确认</el-button>
        </template>
      </el-popconfirm>
    </template>
  </el-dialog>
</template>

<style scoped>
#app-header-1 {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
}
.access-head-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 12px;
}
.access-all-area {
  background-color: #ffffff;
  padding: 20px;
  text-align: center;
  width: calc(100% - 40px);
  height: calc(100vh - 400px);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.access-all-text {
  color: #2c3e50;
  font-size: 1.5em;
  margin: 0;
  animation: fadeIn 1s ease-in-out;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.access-head-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}
.search-new-user {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.running-status-area {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  align-content: flex-start;
  flex-wrap: wrap;
  height: calc(100vh - 230px);
}
</style>
