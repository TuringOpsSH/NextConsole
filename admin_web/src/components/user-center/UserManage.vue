<script setup lang="ts">
import { Search, Setting } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { onMounted, ref, watch, reactive } from 'vue';

import { getAllCompany as getAllCompany, sendRequest, TRequestParams } from '@/api/dashboard';
import {
  adminArchiveUser,
  adminSearchUserAPI,
  adminUpdateRole,
  createUser,
  searchRole,
  twadminSearchUser,
  twadminUpdateRole
} from '@/api/user-manage';

import UserUploadExcel from '@/components/user-center/UserUploadExcel.vue';
import { useUserInfoStore } from '@/stores/user-info-store';
import { ICompany, IDepartment } from '@/types/contacts';
import { IUsers } from '@/types/user-center';
const userInfoStore = useUserInfoStore();
const showAddUserDialogFlag = ref(false);
const showUpgradeDialog = ref(false);
const companyInfo = ref<{ companyName: string; companyId: string }>();
const departInfo = ref();
const companyList = ref([]);
const departList = ref([]);
const departTree = ref([]);
const userId = ref('');
const showAddUserForm = ref(false);
interface IUser {
  user_name: string;
  user_nickname: string;
  user_phone: string;
  user_email: string;
  user_password: string;
  user_gender: string;
  user_resource_limit: number;
  user_position: string;
  user_company_id: number;
  user_department_id: number;
}
const newUserForm = reactive<IUser>({
  user_name: '',
  user_nickname: '',
  user_phone: '',
  user_email: '',
  user_password: '',
  user_gender: '男',
  user_position: '工程师',
  user_resource_limit: 20480,
  user_company_id: null,
  user_department_id: null
});
const newUserFormRef = ref(null);
const newUserRules = {
  user_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
  ],
  user_phone: [{ pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }],
  user_email: [{ type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }]
};
const createLoading = ref(false);
const userRoleList = ref([]);
interface IDepartTree {
  value: string;
  label: string;
  children: IDepartTree[];
}

const CurrentUserTotal = ref(0);
const CurrentUserPageSize = ref(100);
const CurrentUserPageNum = ref(1);
const userAccountType = ref([]);
const userAccountTypeList = ref<string[]>([]);
const userTableData = ref<IUsers[]>([]);
const userIsArchive = ref(0);
const userCompany = ref<ICompany[]>([]);
const userCompanyList = ref<ICompany[]>([]);
const userDepartment = ref([]);
const userDepartmentList = ref<IDepartment[]>([]);
const userRole = ref([]);
const userRegisterTimeRange = ref('');
const userSearchText = ref('');
const adminChangeRoleConfirm = ref(false);
const targetUser = ref<IUsers>();
const loading = ref(false);
const targetArchive = ref(false);
const registerTimeRangeShortCuts = [
  {
    text: '上周',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
      return [start, end];
    }
  },
  {
    text: '上个月',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
      return [start, end];
    }
  },
  {
    text: '上季度',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
      return [start, end];
    }
  }
];
const viewField = ref([
  '用户ID',
  '用户编号',
  '用户昵称',
  '用户头像',
  '账户类型',
  '部门',
  '公司',
  '手机',
  '邮箱',
  '用户角色',
  '用户归档'
]);

async function getCompanyInfo() {
  const res = await getAllCompany({});
  if (!res.error_status) {
    companyList.value = res.result;
  }
}

function buildDepartTree(data: any[]): IDepartTree[] {
  // 创建哈希映射表
  const map = new Map<string, IDepartTree>();

  // 第一次遍历：创建所有节点的映射
  data.forEach(item => {
    map.set(item.id.toString(), {
      value: item.id.toString(),
      label: item.department_name,
      children: []
    });
  });

  // 第二次遍历：建立父子关系
  const tree: IDepartTree[] = [];
  data.forEach(item => {
    const currentNode = map.get(item.id.toString())!;

    if (item.parent_department_id === null) {
      tree.push(currentNode);
    } else {
      const parentNode = map.get(item.parent_department_id.toString());
      parentNode?.children.push(currentNode);
    }
  });

  return tree;
}

