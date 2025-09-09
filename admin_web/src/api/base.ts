import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '';

export const api = {
  version_get: envUrl + '/next_console_admin/version',
  domain_get: envUrl + '/next_console_admin/domain',
  latest_version_get: 'https://www.turingops.com.cn/next_console/version'
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
  });
}

export async function latestVersionGet(): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.latest_version_get,
    noAuth: true
  });
}
