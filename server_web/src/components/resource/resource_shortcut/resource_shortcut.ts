import {computed, ref} from 'vue';
import {ResourceItem, ResourceTag} from '@/types/resource_type';
import {
  batch_delete_resource_object,
  batch_download_resources,
  build_resource_object_ref,
  delete_resource_object_api,
  delete_resource_recycle_object,
  download_resource_object,
  recover_resource_recycle_object,
  search_resource_by_recent_index,
  search_resource_by_recent_upload,
  search_resource_by_resource_keyword,
  search_resource_by_resource_tags,
  search_resource_by_resource_type,
  search_resource_in_recycle
} from '@/api/resource_api';
import router from '@/router';
import {ElMessage, ElNotification} from 'element-plus';
import {show_move_dialog_multiple} from '@/components/resource/resource_tree/resource_tree';
import {push_to_clipboard} from '@/components/resource/resource_clipborad/resource_clipboard';
import {turn_on_resource_meta} from '@/components/resource/resource_meta/resource_meta';
import {
  current_resource_tags,
  current_resource_types,
  resource_types_name_map,
  show_search_config_area
} from '@/components/resource/resource_shortcut/resource_shortcut_head/resource_shortcut_head';
import {md_answer} from '@/components/next_console/messages_flow/message_flow';
import {refresh_panel_count} from '@/components/resource/resource_panel/panel';
import {check_resource_rag_support} from '@/components/resource/resource_main';
import {turn_on_share_selector} from '@/components/resource/resource_share_selector/resource_share_selector';
import {user_info} from '@/components/user_center/user';
import {useResourceStore} from '@/stores/resourceStore';
import {storeToRefs} from 'pinia';
import {useSessionStorage} from '@vueuse/core';
import {RESOURCE_FORMATS} from '@/utils/constant';
import {sortResourceList} from '@/utils/common';

const currentResourceValues = useSessionStorage('currentResourceValues', []);
const resourceFormats = computed(() => {
  if (currentResourceValues.value.length) {
    return currentResourceValues.value.flatMap(item =>
      RESOURCE_FORMATS.find(format => format.value === item)?.formats?.split(',')
    );
  } else {
    return [];
  }
});

