import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '/next_console_admin';

export const api = {
  get_dashboard_index: envUrl + '/dashboard/index',
  get_all_company: envUrl + '/management_center/management/user/all_company/search',
  lookupbytwadmin: `${envUrl}/management_center/management/user/department/lookupbytwadmin`,
  updateuseraccounttypeadmin: `${envUrl}/management_center/management/user/updateuseraccounttypeadmin`,
  getCompanyList: `${envUrl}/management_center/management/user/company/lookupbytwadmin`,
  addCompany: `${envUrl}/management_center/management/user/company/addbytwadmin`,
  updateCompany: `${envUrl}/management_center/management/user/company/updatebyadmin`,
  addDepartment: `${envUrl}/management_center/management/user/department/addbytwadmin`,
  updateDepartment: `${envUrl}/management_center/management/user/department/updatebytwadmin`
};

export async function get_dashboard_index(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_dashboard_index,
    method: 'get',
    params: params
  });
}

export async function get_all_company(params: object): Promise<ServerResponse> {
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
