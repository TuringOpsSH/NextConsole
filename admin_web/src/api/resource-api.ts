import { ISearchByKeywordsParams } from '@/types/resource-type';
import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

let envUrl = '';

export const api = {
  // 资源对象接口
  search_resource_object: envUrl + '/next_console_admin/resources/object/search',
  get_resource_object: envUrl + '/next_console_admin/resources/object/get',
  get_resource_object_path: envUrl + '/next_console_admin/resources/object/get_path',
  add_upload_task: envUrl + '/next_console_admin/resources/object/upload_task/add',
  update_upload_task: envUrl + '/next_console_admin/resources/object/upload_task/update',
  upload_resource_object: envUrl + '/next_console_admin/resources/object/upload',
  delete_resource_object: envUrl + '/next_console_admin/resources/object/delete',
  batch_delete_resource_object: envUrl + '/next_console_admin/resources/object/batch_delete',
  add_resource_object: envUrl + '/next_console_admin/resources/object/add',
  update_resource_object: envUrl + '/next_console_admin/resources/object/update',
  download_resource_object: envUrl + '/next_console_admin/resources/object/download',
  get_resource_usage: envUrl + '/next_console_admin/resources/usage/get',
  move_resources: envUrl + '/next_console_admin/resources/object/move',
  batch_download_resources: envUrl + '/next_console_admin/resources/object/batch_download',
  add_resource_shortcut: envUrl + '/next_console_admin/resources/shortcut/add',
  search_resource_shortcut: envUrl + '/next_console_admin/resources/shortcut/search',
  delete_resource_shortcut: envUrl + '/next_console_admin/resources/shortcut/delete',
  build_resource_object_ref: envUrl + '/next_console_admin/resources/ref/build',
  batch_create_folders: envUrl + '/next_console_admin/resources/object/batch_add_folder',
  upload_resource: envUrl + '/next_console_admin/resources/upload',
  // 资源快捷标签
  get_resource_recent_count: envUrl + '/next_console_admin/resources/resource_recent_count',
  search_resource_by_recent_upload: envUrl + '/next_console_admin/resources/search_by_recent_upload',
  get_resource_recent_format_count: envUrl + '/next_console_admin/resources/resource_recent_format_count',
  get_resource_type_count: envUrl + '/next_console_admin/resources/resource_type_count',
  search_resource_by_recent_index: envUrl + '/next_console_admin/resources/search_by_recent_index',
  search_resource_by_resource_type: envUrl + '/next_console_admin/resources/search_by_resource_type',
  search_resource_by_resource_tags: envUrl + '/next_console_admin/resources/search_by_resource_tags',
  search_resource_by_keyword: envUrl + '/next_console_admin/resources/search_by_resource_keyword',
  // 资源标签
  search_resource_tags: envUrl + '/next_console_admin/resources/tag/search',
  add_resource_tags: envUrl + '/next_console_admin/resources/tag/add',
  update_resource_tags: envUrl + '/next_console_admin/resources/tag/update',
  delete_resource_tags: envUrl + '/next_console_admin/resources/tag/delete',
  // 回收站
  search_resource_in_recycle: envUrl + '/next_console_admin/resources/recycle_object/search_in_recycle_bin',
  search_resource_recycle_object: envUrl + '/next_console_admin/resources/recycle_object/search',
  delete_resource_recycle_object: envUrl + '/next_console_admin/resources/recycle_object/delete',
  recover_resource_recycle_object: envUrl + '/next_console_admin/resources/recycle_object/recover',
  get_resource_recycle_object: envUrl + '/next_console_admin/resources/recycle_object/get',
  // 资源查看
  resource_view_meta_get: envUrl + '/next_console_admin/resources_view/get',
  // 资源共享
  resource_share_get_access_list: envUrl + '/next_console_admin/resources/share_object/get_access_list',
  resource_share_update_access_list: envUrl + '/next_console_admin/resources/share_object/update_access_list',
  resource_share_get_list: envUrl + '/next_console_admin/resources/share_object/get_list',
  resource_share_get_meta: envUrl + '/next_console_admin/resources/share_object/get_meta',
  resource_share_check_access: envUrl + '/next_console_admin/resources/share_object/check_access',
  resource_share_search_by_keyword: envUrl + '/next_console_admin/resources/share_object/search_by_keyword',
  resource_cooing_record_detail: envUrl + '/next_console_admin/resources/cooling_record_detail',
  resource_cooling_record_update: envUrl + '/next_console_admin/resources/cooling_record_update',
  search_by_keyword_in_resource: envUrl + '/next_console_admin/resources/object/search_by_keyword_in_resource',
  search_by_keyword_in_resource_share: envUrl + '/next_console_admin/resources/share_object/search_by_keyword_in_resource'
};

