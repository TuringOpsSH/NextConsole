import {current_session} from "@/components/next-console/messages-flow/sessions";
import {nextTick, reactive, ref} from 'vue'
import {
    console_inner_type,
    console_input_height,
    console_input_Ref,
    show_console_inner_head
} from "@/components/next-console/messages-flow/console_input";
import {
    attachment_add_webpage_tasks,
    attachment_base_init,
    attachment_get_detail,
    attachment_remove_from_session,
    update_session
} from "@/api/next-console";
import {ResourceItem} from "@/types/resource-type";
import {ElMessage} from "element-plus";

export const upload_webpage_resource_list = ref<ResourceItem[]>([])
export const upload_webpage_dialog_Ref = ref(null)
export const upload_webpage_dialog_visible = ref(false)
export const upload_webpage_new_resources = reactive<{ new_urls:ResourceItem[]}>({new_urls:[
        {
            id: null,
            resource_name: '',
            resource_title: '',
            resource_icon: 'html.svg',
            ref_status: null,
            resource_source_url: '',
        } as ResourceItem]
})
export const upload_webpage_new_resource_formRef = ref(null)


export async function switch_on_webpage_search(){
    // 打开网页问答配置区域
    show_console_inner_head.value = true
    console_inner_type.value = 'ai_webpage'
    current_session.session_attachment_webpage_switch = true
    if (!upload_webpage_resource_list.value.length){
        // 打开网页问答地址输入区域
        upload_webpage_dialog_visible.value = true
    }
    if (!current_session?.id){
        return
    }
    // 更新至后端
    update_session({
        session_id: current_session.id,
        session_attachment_webpage_switch: true
    })
    // 获取对应文件资源明细
    if (upload_webpage_resource_list.value.length > 0){
        let params = {
            session_id: current_session.id,
            attachment_source: 'webpage'
        }

        let res = await attachment_get_detail(params)
        if (!res.error_status){
            upload_webpage_resource_list.value = res.result

            // 标记是否支持
            for (let resource of upload_webpage_resource_list.value){
                resource.resource_is_supported = check_webpage_support_status(resource)
            }

        }
    }
}
export function check_webpage_support_status(resource: ResourceItem): boolean{
    // 检查是否支持
    // console.log('判断支持',resource)
    if (resource.resource_status == '异常' || resource?.ref_status == 'Error' || resource?.ref_status == 'Failure'){
        return false
    }
    if (resource?.ref_status == 'Success'){
        return true
    }
    return null
}

