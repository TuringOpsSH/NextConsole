import request, {download_request} from '@/utils/request'
import {ServerResponse} from "@/types/response";
import {ElNotification} from "element-plus";

let envUrl = ''

export const api = {
    parse_process: envUrl + '/next_console/file2index/parse_process',
    kg_list:envUrl +'/next_console/kg_process/kg_db/search',
    kg_detail:envUrl + '/next_console/kg_process/kg_db/get',
    kg_add:envUrl +'/next_console/kg_process/kg_db/add',
    kg_delete:envUrl +'/next_console/kg_process/kg_db/delete',
    kg_update:envUrl +'/next_console/kg_process/kg_db/update',
    kg_icon_upload:envUrl +'/next_console/kg_process/kg_db_icon/upload',
    kg_ref_build: envUrl + '/next_console/kg_process/kg_db_ref/build',
    kg_ref_rebuild: envUrl + '/next_console/kg_process/kg_db_ref/rebuild',
    kg_ref_get: envUrl + '/next_console/kg_process/kg_db_ref/get',
    kg_db_website_add: envUrl + '/next_console/kg_process/kg_db_website/add',
    kg_json_schema_update: envUrl + '/next_console/kg_process/kg_db/update_json_schema',
    kg_download: envUrl+ '/next_console/kg_process/kg_db/download',
    kg_batch_upload_template: envUrl + '/next_console/kg_process/kg_db/batch_upload_template',
    kg_batch_upload: envUrl + '/next_console/kg_process/kg_db/batch_upload',
    doc_upload: envUrl + '/next_console/kg_process/kg_db_doc/upload',
    doc_delete: envUrl + '/next_console/document_process/kg_db_doc/delete',
    doc_update: envUrl + '/next_console/document_process/kg_db_doc/update',
    doc_list: envUrl + '/next_console/document_process/kg_db_doc/search',
    doc_download: envUrl + '/next_console/document_process/kg_db_doc/download',
    doc_content: envUrl + '/next_console/document_process/kg_db_doc_content/get',
    doc_rebuild: envUrl + '/next_console/document_process/kg_db_doc/rebuild',
    doc_upload_before_check: envUrl + '/next_console/kg_process/kg_db_doc/upload_before_check',
    doc_batch_switch: envUrl + '/next_console/document_process/kg_db_doc/batch_switch',
    doc_batch_rebuild: envUrl + '/next_console/document_process/kg_db_doc/batch_rebuild',

}




export async function search_kg_list(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.kg_list,
            data:params,
            responseType: 'json'
        }
    )
}

export async function get_kg_detail(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.kg_detail,
            data:params,
            responseType: 'json'
        }
    )

}

export async function delete_kg(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.kg_delete,
            data:params,
            responseType: 'json'
        }
    )

}

export async function add_kg(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.kg_add,
            data:params,
            responseType: 'json'
        }
    )

}

export async function update_kg(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.kg_update,
            data:params,
            responseType: 'json'
        }
    )

}

export async function download_kg(params:object){
    try {
        // 使用类型断言确保返回的是 Blob 类型
        const blob: Blob = await request(
            {
                url:api.kg_download,
                data:params,
                responseType: 'blob'
            }) as Blob; // 这里使用类型断言

        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        // 使用断言确保file_name存在
        link.setAttribute('download', params["kg_code"] + ".zip");
        link.href = url;
        document.body.appendChild(link);
        link.click();

        // 清理
        window.URL.revokeObjectURL(url);
        link.remove(); // 移除创建的<a>标签
    } catch (error) {
        ElNotification.error(
            {
                title:'系统通知',
                message: '知识库下载失败:' + error.toString(),
                duration: 6666,
            }
        );
    }
}

export async function get_kg_upload_template(params:object){
    try {
        // 使用类型断言确保返回的是 Blob 类型
        const blob: Blob = await request(
            {
                url:api.kg_batch_upload_template,
                data:params,
                responseType: 'blob'
            }) as Blob; // 这里使用类型断言

        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        // 使用断言确保file_name存在
        link.setAttribute('download', params["kg_code"] + "_template.xlsx");
        link.href = url;
        document.body.appendChild(link);
        link.click();

        // 清理
        window.URL.revokeObjectURL(url);
        link.remove(); // 移除创建的<a>标签
    } catch (error) {
        ElNotification.error(
            {
                title:'系统通知',
                message: '模板下载失败:' + error.toString(),
                duration: 6666,
            }
        );
    }
}



export async function doc_delete(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.doc_delete,
            data:params,
            responseType: 'json'
        }
    )


}

export async function doc_update(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.doc_update,
            data:params,
            responseType: 'json'
        }
    )


}


export async function doc_search(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.doc_list,
            data:params,
            responseType: 'json'
        }
    )
}

export async function doc_download(params:object){
    try {
        // 使用类型断言确保返回的是 Blob 类型
        const response = (await download_request({
            url: api.doc_download,
            data: params,
            responseType: 'blob'
        }));
        const blob: Blob = await response.data; // 确保返回的是 Blob 对象

        // 获取 Content-Disposition 头信息
        // @ts-ignore
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'downloaded-file'; // 默认文件名

        if (contentDisposition) {
            // 使用正则表达式提取文件名
            const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            const matches = filenameRegex.exec(contentDisposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
            }

            // 处理 UTF-8 编码的文件名
            const utf8FilenameRegex = /filename\*=UTF-8''(.*)/;
            const utf8Matches = utf8FilenameRegex.exec(contentDisposition);
            if (utf8Matches != null && utf8Matches[1]) {
                filename = decodeURIComponent(utf8Matches[1]);
            }
        }

        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        // 使用断言确保file_name存在
        link.setAttribute('download', filename);
        link.href = url;
        document.body.appendChild(link);
        link.click();

        // 清理
        window.URL.revokeObjectURL(url);
        link.remove(); // 移除创建的<a>标签
    } catch (error) {
        if (error.toString().includes('Request failed with status code 422')) {

            ElNotification.error(
                {
                    title:'系统通知',
                    message: '登录后即可下载！',
                    duration: 6666,
                }
            );
            return
        }
        ElNotification.error(
            {
                title:'系统通知',
                message: '文件下载失败:' + error.toString(),
                duration: 6666,
            }
        );
    }

}

export async function doc_content(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.doc_content,
            data:params,
            responseType: 'json'
        }
    )
}

export async function kg_ref_build(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.kg_ref_build,
            data:params,
            responseType: 'json'
        }
    )
}

export  async function kg_ref_get(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.kg_ref_get,
            data:params,
            responseType: 'json'
        }
    )
}

export async function update_kg_json_schema(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.kg_json_schema_update,
            data:params,
            responseType: 'json'
        }
    )
}

export async function doc_rebuild(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.doc_rebuild,
            data:params,
            responseType: 'json'
        }
    )
}

export async function add_kg_db_website(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.kg_db_website_add,
            data:params,
            responseType: 'json'
        }
    )
}

export async function doc_upload_before_check(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.doc_upload_before_check,
            data:params,
            responseType: 'json'
        }
    )
}

export async function doc_batch_switch(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.doc_batch_switch,
            data:params,
            responseType: 'json'
        }
    )
}

export async function doc_batch_rebuild(params:object):Promise<ServerResponse>{
    return request(
        {
            url:api.doc_batch_rebuild,
            data:params,
            responseType: 'json'
        }
    )
}
