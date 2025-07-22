import router from '@/router';
import {ResourceItem} from '@/types/resource_type';
import {reactive, ref} from 'vue';
import {
  add_resource_object,
  batch_delete_resource_object,
  batch_download_resources,
  build_resource_object_ref,
  delete_resource_object_api,
  download_resource_object,
  get_resource_object,
  get_resource_object_path,
  move_resources,
  search_resource_object
} from '@/api/resource_api';
import {
  add_dir_dialog_flag,
  add_document_flag,
  current_path_tree,
  new_dir_form_Ref,
  new_dir_form_valid
} from '@/components/resource/resource_list/resource_head/resource_head';
import {ElMessage, ElNotification} from 'element-plus';
import {show_move_dialog_multiple} from '@/components/resource/resource_tree/resource_tree';
import {push_to_clipboard} from '@/components/resource/resource_clipborad/resource_clipboard';
import {turn_on_resource_meta} from '@/components/resource/resource_meta/resource_meta';
import {init_my_resource_tree, refresh_panel_count} from '@/components/resource/resource_panel/panel';
import {check_resource_rag_support} from '@/components/resource/resource_main';
import {turn_on_share_selector} from '@/components/resource/resource_share_selector/resource_share_selector';
import {user_info} from '@/components/user_center/user';
import {show_share_resources} from '@/components/resource/share_resources/share_resources';
import {sortResourceList} from '@/utils/common';

export const resource_list_Ref = ref(null);
export const resource_view_model = ref('list');
export const current_resource = reactive<ResourceItem>(
  // @ts-ignore
  {
    sub_rag_file_cnt: 0,
    id: null,
    resource_parent_id: null,
    user_id: null,
    resource_name: null,
    resource_type: null,
    resource_desc: null,
    resource_icon: null,
    resource_format: null,
    resource_path: null,
    resource_size_in_MB: null,
    resource_status: null,
    rag_status: null,
    create_time: null,
    update_time: null,
    delete_time: null,
    show_buttons: null,
    resource_parent_name: null,
    resource_is_selected: null,
    sub_resource_dir_cnt: null,
    sub_resource_file_cnt: null,
    resource_feature_code: '',
    resource_is_supported: false,
    resource_show_url: '',
    resource_source_url: '',
    resource_title: '',
    resource_source: 'resource_center',
    ref_text: null,
    rerank_score: null
  }
);
export const current_resource_list = ref<ResourceItem[]>([]);
export const new_dir_resource_item = reactive<ResourceItem>(
  // @ts-ignore
  {
    id: null,
    resource_parent_id: null,
    user_id: null,
    resource_name: null,
    resource_type: null,
    resource_desc: null,
    resource_icon: null,
    resource_format: null,
    resource_path: null,
    resource_size_in_MB: null,
    resource_status: null,
    rag_status: null,
    create_time: null,
    update_time: null,
    delete_time: null,
    show_buttons: null,
    resource_parent_name: null,
    resource_is_selected: null,
    sub_resource_dir_cnt: null,
    sub_resource_file_cnt: null,
    sub_rag_file_cnt: 0,
    resource_feature_code: '',
    resource_is_supported: false,
    resource_show_url: '',
    resource_source_url: '',
    resource_title: '',
    resource_source: 'resource_center',
    ref_text: null,
    rerank_score: null
  }
);

export const resource_loading = ref(false);

export const resource_list_buttons_Ref = ref();
export const multiple_selection = ref<ResourceItem[]>([]);
export const show_multiple_button = ref(false);
export const show_delete_flag = ref(false);
export const delete_dialog_title = ref('删除资源');
export const resource_list_card_buttons_Ref = ref();
export const current_page_num = ref(1);
export const current_page_size = ref(50);
export const current_total = ref(0);
export const el_scrollbar_Ref = ref(null);
export const resource_list_scroll_Ref = ref(null);
export const resource_card_scroll_Ref = ref(null);
// 新建文档
export const new_document_resource = reactive<ResourceItem>({
  resource_format: 'docx'
});
export const new_document_form_Ref = ref(null);

export const resourceDetailRef = ref(null);

