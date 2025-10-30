<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import { ElMessage, ElNotification } from 'element-plus';
import { storeToRefs } from 'pinia';
import { computed, nextTick, onBeforeUnmount, onMounted, provide, ref } from 'vue';
import { onBeforeRouteLeave, useRoute } from 'vue-router';
import { build_resource_object_ref } from '@/api/resource-api';
import ResourceEmpty from '@/components/resource/ResourceEmpty.vue';
import ResourceDetail from '@/components/resource/resource-detail/index.vue';
import ContextMenu from '@/components/resource/resource-list/resource_context_menu/contextMenu.vue';
import {
  handleDrop,
  openCardContextMenu,
  openContextMenu,
  openTableContextMenu,
  resource_list_context_menu_flag
} from '@/components/resource/resource-list/resource_context_menu/context_menu';
import { resource_head_height } from '@/components/resource/resource-list/resource_head/resource_head';
import ResourceHead from '@/components/resource/resource-list/resource_head/resource_head.vue';
import {
  batch_copy_select_resources as batchCopySelectResource,
  batch_delete_resources as batchDeleteResource,
  batch_download_select_resource,
  batch_move_select_resources,
  cancel_multiple_selection,
  click_resource_card,
  current_page_num,
  current_page_size,
  current_resource,
  current_resource_list,
  current_resource_list as currentResourceList,
  current_total,
  delete_dialog_title,
  delete_resource,
  double_click_resource_card,
  download_resource,
  format_resource_size,
  get_current_resource_object,
  get_parent_resource_list,
  get_resource_icon,
  handleDragOver,
  move_resource,
  multiple_selection,
  onDragEnd,
  onDragStart,
  onDropFunction,
  preview_resource,
  rebuild_resource,
  resource_card_scroll_Ref,
  resource_list_buttons_Ref,
  resource_list_card_buttons_Ref,
  resource_list_Ref,
  resource_list_scroll_Ref,
  resourceDetailRef,
  search_all_resource_object,
  search_all_resource_object_next,
  share_resource,
  show_delete_flag,
  sort_resource_size,
  sort_resource_status
} from '@/components/resource/resource-list/resource_list';
import { close_upload_manager as closeUploadManager } from '@/components/resource/resource-upload/resource-upload';
import ResourceMeta from '@/components/resource/resource_meta/resource_meta.vue';
import ResourceShareSelector from '@/components/resource/resource_share_selector/resource_share_selector.vue';
import ResourceViewTree from '@/components/resource/resource_tree/resource_view_tree.vue';
import { useResourceListStore } from '@/stores/resourceListStore';
import { IResourceItem, TResourceListStatus } from '@/types/resource-type';

const resourceListStore = useResourceListStore();
const { isLoading, isSearchMode } = storeToRefs(resourceListStore);
const dialogWidth = ref(window.innerWidth < 768 ? '90%' : '600px');
const hidePermission = useSessionStorage('hideResourcePermission', false);
const currentResourceId = useSessionStorage('currentResourceId', '');
const route = useRoute();
const multipleSelection = computed(() => {
  return currentResourceList.value.filter(item => item.resource_is_selected);
});
const isMultipleSelection = computed(() => {
  return multipleSelection.value.length > 1;
});
const resourceListStatus = useSessionStorage<TResourceListStatus>('resourceListStatus', 'card');
const showCardList = computed(() => {
  return resourceListStatus.value === 'card';
});
const props = defineProps({
  resource_id: {
    type: String,
    default: '',
    required: false
  }
});

provide('isMultipleSelection', isMultipleSelection);

