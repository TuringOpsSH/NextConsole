import {ElMessage, ElNotification} from 'element-plus';
import {reactive, ref} from 'vue';
import {
    build_resource_object_ref,
    get_resource_object,
    get_resource_recycle_object,
    resource_share_get_meta,
    search_resource_tags,
    update_resource_object
} from '@/api/resource-api';
import {search_all_resource_object} from '@/components/resource/resource-list/resource-list';
import {init_my_resource_tree} from '@/components/resource/resource-panel/panel';
import {search_resource_by_tags} from '@/components/resource/resource-shortcut/resource-shortcut';
import router from '@/router';
import {useUserInfoStore} from '@/stores/user-info-store';
import {IResourceItem, IResourceTag} from '@/types/resource-type';

export const show_meta_flag = ref(false);
export const meta_edit_flag = ref(false);
//@ts-ignore
export const choose_resource_meta = reactive<IResourceItem>({
  id: null,
  resource_parent_id: null,
  user_id: null,
  resource_name: null,
  resource_type: null,
  resource_desc: null,
  resource_icon: null,
  resource_format: null,
  resource_size_in_MB: null,
  resource_status: null,
  resource_language: null,
  ref_status: null,
  delete_time: null,
  resource_parent_name: null,
  create_time: null,
  update_time: null,
  show_buttons: null,
  resource_tags: [],
  resource_is_selected: null,
  sub_resource_dir_cnt: null,
  sub_resource_file_cnt: null,
  author_info: null
});
export const loading_meta = ref(false);
export const loading_meta_tags = ref(false);
export const all_resource_tags = ref<IResourceTag[]>([]);
export const uncommit_notice = ref(false);
export const show_rebuild_button = ref(true);
export async function turn_on_resource_meta(resource_id: number, resource_status: string = '正常') {
  show_meta_flag.value = true;
  loading_meta.value = true;
  let res = null;
  if (resource_status == '删除') {
    res = await get_resource_recycle_object({
      resource_id: resource_id
    });
  } else if (resource_status == '共享') {
    if (resource_id == -1) {
      choose_resource_meta.id = null;
      choose_resource_meta.resource_name = '共享资源';
      choose_resource_meta.resource_icon = 'folder.svg';
      choose_resource_meta.resource_desc = '共享资源';
      choose_resource_meta.resource_language = null;
      choose_resource_meta.resource_size_in_MB = null;
      choose_resource_meta.resource_format = null;
      choose_resource_meta.ref_status = null;
      choose_resource_meta.create_time = null;
      choose_resource_meta.resource_type = null;
      choose_resource_meta.resource_type_cn = null;
      choose_resource_meta.resource_path = null;
      choose_resource_meta.resource_tags = null;
      choose_resource_meta.resource_status = null;
      all_resource_tags.value = null;
      choose_resource_meta.sub_resource_dir_cnt = null;
      choose_resource_meta.sub_resource_file_cnt = null;
      choose_resource_meta.sub_rag_file_cnt = null;
      choose_resource_meta.author_info = null;
      choose_resource_meta.access_list = null;
      choose_resource_meta.resource_parent_id = null;
      loading_meta.value = false;
      return;
    }

    res = await resource_share_get_meta({
      resource_id: resource_id
    });
  } else {
    res = await get_resource_object({
      resource_id: resource_id
    });
  }

  if (!res.error_status) {
    choose_resource_meta.id = res.result.id;
    choose_resource_meta.user_id = res.result.user_id;
    choose_resource_meta.resource_name = res.result.resource_name;
    choose_resource_meta.resource_icon = res.result.resource_icon;
    choose_resource_meta.resource_desc = res.result.resource_desc;
    choose_resource_meta.resource_language = res.result.resource_language;
    choose_resource_meta.resource_size_in_MB = res.result.resource_size_in_MB;
    choose_resource_meta.resource_format = res.result.resource_format;
    choose_resource_meta.ref_status = res.result.ref_status;
    choose_resource_meta.create_time = res.result.create_time;
    choose_resource_meta.resource_type = res.result.resource_type;
    choose_resource_meta.resource_type_cn = res.result.resource_type_cn;
    choose_resource_meta.resource_path = res.result.resource_path;
    choose_resource_meta.resource_tags = res.result.resource_tags;
    choose_resource_meta.resource_status = res.result.resource_status;
    all_resource_tags.value = res.result.resource_tags;
    choose_resource_meta.sub_resource_dir_cnt = res.result?.sub_resource_dir_cnt;
    choose_resource_meta.sub_resource_file_cnt = res.result?.sub_resource_file_cnt;
    choose_resource_meta.sub_rag_file_cnt = res.result?.sub_rag_file_cnt;
    choose_resource_meta.author_info = res.result?.author_info;
    choose_resource_meta.access_list = res.result?.access_list;
    choose_resource_meta.resource_parent_id = res.result?.resource_parent_id;
  }
  loading_meta.value = false;
}