async function getDepartInfo() {
  const params: TRequestParams = {
    url: 'lookupbyadmin',
    company_id: ''
  };
  if (userInfoStore.userInfo?.user_role?.includes('next_console_admin')) {
    params.url = 'lookupbytwadmin';
  }

  const res = await sendRequest(params);
  if (!res.error_status) {
    departList.value = res.result?.data ?? [];
    departTree.value = buildDepartTree(departList.value);
  }
}

async function handleUpgrade(row: any) {
  userId.value = row.user_id;
  await getCompanyInfo();
  await getDepartInfo();
  showUpgradeDialog.value = true;
}

async function submitForm() {
  if (!companyInfo.value) {
    ElMessage.error('请选择企业名称');
    return;
  }
  if (!departInfo.value) {
    ElMessage.error('请选择所属部门');
    return;
  }
  const params: TRequestParams = {
    url: 'updateuseraccounttypeadmin',
    update_user_id: userId.value,
    user_account_type: '企业账号',
    dest_company_id: companyInfo.value?.companyId,
    dest_department_id: departInfo.value
  };
  const res = await sendRequest(params);
  if (!res.error_status) {
    ElMessage.success('升级成功');
    clearCompanyInfo();
    showUpgradeDialog.value = false;
    await adminSearchUser();
  }
}

function resetForm() {
  clearCompanyInfo();
  showUpgradeDialog.value = false;
}

function clearCompanyInfo() {
  companyInfo.value = undefined;
  departInfo.value = undefined;
  departTree.value = [];
}

