<script setup lang="ts">
import { Search, ArrowLeft, ArrowRight } from '@element-plus/icons-vue';
import type Node from 'element-plus/es/components/tree/src/model/node';
import { ref, reactive, watch, nextTick } from 'vue';
import {
  searchDepartmentInfo,
  getFriendList,
  getColleagueList,
  getDepartmentList,
  searchColleague,
  searchFriends
} from '@/api/contacts';
import { useUserInfoStore } from '@/stores/user-info-store';
import { ILLMInstance } from '@/types/config-center';
interface ITree {
  label: string;
  children?: ITree[];
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
  company_logo?: string;
}
const mainProps = defineProps({
  shareModel: {
    type: Object as () => ILLMInstance,
    required: true
  }
});
const emits = defineEmits({
  updateAccessList: (val: ITree[]) => {
    return val;
  }
});
const props = {
  isLeaf: 'leaf',
  disable: 'disabled',
  label: 'label',
  children: 'children'
};
const searchAuthorKeyword = ref('');
const currentModel = ref('tree');
const currentSearchResult = ref([]);
const currentAllShareObjects = ref<ITree[]>([]);
const getAccessObjectList = ref<ITree[]>([]);
const currentShareRef = ref(null);
const currentShareSearchRef = ref(null);
const accessLoading = ref(false);
const leftCnt = ref(0);
const leftSearchCnt = ref(0);
const rightCnt = ref(0);
const phoneView = ref(false);
const userInfoStore = useUserInfoStore();
const currentShareLLM = reactive<Partial<ILLMInstance>>({
  id: 0,
  llm_label: '',
  llm_icon: '',
  user_id: 0
});
const batchShareAccess = ref('use');
const accessOptions = [
  { value: 'use', label: '使用' },
  { value: 'read', label: '查看' },
  { value: 'edit', label: '编辑' },
  { value: 'manage', label: '管理' },
  { value: 'own', label: '拥有' }
];

