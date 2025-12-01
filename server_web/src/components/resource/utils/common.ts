import { ElMessage } from 'element-plus';
import { download_resource_object } from '@/api/resource-api';
import { IResourceItem } from '@/types/resource-type';
export function formatResourceSize(sizeNum: number | null) {
  // 格式化文件大小,保留两位小数,输入为mb单位的数字
  // // console.log(size_num)
  if (sizeNum === null) {
    return '';
  }
  let size = sizeNum;
  let sizeStr = '';

  // kb单位
  if (size < 1) {
    size = size * 1024;
    sizeStr = size.toFixed(2) + 'KB';
  } else if (size < 1024) {
    sizeStr = size.toFixed(2) + 'MB';
  } else if (size < 1024 * 1024) {
    size = size / 1024;
    sizeStr = size.toFixed(2) + 'GB';
  } else if (size < 1024 * 1024 * 1024) {
    size = size / 1024 / 1024;
    sizeStr = size.toFixed(2) + 'TB';
  } else if (size < 1024 * 1024 * 1024 * 1024) {
    size = size / 1024 / 1024 / 1024;
    sizeStr = size.toFixed(2) + 'PB';
  } else {
    size = size / 1024 / 1024 / 1024 / 1024;
    sizeStr = size.toFixed(2) + 'EB';
  }

  return sizeStr;
}

export function getResourceIcon(resource: IResourceItem) {
  // 获取资源图标
  if (resource.resource_icon) {
    if (
      resource.resource_icon.includes('http') ||
      resource.resource_icon.includes('data:image') ||
      resource.resource_icon.includes('/images/')
    ) {
      return resource.resource_icon;
    }
    return '/images/' + resource.resource_icon;
  } else {
    return '/images/' + 'html.svg';
  }
}

export function getInitResource() {
  return <IResourceItem>{
    id: null,
    resource_parent_id: null,
    user_id: null,
    resource_name: null,
    resource_type: null,
    resource_desc: null,
    resource_icon: null,
    resource_format: null,
    resource_path: null,
    resource_size_in_MB: null,
    resource_status: null,
    ref_status: null,
    create_time: null,
    update_time: null,
    delete_time: null,
    show_buttons: null,
    resource_parent_name: null,
    resource_is_selected: null,
    sub_resource_dir_cnt: null,
    sub_resource_file_cnt: null,
    sub_rag_file_cnt: 0
  };
}

export async function downloadResource(resource: IResourceItem) {
  // 下载资源
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除，请恢复后下载!');
    return;
  }
  if (resource.resource_type == 'folder') {
    ElMessage.warning('文件夹无法下载!');
    return;
  }
  const params = {
    resource_id: resource.id
  };
  const res = await download_resource_object(params);
  if (!res.error_status) {
    let downloadUrl = res.result?.download_url;
    if (!downloadUrl) {
      ElMessage.error('下载链接为空');
      return;
    }
      downloadUrl = downloadUrl + '?filename=' + encodeURIComponent(resource.resource_name);
    // 创建一个隐藏的 <a> 标签
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = resource.resource_name; // 设置下载文件的名称
    link.style.display = 'none';

    // 将 <a> 标签添加到文档中
    document.body.appendChild(link);

    // 触发点击事件
    link.click();

    // 移除 <a> 标签
    document.body.removeChild(link);
  }
}
