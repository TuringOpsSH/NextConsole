<script setup lang="ts">
import {useSessionStorage} from '@vueuse/core';
import {ElMessage} from 'element-plus';
import {saveAs} from 'file-saver'; // 使用FileSaver.js
import {storeToRefs} from 'pinia';
import {computed, nextTick, onBeforeUnmount, onMounted, provide, reactive, ref, watch} from 'vue';
import {onBeforeRouteLeave, useRoute} from 'vue-router';
import {
  batch_download_resources, delete_resource_object_api,
  resource_share_get_list,
  resource_share_get_meta,
  searchByKeywordInResource
} from '@/api/resource-api';
import ResourceEmpty from '@/components/resource/ResourceEmpty.vue';
import ResourceDetail from '@/components/resource/resource-detail/index.vue';
import {
  format_resource_size,
  get_resource_icon,
  share_resource,
  sort_resource_size,
  sort_resource_status
} from '@/components/resource/resource-list/resource-list';
import ResourceHead from '@/components/resource/resource-share/ResourceHead.vue';
import ContextMenu from '@/components/resource/resource-share/context_menu/ContextMenu.vue';
import {
  openCardContextMenu,
  openContextMenu,
  openTableContextMenu,
  resource_share_context_menu_flag,
  setCurrentRowItem
} from '@/components/resource/resource-share/context_menu/context-menu';
import ResourceShareSelector from '@/components/resource/resource-share-selector/resource_share_selector.vue';
import ResourceMeta from '@/components/resource/resource_meta/resource_meta.vue';
import ResourceViewTree from '@/components/resource/resource_tree/ResourceViewTree.vue';
import {downloadResource} from "@/components/resource/utils/common";
import router from '@/router';
import {useShareResourceStore} from '@/stores/resourceShareStore';
import {IResourceItem, ISearchByKeywordParams, TResourceListStatus} from '@/types/resource-type';
import { sortShareResourceList } from '@/utils/common';

const props = defineProps({
  resourceId: {
    type: String,
    default: null,
    required: false
  }
});
const resourceViewModel = ref('list');
const resourceShareListCardButtonsRef = ref();
const currentPageNum = ref(1);
const currentPageSize = ref(50);
const elScrollbarRef = ref(null);
const { isSearchMode, isLoading } = storeToRefs(useShareResourceStore());
const shareListStatus = useSessionStorage<TResourceListStatus>('shareListStatus', 'card');
const showCardList = computed(() => {
  return shareListStatus.value === 'card';
});
const hidePermission = useSessionStorage('hideShareResourcePermission', false);
const keyword = ref('');
const route = useRoute();
const resourceId = ref(props.resourceId);
const resourceListScrollRef = ref(null);
const resourceCardScrollRef = ref(null);
const multipleSelection = ref<IResourceItem[]>([]);
const currentResourceId = useSessionStorage('currentResourceId', '');
const isMultipleSelection = computed(() => {
  return multipleSelection.value.length > 1;
});
const currentShareResource = reactive<IResourceItem>(
  // @ts-ignore
  {
    sub_rag_file_cnt: 0,
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
    resource_feature_code: '',
    resource_is_supported: false,
    resource_show_url: '',
    resource_source_url: '',
    resource_title: '',
    resource_source: 'resource_center',
    ref_text: null,
    rerank_score: null
  }
);
const currentTotal = ref(0);
const resourceShareListRef = ref();
const showMultipleButton = ref(false);
const shareResourceLoading = ref(false);
const shareResourceList = ref<IResourceItem[]>([]);
function closeMenu(event) {
  // 关闭菜单
  if (
    event.target.id !== 'resource_list_menu_box' &&
    event.target.id !== 'resource_shortcut_menu_box' &&
    event.target.id !== 'resource_share_menu_box'
  ) {
    resource_share_context_menu_flag.value = false;
  }
}

async function getCurrentShareResource(resourceId: string | number | null = null) {
  if (!resourceId) {
    return;
  }
  let params = {
    resource_id: resourceId
  };
  let res = await resource_share_get_meta(params);
  if (!res.error_status) {
    Object.assign(currentShareResource, res.result);
  }
}

