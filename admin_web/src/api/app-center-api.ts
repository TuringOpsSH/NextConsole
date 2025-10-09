import { useUserInfoStore } from '@/stores/user-info-store';
import { ServerResponse } from '@/types/response';
import request from '@/utils/request';

const envUrl = '';
export const api = {
  app_search: envUrl + '/next_console_admin/app_center/app_manage/search',
  app_icon_upload: envUrl + '/next_console_admin/app_center/app_manage/icon/upload',
  app_add: envUrl + '/next_console_admin/app_center/app_manage/add',
  app_delete: envUrl + '/next_console_admin/app_center/app_manage/delete',
  app_detail: envUrl + '/next_console_admin/app_center/app_manage/detail',
  app_update: envUrl + '/next_console_admin/app_center/app_manage/update',
  app_upload: envUrl + '/next_console_admin/app_center/app_manage/upload',
  app_import: envUrl + '/next_console_admin/app_center/app_manage/import',
  workflow_icon_upload: envUrl + '/next_console_admin/app_center/app_manage/workflow/icon_upload',
  workflow_create: envUrl + '/next_console_admin/app_center/app_manage/workflow/create',
  workflow_delete: envUrl + '/next_console_admin/app_center/app_manage/workflow/delete',
  workflow_update: envUrl + '/next_console_admin/app_center/app_manage/workflow/update',
  workflow_detail: envUrl + '/next_console_admin/app_center/app_manage/workflow/detail',
  workflow_search: envUrl + '/next_console_admin/app_center/app_manage/workflow/search',
  workflow_restore: envUrl + '/next_console_admin/app_center/app_manage/workflow/restore',
  workflow_export: envUrl + '/next_console_admin/app_center/app_manage/workflow/export',
  workflow_import: envUrl + '/next_console_admin/app_center/app_manage/workflow/import',
  workflow_upload: envUrl + '/next_console_admin/app_center/app_manage/workflow/upload',
  workflow_node_init: envUrl + '/next_console_admin/app_center/app_manage/workflow/node/init',
  workflow_node_update: envUrl + '/next_console_admin/app_center/app_manage/workflow/node/update',
  workflow_node_delete: envUrl + '/next_console_admin/app_center/app_manage/workflow/node/delete',
  workflow_node_detail: envUrl + '/next_console_admin/app_center/app_manage/workflow/node/detail',
  workflow_node_avatar: envUrl + '/next_console_admin/app_center/app_manage/workflow/node/agent_avatar_upload',
  workflow_node_search: envUrl + '/next_console_admin/app_center/app_manage/workflow/node/search',
  workflow_node_copy: envUrl + '/next_console_admin/app_center/app_manage/workflow/node/copy',
  workflow_check: envUrl + '/next_console_admin/app_center/app_manage/workflow/check',
  init_app_session: envUrl + '/next_console_admin/app_center/app_run/init_session',
  add_app_message: envUrl + '/next_console_admin/app_center/app_run/messages/add',
  prodAppSearch: envUrl + '/next_console_admin/app_center/publish_manage/search_prod_app',
  publishCreate: envUrl + '/next_console_admin/app_center/publish_manage/create',
  publishSearch: envUrl + '/next_console_admin/app_center/publish_manage/search',
  publishExport: envUrl + '/next_console_admin/app_center/publish_manage/export',
  publishDelete: envUrl + '/next_console_admin/app_center/publish_manage/delete',
  accessSearch: envUrl + '/next_console_admin/app_center/publish_manage/search_access',
  accessAuthor: envUrl + '/next_console_admin/app_center/publish_manage/author',
  accessUnAuthor: envUrl + '/next_console_admin/app_center/publish_manage/unauthor',
  runningStatus: envUrl + '/next_console_admin/app_center/publish_manage/running_status',
  getDebugInfo: envUrl + '/next_console_admin/app_center/app_run/debug_info'
};

export async function appSearch(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_search,
    data: params,
    responseType: 'json'
  });
}

export async function appAdd(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_add,
    data: params,
    responseType: 'json'
  });
}

export async function appDelete(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_delete,
    data: params,
    responseType: 'json'
  });
}

export async function appDetail(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_detail,
    data: params,
    responseType: 'json'
  });
}

export async function appUpdate(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_update,
    data: params,
    responseType: 'json'
  });
}