async function initShareSelector() {
  currentAllShareObjects.value = [];
  // 初始化公司架构
  if (userInfoStore.userInfo?.user_role?.includes('next_console_admin')) {
    currentAllShareObjects.value.push({
      label: '全平台',
      children: [],
      leaf: true,
      disabled: false,
      structure_type: 'user',
      department_logo: '/images/logo.svg',
      structure_id: 'user_all',
      user_avatar: '/images/logo.svg',
      company_id: 0,
      user_id: 0,
      access: 'read'
    } as ITree);
  }
  if (userInfoStore.userInfo?.user_account_type == '企业账号') {
    currentAllShareObjects.value.push({
      label: userInfoStore.userInfo?.user_company,
      children: [],
      leaf: false,
      disabled: false,
      structure_type: 'department',
      department_logo: '/images/department_default.svg',
      structure_id: 'department_all',
      company_id: userInfoStore.userInfo?.user_company_id,
      access: 'read'
    } as ITree);
  }

  // 初始化好友列表
  let friendTree = {
    label: '好友',
    children: [],
    leaf: false,
    disabled: false,
    structure_type: 'friend',
    user_avatar: '/images/default_friends.svg',
    structure_id: 'friend_all',
    user_id: 0,
    access: ''
  } as ITree;
  currentAllShareObjects.value.push(friendTree);
  // 初始化权限列表
  getAccessObjectList.value = [];
  for (let access of currentShareLLM.llm_authors || []) {
    let accessObject = {
      label: '',
      leaf: true,
      disabled: false,
      structure_type: access.structure_type,
      structure_id: access.structure_type + access.id,
      company_logo: '',
      company_id: 0,
      parent_company_id: 0,
      parent_department_id: 0,
      department_id: 0,
      department_logo: '',
      user_id: access.user_id,
      user_avatar: access.user_avatar,
      user_position: access.user_position,
      user_company: access.user_company,
      user_department_id: access.user_department_id,
      user_nick_name: access.user_nick_name,
      user_nick_name_py: access.user_nick_name_py,
      access: access.access,
      children: []
    };
    if (access.structure_type == 'company') {
      accessObject.label = access.company_name;
      accessObject.structure_type = 'department';
      accessObject.department_logo = access.company_logo || '/images/department_default.svg';
      accessObject.leaf = false;
    } else if (access.structure_type == 'department') {
      accessObject.label = access.label || access.department_name;
      accessObject.department_logo = access.department_logo || '/images/department_default.svg';
      accessObject.department_id = access.department_id;
      accessObject.parent_department_id = access.parent_department_id;
      accessObject.structure_id = access.structure_type + access.department_id;
      accessObject.leaf = false;
    } else if (access.structure_type == 'colleague') {
      accessObject.label = access.label || access.user_name || access.user_nick_name;
    } else if (access.structure_type == 'friend') {
      accessObject.label = access.user_nick_name;
      accessObject.structure_id = 'friend' + access.user_id;
    }
    getAccessObjectList.value.push(accessObject);
  }
}
async function searchCompanyDepartmentAndColleague() {
  // 根据关键字搜索公司部门和同事,并展望为树形结构
  if (!searchAuthorKeyword.value) {
    return;
  }
  let params = {
    keyword: searchAuthorKeyword.value
  };
  currentSearchResult.value = [];
  // 搜索公司部门
  let resDepartment = await searchDepartmentInfo(params);
  if (!resDepartment.error_status) {
    for (let department of resDepartment.result) {
      let departmentData = {
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
      } as ITree;
      currentSearchResult.value.push(departmentData);
    }
  }
  // 搜索公司同事
  let resColleague = await searchColleague(params);
  if (!resColleague.error_status) {
    for (let colleague of resColleague.result) {
      let colleagueData = {
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
        user_nick_name: colleague?.user_nick_name,
        user_nick_name_py: colleague?.user_nick_name_py,
        access: ''
      };
      currentSearchResult.value.push(colleagueData);
    }
  }
  // 搜索好友
  let searchRes = await searchFriends({
    friend_keyword: searchAuthorKeyword.value
  });
  if (!searchRes.error_status) {
    for (let friend of searchRes.result.data) {
      let friendData = {
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
      currentSearchResult.value.push(friendData);
    }
  }
}
async function getCompanyStructureTree(node: Node, resolve: (data: ITree[]) => void) {
  if (node.level === 0) {
    return resolve(currentAllShareObjects.value);
  }
  let data: ITree[] = [];
  // 获取全部好友
  if (node.data.structure_type === 'friend') {
    return getFriends(node, resolve);
  }
  // 获取部门下的同事
  if (node.data.structure_type !== 'department') {
    return resolve([]);
  }
  if (node.disabled) {
    return resolve([]);
  }
  let leaders = await getColleagueList({
    department_id: node.data?.department_id,
    is_root: !node.data?.department_id
  });
  if (!leaders.error_status) {
    for (let leader of leaders.result) {
      if (leader.user_id == userInfoStore.userInfo.user_id) {
        continue;
      }
      // 如果在右侧已经存在，则不再添加
      let isExist = false;
      for (let object of getAccessObjectList.value) {
        if (object.user_id == leader.user_id) {
          isExist = true;
          break;
        }
      }
      if (isExist) {
        continue;
      }
      let leaderData = {
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
      } as ITree;
      data.push(leaderData);
    }
  }
  // 获取公司部门
  let departments = await getDepartmentList({
    parent_department_id: node.data?.department_id
  });
  if (!departments.error_status) {
    for (let department of departments.result) {
      // 如果在右侧已经存在，则不再添加
      let isExist = false;
      for (let object of getAccessObjectList.value) {
        if (object.department_id == department.id) {
          isExist = true;
          break;
        }
      }
      if (isExist) {
        continue;
      }
      let departmentData = {
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
      } as ITree;
      data.push(departmentData);
    }
  }
  resolve(data);
}
async function getFriends(node: Node, resolve: (data: ITree[]) => void) {
  let data: ITree[] = [];
  let friendList = await getFriendList({});
  if (!friendList.error_status) {
    for (let friend of friendList.result.data) {
      // 如果在右侧已经存在，则不再添加
      let isExist = false;
      for (let object of getAccessObjectList.value) {
        if (object.user_id == friend.user_id) {
          isExist = true;
          break;
        }
      }
      if (isExist) {
        continue;
      }
      let friendData = {
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
      data.push(friendData);
    }
  }
  return resolve(data);
}
async function autoHandleSearchBlur() {
  if (!searchAuthorKeyword.value) {
    exitSearchModel();
    return;
  }
  await searchCompanyDepartmentAndColleague();
}
function exitSearchModel() {
  searchAuthorKeyword.value = '';
  currentModel.value = 'tree';
  currentSearchResult.value = [];
}
function autoExitSearchModel() {
  if (!searchAuthorKeyword.value) {
    exitSearchModel();
  }
}
function updateLeftCnt() {
  leftCnt.value = currentShareRef.value.getCheckedNodes().length;
}
function updateLeftSearchCnt() {
  leftSearchCnt.value = currentShareSearchRef.value.getCheckedNodes().length;
}
function updateRightCnt() {
  let rightCntVal = 0;
  for (let object of getAccessObjectList.value) {
    if (object.get_access) {
      rightCntVal += 1;
    }
  }
  rightCnt.value = rightCntVal;
}
function removeGetAccessObject() {
  // 获取当前选中的对象并恢复至左侧树状结构
  for (let object of getAccessObjectList.value) {
    if (object.get_access) {
      if (object.structure_type == 'department') {
        // 如果为根节点
        if (object.structure_id == 'department_all') {
          currentAllShareObjects.value.unshift(object);
        } else {
          // console.log(object, '开始恢复')
          currentShareRef.value.append(object, 'department' + object.parent_department_id);
        }
      } else if (object.structure_type == 'colleague') {
        let parentId = 'department' + object.user_department_id;
        let parentNode = currentShareRef.value.getNode(parentId);
        if (!parentNode) {
          currentShareRef.value.append(object, 'department');
        } else {
          currentShareRef.value.append(object, 'department' + object.user_department_id);
        }
      } else if (object.structure_type == 'friend') {
        if (object.structure_id == 'friend_all') {
          currentAllShareObjects.value.push(object);
        } else {
          currentShareRef.value.append(object, 'friend');
        }
      }
    }
  }
  // 删除当前选中的对象
  getAccessObjectList.value = getAccessObjectList.value.filter(object => !object.get_access);
  // 恢复剩下的get_access
  for (let object of getAccessObjectList.value) {
    object.get_access = false;
  }
  nextTick();
  // 更新右侧的数量
  updateRightCnt();
  emits('updateAccessList', getAccessObjectList.value);
}
function addGetAccessObject() {
  let checkedNodes = currentShareRef.value.getCheckedNodes();
  for (let object of checkedNodes) {
    currentShareRef.value.remove(object);
  }
  leftCnt.value = currentShareRef.value.getCheckedNodes().length;
  for (let object of checkedNodes) {
    console.log(1, object)
    let accessObject = {
      label: object.label,
      leaf: true,
      disabled: false,
      structure_type: object.structure_type,
      structure_id: object.structure_id,
      company_logo: object?.company_logo,
      company_id: object?.company_id,
      parent_company_id: 0,
      parent_department_id: 0,
      department_id: object?.department_id,
      department_logo: object?.department_logo,
      user_id: object.user_id,
      user_avatar: object.user_avatar,
      user_position: object.user_position,
      user_company: object.user_company,
      user_department_id: object.user_department_id,
      user_nick_name: object.user_nick_name,
      user_nick_name_py: object.user_nick_name_py,
      access: 'use',
      colleague_id: object?.user_id,
      friend_id: object?.user_id,
      auth_user_id: object?.user_id,
      children: []
    };
    if (object.structure_type == 'department' && object?.structure_id == 'department_all') {
      // 分享整个公司时
      accessObject.department_id = 0;
    }
    getAccessObjectList.value.push(accessObject);
    console.log(2, accessObject);
  }
  emits('updateAccessList', getAccessObjectList.value);
}
async function addGetAccessObjectBySearch() {
  let checkedNodes = currentShareSearchRef.value.getCheckedNodes();
  for (let object of checkedNodes) {
    currentShareSearchRef.value.remove(object);
  }
  leftCnt.value = currentShareSearchRef.value.getCheckedNodes().length;
  for (let object of checkedNodes) {
    object.get_access = false;
    getAccessObjectList.value.push(object);
  }
}
function batchSetShareAccess(val: string) {
  // 批量设置分享权限
  const userInfoStore = useUserInfoStore();
  for (let object of getAccessObjectList.value) {
    if (object.user_id == userInfoStore.userInfo.user_id) {
      continue;
    }
    object.access = val;
  }
}
watch(
  () => mainProps.shareModel,
  val => {
    Object.assign(currentShareLLM, val);
    if (!getAccessObjectList.value.length) {
      initShareSelector();
    }
  },
  { immediate: true, deep: true }
);
defineExpose({
  initShareSelector,
  getAccessObjectList
});
</script>

<template>
  <div id="share_selector_main">
    <div id="resource_share_selector">
      <div id="selector_left">
        <div class="std-middle-box" style="width: 100%">
          <el-form style="width: 100%">
            <el-form-item style="margin-bottom: 0 !important">
              <el-input
                v-model="searchAuthorKeyword"
                placeholder="搜索添加共享成员"
                :prefix-icon="Search"
                clearable
                @focus="currentModel = 'search'"
                @blur="autoHandleSearchBlur"
                @clear="exitSearchModel"
                @change="autoExitSearchModel"
                @keydown.enter.prevent="searchCompanyDepartmentAndColleague"
              />
            </el-form-item>
          </el-form>
        </div>

        <div id="company_search">
          <el-scrollbar>
            <el-tree
              v-show="currentModel == 'tree'"
              ref="currentShareRef"
              :data="currentAllShareObjects"
              lazy
              :load="getCompanyStructureTree"
              :props="props"
              :highlight-current="true"
              node-key="structure_id"
              :show-checkbox="true"
              :check-strictly="true"
              :expand-on-click-node="true"
              @check="updateLeftCnt"
            >
              <template #default="{ node, data }">
                <div class="tree-button">
                  <div class="std-middle-box">
                    <el-avatar
                      v-show="data?.structure_type == 'colleague' && data?.user_avatar"
                      :src="data?.user_avatar"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="data?.structure_type == 'colleague' && !data?.user_avatar"
                      style="width: 24px; height: 24px; background: #d1e9ff"
                    >
                      <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                        {{ data?.user_nick_name_py }}
                      </el-text>
                    </el-avatar>
                    <el-avatar
                      v-show="data?.structure_type == 'department'"
                      :src="data?.department_logo"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="data?.structure_type == 'friend' && data?.user_avatar"
                      :src="data?.user_avatar"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="data?.structure_type == 'friend' && !data?.user_avatar"
                      style="width: 24px; height: 24px; background: #d1e9ff"
                    >
                      <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                        {{ data?.user_nick_name_py }}
                      </el-text>
                    </el-avatar>
                    <el-avatar
                      v-show="data?.structure_type == 'user' && data?.user_avatar"
                      :src="data?.user_avatar"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="data?.structure_type == 'user' && !data?.user_avatar"
                      style="width: 24px; height: 24px; background: #d1e9ff"
                    >
                      <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                        {{ data?.user_nick_name_py }}
                      </el-text>
                    </el-avatar>
                  </div>
                  <div>
                    <el-text>{{ node.data.label }}</el-text>
                  </div>
                </div>
              </template>
            </el-tree>

            <el-tree
              v-show="currentModel == 'search'"
              ref="currentShareSearchRef"
              :data="currentSearchResult"
              :lazy="true"
              :load="getCompanyStructureTree"
              :props="props"
              :highlight-current="true"
              node-key="structure_id"
              :show-checkbox="true"
              :check-strictly="true"
              :expand-on-click-node="true"
              @check="updateLeftSearchCnt"
            >
              <template #default="{ node, data }">
                <div class="tree-button">
                  <div class="std-middle-box">
                    <el-avatar
                      v-show="data?.structure_type == 'colleague' && data?.user_avatar"
                      :src="data?.user_avatar"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="data?.structure_type == 'colleague' && !data?.user_avatar"
                      style="width: 24px; height: 24px; background: #d1e9ff"
                    >
                      <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                        {{ data?.user_nick_name_py }}
                      </el-text>
                    </el-avatar>
                    <el-avatar
                      v-show="data?.structure_type == 'department'"
                      :src="data?.department_logo"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="data?.structure_type == 'friend' && data?.user_avatar"
                      :src="data?.user_avatar"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="data?.structure_type == 'friend' && !data?.user_avatar"
                      style="width: 24px; height: 24px; background: #d1e9ff"
                    >
                      <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                        {{ data?.user_nick_name_py }}
                      </el-text>
                    </el-avatar>
                  </div>
                  <div>
                    <el-text>{{ node.data.label }}</el-text>
                  </div>
                </div>
              </template>
            </el-tree>
          </el-scrollbar>
        </div>
      </div>

      <div v-if="currentModel == 'tree'" id="selector_middle">
        <el-button
          v-if="!phoneView"
          :icon="ArrowLeft"
          type="primary"
          :disabled="!rightCnt"
          @click="removeGetAccessObject"
        />
        <el-button v-else :icon="ArrowLeft" type="primary" :disabled="!rightCnt" @click="removeGetAccessObject" />

        <el-button
          v-if="!phoneView"
          :icon="ArrowRight"
          type="primary"
          :disabled="!leftCnt"
          style="margin: 0"
          @click="addGetAccessObject"
        />
        <el-button
          v-else
          :icon="ArrowRight"
          type="primary"
          :disabled="!leftCnt"
          style="margin: 0"
          @click="addGetAccessObject"
        />
      </div>
      <div v-else-if="currentModel == 'search'" id="selector_middle">
        <el-button
          v-if="!phoneView"
          :icon="ArrowLeft"
          type="primary"
          :disabled="!rightCnt"
          @click="removeGetAccessObject"
        />
        <el-button v-else :icon="ArrowLeft" type="primary" :disabled="!rightCnt" @click="removeGetAccessObject" />
        <el-button
          v-if="!phoneView"
          :icon="ArrowRight"
          type="primary"
          :disabled="!leftSearchCnt"
          style="margin: 0"
          @click="addGetAccessObjectBySearch"
        />
        <el-button
          v-else
          :icon="ArrowRight"
          type="primary"
          :disabled="!leftSearchCnt"
          style="margin: 0"
          @click="addGetAccessObjectBySearch"
        />
      </div>

      <div id="selector_right">
        <div id="selector_resource_area">
          <div class="resource-header">
            <el-text size="large"> 选中资源 </el-text>
          </div>
          <div class="resource-area">
            <div class="resource-area-box">
              <div class="resource-icon-box">
                <el-image :src="currentShareLLM?.llm_icon" class="resource-icon" />
              </div>
              <div class="resource-name-box">
                <el-text>{{ currentShareLLM?.llm_label }}</el-text>
              </div>
            </div>
          </div>
        </div>
        <div id="selector_right_head">
          <div class="std-middle-box">
            <el-text> 已选择授权对象：{{ getAccessObjectList?.length }} 个 </el-text>
          </div>
          <div class="std-middle-box" style="gap: 6px">
            <div class="std-middle-box">
              <el-text> 批量设置为 </el-text>
            </div>
            <div class="std-middle-box" style="width: 70px">
              <el-select v-model="batchShareAccess" size="small" @change="batchSetShareAccess">
                <el-option
                  v-for="option in accessOptions"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>
            </div>
          </div>
        </div>
        <el-scrollbar>
          <div id="selector_right_body" v-loading="accessLoading" element-loading-text="权限加载中...">
            <div v-for="(accessObject, idx) in getAccessObjectList" :key="idx" class="access-object-area">
              <div class="access-object-area-left">
                <el-checkbox
                  v-model="accessObject.get_access"
                  :disabled="accessObject?.user_id == userInfoStore.userInfo?.user_id || accessObject.disabled"
                  @change="updateRightCnt"
                />
                <div class="std-middle-box">
                  <el-avatar
                    v-show="accessObject?.structure_type == 'colleague' && accessObject?.user_avatar"
                    :src="accessObject?.user_avatar"
                    style="width: 24px; height: 24px; background-color: white"
                  />
                  <el-avatar
                    v-show="accessObject?.structure_type == 'colleague' && !accessObject?.user_avatar"
                    style="width: 24px; height: 24px; background: #d1e9ff"
                  >
                    <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                      {{ accessObject?.user_nick_name_py }}
                    </el-text>
                  </el-avatar>
                  <el-avatar
                    v-show="accessObject?.structure_type == 'company'"
                    :src="accessObject.company_logo"
                    style="width: 24px; height: 24px; background-color: white"
                  />
                  <el-avatar
                    v-show="accessObject?.structure_type == 'department'"
                    :src="accessObject?.department_logo"
                    style="width: 24px; height: 24px; background-color: white"
                  />
                  <el-avatar
                    v-show="accessObject?.structure_type == 'friend' && accessObject?.user_avatar"
                    :src="accessObject?.user_avatar"
                    style="width: 24px; height: 24px; background-color: white"
                  />
                  <el-avatar
                    v-show="accessObject?.structure_type == 'friend' && !accessObject?.user_avatar"
                    style="width: 24px; height: 24px; background: #d1e9ff"
                  >
                    <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                      {{ accessObject?.user_nick_name_py }}
                    </el-text>
                  </el-avatar>
                  <el-avatar
                    v-show="accessObject?.structure_type == 'user' && accessObject?.user_avatar"
                    :src="accessObject?.user_avatar"
                    style="width: 24px; height: 24px; background-color: white"
                  />
                  <el-avatar
                    v-show="accessObject?.structure_type == 'user' && !accessObject?.user_avatar"
                    style="width: 24px; height: 24px; background: #d1e9ff"
                  >
                    <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                      {{ accessObject?.user_nick_name_py }}
                    </el-text>
                  </el-avatar>
                </div>
                <div>
                  <el-text style="max-width: 170px" truncated>{{ accessObject.label }}</el-text>
                </div>
                <el-tooltip v-if="accessObject?.disabled" effect="dark" placement="right">
                  <template #default>
                    <div class="std-middle-box">
                      <el-image src="/images/tooltip.svg" style="width: 16px; height: 16px" />
                    </div>
                  </template>
                  <template #content>
                    <el-text
                      v-if="accessObject?.resource_id && accessObject?.resource_id != currentShareLLM.id"
                      style="color: white; font-size: 12px"
                    >
                      权限来自上层资源
                    </el-text>
                    <el-text
                      v-if="accessObject?.user_id == currentShareLLM.user_id"
                      style="color: white; font-size: 12px"
                    >
                      拥有者
                    </el-text>
                  </template>
                </el-tooltip>
              </div>
              <div class="std-middle-box" style="min-width: 70px">
                <el-select
                  v-model="accessObject.access"
                  size="small"
                  :disabled="accessObject?.user_id == userInfoStore.userInfo?.user_id || accessObject.disabled"
                  @change="args => emits('updateAccessList', getAccessObjectList)"
                >
                  <el-option
                    v-for="option in accessOptions"
                    :key="option.value"
                    :label="option.label"
                    :value="option.value"
                  />
                </el-select>
              </div>
            </div>
          </div>
        </el-scrollbar>
      </div>
    </div>
  </div>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
#share_selector_main {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
  width: 100%;
}
#resource_share_selector {
  border-radius: 5px;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  width: calc(100% - 4px);
  height: calc(100% - 4px);
  gap: 12px;
}
#company_search {
  height: calc(100% - 48px);
  width: calc(100% - 24px);
}
#selector_left {
  width: calc(100% - 26px);
  display: flex;
  flex-direction: column;
  border-radius: 5px;
  padding: 10px;
  border: 1px solid #d0d5dd;
  height: calc(100% - 24px);
}
#selector_middle {
  width: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 12px;
}
#selector_right {
  width: calc(100% - 26px);
  height: calc(100% - 24px);
  display: flex;
  flex-direction: column;
  padding: 10px;
  border: 1px solid #d0d5dd;
  border-radius: 5px;
}