async function searchNextResourceShareObject(scrollPosition: object) {
  if (shareResourceLoading.value) {
    console.log('资源正在加载中');
    return;
  }
  if (currentTotal.value && currentTotal.value <= shareResourceList.value.length) {
    return;
  }
  if (resourceViewModel.value == 'card') {
    // @ts-ignore
    if (scrollPosition.scrollTop + window.innerHeight - 120 > resourceCardScrollRef.value.clientHeight - 10) {
      // 下一页
      currentPageNum.value += 1;
      let searchParams = {
        resource_parent_id: currentShareResource.id,
        page_num: currentPageNum.value,
        page_size: currentPageSize.value
      };
      shareResourceLoading.value = true;
      let res = await resource_share_get_list(searchParams);
      if (!res.error_status) {
        currentTotal.value = res.result.total;

        for (let resource of res.result.data) {
          // 去重添加
          let findFlag = false;
          for (let item of shareResourceList.value) {
            if (item.id == resource.resource.id) {
              findFlag = true;
              break;
            }
          }
          if (!findFlag) {
            shareResourceList.value.push({ ...resource.resource, auth_type: resource.auth_type });
          }
        }
      }
      // @ts-ignore
      elScrollbarRef.value.setScrollTop(scrollPosition.scrollTop - 20);
      shareResourceLoading.value = false;
    }
  } else if (resourceViewModel.value == 'list') {
    // @ts-ignore
    if (
      Math.floor(scrollPosition.scrollTop + window.innerHeight - 128) >
      resourceListScrollRef.value.clientHeight - 10
    ) {
      // 下一页
      currentPageNum.value += 1;
      let searchParams = {
        resource_parent_id: currentShareResource.id,
        page_num: currentPageNum.value,
        page_size: currentPageSize.value
      };
      shareResourceLoading.value = true;
      let res = await resource_share_get_list(searchParams);
      if (!res.error_status) {
        currentTotal.value = res.result.total;
        for (let resource of res.result.data) {
          // 去重添加
          let findFlag = false;
          for (let item of shareResourceList.value) {
            if (item.id == resource.resource.id) {
              findFlag = true;
              break;
            }
          }
          if (!findFlag) {
            shareResourceList.value.push({ ...resource.resource, auth_type: resource.auth_type });
          }
        }
      }
      // 往上滚动防止连续加载
      // @ts-ignore
      elScrollbarRef.value.setScrollTop(scrollPosition.scrollTop - 20);
      shareResourceLoading.value = false;
    }
  }
}

async function doubleClickResourceCard(resource: IResourceItem) {
  // 双击资源列表中的某一行触发
  if (resource.resource_type === 'folder') {
    showShareResources(resource);
  } else {
    previewShareResource(resource);
  }
}

async function handleSearch() {
  if (keyword.value === '') {
    // ElMessage({
    //   message: '关键字不能为空',
    //   type: 'warning'
    // });
    return;
  }
  isSearchMode.value = true;
  const params: ISearchByKeywordParams = {
    resource_keyword: keyword.value.trim(),
    resource_id: resourceId.value as number
  };
  await searchAllResourceShareObject(params);
}

function handleClear() {
  isSearchMode.value = false;
  keyword.value = '';
}

function clickResourceCard(resource: IResourceItem, event: MouseEvent) {
  // 如果点击的是多选框，则不触发单击事件
  if ((event.target as HTMLElement).closest('.resource-item-card-body-button')) {
    return;
  }
  resource.resource_is_selected = !resource.resource_is_selected;
  let selectedCnt = 0;
  for (let item of shareResourceList.value) {
    if (item.resource_is_selected) {
      selectedCnt += 1;
    }
  }
  if (selectedCnt > 0) {
    showMultipleButton.value = true;
  }
  // 保证multipleSelection 的顺序来更新
  if (resource.resource_is_selected) {
    multipleSelection.value.push(resource);
  } else {
    let index = multipleSelection.value.findIndex(item => item.id == resource.id);
    multipleSelection.value.splice(index, 1);
  }
  // 同步到列表视图
  resourceShareListRef.value?.toggleRowSelection(resource);
  nextTick(() => {
    currentResourceId.value = multipleSelection.value.at(-1)?.id.toString() ?? '';
  });
}

