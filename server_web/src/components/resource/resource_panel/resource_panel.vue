<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import { useRoute, useRouter } from 'vue-router';
import {
  add_new_user_tag,
  all_search_user_tags,
  current_resource_usage,
  current_resource_usage_percent,
  current_search_choose_tag,
  delete_choose_user_tag,
  edit_new_user_tag,
  edit_tag_dialog_flag,
  edit_tag_form_data,
  edit_tag_form_Ref,
  get_current_resource_usage,
  get_my_resource_tree,
  get_recent_data_count,
  get_resource_data_count,
  get_share_resource_tree,
  handle_search_clear,
  handleFolderSelect,
  init_my_resource_tree,
  init_share_resource_tree,
  init_system_tags,
  init_upload_manager,
  init_user_tags,
  load_all_flag,
  load_all_tags,
  loading_tags_flag,
  my_resource_tree_data,
  my_resource_tree_props,
  new_tag_dialog_flag,
  new_tag_form_data,
  new_tag_form_Ref,
  panel_recent_shortcuts,
  panel_show_label_area,
  panel_show_my_resources_area,
  panel_show_recent_area,
  panel_show_share_resources_area,
  panel_system_labels,
  panel_user_labels,
  panel_width,
  pick_search_resource_tag,
  rag_enhance,
  resource_keyword,
  router_share_resource,
  router_to_recycle_bin,
  router_to_resource,
  router_to_resource_system_tag,
  router_to_resource_user_tag,
  router_to_search_page,
  router_to_share_resource,
  search_resource_tags_by_keyword,
  share_resource_tree_data,
  show_resource_progress_status,
  switch_on_edit_tag_dialog,
  switch_on_new_tag_dialog,
  switch_panel,
  triggerFolderInput,
  folderInput,
  upload_file_Ref,
  tag_color_list,
  show_upload_button
} from '@/components/resource/resource_panel/panel';
import { onMounted, ref, watch } from 'vue';
import { user_info } from '@/components/user_center/user';
import { format_resource_size, get_resource_icon } from '@/components/resource/resource_list/resource_list';
import { getInfo } from '@/utils/auth';
import { Search } from '@element-plus/icons-vue';
import { current_tag } from '@/components/resource/resource_shortcut/resource_shortcut';
import {
  prepare_upload_files,
  upload_file_content,
  upload_file_list
} from '@/components/resource/resource_upload/resource_upload';
import Resource_upload_manager from '@/components/resource/resource_upload/resource_upload_manager.vue';

const dialog_width = ref(window.innerWidth < 500 ? '90%' : '500px');
const router = useRouter();
const route = useRoute();
const isShowResourcePanel = useSessionStorage('isShowResourcePanel', true);
const shareResourceActive = ref(route.name === 'resource_share');
const myResourceActive = ref(route.name === 'resource_list');
const showRecentArea = useSessionStorage('showRecentArea', false);
const showLabelArea = useSessionStorage('showLabelArea', false);

panel_width.value = isShowResourcePanel.value ? '400px' : '0px';

