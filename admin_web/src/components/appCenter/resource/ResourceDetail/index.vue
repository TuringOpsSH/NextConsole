<template>
  <div id="resource-meta-area" v-loading="isLoading" element-loading-text="加载中...">
    <el-scrollbar>
      <div id="resource-meta-main">
        <div id="resource-meta-icon">
          <div class="std-middle-box">
            <el-image
              v-if="resourceDetail?.resource_icon"
              :src="getResourceIcon(resourceDetail)"
              style="width: 40px; height: 40px"
            />
          </div>
          <div class="std-middle-box">
            <el-text
              style="
                width: 100%;
                font-weight: 500;
                font-size: 14px;
                line-height: 20px;
                color: #344054;
                max-width: 200px;
              "
              truncated
            >
              {{ resourceDetail?.resource_name }}
            </el-text>
          </div>

          <div
            v-show="resourceDetail?.id && resourceDetail?.resource_parent_id"
            id="meta-edit-icon"
            class="std-middle-box"
            @click="editResource"
          >
            <el-image v-show="!isShowEdit" src="images/edit_label.svg" style="width: 20px; height: 20px" />
            <el-image v-show="isShowEdit" src="images/edit_label_active.svg" style="width: 20px; height: 20px" />
          </div>
        </div>
        <div id="resource-meta">
          <el-form v-if="resourceDetail?.resource_name" label-position="top">
            <el-form-item label="资源名称">
              <el-input
                v-model="resourceDetail.resource_name"
                type="textarea"
                resize="none"
                class="input-nowrap"
                :rows="2"
                :readonly="!isShowEdit"
              />
            </el-form-item>
            <el-form-item v-if="resourceDetail?.resource_desc" label="资源描述">
              <el-input
                v-model="resourceDetail.resource_desc"
                type="textarea"
                resize="none"
                :rows="4"
                :readonly="!isShowEdit"
              />
            </el-form-item>
            <el-form-item v-if="resourceDetail?.id" label="资源主要语言">
              <el-select v-model="resourceDetail.resource_language" :disabled="!isShowEdit">
                <el-option value="简体中文" label="简体中文" />
                <el-option value="繁體中文" label="繁體中文" />
                <el-option value="English" label="English" />
                <el-option value="Español" label="Español" />
                <el-option value="Français" label="Français" />
                <el-option value="Deutsch" label="Deutsch" />
                <el-option value="日本語" label="日本語" />
                <el-option value="한국어" label="한국어" />
                <el-option value="Русский" label="Русский" />
                <el-option value="Português" label="Português" />
                <el-option value="Italiano" label="Italiano" />
                <el-option value="हिन्दी" label="हिन्दी" />
                <el-option value="العربية" label="العربية" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>
        <el-divider v-show="resourceDetail?.id">
          <div id="resource-meta-divider">
            <div class="std-middle-box">
              <el-image src="images/ai_abstract_active.svg" style="width: 20px; height: 20px" />
            </div>
            <div class="std-middle-box">
              <el-text style="font-size: 14px; line-height: 20px; font-weight: 600; color: #175cd3"> 摘要 </el-text>
            </div>
          </div>
        </el-divider>
        <div v-show="resourceDetail?.id" id="resource-static">
          <div class="resource-static-item">
            <div class="resource-static-item-left">
              <el-text class="resource-static-label">资源ID</el-text>
            </div>
            <div class="resource-static-item-right">
              <el-text class="resource-static-value">{{ resourceDetail?.id }}</el-text>
            </div>
          </div>
          <div class="resource-static-item">
            <div class="resource-static-item-left">
              <el-text class="resource-static-label">资源类型</el-text>
            </div>
            <div class="resource-static-item-right">
              <el-text class="resource-static-value">{{ resourceDetail?.resource_type_cn }}</el-text>
            </div>
          </div>
          <div class="resource-static-item">
            <div class="resource-static-item-left">
              <el-text class="resource-static-label">资源大小</el-text>
            </div>
            <div class="resource-static-item-right">
              <el-text class="resource-static-value">
                {{ formatResourceSize(resourceDetail?.resource_size_in_MB) }}
              </el-text>
            </div>
          </div>
          <div class="resource-static-item" v-show="resourceDetail?.resource_type == 'folder'">
            <div class="resource-static-item-left">
              <el-text class="resource-static-label">资源统计</el-text>
            </div>
            <div class="resource-static-item-right">
              <el-text class="resource-static-value"> 子文件夹：{{ resourceDetail?.sub_resource_dir_cnt }}个 </el-text>
              <el-text class="resource-static-value"> 子文件：{{ resourceDetail?.sub_resource_file_cnt }} 个 </el-text>
            </div>
          </div>
          <div class="resource-static-item" v-show="resourceDetail?.author_info">
            <div class="resource-static-item-left">
              <el-text class="resource-static-label">资源作者</el-text>
            </div>
            <div class="resource-static-item-right">
              <el-avatar :src="resourceDetail?.author_info?.user_avatar" style="width: 18px; height: 18px" />
              <el-text class="resource-static-value" truncated>
                {{ resourceDetail?.author_info?.user_nick_name }}
              </el-text>
            </div>
          </div>
          <div v-show="resourceDetail?.access_list" class="resource-static-item">
            <div class="resource-static-item-left">
              <el-text class="resource-static-label">资源权限</el-text>
            </div>
            <div class="resource-static-item-right">
              <el-tag v-for="(access, idx) in resourceDetail?.access_list" type="success" :key="idx">
                {{ access }}
              </el-tag>
            </div>
          </div>
          <div class="resource-static-item">
            <div class="resource-static-item-left">
              <el-text class="resource-static-label">资源路径</el-text>
            </div>
            <div class="resource-static-item-right">
              <el-text class="resource-static-value">
                {{ resourceDetail?.resource_path }}
              </el-text>
            </div>
          </div>
          <div class="resource-static-item">
            <div class="resource-static-item-left">
              <el-text class="resource-static-label">创建时间</el-text>
            </div>
            <div class="resource-static-item-right">
              <el-text class="resource-static-value">{{ resourceDetail?.create_time }}</el-text>
            </div>
          </div>
          <div class="resource-static-item">
            <div class="resource-static-item-left">
              <el-text class="resource-static-label">索引状态</el-text>
              <el-tooltip effect="light" placement="top">
                <template #default>
                  <div class="std-middle-box">
                    <el-image src="images/tooltip.svg" style="width: 16px; height: 16px" />
                  </div>
                </template>
                <template #content>
                  <el-text> 为什么有多个状态？ </el-text>
                  <br />
                  <br />
                  <el-text> 一份文档可能会生成多个索引。 </el-text>
                  <br />
                  <el-text> 仅会使用成功状态的片段进行搜索。 </el-text>
                </template>
              </el-tooltip>
            </div>
            <div class="resource-static-item-right">
              <el-badge
                v-for="(rag_status, idx) in resourceDetail?.rag_status"
                :key="rag_status?.status"
                :value="rag_status?.cnt"
                :type="rag_status?.status === 'Success' ? 'success' : 'warning'"
                :max="99"
              >
                <el-tag :type="rag_status?.status === 'Success' ? 'success' : 'primary'">
                  {{ rag_status?.status }}
                </el-tag>
              </el-badge>

              <el-button
                v-show="showRebuildButton"
                text
                type="primary"
                :disabled="!isShowEdit"
                @click="rebuildResource"
              >
                重新索引
              </el-button>
            </div>
          </div>
        </div>
        <div v-show="resourceDetail?.id" id="resource-tags">
          <el-form label-position="top">
            <el-form-item label="资源标签">
              <el-select
                v-model="resourceDetail.resource_tags"
                :class="{ 'gxh-el-select': !isShowEdit }"
                multiple
                remote
                filterable
                reserve-keyword
                :loading="isLoadingTags"
                style="height: 200px"
                placeholder="搜索添加标签"
                :remote-method="searchResourceTags"
                size="large"
                :disabled="!isShowEdit"
                value-key="id"
                :remote-show-suffix="true"
              >
                <el-option v-for="item in resourceTags" :key="item.id" :label="item.tag_name" :value="item">
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
            </el-form-item>
          </el-form>
        </div>
      </div>
    </el-scrollbar>
    <div id="resource-meta-foot">
      <div v-show="isShowEdit" class="resource-meta-foot-button" @click="cancelEdit">
        <el-text class="resource-meta-foot-button-text"> 恢复 </el-text>
      </div>
      <div
        v-show="isShowEdit"
        class="resource-meta-foot-button"
        style="background-color: #1570ef"
        @click="updateResource"
      >
        <el-text class="resource-meta-foot-button-text" style="color: white"> 保存 </el-text>
      </div>
    </div>
  </div>
  <el-dialog
    v-model="uncommitNotice"
    title="未保存提示"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <div class="std-middle-box">
      <el-result icon="warning" title="Warning Tip" sub-title="您还有更新内容未保存，确定离开么？" />
    </div>
    <div id="resource-meta-foot">
      <div class="resource-meta-foot-button" @click="uncommitNotice = false">
        <el-text class="resource-meta-foot-button-text"> 返回更新 </el-text>
      </div>
      <div
        class="resource-meta-foot-button"
        style="background-color: #1570ef"
        @click="
          uncommitNotice = false;
          isShowMeta = false;
          isShowEdit = false;
        "
      >
        >
        <el-text class="resource-meta-foot-button-text" style="color: white"> 确定 </el-text>
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ElMessage, ElNotification } from 'element-plus';
import { useSessionStorage } from '@vueuse/core';
import { computed, onMounted, ref, watch, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  build_resource_object_ref as buildResourceObjectRef,
  get_resource_object as getResourceObject,
  resource_share_get_meta as resourceShareGetMeta,
  search_resource_tags as searchAllResourceTags,
  update_resource_object as updateResourceObject
} from '@/api/resource_api';
import {
  format_resource_size as formatResourceSize,
  get_resource_icon as getResourceIcon,
  search_all_resource_object as searchAllResourceObject
} from '@/components/resource/resource_list/resource_list';
import { user_info as useInfo } from '@/components/user_center/user';
import { ResourceTag } from '@/types/resource_type';
import {
  init_my_resource_tree as initMyResourceTree,
  refresh_panel_count as refreshPanelCount
} from '../resource_panel/panel';
import { search_resource_by_tags as searchResourceByTags } from '../resource_shortcut/resource_shortcut';
import { search_all_resource_share_object as searchAllResourceShareObject } from '../share_resources/share_resources';

