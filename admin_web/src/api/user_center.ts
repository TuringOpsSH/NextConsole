import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '';

export const api = {
  get_support_area: envUrl + '/next_console_admin/get_support_area',
  check_register_email: envUrl + '/next_console_admin/check_register_email',
  register_user: envUrl + '/next_console_admin/register',
  confirm_email: envUrl + '/next_console_admin/confirm_email',
  resend_confirm_email: envUrl + '/next_console_admin/resend_confirm_email',
  login_by_password: envUrl + '/next_console_admin/login_by_password',
  reset_account_password: envUrl + '/next_console_admin/reset_account_password',
  valid_reset_password_code: envUrl + '/next_console_admin/reset_password_code/valid',
  update_user: envUrl + '/next_console_admin/user_center/users/update',
  user_avatar_update: envUrl + '/next_console_admin/user_center/users/avatar/update',
  get_user: envUrl + '/next_console_admin/user_center/users/get',
  reset_new_email_url: envUrl + '/next_console_admin/reset_new_email',
  valid_reset_email_code: envUrl + '/next_console_admin/reset_email_code/valid',
  generate_text_code: envUrl + '/next_console_admin/user_center/generate_text_code',
  valid_text_code: envUrl + '/next_console_admin/user_center/valid_text_code',
  login_by_code: envUrl + '/next_console_admin/login_by_code',
  wx_register: envUrl + '/next_console_admin/wx_register',
  bind_new_phone: envUrl + '/next_console_admin/user_center/bind_new_phone',
  valid_new_phone: envUrl + '/next_console_admin/user_center/valid_new_phone',
  // 站内信
  get_system_notices: envUrl + '/next_console_admin/get_system_notices',
  set_system_notices_read: envUrl + '/next_console_admin/set_system_notices_read',
  // 市场活动
  searchCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/search',
  createCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/create',
  deleteCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/delete',
  getCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/get',
  updateCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/update',
  searchCampaignData: envUrl + '/next_console_admin/user_center/marketing_campaign/search_data'
};
export async function get_support_area(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_support_area,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function check_register_email(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.check_register_email,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function register_user(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.register_user,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function confirm_email(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.confirm_email,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function resend_confirm_email(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resend_confirm_email,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function login_by_password(params: object): Promise<ServerResponse> {
  // 请求token
  // @ts-ignore
  return request({
    data: params,
    url: api.login_by_password,
    responseType: 'json',
    noAuth: true
  });
}
export async function reset_account_password(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.reset_account_password,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function valid_reset_password_code(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.valid_reset_password_code,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function getUser(params: object): Promise<ServerResponse> {
  return await request({
    url: api.get_user,
    data: params,
    responseType: 'json'
  });
}

export async function user_update(params: object): Promise<ServerResponse> {
  return request({
    url: api.update_user,
    data: params,
    responseType: 'json'
  });
}

export async function reset_new_email(params: object): Promise<ServerResponse> {
  return request({
    url: api.reset_new_email_url,
    data: params,
    responseType: 'json'
  });
}

export async function valid_reset_email_code(params: object): Promise<ServerResponse> {
  return request({
    url: api.valid_reset_email_code,
    data: params,
    responseType: 'json'
  });
}

export async function generate_text_code(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.generate_text_code,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function valid_text_code(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.valid_text_code,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function login_by_code(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.login_by_code,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function get_system_notices(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_system_notices,
    data: params,
    responseType: 'json'
  });
}

export async function set_system_notices_read(params: object): Promise<ServerResponse> {
  return request({
    url: api.set_system_notices_read,
    data: params,
    responseType: 'json'
  });
}

export async function wx_register(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.wx_register,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function bind_new_phone_api(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.bind_new_phone,
    data: params,
    responseType: 'json'
  });
}

export async function valid_new_phone_api(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.valid_new_phone,
    data: params,
    responseType: 'json'
  });
}

export async function searchCampaignApi(params: object): Promise<ServerResponse> {
  return request({
    url: api.searchCampaign,
    data: params,
    responseType: 'json'
  });
}
export async function createCampaignApi(params: object): Promise<ServerResponse> {
  return request({
    url: api.createCampaign,
    data: params,
    responseType: 'json'
  });
}

export async function deleteCampaignApi(params: object): Promise<ServerResponse> {
  return request({
    url: api.deleteCampaign,
    data: params,
    responseType: 'json'
  });
}

export async function getCampaignApi(params: object): Promise<ServerResponse> {
  return request({
    url: api.getCampaign,
    data: params,
    responseType: 'json'
  });
}

export async function updateCampaignApi(params: object): Promise<ServerResponse> {
  return request({
    url: api.updateCampaign,
    data: params,
    responseType: 'json'
  });
}

export async function searchCampaignDataApi(params: object): Promise<ServerResponse> {
  return request({
    url: api.searchCampaignData,
    data: params,
    responseType: 'json'
  });
}