export function get_init_resource() {
  return <ResourceItem>{
    id: null,
    resource_parent_id: null,
    user_id: null,
    resource_name: null,
    resource_type: null,
    resource_desc: null,
    resource_icon: null,
    resource_format: null,
    resource_path: null,
    resource_size_in_MB: null,
    resource_status: null,
    rag_status: null,
    create_time: null,
    update_time: null,
    delete_time: null,
    show_buttons: null,
    resource_parent_name: null,
    resource_is_selected: null,
    sub_resource_dir_cnt: null,
    sub_resource_file_cnt: null,
    sub_rag_file_cnt: 0
  };
}

export async function show_resource_list(item: ResourceItem | null = null) {
  // 面板跳转
  // console.log('开始跳转', Date.now())
  resource_loading.value = true;
  current_resource.id = null;
  multiple_selection.value = [];
  current_page_num.value = 1;
  current_page_size.value = 50;
  current_total.value = 0;
  console.log(item);
  if (item.user_id == user_info.value.user_id) {
    if (item.resource_type == 'folder') {
      router.push({
        name: 'resource_list',
        query: {
          ...router.currentRoute.value.query
        },
        params: {
          ...router.currentRoute.value.params,
          resource_id: item?.id
        }
      });

      await get_current_resource_object(item.id);
      search_all_resource_object();
      get_parent_resource_list();
    } else {
      await preview_resource(item);
    }
  } else {
    await show_share_resources(item);
  }
  resource_loading.value = false;
  // console.log('完成跳转', Date.now())
}

export async function get_current_resource_object(resource_id: string | number | null = null) {
  let params = {
    resource_id: resource_id
  };
  let res = await get_resource_object(params);
  if (!res.error_status) {
    Object.assign(current_resource, res.result);
  }
}

export async function search_all_resource_object() {
  // 搜索所有资源对象并展示（抬头搜索框，类型过滤按钮）
  let search_params = {
    resource_parent_id: current_resource.id
  };
  resource_loading.value = true;
  let res = await search_resource_object(search_params);
  if (!res.error_status) {
    current_total.value = res.result.total;
    // 排序
    sortResourceList(res.result?.data);
    current_resource_list.value = res.result?.data;
    resource_list_Ref.value?.clearSelection();
  }
  resource_loading.value = false;
}

export async function search_all_resource_object_next(scroll_position: object) {
  if (resource_loading.value) {
    return;
  }
  if (current_total.value && current_total.value <= current_resource_list.value.length) {
    return;
  }
  if (resource_view_model.value == 'card') {
    // @ts-ignore
    if (scroll_position.scrollTop + window.innerHeight - 120 > resource_card_scroll_Ref.value.clientHeight - 10) {
      // 下一页
      current_page_num.value += 1;
      let search_params = {
        resource_parent_id: current_resource.id,
        page_num: current_page_num.value,
        page_size: current_page_size.value
      };
      resource_loading.value = true;
      let res = await search_resource_object(search_params);
      if (!res.error_status) {
        current_total.value = res.result.total;
        for (let resource of res.result.data) {
          // 去重添加
          let find_flag = false;
          for (let item of current_resource_list.value) {
            if (item.id == resource.id) {
              find_flag = true;
              break;
            }
          }
          if (!find_flag) {
            current_resource_list.value.push(resource);
          }
        }
      }
      // 往上滚动防止连续加载
      // @ts-ignore
      el_scrollbar_Ref.value.setScrollTop(scroll_position.scrollTop - 20);
      resource_loading.value = false;
    }
  } else if (resource_view_model.value == 'list') {
    if (
      // @ts-ignore
      Math.floor(scroll_position.scrollTop + window.innerHeight - 128) >
      resource_list_scroll_Ref.value.clientHeight - 10
    ) {
      // 下一页
      current_page_num.value += 1;
      let search_params = {
        resource_parent_id: current_resource.id,
        page_num: current_page_num.value,
        page_size: current_page_size.value
      };
      resource_loading.value = true;
      let res = await search_resource_object(search_params);
      if (!res.error_status) {
        current_total.value = res.result.total;
        for (let resource of res.result.data) {
          // 去重添加
          let find_flag = false;
          for (let item of current_resource_list.value) {
            if (item.id == resource.id) {
              find_flag = true;
              break;
            }
          }
          if (!find_flag) {
            current_resource_list.value.push(resource);
          }
        }
      }
      // 往上滚动防止连续加载
      // @ts-ignore
      el_scrollbar_Ref.value.setScrollTop(scroll_position.scrollTop - 20);
      resource_loading.value = false;
    }
  }
}