function loadMoreResource(e: Event) {
  if (shareResourceList.value.length === 0) {
    return;
  }
  searchNextResourceShareObject(e);
}

async function handleDownLoad(data) {
  for (const item of data) {
    const response = await fetch(item.download_url);
    const blob = new Blob([await response.arrayBuffer()], {
      type: 'application/octet-stream' // 明确为二进制流
    });
    saveAs(blob, encodeURIComponent(item.resource_name));
  }
}

async function batchDownloadSelectResource() {
  const params = {
    resource_list: []
  };

  for (const item of shareResourceList.value) {
    if (item.id && item.resource_is_selected) {
      params.resource_list.push(item.id);
    }
  }
  if (params.resource_list.length === 0) {
    ElMessage.warning('请先选择要下载的资源！');
    return;
  }
  shareResourceLoading.value = true;
  let res = await batch_download_resources(params);
  shareResourceLoading.value = false;
  if (!res.error_status) {
    if (!res.result?.length) {
      ElMessage.info('无可下载资源,请检查资源对应权限!');
      return;
    }
    ElMessage.success('批量下载启动成功！');
    await handleDownLoad(res.result);
  }
}

function cancelMultipleSelection() {
  currentResourceId.value = (route.params.resourceId ) ?? null;
  showMultipleButton.value = false;
  for (let item of multipleSelection.value) {
    item.resource_is_selected = false;
  }
  multipleSelection.value = [];
  resourceShareListRef.value?.clearSelection();
}

function batchShare() {
  let selectedResources = [];
  for (let resource of multipleSelection.value) {
    if (resource.resource_is_selected && resource.id) {
      selectedResources.push(resource);
    }
  }
  if (!selectedResources.length) {
    ElMessage.warning('请先选择要分享的资源!');
    return;
  }
  share_resource(selectedResources[0]);
  if (selectedResources.length > 1) {
    ElMessage.info('当前仅支持单个资源分享，已为您打开第一个资源的分享窗口!');
  }
}

async function previewShareResource(resource: IResourceItem) {
  // 预览资源

  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除，请恢复后查看!');
    return;
  }
  if (!resource?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_type == 'folder') {
    await showShareResources(resource);
    return;
  }
  await router.push({
    name: 'resource_viewer',
    params: {
      resource_id: resource.id
    },
    query: {
      ...router.currentRoute.value.query
    }
  });
}

async function handleSelectionChange(val: IResourceItem[]) {
  // 多选框选中事件
  currentResourceId.value = val.at(-1)?.id.toString() ?? '';
  setCurrentRowItem(val.at(-1));
  multipleSelection.value = val;
  for (const item of multipleSelection.value) {
    item.resource_is_selected = true;
  }
  const selectIds = val.map(item => item.id);
  shareResourceList.value = shareResourceList.value.map(item => ({
    ...item,
    resource_is_selected: selectIds.includes(item.id)
  }));
  console.log(multipleSelection.value);
}

async function showShareResources(item: IResourceItem | null = null) {
  // 面板跳转
  if (item.resource_type == 'folder') {
    router.push({
      name: 'resourceShare',
      query: {
        ...router.currentRoute.value.query
      },
      params: {
        ...router.currentRoute.value.params,
        resourceId: item?.id
      }
    });
    return;
  }
}

async function searchAllResourceShareObject(params?: ISearchByKeywordParams) {
  const { isLoading } = storeToRefs(useShareResourceStore());
  let searchParams = {
    resource_parent_id: currentShareResource.id > 0 ? currentShareResource.id : null
  };
  shareResourceLoading.value = true;
  isLoading.value = true;
  let res;
  if (params) {
    res = await searchByKeywordInResource(params);
  } else {
    res = await resource_share_get_list(searchParams);
  }
  isLoading.value = false;
  if (!res.error_status) {
    currentTotal.value = res.result.total;
    const {
      result: { data = [] }
    } = res;
    sortShareResourceList(data);
    if (params) {
      shareResourceList.value = data;
    } else {
      shareResourceList.value = data.map(({ resource, auth_type }) => {
        return { ...resource, auth_type };
      });
    }
  }
  resourceShareListRef.value?.clearSelection();
  shareResourceLoading.value = false;
}

