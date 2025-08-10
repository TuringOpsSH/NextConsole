import {reactive, ref} from 'vue';
import {
  add_resource_tags,
  batch_create_folders,
  delete_resource_tags,
  get_resource_recent_count,
  get_resource_type_count,
  get_resource_usage,
  resource_share_get_list,
  search_resource_object,
  search_resource_tags,
  update_resource_tags
} from '@/api/resource_api';
import {user_info} from '@/components/user_center/user';
import router from '@/router';
import type Node from 'element-plus/es/components/tree/src/model/node';
import {current_resource, show_resource_list} from '@/components/resource/resource_list/resource_list';
import {ResourceItem, ResourceTag, ResourceUploadItem} from '@/types/resource_type';
import {
  current_tag,
  get_system_tag,
  search_rag_enhance,
  search_resource_by_tags,
  system_tags
} from '@/components/resource/resource_shortcut/resource_shortcut';
import {ElMessage, ElNotification, UploadRequestOptions} from 'element-plus';
import {
  current_resource_tags,
  current_resource_types,
  show_search_config_area
} from '@/components/resource/resource_shortcut/resource_shortcut_head/resource_shortcut_head';
import {
  folder_upload_parent_resource,
  get_task_icon,
  show_upload_manage_box,
  upload_button_Ref,
  upload_file_content,
  upload_file_task_list,
  upload_parent_resource,
  upload_size
} from '@/components/resource/resource_upload/resource_upload';
import {current_share_resource, show_share_resources} from '@/components/resource/share_resources/share_resources';
import {show_upload_folder_dialog} from '@/components/resource/resource_tree/resource_tree';
import {v4 as uuidv4} from 'uuid';
import {sortResourceList, sortShareResourceList} from '@/utils/common';

export const panel_width = ref(window.innerWidth < 768 ? '0px' : '200px');
export const current_resource_usage = ref(0);
export const current_resource_usage_percent = ref(0);
export const panel_show_recent_area = ref(false);
export const panel_show_label_area = ref(false);
export const panel_recent_shortcuts = ref<ResourceTag[]>([]);
export const panel_system_labels = ref<ResourceTag[]>([]);
export const panel_user_labels = ref<ResourceTag[]>([]);
export const panel_show_my_resources_area = ref(false);
export const panel_show_share_resources_area = ref(false);
export const new_tag_form_Ref = ref(null);
export const new_tag_form_data = reactive<ResourceTag>(
  // @ts-ignore
  {
    tag_name: null,
    tag_value: null,
    tag_type: null,
    tag_source: 'user',
    tag_desc: null,
    tag_color: null,
    tag_icon: ''
  }
);
export const new_tag_dialog_flag = ref(false);
export const edit_tag_form_Ref = ref(null);
// @ts-ignore
export const edit_tag_form_data = reactive<ResourceTag>({
  id: null,
  tag_name: null,
  tag_value: null,
  tag_type: null,
  tag_source: 'user',
  tag_desc: null,
  tag_color: null,
  tag_icon: ''
});
export const edit_tag_dialog_flag = ref(false);

