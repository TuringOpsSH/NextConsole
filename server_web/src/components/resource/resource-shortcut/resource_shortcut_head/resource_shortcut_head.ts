import { ref } from 'vue';
import { IResourceTag } from '@/types/resource-type';

export const showConfigFlag = ref(true);
export const resource_types_name_map = {
  文档: 'document',
  图片: 'image',
  网页: 'webpage',
  代码: 'code',
  文件夹: 'folder',
  视频: 'video',
  音频: 'audio',
  程序: 'binary',
  其他: 'other',
  压缩包: 'archive',
  文本: 'text'
};
export const current_resource_types = ref([
  'document',
  'image',
  'webpage',
  'code',
  'folder',
  'video',
  'audio',
  'binary',
  'archive',
  'text',
  'other'
]);
export const current_resource_tags = ref<IResourceTag[]>([]);

// 过滤区域
export function show_search_config_area(targetStatus: boolean = null) {
  if (targetStatus === null || typeof targetStatus != 'boolean') {
    showConfigFlag.value = !showConfigFlag.value;
  } else {
    showConfigFlag.value = targetStatus;
  }
  console.log(showConfigFlag.value);
}
