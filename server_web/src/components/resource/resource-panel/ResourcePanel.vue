<script setup lang="ts">
import {Search} from '@element-plus/icons-vue';
import {useSessionStorage} from '@vueuse/core';
import {computed, onMounted, ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {
  current_resource,
  format_resource_size,
  get_resource_icon, show_resource_list
} from '@/components/resource/resource-list/resource_list';
import {
  current_resource_usage,
  current_resource_usage_percent,
  folderInput,
  get_current_resource_usage,
  get_recent_data_count,
  get_resource_data_count,
  handle_search_clear,
  init_my_resource_tree,
  init_share_resource_tree,
  init_upload_manager,
  my_resource_tree_data,
  my_resource_tree_props,
  panel_recent_shortcuts,
  panel_show_my_resources_area,
  panel_show_share_resources_area,
  panel_system_labels,
  panel_width,
  share_resource_tree_data,
  show_upload_button,
  switch_panel,
  upload_file_Ref
} from '@/components/resource/resource-panel/panel';
import {
  current_tag,
  get_system_tag,
  search_rag_enhance,
  search_resource_by_tags
} from '@/components/resource/resource-shortcut/resource_shortcut';
import {
  calculateMD5, calculateSHA256,
  folder_upload_parent_resource,
  get_task_icon,
  prepare_upload_files,
  show_upload_manage_box,
  upload_file_content,
  upload_file_list,
  upload_file_task_list,
  upload_size
} from '@/components/resource/resource-upload/resource-upload';
import ResourceUploadManager from '@/components/resource/resource-upload/ResourceUploadManager.vue';
import {useUserInfoStore} from '@/stores/user-info-store';
import {batch_create_folders, resource_share_get_list, search_resource_object} from "@/api/resource-api";
import {ElMessage, ElNotification, UploadRequestOptions} from 'element-plus';
import type Node from 'element-plus/es/components/tree/src/model/node';
import {show_upload_folder_dialog} from "@/components/resource/resource_tree/resource_tree";
import {
  current_resource_tags,
  current_resource_types,
  show_search_config_area
} from "@/components/resource/resource-shortcut/resource_shortcut_head/resource_shortcut_head";
import {show_share_resources} from "@/components/resource/resource-share/share_resources";
import {IResourceItem, IResourceUploadItem} from "@/types/resource-type";
import {v4 as uuidv4} from "uuid";
import ResourcePanelTags from "@/components/resource/resource-panel/ResourcePanelTags.vue";

const userInfoStore = useUserInfoStore();

const router = useRouter();
const route = useRoute();
const isShowResourcePanel = useSessionStorage('isShowResourcePanel', true);
const shareResourceActive = ref(route.name === 'resource_share');
const myResourceActive = ref(route.name === 'resource_list');

interface ITree {
  label: string;
  children?: ITree[];
  leaf?: boolean;
  disabled?: boolean;
  resource_type?: string;
  resource_icon?: string;
  resource_id?: number;
  auth_type?: string;
}
const ragEnhance = ref(true);
const resourceKeyword = ref('');
const resourceProgressStatus = computed(() => {
  if (current_resource_usage_percent.value < 60) {
    return 'success';
  } else if (current_resource_usage_percent.value >= 80 && current_resource_usage_percent.value < 100) {
    return 'warning';
  } else {
    return 'exception';
  }
});
panel_width.value = isShowResourcePanel.value ? '200px' : '0px';

async function getMyResourceTree(node: Node, resolve: (data: ITree[]) => void) {
  // // console.log(node)
  if (node.data.resource_type !== 'folder') {
    return resolve([]);
  }
  if (node.disabled) {
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
          resource_icon: item.resource_icon
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
          resource_icon: item.resource_icon
        });
      }
    }
    console.log(res.result.data.length, res.result.total);
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
    resolve(data);
  }
}
async function handleFolderSelect(event: Event) {
  // 处理文件夹选择
  // @ts-ignore
  let files = event.target?.files;
  // @ts-ignore
  // // console.log(event.target?.files)
  if (!files) {
    ElMessage.error({
      type: 'error',
      message: '文件夹选择失败！'
    });
    return;
  }
  // 检查目标文件夹是否存在
  if (!folder_upload_parent_resource.value) {
    // 打开文件夹选择框
    // console.log('打开文件夹选择框')
    show_upload_folder_dialog(handleFolderSelect, event);
    return;
  }
  // 自动创建所有文件夹
  let folderList = [];
  for (let file of files) {
    if (file.webkitRelativePath) {
      folderList.push({
        path: file.webkitRelativePath,
        size: file.size
      });
    }
  }
  let addFolderParams = {
    resource_list: folderList,
    resource_parent_id: folder_upload_parent_resource.value
  };
  let res = await batch_create_folders(addFolderParams);
  if (!res.error_status) {
    folder_upload_parent_resource.value = null;
  } else {
    ElNotification.error({
      title: '系统通知',
      message: '文件夹创建失败！' + res.error_message,
      duration: 5000
    });
    return;
  }
  // 异步上传所有文件
  // console.log(files)
  for (let file of files) {
    uploadFolderFiles(file, res.result?.[file.webkitRelativePath]);
  }
}
function triggerFolderInput() {
  if (router.currentRoute.value.name == 'resource_list') {
    folder_upload_parent_resource.value = current_resource.id;
  }
  folderInput.value.click();
}
function switchPanel() {
  isShowResourcePanel.value = false;
  switch_panel();
}
async function getShareResourceTree(node: Node, resolve: (data: ITree[]) => void) {
  if (node.data.resource_type !== 'folder') {
    return resolve([]);
  }
  if (node.disabled) {
    return resolve([]);
  }
  let params = {
    resource_parent_id: node.data.resource_id
  };
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
    resolve(data);
  }
}
async function routerToSearchPage() {
  if (window.innerWidth < 768) {
    switch_panel();
  }
  if (!resourceKeyword.value) {
    return;
  }
  // 重新赋值
  if (current_tag.value?.tag_value == 'search') {
    current_tag.value.tag_name = resourceKeyword.value;
  } else {
    current_tag.value = {
      id: null,
      tag_name: resourceKeyword.value,
      tag_value: 'search',
      tag_type: 'search',
      tag_source: 'system',
      tag_desc: null,
      tag_color: null,
      tag_icon: '',
      tag_active: false
    };
  }

  // 系统标签处理
  for (let system_tag of panel_recent_shortcuts.value) {
    system_tag.tag_active = false;
  }
  for (let system_tag of panel_system_labels.value) {
    system_tag.tag_active = false;
  }
  if (router.currentRoute.value.name != 'resource_search') {
    // 资源标签清空
    current_resource_tags.value = [];
    show_search_config_area(false);
    // 资源类型清空
    current_resource_types.value = [
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
    ];
  }
  // 资源标签选中的全部保留
  let userTagIds = [];
  for (let userTag of current_resource_tags.value) {
    userTagIds.push(userTag.id);
  }
  if (userTagIds.length) {
    show_search_config_area(true);
  }

  let resourceTypes = [];
  if (current_resource_types.value?.length != 11) {
    resourceTypes = current_resource_types.value;
  } else {
    resourceTypes = [];
  }

  // 保存当前路径至localstorage
  localStorage.setItem('current_path', router.currentRoute.value.fullPath);

  router.push({
    name: 'resource_search',
    params: {
      tag_source: 'system'
    },
    query: {
      ...router.currentRoute.value.query,
      resource_type: resourceTypes,
      resource_keyword: resourceKeyword.value,
      tag_value: 'search',
      tag_id: userTagIds,
      // @ts-ignore
      rag_enhance: ragEnhance.value
    }
  });
  search_rag_enhance.value = ragEnhance.value;
  await search_resource_by_tags();
  return;
}
async function routerToRecycleBin() {
  if (window.innerWidth < 768) {
    switch_panel();
  }
  // @ts-ignore
  current_tag.value = get_system_tag('recycle_bin');
  // 系统标签处理
  for (let systemTag of panel_recent_shortcuts.value) {
    systemTag.tag_active = false;
  }
  for (let systemTag of panel_system_labels.value) {
    systemTag.tag_active = false;
  }
  // 资源标签选中的全部保留
  let userTagIds = [];
  for (let userTag of current_resource_tags.value) {
    userTagIds.push(userTag.id);
  }
  if (userTagIds.length) {
    show_search_config_area(true);
  }
  current_resource_types.value = [
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
  ];

  router.push({
    name: 'resource_recycle_bin',
    params: {
      tag_source: 'system'
    },
    query: {
      ...router.currentRoute.value.query,
      resource_type: current_resource_types.value,
      tag_value: 'recycle_bin',
      tag_id: userTagIds
    }
  });
  search_resource_by_tags();
}
async function routerToShareResource(item: Node) {
  if (window.innerWidth < 768) {
    switch_panel();
  }
  if (item.data.resource_type == 'folder') {
    await show_share_resources({
      id: item.data.resource_id,
      resource_type: item.data.resource_type
    } as IResourceItem);
  } else {
    router.push({
      name: 'resource_viewer',
      params: {
        resource_id: item.data.resource_id
      }
    });
  }
}
async function uploadFolderFiles(file, parentId: number) {
  // 上传文件夹中的所有文件
  await prepareFolderFile(file, parentId);
  await upload_file_content({
    file: file
  } as UploadRequestOptions);
}
async function prepareFolderFile(uploadFile, parentId) {
  // 正对于新上传的文件，需要进行一些准备工作，然后生成一个上传任务
  // 如果没有选择父资源，那么需要打开资源选择器
  show_upload_manage_box.value = true;
  // 1. 计算文件的MD5值
  let fileSHA256 = '';
  try {
    fileSHA256 = await calculateMD5(uploadFile);
    if (!fileSHA256) {
      fileSHA256 = await calculateSHA256(uploadFile);
    }
  } catch (e) {
    fileSHA256 = await calculateSHA256(uploadFile);
  }
  // 2. 准备参数
  let resourceSize = uploadFile.size / 1024 / 1024;
  let contentMaxIdx = Math.floor(resourceSize / upload_size.value);
  // 前端临时可视化文件类型和格式
  let resourceType = '';
  let resourceFormat = '';
  if (uploadFile.name.indexOf('.') > -1) {
    resourceFormat = uploadFile.name.split('.').pop().toLowerCase();
  }
  resourceType = uploadFile.type;
  let taskIcon = get_task_icon(resourceType, resourceFormat);
  uploadFile.uid = uuidv4();
  let newUploadFileTask = <IResourceUploadItem>{
    id: null,
    resource_parent_id: parentId,
    resource_id: null,
    resource_name: uploadFile.name,
    resource_size_in_mb: resourceSize,
    resource_type: resourceType,
    resource_format: resourceFormat,
    content_max_idx: contentMaxIdx,
    content_finish_idx: -1,
    resource_md5: fileSHA256,
    raw_file: uploadFile,
    task_icon: taskIcon,
    task_status: 'pending'
  };
  upload_file_task_list.value.push(newUploadFileTask);
}
async function routerToResource(item: Node) {
  if (window.innerWidth < 768) {
    switch_panel();
  }
  const userInfoStore = useUserInfoStore();
  if (item.data.resource_type == 'folder') {
    await show_resource_list({
      id: item.data.resource_id,
      user_id: userInfoStore.userInfo.user_id,
      resource_type: item.data.resourceType
    } as IResourceItem);
    return;
  } else {
    router.push({
      name: 'resource_viewer',
      params: {
        resource_id: item.data.resource_id
      }
    });
  }
}

