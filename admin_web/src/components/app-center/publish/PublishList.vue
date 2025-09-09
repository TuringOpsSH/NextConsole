<script setup lang="ts">
import { Setting, Search } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { defineProps, onMounted, ref } from 'vue';
import { prodAppSearch, publishDelete } from '@/api/app-center-api';
import router from '@/router';
const currentPageNum = ref(1);
const currentPageSize = ref(20);
const currentTotal = ref(0);
const publishList = ref([]);
const currentStatusList = ref(['正常']);
const currentTypeList = ref([]);
const currentKeyword = ref('');
const prop = defineProps({
  pageNum: {
    type: String,
    default: ''
  },
  pageSize: {
    type: String,
    default: ''
  },
  keyword: {
    type: String,
    default: ''
  },
  status: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: ''
  }
});
async function searchPublishList() {
  const params = {
    app_keyword: currentKeyword.value,
    app_status: currentStatusList.value,
    app_type: currentTypeList.value,
    page_size: currentPageSize.value,
    page_num: currentPageNum.value
  };
  const res = await prodAppSearch(params);
  if (!res.error_status) {
    publishList.value = res.result.data;
    currentTotal.value = res.result.total;
    router.replace({
      query: {
        ...router.currentRoute.value.query,
        page_num: currentPageNum.value,
        page_size: currentPageSize.value,
        app_keyword: currentKeyword.value,
        app_status: currentStatusList.value.join(','),
        app_type: currentTypeList.value.join(',')
      }
    });
  }
}
async function handlePageSizeChange(pageSize: number) {
  currentPageSize.value = pageSize;
  searchPublishList();
}
async function handlePageChange(pageNum: number) {
  currentPageNum.value = pageNum;
  searchPublishList();
}
async function ToPublishConnectors() {
  await router.push({
    name: 'publishConnector'
  });
}
async function beginEdit(app) {
  await router.push({
    name: 'publishDetail',
    params: {
      app_code: app.app_code
    }
  });
}
async function deleteAppPublish(app) {
  const res = await publishDelete({
    app_code: app.app_code
  });
  if (!res.error_status) {
    ElMessage.success('删除发布应用成功！');
    searchPublishList();
  }
}
onMounted(async () => {
  if (prop.pageNum) {
    try {
      currentPageNum.value = parseInt(prop.pageNum);
    } catch (e) {
      currentPageNum.value = 1;
    }
  }
  if (prop.pageSize) {
    try {
      currentPageSize.value = parseInt(prop.pageSize);
    } catch (e) {
      currentPageSize.value = 20;
    }
  }
  if (prop.keyword) {
    currentKeyword.value = prop.keyword;
  }
  if (prop.status) {
    try {
      currentStatusList.value = prop.status.split(',');
    } catch (e) {
      currentStatusList.value = [];
    }
  }
  if (prop.type) {
    try {
      currentTypeList.value = prop.type.split(',');
    } catch (e) {
      currentTypeList.value = [];
    }
  }
  searchPublishList();
});
function getTagType(status) {
  switch (status) {
    case '正常':
      return 'success';
    case '升级中':
      return 'warning';
    case '失效':
      return 'danger';
    default:
      return '';
  }
}
</script>

<template>
  <el-container>
    <el-header height="120px">
      <div id="app-header-1">
        <div>
          <h3>发布列表</h3>
        </div>
        <div>
          <el-button type="primary" :icon="Setting" disabled @click="ToPublishConnectors"> 发布渠道管理 </el-button>
        </div>
      </div>
      <div id="app-header-1">
        <div id="app-header-2">
          <div style="width: 200px">
            <el-select
              v-model="currentStatusList"
              placeholder="发布状态"
              multiple
              clearable
              @change="searchPublishList"
            >
              <el-option value="正常" />
              <el-option value="升级中" />
              <el-option value="失效" />
            </el-select>
          </div>
          <div style="width: 200px">
            <el-select v-model="currentTypeList" placeholder="发布类型" multiple clearable @change="searchPublishList">
              <el-option value="系统应用" />
              <el-option value="个人应用" />
              <el-option value="商店应用" disabled />
            </el-select>
          </div>
        </div>
        <div>
          <el-input
            v-model="currentKeyword"
            :prefix-icon="Search"
            placeholder="搜索发布应用"
            clearable
            @keydown.enter.prevent="searchPublishList"
            @clear="searchPublishList"
          />
        </div>
      </div>
    </el-header>
    <el-main style="height: calc(100vh - 160px); padding: 0">
      <el-scrollbar>
        <div id="app-main">
          <div v-for="app in publishList" :key="app.id" class="app-item-card">
            <div class="app-item-head">
              <div class="app-item-meta">
                <div class="std-left-box">
                  <el-text truncated class="app-name">{{ app.app_name }}</el-text>
                </div>
                <div class="std-left-box">
                  <el-text class="app-desc" truncated>{{ app.app_desc }}</el-text>
                </div>
              </div>
              <div class="app-item-icon">
                <el-image :src="app.app_icon" fit="cover" style="width: 60px; height: 60px; border-radius: 12px" />
              </div>
            </div>
            <div class="app-item-foot">
              <div class="app-tags">
                <el-tag>{{ app.app_type }}</el-tag>
                <el-tag :type="getTagType(app.app_status)">{{ app.app_status }}</el-tag>
                <el-tag type="success"> V{{ app.version }}</el-tag>
              </div>
              <div class="app-manage">
                <div class="app-tags">
                  <el-avatar v-if="app.user_avatar" :src="app.user_avatar" />
                  <el-text>{{ app.user_nick_name }}</el-text>
                  <el-text>最近编辑 {{ app.update_time }}</el-text>
                </div>
                <div class="app-tags">
                  <el-button text size="small" type="primary" @click="beginEdit(app)">编辑</el-button>
                  <el-popconfirm
                    title="删除后所有用户无法再访问此发布应用，且无法恢复！确认删除？"
                    confirm-button-type="danger"
                    width="300px"
                    @confirm="deleteAppPublish(app)"
                  >
                    <template #reference>
                      <el-button text size="small" type="danger"> 删除 </el-button>
                    </template>
                  </el-popconfirm>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-scrollbar>
    </el-main>
    <el-footer height="40px">
      <el-pagination
        background
        size="small"
        layout=" total, sizes, prev, pager, next"
        :total="currentTotal"
        :page-size="currentPageSize"
        :current-page="currentPageNum"
        @update:page-size="handlePageSizeChange"
        @update:current-page="handlePageChange"
      />
    </el-footer>
  </el-container>
</template>

<style scoped>
.std-left-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  justify-content: flex-start;
  max-width: 360px;
}
#app-main {
  padding: 20px;
  display: flex;
  align-content: flex-start;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 12px;
  height: calc(100vh - 320px);
}
#app-header-1 {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 4px 12px;
}
#app-header-2 {
  display: flex;
  flex-direction: row;
  gap: 12px;
}
.app-item-card {
  width: 450px;
  height: 140px;
  padding: 12px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 6px;
  position: relative;
  overflow: hidden;
}
.app-item-card:hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: #1890ff;
  animation: borderGrow 0.3s ease;
}

@keyframes borderGrow {
  from {
    height: 0;
  }
  to {
    height: 100%;
  }
}
.app-item-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 12px;
}
.app-item-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.app-name {
  font-size: 20px;
  max-height: 300px;
}
.app-item-foot {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.app-tags {
  display: flex;
  flex-direction: row;
  gap: 6px;
}
.app-manage {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
</style>