interface IResourceDetail {
  resource_name: string;
  resource_parent_id?: string;
  id?: string;
  resource_desc?: string;
  resource_language?: string;
  resource_type_cn?: string;
  resource_size_in_MB?: number;
  resource_type?: string;
  sub_resource_dir_cnt?: number;
  sub_resource_file_cnt?: number;
  author_info?: object;
  access_list?: string[];
  resource_path?: string;
  create_time?: string;
  rag_status?: object[];
  resource_tags?: any[];
  resource_status?: string;
  user_id?: string;
}

const route = useRoute();
const router = useRouter();
const initResource = { resource_name: '共享资源', resource_desc: '共享资源' };
const myResource = { resource_name: '我的资源', resource_desc: '我的资源' };
const resourceDetail = ref<IResourceDetail>(initResource);
const isShowEdit = ref(false);
const isLoading = ref(false);
const isLoadingTags = ref(false);
const isShowMeta = ref(false);
const showRebuildButton = ref(false);
const uncommitNotice = ref(false);
const resourceTags = ref<ResourceTag[]>([]);
const currentResourceId = useSessionStorage('currentResourceId', '');
const nowResourceId = computed(() => {
  return currentResourceId.value || route.params.resource_id;
});

onMounted(() => {
  if (route.name === 'resource_share') {
    resourceDetail.value = initResource;
  } else {
    resourceDetail.value = myResource;
  }
  getResourceDetail();
});

