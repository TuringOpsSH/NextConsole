import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '/next_console_admin';

export const api = {
  search_session_log: envUrl + '/management_center/management/session/lookup',
  search_session_source: envUrl + '/management_center/management/session/search_source',
  get_session_history_msg: envUrl + '/management_center/management/session/lookupmsg',
  admin_add_like: envUrl + '/management_center/management/session/updateadminmsglike',
  admin_favorite: envUrl + '/management_center/management/session/updateadminfavorite',
  admin_add_tag: envUrl + '/management_center/management/session/addtag',
  msg_rag_trace: envUrl + '/feedback_center/trace/rag/get',
  msg_workflow_trace: envUrl + '/feedback_center/trace/workflow/get'
};

export async function searchSessionLog(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_session_log,
    method: 'post',
    data: params
  });
}
export async function searchSessionSourceAPI(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_session_source,
    method: 'post',
    data: params
  });
}

export async function get_session_history_msg(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_session_history_msg,
    method: 'post',
    data: params
  });
}

export async function admin_add_like(params: object): Promise<ServerResponse> {
  return request({
    url: api.admin_add_like,
    method: 'post',
    data: params
  });
}
export async function admin_favorite(params: object): Promise<ServerResponse> {
  return request({
    url: api.admin_favorite,
    method: 'post',
    data: params
  });
}

export async function admin_add_tag(params: object): Promise<ServerResponse> {
  return request({
    url: api.admin_add_tag,
    method: 'post',
    data: params
  });
}

export async function get_msg_rag_trace(params: object): Promise<ServerResponse> {
  return request({
    url: api.msg_rag_trace,
    method: 'post',
    data: params
  });
}

export async function get_msg_workflow_trace(params: object): Promise<ServerResponse> {
  return request({
    url: api.msg_workflow_trace,
    method: 'post',
    data: params
  });
}
