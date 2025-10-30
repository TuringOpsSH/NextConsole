import { ref } from 'vue';
import {
  get_resource_recent_count,
  get_resource_type_count,
  get_resource_usage,
  resource_share_get_list,
  search_resource_object,
  search_resource_tags
} from '@/api/resource-api';
import { current_resource } from '@/components/resource/resource-list/resource_list';
import {
  folder_upload_parent_resource,
  upload_button_Ref,
  upload_parent_resource
} from '@/components/resource/resource-upload/resource-upload';
import router from '@/router';
import { useUserInfoStore } from '@/stores/user-info-store';
import { IResourceTag } from '@/types/resource-type';
import { sortResourceList, sortShareResourceList } from '@/utils/common';

export const panel_width = ref(window.innerWidth < 768 ? '0px' : '200px');
export const current_resource_usage = ref(0);
export const current_resource_usage_percent = ref(0);
export const panel_recent_shortcuts = ref<IResourceTag[]>([]);
export const panel_system_labels = ref<IResourceTag[]>([]);
export const panel_user_labels = ref<IResourceTag[]>([]);
export const panel_show_my_resources_area = ref(false);
export const panel_show_share_resources_area = ref(false);
export const load_all_flag = ref(false);
export const upload_file_Ref = ref(null);
export const tag_color_list = [
  {
    id: 1,
    name: '红色',
    value: '#FF3B30'
  },
  {
    id: 2,
    name: '橙色',
    value: '#FF9500'
  },
  {
    id: 3,
    name: '黄色',
    value: '#FFCC00'
  },
  {
    id: 4,
    name: '绿色',
    value: '#34C759'
  },
  {
    id: 5,
    name: '蓝色',
    value: '#007AFF'
  },
  {
    id: 6,
    name: '紫色',
    value: '#AF52DE'
  },
  {
    id: 7,
    name: '灰色',
    value: '#8E8E93'
  }
];
export const show_upload_button = ref(null);
export async function switch_panel(status: string = null) {
  if (window.innerWidth < 768) {
    const full_width = window.innerWidth - 60 + 'px';
    if (!status) {
      panel_width.value = panel_width.value === full_width ? '0px' : full_width;
    } else if (status == 'close') {
      panel_width.value = '0px';
    }
    return;
  }
  panel_width.value = panel_width.value === '200px' ? '0px' : '200px';
  if (panel_width.value == '0px') {
    router.replace({
      query: {
        ...router.currentRoute.value.query,
        resource_panel: ''
      }
    });
  } else {
    router.replace({
      query: {
        ...router.currentRoute.value.query,
        resource_panel: 'true'
      }
    });
  }
}
export async function get_current_resource_usage() {
  const params = {};
  const res = await get_resource_usage(params);
  if (!res.error_status) {
    current_resource_usage.value = res.result.usage;
    const userInfoStore = useUserInfoStore();
    if (userInfoStore.userInfo?.user_resource_limit) {
      current_resource_usage_percent.value = Math.round(
        (res.result.usage / userInfoStore.userInfo?.user_resource_limit) * 100
      );
    } else {
      current_resource_usage_percent.value = 0;
    }
  }
}
export async function get_recent_data_count() {
  //获取最近数据的数量
  const params = {
    duration: 30,
    recent_shortcuts: panel_recent_shortcuts.value.map(item => item.tag_value)
  };
  const res = await get_resource_recent_count(params);
  if (!res.error_status) {
    panel_recent_shortcuts.value.forEach(item => {
      item.tag_count = res.result[item.tag_value];
    });
  }
}
export async function get_resource_data_count() {
  //获取系统标签的数量
  const params = {};
  const res = await get_resource_type_count(params);
  if (!res.error_status) {
    for (const item of panel_system_labels.value) {
      for (const cnt_obj of res.result) {
        if (item.tag_value == cnt_obj.name) {
          item.tag_count = cnt_obj.cnt;
        }
      }
    }
  }
}
export function init_upload_manager() {
  upload_parent_resource.value = current_resource;
  upload_button_Ref.value = upload_file_Ref.value;
}
// 标签部分
export async function init_user_tags() {
  const params = {
    page_size: 4,
    page_num: 1,
    fetch_all: load_all_flag.value
  };
  const res = await search_resource_tags(params);
  if (!res.error_status) {
    panel_user_labels.value = res.result;
  }
  // 如果query参数中包含tag_id,则设置激活状态
  if (!router.currentRoute.value.query?.tag_id) {
    return;
  }
  for (const user_tag of panel_user_labels.value) {
    for (const tag_id of router.currentRoute.value.query?.tag_id) {
      if (tag_id == user_tag.id.toString()) {
        user_tag.tag_active = true;
      }
    }
  }
}
// 我的资源目录部分
interface Tree {
  label: string;
  children?: Tree[];
  leaf?: boolean;
  disabled?: boolean;
  resource_type?: string;
  resource_icon?: string;
  resource_id?: number;
  auth_type?: string;
}
export const my_resource_tree_props = {
  isLeaf: 'leaf',
  disable: 'disabled'
};
export const my_resource_tree_data = ref<Tree[]>([]);
export async function init_my_resource_tree() {
  const res = await search_resource_object({});
  if (!res.error_status) {
    // 排序
    sortResourceList(res.result?.data);
    my_resource_tree_data.value = res.result.data.map(item => ({
      label: item.resource_name,
      leaf: item.resource_type !== 'folder',
      disabled: false,
      resource_id: item.id,
      resource_type: item.resource_type,
      resource_icon: item.resource_icon
    }));
  }
}
// 共享资源目录部分
export const share_resource_tree_data = ref<Tree[]>([]);
export async function init_share_resource_tree() {
  const res = await resource_share_get_list({});
  sortShareResourceList(res.result.data);
  if (!res.error_status) {
    share_resource_tree_data.value = [];
    // 先将目录排在前面，剩下的文件按照名称排列
    for (const item of res.result.data) {
      if (item.resource.resource_type == 'folder') {
        share_resource_tree_data.value.push({
          label: item.resource.resource_name,
          leaf: false,
          disabled: false,
          resource_id: item.resource.id,
          resource_type: item.resource.resource_type,
          resource_icon: item.resource.resource_icon,
          auth_type: item.auth_type
        });
      }
    }
    for (const item of res.result.data) {
      if (item.resource.resource_type != 'folder') {
        share_resource_tree_data.value.push({
          label: item.resource.resource_name,
          leaf: true,
          disabled: false,
          resource_id: item.resource.id,
          resource_type: item.resource.resource_type,
          resource_icon: item.resource.resource_icon,
          auth_type: item.auth_type
        });
      }
    }
  }
}
// 搜索资源
export const resource_keyword = ref('');
export async function handle_search_clear() {
  resource_keyword.value = '';
  const beforePath = localStorage.getItem('current_path');

  if (!beforePath) {
    await router.push({
      name: 'resource_list'
    });
    return;
  }
  await router.push(beforePath);
  localStorage.removeItem('current_path');
}
export async function refresh_panel_count() {
  // // console.log('refresh_panel_count')
  get_current_resource_usage();
  get_recent_data_count();
  get_resource_data_count();
  init_user_tags();
}
// 文件夹上传部分
export const folderInput = ref(null);
export function triggerFolderInput() {
  if (router.currentRoute.value.name == 'resource_list') {
    folder_upload_parent_resource.value = current_resource.id;
  }
  folderInput.value.click();
}
