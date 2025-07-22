import { ServerResponse } from '@/types/response';
import { getToken } from '@/utils/auth';
import request from '@/utils/request';

let envUrl = '';

export const api = {
  create_session: envUrl + '/next_console/session/add',
  delete_session: envUrl + '/next_console/session/del',
  update_session: envUrl + '/next_console/session/update',
  search_session: envUrl + '/next_console/session/search',
  create_qa: envUrl + '/next_console/qa/add',
  delete_qa: envUrl + '/next_console/qa/del',
  update_qa: envUrl + '/next_console/qa/update',
  search_qa: envUrl + '/next_console/qa/search',
  add_messages: envUrl + '/next_console/messages/add',
  add_messages2: envUrl + '/next_console/app_center/app_run/v2/chat/completions',
  search_messages: envUrl + '/next_console/messages/search',
  delete_messages: envUrl + '/next_console/messages/del',
  update_messages: envUrl + '/next_console/messages/update',

  attachment_base_init: envUrl + '/next_console/attachment/base_init',
  attachment_add_into_session: envUrl + '/next_console/attachment/add_into_session',
  attachment_remove_from_session: envUrl + '/next_console/attachment/remove_from_session',
  attachment_search_in_session: envUrl + '/next_console/attachment/search_in_session',
  attachment_get_detail: envUrl + '/next_console/attachment/get_detail',
  attachment_add_webpage_tasks: envUrl + '/next_console/attachment/add_webpage_tasks',
  attachment_search_resources: envUrl + '/next_console/attachment/search_resources',
  attachment_search_resources_by_rag: envUrl + '/next_console/attachment/search_resources_by_rag',
  attachment_search_share_resources: envUrl + '/next_console/attachment/search_share_resources',
  attachment_add_resources_into_session: envUrl + '/next_console/attachment/add_resources_into_session',
  attachment_get_all_resource_formats: envUrl + '/next_console/attachment/get_all_resource_formats',
  reference_search: envUrl + '/next_console/reference/search',
  update_recommend_question: envUrl + '/next_console/recommend_question/update',
  create_session_share: envUrl + '/next_console/session_share/create',
  get_share_session: envUrl + '/next_console/session_share/get',
  get_share_qa: envUrl + '/next_console/session_share/get_qa',
  get_share_message: envUrl + '/next_console/session_share/get_message',
  get_share_reference: envUrl + '/next_console/session_share/get_reference',
  get_workflow_progress: envUrl + '/next_console/workflow/get_progress',
  get_workflow_progress_batch: envUrl + '/next_console/workflow/get_progress_batch',
  create_user_feedback: envUrl + '/next_search/user_feedback/create'
};

export async function create_session(params: object): Promise<ServerResponse> {
  return request({
    url: api.create_session,
    data: params,
    responseType: 'json'
  });
}

export async function delete_session(params: object): Promise<ServerResponse> {
  return request({
    url: api.delete_session,
    data: params,
    responseType: 'json'
  });
}

export async function update_session(params: object): Promise<ServerResponse> {
  return request({
    url: api.update_session,
    data: params,
    responseType: 'json'
  });
}

export async function search_session(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_session,
    data: params,
    responseType: 'json'
  });
}

export async function create_qa(params: object): Promise<ServerResponse> {
  return request({
    url: api.create_qa,
    data: params,
    responseType: 'json'
  });
}

export function delete_qa(params: object): Promise<ServerResponse> {
  return request({
    url: api.delete_qa,
    data: params,
    responseType: 'json'
  });
}

export async function update_qa(params: object): Promise<ServerResponse> {
  return request({
    url: api.update_qa,
    data: params,
    responseType: 'json'
  });
}

export async function search_qa(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_qa,
    data: params,
    responseType: 'json'
  });
}

