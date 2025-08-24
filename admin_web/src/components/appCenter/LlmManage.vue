<script setup lang="ts">
import {onMounted, ref, reactive} from 'vue';
import {Search, MoreFilled} from "@element-plus/icons-vue";
import type {TabsPaneContext} from 'element-plus';
import {ElMessage} from 'element-plus';
import {
  llmInstanceAdd,
  llmInstanceDel,
  llmInstanceGet,
  llmInstanceSearch,
  llmInstanceUpdate
} from "@/api/config_center";
import router from "@/router";
import {api} from "@/api/config_center";
import {getToken} from "@/utils/auth";
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
  },
  subpage: {
    type: String,
    default: 'llm'
  }
});
const currentPage = ref('llm');
const currentLLMList = ref([]);
const LLMPageSize = ref(50);
const LLMPageNum = ref(1);
const LLMListLoading = ref(false);
const LLMKeyword = ref('');
const LLMTotal = ref(0);
const currentLLM = ref({});
const LLMStatus = ref([]);
const LLMTypes = ref([]);
const currentLLMTypes = ref([]);
const currentLLMStatus = ref(['正常']);
const SupplierListLoading = ref(false);
const showNewLLMForm = ref(false);
const newLLMFormRef = ref(null);
const newLLMForm = reactive({
  llm_name: '',
  llm_type: '',
  llm_api_secret_key : '',
  llm_api_access_key : '',
  llm_icon: 'images/llm_qwen.svg',
  llm_desc: '',
  llm_tags: [],
  llm_base_url: '',
  llm_is_proxy: false,
  llm_proxy_url: '',
  llm_is_public: false,
  llm_company: '',
  support_vis: false,
  support_file: false,
  is_std_openai: true
});
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
    { min: 2, max: 200, message: '模型描述长度在2到200个字符之间', trigger: 'blur' }
  ],
  llm_icon: [
    { required: true, message: '请上传模型图标', trigger: 'blur' }
  ],
  llm_api_secret_key: [
    { required: true, message: '请输入模型API密钥', trigger: 'blur' },
    { min: 2, max: 100, message: '模型API密钥长度在2到100个字符之间', trigger: 'blur' }
  ],
  llm_base_url: [
    { required: true, message: '请输入模型API地址', trigger: 'blur' },
    { type: 'url', message: '请输入有效的URL地址', trigger: 'blur' }
  ],
}
const uploadHeader = {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  Authorization: 'Bearer ' + getToken()
};
const showDeleteLLMConfirm = ref(false);
const showUpdateLLMForm = ref(false);
const currentLLMFormRef = ref(null);
async function SearchLLMList() {
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
}
async function SearchSupplierList() {
  SupplierListLoading.value = true;
}
async function handleTabClick(tab: TabsPaneContext) {
  if (tab.paneName === 'llm') {
    SearchLLMList();
    router.replace({
      query: {
        ...router.currentRoute.value.query,
        page_num: LLMPageNum.value,
        page_size: LLMPageSize.value
      }
    });
  } else {
    SearchSupplierList();
  }
}
async function handleLLMSizeChange(val: number) {
  LLMPageSize.value = val;
  SearchLLMList();
}
async function handleLLMPageChange(val: number) {
  LLMPageNum.value = val;
  SearchLLMList();
}
async function enterLLMDetail(llm) {

}
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
    newLLMForm.llm_icon = res.result.llm_icon;
  }
}
async function handleAvatarUploadSuccess2(res: any) {
  if (!res.error_status) {
    currentLLM.value.llm_icon = res.result.llm_icon;
  }
}
async function commitNewLLMInstance() {
  const valid = await newLLMFormRef.value?.validate();
  if (!valid) {
    return;
  }
  const commitRes = await llmInstanceAdd(newLLMForm);
  if (!commitRes.error_status) {
    ElMessage.success('新建模型实例成功');
    showNewLLMForm.value = false;
    newLLMFormRef.value?.resetFields();
    SearchLLMList();
  }
}
function beginDeleteLLM(llm) {
  currentLLM.value = llm;
  showDeleteLLMConfirm.value = true;
}
async function commitDeleteLLMInstance() {
  const deleteRes = await llmInstanceDel({
    llm_codes: [currentLLM.value.llm_code],
  });
  if (!deleteRes.error_status) {
    ElMessage.success('删除模型实例成功');
    showDeleteLLMConfirm.value = false;
    SearchLLMList();
  }
}
async function beginUpdateLLMInstance(llm) {
  const res = await llmInstanceGet({
    llm_code: llm.llm_code,
  });
  if (!res.error_status) {
    currentLLM.value = res.result;
    showUpdateLLMForm.value = true;
  }
}
async function commitUpdateLLMInstance() {
  const valid = await currentLLMFormRef.value?.validate();
  if (!valid) {
    return;
  }
  const updateRes = await llmInstanceUpdate(currentLLM.value);
  if (!updateRes.error_status) {
    ElMessage.success('更新模型实例成功');
    showUpdateLLMForm.value = false;
    SearchLLMList();
  }
}
onMounted(async () => {
  if (props.subpage == 'supplier') {
    SearchSupplierList();

  } else {
    SearchLLMList();
  }
});
</script>

