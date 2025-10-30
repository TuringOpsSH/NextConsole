<script setup lang="ts">
import { Search, MoreFilled, Plus } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { onMounted, ref, reactive } from 'vue';
import { llmInstanceDel, llmInstanceSearch, llmInstanceUpdate } from '@/api/config-center';
import { api } from '@/api/config-center';
import router from '@/router';
import { useUserInfoStore } from '@/stores/user-info-store';
import { ILLMInstance } from '@/types/config-center';

const props = defineProps({
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
const currentLLMList = ref([]);
const LLMPageSize = ref(50);
const LLMPageNum = ref(1);
const LLMListLoading = ref(false);
const LLMKeyword = ref('');
const LLMTotal = ref(0);
const currentLLM = reactive<Partial<ILLMInstance>>({
  user_id: 0,
  create_time: '',
  llm_code: '',
  llm_desc: '',
  llm_icon: '',
  llm_name: '',
  llm_status: '',
  llm_type: '',
  support_file: false,
  support_vis: false,
  update_time: ''
});
const LLMStatus = ref([]);
const LLMTypes = ref([]);
const currentLLMTypes = ref([]);
const currentLLMStatus = ref(['正常']);
const newLLMRules = {
  llm_name: [
    { required: true, message: '请输入模型名称', trigger: 'blur' },
    { min: 2, max: 50, message: '模型名称长度在2到50个字符之间', trigger: 'blur' }
  ],
  llm_type: [
    { required: true, message: '请输入模型类型', trigger: 'blur' },
    { min: 2, max: 50, message: '模型类型长度在2到50个字符之间', trigger: 'blur' }
  ],
  llm_desc: [
    { required: true, message: '请输入模型描述', trigger: 'blur' },
    { min: 2, max: 1000, message: '模型描述长度在2到1000个字符之间', trigger: 'blur' }
  ],
  llm_icon: [{ required: true, message: '请上传模型图标', trigger: 'blur' }],
  llm_api_secret_key: [
    { required: true, message: '请输入模型API密钥', trigger: 'blur' },
    { min: 2, max: 100, message: '模型API密钥长度在2到100个字符之间', trigger: 'blur' }
  ],
  llm_base_url: [
    { required: true, message: '请输入模型API地址', trigger: 'blur' },
    { type: 'url', message: '请输入有效的URL地址', trigger: 'blur' }
  ]
};
const userInfoStore = useUserInfoStore();
const showDeleteLLMConfirm = ref(false);
const showUpdateLLMForm = ref(false);
const currentLLMFormRef = ref(null);
async function searchLLMList() {
  LLMListLoading.value = true;
  const searchRes = await llmInstanceSearch({
    page_num: LLMPageNum.value,
    page_size: LLMPageSize.value,
    keyword: LLMKeyword.value,
    llm_status: currentLLMStatus.value,
    llm_type: currentLLMTypes.value
  });
  if (!searchRes.error_status) {
    currentLLMList.value = searchRes.result.data;
    LLMTotal.value = searchRes.result.total;
    LLMTypes.value = searchRes.result.options?.llm_type || [];
    LLMStatus.value = searchRes.result.options?.llm_status || [];
  }
  LLMListLoading.value = false;
  // 更新路由
  router.replace({
    query: {
      pageNum: LLMPageNum.value.toString(),
      pageSize: LLMPageSize.value.toString(),
      keyword: LLMKeyword.value,
      status: currentLLMStatus.value.join(','),
      type: currentLLMTypes.value.join(',')
    }
  });
}
async function handleLLMSizeChange(val: number) {
  LLMPageSize.value = val;
  searchLLMList();
}
async function handleLLMPageChange(val: number) {
  LLMPageNum.value = val;
  searchLLMList();
}
function beforeAvatarUpload(file: File) {
  const isLt5M = file.size / 1024 / 1024 < 5;
  if (!isLt5M) {
    ElMessage.info('上传头像图片大小不能超过 5MB!');
  }
  return isLt5M;
}
async function handleAvatarUploadSuccess2(res: any) {
  if (!res.error_status) {
    currentLLM.llm_icon = res.result.llm_icon;
  }
}
function beginDeleteLLM(llm) {
  Object.assign(currentLLM, llm);
  showDeleteLLMConfirm.value = true;
}
async function commitDeleteLLMInstance() {
  const deleteRes = await llmInstanceDel({
    llm_codes: [currentLLM.llm_code]
  });
  if (!deleteRes.error_status) {
    ElMessage.success('删除模型实例成功');
    showDeleteLLMConfirm.value = false;
    searchLLMList();
  }
}
async function beginUpdateLLMInstance(llm) {
  router.push({
    name: 'llmDetail',
    params: {
      llmCode: llm.llm_code
    }
  });
}
async function commitUpdateLLMInstance() {
  const valid = await currentLLMFormRef.value?.validate();
  if (!valid) {
    return;
  }
  const updateRes = await llmInstanceUpdate(currentLLM);
  if (!updateRes.error_status) {
    ElMessage.success('更新模型实例成功');
    showUpdateLLMForm.value = false;
    searchLLMList();
  }
}
async function disableLLM(llm) {
  const updateRes = await llmInstanceUpdate({
    llm_code: llm.llm_code,
    llm_status: '禁用'
  });
  if (!updateRes.error_status) {
    ElMessage.success('禁用模型实例成功');
    searchLLMList();
  }
}
async function enableLLM(llm) {
  const updateRes = await llmInstanceUpdate({
    llm_code: llm.llm_code,
    llm_status: '正常'
  });
  if (!updateRes.error_status) {
    ElMessage.success('启用模型实例成功');
    searchLLMList();
  }
}
async function toCreateLLM() {
  router.push({
    name: 'llmCreate'
  });
}
function translateTag(tag: string) {
  switch (tag) {
    case 'TG':
      return '文本生成';
    case 'IG':
      return '图片生成';
    case 'QwQ':
      return '推理模型';
    case 'IU':
      return '图片理解';
    case 'VU':
      return '视频理解';
    case 'ASR':
      return '语音识别';
    case 'TTS':
      return '语音合成';
    case 'VG':
      return '视频生成';
    case 'OMNI':
      return '全模态';
    case 'TR':
      return '向量模型';
    case 'RK':
      return '排序模型';
    case 'AU':
      return '音频理解';
    case 'IP':
      return '图像处理';
    default:
      return tag;
  }
}
onMounted(async () => {
  // 加载props
  if (props.pageNum) {
    LLMPageNum.value = parseInt(props.pageNum);
  }
  if (props.pageSize) {
    LLMPageSize.value = parseInt(props.pageSize);
  }
  if (props.keyword) {
    LLMKeyword.value = props.keyword;
  }
  if (props.status) {
    currentLLMStatus.value = props.status.split(',');
  }
  if (props.type) {
    currentLLMTypes.value = props.type.split(',');
  }
  searchLLMList();
});
</script>

<template>
  <el-container>
    <el-header>
      <div id="model-list-head">
        <div id="model-list-left">
          <div style="min-width: 80px">
            <h3>模型列表</h3>
          </div>
          <div class="filter-condition">
            <el-select
              v-model="currentLLMTypes"
              placeholder="模型种类"
              clearable
              multiple
              collapse-tags
              @change="searchLLMList"
            >
              <el-option v-for="typeOption in LLMTypes" :key="typeOption" :label="typeOption" :value="typeOption" />
            </el-select>
          </div>
          <div class="filter-condition">
            <el-select
              v-model="currentLLMStatus"
              placeholder="模型状态"
              clearable
              multiple
              collapse-tags
              @change="searchLLMList"
            >
              <el-option v-for="status in LLMStatus" :key="status" :label="status" :value="status" />
            </el-select>
          </div>
          <div class="filter-condition">
            <el-input
              v-model="LLMKeyword"
              placeholder="搜索模型"
              :prefix-icon="Search"
              clearable
              @keyup.enter.prevent="searchLLMList"
              @change="searchLLMList"
            />
          </div>
        </div>
        <div>
          <el-button type="primary" :icon="Plus" @click="toCreateLLM"> 新建模型实例 </el-button>
        </div>
      </div>
    </el-header>
    <el-main>
      <div v-loading="LLMListLoading" class="model-list-main" element-loading-text="加载中">
        <el-scrollbar>
          <div id="model-list-area">
            <div
              v-for="llm in currentLLMList"
              :key="llm.llm_code"
              class="llm-card"
              @dblclick="beginUpdateLLMInstance(llm)"
            >
              <div class="card-head">
                <div class="std-middle-box">
                  <el-image :src="llm.llm_icon" class="llm-icon" />
                </div>
                <div class="std-middle-box">
                  <el-text> {{ llm.llm_label }} </el-text>
                </div>
                <div class="llm-tags">
                  <el-tag v-for="tag in llm.llm_tags" :key="tag"> {{ translateTag(tag) }} </el-tag>
                </div>
              </div>
              <div class="card-body">
                <div class="std-middle-box">
                  <el-text :line-clamp="3">{{ llm.llm_desc }}</el-text>
                </div>
              </div>
              <div class="card-foot">
                <el-tooltip content="模型供应商" placement="top">
                  <div class="std-middle-box">
                    <el-text truncated size="small">{{ llm.llm_company }}</el-text>
                  </div>
                </el-tooltip>
                <el-divider direction="vertical" />
                <div class="std-middle-box">
                  <el-tooltip :content="llm.author?.user_nick_name" placement="top">
                    <el-avatar v-if="llm.author?.user_avatar" :src="llm.author?.user_avatar" class="author-avatar" />
                    <el-avatar v-else style="background: #d1e9ff" class="author-avatar">
                      <el-text size="small" style="color: #1570ef">
                        {{ llm.author?.user_nick_name_py }}
                      </el-text>
                    </el-avatar>
                  </el-tooltip>
                </div>
                <el-divider direction="vertical" />
                <el-tooltip content="更新时间" placement="top">
                  <div class="std-middle-box">
                    <el-text truncated size="small"> {{ llm.update_time }}</el-text>
                  </div>
                </el-tooltip>
                <el-divider direction="vertical" />
                <div class="std-middle-box">
                  <el-tag v-if="llm.llm_status == '正常'" type="success"> {{ llm.llm_status }} </el-tag>
                  <el-tag v-else type="info"> {{ llm.llm_status }} </el-tag>
                </div>
              </div>
              <el-dropdown class="card-button">
                <el-icon class="card-button-icon">
                  <MoreFilled />
                </el-icon>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="beginUpdateLLMInstance(llm)">编辑</el-dropdown-item>
                    <el-dropdown-item v-if="llm.llm_status == '正常'" divided>
                      <el-text type="warning" @click="disableLLM(llm)">禁用</el-text>
                    </el-dropdown-item>
                    <el-dropdown-item v-else divided>
                      <el-text type="success" @click="enableLLM(llm)">启用</el-text>
                    </el-dropdown-item>
                    <el-dropdown-item divided>
                      <el-text type="danger" @click="beginDeleteLLM(llm)">删除</el-text>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <div v-if="llm.llm_status === '禁用'" class="disabled-mask">
                <div class="disabled-text">已禁用</div>
              </div>
            </div>
            <div v-show="!currentLLMList?.length && !LLMListLoading" class="welcome-area">
              <div v-if="LLMKeyword">
                <el-empty description="没有找到相关联的模型实例" />
              </div>
              <div v-else class="intro-area">
                <div>
                  <el-image src="/images/web.svg" alt="" />
                </div>
                <div>
                  <h3>欢迎使用模型管理</h3>
                </div>
                <div>
                  <el-text>您可以在此配置和管理AI工作流所需的各种模型。</el-text>
                </div>
                <div>
                  <el-button type="primary" size="large" :icon="Plus" @click="toCreateLLM"> 添加模型 </el-button>
                </div>
              </div>
            </div>
          </div>
        </el-scrollbar>
      </div>
    </el-main>
    <el-footer height="40px">
      <el-pagination
        background
        size="small"
        layout=" total, sizes, prev, pager, next"
        :total="LLMTotal"
        :page-size="LLMPageSize"
        :current-page="LLMPageNum"
        @update:page-size="handleLLMSizeChange"
        @update:current-page="handleLLMPageChange"
      />
    </el-footer>
    <el-dialog v-model="showDeleteLLMConfirm" title="删除模型实例">
      <el-result
        :title="'删除选中模型实例:' + currentLLM.llm_label + '?'"
        icon="error"
        sub-title="此删除操作无法回退，请谨慎操作！"
      />
      <template #footer>
        <div class="std-middle-box">
          <el-button round @click="showDeleteLLMConfirm = false"> 取消 </el-button>
          <el-button type="danger" round @click="commitDeleteLLMInstance"> 确认删除 </el-button>
        </div>
      </template>
    </el-dialog>
    <el-dialog v-model="showUpdateLLMForm" :fullscreen="true" title="模型实例详情">
      <div class="std-middle-box">
        <el-form
          ref="currentLLMFormRef"
          :model="currentLLM"
          :rules="newLLMRules"
          class="new-llm"
          label-position="top"
          :disabled="!currentLLM?.is_editable"
        >
          <el-form-item prop="llm_name" label="模型名称" required>
            <el-input v-model="currentLLM.llm_name" placeholder="请输入模型名称（对应model参数）" clearable />
          </el-form-item>
          <el-form-item prop="llm_type" label="模型类型" required>
            <el-input v-model="currentLLM.llm_type" placeholder="请输入模型类型（如deepseek-r1)" clearable />
          </el-form-item>
          <el-form-item prop="llm_desc" label="模型描述" required>
            <el-input v-model="currentLLM.llm_desc" placeholder="请输入模型描述" clearable type="textarea" :rows="6" />
          </el-form-item>
          <el-form-item prop="llm_icon" label="模型图标" required>
            <el-upload
              drag
              :show-file-list="false"
              accept=".png, .jpg, .jpeg, .gif, .bmp, .webp"
              name="llm_icon"
              :headers="userInfoStore.userHeader"
              :before-upload="beforeAvatarUpload"
              :action="api.llm_icon_upload"
              :on-success="handleAvatarUploadSuccess2"
              style="min-width: 160px"
            >
              <div v-if="currentLLM.llm_icon">
                <el-image :src="currentLLM.llm_icon" style="width: 40px; height: 40px" />
              </div>
              <div v-else>
                <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
                <i class="el-icon-upload" />
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              </div>
            </el-upload>
          </el-form-item>
          <el-form-item label="模型API密钥" prop="llm_api_secret_key" required>
            <el-input
              v-model="currentLLM.llm_api_secret_key"
              placeholder="请输入模型API密钥"
              clearable
              type="password"
              show-password
            />
          </el-form-item>
          <el-form-item label="模型API地址" prop="llm_base_url" required>
            <el-input
              v-model="currentLLM.llm_base_url"
              placeholder="请输入模型API地址（如https://api.deepseek.com/v1）"
              clearable
            />
          </el-form-item>
          <el-form-item label="共享使用" prop="llm_is_public">
            <el-switch v-model="currentLLM.llm_is_public" active-text="共享" inactive-text="私有" />
          </el-form-item>
          <el-form-item label="模型标签" prop="llm_tags">
            <el-select
              v-model="currentLLM.llm_tags"
              placeholder="请选择或创建模型标签"
              multiple
              :multiple-limit="4"
              collapse-tags
              clearable
              allow-create
              filterable
            >
              <el-option v-for="tag in ['AI', 'NLP', '视觉', '语音', '多模态']" :key="tag" :label="tag" :value="tag" />
            </el-select>
          </el-form-item>
          <el-form-item label="模型供应商" prop="llm_company">
            <el-input v-model="currentLLM.llm_company" placeholder="请输入模型供应商名称" clearable />
          </el-form-item>
          <el-form-item label="支持OpenAI-SDK" prop="is_std_openai">
            <el-switch v-model="currentLLM.is_std_openai" active-text="是" inactive-text="否" />
          </el-form-item>
          <el-form-item label="支持视觉能力" prop="support_vis">
            <el-switch v-model="currentLLM.support_vis" active-text="支持" inactive-text="不支持" />
          </el-form-item>
          <el-form-item label="支持长文本能力" prop="support_file">
            <el-switch v-model="currentLLM.support_file" active-text="支持" inactive-text="不支持" />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <div class="std-middle-box">
          <el-button round @click="showUpdateLLMForm = false"> 取消 </el-button>
          <el-button type="primary" round :disabled="!currentLLM?.is_editable" @click="commitUpdateLLMInstance">
            更新
          </el-button>
        </div>
      </template>
    </el-dialog>
  </el-container>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  align-items: center;
  justify-content: center;
}
.model-list-main {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 12px;
}
#model-list-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  width: calc(100% - 40px);
  min-width: 200px;
  padding: 4px 20px;
}
#model-list-area {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 12px;
  height: calc(100vh - 200px);
  align-items: flex-start;
  justify-content: flex-start;
  align-content: flex-start;
}
.llm-card {
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
.llm-card:hover::before {
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
#model-list-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}
.card-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.llm-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
}
.card-body {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  height: 60px;
}
.card-foot {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  flex-wrap: wrap;
}
.author-avatar {
  width: 24px;
  height: 24px;
}
.llm-tags {
  display: flex;
  flex-direction: row;
  gap: 4px;
  flex-wrap: wrap;
}
.new-llm {
  max-width: 900px;
  width: 100%;
}
.card-button {
  position: absolute;
  top: 8px;
  right: 8px;
  cursor: pointer;
}
.card-button-icon {
  &:focus {
    outline: none;
  }
}
.filter-condition {
  min-width: 160px;
}
.disabled-mask {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色遮罩 */
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 20; /* 确保遮罩层显示在内容之上 */
}

.disabled-text {
  color: white;
  font-size: 24px;
  font-weight: bold;
}
.welcome-area {
  width: calc(100vw - 120px);
  height: calc(100vh - 250px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.intro-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  padding: 40px;
}
</style>
