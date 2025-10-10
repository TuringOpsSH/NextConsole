<script setup lang="ts">
import { ArrowLeft, ArrowRight, Search, ArrowUp, ArrowDown } from '@element-plus/icons-vue';
import { ref, onMounted } from 'vue';
import {
  access_loading,
  add_get_access_object,
  add_get_access_object_by_search,
  auto_exit_search_model,
  auto_handle_search_blur,
  batch_set_share_access,
  batch_share_access,
  confirm_update_share_access,
  current_all_share_objects,
  current_model,
  current_search_result,
  current_share_Ref,
  current_share_resource,
  current_share_search_Ref,
  exit_search_model,
  get_access_object_list,
  get_company_structure_tree,
  left_cnt,
  left_search_cnt,
  props,
  remove_get_access_object,
  right_cnt,
  search_company_department_and_colleague,
  search_keyword,
  share_selector_vis_flag,
  turn_off_share_selector,
  update_left_cnt,
  update_left_search_cnt,
  update_right_cnt
} from '@/components/resource/resource_share_selector/resource_share_selector';
import { useUserInfoStore } from '@/stores/user-info-store';
const userInfoStore = useUserInfoStore();
const phone_view = ref(window.innerWidth < 768);
const dialog_width = ref(window.innerWidth < 768 ? '90%' : '60%');
function fixResourceIcon(iconPath: string) {
  if (!iconPath) {
    return '/images/default_resource_icon.svg';
  }
  if (iconPath.startsWith('http')) {
    return iconPath;
  }
  return `/images/${iconPath}`;
}
onMounted(() => {
  if (window.innerWidth >= 768 && window.innerWidth * 0.6 < 800) {
    dialog_width.value = '800px';
  }
});
</script>

