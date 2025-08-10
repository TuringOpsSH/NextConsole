import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

let envUrl = '';

export const api = {
  version_get: envUrl + '/next_console/version',
  domain_get: envUrl + '/next_console/domain',
};

export async function versionGet(): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.version_get,
    noAuth: true
  });
}

export async function domainGet(): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.domain_get,
    noAuth: true
  })
}
