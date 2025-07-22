import request from '@/utils/request'
import {ServerResponse} from "@/types/response";

let env_url = ''

export const api = {
    update_session_evaluation: env_url + '/ces_os/online_service/session/update_evaluation',
    change_session_to_human_service: env_url + '/ces_os/online_service/session/change_to_human_service',
}

export async function update_session_evaluation(params: any): Promise<ServerResponse> {
    return request({
        url: api.update_session_evaluation,
        method: 'post',
        data: params
    })
}

export async function change_session_to_human_service(params: any): Promise<ServerResponse> {
    return request({
        url: api.change_session_to_human_service,
        method: 'post',
        data: params
    })
}