<template>
  <el-dialog v-model="share_selector_vis_flag" title="分享资源" :fullscreen="true">
    <div id="share_selector_main">
      <div id="resource_share_selector">
        <div id="selector_left">
          <div class="std-middle-box" style="width: 100%">
            <el-form style="width: 100%">
              <el-form-item style="margin-bottom: 0 !important">
                <el-input
                  v-model="search_keyword"
                  placeholder="搜索添加共享成员"
                  :prefix-icon="Search"
                  clearable
                  @focus="current_model = 'search'"
                  @blur="auto_handle_search_blur()"
                  @clear="exit_search_model"
                  @change="auto_exit_search_model"
                  @keydown.enter.prevent="search_company_department_and_colleague()"
                />
              </el-form-item>
            </el-form>
          </div>

          <div id="company_search">
            <el-scrollbar>
              <el-tree
                v-show="current_model == 'tree'"
                ref="current_share_Ref"
                :data="current_all_share_objects"
                :lazy="true"
                :load="get_company_structure_tree"
                :props="props"
                :highlight-current="true"
                node-key="structure_id"
                :show-checkbox="true"
                :check-strictly="true"
                :expand-on-click-node="true"
                @check="update_left_cnt"
              >
                <template #default="{ node, data }">
                  <div class="tree-button" @click="">
                    <div class="std-middle-box">
                      <el-avatar
                        v-show="data?.structure_type == 'colleague' && data?.user_avatar"
                        :src="data?.user_avatar"
                        style="width: 24px; height: 24px; background-color: white"
                      />
                      <el-avatar
                        v-show="data?.structure_type == 'colleague' && !data?.user_avatar"
                        style="width: 24px; height: 24px; background: #d1e9ff"
                      >
                        <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                          {{ data?.user_nick_name_py }}
                        </el-text>
                      </el-avatar>
                      <el-avatar
                        v-show="data?.structure_type == 'department'"
                        :src="data?.department_logo"
                        style="width: 24px; height: 24px; background-color: white"
                      />
                      <el-avatar
                        v-show="data?.structure_type == 'friend' && data?.user_avatar"
                        :src="data?.user_avatar"
                        style="width: 24px; height: 24px; background-color: white"
                      />
                      <el-avatar
                        v-show="data?.structure_type == 'friend' && !data?.user_avatar"
                        style="width: 24px; height: 24px; background: #d1e9ff"
                      >
                        <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                          {{ data?.user_nick_name_py }}
                        </el-text>
                      </el-avatar>
                    </div>
                    <div>
                      <el-text>{{ node.data.label }}</el-text>
                    </div>
                  </div>
                </template>
              </el-tree>

              <el-tree
                v-show="current_model == 'search'"
                ref="current_share_search_Ref"
                :data="current_search_result"
                :lazy="true"
                :load="get_company_structure_tree"
                :props="props"
                :highlight-current="true"
                node-key="structure_id"
                :show-checkbox="true"
                :check-strictly="true"
                :expand-on-click-node="true"
                @check="update_left_search_cnt"
              >
                <template #default="{ node, data }">
                  <div class="tree-button">
                    <div class="std-middle-box">
                      <el-avatar
                        v-show="data?.structure_type == 'colleague' && data?.user_avatar"
                        :src="data?.user_avatar"
                        style="width: 24px; height: 24px; background-color: white"
                      />
                      <el-avatar
                        v-show="data?.structure_type == 'colleague' && !data?.user_avatar"
                        style="width: 24px; height: 24px; background: #d1e9ff"
                      >
                        <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                          {{ data?.user_nick_name_py }}
                        </el-text>
                      </el-avatar>
                      <el-avatar
                        v-show="data?.structure_type == 'department'"
                        :src="data?.department_logo"
                        style="width: 24px; height: 24px; background-color: white"
                      />
                      <el-avatar
                        v-show="data?.structure_type == 'friend' && data?.user_avatar"
                        :src="data?.user_avatar"
                        style="width: 24px; height: 24px; background-color: white"
                      />
                      <el-avatar
                        v-show="data?.structure_type == 'friend' && !data?.user_avatar"
                        style="width: 24px; height: 24px; background: #d1e9ff"
                      >
                        <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                          {{ data?.user_nick_name_py }}
                        </el-text>
                      </el-avatar>
                    </div>
                    <div>
                      <el-text>{{ node.data.label }}</el-text>
                    </div>
                  </div>
                </template>
              </el-tree>
            </el-scrollbar>
          </div>
        </div>

        <div v-if="current_model == 'tree'" id="selector_middle">
          <el-button
            v-if="!phone_view"
            :icon="ArrowLeft"
            type="primary"
            :disabled="!right_cnt"
            @click="remove_get_access_object()"
          />
          <el-button
            v-else
            :icon="ArrowLeft"
            type="primary"
            :disabled="!right_cnt"
            @click="remove_get_access_object()"
          />

          <el-button
            v-if="!phone_view"
            :icon="ArrowRight"
            type="primary"
            :disabled="!left_cnt"
            style="margin: 0"
            @click="add_get_access_object()"
          />
          <el-button
            v-else
            :icon="ArrowRight"
            type="primary"
            :disabled="!left_cnt"
            style="margin: 0"
            @click="add_get_access_object()"
          />
        </div>
        <div v-else-if="current_model == 'search'" id="selector_middle">
          <el-button
            v-if="!phone_view"
            :icon="ArrowLeft"
            type="primary"
            :disabled="!right_cnt"
            @click="remove_get_access_object()"
          />
          <el-button
            v-else
            :icon="ArrowLeft"
            type="primary"
            :disabled="!right_cnt"
            @click="remove_get_access_object()"
          />
          <el-button
            v-if="!phone_view"
            :icon="ArrowRight"
            type="primary"
            :disabled="!left_search_cnt"
            style="margin: 0"
            @click="add_get_access_object_by_search()"
          />
          <el-button
            v-else
            :icon="ArrowRight"
            type="primary"
            :disabled="!left_search_cnt"
            style="margin: 0"
            @click="add_get_access_object_by_search()"
          />
        </div>

        <div id="selector_right">
          <div id="selector_resource_area">
            <div class="resource-header">
              <el-text size="large"> 选中资源 </el-text>
            </div>
            <div class="resource-area">
              <div class="resource-area-box">
                <div class="resource-icon-box">
                  <el-image :src="fixResourceIcon(current_share_resource?.resource_icon)" class="resource-icon" />
                </div>
                <div class="resource-name-box">
                  <el-text>{{ current_share_resource?.resource_name }}</el-text>
                </div>
              </div>
            </div>
          </div>
          <div id="selector_right_head">
            <div class="std-middle-box">
              <el-text> 已选择授权对象：{{ get_access_object_list?.length }} 个 </el-text>
            </div>
            <div class="std-middle-box" style="gap: 6px">
              <div class="std-middle-box">
                <el-text> 批量设置为 </el-text>
              </div>
              <div class="std-middle-box" style="width: 70px">
                <el-select v-model="batch_share_access" size="small" @change="batch_set_share_access">
                  <el-option label="阅读" value="read"> 阅读 </el-option>
                  <el-option label="下载" value="download"> 下载 </el-option>
                  <el-option label="编辑" value="edit"> 编辑 </el-option>
                  <el-option label="管理" value="manage"> 管理 </el-option>
                </el-select>
              </div>
            </div>
          </div>
          <el-scrollbar>
            <div id="selector_right_body" v-loading="access_loading" element-loading-text="权限加载中...">
              <div v-for="(access_object, idx) in get_access_object_list" :key="idx" class="access-object-area">
                <div class="access-object-area-left">
                  <el-checkbox
                    v-model="access_object.get_access"
                    :disabled="access_object.disabled"
                    @change="update_right_cnt()"
                  />
                  <div class="std-middle-box">
                    <el-avatar
                      v-show="access_object?.structure_type == 'colleague' && access_object?.user_avatar"
                      :src="access_object?.user_avatar"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="access_object?.structure_type == 'colleague' && !access_object?.user_avatar"
                      style="width: 24px; height: 24px; background: #d1e9ff"
                    >
                      <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                        {{ access_object?.user_nick_name_py }}
                      </el-text>
                    </el-avatar>
                    <el-avatar
                      v-show="access_object?.structure_type == 'department'"
                      :src="access_object?.department_logo"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="access_object?.structure_type == 'friend' && access_object?.user_avatar"
                      :src="access_object?.user_avatar"
                      style="width: 24px; height: 24px; background-color: white"
                    />
                    <el-avatar
                      v-show="access_object?.structure_type == 'friend' && !access_object?.user_avatar"
                      style="width: 24px; height: 24px; background: #d1e9ff"
                    >
                      <el-text style="font-size: 8px; font-weight: 600; color: #1570ef">
                        {{ access_object?.user_nick_name_py }}
                      </el-text>
                    </el-avatar>
                  </div>
                  <div>
                    <el-text style="max-width: 170px" truncated>{{ access_object.label }}</el-text>
                  </div>
                  <el-tooltip v-if="access_object?.disabled" effect="dark" placement="right">
                    <template #default>
                      <div class="std-middle-box">
                        <el-image src="/images/tooltip.svg" style="width: 16px; height: 16px" />
                      </div>
                    </template>
                    <template #content>
                      <el-text
                        v-if="access_object?.resource_id && access_object?.resource_id != current_share_resource.id"
                        style="color: white; font-size: 12px"
                      >
                        权限来自上层资源
                      </el-text>
                      <el-text
                        v-if="access_object?.user_id == current_share_resource.user_id"
                        style="color: white; font-size: 12px"
                      >
                        资源作者
                      </el-text>
                    </template>
                  </el-tooltip>
                </div>

                <div class="std-middle-box" style="min-width: 70px">
                  <el-select
                    v-model="access_object.access"
                    size="small"
                    :disabled="access_object?.user_id == userInfoStore.userInfo?.user_id || access_object.disabled"
                  >
                    <el-option label="阅读" value="read"> 阅读 </el-option>
                    <el-option label="下载" value="download"> 下载 </el-option>
                    <el-option label="编辑" value="edit"> 编辑 </el-option>
                    <el-option label="管理" value="manage"> 管理 </el-option>
                  </el-select>
                </div>
              </div>
            </div>
          </el-scrollbar>
        </div>
      </div>

      <div id="resource_share_selector_button">
        <el-button style="width: 100%; max-width: 200px" @click="turn_off_share_selector()"> 取消 </el-button>
        <el-button type="primary" style="width: 100%; max-width: 200px" @click="confirm_update_share_access()">
          确定
        </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