function selectAll(isSelectedAll?: boolean) {
  // 全选
  shareResourceList.value = shareResourceList.value.map(item => ({
    ...item,
    resource_is_selected: !isSelectedAll
  }));
  showMultipleButton.value = !showMultipleButton.value;

  if (!isSelectedAll) {
    resourceShareListRef.value?.toggleAllSelection();
  } else {
    resourceShareListRef.value?.clearSelection();
  }
}
async function deleteResource(resource: IResourceItem) {
  if (!resource.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resource.resource_status == '删除') {
    ElMessage.warning('资源已删除!');
    return;
  }
  // 删除资源
  const params = {
    resource_id: resource.id
  };
  const res = await delete_resource_object_api(params);
  if (!res.error_status) {
    ElMessage.success('删除成功!');
    await searchAllResourceShareObject();
  }
}

provide('keyword', keyword);
provide('isMultipleSelection', isMultipleSelection);

watch(keyword, async newValue => {
  if (newValue === '') {
    isSearchMode.value = false;
    await searchAllResourceShareObject();
  }
});

watch(
  () => props.resourceId,
  newVal => {
    resourceId.value = newVal ?? null;
    currentShareResource.id = resourceId.value;
    searchAllResourceShareObject();
  }
);
defineOptions({
  name: 'ShareResources'
});
const isSelectedAll = computed(() => {
  return shareResourceList.value.every(item => item.resource_is_selected);
});
onMounted(async () => {
  if (props.resourceId && props.resourceId !== '0') {
    await getCurrentShareResource(props.resourceId);
  } else {
    currentShareResource.id = -1;
    currentShareResource.resource_name = '共享资源';
  }
  await searchAllResourceShareObject();
  isLoading.value = false;
  document.addEventListener('click', closeMenu);
});
onBeforeUnmount(() => {
  shareResourceList.value = [];
  isLoading.value = true;
  document.removeEventListener('click', closeMenu);
});
onBeforeRouteLeave((to, from, next) => {
  currentPageNum.value = 1;
  currentPageSize.value = 50;
  currentTotal.value = 0;
  next();
});
</script>

