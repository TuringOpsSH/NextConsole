<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import {ElMessage, genFileId, UploadRawFile} from 'element-plus';
import { storeToRefs } from 'pinia';
import {onBeforeUnmount, onMounted, reactive, ref, watch} from 'vue';
import { onBeforeRouteLeave, useRoute } from 'vue-router';
import { get_resource_recent_format_count, search_resource_tags } from '@/api/resource-api';
import {
  batch_completely_delete_resources,
  batch_copy_select_resources,
  batch_delete_resources,
  batch_download_select_resource,
  batch_move_select_resources,
  batch_rebuild,
  batch_recover_resources,
  button_Ref,
  cancel_multiple_selection,
  click_resource_card,
  completely_delete_flag,
  completely_delete_resource,
  current_page_num,
  current_page_size,
  current_resource_cnt,
  current_resource_list,
  current_tag,
  delete_resource,
  download_resource,
  get_system_tag,
  get_timestamp_duration,
  get_upload_progress,
  getHighlightedText,
  getMarkdownHtml,
  handle_selection_change,
  handleCurrentChange,
  handleDragOver,
  handleSizeChange,
  move_resource,
  multiple_selection,
  onDragEnd,
  onDragStart,
  rebuild_resource,
  recover_resource,
  resource_loading,
  resource_shortcut_Ref,
  resource_view_model,
  search_rag_enhance,
  search_resource_by_tags,
  setCurrentResourceValues,
  share_resource,
  show_delete_flag,
  show_delete_resource_detail, show_multiple_button,
  show_recover_flag,
  show_resource_detail,
  show_upload_progress_status
} from '@/components/resource/resource-shortcut/resource_shortcut';
import {
  current_resource_tags,
  current_resource_types,
  show_search_config_area,
  showConfigFlag
} from '@/components/resource/resource-shortcut/resource_shortcut_head/resource_shortcut_head';
import ResourceEmpty from '@/components/resource/ResourceEmpty.vue';
import {
  double_click_resource_card,
  format_resource_size,
  get_resource_icon,
  sort_resource_size,
  sort_resource_status
} from '@/components/resource/resource-list/resource_list';
import ResourceMeta from '@/components/resource/resource_meta/resource_meta.vue';
import ResourceViewTree from '@/components/resource/resource_tree/resource_view_tree.vue';
import {
  close_upload_manager,
  prepare_upload_files, show_upload_manage_box, upload_button_Ref,
  upload_file_content,
  upload_file_list, upload_parent_resource
} from '@/components/resource/resource-upload/resource-upload';
import ResourceShareSelector from '@/components/resource/resource-share-selector/resource_share_selector.vue';
import router from '@/router';
import { useResourceStore } from '@/stores/resourceStore';
import { useUserInfoStore } from '@/stores/user-info-store';
import { current_resource_usage_percent, handle_search_clear } from '@/components/resource/resource-panel/panel';
import {
  choose_resource_meta,
  show_meta_flag,
  turn_on_resource_meta
} from '@/components/resource/resource_meta/resource_meta';
import { AUTH_TYPE, RESOURCE_FORMATS } from '@/utils/constant';
import {ResourceItem, ResourceTag} from "@/types/resource-type";

const props = defineProps({
  tag_source: {
    type: String,
    default: 'system'
  },
  tag_id: {
    type: Array,
    default: []
  },
  tag_value: {
    type: String,
    default: ''
  },
  resource_type: {
    type: Array,
    default: []
  },
  resource_format: {
    type: Array,
    default: []
  },
  resource_keyword: String,
  resource_key_word: String,
  resource_view_model: String,
  page_size: {
    type: Number,
    default: 50
  },
  page_num: {
    type: Number,
    default: 1
  },
  rag_enhance: {
    type: Boolean,
    default: false
  }
});
const userInfoStore = useUserInfoStore();
const dialogWidth = ref(window.innerWidth < 768 ? '90%' : '600px');
const pageModel = ref(
  window.innerWidth < 768 ? 'total, prev, pager, next, jumper' : 'total, sizes, prev, pager, next, jumper'
);