onBeforeUnmount(() => {
  sessionStorage.removeItem('currentResourceId');
});

watch(nowResourceId, newVal => {
  if (!newVal) {
    if (route.name === 'resource_share') {
      resourceDetail.value = initResource;
    } else {
      resourceDetail.value = myResource;
    }
  } else {
    getResourceDetail();
  }
});

async function getResourceDetail() {
  if (!nowResourceId.value) {
    return;
  }
  const params = {
    resource_id: nowResourceId.value ?? ''
  };
  const isShare = route.name === 'resource_share';
  let res;
  if (isShare) {
    res = await resourceShareGetMeta(params);
  } else {
    res = await getResourceObject(params);
  }
  if (!res.error_status) {
    const result = res.result;
    resourceDetail.value = result;
    resourceDetail.value.rag_status = result?.rag_status;
    resourceTags.value = result.resource_tags;
    showRebuildButton.value =
      result.rag_status.length === 0 ? true : result.rag_status.some(item => item.status === 'Success');
  }
}

async function editResource() {
  if (resourceDetail.value.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 检查是否有编辑和修改权限
  if (resourceDetail.value.user_id == useInfo.value.user_id || resourceDetail.value?.access_list?.includes('管理')) {
    isShowEdit.value = !isShowEdit.value;
    return;
  }
  ElMessage.warning('需要管理权限!');
}

async function cancelEdit() {
  const res = await getResourceObject({
    resource_id: resourceDetail.value.id
  });
  if (!res.error_status) {
    resourceDetail.value.resource_name = res.result.resource_name;
    resourceDetail.value.resource_desc = res.result.resource_desc;
    resourceDetail.value.resource_language = res.result.resource_language;
    resourceDetail.value.resource_tags = res.result.resource_tags;
  }
  isShowEdit.value = false;
}

async function rebuildResource() {
  if (!resourceDetail.value?.id) {
    ElMessage.warning('资源不存在!');
    return;
  }
  if (resourceDetail.value.resource_status == '删除') {
    ElMessage.warning('资源已删除，请先恢复后再操作!');
    return;
  }
  // 检查资源状态
  if (resourceDetail.value.resource_status != '正常') {
    ElMessage.warning('资源无法构建索引!');
    return;
  }

  let params = {
    resource_list: [resourceDetail.value.id]
  };
  let res = await buildResourceObjectRef(params);
  if (!res.error_status) {
    ElNotification({
      title: '系统通知',
      message: `成功提交重新构建任务，请耐心等待！`,
      type: 'success',
      duration: 5000
    });
  }
}

async function searchResourceTags(query: string) {
  if (query === '') {
    return;
  }
  let params = {
    tag_keyword: query,
    fetch_all: true
  };
  isLoadingTags.value = true;
  let res = await searchAllResourceTags(params);
  if (!res.error_status) {
    isLoadingTags.value = res.result;
    resourceTags.value = res.result;
  }
  isLoadingTags.value = false;
}

async function updateResource() {
  const params = {
    resource_id: resourceDetail.value.id,
    resource_name: resourceDetail.value.resource_name,
    resource_desc: resourceDetail.value.resource_desc,
    resource_language: resourceDetail.value.resource_language,
    resource_tags: resourceDetail.value.resource_tags
  };
  const res = await updateResourceObject(params);
  if (!res.error_status) {
    isShowEdit.value = false;
    ElMessage.success('更新成功');
  }
  refreshPanelCount();
  initMyResourceTree();
  if (router.currentRoute.value.name === 'resource_list') {
    searchAllResourceObject();
  } else if (router.currentRoute.value.name === 'resource_shortcut') {
    searchResourceByTags();
  } else if (router.currentRoute.value.name === 'resource_share') {
    searchAllResourceShareObject();
  }
}
</script>

<style scoped lang="scss">
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
#resource-meta-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 16px;
  height: 24px;
  width: calc(100% - 32px);
  border-bottom: 1px solid #d0d5dd;
}

