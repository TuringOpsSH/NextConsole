<script setup lang="ts">
import ShortCutHead from '@/components/resource/resource_shortcut/resource_shortcut_head/resource_shortcut_head.vue';
import { onMounted, ref } from 'vue';
import {
  double_click_resource_card,
  format_resource_size,
  get_resource_icon,
  sort_resource_size,
  sort_resource_status
} from '@/components/resource/resource_list/resource_list';
import Resource_view_tree from '@/components/resource/resource_tree/resource_view_tree.vue';
import {
  handleDrop,
  openCardContextMenu,
  openContextMenu,
  openTableContextMenu
} from '@/components/resource/resource_shortcut/resource_context_menu/context_menu';
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
  preview_resource,
  rebuild_resource,
  recover_resource,
  resource_loading,
  resource_shortcut_Ref,
  resource_view_model,
  search_rag_enhance,
  search_resource_by_tags,
  share_resource,
  show_delete_flag,
  show_delete_resource_detail,
  show_recover_flag,
  show_resource_detail,
  show_upload_progress_status
} from '@/components/resource/resource_shortcut/resource_shortcut';
import Resource_meta from '@/components/resource/resource_meta/resource_meta.vue';
import {
  all_resource_tags,
  current_resource_formats,
  current_resource_tags,
  current_resource_types,
  resource_head_height,
  show_search_config_area
} from '@/components/resource/resource_shortcut/resource_shortcut_head/resource_shortcut_head';
import Context_menu from '@/components/resource/resource_shortcut/resource_context_menu/context_menu.vue';
import { search_resource_tags } from '@/api/resource_api';
import { close_upload_manager } from '@/components/resource/resource_upload/resource_upload';
import { onBeforeRouteLeave } from 'vue-router';
import Resource_share_selector from '@/components/resource/resource_share_selector/resource_share_selector.vue';
import { user_info } from '@/components/user_center/user';
import Resource_empty from '@/components/resource/resource_empty/resource_empty.vue';

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
const dialog_width = ref(window.innerWidth < 768 ? '90%' : '600px');
const page_model = ref(
  window.innerWidth < 768 ? 'total, prev, pager, next, jumper' : 'total, sizes, prev, pager, next, jumper'
);

async function init_page() {
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
      all_resource_tags.value = res.result;
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
      current_resource_formats.value = [props.resource_format];
    } else {
      // @ts-ignore
      current_resource_formats.value = props.resource_format;
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
    page_model.value = 'total, prev, pager, next, jumper';
  }
  console.log(multiple_selection.value?.length);
}
onMounted(async () => {
  await init_page();
});
onBeforeRouteLeave((to, from, next) => {
  close_upload_manager();
  next();
  multiple_selection.value = [];
});

defineOptions({
  name: 'ResourceShortcut'
});
</script>