#share_selector_main {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
}
#resource_share_selector {
  border-radius: 5px;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  width: calc(100% - 4px);
  gap: 12px;
}
#company_search {
  height: calc(80vh - 48px);
  width: calc(100% - 24px);
}
#selector_left {
  width: calc(100% - 26px);
  height: calc(80vh - 24px);
  display: flex;
  flex-direction: column;
  border-radius: 5px;
  padding: 12px;
  border: 1px solid #d0d5dd;
}
#selector_middle {
  width: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 12px;
}
#selector_right {
  width: calc(100% - 26px);
  height: calc(80vh - 24px);
  display: flex;
  flex-direction: column;
  padding: 12px;
  border: 1px solid #d0d5dd;
  border-radius: 5px;
}

.tree-button {
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: flex-start;
  height: 40px;
  width: 100%;
}
:deep(.el-tree-node__content) {
  height: 50px;
}

#resource_share_selector_button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  gap: 16px;
}
#selector_right_head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 30px;
}
#selector_right_body {
  min-width: 350px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: calc(100vh - 360px);
}
.access-object-area {
  display: flex;
  flex-direction: row;
  align-items: center;
  border-radius: 6px;
  padding: 12px;
  justify-content: space-between;
  background-color: #f9fafb;
}
.access-object-area-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
}
#selector_resource_area {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 4px;
  padding: 6px;
  border-radius: 6px;
  background-color: #f9fafb;
  margin-bottom: 4px;
}
.resource-area {
  display: flex;
  flex-direction: row;
  padding: 12px;
  width: calc(100% - 24px);
}
.resource-area-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  padding: 6px;
  background-color: white;
  width: calc(100% - 12px);
  border-radius: 6px;
}
.resource-icon {
  width: 24px;
  height: 24px;
}
@media (width< 768px) {
  #resource_share_selector {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }
  #company_search {
    max-height: 200px;
    width: 100%;
  }
  #selector_right_body {
    max-height: 200px;
    width: 100%;
    min-width: 100%;
  }
  #selector_left {
    padding: 6px;
    width: calc(100% - 14px);
  }
  #selector_right {
    padding: 6px;
    width: calc(100% - 14px);
  }
  #selector_middle {
    flex-direction: row;
  }
}
</style>
