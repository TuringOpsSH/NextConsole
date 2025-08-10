import { ServerResponse } from '@/types/response';
import request from '@/utils/request';
import {getToken} from "@/utils/auth";

const envUrl = '';

export const api = {
  user_config_get: envUrl + '/ces_os/config_center/user_config/get',
  user_config_update: envUrl + '/ces_os/config_center/user_config/update',
  llm_instance_search: envUrl + '/next_console_admin/config_center/llm_instance/search',
  llm_instance_add: envUrl + '/next_console_admin/config_center/llm_instance/add',
  llm_icon_upload: envUrl + '/next_console_admin/config_center/llm_instance/icon/upload',
  llm_instance_del: envUrl + '/next_console_admin/config_center/llm_instance/del',
  llm_instance_get: envUrl + '/next_console_admin/config_center/llm_instance/get',
  llm_instance_update: envUrl + '/next_console_admin/config_center/llm_instance/update',
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

export async function llmInstanceAdd(params: object): Promise<ServerResponse> {
    return request({
      url: api.llm_instance_add,
      data: params,
      responseType: 'json'
    });
}

export async function llmIconUpload(params: object): Promise<ServerResponse> {
  return request({
    url: api.llm_icon_upload,
    data: params,
    responseType: 'json'
  });
}

export async function llmInstanceDel(params: object): Promise<ServerResponse> {
  return request({
    url: api.llm_instance_del,
    data: params,
    responseType: 'json'
  });
}

export async function llmInstanceGet(params: object): Promise<ServerResponse> {
  return request({
    url: api.llm_instance_get,
    data: params,
    responseType: 'json'
  });
}

export async function llmInstanceUpdate(params: object): Promise<ServerResponse> {
  return request({
    url: api.llm_instance_update,
    data: params,
    responseType: 'json'
  });
}

