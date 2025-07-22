import {FormInstance} from 'element-plus';
import {storeToRefs} from 'pinia';
import {ref} from 'vue';
import {searchByKeywordsApi} from '@/api/resource_api';
import {useResourceListStore} from '@/stores/resourceListStore';
import {ISearchByKeywordsParams, ResourceItem, TResourceListStatus} from '@/types/resource_type';
import {
  current_resource as currentResource,
  get_init_resource as getInitResource,
  multiple_selection as multipleSelection,
  new_dir_resource_item as newDirResourceItem,
  resource_view_model as resourceViewModel,
  search_all_resource_object as searchAllResourceObject,
  setResourceList,
  setResourceLoading,
  setResourceTotal
} from '@/components/resource/resource_list/resource_list';
import {turn_on_resource_meta as turnOnResourceMeta} from '@/components/resource/resource_meta/resource_meta';
import {sortResourceList} from '@/utils/common';

import router from '@/router';
import {useSessionStorage} from "@vueuse/core";

export const resource_head_height = ref(60);
export const current_path_tree = ref<ResourceItem[]>([]);
export const show_dir_meta_flag = ref(false);
export const add_dir_dialog_flag = ref(false);
export const new_dir_form_Ref = ref<FormInstance>();
export const new_dir_form_valid = ref(false);
export const add_document_flag = ref(false);
export const keyword = ref('');

export async function refreshData() {
  const resourceListStore = storeToRefs(useResourceListStore());
  resourceListStore.isLoading.value = true;
  if (resourceListStore.isSearchMode.value) {
    await handleSearch();
  } else {
    await searchAllResourceObject();
  }
  resourceListStore.isLoading.value = false;
}

export async function switch_resource_layout(target_model: string = null) {
  // 切换面板展示时暂不刷新数据
  // await refreshData();
  const resourceListStatus = useSessionStorage<TResourceListStatus>('resourceListStatus', 'card');
  if (!target_model) {
    if (resourceListStatus.value === 'list') {
      resourceListStatus.value = 'card';
    } else {
      resourceListStatus.value = 'list';
    }
  } else {
    // @ts-ignore
    resourceListStatus.value = target_model;
  }
  // 更新至url
  router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      view_model: resourceListStatus.value
    }
  });
}
export function switch_show_resource_meta() {
  if (multipleSelection.value?.length > 0) {
    // 将最新选中的资源设置为当前资源
    let resource_id = multipleSelection.value[multipleSelection.value.length - 1]?.id;
    if (!resource_id) {
      return;
    }
    turnOnResourceMeta(resource_id);
    return;
  }
  // 没有选中资源，则显示最近当前主目录的元信息
  if (!currentResource.id) {
    return;
  }
  turnOnResourceMeta(currentResource.id);
}
export function show_add_dir_dialog() {
  add_dir_dialog_flag.value = true;
  new_dir_form_valid.value = false;
  // 初始化 new_dir_resource_item
  Object.assign(newDirResourceItem, getInitResource());
  newDirResourceItem.resource_type = 'folder';
}
export function show_add_document_dialog() {
  add_document_flag.value = true;
}

export async function handleSearch() {
  if (keyword.value === '') {
    // ElMessage({
    //   message: '关键字不能为空',
    //   type: 'warning'
    // });
    return;
  }
  const resourceListStore = storeToRefs(useResourceListStore());

  resourceListStore.isSearchMode.value = true;

  const params: ISearchByKeywordsParams = {
    resource_keyword: keyword.value.trim(),
    resource_id: resourceListStore.resourceId.value
  };
  setResourceLoading(true);
  const res = await searchByKeywordsApi(params);
  setResourceLoading(false);
  if (!res?.error_status) {
    const {
      result: { data, total }
    } = res;
    sortResourceList(data);
    setResourceList(data);
    setResourceTotal(total);
  }
}