export async function appIconUpload(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_icon_upload,
    data: params,
    responseType: 'json'
  });
}

export async function appUpload(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_upload,
    data: params,
    responseType: 'json'
  });
}

export async function appImport(params: object): Promise<ServerResponse> {
  return request({
    url: api.app_import,
    data: params,
    responseType: 'json'
  });
}

export async function workFlowIconUpload(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_icon_upload,
    data: params,
    responseType: 'json'
  });
}

export async function workflowCreate(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_create,
    data: params,
    responseType: 'json'
  });
}

export async function workflowDelete(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_delete,
    data: params,
    responseType: 'json'
  });
}

export async function workflowUpdate(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_update,
    data: params,
    responseType: 'json'
  });
}

export async function workflowDetail(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_detail,
    data: params,
    responseType: 'json'
  });
}

export async function workflowSearch(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_search,
    data: params,
    responseType: 'json'
  });
}

export async function workflowRestore(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_restore,
    data: params,
    responseType: 'json'
  });
}

export async function workflowExport(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_export,
    data: params,
    responseType: 'json'
  });
}

export async function workflowImport(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_import,
    data: params,
    responseType: 'json'
  });
}

export async function workflowCheck(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_check,
    data: params,
    responseType: 'json'
  });
}

export async function nodeInit(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_node_init,
    data: params,
    responseType: 'json'
  });
}

export async function nodeUpdate(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_node_update,
    data: params,
    responseType: 'json'
  });
}

export async function nodeDelete(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_node_delete,
    data: params,
    responseType: 'json'
  });
}

export async function nodeDetail(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_node_detail,
    data: params,
    responseType: 'json'
  });
}

export async function nodeSearch(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_node_search,
    data: params,
    responseType: 'json'
  });
}

export async function nodeCopy(params: object): Promise<ServerResponse> {
  return request({
    url: api.workflow_node_copy,
    data: params,
    responseType: 'json'
  });
}

export async function initAppSession(params: object): Promise<ServerResponse> {
  return request({
    url: api.init_app_session,
    data: params,
    responseType: 'json'
  });
}

export async function addAppMessage(params: object, signal: AbortSignal | null): Promise<ServerResponse> {
  if (params['stream']) {
    const userInfoStore = useUserInfoStore();
    const config: RequestInit = {
      method: 'POST',
      headers: {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        'Content-Type': 'application/json',
        // eslint-disable-next-line @typescript-eslint/naming-convention
        ...userInfoStore.userHeader
      },
      body: JSON.stringify(params),
      signal
    };
    // @ts-ignore
    return fetch(api.add_app_message, config);
  } else {
    return request({
      url: api.add_app_message,
      data: params,
      responseType: 'json'
    });
  }
}

export async function prodAppSearch(params: object): Promise<ServerResponse> {
  return request({
    url: api.prodAppSearch,
    data: params,
    responseType: 'json'
  });
}

export async function publishCreate(params: object): Promise<ServerResponse> {
  return request({
    url: api.publishCreate,
    data: params,
    responseType: 'json'
  });
}

export async function publishSearch(params: object): Promise<ServerResponse> {
  return request({
    url: api.publishSearch,
    data: params,
    responseType: 'json'
  });
}

export async function publishExport(params: object): Promise<ServerResponse> {
  return request({
    url: api.publishExport,
    data: params,
    responseType: 'json'
  });
}

export async function publishDelete(params: object): Promise<ServerResponse> {
  return request({
    url: api.publishDelete,
    data: params,
    responseType: 'json'
  });
}
export async function accessSearch(params: object): Promise<ServerResponse> {
  return request({
    url: api.accessSearch,
    data: params,
    responseType: 'json'
  });
}

export async function accessAuthor(params: object): Promise<ServerResponse> {
  return request({
    url: api.accessAuthor,
    data: params,
    responseType: 'json'
  });
}

export async function accessUnAuthor(params: object): Promise<ServerResponse> {
  return request({
    url: api.accessUnAuthor,
    data: params,
    responseType: 'json'
  });
}

export async function runningStatus(params: object): Promise<ServerResponse> {
  return request({
    url: api.runningStatus,
    data: params,
    responseType: 'json'
  });
}

export async function getDebugInfo(params: object): Promise<ServerResponse> {
  return request({
    url: api.getDebugInfo,
    data: params,
    responseType: 'json'
  });
}
