<script setup lang="ts">
import { ArrowRight, Search } from '@element-plus/icons-vue';
import { useSessionStorage } from '@vueuse/core';
import { storeToRefs } from 'pinia';
import { onUnmounted, ref, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import ResourceClipboard from '@/components/resource/resource_clipborad/resource_clipboard.vue';
import {
  add_dir_dialog_flag,
  add_document_flag,
  current_path_tree as currentPathTree,
  keyword,
  new_dir_form_Ref,
  show_add_dir_dialog,
  show_add_document_dialog,
  show_dir_meta_flag,
  handleSearch,
  refreshData
} from '@/components/resource/resource-list/resource_head/resource_head';
import {
  add_dir_resource,
  create_new_document,
  new_dir_resource_item,
  new_document_resource,
  show_resource_list,
  new_document_form_Ref
} from '@/components/resource/resource-list/resource-list';
import { useResourceListStore } from '@/stores/resourceListStore';
import { TResourceListStatus } from '@/types/resource-type';
import { ElTooltip } from 'element-plus';

const route = useRoute();
const resourceListStore = useResourceListStore();
const phoneView = ref(window.innerWidth < 768);
const dialogWidth = ref(window.innerWidth < 768 ? '90%' : '600px');
const resourceList = storeToRefs(useResourceListStore());
const hidePermission = useSessionStorage('hideResourcePermission', false);
const searchPlaceholder = computed(() => {
  const lastPath = currentPathTree.value.at(-1)?.resource_name ?? '我的资源';
  const searchPlaceholder = lastPath?.length >= 8 ? `在 ${lastPath.slice(0, 8)}... 中搜索` : `在 ${lastPath} 中搜索`;
  return searchPlaceholder;
});
const resourceListStatus = useSessionStorage<TResourceListStatus>('resourceListStatus', 'card');
const showCardList = computed(() => {
  return resourceListStatus.value === 'card';
});

async function handleClear() {
  resourceList.isSearchMode.value = false;
  await refreshData();
}

watch(keyword, async newVal => {
  if (newVal.length === 0) {
    resourceList.isSearchMode.value = false;
    await refreshData();
  }
});

watch(
  () => route.params.resource_id,
  newValue => {
    resourceList.resourceId.value = newValue as string;
  }
);

onUnmounted(() => {
  resourceListStore.$dispose();
  keyword.value = '';
});

const handleMouseEnter = (event, index) => {
  const target = event.target;
  currentPathTree.value[index].isOverflow = target.scrollWidth > target.clientWidth;
};
</script>

<template>
  <div id="resource_header_area">
    <div id="resource_header">
      <div id="resource_path">
        <el-breadcrumb
          :separator-icon="ArrowRight"
          style="display: flex; flex-direction: row; align-items: center; justify-content: flex-start"
        >
          <el-breadcrumb-item
            v-for="(item, index) in currentPathTree"
            :key="item.resource_id"
            @click="show_resource_list(item)"
          >
            <el-tooltip :content="item.resource_name" effect="light" :disabled="!item.isOverflow">
              <el-text
                truncated
                class="resource-sub-path"
                :class="{
                  'resource-sub-path-last': index == currentPathTree?.length - 1
                }"
                @mouseenter="handleMouseEnter($event, index)"
              >
                {{ item?.resource_name }}
              </el-text>
            </el-tooltip>
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>

      <div v-if="!phoneView" id="resource_layout_change" class="resource-head-button2">
        <div
          id="resource_layout_change_left"
          :style="{ background: !showCardList ? '#D1E9FF' : '#F2F4F7' }"
          @click="resourceListStatus = 'list'"
        >
          <el-tooltip content="列表模式" effect="light">
            <el-image v-if="!showCardList" src="/images/list_layout_active.svg" class="resource-head-button-icon" />
            <el-image v-else src="/images/list_layout.svg" class="resource-head-button-icon" />
          </el-tooltip>
        </div>
        <div
          id="resource_layout_change_right"
          :style="{ background: showCardList ? '#D1E9FF' : '#F2F4F7' }"
          @click="resourceListStatus = 'card'"
        >
          <el-tooltip content="卡片模式" effect="light">
            <el-image v-if="showCardList" src="/images/card_layout_active.svg" class="resource-head-button-icon" />
            <el-image v-else src="/images/card_layout.svg" class="resource-head-button-icon" />
          </el-tooltip>
        </div>
      </div>

      <div id="resource_head_buttons">
        <ResourceClipboard v-if="false" />
        <!-- 搜索按钮 -->
        <div class="resource-head-button">
          <el-input
            v-model="keyword"
            :style="{ width: '260px' }"
            clearable
            :placeholder="searchPlaceholder"
            @keyup.enter="handleSearch"
            @clear="handleClear"
          >
            <template #prefix>
              <el-icon @click="handleSearch"><Search /></el-icon>
            </template>
          </el-input>
        </div>
        <el-tooltip effect="light" content="新建文档" placement="top">
          <div
            class="resource-head-button"
            :style="{
              background: add_document_flag ? '#EFF8FF' : '#F2F4F7'
            }"
            @click="show_add_document_dialog()"
          >
            <el-image
              v-show="add_document_flag"
              src="/images/add_document_active.svg"
              class="resource-head-button-icon"
            />
            <el-image v-show="!add_document_flag" src="/images/add_document.svg" class="resource-head-button-icon" />
          </div>
        </el-tooltip>
        <el-tooltip effect="light" content="新建文件夹" placement="top">
          <div
            class="resource-head-button"
            :style="{
              background: add_dir_dialog_flag ? '#EFF8FF' : '#F2F4F7'
            }"
            @click="show_add_dir_dialog()"
          >
            <el-image
              v-show="add_dir_dialog_flag"
              src="/images/add_new_resource_active.svg"
              class="resource-head-button-icon"
            />
            <el-image
              v-show="!add_dir_dialog_flag"
              src="/images/add_new_resource.svg"
              class="resource-head-button-icon"
            />
          </div>
        </el-tooltip>
        <el-tooltip effect="light" content="资源详情" placement="top">
          <div
            class="resource-head-button"
            :style="{
              background: show_dir_meta_flag ? '#EFF8FF' : '#F2F4F7'
            }"
            @click="hidePermission = !hidePermission"
          >
            <el-image
              v-show="show_dir_meta_flag"
              src="/images/switch_resource_detail_active.svg"
              class="resource-head-button-icon"
            />
            <el-image
              v-show="!show_dir_meta_flag"
              src="/images/switch_resource_detail.svg"
              class="resource-head-button-icon"
            />
          </div>
        </el-tooltip>
      </div>
    </div>
  </div>

  <el-dialog v-model="add_dir_dialog_flag" title="新建文件夹" style="max-width: 600px" draggable :width="dialogWidth">
    <el-form
      :model="new_dir_resource_item"
      ref="new_dir_form_Ref"
      label-position="top"
      :rules="{
        resource_name: [{ required: true, message: '请输入文件夹名称', trigger: 'blur' }]
      }"
    >
      <el-form-item prop="resource_name" required label="文件夹名称">
        <el-input v-model="new_dir_resource_item.resource_name" placeholder="请输入文件夹名称" @keydown.enter.prevent />
      </el-form-item>
      <el-form-item prop="resource_desc" label="文件夹描述">
        <el-input
          placeholder="请输入文件夹描述"
          type="textarea"
          resize="none"
          :rows="3"
          show-word-limit
          v-model="new_dir_resource_item.resource_desc"
          maxlength="200"
        />
      </el-form-item>
      <el-form-item>
        <div id="button-area">
          <el-button type="primary" @click="add_dir_resource()">确定</el-button>
          <el-button @click="add_dir_dialog_flag = false">取消</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog v-model="add_document_flag" title="新建文档" style="max-width: 600px" draggable :width="dialogWidth">
    <el-form
      :model="new_document_resource"
      label-position="top"
      ref="new_document_form_Ref"
      :rules="{
        resource_name: [{ required: true, message: '请输入文档名称', trigger: 'blur' }],
        resource_format: [{ required: true, message: '请选择文档类型', trigger: 'blur' }]
      }"
    >
      <el-form-item prop="resource_name" required label="文档名称">
        <el-input v-model="new_document_resource.resource_name" placeholder="请输入文档名称" @keydown.enter.prevent />
      </el-form-item>
      <el-form-item prop="resource_desc" label="文档描述">
        <el-input
          placeholder="请输入文档描述"
          type="textarea"
          resize="none"
          :rows="3"
          show-word-limit
          v-model="new_document_resource.resource_desc"
          maxlength="200"
        />
      </el-form-item>
      <el-form-item prop="resource_format" label="文档类型" size="large">
        <el-radio-group v-model="new_document_resource.resource_format" style="gap: 12px">
          <el-radio value="docx">
            <div class="new_document_type">
              <el-image src="/images/docx.svg" class="document-format-icon" />
              <el-text>文字</el-text>
            </div>
          </el-radio>
          <el-radio value="xlsx">
            <div class="new_document_type">
              <el-image src="/images/xlsx.svg" class="document-format-icon" />
              <el-text>表格</el-text>
            </div>
          </el-radio>
          <el-radio value="pptx">
            <div class="new_document_type">
              <el-image src="/images/pptx.svg" class="document-format-icon" />
              <el-text>演示</el-text>
            </div>
          </el-radio>

          <el-radio value="otl">
            <div class="new_document_type">
              <el-image src="/images/otl.png" class="document-format-icon" />
              <el-text>智能文档</el-text>
            </div>
          </el-radio>
          <el-radio value="dbt">
            <div class="new_document_type">
              <el-image src="/images/dbt.png" class="document-format-icon" />
              <el-text>多维表格</el-text>
            </div>
          </el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <div id="button-area">
          <el-button type="primary" @click="create_new_document()">确定</el-button>
          <el-button @click="add_document_flag = false">取消</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

:deep(.el-textarea__inner::-webkit-scrollbar) {
  width: 4px;
  height: 6px;
}

:deep(.el-textarea__inner::-webkit-scrollbar-thumb) {
  border-radius: 3px;
  -moz-border-radius: 3px;
  -webkit-border-radius: 3px;
  background-color: #c3c3c3;
}

:deep(.el-textarea__inner::-webkit-scrollbar-track) {
  background-color: transparent;
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

#button-area {
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: center;
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

.resource-sub-path {
  cursor: pointer;
  font-size: 14px;
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

.new_document_type {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
}

.document-format-icon {
  width: 32px;
  height: 32px;
}

@media (width < 768px) {
  .resource-sub-path {
    cursor: pointer;
    font-size: 12px;
  }

  .resource-sub-path-last {
    font-weight: 600;
    font-size: 12px;
    line-height: 14px;
    color: #101828;
    cursor: default;
  }
}
</style>