export const load_all_flag = ref(false);
export const loading_tags_flag = ref(false);
export const all_search_user_tags = ref<ResourceTag[]>([]);
export const current_search_choose_tag = ref<ResourceTag>(null);
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
    let full_width = window.innerWidth - 60 + 'px';
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
  let params = {};
  let res = await get_resource_usage(params);
  if (!res.error_status) {
    current_resource_usage.value = res.result.usage;
    if (user_info.value?.user_resource_limit) {
      current_resource_usage_percent.value = Math.round(
        (res.result.usage / user_info.value?.user_resource_limit) * 100
      );
    } else {
      current_resource_usage_percent.value = 0;
    }
  }
}
export function show_resource_progress_status() {
  if (current_resource_usage_percent.value < 60) {
    return 'success';
  }
  if (current_resource_usage_percent.value < 80) {
    return 'warning';
  }
  return 'exception';
}
export async function get_recent_data_count() {
  //获取最近数据的数量
  let params = {
    duration: 30,
    recent_shortcuts: panel_recent_shortcuts.value.map(item => item.tag_value)
  };
  let res = await get_resource_recent_count(params);
  if (!res.error_status) {
    panel_recent_shortcuts.value.forEach(item => {
      item.tag_count = res.result[item.tag_value];
    });
  }
}
export async function get_resource_data_count() {
  //获取系统标签的数量
  let params = {};
  let res = await get_resource_type_count(params);
  if (!res.error_status) {
    for (let item of panel_system_labels.value) {
      for (let cnt_obj of res.result) {
        if (item.tag_value == cnt_obj.name) {
          item.tag_count = cnt_obj.cnt;
        }
      }
    }
  }
}
export async function router_to_resource_system_tag(item: ResourceTag) {
  if (window.innerWidth < 768) {
    switch_panel();
  }
  // @ts-ignore
  current_tag.value = get_system_tag(item.tag_value);

  item.tag_active = true;
  // 系统标签处理,只能有一个系统标签激活
  for (let system_tag of panel_recent_shortcuts.value) {
    system_tag.tag_active = false;
    if (system_tag.tag_value == item.tag_value) {
      system_tag.tag_active = true;
      current_tag.value = system_tag;
    }
  }
  for (let system_tag of panel_system_labels.value) {
    system_tag.tag_active = false;
    if (system_tag.tag_value == item.tag_value) {
      system_tag.tag_active = true;
      current_tag.value = system_tag;
    }
  }
  // 资源标签选中的全部保留
  let user_tag_ids = [];
  for (let user_tag of current_resource_tags.value) {
    user_tag_ids.push(user_tag.id);
  }
  if (user_tag_ids.length) {
    show_search_config_area(true);
  }
  // 搜索条件处理, 重置系统类型标签
  if (current_tag.value.tag_type == 'resource_type') {
    current_resource_types.value = [current_tag.value.tag_value];
  }
  // 进入最近区域，去除格式标签
  else if (current_tag.value.tag_type == 'recent') {
    current_resource_types.value = [
      'document',
      'image',
      'webpage',
      'code',
      'folder',
      'video',
      'audio',
      'binary',
      'archive',
      'text',
      'other'
    ];
  }

  let resource_types = [];
  if (current_tag.value.tag_type == 'resource_type') {
    resource_types = [current_tag.value.tag_value];
  } else {
    if (current_resource_types.value?.length != 11) {
      resource_types = current_resource_types.value;
    } else {
      resource_types = [];
    }
  }
  // 如果param没变，则直接replace 并search
  if (router.currentRoute.value.params?.tag_source == 'system') {
    router.push({
      name: 'resource_shortcut',
      params: {
        ...router.currentRoute.value.params
      },
      query: {
        ...router.currentRoute.value.query,
        resource_type: resource_types,
        tag_value: item.tag_value,
        tag_id: user_tag_ids
      }
    });
    search_resource_by_tags();
    return;
  }
  // 如果param变了，则push
  router.push({
    name: 'resource_shortcut',
    params: {
      tag_source: 'system'
    },
    query: {
      ...router.currentRoute.value.query,
      resource_type: resource_types,
      tag_value: item.tag_value,
      tag_id: user_tag_ids
    }
  });
  search_resource_by_tags();
}
export function init_upload_manager() {
  upload_parent_resource.value = current_resource;
  upload_button_Ref.value = upload_file_Ref.value;
}
// 标签部分