onMounted(async () => {
  get_current_resource_usage();
  get_recent_data_count();
  init_my_resource_tree();
  init_share_resource_tree();
  get_resource_data_count();
  // handle_window_size()
  // window.addEventListener('resize', handle_window_size)
});

watch(
  () => route.name,
  newVal => {
    myResourceActive.value = newVal === 'resource_list';
    shareResourceActive.value = newVal === 'resource_share';
  }
);

defineOptions({
  name: 'ResourcePanel'
});
</script>

<template>
  <div id="resource_panel_box" @contextmenu.prevent>
    <div id="panel_head">
      <div id="panel_head_left">
        <div class="std-middle-box" style="cursor: pointer" @click="switchPanel">
          <el-tooltip :content="$t('closeSidebar')" effect="light">
            <el-image src="/images/layout_alt.svg" style="width: 16px; height: 16px" />
          </el-tooltip>
        </div>
        <div class="std-middle-box" style="width: 200px" @click="router.push({ name: 'resource_list' })">
          <el-text style="font-size: 16px; font-weight: 600; line-height: 24px; color: #101828; cursor: pointer">
            AI资源库
          </el-text>
        </div>
      </div>
      <div id="panel_head_right">
        <el-progress
          :percentage="current_resource_usage_percent"
          :text-inside="true"
          :stroke-width="18"
          style="width: 80%"
          :status="resourceProgressStatus"
        />
        <el-text size="small">
          {{ current_resource_usage }}M/{{ format_resource_size(userInfoStore.userInfo?.user_resource_limit) }}
        </el-text>
      </div>
    </div>
    <div id="panel_face">
      <ResourcePanelTags />
    </div>
    <el-scrollbar>
      <div id="resource_panel_body">
        <div id="my_file">
          <div
            class="resource-router-title"
            :style="{ backgroundColor: myResourceActive || panel_show_my_resources_area ? '#eff8ff' : '#fff' }"
          >
            <div class="resource-router-title-left" @click="router.push({ name: 'resource_list' })">
              <div class="std-middle-box">
                <el-image src="/images/my_resources.svg" style="width: 24px; height: 24px" />
              </div>
              <div class="std-middle-box">
                <el-text style="font-size: 16px; font-weight: 600; line-height: 24px; color: #101828">
                  我的资源
                </el-text>
              </div>
            </div>
            <div class="menu-icon-box" @click="panel_show_my_resources_area = !panel_show_my_resources_area">
              <el-image v-show="panel_show_my_resources_area" src="/images/panel_arrow_down.svg" class="menu-icon" />
              <el-image v-show="!panel_show_my_resources_area" src="/images/panel_arrow_up.svg" class="menu-icon" />
            </div>
          </div>

          <div v-show="panel_show_my_resources_area">
            <el-tree
              ref="resource_tree_Ref"
              :data="my_resource_tree_data"
              :lazy="true"
              :load="getMyResourceTree"
              :props="my_resource_tree_props"
              :expand-on-click-node="false"
              :check-strictly="true"
              :highlight-current="true"
            >
              <template #default="{ node }">
                <div
                  style="
                    display: flex;
                    flex-direction: row;
                    gap: 6px;
                    width: 100%;
                    align-items: center;
                    justify-content: flex-start;
                  "
                  @click="routerToResource(node)"
                >
                  <div>
                    <el-image :src="get_resource_icon(node.data)" style="width: 12px; height: 12px" />
                  </div>
                  <div>
                    <el-text style="max-width: 320px" truncated>{{ node.data.label }}</el-text>
                  </div>
                </div>
              </template>
            </el-tree>
          </div>
        </div>

        <div id="my_share">
          <div
            class="resource-router-title"
            :style="{ backgroundColor: shareResourceActive || panel_show_share_resources_area ? '#eff8ff' : '#fff' }"
          >
            <div class="resource-router-title-left" @click="routerToShareResource">
              <div class="std-middle-box">
                <el-image src="/images/share_resources.svg" style="width: 24px; height: 24px" />
              </div>
              <div class="std-middle-box">
                <el-text style="font-size: 16px; font-weight: 600; line-height: 24px; color: #101828">
                  共享资源
                </el-text>
              </div>
            </div>
            <div class="menu-icon-box" @click="panel_show_share_resources_area = !panel_show_share_resources_area">
              <el-image v-show="panel_show_share_resources_area" class="menu-icon" src="/images/panel_arrow_down.svg" />
              <el-image v-show="!panel_show_share_resources_area" class="menu-icon" src="/images/panel_arrow_up.svg" />
            </div>
          </div>
          <div v-show="panel_show_share_resources_area">
            <el-scrollbar>
              <el-tree
                ref="share_resource_tree_Ref"
                :data="share_resource_tree_data"
                :lazy="true"
                :load="getShareResourceTree"
                :props="my_resource_tree_props"
                :expand-on-click-node="false"
                :check-strictly="true"
                :highlight-current="true"
              >
                <template #default="{ node }">
                  <div
                    style="
                      display: flex;
                      flex-direction: row;
                      gap: 6px;
                      width: 100%;
                      align-items: center;
                      justify-content: flex-start;
                    "
                    @click="routerToShareResource(node)"
                  >
                    <div>
                      <el-image :src="get_resource_icon(node.data)" style="width: 12px; height: 12px" />
                    </div>
                    <div>
                      <el-text style="max-width: 320px" truncated>{{ node.data.label }}</el-text>
                    </div>
                  </div>
                </template>
              </el-tree>
            </el-scrollbar>
          </div>
        </div>
      </div>
    </el-scrollbar>

    <div id="panel_foot">
      <div id="panel_foot_head">
        <div id="resource_search" style="min-width: 100px">
          <el-input
            v-model="resourceKeyword"
            placeholder="资源搜索"
            clearable
            @clear="handle_search_clear"
            @change="
              val => {
                if (val == '') {
                  handle_search_clear();
                } else {
                  routerToSearchPage();
                }
              }
            "
            @keydown.enter="routerToSearchPage"
          >
            <template #prefix>
              <el-icon style="cursor: pointer" @click="routerToSearchPage">
                <Search />
              </el-icon>
            </template>
          </el-input>
        </div>
        <el-popover ref="show_upload_button" trigger="click" width="160px">
          <template #reference>
            <div id="panel_upload_button">
              <div class="std-middle-box">
                <el-image src="/images/upload_white.svg" style="width: 20px; height: 20px" />
              </div>
              <div class="std-middle-box">
                <el-text style="color: white; font-weight: 600; line-height: 20px; font-size: 14px">上传</el-text>
              </div>
            </div>
          </template>

          <template #default>
            <div id="upload-method-area">
              <el-upload
                ref="upload_file_Ref"
                v-model:file-list="upload_file_list"
                multiple
                :show-file-list="false"
                :auto-upload="true"
                name="chunk_content"
                :before-upload="prepare_upload_files"
                :on-change="init_upload_manager"
                :http-request="upload_file_content"
                :disabled="current_resource_usage_percent >= 100"
                accept="*"
                action=""
              >
                <div class="upload-method-button">
                  <div class="std-middle-box">
                    <el-image src="/images/upload_local.svg" style="width: 20px; height: 20px" />
                  </div>
                  <div class="std-middle-box">
                    <el-text style="width: 90px">上传本地资源</el-text>
                  </div>
                </div>
              </el-upload>

              <div class="upload-method-button" @click="triggerFolderInput">
                <div class="std-middle-box">
                  <el-image src="/images/upload_local_dir.svg" style="width: 20px; height: 20px" />
                </div>
                <div class="std-middle-box">
                  <el-text style="width: 80px">上传文件夹</el-text>
                </div>
                <div class="std-middle-box">
                  <input
                    ref="folderInput"
                    type="file"
                    webkitdirectory
                    style="display: none"
                    @change="handleFolderSelect"
                  />
                </div>
              </div>
            </div>
          </template>
        </el-popover>
      </div>
      <div id="panel_foot_body">
        <div v-if="false" class="panel_foot_button" style="border-right: 1px solid #d0d5dd">
          <div class="std-middle-box">
            <el-image src="/images/storage_manager.svg" style="width: 24px; height: 24px" />
          </div>
          <div class="std-middle-box">
            <el-text>存储管理</el-text>
          </div>
        </div>
        <div class="panel_foot_button" @click="routerToRecycleBin">
          <div class="std-middle-box">
            <el-image src="/images/trash_area.svg" style="width: 24px; height: 24px" />
          </div>
          <div class="std-middle-box">
            <el-text>回收站</el-text>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div id="resource_upload_manage_box">
    <ResourceUploadManager />
  </div>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
}
#resource_panel_box {
  height: 100vh;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 8px -2px #1018281a;
  gap: 4px;
  width: calc(100% - 2px);
}
#resource_panel_body {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: calc(100% - 520px);
  gap: 4px;
}
#panel_head {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 7px;
  box-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.1);
}
#panel_head_left {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: flex-start;
  gap: 4px;
  min-width: 84px;
}
#panel_head_right {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: center;
  width: 100%;
}
#panel_face {
  display: flex;
  flex-direction: column;
  padding: 8px 12px;
  gap: 12px;
}
#panel_recent_area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
#panel_recent_head {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  width: 100%;
  padding: 4px 0;
}
#panel_recent_body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
}
.recent-shortcut {
  width: calc(100% - 16px);
  display: flex;
  flex-direction: row;
  padding: 4px 8px;
  align-items: center;
  justify-content: space-between;
  border-radius: 6px;
  cursor: pointer;
}
.recent-shortcut:hover {
  background-color: #eff8ff;
}
.recent-shortcut-active {
  background-color: #eff8ff;
}
.recent-shortcut-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.recent-shortcut-cnt {
  border: 1px solid #1570ef;
  padding: 0 8px;
  border-radius: 16px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
#panel_label_head_buttons {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  width: 100%;
}
.panel_label_head_button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
#panel_label_body {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 8px;
  width: 100%;
}
#system_label_area {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 4px;
}
.system-label {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px;
  border-radius: 6px;
  gap: 8px;
  cursor: pointer;
}
.system-label:hover {
  background: #eff8ff;
}
.system-label-active {
  background: #eff8ff;
}

