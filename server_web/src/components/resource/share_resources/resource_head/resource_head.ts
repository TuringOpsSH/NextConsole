import { ref } from 'vue';
import {ResourceItem, TResourceListStatus} from '@/types/resource-type';
import {
  current_share_resource,
  multiple_selection,
  search_all_resource_share_object
} from '@/components/resource/share_resources/share_resources';
import router from '@/router';
import { turn_on_resource_meta } from '@/components/resource/resource_meta/resource_meta';
import { resource_view_model } from '@/components/resource/share_resources/share_resources';
import {useSessionStorage} from "@vueuse/core";

export const current_path_tree = ref<ResourceItem[]>([]);

export const show_dir_meta_flag = ref(false);

export function switch_resource_layout() {
//   search_all_resource_share_object();
  const shareListStatus = useSessionStorage<TResourceListStatus>('shareListStatus', 'card');
  if (shareListStatus.value === 'list') {
    shareListStatus.value = 'card';
  } else {
    shareListStatus.value = 'list';
  }
  // 更新至url
  router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      view_model: shareListStatus.value
    }
  });
}
export function switch_show_resource_meta() {
  if (multiple_selection.value?.length > 0) {
    // 将最新选中的资源设置为当前资源
    let resource_id = multiple_selection.value[multiple_selection.value.length - 1]?.id;
    if (!resource_id) {
      return;
    }
    turn_on_resource_meta(resource_id, '共享');
    return;
  }
  // 没有选中资源，则显示最近当前主目录的元信息
  if (!current_share_resource.id) {
    console.log(current_share_resource);
    return;
  }
  turn_on_resource_meta(current_share_resource.id, '共享');
}
