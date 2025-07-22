import {
    console_inner_type,
    console_input_height,
    console_input_Ref,
    show_console_inner_head
} from "@/components/next_console/messages_flow/console_input";
import {current_session} from "@/components/next_console/messages_flow/sessions";
import {
    attachment_add_resources_into_session,
    attachment_get_all_resource_formats,
    attachment_get_detail,
    attachment_remove_from_session,
    attachment_search_resources,
    attachment_search_resources_by_rag, attachment_search_share_resources,
    update_session
} from "@/api/next_console";
import {ResourceItem} from "@/types/resource_type";
import {nextTick, reactive, ref} from 'vue'
import {md_answer} from "@/components/next_console/messages_flow/message_flow";
import {ElMessage} from "element-plus";

interface search_type{
    search_type:string,
    search_type_name:string,
    search_type_active:boolean,
}
export const search_resource_loading = ref(false)
export const session_resources_list = ref<ResourceItem[]>([])
export const resource_search_dialog_Ref = ref(null)
export const resource_search_dialog_show = ref(false)
export const resource_search_result = ref<ResourceItem[]>([])
export const resource_search_types = ref<search_type[]>([
    {
        search_type:'all',
        search_type_name:"全部",
        search_type_active:true,
    },
    {
        search_type:'file',
        search_type_name:"文件",
        search_type_active:false,
    },
    {
        search_type:'folder',
        search_type_name:"文件夹",
        search_type_active:false,
    },
    {
        search_type:'share',
        search_type_name:"共享",
        search_type_active:false,
    },
])
export const resource_search_model = ref('recently')
export const resource_search_table_Ref = ref(null)
export const resource_recent_table_Ref = ref(null)
export const search_keyword = ref( '')
export const resource_search_form_Ref=ref(null)
export const current_resource_types = ref([
    '文档', '图片', '网页', '代码', '文件夹'
])
export const all_resource_formats = ref([])
export const current_resource_formats = ref([])
export const resource_search_rag = ref(false)
export const current_page_num = ref(1)
export const current_page_size = ref(50)
export const current_total = ref(0)
export const el_scrollbar_Ref = ref(null)
export const search_resource_list_scroll_Ref = ref(null)
export async function switch_on_resource_search(){
    // 打开文档问答配置区域
    show_console_inner_head.value = true
    console_inner_type.value = 'ai_resource'
    current_session.session_local_resource_switch = true
    // 获取对应文件资源明细
    if (current_session.session_local_resource_use_all){

        session_resources_list.value = [
            //@ts-ignore
            {
                resource_id: -1,
                resource_icon: 'all_resource.svg',
                resource_name: '全部资源'
            } as ResourceItem
        ]
        return
    }


    if (session_resources_list.value?.length > 0){
        if (!current_session?.id){
            return
        }
        // 更新至后端
        update_session({
            session_id: current_session.id,
            session_local_resource_switch: true
        })
        let params = {
            session_id: current_session.id,
            attachment_source: "resources"
        }
        let res = await attachment_get_detail(params)
        if (!res.error_status){
            session_resources_list.value = res.result
        }
    }
    else {
        turn_on_resource_search_dialog()
    }


}
export async function hide_ai_resource_config_area(){
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

    if (!session_resources_list.value.length){
        current_session.session_local_resource_switch = false
        if (!current_session?.id){
            return
        }
        update_session({
            session_id: current_session.id,
            session_local_resource_switch: false
        })
    }
}
export async function switch_off_resource_search(){
    current_session.session_local_resource_switch = false
    hide_ai_resource_config_area()
    if (!current_session?.id){
        return
    }
    update_session({
        session_id: current_session.id,
        session_local_resource_switch: false
    })
}
export async function turn_on_resource_search_dialog(){
    resource_search_dialog_show.value = true
    change_recent_search_type(
      {
          search_type:'all',
          search_type_name:"全部",
          search_type_active:true,
      }
    )
}
export async function remove_resource_item(resource:ResourceItem){
    // 删除资源
    const indexToRemove = session_resources_list.value.findIndex(item => item.id === resource.id)
    if (indexToRemove !== -1){
        session_resources_list.value.splice(indexToRemove, 1);
    }
    if (!current_session?.id){
        return
    }
    // 同步到后端
    attachment_remove_from_session({
        session_id: current_session.id,
        resource_list : [
            resource.id
        ]
    })
}
export async function clean_resource_list(){
    session_resources_list.value = [
        //@ts-ignore
        {
            resource_id: -1,
            resource_icon: 'all_resource.svg',
            resource_name: '全部资源'
        } as ResourceItem
    ]
    current_session.session_local_resource_switch = true
    current_session.session_local_resource_use_all=true
    if (!current_session?.id){
        return
    }
    // 同步到后端
    attachment_remove_from_session({
        session_id: current_session.id,
        clean_all: true,
        attachment_source: "resources"
    })

    update_session({
        session_id: current_session.id,
        session_local_resource_switch: true,
        session_local_resource_use_all: true,
    })
}
export async function commit_add_choose_resources(){
    let choose_resources = []
    if (resource_search_model.value == 'recently'){
        choose_resources = resource_recent_table_Ref.value?.getSelectionRows()
    }
    else if (resource_search_model.value == 'search'){
        choose_resources = resource_search_table_Ref.value?.getSelectionRows()
    }
    if (!choose_resources.length){
        ElMessage.info('请选择资源')
        return
    }
    resource_search_dialog_show.value = false
    session_resources_list.value = choose_resources
    current_session.session_local_resource_switch = true
    current_session.session_local_resource_use_all = false
    if (!current_session?.id){
        return
    }

    update_session({
        session_id: current_session.id,
        session_local_resource_switch: true,
        session_local_resource_use_all: false

    })
    let params = {
        session_id: current_session.id,
        resource_list : [],

    }
    if (!current_session.session_local_resource_use_all && choose_resources){
        for (let resource of choose_resources){
            params.resource_list.push(resource.id)
        }
        await attachment_add_resources_into_session(params)
    }
    switch_on_resource_search()

}
export async function cancel_add_choose_resources(){
    resource_search_dialog_show.value = false
    resource_search_table_Ref.value?.clearSelection()
}
export async function change_recent_search_type(search_type:search_type){
    for (let sub_type of resource_search_types.value){
        if (search_type.search_type == sub_type.search_type){
            sub_type.search_type_active = true
        }else {
            sub_type.search_type_active = false
        }

    }
    resource_search_model.value = 'recently'
    let params = {
        search_type: search_type.search_type,
        search_recently: true,
    }
    // 获取最近会话资源
    let res = await attachment_search_resources(params)
    if (!res.error_status){
        resource_search_result.value = res.result
    }


}
export function click_row(row, column, event){
    // 切换该行的选中状态
    resource_search_table_Ref.value?.toggleRowSelection(row)
}
export async function search_resource_keyword(){
    // 根据关键词从资源库中搜索资源
    if (!search_keyword.value){
        ElMessage.info('请输入关键词')
        return
    }

    resource_search_model.value='search'
    search_resource_loading.value = true
    let current_search_type = 'all'
    for (let search_type of resource_search_types.value){
        if (search_type.search_type_active){
            current_search_type = search_type.search_type
            break
        }
    }

    let params = {
        search_type: current_search_type,
        search_recently: false,
        resource_keyword: search_keyword.value,
        resource_type: current_resource_types.value,
        resource_format: [],
        rag_enhance: resource_search_rag.value,
    }
    for (let format of current_resource_formats.value) {
        params.resource_format.push(format)
    }

    let res = await attachment_search_resources(params)
    if (!res.error_status) {
        resource_search_result.value = []
        current_total.value = res.result.total
        for (let item of res.result.data){
            let author_info = null
            for (let user of res.result.author_info){
                if (user.user_id == item.user_id){
                    author_info = user
                    break
                }

            }
            item.author_info = author_info
            resource_search_result.value.push(item)
        }


    }

    search_resource_loading.value = false
}
export async function search_resource_keyword_next(scroll_position:object){

    if (search_resource_loading.value){
        console.log('资源正在加载中')
        return
    }
    if (current_total.value && current_total.value <= resource_search_result.value.length){
        console.log('资源已全部加载')
        return
    }
    if (((current_page_num.value - 1) * current_page_size.value) >= current_total.value){
        console.log('超过，资源已全部加载',
          current_page_num.value,
          current_page_size.value,
          current_total.value)
        return
    }
    // @ts-ignore
    if (Math.floor(scroll_position.scrollTop + 600) > search_resource_list_scroll_Ref.value.clientHeight - 10){
        // 下一页
        current_page_num.value += 1
        // 根据关键词从资源库中搜索资源
        if (!search_keyword.value){
            ElMessage.info('请输入关键词')
            return
        }
        resource_search_model.value='search'
        search_resource_loading.value = true
        let current_search_type = 'all'
        for (let search_type of resource_search_types.value){
            if (search_type.search_type_active){
                current_search_type = search_type.search_type
                break
            }
        }
        let params = {
            search_type: current_search_type,
            search_recently: false,
            resource_keyword: search_keyword.value,
            resource_type: current_resource_types.value,
            resource_format: [],
            rag_enhance: resource_search_rag.value,
            page_num: current_page_num.value,
            page_size: current_page_size.value
        }
        for (let format of current_resource_formats.value) {
            params.resource_format.push(format)
        }
        let res = await attachment_search_resources(params)
        if (!res.error_status){
            current_total.value = res.result.total
            for (let resource of res.result.data){
                // 去重添加
                let find_flag = false
                for (let item of resource_search_result.value){
                    if (item.id == resource.id){
                        find_flag = true
                        break
                    }
                }
                if (find_flag){
                    continue
                }
                let author_info = null
                for (let user of res.result.author_info){
                    if (user.user_id == resource.user_id){
                        author_info = user
                        break
                    }

                }
                resource.author_info = author_info
                resource_search_result.value.push(resource)
            }

        }
        // 往上滚动防止连续加载
        // @ts-ignore
        el_scrollbar_Ref.value.setScrollTop(scroll_position.scrollTop - 10)
        search_resource_loading.value = false

    }
}


export async function init_all_format_options(){
    let res = await attachment_get_all_resource_formats({})
    if (!res.error_status){
        all_resource_formats.value = res.result
    }
}
export async function change_search_type(search_type:search_type){
    for (let sub_type of resource_search_types.value){
        if (search_type.search_type == sub_type.search_type){
            sub_type.search_type_active = true
        }else {
            sub_type.search_type_active = false
        }

    }
    resource_search_model.value = 'search'
    search_resource_keyword()
}
export function getHighlightedText(text:string){
    if (!search_keyword.value || !text) {
        return text;
    }
    const regex = new RegExp(`(${search_keyword.value})`, 'gi');
    return text.replace(regex, '<span class="highlight-resource-keyword">$1</span>');
}
export function getMarkdownHtml(text:string){
    return md_answer.render(text)
}