export async function router_to_resource_user_tag(item: ResourceTag) {
  // 系统标签处理
  for (let system_tag of panel_recent_shortcuts.value) {
    system_tag.tag_active = false;
  }
  for (let system_tag of panel_system_labels.value) {
    system_tag.tag_active = false;
  }
  // 资源标签处理
  if (item.tag_active == true) {
    // 关闭该标签
    item.tag_active = false;
    for (let i = 0; i < current_resource_tags.value.length; i++) {
      if (current_resource_tags.value[i].id == item.id) {
        current_resource_tags.value.splice(i, 1);
      }
    }
  } else {
    item.tag_active = true;
    current_resource_tags.value.push(item);
  }
  let user_tag_ids = [];
  for (let user_tag of current_resource_tags.value) {
    user_tag_ids.push(user_tag.id);
  }
  // 搜索条件处理
  // 如果param没变，则直接replace 并search
  if (router.currentRoute.value.params?.tag_source == 'user') {
    await router.push({
      name: 'resource_shortcut',
      params: {
        ...router.currentRoute.value.params
      },
      query: {
        ...router.currentRoute.value.query,
        tag_id: user_tag_ids
      }
    });
    await search_resource_by_tags();
    return;
  }
  // 如果param变了，则push
  await router.push({
    name: 'resource_shortcut',
    params: {
      tag_source: 'user'
    },
    query: {
      ...router.currentRoute.value.query,
      tag_id: user_tag_ids
    }
  });
  // 清空当前资源id
  current_resource.id = null;
}
export function init_system_tags(resource_type_max: number = 4) {
  panel_recent_shortcuts.value = [];
  panel_system_labels.value = [];
  let idx = 0;
  for (let system_tag of system_tags) {
    if (system_tag.tag_type == 'recent') {
      //@ts-ignore
      panel_recent_shortcuts.value.push(system_tag);
    } else if (system_tag.tag_type == 'resource_type') {
      //@ts-ignore
      panel_system_labels.value.push(system_tag);
      idx += 1;
      if (idx >= resource_type_max) {
        break;
      }
    }
  }
}
export async function init_user_tags() {
  let params = {
    page_size: 4,
    page_num: 1,
    fetch_all: load_all_flag.value
  };
  let res = await search_resource_tags(params);
  if (!res.error_status) {
    panel_user_labels.value = res.result;
  }
  // 如果query参数中包含tag_id,则设置激活状态
  if (!router.currentRoute.value.query?.tag_id) {
    return;
  }
  for (let user_tag of panel_user_labels.value) {
    for (let tag_id of router.currentRoute.value.query?.tag_id) {
      if (tag_id == user_tag.id.toString()) {
        user_tag.tag_active = true;
      }
    }
  }
}
export async function switch_on_new_tag_dialog() {
  new_tag_dialog_flag.value = true;
  new_tag_form_data.tag_name = '';
  new_tag_form_data.tag_value = '';
  new_tag_form_data.tag_desc = '';
  new_tag_form_data.tag_color = '';
  new_tag_form_data.tag_icon = '';
}
export async function add_new_user_tag() {
  let valid_res = await new_tag_form_Ref.value.validate();
  if (!valid_res) {
    return;
  }
  let params = {
    tag_name: new_tag_form_data.tag_name,
    tag_value: new_tag_form_data.tag_value,
    tag_color: new_tag_form_data.tag_color,
    tag_desc: new_tag_form_data.tag_desc,
    tag_icon: new_tag_form_data.tag_icon
  };
  let res = await add_resource_tags(params);
  if (!res.error_status) {
    new_tag_dialog_flag.value = false;
    ElMessage.success({
      type: 'success',
      message: '标签创建成功！'
    });
    init_user_tags();
  }
}
export async function switch_on_edit_tag_dialog(item: ResourceTag, event: Event) {
  edit_tag_dialog_flag.value = true;
  edit_tag_form_data.id = item.id;
  edit_tag_form_data.tag_name = item.tag_name;
  edit_tag_form_data.tag_value = item.tag_value;
  edit_tag_form_data.tag_desc = item.tag_desc;
  edit_tag_form_data.tag_color = item.tag_color;
  edit_tag_form_data.tag_icon = item.tag_icon;
  // 拦截事件
  event.stopPropagation();
}
export async function edit_new_user_tag() {
  let valid_res = await edit_tag_form_Ref.value.validate();
  if (!valid_res) {
    return;
  }
  let params = {
    tag_id: edit_tag_form_data.id,
    tag_name: edit_tag_form_data.tag_name,
    tag_value: edit_tag_form_data.tag_value,
    tag_color: edit_tag_form_data.tag_color,
    tag_desc: edit_tag_form_data.tag_desc,
    tag_icon: edit_tag_form_data.tag_icon
  };
  let res = await update_resource_tags(params);
  if (!res.error_status) {
    edit_tag_dialog_flag.value = false;
    ElMessage.success({
      type: 'success',
      message: '标签修改成功！'
    });
    init_user_tags();
  }
}
export async function delete_choose_user_tag() {
  let params = {
    tag_list: [edit_tag_form_data.id]
  };
  let res = await delete_resource_tags(params);
  if (!res.error_status) {
    edit_tag_dialog_flag.value = false;
    ElMessage.success({
      type: 'success',
      message: '标签删除成功！'
    });
    init_user_tags();
  }
}
export async function load_all_tags() {
  init_system_tags(20);
  // 加载所有的标签，包括系统标签与资源标签
  let params = {
    fetch_all: true
  };
  let res = await search_resource_tags(params);
  if (!res.error_status) {
    load_all_flag.value = true;
    panel_user_labels.value = res.result;
  }
  // 如果query参数中包含tag_id,则设置激活状态
  for (let user_tag of panel_user_labels.value) {
    if (router.currentRoute.value.query?.tag_id?.length) {
      for (let tag_id of router.currentRoute.value.query?.tag_id) {
        if (tag_id == user_tag.id.toString()) {
          user_tag.tag_active = true;
        }
      }
    }
  }
}
export async function search_resource_tags_by_keyword(query: string) {
  if (query === '') {
    return;
  }
  let params = {
    tag_keyword: query,
    fetch_all: true
  };
  loading_tags_flag.value = true;
  let res = await search_resource_tags(params);
  if (!res.error_status) {
    all_search_user_tags.value = res.result;
  }
  loading_tags_flag.value = false;
}
export async function pick_search_resource_tag() {
  if (!current_search_choose_tag.value) {
    // 清空选择，回到所有标签
    return;
  }
  // 跳转用户选择标签
  router_to_resource_user_tag(current_search_choose_tag.value);
  // 资源标签处理
  let params = {
    tag_id: current_search_choose_tag.value.id,
    tag_click: true
  };
  await update_resource_tags(params);
  await init_user_tags();
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
  let res = await search_resource_object({});
  if (!res.error_status) {
    // my_resource_tree_data.value = [];
    // 先将目录排在前面，剩下的文件按照名称排列
    // for (let item of res.result.data) {
    //   if (item.resource_type == 'folder') {
    //     my_resource_tree_data.value.push({
    //       label: item.resource_name,
    //       leaf: false,
    //       disabled: false,
    //       resource_id: item.id,
    //       resource_type: item.resource_type,
    //       resource_icon: item.resource_icon
    //     });
    //   }
    // }
    // for (let item of res.result.data) {
    //   if (item.resource_type != 'folder') {
    //     my_resource_tree_data.value.push({
    //       label: item.resource_name,
    //       leaf: true,
    //       disabled: false,
    //       resource_id: item.id,
    //       resource_type: item.resource_type,
    //       resource_icon: item.resource_icon
    //     });
    //   }
    // }
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
export async function get_my_resource_tree(node: Node, resolve: (data: Tree[]) => void) {
  // // console.log(node)
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
          resource_icon: item.resource_icon
        });
      }
    }
    for (let item of res.result.data) {
      if (item.resource_type != 'folder') {
        data.push({
          label: item.resource_name,
          leaf: true,
          disabled: false,
          resource_id: item.id,
          resource_type: item.resource_type,
          resource_icon: item.resource_icon
        });
      }
    }
    console.log(res.result.data.length, res.result.total);
    if (res.result.data.length < res.result.total) {
      data.push({
        label: '更多请进入目录查看',
        leaf: true,
        disabled: true,
        resource_id: node.data.resource_id,
        resource_type: 'folder',
        resource_icon: 'images/more.svg'
      });
    }
    resolve(data);
  }
}
export async function router_to_resource(item: Node) {
  if (window.innerWidth < 768) {
    switch_panel();
  }

  if (item.data.resource_type == 'folder') {
    await show_resource_list({
      id: item.data.resource_id,
      user_id: user_info.value.user_id,
      resource_type: item.data.resource_type
    } as ResourceItem);
    return;
  } else {
    router.push({
      name: 'resource_viewer',
      params: {
        resource_id: item.data.resource_id
      }
    });
  }
}
// 共享资源目录部分
export const share_resource_tree_data = ref<Tree[]>([]);
export async function init_share_resource_tree() {
  let res = await resource_share_get_list({});
  sortShareResourceList(res.result.data);
  if (!res.error_status) {
    share_resource_tree_data.value = [];
    // 先将目录排在前面，剩下的文件按照名称排列
    for (let item of res.result.data) {
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
    for (let item of res.result.data) {
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
export async function get_share_resource_tree(node: Node, resolve: (data: Tree[]) => void) {
  if (node.data.resource_type !== 'folder') {
    return resolve([]);
  }
  if (node.disabled) {
    return resolve([]);
  }
  let params = {
    resource_parent_id: node.data.resource_id
  };
  let res = await resource_share_get_list(params);
  if (!res.error_status) {
    let data: Tree[] = [];
    for (let item of res.result.data) {
      if (item.resource.resource_type == 'folder') {
        data.push({
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
    for (let item of res.result.data) {
      if (item.resource.resource_type != 'folder') {
        data.push({
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
    if (res.result.data.length < res.result.total) {
      data.push({
        label: '更多请进入目录查看',
        leaf: true,
        disabled: true,
        resource_id: node.data.resource_id,
        resource_type: 'folder',
        resource_icon: 'images/more.svg'
      });
    }
    resolve(data);
  }
}
export async function router_to_share_resource(item: Node) {
  if (window.innerWidth < 768) {
    switch_panel();
  }
  if (item.data.resource_type == 'folder') {
    await show_share_resources({
      id: item.data.resource_id,
      resource_type: item.data.resource_type
    } as ResourceItem);
  } else {
    router.push({
      name: 'resource_viewer',
      params: {
        resource_id: item.data.resource_id
      }
    });
  }
}
// 回收站部分
export async function router_to_recycle_bin() {
  if (window.innerWidth < 768) {
    switch_panel();
  }
  // @ts-ignore
  current_tag.value = get_system_tag('recycle_bin');
  // 系统标签处理
  for (let system_tag of panel_recent_shortcuts.value) {
    system_tag.tag_active = false;
  }
  for (let system_tag of panel_system_labels.value) {
    system_tag.tag_active = false;
  }
  // 资源标签选中的全部保留
  let user_tag_ids = [];
  for (let user_tag of current_resource_tags.value) {
    user_tag_ids.push(user_tag.id);
  }
  if (user_tag_ids.length) {
    show_search_config_area(true);
  }
  current_resource_types.value = [
    'document',
    'image',
    'webpage',
    'code',
    'folder',
    'video',
    'audio',
    'binary',
    'archive',
    'text',
    'other'
  ];

  router.push({
    name: 'resource_recycle_bin',
    params: {
      tag_source: 'system'
    },
    query: {
      ...router.currentRoute.value.query,
      resource_type: current_resource_types.value,
      tag_value: 'recycle_bin',
      tag_id: user_tag_ids
    }
  });
  search_resource_by_tags();
}

// 搜索资源
export const resource_keyword = ref('');
export const rag_enhance = ref(true);
export async function router_to_search_page() {
  if (window.innerWidth < 768) {
    switch_panel();
  }
  if (!resource_keyword.value) {
    return;
  }
  // 重新赋值
  if (current_tag.value?.tag_value == 'search') {
    current_tag.value.tag_name = resource_keyword.value;
  } else {
    current_tag.value = {
      id: null,
      tag_name: resource_keyword.value,
      tag_value: 'search',
      tag_type: 'search',
      tag_source: 'system',
      tag_desc: null,
      tag_color: null,
      tag_icon: '',
      tag_active: false
    };
  }

  // 系统标签处理
  for (let system_tag of panel_recent_shortcuts.value) {
    system_tag.tag_active = false;
  }
  for (let system_tag of panel_system_labels.value) {
    system_tag.tag_active = false;
  }
  if (router.currentRoute.value.name != 'resource_search') {
    // 资源标签清空
    current_resource_tags.value = [];
    show_search_config_area(false);
    // 资源类型清空
    current_resource_types.value = [
      'document',
      'image',
      'webpage',
      'code',
      'folder',
      'video',
      'audio',
      'binary',
      'archive',
      'text',
      'other'
    ];
  }
  // 资源标签选中的全部保留
  let user_tag_ids = [];
  for (let user_tag of current_resource_tags.value) {
    user_tag_ids.push(user_tag.id);
  }
  if (user_tag_ids.length) {
    show_search_config_area(true);
  }

  let resource_types = [];
  if (current_resource_types.value?.length != 11) {
    resource_types = current_resource_types.value;
  } else {
    resource_types = [];
  }

  // 保存当前路径至localstorage
  localStorage.setItem('current_path', router.currentRoute.value.fullPath);

  router.push({
    name: 'resource_search',
    params: {
      tag_source: 'system'
    },
    query: {
      ...router.currentRoute.value.query,
      resource_type: resource_types,
      resource_keyword: resource_keyword.value,
      tag_value: 'search',
      tag_id: user_tag_ids,
      // @ts-ignore
      rag_enhance: rag_enhance.value
    }
  });
  search_rag_enhance.value = rag_enhance.value;
  await search_resource_by_tags();
  return;
}
export async function handle_search_clear() {
  resource_keyword.value = '';
  let before_path = localStorage.getItem('current_path');

  if (!before_path) {
    await router.push({
      name: 'resource_list'
    });
    return;
  }
  await router.push(before_path);
  localStorage.removeItem('current_path');
}

export async function refresh_panel_count() {
  // // console.log('refresh_panel_count')
  get_current_resource_usage();
  get_recent_data_count();
  get_resource_data_count();
  init_user_tags();
}
export async function router_share_resource() {
  if (window.innerWidth < 768) {
    switch_panel();
  }
  current_share_resource.id = null;
  router.push({
    name: 'resource_share'
  });
}

// 文件夹上传部分
export const folderInput = ref(null);
export function triggerFolderInput() {
  if (router.currentRoute.value.name == 'resource_list') {
    folder_upload_parent_resource.value = current_resource.id;
  }
  folderInput.value.click();
}
export async function handleFolderSelect(event: Event) {
  // 处理文件夹选择
  // @ts-ignore
  let files = event.target?.files;
  // @ts-ignore
  // // console.log(event.target?.files)
  if (!files) {
    ElMessage.error({
      type: 'error',
      message: '文件夹选择失败！'
    });
    return;
  }
  // 检查目标文件夹是否存在
  if (!folder_upload_parent_resource.value) {
    // 打开文件夹选择框
    // console.log('打开文件夹选择框')
    show_upload_folder_dialog(handleFolderSelect, event);
    return;
  }
  // 自动创建所有文件夹
  let folder_list = [];
  for (let file of files) {
    if (file.webkitRelativePath) {
      folder_list.push({
        path: file.webkitRelativePath,
        size: file.size
      });
    }
  }
  let add_folder_params = {
    resource_list: folder_list,
    resource_parent_id: folder_upload_parent_resource.value
  };
  let res = await batch_create_folders(add_folder_params);
  if (!res.error_status) {
    folder_upload_parent_resource.value = null;
  } else {
    ElNotification.error({
      title: '系统通知',
      message: '文件夹创建失败！' + res.error_message,
      duration: 5000
    });
    return;
  }
  // 异步上传所有文件
  // console.log(files)
  for (let file of files) {
    upload_folder_files(file, res.result?.[file.webkitRelativePath]);
  }
}
export async function upload_folder_files(file, parent_id: number) {
  // 上传文件夹中的所有文件
  await prepare_folder_file(file, parent_id);
  await upload_file_content({
    file: file
  } as UploadRequestOptions);
}
export async function prepare_folder_file(uploadFile, parent_id) {
  // 正对于新上传的文件，需要进行一些准备工作，然后生成一个上传任务
  // 如果没有选择父资源，那么需要打开资源选择器
  // console.log('prepare_folder_file',uploadFile)
  show_upload_manage_box.value = true;
  // 1. 计算文件的MD5值
  let fileSHA256 = '';
  try {
    const arrayBuffer = await uploadFile.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    fileSHA256 = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  } catch (e) {
    ElNotification.error({
      title: '系统通知',
      message: '计算文件MD5值失败' + e,
      duration: 5000
    });
    return false;
  }
  if (!fileSHA256) {
    return false;
  }
  // 2. 准备参数
  let resource_size = uploadFile.size / 1024 / 1024;
  let content_max_idx = Math.floor(resource_size / upload_size.value);
  // 前端临时可视化文件类型和格式
  let resource_type = '';
  let resource_format = '';
  if (uploadFile.name.indexOf('.') > -1) {
    resource_format = uploadFile.name.split('.').pop().toLowerCase();
  }
  resource_type = uploadFile.type;
  let task_icon = get_task_icon(resource_type, resource_format);
  uploadFile.uid = uuidv4();
  let new_upload_file_task = <ResourceUploadItem>{
    id: null,
    resource_parent_id: parent_id,
    resource_id: null,
    resource_name: uploadFile.name,
    resource_size_in_mb: resource_size,
    resource_type: resource_type,
    resource_format: resource_format,
    content_max_idx: content_max_idx,
    content_finish_idx: -1,
    resource_md5: fileSHA256,
    raw_file: uploadFile,
    task_icon: task_icon,
    task_status: 'pending'
  };
  upload_file_task_list.value.push(new_upload_file_task);
}
