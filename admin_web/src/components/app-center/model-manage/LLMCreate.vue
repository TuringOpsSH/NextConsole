<script setup lang="ts">
import { Search, SetUp, Share, Shop, Aim, Connection, ChatLineSquare, SuccessFilled } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { computed, type CSSProperties, onMounted, reactive, ref } from 'vue';
import { api, llmHealthCheck, llmInstanceAdd, llmSupplierDetail, llmSupplierSearch } from '@/api/config-center';
import JsonSchemaForm from '@/components/app-center/app-manage/JsonSchemaForm.vue';
import AuthorSelector from '@/components/app-center/model-manage/AuthorSelector.vue';
import router from '@/router';
import { useUserInfoStore } from '@/stores/user-info-store';
import { ILLMInstance, ISupplier } from '@/types/config-center';

const props = defineProps({
  step: {
    type: String,
    default: '0',
    required: false
  }
});
const userInfoStore = useUserInfoStore();
const stepInfo = ref([
  {
    title: '选择供应商与模型',
    content: '选择您想要添加的模型供应商与具体模型',
    icon: Shop
  },
  {
    title: '配置模型参数',
    content: '填写模型的API密钥、API地址等相关参数',
    icon: SetUp
  },
  {
    title: '健康测试',
    content: '测试所填写的参数是否正确，确保能够成功连接到模型服务',
    icon: Aim
  },
  {
    title: '授权确认',
    content: '确认并授权所添加的模型实例，完成添加流程',
    icon: Share
  }
]);
const supplierTypes = ['本地化', '国内', '国际'];
const currentStep = ref(0);
const suppliers = ref<ISupplier[]>([]);
const supplierKeyWord = ref('');
const supplierType = ref('本地化');
const currentSupplier = reactive<ISupplier>({
  create_time: '',
  id: 0,
  supplier_code: '',
  supplier_desc: '',
  supplier_icon: '',
  supplier_models: [],
  supplier_name: '',
  supplier_status: '',
  supplier_website: '',
  supplier_api_url: '',
  update_time: ''
});
const newLLMFormRef = ref(null);
const newLLMForm = reactive<ILLMInstance>({
  id: 0,
  create_time: '',
  llm_code: '',
  llm_status: '',
  update_time: '',
  llm_name: '',
  llm_label: '',
  llm_type: '文本生成',
  stream: true,
  llm_api_secret_key: '',
  llm_icon: '/images/llm_qwen.svg',
  llm_desc: '',
  llm_tags: [],
  llm_base_url: '',
  llm_is_public: false,
  llm_company: '',
  support_vis: false,
  support_file: false,
  is_std_openai: true,
  use_default: true,
  temperature: 1,
  frequency_penalty: 0,
  top_p: 1,
  presence_penalty: 0,
  max_tokens: 1280000,
  extra_headers: {
    properties: {},
    ncOrders: []
  },
  extra_body: {
    properties: {},
    ncOrders: []
  },
  llm_authors: []
});
const newLLMRules = {
  llm_label: [
    { required: true, message: '请输入模型名称', trigger: 'blur' },
    { min: 2, max: 50, message: '模型编号长度在2到30个字符之间', trigger: 'blur' }
  ],
  llm_name: [
    { required: true, message: '请输入模型编号', trigger: 'blur' },
    { min: 2, max: 50, message: '模型编号在2到50个字符之间', trigger: 'blur' }
  ],
  llm_type: [
    { required: true, message: '请输入模型类型', trigger: 'blur' },
    { min: 2, max: 50, message: '模型类型长度在2到50个字符之间', trigger: 'blur' }
  ],
  llm_desc: [{ max: 2000, message: '模型描述长度在2000个字符以内', trigger: 'blur' }],
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
const suppliersLoading = ref(false);
const supplierLoading = ref(false);
const moreConfigVis = ref(false);
const moreConfigTab = ref('base');
const allModelType = [
  {
    label: '文本生成',
    value: '文本生成'
  },
  {
    label: '图片生成',
    value: '图片生成'
  },
  {
    label: '推理模型',
    value: '推理模型'
  },
  {
    label: '图片理解',
    value: '图片理解'
  },
  {
    label: '视频理解',
    value: '视频理解',
    disable: true
  },
  {
    label: '语音识别',
    value: '语音识别',
    disable: true
  },
  {
    label: '语音合成',
    value: '语音合成',
    disable: true
  },
  {
    label: '视频生成',
    value: '视频生成',
    disable: true
  },
  {
    label: '全模态',
    value: '全模态'
  },
  {
    label: '向量模型',
    value: '向量模型'
  },
  {
    label: '排序模型',
    value: '排序模型'
  },
  {
    label: '音频理解',
    value: '音频理解',
    disable: true
  },
  {
    label: '图像处理',
    value: '图像处理',
    disable: true
  }
];
const allSupportCompany = ref([]);
interface IMark {
  style: CSSProperties;
  label: string;
}
// eslint-disable-next-line @typescript-eslint/naming-convention
type Marks = Record<number, IMark | string>;
const temperatureMarks = reactive<Marks>({
  // eslint-disable-next-line @typescript-eslint/naming-convention
  0: '0-精确',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  1: '1-平衡',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  2: '2-创意'
});
const topPMarks = reactive<Marks>({
  // eslint-disable-next-line @typescript-eslint/naming-convention
  0: '0',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  0.5: '0.5',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  1: '1'
});
const frequencyPenaltyMarks = reactive<Marks>({
  // eslint-disable-next-line @typescript-eslint/naming-convention
  '-2': '-2',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  0: '0',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  1: '1',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  2: '2'
});
const modelTestStep = ref(0);
const modelTesting = ref(false);
const modelTestStatus = ref('process');
const modelTestResult = ref([]);
const nextStepDisabled = computed(() => {
  if (currentStep.value == 2 && modelTestStep.value < 3) {
    return true;
  }
  return false;
});
const authorSelectorRef = ref(null);
async function diyModel() {
  currentStep.value = 1;
  router.replace({
    query: { step: currentStep.value.toString() }
  });
  moreConfigVis.value = true;
  stepInfo.value[0].content = '自定义模型';
}
async function handleBackStep() {
  if (currentStep.value) {
    currentStep.value -= 1;
    router.replace({
      query: { step: currentStep.value.toString() }
    });
  }
}
async function handleForwardStep() {
  if (currentStep.value < 3) {
    if (currentStep.value == 0) {
      if (!newLLMForm.llm_name) {
        ElMessage.info('请选择一个模型');
        return;
      }
      moreConfigVis.value = false;
    } else if (currentStep.value == 1) {
      try {
        await newLLMFormRef.value?.validate();
      } catch (e) {
        ElMessage.warning('请完善模型参数信息');
        return;
      }
    }
    currentStep.value += 1;
    router.replace({
      query: { step: currentStep.value.toString() }
    });
    if (currentStep.value == 2) {
      checkModelConfig();
    } else if (currentStep.value == 3) {
      authorSelectorRef.value?.initShareSelector();
    }
  }
}
async function chooseSupplier(item: ISupplier) {
  supplierLoading.value = true;
  const res = await llmSupplierDetail({
    supplier_id: item.id
  });
  if (!res.error_status) {
    Object.assign(currentSupplier, res.result);
  }
  supplierLoading.value = false;
}
async function refreshLLMSuppliers() {
  suppliersLoading.value = true;
  const params = {
    fetch_all: true,
    keyword: supplierKeyWord.value,
    types: [supplierType.value]
  };
  const res = await llmSupplierSearch(params);
  if (!res.error_status) {
    suppliers.value = res.result.data;
  }
  suppliersLoading.value = false;
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
function translateMaxTokens(maxTokens: number) {
  if (!maxTokens || maxTokens <= 0) {
    return '不限制';
  }
  if (maxTokens > 1024 * 1024) {
    return `${(maxTokens / 1024 / 1024).toFixed(0)} M Token`;
  }
  if (maxTokens > 1024) {
    return `${(maxTokens / 1024).toFixed(0)} K Token`;
  }
  return `${maxTokens} Token`;
}
function handleModelChange(val) {
  newLLMForm.llm_label = val.llm_label;
  newLLMForm.llm_name = val.llm_name;
  newLLMForm.is_std_openai = true;
  if (val.llm_type) {
    newLLMForm.llm_type = val.llm_type;
    if (val.llm_type == '排序模型') {
      newLLMForm.is_std_openai = false;
    } else if (val.llm_type == '推理模型') {
      newLLMForm.extra_body.properties['enable_thinking'] = {
        type: 'boolean',
        typeName: 'boolean',
        value: '',
        ref: true,
        showSubArea: true,
        description: ''
      };
      // @ts-ignore
      newLLMForm.extra_body.ncOrders.push('enable_thinking');
    } else if (['图片生成', '视频生成'].includes(val.llm_type)) {
      newLLMForm.is_std_openai = false;
    }
  }
  newLLMForm.llm_tags = val.llm_tags;
  newLLMForm.llm_desc = val.llm_desc;
  newLLMForm.max_tokens = val.max_tokens;
  if (val.llm_icon) {
    newLLMForm.llm_icon = val.llm_icon;
  }
  newLLMForm.llm_code = val.llm_code;
  newLLMForm.llm_company = currentSupplier.supplier_name;
  newLLMForm.llm_base_url = currentSupplier.supplier_api_url;
  newLLMForm.support_vis = val.llm_type == '图片理解';
  stepInfo.value[0].content = `${newLLMForm.llm_company} - ${newLLMForm.llm_label}`;
}
function beforeAvatarUpload(file: File) {
  const isLt5M = file.size / 1024 / 1024 < 5;
  if (!isLt5M) {
    ElMessage.info('上传头像图片大小不能超过 5MB!');
  }
  return isLt5M;
}
async function handleAvatarUploadSuccess(res: any) {
  if (!res.error_status) {
    newLLMForm.llm_icon = res.result.llm_icon;
  }
}
function switchMoreConfig() {
  moreConfigVis.value = !moreConfigVis.value;
}
async function checkModelConfig() {
  modelTestStep.value = 0;
  modelTesting.value = true;
  modelTestStatus.value = 'process';
  for (let step = modelTestStep.value; step < 3; step++) {
    modelTestStep.value = step;
    const res = await llmHealthCheck({
      model: newLLMForm,
      step: step
    });
    modelTestResult.value[step] = res.result;
    console.log(res.result?.status);
    if (res.result?.status != '成功') {
      modelTestStatus.value = 'error';
      modelTesting.value = false;
      return;
    }
  }
  modelTestStatus.value = 'process';
  modelTestStep.value += 1;
  modelTesting.value = false;
}

async function commitNewLLMInstance() {
  const valid = await newLLMFormRef.value?.validate();
  if (!valid) {
    return;
  }
  const commitRes = await llmInstanceAdd(newLLMForm);
  if (!commitRes.error_status) {
    ElMessage.success('新建模型实例成功');
    router.push({
      name: 'llmDetail',
      params: {
        llmCode: commitRes.result.llm_code
      }
    });
  }
}
async function getAllSupportCompany() {
  const res = await llmSupplierSearch({
    fetch_all: true,
    types: ['本地化', '国内', '国际']
  });
  if (!res.error_status) {
    const companySet = new Set<string>();
    res.result.data.forEach(supplier => {
      if (supplier.supplier_name) {
        companySet.add(supplier.supplier_name);
      }
    });
    allSupportCompany.value.push(...Array.from(companySet).sort());
  }
}
onMounted(() => {
  try {
    const stepParam = parseInt(props.step);

    if (stepParam >= 0 && stepParam <= 3) {
      currentStep.value = stepParam;
    }
    // if (!newLLMForm.llm_name) {
    //   currentStep.value = 0;
    // }
  } catch (error) {
    currentStep.value = 0;
  }
  router.replace({
    query: { step: currentStep.value.toString() }
  });
  refreshLLMSuppliers();
  getAllSupportCompany();
});
</script>

<template>
  <el-container>
    <el-header :height="200">
      <div class="step-area">
        <div class="step-left">
          <el-text size="large"> 新建模型实例 </el-text>
        </div>
        <div class="step-right">
          <el-steps :active="currentStep">
            <el-step
              v-for="(item, idx) in stepInfo"
              :key="idx"
              :title="item.title"
              :description="item.content"
              :icon="item.icon"
            />
          </el-steps>
        </div>
      </div>
    </el-header>
    <el-main style="padding: 0">
      <el-scrollbar>
        <div class="main-area">
          <div v-show="currentStep == 0" class="step-one-area">
            <div class="supply-area">
              <div>
                <el-segmented v-model="supplierType" :options="supplierTypes" block @change="refreshLLMSuppliers" />
              </div>
              <div class="pane-area">
                <div>
                  <el-input
                    v-model="supplierKeyWord"
                    :suffix-icon="Search"
                    placeholder="搜索模型供应商"
                    clearable
                    @change="refreshLLMSuppliers"
                  />
                </div>
                <el-scrollbar>
                  <div v-loading="suppliersLoading" class="supplier-list">
                    <div v-if="supplierType == '本地化'" class="supplier-box" @click="diyModel">
                      <div class="supplier-icon-box">
                        <el-avatar
                          src="/images/logo.svg"
                          class="supplier-icon"
                          fit="scale-down"
                          size="large"
                          shape="square"
                        />
                      </div>
                      <div class="supplier-name-area">
                        <div>
                          <el-text class="supplier-name"> 自定义模型 </el-text>
                        </div>
                        <div class="supplier-desc">
                          <el-text> 自定义接入的本地化模型 </el-text>
                        </div>
                      </div>
                    </div>
                    <div
                      v-for="item in suppliers"
                      :key="item.id"
                      class="supplier-box"
                      :class="item.id == currentSupplier.id ? 'supplier-box-active' : ''"
                      @click="chooseSupplier(item)"
                    >
                      <div class="supplier-icon-box">
                        <el-avatar
                          :src="item.supplier_icon"
                          class="supplier-icon"
                          fit="scale-down"
                          size="large"
                          shape="square"
                        />
                      </div>
                      <div class="supplier-name-area">
                        <div>
                          <el-text class="supplier-name">
                            {{ item.supplier_name }}
                          </el-text>
                        </div>
                        <div class="supplier-desc">
                          <el-text>
                            {{ item.supplier_desc }}
                          </el-text>
                        </div>
                      </div>
                    </div>
                  </div>
                </el-scrollbar>
                <div v-if="!suppliers?.length && supplierKeyWord">
                  <el-result title="没有找到关联的模型供应商" sub-title="请联系平台管理员" />
                </div>
                <div v-else-if="!suppliers?.length && !supplierKeyWord && !suppliersLoading">
                  <el-result title="暂无模型供应商" sub-title="请联系平台管理员" />
                </div>
              </div>
            </div>
            <div v-loading="supplierLoading" element-loading-text="加载中" class="models-area">
              <el-table
                v-if="currentSupplier?.supplier_models?.length"
                :data="currentSupplier.supplier_models"
                stripe
                border
                height="100%"
                highlight-current-row
                @current-change="handleModelChange"
              >
                <el-table-column type="index" label="序号" width="60" />
                <el-table-column prop="llm_label" label="模型名称" sortable width="300" />
                <el-table-column prop="llm_name" label="模型编号" sortable width="200" />
                <el-table-column prop="llm_type" label="模型类型" sortable width="120" />
                <el-table-column prop="llm_desc" label="模型描述" min-width="240" show-overflow-tooltip />
                <el-table-column prop="llm_tags" label="模型能力" width="240">
                  <template #default="scope">
                    <el-tag
                      v-for="(tag, index) in scope.row.llm_tags"
                      :key="index"
                      style="margin-right: 4px; margin-bottom: 4px"
                    >
                      {{ translateTag(tag) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="max_tokens" label="上下文长度" sortable width="200">
                  <template #default="scope">
                    {{ translateMaxTokens(scope.row.max_tokens) }}
                  </template>
                </el-table-column>
              </el-table>
              <div v-else class="empty-models-area">
                <el-empty description="暂无支持的模型" />
              </div>
            </div>
          </div>
          <div v-show="currentStep == 1" class="step-two-area">
            <el-form
              ref="newLLMFormRef"
              :model="newLLMForm"
              :rules="newLLMRules"
              status-icon
              label-position="top"
              class="new-llm"
            >
              <el-form-item label="模型API密钥" prop="llm_api_secret_key" required>
                <el-input
                  v-model="newLLMForm.llm_api_secret_key"
                  placeholder="请输入模型API密钥，如果是未鉴权模型，可以填写随机字符"
                  clearable
                  type="password"
                  show-password
                />
              </el-form-item>
              <el-divider>
                <el-button type="primary" @click="switchMoreConfig">更多配置</el-button>
              </el-divider>
              <el-tabs v-show="moreConfigVis" v-model="moreConfigTab" type="border-card">
                <el-tab-pane name="base" label="基础信息">
                  <el-form-item label="模型API地址" prop="llm_base_url" required>
                    <el-input
                      v-model="newLLMForm.llm_base_url"
                      placeholder="如https://api.deepseek.com/v1 Tips: 本地化模型请不要添加/chat/completions等后续路径"
                      clearable
                    />
                  </el-form-item>
                  <el-form-item prop="llm_name" label="模型编号" required>
                    <el-input v-model="newLLMForm.llm_name" placeholder="API中的model参数" clearable />
                  </el-form-item>
                  <el-form-item prop="llm_label" label="模型名称" required>
                    <el-input v-model="newLLMForm.llm_label" placeholder="模型实例显示名称" clearable />
                  </el-form-item>
                  <el-form-item prop="llm_type" label="模型类型" required>
                    <el-radio-group v-model="newLLMForm.llm_type">
                      <el-radio
                        v-for="type in allModelType"
                        :key="type.value"
                        :label="type.value"
                        :disabled="type?.disable"
                      >
                        {{ type.label }}
                      </el-radio>
                    </el-radio-group>
                  </el-form-item>
                  <el-form-item prop="llm_desc" label="模型描述">
                    <el-input
                      v-model="newLLMForm.llm_desc"
                      placeholder="请输入模型描述"
                      clearable
                      type="textarea"
                      :rows="6"
                    />
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
                      :on-success="handleAvatarUploadSuccess"
                      style="min-width: 160px"
                    >
                      <div v-if="newLLMForm.llm_icon">
                        <el-image :src="newLLMForm.llm_icon" style="width: 40px; height: 40px" />
                      </div>
                      <div v-else>
                        <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
                        <i class="el-icon-upload" />
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                      </div>
                    </el-upload>
                  </el-form-item>
                  <el-form-item label="模型上下文窗口(Tokens)" prop="max_tokens">
                    <el-input-number v-model="newLLMForm.max_tokens" />
                  </el-form-item>
                  <el-form-item label="模型标签" prop="llm_tags">
                    <el-select
                      v-model="newLLMForm.llm_tags"
                      placeholder="请选择或创建模型标签"
                      multiple
                      clearable
                      allow-create
                      filterable
                      :multiple-limit="4"
                    >
                      <template #label="{ value }">
                        {{ translateTag(value) }}
                      </template>
                      <el-option
                        v-for="tag in [
                          '文本生成',
                          '图片生成',
                          '推理模型',
                          '图片理解',
                          '视频理解',
                          '语音识别',
                          '语音合成',
                          '视频生成',
                          '全模态',
                          '向量模型',
                          '排序模型',
                          '音频理解',
                          '图像处理'
                        ]"
                        :key="tag"
                        :label="tag"
                        :value="tag"
                      />
                    </el-select>
                  </el-form-item>
                  <el-form-item label="模型供应商" prop="llm_company">
                    <el-select
                      v-model="newLLMForm.llm_company"
                      placeholder="请选择或者输入模型供应商名称"
                      clearable
                      filterable
                      allow-create
                      default-first-option
                    >
                      <el-option v-for="company in allSupportCompany" :key="company" :value="company" />
                    </el-select>
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
                </el-tab-pane>
                <el-tab-pane name="run" label="运行参数">
                  <div v-if="newLLMForm.llm_type && ['文本生成', '推理模型', '全模态'].includes(newLLMForm.llm_type)">
                    <el-form-item prop="stream" label="流式输出" style="height: 80px">
                      <el-switch v-model="newLLMForm.stream" />
                    </el-form-item>
                    <el-form-item prop="use_default" label="使用默认配置" style="height: 80px">
                      <el-switch v-model="newLLMForm.use_default" />
                    </el-form-item>
                    <el-form-item prop="temperature" label="温度" style="height: 80px">
                      <el-slider
                        v-model="newLLMForm.temperature"
                        :min="0"
                        :max="2"
                        :step="0.1"
                        :marks="temperatureMarks"
                        style="margin: 0 24px"
                        show-input
                        :show-input-controls="false"
                        :disabled="newLLMForm.use_default"
                      />
                    </el-form-item>
                    <el-form-item prop="frequency_penalty" label="频率惩罚" style="height: 80px">
                      <el-slider
                        v-model="newLLMForm.frequency_penalty"
                        :min="-2"
                        :max="2"
                        :step="0.1"
                        :marks="frequencyPenaltyMarks"
                        style="margin: 0 24px"
                        show-input
                        :show-input-controls="false"
                        :disabled="newLLMForm.use_default"
                      />
                    </el-form-item>
                    <el-form-item prop="top_p" label="核采样" style="height: 80px">
                      <el-slider
                        v-model="newLLMForm.top_p"
                        :min="0"
                        :max="1"
                        :step="0.1"
                        :marks="topPMarks"
                        style="margin: 0 24px"
                        show-input
                        :show-input-controls="false"
                        :disabled="newLLMForm.use_default"
                      />
                    </el-form-item>
                    <el-form-item prop="presence_penalty" label="出现惩罚" style="height: 80px">
                      <el-slider
                        v-model="newLLMForm.presence_penalty"
                        :min="-2"
                        :max="2"
                        :step="0.1"
                        :marks="frequencyPenaltyMarks"
                        style="margin: 0 24px"
                        show-input
                        :show-input-controls="false"
                        :disabled="newLLMForm.use_default"
                      />
                    </el-form-item>
                    <el-form-item prop="extra_headers" label="额外Header参数" style="height: 80px">
                      <el-row style="width: 100%">
                        <el-col :span="4">
                          <el-text type="info" size="small"> 变量名称 </el-text>
                        </el-col>
                        <el-col :span="4">
                          <el-text type="info" size="small"> 变量描述 </el-text>
                        </el-col>
                        <el-col :span="6">
                          <el-text type="info" size="small"> 变量类型 </el-text>
                        </el-col>
                        <el-col :span="6">
                          <el-text type="info" size="small"> 变量值 </el-text>
                        </el-col>
                      </el-row>
                      <JsonSchemaForm
                        :json-schema="newLLMForm.extra_headers"
                        :value-define="true"
                        @update:schema="
                          newSchema => {
                            newLLMForm.extra_headers = newSchema;
                          }
                        "
                      />
                    </el-form-item>
                    <el-form-item prop="extra_body" label="额外Body参数" style="height: 80px">
                      <el-row style="width: 100%">
                        <el-col :span="4">
                          <el-text type="info" size="small"> 变量名称 </el-text>
                        </el-col>
                        <el-col :span="4">
                          <el-text type="info" size="small"> 变量描述 </el-text>
                        </el-col>
                        <el-col :span="6">
                          <el-text type="info" size="small"> 变量类型 </el-text>
                        </el-col>
                        <el-col :span="6">
                          <el-text type="info" size="small"> 变量值 </el-text>
                        </el-col>
                      </el-row>
                      <JsonSchemaForm
                        :json-schema="newLLMForm.extra_body"
                        :value-define="true"
                        @update:schema="
                          newSchema => {
                            newLLMForm.extra_body = newSchema;
                          }
                        "
                      />
                    </el-form-item>
                  </div>
                  <div v-else>
                    <el-empty description="当前模型类型暂无运行参数配置" />
                  </div>
                </el-tab-pane>
              </el-tabs>
            </el-form>
          </div>
          <div v-show="currentStep == 2" class="step-three-area">
            <el-steps
              :active="modelTestStep"
              finish-status="success"
              direction="vertical"
              :process-status="modelTestStatus"
            >
              <el-step
                v-loading="modelTestStep == 0 && modelTesting"
                title="步骤一：连通性测试"
                content="尝试连接模型服务，确保能够成功访问API"
                element-loading-text="测试中..."
                :icon="Connection"
              >
                <template #description>
                  <el-descriptions
                    v-if="modelTestResult?.[0]"
                    title="检查结果"
                    border
                    direction="vertical"
                    size="large"
                    label-width="300px"
                  >
                    <el-descriptions-item label="模型地址">
                      <el-tag>{{ newLLMForm.llm_base_url }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="模型编号">
                      <el-tag>{{ newLLMForm.llm_name }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="健康状态">
                      <el-tag :type="modelTestResult[0]?.status == '成功' ? 'success' : 'danger'">
                        {{ modelTestResult[0]?.status }}
                      </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="域名">
                      <el-tag>{{ modelTestResult[0]?.domain }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="解析ip">
                      <el-tag>{{ modelTestResult[0]?.ip }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="端口">
                      <el-tag>{{ modelTestResult[0]?.port }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="耗时">
                      <el-tag>{{ modelTestResult[0]?.duration }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="结论">
                      <el-text :type="modelTestResult[0]?.status == '成功' ? 'success' : 'danger'">
                        {{ modelTestResult[0]?.msg }}
                      </el-text>
                    </el-descriptions-item>
                  </el-descriptions>
                </template>
              </el-step>
              <el-step
                v-loading="modelTestStep == 1 && modelTesting"
                title="步骤二：功能测试"
                content="发送测试请求，验证模型是否能够正确响应"
                element-loading-text="测试中..."
                :icon="ChatLineSquare"
              >
                <template #description>
                  <el-descriptions
                    v-if="modelTestResult?.[1]"
                    title="检查结果"
                    border
                    direction="vertical"
                    size="large"
                    label-width="300px"
                  >
                    <el-descriptions-item label="模型供应商">
                      <el-tag>{{ newLLMForm.llm_company }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="测试用例">
                      <el-text>{{ modelTestResult[1]?.test_case }}</el-text>
                      <el-image v-if="modelTestResult[1]?.test_image" :src="modelTestResult[1]?.test_image" />
                    </el-descriptions-item>
                    <el-descriptions-item label="模型类型">
                      <el-tag :type="modelTestResult[1]?.status == '成功' ? 'success' : 'danger'">
                        {{ newLLMForm.llm_type }}
                      </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="耗时">
                      <el-tag>{{ modelTestResult[1]?.duration }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="响应">
                      <el-text>{{ modelTestResult[1]?.answer }}</el-text>
                      <div v-if="modelTestResult[1]?.answer_images">
                        <el-image v-for="img in modelTestResult[1]?.answer_images" :key="img" :src="img" />
                      </div>
                    </el-descriptions-item>
                    <el-descriptions-item label="结论">
                      <el-text :type="modelTestResult[1]?.status == '成功' ? 'success' : 'danger'">
                        {{ modelTestResult[1]?.msg }}
                      </el-text>
                    </el-descriptions-item>
                  </el-descriptions>
                </template>
              </el-step>
              <el-step title="配置完成" :icon="SuccessFilled">
                <template #description />
              </el-step>
            </el-steps>
          </div>
          <div v-show="currentStep == 3" class="step-four-area">
            <AuthorSelector
              ref="authorSelectorRef"
              :share-model="newLLMForm"
              style="height: 100%"
              @update-access-list="
                newList => {
                  newLLMForm.llm_authors = newList;
                }
              "
            />
          </div>
        </div>
      </el-scrollbar>
    </el-main>
    <el-footer style="padding: 0">
      <div class="footer-area">
        <div v-if="currentStep == 3">
          <el-button type="success" size="large" @click="commitNewLLMInstance"> 提交 </el-button>
        </div>
        <div v-else>
          <el-button type="primary" size="large" :disabled="nextStepDisabled" @click="handleForwardStep">
            下一步
          </el-button>
        </div>
        <div v-if="currentStep == 2">
          <el-button type="primary" size="large" :disabled="modelTesting" @click="checkModelConfig">
            健康检查
          </el-button>
        </div>
        <div>
          <el-button v-show="currentStep" type="info" size="large" @click="handleBackStep"> 上一步 </el-button>
        </div>
      </div>
    </el-footer>
  </el-container>
</template>

<style scoped>
.step-area {
  padding: 32px;
  display: flex;
  flex-direction: row;
  gap: 24px;
  align-items: center;
  justify-content: flex-start;
  border-bottom: 1px solid #e0e0e0;
}
.step-left {
  min-width: 120px;
}
.step-right {
  width: 100%;
}
.footer-area {
  width: calc(100% - 32px);
  height: calc(100% - 32px);
  display: flex;
  flex-direction: row-reverse;
  gap: 12px;
  border-top: 1px solid #e0e0e0;
  padding: 16px;
}
.main-area {
  height: calc(100vh - 290px);
}
.step-one-area {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
}
.pane-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 12px;
  height: calc(100% - 40px);
}
.supply-area {
  padding: 8px;
  width: 300px;
  border-right: 1px solid #e0e0e0;
  height: calc(100% - 16px);
}
.supplier-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: calc(100vh - 460px);
  min-height: 300px;
  padding-right: 16px;
}
.supplier-box {
  display: flex;
  flex-direction: row;
  gap: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  min-width: 200px;
  &:hover {
    cursor: pointer;
    background-color: #f5f5f5;
    border: 1px solid #3b82f6;
  }
}
.supplier-box-active {
  background-color: #f0f8ff;
  border: 1px solid #3b82f6;
}
.supplier-icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
}
.supplier-icon {
  width: 48px;
  height: 48px;
  background-color: white;
}
.supplier-name {
  font-size: 16px;
  font-weight: 600;
  color: #101828;
}
.models-area {
  flex: 1;
}
.empty-models-area {
  width: calc(100% - 64px);
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.step-two-area {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: center;
}
.std-middle-box {
  display: flex;
  align-items: center;
  justify-content: center;
}
.new-llm {
  margin: 20px;
  max-width: 900px;
  width: 100%;
}
:deep(.el-input__validateIcon) {
  color: green;
}
.step-three-area {
  display: flex;
  flex-direction: row;
  padding: 24px;
  gap: 24px;
  align-items: center;
  justify-content: center;
  height: calc(100% - 48px);
  width: calc(100% - 64px);
}
.test-result-area {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.test-sub-result {
  height: 100%;
  width: 100%;
  max-width: 500px;
  border-left: 1px solid #e0e0e0;
}
.url-meta {
  display: flex;
  flex-direction: row;
  gap: 16px;
}
.step-four-area {
  display: flex;
  flex-direction: row;
  padding: 24px;
  gap: 24px;
  align-items: flex-start;
  justify-content: center;
  height: calc(100% - 48px);
  width: calc(100% - 64px);
}
</style>
