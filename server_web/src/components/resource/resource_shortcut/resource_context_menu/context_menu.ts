import { ElMessage, genFileId, UploadRawFile } from 'element-plus';
import { reactive, ref } from 'vue';
import { build_resource_object_ref, delete_resource_object_api, download_resource_object } from '@/api/resource-api';
import { check_resource_rag_support } from '@/components/resource/resource_main';
import {
  choose_resource_meta,
  show_meta_flag,
  turn_on_resource_meta
} from '@/components/resource/resource_meta/resource_meta';
import { turn_on_share_selector } from '@/components/resource/resource_share_selector/resource_share_selector';
import {
  current_resource_list,
  resource_shortcut_Ref,
  search_resource_by_tags,
  show_multiple_button
} from '@/components/resource/resource_shortcut/resource_shortcut';
import { show_move_dialog_multiple } from '@/components/resource/resource_tree/resource_tree';
import {
  show_upload_manage_box,
  upload_button_Ref,
  upload_file_list,
  upload_parent_resource
} from '@/components/resource/resource_upload/resource_upload';
import router from '@/router';
import { useUserInfoStore } from '@/stores/userInfoStore';
import { ResourceItem } from '@/types/resource-type';
export const mousePosition = ref({ x: 0, y: 0 });
export const resource_shortcut_context_menu_flag = ref(false);
//@ts-ignore
export const current_row_item = reactive<ResourceItem>({
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
  rag_status: null,
  create_time: null,
  update_time: null,
  delete_time: null,
  show_buttons: null,
  resource_parent_name: null,
  resource_is_selected: null,
  sub_resource_dir_cnt: null,
  sub_resource_file_cnt: null,
  sub_rag_file_cnt: null
});
export const upload_file_Ref = ref(null);
export function openContextMenu(event) {
  // 打开菜单并设置位置

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
  resource_shortcut_context_menu_flag.value = true;
  // 获取鼠标当前位置
  let mouseX = event.clientX;
  let mouseY = event.clientY;

  // 如果鼠标位置未定义，使用默认值（居中）
  if (!mouseX && !mouseY) {
    mouseX = window.innerWidth * 0.5;
    mouseY = window.innerHeight * 0.5;
  }
  // // console.log(window.innerHeight, mouseY, menuHeight)
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

export async function preview_resource() {
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
      name: 'resource_list',
      params: {
        resource_id: current_row_item.id
      }
    });
    return;
  }
  // 使用 router.resolve 构造 URL
  // if (current_row_item.resource_type == 'document'){
  //     const route = router.resolve({
  //         name: 'resource_viewer',
  //         params: { resource_id: current_row_item.id }
  //     }).href
  //     // 打开新页面
  //     window.open(route, '_blank')
  //     return
  // }
  await router.push({
    name: 'resource_viewer',
    params: {
      resource_id: current_row_item.id
    }
  });
}

export async function show_resource_detail() {
  if (current_row_item.id == -1) {
    // 如果没有选中资源，则显示最近上传的元信息
    choose_resource_meta.id = null;
    choose_resource_meta.resource_name = '最近上传';
    choose_resource_meta.resource_icon = '/images/folder.svg';
    choose_resource_meta.resource_desc = '可以查看到最近30天内上传的各类资源';
    show_meta_flag.value = true;
    return;
  }
  if (!current_row_item?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (current_row_item.resource_status == '删除') {
    turn_on_resource_meta(current_row_item.id, '删除');
    return;
  }
  const userInfoStore = useUserInfoStore();
  if (current_row_item.user_id == userInfoStore.userInfo.user_id) {
    turn_on_resource_meta(current_row_item.id);
  } else {
    turn_on_resource_meta(current_row_item.id, '共享');
  }
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
  const params = {
    resource_id: current_row_item.id
  };
  const res = await download_resource_object(params);
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
export async function share_resource() {
  // 分享资源
  if (!current_row_item?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (current_row_item.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  await turn_on_share_selector(current_row_item);
}
export async function move_resource() {
  if (!current_row_item?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (current_row_item.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 移动资源
  show_move_dialog_multiple([current_row_item.id]);
}

export async function rebuild_resource() {
  if (!current_row_item?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (current_row_item.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 检查资源状态
  if (current_row_item.resource_status != '正常') {
    ElMessage.warning('资源无法构建索引!');
    return;
  }
  if (!check_resource_rag_support(current_row_item)) {
    ElMessage.warning(`暂时不支持'${current_row_item.resource_format}'格式构建索引!`);
    return;
  }

  const params = {
    resource_list: [current_row_item.id]
  };
  const res = await build_resource_object_ref(params);
  if (!res.error_status) {
    ElMessage.success('提交重建任务成功!');
  }
}

export async function delete_resource() {
  if (!current_row_item?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (current_row_item.resource_status == '删除') {
    ElMessage.warning('资源已删除!');
    return;
  }
  // 删除资源
  const params = {
    resource_id: current_row_item.id
  };
  const res = await delete_resource_object_api(params);
  if (!res.error_status) {
    ElMessage.success('删除成功!');
    await search_resource_by_tags();
  }
}

export function select_all() {
  // 全选
  for (const item of current_resource_list.value) {
    item.resource_is_selected = !item.resource_is_selected;
  }
  show_multiple_button.value = !show_multiple_button.value;
  resource_shortcut_Ref.value?.toggleAllSelection();
}

export function init_upload_manager() {
  upload_parent_resource.value = null;
  upload_button_Ref.value = upload_file_Ref.value;
}

export async function handleDrop(event) {
  upload_parent_resource.value = null;
  // 获取拖拽文件
  const files = event.dataTransfer.files;
  if (files.length > 0) {
    for (let j = 0; j < files.length; j++) {
      if (files[j]) {
        const file = files[j] as UploadRawFile;
        file.uid = genFileId();
        upload_file_Ref.value?.handleStart(file);
        upload_file_list.value.push(file);
        // prepare_upload_files(file)
      }
    }
    show_upload_manage_box.value = true;
    upload_file_Ref.value?.submit();
  }
}