const resourceStore = useResourceStore();
const phoneView = ref(window.innerWidth < 768);
const route = useRoute();
const { authType } = storeToRefs(resourceStore);
const needAuthType = ref(route.name === 'resource_search');
const currentResourceValues = useSessionStorage('currentResourceValues', []);
const showResourceFormat = ref(true);
const loadingUserTags = ref(false);
const allResourceTypes = [
  { name: '文档', value: 'document' },
  { name: '图片', value: 'image' },
  { name: '网页', value: 'webpage' },
  { name: '代码', value: 'code' },
  { name: '文件夹', value: 'folder' },
  { name: '视频', value: 'video' },
  { name: '音频', value: 'audio' },
  { name: '程序', value: 'binary' },
  { name: '压缩包', value: 'archive' },
  { name: '文本', value: 'text' },
  { name: '其他', value: 'other' }
];
const allResourceFormats = ref([]);
const isIndeterminate = ref(false);
const checkAll = ref(false);
const updateResourceKeyword = ref('');
const updateRagEnhance = ref(false);
const editSearchKeywordFlag = ref(false);
const allResourceTags = ref<ResourceTag[]>([]);
const mousePosition = ref({ x: 0, y: 0 });
const currentRowItem = reactive<ResourceItem>({
  id: null,
  resource_parent_id: null,
  user_id: null,
  resource_name: null,
  resource_type: null,
  resource_desc: null,
  resource_icon: null,
  resource_format: null,
  resource_path: null,
  // eslint-disable-next-line @typescript-eslint/naming-convention
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
const uploadFileRef = ref(null);
const contextMenuFlag = ref(false);
const currentResourceFormats = ref([]);
async function handleCheckAllChange(val: boolean) {
  const cities = [
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
  current_resource_types.value = val ? cities : [];
  isIndeterminate.value = false;
  // 同步至url
  await router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      tag_id: current_resource_tags.value.map(item => item.id),
      resource_type: current_resource_types.value,
      resource_format: currentResourceFormats.value
    }
  });
  await search_resource_by_tags();
}
async function initAllResourceFormats() {
  let params = {};
  let res = await get_resource_recent_format_count(params);
  if (!res.error_status) {
    for (let item of res.result) {
      // 去除已经存在的格式
      // console.log (item)
      let findFlag = false;
      for (let existFormat of allResourceFormats.value) {
        if (existFormat.name === item.name) {
          existFormat.cnt = item.cnt;
          findFlag = true;
          break;
        }
      }
      if (!findFlag) {
        allResourceFormats.value.push(item);
      }
    }
  }
}
async function confirmUpdateKeyword() {
  if (!updateResourceKeyword.value) {
    ElMessage.error('请输入搜索关键字');
    return;
  }

  editSearchKeywordFlag.value = false;
  // @ts-ignore
  current_tag.value.tag_name = updateResourceKeyword.value.trim();
  search_rag_enhance.value = updateRagEnhance.value;
  await router.push({
    name: 'resource_search',
    params: {
      tag_source: 'system'
    },
    query: {
      ...router.currentRoute.value.query,
      resource_keyword: updateResourceKeyword.value,
      tag_value: 'search',
      // @ts-ignore
      rag_enhance: updateRagEnhance.value
    }
  });
  await search_resource_by_tags();
}
function changeResourceFormat(value: string[]) {
  currentResourceValues.value = value;
  setTimeout(() => {
    search_resource_by_tags();
  }, 0);
}
async function searchResourceTagsByKeyword(query: string) {
  if (query === '') {
    return;
  }
  let params = {
    tag_keyword: query,
    fetch_all: true
  };
  loadingUserTags.value = true;
  let res = await search_resource_tags(params);
  if (!res.error_status) {
    allResourceTags.value = res.result;
  }
  loadingUserTags.value = false;
}
async function systemTagsFilterChange() {
  // 同步至url
  await router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      tag_id: current_resource_tags.value.map(item => item.id),
      resource_type: current_resource_types.value,
      resource_format: currentResourceFormats.value
    }
  });
  await search_resource_by_tags();
}
async function initPage() {
  if (props.tag_source == 'system') {
    // @ts-ignore
    current_tag.value = get_system_tag(props.tag_value);
    if (current_tag.value.tag_value == 'search') {
      current_tag.value.tag_name = props.resource_keyword.trim();
    }
    // 根据系统标签搜索展示资源
  }
  if (props.tag_source == 'user') {
    // @ts-ignore
    current_tag.value = {
      tag_name: '标签搜索',
      tag_source: 'user',
      tag_value: 'search'
    };
    // 根据系统标签搜索展示资源
  }
  if (props.tag_id?.length) {
    // @ts-ignore
    current_resource_tags.value = [];
    // 获取标签信息
    let tag_list = [];
    for (let tag_id of props.tag_id) {
      tag_list.push(tag_id);
    }
    let res = await search_resource_tags({
      tag_list: tag_list,
      fetch_all: true
    });
    if (!res.error_status) {
      current_resource_tags.value = res.result;
      allResourceTags.value = res.result;
    }
    show_search_config_area(true);
  }
  if (props.resource_type?.length) {
    if (typeof props.resource_type == 'string') {
      // @ts-ignore
      current_resource_types.value = [props.resource_type];
    } else {
      // @ts-ignore
      current_resource_types.value = props.resource_type;
    }
  }
  if (props.resource_format?.length) {
    if (typeof props.resource_format == 'string') {
      // @ts-ignore
      currentResourceFormats.value = [props.resource_format];
    } else {
      // @ts-ignore
      currentResourceFormats.value = props.resource_format;
    }
  }
  if (props.resource_view_model) {
    resource_view_model.value = props.resource_view_model;
  }
  if (props.page_num) {
    try {
      // 转换为int
      current_page_num.value = props.page_num;
    } catch (e) {}
  }
  if (props.page_size) {
    try {
      // 转换为int
      current_page_size.value = props.page_size;
    } catch (e) {}
  }
  if (props.rag_enhance !== null) {
    search_rag_enhance.value = props.rag_enhance;
  }
  await search_resource_by_tags();
  if (window.innerWidth < 768) {
    pageModel.value = 'total, prev, pager, next, jumper';
  }
  console.log(multiple_selection.value?.length);
}
function switchEditSearchKeywordDialog() {
  editSearchKeywordFlag.value = true;
  updateResourceKeyword.value = '';
  updateRagEnhance.value = false;
}
async function switchShowResourceMeta() {
  // 设置当前资源的meta信息
  // 如果选中了资源，则显示选中资源的meta信息
  if (multiple_selection.value?.length > 0) {
    // 将最新选中的资源设置为当前资源
    let resource_id = multiple_selection.value[multiple_selection.value.length - 1]?.id;
    if (!resource_id) {
      return;
    }
    turn_on_resource_meta(resource_id);
    return;
  }
  // 如果没有选中资源，则显示最近上传的元信息
  choose_resource_meta.id = null;
  choose_resource_meta.resource_name = current_tag.value.tag_name;
  choose_resource_meta.resource_icon = '/images/tag.svg';
  choose_resource_meta.resource_desc = current_tag.value.tag_desc;
  // console.log(choose_resource_meta, current_tag.value)
  show_meta_flag.value = true;
}
async function handleDrop(event) {
  upload_parent_resource.value = null;
  // 获取拖拽文件
  const files = event.dataTransfer.files;
  if (files.length > 0) {
    for (let j = 0; j < files.length; j++) {
      if (files[j]) {
        const file = files[j] as UploadRawFile;
        file.uid = genFileId();
        uploadFileRef.value?.handleStart(file);
        upload_file_list.value.push(file);
        // prepare_upload_files(file)
      }
    }
    show_upload_manage_box.value = true;
    uploadFileRef.value?.submit();
  }
}
function initUploadManager() {
  upload_parent_resource.value = null;
  upload_button_Ref.value = uploadFileRef.value;
}
function selectAll() {
  // 全选
  for (const item of current_resource_list.value) {
    item.resource_is_selected = !item.resource_is_selected;
  }
  show_multiple_button.value = !show_multiple_button.value;
  resource_shortcut_Ref.value?.toggleAllSelection();
}
async function switchResourceLayout(targetModel: string = null) {
  if (!targetModel) {
    if (resource_view_model.value === 'list') {
      resource_view_model.value = 'card';
    } else {
      resource_view_model.value = 'list';
    }
  } else {
    resource_view_model.value = targetModel;
  }
  // 更新至url
  await router.push({
    params: { ...router.currentRoute.value.params },
    query: {
      ...router.currentRoute.value.query,
      view_model: resource_view_model.value
    }
  });
}
function initContextPosition(event, menuHeight = 200) {
  // 打开菜单并设置位置
  contextMenuFlag.value = true;
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
function openCardContextMenu(row, event) {
  initContextPosition(event);
  Object.assign(currentRowItem, row);
  event.preventDefault();
  event.stopPropagation();
}
function openContextMenu(event) {
  // 打开菜单并设置位置
  currentRowItem.id = -1;
  initContextPosition(event, 140);
}
function openTableContextMenu(row, column, event) {
  for (const key in row) {
    currentRowItem[key] = row[key];
  }
  initContextPosition(event, 270);
  event.preventDefault();
  event.stopPropagation();
}
function closeMenu(event) {
  // 关闭菜单
  if (
    event.target.id !== 'resource_list_menu_box' &&
    event.target.id !== 'resource_shortcut_menu_box' &&
    event.target.id !== 'resource_share_menu_box'
  ) {
    contextMenuFlag.value = false;
  }
}
async function previewResource(resource: ResourceItem) {
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
    router.push({
      name: 'resource_list',
      params: {
        resource_id: resource.id
      }
    });
    return;
  }
  await router.push({
    name: 'resource_viewer',
    params: {
      resource_id: resource.id
    }
  });
}
watch(
  () => route.name,
  newVal => {
    needAuthType.value = newVal === 'resource_search';
  }
);
watch(authType, () => {
  search_resource_by_tags();
});
watch(
  () => route.query.resource_type,
  resourceType => {
    showResourceFormat.value = !['code', 'image', 'folder', 'video', 'audio', 'archive', 'webpage'].includes(
      Array.isArray(resourceType) ? resourceType[0] : resourceType
    );
  },
  { immediate: true }
);