export async function add_dir_resource() {
  // 在当前目录下添加一个新的目录
  // 校验表单
  if (!new_dir_form_Ref.value) {
    return;
  }
  await new_dir_form_Ref.value.validate((valid: boolean) => {
    if (valid) {
      new_dir_form_valid.value = true;
    } else {
      return;
    }
  });
  // 不得重名
  for (let item of current_resource_list.value) {
    if (item.resource_name === new_dir_resource_item.resource_name) {
      ElMessage.warning('不得重名');
      return;
    }
  }
  if (!new_dir_form_valid.value) {
    return;
  }
  let params = {
    resource_name: new_dir_resource_item.resource_name,
    resource_parent_id: current_resource.id,
    resource_desc: new_dir_resource_item.resource_desc
  };
  let res = await add_resource_object(params);
  if (!res.error_status) {
    // 更新清单
    search_all_resource_object();
    init_my_resource_tree();
    ElMessage.success('添加成功!');
  }
  // 关闭对话框
  new_dir_form_valid.value = false;
  add_dir_dialog_flag.value = false;
}

export async function get_parent_resource_list() {
  if (!current_resource.id) {
    current_path_tree.value = [];
    return;
  }
  let params = {
    resource_id: current_resource.id
  };
  let res = await get_resource_object_path(params);
  if (!res.error_status) {
    current_path_tree.value = res.result.data;
  }
}

export async function double_click_resource_card(resource: ResourceItem) {
  // 双击资源列表中的某一行触发
  if (resource.resource_type === 'folder') {
    show_resource_list(resource);
  } else {
    preview_resource(resource);
  }
}

export function click_resource_card(resource: ResourceItem, event: MouseEvent) {
  // 如果点击的是多选框，则不触发单击事件
  if ((event.target as HTMLElement).closest('.resource-item-card-body-button')) {
    return;
  }

  resource.resource_is_selected = !resource.resource_is_selected;
  let selected_cnt = 0;
  for (let item of current_resource_list.value) {
    if (item.resource_is_selected) {
      selected_cnt += 1;
    }
  }
  if (selected_cnt > 0) {
    show_multiple_button.value = true;
  }
  // 保证multiple_selection 的顺序来更新
  if (resource.resource_is_selected) {
    multiple_selection.value.push(resource);
  } else {
    let index = multiple_selection.value.findIndex(item => item.id == resource.id);
    multiple_selection.value.splice(index, 1);
  }
  // 同步到列表视图
  resource_list_Ref.value?.toggleRowSelection(resource);
}



export function onDragStart(event) {
  // // console.log('start', event)
  // 设置拖拽时的样式
  const target = event.target as HTMLElement;
  // // console.log(target)
  target.classList.add('dragging');

  // 设置拖拽数据（可选）
  let resource_id = target.getAttribute('id');
  event.dataTransfer.setData('resource_id', resource_id);
  event.dataTransfer.effectAllowed = 'move';
}

export function onDragEnd(event) {
  // // console.log('end',event)
  // 移除拖拽时的样式
  const target = event.target as HTMLElement;
  target.classList.remove('dragging');
}

export async function onDropFunction(event) {
  // 停止事件传播
  event.preventDefault();
  event.stopPropagation();
  const data = event.dataTransfer?.getData('resource_id');
  let data_int = parseInt(data);
  // console.log('Dropped data:', data);
  const target = event.target as HTMLElement;
  let resource_id = target.getAttribute('id');
  // console.log('target', target, resource_id)
  // 如果目标是目录，则进行移动操作
  let resource_id_int = parseInt(resource_id);
  // // console.log(data_int, resource_id, resource_id_int)
  if (resource_id_int && data_int && resource_id_int != data_int) {
    let target_resource_obj = current_resource_list.value.find(item => item.id == resource_id_int);
    if (target_resource_obj.resource_type != 'folder') {
      ElMessage.error('只能移动到目录中');
      return;
    }
    // console.log(data_int, resource_id_int)
    let params = {
      resource_id_list: [data_int],
      target_resource_id: resource_id_int
    };

    let res = await move_resources(params);
    if (!res.error_status) {
      ElMessage.success('移动成功');
      search_all_resource_object();
    }
  }
}

