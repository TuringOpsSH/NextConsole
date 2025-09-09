import { ServerResponse } from '@/types/response';
import request from '@/utils/request';
const envUrl = '';

interface IParams {
  url: string;
  params?: object;
  isUploadFile?: boolean;
}

export async function ajax(requestParams: IParams): Promise<ServerResponse> {
  const { url, params, isUploadFile = false } = requestParams;
  const apiUrl = api[url].includes('next_console') ? api[url] : `/next_console/app_center/${api[url]}`;
  let requestData = {
    url: apiUrl,
    data: params ?? {},
    responseType: 'json',
    headers: {
      // eslint-disable-next-line @typescript-eslint/naming-convention
      ContentType: 'application/json'
    }
  };
  if (isUploadFile) {
    requestData = {
      ...requestData,
      headers: {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        ContentType: 'multipart/form-data'
      }
    };
  }
  // @ts-ignore
  return request(requestData);
}

export const api = {
  searchAppList: 'app_manage/search',
  initSession: 'app_run/init_session',
  completions: 'app_run/v2/chat/completions',
  uploadInit: '/next_console/attachment/base_init',
  createUploadTask: '/next_console/resources/object/upload_task/add',
  uploadResource: '/next_console/resources/object/upload',
  getUploadedList: '/next_console/attachment/search_in_session',
  updateTaskStatus: '/next_console/resources/object/upload_task/update',
  addFileToSession: '/next_console/attachment/add_into_session',
  deleteSessionFile: '/next_console/attachment/remove_from_session',
  getSessionFileList: '/next_console/attachment/get_detail',
  batchDownloadFile: '/next_console/resources/object/batch_download',
  downloadFile: '/next_console/resources/object/download'
};

export function deleteSessionFile(params): Promise<ServerResponse> {
  return request({
    url: api.deleteSessionFile,
    data: params,
    responseType: 'json'
  });
}

export function getSessionFileList(params): Promise<ServerResponse> {
  return request({
    url: api.getSessionFileList,
    data: params,
    responseType: 'json'
  });
}

interface IMessage {
  role: string;
  content: string;
}
export interface ISendQuestion {
  messages: IMessage[];
  app_code: string;
  session_code: string;
  attachments?: string[];
}


export function batchDownloadFile(params: { resource_list: number[] }): Promise<ServerResponse> {
  return request({
    url: envUrl + api.batchDownloadFile,
    data: params,
    responseType: 'json'
  });
}

export function downloadFile(params: { resource_id: number }): Promise<ServerResponse> {
  return request({
    url: envUrl + api.downloadFile,
    data: params,
    responseType: 'json'
  });
}

export function updateTaskStatus(params: { task_id: number }): Promise<ServerResponse> {
  return request({
    url: api.updateTaskStatus,
    data: {
      ...params,
      task_status: 'success'
    },
    responseType: 'json'
  });
}
