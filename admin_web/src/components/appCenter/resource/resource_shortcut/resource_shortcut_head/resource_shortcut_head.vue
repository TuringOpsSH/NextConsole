<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import { storeToRefs } from 'pinia';
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import {
  current_resource_cnt,
  current_tag,
  resource_view_model,
  search_resource_by_tags,
  setCurrentResourceValues
} from '@/components/resource/resource_shortcut/resource_shortcut';
import {
  all_resource_formats,
  all_resource_tags,
  all_resource_types,
  checkAll,
  confirm_update_keyword,
  current_resource_formats,
  current_resource_tags,
  current_resource_types,
  edit_search_keyword_flag,
  handleCheckAllChange,
  init_all_resource_formats,
  isIndeterminate,
  loading_user_tags,
  search_resource_tags_by_keyword,
  show_search_config_area,
  show_search_config_area_flag,
  switch_edit_search_keyword_dialog,
  switch_resource_layout,
  switch_show_resource_meta,
  system_tags_filter_change,
  update_rag_enhance,
  update_resource_keyword
} from '@/components/resource/resource_shortcut/resource_shortcut_head/resource_shortcut_head';
import { show_meta_flag } from '@/components/resource/resource_meta/resource_meta';
import Resource_clipboard from '@/components/resource/resource_clipborad/resource_clipboard.vue';
import { handle_search_clear } from '@/components/resource/resource_panel/panel';
import { useResourceStore } from '@/stores/resourceStore';
import { AUTH_TYPE, RESOURCE_FORMATS } from '@/utils/constant';

const resourceStore = useResourceStore();
const phone_view = ref(window.innerWidth < 768);
const dialog_width = ref(window.innerWidth < 768 ? '90%' : '400px');
const route = useRoute();
const { authType } = storeToRefs(resourceStore);
const needAuthType = ref(route.name === 'resource_search');
const currentResourceValues = useSessionStorage('currentResourceValues', []);
const showResourceFormat = ref(true);

function changeResourceFormat(value: string[]) {
  currentResourceValues.value = value;
  setTimeout(() => {
    search_resource_by_tags();
  }, 0);
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
  init_all_resource_formats();
});

onBeforeUnmount(() => {
  authType.value = '';
  setCurrentResourceValues([]);
  sessionStorage.removeItem('currentResourceValues');
});

defineOptions({
  name: 'ResourceShortcutHead'
});
</script>