.tree-button {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: flex-start;
  height: 40px;
  width: 100%;
}
:deep(.el-tree-node__content) {
  height: 50px;
}

#resource_share_selector_button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  gap: 16px;
}
#selector_right_head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 30px;
}
#selector_right_body {
  min-width: 350px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: calc(100vh - 360px);
}
.access-object-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  border-radius: 6px;
  padding: 12px;
  justify-content: space-between;
  background-color: #f9fafb;
}
.access-object-area-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
}
#selector_resource_area {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 4px;
  padding: 6px;
  border-radius: 6px;
  background-color: #f9fafb;
  margin-bottom: 4px;
}
.resource-area {
  display: flex;
  flex-direction: row;
  padding: 12px;
  width: calc(100% - 24px);
}
.resource-area-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  padding: 6px;
  background-color: white;
  width: calc(100% - 12px);
  border-radius: 6px;
}
.resource-icon {
  width: 24px;
  height: 24px;
}
@media (width< 768px) {
  #resource_share_selector {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }
  #company_search {
    max-height: 200px;
    width: 100%;
  }
  #selector_right_body {
    max-height: 200px;
    width: 100%;
    min-width: 100%;
  }
  #selector_left {
    padding: 6px;
    width: calc(100% - 14px);
  }
  #selector_right {
    padding: 6px;
    width: calc(100% - 14px);
  }
  #selector_middle {
    flex-direction: row;
  }
}
</style>
