<script setup lang="ts">
import { Plus, Search, Upload } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { genFileId } from 'element-plus';
import type { UploadInstance, UploadRawFile } from 'element-plus';
import { defineProps, onMounted, reactive, ref } from 'vue';
import { api, appAdd, appDelete, appImport, appSearch } from '@/api/app-center-api';
import router from '@/router';
import { useUserInfoStore } from '@/stores/user-info-store';
import { IAppMetaInfo } from '@/types/app-center-type';
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
const showNewAppUploadForm = ref(false);
const appList = ref<IAppMetaInfo[]>([]);
const newAppForm = reactive<IAppMetaInfo>({
  app_code: '',
  app_desc: '',
  app_icon: '/images/logo.svg',
  app_name: '',
  app_status: '',
  app_type: '',
  create_time: '',
  id: 0,
  update_time: '',
  user_id: 0
});
const newAppFormRef = ref(null);
const newAppFormRules = {
  app_name: [
    { required: true, message: '请输入应用名称', trigger: 'blur' },
    { message: '应用名称长度不能超过20个字符', trigger: 'blur', max: 20 }
  ],
  app_desc: [{ required: true, message: '请输入应用描述', trigger: 'blur' }],
  app_icon: [{ required: true, message: '请上传应用图标', trigger: 'change' }]
};
const showNewAppForm = ref<boolean>(false);
const userInfoStore = useUserInfoStore();

