import request from '@/utils/request'


import {ServerResponse} from "@/types/response";

let env_url = ''

export const api = {
    list_task: env_url + '/next_console_admin/user_center/user_notice_service/list',
    search_task: env_url + '/next_console_admin/user_center/user_notice_service/search',
    delete_task: env_url + '/next_console_admin/user_center/user_notice_service/del',
    get_task_detail: env_url + '/next_console_admin/user_center/user_notice_service/detail',
    init_task: env_url + '/next_console_admin/user_center/user_notice_service/init',
    update_task: env_url + '/next_console_admin/user_center/user_notice_service/update',
    search_notice_company: env_url + '/next_console_admin/user_center/user_notice_service/search_notice_company',
    search_notice_department: env_url + '/next_console_admin/user_center/user_notice_service/search_notice_department',
    search_notice_user: env_url + '/next_console_admin/user_center/user_notice_service/search_notice_user',
    start_task: env_url + '/next_console_admin/user_center/user_notice_service/start',
    pause_task: env_url + '/next_console_admin/user_center/user_notice_service/pause',
    resume_task: env_url + '/next_console_admin/user_center/user_notice_service/resume',
    stop_task: env_url + '/next_console_admin/user_center/user_notice_service/stop',
    list_task_instance: env_url + '/next_console_admin/user_center/user_notice_service/list_instance',
}

export async function list_task(params:object) :Promise<ServerResponse> {
    return request({
        url: api.list_task,
        method: 'post',
        data: params
    })
}

export async function search_task(params:object) :Promise<ServerResponse> {
    return request({
        url: api.search_task,
        method: 'post',
        data: params
    })
}

export async function delete_task(params:object) :Promise<ServerResponse> {
    return request({
        url: api.delete_task,
        method: 'post',
        data: params
    })
}

export async function get_task_detail(params:object) :Promise<ServerResponse> {
    return request({
        url: api.get_task_detail,
        method: 'post',
        data: params
    })
}

export async function init_task(params:object) :Promise<ServerResponse> {
    return request({
        url: api.init_task,
        method: 'post',
        data: params
    })
}

export async function update_task(params:object) :Promise<ServerResponse> {
    return request({
        url: api.update_task,
        method: 'post',
        data: params
    })
}

export async function search_notice_company(params:object) :Promise<ServerResponse> {
    return request({
        url: api.search_notice_company,
        method: 'post',
        data: params
    })
}


export async function search_notice_department(params:object) :Promise<ServerResponse> {
    return request({
        url: api.search_notice_department,
        method: 'post',
        data: params
    })
}

export async function search_notice_user(params:object) :Promise<ServerResponse> {
    return request({
        url: api.search_notice_user,
        method: 'post',
        data: params
    })
}

export async function start_task(params:object) :Promise<ServerResponse> {
    return request({
        url: api.start_task,
        method: 'post',
        data: params
    })
}

export async function pause_task(params:object) :Promise<ServerResponse> {
    return request({
        url: api.pause_task,
        method: 'post',
        data: params
    })
}

export async function resume_task(params:object) :Promise<ServerResponse> {
    return request({
        url: api.resume_task,
        method: 'post',
        data: params
    })
}

export async function stop_task(params:object) :Promise<ServerResponse> {
    return request({
        url: api.stop_task,
        method: 'post',
        data: params
    })
}

export async function list_task_instance(params:object) :Promise<ServerResponse> {
    return request({
        url: api.list_task_instance,
        method: 'post',
        data: params
    })
}
