<script setup lang="ts">
import { Sunny, MoonNight } from '@element-plus/icons-vue';
import { Picture as IconPicture } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { onMounted, reactive, ref } from 'vue';
import { domainGet, latestVersionGet } from '@/api/base';
import { llmInstanceSearch, userConfigGet, userConfigUpdate } from '@/api/user-center';
import ResourcesSearch from '@/components/next-console/messages-flow/ResourcesSearch.vue';
import { useUserConfigStore } from '@/stores/user-config-store';
import { useUserInfoStore } from '@/stores/user-info-store';
import { IResourceItem } from '@/types/resource-type';
import { IUserConfig } from '@/types/user-center';

const userInfoStore = useUserInfoStore();
const userConfigStore = useUserConfigStore();
const localUserConfig = reactive<IUserConfig>({
  user_id: null,
  workbench: {
    model_list: [],
    message_layout: 'default',
    search_engine_language: 'zh',
    search_engine_resource: 'search',
    session_resources_list: [
      {
        resource_id: -1,
        resource_icon: 'all_resource.svg',
        resource_name: '全部资源'
      } as IResourceItem
    ]
  },
  contact: {
    allow_search: true
  },
  system: {
    theme: 'light',
    language: '中文'
  }
});
const availAbleModels = ref([]);
const pickedRightModels = ref([]);
const themeOptions = [
  {
    label: '明亮',
    value: 'light',
    icon: Sunny
  },
  {
    label: '暗黑',
    value: 'dark',
    icon: MoonNight,
    disabled: true
  }
];
const resourcesSearchRef = ref(null);
const resourceSearchDialogShow = ref(false);
async function handleChangeUpdate(configKey: string) {
  const res = await userConfigUpdate({
    config_key: configKey,
    config_value: localUserConfig[configKey]
  });
  if (!res.error_status) {
    userConfigStore.updateUserConfig({ configKey: localUserConfig[configKey] } as Partial<IUserConfig>);
    ElMessage.success({
      message: '更新成功',
      type: 'success',
      duration: 3000
    });
  }
}
function handleRightCheckChange(val: any) {
  pickedRightModels.value = val;
}
async function openNewModelForm() {
  // 新标签页打开管理后台
  const res = await domainGet();
  const adminDomain = res.result.admin_domain;
  window.open(adminDomain + '/next-console/appCenter/llm_manage/llm', '_blank');
}
async function upPickModelList() {
  // 所有选中模型上移一位
  // 获取当前选中的模型索引
  const selectedIndices = pickedRightModels.value
    .map(model => localUserConfig.workbench.model_list.findIndex(m => m === model))
    .filter(index => index !== -1)
    .sort((a, b) => a - b);

  // 如果没有选中项或选中了第一个无法上移，直接返回
  if (selectedIndices.length === 0 || selectedIndices[0] === 0) {
    return;
  }

  // 创建模型列表的副本
  const newModelList = [...localUserConfig.workbench.model_list];

  // 遍历所有选中的模型
  for (const index of selectedIndices) {
    // 交换当前模型和上一个模型的位置
    [newModelList[index - 1], newModelList[index]] = [newModelList[index], newModelList[index - 1]];
  }
  console.log(newModelList);
  localUserConfig.workbench.model_list = newModelList;
  handleChangeUpdate('workbench');
}
async function downPickModelList() {
  // 获取当前选中的模型索引
  const selectedIndices = pickedRightModels.value
    .map(model => localUserConfig.workbench.model_list.findIndex(m => m === model))
    .filter(index => index !== -1)
    .sort((a, b) => b - a); // 倒序排列，从后往前处理

  // 如果没有选中项或选中了最后一个无法下移，直接返回
  const lastIndex = localUserConfig.workbench.model_list.length - 1;
  if (selectedIndices.length === 0 || selectedIndices[0] === lastIndex) {
    return;
  }

  // 创建模型列表的副本
  const newModelList = [...localUserConfig.workbench.model_list];

  // 遍历所有选中的模型（从后往前）
  for (const index of selectedIndices) {
    // 交换当前模型和下一个模型的位置
    [newModelList[index], newModelList[index + 1]] = [newModelList[index + 1], newModelList[index]];
  }

  console.log(newModelList);
  localUserConfig.workbench.model_list = newModelList;
  handleChangeUpdate('workbench');
}
async function checkLatestVersion() {
  const res = await latestVersionGet();
  if (!res.error_status) {
    if (res.result.version && userConfigStore.systemVersion && res.result.version !== userConfigStore.systemVersion) {
      ElMessage.info({
        message: `发现新版本 ${res.result.version}，请前往GitHub下载最新版本`,
        type: 'info',
        duration: 5000
      });
    } else {
      ElMessage.success({
        message: '当前已是最新版本',
        type: 'success',
        duration: 3000
      });
    }
  }
}
function getResourceIcon(resource: IResourceItem) {
  // 获取资源图标
  if (resource.resource_icon) {
    if (
      resource.resource_icon.includes('http') ||
      resource.resource_icon.includes('data:image') ||
      resource.resource_icon.includes('/images/')
    ) {
      return resource.resource_icon;
    }
    return '/images/' + resource.resource_icon;
  } else {
    return '/images/html.svg';
  }
}
function removeResourceItem(resource: IResourceItem) {
  const indexToRemove = localUserConfig.workbench.session_resources_list.findIndex(item => item.id === resource.id);
  if (indexToRemove !== -1) {
    localUserConfig.workbench.session_resources_list.splice(indexToRemove, 1);
  }
  handleChangeUpdate('workbench');
}
function setDefaultResources() {
  localUserConfig.workbench.session_resources_list = [
    {
      resource_id: -1,
      resource_icon: 'all_resource.svg',
      resource_name: '全部资源'
    } as IResourceItem
  ];
  handleChangeUpdate('workbench');
}
function commitAddChooseResources() {
  const res = resourcesSearchRef.value?.getSelectedResources();
  if (!res?.length) {
    return;
  }
  resourceSearchDialogShow.value = false;
  localUserConfig.workbench.session_resources_list = res;
  handleChangeUpdate('workbench');
}
onMounted(async () => {
  const userConfigData = await userConfigGet({});
  if (!userConfigData.error_status) {
    Object.assign(localUserConfig, userConfigData.result);
    userConfigStore.updateUserConfig(userConfigData.result as IUserConfig);
  }
  const res = await llmInstanceSearch({ fetch_all: true });
  if (!res.error_status) {
    availAbleModels.value = res.result?.data;
  }
});
</script>

