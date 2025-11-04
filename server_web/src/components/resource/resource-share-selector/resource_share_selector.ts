import { ref, nextTick } from 'vue';
import { ResourceAccess, ResourceItem } from '@/types/resource-type';
import {
  get_colleague_list,
  get_department_list,
  get_friend_list,
  search_colleague,
  search_department_info,
  search_friends
} from '@/api/contacts';
import type Node from 'element-plus/es/components/tree/src/model/node';
import { useUserInfoStore } from '@/stores/user-info-store';
import {
  resource_share_check_access,
  resource_share_get_access_list,
  resource_share_update_access_list
} from '@/api/resource-api';
import { ElMessage } from 'element-plus';
import { init_share_resource_tree } from '@/components/resource/resource-panel/panel';

export const share_selector_vis_flag = ref(false);
export const current_share_resource = ref<ResourceItem>(null);

export const search_keyword = ref('');
export const current_model = ref('tree');
export const props = {
  isLeaf: 'leaf',
  disable: 'disabled',
  label: 'label',
  children: 'children'
};
export interface Tree {
  label: string;
  children?: Tree[];
  leaf?: boolean;
  disabled?: boolean;
  structure_type: string;
  user_id?: number;
  user_avatar?: string;
  user_position?: string;
  user_company?: string;
  user_department?: string;
  user_gender?: string;
  user_email?: string;
  user_department_id?: number;
  user_nick_name_py?: string;

