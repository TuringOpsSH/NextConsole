<script setup lang="ts">
import {useSessionStorage} from '@vueuse/core';
import {ElMessage} from 'element-plus';
import {onMounted, reactive, ref} from 'vue';
import {useRouter} from 'vue-router';
import {
  add_resource_tags,
  delete_resource_tags,
  get_resource_recent_count,
  get_resource_type_count,
  search_resource_tags,
  update_resource_tags
} from '@/api/resource-api';

import {
  current_tag,
  search_resource_by_tags,
  system_tags
} from '@/components/resource/resource-shortcut/resource-shortcut';
import {
  current_resource_types,
  show_search_config_area
} from '@/components/resource/resource-shortcut/resource_shortcut_head/resource_shortcut_head';
import { IResourceTag } from '@/types/resource-type';

const router = useRouter();
const showRecentArea = useSessionStorage('showRecentArea', false);
const showLabelArea = useSessionStorage('showLabelArea', false);
const dialogWidth = ref(window.innerWidth < 500 ? '90%' : '500px');
const allSearchUserTags = ref<IResourceTag[]>([]);
const newTagFormRef = ref(null);
const newTagFormData = reactive<IResourceTag>({
  id: null,
  tag_name: null,
  tag_value: null,
  tag_type: null,
  tag_source: 'user',
  tag_desc: null,
  tag_color: null,
  tag_icon: ''
});
const newTagDialogFlag = ref(false);
const editTagFormRef = ref(null);
const loadAllFlag = ref(false);
const panelUserLabels = ref<IResourceTag[]>([]);
const tagColorList = [
  {
    id: 1,
    name: '红色',
    value: '#FF3B30'
  },
  {
    id: 2,
    name: '橙色',
    value: '#FF9500'
  },
  {
    id: 3,
    name: '黄色',
    value: '#FFCC00'
  },
  {
    id: 4,
    name: '绿色',
    value: '#34C759'
  },
  {
    id: 5,
    name: '蓝色',
    value: '#007AFF'
  },
  {
    id: 6,
    name: '紫色',
    value: '#AF52DE'
  },
  {
    id: 7,
    name: '灰色',
    value: '#8E8E93'
  }
];
// @ts-ignore
const editTagFormData = reactive<IResourceTag>({
  id: null,
  tag_name: null,
  tag_value: null,
  tag_type: null,
  tag_source: 'user',
  tag_desc: null,
  tag_color: null,
  tag_icon: ''
});
const editTagDialogFlag = ref(false);
const loadingTagsFlag = ref(false);
const currentSearchChooseTag = ref<IResourceTag>(null);
const panelRecentShortcuts = ref<IResourceTag[]>([]);
const panelSystemLabels = ref<IResourceTag[]>([]);

async function searchResourceTagsByKeyword(query: string) {
  if (query === '') {
    return;
  }
  let params = {
    tag_keyword: query,
    fetch_all: true
  };
  loadingTagsFlag.value = true;
  let res = await search_resource_tags(params);
  if (!res.error_status) {
    allSearchUserTags.value = res.result;
  }
  loadingTagsFlag.value = false;
}
async function routerToResourceUserTag(item: IResourceTag) {
  // 系统标签处理
  for (let systemTag of panelRecentShortcuts.value) {
    systemTag.tag_active = false;
  }
  for (let systemTag of panelSystemLabels.value) {
    systemTag.tag_active = false;
  }
  // 资源标签处理
  if (item.tag_active == true) {
    // 关闭该标签
    item.tag_active = false;
    for (let i = 0; i < panelRecentShortcuts.value.length; i++) {
      if (panelRecentShortcuts.value[i].id == item.id) {
        panelRecentShortcuts.value.splice(i, 1);
      }
    }
  } else {
    item.tag_active = true;
    panelRecentShortcuts.value.push(item);
  }
  let userTagIds = [];
  for (let userTag of panelRecentShortcuts.value) {
    userTagIds.push(userTag.id);
  }
  // 搜索条件处理
  // 如果param没变，则直接replace 并search
  if (router.currentRoute.value.params?.tag_source == 'user') {
    await router.push({
      name: 'resource_shortcut',
      params: {
        ...router.currentRoute.value.params
      },
      query: {
        ...router.currentRoute.value.query,
        tag_id: userTagIds
      }
    });
    await search_resource_by_tags();
    return;
  }
  // 如果param变了，则push
  await router.push({
    name: 'resource_shortcut',
    params: {
      tag_source: 'user'
    },
    query: {
      ...router.currentRoute.value.query,
      tag_id: userTagIds
    }
  });
}
function initSystemTags(resourceTypeMax: number = 4) {
  panelRecentShortcuts.value = [];
  panelSystemLabels.value = [];
  let idx = 0;
  for (let systemTag of system_tags) {
    if (systemTag.tag_type == 'recent') {
      //@ts-ignore
      panelRecentShortcuts.value.push(systemTag);
    } else if (systemTag.tag_type == 'resource_type') {
      //@ts-ignore
      panelSystemLabels.value.push(systemTag);
      idx += 1;
      if (idx >= resourceTypeMax) {
        break;
      }
    }
  }
}
async function pickSearchResourceTag() {
  if (!currentSearchChooseTag.value) {
    // 清空选择，回到所有标签
    return;
  }
  // 跳转用户选择标签
  routerToResourceUserTag(currentSearchChooseTag.value);
  // 资源标签处理
  let params = {
    tag_id: currentSearchChooseTag.value.id,
    tag_click: true
  };
  await update_resource_tags(params);
  await initUserTags();
}

