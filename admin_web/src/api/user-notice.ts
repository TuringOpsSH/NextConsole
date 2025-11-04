import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '';

export const api = {
  list_task: envUrl + '/next_console_admin/user_center/user_notice_service/list',
  search_task: envUrl + '/next_console_admin/user_center/user_notice_service/search',
  delete_task: envUrl + '/next_console_admin/user_center/user_notice_service/del',
  get_task_detail: envUrl + '/next_console_admin/user_center/user_notice_service/detail',
  init_task: envUrl + '/next_console_admin/user_center/user_notice_service/init',
  update_task: envUrl + '/next_console_admin/user_center/user_notice_service/update',
  search_notice_company: envUrl + '/next_console_admin/user_center/user_notice_service/search_notice_company',
  search_notice_department: envUrl + '/next_console_admin/user_center/user_notice_service/search_notice_department',
  search_notice_user: envUrl + '/next_console_admin/user_center/user_notice_service/search_notice_user',
  start_task: envUrl + '/next_console_admin/user_center/user_notice_service/start',
  pause_task: envUrl + '/next_console_admin/user_center/user_notice_service/pause',
  resume_task: envUrl + '/next_console_admin/user_center/user_notice_service/resume',
  stop_task: envUrl + '/next_console_admin/user_center/user_notice_service/stop',
  list_task_instance: envUrl + '/next_console_admin/user_center/user_notice_service/list_instance'
};

export async function listTask(params: object): Promise<ServerResponse> {
  return request({
    url: api.list_task,
    method: 'post',
    data: params
  });
}

export async function searchTask(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_task,
    method: 'post',
    data: params
  });
}

export async function deleteTask(params: object): Promise<ServerResponse> {
  return request({
    url: api.delete_task,
    method: 'post',
    data: params
  });
}

export async function getTaskDetail(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_task_detail,
    method: 'post',
    data: params
  });
}

export async function initTask(params: object): Promise<ServerResponse> {
  return request({
    url: api.init_task,
    method: 'post',
    data: params
  });
}

export async function updateTask(params: object): Promise<ServerResponse> {
  return request({
    url: api.update_task,
    method: 'post',
    data: params
  });
}

export async function searchNoticeCompany(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_notice_company,
    method: 'post',
    data: params
  });
}

export async function searchNoticeDepartment(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_notice_department,
    method: 'post',
    data: params
  });
}

export async function searchNoticeUser(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_notice_user,
    method: 'post',
    data: params
  });
}

export async function startTask(params: object): Promise<ServerResponse> {
  return request({
    url: api.start_task,
    method: 'post',
    data: params
  });
}

export async function pauseTask(params: object): Promise<ServerResponse> {
  return request({
    url: api.pause_task,
    method: 'post',
    data: params
  });
}

export async function resumeTask(params: object): Promise<ServerResponse> {
  return request({
    url: api.resume_task,
    method: 'post',
    data: params
  });
}

export async function stopTask(params: object): Promise<ServerResponse> {
  return request({
    url: api.stop_task,
    method: 'post',
    data: params
  });
}

export async function listTaskInstance(params: object): Promise<ServerResponse> {
  return request({
    url: api.list_task_instance,
    method: 'post',
    data: params
  });
}