#user_label_area {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  gap: 4px;
  max-height: 250px;
}
.user-label {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px;
  border-radius: 6px;
  gap: 8px;
  cursor: pointer;
}
.user-label-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.user-label:hover {
  background: #eff8ff;
}
.user-label-active {
  background: #eff8ff;
}
.user-label-color {
  width: 12px;
  height: 12px;
  border-radius: 12px;
}

#panel_label_foot {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  padding: 4px 8px;
  border-radius: 8px;
  width: calc(100% - 16px);
  opacity: 0.8;
}
.show-all-button {
  cursor: pointer;
  color: #344054;
  line-height: 20px;
  font-weight: 400;
  font-size: 14px;
}
.show-all-button:hover {
  color: #1570ef;
}

#my_file {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: calc(100% - 16px);
  padding: 0 8px;
}
.resource-router-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  width: calc(100% - 16px);
  flex-direction: row;
  background: #eff8ff;
  cursor: pointer;
  border-radius: 6px;
}
.resource-router-title-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  width: 100%;
}
#my_share {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: calc(100% - 16px);
  padding: 0 8px;
}
#my_favourite {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: calc(100% - 16px);
  padding: 0 8px;
}

.menu-icon-box {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.menu-icon {
  width: 16px;
  height: 16px;
}
#panel_foot {
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 160px;
  justify-content: flex-end;
}
#panel_foot_head {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 6px 8px;
  width: calc(100% - 16px);
}
#panel_upload_button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background: #1570ef;
  box-shadow: 0 1px 2px 0 #1018280d;
  padding: 6px 12px;
  gap: 8px;
  width: calc(100% - 24px);
  border-radius: 6px;
  cursor: pointer;
}
#upload-method-area {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 8px;
  align-items: flex-start;
}
.upload-method-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  padding: 2px 8px;
  gap: 8px;
  width: calc(100% - 16px);
  cursor: pointer;
}
.upload-method-button:hover {
  background: #eff8ff;
  border-radius: 8px;
}

#panel_foot_body {
  padding: 8px 12px;
  border-top: 1px solid #d0d5dd;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 36px;
}
.panel_foot_button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  width: 100%;
}
.user-label-color {
  width: 12px;
  height: 12px;
  border-radius: 12px;
}
.user-tag-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  padding: 2px 6px;
  width: 160px;
}
#resource_upload_manage_box {
  position: fixed;
  right: 20px;
  bottom: 100px;
  z-index: 999;
}
</style>