export function setCurrentResourceValues(values: string[]) {
  currentResourceValues.value = values;
}
export const resourceId = ref('');
export const current_tag = ref<ResourceTag>(
  //@ts-ignore
  {
    id: null,
    tag_name: '',
    tag_value: '',
    tag_type: '',
    tag_source: ''
  }
);
export const system_tags = [
  {
    tag_name: '最近上传',
    tag_source: 'system',
    tag_type: 'recent',
    tag_value: 'recent_upload',
    tag_icon: 'images/recent_upload.svg',
    tag_desc: '最近上传的资源',
    tag_count: 0
  },
  {
    tag_name: '最近索引',
    tag_source: 'system',
    tag_type: 'recent',
    tag_value: 'recent_index',
    tag_icon: 'images/recent_index.svg',
    tag_desc: '最近索引的资源',
    tag_count: 0
  },
  {
    tag_name: '文档',
    tag_source: 'system',
    tag_type: 'resource_type',
    tag_icon: 'images/document.svg',
    tag_count: 0,
    tag_value: 'document',
    tag_desc: '文档资源'
  },
  {
    tag_name: '文件夹',
    tag_source: 'system',
    tag_type: 'resource_type',
    tag_icon: 'images/folder.svg',
    tag_count: 0,
    tag_value: 'folder',
    tag_desc: '文件夹'
  },
  {
    tag_name: '代码',
    tag_source: 'system',
    tag_type: 'resource_type',
    tag_icon: 'images/code.svg',
    tag_count: 0,
    tag_value: 'code',
    tag_desc: '代码资源'
  },
  {
    tag_name: '图片',
    tag_source: 'system',
    tag_type: 'resource_type',
    tag_icon: 'images/picture.svg',
    tag_count: 0,
    tag_value: 'image',
    tag_desc: '图片资源'
  },
  {
    tag_name: '视频',
    tag_source: 'system',
    tag_type: 'resource_type',
    tag_icon: 'images/video.svg',
    tag_count: 0,
    tag_value: 'video',
    tag_desc: '视频资源'
  },
  {
    tag_name: '音频',
    tag_source: 'system',
    tag_type: 'resource_type',
    tag_icon: 'images/audio.svg',
    tag_count: 0,
    tag_value: 'audio',
    tag_desc: '音频资源'
  },
  {
    tag_name: '压缩包',
    tag_source: 'system',
    tag_type: 'resource_type',
    tag_icon: 'images/archive.svg',
    tag_count: 0,
    tag_value: 'archive',
    tag_desc: '压缩包资源'
  },
  {
    tag_name: '网页',
    tag_source: 'system',
    tag_type: 'resource_type',
    tag_icon: 'images/webpage.svg',
    tag_count: 0,
    tag_value: 'webpage',
    tag_desc: '网页资源'
  },
  {
    tag_name: '回收站',
    tag_source: 'system',
    tag_type: 'recycle',
    tag_value: 'recycle_bin',
    tag_icon: 'images/recycle_bin.svg',
    tag_desc: '回收站资源',
    tag_count: 0
  },
  {
    tag_name: '搜索',
    tag_source: 'system',
    tag_type: 'search',
    tag_value: 'search',
    tag_icon: 'images/search.svg',
    tag_desc: '搜索资源',
    tag_count: 0
  }
];
export const resource_view_model = ref('list');
export const resource_loading = ref(false);
export const current_resource_list = ref<ResourceItem[]>([]);
export const current_resource_cnt = ref(0);
export const multiple_selection = ref<ResourceItem[]>([]);
export const show_multiple_button = ref(false);
export const resource_shortcut_Ref = ref(null);
export const current_page_size = ref(50);
export const current_page_num = ref(1);
export const button_Ref = ref(null);
export const show_delete_flag = ref(false);
export const resource_shortcut_card_buttons_Ref = ref(null);
export const search_rag_enhance = ref(false);
export function parseTagId(tag_id: any) {
  if (typeof tag_id == 'string') {
    return [parseInt(tag_id)];
  }
  if (typeof tag_id == 'number') {
    return tag_id;
  }
  if (!tag_id) {
    return [];
  }
  let new_tag_id = [];
  for (let id of tag_id) {
    try {
      new_tag_id.push(parseInt(id));
    } catch (e) {
      // console.log('tag_id', tag_id  ,e )
    }
  }
  return new_tag_id;
}
export function parseResourceType(resource_type: any) {
  if (typeof resource_type == 'string') {
    return [resource_type];
  }
  if (!resource_type) {
    return [];
  }
  return resource_type;
}
export function get_system_tag(tag_value: string) {
  return system_tags.find(tag => tag.tag_value === tag_value);
}
export async function search_resource_by_tags() {
  // 根据标签搜索资源
  show_search_config_area(true);
  if (current_tag.value.tag_source == 'system') {
    if (current_tag.value.tag_value == 'search') {
      search_resource_by_keyword();
      return;
    }
    // @ts-ignore
    current_tag.value = get_system_tag(current_tag.value.tag_value);
    if (current_tag.value.tag_value == 'recent_upload') {
      search_resource_recent_upload();
    } else if (current_tag.value.tag_value == 'recent_index') {
      search_resource_recent_index();
    } else if (current_tag.value.tag_type == 'resource_type') {
      search_resource_resource_type();
    } else if (current_tag.value.tag_value == 'recycle_bin') {
      search_resource_recycle_bin();
    }
  } else if (current_tag.value.tag_source == 'user') {
    search_resource_resource_tag();
  }
}
export async function search_resource_recent_upload() {
  // 最近上传
  let params = {
    resource_type: [],
    resource_format: resourceFormats.value,
    resource_tags: [],
    page_size: current_page_size.value,
    page_num: current_page_num.value
  };
  // 更新resource_type 的值
  for (let resource_type of current_resource_types.value) {
    if (resource_types_name_map?.[resource_type]) {
      params.resource_type.push(resource_types_name_map?.[resource_type]);
      continue;
    }
    params.resource_type.push(resource_type);
  }
  // for (let resource_format of current_resource_formats.value) {
  //   if (resource_format != '未知') {
  //     params.resource_format.push(resource_format);
  //   } else {
  //     params.resource_format.push('');
  //   }
  // }
  for (let resource_tag of current_resource_tags.value) {
    if (resource_tag.id) {
      params.resource_tags.push(resource_tag.id);
    }
  }

  resource_loading.value = true;
  let res = await search_resource_by_recent_upload(params);
  if (!res.error_status) {
    current_resource_list.value = [];
    for (let item of res.result.data) {
      current_resource_list.value.push({
        id: item.resource.id,
        resource_parent_id: item.resource.resource_parent_id,
        resource_name: item.resource.resource_name ? item.resource.resource_name : item.upload_task.resource_name,
        resource_type: item.resource.resource_type ? item.resource.resource_type : item.upload_task.resource_type,
        resource_type_cn: item.resource.resource_type_cn
          ? item.resource.resource_type_cn
          : item.upload_task.resource_type_cn,
        resource_title: item.resource.resource_title,
        resource_desc: item.resource.resource_desc,
        resource_icon: item.resource.resource_icon ? item.resource.resource_icon : item.upload_task.task_icon,
        resource_format: item.resource.resource_format
          ? item.resource.resource_format
          : item.upload_task.resource_format,
        resource_size_in_MB: item.resource.resource_size_in_MB
          ? item.resource.resource_size_in_MB
          : item.upload_task.resource_size_in_mb,
        resource_status: item.resource.resource_status ? item.resource.resource_status : item.upload_task.task_status,
        resource_source: item.resource.resource_source,
        resource_source_url: item.resource.resource_source_url,
        resource_show_url: item.resource.resource_show_url,
        resource_language: item.resource.resource_language,
        create_time: item.resource.create_time ? item.resource.create_time : item.upload_task.create_time,
        update_time: item.resource.update_time ? item.resource.update_time : item.upload_task.update_time,
        delete_time: item.resource.delete_time,
        // @ts-ignore
        task_source: item.upload_task.task_source,
        task_status: item.upload_task.task_status,
        content_finish_idx: item.upload_task.content_finish_idx,
        content_max_idx: item.upload_task.content_max_idx
      });
    }
    current_resource_cnt.value = res.result.total;
  }
  resource_loading.value = false;
  await search_resource_jumper();
}
export async function search_resource_recent_index() {
  // 最近索引
  let params = {
    resource_type: [],
    resource_format: resourceFormats.value,
    resource_tags: [],
    page_size: current_page_size.value,
    page_num: current_page_num.value
  };
  // 更新resource_type 的值
  for (let resource_type of current_resource_types.value) {
    if (resource_types_name_map?.[resource_type]) {
      params.resource_type.push(resource_types_name_map?.[resource_type]);
      continue;
    }
    params.resource_type.push(resource_type);
  }
  // for (let resource_format of current_resource_formats.value) {
  //   if (resource_format != '未知') {
  //     params.resource_format.push(resource_format);
  //   } else {
  //     params.resource_format.push('');
  //   }
  // }
  for (let resource_tag of current_resource_tags.value) {
    if (resource_tag.id) {
      params.resource_tags.push(resource_tag.id);
    }
  }
  resource_loading.value = true;
  let res = await search_resource_by_recent_index(params);
  if (!res.error_status) {
    current_resource_list.value = [];
    for (let item of res.result.data) {
      current_resource_list.value.push({
        id: item.resource.id,
        resource_parent_id: item.resource.resource_parent_id,
        resource_name: item.resource.resource_name,
        resource_type: item.resource.resource_type,
        resource_type_cn: item.resource.resource_type_cn,
        resource_title: item.resource.resource_title,
        resource_desc: item.resource.resource_desc,
        resource_icon: item.resource.resource_icon,
        resource_format: item.resource.resource_format,
        resource_size_in_MB: item.resource.resource_size_in_MB,
        resource_status: item.resource.resource_status,
        resource_source: item.resource.resource_source,
        resource_source_url: item.resource.resource_source_url,
        resource_show_url: item.resource.resource_show_url,
        resource_language: item.resource.resource_language,
        create_time: item.resource.create_time,
        update_time: item.resource.update_time,
        delete_time: item.resource.delete_time,
        rag_status: item.rag_info?.[0].ref_status,
        // @ts-ignore
        rag_duration:
          new Date(item.rag_info?.[0].update_time).getTime() - new Date(item.rag_info?.[0].create_time).getTime()
      });
    }
    current_resource_cnt.value = res.result.total;
  }
  resource_loading.value = false;
  await search_resource_jumper();
}
export async function search_resource_resource_type() {
  // 根据系统资源类型进行搜索
  let params = {
    resource_type: [],
    resource_format: resourceFormats.value,
    resource_tags: [],
    page_size: current_page_size.value,
    page_num: current_page_num.value
  };
  // 更新resource_type 的值
  params.resource_type.push(current_tag.value.tag_value);
  // for (let resource_format of current_resource_formats.value) {
  //   if (resource_format != '未知') {
  //     params.resource_format.push(resource_format);
  //   } else {
  //     params.resource_format.push('');
  //   }
  // }
  for (let resource_tag of current_resource_tags.value) {
    if (resource_tag.id) {
      params.resource_tags.push(resource_tag.id);
    }
  }
  resource_loading.value = true;
  let res = await search_resource_by_resource_type(params);
  if (!res.error_status) {
    current_resource_list.value = [];
    for (let item of res.result.data) {
      // @ts-ignore
      current_resource_list.value.push({
        id: item.id,
        resource_parent_id: item.resource_parent_id,
        resource_name: item.resource_name,
        resource_type: item.resource_type,
        resource_type_cn: item.resource_type_cn,
        resource_title: item.resource_title,
        resource_desc: item.resource_desc,
        resource_icon: item.resource_icon,
        resource_format: item.resource_format,
        resource_size_in_MB: item.resource_size_in_MB,
        resource_status: item.resource_status,
        resource_source: item.resource_source,
        resource_source_url: item.resource_source_url,
        resource_show_url: item.resource_show_url,
        resource_language: item.resource_language,
        create_time: item.create_time,
        update_time: item.update_time,
        delete_time: item.delete_time
      });
    }
    current_resource_cnt.value = res.result.total;
  }
  resource_loading.value = false;
  await search_resource_jumper();
}
export async function search_resource_resource_tag() {
  // 根据资源标签进行搜索
  let params = {
    resource_type: [],
    resource_format: resourceFormats.value,
    resource_tags: [],
    page_size: current_page_size.value,
    page_num: current_page_num.value
  };
  // 更新resource_type 的值
  for (let resource_type of current_resource_types.value) {
    if (resource_types_name_map?.[resource_type]) {
      params.resource_type.push(resource_types_name_map?.[resource_type]);
      continue;
    }
    params.resource_type.push(resource_type);
  }
  // for (let resource_format of current_resource_formats.value) {
  //   if (resource_format != '未知') {
  //     params.resource_format.push(resource_format);
  //   } else {
  //     params.resource_format.push('');
  //   }
  // }
  for (let resource_tag of current_resource_tags.value) {
    if (resource_tag.id) {
      params.resource_tags.push(resource_tag.id);
    }
  }
  resource_loading.value = true;
  let res = await search_resource_by_resource_tags(params);
  if (!res.error_status) {
    current_resource_list.value = [];
    for (let item of res.result.data) {
      let new_data = {
        id: item.id,
        resource_parent_id: item.resource_parent_id,
        resource_name: item.resource_name,
        resource_type: item.resource_type,
        resource_type_cn: item.resource_type_cn,
        resource_title: item.resource_title,
        resource_desc: item.resource_desc,
        resource_icon: item.resource_icon,
        resource_format: item.resource_format,
        resource_size_in_MB: item.resource_size_in_MB,
        resource_status: item.resource_status,
        resource_source: item.resource_source,
        resource_source_url: item.resource_source_url,
        resource_show_url: item.resource_show_url,
        resource_language: item.resource_language,
        create_time: item.create_time,
        update_time: item.update_time,
        delete_time: item.delete_time
      };
      // 还原标签信息
      let new_data_tags = [];
      for (let tag_id of item.resource_tags) {
        for (let tag of res.result.resource_tags) {
          if (tag.id == tag_id) {
            new_data_tags.push(tag);
          }
        }
      }
      // @ts-ignore
      new_data.resource_tags = new_data_tags;
      // @ts-ignore
      current_resource_list.value.push(new_data);
    }
    current_resource_cnt.value = res.result.total;
  }
  resource_loading.value = false;
  await search_resource_jumper();
}
export async function search_resource_recycle_bin() {
  // 回收站
  let params = {
    resource_type: [],
    resource_format: resourceFormats.value,
    resource_tags: [],
    page_size: current_page_size.value,
    page_num: current_page_num.value
  };
  // 更新resource_type 的值
  for (let resource_type of current_resource_types.value) {
    if (resource_types_name_map?.[resource_type]) {
      params.resource_type.push(resource_types_name_map?.[resource_type]);
      continue;
    }
    params.resource_type.push(resource_type);
  }
  // for (let resource_format of current_resource_formats.value) {
  //   if (resource_format != '未知') {
  //     params.resource_format.push(resource_format);
  //   } else {
  //     params.resource_format.push('');
  //   }
  // }
  for (let resource_tag of current_resource_tags.value) {
    if (resource_tag.id) {
      params.resource_tags.push(resource_tag.id);
    }
  }
  resource_loading.value = true;
  let res = await search_resource_in_recycle(params);
  if (!res.error_status) {
    current_resource_list.value = [];
    for (let item of res.result.data) {
      current_resource_list.value.push({
        id: item.id,
        resource_parent_id: item.resource_parent_id,
        resource_name: item.resource_name,
        resource_type: item.resource_type,
        resource_type_cn: item.resource_type_cn,
        resource_title: item.resource_title,
        resource_desc: item.resource_desc,
        resource_icon: item.resource_icon,
        resource_format: item.resource_format,
        resource_size_in_MB: item.resource_size_in_MB,
        resource_status: item.resource_status,
        resource_source: item.resource_source,
        resource_source_url: item.resource_source_url,
        resource_show_url: item.resource_show_url,
        resource_language: item.resource_language,
        create_time: item.create_time,
        update_time: item.update_time,
        delete_time: item.delete_time,
        // @ts-ignore
        left_time: item.left_time
      });
    }
    current_resource_cnt.value = res.result.total;
  }

  resource_loading.value = false;
  await search_resource_jumper();
}
export async function search_resource_by_keyword() {
  const { authType } = storeToRefs(useResourceStore());
  // 根据关键字搜索资源
  let params = {
    resource_type: [],
    resource_format: resourceFormats.value,
    resource_tags: [],
    page_size: current_page_size.value,
    page_num: current_page_num.value,
    resource_keyword: current_tag.value.tag_name,
    rag_enhance: search_rag_enhance.value,
    auth_type: authType.value
  };
  // 更新resource_type 的值
  for (let resource_type of current_resource_types.value) {
    if (resource_types_name_map?.[resource_type]) {
      params.resource_type.push(resource_types_name_map?.[resource_type]);
      continue;
    }
    params.resource_type.push(resource_type);
  }
  // for (let resource_format of current_resource_formats.value) {
  //   if (resource_format != '未知') {
  //     params.resource_format.push(resource_format);
  //   } else {
  //     params.resource_format.push('');
  //   }
  // }
  for (let resource_tag of current_resource_tags.value) {
    if (resource_tag.id) {
      params.resource_tags.push(resource_tag.id);
    }
  }
  resource_loading.value = true;
  let res = await search_resource_by_resource_keyword(params);
  if (!res.error_status) {
    current_resource_list.value = [];
    current_resource_cnt.value = res.result.total;
    // 获取作者信息
    sortResourceList(res.result.data);
    for (let item of res.result.data) {
      // 获取作者信息
      let author_info = null;
      for (let user of res.result.author_info) {
        if (user.user_id == item.user_id) {
          author_info = user;
          break;
        }
      }
      // @ts-ignore
      current_resource_list.value.push({
        id: item.id,
        resource_parent_id: item.resource_parent_id,
        resource_name: item.resource_name,
        resource_type: item.resource_type,
        resource_type_cn: item.resource_type_cn,
        resource_title: item.resource_title,
        resource_desc: item.resource_desc,
        resource_icon: item.resource_icon,
        resource_format: item.resource_format,
        resource_size_in_MB: item.resource_size_in_MB,
        resource_status: item.resource_status,
        resource_source: item.resource_source,
        resource_source_url: item.resource_source_url,
        resource_show_url: item.resource_show_url,
        resource_language: item.resource_language,
        create_time: item.create_time,
        update_time: item.update_time,
        rerank_score: item.rerank_score,
        ref_text: item.ref_text,
        // @ts-ignore
        user_id: item.user_id,
        author_info: author_info,
        authType: item.auth_type
      });
    }
    current_resource_cnt.value = res.result.total;
  }
  // let share_res = await resource_share_search_by_keyword(params)
  // if (!share_res.error_status){
  //
  //     for (let item of share_res.result.data){
  //         // 如果存在重复的资源，则不再添加
  //         let is_exist = false
  //         for (let resource of current_resource_list.value){
  //             if (resource.id == item.id){
  //                 is_exist = true
  //                 break
  //             }
  //         }
  //         if (is_exist){
  //             continue
  //         }
  //         current_resource_cnt.value += 1
  //         // 获取作者信息
  //         let author_info = null
  //         for (let user of share_res.result.author_info){
  //             if (user.user_id == item.user_id){
  //                 author_info = user
  //                 break
  //             }
  //         }
  //         // @ts-ignore
  //         current_resource_list.value.push({
  //         id: item.id,
  //         resource_parent_id: item.resource_parent_id,
  //         resource_name: item.resource_name ,
  //         resource_type: item.resource_type ,
  //         resource_type_cn: item.resource_type_cn ,
  //         resource_title: item.resource_title,
  //         resource_desc: item.resource_desc,
  //         resource_icon: item.resource_icon ,
  //         resource_format: item.resource_format ,
  //         resource_size_in_MB: item.resource_size_in_MB ,
  //         resource_status: item.resource_status ,
  //         resource_source: item.resource_source,
  //         resource_source_url: item.resource_source_url,
  //         resource_show_url: item.resource_show_url,
  //         resource_language: item.resource_language,
  //         create_time: item.create_time ,
  //         update_time: item.update_time ,
  //         rerank_score: item.rerank_score,
  //         ref_text: item.ref_text,
  //         // @ts-ignore
  //         user_id: item.user_id,
  //         author_info: author_info
  //     })
  //         current_resource_cnt.value += 1
  //     }
  // }
  resource_loading.value = false;
  resource_shortcut_Ref.value?.sort('rerank_score', 'descending');
  await search_resource_jumper();
}
export async function search_resource_jumper() {
  // 如果过滤参数不为默认值，则将参数推送至url
  if (current_resource_types.value.length != 11) {
    router.push({
      params: {
        ...router.currentRoute.value.params
      },
      query: {
        ...router.currentRoute.value.query,
        resource_type: current_resource_types.value
      }
    });
  }
  let all_resource_tags = [];
  for (let tag of current_resource_tags.value) {
    all_resource_tags.push(tag.id);
  }
  router.push({
    params: {
      ...router.currentRoute.value.params
    },
    query: {
      ...router.currentRoute.value.query,
      tag_id: all_resource_tags,
      page_size: current_page_size.value,
      page_num: current_page_num.value
    }
  });
}
export async function handle_selection_change(val: ResourceItem[]) {
  // 多选框选中事件
  multiple_selection.value = val;
  show_multiple_button.value = !!val.length;
  for (let item of val) {
    item.resource_is_selected = true;
  }
}
export function get_upload_progress(item: ResourceItem) {
  // @ts-ignore
  if (item.task_status == 'success') {
    return 100;
  }
  // @ts-ignore
  const res = Math.round(((item.content_finish_idx + 1) / (item.content_max_idx + 1)) * 100);
  return res || 0;
}
export function show_upload_progress_status(item: ResourceItem) {
  let progress = get_upload_progress(item);
  if (progress == 100) {
    return 'success';
  }

  return null;
}
export function batch_move_select_resources() {
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
  show_move_dialog_multiple(selected_resources);
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
export function batch_share_select_resource() {
  let selected_resources = [];
  for (let resource of multiple_selection.value) {
    if (resource.id && resource.resource_status == '正常') {
      selected_resources.push(resource.id);
    }
  }
  // 调用分享接口
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
  let params = {
    resource_list: []
  };
  let delete_cnt = 0;
  for (let item of multiple_selection.value) {
    if (item.resource_status != '删除' && item?.id) {
      params.resource_list.push(item.id);
    } else {
      delete_cnt += 1;
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
  let res = await batch_delete_resource_object(params);
  if (!res.error_status) {
    ElNotification({
      title: '系统通知',
      message: `共成功删除${res.result.delete_cnt}个资源!`,
      type: 'success',
      duration: 5000
    });
  }
  await search_resource_by_tags();
  refresh_panel_count();
}
export async function batch_rebuild() {
  // 批量重建

  let params = {
    resource_list: []
  };

  for (let item of multiple_selection.value) {
    if (item?.id && item.resource_status == '正常' && check_resource_rag_support(item)) {
      params.resource_list.push(item.id);
    }
  }
  if (!params.resource_list.length) {
    ElMessage.warning('所选资源无法构建索引!');
    return;
  }
  let res = await build_resource_object_ref(params);
  if (!res.error_status) {
    let task_cnt = res.result.build_cnt;
    ElNotification({
      title: '系统通知',
      message: `共成功提交${task_cnt}个重新构建任务，请耐心等待!`,
      type: 'success',
      duration: 5000
    });
  }
}
export function cancel_multiple_selection() {
  show_multiple_button.value = false;
  for (let item of multiple_selection.value) {
    item.resource_is_selected = false;
  }
  multiple_selection.value = [];
  resource_shortcut_Ref.value.clearSelection();
}
export async function handleSizeChange(val: number) {
  // 更新路由
  current_page_size.value = val;
  await search_resource_by_tags();
}
export async function handleCurrentChange(val: number) {
  // 更新路由
  current_page_num.value = val;
  await search_resource_by_tags();
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
    router.push({
      name: 'resource_list',
      params: {
        resource_id: resource.id
      }
    });
    return;
  }
  // if (resource.resource_type == 'document'){
  //     const route = router.resolve({
  //         name: 'resource_viewer',
  //         params: { resource_id: resource.id }
  //     }).href
  //     // 打开新页面
  //     window.open(route, '_blank')
  //     return
  // }
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
  if (resource.user_id == user_info.value.user_id) {
    turn_on_resource_meta(resource.id);
  } else {
    turn_on_resource_meta(resource.id, '共享');
  }
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
export async function share_resource(resource: ResourceItem) {
  // 分享资源
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除，请恢复后分享!');
    return;
  }
  // 调用分享接口
  await turn_on_share_selector(resource);
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
  show_move_dialog_multiple([resource.id]);
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
    await search_resource_by_tags();
  }
  refresh_panel_count();
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
  resource_shortcut_Ref.value?.toggleRowSelection(resource);
}
export function get_timestamp_duration(duration) {
  // 格式化为人可读的单位

  if (duration < 1000) {
    return duration + 'ms';
  }
  if (duration < 1000 * 60) {
    return Math.round(duration / 1000) + 's';
  }
  if (duration < 1000 * 60 * 60) {
    return Math.round(duration / 1000 / 60) + 'min';
  }
  if (duration < 1000 * 60 * 60 * 24) {
    return Math.round(duration / 1000 / 60 / 60) + 'h';
  }
  return Math.round(duration / 1000 / 60 / 60 / 24) + 'd';
}
export function handleDragOver(event) {
  event.preventDefault();
}

// 回收站
export const show_recover_flag = ref(false);
export const completely_delete_flag = ref(false);
export async function batch_recover_resources() {
  show_recover_flag.value = false;
  let params = {
    resource_list: []
  };
  let recover_cnt = 0;
  for (let item of multiple_selection.value) {
    if (item.resource_status == '删除' && item?.id) {
      params.resource_list.push(item.id);
    } else {
      recover_cnt += 1;
    }
  }
  if (!params.resource_list.length) {
    ElNotification({
      title: '系统通知',
      message: `所选资源均已恢复!`,
      type: 'info',
      duration: 5000
    });
    return;
  }
  let res = await recover_resource_recycle_object(params);
  if (!res.error_status) {
    ElNotification({
      title: '系统通知',
      message: `共成功恢复${res.result.recover_cnt}个资源!`,
      type: 'success',
      duration: 5000
    });
  }
  await search_resource_by_tags();
}
export async function batch_completely_delete_resources() {
  completely_delete_flag.value = false;
  let params = {
    resource_list: []
  };
  // console.log(multiple_selection.value)
  for (let item of multiple_selection.value) {
    if (item.resource_status == '删除' && item?.id) {
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
  let res = await delete_resource_recycle_object(params);
  if (!res.error_status) {
    ElNotification({
      title: '系统通知',
      message: `共成功彻底删除${res.result.delete_cnt}个资源!`,
      type: 'success',
      duration: 5000
    });
  }
  await search_resource_by_tags();
}
export async function show_delete_resource_detail(resource: ResourceItem) {
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '正常') {
    ElMessage.warning('资源未删除!');
    return;
  }
  turn_on_resource_meta(resource.id, '删除');
}
export async function recover_resource(resource: ResourceItem) {
  let params = {
    resource_list: [resource.id]
  };
  let res = await recover_resource_recycle_object(params);
  if (!res.error_status) {
    ElMessage.success('恢复成功!');
    await search_resource_by_tags();
  }
  resource_shortcut_card_buttons_Ref.value?.hide();
  button_Ref.value?.hide();
}
export async function completely_delete_resource(resource: ResourceItem) {
  let params = {
    resource_list: [resource.id]
  };
  let res = await delete_resource_recycle_object(params);
  if (!res.error_status) {
    ElMessage.success('彻底删除成功!');
    await search_resource_by_tags();
  }
}

// 搜索
export function getHighlightedText(text: string) {
  if (!current_tag.value?.tag_name || !text) {
    return text;
  }
  const regex = new RegExp(`(${current_tag.value.tag_name})`, 'gi');
  return text.replace(regex, '<span class="highlight-resource-keyword">$1</span>');
}
export function getMarkdownHtml(text: string) {
  return md_answer.render(text);
}
