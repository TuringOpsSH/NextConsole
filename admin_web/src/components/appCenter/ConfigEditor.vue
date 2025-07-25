<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { reactive, ref, watch } from 'vue';
import { api, appDetail, appUpdate } from '@/api/appCenterApi';
import { configArea, currentAppConfigArea } from '@/components/appCenter/ts/app-config';
import { currentApp } from '@/components/appCenter/ts/app-detail';
import router from '@/router';
import { getToken } from '@/utils/auth';

const props = defineProps({
  area: {
    type: String,
    default: '',
    required: false
  }
});
const welcomeConfigRef = ref(null);
const welcomeConfig = reactive({
  title: '欢迎使用',
  description: '这是一个配置示例',
  image: 'images/welcome.svg',
  prefixQuestions: ['你喜欢什么样的界面？', '你希望添加哪些功能？']
});
const welcomeConfigRules = {
  title: [{ required: true, message: '标题不能为空', trigger: 'blur' }],
  description: [{ required: true, message: '描述不能为空', trigger: 'blur' }],
  image: [{ required: true, message: '图片不能为空', trigger: 'change' }],
  prefixQuestions: [{ type: 'array', required: true, message: '前置问题不能为空', trigger: 'change' }]
};
const uploadHeader = {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  Authorization: 'Bearer ' + getToken()
};

function beforeAvatarUpload(file: File) {
  const isLt5M = file.size / 1024 / 1024 < 5;
  if (!isLt5M) {
    ElMessage.info('上传头像图片大小不能超过 5MB!');
  }
  uploadHeader.Authorization = 'Bearer ' + getToken();
  return isLt5M;
}

async function handleAvatarUploadSuccess(res: any) {
  if (!res.error_status) {
    welcomeConfig.image = res.result.app_icon;
  }
}

async function commitSaveConfig() {
  const validRes = await welcomeConfigRef.value.validate();
  if (!validRes) {
    return;
  }
  const configData = {
    app_code: currentApp.app_code,
    app_config: currentApp.app_config
  };
  configData.app_config.welcome = welcomeConfig;
  const res = await appUpdate(configData);
  if (!res.error_status) {
    ElMessage.success('配置保存成功');
  }
}

watch(
  () => props.area,
  async newVal => {
    for (let area of configArea) {
      if (newVal == area.area) {
        currentAppConfigArea.value = area;
        if (!currentApp.app_code) {
          currentApp.app_code = router.currentRoute.value.params.app_code || '';
          const res = await appDetail({
            app_code: currentApp.app_code
          });
          if (!res.error_status) {
            Object.assign(currentApp, res.result?.meta);
          }
        }
        if (newVal == 'welcome') {
          welcomeConfig.image = currentApp.app_config?.[area.area]?.image || 'images/welcome.svg';
          welcomeConfig.title = currentApp.app_config?.[area.area]?.title || '欢迎使用';
          welcomeConfig.description = currentApp.app_config?.[area.area]?.description || '这是一个配置示例';
          welcomeConfig.prefixQuestions = currentApp.app_config?.[area.area]?.prefixQuestions || [];
        }
      }
    }
  },
  { immediate: true }
);
</script>

<template>
  <el-container>
    <el-main>
      <div class="preview-area">
        <div class="preview-area-top">
          <div class="top-row">
            <div class="icon-area">
              <el-image :src="welcomeConfig.image" class="welcome-icon" />
            </div>
            <div>
              <el-text class="title-text">{{ welcomeConfig.title }}</el-text>
            </div>
          </div>
          <div>
            <el-text class="desc-text">{{ welcomeConfig.description }}</el-text>
          </div>
        </div>
        <div class="preview-area-body"></div>
        <div class="preview-area-foot">
          <el-tag
            v-for="(question, index) in welcomeConfig.prefixQuestions"
            :key="index"
            class="prefix-question-tag"
            size="large"
            round
          >
            {{ question }}
          </el-tag>
        </div>
      </div>

      <div class="config-area">
        <el-scrollbar>
          <el-form ref="welcomeConfigRef" :model="welcomeConfig" :rules="welcomeConfigRules">
            <el-form-item label="标题" prop="title">
              <el-input v-model="welcomeConfig.title" placeholder="请输入标题" />
            </el-form-item>
            <el-form-item label="描述" prop="description">
              <el-input v-model="welcomeConfig.description" type="textarea" placeholder="请输入描述" />
            </el-form-item>
            <el-form-item label="图片" prop="image">
              <el-upload
                drag
                :show-file-list="false"
                accept=".png, .jpg, .jpeg, .gif, .bmp, .webp"
                name="app_icon"
                :headers="uploadHeader"
                :before-upload="beforeAvatarUpload"
                :action="api.app_icon_upload"
                :on-success="handleAvatarUploadSuccess"
                style="min-width: 160px"
              >
                <div v-if="welcomeConfig.image">
                  <el-image :src="welcomeConfig.image" style="width: 40px; height: 40px" />
                </div>
                <div v-else>
                  <el-avatar src="images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                </div>
              </el-upload>
            </el-form-item>
            <el-form-item label="前置问题">
              <el-select
                v-model="welcomeConfig.prefixQuestions"
                multiple
                placeholder="请输入预置问题"
                allow-create
                filterable
                default-first-option
              />
            </el-form-item>
            <el-form-item>
              <el-popconfirm title="确认更新应用配置么" @confirm="commitSaveConfig">
                <template #reference>
                  <el-button type="primary">保存配置</el-button>
                </template>
              </el-popconfirm>
            </el-form-item>
          </el-form>
        </el-scrollbar>
      </div>
    </el-main>
  </el-container>
</template>

<style scoped>
.preview-area {
  height: 40vh;
  display: flex;
  flex-direction: column;
  gap: 16px;

  /* 新增边框样式 */
  border: 1px dashed #d1d5db; /* 浅灰色虚线边框 */
  border-radius: 8px; /* 圆角 */
  padding: 20px; /* 内边距 */
  background-color: #f9fafb; /* 非常浅的背景色 */
  position: relative; /* 为标题装饰定位 */

  /* 添加预览区域标识 */
  &::before {
    content: '预览区域';
    position: absolute;
    top: -10px;
    left: 16px;
    background-color: #fff;
    padding: 0 8px;
    font-size: 12px;
    color: #6b7280;
    font-weight: 500;
  }

  /* 悬停效果 */
  &:hover {
    border-color: #9ca3af;
    box-shadow: 0 0 0 3px rgba(156, 163, 175, 0.1);
  }
}

.preview-area-top {
  background: linear-gradient(95.64772deg, #5ac4ff1f -17%, #ae88ff1f 123%);
  border-radius: 12px;
  width: 100%;
  padding: 19px 16px 13px;
  box-sizing: border-box;
  color: #000000e0;
  font-weight: 400;
}

.preview-area-top {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.top-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}

.title-text {
  font-size: 20px;
  font-weight: 600;
  line-height: 1.4;
  background: linear-gradient(270deg, #8b5cf6, #3b82f6 43%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.desc-text {
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: #000000b3;
}

.preview-area-foot {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

.prefix-question-tag {
  cursor: pointer;
}

.config-area {
  height: 30vh;
  margin-top: 12px;
}

.welcome-icon {
  width: 40px;
  height: 40px;
  background: #f2f4f7;
}
</style>
