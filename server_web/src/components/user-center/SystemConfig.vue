<script setup lang="ts">
import { Connection, DocumentRemove, Plus, TopRight } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { computed, onMounted, reactive, ref } from 'vue';
import { domainGet } from '@/api/base';
import { api as resourceApi } from '@/api/resource-api';
import { llmInstanceSearch, systemConfigGet, systemConfigUpdate } from '@/api/user-center';
import { useUserConfigStore } from '@/stores/user-config-store';
import { useUserInfoStore } from '@/stores/user-info-store';
import { ILLMInstance, ISystemConfig } from '@/types/user-center';
const userInfoStore = useUserInfoStore();
const userConfigStore = useUserConfigStore();
const localSystemConfig = reactive<Partial<ISystemConfig>>({});
const availAbleModels = ref<ILLMInstance[]>([]);
const embeddingModels = computed(() => availAbleModels.value.filter(item => item.llm_type === '向量模型'));
const rerankModels = computed(() => availAbleModels.value.filter(item => item.llm_type === '排序模型'));
const aiRef = ref(null);
const connectorsRef = ref(null);
const toolsRef = ref(null);
const opsRef = ref(null);
const aiFormRules = {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  'xiaoyi.llm_code': [
    {
      required: true,
      message: '请选择默认模型',
      trigger: 'change'
    }
  ],
  // eslint-disable-next-line @typescript-eslint/naming-convention
  'xiaoyi.name': [
    {
      required: true,
      message: '请输入助手名称',
      trigger: 'blur'
    },
    {
      min: 2,
      max: 20,
      message: '助手名称长度在2-20个字符之间',
      trigger: 'blur'
    }
  ],
  // eslint-disable-next-line @typescript-eslint/naming-convention
  'xiaoyi.avatar_url': [
    {
      required: true,
      message: '请上传助手图标',
      trigger: 'change'
    }
  ],
  // eslint-disable-next-line @typescript-eslint/naming-convention
  'embedding.embedding_endpoint': [
    {
      type: 'url',
      trigger: 'change',
      message: '请输入正确的URL地址'
    }
  ],
  // eslint-disable-next-line @typescript-eslint/naming-convention
  'rerank.rerank_endpoint': [
    {
      type: 'url',
      trigger: 'change',
      message: '请输入正确的URL地址'
    }
  ],
  // eslint-disable-next-line @typescript-eslint/naming-convention
  'stt.xf_api': [
    {
      type: 'url',
      trigger: 'change',
      message: '请输入正确的URL地址'
    }
  ]
};
const connectorsFormRules = {};
const toolsFormRules = {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  'search_engine.endpoint': [
    {
      type: 'url',
      trigger: 'change',
      message: '请输入正确的URL地址'
    }
  ]
};
const opsFormRules = {};
const adminDomain = ref('');
async function handleChangeUpdate(configKey: string) {
  const refMap = {
    ai: aiRef,
    connectors: connectorsRef,
    tools: toolsRef,
    ops: opsRef
  };
  const valid = await refMap[configKey].value?.validate();
  if (!valid) {
    console.log(valid);
    return;
  }
  const res = await systemConfigUpdate({
    config_key: configKey,
    config_value: localSystemConfig[configKey]
  });
  if (!res.error_status) {
    userConfigStore.updateSystemConfig({ configKey: localSystemConfig[configKey] } as Partial<ISystemConfig>);
    ElMessage.success({
      message: '更新成功',
      type: 'success',
      duration: 3000
    });
  }
}
function getLLMDesc(llmCode: string) {
  const llm = availAbleModels.value.find(item => item.llm_code === llmCode);
  return llm ? llm.llm_label : llmCode;
}
function getLLMIcon(llmCode: string) {
  const llm = availAbleModels.value.find(item => item.llm_code === llmCode);
  return llm ? llm.llm_icon : '';
}
async function getSystemConfigs() {
  const res = await systemConfigGet({});
  if (!res.error_status) {
    Object.assign(localSystemConfig, res.result);
    userConfigStore.updateSystemConfig(res.result);
  }
}
function addNewConnector() {
  localSystemConfig.connectors.weixin.push({
    domain: '',
    wx_app_id: '',
    wx_app_secret: ''
  });
}
function removeConnector(index: number) {
  localSystemConfig.connectors.weixin.splice(index, 1);
  ElMessage.success('配置已删除');
}
async function handleUploadLogoSuccess(res: any) {
  if (!res.error_status) {
    localSystemConfig.ops.brand.logo_url = res.result.url;
    handleChangeUpdate('ops');
  }
}
async function handleUploadFullLogoSuccess(res: any) {
  if (!res.error_status) {
    localSystemConfig.ops.brand.logo_full_url = res.result.url;
    handleChangeUpdate('ops');
  }
}
async function toLLMCreate() {
  const res = await domainGet({});
  if (!res.error_status) {
    adminDomain.value = res.result.admin_domain;
  }
  if (adminDomain.value) {
    window.open(`${adminDomain.value}/next-console/app-center/llm-create`, '_blank');
    return;
  }
  ElMessage.info('请先配置系统域名');
}
async function handleUploadXiaoyiAvatarSuccess(res: any) {
  if (!res.error_status) {
    localSystemConfig.ai.xiaoyi.avatar_url = res.result.url;
    handleChangeUpdate('ai');
  }
}
onMounted(async () => {
  getSystemConfigs();
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
        <div v-if="localSystemConfig?.ai" class="form-area">
          <div>
            <el-text class="form-label-text">AI组件</el-text>
          </div>
          <div class="form-area-body">
            <el-form ref="aiRef" label-width="auto" :model="localSystemConfig.ai" :rules="aiFormRules">
              <div class="sub-title">
                <el-text>内置官方AI助手</el-text>
              </div>
              <el-form-item label="默认模型:" label-position="left" prop="xiaoyi.llm_code">
                <el-select v-model="localSystemConfig.ai.xiaoyi.llm_code" @change="handleChangeUpdate('ai')">
                  <template #label="{ label }">
                    <div class="llm-instance-item">
                      <div class="std-middle-box">
                        <el-avatar
                          :src="getLLMIcon(label)"
                          style="width: 20px; height: 20px; background-color: white"
                          fit="contain"
                        />
                      </div>
                      <div class="std-middle-box" style="justify-content: flex-start">
                        <el-text truncated style="font-size: 14px; font-weight: 500; line-height: 20px; color: #344054">
                          {{ getLLMDesc(label) }}
                        </el-text>
                      </div>
                    </div>
                  </template>
                  <el-option v-for="llm in availAbleModels" :key="llm.llm_code" :value="llm.llm_code">
                    <div class="llm-options">
                      <div>
                        <el-image :src="llm.llm_icon" style="width: 12px; height: 12px" />
                      </div>
                      <div>
                        <el-text>{{ llm.llm_label }}</el-text>
                      </div>
                    </div>
                  </el-option>
                  <el-button class="to-llm-button" :icon="TopRight" @click="toLLMCreate">前往模型配置 </el-button>
                </el-select>
              </el-form-item>
              <el-form-item label="助手名称：" label-position="left" prop="xiaoyi.name">
                <el-input v-model="localSystemConfig.ai.xiaoyi.name" @change="handleChangeUpdate('ai')" />
              </el-form-item>
              <el-form-item label="助手头像：" label-position="left" prop="xiaoyi.avatar_url">
                <div style="display: flex; gap: 12px">
                  <el-image
                    v-if="localSystemConfig.ai.xiaoyi.avatar_url"
                    :src="localSystemConfig.ai.xiaoyi.avatar_url"
                    class="assistant-avatar"
                  />
                  <el-upload
                    v-model="localSystemConfig.ai.xiaoyi.avatar_url"
                    list-type="picture-card"
                    :limit="1"
                    accept=".png, .jpg, .jpeg, .svg, .gif, .bmp, .webp"
                    name="data"
                    :headers="userInfoStore.userHeader"
                    :action="resourceApi.upload_resource"
                    :on-success="handleUploadXiaoyiAvatarSuccess"
                  >
                    <el-icon><Plus /></el-icon>
                  </el-upload>
                </div>
              </el-form-item>
              <div class="sub-title">
                <el-text>向量化模型</el-text>
              </div>
              <el-form-item label="启用" label-position="left" prop="embedding.enable">
                <el-switch v-model="localSystemConfig.ai.embedding.enable" @change="handleChangeUpdate('ai')" />
              </el-form-item>
              <el-form-item label="默认模型" label-position="left" prop="embedding.llm_code">
                <el-select v-model="localSystemConfig.ai.embedding.llm_code" @change="handleChangeUpdate('ai')">
                  <template #label="{ label }">
                    <div class="llm-instance-item">
                      <div class="std-middle-box">
                        <el-avatar
                          :src="getLLMIcon(label)"
                          style="width: 20px; height: 20px; background-color: white"
                          fit="contain"
                        />
                      </div>
                      <div class="std-middle-box" style="justify-content: flex-start">
                        <el-text truncated style="font-size: 14px; font-weight: 500; line-height: 20px; color: #344054">
                          {{ getLLMDesc(label) }}
                        </el-text>
                      </div>
                    </div>
                  </template>
                  <el-option v-for="llm in embeddingModels" :key="llm.llm_code" :value="llm.llm_code">
                    <div class="llm-options">
                      <div>
                        <el-image :src="llm.llm_icon" style="width: 12px; height: 12px" />
                      </div>
                      <div>
                        <el-text>{{ llm.llm_label }}</el-text>
                      </div>
                    </div>
                  </el-option>
                  <el-button class="to-llm-button" :icon="TopRight" @click="toLLMCreate">前往模型配置 </el-button>
                </el-select>
              </el-form-item>
              <el-form-item label="阈值" label-position="left" prop="embedding.threshold">
                <el-slider
                  v-model="localSystemConfig.ai.embedding.threshold"
                  :max="1"
                  :min="0"
                  :step="0.1"
                  show-input
                  @change="handleChangeUpdate('ai')"
                />
              </el-form-item>
              <el-form-item label="Top-K" label-position="left" prop="embedding.topK">
                <el-input-number
                  v-model="localSystemConfig.ai.embedding.topK"
                  :max="100"
                  :min="1"
                  :step="1"
                  @change="handleChangeUpdate('ai')"
                />
              </el-form-item>
              <div class="sub-title">
                <el-text>重排序模型</el-text>
              </div>
              <el-form-item label="启用" label-position="left" prop="rerank.enable">
                <el-switch v-model="localSystemConfig.ai.rerank.enable" @change="handleChangeUpdate('ai')" />
              </el-form-item>
              <el-form-item label="默认模型" label-position="left" prop="rerank.llm_code">
                <el-select v-model="localSystemConfig.ai.rerank.llm_code" @change="handleChangeUpdate('ai')">
                  <template #label="{ label }">
                    <div class="llm-instance-item">
                      <div class="std-middle-box">
                        <el-avatar
                          :src="getLLMIcon(label)"
                          style="width: 20px; height: 20px; background-color: white"
                          fit="contain"
                        />
                      </div>
                      <div class="std-middle-box" style="justify-content: flex-start">
                        <el-text truncated style="font-size: 14px; font-weight: 500; line-height: 20px; color: #344054">
                          {{ getLLMDesc(label) }}
                        </el-text>
                      </div>
                    </div>
                  </template>
                  <el-option v-for="llm in rerankModels" :key="llm.llm_code" :value="llm.llm_code">
                    <div class="llm-options">
                      <div>
                        <el-image :src="llm.llm_icon" style="width: 12px; height: 12px" />
                      </div>
                      <div>
                        <el-text>{{ llm.llm_label }}</el-text>
                      </div>
                    </div>
                  </el-option>
                  <el-button class="to-llm-button" :icon="TopRight" @click="toLLMCreate">前往模型配置 </el-button>
                </el-select>
              </el-form-item>
              <el-form-item label="阈值" label-position="left" prop="rerank.threshold">
                <el-slider
                  v-model="localSystemConfig.ai.rerank.threshold"
                  :max="1"
                  :min="-1"
                  :step="0.1"
                  show-input
                  @change="handleChangeUpdate('ai')"
                />
              </el-form-item>
              <el-form-item label="Top-K" label-position="left" prop="rerank.topK">
                <el-input-number
                  v-model="localSystemConfig.ai.rerank.topK"
                  :max="100"
                  :min="1"
                  :step="1"
                  @change="handleChangeUpdate('ai')"
                />
              </el-form-item>
              <div class="sub-title">
                <el-text>语音识别</el-text>
              </div>
              <el-form-item label="供应商:" label-position="left">
                <el-select v-model="localSystemConfig.ai.stt.provider" @change="handleChangeUpdate('ai')" />
              </el-form-item>
              <el-form-item label="访问地址:" label-position="left" prop="stt.xf_api">
                <el-input v-model="localSystemConfig.ai.stt.xf_api" @change="handleChangeUpdate('ai')" />
              </el-form-item>
              <el-form-item label="应用id:" label-position="left">
                <el-input v-model="localSystemConfig.ai.stt.xf_api_id" @change="handleChangeUpdate('ai')" />
              </el-form-item>
              <el-form-item label="应用公钥:" label-position="left">
                <el-input v-model="localSystemConfig.ai.stt.xf_api_key" @change="handleChangeUpdate('ai')" />
              </el-form-item>
              <el-form-item label="应用秘钥:" label-position="left">
                <el-input
                  v-model="localSystemConfig.ai.stt.xf_api_secret"
                  show-password
                  type="password"
                  @change="handleChangeUpdate('ai')"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="localSystemConfig?.connectors" class="form-area">
          <div>
            <el-text class="form-label-text">连接授权</el-text>
          </div>
          <div class="form-area-body">
            <el-form
              ref="connectorsRef"
              label-width="auto"
              :model="localSystemConfig.connectors"
              :rules="connectorsFormRules"
            >
              <div class="sub-title">
                <el-text>微信</el-text>
              </div>
              <div v-if="!localSystemConfig.connectors.weixin?.length" class="empty-state">
                <el-icon><DocumentRemove /></el-icon>
                <p>暂无微信连接器配置</p>
                <el-button type="primary" @click="addNewConnector">添加配置</el-button>
              </div>
              <div v-else>
                <div v-for="(item, idx) in localSystemConfig.connectors.weixin" :key="idx" class="author-info">
                  <div class="author-header">
                    <div class="author-title">
                      <el-icon><Connection /></el-icon>
                      <span>微信连接器 #{{ idx + 1 }}</span>
                      <span
                        v-if="userConfigStore.systemConfig?.connectors.weixin.includes(item)"
                        class="status-indicator"
                      >
                        已配置
                      </span>
                    </div>
                    <div class="author-actions">
                      <el-button size="small" type="danger" @click="removeConnector(idx)">删除</el-button>
                    </div>
                  </div>
                  <div class="author-content">
                    <el-form-item label="登录域名:" label-position="left">
                      <el-input v-model="item.domain" />
                    </el-form-item>
                    <el-form-item label="应用ID:" label-position="left">
                      <el-input v-model="item.wx_app_id" />
                    </el-form-item>
                    <el-form-item label="应用秘钥:" label-position="left">
                      <el-input v-model="item.wx_app_secret" type="password" show-password />
                    </el-form-item>
                  </div>
                </div>
                <div style="margin-top: 20px; text-align: center">
                  <el-button type="primary" @click="addNewConnector"> 添加登录信息 </el-button>
                  <el-button type="primary" @click="handleChangeUpdate('connectors')">保存配置</el-button>
                </div>
              </div>
            </el-form>
          </div>
        </div>
        <div v-if="localSystemConfig?.tools" class="form-area">
          <div>
            <el-text class="form-label-text">工具信息</el-text>
          </div>
          <div class="form-area-body">
            <el-form
              ref="toolsRef"
              label-width="auto"
              :model="localSystemConfig.tools"
              :rules="toolsFormRules"
              @change="handleChangeUpdate('tools')"
            >
              <div class="sub-title">
                <el-text>搜索引擎</el-text>
              </div>
              <el-form-item label="供应商:" label-position="left" prop="search_engine.provider">
                <el-select v-model="localSystemConfig.tools.search_engine.provider">
                  <el-option value="serper" />
                </el-select>
              </el-form-item>
              <el-form-item label="访问地址:" label-position="left" prop="search_engine.endpoint">
                <el-input v-model="localSystemConfig.tools.search_engine.endpoint" />
              </el-form-item>
              <el-form-item label="秘钥:" label-position="left" prop="search_engine.key">
                <el-input v-model="localSystemConfig.tools.search_engine.key" show-password type="password" />
              </el-form-item>
              <div class="sub-title">
                <el-text>短信</el-text>
              </div>
              <el-form-item label="供应商:" label-position="left" prop="sms.provider">
                <el-select v-model="localSystemConfig.tools.sms.provider">
                  <el-option value="阿里云" />
                </el-select>
              </el-form-item>
              <el-form-item label="访问地址:" label-position="left" prop="sms.endpoint">
                <el-input v-model="localSystemConfig.tools.sms.endpoint" />
              </el-form-item>
              <el-form-item label="秘钥ID:" label-position="left" prop="sms.key_id">
                <el-input v-model="localSystemConfig.tools.sms.key_id" />
              </el-form-item>
              <el-form-item label="秘钥:" label-position="left" prop="sms.key_secret">
                <el-input v-model="localSystemConfig.tools.sms.key_secret" show-password type="password" />
              </el-form-item>
              <el-form-item label="签名名称:" label-position="left" prop="sms.sign_name">
                <el-input v-model="localSystemConfig.tools.sms.sign_name" />
              </el-form-item>
              <el-form-item label="模板代码" label-position="left" prop="sms.template_code">
                <el-input v-model="localSystemConfig.tools.sms.template_code" />
              </el-form-item>
              <div class="sub-title">
                <el-text>邮箱</el-text>
              </div>
              <el-form-item label="服务器地址:" label-position="left" prop="email.smtp_server">
                <el-input v-model="localSystemConfig.tools.email.smtp_server" />
              </el-form-item>
              <el-form-item label="服务器端口:" label-position="left" prop="email.smtp_port">
                <el-input v-model="localSystemConfig.tools.email.smtp_port" />
              </el-form-item>
              <el-form-item label="用户名:" label-position="left" prop="email.smtp_user">
                <el-input v-model="localSystemConfig.tools.email.smtp_user" />
              </el-form-item>
              <el-form-item label="密码:" label-position="left" prop="email.smtp_password">
                <el-input v-model="localSystemConfig.tools.email.smtp_password" show-password type="password" />
              </el-form-item>
              <div class="sub-title">
                <el-text>WPS</el-text>
              </div>
              <el-form-item label="启用:" label-position="left" prop="wps.enabled">
                <el-switch v-model="localSystemConfig.tools.wps.enabled" @change="handleChangeUpdate('tools')" />
              </el-form-item>
              <el-form-item label="应用ID:" label-position="left" prop="wps.app_id">
                <el-input v-model="localSystemConfig.tools.wps.app_id" />
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-if="localSystemConfig?.ops" class="form-area">
          <div>
            <el-text class="form-label-text">运维配置</el-text>
          </div>
          <div class="form-area-body">
            <el-form
              ref="opsRef"
              label-width="auto"
              :model="localSystemConfig.ops"
              :rules="opsFormRules"
              @change="handleChangeUpdate('ops')"
            >
              <div class="sub-title">
                <el-text>自主品牌</el-text>
              </div>
              <el-form-item label="自定义品牌:" label-position="left">
                <el-switch v-model="localSystemConfig.ops.brand.enable" @change="handleChangeUpdate('ops')" />
              </el-form-item>
              <el-form-item label="品牌名称:" label-position="left">
                <el-input v-model="localSystemConfig.ops.brand.brand_name" />
              </el-form-item>
              <el-form-item label="品牌小图标:" label-position="left">
                <div style="display: flex; gap: 12px">
                  <el-image
                    v-if="userConfigStore.systemConfig.ops.brand.logo_url"
                    :src="userConfigStore.systemConfig.ops.brand.logo_url"
                    :preview-src-list="[userConfigStore.systemConfig.ops.brand.logo_url]"
                    class="assistant-avatar"
                    show-progress
                  />
                  <el-upload
                    v-model="localSystemConfig.ops.brand.logo_url"
                    list-type="picture-card"
                    :limit="1"
                    accept=".png, .jpg, .jpeg, .svg, .gif, .bmp, .webp"
                    name="data"
                    :headers="userInfoStore.userHeader"
                    :action="resourceApi.upload_resource"
                    :on-success="handleUploadLogoSuccess"
                  >
                    <el-icon><Plus /></el-icon>
                  </el-upload>
                </div>
              </el-form-item>
              <el-form-item label="品牌完整图标:" label-position="left">
                <div style="display: flex; gap: 12px">
                  <el-image
                    v-if="userConfigStore.systemConfig.ops.brand.logo_full_url"
                    :src="userConfigStore.systemConfig.ops.brand.logo_full_url"
                    :preview-src-list="[userConfigStore.systemConfig.ops.brand.logo_full_url]"
                    show-progress
                    class="assistant-avatar"
                  />
                  <el-upload
                    v-model="localSystemConfig.ops.brand.logo_full_url"
                    list-type="picture-card"
                    :limit="1"
                    accept=".png, .jpg, .jpeg, .svg, .gif, .bmp, .webp"
                    name="data"
                    :headers="userInfoStore.userHeader"
                    :action="resourceApi.upload_resource"
                    :on-success="handleUploadFullLogoSuccess"
                  >
                    <el-icon><Plus /></el-icon>
                  </el-upload>
                </div>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
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
.llm-options {
  display: flex;
  flex-direction: row;
  padding: 6px;
  gap: 12px;
}
.sub-title {
  margin: 24px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eaeaea;
  position: relative;
}
.sub-title .el-text {
  font-size: 16px;
  font-weight: 600;
  color: #1f2f3d;
  letter-spacing: 1px;
}
.author-info {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
  border: 1px solid #e6e6e6;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  position: relative;
}

.author-info:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.author-info::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, #409eff, #79bbff);
  border-radius: 4px 0 0 4px;
}
.author-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #e6e6e6;
}

