<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import { ElMessage, ElNotification } from 'element-plus';
import { computed, nextTick, onBeforeUnmount, onMounted, provide, ref, watch } from 'vue';
import {
  batch_download_select_resource,
  click_resource_card,
  double_click_resource_card,
  get_current_share_resource,
  get_share_parent_resource_list,
  handle_selection_change,
  multiple_selection,
  preview_share_resource,
  resource_share_list_card_buttons_Ref,
  resource_share_list_Ref,
  search_all_resource_share_object as searchAllResources,
  share_resource_list,
  cancel_multiple_selection,
  current_share_resource,
  el_scrollbar_Ref,
  current_page_num,
  current_page_size,
  current_total,
  resource_list_scroll_Ref,
  resource_card_scroll_Ref,
  search_next_resource_share_object
} from '@/components/resource/resource-share/share_resources';
import ResourceHead from '@/components/resource/resource-share/resource_head/resource_head.vue';
import ResourceMeta from '@/components/resource/resource_meta/resource_meta.vue';
import ResourceDetail from '@/components/resource/resource-detail/index.vue';
import {
  setCurrentRowItem,
  openCardContextMenu,
  openContextMenu,
  openTableContextMenu, resource_share_context_menu_flag
} from '@/components/resource/resource-share/context_menu/context_menu';
import { onBeforeRouteLeave, useRoute } from 'vue-router';
import {
  download_resource,
  format_resource_size,
  get_resource_icon,
  share_resource,
  sort_resource_size,
  sort_resource_status
} from '@/components/resource/resource-list/resource_list';
import ContextMenu from '@/components/resource/resource-share/context_menu/context_menu.vue';
import ResourceShareSelector from '@/components/resource/resource_share_selector/resource_share_selector.vue';
import ResourceEmpty from '@/components/resource/ResourceEmpty.vue';
import ResourceViewTree from '@/components/resource/resource_tree/resource_view_tree.vue';
import { ISearchByKeywordParams, ResourceItem, TResourceListStatus } from '@/types/resource-type';
import { useShareResourceStore } from '@/stores/resourceShareStore';
import { storeToRefs } from 'pinia';

const props = defineProps({
  resource_id: {
    type: String,
    default: '',
    required: false
  }
});
const { isSearchMode, isLoading } = storeToRefs(useShareResourceStore());
const shareListStatus = useSessionStorage<TResourceListStatus>('shareListStatus', 'card');
const showCardList = computed(() => {
  return shareListStatus.value === 'card';
});
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
defineOptions({
  name: 'ShareResources'
});

onMounted(async () => {
  if (props.resource_id) {
    await get_current_share_resource(props.resource_id);
  } else {
    current_share_resource.id = -1;
    current_share_resource.resource_name = '共享资源';
  }
  await get_share_parent_resource_list();
  await searchAllResources();
  isLoading.value = false;
  document.addEventListener('click', closeMenu);
});
onBeforeUnmount(() => {
  share_resource_list.value = [];
  isLoading.value = true;
  document.removeEventListener('click', closeMenu);
});
onBeforeRouteLeave((to, from, next) => {
  current_page_num.value = 1;
  current_page_size.value = 50;
  current_total.value = 0;
  next();
});

const hidePermission = useSessionStorage('hideShareResourcePermission', false);
const keyword = ref('');
const route = useRoute();
const resourceId = ref(route.params.resource_id);
const currentResourceId = useSessionStorage('currentResourceId', '');
const multipleSelection = computed(() => {
  return share_resource_list.value.filter(item => item.resource_is_selected);
});
const isMultipleSelection = computed(() => {
  return multipleSelection.value.length > 1;
});
provide('isMultipleSelection', isMultipleSelection);

watch(keyword, async newValue => {
  if (newValue === '') {
    isSearchMode.value = false;
    await searchAllResources();
  }
});

watch(
  () => route.params,
  newVal => {
    resourceId.value = (newVal.resource_id as string) ?? '';
  }
);

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
    resource_id: resourceId.value as string
  };
  await searchAllResources(params);
}

