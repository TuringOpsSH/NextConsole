<script setup lang="ts">
import {
  Delete,
  Connection,
  ChatLineSquare,
  SuccessFilled,
  CaretTop,
  CaretBottom,
  Warning
} from '@element-plus/icons-vue';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';
import { cloneDeep } from 'lodash-es';
import { watch, ref, reactive, type CSSProperties, onMounted, nextTick } from 'vue';
import VueJsonPretty from 'vue-json-pretty';
import {
  api,
  llmHealthCheck,
  llmInstanceGet,
  llmInstanceRemoveAccess,
  llmInstanceUpdate,
  llmSupplierSearch
} from '@/api/config-center';
import { getModelRunIndex } from '@/api/dashboard';
import JsonSchemaForm from '@/components/app-center/app-manage/JsonSchemaForm.vue';
import AuthorSelector from '@/components/app-center/model-manage/AuthorSelector.vue';
import router from '@/router';
import { useUserInfoStore } from '@/stores/user-info-store';
import { ILLMInstance } from '@/types/config-center';
import { generateNcSchema } from '@/utils/alg';

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
const props = defineProps({
  llmCode: {
    type: String,
    required: true
  },
  tab: {
    type: String,
    required: false,
    default: 'base'
  }
});
const userInfoStore = useUserInfoStore();
const currentTab = ref('base');
const currentLLM = reactive<Partial<ILLMInstance>>({
  create_time: '',
  llm_code: '',
  llm_desc: '',
  llm_icon: '',
  llm_name: '',
  llm_status: '',
  llm_type: '',
  support_file: false,
  support_vis: false,
  update_time: '',
  access: [],
  llm_authors: [],
  use_default: true,
  id: 0,
  llm_label: '',
  llm_company: '',
  llm_api_secret_key: '',
  llm_base_url: '',
  is_std_openai: false,
  max_tokens: 0,
  temperature: 1,
  top_p: 1,
  frequency_penalty: 0,
  presence_penalty: 0,
  stream: false,
  extra_headers: {},
  extra_body: {},
  llm_tags: [],
  user_id: 0,
  schema_type: 'data',
  think_attr: {
    begin: '',
    end: ''
  }
});
const editLLM = reactive<ILLMInstance>({
  create_time: '',
  llm_code: '',
  llm_desc: '',
  llm_icon: '',
  llm_name: '',
  llm_status: '',
  llm_type: '',
  support_file: false,
  support_vis: false,
  update_time: '',
  access: [],
  llm_authors: [],
  use_default: true,
  id: 0,
  llm_label: '',
  llm_company: '',
  llm_api_secret_key: '',
  llm_base_url: '',
  is_std_openai: false,
  max_tokens: 0,
  temperature: 1,
  top_p: 1,
  frequency_penalty: 0,
  presence_penalty: 0,
  stream: false,
  extra_headers: {},
  extra_body: {},
  llm_tags: [],
  user_id: 0,
  think_attr: {
    begin: '',
    end: ''
  }
});
const showUpdateLLMForm = ref(false);
const currentLLMFormRef = ref(null);
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
const modelTestStep = ref(0);
const modelTestStatus = ref('process');
const modelTesting = ref(false);
const modelTestResult = ref([]);
const rules = {
  llm_label: [
    { required: true, message: '请输入模型名称', trigger: 'blur' },
    { min: 2, max: 50, message: '模型编号长度在2到30个字符之间', trigger: 'blur' }
  ],
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
const allSupportCompany = ref([]);
const modelParams = reactive({
  timeRange: [
    new Date(new Date().setDate(new Date().getDate() - 7) + 8 * 60 * 60 * 1000), // 加上8小时
    new Date(new Date().getTime() + 8 * 60 * 60 * 1000) // 加上8小时
  ],
  duration: 'day'
});
const durationOptions = [
  { label: '分钟', value: 'minute' },
  { label: '小时', value: 'hour' },
  { label: '天', value: 'day' },
  { label: '周', value: 'week' },
  { label: '月', value: 'month' }
];
const shortcuts = [
  {
    text: '上周',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setDate(start.getDate() - 7);
      return [start, end];
    }
  },
  {
    text: '上月',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setMonth(start.getMonth() - 1);
      return [start, end];
    }
  },
  {
    text: '上季度',
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setMonth(start.getMonth() - 3);
      return [start, end];
    }
  }
];
const modelBaseCnt = ref([
  {
    title: '总Token消耗',
    desc: '通过此模型实例产生的总token消耗数',
    cnt: 0,
    compare: 'up',
    percent: 0,
    icon: '/images/app-center/blue_line.svg',
    last_begin_time: ''
  }
]);
const echartsData = {
  token_time_cnt: {
    ref: null,
    options: {
      title: { text: 'Token消耗统计' },
      color: ['#80FFA5', '#FF0087'],
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        data: ['官方助手', '自定义应用']
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      xAxis: [
        {
          type: 'category',
          // 自定义时间格式化
          data: [],
          axisLabel: {
            rotate: 45 // 如果标签太长可以旋转
          }
        }
      ],
      yAxis: [
        {
          type: 'value'
        }
      ],
      series: [
        {
          name: '官方助手',
          type: 'line',
          stack: 'Total',
          smooth: true,
          lineStyle: {
            width: 0
          },
          showSymbol: false,
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: 'rgb(128, 255, 165)'
              },
              {
                offset: 1,
                color: 'rgb(1, 191, 236)'
              }
            ])
          },
          emphasis: {
            focus: 'series'
          },
          data: [140, 232, 101, 264, 90, 340, 250]
        },
        {
          name: '自定义应用',
          type: 'line',
          stack: 'Total',
          smooth: true,
          lineStyle: {
            width: 0
          },
          showSymbol: false,
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: 'rgb(255, 0, 135)'
              },
              {
                offset: 1,
                color: 'rgb(135, 0, 157)'
              }
            ])
          },
          emphasis: {
            focus: 'series'
          },
          data: [120, 282, 111, 234, 220, 340, 310]
        }
      ]
    }
  },
  qa_time_cnt: {
    ref: null,
    options: {
      title: { text: '问答次数分析' },
      legend: {
        data: ['成功', '中断']
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      xAxis: [
        {
          data: []
        }
      ],
      yAxis: [
        {
          type: 'value'
        }
      ],
      series: [
        {
          name: '成功',
          data: [10, 22, 28, 43, 49],
          type: 'bar',
          stack: 'x',
          itemStyle: {
            color: '#91cc75'
          }
        },
        {
          name: '中断',
          data: [5, 4, 3, 5, 10],
          type: 'bar',
          stack: 'x',
          itemStyle: {
            color: '#ee6666'
          }
        }
      ]
    }
  },
  user_time_cnt: {
    ref: null,
    options: {
      title: { text: '活跃用户趋势' },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      xAxis: [
        {
          data: []
        }
      ],
      yAxis: [
        {
          type: 'value'
        }
      ],
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['活跃用户']
      },
      series: [
        {
          name: '活跃用户',
          type: 'line',
          data: []
        }
      ]
    }
  },
  session_source_cnt: {
    ref: null,
    options: {
      title: { text: '关联会话分布' },
      tooltip: {
        trigger: 'item'
      },
      legend: {},
      series: [
        {
          name: '关联会话分布',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 40,
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: []
        }
      ]
    }
  },
  app_top_cnt: {
    ref: null,
    options: {
      title: {
        text: '应用使用排行'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {},
      xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
      },
      yAxis: {
        type: 'category',
        inverse: true,
        data: []
      },
      series: [
        {
          name: 'Token消耗',
          type: 'bar',
          data: [18203, 23489, 29034, 104970, 131744, 630230]
        }
      ]
    }
  }
};
const echartsSize = [577, 400];
const showUpdateRunConfig = ref(false);
const currentLLMConfigRef = ref(null);
const configRules = [];
const showUpdateAccess = ref(false);
const authorSelectorRef = ref(null);
async function refreshCurrentModel() {
  const res = await llmInstanceGet({
    llm_code: currentLLM.llm_code
  });
  if (!res.error_status) {
    Object.assign(currentLLM, res.result);
  }
  modelTestStep.value = 0;
  modelTestStatus.value = 'process';
  modelTesting.value = false;
  modelTestResult.value = [];
}
async function handleTabChange() {
  if (currentTab.value === 'base') {
    await refreshCurrentModel();
  } else if (currentTab.value === 'health') {
    modelTestStep.value = 0;
    modelTestStatus.value = 'process';
    modelTesting.value = false;
    modelTestResult.value = [];
  } else if (currentTab.value === 'dashboard') {
    refreshModelIndex();
  }
  router.replace({
    query: {
      tab: currentTab.value
    }
  });
}
async function beginUpdateBaseInfo() {
  showUpdateLLMForm.value = true;
  const copy = cloneDeep(currentLLM);
  Object.assign(editLLM, copy);
  editLLM.extra_headers = generateNcSchema(editLLM.extra_headers || {});
  editLLM.extra_body = generateNcSchema(editLLM.extra_body || {});
  await getAllSupportCompany();
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
    editLLM.llm_icon = res.result.llm_icon;
  }
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
async function commitUpdateLLMInstance() {
  const valid = await currentLLMFormRef.value?.validate();
  if (!valid) {
    return;
  }
  const updateRes = await llmInstanceUpdate(editLLM);
  if (!updateRes.error_status) {
    ElMessage.success('更新模型实例成功');
    showUpdateLLMForm.value = false;
    refreshCurrentModel();
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
function beginUpdateRunConfig() {
  showUpdateRunConfig.value = true;
  const copy = cloneDeep(currentLLM);
  Object.assign(editLLM, copy);
  editLLM.extra_headers = generateNcSchema(editLLM.extra_headers || {});
  editLLM.extra_body = generateNcSchema(editLLM.extra_body || {});
}
function getAccessIcon(access) {
  if (access.structure_type == 'company') {
    return '/images/app-center/company.svg';
  } else if (access.structure_type == 'department') {
    return '/images/app-center/department.svg';
  } else if (access.structure_type == 'colleague') {
    return '/images/app-center/colleague.svg';
  } else if (access.structure_type == 'friend') {
    return '/images/app-center/friend.svg';
  } else if (access.structure_type == 'user') {
    return '/images/app-center/friend.svg';
  } else {
    return '/images/app-center/unknown.svg';
  }
}
async function beginUpdateAccess() {
  const copy = cloneDeep(currentLLM);
  Object.assign(editLLM, copy);
  if (!editLLM.llm_authors) {
    editLLM.llm_authors = [];
  }
  showUpdateAccess.value = true;
  showUpdateAccess.value = false;
  showUpdateAccess.value = true;
}
function getAccessTranslate(name: string) {
  switch (name) {
    case 'own':
      return '所有者';
    case 'manage':
      return '管理';
    case 'use':
      return '使用';
    case 'edit':
      return '编辑';
    case 'read':
      return '查看';
    default:
      return name;
  }
}
function getAccessName(access) {
  if (access.structure_type == 'company') {
    return access.company_name;
  } else if (access.structure_type == 'department') {
    return access.department_name;
  } else if (access.structure_type == 'colleague') {
    return access.user_nick_name;
  } else if (access.structure_type == 'friend') {
    return access.user_nick_name;
  } else if (access.structure_type == 'user') {
    return access.user_name || access.user_nick_name;
  } else {
    return '';
  }
}
function getAccessID(access) {
  if (access.structure_type == 'company') {
    return access.company_id;
  } else if (access.structure_type == 'department') {
    return access.department_id;
  } else if (access.structure_type == 'colleague') {
    return access.user_id;
  } else if (access.structure_type == 'friend') {
    return access.user_id;
  } else {
    return '';
  }
}
async function checkModelConfig() {
  modelTestStep.value = 0;
  modelTesting.value = true;
  modelTestStatus.value = 'process';
  for (let step = modelTestStep.value; step < 3; step++) {
    modelTestStep.value = step;
    const res = await llmHealthCheck({
      model: currentLLM,
      step: step
    });
    modelTestResult.value[step] = res.result;
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
async function refreshModelIndex() {
  try {
    initModelBaseCnt();
    initModelTimeCnt();
  } catch (e) {
    console.error(e);
  }
}
async function initModelBaseCnt() {
  // 时间格式为 2023-10-01 00:00:00
  const res = await getModelRunIndex({
    llm_code: currentLLM.llm_code,
    index_name: 'base_cnt',
    begin_time: modelParams.timeRange[0].toISOString().slice(0, 19).replace('T', ' '),
    end_time: modelParams.timeRange[1].toISOString().slice(0, 19).replace('T', ' ')
  });
  if (!res.error_status) {
    modelBaseCnt.value[0] = res.result?.data?.total_token;
    modelBaseCnt.value[1] = res.result?.data?.total_requests;
    modelBaseCnt.value[2] = res.result?.data?.total_sessions;
    modelBaseCnt.value[3] = res.result?.data?.total_apps;
    modelBaseCnt.value[4] = res.result?.data?.total_users;
  }
}
async function initModelTimeCnt() {
  // 时序相关图表
  initTokenTimeCnt();
  initQATimeCnt();
  initUserTimeCnt();
  sessionSourceCnt();
  appTopCnt();
}
async function initTokenTimeCnt() {
  const res = await getModelRunIndex({
    llm_code: currentLLM.llm_code,
    index_name: 'token_time_cnt',
    begin_time: modelParams.timeRange[0].toISOString().slice(0, 19).replace('T', ' '),
    end_time: modelParams.timeRange[1].toISOString().slice(0, 19).replace('T', ' '),
    duration: modelParams.duration
  });
  if (!res.error_status) {
    echartsData.token_time_cnt.options.xAxis[0].data = res.result.xAxis;
    echartsData.token_time_cnt.options.series[0].data = res.result.series[0].data;
    echartsData.token_time_cnt.options.series[1].data = res.result.series[1].data;
  }
  if (!echartsData.token_time_cnt.ref) {
    echartsData.token_time_cnt.ref = await echarts.init(document.getElementById('token_time_cnt'), null, {
      width: echartsSize[0],
      height: echartsSize[1]
    });
  }
  echartsData.token_time_cnt.ref?.setOption(echartsData.token_time_cnt.options);
}
async function initQATimeCnt() {
  const res = await getModelRunIndex({
    llm_code: currentLLM.llm_code,
    index_name: 'qa_time_cnt',
    begin_time: modelParams.timeRange[0].toISOString().slice(0, 19).replace('T', ' '),
    end_time: modelParams.timeRange[1].toISOString().slice(0, 19).replace('T', ' '),
    duration: modelParams.duration
  });
  if (!res.error_status) {
    echartsData.qa_time_cnt.options.xAxis[0].data = res.result.xAxis;
    echartsData.qa_time_cnt.options.series[0].data = res.result.series[0].data;
    echartsData.qa_time_cnt.options.series[1].data = res.result.series[1].data;
  }
  if (!echartsData.qa_time_cnt.ref) {
    echartsData.qa_time_cnt.ref = await echarts.init(document.getElementById('qa_time_cnt'), null, {
      width: echartsSize[0],
      height: echartsSize[1]
    });
  }
  echartsData.qa_time_cnt.ref?.setOption(echartsData.qa_time_cnt.options);
}
async function initUserTimeCnt() {
  const res = await getModelRunIndex({
    llm_code: currentLLM.llm_code,
    index_name: 'user_time_cnt',
    begin_time: modelParams.timeRange[0].toISOString().slice(0, 19).replace('T', ' '),
    end_time: modelParams.timeRange[1].toISOString().slice(0, 19).replace('T', ' '),
    duration: modelParams.duration
  });
  if (!res.error_status) {
    echartsData.user_time_cnt.options.xAxis[0].data = res.result.xAxis;
    echartsData.user_time_cnt.options.series[0].data = res.result.series[0].data;
  }
  if (!echartsData.user_time_cnt.ref) {
    echartsData.user_time_cnt.ref = await echarts.init(document.getElementById('user_time_cnt'), null, {
      width: echartsSize[0],
      height: echartsSize[1]
    });
  }
  echartsData.user_time_cnt.ref?.setOption(echartsData.user_time_cnt.options);
}
async function sessionSourceCnt() {
  const res = await getModelRunIndex({
    llm_code: currentLLM.llm_code,
    index_name: 'session_source_cnt',
    begin_time: modelParams.timeRange[0].toISOString().slice(0, 19).replace('T', ' '),
    end_time: modelParams.timeRange[1].toISOString().slice(0, 19).replace('T', ' ')
  });
  if (!res.error_status) {
    echartsData.session_source_cnt.options.series[0].data = res.result.series[0].data;
  }
  if (!echartsData.session_source_cnt.ref) {
    echartsData.session_source_cnt.ref = await echarts.init(document.getElementById('session_source_cnt'), null, {
      width: echartsSize[0],
      height: echartsSize[1]
    });
  }
  echartsData.session_source_cnt.ref?.setOption(echartsData.session_source_cnt.options);
}
async function appTopCnt() {
  const res = await getModelRunIndex({
    llm_code: currentLLM.llm_code,
    index_name: 'app_top_cnt',
    begin_time: modelParams.timeRange[0].toISOString().slice(0, 19).replace('T', ' '),
    end_time: modelParams.timeRange[1].toISOString().slice(0, 19).replace('T', ' ')
  });
  if (!res.error_status) {
    echartsData.app_top_cnt.options.yAxis.data = res.result.yAxis;
    echartsData.app_top_cnt.options.series[0].data = res.result.series[0].data;
  }
  if (!echartsData.app_top_cnt.ref) {
    echartsData.app_top_cnt.ref = await echarts.init(document.getElementById('app_top_cnt'), null, {
      width: echartsSize[0],
      height: echartsSize[1]
    });
  }
  echartsData.app_top_cnt.ref?.setOption(echartsData.app_top_cnt.options);
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
async function commitUpdateLLMConfig() {
  const valid = await currentLLMConfigRef.value?.validate();
  if (!valid) {
    return;
  }
  const updateRes = await llmInstanceUpdate(editLLM);
  if (!updateRes.error_status) {
    ElMessage.success('更新模型实例成功');
    showUpdateRunConfig.value = false;
    refreshCurrentModel();
  }
}
async function commitUpdateLLMAccess() {
  const updateRes = await llmInstanceUpdate(editLLM);
  if (!updateRes.error_status) {
    ElMessage.success('更新模型实例访问权限成功');
    showUpdateAccess.value = false;
    refreshCurrentModel();
  }
}
async function removeAccess(access) {
  const res = await llmInstanceRemoveAccess({
    llm_code: currentLLM.llm_code,
    access_id: access.access_id
  });
  if (!res.error_status) {
    ElMessage.success('移除访问权限成功');
    refreshCurrentModel();
  }
}
watch(
  () => props.llmCode,
  newVal => {
    currentLLM.llm_code = newVal;
    refreshCurrentModel();
  },
  { immediate: true }
);
watch(
  () => props.tab,
  async newVal => {
    if (newVal == currentTab.value) {
      return;
    }
    if (newVal && ['base', 'health', 'dashboard'].includes(newVal)) {
      currentTab.value = newVal;
    } else {
      currentTab.value = 'base';
    }
    await handleTabChange();
  },
  { immediate: false }
);
onMounted(async () => {
  if (props.tab && ['base', 'health', 'dashboard'].includes(props.tab)) {
    currentTab.value = props.tab;
  } else {
    currentTab.value = 'base';
  }
  await nextTick();
});
</script>

<template>
  <el-container>
    <el-main>
      <el-scrollbar>
        <div class="main-area">
          <el-tabs v-model="currentTab" tab-position="top" type="border-card" @tab-change="handleTabChange">
            <el-tab-pane name="base" label="基础信息">
              <el-scrollbar>
                <div class="tab-pane-area">
                  <el-descriptions title="实例详情" border label-width="150" size="large">
                    <template #extra>
                      <el-button v-if="currentLLM.access.includes('edit')" type="primary" @click="beginUpdateBaseInfo">
                        编辑
                      </el-button>
                    </template>
                    <el-descriptions-item label="模型图标" :rowspan="3">
                      <el-image :src="currentLLM.llm_icon" size="large" class="std-icon" />
                    </el-descriptions-item>
                    <el-descriptions-item label="模型名称">{{ currentLLM.llm_label }}</el-descriptions-item>
                    <el-descriptions-item label="模型编号">{{ currentLLM.llm_name }}</el-descriptions-item>
                    <el-descriptions-item label="模型类型">
                      <el-tag>
                        {{ currentLLM.llm_type }}
                      </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="供应商">{{ currentLLM.llm_company }}</el-descriptions-item>
                    <el-descriptions-item label="API地址">{{ currentLLM.llm_base_url }}</el-descriptions-item>
                    <el-descriptions-item label="上下文长度">
                      {{ translateMaxTokens(currentLLM.max_tokens) }}
                    </el-descriptions-item>
                    <el-descriptions-item label="所有者">
                      <div style="display: flex; flex-direction: row; gap: 12px; align-items: center">
                        <div>
                          <el-tooltip :content="currentLLM.author?.user_nick_name" placement="left">
                            <el-avatar
                              v-if="currentLLM.author?.user_avatar"
                              :src="currentLLM.author.user_avatar"
                              class="std-icon"
                            />
                            <el-avatar v-else style="background: #d1e9ff">
                              <el-text style="font-weight: 600; color: #1570ef">
                                {{ currentLLM.author?.user_nick_name_py }}
                              </el-text>
                            </el-avatar>
                          </el-tooltip>
                        </div>
                        <div>
                          <el-text>
                            {{ currentLLM.author?.user_nick_name }}
                          </el-text>
                        </div>
                      </div>
                    </el-descriptions-item>
                    <el-descriptions-item label="模型标签">
                      <div class="std-middle-box" style="justify-content: flex-start">
                        <el-tag v-for="tag in currentLLM.llm_tags" :key="tag"> {{ tag }} </el-tag>
                      </div>
                    </el-descriptions-item>
                    <el-descriptions-item label="模型状态">
                      <el-tag> {{ currentLLM.llm_status }} </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="模型密钥">
                      <el-input v-model="currentLLM.llm_api_secret_key" type="password" show-password readonly />
                    </el-descriptions-item>
                    <el-descriptions-item label="支持OpenAI-SDK">
                      <el-tag> {{ currentLLM.is_std_openai ? '是' : '否' }} </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="支持文件">
                      <el-tag> {{ currentLLM.support_file ? '是' : '否' }} </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="支持视觉">
                      <el-tag>
                        {{ currentLLM.support_vis ? '是' : '否' }}
                      </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="创建时间">{{ currentLLM.create_time }}</el-descriptions-item>
                    <el-descriptions-item label="更新时间">{{ currentLLM.update_time }}</el-descriptions-item>
                    <el-descriptions-item label="模型描述">{{ currentLLM.llm_desc }}</el-descriptions-item>
                  </el-descriptions>
                  <el-descriptions title="运行配置" border label-width="150" size="large">
                    <template #extra>
                      <el-button
                        v-if="
                          currentLLM.access.includes('edit') &&
                          ['文本生成', '推理模型', '全模态', '图片理解'].includes(currentLLM.llm_type)
                        "
                        type="primary"
                        @click="beginUpdateRunConfig"
                      >
                        编辑
                      </el-button>
                    </template>
                    <div v-if="['文本生成', '推理模型', '全模态'].includes(currentLLM.llm_type)">
                      <el-descriptions-item label="流式输出">
                        <el-tag> {{ currentLLM.stream ? '是' : '否' }} </el-tag>
                      </el-descriptions-item>
                      <el-descriptions-item label="使用默认配置">
                        <el-tag> {{ currentLLM.use_default ? '是' : '否' }} </el-tag>
                      </el-descriptions-item>
                      <el-descriptions-item label="温度">
                        <el-tag> {{ currentLLM.temperature }} </el-tag>
                      </el-descriptions-item>
                      <el-descriptions-item label="频率惩罚">
                        <el-tag> {{ currentLLM.frequency_penalty }} </el-tag>
                      </el-descriptions-item>
                      <el-descriptions-item label="出现惩罚">
                        <el-tag> {{ currentLLM.presence_penalty }} </el-tag>
                      </el-descriptions-item>
                      <el-descriptions-item label="核采样">
                        <el-tag> {{ currentLLM.top_p }} </el-tag>
                      </el-descriptions-item>
                      <el-descriptions-item label="额外Header参数">
                        <VueJsonPretty
                          :data="currentLLM.extra_headers"
                          :show-length="true"
                          :show-line-number="true"
                          :show-icon="true"
                          :show-select-controller="true"
                        />
                      </el-descriptions-item>
                      <el-descriptions-item label="额外Body参数">
                        <VueJsonPretty
                          :data="currentLLM.extra_body"
                          :show-length="true"
                          :show-line-number="true"
                          :show-icon="true"
                          :show-select-controller="true"
                        />
                      </el-descriptions-item>
                      <el-descriptions-item v-if="currentLLM?.think_attr?.begin" label="推理标签">
                        <div class="std-middle-box" style="gap: 4px; justify-content: flex-start">
                          <el-tag v-for="tag in currentLLM.think_attr" :key="tag"> {{ tag }} </el-tag>
                        </div>
                      </el-descriptions-item>
                    </div>
                    <div v-else>
                      <el-descriptions-item>
                        <el-empty description="当前模型暂无运行参数配置" />
                      </el-descriptions-item>
                    </div>
                  </el-descriptions>
                  <el-descriptions v-if="currentLLM.access.includes('manage')" title="授权信息">
                    <template #extra>
                      <el-button v-if="currentLLM.access.includes('manage')" type="primary" @click="beginUpdateAccess">
                        编辑
                      </el-button>
                    </template>
                  </el-descriptions>
                  <div class="access-area">
                    <el-card v-for="(access, idx) in currentLLM.llm_authors" :key="idx" class="access-card">
                      <template #header>
                        <div class="access-head">
                          <div>
                            <el-image :src="getAccessIcon(access)" class="access-icon" />
                          </div>
                          <div>
                            <el-tag> {{ getAccessTranslate(access.access) }} </el-tag>
                          </div>
                        </div>
                      </template>
                      <div class="access-info">
                        <h4>{{ getAccessName(access) }}</h4>
                        <el-text> ID:{{ getAccessID(access) }}</el-text>
                      </div>
                      <template #footer>
                        <div class="access-foot">
                          <el-popconfirm
                            title="是否取消授权？"
                            confirm-button-type="danger"
                            @confirm="removeAccess(access)"
                          >
                            <template #reference>
                              <el-button :disabled="access.access == 'own'" size="small" :icon="Delete" />
                            </template>
                          </el-popconfirm>
                        </div>
                      </template>
                    </el-card>
                  </div>
                </div>
              </el-scrollbar>
            </el-tab-pane>
            <el-tab-pane :disabled="!currentLLM.access.includes('use')" name="health" label="健康检查">
              <el-scrollbar>
                <div class="tab-pane-area">
                  <div>
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
                              <el-tag>{{ currentLLM.llm_base_url }}</el-tag>
                            </el-descriptions-item>
                            <el-descriptions-item label="模型编号">
                              <el-tag>{{ currentLLM.llm_name }}</el-tag>
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
                              <el-tag>{{ currentLLM.llm_company }}</el-tag>
                            </el-descriptions-item>
                            <el-descriptions-item label="测试用例">
                              <el-text>{{ modelTestResult[1]?.test_case }}</el-text>
                              <el-image v-if="modelTestResult[1]?.test_image" :src="modelTestResult[1]?.test_image" />
                            </el-descriptions-item>
                            <el-descriptions-item label="模型类型">
                              <el-tag :type="modelTestResult[1]?.status == '成功' ? 'success' : 'danger'">
                                {{ currentLLM.llm_type }}
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
                  <div v-if="currentTab == 'health'">
                    <el-button type="primary" size="large" :disabled="modelTesting" @click="checkModelConfig">
                      健康检查
                    </el-button>
                  </div>
                </div>
              </el-scrollbar>
            </el-tab-pane>
            <el-tab-pane :disabled="!currentLLM.access.includes('manage')" name="dashboard" label="运行信息">
              <el-scrollbar>
                <div class="tab-pane-area">
                  <div class="params-area">
                    <el-form :model="modelParams" inline label-position="left">
                      <el-form-item prop="timeRange" label="时间范围">
                        <el-date-picker
                          v-model="modelParams.timeRange"
                          type="datetimerange"
                          :shortcuts="shortcuts"
                          @change="refreshModelIndex"
                        />
                      </el-form-item>
                      <el-form-item prop="duration" label="数据粒度">
                        <el-segmented
                          v-model="modelParams.duration"
                          :options="durationOptions"
                          @change="refreshModelIndex"
                        />
                      </el-form-item>
                    </el-form>
                  </div>
                  <div class="base-cnt-area">
                    <el-card v-for="(data, idx) in modelBaseCnt" :key="idx" class="base-cnt-card">
                      <el-statistic :value="data.cnt" style="width: 100px; margin: auto">
                        <template #title>
                          <div style="display: inline-flex; align-items: center">
                            {{ data.title }}
                            <el-tooltip effect="dark" :content="data.desc" placement="top">
                              <el-icon style="margin-left: 4px" :size="12">
                                <Warning />
                              </el-icon>
                            </el-tooltip>
                          </div>
                        </template>
                      </el-statistic>
                      <div class="statistic-footer">
                        <div class="footer-item">
                          <span>与 {{ data.last_begin_time }} 同比</span>
                          <span>
                            {{ data.percent }}
                            <el-icon v-if="data.compare == 'up'" color="green">
                              <CaretTop />
                            </el-icon>
                            <el-icon v-else color="red">
                              <CaretBottom />
                            </el-icon>
                          </span>
                        </div>
                      </div>
                    </el-card>
                  </div>
                  <div class="time-cnt-area">
                    <el-card>
                      <div id="token_time_cnt" />
                    </el-card>
                    <el-card>
                      <div id="qa_time_cnt" />
                    </el-card>
                    <el-card>
                      <div id="user_time_cnt" />
                    </el-card>
                    <el-card>
                      <div id="session_source_cnt" />
                    </el-card>
                    <el-card>
                      <div id="app_top_cnt" />
                    </el-card>
                  </div>
                </div>
              </el-scrollbar>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-scrollbar>
    </el-main>
  </el-container>
  <el-dialog v-model="showUpdateLLMForm" title="模型实例详情" draggable @closed="refreshCurrentModel">
    <el-scrollbar>
      <div class="new-llm">
        <el-form ref="currentLLMFormRef" :model="editLLM" :rules="rules" label-position="top">
          <el-form-item label="模型API密钥" prop="llm_api_secret_key" required>
            <el-input
              v-model="editLLM.llm_api_secret_key"
              placeholder="请输入模型API密钥"
              clearable
              type="password"
              show-password
            />
          </el-form-item>
          <el-form-item label="模型API地址" prop="llm_base_url" required>
            <el-input
              v-model="editLLM.llm_base_url"
              placeholder="请输入模型API地址（如https://api.deepseek.com/v1）"
              clearable
            />
          </el-form-item>
          <el-form-item prop="llm_name" label="模型编号" required>
            <el-input v-model="editLLM.llm_name" placeholder="API中的model参数" clearable />
          </el-form-item>
          <el-form-item prop="llm_label" label="模型名称" required>
            <el-input v-model="editLLM.llm_label" placeholder="模型实例显示名称" clearable />
          </el-form-item>
          <el-form-item prop="llm_type" label="模型类型" required>
            <el-radio-group v-model="editLLM.llm_type">
              <el-radio v-for="type in allModelType" :key="type.value" :label="type.value" :disabled="type?.disable">
                {{ type.label }}
              </el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item prop="llm_desc" label="模型描述">
            <el-input v-model="editLLM.llm_desc" placeholder="请输入模型描述" clearable type="textarea" :rows="6" />
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
              <div v-if="editLLM.llm_icon">
                <el-image :src="editLLM.llm_icon" style="width: 40px; height: 40px" />
              </div>
              <div v-else>
                <el-avatar src="/images/upload_cloud.svg" style="background: #f2f4f7" fit="scale-down" />
                <i class="el-icon-upload" />
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              </div>
            </el-upload>
          </el-form-item>
          <el-form-item label="模型上下文窗口(Tokens)" prop="max_tokens">
            <el-input-number v-model="editLLM.max_tokens" />
          </el-form-item>
          <el-form-item label="模型标签" prop="llm_tags">
            <el-select
              v-model="editLLM.llm_tags"
              placeholder="请选择或创建模型标签"
              multiple
              :multiple-limit="4"
              clearable
              allow-create
              filterable
              default-first-option
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
              v-model="editLLM.llm_company"
              placeholder="请输入模型供应商名称"
              clearable
              filterable
              allow-create
              default-first-option
            >
              <el-option v-for="company in allSupportCompany" :key="company" :value="company" />
            </el-select>
          </el-form-item>
          <el-form-item label="支持OpenAI-SDK" prop="is_std_openai">
            <el-switch v-model="editLLM.is_std_openai" active-text="是" inactive-text="否" />
          </el-form-item>
          <el-form-item label="支持视觉能力" prop="support_vis">
            <el-switch v-model="editLLM.support_vis" active-text="支持" inactive-text="不支持" />
          </el-form-item>
          <el-form-item label="支持长文本能力" prop="support_file">
            <el-switch v-model="editLLM.support_file" active-text="支持" inactive-text="不支持" />
          </el-form-item>
        </el-form>
      </div>
    </el-scrollbar>
    <template #footer>
      <div class="std-middle-box">
        <el-button round @click="showUpdateLLMForm = false"> 取消 </el-button>
        <el-button type="primary" round @click="commitUpdateLLMInstance"> 更新 </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="showUpdateRunConfig" title="模型运行参数" draggable @closed="refreshCurrentModel">
    <el-scrollbar>
      <div class="new-llm">
        <div v-if="editLLM.llm_type && ['文本生成', '推理模型', '全模态'].includes(editLLM.llm_type)">
          <el-form ref="currentLLMConfigRef" :model="editLLM" :rules="configRules" label-position="top">
            <el-form-item prop="stream" label="流式输出" style="height: 80px">
              <el-switch v-model="editLLM.stream" />
            </el-form-item>
            <el-form-item prop="use_default" label="使用默认配置" style="height: 80px">
              <el-switch v-model="editLLM.use_default" />
            </el-form-item>
            <el-form-item prop="temperature" label="温度" style="height: 80px">
              <el-slider
                v-model="editLLM.temperature"
                :min="0"
                :max="2"
                :step="0.1"
                :marks="temperatureMarks"
                style="margin: 0 24px"
                show-input
                :show-input-controls="false"
                :disabled="editLLM.use_default"
              />
            </el-form-item>
            <el-form-item prop="frequency_penalty" label="频率惩罚" style="height: 80px">
              <el-slider
                v-model="editLLM.frequency_penalty"
                :min="-2"
                :max="2"
                :step="0.1"
                :marks="frequencyPenaltyMarks"
                style="margin: 0 24px"
                show-input
                :show-input-controls="false"
                :disabled="editLLM.use_default"
              />
            </el-form-item>
            <el-form-item prop="top_p" label="核采样" style="height: 80px">
              <el-slider
                v-model="editLLM.top_p"
                :min="0"
                :max="1"
                :step="0.1"
                :marks="topPMarks"
                style="margin: 0 24px"
                show-input
                :show-input-controls="false"
                :disabled="editLLM.use_default"
              />
            </el-form-item>
            <el-form-item prop="presence_penalty" label="出现惩罚" style="height: 80px">
              <el-slider
                v-model="editLLM.presence_penalty"
                :min="-2"
                :max="2"
                :step="0.1"
                :marks="frequencyPenaltyMarks"
                style="margin: 0 24px"
                show-input
                :show-input-controls="false"
                :disabled="editLLM.use_default"
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
                :json-schema="editLLM.extra_headers"
                :value-define="true"
                @update:schema="
                  newSchema => {
                    editLLM.extra_headers = newSchema;
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
                :json-schema="editLLM.extra_body"
                :value-define="true"
                @update:schema="
                  newSchema => {
                    editLLM.extra_body = newSchema;
                  }
                "
              />
            </el-form-item>
            <el-form-item prop="think_attr.begin" label="推理开始标签" style="height: 80px">
              <el-input v-model="editLLM.think_attr.begin" placeholder="请输入推理开始标签，如<think>" clearable />
            </el-form-item>
            <el-form-item prop="think_attr.end" label="推理关闭标签" style="height: 80px">
              <el-input v-model="editLLM.think_attr.end" placeholder="请输入推理结束标签,如</think>" clearable />
            </el-form-item>
          </el-form>
        </div>
      </div>
    </el-scrollbar>
    <template #footer>
      <div class="std-middle-box">
        <el-button round @click="showUpdateRunConfig = false"> 取消 </el-button>
        <el-button type="primary" round @click="commitUpdateLLMConfig"> 更新 </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="showUpdateAccess" title="模型授权信息" draggable :fullscreen="true" @closed="refreshCurrentModel">
    <el-scrollbar>
      <div class="new-llm">
        <AuthorSelector
          ref="authorSelectorRef"
          :share-model="editLLM"
          style="height: 100%"
          @update-access-list="
            newList => {
              editLLM.llm_authors = newList;
            }
          "
        />
      </div>
    </el-scrollbar>
    <template #footer>
      <div class="std-middle-box">
        <el-button round @click="showUpdateAccess = false"> 取消 </el-button>
        <el-button type="primary" round @click="commitUpdateLLMAccess"> 更新 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.main-area {
  height: calc(100vh - 90px);
}
.tab-pane-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: calc(100vh - 180px);
}
.std-middle-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.new-llm {
  width: 100%;
  height: 60vh;
}
.access-card {
  width: 320px;
}
.access-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.access-icon {
  width: 24px;
  height: 24px;
}
.access-area {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 16px;
}
.base-cnt-area {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 16px;
}
.base-cnt-card {
  width: 300px;
  height: 130px;
}
.statistic-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--el-text-color-regular);
  margin-top: 16px;
}
.statistic-footer .footer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.statistic-footer .footer-item span:last-child {
  display: inline-flex;
  align-items: center;
  margin-left: 4px;
}
.time-cnt-area {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 16px;
}
.std-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
}
</style>
