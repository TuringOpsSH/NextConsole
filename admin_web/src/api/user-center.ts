import { useUserInfoStore } from '@/stores/user-info-store';
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
  close_user: envUrl + '/next_console_admin/user_center/users/close',
  // 站内信
  get_system_notices: envUrl + '/next_console_admin/get_system_notices',
  set_system_notices_read: envUrl + '/next_console_admin/set_system_notices_read',
  // 邀请码
  refresh_invite_code: envUrl + '/next_console_admin/user_center/refresh_invite_code',
  send_invite_code_by_email: envUrl + '/next_console_admin/user_center/send_invite_code_by_email',
  get_invite_detail: envUrl + '/next_console_admin/user_center/get_invite_detail',
  // 账户
  list_point_transaction: envUrl + '/next_console_admin/user_center/list_points_transaction',
  // 市场活动
  searchCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/search',
  createCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/create',
  deleteCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/delete',
  getCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/get',
  updateCampaign: envUrl + '/next_console_admin/user_center/marketing_campaign/update',
  searchCampaignData: envUrl + '/next_console_admin/user_center/marketing_campaign/search_data',
  // 配置
  user_config_get: envUrl + '/next_console_admin/config_center/user_config/get',
  user_config_update: envUrl + '/next_console_admin/config_center/user_config/update',
  llm_instance_search: envUrl + '/next_console_admin/config_center/llm_instance/search',
  system_config_get: envUrl + '/next_console_admin/config_center/system_config/get',
  system_config_update: envUrl + '/next_console_admin/config_center/system_config/update',
  refresh_token: envUrl + '/next_console_admin/user_center/refresh_token',
  get_wx_config: envUrl + '/next_console_admin/config_center/system_config/get_wx_config',
  system_config_load: envUrl + '/next_console_admin/config_center/system_config/load',
  system_config_reset: envUrl + '/next_console_admin/config_center/system_config/reset'
};
export async function getSupportArea(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_support_area,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function loginByPassword(params: object): Promise<ServerResponse> {
  // 请求token
  // @ts-ignore
  return request({
    data: params,
    url: api.login_by_password,
    responseType: 'json',
    noAuth: true
  });
}
export async function resetAccountPassword(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.reset_account_password,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function validResetPasswordCode(params: object): Promise<ServerResponse> {
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

export async function userUpdate(params: object): Promise<ServerResponse> {
  return request({
    url: api.update_user,
    data: params,
    responseType: 'json'
  });
}

export async function resetNewEmail(params: object): Promise<ServerResponse> {
  return request({
    url: api.reset_new_email_url,
    data: params,
    responseType: 'json'
  });
}

export async function validResetEmailCode(params: object): Promise<ServerResponse> {
  return request({
    url: api.valid_reset_email_code,
    data: params,
    responseType: 'json'
  });
}

export async function generateTextCode(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.generate_text_code,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function validTextCode(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.valid_text_code,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function loginByCode(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.login_by_code,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function getSystemNotices(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_system_notices,
    data: params,
    responseType: 'json'
  });
}

export async function setSystemNoticesRead(params: object): Promise<ServerResponse> {
  return request({
    url: api.set_system_notices_read,
    data: params,
    responseType: 'json'
  });
}

export async function wxRegister(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.wx_register,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function bindNewPhoneApi(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.bind_new_phone,
    data: params,
    responseType: 'json'
  });
}

export async function validNewPhoneApi(params: object): Promise<ServerResponse> {
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

export async function refreshInviteCode(params: object): Promise<ServerResponse> {
  return request({
    url: api.refresh_invite_code,
    data: params,
    responseType: 'json'
  });
}

export async function sendInviteCodeByEmail(params: object): Promise<ServerResponse> {
  return request({
    url: api.send_invite_code_by_email,
    data: params,
    responseType: 'json'
  });
}

export async function getInviteDetail(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_invite_detail,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function closeUser(params: object): Promise<ServerResponse> {
  return request({
    url: api.close_user,
    data: params,
    responseType: 'json'
  });
}

export async function listPointTransaction(params: object): Promise<ServerResponse> {
  return request({
    url: api.list_point_transaction,
    data: params,
    responseType: 'json'
  });
}

export async function userConfigGet(params: object): Promise<ServerResponse> {
  return request({
    url: api.user_config_get,
    data: params,
    responseType: 'json'
  });
}

export async function userConfigUpdate(params: object): Promise<ServerResponse> {
  return request({
    url: api.user_config_update,
    data: params,
    responseType: 'json'
  });
}

export async function llmInstanceSearch(params: object): Promise<ServerResponse> {
  const userInfoStore = useUserInfoStore();
  if (userInfoStore.token) {
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

export async function systemConfigGet(params: object): Promise<ServerResponse> {
  return request({
    url: api.system_config_get,
    data: params,
    responseType: 'json'
  });
}

export async function systemConfigUpdate(params: object): Promise<ServerResponse> {
  return request({
    url: api.system_config_update,
    data: params,
    responseType: 'json'
  });
}

export async function refreshToken(params: object): Promise<ServerResponse> {
  return request({
    url: api.refresh_token,
    data: params,
    responseType: 'json'
  });
}

export async function getWxConfig(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_wx_config,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function systemConfigLoad(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.system_config_load,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function systemConfigReset(params: object): Promise<ServerResponse> {
  return request({
    url: api.system_config_reset,
    data: params,
    responseType: 'json'
  });
}
