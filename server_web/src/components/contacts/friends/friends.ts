import { ElMessage } from 'element-plus';
import { ref } from 'vue';
import {
  accept_friend_request,
  add_friend,
  delete_friend,
  get_friend_list,
  get_friend_request_history,
  reject_friend_request,
  search_friends,
  search_stranger
} from '@/api/contacts';
import { init_friend_request_cnt } from '@/components/contacts/contacts-panel/contacts_panel';
import { Friend, FriendRelation } from '@/types/contacts';

export const current_friend_list = ref<Friend[]>([]);
export const current_friend = ref<Friend>();
export const current_search_friends = ref<Friend[]>([]);
export const friend_search_keyword = ref('');
export const current_model = ref('list');

export const new_friend_search_keyword = ref('');
export const search_new_friends = ref<Friend[]>([]);
export const current_new_friend = ref<Friend>();
export const friend_loading = ref(false);
export const show_delete_confirm_flag = ref(false);

export const history_friends = ref<Friend[]>([]);
export const friends_width = ref(window.innerWidth < 768 ? window.innerWidth - 60 + 'px' : '300px');

export async function init_current_friend_list() {
  friend_loading.value = true;
  const friend_list = await get_friend_list({});
  if (!friend_list.error_status) {
    current_friend_list.value = friend_list.result.data;
  }
  friend_loading.value = false;
}
export async function search_friend_list() {
  if (!friend_search_keyword.value) {
    return;
  }
  current_model.value = 'search';
  friend_loading.value = true;
  const search_res = await search_friends({
    friend_keyword: friend_search_keyword.value
  });
  if (!search_res.error_status) {
    current_search_friends.value = search_res.result.data;
  }
  friend_loading.value = false;
  // console.log(current_model.value)
}

export function set_current_friend(friend: Friend) {
  current_friend.value = friend;
  current_new_friend.value = null;
  current_model.value = 'list';
  if (window.innerWidth < 768) {
    friends_width.value = '0px';
  }
}
export function set_current_new_friend(friend: Friend) {
  current_friend.value = null;
  current_new_friend.value = friend;
  current_model.value = 'add';
  if (window.innerWidth < 768) {
    friends_width.value = '0px';
  }
}
export function exit_search_model() {
  current_model.value = 'list';
  friend_search_keyword.value = '';
  current_search_friends.value = [];
}

export function auto_exit_search_model() {
  if (!friend_search_keyword.value) {
    current_model.value = 'list';
    friend_search_keyword.value = '';
    current_search_friends.value = [];
  }
}
export async function auto_handle_search_blur() {
  if (!friend_search_keyword.value) {
    current_model.value = 'list';
    friend_search_keyword.value = '';
    current_search_friends.value = [];
    return;
  }
  search_friend_list();
}
export function back_friends_list() {
  friends_width.value = window.innerWidth < 768 ? window.innerWidth - 60 + 'px' : '300px';
}
export function enter_add_model() {
  current_model.value = 'add';
}
export function exit_add_model() {
  current_model.value = 'list';
  current_new_friend.value = null;
  new_friend_search_keyword.value = '';
}
export async function confirm_delete_friend() {
  if (!current_friend.value.user_id) {
    ElMessage.info('用户状态异常！');
    show_delete_confirm_flag.value = false;
    return;
  }
  const params = {
    friend_id: current_friend.value.user_id
  };
  const res = await delete_friend(params);
  if (!res.error_status) {
    ElMessage.success('删除好友成功！');
    show_delete_confirm_flag.value = false;
    init_current_friend_list();
    current_friend.value = null;
  }
}
export async function search_new_friends_list() {
  if (!new_friend_search_keyword.value) {
    return;
  }
  const params = {
    new_friend_email: new_friend_search_keyword.value
  };
  const res = await search_stranger(params);
  if (!res.error_status) {
    if (res.result) {
      current_new_friend.value = [res.result];
    } else {
      ElMessage.info('未找到该用户！');
      current_new_friend.value = [];
    }
  }
}
export async function auto_handle_add_blur() {
  search_new_friends_list();
}
export async function send_add_friend_request() {
  if (!current_new_friend.value.user_id) {
    ElMessage.info('用户状态异常！');
    return;
  }
  const params = {
    friend_id: current_new_friend.value.user_id
  };
  const res = await add_friend(params);
  if (!res.error_status) {
    ElMessage.success('添加好友请求已发送！');
    const params = {
      new_friend_email: new_friend_search_keyword.value
    };
    const new_friend = await search_stranger(params);
    if (!new_friend.error_status) {
      search_new_friends.value = [new_friend.result];
      current_new_friend.value = new_friend.result;
    }
  }
}

export async function enter_history_model() {
  current_model.value = 'history';
  friend_loading.value = true;
  const history_friends_res = await get_friend_request_history({});
  if (!history_friends_res.error_status) {
    history_friends.value = history_friends_res.result;
  }
  friend_loading.value = false;
  if (window.innerWidth < 768) {
    friends_width.value = '0px';
  }
}
export async function handle_accept(friend_request: FriendRelation) {
  const params = {
    friend_id: friend_request?.user_id
  };
  const res = await accept_friend_request(params);
  if (!res.error_status) {
    ElMessage.success('添加好友成功！');
    init_current_friend_list();
    init_friend_request_cnt();
    friend_loading.value = true;
    const history_friends_res = await get_friend_request_history({});
    if (!history_friends_res.error_status) {
      history_friends.value = history_friends_res.result;
    }
    friend_loading.value = false;
  }
}

export async function handle_reject(friend_request: FriendRelation) {
  const params = {
    friend_id: friend_request?.user_id
  };
  const res = await reject_friend_request(params);
  if (!res.error_status) {
    ElMessage.success('拒绝申请成功！');
    init_friend_request_cnt();
    friend_loading.value = true;
    const history_friends_res = await get_friend_request_history({});
    if (!history_friends_res.error_status) {
      history_friends.value = history_friends_res.result;
    }
    friend_loading.value = false;
  }
}
