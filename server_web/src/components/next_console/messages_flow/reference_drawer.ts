import {ref} from 'vue';
import {reference_item} from "@/types/next_console";
import * as string_decoder from "node:string_decoder";
import {search_reference} from "@/api/next_console";
import router from "@/router";
export const show_reference_drawer = ref(false)
export const reference_drawer_data = ref<reference_item[]>([])
export function show_reference_drawer_fn(data: reference_item[] | null) {
    reference_drawer_data.value = data
    show_reference_drawer.value = true

}

export function open_reference(data:reference_item | null) {
    if (data.source_type == 'webpage'){
        // 新标签页打开
        window.open(data.resource_source_url as string)
    }
    else {
        // 跳转资源预览页面
        const route = router.resolve({
            name: 'resource_viewer',
            params: {
                resource_id: data.resource_id,
            },
        });
        window.open(route.href, '_blank');
    }
}

export async function retry_get_icon(data:reference_item){
    // // console.log(data)
    if (!data.resource_icon){
        return
    }
    try{
        const response = await fetch(
            data.resource_icon,{
                method: 'GET',
                headers: {
                    'User-Agent': 'Mozilla/5.0', // 模拟常见浏览器的User-Agent
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                },
            }
        );
        // // console.log(response)
        const blob = await response.blob();
        const reader = new FileReader();

        reader.onloadend = () => {
            // 使用类型断言，告诉 TypeScript 这个元素是 HTMLImageElement 类型
            const imgElement = document.getElementById(data.resource_icon) as HTMLImageElement;
            // 将图片数据作为Base64字符串设置为img的src
            if (imgElement) {
                imgElement.src = reader.result as string;
            }
        };

        reader.readAsDataURL(blob);
    } catch (e) {
        
    }
}
