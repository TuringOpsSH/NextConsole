import { ref } from 'vue';
import { search_resource_object } from '@/api/resource-api';
import {useResourceInfoStore} from "@/stores/resource-info-store";

interface ITree {
  label: string;
  children?: ITree[];
  leaf?: boolean;
  disabled?: boolean;
  resource_type?: string;
  resource_icon?: string;
  resource_id?: number;
  resource_parent_id?: number;
  resource_source?: string;
}

export const currentCallback = ref(null);

// 选择上传文件夹
export const showUploadResourceTree = ref(false);

export const resourceUploadTreeData = ref<ITree[]>([]);

export async function showUploadDialogMultiple(callback?: () => Promise<any>) {
  showUploadResourceTree.value = true;
  // 获取第一层目录
  const res = await search_resource_object({});
  if (!res.error_status) {
    resourceUploadTreeData.value = [
      {
        label: res.result.root.resource_name,
        leaf: false,
        disabled: false,
        resource_id: res.result.root.id,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: res.result.root.resource_parent_id,
        resource_source: 'my',
        children: []
      },
      {
        label: '共享资源',
        leaf: false,
        disabled: false,
        resource_id: null,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: null,
        resource_source: 'share',
        children: []
      }
    ];

    // 先添加目录
    // for (let item of res.result.data){
    //     if (item.resource_type == 'folder'){
    //         resourceUploadTreeData.value[0].children.push({
    //             label: item.resource_name,
    //             leaf: false,
    //             disabled: false,
    //             resource_id: item.id,
    //             resource_type: item.resource_type,
    //             resource_icon: item.resource_icon,
    //             resource_parent_id : item.resource_parent_id
    //         })
    //     }
    //
    // }
    // for (let item of res.result.data){
    //     if (item.resource_type != 'folder'){
    //         resourceUploadTreeData.value[0].children.push({
    //             label: item.resource_name,
    //             leaf: true,
    //             disabled: true,
    //             resource_id: item.id,
    //             resource_type: item.resource_type,
    //             resource_icon: item.resource_icon,
    //             resource_parent_id : item.resource_parent_id
    //         })
    //     }
    // }
  }
  currentCallback.value = callback;
    const resourceInfoStore = useResourceInfoStore();
    console.log(resourceInfoStore.uploadFileList);
}