export async function search_resource_object(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_resource_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function get_resource_object(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_resource_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function get_resource_object_path(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_resource_object_path,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function add_upload_task(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.add_upload_task,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function update_upload_task(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.update_upload_task,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function upload_resource_object(params: FormData): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.upload_resource_object,
    data: params,
    responseType: 'json',
    // noAuth: true
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

export async function delete_resource_object_api(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.delete_resource_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function batch_delete_resource_object(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.batch_delete_resource_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function add_resource_object(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.add_resource_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function update_resource_object(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.update_resource_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function download_resource_object(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.download_resource_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function batch_download_resources(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.batch_download_resources,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function move_resources(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.move_resources,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function get_resource_usage(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_resource_usage,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

// 快捷方式
export async function add_resource_shortcut(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.add_resource_shortcut,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function search_resource_shortcut(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_resource_shortcut,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function delete_resource_shortcut(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.delete_resource_shortcut,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function build_resource_object_ref(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.build_resource_object_ref,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}
// 最近区域
export async function get_resource_recent_count(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_resource_recent_count,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function search_resource_by_recent_upload(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_resource_by_recent_upload,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function get_resource_recent_format_count(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_resource_recent_format_count,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function get_resource_type_count(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_resource_type_count,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function search_resource_tags(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_resource_tags,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function search_resource_by_recent_index(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_resource_by_recent_index,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function search_resource_by_resource_type(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_resource_by_resource_type,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function search_resource_by_resource_tags(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_resource_by_resource_tags,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function add_resource_tags(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.add_resource_tags,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function update_resource_tags(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.update_resource_tags,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function delete_resource_tags(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.delete_resource_tags,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

// 回收站
export async function delete_resource_recycle_object(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.delete_resource_recycle_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function recover_resource_recycle_object(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.recover_resource_recycle_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function search_resource_in_recycle(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_resource_in_recycle,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function get_resource_recycle_object(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.get_resource_recycle_object,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function search_resource_by_resource_keyword(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_resource_by_keyword,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function resource_view_meta_get(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resource_view_meta_get,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}
// 资源共享
export async function resource_share_get_access_list(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resource_share_get_access_list,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function resource_share_update_access_list(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resource_share_update_access_list,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function resource_share_get_list(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resource_share_get_list,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function resource_share_get_meta(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resource_share_get_meta,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function resource_share_check_access(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resource_share_check_access,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function resource_share_search_by_keyword(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resource_share_search_by_keyword,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function batch_create_folders(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.batch_create_folders,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function resource_cooing_record_detail(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resource_cooing_record_detail,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function resource_cooling_record_update(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.resource_cooling_record_update,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function searchByKeywordsApi(params: ISearchByKeywordsParams): Promise<ServerResponse> {
  return request({
    url: api.search_by_keyword_in_resource,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}

export async function searchByKeywordInResource(params: object): Promise<ServerResponse> {
  // @ts-ignore
  return request({
    url: api.search_by_keyword_in_resource_share,
    data: params,
    responseType: 'json'
    // noAuth: true
  });
}