onMounted(async () => {
  init_system_tags();
  get_current_resource_usage();
  get_recent_data_count();
  init_my_resource_tree();
  init_share_resource_tree();
  init_user_tags();
  get_resource_data_count();
  user_info.value = await getInfo(true);
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

function switchPanel() {
  isShowResourcePanel.value = false;
  switch_panel();
}

defineOptions({
  name: 'ResourcePanel'
});
</script>

<template>
  <div id="resource_panel_box" @contextmenu.prevent>
    <div id="panel_head">
      <div id="panel_head_left">
        <div class="std-middle-box" style="cursor: pointer" @click="switchPanel">
          <el-tooltip :content="$t('openSidebar')" effect="light">
            <el-image src="images/layout_alt.svg" style="width: 16px; height: 16px" />
          </el-tooltip>
        </div>
        <div class="std-middle-box" @click="router.push({ name: 'resource_list' })" style="width: 200px">
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
          :status="show_resource_progress_status()"
        />
        <el-text>{{ current_resource_usage }}M/{{ format_resource_size(user_info?.user_resource_limit) }}</el-text>
      </div>
    </div>
    <div id="panel_face">
      <div id="panel_recent_area">
        <div id="panel_recent_head">
          <div class="std-middle-box">
            <el-text>最近</el-text>
          </div>
          <div class="std-middle-box" style="cursor: pointer" @click="showRecentArea = !showRecentArea">
            <el-image v-show="showRecentArea" src="images/panel_arrow_down.svg" style="width: 16px; height: 16px" />
            <el-image v-show="!showRecentArea" src="images/panel_arrow_up.svg" style="width: 16px; height: 16px" />
          </div>
        </div>
        <div v-show="showRecentArea" id="panel_recent_body">
          <div
            v-for="shortcut in panel_recent_shortcuts"
            :key="shortcut.id"
            class="recent-shortcut"
            :class="
              current_tag?.tag_source == 'system' && current_tag.tag_value == shortcut.tag_value
                ? 'recent-shortcut-active'
                : ''
            "
            @click="router_to_resource_system_tag(shortcut)"
          >
            <div class="recent-shortcut-left">
              <div class="std-middle-box">
                <el-image :src="shortcut.tag_icon" style="width: 20px; height: 20px" />
              </div>
              <div class="std-middle-box">
                <el-text>{{ shortcut.tag_name }}</el-text>
              </div>
            </div>

            <div v-show="shortcut.tag_count" class="recent-shortcut-cnt">
              <el-text style="color: #1570ef; font-weight: 500; font-size: 12px; line-height: 18px">
                {{ shortcut.tag_count }}
              </el-text>
            </div>
          </div>
        </div>
      </div>
      <div id="panel_recent_area">
        <div id="panel_recent_head">
          <div class="std-middle-box">
            <el-text> 标签 </el-text>
          </div>
          <div id="panel_label_head_buttons">
            <div class="panel_label_head_button">
              <el-select
                size="small"
                style="width: 200px"
                placeholder="搜索标签"
                filterable
                clearable
                remote
                :loading="loading_tags_flag"
                value-key="id"
                v-model="current_search_choose_tag"
                :remote-show-suffix="true"
                :remote-method="search_resource_tags_by_keyword"
                @change="pick_search_resource_tag()"
              >
                <template #prefix>
                  <el-image style="width: 16px; height: 16px" src="images/search_label.svg" />
                </template>
                <el-option
                  v-for="item in all_search_user_tags"
                  :key="item.id"
                  :label="item.tag_name"
                  :value="item"
                  style="width: 180px"
                >
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
            <div class="panel_label_head_button" @click="switch_on_new_tag_dialog()">
              <el-image style="width: 16px; height: 16px" src="images/add_label.svg" />
            </div>
            <div class="panel_label_head_button" @click="showLabelArea = !showLabelArea">
              <el-image v-show="showLabelArea" src="images/panel_arrow_down.svg" style="width: 16px; height: 16px" />
              <el-image v-show="!showLabelArea" src="images/panel_arrow_up.svg" style="width: 16px; height: 16px" />
            </div>
          </div>
        </div>
        <div id="panel_label_body" v-show="showLabelArea">
          <div id="system_label_area">
            <div
              class="system-label"
              v-for="(system_label, idx) in panel_system_labels"
              :class="
                current_tag?.tag_source == 'system' && current_tag.tag_value == system_label.tag_value
                  ? 'system-label-active'
                  : ''
              "
              @click="router_to_resource_system_tag(system_label)"
            >
              <div class="std-middle-box">
                <div class="std-middle-box">
                  <el-image :src="system_label.tag_icon" style="width: 20px; height: 20px" />
                </div>
                <div class="std-middle-box">
                  <el-text>{{ system_label.tag_name }}</el-text>
                </div>
              </div>

              <div v-show="system_label.tag_count" class="recent-shortcut-cnt">
                <el-text style="color: #1570ef; font-weight: 500; font-size: 12px; line-height: 18px">
                  {{ system_label.tag_count }}
                </el-text>
              </div>
            </div>
          </div>
          <el-scrollbar style="width: 100%">
            <div id="user_label_area">
              <div
                class="user-label"
                v-for="(user_label, idx) in panel_user_labels"
                @click="router_to_resource_user_tag(user_label)"
                :class="user_label.tag_active ? 'user-label-active' : ''"
              >
                <div class="user-label-left">
                  <div class="user-label-color" :style="{ background: user_label.tag_color }" />
                  <div class="std-middle-box">
                    <el-text truncated style="max-width: 80px">
                      {{ user_label.tag_name }}
                    </el-text>
                  </div>
                  <div v-show="user_label?.tag_count" class="recent-shortcut-cnt">
                    <el-text style="color: #1570ef; font-weight: 500; font-size: 12px; line-height: 18px">
                      {{ user_label?.tag_count }}
                    </el-text>
                  </div>
                </div>

                <div
                  class="std-middle-box"
                  v-show="user_label.tag_active"
                  @click="switch_on_edit_tag_dialog(user_label, $event)"
                >
                  <el-image src="images/edit_label.svg" style="width: 16px; height: 16px" />
                </div>
              </div>
              <div v-show="!panel_user_labels.length" class="std-middle-box">
                <el-empty description="快来创建第一个资源标签吧" :image-size="80"></el-empty>
              </div>
            </div>
          </el-scrollbar>
        </div>
        <div id="panel_label_foot" v-show="showLabelArea && !load_all_flag" @click="load_all_tags()">
          <el-text class="show-all-button">加载全部标签</el-text>
        </div>
      </div>
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
                <el-image src="images/my_resources.svg" style="width: 24px; height: 24px" />
              </div>
              <div class="std-middle-box">
                <el-text style="font-size: 16px; font-weight: 600; line-height: 24px; color: #101828">
                  我的资源
                </el-text>
              </div>
            </div>
            <div class="menu-icon-box" @click="panel_show_my_resources_area = !panel_show_my_resources_area">
              <el-image v-show="panel_show_my_resources_area" src="images/panel_arrow_down.svg" class="menu-icon" />
              <el-image v-show="!panel_show_my_resources_area" src="images/panel_arrow_up.svg" class="menu-icon" />
            </div>
          </div>

          <div v-show="panel_show_my_resources_area">
            <el-tree
              :data="my_resource_tree_data"
              :lazy="true"
              :load="get_my_resource_tree"
              :props="my_resource_tree_props"
              :expand-on-click-node="false"
              :check-strictly="true"
              :highlight-current="true"
              ref="resource_tree_Ref"
            >
              <template #default="{ node, data }">
                <div
                  @click="router_to_resource(node)"
                  style="
                    display: flex;
                    flex-direction: row;
                    gap: 6px;
                    width: 100%;
                    align-items: center;
                    justify-content: flex-start;
                  "
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
            <div class="resource-router-title-left" @click="router_share_resource()">
              <div class="std-middle-box">
                <el-image src="images/share_resources.svg" style="width: 24px; height: 24px" />
              </div>
              <div class="std-middle-box">
                <el-text style="font-size: 16px; font-weight: 600; line-height: 24px; color: #101828">
                  共享资源
                </el-text>
              </div>
            </div>
            <div class="menu-icon-box" @click="panel_show_share_resources_area = !panel_show_share_resources_area">
              <el-image src="images/panel_arrow_down.svg" v-show="panel_show_share_resources_area" class="menu-icon" />
              <el-image src="images/panel_arrow_up.svg" v-show="!panel_show_share_resources_area" class="menu-icon" />
            </div>
          </div>
          <div v-show="panel_show_share_resources_area">
            <el-scrollbar>
              <el-tree
                :data="share_resource_tree_data"
                :lazy="true"
                :load="get_share_resource_tree"
                :props="my_resource_tree_props"
                :expand-on-click-node="false"
                :check-strictly="true"
                :highlight-current="true"
                ref="share_resource_tree_Ref"
              >
                <template #default="{ node, data }">
                  <div
                    @click="router_to_share_resource(node)"
                    style="
                      display: flex;
                      flex-direction: row;
                      gap: 6px;
                      width: 100%;
                      align-items: center;
                      justify-content: flex-start;
                    "
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
            placeholder="资源搜索"
            v-model="resource_keyword"
            clearable
            @clear="handle_search_clear()"
            @change="
              val => {
                if (val == '') {
                  handle_search_clear();
                }
              }
            "
            @keydown.enter="router_to_search_page"
          >
            <template #prefix>
              <el-icon style="cursor: pointer" @click="router_to_search_page">
                <Search />
              </el-icon>
            </template>
            <template #suffix>
              <div class="std-middle-box">
                <el-switch v-model="rag_enhance" active-text="内容检索" style="margin-right: 6px"></el-switch>
                <el-tooltip effect="dark" placement="top">
                  <template #default>
                    <div class="std-middle-box">
                      <el-image src="images/tooltip.svg" style="width: 16px; height: 16px" />
                    </div>
                  </template>
                  <template #content> 基于内容理解的深度搜索，提供更精准的搜索结果 </template>
                </el-tooltip>
              </div>
            </template>
          </el-input>
        </div>
        <el-popover trigger="click" width="160px" ref="show_upload_button">
          <template #reference>
            <div id="panel_upload_button">
              <div class="std-middle-box">
                <el-image src="images/upload_white.svg" style="width: 20px; height: 20px" />
              </div>
              <div class="std-middle-box">
                <el-text style="color: white; font-weight: 600; line-height: 20px; font-size: 14px">上传</el-text>
              </div>
            </div>
          </template>

          <template #default>
            <div id="upload-method-area">
              <el-upload
                multiple
                :show-file-list="false"
                :auto-upload="true"
                name="chunk_content"
                v-model:file-list="upload_file_list"
                :before-upload="prepare_upload_files"
                :on-change="init_upload_manager"
                :http-request="upload_file_content"
                :disabled="current_resource_usage_percent >= 100"
                accept="*"
                ref="upload_file_Ref"
                action=""
              >
                <div class="upload-method-button">
                  <div class="std-middle-box">
                    <el-image src="images/upload_local.svg" style="width: 20px; height: 20px" />
                  </div>
                  <div class="std-middle-box">
                    <el-text style="width: 90px">上传本地资源</el-text>
                  </div>
                </div>
              </el-upload>

              <div class="upload-method-button" @click="triggerFolderInput">
                <div class="std-middle-box">
                  <el-image src="images/upload_local_dir.svg" style="width: 20px; height: 20px" />
                </div>
                <div class="std-middle-box">
                  <el-text style="width: 80px">上传文件夹</el-text>
                </div>
                <div class="std-middle-box">
                  <input
                    type="file"
                    webkitdirectory
                    @change="handleFolderSelect"
                    style="display: none"
                    ref="folderInput"
                  />
                </div>
              </div>
            </div>
          </template>
        </el-popover>
      </div>
      <div id="panel_foot_body">
        <div class="panel_foot_button" style="border-right: 1px solid #d0d5dd" v-if="false">
          <div class="std-middle-box">
            <el-image src="images/storage_manager.svg" style="width: 24px; height: 24px" />
          </div>
          <div class="std-middle-box">
            <el-text>存储管理</el-text>
          </div>
        </div>
        <div class="panel_foot_button" @click="router_to_recycle_bin()">
          <div class="std-middle-box">
            <el-image src="images/trash_area.svg" style="width: 24px; height: 24px" />
          </div>
          <div class="std-middle-box">
            <el-text>回收站</el-text>
          </div>
        </div>
      </div>
    </div>
  </div>
  <el-dialog title="新增标签" v-model="new_tag_dialog_flag" style="max-width: 500px">
    <el-form
      :model="new_tag_form_data"
      label-position="top"
      ref="new_tag_form_Ref"
      :rules="{
        tag_name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }],
        tag_color: [{ required: true, message: '请选择一个喜欢的颜色', trigger: 'blur' }]
      }"
    >
      <el-form-item prop="tag_name" label="标签名称">
        <el-input v-model="new_tag_form_data.tag_name" />
      </el-form-item>
      <el-form-item prop="tag_desc" label="标签描述">
        <el-input v-model="new_tag_form_data.tag_desc" type="textarea" resize="none" :rows="4" />
      </el-form-item>
      <el-form-item prop="tag_color" label="标签颜色">
        <el-select v-model="new_tag_form_data.tag_color" :default-first-option="true">
          <template #prefix>
            <el-tag :color="new_tag_form_data.tag_color" round></el-tag>
          </template>
          <el-option v-for="(tag_color, idx) in tag_color_list" :value="tag_color.value" :label="tag_color.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <div class="std-middle-box" style="width: 100%; gap: 24px">
          <el-button @click="new_tag_dialog_flag = false" style="width: 100%"> 取消 </el-button>
          <el-button type="primary" @click="add_new_user_tag()" style="width: 100%"> 确认 </el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog title="编辑标签" v-model="edit_tag_dialog_flag" style="max-width: 500px" :width="dialog_width">
    <el-form
      :model="edit_tag_form_data"
      label-position="top"
      ref="edit_tag_form_Ref"
      :rules="{
        tag_name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }],
        tag_color: [{ required: true, message: '请选择一个喜欢的颜色', trigger: 'blur' }]
      }"
    >
      <el-form-item prop="tag_name" label="标签名称">
        <el-input v-model="edit_tag_form_data.tag_name" />
      </el-form-item>
      <el-form-item prop="tag_desc" label="标签描述">
        <el-input v-model="edit_tag_form_data.tag_desc" type="textarea" resize="none" :rows="4" />
      </el-form-item>
      <el-form-item prop="tag_color" label="标签颜色">
        <el-select v-model="edit_tag_form_data.tag_color" :default-first-option="true">
          <template #prefix>
            <el-tag :color="edit_tag_form_data.tag_color" round></el-tag>
          </template>
          <el-option v-for="(tag_color, idx) in tag_color_list" :value="tag_color.value" :label="tag_color.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <div class="std-middle-box" style="width: 100%; gap: 24px">
          <el-popconfirm @confirm="delete_choose_user_tag()" title="该操作不可回退，确认删除该标签？">
            <template #reference>
              <el-button style="width: 100%" type="danger"> 删除 </el-button>
            </template>
          </el-popconfirm>

          <el-button type="primary" @click="edit_new_user_tag()" style="width: 100%"> 确认 </el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
  <div id="resource_upload_manage_box">
    <resource_upload_manager />
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
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  gap: 36px;
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
  padding: 12px 16px;
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
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
}
.recent-shortcut {
  width: calc(50% - 20px);
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
  border: 1.5px solid #1570ef;
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
  gap: 8px;
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
  flex-direction: row;
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
  padding: 12px 16px;
  width: calc(100% - 32px);
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
  padding: 12px 16px;
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