function beforeAvatarUpload(file: File) {
  const isLt5M = file.size / 1024 / 1024 < 5;
  if (!isLt5M) {
    ElMessage.info('上传头像图片大小不能超过 5MB!');
  }
  return isLt5M;
}
const currentPageSize = ref<number>(20);
const currentPageNum = ref<number>(1);
const currentTotal = ref<number>(0);
const currentKeyword = ref<string>('');
const currentStatusList = ref<string[]>([]);
const currentTypeList = ref<string[]>([]);
const newUploadAppFormRef = ref(null);
const newUploadAppForm = reactive({
  uploadFileUrl: ''
});
const newUploadAppFormRules = {
  uploadFileUrl: [{ required: true, message: '请上传应用包', trigger: 'blur' }]
};
const uploadRef = ref<UploadInstance>();
const uploadAppLoading = ref(false);
function initNewAppForm(): void {
  newAppForm.app_name = '';
  newAppForm.app_type = '个人应用';
  newAppForm.app_desc = '';
  newAppForm.app_status = '';
  newAppForm.app_icon = '/images/logo.svg';
  showNewAppForm.value = true;
}
async function searchAppList(): Promise<void> {
  const params = {
    app_keyword: currentKeyword.value,
    app_status: currentStatusList.value,
    app_type: currentTypeList.value,
    page_size: currentPageSize.value,
    page_num: currentPageNum.value
  };
  const res = await appSearch(params);
  if (!res.error_status) {
    appList.value = res.result.data;
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
function handlePageChange(pageNum: number): void {
  currentPageNum.value = pageNum;
  searchAppList();
}
function handlePageSizeChange(pageSize: number): void {
  currentPageSize.value = pageSize;
  searchAppList();
}
async function newAppFormSubmit() {
  const validRes = await newAppFormRef.value.validate();
  if (!validRes) return;
  const params = {
    app_name: newAppForm.app_name,
    app_type: newAppForm.app_type,
    app_desc: newAppForm.app_desc,
    app_icon: newAppForm.app_icon
  };
  const res = await appAdd(params);
  if (!res.error_status) {
    showNewAppForm.value = false;
    await router.push({
      name: 'appDetail',
      params: {
        app_code: res.result.app_code
      }
    });
  }
}
async function handleAvatarUploadSuccess(res: any) {
  if (!res.error_status) {
    newAppForm.app_icon = res.result.app_icon;
  }
}
async function  beginEdit(app: IAppMetaInfo) {
  await router.push({
    name: 'appDetail',
    params: {
      app_code: app.app_code
    }
  });
}
async function deleteAppItem(app: IAppMetaInfo) {
  const res = await appDelete({ app_code: app.app_code });
  if (!res.error_status) {
    searchAppList();
  }
}
function initNewAppUploadForm(): void {
  showNewAppUploadForm.value = true;
}
async function handleExceed(files) {
  uploadRef.value!.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  uploadRef.value!.handleStart(file);
  uploadRef.value.submit();
}
async function handleAppUploadSuccess(res: any) {
  if (!res.error_status) {
    newUploadAppForm.uploadFileUrl = res.result.app_schema_url;
  }
}
async function submitNewAppUploadForm() {
  const validRes = await newUploadAppFormRef.value.validate();
  if (!validRes) return;
  uploadAppLoading.value = true;
  const res = await appImport({
    app_schema_url: newUploadAppForm.uploadFileUrl
  });
  if (!res.error_status) {
    showNewAppUploadForm.value = false;
    ElMessage.success('导入成功');
    searchAppList();
  } else {
    ElMessage.error('导入失败');
  }
  uploadAppLoading.value = false;
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
  searchAppList();
});
</script>

<template>
  <el-container>
    <el-header>
      <div class="app-header">
        <div class="app-header-left">
          <div style="min-width: 80px">
            <h3>应用列表</h3>
          </div>
          <div class="filter-condition">
            <el-select v-model="currentStatusList" placeholder="应用状态" multiple clearable @change="searchAppList">
              <el-option value="创建中" />
              <el-option value="已发布" />
              <el-option value="已禁用" />
            </el-select>
          </div>
          <div class="filter-condition">
            <el-select v-model="currentTypeList" placeholder="应用类型" multiple clearable @change="searchAppList">
              <el-option value="系统应用" />
              <el-option value="个人应用" />
              <el-option value="商店应用" disabled />
            </el-select>
          </div>
          <div class="filter-condition">
            <el-input
              v-model="currentKeyword"
              placeholder="搜索应用"
              :prefix-icon="Search"
              clearable
              @change="searchAppList"
            >
              <el-option value="系统应用" />
              <el-option value="个人应用" />
              <el-option value="商店应用" disabled />
            </el-input>
          </div>
        </div>
        <div class="app-header-right">
          <el-button type="primary" :icon="Upload" @click="initNewAppUploadForm"> 导入应用 </el-button>
          <el-button type="primary" :icon="Plus" @click="initNewAppForm"> 创建应用 </el-button>
        </div>
      </div>
    </el-header>
    <el-main>
      <el-scrollbar>
        <div id="app-main">
          <div v-for="app in appList" :key="app.id" class="app-item-card" @dblclick="beginEdit(app)">
            <div class="app-item-head">
              <div class="app-item-meta">
                <div class="std-left-box">
                  <el-text truncated class="app-name">
                    {{ app.app_name }}
                  </el-text>
                </div>
                <div class="std-left-box">
                  <el-text class="app-desc" truncated>
                    {{ app.app_desc }}
                  </el-text>
                </div>
              </div>
              <div class="app-item-icon">
                <el-image :src="app.app_icon" fit="cover" style="width: 60px; height: 60px; border-radius: 12px" />
              </div>
            </div>
            <div class="app-item-foot">
              <div class="app-tags">
                <el-tag>{{ app.app_type }}</el-tag>
                <el-tag>{{ app.app_status }}</el-tag>
              </div>
              <div class="app-manage">
                <div class="app-tags">
                  <el-avatar v-if="app.user_avatar" :src="app.user_avatar" />
                  <el-text>{{ app.user_nick_name }}</el-text>
                  <el-text>最近编辑 {{ app.update_time }}</el-text>
                </div>
                <div class="app-tags">
                  <el-button text size="small" type="primary" @click="beginEdit(app)"> 编辑 </el-button>
                  <el-popconfirm title="确认删除？" @confirm="deleteAppItem(app)">
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
  <el-dialog v-model="showNewAppForm" title="创建应用">
    <el-form ref="newAppFormRef" :model="newAppForm" label-position="top" :rules="newAppFormRules">
      <el-form-item label="应用名称" prop="app_name" required>
        <el-input v-model="newAppForm.app_name" @keydown.enter.prevent />
      </el-form-item>
      <el-form-item label="应用描述" prop="app_desc" required>
        <el-input v-model="newAppForm.app_desc" type="textarea" :rows="8" show-word-limit maxlength="500" />
      </el-form-item>
      <el-form-item label="应用图标" prop="app_icon" required>
        <el-upload
          drag
          :show-file-list="false"
          accept=".png, .jpg, .jpeg, .gif, .bmp, .webp"
          name="app_icon"
          :headers="userInfoStore.userHeader"
          :before-upload="beforeAvatarUpload"
          :action="api.app_icon_upload"
          :on-success="handleAvatarUploadSuccess"
          style="min-width: 160px"
        >
          <div v-if="newAppForm.app_icon">
            <el-image :src="newAppForm.app_icon" style="width: 40px; height: 40px" />
          </div>
          <div v-else>
            <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
            <i class="el-icon-upload" />
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </div>
        </el-upload>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showNewAppForm = false"> 取消 </el-button>
      <el-button type="primary" @click="newAppFormSubmit"> 创建 </el-button>
    </template>
  </el-dialog>
  <el-dialog v-model="showNewAppUploadForm" title="导入应用">
    <el-form
      ref="newUploadAppFormRef"
      v-loading="uploadAppLoading"
      element-loading-text="努力导入中..."
      :model="newUploadAppForm"
      label-position="top"
      :rules="newUploadAppFormRules"
    >
      <el-form-item label="上传应用包" prop="uploadFileUrl" required>
        <div class="upload-area">
          <el-upload
            ref="uploadRef"
            drag
            :show-file-list="true"
            accept=".json"
            :limit="1"
            name="app_schema"
            :headers="userInfoStore.userHeader"
            :action="api.app_upload"
            :on-exceed="handleExceed"
            :on-success="handleAppUploadSuccess"
            style="min-width: 160px; width: 100%"
          >
            <div>
              <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
              <i class="el-icon-upload" />
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            </div>
          </el-upload>
        </div>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button text type="info" @click="showNewAppUploadForm = false"> 取消 </el-button>
      <el-button text type="primary" @click="submitNewAppUploadForm"> 确认 </el-button>
    </template>
  </el-dialog>
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
  display: flex;
  align-content: flex-start;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 12px;
  height: calc(100vh - 200px);
}
.app-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 4px 20px;
}
.app-header-left {
  display: flex;
  flex-direction: row;
  align-items: center;
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
  cursor: pointer;
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
.upload-area {
  display: flex;
  flex-direction: row;
  width: 100%;
  align-items: center;
  justify-content: center;
}
.filter-condition {
  min-width: 160px;
}
.app-header-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  margin-left: 12px;
}
</style>
