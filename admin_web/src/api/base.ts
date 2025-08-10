import request from '@/utils/request'
import {ServerResponse} from "@/types/response";


let env_url = ''



export const api = {
    version_get: env_url + '/next_console_admin/version',
    domain_get: env_url + '/next_console_admin/domain',


}

export async function version_get(): Promise<ServerResponse> {
    // @ts-ignore
    return request({
        url: api.version_get,
        noAuth: true

    })
}

export async function domainGet(): Promise<ServerResponse> {
    // @ts-ignore
    return request({
        url: api.domain_get,
        noAuth: true
    })
}