export async function switch_resource_edit_model() {
  if (choose_resource_meta.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 检查是否有编辑和修改权限
  const userInfoStore = useUserInfoStore();
  if (
    choose_resource_meta.user_id == userInfoStore.userInfo.user_id ||
    choose_resource_meta?.access_list?.includes('管理')
  ) {
    meta_edit_flag.value = !meta_edit_flag.value;
    return;
  }
  ElMessage.warning('需要管理权限!');
}

export async function search_resource_tags_by_keyword(query: string) {
  if (query === '') {
    return;
  }
  const params = {
    tag_keyword: query,
    fetch_all: true
  };
  loading_meta_tags.value = true;
  const res = await search_resource_tags(params);
  if (!res.error_status) {
    all_resource_tags.value = res.result;
  }
  loading_meta_tags.value = false;
}

export async function update_choose_resource_meta() {
  const params = {
    resource_id: choose_resource_meta.id,
    resource_name: choose_resource_meta.resource_name,
    resource_desc: choose_resource_meta.resource_desc,
    resource_language: choose_resource_meta.resource_language,
    resource_tags: choose_resource_meta.resource_tags
  };
  const res = await update_resource_object(params);
  if (!res.error_status) {
    meta_edit_flag.value = false;
    ElMessage.success('更新成功');
  }
  init_my_resource_tree();
  if (router.currentRoute.value.name === 'resource_list') {
    search_all_resource_object();
  } else if (router.currentRoute.value.name === 'resource_shortcut') {
    search_resource_by_tags();
  }
}

export async function before_leave_check(done) {
  if (!choose_resource_meta.id) {
    return done(false);
  }

  // // console.log(choose_resource_meta,'choose_resource_meta')
  if (choose_resource_meta.resource_status == '删除') {
    return done(false);
  }
  // 检查是否有未提交的修改
  const userInfoStore = useUserInfoStore();
  let res = null;
  if (choose_resource_meta.user_id != userInfoStore.userInfo.user_id) {
    res = await resource_share_get_meta({
      resource_id: choose_resource_meta.id
    });
  } else {
    res = await get_resource_object({
      resource_id: choose_resource_meta.id
    });
  }

  if (!res.error_status) {
    // 逐个检查属性是否有变化
    if (res.result.resource_name !== choose_resource_meta.resource_name) {
      uncommit_notice.value = true;
      return;
    }
    if (res.result.resource_desc !== choose_resource_meta.resource_desc) {
      uncommit_notice.value = true;
      return;
    }
    if (res.result.resource_language !== choose_resource_meta.resource_language) {
      uncommit_notice.value = true;
      return;
    }
    const all_history_tag_ids = [];
    for (const item of res.result.resource_tags) {
      all_history_tag_ids.push(item.id);
    }
    const all_now_tag_ids = [];
    for (const item of choose_resource_meta.resource_tags) {
      all_now_tag_ids.push(item.id);
    }
    if (all_history_tag_ids.length !== all_now_tag_ids.length) {
      uncommit_notice.value = true;
      return;
    }
  }
  return done(false);
}

export async function cancel_resource_edit_model() {
  const res = await get_resource_object({
    resource_id: choose_resource_meta.id
  });
  if (!res.error_status) {
    choose_resource_meta.resource_name = res.result.resource_name;
    choose_resource_meta.resource_desc = res.result.resource_desc;
    choose_resource_meta.resource_language = res.result.resource_language;
    choose_resource_meta.resource_tags = res.result.resource_tags;
  }
  meta_edit_flag.value = false;
}

export async function rebuild_resource() {
  if (!choose_resource_meta?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (choose_resource_meta.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 检查资源状态
  if (choose_resource_meta.resource_status != '正常') {
    ElMessage.warning('资源无法构建索引!');
    return;
  }

  const params = {
    resource_list: [choose_resource_meta.id]
  };
  const res = await build_resource_object_ref(params);
  if (!res.error_status) {
    ElNotification({
      title: '系统通知',
      message: `成功提交重新构建任务，请耐心等待！`,
      type: 'success',
      duration: 5000
    });
  }
}