.author-title {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
  color: #1f2f3d;
}

.author-title .el-icon {
  margin-right: 8px;
  color: #67c23a;
}
.author-actions {
  display: flex;
  gap: 10px;
}
.author-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.author-content .el-form-item {
  margin-bottom: 0;
}

.author-content .el-form-item__label {
  font-weight: 500;
  color: #606266;
}
@media (max-width: 768px) {
  .author-content {
    grid-template-columns: 1fr;
  }

  .author-header {
    flex-direction: column;

    align-items: flex-start;

    gap: 12px;
  }

  .author-actions {
    align-self: flex-end;
  }
}
.author-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px dashed #e6e6e6;
}
/* 状态指示器 */
.status-indicator {
  display: inline-flex;
  align-items: center;
  margin-left: 12px;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  background-color: #f0f9eb;
  color: #67c23a;
}

.status-indicator::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #67c23a;
  margin-right: 4px;
}
/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
}

.empty-state .el-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.llm-instance-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  border-radius: 8px;
  margin-right: 10px;
  cursor: pointer;
}
.assistant-avatar {
  width: 148px;
  height: 148px;
  border-radius: 12px;
}
.to-llm-button {
  background: transparent;
  border: none;
  padding: 0;
  font-size: 14px;
  width: 100%;
}
</style>
