<script setup lang="ts">
import { format_resource_size, get_resource_icon } from '@/components/resource/resource-list/resource-list';
import {
  all_resource_tags,
  before_leave_check,
  cancel_resource_edit_model,
  choose_resource_meta,
  loading_meta,
  loading_meta_tags,
  meta_edit_flag,
  rebuild_resource,
  search_resource_tags_by_keyword,
  show_meta_flag,
  show_rebuild_button,
  switch_resource_edit_model,
  uncommit_notice,
  update_choose_resource_meta
} from '@/components/resource/resource_meta/resource_meta';
import { onMounted, ref } from 'vue';
const dialog_width = ref(window.innerWidth < 768 ? '90%' : '600px');
function getRagStatus(ref_status :string) {
  if (!ref_status) {
    return 'info';
  }
  if (ref_status === '成功') {
    return 'success';
  }
  if (ref_status === '失败') {
    return 'warning';
  }
  if (ref_status === '异常') {
    return 'danger';
  }
  return 'primary';
}
onMounted(() => {
  let headers = document.querySelectorAll('.el-drawer__header');
  let bodys = document.querySelectorAll('.el-drawer__body');
  headers.forEach(header => {
    // 在这里使用 as 关键字进行类型断言
    (header as HTMLElement).style.padding = '0';
    (header as HTMLElement).style.marginBottom = '0';
  });
});
</script>

