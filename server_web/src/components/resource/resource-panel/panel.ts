import { ref } from 'vue';
import { resource_share_get_list, search_resource_object } from '@/api/resource-api';
import { current_resource } from '@/components/resource/resource-list/resource-list';
import {
  folder_upload_parent_resource,
  upload_button_Ref,
  upload_parent_resource
} from '@/components/resource/resource-upload/resource-upload';
import router from '@/router';

import { sortResourceList, sortShareResourceList } from '@/utils/common';

export const upload_file_Ref = ref(null);

export const show_upload_button = ref(null);

export function init_upload_manager() {
  upload_parent_resource.value = current_resource;
  upload_button_Ref.value = upload_file_Ref.value;
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

// 文件夹上传部分
export const folderInput = ref(null);
export function triggerFolderInput() {
  if (router.currentRoute.value.name == 'resource_list') {
    folder_upload_parent_resource.value = current_resource.id;
  }
  folderInput.value.click();
}