<template>
  <el-container>
    <el-main style="height: calc(100vh - 40px);">
      <el-tabs v-model="currentPage" @tab-click="handleTabClick">
        <el-tab-pane v-loading="LLMListLoading" label="模型管理" name="llm">
          <div id="model-list-area">
            <div id="model-list-head">
              <div id="model-list-left">
                <el-select
                    v-model="currentLLMTypes"
                    placeholder="模型种类"
                    @change="SearchLLMList"
                    clearable
                    multiple
                    collapse-tags
                >
                  <el-option v-for="type in LLMTypes" :key="type" :label="type" :value="type" />
                </el-select>
                <el-select
                    v-model="currentLLMStatus"
                    placeholder="模型状态"
                    @change="SearchLLMList"
                    clearable
                    multiple
                    collapse-tags
                >
                  <el-option v-for="status in LLMStatus" :key="status" :label="status" :value="status" />
                </el-select>
                <el-input
                    v-model="LLMKeyword"
                    placeholder="搜索模型"
                    :suffix-icon="Search"
                    @keyup.enter.prevent="SearchLLMList"
                    clearable
                    @clear="SearchLLMList"
                />
              </div>
              <div id="model-list-right">
                <el-button type="primary" round @click="showNewLLMForm = true"> 新建模型实例 </el-button>
              </div>
            </div>
            <div id="model-list-area">
              <div v-for="llm in currentLLMList" class="llm-card" @click="enterLLMDetail(llm)">
                <div class="card-head">
                  <div class="std-middle-box">
                    <el-image :src="llm.llm_icon" class="llm-icon" />
                  </div>
                  <div class="std-middle-box">
                    <el-text> {{ llm.llm_type }} </el-text>
                  </div>
                  <div class="llm-tags">
                    <el-tag v-if="llm.support_vis" type="primary">视觉能力</el-tag>
                    <el-tag v-if="llm.support_file" type="primary">长文本能力</el-tag>
                    <el-tag v-for="tag in llm.llm_tags" :key="tag"> {{ tag }} </el-tag>
                  </div>
                </div>
                <div class="card-body">
                  <div class="std-middle-box">
                    <el-text>{{ llm.llm_desc }}</el-text>
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
                      <el-avatar v-else style="background: #d1e9ff" class="author-avatar" >
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
                    <el-tag type="success" v-if="llm.llm_status=='正常'"> {{ llm.llm_status }} </el-tag>
                    <el-tag type="info" v-else> {{ llm.llm_status }} </el-tag>
                  </div>
                </div>
                <el-dropdown class="card-button">
                  <el-icon class="card-button-icon">
                    <MoreFilled />
                  </el-icon>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="beginUpdateLLMInstance(llm)">编辑</el-dropdown-item>
                      <el-dropdown-item divided>
                        <el-text type="danger" @click="beginDeleteLLM(llm)">删除</el-text>
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-main>
    <el-footer  height="40px">
      <el-pagination
        v-show="currentPage=='llm'"
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
    <el-dialog v-model="showNewLLMForm" :fullscreen="true" title="新建模型实例">
      <div class="std-middle-box">
        <el-form ref="newLLMFormRef" :model="newLLMForm" :rules="newLLMRules" class="new-llm" label-position="top">
          <el-form-item prop="llm_name" label="模型名称" required>
            <el-input v-model="newLLMForm.llm_name" placeholder="请输入模型名称（对应model参数）" clearable />
          </el-form-item>
          <el-form-item prop="llm_type" label="模型类型" required>
            <el-input v-model="newLLMForm.llm_type" placeholder="请输入模型类型（如deepseek-r1)" clearable />
          </el-form-item>
          <el-form-item prop="llm_desc" label="模型描述" required>
            <el-input v-model="newLLMForm.llm_desc" placeholder="请输入模型描述" clearable type="textarea" :rows="6" />
          </el-form-item>
          <el-form-item prop="llm_icon" label="模型图标" required>
            <el-upload
                drag
                :show-file-list="false"
                accept=".png, .jpg, .jpeg, .gif, .bmp, .webp"
                name="llm_icon"
                :headers="uploadHeader"
                :before-upload="beforeAvatarUpload"
                :action="api.llm_icon_upload"
                :on-success="handleAvatarUploadSuccess"
                style="min-width: 160px"
            >
              <div v-if="newLLMForm.llm_icon">
                <el-image :src="newLLMForm.llm_icon" style="width: 40px; height: 40px" />
              </div>
              <div v-else>
                <el-avatar src="images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              </div>
            </el-upload>
          </el-form-item>
          <el-form-item label="模型API密钥" prop="llm_api_secret_key" required>
            <el-input
                v-model="newLLMForm.llm_api_secret_key"
                placeholder="请输入模型API密钥"
                clearable
                type="password"
                show-password
            />
          </el-form-item>
          <el-form-item label="模型API访问密钥" prop="llm_api_access_key" >
            <el-input v-model="newLLMForm.llm_api_access_key"
                      placeholder="请输入模型API访问密钥"
                      clearable
                      type="password"
                      show-password
            />
          </el-form-item>
          <el-form-item label="模型API地址" prop="llm_base_url" required>
            <el-input v-model="newLLMForm.llm_base_url"
                      placeholder="请输入模型API地址（如https://api.deepseek.com/v1/chat/completions）"
                      clearable />
          </el-form-item>
          <el-form-item label="是否开启代理" prop="llm_is_proxy">
            <el-switch v-model="newLLMForm.llm_is_proxy" active-text="开启" inactive-text="关闭" />
          </el-form-item>
          <el-form-item v-show="newLLMForm.llm_is_proxy" label="代理地址" prop="llm_proxy_url">
            <el-input v-model="newLLMForm.llm_proxy_url"
                      placeholder="请输入模型代理访问地址"
                      clearable />
          </el-form-item>
          <el-form-item label="共享使用" prop="llm_is_public">
            <el-switch v-model="newLLMForm.llm_is_public" active-text="共享" inactive-text="私有" />
          </el-form-item>
          <el-form-item label="模型标签" prop="llm_tags">
            <el-select
                v-model="newLLMForm.llm_tags"
                placeholder="请选择或创建模型标签"
                multiple
                collapse-tags
                clearable
                allow-create
                filterable
                :multiple-limit="4"
            >
              <el-option v-for="tag in ['AI', 'NLP', '视觉', '语音', '多模态']" :key="tag" :label="tag" :value="tag" />
            </el-select>
          </el-form-item>
          <el-form-item label="模型供应商" prop="llm_company">
            <el-input v-model="newLLMForm.llm_company"
                      placeholder="请输入模型供应商名称"
                      clearable />
          </el-form-item>
          <el-form-item label="支持OpenAI-SDK" prop="is_std_openai">
            <el-switch v-model="newLLMForm.is_std_openai" active-text="是" inactive-text="否" />
          </el-form-item>
          <el-form-item label="支持视觉能力" prop="support_vis">
            <el-switch v-model="newLLMForm.support_vis" active-text="支持" inactive-text="不支持" />
          </el-form-item>
          <el-form-item label="支持长文本能力" prop="support_file">
            <el-switch v-model="newLLMForm.support_file" active-text="支持" inactive-text="不支持" />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <div class="std-middle-box">
          <el-button @click="showNewLLMForm = false" round> 取消 </el-button>
          <el-button type="primary" @click="commitNewLLMInstance" round> 确认 </el-button>
        </div>
      </template>
    </el-dialog>
    <el-dialog v-model="showDeleteLLMConfirm" title="删除模型实例">
      <el-result :title="'删除选中模型实例:' + currentLLM.llm_name + '?'" icon="error" sub-title="此删除操作无法回退，请谨慎操作！" />
      <template #footer>
        <div class="std-middle-box">
          <el-button @click="showDeleteLLMConfirm = false" round> 取消 </el-button>
          <el-button type="danger" @click="commitDeleteLLMInstance" round> 确认删除 </el-button>
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
            <el-input
                v-model="currentLLM.llm_name"
                placeholder="请输入模型名称（对应model参数）"
                clearable
            />
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
                :headers="uploadHeader"
                :before-upload="beforeAvatarUpload"
                :action="api.llm_icon_upload"
                :on-success="handleAvatarUploadSuccess2"
                style="min-width: 160px"
            >
              <div v-if="currentLLM.llm_icon">
                <el-image :src="currentLLM.llm_icon" style="width: 40px; height: 40px" />
              </div>
              <div v-else>
                <el-avatar src="images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
                <i class="el-icon-upload"></i>
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
          <el-form-item label="模型API访问密钥" prop="llm_api_access_key">
            <el-input v-model="currentLLM.llm_api_access_key"
                      placeholder="请输入模型API访问密钥"
                      clearable
                      type="password"
                      show-password
            />
          </el-form-item>
          <el-form-item label="模型API地址" prop="llm_base_url" required>
            <el-input v-model="currentLLM.llm_base_url"
                      placeholder="请输入模型API地址（如https://api.deepseek.com/v1/chat/completions）"
                      clearable />
          </el-form-item>
          <el-form-item label="是否开启代理" prop="llm_is_proxy">
            <el-switch v-model="currentLLM.llm_is_proxy" active-text="开启" inactive-text="关闭" />
          </el-form-item>
          <el-form-item v-show="currentLLM.llm_is_proxy" label="代理地址" prop="llm_proxy_url">
            <el-input v-model="currentLLM.llm_proxy_url"
                      placeholder="请输入模型代理访问地址"
                      clearable />
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
            <el-input v-model="currentLLM.llm_company"
                      placeholder="请输入模型供应商名称"
                      clearable />
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
          <el-button @click="showUpdateLLMForm = false" round> 取消 </el-button>
          <el-button type="primary" @click="commitUpdateLLMInstance" round :disabled="!currentLLM?.is_editable">
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
#model-list-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
}
#model-list-area {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}
.llm-card {
  width: 420px;
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
</style>