<template>
  <el-container>
    <el-header height="60" style="padding: 0 !important">
      <ResourceHead :resource-id="currentShareResource.id" @handle-search="handleSearch" @handle-clear="handleClear" />
    </el-header>
    <el-main style="padding: 2px !important" @contextmenu.prevent="openContextMenu">
      <div
        id="resource_list_main"
        v-loading="isLoading"
        element-loading-text="加载中"
        :style="{ height: 'calc(100vh -  121px)' }"
      >
        <el-scrollbar
          v-if="shareResourceList.length"
          ref="elScrollbarRef"
          style="width: 100%"
          @scroll="loadMoreResource"
        >
          <div v-show="!showCardList" id="list_model" ref="resourceListScrollRef">
            <el-table
              ref="resourceShareListRef"
              :data="shareResourceList"
              :highlight-current-row="true"
              :row-key="row => row.id"
              border
              select-all
              @row-contextmenu="openTableContextMenu"
              @selection-change="handleSelectionChange"
            >
              <el-table-column type="selection" :reserve-selection="true" width="40" class-name="resource-selection" />
              <el-table-column prop="resource_name" label="资源名称" min-width="160" show-overflow-tooltip sortable>
                <template #default="scope">
                  <div class="resource-item-name">
                    <div :id="scope.row.id" class="resource-item-name-drag">
                      <img :id="scope.row.id" :src="get_resource_icon(scope.row)" class="resource-icon" alt="" />
                    </div>
                    <div class="std-box" @click="previewShareResource(scope.row)">
                      <el-text style="cursor: pointer" class="resource-name-text">
                        {{ scope.row.resource_name }}
                      </el-text>
                    </div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="create_time" label="创建时间" min-width="180" sortable />
              <el-table-column prop="resource_type_cn" label="资源类型" min-width="120" sortable />
              <el-table-column prop="resource_format" label="资源格式" min-width="120" sortable />
              <el-table-column
                prop="resource_size"
                label="资源大小"
                min-width="120"
                :sortable="true"
                :sort-method="sort_resource_size"
              >
                <template #default="scope">
                  <el-text v-if="scope.row.resource_type != 'folder'">
                    {{ format_resource_size(scope.row.resource_size_in_MB) }}
                  </el-text>
                  <el-text v-else> - </el-text>
                </template>
              </el-table-column>
              <el-table-column prop="author_info" label="资源作者" min-width="200" sortable>
                <template #default="scope">
                  <div class="std-box">
                    <el-avatar :src="scope.row?.author_info?.user_avatar" style="width: 18px; height: 18px" />
                    <el-text style="font-size: 12px; font-weight: 500; line-height: 18px; color: #475467" truncated>
                      {{ scope.row?.author_info?.user_nick_name }}
                    </el-text>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="resource_status"
                label="索引状态"
                min-width="160"
                sortable
                :sort-method="sort_resource_status"
              >
                <template #default="scope">
                  <div class="std-box">
                    <el-tag v-if="scope.row.ref_status == 'Success'" type="success" round> 索引 </el-tag>
                  </div>
                </template>
              </el-table-column>

              <el-table-column prop="" label="操作" width="60" class-name="resource-selection" fixed="right">
                <template #default="scope">
                  <el-popover ref="resource_list_buttons_Ref" trigger="click" :visible="scope.row?.show_buttons">
                    <template #reference>
                      <el-image src="/images/dot_list_grey.svg" class="resource-icon2" />
                    </template>
                    <div class="resource-button-group">
                      <div class="resource-button">
                        <el-button text class="resource-button" @click="previewShareResource(scope.row)">
                          查看
                        </el-button>
                      </div>
                      <div class="resource-button">
                        <el-button text class="resource-button" @click="downloadResource(scope.row)"> 下载 </el-button>
                      </div>
                      <div class="resource-button">
                        <el-button text class="resource-button" @click="share_resource(scope.row)"> 分享 </el-button>
                      </div>
                      <div class="resource-button">
                        <el-popconfirm
                          confirm-button-type="danger"
                          title="确认删除？可在回收站中找回"
                          @confirm="deleteResource(scope.row)"
                        >
                          <template #reference>
                            <el-button type="danger" text class="resource-button"> 删除 </el-button>
                          </template>
                        </el-popconfirm>
                      </div>
                    </div>
                  </el-popover>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div v-show="showCardList" id="card-model" ref="resourceCardScrollRef">
            <div
              v-for="item in shareResourceList"
              :id="item.id.toString()"
              :key="item.id"
              draggable="true"
              class="resource-item-card"
              :class="{ resource_selected: item.resource_is_selected }"
              @click="clickResourceCard(item, $event)"
              @contextmenu.prevent="openCardContextMenu(item, $event)"
              @dblclick="doubleClickResourceCard(item)"
            >
              <div :id="item.id.toString()" class="resource-item-card-head">
                <div :id="item.id.toString()" class="resource-item-card-icon">
                  <el-image :id="item.id.toString()" :src="get_resource_icon(item)" class="resource-card-icon" />
                </div>
                <div :id="item.id.toString()" class="resource-item-select">
                  <el-checkbox v-model="item.resource_is_selected" @click.prevent />
                </div>
              </div>
              <div :id="item.id.toString()" class="resource-item-card-body card-panel">
                <div class="resource-item-card-panel">
                  <div :id="item.id.toString()" class="std-middle-box">
                    <el-image
                      :id="item.id.toString()"
                      :src="get_resource_icon(item)"
                      style="width: 40px; height: 40px"
                    />
                  </div>
                  <div :id="item.id.toString()" class="std-middle-box">
                    <el-text :id="item.id.toString()" class="card-title" truncated style="width: 140px">
                      {{ item.resource_name }}
                    </el-text>
                  </div>
                </div>
                <div class="resource-item-card-panel">
                  <div class="resource-item-card-body-button">
                    <el-popover ref="resourceShareListCardButtonsRef" trigger="click" :hide-after="0">
                      <template #reference>
                        <el-image src="/images/dot_list_grey.svg" class="resource-icon2" />
                      </template>
                      <div class="resource-button-group">
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="previewShareResource(item)"> 查看 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="downloadResource(item)"> 下载 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="share_resource(item)"> 分享 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-popconfirm
                            confirm-button-type="danger"
                            title="确认删除？可在回收站中找回"
                            @confirm="deleteResource(item)"
                          >
                            <template #reference>
                              <el-button type="danger" text class="resource-button"> 删除 </el-button>
                            </template>
                          </el-popconfirm>
                        </div>
                      </div>
                    </el-popover>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-scrollbar>
        <div v-if="!shareResourceList?.length && !isLoading" class="std-middle-box" style="width: 100%; height: 100%">
          <ResourceEmpty :is-search-mode="isSearchMode" />
        </div>
        <div v-if="!isLoading" :class="['permission-container', { 'permission-container-hide': hidePermission }]">
          <ResourceDetail />
        </div>
      </div>
    </el-main>
    <el-footer height="60px" style="padding: 0 !important; background-color: #f9fafb">
      <el-scrollbar>
        <div id="resource_footer">
          <div id="resource_foot_left">
            <div class="std-middle-box">
              <el-text style="min-width: 120px"> 当前已经选择{{ multipleSelection.length }}项 </el-text>
            </div>
            <div class="resource-foot-button" @click="batchShare">
              <el-text> 分享 </el-text>
            </div>
          </div>
          <div id="resource_foot_middle">
            <el-popconfirm
              title="您在一段时间内可以下载的共享资源是有限的，确认启用批量下载？"
              @confirm="batchDownloadSelectResource"
            >
              <template #reference>
                <div class="resource-foot-button">
                  <el-text> 下载 </el-text>
                </div>
              </template>
            </el-popconfirm>
          </div>
          <div id="resource_foot_right">
            <div class="resource-foot-button" @click="cancelMultipleSelection">
              <el-text> 取消 </el-text>
            </div>
          </div>
        </div>
        <ResourceMeta />
        <ContextMenu :resource-id="currentShareResource.id" @select-all="selectAll(isSelectedAll)" />
        <ResourceShareSelector />
        <ResourceViewTree />
      </el-scrollbar>
    </el-footer>
  </el-container>
