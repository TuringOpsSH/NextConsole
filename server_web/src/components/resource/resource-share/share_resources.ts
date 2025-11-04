import router from '@/router';
import { ISearchByKeywordParams, IResourceItem } from '@/types/resource-type';
import {
  batch_download_resources,
  get_resource_object_path,
  resource_share_get_list,
  resource_share_get_meta,
  searchByKeywordInResource
} from '@/api/resource-api';
import {reactive, ref} from 'vue';
import {current_path_tree} from '@/components/resource/resource-share/resource_head/resource_head';
import {ElMessage} from 'element-plus';
import {turn_on_resource_meta} from '@/components/resource/resource_meta/resource_meta';
import {push_to_clipboard} from '@/components/resource/resource_clipborad/resource_clipboard';
import {useShareResourceStore} from '@/stores/resourceShareStore';
import {storeToRefs} from 'pinia';
import {sortShareResourceList} from '@/utils/common';
import {saveAs} from 'file-saver'; // 使用FileSaver.js

export const current_share_resource = reactive<IResourceItem>(
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
export const share_resource_list = ref<IResourceItem[]>([]);
export const share_resource_loading = ref(false);
export const multiple_selection = ref<IResourceItem[]>([]);
export const show_multiple_button = ref(false);
export const resource_share_list_card_buttons_Ref = ref();
export const resource_share_list_Ref = ref();

export const current_page_num = ref(1);
export const current_page_size = ref(50);
export const current_total = ref(0);
export const el_scrollbar_Ref = ref(null);
export const resource_list_scroll_Ref = ref(null);
export const resource_card_scroll_Ref = ref(null);

export async function show_share_resources(item: IResourceItem | null = null) {
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

export async function preview_share_resource(resource: IResourceItem) {
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

export async function handle_selection_change(val: IResourceItem[]) {
  // 多选框选中事件
  multiple_selection.value = val;
  const selectIds = val.map(item => item.id);
  share_resource_list.value = share_resource_list.value.map(item => ({
    ...item,
    resource_is_selected: selectIds.includes(item.id)
  }));
}

export function click_resource_card(resource: IResourceItem, event: MouseEvent) {
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