function handleClear() {
  isSearchMode.value = false;
  keyword.value = '';
}

function handleSelectionChange(val: ResourceItem[]) {
  currentResourceId.value = val.at(-1)?.id.toString() ?? '';
  setCurrentRowItem(val.at(-1));
  handle_selection_change(val);
}

function clickResourceCard(item: ResourceItem, event: MouseEvent) {
  click_resource_card(item, event);
  nextTick(() => {
    currentResourceId.value = multiple_selection.value.at(-1)?.id.toString() ?? '';
  });
}

function cancelMultipleSelection() {
  currentResourceId.value = (route.params.resource_id as string) ?? '';
  cancel_multiple_selection();
}

function loadMoreResource(e: Event) {
  if (share_resource_list.value.length === 0) {
    return;
  }
  search_next_resource_share_object(e);
}

provide('keyword', keyword);
</script>

<template>
  <el-container>
    <el-header height="60" style="padding: 0 !important">
      <ResourceHead @handle-search="handleSearch" @handle-clear="handleClear" />
    </el-header>
    <el-main style="padding: 2px !important" @contextmenu.prevent="openContextMenu">
      <div
        id="resource_list_main"
        v-loading="isLoading"
        element-loading-text="加载中"
        :style="{ height: 'calc(100vh -  121px)' }"
      >
        <el-scrollbar
          v-if="share_resource_list.length"
          ref="el_scrollbar_Ref"
          style="width: 100%"
          @scroll="loadMoreResource"
        >
          <div v-show="!showCardList" id="list_model" ref="resource_list_scroll_Ref">
            <el-table
              ref="resource_share_list_Ref"
              :data="share_resource_list"
              :highlight-current-row="true"
              :row-key="row => row.id"
              border
              @row-contextmenu="openTableContextMenu"
              select-all
              @selection-change="handleSelectionChange"
            >
              <el-table-column type="selection" :reserve-selection="true" width="40" class-name="resource-selection" />
              <el-table-column prop="resource_name" label="资源名称" min-width="160" show-overflow-tooltip sortable>
                <template #default="scope">
                  <div class="resource-item-name">
                    <div class="resource-item-name-drag" :id="scope.row.id">
                      <img :src="get_resource_icon(scope.row)" class="resource-icon" :id="scope.row.id" alt="" />
                    </div>
                    <div class="std-box" @click="preview_share_resource(scope.row)">
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
                label="资源状态"
                min-width="160"
                sortable
                :sort-method="sort_resource_status"
              >
                <template #default="scope">
                  <div class="std-box">
                    <el-tag v-if="scope.row.resource_status == '正常'" type="success" round>正常</el-tag>
                    <el-tag v-else type="danger" round>{{ scope.row.resource_status }}</el-tag>
                    <el-tag v-if="scope.row.rag_status == 'Success'" type="success" round> 索引 </el-tag>
                  </div>
                </template>
              </el-table-column>

              <el-table-column prop="" label="操作" width="60" class-name="resource-selection" fixed="right">
                <template #default="scope">
                  <el-popover trigger="click" :visible="scope.row?.show_buttons" ref="resource_list_buttons_Ref">
                    <template #reference>
                      <el-image src="/images/dot_list_grey.svg" class="resource-icon2" />
                    </template>
                    <div class="resource-button-group">
                      <div class="resource-button">
                        <el-button text @click="preview_share_resource(scope.row)" class="resource-button">
                          查看
                        </el-button>
                      </div>
                      <!-- <div class="resource-button">
                        <el-button text @click="show_resource_detail(scope.row)" class="resource-button">
                          详情
                        </el-button>
                      </div> -->
                      <div class="resource-button">
                        <el-button text @click="download_resource(scope.row)" class="resource-button"> 下载 </el-button>
                      </div>
                      <div class="resource-button">
                        <el-button text @click="share_resource(scope.row)" class="resource-button"> 分享 </el-button>
                      </div>
                    </div>
                  </el-popover>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div v-show="showCardList" id="card-model" ref="resource_card_scroll_Ref">
            <div
              v-for="item in share_resource_list"
              class="resource-item-card"
              :class="{ resource_selected: item.resource_is_selected }"
              @dblclick="double_click_resource_card(item)"
              @click="clickResourceCard(item, $event)"
              draggable="true"
              :key="item.id"
              @contextmenu.prevent="openCardContextMenu(item, $event)"
              :id="item.id.toString()"
            >
              <div class="resource-item-card-head" :id="item.id.toString()">
                <div class="resource-item-card-icon" :id="item.id.toString()">
                  <el-image :src="get_resource_icon(item)" class="resource-card-icon" :id="item.id.toString()" />
                </div>
                <div class="resource-item-select" :id="item.id.toString()">
                  <el-checkbox v-model="item.resource_is_selected" @click.prevent />
                </div>
              </div>
              <div class="resource-item-card-body card-panel" :id="item.id.toString()">
                <div class="resource-item-card-panel">
                  <div class="std-middle-box" :id="item.id.toString()">
                    <el-image
                      :src="get_resource_icon(item)"
                      style="width: 40px; height: 40px"
                      :id="item.id.toString()"
                    />
                  </div>
                  <div class="std-middle-box" :id="item.id.toString()">
                    <el-text class="card-title" truncated style="width: 140px" :id="item.id.toString()">
                      {{ item.resource_name }}
                    </el-text>
                  </div>
                </div>
                <div class="resource-item-card-panel">
                  <!-- <div v-show="item.auth_type" class="std-middle-box" :id="item.id.toString()">
                    <el-tag type="primary">{{ getAuthTypeText(item.auth_type) }}</el-tag>
                  </div> -->
                  <div class="resource-item-card-body-button">
                    <el-popover trigger="click" :hide-after="0" ref="resource_share_list_card_buttons_Ref">
                      <template #reference>
                        <el-image src="/images/dot_list_grey.svg" class="resource-icon2" />
                      </template>
                      <div class="resource-button-group">
                        <div class="resource-button">
                          <el-button text @click="preview_share_resource(item)" class="resource-button">
                            查看
                          </el-button>
                        </div>
                        <!-- <div class="resource-button">
                          <el-button text @click="show_resource_detail(item)" class="resource-button"> 详情 </el-button>
                        </div> -->
                        <div class="resource-button">
                          <el-button text @click="download_resource(item)" class="resource-button"> 下载 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text @click="share_resource(item)" class="resource-button"> 分享 </el-button>
                        </div>
                      </div>
                    </el-popover>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-scrollbar>
        <div v-if="!share_resource_list?.length && !isLoading" class="std-middle-box" style="width: 100%; height: 100%">
          <ResourceEmpty :is-search-mode="isSearchMode" />
        </div>
        <div v-if="!isLoading" :class="['permission-container', { 'permission-container-hide': hidePermission }]">
          <ResourceDetail />
        </div>
      </div>
    </el-main>
    <el-footer
      v-if="multipleSelection.length > 0"
      height="60px"
      style="padding: 0 !important; background-color: #f9fafb"
    >
      <el-scrollbar>
        <div id="resource_footer">
          <div id="resource_foot_left">
            <div class="std-middle-box">
              <el-text style="min-width: 120px"> 当前已经选择{{ multipleSelection.length }}项 </el-text>
            </div>
          </div>
          <div id="resource_foot_middle">
            <el-popconfirm
              title="您在一段时间内可以下载的共享资源是有限的，确认启用批量下载？"
              @confirm="batch_download_select_resource"
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
      </el-scrollbar>
    </el-footer>
  </el-container>
  <ResourceMeta />
  <ContextMenu />
  <ResourceShareSelector />
  <ResourceViewTree />
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

.permission-container {
  margin-left: 16px;
  box-shadow: -5px 0 10px -5px rgba(0, 0, 0, 0.1);
  // transition: all 0.5s ease-in-out;
  width: 200px;
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
