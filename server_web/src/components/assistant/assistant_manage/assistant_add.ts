import {
    assistant_avatar_upload_data,
    assistant_choose,
    show_test_console_flag,
    upload_avatar
} from "@/components/assistant/assistant_manage/assistant_manage";
import {ElMessage, ElNotification} from "element-plus";
import {assistant_add, assistant_get, assistant_update} from "@/api/assistant_center";
import router from "@/router";


export function reset_new_assistant(notice = true) {
    assistant_choose.assistant_publish_shop_id = null;
    assistant_choose.comments = undefined;
    assistant_choose.assistant_author_avatar = "";
    assistant_choose.assistant_author_id = "";
    assistant_choose.assistant_author_name = "";
    assistant_choose.id = null;
    assistant_choose.assistant_name = '';
    assistant_choose.assistant_desc = '';
    assistant_choose.assistant_status = '创建';
    assistant_choose.assistant_tags = [];
    assistant_choose.assistant_role_prompt = '';
    assistant_choose.assistant_avatar = 'images/logo.svg';
    assistant_choose.assistant_avatar_url = '';
    assistant_choose.assistant_language = '中文';
    assistant_choose.assistant_voice= '';
    assistant_choose.assistant_memory_size= 4;
    assistant_choose.assistant_model_name= 'deepseek-chat';
    assistant_choose.assistant_model_type= 'chat';
    assistant_choose.assistant_model_temperature= 1;
    assistant_choose.assistant_model_icon= 'images/deep_seek_logo.png';
    assistant_choose.create_time= '';
    assistant_choose.update_time= '';
    assistant_choose.assistant_knowledge_base= [];
    assistant_choose.assistant_function_lists= [];
    assistant_choose.assistant_source= 1;
    assistant_choose.authority_create_time= "";
    assistant_choose.authority_value= 0;
    assistant_choose.assistant_is_start= false;
    assistant_choose.call_cnt= 0;
    assistant_choose.is_shop_assistant= false;
    assistant_choose.rag_factor= 0.75;
    assistant_choose.rag_miss= 1;
    assistant_choose.rag_miss_answer= "";
    assistant_choose.rag_relevant_threshold= 0.25;
    if (notice) {
        ElNotification.success({
            title: "系统消息",
            message: '重置成功' ,
            duration: 3000
        })
    }
}

export async function add_new_assistant() {
    // 检测参数
    if (assistant_choose.id) {
        ElMessage.success({
            message: '已经创建成功!',
            type: 'warning',
            duration: 600
        })
        return
    }
    if (!assistant_choose.assistant_name) {
        ElMessage.warning({
            message: '请填写助手名称！',
            type: 'warning',
            duration: 600
        })
        return
    }
    if (assistant_choose.assistant_name.length > 200) {
        ElMessage.warning({
            message: '助手名称过长！请不要超过200个字符',
            type: 'warning',
            duration: 600
        })
        return
    }
    if (assistant_choose.assistant_desc.length > 4096) {
        ElMessage.warning({
            message: '助手描述过长！请不要超过4096个字符',
            type: 'warning',
            duration: 600
        })
        return
    }


    // 创建助手
    let res = await assistant_add(assistant_choose)
    if (!res.error_status) {
        // 上传头像
        assistant_choose.id = res.result.id
        assistant_avatar_upload_data.value.assistant_id = res.result.id
        await upload_avatar.value!.submit()
        let new_res = await assistant_get({
            "id": assistant_choose.id
        })
        if (!new_res.error_status) {
            Object.assign(assistant_choose, new_res.result);
            ElMessage.success({
                message: '创建成功!',
                type: 'success',
                duration: 1200
            })
            // 刷新列表
            show_test_console_flag.value = true
            await router.push({
                query: {
                    ...router.currentRoute.value.query, // 保持既有参数
                    assistant: res.result.id
                }
            })
        }


    }
}

export async function save_new_assistant() {
    if (assistant_choose.id === null) {
        await add_new_assistant()
        show_test_console_flag.value = true

        return
    }
    else {
        let res1 = await assistant_update(assistant_choose)
        await upload_avatar.value!.submit()
        if (!res1.error_status) {
            ElMessage.success({
                message: '保存成功!',
                type: 'success',
                duration: 600
            })
            let new_res = await assistant_get({
                "id": assistant_choose.id
            })
            Object.assign(assistant_choose, new_res.result);
            show_test_console_flag.value = true
            await router.push({
                query: {

                    assistant: assistant_choose.id
                }
            })
        }

    }
}
