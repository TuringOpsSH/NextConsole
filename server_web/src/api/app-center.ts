import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

let envUrl = '';

export const api = {
  app_detail: envUrl + '/next_console/app_center/app/detail',
  init_app_session: envUrl + '/next_console/app_center/app/init_session',
  init_app_msg: envUrl + '/next_console/app_center/app/init_app_msg',
  app_search: envUrl + '/next_console/app_center/app_manage/search',
};

export async function appDetail(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_detail,
    data: params,
    responseType: 'json'
  });
}

export async function initAppSession(params: object): Promise<ServerResponse> {
  return request({
    url: api.init_app_session,
    data: params,
    responseType: 'json'
  });
}

export async function initAppMsg(params: object): Promise<ServerResponse> {
  return request({
    url: api.init_app_msg,
    data: params,
    responseType: 'json'
  });
}

export async function appSearch(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_search,
    data: params,
    responseType: 'json'
  });
}
