import {
  current_tag,
  multiple_selection,
  resource_view_model,
  search_rag_enhance,
  search_resource_by_tags
} from '@/components/resource/resource_shortcut/resource_shortcut';
import router from '@/router';
import { ref } from 'vue';
import { get_resource_recent_format_count, search_resource_tags } from '@/api/resource_api';
import {
  choose_resource_meta,
  show_meta_flag,
  turn_on_resource_meta
} from '@/components/resource/resource_meta/resource_meta';
import { ResourceTag } from '@/types/resource_type';
import { ElMessage } from 'element-plus';
import { useResourceListStore } from '@/stores/resourceListStore';

export const resource_head_height = ref(60);
export const show_search_config_area_flag = ref(true);
export const loading_user_tags = ref(false);
export const all_resource_types = [
  { name: '文档', value: 'document' },
  { name: '图片', value: 'image' },
  { name: '网页', value: 'webpage' },
  { name: '代码', value: 'code' },
  { name: '文件夹', value: 'folder' },
  { name: '视频', value: 'video' },
  { name: '音频', value: 'audio' },
  { name: '程序', value: 'binary' },
  { name: '压缩包', value: 'archive' },
  { name: '文本', value: 'text' },
  { name: '其他', value: 'other' }
];
export const resource_types_name_map = {
  文档: 'document',
  图片: 'image',
  网页: 'webpage',
  代码: 'code',
  文件夹: 'folder',
  视频: 'video',
  音频: 'audio',
  程序: 'binary',
  其他: 'other',
  压缩包: 'archive',
  文本: 'text'
};
export const current_resource_types = ref([
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
]);
export const all_resource_formats = ref([]);
export const current_resource_formats = ref([]);
export const current_resource_tags = ref<ResourceTag[]>([]);
export const all_resource_tags = ref<ResourceTag[]>([]);
export const isIndeterminate = ref(false);
export const checkAll = ref(false);
export async function switch_resource_layout(target_model: string = null) {
  if (!target_model) {
    if (resource_view_model.value === 'list') {
      resource_view_model.value = 'card';
    } else {
      resource_view_model.value = 'list';
    }
  } else {
    resource_view_model.value = target_model;
  }
  // 更新至url
  await router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      view_model: resource_view_model.value
    }
  });
}
export async function switch_show_resource_meta() {
  // 设置当前资源的meta信息
  // 如果选中了资源，则显示选中资源的meta信息
  if (multiple_selection.value?.length > 0) {
    // 将最新选中的资源设置为当前资源
    let resource_id = multiple_selection.value[multiple_selection.value.length - 1]?.id;
    if (!resource_id) {
      return;
    }
    turn_on_resource_meta(resource_id);
    return;
  }
  // 如果没有选中资源，则显示最近上传的元信息
  choose_resource_meta.id = null;
  choose_resource_meta.resource_name = current_tag.value.tag_name;
  choose_resource_meta.resource_icon = 'images/tag.svg';
  choose_resource_meta.resource_desc = current_tag.value.tag_desc;
  // console.log(choose_resource_meta, current_tag.value)
  show_meta_flag.value = true;
}
// 过滤区域
export function show_search_config_area(target_status: boolean = null) {
  if (target_status === null) {
    show_search_config_area_flag.value = !show_search_config_area_flag.value;
  } else {
    show_search_config_area_flag.value = target_status;
  }
  if (show_search_config_area_flag.value && window.innerWidth > 768) {
    resource_head_height.value = 180;
  } else {
    resource_head_height.value = 60;
  }
}

export async function init_all_resource_formats() {
  let params = {};
  let res = await get_resource_recent_format_count(params);
  if (!res.error_status) {
    for (let item of res.result) {
      // 去除已经存在的格式
      // console.log (item)
      let find_flag = false;
      for (let exist_format of all_resource_formats.value) {
        if (exist_format.name === item.name) {
          exist_format.cnt = item.cnt;
          find_flag = true;
          break;
        }
      }
      if (!find_flag) {
        all_resource_formats.value.push(item);
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
  loading_user_tags.value = true;
  let res = await search_resource_tags(params);
  if (!res.error_status) {
    all_resource_tags.value = res.result;
  }
  loading_user_tags.value = false;
}

export async function handleCheckAllChange(val: boolean) {
  const cities = [
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
  current_resource_types.value = val ? cities : [];
  isIndeterminate.value = false;
  // 同步至url
  await router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      tag_id: current_resource_tags.value.map(item => item.id),
      resource_type: current_resource_types.value,
      resource_format: current_resource_formats.value
    }
  });
  await search_resource_by_tags();
}

export async function system_tags_filter_change() {
  // 同步至url
  await router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      tag_id: current_resource_tags.value.map(item => item.id),
      resource_type: current_resource_types.value,
      resource_format: current_resource_formats.value
    }
  });
  await search_resource_by_tags();
}

// 搜索模式
export const update_resource_keyword = ref('');
export const update_rag_enhance = ref(false);
export const edit_search_keyword_flag = ref(false);
export function switch_edit_search_keyword_dialog() {
  edit_search_keyword_flag.value = true;
  update_resource_keyword.value = '';
  update_rag_enhance.value = false;
}
export async function confirm_update_keyword() {
  if (!update_resource_keyword.value) {
    ElMessage.error('请输入搜索关键字');
    return;
  }

  edit_search_keyword_flag.value = false;
  // @ts-ignore
  current_tag.value.tag_name = update_resource_keyword.value.trim();
  search_rag_enhance.value = update_rag_enhance.value;
  await router.push({
    name: 'resource_search',
    params: {
      tag_source: 'system'
    },
    query: {
      ...router.currentRoute.value.query,
      resource_keyword: update_resource_keyword.value,
      tag_value: 'search',
      // @ts-ignore
      rag_enhance: update_rag_enhance.value
    }
  });
  await search_resource_by_tags();
}