  department_id?: number;
  company_id?: number;
  parent_department_id?: number;
  department_name?: string;
  department_logo?: string;
  structure_id?: string;
  get_access?: boolean;
  access?: string;
  resource_id?: number;
}
export const current_all_share_objects = ref<Tree[]>([]);
export const current_share_Ref = ref();
export const get_access_object_list = ref<Tree[]>([]);
export const batch_share_access = ref('read');
export const left_cnt = ref(0);
export const right_cnt = ref(0);
export const access_loading = ref(false);
export const current_search_result = ref<Tree[]>([]);
export async function turn_on_share_selector(resource: ResourceItem) {
  // 判断是否有权限
  const userInfoStore = useUserInfoStore();
  if (resource.user_id != userInfoStore.userInfo.user_id) {
    let check_res = await resource_share_check_access({
      resource_id: resource.id,
      access_type: 'manage'
    });
    if (check_res.error_status) {
      return;
    }
    if (check_res.result == false) {
      ElMessage.warning('需要管理权限!');
      return;
    }
  }

  share_selector_vis_flag.value = true;
  await nextTick();
  current_share_resource.value = resource;
  current_all_share_objects.value = [];
  // 初始化公司架构
  if (userInfoStore.userInfo?.user_account_type == '企业账号') {
    current_all_share_objects.value.push({
      label: userInfoStore.userInfo?.user_company,
      children: [],
      leaf: false,
      disabled: false,
      structure_type: 'department',
      department_logo: '/images/department_default.svg',
      structure_id: 'department',
      company_id: userInfoStore.userInfo?.user_company_id,
      access: 'read'
    } as Tree);
  }
  // 初始化好友列表
  let friend_tree = {
    label: '好友',
    children: [],
    leaf: false,
    disabled: false,
    structure_type: 'friend',
    user_avatar: '/images/default_friends.svg',
    structure_id: 'friend',
    access: ''
  } as Tree;
  current_all_share_objects.value.push(friend_tree);
  // 初始化权限列表
  get_access_object_list.value = [];
  if (resource.user_id == userInfoStore.userInfo.user_id) {
    get_access_object_list.value.push({
      label: userInfoStore.userInfo.user_name || userInfoStore.userInfo.user_nick_name,
      leaf: true,
      disabled: true,
      structure_type: 'colleague',
      structure_id: 'colleague' + userInfoStore.userInfo.user_id,
      user_nick_name_py: userInfoStore.userInfo.user_nick_name_py,
      //@ts-ignore
      user_id: userInfoStore.userInfo.user_id,
      user_avatar: userInfoStore.userInfo?.user_avatar,
      user_position: userInfoStore.userInfo?.user_position,
      user_company: userInfoStore.userInfo?.user_company,
      user_email: userInfoStore.userInfo?.user_email,
      user_gender: userInfoStore.userInfo?.user_gender,
      user_department: userInfoStore.userInfo?.user_department,
      user_department_id: userInfoStore.userInfo?.user_department_id,
      access: 'manage'
    });
  }

  access_loading.value = true;
  let all_access_res = await resource_share_get_access_list({
    resource_id: resource.id
  });
  if (!all_access_res.error_status) {
    for (let access of all_access_res.result.access_list) {
      // 如果权限来源资源不是当前资源，则显示禁用
      if (access.type == 'company') {
        get_access_object_list.value.push({
          label: access.meta.company_name,
          children: [],
          leaf: false,
          disabled: access?.resource_id && access?.resource_id != resource.id,
          structure_type: 'department',
          department_logo: access.meta.company_logo || '/images/department_default.svg',
          structure_id: 'department' + access.meta.id,
          company_id: access.meta.id,
          access: access.auth_type,
          resource_id: access.resource_id
        } as Tree);
      } else if (access.type == 'department') {
        get_access_object_list.value.push({
          label: access.meta.department_name,
          children: [],
          leaf: false,
          disabled: false,
          structure_type: 'department',
          department_logo: access.meta.department_logo || '/images/department_default.svg',
          structure_id: 'department' + access.meta.id,
          department_id: access.meta.id,
          parent_department_id: access.meta.parent_department_id,
          access: access.auth_type,
          resource_id: access.resource_id
        } as Tree);
      } else if (access.type == 'colleague') {
        get_access_object_list.value.push({
          label: access.meta.user_name || access.meta.user_nick_name,
          leaf: true,
          disabled:
            (access?.resource_id && access?.resource_id != resource.id) || resource.user_id == access.meta.user_id,
          structure_type: 'colleague',
          structure_id: 'colleague' + access.meta.user_id,
          user_id: access.meta.user_id,
          user_avatar: access.meta?.user_avatar,
          user_position: access.meta?.user_position,
          user_company: access.meta?.user_company,
          user_email: access.meta?.user_email,
          user_gender: access.meta?.user_gender,
          user_department: access.meta?.user_department,
          user_department_id: access.meta?.user_department_id,
          access: access.auth_type,
          resource_id: access.resource_id,
          user_nick_name_py: access.meta.user_nick_name_py
        });
      } else if (access.type == 'friend') {
        // 如果是全部好友
        if (!access.id) {
          get_access_object_list.value.push(friend_tree);
        } else {
          get_access_object_list.value.push({
            label: access.meta.user_nick_name,
            leaf: true,
            disabled:
              (access?.resource_id && access?.resource_id != resource.id) || resource.user_id == access.meta.user_id,
            structure_type: 'friend',
            structure_id: 'friend' + access.meta.user_id,
            user_id: access.meta.user_id,
            user_avatar: access.meta?.user_avatar,
            user_position: access.meta?.user_position,
            user_company: access.meta?.user_company,
            user_email: access.meta?.user_email,
            user_gender: access.meta?.user_gender,
            user_department: access.meta?.user_department,
            user_department_id: access.meta?.user_department_id,
            user_nick_name_py: access.meta?.user_nick_name_py,
            access: access.auth_type,
            resource_id: access.resource_id
          });
        }
      }
    }
  }
  access_loading.value = false;
}
export async function turn_off_share_selector() {
  share_selector_vis_flag.value = false;
}
export async function get_company_structure_tree(node: Node, resolve: (data: Tree[]) => void) {
  let data: Tree[] = [];
  // 获取全部好友
  if (node.data.structure_type === 'friend') {
    let friend_list = await get_friend_list({});
    if (!friend_list.error_status) {
      for (let friend of friend_list.result.data) {
        // 如果在右侧已经存在，则不再添加
        let is_exist = false;
        for (let object of get_access_object_list.value) {
          if (object.user_id == friend.user_id) {
            is_exist = true;
            break;
          }
        }
        if (is_exist) {
          continue;
        }
        let friend_data = {
          label: friend.user_nick_name,
          leaf: true,
          disabled: false,
          structure_type: 'friend',
          structure_id: 'friend' + friend.user_id,
          user_id: friend.user_id,
          user_avatar: friend?.user_avatar,
          user_position: friend?.user_position,
          user_company: friend?.user_company,
          user_email: friend?.user_email,
          user_nick_name_py: friend?.user_nick_name_py,
          access: ''
        };
        data.push(friend_data);
      }
    }
    return resolve(data);
  }
  // 获取部门下的同事
  if (node.data.structure_type !== 'department') {
    return resolve([]);
  }
  if (node.disabled) {
    return resolve([]);
  }
  let leaders = await get_colleague_list({
    department_id: node.data?.department_id,
    is_root: !node.data?.department_id
  });
  const userInfoStore = useUserInfoStore();
  if (!leaders.error_status) {
    for (let leader of leaders.result) {
      if (leader.user_id == userInfoStore.userInfo.user_id) {
        continue;
      }
      // 如果在右侧已经存在，则不再添加
      let is_exist = false;
      for (let object of get_access_object_list.value) {
        if (object.user_id == leader.user_id) {
          is_exist = true;
          break;
        }
      }
      if (is_exist) {
        continue;
      }
      let leader_data = {
        label: leader.user_name || leader.user_nick_name,
        leaf: true,
        disabled: false,
        structure_type: 'colleague',
        structure_id: 'colleague' + leader.user_id,
        user_id: leader.user_id,
        user_avatar: leader?.user_avatar,
        user_position: leader?.user_position,
        user_company: leader?.user_company,
        user_email: leader?.user_email,
        user_gender: leader?.user_gender,
        user_department: leader?.user_department,
        user_department_id: leader?.user_department_id,
        user_nick_name_py: leader?.user_nick_name_py,
        access: ''
      } as Tree;
      data.push(leader_data);
    }
  }
  // 获取公司部门
  let departments = await get_department_list({
    parent_department_id: node.data?.department_id
  });
  if (!departments.error_status) {
    for (let department of departments.result) {
      // 如果在右侧已经存在，则不再添加
      let is_exist = false;
      for (let object of get_access_object_list.value) {
        if (object.department_id == department.id) {
          is_exist = true;
          break;
        }
      }
      if (is_exist) {
        continue;
      }
      let department_data = {
        label: department.department_name,
        children: [],
        leaf: false,
        disabled: false,
        structure_type: 'department',
        structure_id: 'department' + department.id,
        company_id: department.company_id,
        department_id: department.id,
        department_name: department.department_name,
        department_logo: department?.department_logo || '/images/department_default.svg',
        parent_department_id: department.parent_department_id,
        access: ''
      } as Tree;
      data.push(department_data);
    }
  }
  resolve(data);
}
export function batch_set_share_access(val: string) {
  // 批量设置分享权限
  const userInfoStore = useUserInfoStore();
  for (let object of get_access_object_list.value) {
    if (object.user_id == userInfoStore.userInfo.user_id) {
      continue;
    }
    object.access = val;
  }
}
export function add_get_access_object() {
  let checked_nodes = current_share_Ref.value.getCheckedNodes();
  for (let object of checked_nodes) {
    current_share_Ref.value.remove(object);
  }
  left_cnt.value = current_share_Ref.value.getCheckedNodes().length;
  for (let object of checked_nodes) {
    object.get_access = false;
    object.access = batch_share_access.value;
    object.disable = false;
    get_access_object_list.value.push(object);
  }
}
export function remove_get_access_object() {
  // 获取当前选中的对象并恢复至左侧树状结构
  for (let object of get_access_object_list.value) {
    if (object.get_access) {
      if (object.structure_type == 'department') {
        // 如果为根节点
        if (object.structure_id == 'department') {
          current_all_share_objects.value.unshift(object);
        } else {
          // console.log(object, '开始恢复')
          current_share_Ref.value.append(object, 'department' + object.parent_department_id);
        }
      } else if (object.structure_type == 'colleague') {
        let parent_id = 'department' + object.user_department_id;
        let parent_node = current_share_Ref.value.getNode(parent_id);
        if (!parent_node) {
          current_share_Ref.value.append(object, 'department');
        } else {
          current_share_Ref.value.append(object, 'department' + object.user_department_id);
        }
      } else if (object.structure_type == 'friend') {
        if (object.structure_id == 'friend') {
          current_all_share_objects.value.push(object);
        } else {
          current_share_Ref.value.append(object, 'friend');
        }
      }
    }
  }
  // 删除当前选中的对象
  get_access_object_list.value = get_access_object_list.value.filter(object => !object.get_access);
  // 更新右侧的数量
  update_right_cnt();
}
export function update_right_cnt() {
  let right_cnt_val = 0;
  for (let object of get_access_object_list.value) {
    if (object.get_access) {
      right_cnt_val += 1;
    }
  }
  right_cnt.value = right_cnt_val;
}
export function update_left_cnt(data, status) {
  left_cnt.value = current_share_Ref.value.getCheckedNodes().length;
}
export async function confirm_update_share_access() {
  // 确认更新分享权限
  let access_list = [];
  for (let object of get_access_object_list.value) {
    if (object.structure_type == 'department') {
      // console.log(object)
      if (!object.parent_department_id) {
        access_list.push({
          type: 'company',
          id: object.company_id,
          auth_type: object.access
        } as ResourceAccess);
        continue;
      }
      access_list.push({
        type: 'department',
        id: object.department_id,
        auth_type: object.access
      } as ResourceAccess);
    } else if (object.structure_type == 'colleague') {
      const userInfoStore = useUserInfoStore();
      if (object.user_id == userInfoStore.userInfo.user_id) {
        continue;
      }
      access_list.push({
        type: 'colleague',
        id: object.user_id,
        auth_type: object.access
      } as ResourceAccess);
    } else if (object.structure_type == 'friend') {
      access_list.push({
        type: 'friend',
        id: object?.user_id,
        auth_type: object.access
      } as ResourceAccess);
    }
  }
  let params = {
    resource_id: current_share_resource.value.id,
    access_list: access_list
  };
  let res = await resource_share_update_access_list(params);
  if (!res.error_status) {
    // 更新成功，刷新权限列表
    await turn_on_share_selector(current_share_resource.value);
    await init_share_resource_tree();
    ElMessage.success('更新成功!');
  }
}

