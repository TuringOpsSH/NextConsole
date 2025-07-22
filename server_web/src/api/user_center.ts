import request from '@/utils/request';
import { ServerResponse } from '@/types/response';

let envUrl = '';

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
  check_market_info: envUrl + '/next_console/user_center/check_market_info'
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

export async function confirm_email(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.confirm_email,
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

export async function get_user(params: object): Promise<ServerResponse> {
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

export async function refresh_invite_code(params: object): Promise<ServerResponse> {
  return request({
    url: api.refresh_invite_code,
    data: params,
    responseType: 'json'
  });
}

export async function send_invite_code_by_email(params: object): Promise<ServerResponse> {
  return request({
    url: api.send_invite_code_by_email,
    data: params,
    responseType: 'json'
  });
}

export async function get_invite_detail(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_invite_detail,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function accept_invite_friend(params: object): Promise<ServerResponse> {
  return request({
    url: api.accept_invite_friend,
    data: params,
    responseType: 'json'
  });
}

export async function update_invite_status(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.update_invite_status,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function add_website_invite(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.add_website_invite,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function close_user(params: object): Promise<ServerResponse> {
  return request({
    url: api.close_user,
    data: params,
    responseType: 'json'
  });
}

export async function list_point_transaction(params: object): Promise<ServerResponse> {
  return request({
    url: api.list_point_transaction,
    data: params,
    responseType: 'json'
  });
}

export async function list_products(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.list_products,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function init_order(params: object): Promise<ServerResponse> {
  return request({
    url: api.init_order,
    data: params,
    responseType: 'json'
  });
}
export async function list_orders(params: object): Promise<ServerResponse> {
  return request({
    url: api.list_orders,
    data: params,
    responseType: 'json'
  });
}

export async function get_order(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_order,
    data: params,
    responseType: 'json'
  });
}

export async function cancel_order(params: object): Promise<ServerResponse> {
  return request({
    url: api.cancel_order,
    data: params,
    responseType: 'json'
  });
}
export async function add_order_item(params: object): Promise<ServerResponse> {
  return request({
    url: api.add_order_item,
    data: params,
    responseType: 'json'
  });
}

export async function remove_order_item(params: object): Promise<ServerResponse> {
  return request({
    url: api.remove_order_item,
    data: params,
    responseType: 'json'
  });
}

export async function generate_exchange_code(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.generate_exchange_code,
    data: params,
    responseType: 'json'
  });
}

export async function valid_exchange_code(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.valid_exchange_code,
    data: params,
    responseType: 'json'
  });
}

export async function confirm_user_order(params: object): Promise<ServerResponse> {
  return request({
    url: api.confirm_order,
    data: params,
    responseType: 'json'
  });
}

export async function get_user_activity_days(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_user_activity_days,
    data: params,
    responseType: 'json'
  });
}

export async function check_market_info(params: object): Promise<ServerResponse> {
  return request({
    url: api.check_market_info,
    data: params,
    responseType: 'json'
  });
}

export async function uploadAvatar(params: object): Promise<ServerResponse> {
  return request({
    url: api.user_avatar_update,
    data: params,
    responseType: 'json'
  });
}
