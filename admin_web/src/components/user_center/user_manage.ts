import { format, parseISO } from 'date-fns';
import { ElMessage, genFileId } from 'element-plus';
import type { UploadInstance, UploadProps, UploadRawFile, UploadUserFile } from 'element-plus';
import { reactive, ref } from 'vue';
import {
  admin_archive_user,
  admin_search_user,
  admin_update_role,
  createUserByExcel,
  createUserByExcelTW,
  search_role,
  twadmin_search_user,
  twadmin_update_role
} from '@/api/user_manage';
import router from '@/router';
import { Company, Department } from '@/types/contacts';
import { Users } from '@/types/users';
import { handleUserName } from '@/utils/alg';
import { getInfo, getToken } from '@/utils/auth';
export const CurrentUserTotal = ref(0);
export const CurrentUserPageSize = ref(100);
export const CurrentUserPageNum = ref(1);
export const user_info = ref<Users>();
export const user_id = ref(0);
export const user_account_type = ref([]);
export const user_account_type_list = ref<string[]>([]);
export const user_table_data = ref<Users[]>([]);
export const user_is_archive = ref(0);
export const user_company = ref<Company[]>([]);
export const user_company_list = ref<Company[]>([]);
export const user_department = ref([]);
export const user_department_list = ref<Department[]>([]);
export const user_role = ref([]);
export const user_role_list = ref([]);
export const user_register_time_range = ref('');
export const registerTimeRangeShortCuts = [
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
export const user_search_text = ref('');
export const user_is_next_console_admin = ref(false);
export const user_is_next_console_reader_admin = ref(false);
export const adminChangeRoleConfirm = ref(false);
export const targetUser = ref<Users>();
export const showAddUserDialogFlag = ref(false);
export const uploadRef = ref<UploadInstance>();
export const user_excel_file_progress = ref(0);
export const user_excel_file_name = ref('待上传');
export const user_excel_file_size = ref('');
export const user_excel_file_flag = ref(false);
export const user_excel_file_status = ref('');
export const user_excel_file_result = ref('');
export const user_excel_file = ref<UploadUserFile[]>();
export const user_excel_file_result_str = ref('');
export const loading = ref(false);
export const target_archive = ref(false);
export async function adminSearchUser() {
  if (user_is_next_console_admin.value) {
    await TWAdminSearchUser();
    return;
  }
  const params = {
    page_size: CurrentUserPageSize.value,
    page_num: CurrentUserPageNum.value
  };
  if ([0, 1].includes(user_is_archive.value)) {
    params['is_archive'] = user_is_archive.value;
  }
  if (user_department.value) {
    params['user_department_id'] = user_department.value;
  }
  if (user_role.value?.length) {
    params['role_desc'] = user_role.value;
  }
  if (user_register_time_range.value !== '') {
    params['register_start_date'] = formatDateToUTC8(user_register_time_range.value[0]);
    params['register_end_date'] = formatDateToUTC8(user_register_time_range.value[1]);
  }
  if (user_search_text.value !== '') {
    params['search_text'] = user_search_text.value;
  }
  loading.value = true;
  const res = await admin_search_user(params);
  if (!res.error_status) {
    user_table_data.value = res.result.data;
    user_department_list.value = [];
    for (let i = 0; i < res.result.user_departments.length; i++) {
      if (res.result.user_departments[i]) {
        user_department_list.value.push(res.result.user_departments[i]);
      }
    }
    CurrentUserTotal.value = res.result.total;
    for (let i = 0; i < res.result.data.length; i++) {
      if (res.result.data[i].role_desc) {
        user_table_data.value[i].user_role_list = res.result.data[i].role_desc.split(',');
      }
      if (res.result.data[i].is_archive === 1) {
        user_table_data.value[i].is_archive = true;
      } else {
        user_table_data.value[i].is_archive = false;
      }

      if (res.result.data[i].reg_time) {
        try {
          user_table_data.value[i].reg_time = format_time(res.result.data[i].reg_time);
        } catch (e) {
          console.log(res.result.data[i]);
        }
      }
    }
  }
  loading.value = false;
}
export async function TWAdminSearchUser() {
  const params = {
    page_size: CurrentUserPageSize.value,
    page_num: CurrentUserPageNum.value
  };
  if (user_account_type.value?.length) {
    params['user_account_type'] = user_account_type.value;
  }
  if ([0, 1].includes(user_is_archive.value)) {
    params['is_archive'] = user_is_archive.value;
  }
  if (user_company.value?.length) {
    params['user_company_id'] = user_company.value;
  }
  if (user_department.value?.length) {
    params['user_department_id'] = user_department.value;
  }
  if (user_role.value?.length) {
    params['role_desc'] = user_role.value;
  }
  if (user_register_time_range.value?.length) {
    params['register_start_date'] = formatDateToUTC8(user_register_time_range.value[0]);
    params['register_end_date'] = formatDateToUTC8(user_register_time_range.value[1]);
  }
  if (user_search_text.value !== '') {
    params['search_text'] = user_search_text.value;
  }
  loading.value = true;
  const res = await twadmin_search_user(params);
  if (!res.error_status) {
    user_table_data.value = res.result.data;
    user_account_type_list.value = [];
    for (let i = 0; i < res.result.user_account_type.length; i++) {
      if (res.result.user_account_type[i]) {
        user_account_type_list.value.push(res.result.user_account_type[i]);
      }
    }
    user_department_list.value = [];
    for (let i = 0; i < res.result.user_departments.length; i++) {
      if (res.result.user_departments[i]) {
        user_department_list.value.push(res.result.user_departments[i]);
      }
    }
    user_company_list.value = [];
    for (let i = 0; i < res.result.user_companies.length; i++) {
      if (res.result.user_companies[i]) {
        user_company_list.value.push(res.result.user_companies[i]);
      }
    }

    CurrentUserTotal.value = res.result.total;

    for (let i = 0; i < res.result.data.length; i++) {
      if (res.result.data[i].role_desc) {
        try {
          user_table_data.value[i].user_role_list = res.result.data[i].role_desc.split(',');
        } catch (e) {
          console.log(e, res.result.data[i].role_desc);
        }
      }
    }
  }
  loading.value = false;
}
export function format_time(time: string) {
  return format(parseISO(new Date(time).toISOString()), 'yyyy-MM-dd HH:mm:ss');
}
export async function handleUserSizeChange(val: number) {
  CurrentUserPageSize.value = val;
  await adminSearchUser();
}
export async function handleUserCurrentChange(val: number) {
  CurrentUserPageNum.value = val;
  await adminSearchUser();
}
export async function checkUserPermission(): Promise<boolean> {
  // 检查用户是否有NextConsole管理员权限
  user_info.value = await getInfo(true);
  if (user_info.value.user_role.includes('next_console_admin')) {
    user_is_next_console_admin.value = true;
    return true;
  }
  if (user_info.value.user_role.includes('next_console_reader_admin')) {
    user_is_next_console_reader_admin.value = true;
    return true;
  }

  return false;
}
export async function showAddUserDialog() {
  showAddUserDialogFlag.value = true;
}
export function get_user_avatar(avatar: string) {
  // user_avatar 不存在，就使用user_name的首字母作为头像
  if (avatar === '' || avatar === null || avatar === undefined) {
    return handleUserName(avatar, 3);
  }
  if (avatar.startsWith('http')) {
    return avatar;
  }
  return import.meta.env.VITE_APP_NEXT_CONSOLE_PATH + avatar;
}
export async function handleUserRoleChange(user: Users) {
  const params = {
    update_user_id: user.user_id,
    dest_role_desc: user.user_role_list
  };
  if (user_is_next_console_admin.value) {
    const res = await twadmin_update_role(params);
    if (!res.error_status) {
      ElMessage.success('操作成功');
      user.user_role_list = res.result;

    } else {
      await TWAdminSearchUser();
    }
    return;
  }
  const res = await admin_update_role(params);
  if (!res.error_status) {
    ElMessage.success('操作成功');
    user.user_role_list = res.result;
    return;
  } else {
    await adminSearchUser();
  }
}
export async function handleUserArchiveChange() {
  const params = {
    update_user_id: targetUser.value.user_id,
    orig_is_archive: targetUser.value.is_archive ? 0 : 1,
    dest_is_archive: targetUser.value.is_archive ? 1 : 0
  };
  const res = await admin_archive_user(params);
  if (!res.error_status) {
    ElMessage.success('操作成功');
    adminChangeRoleConfirm.value = false;
    await adminSearchUser();
  }
}
export async function downloadUserTemplate() {
  if (user_is_next_console_admin.value) {
    await createUserByExcelTW({ file_name: '天问用户导入模板.xlsx' }, 'get');
    return;
  }
  await createUserByExcel({ file_name: '用户导入模板.xlsx' }, 'get');
}

export function get_upload_headers() {
  return {
    Authorization: 'Bearer ' + getToken()
  };
}

export function handleExcelExceed(files: UploadProps['onExceed']) {
  uploadRef.value.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  uploadRef.value!.handleStart(file);
}
export async function updateUserResult(response, file, fileList) {
  // 在这里处理服务器返回的结果

  user_excel_file_name.value = '';
  user_excel_file_size.value = '';
  user_excel_file_flag.value = false;
  user_excel_file_progress.value = (response.result.finished_cnt / response.result.total_cnt) * 100;
  if (user_excel_file_progress.value == 100) {
    user_excel_file_status.value = 'success';
  }
  if (user_excel_file_progress.value < 60 && user_excel_file_progress.value >= 30) {
    user_excel_file_status.value = 'warning';
  }
  if (user_excel_file_progress.value < 30) {
    user_excel_file_status.value = 'exception';
  }
  uploadRef.value.clearFiles();
  if (response.error_status) {
    user_excel_file_result.value = response.error_message;
  } else {
    user_excel_file_result.value =
      '总共导入' +
      response.result.total_cnt +
      '条数据，成功导入' +
      response.result.finished_cnt +
      '条数据，失败' +
      response.result.error_cnt +
      '条数据';
    for (let i = 0; i < response.result.trace.length; i++) {
      if (response.result.trace[i]?.error)
        user_excel_file_result.value +=
          '\n错误原因：' + response.result.trace[i]?.error + '，行号：' + response.result.trace[i]?.row_num;
    }
  }

  await adminSearchUser();
}
export function getFileInfo(file) {
  user_excel_file_name.value = file.name;
  user_excel_file_size.value = (file.size / 1024).toFixed(2) + 'KB';
  user_excel_file_flag.value = true;
}

export function uploadUserExcelFile() {
  if (typeof user_excel_file.value === 'undefined') {
    ElMessage.warning('请上传文件！');
    return false;
  }
  uploadRef.value!.submit();
  // uploadRef.value.clearFiles()
}
export async function get_all_role_options() {
  const params = {
    page_size: 100,
    page_num: 1
  };
  const res = await search_role(params);
  if (!res.error_status) {
    user_role_list.value = [];
    if (res.result.cnt == res.result.data.length) {
      for (let i = 0; i < res.result.data.length; i++) {
        user_role_list.value.push(res.result.data[i].role_desc);
      }
    } else {
      const new_params = {
        page_size: res.result.cnt,
        page_num: 1
      };
      const new_res = await search_role(new_params);
      if (!new_res.error_status) {
        for (let i = 0; i < new_res.result.data.length; i++) {
          user_role_list.value.push(new_res.result.data[i].role_desc);
        }
      }
    }
  }
}

export function triggerUpdateRole(user: Users) {
  return !!loading.value;
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
