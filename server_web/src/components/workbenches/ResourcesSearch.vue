<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { nextTick, onMounted, ref, watch } from 'vue';
import { attachment_get_all_resource_formats, attachment_search_resources } from '@/api/next_console';
import { ResourceItem } from '@/types/resource_type';
import { Users } from '@/types/users';
import { getInfo } from '@/utils/auth';

const props = defineProps({
  model: {
    type: Boolean,
    default: false,
    required: false
  },
  sessionResources: {
    type: Array as () => ResourceItem[],
    default: () => [],
    required: false
  }
});
const emit = defineEmits(['commit', 'close']);
const userInfo = ref<Users>({
  user_resource_limit: 0,
  user_id: null,
  user_code: null,
  user_name: null,
  user_nick_name: null,
  user_nick_name_py: 'null',
  user_email: null,
  user_phone: null,
  user_gender: null,
  user_age: null,
  user_avatar: null,
  user_department: null,
  user_company: null,
  user_account_type: null,
  create_time: null,
  update_time: null,
  user_expire_time: null,
  last_login_time: null,
  user_role: null,
  user_status: null,
  user_source: null,
  user_wx_nickname: null,
  user_wx_avatar: null,
  user_wx_openid: null,
  user_wx_union_id: null,
  user_position: null,
  user_department_id: null,
  user_company_id: null
});
interface ISearchType {
  search_type: string;
  search_type_name: string;
  search_type_active: boolean;
}
const resourceSearchTypes = ref<ISearchType[]>([
  {
    search_type: 'all',
    search_type_name: '全部',
    search_type_active: true
  },
  {
    search_type: 'file',
    search_type_name: '文件',
    search_type_active: false
  },
  {
    search_type: 'folder',
    search_type_name: '文件夹',
    search_type_active: false
  },
  {
    search_type: 'share',
    search_type_name: '共享',
    search_type_active: false
  }
]);
const allResourceFormats = ref([]);
const resourceSearchModel = ref('recently');
const resourceSearchResult = ref<ResourceItem[]>([]);
const resourceSearchDialogShow = ref(false);
const sessionResourceList = ref<ResourceItem[]>([]);
const searchResourceLoading = ref(false);
const resourceRecentTableRef = ref(null);
const resourceSearchTableRef = ref(null);
const searchKeyword = ref('');
const resourceSearchRag = ref(false);
const currentResourceFormats = ref([]);
const currentPageNum = ref(1);
const currentPageSize = ref(50);
const currentTotal = ref(0);
const searchResourceListScrollRef = ref(null);
const currentResourceTypes = ref(['文档', '图片', '网页', '代码', '文件夹']);
const elScrollbarRef = ref(null);
function formatResourceSize(sizeNum: number | null) {
  // 格式化文件大小,保留两位小数,输入为mb单位的数字
  if (sizeNum === null) {
    return '';
  }
  let size = sizeNum;
  let sizeStr = '';

  // kb单位
  if (size < 1) {
    size = size * 1024;
    sizeStr = size.toFixed(2) + 'KB';
  } else if (size < 1024) {
    sizeStr = size.toFixed(2) + 'MB';
  } else if (size < 1024 * 1024) {
    size = size / 1024;
    sizeStr = size.toFixed(2) + 'GB';
  } else if (size < 1024 * 1024 * 1024) {
    size = size / 1024 / 1024;
    sizeStr = size.toFixed(2) + 'TB';
  } else if (size < 1024 * 1024 * 1024 * 1024) {
    size = size / 1024 / 1024 / 1024;
    sizeStr = size.toFixed(2) + 'PB';
  } else {
    size = size / 1024 / 1024 / 1024 / 1024;
    sizeStr = size.toFixed(2) + 'EB';
  }
  return sizeStr;
}
function getResourceIcon(resource: ResourceItem) {
  // 获取资源图标
  if (resource.resource_icon) {
    if (
      resource.resource_icon.includes('http') ||
      resource.resource_icon.includes('data:image') ||
      resource.resource_icon.includes('images/')
    ) {
      return resource.resource_icon;
    }
    return 'images/' + resource.resource_icon;
  } else {
    return 'images/' + 'html.svg';
  }
}
function sortResourceSize(a, b) {
  // 按照文件大小排序
  return a.resource_size_in_MB - b.resource_size_in_MB;
}
async function changeRecentSearchType(searchType: ISearchType) {
  for (let subType of resourceSearchTypes.value) {
    subType.search_type_active = searchType.search_type == subType.search_type;
  }
  resourceSearchModel.value = 'recently';
  let params = {
    search_type: searchType.search_type,
    search_recently: true
  };
  // 获取最近会话资源
  let res = await attachment_search_resources(params);
  if (!res.error_status) {
    resourceSearchResult.value = res.result;
    // 在resourceSearchResult 中设置选中
    await updateSelectedRow();
  }
}
async function initAllFormatOptions() {
  let res = await attachment_get_all_resource_formats({});
  if (!res.error_status) {
    allResourceFormats.value = res.result;
  }
}
function getSelectedResources() {
  let chooseResources = [];
  if (resourceSearchModel.value == 'recently') {
    chooseResources = resourceRecentTableRef.value?.getSelectionRows();
  } else if (resourceSearchModel.value == 'search') {
    chooseResources = resourceSearchTableRef.value?.getSelectionRows();
  }
  if (!chooseResources.length) {
    ElMessage.info('请选择资源');
    return [];
  }
  console.log('选择的资源', chooseResources);
  return chooseResources;
}
async function changeSearchType(searchType: ISearchType) {
  for (let subType of resourceSearchTypes.value) {
    subType.search_type_active = searchType.search_type == subType.search_type;
  }
  resourceSearchModel.value = 'search';
  searchResourceKeyword();
}
function clickRow(row, column, event) {
  // 切换该行的选中状态
  resourceSearchTableRef.value?.toggleRowSelection(row);
}
function getHighlightedText(text: string) {
  if (!searchKeyword.value || !text) {
    return text;
  }
  const regex = new RegExp(`(${searchKeyword.value})`, 'gi');
  return text.replace(regex, '<span class="highlight-resource-keyword">$1</span>');
}
async function cancelAddChooseResources() {
  resourceSearchDialogShow.value = false;
  resourceSearchTableRef.value?.clearSelection();
}
async function searchResourceKeyword(notice = true) {
  // 根据关键词从资源库中搜索资源
  if (!searchKeyword.value) {
    if (notice) {
      ElMessage.info('请输入关键词');
    }
    return;
  }
  resourceSearchModel.value = 'search';
  searchResourceLoading.value = true;
  let currentSearchType = 'all';
  for (let searchType of resourceSearchTypes.value) {
    if (searchType.search_type_active) {
      currentSearchType = searchType.search_type;
      break;
    }
  }
  let params = {
    search_type: currentSearchType,
    search_recently: false,
    resource_keyword: searchKeyword.value,
    resource_type: currentResourceTypes.value,
    resource_format: [],
    rag_enhance: resourceSearchRag.value
  };
  for (let format of currentResourceFormats.value) {
    params.resource_format.push(format);
  }
  let res = await attachment_search_resources(params);
  if (!res.error_status) {
    resourceSearchResult.value = [];
    currentTotal.value = res.result.total;
    for (let item of res.result.data) {
      let authorInfo = null;
      for (let user of res.result.author_info) {
        if (user.user_id == item.user_id) {
          authorInfo = user;
          break;
        }
      }
      item.author_info = authorInfo;
      resourceSearchResult.value.push(item);
    }
  }
  searchResourceLoading.value = false;
}
async function searchResourceKeywordNext(scrollPosition: object) {
  if (searchResourceLoading.value) {
    return;
  }
  if (currentTotal.value && currentTotal.value <= resourceSearchResult.value.length) {
    return;
  }
  if ((currentPageNum.value - 1) * currentPageSize.value >= currentTotal.value) {
    return;
  }
  // @ts-ignore
  if (Math.floor(scrollPosition.scrollTop + 600) > searchResourceListScrollRef.value.clientHeight - 10) {
    // 下一页
    currentPageNum.value += 1;
    // 根据关键词从资源库中搜索资源
    if (!searchKeyword.value) {
      ElMessage.info('请输入关键词');
      return;
    }
    resourceSearchModel.value = 'search';
    searchResourceLoading.value = true;
    let currentSearchType = 'all';
    for (let searchType of resourceSearchTypes.value) {
      if (searchType.search_type_active) {
        currentSearchType = searchType.search_type;
        break;
      }
    }
    let params = {
      search_type: currentSearchType,
      search_recently: false,
      resource_keyword: searchKeyword.value,
      resource_type: currentResourceTypes.value,
      resource_format: [],
      rag_enhance: resourceSearchRag.value,
      page_num: currentPageNum.value,
      page_size: currentPageSize.value
    };
    for (let format of currentResourceFormats.value) {
      params.resource_format.push(format);
    }
    let res = await attachment_search_resources(params);
    if (!res.error_status) {
      currentTotal.value = res.result.total;
      for (let resource of res.result.data) {
        // 去重添加
        let findFlag = false;
        for (let item of resourceSearchResult.value) {
          if (item.id == resource.id) {
            findFlag = true;
            break;
          }
        }
        if (findFlag) {
          continue;
        }
        let authorInfo = null;
        for (let user of res.result.author_info) {
          if (user.user_id == resource.user_id) {
            authorInfo = user;
            break;
          }
        }
        resource.author_info = authorInfo;
        resourceSearchResult.value.push(resource);
      }
    }
    // 往上滚动防止连续加载
    // @ts-ignore
    elScrollbarRef.value?.setScrollTop(scrollPosition.scrollTop - 10);
    searchResourceLoading.value = false;
  }
}
async function updateSelectedRow() {
  await nextTick();
  if (resourceSearchModel.value == 'recently') {
    // 清除所有已选中的行
    resourceRecentTableRef.value?.clearSelection();
    // 遍历表格数据
    resourceRecentTableRef.value?.data.forEach(row => {
      // 检查当前行的resource_id是否在sessionResourceList中

      for (let selectedResource of sessionResourceList.value) {
        if (selectedResource.id == row.id) {
          // 选中符合条件的行
          resourceRecentTableRef.value?.toggleRowSelection(row, true);
          break;
        }
      }
    });
  }
}
onMounted(async () => {
  userInfo.value = await getInfo();
  changeRecentSearchType({
    search_type: 'all',
    search_type_name: '全部',
    search_type_active: true
  });
  initAllFormatOptions();
  resourceSearchDialogShow.value = props.model;
  sessionResourceList.value = props.sessionResources;
  await updateSelectedRow();
});
watch(
  () => props.model,
  newVal => {
    resourceSearchDialogShow.value = newVal;
  },
  { immediate: true }
);
watch(
  () => props.sessionResources,
  async newVal => {
    if (newVal) {
      sessionResourceList.value = newVal;
      await updateSelectedRow();
    }
  },
  { immediate: true }
);
defineExpose({
  getSelectedResources
});
</script>