<template>
  <el-scrollbar>
    <div class="user_info_main">
      <div class="user_info_box">
        <div class="form-area">
          <div>
            <el-text class="form-label-text">AI工作台</el-text>
          </div>
          <div class="form-area-body">
            <el-form-item label="会话布局模式" label-position="left">
              <el-radio-group
                v-model="localUserConfig.workbench.message_layout"
                @change="handleChangeUpdate('workbench')"
              >
                <el-radio value="default" border> 左右布局 </el-radio>
                <el-radio value="left" border> 靠左布局 </el-radio>
                <el-radio value="right" border> 靠右布局 </el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="小亦模型列表" label-position="left">
              <el-transfer
                v-model="localUserConfig.workbench.model_list"
                :data="availAbleModels"
                target-order="push"
                :props="{
                  key: 'llm_code',
                  label: 'llm_label'
                }"
                :filterable="true"
                filter-placeholder="请输入关键词进行搜索"
                :titles="['可用模型', '工作台可选模型']"
                @change="handleChangeUpdate('workbench')"
                @right-check-change="handleRightCheckChange"
              >
                <template #left-footer>
                  <el-button
                    class="transfer-footer"
                    size="small"
                    :disabled="!userInfoStore.adminAccess"
                    @click="openNewModelForm"
                  >
                    新增
                  </el-button>
                </template>
                <template #right-footer>
                  <el-button class="transfer-footer" size="small" @click="upPickModelList">上移</el-button>
                  <el-button class="transfer-footer" size="small" @click="downPickModelList">下移</el-button>
                </template>
                <template #default="{ option }">
                  <el-tooltip :content="option.llm_desc" placement="top">
                    {{ option.llm_label }}
                  </el-tooltip>
                </template>
              </el-transfer>
            </el-form-item>
            <el-form-item label="默认知识库列表" label-position="left">
              <div id="ai-image-body">
                <el-scrollbar style="width: calc(100%)">
                  <div id="ai-file-body-left">
                    <div id="ai_file_body_left_bg">
                      <div
                        v-for="(item, idx) in localUserConfig.workbench.session_resources_list"
                        :key="idx"
                        class="ai-file-item"
                      >
                        <el-tooltip placement="top" effect="light">
                          <template #default>
                            <el-image src="/images/support_attachment.svg" style="width: 16px; height: 16px" />
                          </template>
                          <template #content>
                            <el-text> 资源解析完成 </el-text>
                          </template>
                        </el-tooltip>
                        <el-image :src="getResourceIcon(item)" style="width: 20px; height: 20px">
                          <template #error>
                            <el-icon>
                              <IconPicture />
                            </el-icon>
                          </template>
                        </el-image>
                        <el-text style="max-width: 120px" truncated>
                          {{ item?.resource_name }}
                        </el-text>
                        <el-image
                          src="/images/remove_img.svg"
                          style="width: 16px; height: 16px; cursor: pointer"
                          @click="removeResourceItem(item)"
                        />
                      </div>
                    </div>
                  </div>
                </el-scrollbar>
                <div id="ai-image-body-right">
                  <el-button text type="primary" @click="resourceSearchDialogShow = true"> 搜索 </el-button>
                  <el-button text type="primary" @click="setDefaultResources"> 重置 </el-button>
                </div>
              </div>
              <ResourcesSearch
                ref="resourcesSearchRef"
                :model="resourceSearchDialogShow"
                :session-resources="localUserConfig.workbench.session_resources_list"
                @commit="
                  args => {
                    commitAddChooseResources();
                  }
                "
              />
            </el-form-item>
          </div>
        </div>
        <div class="form-area">
          <div>
            <el-text class="form-label-text">通讯录</el-text>
          </div>
          <div class="form-area-body">
            <el-form-item label="允许被陌生人搜索" label-position="left">
              <el-switch v-model="localUserConfig.contact.allow_search" @change="handleChangeUpdate('contact')" />
            </el-form-item>
          </div>
        </div>
        <div class="form-area">
          <div>
            <el-text class="form-label-text">系统界面</el-text>
          </div>
          <div class="form-area-body">
            <el-form-item label="主题" label-position="left">
              <el-segmented
                v-model="localUserConfig.system.theme"
                :options="themeOptions"
                @change="handleChangeUpdate('system')"
              >
                <template #default="scope">
                  <div class="theme-button">
                    <el-icon size="20">
                      <component :is="scope.item.icon" />
                    </el-icon>
                    <div>{{ scope.item.label }}</div>
                  </div>
                </template>
              </el-segmented>
            </el-form-item>
            <el-form-item label="语言" label-position="left">
              <el-select v-model="localUserConfig.system.language" @change="handleChangeUpdate('system')">
                <!-- 东亚语言 -->
                <el-option value="中文">中文</el-option>
                <el-option value="English" disabled>English</el-option>
                <el-option value="日本語" disabled>日本語</el-option>
                <el-option value="한국어" disabled>한국어</el-option>

                <!-- 欧洲语言 -->
                <el-option value="Français" disabled>Français</el-option>
                <el-option value="Deutsch" disabled>Deutsch</el-option>
                <el-option value="Español" disabled>Español</el-option>
                <el-option value="Português" disabled>Português</el-option>
                <el-option value="Italiano" disabled>Italiano</el-option>
                <el-option value="Nederlands" disabled>Nederlands</el-option>
                <el-option value="Polski" disabled>Polski</el-option>
                <el-option value="Русский" disabled>Русский</el-option>

                <!-- 其他地区语言 -->
                <el-option value="العربية" disabled>العربية</el-option>
                <el-option value="हिन्दी" disabled>हिन्दी</el-option>
                <el-option value="ไทย" disabled>ไทย</el-option>
                <el-option value="Tiếng Việt" disabled>Tiếng Việt</el-option>
                <el-option value="Türkçe" disabled>Türkçe</el-option>
              </el-select>
            </el-form-item>
          </div>
        </div>
        <div class="form-area">
          <div>
            <el-text class="form-label-text">关于NextConsole</el-text>
          </div>
          <div class="form-area-body">
            <el-form-item label="当前版本:" label-position="left">
              <div>
                <el-text>
                  {{ userConfigStore.systemVersion }}
                </el-text>
              </div>
              <div style="margin-left: 12px">
                <el-button text type="primary" @click="checkLatestVersion"> 检查更新 </el-button>
              </div>
            </el-form-item>
          </div>
        </div>
      </div>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.user_info_main {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
  height: calc(100vh - 40px);
  gap: 12px;
}
.user_info_box {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 900px;
  gap: 24px;
}
.form-area {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.form-label-text {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}
.form-area-body {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  padding: 24px;
  background: #ffffff;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease-in-out;
}
.transfer-footer {
  margin-left: 8px;
}
.theme-button {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px;
}
#ai-image-body {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin: 0 16px;
  padding: 8px 0;
  gap: 10px;
  border-bottom: 1px solid #d0d5dd;
  width: 100%;
}
#ai-file-body-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  width: 100%;
}
#ai-file-body-left-bg {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  padding: 6px 8px;
  border-radius: 8px;
  background: #eff8ff;
}
.ai-file-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  padding: 2px 6px;
  border-radius: 6px;
  background-color: #ffffff;
  border: 1px solid #d0d5dd;
  box-shadow: 0 1px 2px 0 #1018280d;
  margin-bottom: 6px;
}
#ai-image-body-right {
  display: flex;
  flex-direction: row;
}
</style>