<template>
  <el-container>
    <el-header :height="resource_head_height + 'px'" style="padding: 0 !important">
      <ShortCutHead />
    </el-header>
    <el-main @contextmenu.prevent="openContextMenu" style="padding: 2px !important">
      <el-scrollbar style="width: 100%">
        <div
          id="resource_list_main"
          :style="{ height: 'calc(100vh - 61px - ' + resource_head_height + 'px)' }"
          v-loading="resource_loading"
          element-loading-text="加载中"
          @dragover.prevent="handleDragOver"
          @drop.prevent="handleDrop"
        >
          <template v-if="!resource_loading">
            <div v-show="resource_view_model == 'list'" id="list_model">
              <el-table
                :data="current_resource_list"
                :highlight-current-row="true"
                @row-contextmenu="openTableContextMenu"
                @selection-change="handle_selection_change"
                @select-all="handle_selection_change"
                :default-sort="{ prop: 'update_time', order: 'descending' }"
                ref="resource_shortcut_Ref"
                v-if="current_resource_list.length"
                border
                style="height: 100%;"
              >
                <el-table-column type="selection" width="55" class-name="resource-selection" />
                <el-table-column prop="resource_name" label="资源名称" min-width="200" show-overflow-tooltip sortable>
                  <template #default="scope">
                    <div class="resource-item-name">
                      <div
                        @dragstart="onDragStart"
                        @dragend="onDragEnd"
                        @dragover.prevent
                        :draggable="true"
                        class="resource-item-name-drag"
                        :id="scope.row.id"
                      >
                        <img :src="get_resource_icon(scope.row)" class="resource-icon" :id="scope.row.id" alt="" />
                      </div>
                      <div class="std-box" @click="preview_resource(scope.row)" style="cursor: pointer">
                        <el-text class="resource-name-text">
                          {{ scope.row.resource_name }}
                        </el-text>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="resource_desc" label="资源描述" min-width="120" show-overflow-tooltip sortable />
                <el-table-column
                  prop=""
                  label="资源来源"
                  min-width="200"
                  v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'search'"
                >
                  <template #default="scope">
                    <div class="std-box" v-if="scope.row.user_id == user_info?.user_id">
                      <el-avatar :src="user_info?.user_avatar" style="width: 16px; height: 16px" />
                      <el-text
                        style="width: 160px; font-size: 12px; font-weight: 500; line-height: 18px; color: #475467"
                        truncated
                      >
                        {{ user_info?.user_nick_name }}
                      </el-text>
                    </div>
                    <div class="std-box" v-else>
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
                  prop="delete_time"
                  label="删除时间"
                  min-width="160"
                  sortable
                  v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recycle_bin'"
                />
                <el-table-column prop="update_time" label="更新时间" min-width="160" sortable v-else />
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
                  prop="resource_tags"
                  label="资源标签"
                  min-width="200"
                  v-if="current_tag?.tag_source == 'user'"
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
                  prop="task_source"
                  label="上传来源"
                  min-width="120"
                  sortable
                  v-if="current_tag?.tag_source == 'system' && current_tag.tag_value == 'recent_upload'"
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
                  prop="left_time"
                  label="剩余天数"
                  min-width="160"
                  sortable
                  v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recycle_bin'"
                />
                <el-table-column
                  prop="update_time"
                  label="上传进度"
                  min-width="120"
                  sortable
                  v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recent_upload'"
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
                  prop="rag_status"
                  label="构建状态"
                  min-width="120"
                  v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recent_index'"
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
                  prop="rag_duration"
                  label="构建耗时"
                  min-width="120"
                  sortable
                  v-if="current_tag?.tag_source == 'system' && current_tag?.tag_value == 'recent_index'"
                >
                  <template #default="scope">
                    <div class="std-middle-box">
                      <el-text>
                        {{ get_timestamp_duration(scope.row.rag_duration) }}
                      </el-text>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="ref_text" label="关联文本" min-width="120" v-if="search_rag_enhance">
                  <template #default="scope">
                    <div class="std-box">
                      <el-tooltip effect="light">
                        <el-text
                          style="cursor: default"
                          class="resource-name-text"
                          v-html="getHighlightedText(scope.row.ref_text)"
                          truncated
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
                  prop="rerank_score"
                  label="相关度"
                  min-width="120"
                  show-overflow-tooltip
                  sortable
                  v-if="search_rag_enhance"
                />
                <el-table-column prop="" label="操作" min-width="60" class-name="resource-selection" fixed="right">
                  <template #default="scope">
                    <el-popover trigger="click" ref="button_Ref">
                      <template #reference>
                        <el-image src="images/dot_list_grey.svg" class="resource-icon2" />
                      </template>
                      <div class="resource-button-group" v-show="current_tag?.tag_value != 'recycle_bin'">
                        <div class="resource-button">
                          <el-button text @click="preview_resource(scope.row)" class="resource-button">
                            查看
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text @click="show_resource_detail(scope.row)" class="resource-button">
                            详情
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text @click="download_resource(scope.row)" class="resource-button">
                            下载
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text @click="share_resource(scope.row)" class="resource-button"> 分享 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text @click="move_resource(scope.row)" class="resource-button"> 移动到 </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text @click="rebuild_resource(scope.row)" class="resource-button">
                            重新索引
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text @click="delete_resource(scope.row)" type="danger" class="resource-button">
                            删除
                          </el-button>
                        </div>
                      </div>
                      <div class="resource-button-group" v-show="current_tag?.tag_value == 'recycle_bin'">
                        <div class="resource-button">
                          <el-button text @click="show_delete_resource_detail(scope.row)" class="resource-button">
                            详情
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button text @click="recover_resource(scope.row)" class="resource-button">
                            恢复
                          </el-button>
                        </div>
                        <div class="resource-button">
                          <el-button
                            text
                            @click="completely_delete_resource(scope.row)"
                            type="danger"
                            class="resource-button"
                          >
                            彻底删除
                          </el-button>
                        </div>
                      </div>
                    </el-popover>
                  </template>
                </el-table-column>
              </el-table>
              <resource_empty v-else />
            </div>
            <div v-show="resource_view_model == 'card'" id="card-model">
              <div
                v-for="item in current_resource_list"
                class="resource-item-card"
                :class="{ resource_selected: item.resource_is_selected }"
                @dblclick="double_click_resource_card(item)"
                @click="click_resource_card(item, $event)"
                @dragstart="onDragStart"
                @dragend="onDragEnd"
                @dragover.prevent
                draggable="true"
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
                    <div class="std-middle-box" @click="preview_resource(item)">
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
                      <el-popover trigger="click" :hide-after="0" ref="resource_shortcut_card_buttons_Ref">
                        <template #reference>
                          <el-image src="images/dot_list_grey.svg" class="resource-icon2" />
                        </template>
                        <div class="resource-button-group" v-show="current_tag?.tag_value != 'recycle_bin'">
                          <div class="resource-button">
                            <el-button text @click="preview_resource(item)" class="resource-button"> 查看 </el-button>
                          </div>
                          <div class="resource-button">
                            <el-button text @click="show_resource_detail(item)" class="resource-button">
                              详情
                            </el-button>
                          </div>
                          <div class="resource-button">
                            <el-button text @click="download_resource(item)" class="resource-button"> 下载 </el-button>
                          </div>
                          <div class="resource-button">
                            <el-button text @click="share_resource(item)" class="resource-button"> 分享 </el-button>
                          </div>
                          <div class="resource-button">
                            <el-button text @click="move_resource(item)" class="resource-button"> 移动到 </el-button>
                          </div>
                          <div class="resource-button">
                            <el-button text @click="rebuild_resource(item)" class="resource-button">
                              重新索引
                            </el-button>
                          </div>
                          <div class="resource-button">
                            <el-button text @click="delete_resource(item)" type="danger" class="resource-button">
                              删除
                            </el-button>
                          </div>
                        </div>
                        <div class="resource-button-group" v-show="current_tag?.tag_value == 'recycle_bin'">
                          <div class="resource-button">
                            <el-button text @click="show_delete_resource_detail(item)" class="resource-button">
                              详情
                            </el-button>
                          </div>

                          <div class="resource-button">
                            <el-button text @click="recover_resource(item)" class="resource-button"> 恢复 </el-button>
                          </div>
                          <div class="resource-button">
                            <el-button
                              text
                              @click="completely_delete_resource(item)"
                              type="danger"
                              class="resource-button"
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
                <resource_empty />
              </div>
            </div>
          </template>
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
              class="resource-foot-button"
              @click="batch_move_select_resources()"
              v-show="current_tag?.tag_value != 'recycle_bin'"
            >
              <el-text> 移动到 </el-text>
            </div>
            <div
              class="resource-foot-button"
              @click="batch_copy_select_resources()"
              v-if="false"
              v-show="current_tag?.tag_value != 'recycle_bin'"
            >
              <el-text> 复制 </el-text>
            </div>
            <div
              class="resource-foot-button"
              @click="show_recover_flag = true"
              v-show="current_tag?.tag_value == 'recycle_bin'"
            >
              <el-text> 恢复 </el-text>
            </div>
          </div>
          <div v-if="multiple_selection?.length > 0" id="resource_foot_middle">
            <div
              class="resource-foot-button"
              @click="batch_download_select_resource()"
              v-show="current_tag?.tag_value != 'recycle_bin'"
            >
              <el-text> 下载 </el-text>
            </div>
            <div
              class="resource-foot-button"
              @click="show_delete_flag = true"
              v-show="current_tag?.tag_value != 'recycle_bin'"
            >
              <el-text> 删除 </el-text>
            </div>
            <div
              class="resource-foot-button"
              @click="completely_delete_flag = true"
              v-show="current_tag?.tag_value == 'recycle_bin'"
            >
              <el-text> 彻底删除 </el-text>
            </div>
          </div>
          <div v-if="multiple_selection?.length > 0" id="resource_foot_right">
            <div class="resource-foot-button" @click="batch_rebuild()" v-show="current_tag?.tag_value != 'recycle_bin'">
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
              :layout="page_model"
              :total="current_resource_cnt"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </div>
      </el-scrollbar>
    </el-footer>
  </el-container>
  <Resource_meta />
  <resource_view_tree />
  <Context_menu />
  <resource_share_selector />

  <el-dialog v-model="show_delete_flag" title="删除资源" style="max-width: 600px" :width="dialog_width">
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
  <el-dialog v-model="show_recover_flag" title="恢复资源" style="max-width: 600px" :width="dialog_width">
    <div style="display: flex; flex-direction: column; gap: 16px; align-items: center; justify-content: center">
      <div class="std-middle-box">
        <el-result icon="info" title="确认恢复选中资源？" sub-title="恢复的内容将回到原目录" />
      </div>

      <div id="button-area">
        <el-button @click="show_recover_flag = false"> 取消 </el-button>
        <el-button type="danger" @click="batch_recover_resources()"> 确定 </el-button>
      </div>
    </div>
  </el-dialog>
  <el-dialog v-model="completely_delete_flag" title="彻底删除资源" style="max-width: 600px" :width="dialog_width">
    <div style="display: flex; flex-direction: column; gap: 16px; align-items: center; justify-content: center">
      <div class="std-middle-box">
        <el-result icon="warning" title="确认彻底删除选中资源？" sub-title="注意！将会从系统中彻底删除，不可恢复！" />
      </div>

      <div id="button-area">
        <el-button @click="completely_delete_flag = false"> 取消 </el-button>
        <el-button type="danger" @click="batch_completely_delete_resources()"> 确定 </el-button>
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
  align-content: flex-start;
  box-sizing: border-box;
}
.resource-item-card {
  display: flex;
  flex-direction: column;
  border: 1px solid #d0d5dd;
  border-radius: 6px;
  width: 300px;
  height: 200px;
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
</style>
