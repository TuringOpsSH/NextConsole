import {ref} from "vue";
import {CurrentKgDocPageNum, CurrentKgDocPageSize,} from "@/components/kg/kg_process";
import {KGMeta} from "@/types/kg";
import {search_kg_docs} from "@/components/kg/doc_process";
import {user_info} from "@/components/user_center/user";

export const scrollbarHeight = ref(0)
export async function handleKgDocSizeChange  (val: number)   {
    CurrentKgDocPageSize.value = val
    await search_kg_docs()
}
export async function handleKgDocCurrentChange(val: number) {
    CurrentKgDocPageNum.value = val
    await search_kg_docs()
}
export function check_kg_permission(kg: KGMeta, permission :string="write"):boolean{

    // 前端检查用户对kg的权限
    // 知识库作者
    if (kg.kg_author_id == user_info.value?.user_id) {
        return true
    }
    // 公司管理员
    else if  (user_info.value.user_company == kg.kg_company &&
        (user_info.value.user_role.includes('admin') || user_info.value.user_role.includes('super_admin')  )) {
        return true
    }
    // NextConsole管理员
    else if ( user_info.value.user_role.includes('next_console_admin') ) {
        return true
    }
    // 公开知识库给公司所有人
    else if (kg.kg_public === 1 && kg.kg_company === user_info.value.user_company && permission === 'read') {
        return true
    }
    return false
}

export const isAdmin = ref(false)
