import type Node from 'element-plus/es/components/tree/src/model/node';
import { ref } from 'vue';
import {
  get_colleague_list,
  get_department_info,
  get_department_list,
  search_colleague,
  search_department_info
} from '@/api/contacts';
import { useUserInfoStore } from '@/stores/user-info-store';
import { Colleague, Department } from '@/types/contacts';

export const current_department = ref<Department>();
export const current_colleague = ref<Colleague>({
  user_id: null,
  user_nick_name: '测试用户昵称',
  user_email: '',
  user_gender: '女',
  user_avatar: '',
  user_department: '产品研发部',
  user_company: '',
  user_position: '高级算法工程师',
  user_name: '测试用户',
  roles: []
});
export const current_item_type = ref('department');
export const current_model = ref('tree');
export const current_search_keyword = ref('');
export const props = {
  isLeaf: 'leaf',
  disable: 'disabled',
  value: 'id'
};
interface Tree {
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
  department_id?: number;
  department_name?: string;
  department_logo?: string;
  user_nick_name?: string;
  user_nick_name_py?: string;
  user_name?: string;
  roles?: any;
}
export const current_company_structure_Ref = ref();
export const current_company_structure_data = ref<Tree[]>();
export async function init_company_structure_tree() {
  const userInfoStore = useUserInfoStore();
  // 初始化公司结构树
  current_company_structure_data.value = [];
  if (userInfoStore.userInfo.user_account_type != '企业账号') {
    console.log('非企业账号，无法查看公司结构', userInfoStore.userInfo);
    return;
  }
  // 获取公司领导人
  const leaders = await get_colleague_list({ is_root: true });
  if (!leaders.error_status) {
    for (const leader of leaders.result) {
      const leader_data = {
        label: leader.user_name || leader?.user_nick_name,
        leaf: true,
        disabled: false,
        structure_type: 'colleague',
        user_id: leader.user_id,
        user_avatar: leader?.user_avatar,
        user_position: leader?.user_position,
        user_company: leader?.user_company,
        user_email: leader?.user_email,
        user_gender: leader?.user_gender,
        user_department: leader?.user_department,
        user_name: leader?.user_name,
        user_nick_name: leader?.user_nick_name,
        user_nick_name_py: leader?.user_nick_name_py,
        roles: leader.roles
      } as Tree;
      current_company_structure_data.value.push(leader_data);
    }
  }
  // 获取公司部门
  const departments = await get_department_list({});
  if (!departments.error_status) {
    for (const department of departments.result) {
      const department_data = {
        label: department.department_name,
        children: [],
        leaf: false,
        disabled: false,
        structure_type: 'department',
        department_id: department.id,
        department_name: department.department_name,
        department_logo: department?.department_logo || '/images/department_default.svg'
      } as Tree;
      current_company_structure_data.value.push(department_data);
    }
  }
}
export async function get_company_structure_tree(node: Node, resolve: (data: Tree[]) => void) {
  // 获得下一层目录，并标记叶子节点，不可用目录
  if (node.data.structure_type !== 'department') {
    return resolve([]);
  }
  if (node.disabled) {
    return resolve([]);
  }
  const data: Tree[] = [];
  // 获取部门下的同事
  const leaders = await get_colleague_list({ department_id: node.data?.department_id });
  if (!leaders.error_status) {
    for (const leader of leaders.result) {
      const leader_data = {
        label: leader.user_name || leader?.user_nick_name,
        leaf: true,
        disabled: false,
        structure_type: 'colleague',
        user_id: leader.user_id,
        user_avatar: leader?.user_avatar,
        user_position: leader?.user_position,
        user_company: leader?.user_company,
        user_email: leader?.user_email,
        user_gender: leader?.user_gender,
        user_department: leader?.user_department,
        user_name: leader?.user_name,
        user_nick_name: leader?.user_nick_name,
        user_nick_name_py: leader?.user_nick_name_py,
        roles: leader.roles
      } as Tree;
      data.push(leader_data);
    }
  }
  // 获取公司部门
  const departments = await get_department_list({
    parent_department_id: node.data?.department_id
  });
  if (!departments.error_status) {
    for (const department of departments.result) {
      const department_data = {
        label: department.department_name,
        children: [],
        leaf: false,
        disabled: false,
        structure_type: 'department',
        department_id: department.id,
        department_name: department.department_name,
        department_logo: department?.department_logo || '/images/department_default.svg'
      } as Tree;
      data.push(department_data);
    }
  }
  resolve(data);
}
export async function set_current_item_type(node: Node, data: Tree) {
  current_item_type.value = data.structure_type;
  if (data.structure_type === 'department') {
    const department_detail_res = await get_department_info({ department_id: data.department_id });
    if (!department_detail_res.error_status) {
      current_department.value = department_detail_res.result;
    }
  } else if (data.structure_type === 'colleague') {
    // @ts-ignore
    current_colleague.value = {
      user_id: data.user_id,
      user_nick_name: data.user_nick_name,
      user_email: data.user_email,
      user_gender: data.user_gender,
      user_avatar: data.user_avatar,
      user_department: data.user_department,
      user_company: data.user_company,
      user_position: data.user_position,
      user_name: data.user_name
    };
  }
  if (window.innerWidth < 768) {
    company_structure_width.value = '0px';
  }
}

export const search_department_colleague_data = ref<Tree[]>([]);

export const company_structure_width = ref(window.innerWidth < 768 ? window.innerWidth - 60 + 'px' : '300px');

export async function search_company_department_and_colleague() {
  // 根据关键字搜索公司部门和同事,并展望为树形结构
  if (!current_search_keyword.value) {
    return;
  }
  const params = {
    keyword: current_search_keyword.value
  };
  // 搜索公司部门
  const res_department = await search_department_info(params);
  if (!res_department.error_status) {
    search_department_colleague_data.value = [];
    for (const department of res_department.result) {
      const department_data = {
        label: department.department_name,
        leaf: false,
        disabled: false,
        structure_type: 'department',
        department_id: department.id,
        department_name: department.department_name,
        department_logo: department?.department_logo || '/images/department_default.svg'
      } as Tree;
      search_department_colleague_data.value.push(department_data);
    }
  }
  // 搜索公司同事
  const res_colleague = await search_colleague(params);
  if (!res_colleague.error_status) {
    for (const colleague of res_colleague.result) {
      const colleague_data = {
        label: colleague.user_name || colleague?.user_nick_name,
        leaf: true,
        disabled: false,
        structure_type: 'colleague',
        user_id: colleague.user_id,
        user_avatar: colleague?.user_avatar,
        user_position: colleague?.user_position,
        user_company: colleague?.user_company,
        user_email: colleague?.user_email,
        user_gender: colleague?.user_gender,
        user_department: colleague?.user_department,
        user_name: colleague?.user_name,
        user_nick_name: colleague?.user_nick_name,
        user_nick_name_py: colleague?.user_nick_name_py,
        roles: colleague.roles
      } as Tree;
      search_department_colleague_data.value.push(colleague_data);
    }
  }
}

export function exit_search_model() {
  current_model.value = 'tree';
  current_search_keyword.value = '';
  current_colleague.value = null;
  current_department.value = null;
  search_department_colleague_data.value = [];
}
export function auto_exit_search_model() {
  if (!current_search_keyword.value) {
    exit_search_model();
  }
}
export async function auto_handle_search_blur() {
  if (!current_search_keyword.value) {
    exit_search_model();
  }
  search_company_department_and_colleague();
}
export function back_company_lists() {
  company_structure_width.value = window.innerWidth < 768 ? window.innerWidth - 60 + 'px' : '300px';
}
