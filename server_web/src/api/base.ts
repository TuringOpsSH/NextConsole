import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

let envUrl = '';

export const api = {
  version_get: envUrl + '/next_console/version'
};

export async function versionGet(): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.version_get,
    noAuth: true
  });
}