async function showAddUserFormFunc() {
  if (userInfoStore.userInfo?.user_role?.includes('next_console_admin')) {
    await getCompanyInfo();
  }
  showAddUserForm.value = true;
  newUserForm.user_company_id = userInfoStore.userInfo.user_company_id;
  await getDepartInfo();
}
async function changeNewUserCompany(newVal) {
  departInfo.value = undefined;
  const data = departList.value.filter(item => item.company_id === newVal);
  departTree.value = buildDepartTree(data);
}
async function addNewUser() {
  const res = await newUserFormRef.value?.validate();
  if (!res) {
    return;
  }
  createLoading.value = true;
  const addRes = await createUser(newUserForm);
  createLoading.value = false;
  if (!addRes.error_status) {
    ElMessage.success('添加用户成功');
    // 重置表单
    showAddUserForm.value = false;
    newUserForm.user_name = '';
    newUserForm.user_nickname = '';
    newUserForm.user_phone = '';
    newUserForm.user_email = '';
    newUserForm.user_password = '';
    newUserForm.user_gender = '男';
    newUserForm.user_resource_limit = 2048;
    newUserForm.user_position = '工程师';
    newUserForm.user_company_id = userInfoStore.userInfo?.user_company_id;
    newUserForm.user_department_id = null;
    // 刷新数据
    await adminSearchUser();
  }
}
function checkRoleChangeAvailable(row) {
  // 如果是个人账号，且当前用户不是超级管理员，则不允许修改角色
  if (row.user_account_type === '个人账号') {
    return true;
  }
  if (
    !userInfoStore.userInfo?.user_role?.includes('next_console_admin') &&
    !userInfoStore.userInfo?.user_role?.includes('super_admin')
  ) {
    return true;
  }
  if (
    (row.user_role_list?.includes('平台管理员') || row.user_role_list?.includes('超级管理员')) &&
    !userInfoStore.userInfo?.user_role?.includes('next_console_admin')
  ) {
    return true;
  }
  return false;
}
async function showAddUserDialog() {
  showAddUserDialogFlag.value = true;
}
async function getAllRoleOptions() {
  const params = {
    fetch_all: true
  };
  const res = await searchRole(params);
  if (!res.error_status) {
    userRoleList.value = [];
    if (res.result.cnt == res.result.data.length) {
      for (let i = 0; i < res.result.data.length; i++) {
        userRoleList.value.push(res.result.data[i].role_desc);
      }
    }
  }
}
async function handleUserArchiveChange() {
  const params = {
    update_user_id: targetUser.value.user_id,
    orig_is_archive: targetUser.value.is_archive ? 0 : 1,
    dest_is_archive: targetUser.value.is_archive ? 1 : 0
  };
  const res = await adminArchiveUser(params);
  if (!res.error_status) {
    ElMessage.success('操作成功');
    adminChangeRoleConfirm.value = false;
    await adminSearchUser();
  }
}
async function handleUserCurrentChange(val: number) {
  CurrentUserPageNum.value = val;
  await adminSearchUser();
}
async function handleUserRoleChange(user: IUsers) {
  const params = {
    update_user_id: user.user_id,
    dest_role_desc: user.user_role_list
  };
  if (userInfoStore.userInfo.user_role.includes('next_console_admin')) {
    const res = await twadminUpdateRole(params);
    if (!res.error_status) {
      ElMessage.success('操作成功');
      user.user_role_list = res.result;
    } else {
      await TWAdminSearchUser();
    }
    return;
  }
  const res = await adminUpdateRole(params);
  if (!res.error_status) {
    ElMessage.success('操作成功');
    user.user_role_list = res.result;
    return;
  } else {
    await adminSearchUser();
  }
}
async function handleUserSizeChange(val: number) {
  CurrentUserPageSize.value = val;
  await adminSearchUser();
}
async function adminSearchUser() {
  if (userInfoStore.userInfo?.user_role?.includes('next_console_admin')) {
    await TWAdminSearchUser();
    return;
  }
  const params = {
    page_size: CurrentUserPageSize.value,
    page_num: CurrentUserPageNum.value
  };
  if ([0, 1].includes(userIsArchive.value)) {
    params['is_archive'] = userIsArchive.value;
  }
  if (userDepartment.value) {
    params['user_department_id'] = userDepartment.value;
  }
  if (userRole.value?.length) {
    params['role_desc'] = userRole.value;
  }
  if (userRegisterTimeRange.value !== '') {
    params['register_start_date'] = formatDateToUTC8(userRegisterTimeRange.value[0]);
    params['register_end_date'] = formatDateToUTC8(userRegisterTimeRange.value[1]);
  }
  if (userSearchText.value !== '') {
    params['search_text'] = userSearchText.value;
  }
  loading.value = true;
  const res = await adminSearchUserAPI(params);
  if (!res.error_status) {
    userTableData.value = res.result?.data;
    userDepartmentList.value = [];
    for (let i = 0; i < res.result?.user_departments.length; i++) {
      if (res.result.user_departments[i]) {
        userDepartmentList.value.push(res.result.user_departments[i]);
      }
    }
    CurrentUserTotal.value = res.result.total;
    for (let i = 0; i < res.result.data.length; i++) {
      if (res.result.data[i].role_desc) {
        userTableData.value[i].user_role_list = res.result.data[i].role_desc.split(',');
      }
      if (res.result.data[i].is_archive === 1) {
        userTableData.value[i].is_archive = true;
      } else {
        userTableData.value[i].is_archive = false;
      }
    }
  }
  loading.value = false;
}
async function TWAdminSearchUser() {
  const params = {
    page_size: CurrentUserPageSize.value,
    page_num: CurrentUserPageNum.value
  };
  if (userAccountType.value?.length) {
    params['user_account_type'] = userAccountType.value;
  }
  if ([0, 1].includes(userIsArchive.value)) {
    params['is_archive'] = userIsArchive.value;
  }
  if (userCompany.value?.length) {
    params['user_company_id'] = userCompany.value;
  }
  if (userDepartment.value?.length) {
    params['user_department_id'] = userDepartment.value;
  }
  if (userRole.value?.length) {
    params['role_desc'] = userRole.value;
  }
  if (userRegisterTimeRange.value?.length) {
    params['register_start_date'] = formatDateToUTC8(userRegisterTimeRange.value[0]);
    params['register_end_date'] = formatDateToUTC8(userRegisterTimeRange.value[1]);
  }
  if (userSearchText.value !== '') {
    params['search_text'] = userSearchText.value;
  }
  loading.value = true;
  const res = await twadminSearchUser(params);
  if (!res.error_status) {
    userTableData.value = res.result.data;
    userAccountTypeList.value = [];
    for (let i = 0; i < res.result.user_account_type.length; i++) {
      if (res.result.user_account_type[i]) {
        userAccountTypeList.value.push(res.result.user_account_type[i]);
      }
    }
    userDepartmentList.value = [];
    for (let i = 0; i < res.result.user_departments.length; i++) {
      if (res.result.user_departments[i]) {
        userDepartmentList.value.push(res.result.user_departments[i]);
      }
    }
    userCompanyList.value = [];
    for (let i = 0; i < res.result.user_companies.length; i++) {
      if (res.result.user_companies[i]) {
        userCompanyList.value.push(res.result.user_companies[i]);
      }
    }

    CurrentUserTotal.value = res.result.total;

    for (let i = 0; i < res.result.data.length; i++) {
      if (res.result.data[i].role_desc) {
        try {
          userTableData.value[i].user_role_list = res.result.data[i].role_desc.split(',');
        } catch (e) {
          console.log(e, res.result.data[i].role_desc);
        }
      }
    }
  }
  loading.value = false;
}
function formatDateToUTC8(date) {
  return new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
    .format(date)
    .replace(/\//g, '-')
    .replace(/,/g, '');
}

onMounted(async () => {
  await adminSearchUser();
  await getAllRoleOptions();
});
watch(
  () => companyInfo.value,
  newVal => {
    departInfo.value = undefined;
    const data = departList.value.filter(item => item.company_id === newVal?.companyId);
    departTree.value = buildDepartTree(data);
  }
);
</script>

<template>
  <el-container style="height: calc(100vh - 60px)">
    <el-main>
      <div style="height: calc(100vh - 170px)">
        <el-scrollbar>
          <div
            class="next-console-div"
            style="
              flex-direction: row;
              justify-content: space-between;
              border-bottom: 1px solid #d0d5dd;
              padding: 12px 16px;
            "
          >
            <div class="next-console-div" style="width: 60px">
              <el-text class="next-console-font-bold" style="width: 60px; color: #101828"> 用户列表</el-text>
            </div>
            <div class="next-console-div">
              <div v-if="userInfoStore.userInfo.user_role.includes('next_console_admin')">
                <el-select
                  v-model="userAccountType"
                  style="width: 100px"
                  multiple
                  clearable
                  placeholder="账户类型"
                  @change="adminSearchUser"
                >
                  <el-option
                    v-for="(accountType, idx) in userAccountTypeList"
                    :key="idx"
                    :value="accountType"
                    :label="accountType"
                  />
                </el-select>
              </div>
              <div v-if="userInfoStore.userInfo.user_role.includes('next_console_admin')">
                <el-select
                  v-model="userCompany"
                  style="width: 100px"
                  value-key="id"
                  multiple
                  clearable
                  placeholder="所属公司"
                  @change="adminSearchUser"
                >
                  <el-option
                    v-for="(company, idx) in userCompanyList"
                    :key="idx"
                    :value="company.id"
                    :label="company.company_name"
                  />
                </el-select>
              </div>
              <div>
                <el-select
                  v-model="userIsArchive"
                  style="width: 100px"
                  clearable
                  placeholder="归档状态"
                  @change="adminSearchUser"
                >
                  <el-option :value="1" label="归档" />
                  <el-option :value="0" label="未归档" />
                </el-select>
              </div>
              <div>
                <el-select
                  v-model="userDepartment"
                  style="width: 100px"
                  value-key="id"
                  multiple
                  clearable
                  placeholder="所属部门"
                  @change="adminSearchUser"
                >
                  <el-option
                    v-for="(department, idx) in userDepartmentList"
                    :key="idx"
                    :value="department.id"
                    :label="department.department_name"
                  />
                </el-select>
              </div>
              <div>
                <el-select
                  v-model="userRole"
                  style="width: 100px"
                  multiple
                  clearable
                  placeholder="拥有角色"
                  @change="adminSearchUser"
                >
                  <el-option v-for="(role, idx) in userRoleList" :key="idx" :value="role" :label="role" />
                </el-select>
              </div>
              <div style="width: 380px">
                <el-date-picker
                  v-model="userRegisterTimeRange"
                  style="width: 350px"
                  type="datetimerange"
                  :shortcuts="registerTimeRangeShortCuts"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="截止时间"
                  @change="adminSearchUser"
                />
              </div>
              <div style="width: 200px">
                <el-input
                  v-model="userSearchText"
                  placeholder="可搜索用户ID,昵称,手机"
                  :prefix-icon="Search"
                  clearable
                  @change="adminSearchUser"
                />
              </div>
              <div>
                <el-popover trigger="click" placement="bottom" width="300">
                  <template #reference>
                    <el-button size="small" :icon="Setting" circle />
                  </template>
                  <el-checkbox-group v-model="viewField">
                    <el-checkbox
                      v-for="item in [
                        '用户ID',
                        '用户编号',
                        '用户姓名',
                        '用户昵称',
                        '用户头像',
                        '账户类型',
                        '部门',
                        '公司',
                        '注册时间',
                        '上次登录时间',
                        '手机',
                        '邮箱',
                        '微信id',
                        '用户角色',
                        '用户归档'
                      ]"
                      :key="item"
                      :value="item"
                    >
                      {{ item }}
                    </el-checkbox>
                  </el-checkbox-group>
                </el-popover>
              </div>
              <div>
                <el-dropdown trigger="click" size="small">
                  <div class="user-add-area">
                    <el-image src="/images/user_plus_white.svg" style="width: 20px; height: 20px" />
                  </div>
                  <template #dropdown>
                    <el-dropdown-item @click="showAddUserFormFunc">添加用户</el-dropdown-item>
                    <el-dropdown-item @click="showAddUserDialog">批量导入用户</el-dropdown-item>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>
          <div class="next-console-div">
            <el-table :data="userTableData" stripe border element-loading-text="加载中" height="calc(100vh - 240px)">
              <el-table-column type="selection" width="55" />
              <el-table-column v-if="viewField.includes('用户ID')" prop="user_id" label="用户ID" sortable width="100" />
              <el-table-column
                v-if="viewField.includes('用户编号')"
                prop="user_code"
                label="用户编号"
                sortable
                width="300"
              />
              <el-table-column
                v-if="viewField.includes('用户姓名')"
                prop="user_name"
                label="用户姓名"
                sortable
                width="110"
              />
              <el-table-column
                v-if="viewField.includes('用户昵称')"
                prop="user_nick_name"
                label="用户昵称"
                width="110"
              />
              <el-table-column v-if="viewField.includes('用户头像')" prop="user_avatar" label="用户头像" width="110">
                <template #default="{ row }">
                  <el-avatar v-if="row.user_avatar" :src="row.user_avatar" />
                  <el-avatar v-else style="background: #d1e9ff">
                    <el-text style="font-weight: 600; color: #1570ef">
                      {{ row.user_nick_name_py }}
                    </el-text>
                  </el-avatar>
                </template>
              </el-table-column>
              <el-table-column
                v-if="userInfoStore.userInfo.user_role.includes('next_console_admin') && viewField.includes('账户类型')"
                prop="user_account_type"
                label="账户类型"
                sortable
                width="110"
              >
                <template #default="{ row }">
                  <div class="user-account-type">
                    <el-text>{{ row.user_account_type }}</el-text>
                    <el-tag v-if="row.user_account_type === '个人账号'" class="btn-upgrade" @click="handleUpgrade(row)">
                      升级
                    </el-tag>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                v-if="viewField.includes('部门')"
                prop="user_department"
                label="部门"
                sortable
                width="120"
              />
              <el-table-column
                v-if="userInfoStore.userInfo.user_role.includes('next_console_admin') && viewField.includes('公司')"
                prop="user_company"
                label="公司"
                sortable
                width="120"
              />
              <el-table-column
                v-if="viewField.includes('注册时间')"
                prop="create_time"
                label="注册时间"
                sortable
                width="120"
              />
              <el-table-column
                v-if="viewField.includes('上次登录时间')"
                prop="last_login_time"
                label="上次登录时间"
                sortable
                width="140"
              />
              <el-table-column v-if="viewField.includes('手机')" prop="user_phone" label="手机" sortable width="140" />
              <el-table-column v-if="viewField.includes('邮箱')" prop="user_email" label="邮箱" sortable width="140" />
              <el-table-column v-if="viewField.includes('微信id')" prop="user_wx_openid" label="微信id" sortable />
              <el-table-column
                v-if="viewField.includes('用户角色')"
                prop="user_role"
                label="用户角色"
                sortable
                min-width="300"
              >
                <template #default="{ row }">
                  <el-select
                    v-model="row.user_role_list"
                    multiple
                    collapse-tags
                    collapse-tags-tooltip
                    placeholder="用户角色"
                    style="width: 240px"
                    :disabled="checkRoleChangeAvailable(row)"
                    @change="handleUserRoleChange(row)"
                  >
                    <el-option
                      v-for="(item, idx) in userRoleList"
                      :key="idx"
                      class="role-desc"
                      :label="item"
                      :value="item"
                    />
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column
                v-if="viewField.includes('用户归档')"
                prop="is_archive"
                label="用户归档"
                sortable
                min-width="200px"
              >
                <template #default="{ row }">
                  <el-switch
                    v-model="row.is_archive"
                    active-color="#FF4949"
                    inactive-color="#13CE66"
                    active-text="已归档"
                    inactive-text="未归档"
                    @change="
                      adminChangeRoleConfirm = true;
                      targetUser = row;
                      targetArchive = row.is_archive;
                    "
                  />
                </template>
              </el-table-column>
            </el-table>
            <el-dialog
              v-model="adminChangeRoleConfirm"
              title="请确认当前变更操作"
              max-width="480"
              @closed="adminSearchUser"
            >
              <el-result
                v-if="targetArchive"
                title="归档用户"
                sub-title="归档用户后，该用户不可再登录使用平台，是否确认？"
                icon="error"
              />
              <el-result
                v-else
                title="解除归档"
                sub-title="解除归档用户后，该用户可再登录使用平台，是否确认？"
                icon="success"
              />
              <template #footer>
                <div class="next-console-div">
                  <div style="width: 100%">
                    <el-button style="width: 100%; background-color: #175cd3" @click="handleUserArchiveChange">
                      <el-text style="color: white"> 确认 </el-text>
                    </el-button>
                  </div>
                  <div style="width: 100%">
                    <el-button
                      style="width: 100%"
                      @click="
                        targetUser.is_archive = !targetUser.is_archive;
                        adminChangeRoleConfirm = false;
                      "
                    >
                      取消
                    </el-button>
                  </div>
                </div>
              </template>
            </el-dialog>
          </div>
        </el-scrollbar>
      </div>
      <UserUploadExcel v-model="showAddUserDialogFlag" @refresh="adminSearchUser" />
      <el-dialog v-model="showAddUserForm" title="添加用户">
        <el-form
          ref="newUserFormRef"
          v-loading="createLoading"
          :model="newUserForm"
          :rules="newUserRules"
          label-position="right"
          label-width="140px"
          element-loading-text="创建中..."
        >
          <el-form-item prop="user_name" label="用户姓名" required>
            <el-input v-model="newUserForm.user_name" placeholder="请输入用户姓名" />
          </el-form-item>
          <el-form-item prop="user_nickname" label="用户昵称">
            <el-input v-model="newUserForm.user_nickname" placeholder="请输入用户昵称" />
          </el-form-item>
          <el-form-item prop="user_phone" label="用户手机">
            <el-input v-model="newUserForm.user_phone" placeholder="请输入用户手机" />
          </el-form-item>
          <el-form-item prop="user_email" label="用户邮箱">
            <el-input v-model="newUserForm.user_email" placeholder="请输入用户邮箱" clearable />
          </el-form-item>
          <el-form-item prop="user_password" label="用户密码">
            <el-input
              v-model="newUserForm.user_password"
              placeholder="请输入用户密码"
              show-password
              type="password"
              clearable
            />
          </el-form-item>
          <el-form-item prop="user_gender" label="用户性别">
            <el-radio-group v-model="newUserForm.user_gender">
              <el-radio value="男">男</el-radio>
              <el-radio value="女">女</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item prop="user_resource_limit" label="用户资源空间(MB)">
            <el-input-number v-model="newUserForm.user_resource_limit" />
          </el-form-item>
          <el-form-item prop="user_position" label="岗位">
            <el-input v-model="newUserForm.user_position" />
          </el-form-item>
          <el-form-item
            v-if="userInfoStore.userInfo.user_role.includes('next_console_admin')"
            prop="user_company_id"
            label="所属公司"
          >
            <el-select
              v-model="newUserForm.user_company_id"
              value-key="id"
              placeholder="请选择用户所属公司"
              clearable
              :disabled="!userInfoStore.userInfo?.user_role.includes('next_console_admin')"
              @change="changeNewUserCompany"
            >
              <el-option
                v-for="company in companyList"
                :key="company.id"
                :label="company.company_name"
                :value="company.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item prop="user_department_id" label="所属部门">
            <el-tree-select
              v-model="newUserForm.user_department_id"
              :disabled="!newUserForm.user_company_id"
              :data="departTree"
              check-strictly
              :render-after-expand="false"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button text @click="showAddUserForm = false"> 取消 </el-button>
          <el-button type="primary" @click="addNewUser"> 确定 </el-button>
        </template>
      </el-dialog>
    </el-main>
    <el-footer>
      <div class="kg-pagination">
        <el-pagination
          size="small"
          layout=" total, sizes, prev, pager, next"
          :total="CurrentUserTotal"
          :page-sizes="[100, 200, 500, 1000]"
          :page-size="CurrentUserPageSize"
          :current-page="CurrentUserPageNum"
          @update:page-size="handleUserSizeChange"
          @update:current-page="handleUserCurrentChange"
        />
      </div>
    </el-footer>
  </el-container>
  <div class="upgrade-dialog">
    <el-dialog v-model="showUpgradeDialog" title="个人用户升级" center width="600px">
      <el-form label-width="120px">
        <el-form-item label="企业名称">
          <el-select
            v-model="companyInfo"
            value-key="companyId"
            placeholder="请选择"
            clearable
            style="width: 400px; height: 150px"
            @clear="clearCompanyInfo"
          >
            <el-option
              v-for="company in companyList"
              :key="company.id"
              :label="company.company_name"
              :value="{ companyName: company.company_name, companyId: company.id }"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="所属部门">
          <el-tree-select
            v-model="departInfo"
            :disabled="!companyInfo"
            :data="departTree"
            check-strictly
            :render-after-expand="false"
            style="width: 400px; height: 150px"
          />
        </el-form-item>
        <el-form-item style="height: 60px" class="btns-form-item">
          <el-button type="primary" @click="submitForm()"> 确定 </el-button>
          <el-button @click="resetForm()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<style lang="scss">
.el-header {
  --el-header-padding: 0 !important;
}
.kg-pagination {
  display: flex;
  justify-content: center;
  align-content: center;
  width: 100%;
  height: 100%;
}

.user-account-type {
  display: flex;
  gap: 6px;
  .btn-upgrade {
    height: 22px;
    cursor: pointer;
  }
}

.btns-form-item {
  margin-top: 60px;
  .el-form-item__content {
    width: 100%;
    justify-content: center;
    margin-left: 0 !important;
    gap: 10px;
  }
}

.el-dialog__header {
  margin-bottom: 40px;
}
.user-add-area {
  cursor: pointer;
  display: flex;
  flex-direction: row;
  gap: 6px;
  background: #1570ef;
  border-radius: 8px;
  padding: 8px 14px;
  border: 1px solid #1570ef;
  align-items: center;
  justify-content: center;
}
</style>
