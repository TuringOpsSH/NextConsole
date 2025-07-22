<script setup lang="ts">
import { ArrowRight, Search } from '@element-plus/icons-vue';
import { useSessionStorage } from '@vueuse/core';
import { computed, inject, Ref, ref } from 'vue';
import ResourceClipboard from '@/components/resource/resource_clipborad/resource_clipboard.vue';
import {
  current_path_tree as currentPathTree,
  show_dir_meta_flag as showDirMetaFlag,
  switch_resource_layout as switchResourceLayout
} from '@/components/resource/share_resources/resource_head/resource_head';
import { show_share_resources as showShareResources } from '@/components/resource/share_resources/share_resources';
import { TResourceListStatus } from '@/types/resource_type';
const phoneView = ref(window.innerWidth < 768);
const hidePermission = useSessionStorage('hideShareResourcePermission', false);
const keyword = inject<Ref<string>>('keyword');
const searchPlaceholder = computed(() => {
  const lastPath = currentPathTree.value.at(-1)?.resource_name ?? '共享资源';
  const searchPlaceholder = lastPath?.length >= 8 ? `在 ${lastPath.slice(0, 8)}... 中搜索` : `在 ${lastPath} 中搜索`;
  return searchPlaceholder;
});
const shareListStatus = useSessionStorage<TResourceListStatus>('shareListStatus', 'card');
const showCardList = computed(() => {
  return shareListStatus.value === 'card';
});

interface IEmits {
  (e: 'handleSearch'): void;
  (e: 'handleClear'): void;
}

const emit = defineEmits<IEmits>();
defineOptions({
  name: 'ShareResourceHead'
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
            @click="showShareResources(item)"
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
          :style="{
            background: !showCardList ? '#D1E9FF' : '#F2F4F7'
          }"
          @click="shareListStatus = 'list'"
        >
          <el-tooltip content="列表模式" effect="light">
            <el-image v-if="!showCardList" src="images/list_layout_active.svg" class="resource-head-button-icon" />
            <el-image v-else src="images/list_layout.svg" class="resource-head-button-icon" />
          </el-tooltip>
        </div>
        <div
          id="resource_layout_change_right"
          :style="{
            background: showCardList ? '#D1E9FF' : '#F2F4F7'
          }"
          @click="shareListStatus = 'card'"
        >
          <el-tooltip content="卡片模式" effect="light">
            <el-image v-if="showCardList" src="images/card_layout_active.svg" class="resource-head-button-icon" />
            <el-image v-else src="images/card_layout.svg" class="resource-head-button-icon" />
          </el-tooltip>
        </div>
      </div>

      <div id="resource_head_buttons">
        <ResourceClipboard v-if="false" />
        <div class="resource-head-button">
          <!-- 搜索按钮 -->
          <el-input
            v-model="keyword"
            :style="{ width: '260px' }"
            clearable
            :placeholder="searchPlaceholder"
            @keyup.enter="emit('handleSearch')"
            @clear="emit('handleClear')"
          >
            <template #prefix>
              <el-icon @click="emit('handleSearch')"><Search /></el-icon>
            </template>
          </el-input>
        </div>
        <div
          class="resource-head-button"
          :style="{
            background: showDirMetaFlag ? '#EFF8FF' : '#F2F4F7'
          }"
          @click="hidePermission = !hidePermission"
        >
          <el-tooltip effect="light" :content="$t('resourceDetails')" placement="bottom">
            <el-image
              v-show="showDirMetaFlag"
              src="images/switch_resource_detail_active.svg"
              class="resource-head-button-icon"
            />
          </el-tooltip>
          <el-tooltip effect="light" :content="$t('resourceDetails')" placement="bottom">
            <el-image
              v-show="!showDirMetaFlag"
              src="images/switch_resource_detail.svg"
              class="resource-head-button-icon"
            />
          </el-tooltip>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
  border-bottom: 1px solid #d0d5dd;
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
  cursor: pointer;
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
}
#resource_layout_change_right {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background: #f2f4f7;
  padding: 4px 6px;
  border-radius: 0 8px 8px 0;
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
  gap: 32px;
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
  width: 100%;
}
#search_config_area_bottom {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
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
  #resource_header {
    border-bottom: none;
  }
}
</style>
