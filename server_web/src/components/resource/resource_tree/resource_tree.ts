import { reactive, ref } from 'vue';
import { ResourceItem } from '@/types/resource-type';
import { get_init_resource } from '@/components/resource/resource_list/resource_list';
import type Node from 'element-plus/es/components/tree/src/model/node';
import { add_resource_object, move_resources, search_resource_object } from '@/api/resource-api';
import { ElMessage, ElNotification } from 'element-plus';
import {
  close_upload_manager,
  folder_upload_parent_resource,
  upload_file_task_list
} from '@/components/resource/resource_upload/resource_upload';
import { init_my_resource_tree } from '@/components/resource/resource_panel/panel';

export const props = {
  isLeaf: 'leaf',
  disable: 'disabled',
  value: 'id'
};
interface Tree {
  label: string;
  children?: Tree[];
  leaf?: boolean;
  disabled?: boolean;
  resource_type?: string;
  resource_icon?: string;
  resource_id?: number;
  resource_parent_id?: number;
}
export const current_tree_Ref = ref(null);
export const current_callback = ref(null);
export const current_callback_params = ref(null);
export const choose_folder_resource = ref(null);
//@ts-ignore
export const new_resource_dir = reactive<ResourceItem>({
  id: null,
  resource_parent_id: null,
  user_id: null,
  resource_name: null,
  resource_type: null,
  resource_desc: null,
  resource_icon: null,
  resource_format: null,
  rag_status: null,
  resource_size_in_MB: null,
  resource_status: null,
  create_time: null,
  update_time: null,
  delete_time: null,
  show_buttons: null,
  resource_parent_name: null,
  resource_is_selected: null,
  sub_resource_dir_cnt: null,
  sub_resource_file_cnt: null,
  resource_path: '',
  sub_rag_file_cnt: 0,
  resource_show_url: null,
  resource_is_supported: false
});
export const add_new_dir_dialog_flag = ref(false);
export function convert_to_single_choose(a, b) {
  // 手动将其余选中节点取消选中，只保留当前节点
  choose_folder_resource.value = a;
}

// 选择移动文件夹
export const show_mv_resource_tree = ref(false);
export const current_move_resource_list = ref<number[]>([]);
export const resource_mv_tree_data = ref<Tree[]>([]);
export const resource_mv_tree_Ref = ref(null);
export const mv_confirm_flag = ref(false);

