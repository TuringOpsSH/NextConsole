import request from '@/utils/request';
import { ServerResponse } from '@/types/response';

let envUrl = '';

export const api = {
  wikiFileUpload: envUrl + '/next_console/wiki/space/file/upload',
  wikiSpaceList: envUrl + '/next_console/open-api/wiki/space/list',
  wikiSearch: envUrl + '/next_console/open-api/wiki/page/search',
  wikiOverview: envUrl + '/next_console/open-api/wiki/space/overview',
  wikiDetail: envUrl + '/next_console/open-api/wiki/page/detail'
};

export async function wikiFileUpload(params: object): Promise<ServerResponse> {
  const requestData = {
    url: api.wikiFileUpload,
    data: params ?? {},
    responseType: 'json',
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  };
  // @ts-ignore
  return request(requestData);
}

export async function wikiSpaceList(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.wikiSpaceList,
    method: 'post',
    data: params,
    noAuth: true
  });
}

export async function wikiSearch(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.wikiSearch,
    method: 'post',
    data: params,
    noAuth: true
  });
}

export async function wikiOverview(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.wikiOverview,
    method: 'post',
    data: params,
    noAuth: true
  });
}

export async function wikiDetail(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.wikiDetail,
    method: 'post',
    data: params,
    noAuth: true
  });
}
