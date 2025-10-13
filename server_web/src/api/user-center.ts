import { useUserInfoStore } from '@/stores/user-info-store';
import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '';

export const api = {
  get_support_area: envUrl + '/next_console/get_support_area',
  check_register_email: envUrl + '/next_console/check_register_email',
  register_user: envUrl + '/next_console/register',
  confirm_email: envUrl + '/next_console/confirm_email',
  resend_confirm_email: envUrl + '/next_console/resend_confirm_email',
  login_by_password: envUrl + '/next_console/login_by_password',
  reset_account_password: envUrl + '/next_console/reset_account_password',
  valid_reset_password_code: envUrl + '/next_console/reset_password_code/valid',

  update_user: envUrl + '/next_console/user_center/users/update',
  user_avatar_update: envUrl + '/next_console/user_center/users/avatar/update',
  get_user: envUrl + '/next_console/user_center/users/get',
  reset_new_email_url: envUrl + '/next_console/reset_new_email',
  valid_reset_email_code: envUrl + '/next_console/reset_email_code/valid',
  generate_text_code: envUrl + '/next_console/user_center/generate_text_code',
  valid_text_code: envUrl + '/next_console/user_center/valid_text_code',
  login_by_code: envUrl + '/next_console/login_by_code',
  wx_register: envUrl + '/next_console/wx_register',
  bind_new_phone: envUrl + '/next_console/user_center/bind_new_phone',
  valid_new_phone: envUrl + '/next_console/user_center/valid_new_phone',
  close_user: envUrl + '/next_console/user_center/users/close',
  // 站内信
  get_system_notices: envUrl + '/next_console/get_system_notices',
  set_system_notices_read: envUrl + '/next_console/set_system_notices_read',
  // 邀请码
  refresh_invite_code: envUrl + '/next_console/user_center/refresh_invite_code',
  send_invite_code_by_email: envUrl + '/next_console/user_center/send_invite_code_by_email',
  get_invite_detail: envUrl + '/next_console/user_center/get_invite_detail',
  accept_invite_friend: envUrl + '/next_console/user_center/accept_invite_friend',
  update_invite_status: envUrl + '/next_console/user_center/update_invite_status',
  add_website_invite: envUrl + '/next_console/user_center/add_website_invite',

  // 账户
  list_point_transaction: envUrl + '/next_console/user_center/list_points_transaction',
  list_products: envUrl + '/next_console/user_center/list_products',
  init_order: envUrl + '/next_console/user_center/init_order',
  get_order: envUrl + '/next_console/user_center/get_order',
  list_orders: envUrl + '/next_console/user_center/list_orders',
  cancel_order: envUrl + '/next_console/user_center/cancel_order',
  remove_order_item: envUrl + '/next_console/user_center/remove_order_item',
  add_order_item: envUrl + '/next_console/user_center/add_order_item',
  generate_exchange_code: envUrl + '/next_console/user_center/generate_exchange_code',
  valid_exchange_code: envUrl + '/next_console/user_center/valid_exchange_code',
  confirm_order: envUrl + '/next_console/user_center/confirm_order',
  get_user_activity_days: envUrl + '/next_console/user_center/get_user_activity_days',
  check_market_info: envUrl + '/next_console/user_center/check_market_info',

  // 配置
  user_config_get: envUrl + '/next_console/config_center/user_config/get',
  user_config_update: envUrl + '/next_console/config_center/user_config/update',
  llm_instance_search: envUrl + '/next_console/config_center/llm_instance/search',
  system_config_get: envUrl + '/next_console/config_center/system_config/get',
  system_config_update: envUrl + '/next_console/config_center/system_config/update',
  refresh_token: envUrl + '/next_console/user_center/refresh_token',
  get_wx_config: envUrl + '/next_console/config_center/system_config/get_wx_config',
  system_config_load: envUrl + '/next_console/config_center/system_config/load',
  get_domain: envUrl + '/next_console/domain'
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

export async function acceptInviteFriend(params: object): Promise<ServerResponse> {
  return request({
    url: api.accept_invite_friend,
    data: params,
    responseType: 'json'
  });
}

export async function updateInviteStatus(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.update_invite_status,
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
