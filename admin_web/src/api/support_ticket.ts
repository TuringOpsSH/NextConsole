import request from '@/utils/request'
import {ServerResponse} from "@/types/response";

let env_url = ''

export const api = {
    search_tickets : env_url + '/ces_os/support_ticket/search',
    get_ticket: env_url + '/ces_os/support_ticket/get',
    add_ticket: env_url + '/ces_os/support_ticket/add',
    update_ticket: env_url + '/ces_os/support_ticket/update',
    get_ticket_options: env_url + '/ces_os/support_ticket/get_options',
    update_ticket_stage: env_url + '/ces_os/support_ticket/update_stage',
    submit_ticket: env_url + '/ces_os/support_ticket/submit',
    get_ticket_change_list: env_url + '/ces_os/support_ticket/get_change_list',
    get_ticket_msg_list: env_url + '/ces_os/support_ticket/get_msg_list',
    add_ticket_question: env_url + '/ces_os/support_ticket/question',
    delete_ticket_attachment: env_url + '/ces_os/support_ticket/attachment/delete',
}

export async function search_ticket_list(params:object): Promise<ServerResponse>{
    return request({
        url: api.search_tickets,
        method: 'post',
        data: params
    })
}

export async function get_ticket(params:object): Promise<ServerResponse>{
    return request({
        url: api.get_ticket,
        method: 'post',
        data: params
    })
}

export async function add_ticket(params:object): Promise<ServerResponse>{
    return request({
        url: api.add_ticket,
        method: 'post',
        data: params
    })
}

export async function update_ticket(params:object): Promise<ServerResponse>{
    return request({
        url: api.update_ticket,
        method: 'post',
        data: params
    })
}
export async function get_ticket_options(params:object): Promise<ServerResponse>{
    return request({
        url: api.get_ticket_options,
        method: 'post',
        data: params
    })
}

export async function update_ticket_stage(params:object): Promise<ServerResponse>{
    return request({
        url: api.update_ticket_stage,
        method: 'post',
        data: params
    })
}

export async function submit_ticket(params:object): Promise<ServerResponse>{
    return request({
        url: api.submit_ticket,
        method: 'post',
        data: params
    })
}

export async function get_ticket_change_list(params:object): Promise<ServerResponse>{
    return request({
        url: api.get_ticket_change_list,
        method: 'post',
        data: params
    })
}

export async function get_ticket_msg_list(params:object): Promise<ServerResponse>{
    return request({
        url: api.get_ticket_msg_list,
        method: 'post',
        data: params
    })
}

export async function add_ticket_question_api(params:object): Promise<ServerResponse>{
    return request({
        url: api.add_ticket_question,
        method: 'post',
        data: params
    })
}

export async function delete_ticket_attachment_api(params:object): Promise<ServerResponse>{
    return request({
        url: api.delete_ticket_attachment,
        method: 'post',
        data: params
    })
}
