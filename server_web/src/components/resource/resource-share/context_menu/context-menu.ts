import {reactive, ref} from 'vue';
import {download_resource_object} from '@/api/resource-api';
import {IResourceItem, ResourceItem} from '@/types/resource-type';
import {ElMessage} from 'element-plus';
import router from '@/router';

export const current_row_item = reactive<ResourceItem>(
  // @ts-ignore
  {
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
    sub_rag_file_cnt: null
  }
);

////// 更新版本///////////
export const resource_share_context_menu_flag = ref(false);
export const mousePosition = ref({ x: 0, y: 0 });
export function openContextMenu(event) {
  // 重置当前行项目的 ID
  current_row_item.id = -1;
  init_context_position(event, 140);
}
export function openTableContextMenu(row, column, event) {
  for (const key in row) {
    current_row_item[key] = row[key];
  }
  init_context_position(event, 270);
  event.preventDefault();
  event.stopPropagation();
}
export function openCardContextMenu(row, event) {
  init_context_position(event);
  Object.assign(current_row_item, row);
  event.preventDefault();
  event.stopPropagation();
}

function init_context_position(event, menuHeight = 200) {
  // 打开菜单并设置位置
  resource_share_context_menu_flag.value = true;
  // 获取鼠标当前位置
  let mouseX = event.clientX;
  let mouseY = event.clientY;

  // 如果鼠标位置未定义，使用默认值（居中）
  if (!mouseX && !mouseY) {
    mouseX = window.innerWidth * 0.5;
    mouseY = window.innerHeight * 0.5;
  }
  // 判断鼠标距离屏幕下沿的距离
  if (window.innerHeight - mouseY < menuHeight) {
    // 如果太近，将菜单显示在上方
    mouseY -= menuHeight;
  }
  mousePosition.value = {
    x: mouseX,
    y: mouseY
  };
}



export async function preview_share_resource() {
  // 预览资源
  if (current_row_item.resource_status == '删除') {
    ElMessage.warning('资源已删除，请恢复后查看!');
    return;
  }
  if (!current_row_item?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (current_row_item.resource_type == 'folder') {
    router.push({
      name: 'resourceShare',
      params: {
        resource_id: current_row_item.id
      }
    });
    return;
  }
  await router.push({
    name: 'resource_viewer',
    params: {
      resource_id: current_row_item.id
    }
  });
}
export async function download_resource() {
  // 下载资源
  if (!current_row_item?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (current_row_item.resource_status == '删除') {
    ElMessage.warning('资源已删除，请恢复后下载!');
    return;
  }
  if (current_row_item.resource_type == 'folder') {
    ElMessage.warning('文件夹无法下载!');
    return;
  }
  let params = {
    resource_id: current_row_item.id
  };
  let res = await download_resource_object(params);
  if (!res.error_status) {
    let download_url = res.result?.download_url;
    if (!download_url) {
      ElMessage.error('下载链接为空');
      return;
    }
    download_url = download_url + '?filename=' + encodeURIComponent(current_row_item.resource_name);
    // 创建一个隐藏的 <a> 标签
    const link = document.createElement('a');
    link.href = download_url;
    link.download = current_row_item.resource_name; // 设置下载文件的名称
    link.style.display = 'none';
    // 将 <a> 标签添加到文档中
    document.body.appendChild(link);
    // 触发点击事件
    link.click();
    // 移除 <a> 标签
    document.body.removeChild(link);
  }
}

export async function setCurrentRowItem(item: IResourceItem) {
  Object.assign(current_row_item, item);
}
