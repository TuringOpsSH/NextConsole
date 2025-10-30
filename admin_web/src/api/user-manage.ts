import { ElMessage } from 'element-plus';
import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '';

export const api = {
  register_user: envUrl + '/next_console_admin/register',
  create_user: envUrl + '/next_console_admin/management_center/management/user/create',
  update_user: envUrl + '/next_console_admin/user_center/users/update',
  user_avatar_update: envUrl + '/next_console_admin/user_center/users/avatar/update',
  delete_user: envUrl + '/next_console_admin/user_center/users/delete',
  search_user: envUrl + '/next_console_admin/user_center/users/search',
  get_user: envUrl + '/next_console_admin/user_center/users/get',
  close_user: envUrl + '/next_console_admin/user_center/users/close',
  login_user: envUrl + '/next_console_admin/login',
  valid_token: envUrl + '/next_console_admin/valid_token',
  create_role: envUrl + '/next_console_admin/user_center/create_role',
  update_role: envUrl + '/next_console_admin/user_center/update_role',
  delete_role: envUrl + '/next_console_admin/user_center/delete_role',
  search_role: envUrl + '/next_console_admin/user_center/role/search',
  wx_register: envUrl + '/next_console_admin/wx_register',
  reset_email_password: envUrl + '/next_console_admin/reset_email_password',
  valid_reset_password_code: envUrl + '/next_console_admin/reset_password_code/valid',
  reset_new_email_url: envUrl + '/next_console_admin/reset_new_email',
  valid_reset_email_code: envUrl + '/next_console_admin/reset_email_code/valid',
  lookup_user_token_sta: envUrl + '/next_console_admin/user_center/user_token_sta/lookup',
  lookup_user_token_used_current: envUrl + '/next_console_admin/user_center/user_token_used_current/lookup',
  admin_search_user: envUrl + '/next_console_admin/management_center/management/user/lookupbyadmin',
  twadmin_search_user: envUrl + '/next_console_admin/management_center/management/user/lookupbytwadmin',
  admin_update_role: envUrl + '/next_console_admin/management_center/management/user/updateroleadmin',
  twadmin_update_role: envUrl + '/next_console_admin/management_center/management/user/updateroletwadmin',
  admin_archive_user: envUrl + '/next_console_admin/management_center/management/user/updateuserstatusadmin',
  admin_get_user_template: envUrl + '/next_console_admin/management_center/management/user/add_user_by_excel_corp',
  twadmin_get_user_template: envUrl + '/next_console_admin/management_center/management/user/add_user_by_excel_twadmin',
  admin_create_user_by_excel: envUrl + '/next_console_admin/management_center/management/user/add_user_by_excel_corp',
  twadmin_create_user_by_excel:
    envUrl + '/next_console_admin/management_center/management/user/add_user_by_excel_twadmin',
  admin_close_user: envUrl + '/next_console_admin/management_center/management/user/close',
  admin_update_user: envUrl + '/next_console_admin/management_center/management/user/update',
};

export async function createUserByExcel(params: object, method: string) {
  if (method === 'get') {
    try {
      // 使用类型断言确保返回的是 Blob 类型
      const blob: Blob = (await request({
        url: api.admin_create_user_by_excel,
        method: 'get',
        responseType: 'blob' // 确保返回的是blob类型
      })) as Blob; // 这里使用类型断言

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      // 使用断言确保file_name存在
      link.setAttribute('download', params['file_name']);
      link.href = url;
      document.body.appendChild(link);
      link.click();

      // 清理
      window.URL.revokeObjectURL(url);
      link.remove(); // 移除创建的<a>标签
    } catch (error) {
      console.error('文件下载失败', error);
      ElMessage.error('文件下载失败:' + error.toString());
    }
  }
}
export async function createUserByExcelTW(params: object, method: string) {
  if (method === 'get') {
    try {
      // 使用类型断言确保返回的是 Blob 类型
      const blob: Blob = (await request({
        url: api.twadmin_create_user_by_excel,
        method: 'get',
        params: params,
        responseType: 'blob' // 确保返回的是blob类型
      })) as Blob; // 这里使用类型断言

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      // 使用断言确保file_name存在
      link.setAttribute('download', params['file_name']);
      link.href = url;
      document.body.appendChild(link);
      link.click();

      // 清理
      window.URL.revokeObjectURL(url);
      link.remove(); // 移除创建的<a>标签
    } catch (error) {
      console.error('文件下载失败', error);
      ElMessage.error('文件下载失败:' + error.toString());
    }
  }
}
export function update_user(params: object): Promise<ServerResponse> {
  return request({
    url: api.update_user,
    data: params
  });
}

export function delete_user(params: object): Promise<ServerResponse> {
  return request({
    url: api.delete_user,
    data: params,
    responseType: 'json'
  });
}

export function close_user(params: object): Promise<ServerResponse> {
  return request({
    url: api.close_user,
    data: params,
    responseType: 'json'
  });
}

export function search_user(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_user,
    data: params,
    responseType: 'json'
  });
}
export function createUser(params: object): Promise<ServerResponse> {
  return request({
    url: api.create_user,
    data: params,
    responseType: 'json'
  });
}

export function searchRole(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_role,
    data: params,
    responseType: 'json'
  });
}

export async function adminSearchUserAPI(params: object): Promise<ServerResponse> {
  return request({
    url: api.admin_search_user,
    data: params,
    responseType: 'json'
  });
}
export async function twadminSearchUser(params: object): Promise<ServerResponse> {
  return request({
    url: api.twadmin_search_user,
    data: params,
    responseType: 'json'
  });
}
export async function adminUpdateRole(params: object): Promise<ServerResponse> {
  return request({
    url: api.admin_update_role,
    data: params,
    responseType: 'json'
  });
}

export async function twadminUpdateRole(params: object): Promise<ServerResponse> {
  return request({
    url: api.twadmin_update_role,
    data: params,
    responseType: 'json'
  });
}

export async function adminArchiveUser(params: object): Promise<ServerResponse> {
  return request({
    url: api.admin_archive_user,
    data: params,
    responseType: 'json'
  });
}

export async function adminCloseUser(params: object): Promise<ServerResponse> {
  return request({
    url: api.admin_close_user,
    data: params,
    responseType: 'json'
  });
}

export async function adminUpdateUserAPI(params: object): Promise<ServerResponse> {
  return request({
    url: api.admin_update_user,
    data: params,
    responseType: 'json'
  });
}