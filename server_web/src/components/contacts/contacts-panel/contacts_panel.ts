import {ref} from 'vue';
import {get_company_info, get_friend_request_cnt} from '@/api/contacts';
import router from '@/router';
import {Company} from '@/types/contacts';

export const panel_width = ref(window.innerWidth < 768 ? window.innerWidth - 60 + 'px' : '200px');
export function switch_panel() {
  if (window.innerWidth < 768) {
    if (panel_width.value === '0px') {
      panel_width.value = window.innerWidth - 60 + 'px';
    } else {
      panel_width.value = '0px';
    }
    return;
  }
  panel_width.value = panel_width.value === '200px' ? '0px' : '200px';
}

export const current_friend_request_cnt = ref(0);
// @ts-ignore
export const current_company = ref<Company>({});

export async function router_to_company_structure() {
  router.push({ name: 'company_structure' });
  if (window.innerWidth < 768) {
    panel_width.value = '0px';
  }
}
export async function router_to_friends() {
  router.push({ name: 'friends' });
  if (window.innerWidth < 768) {
    panel_width.value = '0px';
  }
}
export async function router_to_groups_chat() {
  router.push({ name: 'groups_chat' });
}

export async function init_friend_request_cnt() {
  const res = await get_friend_request_cnt({});
  if (!res.error_status) {
    current_friend_request_cnt.value = res.result;
  }
}
