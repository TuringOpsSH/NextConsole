import request from '@/utils/request'
import {ServerResponse} from "@/types/response";
import {ElNotification} from "element-plus";

let env_url = '/next_console_admin'

if (process.env.NODE_ENV === 'development') {
    env_url = '/dev/next_console_admin';
}  else if (process.env.NODE_ENV === 'local') {
    env_url = '/local/next_console_admin';
}

export const api = {
    add_dataset : env_url + '/dataset_center/dataset/add',
    search_dataset : env_url + '/dataset_center/dataset/search',
    get_dataset : env_url + '/dataset_center/dataset/get',
    update_dataset : env_url + '/dataset_center/dataset/update',
    delete_dataset : env_url + '/dataset_center/dataset/delete',

    add_dataset_sample : env_url + '/dataset_center/data_sample/add',
    search_dataset_sample : env_url + '/dataset_center/data_sample/search',
    get_dataset_sample : env_url + '/dataset_center/data_sample/get',
    update_dataset_sample : env_url + '/dataset_center/data_sample/update',
    delete_dataset_sample : env_url + '/dataset_center/data_sample/delete',
    download_dataset_sample : env_url + '/dataset_center/data_sample/download',
    dryrun_dataset_sample : env_url + '/dataset_center/data_sample/dryrun',
    get_relate_dataset: env_url + '/dataset_center/data_sample/relate_dataset/get',
    update_relate_dataset: env_url + '/dataset_center/data_sample/relate_dataset/update',
    get_data_sample_context: env_url + '/dataset_center/data_sample/get_data_sample_context',

    search_instructions: env_url + '/dataset_center/instructions/search',
    extract_result: env_url + '/dataset_center/instructions/result_extract',
    upsert_tags: env_url + '/dataset_center/data_sample/tags/upsert',
    get_tags: env_url + '/dataset_center/data_sample/tags/get',

}

export async function add_dataset(data:object):Promise<ServerResponse>{
    return request({
        url: api.add_dataset,
        method: 'post',
        data: data
    })
}

export async function search_dataset(data:object):Promise<ServerResponse>{
    return request({
        url: api.search_dataset,
        
        data: data
    })
}

export async function get_dataset(data:object):Promise<ServerResponse>{
    return request({
        url: api.get_dataset,
        
        data: data
    })
}

export async function update_dataset(data:object):Promise<ServerResponse>{
    return request({
        url: api.update_dataset,
        method: 'post',
        data: data
    })
}

export async function delete_dataset(data:object):Promise<ServerResponse>{
    return request({
        url: api.delete_dataset,
        method: 'post',
        data: data
    })
}

export async function add_dataset_sample(data:object):Promise<ServerResponse>{
    return request({
        url: api.add_dataset_sample,
        method: 'post',
        data: data
    })
}

export async function search_dataset_sample(data:object):Promise<ServerResponse>{
    return request({
        url: api.search_dataset_sample,
        
        data: data
    })
}

export async function get_dataset_sample(data:object):Promise<ServerResponse>{
    return request({
        url: api.get_dataset_sample,
        
        data: data
    })
}

export async function update_dataset_sample(data:object):Promise<ServerResponse>{
    return request({
        url: api.update_dataset_sample,
        method: 'post',
        data: data
    })
}

export async function delete_dataset_sample(data:object):Promise<ServerResponse>{
    return request({
        url: api.delete_dataset_sample,
        method: 'post',
        data: data
    })
}

export async function download_dataset_sample(data:object){
    try {
        const blob: Blob = await request(
            {
                url:api.download_dataset_sample,
                data:data,
                responseType: 'blob'
            }) as Blob;
        const url = window.URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.setAttribute('download', '样本数据.xlsx');
        link.href = url;
        document.body.appendChild(link);
        link.click();
        // 清理
        window.URL.revokeObjectURL(url);
        link.remove(); // 移除创建的<a>标签
    }
    catch (e) {
        ElNotification.error({
            title:"系统通知",
            message:"下载失败！" + e.toString(),
            duration:888
        })
    }

}

export async function dryrun_dataset_sample(data:object):Promise<ServerResponse>{
    return request({
        url: api.dryrun_dataset_sample,
        method: 'post',
        data: data
    })
}

export async function search_instructions(data:object):Promise<ServerResponse>{
    return request({
        url: api.search_instructions,
        
        data: data
    })
}

export async function get_relate_dataset(data:object):Promise<ServerResponse>{
    return request({
        url: api.get_relate_dataset,

        data: data
    })
}
export async function update_relate_dataset(data:object):Promise<ServerResponse>{
    return request({
        url: api.update_relate_dataset,
        method: 'post',
        data: data
    })
}

export async function upsert_tags(data:object):Promise<ServerResponse>{
    return request({
        url: api.upsert_tags,
        method: 'post',
        data: data
    })
}

export async function get_tags(data:object):Promise<ServerResponse>{
    return request({
        url: api.get_tags,

        data: data
    })
}

export async function extract_result(data:object):Promise<ServerResponse>{
    return request({
        url: api.extract_result,
        method: 'post',
        data: data
    })
}

export async function get_data_sample_context_msg(data:object):Promise<ServerResponse>{
    return request({
        url: api.get_data_sample_context,

        data: data
    })
}