</template>

<style scoped lang="scss">
.std-middle-box {
  display: flex;
  align-items: center;
  justify-content: center;
}
.resource-icon {
  width: 22px;
  height: 22px;
  margin-right: 4px;
}
.resource-icon2 {
  width: 16px;
  height: 16px;
  cursor: pointer;
}
.resource-button-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  justify-content: flex-start;
  align-items: flex-start;
}
#resource_list_main {
  display: flex;
  flex-direction: row;
  width: 100%;
}
#list_model {
  margin-top: 6px;
  width: 100%;
}
#button-area {
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: center;
}
#card-model {
  width: 100%;
  height: calc(100% - 24px);
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 12px 16px;
  box-sizing: border-box;
  margin-bottom: 16px;
}
.resource-item-card {
  display: flex;
  flex-direction: column;
  border: 1px solid #d0d5dd;
  border-radius: 6px;
  width: 240px;
  height: 160px;
  cursor: pointer;
  box-sizing: border-box;
}
.resource-item-card:hover {
  border: 1px solid #1570ef;
}
.resource-item-card-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 8px;
  height: calc(100% - 16px);
  width: calc(100% - 16px);
  background-color: #f8fafc;
  border-radius: 8px 8px 0 0;
  position: relative;
}
.resource_selected {
  border: 1px solid #1570ef;
}
.resource-item-card-icon {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background-color: white;
  width: 100%;
  height: 100%;
  gap: 4px;
}
.resource-item-card-body {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  height: 40px;
  width: calc(100% - 24px);
  padding: 6px 12px;
  border-top: 1px solid #d0d5dd;
  gap: 8px;

  .resource-item-card-panel {
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

.card-panel {
  justify-content: space-between;
}
.std-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  width: 100%;
  overflow: hidden;
}
.card-title {
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  color: #344054;
}
.resource-button {
  width: 100%;
}
.resource-item-name {
  display: flex;
  width: 100%;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  justify-content: flex-start;
}
.resource-item-name-drag {
  display: flex;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  justify-content: flex-start;
  cursor: grab;
  padding: 4px;
  flex: 0;
  box-sizing: border-box;
  padding-right: 20px;
}
:deep(.el-upload-dragger) {
  padding: 24px;
}
.resource-name-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.resource-name-text:hover {
  color: #1570ef;
}
#resource_footer {
  display: flex;
  flex-direction: row;
  min-width: 32px;
  width: calc(100% - 32px);
  height: calc(100% - 16px);
  align-items: center;
  justify-content: space-between;
  background-color: #f9fafb;
  padding: 8px 16px;
  gap: 12px;
}
#resource_foot_left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  width: 100%;
}
.resource-foot-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px; /* 增大内边距，提升点击区域与舒适度 */
  border: 1px solid #d1d5db; /* 微调边框色，更接近现代UI风格 */
  border-radius: 8px; /* 圆角增大，更柔和 */
  background-color: #ffffff;
  color: #374151; /* 明确文字颜色，提升可读性 */
  font-family: 'Inter', system-ui, sans-serif; /* 统一字体 */
  font-size: 14px;
  font-weight: 500; /* 增强文字权重，突出按钮身份 */
  cursor: pointer;
  min-width: 72px; /* 适度增大最小宽度 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06); /* 优化阴影，增强立体感 */
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); /* 平滑过渡所有状态变化 */
  outline: none;

  /* Hover状态：强化反馈 + 色彩协调 */
  &:hover {
    background-color: #e6f0ff;
    border-color: #60a5fa; /* 边框与背景色呼应 */
    color: #1d4ed8; /* 文字颜色加深，提升对比 */
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1); /* 阴影放大，增强悬浮感 */
  }

  /* Active状态：按压反馈（物理感） */
  &:active {
    background-color: #d1e0ff;
    transform: scale(0.98); /* 轻微缩放，模拟按压 */
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1); /* 内阴影，强化凹陷感 */
  }

  /* Focus状态：无障碍支持（键盘导航） */
  &:focus-visible {
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.4); /* 蓝色焦点环，符合WCAG标准 */
    border-color: #3b82f6;
  }

  /* 禁用状态（可选扩展） */
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background-color: #f3f4f6;
    border-color: #e5e7eb;
    color: #9ca3af;
    transform: none;
    box-shadow: none;
  }
}
#resource_foot_middle {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
}
#resource_foot_right {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  width: 100%;
}
.el-table :deep(th.el-table__cell) {
  background-color: #f9fafb;
}

.el-table :deep(.cell) {
  font-size: 12px;
  font-weight: 500;
  line-height: 18px;
  color: #475467;
}
.resource-item-select {
  position: absolute;
  top: 4px;
  right: 16px;
}
.resource-card-icon {
  width: 60px;
  height: 60px;
}
@media (width < 768px) {
  #card-model {
    gap: 6px;
  }
  .resource-item-card {
    border: 1px solid #d0d5dd;
    border-radius: 6px;
    width: 100%;
    height: 60px;
    cursor: pointer;
  }
  .resource-item-card-head {
    display: none;
  }
  .resource_selected {
    border: 1px solid #1570ef;
  }
  .resource-item-card-body {
    border-top: none;
  }
}

.permission-container {
  margin-left: 16px;
  box-shadow: -5px 0 10px -5px rgba(0, 0, 0, 0.1);
  // transition: all 0.5s ease-in-out;
  box-sizing: border-box;
  flex-shrink: 0;
  padding: 16px;
}

#resource_list_main .permission-container-hide {
  width: 0;
  margin-left: 0;
  padding: 0;
}
</style>