onMounted(async () => {
  initPage();
  initAllResourceFormats();
  document.addEventListener('click', closeMenu);
});
onBeforeRouteLeave((to, from, next) => {
  close_upload_manager();
  next();
  multiple_selection.value = [];
});
onBeforeUnmount(() => {
  authType.value = '';
  setCurrentResourceValues([]);
  sessionStorage.removeItem('currentResourceValues');
  document.removeEventListener('click', closeMenu);
});

defineOptions({
  name: 'ResourceShortcut'
});
</script>

<template>
  <el-container>
    <el-header height="60px" style="padding: 0 !important">
      <div id="resource_header_area">
        <div
          id="resource_header"
          :style="{
            'box-shadow': showConfigFlag ? '0 2px 4px 0 rgba(0, 0, 0, .1)' : 'none'
          }"
        >
          <div id="resource_path">
            <el-image
              v-show="current_tag?.tag_value == 'search'"
              src="/images/back.svg"
              style="width: 20px; height: 20px; margin-right: 12px; cursor: pointer"
              @click="handle_search_clear"
            />

            <el-text class="resource-sub-path resource-sub-path-last" truncated>
              {{ current_tag.tag_name }}
            </el-text>
            <el-text
              v-show="current_tag?.tag_value == 'recycle_bin'"
              style="
                font-weight: 400;
                font-size: 14px;
                line-height: 20px;
                color: #475467;
                margin-left: 12px;
                min-width: 172px;
              "
            >
              进入回收站后75天自动清理
            </el-text>

            <el-image
              v-show="current_tag?.tag_value == 'search'"
              style="width: 20px; height: 20px; cursor: pointer; margin-left: 12px"
              src="/images/edit_label.svg"
              @click="switchEditSearchKeywordDialog"
            />
          </div>

          <div v-if="!phoneView" id="resource_layout_change" class="resource-head-button2" style="">
            <div
              id="resource_layout_change_left"
              :style="{ background: resource_view_model == 'list' ? '#D1E9FF' : '#F2F4F7' }"
              @click="switchResourceLayout('list')"
            >
              <el-tooltip content="列表模式" effect="light">
                <el-image
                  v-if="resource_view_model == 'list'"
                  src="/images/list_layout_active.svg"
                  class="resource-head-button-icon"
                />
                <el-image v-else src="/images/list_layout.svg" class="resource-head-button-icon" />
              </el-tooltip>
            </div>
            <div
              id="resource_layout_change_right"
              :style="{ background: resource_view_model == 'card' ? '#D1E9FF' : '#F2F4F7' }"
              @click="switchResourceLayout('card')"
            >
              <el-tooltip content="卡片模式" effect="light">
                <el-image
                  v-if="resource_view_model == 'card'"
                  src="/images/card_layout_active.svg"
                  class="resource-head-button-icon"
                />
                <el-image v-else src="/images/card_layout.svg" class="resource-head-button-icon" />
              </el-tooltip>
            </div>
          </div>
          <div id="resource_head_buttons">
            <div
              v-if="!phoneView"
              class="resource-head-button"
              :style="{
                background: showConfigFlag ? '#EFF8FF' : '#F2F4F7'
              }"
              @click="show_search_config_area"
            >
              <el-tooltip v-if="showConfigFlag" effect="light" :content="$t('resourceList')">
                <el-image src="/images/search_config_active.svg" class="resource-head-button-icon" />
              </el-tooltip>
              <el-tooltip v-else effect="light" :content="$t('resourceList')">
                <el-image src="/images/search_config.svg" class="resource-head-button-icon" />
              </el-tooltip>
            </div>
            <div
              class="resource-head-button"
              :style="{
                background: show_meta_flag ? '#EFF8FF' : '#F2F4F7'
              }"
              @click="switchShowResourceMeta"
            >
              <el-tooltip effect="light" :content="$t('resourceDetails')">
                <el-image
                  v-show="show_meta_flag"
                  src="/images/switch_resource_detail_active.svg"
                  class="resource-head-button-icon"
                />
              </el-tooltip>
              <el-tooltip effect="light" :content="$t('resourceDetails')">
                <el-image
                  v-show="!show_meta_flag"
                  src="/images/switch_resource_detail.svg"
                  class="resource-head-button-icon"
                />
              </el-tooltip>
            </div>
          </div>
        </div>
      </div>
    </el-header>
    <el-main style="padding: 2px !important" @contextmenu.prevent="openContextMenu">
      <el-scrollbar style="width: 100%">
        <div
          id="resource_list_main"
          v-loading="resource_loading"
          element-loading-text="加载中"
          @dragover.prevent="handleDragOver"
          @drop.prevent="handleDrop"
        >
          <div v-if="showConfigFlag" id="search_config_area">
            <div v-show="current_tag?.tag_type != 'resource_type'" id="search_config_area_top">
              <div class="std-middle-box">
                <el-text style="min-width: 60px">资源类型 </el-text>
              </div>
              <div class="std-middle-box" style="gap: 12px">
                <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange">
                  全选
                </el-checkbox>
                <el-checkbox-group v-model="current_resource_types" @change="systemTagsFilterChange">
                  <el-checkbox
                      v-for="item in allResourceTypes"
                      :key="item.value"
                      :value="item.value"
                      :label="item.name"
                  />
                </el-checkbox-group>
              </div>
            </div>
            <div id="search_config_area_mid">
              <div class="search_config_mid">
                <div class="std-middle-box">
                  <el-text style="width: 60px"> 资源标签 </el-text>
                </div>
                <div class="std-middle-box" style="width: 100%; max-width: 300px">
                  <el-select
                      v-model="current_resource_tags"
                      multiple
                      placeholder="搜索标签"
                      filterable
                      remote
                      reserve-keyword
                      :loading="loadingUserTags"
                      collapse-tags
                      collapse-tags-tooltip
                      value-key="id"
                      clearable
                      :remote-method="searchResourceTagsByKeyword"
                      @change="systemTagsFilterChange"
                  >
                    <el-option v-for="item in allResourceTags" :key="item.id" :label="item.tag_name" :value="item">
                      <div class="user-tag-area">
                        <div class="std-middle-box">
                          <el-image v-if="item?.tag_icon" class="user-label-color" :src="item?.tag_icon" />
                          <div v-else class="user-label-color" :style="{ background: item?.tag_color }" />
                        </div>
                        <div class="std-middle-box">
                          <el-text>
                            {{ item.tag_name }}
                          </el-text>
                        </div>
                      </div>
                    </el-option>
                  </el-select>
                </div>
              </div>
              <div v-if="showResourceFormat" class="search_config_mid">
                <div class="std-middle-box">
                  <el-text style="width: 60px"> 文档格式 </el-text>
                </div>
                <div class="std-middle-box" style="width: 100%; max-width: 160px">
                  <el-select
                      v-model="currentResourceValues"
                      multiple
                      placeholder="全部格式"
                      collapse-tags
                      collapse-tags-tooltip
                      @change="changeResourceFormat"
                  >
                    <el-option
                        v-for="resourceFormat in RESOURCE_FORMATS"
                        :key="resourceFormat.value"
                        :value="resourceFormat.value"
                        :label="resourceFormat.text"
                    >
                      {{ resourceFormat.text }}
                    </el-option>
                  </el-select>
                </div>
              </div>
              <div v-if="needAuthType" class="search_config_mid">
                <div class="std-middle-box">
                  <el-text style="width: 60px"> 资源权限 </el-text>
                </div>
                <div class="std-middle-box" style="width: 100%; max-width: 160px">
                  <el-select v-model="authType" placeholder="全部资源" collapse-tags collapse-tags-tooltip clearable>
                    <el-option v-for="item in AUTH_TYPE" :key="item.value" :value="item.value" :label="item.text">
                      <el-tag type="primary">
                        {{ item.text }}
                      </el-tag>
                    </el-option>
                  </el-select>
                </div>
              </div>
            </div>
            <div id="search_config_area_bottom">
              <div class="std-middle-box">
                <el-text> 共{{ current_resource_cnt }}个资源 </el-text>
              </div>
            </div>
          </div>
          <div v-show="resource_view_model == 'list' && !resource_loading" id="list_model">
            <el-table
              v-if="current_resource_list.length"
              ref="resource_shortcut_Ref"
              :data="current_resource_list"
              :highlight-current-row="true"
              :default-sort="{ prop: 'update_time', order: 'descending' }"
              border
              style="height: 100%"
              @row-contextmenu="openTableContextMenu"
              @selection-change="handle_selection_change"
              @select-all="handle_selection_change"
            >
              <el-table-column type="selection" width="55" class-name="resource-selection" />
              <el-table-column prop="resource_name" label="资源名称" min-width="200" show-overflow-tooltip sortable>
                <template #default="scope">
                  <div class="resource-item-name">
                    <div
                      :id="scope.row.id"
                      :draggable="true"
                      class="resource-item-name-drag"
                      @dragstart="onDragStart"
                      @dragend="onDragEnd"
                      @dragover.prevent
                    >
                      <img :id="scope.row.id" :src="get_resource_icon(scope.row)" class="resource-icon" alt="" />
                    </div>
                    <div class="std-box" style="cursor: pointer" @click="previewResource(scope.row)">
                      <el-text class="resource-name-text">
                        {{ scope.row.resource_name }}
                      </el-text>
                    </div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="resource_desc" label="资源描述" min-width="120" show-overflow-tooltip sortable />
              <el-table-column
                v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'search'"
                prop=""
                label="资源来源"
                min-width="200"
              >
                <template #default="scope">
                  <div v-if="scope.row.user_id == userInfoStore.userInfo?.user_id" class="std-box">
                    <el-avatar :src="userInfoStore.userInfo?.user_avatar" style="width: 16px; height: 16px" />
                    <el-text
                      style="width: 160px; font-size: 12px; font-weight: 500; line-height: 18px; color: #475467"
                      truncated
                    >
                      {{ userInfoStore.userInfo?.user_nick_name }}
                    </el-text>
                  </div>
                  <div v-else class="std-box">
                    <el-avatar :src="scope.row?.author_info?.user_avatar" style="width: 16px; height: 16px" />
                    <el-text
                      style="width: 160px; font-size: 12px; font-weight: 500; line-height: 18px; color: #475467"
                      truncated
                    >
                      {{ scope.row?.author_info?.user_nick_name }}
                    </el-text>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="create_time" label="创建时间" min-width="160" sortable />
              <el-table-column
                v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recycle_bin'"
                prop="delete_time"
                label="删除时间"
                min-width="160"
                sortable
              />
              <el-table-column v-else prop="update_time" label="更新时间" min-width="160" sortable />
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
                v-if="current_tag?.tag_source == 'user'"
                prop="resource_tags"
                label="资源标签"
                min-width="200"
              >
                <template #default="scope">
                  <div
                    class="std-middle-box"
                    style="width: 100%; flex-wrap: wrap; gap: 6px; justify-content: flex-start"
                  >
                    <el-tag v-for="tag in scope.row.resource_tags" :key="tag.id" type="success" round>
                      {{ tag.tag_name }}
                    </el-tag>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                v-if="current_tag?.tag_source == 'system' && current_tag.tag_value == 'recent_upload'"
                prop="task_source"
                label="上传来源"
                min-width="120"
                sortable
              >
                <template #default="scope">
                  <div class="std-box">
                    <el-tag v-if="scope.row.task_source == 'session'" type="success" round> 会话 </el-tag>

                    <el-tag v-else-if="scope.row.task_source == 'resource_center'" type="success" round>
                      资源库
                    </el-tag>
                    <el-tag v-else>
                      {{ scope.row.task_source }}
                    </el-tag>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="resource_status"
                label="资源状态"
                min-width="120"
                sortable
                :sort-method="sort_resource_status"
              >
                <template #default="scope">
                  <div class="std-box">
                    <el-tag v-if="scope.row.resource_status == '正常'" type="success" round>正常</el-tag>
                    <el-tag v-else type="danger" round>{{ scope.row.resource_status }}</el-tag>
                  </div>
                </template>
              </el-table-column>
              <!-- <el-table-column
              v-if="isShowAuthType"
              prop="authType"
              label="资源权限"
              min-width="120"
              sortable
              row-class-name="align-center"
            >
              <template #default="scope">
                <div class="std-box">
                  <el-tag type="success" round>{{ getAuthTypeText(scope.row.authType) }}</el-tag>
                </div>
              </template>
            </el-table-column> -->
              <el-table-column
                v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recycle_bin'"
                prop="left_time"
                label="剩余天数"
                min-width="160"
                sortable
              />
              <el-table-column
                v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recent_upload'"
                prop="update_time"
                label="上传进度"
                min-width="120"
                sortable
              >
                <template #default="scope">
                  <el-progress
                    :percentage="get_upload_progress(scope.row)"
                    :stroke-width="14"
                    :status="show_upload_progress_status(scope.row)"
                  />
                </template>
              </el-table-column>
              <el-table-column
                v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recent_index'"
                prop="rag_status"
                label="构建状态"
                min-width="120"
              >
                <template #default="scope">
                  <div class="std-middle-box">
                    <el-tag v-if="scope.row.rag_status == 'Success'" type="success" round> 索引成功 </el-tag>
                    <el-tag v-else-if="scope.row.rag_status == 'Failure'" type="warning" round> 索引失败 </el-tag>
                    <el-tag v-else-if="scope.row.rag_status == 'Pending'" type="primary" round> 索引中 </el-tag>
                    <el-tag v-else-if="scope.row.rag_status == 'Error'" type="danger" round> 索引错误 </el-tag>
                    <el-tag v-else> 未知 </el-tag>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recent_index'"
                prop="rag_duration"
                label="构建耗时"
                min-width="120"
                sortable
              >
                <template #default="scope">
                  <div class="std-middle-box">
                    <el-text>
                      {{ get_timestamp_duration(scope.row.rag_duration) }}
                    </el-text>
                  </div>
                </template>
              </el-table-column>
              <el-table-column v-if="search_rag_enhance" prop="ref_text" label="关联文本" min-width="120">
                <template #default="scope">
                  <div class="std-box">
                    <el-tooltip effect="light">
                      <el-text
                        style="cursor: default"
                        class="resource-name-text"
                        truncated
                        v-html="getHighlightedText(scope.row.ref_text)"
                      />
                      <template #content>
                        <el-scrollbar>
                          <div style="max-height: 500px; max-width: 500px">
                            <div
                              style="cursor: default"
                              class="resource-name-text"
                              v-html="getMarkdownHtml(getHighlightedText(scope.row.ref_text))"
                            />
                          </div>
                        </el-scrollbar>
                      </template>
                    </el-tooltip>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                v-if="search_rag_enhance"
                prop="rerank_score"
                label="相关度"
                min-width="120"
                show-overflow-tooltip
                sortable
              />
              <el-table-column prop="" label="操作" min-width="60" class-name="resource-selection" fixed="right">
                <template #default="scope">
                  <el-popover ref="button_Ref" trigger="click">
                    <template #reference>
                      <el-image src="/images/dot_list_grey.svg" class="resource-icon2" />
                    </template>
                    <div v-show="current_tag?.tag_value != 'recycle_bin'" class="resource-button-group">
                      <div class="resource-button">
                        <el-button text class="resource-button" @click="previewResource(scope.row)">
                          查看
                        </el-button>
                      </div>
                      <div class="resource-button">
                        <el-button text class="resource-button" @click="show_resource_detail(scope.row)">
                          详情
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
                    <div v-show="current_tag?.tag_value == 'recycle_bin'" class="resource-button-group">
                      <div class="resource-button">
                        <el-button text class="resource-button" @click="show_delete_resource_detail(scope.row)">
                          详情
                        </el-button>
                      </div>
                      <div class="resource-button">
                        <el-button text class="resource-button" @click="recover_resource(scope.row)">
                          恢复
                        </el-button>
                      </div>
                      <div class="resource-button">
                        <el-button
                          text
                          type="danger"
                          class="resource-button"
                          @click="completely_delete_resource(scope.row)"
                        >
                          彻底删除
                        </el-button>
                      </div>
                    </div>
                  </el-popover>
                </template>
              </el-table-column>
            </el-table>
            <ResourceEmpty v-else />
          </div>
          <div v-show="resource_view_model == 'card' && !resource_loading" id="card-model">
            <div
              v-for="item in current_resource_list"
              class="resource-item-card"
              :class="{ resource_selected: item.resource_is_selected }"
              draggable="true"
              @dblclick="double_click_resource_card(item)"
              @click="click_resource_card(item, $event)"
              @dragstart="onDragStart"
              @dragend="onDragEnd"
              @dragover.prevent
              @contextmenu.prevent="openCardContextMenu(item, $event)"
            >
              <div class="resource-item-card-head">
                <div class="resource-item-card-icon">
                  <el-image :src="get_resource_icon(item)" class="resource-card-icon" />
                </div>
                <div class="resource-item-select">
                  <el-checkbox v-model="item.resource_is_selected" @click.prevent />
                </div>
              </div>
              <div class="resource-item-card-body card-panel">
                <div class="resource-item-card-panel">
                  <div class="std-middle-box">
                    <el-image :src="get_resource_icon(item)" style="width: 40px; height: 40px" />
                  </div>
                  <div class="std-middle-box" @click="previewResource(item)">
                    <el-text class="card-title" truncated style="width: 140px">
                      {{ item.resource_name }}
                    </el-text>
                  </div>
                </div>
                <div class="resource-item-card-panel">
                  <!-- <div v-show="item.authType" class="std-middle-box" :id="item.id.toString()">
                  <el-tag type="primary">{{ getAuthTypeText(item.authType) }}</el-tag>
                </div> -->
                  <div class="resource-item-card-body-button">
                    <el-popover ref="resource_shortcut_card_buttons_Ref" trigger="click" :hide-after="0">
                      <template #reference>
                        <el-image src="/images/dot_list_grey.svg" class="resource-icon2" />
                      </template>
                      <div v-show="current_tag?.tag_value != 'recycle_bin'" class="resource-button-group">
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="previewResource(item)"> 查看 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="show_resource_detail(item)">
                            详情
                          </el-button>
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
                          <el-button text class="resource-button" @click="rebuild_resource(item)">
                            重新索引
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text type="danger" class="resource-button" @click="delete_resource(item)">
                            删除
                          </el-button>
                        </div>
                      </div>
                      <div v-show="current_tag?.tag_value == 'recycle_bin'" class="resource-button-group">
                        <div class="resource-button">
                          <el-button text class="resource-button" @click="show_delete_resource_detail(item)">
                            详情
                          </el-button>
                        </div>

                        <div class="resource-button">
                          <el-button text class="resource-button" @click="recover_resource(item)"> 恢复 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button
                            text
                            type="danger"
                            class="resource-button"
                            @click="completely_delete_resource(item)"
                          >
                            彻底删除
                          </el-button>
                        </div>
                      </div>
                    </el-popover>
                  </div>
                </div>
              </div>
            </div>
            <div v-show="!current_resource_list?.length" class="std-middle-box" style="width: 100%; height: 100%">
              <ResourceEmpty />
            </div>
          </div>
        </div>
      </el-scrollbar>
    </el-main>
    <el-footer height="60px" style="padding: 0 !important; background-color: #f9fafb">
      <el-scrollbar>
        <div id="resource_footer">
          <div v-if="multiple_selection?.length > 0" id="resource_foot_left">
            <div class="std-middle-box">
              <el-text style="min-width: 120px"> 当前已经选择{{ multiple_selection?.length }}项 </el-text>
            </div>
            <div
              v-show="current_tag?.tag_value != 'recycle_bin'"
              class="resource-foot-button"
              @click="batch_move_select_resources()"
            >
              <el-text> 移动到 </el-text>
            </div>
            <div
              v-if="false"
              v-show="current_tag?.tag_value != 'recycle_bin'"
              class="resource-foot-button"
              @click="batch_copy_select_resources()"
            >
              <el-text> 复制 </el-text>
            </div>
            <div
              v-show="current_tag?.tag_value == 'recycle_bin'"
              class="resource-foot-button"
              @click="show_recover_flag = true"
            >
              <el-text> 恢复 </el-text>
            </div>
          </div>
          <div v-if="multiple_selection?.length > 0" id="resource_foot_middle">
            <div
              v-show="current_tag?.tag_value != 'recycle_bin'"
              class="resource-foot-button"
              @click="batch_download_select_resource()"
            >
              <el-text> 下载 </el-text>
            </div>
            <div
              v-show="current_tag?.tag_value != 'recycle_bin'"
              class="resource-foot-button"
              @click="show_delete_flag = true"
            >
              <el-text> 删除 </el-text>
            </div>
            <div
              v-show="current_tag?.tag_value == 'recycle_bin'"
              class="resource-foot-button"
              @click="completely_delete_flag = true"
            >
              <el-text> 彻底删除 </el-text>
            </div>
          </div>
          <div v-if="multiple_selection?.length > 0" id="resource_foot_right">
            <div v-show="current_tag?.tag_value != 'recycle_bin'" class="resource-foot-button" @click="batch_rebuild()">
              <el-text> 重新索引 </el-text>
            </div>
            <div class="resource-foot-button" @click="cancel_multiple_selection()">
              <el-text> 取消 </el-text>
            </div>
          </div>
          <div v-else>
            <el-pagination
              :page-sizes="[20, 50, 100, 200, 500, 1000]"
              size="small"
              :page-size="current_page_size"
              :current-page="current_page_num"
              :layout="pageModel"
              :total="current_resource_cnt"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </div>
      </el-scrollbar>
    </el-footer>
  </el-container>
  <ResourceMeta />
  <ResourceViewTree />
  <div
    v-show="contextMenuFlag"
    id="resource_shortcut_menu_box"
    ref=""
    :style="{ left: mousePosition.x + 'px', top: mousePosition.y + 'px', position: 'absolute' }"
    class="ces-os-context-menu"
  >
    <div class="context-menu-button">
      <el-button text style="width: 100%" @click="search_resource_by_tags"> 刷新 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button text style="width: 100%" @click="show_resource_detail"> 详情 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="currentRowItem.id == -1" text style="width: 100%" @click="switchResourceLayout">
        切换布局
      </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="currentRowItem.id == -1" text style="width: 100%" @click="selectAll"> 全选 </el-button>
    </div>
    <el-upload
      ref="uploadFileRef"
      v-model:file-list="upload_file_list"
      multiple
      :show-file-list="false"
      :auto-upload="true"
      name="chunk_content"
      :before-upload="prepare_upload_files"
      :on-change="initUploadManager"
      :http-request="upload_file_content"
      :disabled="current_resource_usage_percent >= 100"
      accept="*"
      action=""
    >
      <div class="context-menu-button">
        <el-button text style="width: 100%"> 上传 </el-button>
      </div>
    </el-upload>
    <div class="context-menu-button">
      <el-button v-if="currentRowItem.id > 0" text style="width: 100%" @click="previewResource"> 查看 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="currentRowItem.id > 0" text style="width: 100%" @click="download_resource"> 下载 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="currentRowItem.id > 0" text style="width: 100%" @click="share_resource"> 分享 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="currentRowItem.id > 0" text style="width: 100%" @click="move_resource"> 移动到 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button v-if="currentRowItem.id > 0" text style="width: 100%" @click="rebuild_resource"> 重新构建 </el-button>
    </div>
    <div class="context-menu-button">
      <el-button
        v-if="currentRowItem.id > 0 && currentRowItem.resource_status != '删除'"
        text
        type="danger"
        style="width: 100%"
        @click="delete_resource"
      >
        删除
      </el-button>
      <el-button
        v-if="currentRowItem.id > 0 && currentRowItem.resource_status == '删除'"
        text
        type="danger"
        style="width: 100%"
        @click="completely_delete_resource(currentRowItem)"
      >
        彻底删除
      </el-button>
    </div>
  </div>
  <ResourceShareSelector />
  <el-dialog v-model="show_delete_flag" title="删除资源" style="max-width: 600px" :width="dialogWidth">
    <div style="display: flex; flex-direction: column; gap: 16px; align-items: center; justify-content: center">
      <div class="std-middle-box">
        <el-result
          icon="warning"
          title="确认删除选中资源？"
          sub-title="删除的内容将进入回收站，您可以在回收站中找回，30天后自动彻底删除！"
        />
      </div>

      <div id="button-area">
        <el-button @click="show_delete_flag = false"> 取消 </el-button>
        <el-button type="danger" @click="batch_delete_resources()"> 确定 </el-button>
      </div>
    </div>
  </el-dialog>
  <el-dialog v-model="show_recover_flag" title="恢复资源" style="max-width: 600px" :width="dialogWidth">
    <div style="display: flex; flex-direction: column; gap: 16px; align-items: center; justify-content: center">
      <div class="std-middle-box">
        <el-result icon="info" title="确认恢复选中资源？" sub-title="恢复的内容将回到原目录" />
      </div>

      <div id="button-area">
        <el-button @click="show_recover_flag = false"> 取消 </el-button>
        <el-button type="danger" @click="batch_recover_resources"> 确定 </el-button>
      </div>
    </div>
  </el-dialog>
  <el-dialog v-model="completely_delete_flag" title="彻底删除资源" style="max-width: 600px" :width="dialogWidth">
    <div style="display: flex; flex-direction: column; gap: 16px; align-items: center; justify-content: center">
      <div class="std-middle-box">
        <el-result icon="warning" title="确认彻底删除选中资源？" sub-title="注意！将会从系统中彻底删除，不可恢复！" />
      </div>

      <div id="button-area">
        <el-button @click="completely_delete_flag = false"> 取消 </el-button>
        <el-button type="danger" @click="batch_completely_delete_resources"> 确定 </el-button>
      </div>
    </div>
  </el-dialog>
  <el-dialog v-model="editSearchKeywordFlag" title="资源搜索" :width="dialogWidth">
    <div id="update_search_keyword_area">
      <div class="std-middle-box" style="width: 100%">
        <el-input
          v-model="updateResourceKeyword"
          placeholder="请输入搜索意图"
          type="textarea"
          :rows="4"
          resize="none"
        />
      </div>
      <div class="std-middle-box">
        <el-switch v-model="updateRagEnhance" active-text="内容检索" style="margin-right: 6px" />
      </div>
      <div class="std-middle-box" style="width: 100%">
        <el-button @click="editSearchKeywordFlag = false">取消</el-button>
        <el-button type="primary" @click="confirmUpdateKeyword">确定</el-button>
      </div>
    </div>
  </el-dialog>
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
  flex-direction: column;
  width: 100%;
  height: calc(100vh - 121px);
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
  align-content: flex-start;
  box-sizing: border-box;
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
  width: 100%;
  padding: 6px 12px;
  border-top: 1px solid #d0d5dd;
  gap: 8px;
  box-sizing: border-box;

  .resource-item-card-panel {
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

.card-panel {
  justify-content: space-between;
  height: auto;
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
.card-title:hover {
  color: #1570ef;
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
  .std-box {
    overflow: hidden;
  }
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
  background-color: white;
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
:deep(.el-progress__text) {
  font-size: 14px !important;
  font-weight: 500 !important;
  line-height: 20px !important;
}
#resource_shortcut_menu_box {
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 5px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  min-width: 80px;
  min-height: 100px;
}

.context-menu-button {
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
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
  #resource_footer {
    padding: 8px 0;
    height: 40px;
    justify-content: center;
  }
}

.std-middle-box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

#resource_header_area {
  display: flex;
  flex-direction: column;
  width: 100%;

  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

#resource_header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  height: 24px;
}