export async function add_messages(params: object, signal: AbortSignal | null): Promise<ServerResponse> {
  if (params['stream']) {
    const authHeader = 'Bearer ' + getToken();
    const config: RequestInit = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader && { Authorization: authHeader })
      },
      body: JSON.stringify(params),
      signal
    };
    // @ts-ignore
    return fetch(api.add_messages, config);
  } else {
    return request({
      url: api.add_messages,
      data: params,
      responseType: 'json'
    });
  }
}

export async function add_messages2(params: object, signal: AbortSignal | null): Promise<ServerResponse> {
  if (params['stream']) {
    const authHeader = 'Bearer ' + getToken();
    const config: RequestInit = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader && { Authorization: authHeader })
      },
      body: JSON.stringify(params),
      signal
    };
    // @ts-ignore
    return fetch(api.add_messages2, config);
  } else {
    return request({
      url: api.add_messages2,
      data: params,
      responseType: 'json'
    });
  }
}

export async function addAppMessages(params: object, signal: AbortSignal | null): Promise<ServerResponse> {
  // @ts-ignore
  const url = envUrl + '/next_console/app_center/' + params?.app_code + '/messages/add';
  if (params['stream']) {
    const authHeader = 'Bearer ' + getToken();
    const config: RequestInit = {
      method: 'POST',
      headers: {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        'Content-Type': 'application/json',
        // eslint-disable-next-line @typescript-eslint/naming-convention
        ...(authHeader && { Authorization: authHeader })
      },
      body: JSON.stringify(params),
      signal
    };
    // @ts-ignore
    return fetch(url, config);
  } else {
    return request({
      url: url,
      data: params,
      responseType: 'json'
    });
  }
}

export function search_messages(params: object): Promise<ServerResponse> {
  return request({
    url: api.search_messages,
    data: params,
    responseType: 'json'
  });
}

export function delete_messages(params: object): Promise<ServerResponse> {
  return request({
    url: api.delete_messages,
    data: params,
    responseType: 'json'
  });
}

export function update_messages(params: object): Promise<ServerResponse> {
  return request({
    url: api.update_messages,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_base_init(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_base_init,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_add_into_session(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_add_into_session,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_remove_from_session(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_remove_from_session,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_search_in_session(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_search_in_session,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_get_detail(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_get_detail,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_add_webpage_tasks(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_add_webpage_tasks,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_search_resources(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_search_resources,
    data: params,
    responseType: 'json'
  });
}
export async function attachment_search_resources_by_rag(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_search_resources_by_rag,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_search_share_resources(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_search_share_resources,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_add_resources_into_session(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_add_resources_into_session,
    data: params,
    responseType: 'json'
  });
}

export async function attachment_get_all_resource_formats(params: object): Promise<ServerResponse> {
  return request({
    url: api.attachment_get_all_resource_formats,
    data: params,
    responseType: 'json'
  });
}

export async function search_reference(params: object): Promise<ServerResponse> {
  return request({
    url: api.reference_search,
    data: params,
    responseType: 'json'
  });
}

export async function update_recommend_question(params: object): Promise<ServerResponse> {
  return request({
    url: api.update_recommend_question,
    data: params,
    responseType: 'json'
  });
}

export async function create_session_share(params: object): Promise<ServerResponse> {
  return request({
    url: api.create_session_share,
    data: params,
    responseType: 'json'
  });
}

export async function get_share_session(params: object): Promise<ServerResponse> {
  //@ts-ignore
  return request({
    url: api.get_share_session,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function get_share_qa(params: object): Promise<ServerResponse> {
  //@ts-ignore
  return request({
    url: api.get_share_qa,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}

export async function get_share_message(params: object): Promise<ServerResponse> {
  //@ts-ignore
  return request({
    url: api.get_share_message,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function get_share_reference(params: object): Promise<ServerResponse> {
  //@ts-ignore
  return request({
    url: api.get_share_reference,
    data: params,
    responseType: 'json',
    noAuth: true
  });
}
export async function get_workflow_progress_batch(params: object): Promise<ServerResponse> {
  return request({
    url: api.get_workflow_progress_batch,
    data: params,
    responseType: 'json'
  });
}