<template>
  <div id="resource_header_area">
    <div
      id="resource_header"
      :style="{
        'box-shadow': show_search_config_area_flag ? '0 2px 4px 0 rgba(0, 0, 0, .1)' : 'none'
      }"
    >
      <div id="resource_path">
        <el-image
          v-show="current_tag?.tag_value == 'search'"
          src="images/back.svg"
          style="width: 20px; height: 20px; margin-right: 12px; cursor: pointer"
          @click="handle_search_clear()"
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
          src="images/edit_label.svg"
          @click="switch_edit_search_keyword_dialog()"
        >
        </el-image>
      </div>

      <div id="resource_layout_change" class="resource-head-button2" style="" v-if="!phone_view">
        <div
          id="resource_layout_change_left"
          @click="switch_resource_layout('list')"
          :style="{ background: resource_view_model == 'list' ? '#D1E9FF' : '#F2F4F7' }"
        >
          <el-tooltip content="列表模式" effect="light">
            <el-image
              src="images/list_layout_active.svg"
              class="resource-head-button-icon"
              v-if="resource_view_model == 'list'"
            />
            <el-image src="images/list_layout.svg" class="resource-head-button-icon" v-else />
          </el-tooltip>
        </div>
        <div
          id="resource_layout_change_right"
          @click="switch_resource_layout('card')"
          :style="{ background: resource_view_model == 'card' ? '#D1E9FF' : '#F2F4F7' }"
        >
          <el-tooltip content="卡片模式" effect="light">
            <el-image
              src="images/card_layout_active.svg"
              class="resource-head-button-icon"
              v-if="resource_view_model == 'card'"
            />
            <el-image src="images/card_layout.svg" class="resource-head-button-icon" v-else />
          </el-tooltip>
        </div>
      </div>

      <div id="resource_head_buttons">
        <resource_clipboard v-if="false" />
        <div
          v-if="!phone_view"
          class="resource-head-button"
          :style="{
            background: show_search_config_area_flag ? '#EFF8FF' : '#F2F4F7'
          }"
          @click="show_search_config_area()"
        >
          <el-tooltip v-if="show_search_config_area_flag" effect="light" :content="$t('resourceList')">
            <el-image src="images/search_config_active.svg" class="resource-head-button-icon" />
          </el-tooltip>
          <el-tooltip v-else effect="light" :content="$t('resourceList')">
            <el-image src="images/search_config.svg" class="resource-head-button-icon" />
          </el-tooltip>
        </div>
        <div
          class="resource-head-button"
          :style="{
            background: show_meta_flag ? '#EFF8FF' : '#F2F4F7'
          }"
          @click="switch_show_resource_meta()"
        >
          <el-tooltip effect="light" :content="$t('resourceDetails')">
            <el-image
              v-show="show_meta_flag"
              src="images/switch_resource_detail_active.svg"
              class="resource-head-button-icon"
            />
          </el-tooltip>
          <el-tooltip effect="light" :content="$t('resourceDetails')">
            <el-image
              v-show="!show_meta_flag"
              src="images/switch_resource_detail.svg"
              class="resource-head-button-icon"
            />
          </el-tooltip>
        </div>
      </div>
    </div>
    <el-scrollbar style="width: 100%">
      <div v-show="show_search_config_area_flag" id="search_config_area" v-if="!phone_view">
        <div id="search_config_area_top" v-show="current_tag?.tag_type != 'resource_type'">
          <div class="std-middle-box">
            <el-text style="min-width: 60px">资源类型 </el-text>
          </div>
          <div class="std-middle-box" style="gap: 12px">
            <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange"
              >全选</el-checkbox
            >
            <el-checkbox-group v-model="current_resource_types" @change="system_tags_filter_change()">
              <el-checkbox v-for="item in all_resource_types" :value="item.value" :label="item.name" />
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
                multiple
                placeholder="搜索标签"
                filterable
                remote
                reserve-keyword
                :loading="loading_user_tags"
                v-model="current_resource_tags"
                collapse-tags
                collapse-tags-tooltip
                @change="system_tags_filter_change()"
                value-key="id"
                clearable
                :remote-method="search_resource_tags_by_keyword"
              >
                <el-option v-for="item in all_resource_tags" :key="item.id" :label="item.tag_name" :value="item">
                  <div class="user-tag-area">
                    <div class="std-middle-box">
                      <el-image class="user-label-color" :src="item?.tag_icon" v-if="item?.tag_icon" />
                      <div class="user-label-color" :style="{ background: item?.tag_color }" v-else />
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
                  :value="resourceFormat.value"
                  :label="resourceFormat.text"
                  :key="resourceFormat.value"
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
    </el-scrollbar>
  </div>
  <el-dialog title="资源搜索" v-model="edit_search_keyword_flag" :width="dialog_width">
    <div id="update_search_keyword_area">
      <div class="std-middle-box" style="width: 100%">
        <el-input
          v-model="update_resource_keyword"
          placeholder="请输入搜索意图"
          type="textarea"
          :rows="4"
          resize="none"
        />
      </div>
      <div class="std-middle-box">
        <el-switch v-model="update_rag_enhance" active-text="内容检索" style="margin-right: 6px"></el-switch>
      </div>
      <div class="std-middle-box" style="width: 100%">
        <el-button @click="edit_search_keyword_flag = false">取消</el-button>
        <el-button type="primary" @click="confirm_update_keyword()">确定</el-button>
      </div>
    </div>
  </el-dialog>
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

.search-box {
  margin-right: 10px;
}
</style>