#resource_path {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 16px;
  width: calc(100% - 32px);
}

.resource-head-button-icon {
  width: 16px;
  height: 16px;
}

.resource-head-button2 {
  display: flex;
  padding: 2px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  border-radius: 8px;

  border: 0;
  min-width: 20px;
  width: 20px;
}

#resource_layout_change {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 2px;
  width: 100%;
}

#resource_layout_change_left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background: #f2f4f7;
  padding: 4px 6px;
  border-radius: 8px 0 0 8px;
  cursor: pointer;
}

#resource_layout_change_right {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background: #f2f4f7;
  padding: 4px 6px;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
}

#resource_head_buttons {
  display: flex;
  flex-direction: row;
  gap: 8px;
  width: 100%;
  align-items: center;
  justify-content: flex-end;
}

.resource-head-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px;
  padding: 2px;
}

.resource-head-button:hover {
  background: #eff8ff;
}

#search_config_area {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px 16px;
  /* height: 100px; */
}

#search_config_area_top {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}

#search_config_area_mid {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 32px;
}

.search_config_mid {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  min-width: 200px;
}

#search_config_area_bottom {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
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
}
#update_search_keyword_area {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}
.resource-sub-path {
  cursor: pointer;
  font-size: 14px;
}
.resource-sub-path:hover {
  color: #8ec5fc;
}
.resource-sub-path-last {
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  color: #101828;
}
@media (width < 768px) {
  .resource-sub-path {
    cursor: pointer;
    font-size: 12px;
    min-width: 40px;
    max-width: 120px;
  }
  .resource-sub-path-last {
    font-weight: 600;
    font-size: 12px;
    line-height: 14px;
    color: #101828;
    cursor: default;
  }
  #resource_header_area {
    box-shadow: none;
  }
}
</style>
