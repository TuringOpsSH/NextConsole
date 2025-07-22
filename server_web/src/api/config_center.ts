import { ServerResponse } from '@/types/response';
import { getToken } from '@/utils/auth';
import request from '@/utils/request';

let envUrl = '';

export const api = {
  user_config_get: envUrl + '/next_console/config_center/user_config/get',
  user_config_update: envUrl + '/next_console/config_center/user_config/update',
  llm_instance_search: envUrl + '/next_console/config_center/llm_instance/search'
};

export async function user_config_get(params: object): Promise<ServerResponse> {
  return request({
    url: api.user_config_get,
    data: params,
    responseType: 'json'
  });
}

export async function user_config_update(params: object): Promise<ServerResponse> {
  return request({
    url: api.user_config_update,
    data: params,
    responseType: 'json'
  });
}

export async function llmInstanceSearch(params: object): Promise<ServerResponse> {
  const token = getToken();
  if (token) {
    return request({
      url: api.llm_instance_search,
      data: params,
      responseType: 'json'
    });
  }
  // @ts-ignore
  return request({
    url: api.llm_instance_search,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
