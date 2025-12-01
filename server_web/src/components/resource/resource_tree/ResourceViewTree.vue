<script setup lang="ts">
import type Node from 'element-plus/es/components/tree/src/model/node';
import { reactive, ref } from 'vue';
import { get_resource_icon } from '@/components/resource/resource-list/resource-list';
import {
  resourceUploadTreeData,
  showUploadResourceTree,
  currentCallback
} from '@/components/resource/resource_tree/resource-tree';
import { ElMessage, ElNotification } from 'element-plus';
import {add_resource_object, move_resources, resource_share_get_list, search_resource_object} from '@/api/resource-api';
import { init_my_resource_tree } from '@/components/resource/resource-panel/panel';
import {
  close_upload_manager,
  folder_upload_parent_resource,
  upload_file_task_list
} from '@/components/resource/resource-upload/resource-upload';
import { getInitResource } from '@/components/resource/utils/common';
import { IResourceItem } from '@/types/resource-type';
import {useResourceInfoStore} from "@/stores/resource-info-store";

const dialogWidth = ref(window.innerWidth < 768 ? '90%' : '600px');
const props = {
  isLeaf: 'leaf',
  disable: 'disabled',
  value: 'id'
};
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
  auth_type?: string;
}
const currentTreeRef = ref(null);
const chooseFolderResource = ref(null);
const newResourceDir = reactive<IResourceItem>({
  id: null,
  resource_parent_id: null,
  user_id: null,
  resource_name: null,
  resource_type: null,
  resource_desc: '',
  resource_icon: null,
  resource_format: null,
  ref_status: null,
  // eslint-disable-next-line @typescript-eslint/naming-convention
  resource_size_in_MB: null,
  resource_status: null,
  create_time: null,
  update_time: null,
  delete_time: null,
  show_buttons: null,
  resource_parent_name: null,
  resource_is_selected: null,
  sub_resource_dir_cnt: null,
  sub_resource_file_cnt: null,
  resource_path: '',
  sub_rag_file_cnt: 0,
  resource_show_url: null,
  resource_is_supported: false
});
const addNewDirDialogFlag = ref(false);
const resourceMvTreeRef = ref(null);
const showMvResourceTree = ref(false);
const currentMoveResourceList = ref<number[]>([]);
const resourceMvTreeData = ref<ITree[]>([]);
const mvConfirmFlag = ref(false);
const uploadConfirmFlag = ref(false);
const resourceUploadTreeRef = ref(null);
const uploadFolderConfirmFlag = ref(false);
const folderUploadTreeRef = ref(null);
const folderUploadTreeData = ref<ITree[]>([]);
const showUploadFolderTree = ref(false);
const currentCallbackParams = ref(null);
const resourceInfoStore = useResourceInfoStore();
const loading = ref(false);
const showRagResourceTree = ref(false);
const ragResourceTreeRef = ref(null);
const ragResourceTreeData = ref<ITree[]>([]);
const ragSelectedResourceTree = ref<ITree[]>([]);
function showAddNewDirDialog(currentTreeRef: any) {
  addNewDirDialogFlag.value = true;
  Object.assign(newResourceDir, getInitResource());
  newResourceDir.resource_type = 'folder';
  currentTreeRef.value = currentTreeRef;
}

async function addNewDir() {
  let pickResource = currentTreeRef.value.getCurrentNode();
  let params = {
    resource_name: newResourceDir.resource_name,
    resource_desc: newResourceDir.resource_desc,
    resource_type: 'folder',
    resource_parent_id: pickResource?.resource_id
  };
  let res = await add_resource_object(params);
  if (!res.error_status) {
    addNewDirDialogFlag.value = false;
    // 触发树节点新增
    currentTreeRef.value.append(
      {
        label: res.result.resource_name,
        leaf: true,
        disabled: false,
        resource_id: res.result.id,
        resource_type: res.result.resource_type,
        resource_icon: res.result.resource_icon
      },
      pickResource
    );
  }
}

