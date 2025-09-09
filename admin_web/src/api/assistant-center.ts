import request from '@/utils/request'
import {ServerResponse} from "@/types/response";


let env_url = ''

export const api = {
    assistant_add: env_url + '/console/assistant_center/assistant_manage/assistants/add',
    assistant_update: env_url + '/console/assistant_center/assistant_manage/assistants/update',
    assistant_delete: env_url + '/console/assistant_center/assistant_manage/assistants/delete',
    assistant_search: env_url + '/console/assistant_center/assistant_manage/assistants/search',
    assistant_get: env_url + '/ces_os/assistant_center/assistant_manage/assistants/get',
    assistant_metric: env_url + '/console/assistant_center/assistant_manage/assistants/metric/get',
    models_search: env_url + '/console/assistant_center/assistant_manage/models/search',
    assistant_avatar_upload: env_url + '/console/assistant_center/assistant_manage/assistants/avatar/upload',
    change_target_assistant: env_url + '/console/assistant_center/assistant_manage/assistants/change',
    list_shop_assistants: env_url + '/console/assistant_center/shop_assistant_manage/shop_assistants/listing',
    off_list_shop_assistants: env_url + '/console/assistant_center/shop_assistant_manage/shop_assistants/off_listing',
    shop_assistant_search: env_url + '/console/assistant_center/shop_assistant_manage/shop_assistants/search',
    shop_assistant_subscribe: env_url + '/console/assistant_center/shop_assistant_manage/shop_assistants/subscribe',
    shop_assistant_unsubscribe: env_url + '/console/assistant_center/shop_assistant_manage/shop_assistants/unsubscribe',
    shop_assistant_switch: env_url + '/console/assistant_center/shop_assistant_manage/shop_assistants/switch',
    shop_assistant_comment: env_url + '/console/assistant_center/shop_assistant_manage/shop_assistants/comment',
    shop_assistant_get: env_url + '/console/assistant_center/shop_assistant_manage/shop_assistants/get',


}

export async function assistant_search(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.assistant_search,
            data:params,
            responseType: 'json'
        }
    )
}

export async function assistant_add(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.assistant_add,
            data:params,
            responseType: 'json'
        }
    )
}

export async function assistant_update(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.assistant_update,
            data:params,
            responseType: 'json'
        }
    )
}

export async function assistant_delete(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.assistant_delete,
            data:params,
            responseType: 'json'
        }
    )
}

export async function assistant_get(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.assistant_get,
            data:params,
            responseType: 'json'
        }
    )
}

export async function assistant_metric(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.assistant_metric,
            data:params,
            responseType: 'json'
        }
    )
}

export async function models_search(): Promise<ServerResponse>{
    return request(
        {
            method:'get',
            url:api.models_search,
            responseType: 'json'
        }
    )
}

export async function change_target_assistant(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.change_target_assistant,
            data:params,
            responseType: 'json'
        }
    )
}

export async function list_shop_assistants(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.list_shop_assistants,
            data:params,
            responseType: 'json'
        }
    )
}


export async function off_list_shop_assistants(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.off_list_shop_assistants,
            data:params,
            responseType: 'json'
        }
    )
}

export async function shop_assistant_search(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.shop_assistant_search,
            data:params,
            responseType: 'json'
        }
    )
}

export async function shop_assistant_subscribe(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.shop_assistant_subscribe,
            data:params,
            responseType: 'json'
        }
    )
}

export async function shop_assistant_unsubscribe(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.shop_assistant_unsubscribe,
            data:params,
            responseType: 'json'
        }
    )
}

export async function shop_assistant_switch(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.shop_assistant_switch,
            data:params,
            responseType: 'json'
        }
    )
}

export async function shop_assistant_comment(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.shop_assistant_comment,
            data:params,
            responseType: 'json'
        }
    )
}

export async function shop_assistant_get(params:object): Promise<ServerResponse>{
    return request(
        {
            url:api.shop_assistant_get,
            data:params,
            responseType: 'json'
        }
    )
}
