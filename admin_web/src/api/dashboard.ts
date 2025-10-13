import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '/next_console_admin';

export const api = {
  get_dashboard_index: envUrl + '/dashboard/index',
  get_model_run_index: `${envUrl}/dashboard/model`,
  get_all_company: envUrl + '/management_center/management/user/all_company/search',
  lookupbyadmin: `${envUrl}/management_center/management/user/department/lookupbyadmin`,
  lookupbytwadmin: `${envUrl}/management_center/management/user/department/lookupbytwadmin`,
  updateuseraccounttypeadmin: `${envUrl}/management_center/management/user/updateuseraccounttypeadmin`,
  getCompanyList: `${envUrl}/management_center/management/user/company/lookupbytwadmin`,
  addCompany: `${envUrl}/management_center/management/user/company/addbytwadmin`,
  updateCompany: `${envUrl}/management_center/management/user/company/updatebyadmin`,
  addDepartment: `${envUrl}/management_center/management/user/department/addbytwadmin`,
  updateDepartment: `${envUrl}/management_center/management/user/department/updatebytwadmin`

};

export async function getDashboardIndex(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_dashboard_index,
    method: 'get',
    params: params
  });
}

export async function getAllCompany(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_all_company,
    data: params,
    responseType: 'json'
  });
}

export async function sendRequest(params: TRequestParams): Promise<ServerResponse> {
  const { url: paramsUrl, ...args } = params;
  return request({
    url: api[paramsUrl],
    data: args,
    responseType: 'json'
  });
}
export async function searchDepartments(params: object): Promise<ServerResponse> {
  return request({
    url: api.lookupbytwadmin,
    data: params,
    method: 'post'
  });
}

export type TRequestParams = { url: keyof typeof api } & { [key: string]: any };

export async function getModelRunIndex(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_model_run_index,
    method: 'get',
    params: params
  });
}
