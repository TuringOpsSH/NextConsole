import { nextTick, reactive, ref } from 'vue';
import { get_system_notices, set_system_notices_read } from '@/api/user_center';
import { SystemNotice } from '@/types/users';

export const menuData = reactive([
  {
    icon: 'presentation_chart_02_grey.svg',
    active_icon: 'presentation_chart_02_blue.svg',
    text: '监控中心',
    is_active: false,
    name: 'user_activity'
  },
  {
    icon: 'heart_circle_grey.svg',
    active_icon: 'heart_circle_blue.svg',
    text: '反馈中心',
    is_active: false,
    name: 'search_model'
  },
  {
    icon: 'user_01_grey.svg',
    active_icon: 'user_01_blue.svg',
    text: '用户管理',
    is_active: false,
    name: 'user_manage'
  },
  {
    icon: 'app_center_grey.svg',
    active_icon: 'app_center_blue.svg',
    text: 'AI应用工厂',
    is_active: false,
    name: 'appCenter'
  }
]);

export const userButtonData = reactive([
  {
    icon: 'user_center.svg',
    active_icon: 'console_blue.svg',
    text: '用户中心',
    is_active: false,
    name: 'next_console_user_info',
    new_window: false
  },
  {
    icon: 'logo.svg',
    active_icon: 'logo.svg',
    text: '服务端',
    is_active: false,
    url: '',
    name: 'server_app',
    new_window: true
  },
  {
    icon: 'book-open.svg',
    active_icon: 'logo.svg',
    text: '使用文档',
    is_active: false,
    url: 'https://docs.nextconsole.cn',
    name: 'contract',
    new_window: true
  },
  {
    icon: 'privacy.svg',
    active_icon: 'privacy.svg',
    text: '隐私说明',
    is_active: false,
    name: 'privacy_policy',
    new_window: true
  },
  {
    icon: 'documents.svg',
    active_icon: 'documents.svg',
    text: '用户协议',
    is_active: false,
    name: 'contract',
    new_window: true
  }
]);

export const currentSystemNoticeType = ref('unread');
export const unread_system_notice = ref<SystemNotice[]>([]);
export const all_system_notice = ref<SystemNotice[]>([]);
export const current_page_size = ref(50);
export const current_page_num = ref(1);

export async function set_all_notice_read() {
  const params = {
    read_all: true
  };
  const res = await set_system_notices_read(params);
  unread_system_notice.value = [];
}

export async function change_notice_type(target_type: string = 'unread') {
  currentSystemNoticeType.value = target_type;
  if (target_type == 'unread') {
    const params = {
      fetch_all: true,
      status: '未读'
    };
    const res = await get_system_notices(params);
    unread_system_notice.value = res.result;
  } else {
    const params = {
      page_size: 50,
      page_num: 1
    };
    const res = await get_system_notices(params);
    all_system_notice.value = res.result;
  }
}

export function get_notice_icon(notice_icon_url: string) {
  if (!notice_icon_url) {
    return '';
  }
  if (notice_icon_url.startsWith('http')) {
    return notice_icon_url;
  }
  if (notice_icon_url.startsWith('images/')) {
    return notice_icon_url;
  }
  if (notice_icon_url.includes('data:image')) {
    return notice_icon_url;
  }

  return 'images/' + notice_icon_url;
}

export async function set_notice_read(notice: SystemNotice) {
  const params = {
    notice_id: notice.id
  };
  const res = await set_system_notices_read(params);
  if (!res.error_status) {
    notice.notice_status = '已读';
    // 更新消息队列
    if (currentSystemNoticeType.value == 'unread') {
      await change_notice_type(currentSystemNoticeType.value);
    }
  }
}

export async function load_more_notice() {
  current_page_num.value += 1;
  const params = {
    page_size: current_page_size.value,
    page_num: current_page_num.value
  };
  const res = await get_system_notices(params);
  for (const notice of res.result) {
    // 只添加不重复的消息
    let is_exist = false;
    for (const exist_notice of all_system_notice.value) {
      if (exist_notice.id == notice.id) {
        is_exist = true;
        break;
      }
    }
    if (!is_exist) {
      all_system_notice.value.push(notice);
    }
  }
}