export const current_share_search_Ref = ref();
export const left_search_cnt = ref(0);
export async function search_company_department_and_colleague() {
  // 根据关键字搜索公司部门和同事,并展望为树形结构
  if (!search_keyword.value) {
    return;
  }
  let params = {
    keyword: search_keyword.value
  };
  current_search_result.value = [];
  // 搜索公司部门
  let res_department = await search_department_info(params);
  if (!res_department.error_status) {
    for (let department of res_department.result) {
      let department_data = {
        label: department.department_name,
        children: [],
        leaf: false,
        disabled: false,
        structure_type: 'department',
        structure_id: 'department' + department.id,
        company_id: department.company_id,
        department_id: department.id,
        department_name: department.department_name,
        department_logo: department?.department_logo || '/images/department_default.svg',
        parent_department_id: department.parent_department_id,
        access: ''
      } as Tree;
      current_search_result.value.push(department_data);
    }
  }
  // 搜索公司同事
  let res_colleague = await search_colleague(params);
  if (!res_colleague.error_status) {
    for (let colleague of res_colleague.result) {
      let colleague_data = {
        label: colleague.user_name || colleague.user_nick_name,
        leaf: true,
        disabled: false,
        structure_type: 'colleague',
        structure_id: 'colleague' + colleague.user_id,
        user_id: colleague.user_id,
        user_avatar: colleague?.user_avatar,
        user_position: colleague?.user_position,
        user_company: colleague?.user_company,
        user_email: colleague?.user_email,
        user_gender: colleague?.user_gender,
        user_department: colleague?.user_department,
        user_department_id: colleague?.user_department_id,
        user_nick_name_py: colleague?.user_nick_name_py,

        access: ''
      };
      current_search_result.value.push(colleague_data);
    }
  }
  // 搜索好友
  let search_res = await search_friends({
    friend_keyword: search_keyword.value
  });
  if (!search_res.error_status) {
    for (let friend of search_res.result.data) {
      let friend_data = {
        label: friend.user_nick_name,
        leaf: true,
        disabled: false,
        structure_type: 'friend',
        structure_id: 'friend' + friend.user_id,
        user_id: friend.user_id,
        user_avatar: friend?.user_avatar,
        user_position: friend?.user_position,
        user_company: friend?.user_company,
        user_email: friend?.user_email,
        user_gender: friend?.user_gender,
        user_department: friend?.user_department,
        user_department_id: friend?.user_department_id,
        user_nick_name_py: friend?.user_nick_name_py,
        access: ''
      };
      current_search_result.value.push(friend_data);
    }
  }
}
export function exit_search_model() {
  search_keyword.value = '';
  current_model.value = 'tree';
  current_search_result.value = [];
}
export function auto_exit_search_model() {
  if (!search_keyword.value) {
    exit_search_model();
  }
}
export async function auto_handle_search_blur() {
  if (!search_keyword.value) {
    exit_search_model();
    return;
  }
  await search_company_department_and_colleague();
}
export async function add_get_access_object_by_search() {
  let checked_nodes = current_share_search_Ref.value.getCheckedNodes();
  for (let object of checked_nodes) {
    current_share_search_Ref.value.remove(object);
  }
  left_cnt.value = current_share_search_Ref.value.getCheckedNodes().length;
  for (let object of checked_nodes) {
    object.get_access = false;
    object.access = batch_share_access.value;
    get_access_object_list.value.push(object);
  }
}
export function update_left_search_cnt(data, status) {
  left_search_cnt.value = current_share_search_Ref.value.getCheckedNodes().length;
}