<template>
  <el-dialog
    v-model="resourceSearchDialogShow"
    title="资源检索"
    :draggable="true"
    :modal="true"
    style="max-width: 1500px"
    width="80%"
    @closed="emit('close')"
  >
    <div id="search_dialog_main">
      <div id="search_input_area">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索关键词或者问题"
          clearable
          @clear="
            changeRecentSearchType({
              search_type: 'all',
              search_type_name: '全部',
              search_type_active: true
            })
          "
          @keydown.enter="searchResourceKeyword"
          @change="
            val => {
              if (val == '') {
                changeRecentSearchType({
                  search_type: 'all',
                  search_type_name: '全部',
                  search_type_active: true
                });
              }
            }
          "
        >
          <template #prefix>
            <el-image
              src="images/search.svg"
              style="width: 20px; height: 20px; cursor: pointer"
              @click="searchResourceKeyword"
            />
          </template>
          <template #suffix>
            <el-switch
              v-model="resourceSearchRag"
              active-text="内容检索"
              style="margin-right: 6px"
              @change="searchResourceKeyword(false)"
            />
            <el-tooltip placement="top" effect="dark">
              <el-image src="images/tooltip.svg" style="width: 20px; height: 20px" />
              <template #content> 基于内容理解的深度搜索，提供更精准的搜索结果 </template>
            </el-tooltip>
          </template>
        </el-input>
      </div>
      <div v-show="resourceSearchModel == 'recently'" id="search_recent_area">
        <div class="std-middle-box">
          <el-text class="std-sub-title"> 最近检索 </el-text>
        </div>
        <div id="search_recent_type">
          <div
            v-for="(search_type, idx) in resourceSearchTypes"
            :key="idx"
            class="search-type-box"
            :class="{ 'search-type-box-active': search_type.search_type_active }"
            @click="changeRecentSearchType(search_type)"
          >
            <el-text class="search-type-text" :class="{ 'search-type-text-active': search_type.search_type_active }">
              {{ search_type.search_type_name }}
            </el-text>
          </div>
        </div>
        <el-scrollbar v-loading="searchResourceLoading" style="width: 100%">
          <div id="search_recent_result">
            <el-table
              ref="resourceRecentTableRef"
              :data="resourceSearchResult"
              style="width: 100%; margin-top: 8px"
              :default-sort="{ prop: 'rag_time', order: 'descending' }"
              row-key="id"
              @row-click="clickRow"
            >
              <el-table-column type="selection" width="55" />
              <el-table-column prop="resource_name" label="资源名称" min-width="120" show-overflow-tooltip sortable>
                <template #default="scope">
                  <div class="resource-item-name">
                    <div :id="scope.row.id" class="resource-item-name-drag">
                      <img :id="scope.row.id" :src="getResourceIcon(scope.row)" class="resource-icon" alt="" />
                    </div>
                    <div class="std-box">
                      <el-text style="cursor: default" class="resource-name-text">
                        {{ scope.row.resource_name }}
                      </el-text>
                    </div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="resource_desc" label="资源描述" show-overflow-tooltip sortable />
              <el-table-column prop="create_time" label="创建时间" width="180" sortable />
              <el-table-column prop="rag_time" label="检索时间" width="180" sortable />
              <el-table-column prop="resource_type_cn" label="资源类型" width="120" sortable />
              <el-table-column prop="resource_format" label="资源格式" width="120" sortable />
              <el-table-column
                prop="resource_size"
                label="资源大小"
                width="120"
                :sortable="true"
                :sort-method="sortResourceSize"
              >
                <template #default="scope">
                  <el-text v-if="scope.row.resource_type != 'folder'">
                    {{ formatResourceSize(scope.row.resource_size_in_MB) }}
                  </el-text>
                  <el-text v-else> - </el-text>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-scrollbar>
        <div id="search_confirm_area">
          <el-button style="width: 100%" @click="cancelAddChooseResources()"> 取消 </el-button>
          <el-button type="primary" style="width: 100%" @click="emit('commit')"> 确认 </el-button>
        </div>
      </div>
      <div v-show="resourceSearchModel == 'search'" id="search_result_area">
        <div id="search_resource_condition">
          <div id="search_resource_condition_left">
            <div class="std-middle-box">
              <el-text>资源种类</el-text>
            </div>
            <div class="std-middle-box">
              <el-checkbox-group v-model="currentResourceTypes" :min="1" @change="searchResourceKeyword()">
                <el-checkbox value="文档" label="文档" />
                <el-checkbox value="图片" label="图片" />
                <el-checkbox value="网页" label="网页" />
                <el-checkbox value="代码" label="代码" />
                <el-checkbox value="文件夹" label="文件夹" />
              </el-checkbox-group>
            </div>
          </div>
          <div id="search_resource_condition_right">
            <div class="std-middle-box">
              <el-text>资源格式</el-text>
            </div>
            <div class="std-middle-box">
              <el-select
                v-model="currentResourceFormats"
                multiple
                style="min-width: 120px"
                placeholder="全部格式"
                filterable
                :clearable="true"
                collapse-tags
                collapse-tags-tooltip
                :max-collapse-tags="2"
                @change="searchResourceKeyword()"
              >
                <el-option v-for="item in allResourceFormats" :key="item.name" :label="item.name" :value="item.name">
                  <el-text>{{ item.name }}</el-text>
                  <el-text>({{ item.count }})</el-text>
                </el-option>
              </el-select>
            </div>
          </div>
        </div>
        <div id="search_recent_type">
          <div
            v-for="(searchType, idx) in resourceSearchTypes"
            :key="idx"
            class="search-type-box"
            :class="{ 'search-type-box-active': searchType.search_type_active }"
            @click="changeSearchType(searchType)"
          >
            <el-text class="search-type-text" :class="{ 'search-type-text-active': searchType.search_type_active }">
              {{ searchType.search_type_name }}
            </el-text>
          </div>
        </div>
        <el-scrollbar
          ref="elScrollbarRef"
          v-loading="searchResourceLoading"
          style="width: 100%"
          element-loading-text="资源检索中..."
          @scroll="searchResourceKeywordNext"
        >
          <div id="search_recent_result">
            <div ref="searchResourceListScrollRef">
              <el-table
                ref="resourceSearchTableRef"
                :data="resourceSearchResult"
                style="width: 100%; margin-top: 8px"
                @row-click="clickRow"
              >
                <el-table-column type="selection" width="55" />
                <el-table-column prop="resource_name" label="资源名称" min-width="120" sortable>
                  <template #default="scope">
                    <div class="resource-item-name">
                      <div :id="scope.row.id" class="resource-item-name-drag">
                        <img :id="scope.row.id" :src="getResourceIcon(scope.row)" class="resource-icon" alt="" />
                      </div>
                      <div class="std-box">
                        <el-text
                          style="cursor: default"
                          class="resource-name-text"
                          v-html="getHighlightedText(scope.row.resource_name)"
                        />
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="author_info" label="资源作者" width="200" sortable>
                  <template #default="scope">
                    <div v-if="scope.row.user_id == userInfo?.user_id" class="std-box">
                      <el-avatar :src="userInfo?.user_avatar" style="width: 16px; height: 16px" />
                      <el-text
                        style="width: 160px; font-size: 12px; font-weight: 500; line-height: 18px; color: #475467"
                        truncated
                      >
                        {{ userInfo?.user_nick_name }}
                      </el-text>
                    </div>
                    <div v-else class="std-box">
                      <el-avatar :src="scope.row?.author_info?.user_avatar" style="width: 18px; height: 18px" />
                      <el-text style="font-size: 12px; font-weight: 500; line-height: 18px; color: #475467" truncated>
                        {{ scope.row?.author_info?.user_nick_name }}
                      </el-text>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="resource_desc" label="资源描述" min-width="120" sortable>
                  <template #default="scope">
                    <div class="std-box">
                      <el-text
                        style="cursor: default"
                        class="resource-name-text"
                        v-html="getHighlightedText(scope.row.resource_desc)"
                      />
                    </div>
                  </template>
                </el-table-column>
                <el-table-column v-if="resourceSearchRag" prop="ref_text" label="关联内容" min-width="120" sortable>
                  <template #default="scope">
                    <div class="std-box">
                      <el-tooltip effect="light">
                        <el-text
                          style="cursor: default"
                          class="resource-name-text"
                          truncated
                          v-html="getHighlightedText(scope.row.ref_text)"
                        />
                        <template #content>
                          <el-scrollbar>
                            <div style="max-height: 500px">
                              <div
                                style="cursor: default"
                                class="resource-name-text"
                                v-html="getHighlightedText(scope.row.ref_text)"
                              ></div>
                            </div>
                          </el-scrollbar>
                        </template>
                      </el-tooltip>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  v-if="resourceSearchRag"
                  prop="rerank_score"
                  label="相关度评分"
                  width="120"
                  show-overflow-tooltip
                  sortable
                />
                <el-table-column prop="create_time" label="创建时间" width="180" sortable />
                <el-table-column prop="update_time" label="更新时间" width="180" sortable />
                <el-table-column prop="resource_type_cn" label="资源类型" width="120" sortable />
                <el-table-column prop="resource_format" label="资源格式" width="120" sortable />
                <el-table-column
                  prop="resource_size"
                  label="资源大小"
                  width="120"
                  :sortable="true"
                  :sort-method="sortResourceSize"
                >
                  <template #default="scope">
                    <el-text v-if="scope.row.resource_type != 'folder'">
                      {{ formatResourceSize(scope.row.resource_size_in_MB) }}
                    </el-text>
                    <el-text v-else> - </el-text>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-scrollbar>
        <div id="search_confirm_area">
          <el-button style="width: 100%" @click="cancelAddChooseResources()"> 取消 </el-button>
          <el-button type="primary" style="width: 100%" @click="emit('commit')"> 确认 </el-button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
}
.std-sub-title {
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  color: #344054;
}
#search_dialog_main {
  display: flex;
  width: 100%;
  height: 100%;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 8px;
}
#search_input_area {
  width: 100%;
}
#search_recent_area {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  justify-content: flex-start;
  align-items: flex-start;
}
#search_result_area {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 8px;
}
#search_recent_type {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  width: calc(100% - 8px);
  background: #f9fafb;
  border: 1px solid #eaecf0;
  border-radius: 8px;
  padding: 4px;
  height: 32px;
}
.search-type-box {
  display: flex;
  align-items: center;
  flex-direction: column;
  width: calc(100% - 24px);
  justify-content: center;
  padding: 6px 12px;
  border-radius: 6px;
  height: 20px;
  cursor: pointer;
}
.search-type-box-active {
  background-color: #ffffff;
  box-shadow: 0 1px 3px 0 #1018281a;
}
.search-type-text {
  font-size: 14px;
  line-height: 20px;
  font-weight: 600;
  color: #667085;
}
.search-type-text-active {
  color: #344054;
}
#search_recent_result {
  width: 100%;
  max-height: 600px;
}
.resource-item-name {
  display: flex;
  width: 100%;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  justify-content: flex-start;
}
.resource-icon {
  width: 22px;
  height: 22px;
  margin-right: 4px;
}
#search_confirm_area {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
  justify-content: space-around;
  align-items: center;
  margin-top: 8px;
  gap: 16px;
}
#search_resource_condition {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  width: 100%;
}
#search_resource_condition_left {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: flex-start;
  gap: 16px;
}
#search_resource_condition_right {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: flex-start;
  gap: 16px;
  min-width: 200px;
}
</style>