export async function switch_off_webpage_search(){
    current_session.session_attachment_webpage_switch = false
    hide_ai_webpage_config_area()
    if (!current_session?.id){
        return
    }
    update_session({
        session_id: current_session.id,
        session_attachment_webpage_switch: false
    })
}
export async function hide_ai_webpage_config_area(){
    show_console_inner_head.value = false
    await nextTick(
      () => {
          if (window.innerWidth >= 768){
              console_input_Ref.value.focus()
          }
          // 更新高度
          console_input_height.value = Math.max(130, console_input_Ref.value.clientHeight + 70)

      }
    )

    if (!upload_webpage_resource_list.value.length){
        current_session.session_attachment_webpage_switch = false
        if (!current_session?.id){
            return
        }
        update_session({
            session_id: current_session.id,
            session_attachment_webpage_switch: false
        })
    }

}
export async function clean_tmp_webpage_list(){
    upload_webpage_resource_list.value = []
    if (!current_session?.id){
        return
    }
    // 同步到后端
    attachment_remove_from_session({
        session_id: current_session.id,
        clean_all: true,
        attachment_source: "webpage"
    })
}
export async function remove_webpage_item(index:number){
    // 删除网页
    const resource_id = upload_webpage_resource_list.value[index].id

    upload_webpage_resource_list.value.splice(index, 1)
    if (!current_session?.id){
        return
    }
    // 同步到后端
    attachment_remove_from_session({
        session_id: current_session.id,
        resource_list : [
            resource_id
        ]
    })
}
export async function add_new_webpage_resource(){
    // 添加新的网页资源
    upload_webpage_new_resources.new_urls.push({
        id: null,
        resource_name: '',
        resource_title: '',
        resource_icon: 'html.svg',
        ref_status: null,
        resource_source_url: '',
    } as ResourceItem)
}
export async function remove_new_webpage_resource(index:number){
    // 删除新的网页资源
    if (upload_webpage_new_resources.new_urls?.length == 1){
        upload_webpage_new_resources.new_urls[0].resource_source_url = ""
        ElMessage.warning('没办法再删了哦！')
        return
    }
    upload_webpage_new_resources.new_urls.splice(index, 1)
}
export async function switch_off_new_webpage(){
    // 关闭新的网页资源输入框
    upload_webpage_dialog_visible.value = false
    // 去除非法数据
    for (let i = 0; i < upload_webpage_new_resources.new_urls.length; i++){
        if (!upload_webpage_new_resources.new_urls[i].resource_source_url){
            upload_webpage_new_resources.new_urls.splice(i, 1)
            i--
        }
    }

    if(!upload_webpage_new_resources.new_urls.length){
        upload_webpage_new_resources.new_urls.push({
            id: null,
            resource_title: '',
            ref_status: null,
            resource_source_url: '',
        } as ResourceItem)

    }
    if (!current_session?.id){
        return
    }
}
export async function commit_add_new_webpages(){
    // 先对新的网页资源进行校验
    let valid_res = await upload_webpage_new_resource_formRef.value?.validate()
    if (upload_webpage_new_resource_formRef.value?.validate && !valid_res){
        return
    }
    upload_webpage_dialog_visible.value = false
    let all_urls = []
    for (let i of upload_webpage_resource_list.value){
        if (i.resource_source_url && !i.id){
            all_urls.push(i.resource_source_url)
        }
    }
    for (let i of upload_webpage_new_resources.new_urls){
        if (!i.resource_source_url){
            continue
        }
        i.resource_name = i.resource_source_url
        if (all_urls.includes(i.resource_source_url)){
            continue
        }
        upload_webpage_resource_list.value.push(i)
        all_urls.push(i.resource_source_url)
    }
    // 更新至后端
    if (!current_session?.id){
        return
    }
    update_session({
        session_id: current_session.id,
        session_attachment_webpage_switch: true
    })
    let init_res = await attachment_base_init({
        session_id: current_session.id
    })
    if (init_res.error_status) {
        return false
    }
    let resource_parent_id = init_res.result.id

    let res =await attachment_add_webpage_tasks({
        session_id: current_session.id,
        qa_id: '',
        msg_id:'',
        resource_parent_id : resource_parent_id,
        urls: all_urls
    })
    if (!res.error_status){
        // 更新资源信息
        for (let i of res.result){
            for (let j of upload_webpage_resource_list.value){
                if (i.resource_source_url == j.resource_source_url){
                    j.id = i.id
                    break
                }
                j.resource_is_supported = check_webpage_support_status( j )
            }
        }
    }
    // 重置新的网页资源
    upload_webpage_new_resources.new_urls = [{
        id: null,
        resource_name: '',
        resource_title: '',
        resource_icon: 'html.svg',
        ref_status: null,
        resource_source_url: '',
    } as ResourceItem]


}
export function validate_url_repeat(rule: any, value: any, callback: any){
    // 验证网页地址是否与已有数据重复

    let repeat = 0
    for (let i of upload_webpage_new_resources.new_urls){
        if (i.resource_source_url == value && value){
            repeat ++
        }
    }
    if (repeat > 1){
        callback(new Error('不能重复添加相同的网页地址'))
    }
    repeat = 0
    // console.log(upload_webpage_resource_list.value, value)
    for (let i of upload_webpage_resource_list.value){
        if (i.resource_source_url == value && value) {
            repeat ++
        }
    }
    if (repeat > 1){
        callback(new Error('会话中已经有相同的网页地址了哦！'))
    }
    else{
        callback()
    }
}
export function get_resource_icon(resource: ResourceItem){
    // 获取资源图标
    // // console.log(resource.resource_icon)
    if (resource.resource_icon){
        if (resource.resource_icon.includes('http') || resource.resource_icon.includes('data:image')
          || resource.resource_icon.includes('/images/')
        ){
            return resource.resource_icon
        }
        return "/images/" +resource.resource_icon
    }
    else{
        return '/images/html.svg'
    }

}