export async function show_move_dialog_multiple(resource_list: number[], callback?: () => Promise<any>) {
  show_mv_resource_tree.value = true;
  current_move_resource_list.value = resource_list;
  // 获取第一层目录
  let res = await search_resource_object({});
  if (!res.error_status) {
    resource_mv_tree_data.value = [];
    // 先添加根目录
    if (res.result?.root) {
      resource_mv_tree_data.value.push({
        label: res.result.root.resource_name,
        leaf: false,
        disabled: false,
        resource_id: res.result.root.id,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: res.result.root.resource_parent_id,
        children: []
      });
      // 目录不能移动到自身
      if (resource_list.includes(res.result.root.id)) {
        resource_mv_tree_data.value[resource_mv_tree_data.value.length - 1].disabled = true;
      }
      // 先添加目录

      for (let item of res.result.data) {
        if (item.resource_type == 'folder') {
          resource_mv_tree_data.value[0].children.push({
            label: item.resource_name,
            leaf: false,
            disabled: false,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id
          });
          // 目录不能移动到自身
          if (resource_list.includes(item.id)) {
            resource_mv_tree_data.value[resource_mv_tree_data.value.length - 1].disabled = true;
          }
        }
      }
      for (let item of res.result.data) {
        if (item.resource_type != 'folder') {
          resource_mv_tree_data.value[0].children.push({
            label: item.resource_name,
            leaf: true,
            disabled: true,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id
          });
        }
      }
    }
  }
  current_callback.value = callback;
}
export async function get_move_resource_tree(node: Node, resolve: (data: Tree[]) => void) {
  // 获得下一层目录，并标记叶子节点，不可用目录
  if (node.data.resource_type !== 'folder') {
    return resolve([]);
  }
  if (node.level !== 1 && node.disabled) {
    return resolve([]);
  }
  let params = {
    resource_parent_id: node.data.resource_id
  };
  let res = await search_resource_object(params);
  if (!res.error_status) {
    let data: Tree[] = [];
    for (let item of res.result.data) {
      if (item.resource_type == 'folder') {
        data.push({
          label: item.resource_name,
          leaf: false,
          disabled: false,
          resource_id: item.id,
          resource_type: item.resource_type,
          resource_icon: item.resource_icon,
          resource_parent_id: item.resource_parent_id
        });
        // 目录不能移动到自身
        if (current_move_resource_list.value.includes(item.id)) {
          data[data.length - 1].disabled = true;
        }
      }
    }
    for (let item of res.result.data) {
      if (item.resource_type != 'folder') {
        data.push({
          label: item.resource_name,
          leaf: true,
          disabled: true,
          resource_id: item.id,
          resource_type: item.resource_type,
          resource_icon: item.resource_icon,
          resource_parent_id: item.resource_parent_id
        });
      }
    }
    resolve(data);
  }
}
export function mv_double_check() {
  // 如果目标资源不是文件夹，则提醒选择文件夹
  if (choose_folder_resource.value.resource_type !== 'folder') {
    ElNotification({
      title: '系统通知',
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }

  mv_confirm_flag.value = true;
}
export async function confirm_mv_resource() {
  // 确认移动资源

  let params = {
    resource_id_list: current_move_resource_list.value,
    target_resource_id: choose_folder_resource.value.resource_id
  };

  // 目标文件夹不能在移动资源中
  if (params.resource_id_list.includes(params.target_resource_id)) {
    ElNotification({
      title: '错误',
      message: '不能移动到自身',
      type: 'error'
    });
    return;
  }

  let res = await move_resources(params);
  if (!res.error_status) {
    show_mv_resource_tree.value = false;
    mv_confirm_flag.value = false;
    ElMessage.success('移动成功');
  }
  if (current_callback.value) {
    await current_callback.value();
  }
  init_my_resource_tree();
}
// 新建文件夹
export function show_add_new_dir_dialog(current_tree_ref: any) {
  add_new_dir_dialog_flag.value = true;
  Object.assign(new_resource_dir, get_init_resource());
  new_resource_dir.resource_type = 'folder';
  current_tree_Ref.value = current_tree_ref;
}
export async function add_new_dir() {
  let pick_resource = current_tree_Ref.value.getCurrentNode();
  let params = {
    resource_name: new_resource_dir.resource_name,
    resource_desc: new_resource_dir.resource_desc,
    resource_type: 'folder',
    resource_parent_id: pick_resource?.resource_id
  };
  let res = await add_resource_object(params);
  if (!res.error_status) {
    add_new_dir_dialog_flag.value = false;
    // 触发树节点新增
    current_tree_Ref.value.append(
      {
        label: res.result.resource_name,
        leaf: true,
        disabled: false,
        resource_id: res.result.id,
        resource_type: res.result.resource_type,
        resource_icon: res.result.resource_icon
      },
      pick_resource
    );
  }
}

// 选择上传文件夹
export const show_upload_resource_tree = ref(false);
export const upload_confirm_flag = ref(false);
export const resource_upload_tree_data = ref<Tree[]>([]);
export const resource_upload_tree_Ref = ref(null);
export async function show_upload_dialog_multiple(callback?: () => Promise<any>) {
  show_upload_resource_tree.value = true;
  // 获取第一层目录
  let res = await search_resource_object({});
  if (!res.error_status) {
    resource_upload_tree_data.value = [
      {
        label: res.result.root.resource_name,
        leaf: false,
        disabled: false,
        resource_id: res.result.root.id,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: res.result.root.resource_parent_id,
        children: []
      }
    ];
    // 先添加目录
    // for (let item of res.result.data){
    //     if (item.resource_type == 'folder'){
    //         resource_upload_tree_data.value[0].children.push({
    //             label: item.resource_name,
    //             leaf: false,
    //             disabled: false,
    //             resource_id: item.id,
    //             resource_type: item.resource_type,
    //             resource_icon: item.resource_icon,
    //             resource_parent_id : item.resource_parent_id
    //         })
    //     }
    //
    // }
    // for (let item of res.result.data){
    //     if (item.resource_type != 'folder'){
    //         resource_upload_tree_data.value[0].children.push({
    //             label: item.resource_name,
    //             leaf: true,
    //             disabled: true,
    //             resource_id: item.id,
    //             resource_type: item.resource_type,
    //             resource_icon: item.resource_icon,
    //             resource_parent_id : item.resource_parent_id
    //         })
    //     }
    // }
  }
  current_callback.value = callback;
}
export async function get_upload_resource_tree(node: Node, resolve: (data: Tree[]) => void) {
  // 获得下一层目录，并标记叶子节点，不可用目录
  if (node.data.resource_type !== 'folder') {
    return resolve([]);
  }
  if (node.disabled) {
    return resolve([]);
  }
  let params = {
    resource_parent_id: node.data.resource_id
  };
  let res = await search_resource_object(params);
  if (!res.error_status) {
    let data: Tree[] = [];
    for (let item of res.result.data) {
      if (item.resource_type == 'folder') {
        data.push({
          label: item.resource_name,
          leaf: false,
          disabled: false,
          resource_id: item.id,
          resource_type: item.resource_type,
          resource_icon: item.resource_icon,
          resource_parent_id: item.resource_parent_id
        });
      }
    }
    for (let item of res.result.data) {
      if (item.resource_type != 'folder') {
        data.push({
          label: item.resource_name,
          leaf: true,
          disabled: true,
          resource_id: item.id,
          resource_type: item.resource_type,
          resource_icon: item.resource_icon,
          resource_parent_id: item.resource_parent_id
        });
      }
    }
    resolve(data);
  }
}
export function upload_double_check() {
  // 触发上传资源的回调
  if (!choose_folder_resource.value?.resource_id) {
    ElNotification({
      title: '系统通知',
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }
  // 如果目标资源不是文件夹，则提醒选择文件夹
  if (choose_folder_resource.value.resource_type !== 'folder') {
    ElNotification({
      title: '系统通知',
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }
  upload_confirm_flag.value = true;
}
export async function confirm_upload_resource() {
  show_upload_resource_tree.value = false;
  upload_confirm_flag.value = false;
  for (let task of upload_file_task_list.value) {
    if (task.resource_parent_id === null && !task.id) {
      task.resource_parent_id = choose_folder_resource.value.resource_id;
    }
  }
  if (current_callback.value) {
    await current_callback.value();
  }
}
export async function cancel_upload_resource() {
  show_upload_resource_tree.value = false;
  close_upload_manager(false);
}

// 选择文件夹上传的父文件夹
export const show_upload_folder_tree = ref(false);
export const upload_folder_confirm_flag = ref(false);
export const folder_upload_tree_data = ref<Tree[]>([]);
export const folder_upload_tree_Ref = ref(null);
export async function show_upload_folder_dialog(callback?: (params?: any) => Promise<void>, params?: any) {
  show_upload_folder_tree.value = true;
  // 获取第一层目录
  let res = await search_resource_object({});
  if (!res.error_status) {
    folder_upload_tree_data.value = [];
    // 先添加根目录
    if (res.result?.root) {
      folder_upload_tree_data.value.push({
        label: res.result.root.resource_name,
        leaf: false,
        disabled: false,
        resource_id: res.result.root.id,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: res.result.root.resource_parent_id,
        children: []
      });
      // 先添加目录
      for (let item of res.result.data) {
        if (item.resource_type == 'folder') {
          folder_upload_tree_data.value[0].children.push({
            label: item.resource_name,
            leaf: false,
            disabled: false,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id
          });
        }
      }
      for (let item of res.result.data) {
        if (item.resource_type != 'folder') {
          folder_upload_tree_data.value[0].children.push({
            label: item.resource_name,
            leaf: true,
            disabled: true,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id
          });
        }
      }
    }
  }
  current_callback.value = callback;
  current_callback_params.value = params;
  // // console.log('打开文件夹选择框')
}
export function folder_upload_double_check() {
  if (!choose_folder_resource.value?.resource_id) {
    ElNotification({
      title: '系统通知',
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }
  // 如果目标资源不是文件夹，则提醒选择文件夹
  if (choose_folder_resource.value.resource_type !== 'folder') {
    ElNotification({
      title: '系统通知',
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }
  upload_folder_confirm_flag.value = true;
}
export async function confirm_upload_folder() {
  show_upload_folder_tree.value = false;
  upload_folder_confirm_flag.value = false;
  folder_upload_parent_resource.value = choose_folder_resource.value.resource_id;
  if (current_callback.value) {
    // 触发回调
    await current_callback.value(current_callback_params.value);
  }
}
export async function cancel_upload_folder() {
  show_upload_folder_tree.value = false;
  close_upload_manager(false);
}