#resource-meta-area {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

#resource-meta-foot {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  height: 32px;
  width: 100%;
  gap: 16px;
}
.resource-meta-foot-button {
  display: flex;
  flex-direction: row;
  justify-content: center;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid #d0d5dd;
  box-shadow: 0 1px 2px 0 #1018280d;
  width: calc(100% - 24px);
  height: 20px;
  cursor: pointer;
}
.resource-meta-foot-button-text {
  line-height: 20px;
  font-size: 14px;
  font-weight: 600;
  color: #344054;
}
#resource-meta-main {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: calc(100% - 24px);
  background-color: white;
  gap: 12px;
  margin-right: 12px;
}
#resource-meta-icon {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 40px;
  gap: 8px;
  width: 100%;
  position: relative;
}
#meta-edit-icon {
  position: absolute;
  right: 16px;
  cursor: pointer;
}
#resource-meta-divider {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background-color: #eff8ff;
  border: 1px solid #b2ddff;
  cursor: default;
  border-radius: 8px;
}
#resource-static {
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-bottom: 1px solid #d0d5dd;
  padding: 16px 0;
}
.resource-static-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
}
.resource-static-item-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  width: 160px;
  gap: 8px;
}
.resource-static-label {
  font-size: 14px;
  line-height: 20px;
  font-weight: 400;
  color: #667085;
}
.resource-static-item-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  gap: 12px;
}
.resource-static-value {
  font-size: 14px;
  line-height: 20px;
  font-weight: 400;
  color: #101828;
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

:deep(.el-select--large .el-select__wrapper) {
  min-height: 160px;
  align-items: flex-start;
}

.resource-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
#resource-icon {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  min-height: 100px;
}
.meta-icon {
  width: 36px;
  height: 36px;
}
@media (width < 768px) {
  .resource-static-item-right {
    flex-direction: column;
    gap: 4px;
  }
}
.gxh-el-select {
  :deep(.el-select__placeholder) {
    position: static;
    transform: inherit;
  }
}
.input-nowrap {
  :deep(.el-textarea__inner) {
    overflow: auto; /* 启用滚动 */
    -ms-overflow-style: none; /* IE 和 Edge */
    scrollbar-width: none; /* Firefox */
    /* WebKit 浏览器 */
    &::-webkit-scrollbar {
      display: none; /* 隐藏滚动条 */
    }
  }
}
</style>