async function switchOnNewTagDialog() {
  newTagDialogFlag.value = true;
  newTagFormData.tag_name = '';
  newTagFormData.tag_value = '';
  newTagFormData.tag_desc = '';
  newTagFormData.tag_color = '';
  newTagFormData.tag_icon = '';
}

async function switchOnEditTagDialog(item: IResourceTag, event: Event) {
  editTagDialogFlag.value = true;
  editTagFormData.id = item.id;
  editTagFormData.tag_name = item.tag_name;
  editTagFormData.tag_value = item.tag_value;
  editTagFormData.tag_desc = item.tag_desc;
  editTagFormData.tag_color = item.tag_color;
  editTagFormData.tag_icon = item.tag_icon;
  // 拦截事件
  event.stopPropagation();
}

async function loadAllTags() {
  initSystemTags(20);
  // 加载所有的标签，包括系统标签与资源标签
  let params = {
    fetch_all: true
  };
  let res = await search_resource_tags(params);
  if (!res.error_status) {
    loadAllFlag.value = true;
    panelUserLabels.value = res.result;
  }
  // 如果query参数中包含tag_id,则设置激活状态
  for (let userTag of panelUserLabels.value) {
    if (router.currentRoute.value.query?.tag_id?.length) {
      for (let tagId of router.currentRoute.value.query?.tag_id as string[]) {
        if (tagId == userTag.id.toString()) {
          userTag.tag_active = true;
        }
      }
    }
  }
}

async function addNewUserTag() {
  let validRes = await newTagFormRef.value.validate();
  if (!validRes) {
    return;
  }
  let params = {
    tag_name: newTagFormData.tag_name,
    tag_value: newTagFormData.tag_value,
    tag_color: newTagFormData.tag_color,
    tag_desc: newTagFormData.tag_desc,
    tag_icon: newTagFormData.tag_icon
  };
  let res = await add_resource_tags(params);
  if (!res.error_status) {
    newTagDialogFlag.value = false;
    ElMessage.success({
      type: 'success',
      message: '标签创建成功！'
    });
    initUserTags();
  }
}

async function deleteChooseUserTag() {
  let params = {
    tag_list: [editTagFormData.id]
  };
  let res = await delete_resource_tags(params);
  if (!res.error_status) {
    editTagDialogFlag.value = false;
    ElMessage.success({
      type: 'success',
      message: '标签删除成功！'
    });
    initUserTags();
  }
}

async function editNewUserTag() {
  let validRes = await editTagFormRef.value.validate();
  if (!validRes) {
    return;
  }
  let params = {
    tag_id: editTagFormData.id,
    tag_name: editTagFormData.tag_name,
    tag_value: editTagFormData.tag_value,
    tag_color: editTagFormData.tag_color,
    tag_desc: editTagFormData.tag_desc,
    tag_icon: editTagFormData.tag_icon
  };
  let res = await update_resource_tags(params);
  if (!res.error_status) {
    editTagDialogFlag.value = false;
    ElMessage.success({
      type: 'success',
      message: '标签修改成功！'
    });
    initUserTags();
  }
}

async function initUserTags() {
  let params = {
    page_size: 4,
    page_num: 1,
    fetch_all: loadAllFlag.value
  };
  let res = await search_resource_tags(params);
  if (!res.error_status) {
    panelUserLabels.value = res.result;
  }
  // 如果query参数中包含tag_id,则设置激活状态
  if (!router.currentRoute.value.query?.tag_id) {
    return;
  }
  for (let userTag of panelUserLabels.value) {
    for (let tagId of router.currentRoute.value.query?.tag_id as string[]) {
      if (tagId == userTag.id.toString()) {
        userTag.tag_active = true;
      }
    }
  }
}

