import { nextTick, reactive, ref } from 'vue';
import { SystemNotice } from '@/types/users';
import { get_system_notices, set_system_notices_read } from '@/api/user_center';
import { getToken } from '@/utils/auth';

export const menu_data = reactive([
    {
        icon: 'console_grey.svg',
        active_icon: 'console_blue.svg',
        text: 'AI工作台',
        is_active: false,
        name: 'next_console_welcome_home',
        path: '/next_console/console',
        rootName: 'console'
    },
    {
        icon: 'contacts_grey.svg',
        active_icon: 'contacts_blue.svg',
        text: '通讯录',
        is_active: false,
        name: 'contacts',
        path: '/next_console/contacts',
        rootName: 'contacts'
    },

    {
        icon: 'folder_grey.svg',
        active_icon: 'folder_blue.svg',
        text: 'AI资源库',
        is_active: false,
        name: 'resource_list',
        path: '/next_console/resources/resource_list',
        rootName: 'resources'
    }
]);

export const user_button_data = reactive([
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
        text: '管理端',
        is_active: false,
        url: '',
        name: 'admin_app',
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

export const current_system_notice_type = ref('unread');
export const unread_system_notice = ref<SystemNotice[]>([]);
export const all_system_notice = ref<SystemNotice[]>([]);
export const current_page_size = ref(50);
export const current_page_num = ref(1);
export async function init_system_notice() {
    let params = {
        fetch_all: true,
        status: '未读'
    };
    let res = await get_system_notices(params);
    unread_system_notice.value = res.result;
}

export async function set_all_notice_read() {
    let params = {
        read_all: true
    };
    let res = await set_system_notices_read(params);
    unread_system_notice.value = [];
}

export async function change_notice_type(target_type: string = 'unread') {
    current_system_notice_type.value = target_type;
    if (target_type == 'unread') {
        let params = {
            fetch_all: true,
            status: '未读'
        };
        let res = await get_system_notices(params);
        unread_system_notice.value = res.result;
    } else {
        let params = {
            page_size: 50,
            page_num: 1
        };
        let res = await get_system_notices(params);
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
    let params = {
        notice_id: notice.id
    };
    let res = await set_system_notices_read(params);
    if (!res.error_status) {
        notice.notice_status = '已读';
        // 更新消息队列
        if (current_system_notice_type.value == 'unread') {
            await change_notice_type(current_system_notice_type.value);
        }
    }
}

export async function load_more_notice() {
    current_page_num.value += 1;
    let params = {
        page_size: current_page_size.value,
        page_num: current_page_num.value
    };
    let res = await get_system_notices(params);
    for (let notice of res.result) {
        // 只添加不重复的消息
        let is_exist = false;
        for (let exist_notice of all_system_notice.value) {
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
