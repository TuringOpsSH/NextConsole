import router from '@/router';
import {ISearchByKeywordParams, ResourceItem} from '@/types/resource_type';
import {
  batch_download_resources,
  get_resource_object_path,
  resource_share_get_list,
  resource_share_get_meta,
  searchByKeywordInResource
} from '@/api/resource_api';
import {reactive, ref} from 'vue';
import {current_path_tree} from '@/components/resource/share_resources/resource_head/resource_head';
import {ElMessage} from 'element-plus';
import {turn_on_resource_meta} from '@/components/resource/resource_meta/resource_meta';
import {push_to_clipboard} from '@/components/resource/resource_clipborad/resource_clipboard';
import {useShareResourceStore} from '@/stores/resourceShareStore';
import {storeToRefs} from 'pinia';
import {sortShareResourceList} from '@/utils/common';
import {saveAs} from 'file-saver'; // 使用FileSaver.js

export const current_share_resource = reactive<ResourceItem>(
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
export const resource_view_model = ref('list');
export const share_resource_list = ref<ResourceItem[]>([]);
export const share_resource_loading = ref(false);
export const multiple_selection = ref<ResourceItem[]>([]);
export const show_multiple_button = ref(false);
export const resource_share_list_card_buttons_Ref = ref();
export const resource_share_list_Ref = ref();

export const current_page_num = ref(1);
export const current_page_size = ref(50);
export const current_total = ref(0);
export const el_scrollbar_Ref = ref(null);
export const resource_list_scroll_Ref = ref(null);
export const resource_card_scroll_Ref = ref(null);

export async function show_share_resources(item: ResourceItem | null = null) {
  current_share_resource.id = item?.id;
  // 面板跳转
  if (item.resource_type == 'folder') {
    router.push({
      name: 'resource_share',
      query: {
        ...router.currentRoute.value.query
      },
      params: {
        ...router.currentRoute.value.params,
        resource_id: item?.id
      }
    });
    get_share_parent_resource_list();
    search_all_resource_share_object();

    return;
  }
  router.push({
    name: 'resource_viewer',
    params: {
      resource_id: item.id
    }
  });
}

export async function get_current_share_resource(resource_id: string | number | null = null) {
  let params = {
    resource_id: resource_id
  };
  let res = await resource_share_get_meta(params);
  if (!res.error_status) {
    Object.assign(current_share_resource, res.result);
  }
}

export async function search_all_resource_share_object(params?: ISearchByKeywordParams) {
  const { isLoading } = storeToRefs(useShareResourceStore());
  let search_params = {
    resource_parent_id: current_share_resource.id > 0 ? current_share_resource.id : null
  };
  share_resource_loading.value = true;
  isLoading.value = true;
  let res;
  if (params) {
    res = await searchByKeywordInResource(params);
  } else {
    res = await resource_share_get_list(search_params);
  }
  isLoading.value = false;
  if (!res.error_status) {
    current_total.value = res.result.total;
    const {
      result: { data = [] }
    } = res;
    sortShareResourceList(data);
    if (params) {
      share_resource_list.value = data;
    } else {
      share_resource_list.value = data.map(({ resource, auth_type }) => {
        return { ...resource, auth_type };
      });
    }
  }
  resource_share_list_Ref.value?.clearSelection();
  share_resource_loading.value = false;
}

export async function search_next_resource_share_object(scroll_position: object) {
  if (share_resource_loading.value) {
    console.log('资源正在加载中');
    return;
  }
  if (current_total.value && current_total.value <= share_resource_list.value.length) {
    return;
  }
  if (resource_view_model.value == 'card') {
    // @ts-ignore
    if (scroll_position.scrollTop + window.innerHeight - 120 > resource_card_scroll_Ref.value.clientHeight - 10) {
      // 下一页
      current_page_num.value += 1;
      let search_params = {
        resource_parent_id: current_share_resource.id,
        page_num: current_page_num.value,
        page_size: current_page_size.value
      };
      share_resource_loading.value = true;
      let res = await resource_share_get_list(search_params);
      if (!res.error_status) {
        current_total.value = res.result.total;

        for (let resource of res.result.data) {
          // 去重添加
          let find_flag = false;
          for (let item of share_resource_list.value) {
            if (item.id == resource.resource.id) {
              find_flag = true;
              break;
            }
          }
          if (!find_flag) {
            share_resource_list.value.push({ ...resource.resource, auth_type: resource.auth_type });
          }
        }
      }
      // @ts-ignore
      el_scrollbar_Ref.value.setScrollTop(scroll_position.scrollTop - 20);
      share_resource_loading.value = false;
    }
  } else if (resource_view_model.value == 'list') {
    // @ts-ignore
    if (
      Math.floor(scroll_position.scrollTop + window.innerHeight - 128) >
      resource_list_scroll_Ref.value.clientHeight - 10
    ) {
      // 下一页
      current_page_num.value += 1;
      let search_params = {
        resource_parent_id: current_share_resource.id,
        page_num: current_page_num.value,
        page_size: current_page_size.value
      };
      share_resource_loading.value = true;
      let res = await resource_share_get_list(search_params);
      if (!res.error_status) {
        current_total.value = res.result.total;
        for (let resource of res.result.data) {
          // 去重添加
          let find_flag = false;
          for (let item of share_resource_list.value) {
            if (item.id == resource.resource.id) {
              find_flag = true;
              break;
            }
          }
          if (!find_flag) {
            share_resource_list.value.push({ ...resource.resource, auth_type: resource.auth_type });
          }
        }
      }
      // 往上滚动防止连续加载
      // @ts-ignore
      el_scrollbar_Ref.value.setScrollTop(scroll_position.scrollTop - 20);
      share_resource_loading.value = false;
    }
  }
}

export async function get_share_parent_resource_list() {
  current_path_tree.value = [
    // @ts-ignore
    {
      id: null,
      resource_name: '共享资源',
      resource_type: 'folder',
      resource_status: '正常',
      resource_type_cn: '文件夹'
    }
  ];
  if (current_share_resource.id < 0 || !current_share_resource.id) {
    return;
  }
  let params = {
    resource_id: current_share_resource.id
  };
  let res = await get_resource_object_path(params);
  if (!res.error_status) {
    for (let item of res.result.data) {
      if (item?.resource_parent_id) {
        current_path_tree.value.push(item);
      }
    }
  }
}

export async function preview_share_resource(resource: ResourceItem) {
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
    await show_share_resources(resource);
    return;
  }
  await router.push({
    name: 'resource_viewer',
    params: {
      resource_id: resource.id
    }
  });
}