export function format_resource_size(size_num: number | null) {
  // 格式化文件大小,保留两位小数,输入为mb单位的数字
  // // console.log(size_num)
  if (size_num === null) {
    return '';
  }
  let size = size_num;
  let size_str = '';

  // kb单位
  if (size < 1) {
    size = size * 1024;
    size_str = size.toFixed(2) + 'KB';
  } else if (size < 1024) {
    size_str = size.toFixed(2) + 'MB';
  } else if (size < 1024 * 1024) {
    size = size / 1024;
    size_str = size.toFixed(2) + 'GB';
  } else if (size < 1024 * 1024 * 1024) {
    size = size / 1024 / 1024;
    size_str = size.toFixed(2) + 'TB';
  } else if (size < 1024 * 1024 * 1024 * 1024) {
    size = size / 1024 / 1024 / 1024;
    size_str = size.toFixed(2) + 'PB';
  } else {
    size = size / 1024 / 1024 / 1024 / 1024;
    size_str = size.toFixed(2) + 'EB';
  }

  return size_str;
}

export function sort_resource_size(a, b) {
  // 按照文件大小排序
  return a.resource_size_in_MB - b.resource_size_in_MB;
}

export function sort_resource_status(a, b) {
  // 按照文件状态排序
  if (a.rag_status) {
    return 1;
  } else {
    return -1;
  }
}

export function get_resource_icon(resource: ResourceItem) {
  // 获取资源图标
  if (resource.resource_icon) {
    if (
      resource.resource_icon.includes('http') ||
      resource.resource_icon.includes('data:image') ||
      resource.resource_icon.includes('images/')
    ) {
      return resource.resource_icon;
    }
    return 'images/' + resource.resource_icon;
  } else {
    return 'images/' + 'html.svg';
  }
}

export function cancel_multiple_selection() {
  show_multiple_button.value = false;
  for (let item of multiple_selection.value) {
    item.resource_is_selected = false;
  }
  multiple_selection.value = [];
  resource_list_Ref.value?.clearSelection();
}

export function batch_move_select_resources() {
  let selected_resources = [];
  for (let resource of current_resource_list.value) {
    if (resource.resource_is_selected && resource.id && resource.resource_status == '正常') {
      selected_resources.push(resource.id);
    }
  }
  show_move_dialog_multiple(selected_resources, search_all_resource_object);
}
export function batch_copy_select_resources() {
  let selected_resources = [];
  if (resource_view_model.value == 'list') {
    for (let resource of multiple_selection.value) {
      if (resource.id && resource.resource_status == '正常') {
        selected_resources.push(resource.id);
      }
    }
  } else {
    for (let resource of current_resource_list.value) {
      if (resource.resource_is_selected && resource.id && resource.resource_status == '正常') {
        selected_resources.push(resource.id);
      }
    }
  }
  push_to_clipboard(selected_resources);
}
export async function batch_download_select_resource() {
  let params = {
    resource_list: []
  };

  for (let item of multiple_selection.value) {
    if (item.id && item.resource_status == '正常') {
      params.resource_list.push(item.id);
    }
  }
  resource_loading.value = true;
  let res = await batch_download_resources(params);
  resource_loading.value = false;
  if (!res.error_status) {
    if (!res.result?.length) {
      ElMessage.info('无可下载资源,请检查资源对应权限!');
      return;
    }
    ElMessage.success('批量下载启动成功！');
    for (let link_item of res.result) {
      // 创建一个隐藏的 <a> 标签
      const link = document.createElement('a');
      link.href = link_item.download_url + '?filename=' + encodeURIComponent(link_item.resource_name);
      link.download = link_item.resource_name; // 设置下载文件的名称
      link.style.display = 'none';

      // 将 <a> 标签添加到文档中
      document.body.appendChild(link);

      // 触发点击事件
      link.click();

      // 移除 <a> 标签
      document.body.removeChild(link);
    }
  }
}
export async function batch_delete_resources() {
  show_delete_flag.value = false;
  const params = {
    resource_list: []
  };
  for (const item of current_resource_list.value) {
    if (item.resource_is_selected && item?.id) {
      params.resource_list.push(item.id);
    }
  }
  if (!params.resource_list.length) {
    ElNotification({
      title: '系统通知',
      message: `所选资源均已删除!`,
      type: 'info',
      duration: 5000
    });
    return;
  }
  const res = await batch_delete_resource_object(params);
  if (!res.error_status) {
    ElNotification({
      title: '系统通知',
      message: `共成功删除${res.result.delete_cnt}个资源!`,
      type: 'success',
      duration: 5000
    });
    // 刷新文档树
    await init_my_resource_tree();
  }
  await search_all_resource_object();
  refresh_panel_count();
}