<template>
  <el-drawer
    v-model="show_meta_flag"
    :show-close="false"
    custom-class="resource-meta"
    :before-close="before_leave_check"
    :size="dialog_width"
  >
    <template #header>
      <div id="resource-meta-head">
        <div class="std-middle-box">
          <el-text style="font-weight: 600; font-size: 16px; line-height: 24px; color: #101828"> 资源详情 </el-text>
        </div>
      </div>
    </template>
    <div id="resource-meta-area" v-loading="loading_meta" element-loading-text="加载中...">
      <el-scrollbar>
        <div id="resource-meta-main">
          <div id="resource-meta-icon">
            <div class="std-middle-box">
              <el-image :src="get_resource_icon(choose_resource_meta)" style="width: 40px; height: 40px" />
            </div>
            <div class="std-middle-box">
              <el-text
                style="
                  width: 100%;
                  font-weight: 500;
                  font-size: 14px;
                  line-height: 20px;
                  color: #344054;
                  max-width: 300px;
                "
                truncated
              >
                {{ choose_resource_meta?.resource_name }}
              </el-text>
            </div>

            <div
              class="std-middle-box"
              id="meta-edit-icon"
              @click="switch_resource_edit_model"
              v-show="choose_resource_meta?.id && choose_resource_meta?.resource_parent_id"
            >
              <el-image src="/images/edit_label.svg" style="width: 20px; height: 20px" v-show="!meta_edit_flag" />
              <el-image src="/images/edit_label_active.svg" style="width: 20px; height: 20px" v-show="meta_edit_flag" />
            </div>
          </div>
          <div id="resource-meta">
            <el-form label-position="top">
              <el-form-item label="资源名称">
                <el-input
                  v-model="choose_resource_meta.resource_name"
                  type="textarea"
                  resize="none"
                  :rows="2"
                  :readonly="!meta_edit_flag"
                />
              </el-form-item>
              <el-form-item label="资源描述">
                <el-input
                  v-model="choose_resource_meta.resource_desc"
                  type="textarea"
                  resize="none"
                  :rows="4"
                  :readonly="!meta_edit_flag"
                />
              </el-form-item>
              <el-form-item label="资源主要语言" v-show="choose_resource_meta?.id">
                <el-select v-model="choose_resource_meta.resource_language" :disabled="!meta_edit_flag">
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
          <el-divider v-show="choose_resource_meta?.id">
            <div id="resource-meta-divider">
              <div class="std-middle-box">
                <el-image src="/images/ai_abstract_active.svg" style="width: 20px; height: 20px" />
              </div>
              <div class="std-middle-box">
                <el-text style="font-size: 14px; line-height: 20px; font-weight: 600; color: #175cd3"> 摘要 </el-text>
              </div>
            </div>
          </el-divider>
          <div id="resource-static" v-show="choose_resource_meta?.id">
            <div class="resource-static-item">
              <div class="resource-static-item-left">
                <el-text class="resource-static-label">资源ID</el-text>
              </div>
              <div class="resource-static-item-right">
                <el-text class="resource-static-value">{{ choose_resource_meta?.id }}</el-text>
              </div>
            </div>
            <div class="resource-static-item">
              <div class="resource-static-item-left">
                <el-text class="resource-static-label">资源类型</el-text>
              </div>
              <div class="resource-static-item-right">
                <el-text class="resource-static-value">{{ choose_resource_meta?.resource_type_cn }}</el-text>
              </div>
            </div>
            <div class="resource-static-item">
              <div class="resource-static-item-left">
                <el-text class="resource-static-label">资源大小</el-text>
              </div>
              <div class="resource-static-item-right">
                <el-text class="resource-static-value">
                  {{ format_resource_size(choose_resource_meta?.resource_size_in_MB) }}
                </el-text>
              </div>
            </div>
            <div class="resource-static-item" v-show="choose_resource_meta?.resource_type == 'folder'">
              <div class="resource-static-item-left">
                <el-text class="resource-static-label">资源统计</el-text>
              </div>
              <div class="resource-static-item-right">
                <el-text class="resource-static-value">
                  子文件夹：{{ choose_resource_meta?.sub_resource_dir_cnt }}个
                </el-text>
                <el-text class="resource-static-value">
                  子文件：{{ choose_resource_meta?.sub_resource_file_cnt }} 个
                </el-text>
              </div>
            </div>
            <div class="resource-static-item" v-show="choose_resource_meta?.author_info">
              <div class="resource-static-item-left">
                <el-text class="resource-static-label">资源作者</el-text>
              </div>
              <div class="resource-static-item-right">
                <el-avatar :src="choose_resource_meta?.author_info?.user_avatar" style="width: 18px; height: 18px" />
                <el-text class="resource-static-value" truncated>
                  {{ choose_resource_meta?.author_info?.user_nick_name }}
                </el-text>
              </div>
            </div>
            <div class="resource-static-item" v-show="choose_resource_meta?.access_list">
              <div class="resource-static-item-left">
                <el-text class="resource-static-label">资源权限</el-text>
              </div>
              <div class="resource-static-item-right">
                <el-tag v-for="(access, idx) in choose_resource_meta?.access_list" type="success">
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
                  {{ choose_resource_meta?.resource_path }}
                </el-text>
              </div>
            </div>
            <div class="resource-static-item">
              <div class="resource-static-item-left">
                <el-text class="resource-static-label">创建时间</el-text>
              </div>
              <div class="resource-static-item-right">
                <el-text class="resource-static-value">{{ choose_resource_meta?.create_time }}</el-text>
              </div>
            </div>
            <div class="resource-static-item">
              <div class="resource-static-item-left">
                <el-text class="resource-static-label">索引状态</el-text>
                <el-tooltip effect="light" placement="top">
                  <template #default>
                    <div class="std-middle-box">
                      <el-image src="/images/tooltip.svg" style="width: 16px; height: 16px" />
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

                  <el-tag :type="getRagStatus(choose_resource_meta?.ref_status)">
                    {{ choose_resource_meta?.ref_status || '未索引' }}
                  </el-tag>
                <el-button
                  @click="rebuild_resource()"
                  text
                  type="primary"
                  :disabled="!meta_edit_flag"
                  v-show="show_rebuild_button"
                >
                  重新索引
                </el-button>
              </div>
            </div>
          </div>
          <div id="resource-tags" v-show="choose_resource_meta?.id">
            <el-form label-position="top">
              <el-form-item label="资源标签">
                <el-select
                  v-model="choose_resource_meta.resource_tags"
                  multiple
                  remote
                  filterable
                  reserve-keyword
                  :loading="loading_meta_tags"
                  style="height: 200px"
                  placeholder="搜索添加标签"
                  :remote-method="search_resource_tags_by_keyword"
                  size="large"
                  :disabled="!meta_edit_flag"
                  value-key="id"
                  :remote-show-suffix="true"
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
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-scrollbar>
      <div id="resource-meta-foot">
        <div class="resource-meta-foot-button" v-show="meta_edit_flag" @click="cancel_resource_edit_model()">
          <el-text class="resource-meta-foot-button-text"> 恢复 </el-text>
        </div>
        <div
          class="resource-meta-foot-button"
          style="background-color: #1570ef"
          @click="update_choose_resource_meta"
          v-show="meta_edit_flag"
        >
          <el-text class="resource-meta-foot-button-text" style="color: white"> 保存 </el-text>
        </div>
      </div>
    </div>
  </el-drawer>
  <el-dialog
    v-model="uncommit_notice"
    title="未保存提示"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <div class="std-middle-box">
      <el-result icon="warning" title="Warning Tip" sub-title="您还有更新内容未保存，确定离开么？"> </el-result>
    </div>
    <div id="resource-meta-foot">
      <div class="resource-meta-foot-button" @click="uncommit_notice = false">
        <el-text class="resource-meta-foot-button-text"> 返回更新 </el-text>
      </div>
      <div
        class="resource-meta-foot-button"
        style="background-color: #1570ef"
        @click="
          uncommit_notice = false;
          show_meta_flag = false;
          meta_edit_flag = false;
        "
      >
        >
        <el-text class="resource-meta-foot-button-text" style="color: white"> 确定 </el-text>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
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
  width: 100%;
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
  gap: 64px;
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
</style>