export async function handle_selection_change(val: ResourceItem[]) {
  // 多选框选中事件
  multiple_selection.value = val;
  const selectIds = val.map(item => item.id);
  share_resource_list.value = share_resource_list.value.map(item => ({
    ...item,
    resource_is_selected: selectIds.includes(item.id)
  }));
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
  turn_on_resource_meta(resource.id, '共享');
}

export async function double_click_resource_card(resource: ResourceItem) {
  // 双击资源列表中的某一行触发
  if (resource.resource_type === 'folder') {
    show_share_resources(resource);
  } else {
    preview_share_resource(resource);
  }
}
export function click_resource_card(resource: ResourceItem, event: MouseEvent) {
  // 如果点击的是多选框，则不触发单击事件
  if ((event.target as HTMLElement).closest('.resource-item-card-body-button')) {
    return;
  }
  resource.resource_is_selected = !resource.resource_is_selected;
  let selected_cnt = 0;
  for (let item of share_resource_list.value) {
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
  resource_share_list_Ref.value?.toggleRowSelection(resource);
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
    for (let resource of share_resource_list.value) {
      if (resource.resource_is_selected && resource.id && resource.resource_status == '正常') {
        selected_resources.push(resource.id);
      }
    }
  }
  push_to_clipboard(selected_resources);
}
export async function batch_download_select_resource() {
  const params = {
    resource_list: []
  };

  for (const item of share_resource_list.value) {
    if (item.id && item.resource_is_selected) {
      params.resource_list.push(item.id);
    }
  }
  share_resource_loading.value = true;
  let res = await batch_download_resources(params);
  share_resource_loading.value = false;
  if (!res.error_status) {
    if (!res.result?.length) {
      ElMessage.info('无可下载资源,请检查资源对应权限!');
      return;
    }
    ElMessage.success('批量下载启动成功！');
    await handleDownLoad(res.result);
    // for (let link_item of res.result) {
    //   // 创建一个隐藏的 <a> 标签
    //   const link = document.createElement('a');
    //   link.href = link_item.download_url + '?filename=' + encodeURIComponent(link_item.resource_name);
    //   link.download = link_item.resource_name; // 设置下载文件的名称
    //   link.style.display = 'none';

    //   // 将 <a> 标签添加到文档中
    //   document.body.appendChild(link);

    //   // 触发点击事件
    //   link.click();

    //   // 移除 <a> 标签
    //   document.body.removeChild(link);
    // }
  }
}

async function handleDownLoad(data) {
  for (const item of data) {
    const response = await fetch(item.download_url);
    const blob = new Blob([await response.arrayBuffer()], {
      type: 'application/octet-stream' // 明确为二进制流
    });
    saveAs(blob, encodeURIComponent(item.resource_name));
  }
}

export function cancel_multiple_selection() {
  show_multiple_button.value = false;
  for (let item of multiple_selection.value) {
    item.resource_is_selected = false;
  }
  multiple_selection.value = [];
  resource_share_list_Ref.value?.clearSelection();
}
