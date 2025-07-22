import { ref } from 'vue'
export const panel_width = ref(window.innerWidth < 768 ? window.innerWidth - 60 + 'px' :'400px')
export function switch_panel(){
    if (window.innerWidth < 768){
        if (panel_width.value === '0px'){
            panel_width.value = window.innerWidth - 60 + 'px'
        } else {
            panel_width.value = '0px'
        }
        return
    }
    panel_width.value = panel_width.value === '400px' ? '0px' : '400px'
}
import {Company} from '@/types/contacts'
import {get_company_info, get_friend_request_cnt} from "@/api/contacts";
import router from "@/router";
import {init_current_friend_list} from "@/components/contacts/friends/friends";
import {init_company_structure_tree} from "@/components/contacts/company_structure/company_structure";
export const current_friend_request_cnt = ref(0)
// @ts-ignore
export const current_company = ref<Company>({})
export async function init_current_company (){
    let res = await get_company_info({})
    if (!res.error_status){
        current_company.value = res.result
    }
}
export async function router_to_company_structure(){
    router.push({name: 'company_structure',  })
    if (window.innerWidth < 768){
        panel_width.value = '0px'
    }

}
export async function router_to_friends(){
    router.push({name: 'friends',  })
    if (window.innerWidth < 768){
        panel_width.value = '0px'
    }

}
export async function router_to_groups_chat(){
    router.push({name: 'groups_chat',  })
}

export async function init_friend_request_cnt(){
    let res = await get_friend_request_cnt({})
    if (!res.error_status){
        current_friend_request_cnt.value = res.result
    }
}
