import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '';

export const api = {
  get_company_info: envUrl + '/next_console_admin/contacts/get_company_info',
  get_department_list: envUrl + '/next_console_admin/contacts/get_department_list',
  get_department_info: envUrl + '/next_console_admin/contacts/get_department_info',
  search_department_info: envUrl + '/next_console_admin/contacts/search_department_info',
  get_colleague_list: envUrl + '/next_console_admin/contacts/get_colleague_list',
  search_colleague: envUrl + '/next_console_admin/contacts/search_colleague',
  get_friend_list: envUrl + '/next_console_admin/contacts/friends/get_friend_list',
  search_friends: envUrl + '/next_console_admin/user_center/friends/search',
  delete_friend: envUrl + '/next_console_admin/user_center/friends/delete',
  search_stranger: envUrl + '/next_console_admin/user_center/friends/stranger',
  add_friend: envUrl + '/next_console_admin/user_center/friends/add',
  friend_requests_cnt: envUrl + '/next_console_admin/user_center/friends/friend_requests_cnt',
  friend_requests_history: envUrl + '/next_console_admin/user_center/friends/friend_requests_history',
  accept_friend_request: envUrl + '/next_console_admin/user_center/friends/accept_friend_request',
  reject_friend_request: envUrl + '/next_console_admin/user_center/friends/reject_friend_request',
  add_subscribe: envUrl + '/next_console_admin/user_center/visitor/subscribe'
};
export async function get_company_info(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_company_info,
    data: params,
    responseType: 'json'
  });
}

export async function getDepartmentList(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_department_list,
    data: params,
    responseType: 'json'
  });
}

export async function get_department_info(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_department_info,
    data: params,
    responseType: 'json'
  });
}

export async function getColleagueList(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_colleague_list,
    data: params,
    responseType: 'json'
  });
}

export async function getFriendList(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_friend_list,
    data: params,
    responseType: 'json'
  });
}

export async function searchFriends(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_friends,
    data: params,
    responseType: 'json'
  });
}

export async function delete_friend(params: object): Promise<ServerResponse> {
  return request({
    url: api.delete_friend,
    data: params,
    responseType: 'json'
  });
}

export async function search_stranger(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_stranger,
    data: params,
    responseType: 'json'
  });
}

export async function add_friend(params: object): Promise<ServerResponse> {
  return request({
    url: api.add_friend,
    data: params,
    responseType: 'json'
  });
}
export async function get_friend_request_cnt(params: object): Promise<ServerResponse> {
  return request({
    url: api.friend_requests_cnt,
    data: params,
    responseType: 'json'
  });
}

export async function get_friend_request_history(params: object): Promise<ServerResponse> {
  return request({
    url: api.friend_requests_history,
    data: params,
    responseType: 'json'
  });
}

export async function accept_friend_request(params: object): Promise<ServerResponse> {
  return request({
    url: api.accept_friend_request,
    data: params,
    responseType: 'json'
  });
}

export async function reject_friend_request(params: object): Promise<ServerResponse> {
  return request({
    url: api.reject_friend_request,
    data: params,
    responseType: 'json'
  });
}

export async function searchColleague(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_colleague,
    data: params,
    responseType: 'json'
  });
}

export async function searchDepartmentInfo(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_department_info,
    data: params,
    responseType: 'json'
  });
}

export async function add_subscribe_api(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.add_subscribe,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