async function routerToResourceSystemTag(item: IResourceTag) {
  // @ts-ignore
  current_tag.value = system_tags.find(tag => tag.tag_value === item.tag_value);

  item.tag_active = true;
  // 系统标签处理,只能有一个系统标签激活
  for (let systemTag of panelRecentShortcuts.value) {
    systemTag.tag_active = false;
    if (systemTag.tag_value == item.tag_value) {
      systemTag.tag_active = true;
      current_tag.value = systemTag;
    }
  }
  for (let systemTag of panelSystemLabels.value) {
    systemTag.tag_active = false;
    if (systemTag.tag_value == item.tag_value) {
      systemTag.tag_active = true;
      current_tag.value = systemTag;
    }
  }
  // 资源标签选中的全部保留
  let userTagIds = [];
  for (let userTag of panelRecentShortcuts.value) {
    userTagIds.push(userTag.id);
  }
  if (userTagIds.length) {
    show_search_config_area(true);
  }
  // 搜索条件处理, 重置系统类型标签
  if (current_tag.value.tag_type == 'resource_type') {
    current_resource_types.value = [current_tag.value.tag_value];
  }
  // 进入最近区域，去除格式标签
  else if (current_tag.value.tag_type == 'recent') {
    current_resource_types.value = [
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
  }

  let resourceTypes = [];
  if (current_tag.value.tag_type == 'resource_type') {
    resourceTypes = [current_tag.value.tag_value];
  } else {
    if (current_resource_types.value?.length != 11) {
      resourceTypes = current_resource_types.value;
    } else {
      resourceTypes = [];
    }
  }
  // 如果param没变，则直接replace 并search
  if (router.currentRoute.value.params?.tag_source == 'system') {
    router.push({
      name: 'resource_shortcut',
      params: {
        ...router.currentRoute.value.params
      },
      query: {
        ...router.currentRoute.value.query,
        resource_type: resourceTypes,
        tag_value: item.tag_value,
        tag_id: userTagIds
      }
    });
    search_resource_by_tags();
    return;
  }
  // 如果param变了，则push
  router.push({
    name: 'resource_shortcut',
    params: {
      tag_source: 'system'
    },
    query: {
      ...router.currentRoute.value.query,
      resource_type: resourceTypes,
      tag_value: item.tag_value,
      tag_id: userTagIds
    }
  });
  search_resource_by_tags();
}


async function getResourceDataCount() {
  //获取系统标签的数量
  const params = {};
  const res = await get_resource_type_count(params);
  if (!res.error_status) {
    for (const item of panelSystemLabels.value) {
      for (const cntObj of res.result) {
        if (item.tag_value == cntObj.name) {
          item.tag_count = cntObj.cnt;
        }
      }
    }
  }
}
async function getRecentDataCount() {
  //获取最近数据的数量
  const params = {
    duration: 30,
    recent_shortcuts: panelRecentShortcuts.value.map(item => item.tag_value)
  };
  const res = await get_resource_recent_count(params);
  if (!res.error_status) {
    panelRecentShortcuts.value.forEach(item => {
      item.tag_count = res.result[item.tag_value];
    });
  }
}
async function refreshPanel() {
  // // console.log('refresh_panel_count')

  getRecentDataCount();
  getResourceDataCount();
  initSystemTags();
  initUserTags();
}

onMounted(async () => {
  refreshPanel();
});

</script>

<template>
  <div>
    <div id="panel_recent_area">
      <div id="panel_recent_head">
        <div class="std-middle-box">
          <el-text>最近</el-text>
        </div>
        <div class="std-middle-box" style="cursor: pointer" @click="showRecentArea = !showRecentArea">
          <el-image v-show="showRecentArea" src="/images/panel_arrow_down.svg" style="width: 16px; height: 16px" />
          <el-image v-show="!showRecentArea" src="/images/panel_arrow_up.svg" style="width: 16px; height: 16px" />
        </div>
      </div>
      <div v-show="showRecentArea" id="panel_recent_body">
        <div
          v-for="shortcut in panelRecentShortcuts"
          :key="shortcut.id"
          class="recent-shortcut"
          :class="
            current_tag?.tag_source == 'system' && current_tag.tag_value == shortcut.tag_value
              ? 'recent-shortcut-active'
              : ''
          "
          @click="routerToResourceSystemTag(shortcut)"
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
          <el-text style="width: 40px"> 标签 </el-text>
        </div>
        <div id="panel_label_head_buttons">
          <div class="panel_label_head_button">
            <el-select
              v-model="currentSearchChooseTag"
              size="small"
              placeholder="搜索标签"
              style="width: 100px"
              filterable
              clearable
              remote
              :loading="loadingTagsFlag"
              value-key="id"
              :remote-show-suffix="true"
              :remote-method="searchResourceTagsByKeyword"
              @change="pickSearchResourceTag"
            >
              <template #prefix>
                <el-image style="width: 16px; height: 16px" src="/images/search_label.svg" />
              </template>
              <el-option
                v-for="item in allSearchUserTags"
                :key="item.id"
                :label="item.tag_name"
                :value="item"
                style="width: 180px"
              >
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
          <div class="panel_label_head_button" @click="switchOnNewTagDialog">
            <el-image style="width: 16px; height: 16px" src="/images/add_label.svg" />
          </div>
          <div class="panel_label_head_button" @click="showLabelArea = !showLabelArea">
            <el-image v-show="showLabelArea" src="/images/panel_arrow_down.svg" style="width: 16px; height: 16px" />
            <el-image v-show="!showLabelArea" src="/images/panel_arrow_up.svg" style="width: 16px; height: 16px" />
          </div>
        </div>
      </div>
      <div v-show="showLabelArea" id="panel_label_body">
        <div id="system_label_area">
          <div
            v-for="(system_label, idx) in panelSystemLabels"
            :key="idx"
            class="system-label"
            :class="
              current_tag?.tag_source == 'system' && current_tag.tag_value == system_label.tag_value
                ? 'system-label-active'
                : ''
            "
            @click="routerToResourceSystemTag(system_label)"
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
              v-for="(user_label, idx) in panelUserLabels"
              :key="idx"
              class="user-label"
              :class="user_label.tag_active ? 'user-label-active' : ''"
              @click="routerToResourceUserTag(user_label)"
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
                v-show="user_label.tag_active"
                class="std-middle-box"
                @click="switchOnEditTagDialog(user_label, $event)"
              >
                <el-image src="/images/edit_label.svg" style="width: 16px; height: 16px" />
              </div>
            </div>
          </div>
        </el-scrollbar>
      </div>
      <div v-show="showLabelArea && !loadAllFlag" id="panel_label_foot" @click="loadAllTags">
        <el-text class="show-all-button">加载全部标签</el-text>
      </div>
    </div>
    <el-dialog v-model="newTagDialogFlag" title="新增标签" style="max-width: 500px">
      <el-form
        ref="newTagFormRef"
        :model="newTagFormData"
        label-position="top"
        :rules="{
          tag_name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }],
          tag_color: [{ required: true, message: '请选择一个喜欢的颜色', trigger: 'blur' }]
        }"
      >
        <el-form-item prop="tag_name" label="标签名称">
          <el-input v-model="newTagFormData.tag_name" />
        </el-form-item>
        <el-form-item prop="tag_desc" label="标签描述">
          <el-input v-model="newTagFormData.tag_desc" type="textarea" resize="none" :rows="4" />
        </el-form-item>
        <el-form-item prop="tag_color" label="标签颜色">
          <el-select v-model="newTagFormData.tag_color" :default-first-option="true">
            <template #prefix>
              <el-tag :color="newTagFormData.tag_color" round />
            </template>
            <el-option
              v-for="(tag_color, idx) in tagColorList"
              :key="idx"
              :value="tag_color.value"
              :label="tag_color.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <div class="std-middle-box" style="width: 100%; gap: 24px">
            <el-button style="width: 100%" @click="newTagDialogFlag = false"> 取消 </el-button>
            <el-button type="primary" style="width: 100%" @click="addNewUserTag"> 确认 </el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-dialog v-model="editTagDialogFlag" title="编辑标签" style="max-width: 500px" :width="dialogWidth">
      <el-form
        ref="editTagFormRef"
        :model="editTagFormData"
        label-position="top"
        :rules="{
          tag_name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }],
          tag_color: [{ required: true, message: '请选择一个喜欢的颜色', trigger: 'blur' }]
        }"
      >
        <el-form-item prop="tag_name" label="标签名称">
          <el-input v-model="editTagFormData.tag_name" />
        </el-form-item>
        <el-form-item prop="tag_desc" label="标签描述">
          <el-input v-model="editTagFormData.tag_desc" type="textarea" resize="none" :rows="4" />
        </el-form-item>
        <el-form-item prop="tag_color" label="标签颜色">
          <el-select v-model="editTagFormData.tag_color" :default-first-option="true">
            <template #prefix>
              <el-tag :color="editTagFormData.tag_color" round />
            </template>
            <el-option
              v-for="(tag_color, idx) in tagColorList"
              :key="idx"
              :value="tag_color.value"
              :label="tag_color.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <div class="std-middle-box" style="width: 100%; gap: 24px">
            <el-popconfirm title="该操作不可回退，确认删除该标签？" @confirm="deleteChooseUserTag">
              <template #reference>
                <el-button style="width: 100%" type="danger"> 删除 </el-button>
              </template>
            </el-popconfirm>

            <el-button type="primary" style="width: 100%" @click="editNewUserTag"> 确认 </el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
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
  flex-direction: column;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
}
.recent-shortcut {
  width: calc(100% - 16px);
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
  border: 1px solid #1570ef;
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
  gap: 4px;
  width: 100%;
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
  flex-direction: column;
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
</style>