function mvDoubleCheck() {
  // 如果目标资源不是文件夹，则提醒选择文件夹
  if (chooseFolderResource.value.resource_type !== 'folder') {
    ElNotification({
      title: '系统通知',
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }
  mvConfirmFlag.value = true;
}

async function confirmMvResource() {
  // 确认移动资源

  let params = {
    resource_id_list: currentMoveResourceList.value,
    target_resource_id: chooseFolderResource.value.resource_id
  };

  // 目标文件夹不能在移动资源中
  if (params.resource_id_list.includes(params.target_resource_id)) {
    ElNotification({
      title: '错误',
      message: '不能移动到自身',
      type: 'error'
    });
    return;
  }

  let res = await move_resources(params);
  if (!res.error_status) {
    showMvResourceTree.value = false;
    mvConfirmFlag.value = false;
    ElMessage.success('移动成功');
  }
  if (currentCallback.value) {
    await currentCallback.value();
  }
  init_my_resource_tree();
}

async function cancelUploadResource() {
  showUploadResourceTree.value = false;
  close_upload_manager(false);
}

async function confirmUploadResource() {
  showUploadResourceTree.value = false;
  uploadConfirmFlag.value = false;

  for (let task of upload_file_task_list.value) {
    if (task.resource_parent_id === null && !task.id) {
      task.resource_parent_id = chooseFolderResource.value.resource_id;
    }
  }
  console.log(upload_file_task_list.value, currentCallback.value);
  if (currentCallback.value) {
    console.log(resourceInfoStore.uploadFileList);
    await currentCallback.value(resourceInfoStore.uploadFileList);
  }
}

async function getMoveResourceTree(node: Node, resolve: (data: ITree[]) => void) {
  // 获得下一层目录，并标记叶子节点，不可用目录
  if (node.data.resource_type !== 'folder') {
    return resolve([]);
  }
  if (node.level !== 1 && node.disabled) {
    return resolve([]);
  }
  let params = {
    resource_parent_id: node.data.resource_id
  };
  let res = await search_resource_object(params);
  if (!res.error_status) {
    let data: ITree[] = [];
    for (let item of res.result.data) {
      if (item.resource_type == 'folder') {
        data.push({
          label: item.resource_name,
          leaf: false,
          disabled: false,
          resource_id: item.id,
          resource_type: item.resource_type,
          resource_icon: item.resource_icon,
          resource_parent_id: item.resource_parent_id
        });
        // 目录不能移动到自身
        if (currentMoveResourceList.value.includes(item.id)) {
          data[data.length - 1].disabled = true;
        }
      }
    }
    for (let item of res.result.data) {
      if (item.resource_type != 'folder') {
        data.push({
          label: item.resource_name,
          leaf: true,
          disabled: true,
          resource_id: item.id,
          resource_type: item.resource_type,
          resource_icon: item.resource_icon,
          resource_parent_id: item.resource_parent_id
        });
      }
    }
    resolve(data);
  }
}

async function getUploadResourceTree(node: Node, resolve: (data: ITree[]) => void) {
  // 获得下一层目录，并标记叶子节点，不可用目录
  if (node.data.resource_type !== 'folder') {
    return resolve([]);
  }
  if (node.disabled) {
    return resolve([]);
  }
  let params = {
    resource_parent_id: node.data.resource_id
  };
  if (node.data.resource_source == 'my') {
    let res = await search_resource_object(params);
    if (!res.error_status) {
      let data: ITree[] = [];
      for (let item of res.result.data) {
        if (item.resource_type == 'folder') {
          data.push({
            label: item.resource_name,
            leaf: false,
            disabled: false,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id,
            resource_source: 'my'
          });
        }
      }
      for (let item of res.result.data) {
        if (item.resource_type != 'folder') {
          data.push({
            label: item.resource_name,
            leaf: true,
            disabled: true,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id,
            resource_source: 'my'
          });
        }
      }
      resolve(data);
    }
  } else if (node.data.resource_source == 'share') {
    let res = await resource_share_get_list(params);
    if (!res.error_status) {
      let data: ITree[] = [];
      for (let item of res.result.data) {
        if (item.resource.resource_type == 'folder') {
          data.push({
            label: item.resource.resource_name,
            leaf: false,
            disabled: false,
            resource_id: item.resource.id,
            resource_type: item.resource.resource_type,
            resource_icon: item.resource.resource_icon,
            resource_parent_id: item.resource.resource_parent_id,
            resource_source: 'share',
            auth_type: item.auth_type
          });
        }
      }
      for (let item of res.result.data) {
        if (item.resource.resource_type != 'folder') {
          data.push({
            label: item.resource.resource_name,
            leaf: true,
            disabled: false,
            resource_id: item.resource.id,
            resource_type: item.resource.resource_type,
            resource_icon: item.resource.resource_icon,
            resource_parent_id: item.resource.resource_parent_id,
            resource_source: 'share',
            auth_type: item.auth_type
          });
        }
      }
      if (res.result.data.length < res.result.total) {
        data.push({
          label: '更多请进入目录查看',
          leaf: true,
          disabled: true,
          resource_id: node.data.resource_id,
          resource_type: 'folder',
          resource_icon: '/images/more.svg'
        });
      }
      node.data.access_type = res.result.access_type;
      resolve(data);
    }
  }
}

function uploadDoubleCheck() {
  // 触发上传资源的回调
  if (!chooseFolderResource.value?.resource_id) {
    ElMessage({
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }
  // 如果目标资源不是文件夹，则提醒选择文件夹
  if (chooseFolderResource.value.resource_type !== 'folder') {
    ElMessage({
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }
  // 如果目标资源没有管理权限，则提醒没有权限
  console.log(chooseFolderResource.value);
  if (
    chooseFolderResource.value.auth_type !== 'edit' &&
    chooseFolderResource.value.auth_type !== 'manage' &&
    chooseFolderResource.value.access_type !== 'edit' &&
    chooseFolderResource.value.access_type !== 'manage'
  ) {
    ElMessage({
      message: '您没有该目录的管理权限，无法上传资源',
      type: 'error'
    });
    return;
  }
  uploadConfirmFlag.value = true;

}

function folderUploadDoubleCheck() {
  if (!chooseFolderResource.value?.resource_id) {
    ElMessage({
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }
  // 如果目标资源不是文件夹，则提醒选择文件夹
  if (chooseFolderResource.value.resource_type !== 'folder') {
    ElMessage({
      message: '请选择文件夹',
      type: 'error'
    });
    return;
  }
  console.log(chooseFolderResource.value);
  if (chooseFolderResource.value.auth_type !== 'edit' && chooseFolderResource.value.auth_type !== 'manage') {
    ElMessage.error({
      message: '没有此文件夹的编辑权限！'
    });
    return;
  }
  uploadFolderConfirmFlag.value = true;
}

async function confirmUploadFolder() {
  showUploadFolderTree.value = false;
  uploadFolderConfirmFlag.value = false;
  folder_upload_parent_resource.value = chooseFolderResource.value.resource_id;
  if (currentCallback.value) {
    // 触发回调
    await currentCallback.value(currentCallbackParams.value);
  }
}

async function cancelUploadFolder() {
  showUploadFolderTree.value = false;
  close_upload_manager(false);
}

async function showUploadFolderDialog(callback?: (params?: any) => Promise<void>, params?: any) {
  showUploadFolderTree.value = true;
  // 获取第一层目录
  let res = await search_resource_object({});
  if (!res.error_status) {
    folderUploadTreeData.value = [];
    // 先添加根目录
    if (res.result?.root) {
      folderUploadTreeData.value.push({
        label: res.result.root.resource_name,
        leaf: false,
        disabled: false,
        resource_id: res.result.root.id,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: res.result.root.resource_parent_id,
        resource_source: 'my',
        children: []
      });
      folderUploadTreeData.value.push({
        label: '共享资源',
        leaf: false,
        disabled: false,
        resource_id: null,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: null,
        resource_source: 'share',
        children: []
      });
    }
  }
  currentCallback.value = callback;
  currentCallbackParams.value = params;
  // // console.log('打开文件夹选择框')
}

async function showMoveDialogMultiple(resourceList: number[], callback?: () => Promise<any>) {
  showMvResourceTree.value = true;
  currentMoveResourceList.value = resourceList;
  // 获取第一层目录
  const res = await search_resource_object({});
  if (!res.error_status) {
    resourceMvTreeData.value = [];
    // 先添加根目录
    if (res.result?.root) {
      resourceMvTreeData.value.push({
        label: res.result.root.resource_name,
        leaf: false,
        disabled: false,
        resource_id: res.result.root.id,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: res.result.root.resource_parent_id,
        children: []
      });
      // 目录不能移动到自身
      if (resourceList.includes(res.result.root.id)) {
        resourceMvTreeData.value[resourceMvTreeData.value.length - 1].disabled = true;
      }
      // 先添加目录

      for (const item of res.result.data) {
        if (item.resource_type == 'folder') {
          resourceMvTreeData.value[0].children.push({
            label: item.resource_name,
            leaf: false,
            disabled: false,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id
          });
          // 目录不能移动到自身
          if (resourceList.includes(item.id)) {
            resourceMvTreeData.value[resourceMvTreeData.value.length - 1].disabled = true;
          }
        }
      }
      for (const item of res.result.data) {
        if (item.resource_type != 'folder') {
          resourceMvTreeData.value[0].children.push({
            label: item.resource_name,
            leaf: true,
            disabled: true,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id
          });
        }
      }
    }
  }
  currentCallback.value = callback;
}

async function showRagMultiple() {
  showRagResourceTree.value = true;
  // 获取第一层目录
  let res = await search_resource_object({});
  if (!res.error_status) {
    ragResourceTreeData.value = [];
    // 先添加根目录
    if (res.result?.root) {
      ragResourceTreeData.value.push({
        label: res.result.root.resource_name,
        leaf: false,
        disabled: false,
        resource_id: res.result.root.id,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: res.result.root.resource_parent_id,
        resource_source: 'my',
        children: []
      });
      ragResourceTreeData.value.push({
        label: '共享资源',
        leaf: false,
        disabled: false,
        resource_id: null,
        resource_type: res.result.root.resource_type,
        resource_icon: res.result.root.resource_icon,
        resource_parent_id: null,
        resource_source: 'share',
        children: []
      });
    }
  }
}

async function getRagResourceTree(node: Node, resolve: (data: ITree[]) => void) {
  // 获得下一层目录，并标记叶子节点，不可用目录
  if (node.data.resource_type !== 'folder') {
    return resolve([]);
  }
  if (node.disabled) {
    return resolve([]);
  }
  let params = {
    resource_parent_id: node.data.resource_id
  };
  if (node.data.resource_source == 'my') {
    let res = await search_resource_object(params);
    if (!res.error_status) {
      let data: ITree[] = [];
      for (let item of res.result.data) {
        if (item.resource_type == 'folder') {
          data.push({
            label: item.resource_name,
            leaf: false,
            disabled: false,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id,
            resource_source: 'my'
          });
        }
      }
      for (let item of res.result.data) {
        if (item.resource_type != 'folder') {
          data.push({
            label: item.resource_name,
            leaf: true,
            disabled: false,
            resource_id: item.id,
            resource_type: item.resource_type,
            resource_icon: item.resource_icon,
            resource_parent_id: item.resource_parent_id,
            resource_source: 'my'
          });
        }
      }
      resolve(data);
    }
  } else if (node.data.resource_source == 'share') {
    let res = await resource_share_get_list(params);
    if (!res.error_status) {
      let data: ITree[] = [];
      for (let item of res.result.data) {
        if (item.resource.resource_type == 'folder') {
          data.push({
            label: item.resource.resource_name,
            leaf: false,
            disabled: false,
            resource_id: item.resource.id,
            resource_type: item.resource.resource_type,
            resource_icon: item.resource.resource_icon,
            resource_parent_id: item.resource.resource_parent_id,
            resource_source: 'share',
            auth_type: item.auth_type
          });
        }
      }
      for (let item of res.result.data) {
        if (item.resource.resource_type != 'folder') {
          data.push({
            label: item.resource.resource_name,
            leaf: true,
            disabled: false,
            resource_id: item.resource.id,
            resource_type: item.resource.resource_type,
            resource_icon: item.resource.resource_icon,
            resource_parent_id: item.resource.resource_parent_id,
            resource_source: 'share',
            auth_type: item.auth_type
          });
        }
      }
      if (res.result.data.length < res.result.total) {
        data.push({
          label: '更多请进入目录查看',
          leaf: true,
          disabled: true,
          resource_id: node.data.resource_id,
          resource_type: 'folder',
          resource_icon: '/images/more.svg'
        });
      }
      node.data.access_type = res.result.access_type;
      resolve(data);
    }
  }
}

async function handleRagCheckChange(data: ITree, checked: boolean) {
  if (checked) {
    if (!ragSelectedResourceTree.value.filter(item => item.resource_id == data.resource_id)?.length) {
      data.id = data.resource_id;
      data.resource_name = data.label;
      ragSelectedResourceTree.value.push(data);
    }
  } else {
    ragSelectedResourceTree.value = ragSelectedResourceTree.value.filter(item => item.resource_id != data.resource_id);
  }
}
defineExpose({
  showUploadFolderDialog,
  showMoveDialogMultiple,
  showRagMultiple,
  ragSelectedResourceTree
});
</script>

<template>
  <div>
    <el-dialog
      v-model="showUploadResourceTree"
      title="上传资源至目录"
      draggable
      style="max-width: 700px"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :width="dialogWidth"
    >
      <div id="resource-move-dialog">
        <div id="resource-move-tree">
          <el-scrollbar>
            <el-tree
              ref="resourceUploadTreeRef"
              :data="resourceUploadTreeData"
              :lazy="true"
              :load="getUploadResourceTree"
              :props="props"
              :check-on-click-node="true"
              :check-strictly="true"
              :expand-on-click-node="true"
              :highlight-current="true"
              node-key="resource_id"
              @current-change="a => (chooseFolderResource = a)"
            >
              <template #default="{ node }">
                <div
                  style="display: flex; flex-direction: row; gap: 6px; align-items: center; justify-content: flex-start"
                >
                  <div>
                    <el-image :src="get_resource_icon(node.data)" style="width: 12px; height: 12px" />
                  </div>
                  <div>
                    <el-text>{{ node.data.label }}</el-text>
                  </div>
                </div>
              </template>
            </el-tree>
          </el-scrollbar>
        </div>
        <div id="resource-move-button-box">
          <div>
            <el-button text @click="showAddNewDirDialog(resourceUploadTreeRef)"> 新建目录 </el-button>
          </div>
          <div id="resource-move-button-box">
            <div>
              <el-button text type="primary" @click="uploadDoubleCheck"> 确定 </el-button>
            </div>
            <div>
              <el-button text @click="cancelUploadResource"> 取消 </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
    <el-dialog
      v-model="uploadConfirmFlag"
      title="上传确认"
      draggable
      style="max-width: 700px"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :width="dialogWidth"
    >
      <el-result
        icon="info"
        :title="`是否将选中资源上传至新目录:'${chooseFolderResource.label}'?`"
        sub-title="上传后资源会同步继承父目录的权限"
      />
      <div class="resource-move-button-area">
        <el-button @click="uploadConfirmFlag = false">取消</el-button>
        <el-button type="primary" @click="confirmUploadResource">确认</el-button>
      </div>
    </el-dialog>
    <el-dialog
      v-model="showUploadFolderTree"
      title="上传文件夹"
      draggable
      style="max-width: 700px"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :width="dialogWidth"
    >
      <div id="resource-move-dialog">
        <div id="resource-move-tree">
          <el-scrollbar>
            <el-tree
              ref="folderUploadTreeRef"
              :data="folderUploadTreeData"
              :lazy="true"
              :load="getUploadResourceTree"
              :props="props"
              :check-on-click-node="true"
              :check-strictly="true"
              :expand-on-click-node="true"
              :highlight-current="true"
              node-key="resource_id"
              @current-change="a => (chooseFolderResource = a)"
            >
              <template #default="{ node }">
                <div
                  style="display: flex; flex-direction: row; gap: 6px; align-items: center; justify-content: flex-start"
                >
                  <div>
                    <el-image :src="get_resource_icon(node.data)" style="width: 12px; height: 12px" />
                  </div>
                  <div>
                    <el-text>{{ node.data.label }}</el-text>
                  </div>
                </div>
              </template>
            </el-tree>
          </el-scrollbar>
        </div>
        <div id="resource-move-button-box">
          <div>
            <el-button text @click="showAddNewDirDialog(folderUploadTreeRef)"> 新建目录 </el-button>
          </div>
          <div id="resource-move-button-box">
            <div>
              <el-button text type="primary" @click="folderUploadDoubleCheck"> 确定 </el-button>
            </div>
            <div>
              <el-button text @click="cancelUploadFolder"> 取消 </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
    <el-dialog
      v-model="uploadFolderConfirmFlag"
      title="上传文件夹确认"
      draggable
      style="max-width: 700px"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :width="dialogWidth"
    >
      <el-result
        icon="info"
        :title="`是否将选中资源上传至新目录:'${chooseFolderResource.label}'?`"
        sub-title="上传后资源会同步继承父目录的权限"
      />
      <div class="resource-move-button-area">
        <el-button @click="uploadFolderConfirmFlag = false">取消</el-button>
        <el-button type="primary" @click="confirmUploadFolder">确认</el-button>
      </div>
    </el-dialog>
    <el-dialog
      v-model="showMvResourceTree"
      title="移动资源至新目录"
      draggable
      style="max-width: 700px"
      :width="dialogWidth"
    >
      <div id="resource-move-dialog">
        <div id="resource-move-tree">
          <el-scrollbar>
            <el-tree
              ref="resourceMvTreeRef"
              :data="resourceMvTreeData"
              :lazy="true"
              :load="getMoveResourceTree"
              :props="props"
              :check-on-click-node="true"
              :check-strictly="true"
              :expand-on-click-node="true"
              :highlight-current="true"
              node-key="resource_id"
              @current-change="a => (chooseFolderResource = a)"
            >
              <template #default="{ node }">
                <div
                  style="display: flex; flex-direction: row; gap: 6px; align-items: center; justify-content: flex-start"
                >
                  <div>
                    <el-image :src="get_resource_icon(node.data)" style="width: 12px; height: 12px" />
                  </div>
                  <div>
                    <el-text>{{ node.data.label }}</el-text>
                  </div>
                </div>
              </template>
            </el-tree>
          </el-scrollbar>
        </div>
        <div id="resource-move-button-box">
          <div>
            <el-button text @click="showAddNewDirDialog(resourceMvTreeRef)"> 新建目录 </el-button>
          </div>
          <div id="resource-move-button-box">
            <div>
              <el-button text type="primary" @click="mvDoubleCheck"> 确定 </el-button>
            </div>
            <div>
              <el-button text @click="showMvResourceTree = false"> 取消 </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
    <el-dialog
      v-model="mvConfirmFlag"
      title="移动确认"
      draggable
      style="max-width: 700px"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :width="dialogWidth"
    >
      <div v-loading="loading">
        <el-result
          icon="warning"
          :title="`是否将选中的${currentMoveResourceList.length}个资源移动至新目录:'${chooseFolderResource.label}'?`"
          sub-title="移动后资源会同步继承父目录的权限！"
        />
        <div class="resource-move-button-area">
          <el-button @click="mvConfirmFlag = false">取消</el-button>
          <el-button type="primary" @click="confirmMvResource">确认</el-button>
        </div>
      </div>
    </el-dialog>
    <el-dialog
      v-model="addNewDirDialogFlag"
      title="新增资源目录"
      draggable
      style="max-width: 700px"
      :width="dialogWidth"
    >
      <el-form :model="newResourceDir" label-position="top">
        <el-form-item label="目录名称" required prop="resource_name">
          <el-input v-model="newResourceDir.resource_name" placeholder="请输入目录名称" @keydown.enter.prevent />
        </el-form-item>
        <el-form-item label="目录描述" prop="resource_desc">
          <el-input
            v-model="newResourceDir.resource_desc"
            placeholder="请输入目录描述"
            type="textarea"
            :rows="3"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
        <el-form-item>
          <div class="resource-move-button-area">
            <el-button type="primary" @click="addNewDir">确定</el-button>
            <el-button @click="addNewDirDialogFlag = false">取消</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
    <div v-show="showRagResourceTree" id="resource-move-dialog">
      <div id="resource-move-tree">
        <el-scrollbar>
          <el-tree
            ref="ragResourceTreeRef"
            :data="ragResourceTreeData"
            :lazy="true"
            :load="getRagResourceTree"
            :props="props"
            :check-on-click-node="false"
            :check-strictly="true"
            :expand-on-click-node="true"
            :highlight-current="true"
            node-key="resource_id"
            show-checkbox
            @check-change="handleRagCheckChange"
          >
            <template #default="{ node }">
              <div
                style="display: flex; flex-direction: row; gap: 6px; align-items: center; justify-content: flex-start"
              >
                <div>
                  <el-image :src="get_resource_icon(node.data)" style="width: 12px; height: 12px" />
                </div>
                <div>
                  <el-text>{{ node.data.label }}</el-text>
                </div>
              </div>
            </template>
          </el-tree>
        </el-scrollbar>
      </div>
      <div id="resource-move-button-box">
        <div>
          <el-button text @click="showAddNewDirDialog(folderUploadTreeRef)"> 新建目录 </el-button>
        </div>
        <div id="resource-move-button-box">
          <div>
            <el-button text type="primary" @click="folderUploadDoubleCheck"> 确定 </el-button>
          </div>
          <div>
            <el-button text @click="cancelUploadFolder"> 取消 </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#resource-move-dialog {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  min-height: 300px;
  height: 600px;

  gap: 12px;
}
#resource-move-tree {
  height: 540px;
}
#resource-move-button-box {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  flex-direction: row;
}
.resource-move-button-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
}
</style>