export async function preview_resource(resource: ResourceItem) {
  // 预览资源
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除，请恢复后查看!');
    return;
  }
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_type == 'folder') {
    await show_resource_list(resource);
    return;
  }

  await router.push({
    name: 'resource_viewer',
    params: {
      resource_id: resource.id
    }
  });
}
export async function show_resource_detail(resource: ResourceItem) {
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除，请恢复后查看!');
    return;
  }
  turn_on_resource_meta(resource.id);
}

export async function download_resource(resource: ResourceItem) {
  // 下载资源
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除，请恢复后下载!');
    return;
  }
  if (resource.resource_type == 'folder') {
    ElMessage.warning('文件夹无法下载!');
    return;
  }
  let params = {
    resource_id: resource.id
  };
  let res = await download_resource_object(params);
  if (!res.error_status) {
    let download_url = res.result?.download_url;
    if (!download_url) {
      ElMessage.error('下载链接为空');
      return;
    }
    download_url = download_url + '?filename=' + encodeURIComponent(resource.resource_name);
    // 创建一个隐藏的 <a> 标签
    const link = document.createElement('a');
    link.href = download_url;
    link.download = resource.resource_name; // 设置下载文件的名称
    link.style.display = 'none';

    // 将 <a> 标签添加到文档中
    document.body.appendChild(link);

    // 触发点击事件
    link.click();

    // 移除 <a> 标签
    document.body.removeChild(link);
  }
}
export async function move_resource(resource: ResourceItem) {
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 移动资源
  show_move_dialog_multiple([resource.id], search_all_resource_object);
}

export async function rebuild_resource(resource: ResourceItem) {
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 检查资源状态
  if (resource.resource_status != '正常') {
    ElMessage.warning('资源无法构建索引!');
    return;
  }
  if (!check_resource_rag_support(resource)) {
    ElMessage.warning('资源无法构建索引!');
    return;
  }

  let params = {
    resource_list: [resource.id]
  };
  let res = await build_resource_object_ref(params);
  if (!res.error_status) {
    ElMessage.success('提交重建任务成功!');
    for (let item of current_resource_list.value) {
      if (item.id == resource.id) {
        item.rag_status = '';
        break
      }
    }
  }
}
export async function delete_resource(resource: ResourceItem) {
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除!');
    return;
  }
  // 删除资源
  let params = {
    resource_id: resource.id
  };
  let res = await delete_resource_object_api(params);
  if (!res.error_status) {
    ElMessage.success('删除成功!');
    await search_all_resource_object();
    // 刷新文档树
    await init_my_resource_tree();
  }
  // 关闭popover
  if (resource_list_card_buttons_Ref.value) {
    for (let item of resource_list_card_buttons_Ref.value) {
      item?.hide();
    }
  }
  if (resource_list_buttons_Ref.value) {
    resource_list_buttons_Ref.value?.hide();
  }
  refresh_panel_count();
}
export function handleDragOver(event) {
  event.preventDefault();
}

export async function share_resource(resource: ResourceItem) {
  // 分享资源
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 分享资源
  await turn_on_share_selector(resource);
}
export async function create_new_document() {
  console.log('创建新文档');
  // 检验文档信息
  if (!new_document_form_Ref.value) {
    return;
  }
  let valid_res = await new_document_form_Ref.value.validate();
  if (!valid_res) {
    return;
  }

  // 创建新文档
  let params = {
    resource_parent_id: current_resource.id,
    resource_name: new_document_resource.resource_name,
    resource_desc: new_document_resource.resource_desc,
    resource_format: new_document_resource.resource_format,
    resource_type: 'document'
  };
  let res = await add_resource_object(params);
  if (!res.error_status) {
    ElMessage.success('创建成功!');
    // 刷新文档树
    await init_my_resource_tree();
    add_document_flag.value = false;
    new_document_resource.resource_name = '';
    new_document_resource.resource_desc = '';
    new_document_resource.resource_format = 'docx';
    // 直接打开文档
    await preview_resource(res.result);
  }
}

export function setResourceList(list: ResourceItem[]) {
  current_resource_list.value = list;
}

export function setResourceTotal(total: number) {
  current_total.value = total;
}

export function setResourceLoading(status: boolean) {
  resource_loading.value = status;
}