onMounted(async () => {
  await get_current_resource_object(props.resource_id);
  // 获取当前目录下的资源列表
  await search_all_resource_object();
  // 获取当前目录的父目录用于导航栏
  get_parent_resource_list();
  isLoading.value = false;
  document.addEventListener('click', closeMenu);
});
onBeforeUnmount(() => {
  currentResourceList.value = [];
  document.removeEventListener('click', closeMenu);
  isLoading.value = true;
});
onBeforeRouteLeave((to, from, next) => {
  closeUploadManager();
  current_resource.id = null;
  multiple_selection.value = [];
  current_page_num.value = 1;
  current_page_size.value = 50;
  current_total.value = 0;
  next();
});
function clickResourceCard(item: IResourceItem, event: MouseEvent) {
  click_resource_card(item, event);
  nextTick(() => {
    currentResourceId.value = multipleSelection.value.at(-1)?.id.toString() ?? '';
  });
}
function cancelMultipleSelection() {
  currentResourceId.value = (route.params.resource_id as string) ?? '';
  cancel_multiple_selection();
}
function loadMoreResource(e: Event) {
  if (currentResourceList.value.length === 0) {
    return;
  }
  search_all_resource_object_next(e);
}
function getResourceRagStatus(resource) {
  if (!resource.rag_status) {
    return 'info';
  }
  if (resource.rag_status === '成功') {
    return 'success';
  }
  if (resource.rag_status === '失败') {
    return 'warning';
  }
  if (resource.rag_status === '异常') {
    return 'danger';
  }
  return 'primary';
}
async function batchRebuild() {
  // 批量重建
  let params = {
    resource_list: []
  };
  if (showCardList.value) {
    for (let item of current_resource_list.value) {
      if (item?.id && item.resource_status == '正常' && item?.resource_is_selected) {
        params.resource_list.push(item.id);
      }
    }
  } else {
    for (let item of multiple_selection.value) {
      if (item?.id && item.resource_status == '正常') {
        params.resource_list.push(item.id);
      }
    }
  }

  if (!params.resource_list.length) {
    ElMessage.warning('所选资源无法构建索引!');
    return;
  }
  let res = await build_resource_object_ref(params);
  if (!res.error_status) {
    let taskCnt = res.result.build_cnt;
    ElNotification({
      title: '系统通知',
      message: `共成功提交${taskCnt}个重新构建任务，请耐心等待!`,
      type: 'success',
      duration: 5000
    });
  }
}
async function handleSelectionChange(val: IResourceItem[]) {
  // 多选框选中事件
  // multiple_selection.value = val;
  // show_multiple_button.value = !!val.length;
  // for (let item of val) {
  //   item.resource_is_selected = true;
  // }
  currentResourceId.value = val.at(-1)?.id.toString() ?? '';
  current_resource_list.value = current_resource_list.value.map(item => ({
    ...item,
    resource_is_selected: val.some(selectedItem => selectedItem.id === item.id)
  }));
}
function closeMenu(event) {
  // 关闭菜单
  if (
    event.target.id !== 'resource_list_menu_box' &&
    event.target.id !== 'resource_shortcut_menu_box' &&
    event.target.id !== 'resource_share_menu_box'
  ) {
    resource_list_context_menu_flag.value = false;
  }
}
</script>

<template>
  <el-container>
    <el-header :height="resource_head_height + 'px'" style="padding: 0 !important">
      <ResourceHead />
    </el-header>
    <el-main style="padding: 2px !important" @contextmenu.prevent="openContextMenu">
      <div
        id="resource_list_main"
        v-loading="isLoading"
        :style="{ height: 'calc(100vh - 61px - ' + resource_head_height + 'px)' }"
        element-loading-text="加载中"
        @dragover.prevent="handleDragOver"
        @drop.prevent="handleDrop"
      >
        <el-scrollbar
          v-if="currentResourceList.length"
          ref="elScrollbarRef"
          style="width: 100%"
          @scroll="loadMoreResource"
        >
          <div class="resource_list_main_content">
            <div v-show="!showCardList" id="list_model" ref="resource_list_scroll_Ref">
              <el-table
                ref="resource_list_Ref"
                border
                :row-key="row => row.id"
                :data="currentResourceList"
                :highlight-current-row="true"
                select-all
                @row-contextmenu="openTableContextMenu"
                @selection-change="handleSelectionChange"
              >
                <el-table-column
                  type="selection"
                  :reserve-selection="true"
                  width="40"
                  class-name="resource-selection"
                />
                <el-table-column prop="resource_name" label="资源名称" min-width="120" show-overflow-tooltip sortable>
                  <template #default="scope">
                    <div class="resource-item-name">
                      <div
                        :id="scope.row.id"
                        draggable="true"
                        class="resource-item-name-drag"
                        @dragstart="onDragStart"
                        @dragend="onDragEnd"
                        @drop.prevent="onDropFunction"
                        @dragover.prevent
                      >
                        <img :id="scope.row.id" :src="get_resource_icon(scope.row)" class="resource-icon" alt="" />
                        <div class="std-box" @click="preview_resource(scope.row)">
                          <el-text style="cursor: pointer" class="resource-name-text">
                            {{ scope.row.resource_name }}
                          </el-text>
                        </div>
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
                <el-table-column
                  prop="resource_status"
                  label="资源状态"
                  min-width="160"
                  sortable
                  :sort-method="sort_resource_status"
                >
                  <template #default="scope">
                    <div class="std-box">
                      <el-tag v-if="scope.row.resource_status == '正常'" type="success" round>正常</el-tag>
                      <el-tag v-else type="danger" round>{{ scope.row.resource_status }}</el-tag>
                      <el-tooltip content="索引状态" placement="top">
                        <el-tag v-if="scope.row.rag_status" :type="getResourceRagStatus(scope.row)" round>
                          {{ scope.row.rag_status }}
                        </el-tag>
                      </el-tooltip>
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
                          <el-button text class="resource-button" @click="preview_resource(scope.row)">
                            查看
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="download_resource(scope.row)">
                            下载
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="share_resource(scope.row)"> 分享 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="move_resource(scope.row)"> 移动到 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="rebuild_resource(scope.row)">
                            重新索引
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text type="danger" class="resource-button" @click="delete_resource(scope.row)">
                            删除
                          </el-button>
                        </div>
                      </div>
                    </el-popover>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            <div v-show="showCardList" id="card-model" ref="resource_card_scroll_Ref">
              <div
                v-for="item in currentResourceList"
                :id="item.id.toString()"
                :key="item.id"
                class="resource-item-card"
                :class="{ resource_selected: item.resource_is_selected }"
                draggable="true"
                :row-key="row => row.id"
                @dblclick="double_click_resource_card(item)"
                @click="clickResourceCard(item, $event)"
                @dragstart="onDragStart"
                @dragend="onDragEnd"
                @dragover.prevent
                @drop.prevent="onDropFunction"
                @contextmenu.prevent="openCardContextMenu(item, $event)"
              >
                <div :id="item.id.toString()" class="resource-item-card-head">
                  <div :id="item.id.toString()" class="resource-item-card-icon">
                    <el-image :id="item.id.toString()" :src="get_resource_icon(item)" class="resource-card-icon" />
                  </div>
                  <div :id="item.id.toString()" class="resource-item-select">
                    <el-checkbox v-model="item.resource_is_selected" @click.prevent />
                  </div>
                </div>
                <div :id="item.id.toString()" class="resource-item-card-body">
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
                  <div class="resource-item-card-body-button">
                    <el-popover ref="resource_list_card_buttons_Ref" trigger="click" :hide-after="0">
                      <template #reference>
                        <el-image src="/images/dot_list_grey.svg" class="resource-icon2" />
                      </template>
                      <div class="resource-button-group">
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="preview_resource(item)"> 查看 </el-button>
                        </div>

                        <div class="resource-button">
                          <el-button text class="resource-button" @click="download_resource(item)"> 下载 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="share_resource(item)"> 分享 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="move_resource(item)"> 移动到 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="rebuild_resource(item)"> 重新索引 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text type="danger" class="resource-button" @click="delete_resource(item)">
                            删除
                          </el-button>
                        </div>
                      </div>
                    </el-popover>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-scrollbar>
        <div v-if="!currentResourceList?.length && !isLoading" class="std-middle-box" style="width: 100%; height: 100%">
          <ResourceEmpty :is-search-mode="isSearchMode" />
        </div>
        <div v-if="!isLoading" :class="['permission-container', { 'permission-container-hide': hidePermission }]">
          <ResourceDetail ref="resourceDetailRef" />
        </div>
      </div>
    </el-main>
    <el-footer
      v-show="multipleSelection.length > 0"
      height="60px"
      style="padding: 0 !important; background-color: #f9fafb"
    >
      <el-scrollbar>
        <div id="resource_footer">
          <div id="resource_foot_left">
            <div class="std-middle-box">
              <el-text style="min-width: 120px"> 当前已经选择{{ multipleSelection.length }}项 </el-text>
            </div>
            <div class="resource-foot-button" @click="batch_move_select_resources">
              <el-text> 移动到 </el-text>
            </div>
            <div v-if="false" class="resource-foot-button" @click="batchCopySelectResource">
              <el-text> 复制 </el-text>
            </div>
          </div>
          <div id="resource_foot_middle">
            <div class="resource-foot-button" @click="batch_download_select_resource">
              <el-text> 下载 </el-text>
            </div>
            <div class="resource-foot-button" @click="show_delete_flag = true">
              <el-text> 删除 </el-text>
            </div>
          </div>
          <div id="resource_foot_right">
            <div class="resource-foot-button" @click="batchRebuild">
              <el-text> 重新索引 </el-text>
            </div>
            <div class="resource-foot-button" @click="cancelMultipleSelection">
              <el-text> 取消 </el-text>
            </div>
          </div>
        </div>
      </el-scrollbar>
    </el-footer>
    <el-dialog v-model="show_delete_flag" :title="delete_dialog_title" style="max-width: 600px" :width="dialogWidth">
      <div
        style="display: flex; flex-direction: column; gap: 16px; align-items: flex-start; justify-content: flex-start"
      >
        <div class="std-middle-box">
          <el-result
            icon="warning"
            title="确认删除选中资源？"
            sub-title="删除的内容将进入回收站，您可以在回收站中找回，30天后自动彻底删除！"
          />
        </div>

        <div id="button-area">
          <el-button @click="show_delete_flag = false"> 取消 </el-button>
          <el-button type="danger" @click="batchDeleteResource()"> 确定 </el-button>
        </div>
      </div>
    </el-dialog>
  </el-container>
  <ResourceMeta />
  <ResourceViewTree />
  <ContextMenu />
  <ResourceShareSelector />
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
  justify-content: flex-start;
  align-items: flex-start;
  padding: 12px 16px 0;
  align-content: flex-start;
  box-sizing: border-box;
  gap: 16px;
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
}

.std-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  width: 100%;
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
  width: 100%;
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
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border: 1px solid #d0d5dd;
  box-shadow: 0 1px 2px 0 #1018280d;
  border-radius: 6px;
  cursor: pointer;
  min-width: 60px;
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

.std-box-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: auto;
  gap: 8px;
  margin-left: 12px;
  & > .resource-name-text:last-child {
    color: #999;
  }
}

.permission-container {
  margin-left: 16px;
  box-shadow: -5px 0 10px -5px rgba(0, 0, 0, 0.1);
  // transition: all 0.5s ease-in-out;
  width: 320px;
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
