<script setup lang="ts">
import { Microphone, Picture as IconPicture, VideoPause, TopRight } from '@element-plus/icons-vue';
import {
  ElMessage,
  ElNotification,
  genFileId,
  UploadFile,
  UploadFiles,
  UploadRawFile,
  type UploadUserFile
} from 'element-plus';
import { v4 as uuidv4 } from 'uuid';
import { computed, nextTick, onMounted, onUnmounted, reactive, ref, watch } from 'vue';
import { llmInstanceSearch } from '@/api/user-center';
import {
  add_messages,
  attachment_add_into_session,
  attachment_add_resources_into_session,
  attachment_add_webpage_tasks,
  attachment_base_init,
  attachment_get_detail,
  attachment_remove_from_session,
  attachment_search_in_session,
  create_session,
  search_session,
  update_session
} from '@/api/next-console';
import { isRecording, startRecording, stopRecording } from '@/components/app-center/ts/agent_console';
import ResourcesSearch from '@/components/next-console/ResourcesSearch.vue';
import {
  calculateMD5,
  calculateSHA256,
  close_upload_manager,
  get_task_icon,
  show_upload_manage_box,
  upload_file_content,
  upload_file_task_list,
  upload_size
} from '@/components/resource/resource_upload/resource_upload';
import ResourceUploadManager from '@/components/resource/resource_upload/resource_upload_manager.vue';
import router from '@/router';
import { useUserConfigStore } from '@/stores/user-config-store';
import { ILLMInstance, ISearchResourceType } from '@/types/user-center';
import { running_question_meta, session_item } from '@/types/next-console';
import { ResourceItem, ResourceUploadItem } from '@/types/resource-type';

const userConfigStore = useUserConfigStore();
const urlDialogWidth = ref(window.innerWidth < 768 ? '80vw' : '40vw');
const simpleVis = ref(window.innerWidth < 768);
const userInputRef = ref();
const consoleInputRef = ref();
const userInput = ref('');
const userComposition = ref(false);
const userBatchSize = ref(0);
const runningQuestions = ref<running_question_meta[]>([]);
const showConsoleInnerHead = ref(false);
const modelListRef = ref(null);
const currentSession = reactive<session_item>({});
const attachmentImagesViewList = computed(() => {
  return uploadImgResourceList.value.map(item => item?.resource_show_url);
});
const emit = defineEmits([
  'begin-answer',
  'update-answer',
  'finish-answer',
  'stop-answer',
  'turn-on-msg-choose-model',
  'height-change',
  'create-session'
]);
const llmInstanceQueue = ref<ILLMInstance[]>([]);
const props = defineProps({
  sessionCode: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '130px'
  },
  mode: {
    type: String,
    default: 'ai_search'
  }
});
const consoleHeight = ref('130px');
const consoleInnerType = ref('ai_search');
const searchEngineLanguageEn = ref(true);
const uploadWebpageDialogVisible = ref(false);
const uploadWebpageDialogRef = ref(null);
const uploadWebpageResourceList = ref<ResourceItem[]>([]);
const uploadWebpageNewResources = reactive<{ new_urls: ResourceItem[] }>({
  new_urls: [
    {
      id: null,
      resource_name: '',
      resource_title: '',
      resource_icon: 'html.svg',
      rag_status: null,
      resource_source_url: ''
    } as ResourceItem
  ]
});
const uploadWebpageNewResourceFormRef = ref(null);
const uploadImgList = ref<UploadUserFile[]>([]);
const uploadImgResourceList = ref<ResourceItem[]>([]);
const uploadImgRef = ref(null);
const uploadImgRepeatCnt = ref(0);
const uploadFileList = ref<UploadUserFile[]>([]);
const uploadFileRef = ref(null);
const uploadFileResourceList = ref<ResourceItem[]>([]);
const uploadFileRepeatCnt = ref(0);
const resourceSearchDialogShow = ref(false);
const availableSearchResourceType = ref<ISearchResourceType[]>([
  {
    resource_type: 'search',
    resource_name: '网页',
    resource_active: true
  },
  {
    resource_type: 'news',
    resource_name: '新闻',
    resource_active: false
  },
  {
    resource_type: 'scholar',
    resource_name: '学术',
    resource_active: false
  }
]);
const sessionResourcesList = ref<ResourceItem[]>([]);
const resourcesSearchRef = ref(null);
const firstImage = ref();
const firstFile = ref();
const loadingSession = ref(false);
async function searchLlmInstance() {
  const params = {
    fetch_all: true
  };
  if (userConfigStore.userConfig.workbench.model_list?.length > 0) {
    params['llm_code'] = userConfigStore.userConfig.workbench.model_list;
  }
  let data = await llmInstanceSearch(params);
  if (!data.error_status) {
    llmInstanceQueue.value = data.result.data;
  }
}
async function switchLlmInstance(item: ILLMInstance) {
  // 切换llm_instance
  // welcome界面
  if (!currentSession?.id) {
    currentSession.session_llm_code = item.llm_code;
    modelListRef.value?.hide();
    ElMessage.success('切换成功!');
    return;
  }
  let params = {
    session_id: currentSession.id,
    session_llm_code: item.llm_code
  };
  let data = await update_session(params);
  if (!data.error_status) {
    currentSession.session_llm_code = item.llm_code;
    modelListRef.value?.hide();
    ElMessage.success('切换成功!');
  }
}
function getSessionLlmName() {
  let currentLlmName = 'DeepSeek-V3';
  if (currentSession.session_llm_code) {
    for (let i = 0; i < llmInstanceQueue.value.length; i++) {
      if (llmInstanceQueue.value[i].llm_code === currentSession.session_llm_code) {
        currentLlmName = llmInstanceQueue.value[i].llm_label;
        if (window.innerWidth < 768) {
          currentLlmName = llmInstanceQueue.value[i].llm_type;
        }
        break;
      }
    }
  }
  return currentLlmName;
}
async function createNewSession() {
  // 创建新的搜索会话
  const params = {
    session_assistant_id: -12345,
    session_status: '进行中',
    session_source: 'next_search',
    session_search_engine_switch: currentSession.session_search_engine_switch,
    session_search_engine_language_type: currentSession.session_search_engine_language_type,
    session_search_engine_resource_type: currentSession.session_search_engine_resource_type,
    session_llm_code: currentSession.session_llm_code,
    session_attachment_image_switch: currentSession.session_attachment_image_switch,
    session_attachment_file_switch: currentSession.session_attachment_file_switch,
    session_attachment_webpage_switch: currentSession.session_attachment_webpage_switch,
    session_local_resource_switch: currentSession.session_local_resource_switch,
    session_local_resource_use_all: currentSession.session_local_resource_use_all
  };
  const res = await create_session(params);
  if (!res.error_status) {
    Object.assign(currentSession, res.result);
    emit('create-session', {});
  }
  await nextTick();
}
async function askQuestion(src = null) {
  // 判断是否达到并发限制
  console.log('askQuestion', currentSession.id, userBatchSize.value, src);
  if (userBatchSize.value >= 3) {
    ElNotification.warning({
      title: '系统消息',
      message: '请等待当前问题处理完毕！',
      duration: 2000
    });
    return false;
  }
  // 判断会话情况
  if (loadingSession.value) {
    await waitForSession();
  }
  if (!currentSession.session_code) {
    // 判断是否为空
    if (!userInput.value || userInput.value.trim() === '') {
      ElNotification.warning({
        title: '系统消息',
        message: '请输入有效问题！',
        duration: 2000
      });
      return false;
    }
    await createNewSession();
    let userMsgContent = userInput.value.replace(/\n/g, '\n\n');
    localStorage.setItem('nc_new_ask_question', userMsgContent);
    router.push({
      name: 'message_flow',
      params: { session_code: currentSession.session_code },
      query: { ...router.currentRoute.value.query, auto_ask: 'true' } // 保持既有参数
    });
    return;
  }
  if (router.currentRoute.value.query?.auto_ask) {
    const localQuestion = localStorage.getItem('nc_new_ask_question');
    if (localQuestion && !userInput.value) {
      userInput.value = localQuestion;
      localStorage.removeItem('nc_new_ask_question');
    }
  }
  // 判断是否为空
  if (!userInput.value || userInput.value.trim() === '') {
    console.log(userInput.value, currentSession.session_code);
    ElNotification.warning({
      title: '系统消息',
      message: '请输入有效问题！',
      duration: 2000
    });
    return false;
  }
  // 用户输入预处理：将换行符替换为两个换行符
  let userMsgContent = userInput.value.replace(/\n/g, '\n\n');
  let msgAbortController = new AbortController();
  // 更新数据
  let targetQuestion = {
    qa_item_idx: uuidv4(),
    begin_time: performance.now(),
    abort_controller: msgAbortController,
    end_time: null,
    status: 'running'
  };
  runningQuestions.value.push(targetQuestion);
  emit('begin-answer', {
    data: userMsgContent,
    userQaID: targetQuestion.qa_item_idx
  });
  // 开始启动
  userInput.value = null;
  let params = {
    session_id: currentSession.id,
    msg_content: userMsgContent,
    stream: true,
    session_source: 'next_search'
  };
  userBatchSize.value += 1;
  let qaId = null;
  try {
    let data = await add_messages(params, msgAbortController.signal);
    // 处理流式响应来更新消息
    const reader = data.body.getReader();
    let chunk = await reader.read();
    while (!chunk.done) {
      emit('update-answer', {
        data: chunk,
        userQaID: targetQuestion.qa_item_idx
      });
      if (!qaId) {
        let jsonData = new TextDecoder('utf-8').decode(chunk.value);
        const lines = jsonData.split('\n');
        for (const line of lines) {
          if (line.startsWith('data:')) {
            jsonData = line.slice(5).trim(); // 移除"data:"前缀
            try {
              jsonData = JSON.parse(jsonData);
            } catch (e) {
              break;
            }
            qaId = jsonData?.qa_id;
            break;
          }
        }
      }
      chunk = await reader.read();
    }
  } catch (e) {
    if (e.name == 'AbortError') {
      console.log('问题已停止');
    }
  }
  userBatchSize.value -= 1;
  // 完成后更新回答结果的id
  emit('finish-answer', { qaId: qaId });
  // 更新问题状态
  let idx = runningQuestions.value.indexOf(targetQuestion);
  runningQuestions.value.splice(idx, 1);
}
async function stopQuestion(targetQuestion: running_question_meta | null = null) {
  // 如果没有传入参数，则停止最新的问题
  if (!targetQuestion) {
    if (runningQuestions.value.length === 0) {
      ElMessage({
        message: '没有正在运行的问题',
        type: 'warning'
      });
      return;
    }
    targetQuestion = runningQuestions.value[0];
  }
  // 将传入的消息队列中的所有问题停止
  targetQuestion.abort_controller.abort();
  targetQuestion.end_time = performance.now();
  ElMessage({
    message: '问题已停止',
    type: 'success'
  });
  emit('stop-answer', {
    userQaId: targetQuestion.qa_item_idx
  });
}
async function handleKeyDown(event) {
  // 正确识别用户提交行为与换行行为
  if (event.key === 'Enter' && !userComposition.value) {
    if (event.ctrlKey || event.shiftKey) {
      const start = event.target.selectionStart;
      const end = event.target.selectionEnd;
      if (!userInput.value) {
        return false;
      }
      userInput.value = userInput.value.slice(0, start) + '\n' + userInput.value.slice(end);
      nextTick().then(() => {
        event.target.selectionStart = start + 1;
        event.target.selectionEnd = start + 1;

        const textarea = userInputRef.value.$el.querySelector('textarea');
        textarea.scrollTop = textarea.scrollHeight;
      });
    } else {
      await askQuestion('keydown');
    }
  }
}
async function handleUserPaste(event: any) {
  // 处理用户复制动作
  const items = event.clipboardData.items;
  // 分析剪切板文件类型
  let imagesList = [];
  let fileList = [];
  for (let i = 0; i < items.length; i++) {
    if (items[i].kind == 'string') {
      continue;
    }
    if (items[i].type.indexOf('image') !== -1) {
      imagesList.push(items[i].getAsFile());
    } else {
      fileList.push(items[i].getAsFile());
    }
  }
  console.log(imagesList, fileList);
  if (imagesList.length > 0) {
    await switchOnImgSearch();
    for (let j = 0; j < imagesList.length; j++) {
      if (imagesList[j]) {
        const file = new File([imagesList[j]], imagesList[j].name, { type: imagesList[j].type }) as UploadRawFile;
        file.uid = genFileId();
        uploadImgRef.value?.handleStart(file);
        uploadImgList.value.push(file);
      }
    }
    uploadImgRef.value?.submit();
  }
  if (fileList.length > 0) {
    await switchOnFileSearch();
    for (let j = 0; j < fileList.length; j++) {
      if (fileList[j]) {
        const file = new File([fileList[j]], fileList[j].name, { type: fileList[j].type }) as UploadRawFile;
        file.uid = genFileId();
        uploadFileRef.value?.handleStart(file);
        uploadFileList.value.push(file);
      }
    }
    uploadFileRef.value?.submit();
  }
}
function handleDragOver(event) {
  event.preventDefault();
}
async function handleDrop(event) {
  // 获取拖拽文件
  const files = event.dataTransfer.files;
  if (files.length > 0) {
    let imagesList = [];
    let fileList = [];
    for (let file of files) {
      if (file.type.indexOf('image') !== -1) {
        imagesList.push(file);
      } else {
        fileList.push(file);
      }
    }
    if (imagesList.length > 0) {
      await switchOnImgSearch();
      for (let j = 0; j < imagesList.length; j++) {
        if (imagesList[j]) {
          const file = imagesList[j] as UploadRawFile;
          file.uid = genFileId();
          uploadImgRef.value?.handleStart(file);
          uploadImgList.value.push(file);
          if (!currentSession?.id) {
            prepareUploadImage(file);
          }
        }
      }
      if (currentSession?.id) {
        uploadImgRef.value?.submit();
      }
    }
    if (fileList.length > 0) {
      await switchOnFileSearch();
      for (let j = 0; j < fileList.length; j++) {
        if (fileList[j]) {
          const file = fileList[j] as UploadRawFile;
          file.uid = genFileId();
          uploadFileRef.value?.handleStart(file);
          uploadFileList.value.push(file);
          if (!currentSession?.id) {
            prepareUploadFile(file);
          }
        }
      }
      if (currentSession?.id) {
        uploadFileRef.value?.submit();
      }
    }
  }
}
async function handleInputChange() {
  // 更新高度
  setTimeout(() => {
    const newHeight = Math.min(150, consoleInputRef.value.clientHeight + 130);
    emit('height-change', { newHeight: newHeight });
  }, 10);
}
async function initCurrentSession(sessionCode = null) {
  if (sessionCode) {
    const params = {
      session_codes: [props.sessionCode]
    };
    loadingSession.value = true;
    const data = await search_session(params);
    Object.assign(currentSession, data.result[0]);
    loadingSession.value = false;
    getAllSessionAttachments();
  }
}
async function clickRecommendQuestion(data) {
  userInput.value = data.question;
  userInputRef.value.focus();
  askQuestion('recommend');
}
function handleAsr(data) {
  // 语音识别
  if (data) {
    userInput.value += data;
    userInputRef.value.focus();
  }
}
async function switchOnAiSearch() {
  // 启停ai搜索功能
  if (!currentSession.session_search_engine_switch) {
    // 启动并展示配置区域
    currentSession.session_search_engine_switch = true;
    // 保持会话配置
    if (currentSession.id) {
      update_session({
        session_id: currentSession.id,
        session_search_engine_switch: true
      });
    }
  }
  showConsoleInnerHead.value = true;
  consoleInnerType.value = 'ai_search';
  // @ts-ignore
  if (!currentSession.session_search_engine_language_type?.gl) {
    searchEngineLanguageEn.value = true;
  } else {
    searchEngineLanguageEn.value = false;
  }
  for (let i = 0; i < availableSearchResourceType.value.length; i++) {
    availableSearchResourceType.value[i].resource_active =
      availableSearchResourceType.value[i].resource_type == currentSession.session_search_engine_resource_type;
  }
  await nextTick(() => {
    if (window.innerWidth >= 768) {
      consoleInputRef.value.focus();
    }
  });
}
async function switchAiSearchLanguage() {
  // 切换搜索语言
  if (searchEngineLanguageEn.value) {
    currentSession.session_search_engine_language_type = {};
  }
  // 中文
  else {
    currentSession.session_search_engine_language_type = { hl: 'zh-cn', gl: 'cn' };
  }
  // 保存配置
  if (currentSession.id) {
    update_session({
      session_id: currentSession.id,
      session_search_engine_language_type: currentSession.session_search_engine_language_type
    });
  }
}
async function hideAiSearchConfigArea() {
  showConsoleInnerHead.value = false;
  await nextTick(() => {
    consoleInputRef.value.focus();
  });
}
async function switchOffAiSearch() {
  currentSession.session_search_engine_switch = false;
  if (currentSession.id) {
    update_session({
      session_id: currentSession.id,
      session_search_engine_switch: false
    });
  }
  hideAiSearchConfigArea();
}
async function switchOnWebpageSearch() {
  // 打开网页问答配置区域
  showConsoleInnerHead.value = true;
  consoleInnerType.value = 'ai_webpage';
  currentSession.session_attachment_webpage_switch = true;
  if (!uploadWebpageResourceList.value.length) {
    // 打开网页问答地址输入区域
    uploadWebpageDialogVisible.value = true;
  }
  if (!currentSession?.id) {
    return;
  }
  // 更新至后端
  update_session({
    session_id: currentSession.id,
    session_attachment_webpage_switch: true
  });
  // 获取对应文件资源明细
  if (uploadWebpageResourceList.value.length > 0) {
    let params = {
      session_id: currentSession.id,
      attachment_source: 'webpage'
    };
    let res = await attachment_get_detail(params);
    if (!res.error_status) {
      uploadWebpageResourceList.value = res.result;
      // 标记是否支持
      for (let resource of uploadWebpageResourceList.value) {
        resource.resource_is_supported = checkWebpageSupportStatus(resource);
      }
    }
  }
}
async function hideAiWebpageConfigArea() {
  showConsoleInnerHead.value = false;
  await nextTick(() => {
    if (window.innerWidth >= 768) {
      consoleInputRef.value.focus();
    }
  });
  if (!uploadWebpageResourceList.value.length) {
    currentSession.session_attachment_webpage_switch = false;
    if (!currentSession?.id) {
      return;
    }
    update_session({
      session_id: currentSession.id,
      session_attachment_webpage_switch: false
    });
  }
}
async function switchOffWebpageSearch() {
  currentSession.session_attachment_webpage_switch = false;
  hideAiWebpageConfigArea();
  if (!currentSession?.id) {
    return;
  }
  update_session({
    session_id: currentSession.id,
    session_attachment_webpage_switch: false
  });
}
function getResourceIcon(resource: ResourceItem) {
  // 获取资源图标
  if (resource.resource_icon) {
    if (
      resource.resource_icon.includes('http') ||
      resource.resource_icon.includes('data:image') ||
      resource.resource_icon.includes('/images/')
    ) {
      return resource.resource_icon;
    }
    return '/images/' + resource.resource_icon;
  } else {
    return '/images/html.svg';
  }
}
async function removeWebpageItem(index: number) {
  // 删除网页
  const resourceId = uploadWebpageResourceList.value[index].id;
  uploadWebpageResourceList.value.splice(index, 1);
  if (!currentSession?.id) {
    return;
  }
  // 同步到后端
  attachment_remove_from_session({
    session_id: currentSession.id,
    resource_list: [resourceId]
  });
}
async function cleanTmpWebpageList() {
  uploadWebpageResourceList.value = [];
  if (!currentSession?.id) {
    return;
  }
  // 同步到后端
  attachment_remove_from_session({
    session_id: currentSession.id,
    clean_all: true,
    attachment_source: 'webpage'
  });
}
function validateUrlRepeat(rule: any, value: any, callback: any) {
  // 验证网页地址是否与已有数据重复
  let repeat = 0;
  for (let i of uploadWebpageNewResources.new_urls) {
    if (i.resource_source_url == value && value) {
      repeat++;
    }
  }
  if (repeat > 1) {
    callback(new Error('不能重复添加相同的网页地址'));
  }
  repeat = 0;
  for (let i of uploadWebpageResourceList.value) {
    if (i.resource_source_url == value && value) {
      repeat++;
    }
  }
  if (repeat > 1) {
    callback(new Error('会话中已经有相同的网页地址了哦！'));
  } else {
    callback();
  }
}
function removeNewWebpageResource(index: number) {
  // 删除新的网页资源
  if (uploadWebpageNewResources.new_urls?.length == 1) {
    uploadWebpageNewResources.new_urls[0].resource_source_url = '';
    ElMessage.warning('没办法再删了哦！');
    return;
  }
  uploadWebpageNewResources.new_urls.splice(index, 1);
}
function addNewWebpageResource() {
  // 添加新的网页资源
  uploadWebpageNewResources.new_urls.push({
    id: null,
    resource_name: '',
    resource_title: '',
    resource_icon: 'html.svg',
    rag_status: null,
    resource_source_url: ''
  } as ResourceItem);
}
function switchOffNewWebpage() {
  // 关闭新的网页资源输入框
  uploadWebpageDialogVisible.value = false;
  // 去除非法数据
  for (let i = 0; i < uploadWebpageNewResources.new_urls.length; i++) {
    if (!uploadWebpageNewResources.new_urls[i].resource_source_url) {
      uploadWebpageNewResources.new_urls.splice(i, 1);
      i--;
    }
  }
  if (!uploadWebpageNewResources.new_urls.length) {
    uploadWebpageNewResources.new_urls.push({
      id: null,
      resource_title: '',
      rag_status: null,
      resource_source_url: ''
    } as ResourceItem);
  }
  if (!currentSession?.id) {
    return;
  }
}
function checkWebpageSupportStatus(resource: ResourceItem): boolean {
  // 检查是否支持
  if (resource?.rag_status == '异常' || resource?.rag_status == '失败') {
    return false;
  }
  if (resource?.rag_status == '成功') {
    return true;
  }
  return null;
}
async function commitAddNewWebpages() {
  // 先对新的网页资源进行校验
  let validRes = await uploadWebpageNewResourceFormRef.value?.validate();
  if (uploadWebpageNewResourceFormRef.value?.validate && !validRes) {
    return;
  }
  uploadWebpageDialogVisible.value = false;
  let allUrls = [];
  for (let i of uploadWebpageResourceList.value) {
    if (i.resource_source_url && !i.id) {
      allUrls.push(i.resource_source_url);
    }
  }
  for (let i of uploadWebpageNewResources.new_urls) {
    if (!i.resource_source_url) {
      continue;
    }
    i.resource_name = i.resource_source_url;
    if (allUrls.includes(i.resource_source_url)) {
      continue;
    }
    uploadWebpageResourceList.value.push(i);
    allUrls.push(i.resource_source_url);
  }
  // 更新至后端
  if (!currentSession?.id) {
    await createNewSession();
  }
  await update_session({
    session_id: currentSession.id,
    session_attachment_webpage_switch: true
  });
  let initRes = await attachment_base_init({
    session_id: currentSession.id
  });
  if (initRes.error_status) {
    return false;
  }
  let resourceParentId = initRes.result.id;

  let res = await attachment_add_webpage_tasks({
    session_id: currentSession.id,
    qa_id: '',
    msg_id: '',
    resource_parent_id: resourceParentId,
    urls: allUrls
  });
  if (!res.error_status) {
    // 更新资源信息
    for (let i of res.result) {
      for (let j of uploadWebpageResourceList.value) {
        if (i.resource_source_url == j.resource_source_url) {
          j.id = i.id;
          break;
        }
        j.resource_is_supported = checkWebpageSupportStatus(j);
      }
    }
  }
  // 重置新的网页资源
  uploadWebpageNewResources.new_urls = [
    {
      id: null,
      resource_name: '',
      resource_title: '',
      resource_icon: 'html.svg',
      rag_status: null,
      resource_source_url: ''
    } as ResourceItem
  ];
  await router.push({
    name: 'message_flow',
    params: { session_code: currentSession.session_code },
    query: { ...router.currentRoute.value.query, auto_ask: 'true' } // 保持既有参数
  });
  await nextTick();
}
function updateSessionAttachment(data) {
  for (const resource of data) {
    if (resource.resource_source == 'session') {
      // 更新附件资源状态
      for (let i = 0; i < uploadFileResourceList.value.length; i++) {
        if (uploadFileResourceList.value[i].id == resource.id) {
          uploadFileResourceList.value[i].rag_status = resource.rag_status;
          uploadFileResourceList.value[i].resource_is_supported = checkFileSupportStatus(
            uploadFileResourceList.value[i]
          );
        }
      }
      for (let i = 0; i < uploadWebpageResourceList.value.length; i++) {
        if (uploadWebpageResourceList.value[i].id == resource.id) {
          if (resource?.rag_status) {
            uploadWebpageResourceList.value[i].rag_status = resource.rag_status;
          }
          if (resource?.resource_icon) {
            uploadWebpageResourceList.value[i].resource_icon = resource.resource_icon;
          }
          if (resource?.resource_title) {
            uploadWebpageResourceList.value[i].resource_title = resource.resource_title;
          }
          if (resource?.resource_name) {
            uploadWebpageResourceList.value[i].resource_name = resource.resource_name;
          }
          if (resource?.resource_size_in_MB) {
            uploadWebpageResourceList.value[i].resource_size_in_MB = resource.resource_size_in_MB;
          }
          if (resource?.resource_status) {
            uploadWebpageResourceList.value[i].resource_status = resource.resource_status;
          }
          uploadWebpageResourceList.value[i].resource_is_supported = checkWebpageSupportStatus(
            uploadWebpageResourceList.value[i]
          );
        }
      }
    }
  }
}
async function getAllSessionAttachments() {
  // 获取当前会话的所有附件
  if (!currentSession.id) {
    return;
  }
  const params = {
    session_id: currentSession.id,
    attachment_sources: []
  };
  const res = await attachment_search_in_session(params);
  if (!res.error_status) {
    let currentSessionAttachments = res.result;
    uploadImgResourceList.value = [];
    uploadFileResourceList.value = [];
    uploadWebpageResourceList.value = [];
    sessionResourcesList.value = [];
    if (currentSessionAttachments.length > 0) {
      for (const i of currentSessionAttachments) {
        if (i.attachment_source == 'images') {
          uploadImgResourceList.value.push({
            id: i.id
          } as ResourceItem);
        } else if (i.attachment_source == 'files') {
          uploadFileResourceList.value.push({
            id: i.id
          } as ResourceItem);
        } else if (i.attachment_source == 'webpage') {
          uploadWebpageResourceList.value.push({
            id: i.id
          } as ResourceItem);
        } else if (i.attachment_source == 'resources') {
          sessionResourcesList.value.push({
            id: i.id
          } as ResourceItem);
        }
      }
    }
    if (currentSession.session_local_resource_use_all) {
      sessionResourcesList.value.push(
        //@ts-ignore
        {
          resource_id: -1,
          resource_icon: 'all_resource.svg',
          resource_name: '全部资源'
        } as ResourceItem
      );
    }
    // 更新会话附件标签
    if (!uploadImgResourceList.value.length) {
      currentSession.session_attachment_image_switch = false;
    }
    if (!uploadFileResourceList.value.length) {
      currentSession.session_attachment_file_switch = false;
    }
    if (!uploadWebpageResourceList.value.length) {
      currentSession.session_attachment_webpage_switch = false;
    }
    update_session({
      session_id: currentSession.id,
      session_attachment_image_switch: currentSession.session_attachment_image_switch,
      session_attachment_file_switch: currentSession.session_attachment_file_switch,
      session_attachment_webpage_switch: currentSession.session_attachment_webpage_switch
    });
  }
}
async function cleanTmpImgList() {
  // 清空临时图片列表
  uploadImgList.value = [];
  uploadImgResourceList.value = [];
  if (!currentSession?.id) {
    return;
  }
  // 同步到后端
  attachment_remove_from_session({
    session_id: currentSession.id,
    clean_all: true,
    attachment_source: 'images'
  });
}
async function hideAiImageConfigArea() {
  showConsoleInnerHead.value = false;
  await nextTick(() => {
    if (window.innerWidth >= 768) {
      consoleInputRef.value.focus();
    }
  });
  if (!uploadImgResourceList.value.length) {
    currentSession.session_attachment_image_switch = false;
    if (!currentSession?.id) {
      return;
    }
    update_session({
      session_id: currentSession.id,
      session_attachment_image_switch: false
    });
  }
}
async function removeImgItem(index: number) {
  // 删除图片
  const resourceId = uploadImgResourceList.value[index].id;
  uploadImgList.value?.splice(index, 1);
  uploadImgResourceList.value.splice(index, 1);
  if (!currentSession?.id) {
    return;
  }
  // 同步到后端
  attachment_remove_from_session({
    session_id: currentSession.id,
    resource_list: [resourceId]
  });
}
async function switchOnImgSearch() {
  // 打开图像问答配置区域
  showConsoleInnerHead.value = true;
  consoleInnerType.value = 'ai_image';
  currentSession.session_attachment_image_switch = true;
  if (!currentSession?.id) {
    return;
  }
  // 更新至后端
  update_session({
    session_id: currentSession.id,
    session_attachment_image_switch: true
  });
  // 获取对应图片资源明细
  if (uploadImgResourceList.value.length > 0) {
    let params = {
      session_id: currentSession.id,
      attachment_source: 'images'
    };
    let res = await attachment_get_detail(params);
    if (!res.error_status) {
      uploadImgResourceList.value = res.result;
      // 标记是否支持
      for (let resource of uploadImgResourceList.value) {
        resource.resource_is_supported = checkImgSupportStatus(resource);
      }
    }
  }
}
function checkImgSupportStatus(imgResource: ResourceItem) {
  // 基于图像类型进行预检查
  // 格式支持png，gif，jpg，jpeg,webp
  // 每张图片不能超过20Mb
  if (
    imgResource.resource_name.endsWith('.png') ||
    imgResource.resource_name.endsWith('.jpg') ||
    imgResource.resource_name.endsWith('.jpeg') ||
    imgResource.resource_name.endsWith('.webp')
  ) {
    if (imgResource.resource_size_in_MB < 20) {
      return true;
    }
  }
  return false;
}
async function switchOffImageSearch() {
  currentSession.session_attachment_image_switch = false;
  hideAiImageConfigArea();
  if (!currentSession?.id) {
    return;
  }
  update_session({
    session_id: currentSession.id,
    session_attachment_image_switch: false
  });
}
async function waitForSession() {
  return new Promise(resolve => {
    const check = () => {
      if (currentSession?.id) {
        resolve(void 0);
      } else {
        setTimeout(check, 100);
      }
    };
    check();
  });
}
async function handleImageFileChange(uploadFile: UploadFile, uploadFiles: UploadFiles) {
  if (!firstImage.value) {
    firstImage.value = uploadFile;
  }
  console.log(uploadFile.uid, uploadFile.raw, firstImage.value.uid);
}
async function prepareUploadImage(uploadFile: UploadRawFile) {
  // 如果没有会话，则等待到会话生成
  if (!currentSession?.id) {
    if (uploadFile?.uid == firstImage.value.uid) {
      await createNewSession();
    } else {
      await waitForSession();
    }
  }
  let fileSHA256 = '';
  try {
    fileSHA256 = await calculateMD5(uploadFile);
    if (!fileSHA256) {
      fileSHA256 = await calculateSHA256(uploadFile);
    }
  } catch (e) {
    fileSHA256 = await calculateSHA256(uploadFile);
  }
  // 2. 准备参数
  let resourceSize = uploadFile.size / 1024 / 1024;
  let contentMaxIdx = Math.floor(resourceSize / upload_size.value);
  // 前端临时可视化文件类型和格式
  let resourceType = '';
  let resourceFormat = '';
  if (uploadFile.name.indexOf('.') > -1) {
    resourceFormat = uploadFile.name.split('.').pop().toLowerCase();
  }
  resourceType = uploadFile.type;
  let taskIcon = get_task_icon(resourceType, resourceFormat);

  //@ts-ignore
  let newResource = {
    id: uploadFile.uid,
    resource_name: uploadFile.name,
    resource_size_in_mb: resourceSize,
    resource_type: resourceType,
    resource_format: resourceFormat,
    resource_show_url: URL.createObjectURL(uploadFile),
    resource_is_supported: checkImgSupportStatus({
      resource_name: uploadFile.name,
      resource_format: resourceFormat,
      resource_size_in_MB: resourceSize
    } as ResourceItem),
    resource_feature_code: fileSHA256
  } as ResourceItem;
  // 如果有则覆盖，如果没有则更新
  let findFlag = false;
  let repeatFlag = false;
  for (let i = 0; i < uploadImgResourceList.value.length; i++) {
    if (uploadImgResourceList.value[i].id == newResource.id) {
      findFlag = true;
      uploadImgResourceList.value[i] = newResource;
      break;
    }
    if (uploadImgResourceList.value[i].resource_feature_code == newResource.resource_feature_code) {
      repeatFlag = true;
      break;
    }
  }
  if (!findFlag && !repeatFlag) {
    uploadImgResourceList.value.push(newResource);
  }
  if (repeatFlag) {
    uploadImgRepeatCnt.value += 1;
    await uploadImgRef.value.handleRemove(uploadFile);
  }
  if (uploadImgList.value.length == uploadImgResourceList.value.length && uploadImgRepeatCnt.value > 0) {
    ElNotification.success({
      title: '系统通知',
      message: `检测到重复图片${uploadImgRepeatCnt.value}个，已自动过滤！`,
      duration: 5000
    });
    uploadImgRepeatCnt.value = 0;
  }

  // 3. 初始化会话资源文件夹并获取到资源文件夹id
  show_upload_manage_box.value = true;
  let initRes = await attachment_base_init({
    session_id: currentSession.id
  });
  if (initRes.error_status) {
    return false;
  }
  let resourceParentId = initRes.result.id;
  upload_file_task_list.value.push(<ResourceUploadItem>{
    id: null,
    resource_parent_id: resourceParentId,
    resource_id: null,
    resource_name: uploadFile.name,
    resource_size_in_mb: resourceSize,
    resource_type: resourceType,
    resource_format: resourceFormat,
    content_max_idx: contentMaxIdx,
    content_finish_idx: -1,
    resource_md5: fileSHA256,
    raw_file: uploadFile,
    task_icon: taskIcon,
    task_source: 'session',
    task_status: 'pending'
  });
}
async function uploadImgSuccess(response: any, uploadFile: UploadFile, uploadFiles: UploadFiles) {
  // 上传成功后，添加附件与会话消息
  let imgResource = response.result as ResourceUploadItem;
  let resourceId = response.result?.resource_id;
  if (!resourceId) {
    return;
  }
  let params = {
    session_id: currentSession.id,
    resource_id: resourceId,
    attachment_source: 'images'
  };
  await attachment_add_into_session(params);
  // 找到预处理阶段保存的并更新resource_id
  for (let resource of uploadImgResourceList.value) {
    if (uploadFile.raw.uid == resource.id) {
      resource.id = imgResource.resource_id;
    }
  }
  // 判断当前模型并升级为视觉模型
  // 找到用户的第一个视觉模型
  let availableVisionLlmCode = '';
  for (let i = 0; i < llmInstanceQueue.value.length; i++) {
    if (llmInstanceQueue.value[i]?.support_vis) {
      availableVisionLlmCode = llmInstanceQueue.value[i].llm_code;
      break;
    }
  }
  if (!availableVisionLlmCode) {
    ElNotification.warning({
      title: '系统通知',
      message: '未找到可用的视觉模型',
      duration: 5000
    });
    return;
  }
  for (let i = 0; i < llmInstanceQueue.value.length; i++) {
    // 找到当前会话的模型
    if (llmInstanceQueue.value[i].llm_code === currentSession.session_llm_code) {
      // 判断是否为视觉模型
      if (llmInstanceQueue.value[i].support_vis) {
        break;
      }
      currentSession.session_llm_code = availableVisionLlmCode;
      update_session({
        session_id: currentSession.id,
        session_llm_code: availableVisionLlmCode
      });
      ElNotification.success({
        title: '系统通知',
        message: '已为您自动升级为支持视觉的大模型！',
        duration: 5000
      });
      break;
    }
  }

  // 判断是否全部任务完成，完成则关闭上传管理框
  let finishFlag = true;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (
      upload_file_task_list.value[i].task_status == 'pending' ||
      upload_file_task_list.value[i].task_status == 'uploading'
    ) {
      finishFlag = false;
      break;
    }
  }
  if (finishFlag) {
    close_upload_manager();
    firstImage.value = null;
    await router.push({
      name: 'message_flow',
      params: { session_code: currentSession.session_code },
      query: { ...router.currentRoute.value.query, auto_ask: 'true' } // 保持既有参数
    });
    await nextTick();
  }
}
async function cleanTmpFileList() {
  // 清空临时图片列表
  uploadFileList.value = [];
  uploadFileResourceList.value = [];
  if (!currentSession?.id) {
    return;
  }
  // 同步到后端
  attachment_remove_from_session({
    session_id: currentSession.id,
    clean_all: true,
    attachment_source: 'files'
  });
}
async function hideAiFileConfigArea() {
  showConsoleInnerHead.value = false;
  await nextTick(() => {
    if (window.innerWidth >= 768) {
      consoleInputRef.value.focus();
    }
  });
  if (!uploadFileResourceList.value.length) {
    currentSession.session_attachment_file_switch = false;
    if (!currentSession?.id) {
      return;
    }
    update_session({
      session_id: currentSession.id,
      session_attachment_file_switch: false
    });
  }
}
async function switchOnFileSearch() {
  // 打开文档问答配置区域
  showConsoleInnerHead.value = true;
  consoleInnerType.value = 'ai_file';
  currentSession.session_attachment_file_switch = true;
  if (!currentSession?.id) {
    return;
  }
  // 更新至后端
  update_session({
    session_id: currentSession.id,
    session_attachment_file_switch: true
  });
  // 获取对应文件资源明细
  if (uploadFileResourceList.value.length > 0) {
    let params = {
      session_id: currentSession.id,
      attachment_source: 'files'
    };
    let res = await attachment_get_detail(params);
    if (!res.error_status) {
      uploadFileResourceList.value = res.result;
      // 标记是否支持
      for (let resource of uploadFileResourceList.value) {
        resource.resource_is_supported = checkFileSupportStatus(resource);
      }
    }
  }
}
async function switchOffFileSearch() {
  currentSession.session_attachment_file_switch = false;
  hideAiFileConfigArea();
  if (!currentSession?.id) {
    return;
  }
  update_session({
    session_id: currentSession.id,
    session_attachment_file_switch: false
  });
}
function checkFileSupportStatus(fileResource: ResourceItem) {
  let allSupportFormats = [
    // 文档
    'doc',
    'docx',
    'xls',
    'xlsx',
    'ppt',
    'pptx',
    'pdf',
    'txt',
    // 代码
    'css',
    'js',
    'json',
    'xml',
    'java',
    'cpp',
    'c',
    'py',
    'php',
    'go',
    'h',
    'hpp',
    'rb',
    'cs',
    'sh',
    'bat',
    'swift',
    'kt',
    'ts',
    'pl',
    'lua',
    'r',
    'scala',
    'sql',
    'vb',
    'vbs',
    'yaml',
    'yml',
    'md',
    'ps1',
    'ini',
    'conf',
    'properties',
    'cmd',
    'vue',
    'jsx',
    'perl',
    'db2',
    'rs',
    'mm',
    'm',
    'plsql',
    'hs',
    'hsc',
    'Dockerfile',
    'dart',
    'pm',
    'bash',
    'svelte',
    'htm',
    'html',
    'log',
    'syslog',
    'audit',
    'wevt',
    'kmsg',
    'access',
    'cfg',
    'ini',
    'service',
    'rules',
    'policy',
    'rrd',
    'tsd',
    'metrics',
    'stats',
    'pcap',
    'flow',
    'sflow',
    'pdns',
    'crontab',
    'fstab',
    'grub',
    'conf',
    'ovf',
    'qcow2',
    'yaml',
    'toml',
    'hash',
    'sig',
    'gpg',
    'p12',
    'diff',
    'snap',
    'tar',
    'manifest'
  ];
  if (fileResource?.rag_status) {
    if (typeof fileResource.rag_status == 'string') {
      if (fileResource.rag_status == '成功') {
        return true;
      }
      if (fileResource.rag_status == '失败' || fileResource.rag_status == '异常') {
        return false;
      }
      if (fileResource.rag_status == '排队') {
        return null;
      }
    }
    // 资源空间
    for (let i of fileResource.rag_status) {
      // @ts-ignore
      if (i?.status == '失败' || i?.status == '异常') {
        return false;
      }
      // @ts-ignore
      else if (i?.status == '成功') {
        return true;
      }
      // @ts-ignore
      else if (i?.status == '排队') {
        return null;
      }
    }
  } else if (!allSupportFormats.includes(fileResource.resource_format)) {
    return false;
  }
  return null;
}
async function removeFileItem(index: number) {
  const resourceId = uploadFileResourceList.value[index].id;
  uploadFileList.value?.splice(index, 1);
  uploadFileResourceList.value.splice(index, 1);
  if (!currentSession?.id) {
    return;
  }
  // 同步到后端
  attachment_remove_from_session({
    session_id: currentSession.id,
    resource_list: [resourceId]
  });
}
function handleFileChange(uploadFile: UploadFile, uploadFiles: UploadFiles) {
  // 处理文件上传
  if (!firstFile.value) {
    firstFile.value = uploadFile;
  }
}
async function prepareUploadFile(uploadFile: UploadRawFile) {
  if (!currentSession?.id) {
    if (uploadFile?.uid == firstFile.value.uid) {
      await createNewSession();
    } else {
      await waitForSession();
    }
  }
  // 1. 计算文件的MD5值
  let fileSHA256 = '';
  try {
    fileSHA256 = await calculateMD5(uploadFile);
    if (!fileSHA256) {
      fileSHA256 = await calculateSHA256(uploadFile);
    }
  } catch (e) {
    fileSHA256 = await calculateSHA256(uploadFile);
  }
  // 2. 准备参数
  let resourceSize = uploadFile.size / 1024 / 1024;
  let contentMaxIdx = Math.floor(resourceSize / upload_size.value);
  // 前端临时可视化文件类型和格式
  let resourceType = '';
  let resourceFormat = '';
  if (uploadFile.name.indexOf('.') > -1) {
    resourceFormat = uploadFile.name.split('.').pop().toLowerCase();
  }
  resourceType = uploadFile.type;
  let taskIcon = get_task_icon(resourceType, resourceFormat);
  //@ts-ignore
  let newResource = {
    id: uploadFile.uid,
    resource_name: uploadFile.name,
    resource_size_in_mb: resourceSize,
    resource_type: resourceType,
    resource_format: resourceFormat,
    resource_icon: resourceFormat + '.svg',
    resource_is_supported: checkFileSupportStatus({
      resource_name: uploadFile.name,
      resource_format: resourceFormat,
      resource_size_in_MB: resourceSize
    } as ResourceItem),
    resource_feature_code: fileSHA256
  } as ResourceItem;
  let findFlag = false;
  let repeatFlag = false;
  for (let i = 0; i < uploadFileResourceList.value.length; i++) {
    if (uploadFileResourceList.value[i].id == newResource.id) {
      findFlag = true;
      uploadFileResourceList.value[i].id = newResource.id;
      break;
    }
    if (uploadFileResourceList.value[i].resource_feature_code == newResource.resource_feature_code) {
      repeatFlag = true;
      break;
    }
  }
  if (!findFlag && !repeatFlag) {
    uploadFileResourceList.value.push(newResource);
  }
  if (repeatFlag) {
    uploadFileRepeatCnt.value += 1;
    await uploadFileRef.value.handleRemove(uploadFile);
  }

  if (uploadFileList.value.length == uploadFileResourceList.value.length && uploadFileRepeatCnt.value > 0) {
    ElNotification.success({
      title: '系统通知',
      message: '检测到重复文件' + uploadFileRepeatCnt.value + '个，已自动过滤！',
      duration: 5000
    });
    uploadFileRepeatCnt.value = 0;
  }
  // 如果没有会话，则创建会话，并推送至url
  if (!currentSession?.id) {
    await createNewSession();
  }
  // 3. 初始化会话资源文件夹并获取到资源文件夹id
  show_upload_manage_box.value = true;
  let initRes = await attachment_base_init({
    session_id: currentSession.id
  });
  if (initRes.error_status) {
    return false;
  }
  let resourceParentId = initRes.result.id;
  upload_file_task_list.value.push(<ResourceUploadItem>{
    id: null,
    resource_parent_id: resourceParentId,
    resource_id: null,
    resource_name: uploadFile.name,
    resource_size_in_mb: resourceSize,
    resource_type: resourceType,
    resource_format: resourceFormat,
    content_max_idx: contentMaxIdx,
    content_finish_idx: -1,
    resource_md5: fileSHA256,
    raw_file: uploadFile,
    task_icon: taskIcon,
    task_source: 'session',
    task_status: 'pending'
  });
}
async function uploadFileSuccess(response: any, uploadFile: UploadFile, uploadFiles: UploadFiles) {
  // 上传成功后，添加附件与会话消息
  let fileResource = response.result as ResourceUploadItem;
  let resourceId = response.result?.resource_id;
  if (!resourceId) {
    return;
  }
  let params = {
    session_id: currentSession.id,
    resource_id: resourceId,
    attachment_source: 'files'
  };
  attachment_add_into_session(params);
  // 找到预处理阶段保存的并更新resource_id
  for (let resource of uploadFileResourceList.value) {
    if (uploadFile.raw.uid == resource.id) {
      resource.id = fileResource.resource_id;
    }
  }
  // 判断是否全部任务完成，完成则关闭上传管理框
  let finishFlag = true;
  for (let i = 0; i < upload_file_task_list.value.length; i++) {
    if (
      upload_file_task_list.value[i].task_status == 'pending' ||
      upload_file_task_list.value[i].task_status == 'uploading'
    ) {
      finishFlag = false;
      break;
    }
  }
  if (finishFlag) {
    close_upload_manager();
    if (router.currentRoute.value.name === 'next_console_welcome_home') {
      await router.push({
        name: 'message_flow',
        params: { session_code: currentSession.session_code },
        query: { ...router.currentRoute.value.query, auto_ask: 'false' } // 保持既有参数
      });
      await nextTick();
    }
  }
}
async function switchOnResourceSearch() {
  // 打开文档问答配置区域
  showConsoleInnerHead.value = true;
  consoleInnerType.value = 'ai_resource';
  currentSession.session_local_resource_switch = true;
  // 获取对应文件资源明细
  if (currentSession.session_local_resource_use_all) {
    sessionResourcesList.value = [
      //@ts-ignore
      {
        resource_id: -1,
        resource_icon: 'all_resource.svg',
        resource_name: '全部资源'
      } as ResourceItem
    ];
    return;
  }
  if (sessionResourcesList.value?.length > 0) {
    if (!currentSession?.id) {
      return;
    }
    // 更新至后端
    update_session({
      session_id: currentSession.id,
      session_local_resource_switch: true
    });
    let params = {
      session_id: currentSession.id,
      attachment_source: 'resources'
    };
    let res = await attachment_get_detail(params);
    if (!res.error_status) {
      sessionResourcesList.value = res.result;
    }
  } else {
    resourceSearchDialogShow.value = true;
  }
}
async function switchOffResourceSearch() {
  currentSession.session_local_resource_switch = false;
  hideAiResourceConfigArea();
  if (!currentSession?.id) {
    return;
  }
  update_session({
    session_id: currentSession.id,
    session_local_resource_switch: false
  });
}
async function hideAiResourceConfigArea() {
  showConsoleInnerHead.value = false;
  await nextTick(() => {
    if (window.innerWidth >= 768) {
      consoleInputRef.value.focus();
    }
  });
  if (!sessionResourcesList.value.length) {
    currentSession.session_local_resource_switch = false;
    if (!currentSession?.id) {
      return;
    }
    update_session({
      session_id: currentSession.id,
      session_local_resource_switch: false
    });
  }
}
async function cleanResourceList() {
  sessionResourcesList.value = [
    //@ts-ignore
    {
      resource_id: -1,
      resource_icon: 'all_resource.svg',
      resource_name: '全部资源'
    } as ResourceItem
  ];
  currentSession.session_local_resource_switch = true;
  currentSession.session_local_resource_use_all = true;
  if (!currentSession?.id) {
    return;
  }
  // 同步到后端
  attachment_remove_from_session({
    session_id: currentSession.id,
    clean_all: true,
    attachment_source: 'resources'
  });
  update_session({
    session_id: currentSession.id,
    session_local_resource_switch: true,
    session_local_resource_use_all: true
  });
}
async function removeResourceItem(resource: ResourceItem) {
  // 删除资源
  const indexToRemove = sessionResourcesList.value.findIndex(item => item.id === resource.id);
  if (indexToRemove !== -1) {
    sessionResourcesList.value.splice(indexToRemove, 1);
  }
  if (!currentSession?.id) {
    return;
  }
  // 同步到后端
  attachment_remove_from_session({
    session_id: currentSession.id,
    resource_list: [resource.id]
  });
}
async function commitAddChooseResources() {
  const res = resourcesSearchRef.value?.getSelectedResources();
  if (!res?.length) {
    return;
  }
  sessionResourcesList.value = res;
  resourceSearchDialogShow.value = false;
  currentSession.session_local_resource_switch = true;
  currentSession.session_local_resource_use_all = false;
  if (!currentSession?.id) {
    await createNewSession();
  }
  update_session({
    session_id: currentSession.id,
    session_local_resource_switch: true,
    session_local_resource_use_all: false
  });
  let params = {
    session_id: currentSession.id,
    resource_list: []
  };
  if (!currentSession.session_local_resource_use_all && sessionResourcesList.value) {
    for (let resource of sessionResourcesList.value) {
      params.resource_list.push(resource.id);
    }
    await attachment_add_resources_into_session(params);
  }
  resourceSearchDialogShow.value = false;
  await router.push({
    name: 'message_flow',
    params: { session_code: currentSession.session_code },
    query: { ...router.currentRoute.value.query, auto_ask: 'true' } // 保持既有参数
  });
  await nextTick();
}
async function toLLMConfigArea() {
  router.push({ name: 'next_console_user_info', query: { tab: 'setting' } });
}
onMounted(async () => {
  if (window.innerWidth >= 768) {
    userInputRef.value.focus();
  }
  consoleHeight.value = props.height;
  // 获取模型列表
  searchLlmInstance();
  // 增加copy时间监听
  window.addEventListener('paste', handleUserPaste);
});
onUnmounted(() => {
  window.removeEventListener('paste', handleUserPaste);
});
watch(
  () => props.sessionCode,
  async newVal => {
    if (newVal && newVal != currentSession?.session_code) {
      await initCurrentSession(newVal);
    }
  },
  { immediate: true }
);
watch(
  () => props.height,
  newVal => {
    consoleHeight.value = newVal;
  }
);
defineExpose({
  clickRecommendQuestion,
  handleAsr,
  switchOnAiSearch,
  updateSessionAttachment,
  switchOnResourceSearch,
  askQuestion
});
</script>

<template>
  <div
    id="console-input"
    :style="{ height: consoleHeight }"
    @dragover.prevent="handleDragOver"
    @drop.prevent="handleDrop"
  >
    <div id="console-input-box" ref="consoleInputRef">
      <div v-show="!showConsoleInnerHead" id="console-input-buttons">
        <div
          class="console-button"
          :class="{ 'console-button-active': currentSession.session_search_engine_switch }"
          @click="switchOnAiSearch()"
        >
          <div class="std-middle-box">
            <el-image
              v-show="!currentSession.session_search_engine_switch"
              src="/images/ai_search_logo.svg"
              class="console-button-icon"
            />
            <el-image
              v-show="currentSession.session_search_engine_switch"
              src="/images/ai_search_logo_active.svg"
              class="console-button-icon"
            />
          </div>
          <div class="std-middle-box">
            <el-text
              class="console-button-text"
              :class="{ 'console-button-text-active': currentSession.session_search_engine_switch }"
            >
              AI 搜索
            </el-text>
          </div>
        </div>
        <div
          class="console-button"
          :class="{ 'console-button-active': currentSession.session_attachment_webpage_switch }"
          @click="switchOnWebpageSearch()"
        >
          <div class="std-middle-box">
            <el-image
              v-show="!currentSession.session_attachment_webpage_switch"
              src="/images/webpage_search_logo.svg"
              class="console-button-icon"
            />
            <el-image
              v-show="currentSession.session_attachment_webpage_switch"
              src="/images/webpage_search_logo_active.svg"
              class="console-button-icon"
            />
          </div>
          <div class="std-middle-box">
            <el-text
              class="console-button-text"
              :class="{ 'console-button-text-active': currentSession.session_attachment_webpage_switch }"
            >
              网页问答
            </el-text>
          </div>
          <div
            v-if="uploadWebpageResourceList?.length"
            class="std-middle-box"
            style="border-radius: 3px; padding: 0 4px"
            :style="{ backgroundColor: currentSession.session_attachment_webpage_switch ? '#D1E9FF' : '' }"
          >
            <el-text
              style="font-weight: 500; font-size: 12px; line-height: 18px; color: #344054"
              :style="{ color: currentSession.session_attachment_webpage_switch ? '#175CD3' : '' }"
            >
              {{ uploadWebpageResourceList?.length }}
            </el-text>
          </div>
        </div>
        <el-upload
          ref="uploadImgRef"
          v-model:file-list="uploadImgList"
          action=""
          :show-file-list="false"
          :auto-upload="true"
          :disabled="uploadImgResourceList?.length > 0"
          multiple
          name="chunk_content"
          accept="image/*"
          :on-change="handleImageFileChange"
          :before-upload="prepareUploadImage"
          :http-request="upload_file_content"
          :on-success="uploadImgSuccess"
          @click="switchOnImgSearch()"
        >
          <div
            class="console-button"
            :class="{ 'console-button-active': currentSession.session_attachment_image_switch }"
          >
            <div class="std-middle-box">
              <el-image
                v-show="!currentSession.session_attachment_image_switch"
                src="/images/picture_search_logo.svg"
                class="console-button-icon"
              />
              <el-image
                v-show="currentSession.session_attachment_image_switch"
                src="/images/picture_search_logo_active.svg"
                class="console-button-icon"
              />
            </div>
            <div class="std-middle-box">
              <el-text
                class="console-button-text"
                :class="{ 'console-button-text-active': currentSession.session_attachment_image_switch }"
              >
                图像问答
              </el-text>
            </div>
            <div
              v-if="uploadImgResourceList?.length"
              class="std-middle-box"
              style="border-radius: 3px; margin-left: 4px"
              :style="{ backgroundColor: currentSession.session_attachment_image_switch ? '#EFF8FF' : '' }"
            >
              <el-text
                style="font-weight: 500; font-size: 12px; line-height: 12px; color: #344054"
                :style="{ color: currentSession.session_attachment_image_switch ? '#175CD3' : '' }"
              >
                {{ uploadImgResourceList?.length }}
              </el-text>
            </div>
          </div>
        </el-upload>
        <el-upload
          ref="uploadFileRef"
          v-model:file-list="uploadFileList"
          action=""
          :show-file-list="false"
          :auto-upload="true"
          :disabled="uploadFileResourceList?.length > 0"
          multiple
          name="chunk_content"
          accept="*"
          :on-change="handleFileChange"
          :before-upload="prepareUploadFile"
          :http-request="upload_file_content"
          :on-success="uploadFileSuccess"
          @click.prevent="switchOnFileSearch()"
        >
          <div
            class="console-button"
            :class="{ 'console-button-active': currentSession.session_attachment_file_switch }"
          >
            <div class="std-middle-box">
              <el-image
                v-show="!currentSession.session_attachment_file_switch"
                src="/images/tmp_doc_search_logo.svg"
                class="console-button-icon"
              />
              <el-image
                v-show="currentSession.session_attachment_file_switch"
                src="/images/tmp_doc_search_logo_active.svg"
                class="console-button-icon"
              />
            </div>
            <div class="std-middle-box">
              <el-text
                class="console-button-text"
                :class="{ 'console-button-text-active': currentSession.session_attachment_file_switch }"
              >
                文档问答
              </el-text>
            </div>
            <div
              v-show="uploadFileResourceList?.length"
              class="std-middle-box"
              style="border-radius: 3px; margin-left: 4px"
              :style="{ backgroundColor: currentSession.session_attachment_file_switch ? '#EFF8FF' : '' }"
            >
              <el-text
                style="font-weight: 500; font-size: 12px; line-height: 12px; color: #344054"
                :style="{ color: currentSession.session_attachment_file_switch ? '#175CD3' : '' }"
              >
                {{ uploadFileResourceList?.length }}
              </el-text>
            </div>
          </div>
        </el-upload>
        <div
          class="console-button"
          :class="{ 'console-button-active': currentSession.session_local_resource_switch }"
          @click="switchOnResourceSearch()"
        >
          <div class="std-middle-box">
            <el-image
              v-show="!currentSession.session_local_resource_switch"
              src="/images/kg_search_logo.svg"
              class="console-button-icon"
            />
            <el-image
              v-show="currentSession.session_local_resource_switch"
              src="/images/kg_search_logo_active.svg"
              class="console-button-icon"
            />
          </div>
          <div class="std-middle-box">
            <el-text
              class="console-button-text"
              :class="{ 'console-button-text-active': currentSession.session_local_resource_switch }"
            >
              知识库问答
            </el-text>
          </div>
          <div
            v-if="sessionResourcesList?.length"
            class="std-middle-box"
            style="border-radius: 3px; margin-left: 4px"
            :style="{ backgroundColor: currentSession.session_local_resource_switch ? '#EFF8FF' : '' }"
          >
            <el-text
              v-if="currentSession.session_local_resource_use_all"
              style="font-weight: 500; font-size: 12px; line-height: 12px; color: #344054"
              :style="{ color: currentSession.session_local_resource_switch ? '#175CD3' : '' }"
            >
              *
            </el-text>
            <el-text
              v-else
              style="font-weight: 500; font-size: 12px; line-height: 18px; color: #344054"
              :style="{ color: currentSession.session_local_resource_switch ? '#175CD3' : '' }"
            >
              {{ sessionResourcesList?.length }}
            </el-text>
          </div>
        </div>
      </div>
      <div id="console-input-box-inner">
        <div v-show="showConsoleInnerHead" id="console-input-box-inner-head">
          <div v-show="consoleInnerType == 'ai_search'" id="ai_search">
            <div id="ai_search_head">
              <div id="ai_search_head_left">
                <div class="std-middle-box">
                  <el-image src="/images/ai_search_logo.svg" class="rag-icon" />
                </div>
                <div class="std-middle-box">
                  <el-text class="console-button-text2">AI搜索</el-text>
                </div>
              </div>
              <div id="ai_search_head_right">
                <div class="std-middle-box">
                  <el-switch
                    v-model="searchEngineLanguageEn"
                    active-text="英文检索"
                    @change="switchAiSearchLanguage()"
                  />
                </div>
                <el-tooltip v-if="!simpleVis" effect="light" placement="top">
                  <template #default>
                    <div class="std-middle-box">
                      <el-image src="/images/tooltip.svg" style="width: 16px; height: 16px" />
                    </div>
                  </template>
                  <template #content>
                    <el-text> 自动翻译成英文并检索英文资源 </el-text>
                  </template>
                </el-tooltip>
                <el-divider direction="vertical" />
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="hideAiSearchConfigArea()">
                    <el-image src="/images/minimize.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 隐藏配置区域 </el-text>
                  </template>
                </el-tooltip>
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="switchOffAiSearch()">
                    <el-image src="/images/switch_off.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 退出AI搜索 </el-text>
                  </template>
                </el-tooltip>
              </div>
            </div>
          </div>
          <div v-show="consoleInnerType == 'ai_webpage'" id="ai_webpage">
            <div id="ai_search_head">
              <div id="ai_search_head_left">
                <div class="std-middle-box">
                  <el-image src="/images/ai_webpage_logo.svg" class="rag-icon" />
                </div>
                <div class="std-middle-box">
                  <el-text class="console-button-text2">网页问答</el-text>
                </div>
              </div>
              <div id="ai_images_head_middle" style="cursor: pointer" @click="uploadWebpageDialogVisible = true">
                <div class="std-middle-box" style="gap: 8px">
                  <div class="std-middle-box">
                    <el-image src="/images/add_blue.svg" class="rag-icon" />
                  </div>
                  <div class="std-middle-box">
                    <el-text style="color: #175cd3">添加网页</el-text>
                  </div>
                </div>
              </div>
              <div id="ai_image_head_right">
                <el-tooltip v-if="!simpleVis" effect="light" placement="top">
                  <template #default>
                    <div class="std-middle-box">
                      <el-image src="/images/tooltip.svg" class="rag-icon" />
                    </div>
                  </template>
                  <template #content>
                    <el-text> 获取到的网页内容会在每个提问中从中检索有效信息，并整个会话中保持记忆 </el-text>
                  </template>
                </el-tooltip>
                <el-divider direction="vertical" />
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="hideAiWebpageConfigArea()">
                    <el-image src="/images/minimize.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 隐藏配置区域 </el-text>
                  </template>
                </el-tooltip>
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="switchOffWebpageSearch()">
                    <el-image src="/images/switch_off.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 退出网页问答 </el-text>
                  </template>
                </el-tooltip>
              </div>
            </div>
            <div id="ai_image_body">
              <el-scrollbar style="width: calc(100%)">
                <div id="ai_file_body_left">
                  <div id="ai_file_body_left_bg">
                    <div v-for="(item, idx) in uploadWebpageResourceList" :key="idx" class="ai_file_item">
                      <el-tooltip v-if="item?.resource_is_supported === true" placement="top" effect="light">
                        <template #default>
                          <el-image src="/images/support_attachment.svg" style="width: 16px; height: 16px" />
                        </template>
                        <template #content>
                          <el-text> 网页解析完成 </el-text>
                        </template>
                      </el-tooltip>
                      <el-tooltip v-else-if="item?.resource_is_supported === false" placement="top" effect="light">
                        <template #default>
                          <el-image src="/images/unsupported_attachment.svg" style="width: 16px; height: 16px" />
                        </template>
                        <template #content>
                          <el-text>
                            {{ item?.resource_desc || '此网页解析失败！' }}
                          </el-text>
                        </template>
                      </el-tooltip>
                      <el-tooltip v-else placement="top" effect="light">
                        <template #default>
                          <el-image src="/images/building_attachment.svg" style="width: 16px; height: 16px" />
                        </template>
                        <template #content>
                          <el-text> 此网页解析中... </el-text>
                        </template>
                      </el-tooltip>
                      <el-image :src="getResourceIcon(item)" style="width: 20px; height: 20px">
                        <template #error>
                          <el-icon>
                            <IconPicture />
                          </el-icon>
                        </template>
                      </el-image>
                      <el-text style="max-width: 120px" truncated>
                        {{ item?.resource_name }}
                      </el-text>

                      <el-image
                        src="/images/remove_img.svg"
                        style="width: 16px; height: 16px; cursor: pointer"
                        @click="removeWebpageItem(idx)"
                      />
                    </div>
                  </div>
                </div>
              </el-scrollbar>
              <div id="ai_image_body_right">
                <el-button text type="primary" @click="cleanTmpWebpageList()"> 重置 </el-button>
              </div>
            </div>
          </div>
          <div v-show="consoleInnerType == 'ai_image'" id="ai_image">
            <div id="ai_search_head">
              <div id="ai_search_head_left">
                <div class="std-middle-box">
                  <el-image src="/images/ai_image_logo.svg" class="rag-icon" />
                </div>
                <div class="std-middle-box">
                  <el-text class="console-button-text2">图像问答</el-text>
                </div>
              </div>
              <div id="ai_images_head_middle">
                <el-upload
                  ref="uploadImgRef"
                  v-model:file-list="uploadImgList"
                  action=""
                  :show-file-list="false"
                  :auto-upload="true"
                  :disabled="uploadImgResourceList?.length > 0 && !showConsoleInnerHead"
                  multiple
                  name="chunk_content"
                  accept="image/*"
                  :on-change="handleImageFileChange"
                  :before-upload="prepareUploadImage"
                  :http-request="upload_file_content"
                  :on-success="uploadImgSuccess"
                  @click="switchOnImgSearch()"
                >
                  <div class="std-middle-box" style="gap: 8px">
                    <div class="std-middle-box">
                      <el-image src="/images/add_blue.svg" class="rag-icon" />
                    </div>
                    <div class="std-middle-box">
                      <el-text style="color: #175cd3">添加图像</el-text>
                    </div>
                  </div>
                </el-upload>
              </div>
              <div id="ai_image_head_right">
                <el-tooltip v-if="!simpleVis" effect="light" placement="top">
                  <template #default>
                    <div class="std-middle-box">
                      <el-image src="/images/tooltip.svg" class="rag-icon" />
                    </div>
                  </template>
                  <template #content>
                    <el-text> 图片上传后会通过视觉模型识别，并整个会话中保持记忆 </el-text>
                  </template>
                </el-tooltip>
                <el-divider direction="vertical" />
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="hideAiImageConfigArea()">
                    <el-image src="/images/minimize.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 隐藏配置区域 </el-text>
                  </template>
                </el-tooltip>
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="switchOffImageSearch()">
                    <el-image src="/images/switch_off.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 退出图像问答 </el-text>
                  </template>
                </el-tooltip>
              </div>
            </div>
            <div id="ai_image_body">
              <el-scrollbar style="width: 100%">
                <div id="ai_image_body_left">
                  <div id="ai_image_body_left_bg">
                    <div v-for="(item, idx) in uploadImgResourceList" :key="idx" class="ai_image_item">
                      <el-tooltip v-if="item?.resource_is_supported" placement="top" effect="light">
                        <template #default>
                          <el-image src="/images/support_attachment.svg" style="width: 16px; height: 16px" />
                        </template>
                        <template #content>
                          <el-text> 图片解析成功 </el-text>
                        </template>
                      </el-tooltip>
                      <el-tooltip v-else placement="top" effect="light">
                        <template #default>
                          <el-image src="/images/unsupported_attachment.svg" style="width: 16px; height: 16px" />
                        </template>
                        <template #content>
                          <el-text> 图片解析失败 </el-text>
                        </template>
                      </el-tooltip>

                      <el-image
                        :src="item?.resource_show_url"
                        style="width: 20px; height: 20px"
                        :zoom-rate="1.2"
                        :max-scale="7"
                        :min-scale="0.2"
                        :preview-src-list="attachmentImagesViewList"
                        :initial-index="idx"
                        fit="cover"
                      >
                        <template #error>
                          <el-icon>
                            <IconPicture />
                          </el-icon>
                        </template>
                      </el-image>

                      <el-image
                        src="/images/remove_img.svg"
                        style="width: 16px; height: 16px; cursor: pointer"
                        @click="removeImgItem(idx)"
                      />
                    </div>
                  </div>
                </div>
              </el-scrollbar>
              <div id="ai_image_body_right">
                <el-button text type="primary" @click="cleanTmpImgList()"> 重置 </el-button>
              </div>
            </div>
          </div>
          <div v-show="consoleInnerType == 'ai_file'" id="ai_file">
            <div id="ai_search_head">
              <div id="ai_search_head_left">
                <div class="std-middle-box">
                  <el-image src="/images/ai_file_logo.svg" class="rag-icon" />
                </div>
                <div class="std-middle-box">
                  <el-text class="console-button-text2">文档问答</el-text>
                </div>
              </div>
              <div id="ai_images_head_middle">
                <el-upload
                  ref="uploadFileRef"
                  v-model:file-list="uploadFileList"
                  action=""
                  :show-file-list="false"
                  :auto-upload="true"
                  :disabled="uploadFileResourceList?.length > 0 && !showConsoleInnerHead"
                  multiple
                  name="chunk_content"
                  accept="*"
                  :on-change="handleFileChange"
                  :before-upload="prepareUploadFile"
                  :http-request="upload_file_content"
                  :on-success="uploadFileSuccess"
                  @click="switchOnFileSearch()"
                >
                  <div class="std-middle-box" style="gap: 8px">
                    <div class="std-middle-box">
                      <el-image src="/images/add_blue.svg" class="rag-icon" />
                    </div>
                    <div class="std-middle-box">
                      <el-text style="color: #175cd3">添加文档</el-text>
                    </div>
                  </div>
                </el-upload>
              </div>
              <div id="ai_image_head_right">
                <el-tooltip v-if="!simpleVis" effect="light" placement="top">
                  <template #default>
                    <div class="std-middle-box">
                      <el-image src="/images/tooltip.svg" class="rag-icon" />
                    </div>
                  </template>
                  <template #content>
                    <el-text> 文档上传后会在每个提问中从中检索有效信息，并整个会话中保持记忆 </el-text>
                  </template>
                </el-tooltip>
                <el-divider direction="vertical" />
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="hideAiFileConfigArea()">
                    <el-image src="/images/minimize.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 隐藏配置区域 </el-text>
                  </template>
                </el-tooltip>
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="switchOffFileSearch()">
                    <el-image src="/images/switch_off.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 退出文档问答 </el-text>
                  </template>
                </el-tooltip>
              </div>
            </div>
            <div id="ai_image_body">
              <el-scrollbar style="width: calc(100%)">
                <div id="ai_file_body_left">
                  <div id="ai_file_body_left_bg">
                    <div v-for="(item, idx) in uploadFileResourceList" :key="idx" class="ai_file_item">
                      <el-tooltip v-if="item?.resource_is_supported === true" placement="top" effect="light">
                        <template #default>
                          <el-image src="/images/support_attachment.svg" style="width: 16px; height: 16px" />
                        </template>
                        <template #content>
                          <el-text> 文档解析完成 </el-text>
                        </template>
                      </el-tooltip>
                      <el-tooltip v-else-if="item?.resource_is_supported === false" placement="top" effect="light">
                        <template #default>
                          <el-image src="/images/unsupported_attachment.svg" style="width: 16px; height: 16px" />
                        </template>
                        <template #content>
                          <el-text> 文档解析失败！ </el-text>
                        </template>
                      </el-tooltip>
                      <el-tooltip v-else placement="top" effect="light">
                        <template #default>
                          <el-image src="/images/building_attachment.svg" style="width: 16px; height: 16px" />
                        </template>
                        <template #content>
                          <el-text> 文档解析中... </el-text>
                        </template>
                      </el-tooltip>
                      <el-image :src="getResourceIcon(item)" style="width: 20px; height: 20px">
                        <template #error>
                          <el-icon>
                            <IconPicture />
                          </el-icon>
                        </template>
                      </el-image>
                      <el-text style="max-width: 120px" truncated>
                        {{ item?.resource_name }}
                      </el-text>

                      <el-image
                        src="/images/remove_img.svg"
                        style="width: 16px; height: 16px; cursor: pointer"
                        @click="removeFileItem(idx)"
                      />
                    </div>
                  </div>
                </div>
              </el-scrollbar>
              <div id="ai_image_body_right">
                <el-button text type="primary" @click="cleanTmpFileList()"> 重置 </el-button>
              </div>
            </div>
          </div>
          <div v-show="consoleInnerType == 'ai_resource'" id="ai_resource">
            <div id="ai_search_head">
              <div id="ai_search_head_left">
                <div class="std-middle-box">
                  <el-image src="/images/ai_resource_logo.svg" class="rag-icon" />
                </div>
                <div class="std-middle-box">
                  <el-text class="console-button-text2">知识库问答</el-text>
                </div>
              </div>
              <div id="ai_images_head_middle" style="cursor: pointer" @click="resourceSearchDialogShow = true">
                <div class="std-middle-box" style="gap: 8px">
                  <div class="std-middle-box">
                    <el-image src="/images/search_blue.svg" class="rag-icon" />
                  </div>
                  <div class="std-middle-box">
                    <el-text style="color: #175cd3">搜索添加资源</el-text>
                  </div>
                </div>
              </div>
              <div id="ai_image_head_right">
                <el-tooltip v-if="!simpleVis" effect="light" placement="top">
                  <template #default>
                    <div class="std-middle-box">
                      <el-image src="/images/tooltip.svg" class="rag-icon" />
                    </div>
                  </template>
                  <template #content>
                    <el-text> 会自动从资源库中检索相关知识，并在整个会话中保持记忆 </el-text>
                  </template>
                </el-tooltip>
                <el-divider direction="vertical" />
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="hideAiResourceConfigArea()">
                    <el-image src="/images/minimize.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 隐藏配置区域 </el-text>
                  </template>
                </el-tooltip>
                <el-tooltip effect="light" placement="top">
                  <div class="std-middle-box" style="cursor: pointer" @click="switchOffResourceSearch()">
                    <el-image src="/images/switch_off.svg" class="rag-icon" />
                  </div>
                  <template #content>
                    <el-text> 退出知识库问答 </el-text>
                  </template>
                </el-tooltip>
              </div>
            </div>
            <div id="ai_image_body">
              <el-scrollbar style="width: calc(100%)">
                <div id="ai_file_body_left">
                  <div id="ai_file_body_left_bg">
                    <div v-for="(item, idx) in sessionResourcesList" :key="idx" class="ai_file_item">
                      <el-tooltip placement="top" effect="light">
                        <template #default>
                          <el-image src="/images/support_attachment.svg" style="width: 16px; height: 16px" />
                        </template>
                        <template #content>
                          <el-text> 资源解析完成 </el-text>
                        </template>
                      </el-tooltip>
                      <el-image :src="getResourceIcon(item)" style="width: 20px; height: 20px">
                        <template #error>
                          <el-icon>
                            <IconPicture />
                          </el-icon>
                        </template>
                      </el-image>
                      <el-text style="max-width: 120px" truncated>
                        {{ item?.resource_name }}
                      </el-text>
                      <el-image
                        src="/images/remove_img.svg"
                        style="width: 16px; height: 16px; cursor: pointer"
                        @click="removeResourceItem(item)"
                      />
                    </div>
                  </div>
                </div>
              </el-scrollbar>
              <div id="ai_image_body_right">
                <el-button text type="primary" @click="cleanResourceList()"> 重置 </el-button>
              </div>
            </div>
          </div>
        </div>
        <div id="console-input-box-inner-body">
          <div id="input-text-box">
            <el-input
              ref="userInputRef"
              v-model="userInput"
              placeholder="请输入您想咨询的问题"
              type="textarea"
              input-style="box-shadow: none; border-radius: 8px; border: none;"
              class="msg-input-textarea"
              resize="none"
              :autosize="{ minRows: 2, maxRows: 5 }"
              @keydown.enter.prevent
              @keydown="handleKeyDown"
              @compositionend="userComposition = false"
              @compositionstart="userComposition = true"
              @input="handleInputChange"
            />
          </div>

          <div v-show="userBatchSize == 1" class="input-button" style="background-color: red" @click="stopQuestion()">
            <el-image src="/images/pause_white.svg" class="input-icon" />
          </div>
          <el-popover rigger="hover" width="300px">
            <template #reference>
              <el-badge v-show="userBatchSize > 1" :value="userBatchSize">
                <div class="input-button" style="background-color: red">
                  <el-image src="/images/pause_white.svg" class="input-icon" />
                </div>
              </el-badge>
            </template>
            <div
              v-for="(running_question, idx) in runningQuestions"
              :key="running_question.qa_item_idx"
              class="running_question_item_box"
            >
              <div class="running-question-idx-box">
                <el-text truncated> 第{{ idx + 1 }}个问题 </el-text>
              </div>
              <div class="running-question-stop-button">
                <el-image src="/images/close_red.svg" @click="stopQuestion(running_question)" />
              </div>
            </div>
          </el-popover>
          <div v-show="!userBatchSize" class="input-button" @click="askQuestion('icon')">
            <el-image src="/images/send_blue.svg" class="input-icon" />
          </div>
          <div
            class="input-button"
            @mousedown.prevent="startRecording(1)"
            @mouseup="stopRecording(2)"
            @touchstart.prevent="startRecording(3)"
            @touchend="stopRecording(4)"
          >
            <div v-show="isRecording" class="recording-box">
              <div class="wave" />
              <div class="wave" />
              <div class="wave" />
            </div>
            <el-tooltip content="语音输入" placement="top">
              <el-icon class="input-icon">
                <Microphone v-show="!isRecording" class="input-icon" />
                <VideoPause v-show="isRecording" class="input-icon" style="color: #c45656" />
              </el-icon>
            </el-tooltip>
          </div>
        </div>
      </div>
    </div>
    <div id="input-tips">
      <div class="std-middle-box">
        <el-text class="msg-tips-text"> 以上内容均由AI生成式模型 </el-text>
        <el-text class="msg-tips-text">
          {{ getSessionLlmName() || 'DeepSeek-V3' }}
        </el-text>
        <el-popover ref="modelListRef" trigger="click" width="280px">
          <template #reference>
            <div class="std-middle-box">
              <el-image src="/images/arrow_down_grey.svg" class="model-select-icon" />
            </div>
          </template>
          <el-scrollbar>
            <div class="llm-instance-area">
              <div
                v-for="(item, idx) in llmInstanceQueue"
                :key="idx"
                class="llm-instance-item"
                :class="{
                  'llm-instance-item-active': item.llm_code == currentSession?.session_llm_code
                }"
                @click="switchLlmInstance(item)"
              >
                <div class="std-middle-box">
                  <el-avatar
                    :src="item.llm_icon"
                    style="width: 20px; height: 20px; background-color: white"
                    fit="contain"
                  />
                </div>
                <div class="std-middle-box" style="justify-content: flex-start">
                  <el-text truncated style="font-size: 14px; font-weight: 500; line-height: 20px; color: #344054">
                    {{ item.llm_label }}
                  </el-text>
                </div>
              </div>
              <el-button :icon="TopRight" @click="toLLMConfigArea">前往配置 </el-button>
            </div>
          </el-scrollbar>
        </el-popover>
        <el-text class="msg-tips-text"> 生成，仅供参考 </el-text>
      </div>
    </div>
  </div>
  <div id="upload-box">
    <ResourceUploadManager />
  </div>
  <el-dialog
    ref="uploadWebpageDialogRef"
    v-model="uploadWebpageDialogVisible"
    title="目标网页"
    :draggable="true"
    :modal="true"
    style="max-width: 500px"
    :width="urlDialogWidth"
  >
    <el-scrollbar>
      <el-form
        ref="uploadWebpageNewResourceFormRef"
        style="max-height: 500px; margin-right: 24px"
        :model="uploadWebpageNewResources"
      >
        <el-form-item
          v-for="(item, idx) in uploadWebpageNewResources.new_urls"
          :key="idx"
          label="URL"
          label-position="top"
          :prop="'new_urls.' + idx + '.resource_source_url'"
          :rules="[
            { required: true, message: '请输入目标网页URL', trigger: 'blur' },
            { type: 'url', message: '请输入正确的URL', trigger: 'blur' },
            { validator: validateUrlRepeat, trigger: 'blur' }
          ]"
        >
          <el-input
            v-model="item.resource_source_url"
            placeholder="请输入目标网页URL"
            @change="item.resource_source_url = item.resource_source_url.trim()"
          >
            <template #append>
              <el-button style="display: flex; flex-direction: row; gap: 6px" @click="removeNewWebpageResource(idx)">
                <el-tooltip effect="light" placement="right">
                  <template #content>
                    <el-text> 删除此URL </el-text>
                  </template>
                  <el-image src="/images/delete_url.svg" style="width: 20px; height: 20px" />
                </el-tooltip>
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-divider>
            <el-button type="primary" @click="addNewWebpageResource()"> 添加新的URL </el-button>
          </el-divider>
        </el-form-item>
        <el-form-item>
          <div class="std-middle-box" style="width: 100%">
            <el-button style="width: 100%" @click="switchOffNewWebpage()">取消</el-button>
            <el-button style="width: 100%" type="primary" @click="commitAddNewWebpages()">确定</el-button>
          </div>
        </el-form-item>
      </el-form>
      <div />
    </el-scrollbar>
  </el-dialog>
  <ResourcesSearch
    ref="resourcesSearchRef"
    :model="resourceSearchDialogShow"
    :session-resources="sessionResourcesList"
    @close="resourceSearchDialogShow = false"
    @commit="
      args => {
        commitAddChooseResources();
      }
    "
  />
</template>

<style scoped>
.msg-input-textarea :deep(.el-textarea__inner::-webkit-scrollbar) {
  width: 4px;
  height: 6px;
}

.msg-input-textarea :deep(.el-textarea__inner::-webkit-scrollbar-thumb) {
  border-radius: 3px;
  -moz-border-radius: 3px;
  -webkit-border-radius: 3px;
  background-color: #c3c3c3;
}

.msg-input-textarea :deep(.el-textarea__inner::-webkit-scrollbar-track) {
  background-color: transparent;
}

#console-input {
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
  align-items: center;
  width: 100%;
  position: relative;
}

#console-input-box {
  width: 100%;
  max-width: 900px;
  display: flex;
  flex-direction: row;
  gap: 4px;
  box-shadow: 0 1px 2px 0 #1018280d;
  border-radius: 24px;
  padding: 4px;
  background-color: #f3f4f6;
  position: relative;
}

#console-input-box-inner {
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  border: 1px solid #d0d5dd;
  background-color: white;
  box-shadow: 0 1px 2px 0 #1018280d;
  gap: 4px;
  width: 100%;
  align-items: center;
}

#console-input-box-inner-body {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px;
  width: calc(100% - 24px);
}

.input-button {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 4px;
}

.input-button:hover {
  background-color: #f3f4f6;
}

.input-button:active {
  transform: scale(0.95);
}

#input-text-box {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.input-icon {
  width: 24px;
  height: 24px;
}

.msg-tips-text {
  font-size: 12px;
  line-height: 18px;
  font-weight: 400;
  color: #475467;
}

.running_question_item_box {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-bottom: 1px solid #d0d5dd;
}

.running-question-idx-box {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  background-color: #f3f4f6;
  padding: 4px;
}

.running-question-word-cnt-box {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  background-color: #f3f4f6;
  padding: 4px;
}

.running-question-stop-button {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 4px;
  background-color: #f3f4f6;
  padding: 4px;
  width: 24px;
  height: 24px;
}

.running-question-stop-button:hover {
  background-color: #f3f4f6;
}

.running-question-stop-button:active {
  transform: scale(0.95);
}

#input-tips {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 8px;
  border-radius: 8px;
  gap: 4px;
  height: 20px;
}

.std-middle-box {
  display: flex;
  justify-content: center;
  align-items: center;
}

#console-input-buttons {
  position: absolute;
  left: 20px;
  top: -30px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
}

.console-button-icon {
  width: 12px;
  height: 12px;
}

.console-button-text {
  font-weight: 500;
  font-size: 12px;
  line-height: 18px;
  color: #344054;
}

.console-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: #ffffff;
  gap: 4px;
  border: 1px solid #d0d5dd;
}

.console-button:hover {
  background-color: #eff8ff;
  border: 1px solid #2e90fa;
  cursor: pointer;
}

#console-input-box-inner-head {
  width: 100%;
}

#ai_search {
  display: flex;
  flex-direction: column;
  max-height: 90px;
  width: 100%;
}

#ai_search_head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  width: calc(100% - 32px);
  height: 20px;
  background: #f5f5f4;
  border-radius: 20px 20px 0 0;
}

#ai_search_head_left {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
}

#ai_search_head_right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
}

.console-button-text2 {
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  color: #344054;
}

#ai_search_body {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 0 16px;
  padding: 8px 0;
  gap: 10px;
  border-bottom: 1px solid #d0d5dd;
}

.search-research-type {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  border-radius: 6px;
  background-color: #f9f9f9;
  cursor: pointer;
}

.search-research-type-active {
  background-color: #eff8ff;
  border: 1px solid #2e90fa;
}

.search-research-type-text {
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  color: #344054;
}

.search-research-type-text-active {
  color: #175cd3;
}

.console-button-active {
  border: none;
  background-color: #eff8ff;
}

.console-button-text-active {
  color: #175cd3;
}

#ai_image_body {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin: 0 16px;
  padding: 8px 0;
  gap: 10px;
  border-bottom: 1px solid #d0d5dd;
}

#ai_image_head_right {
  max-width: 200px;
  display: flex;
  flex-direction: row;
  gap: 8px;
}

#ai_image_body_left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}

#ai_image_body_left_bg {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  padding: 6px 8px;
  border-radius: 8px;
  background: #eff8ff;
}

.ai_image_item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 6px;
  border-radius: 6px;
  cursor: pointer;
  background: #ffffff;
  margin-bottom: 6px;
}

.llm-instance-area {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 200px;
}

.llm-instance-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  border-radius: 8px;
  padding: 6px 8px;
  margin-right: 10px;
  cursor: pointer;
  background: #ffffff;
}

.llm-instance-item:hover {
  background: #eff8ff;
}

.llm-instance-item-active {
  background: #eff8ff;
}

#upload-box {
  position: fixed;
  bottom: 250px;
  right: 380px;
  max-width: 200px;
  z-index: 99;
}

.ai_file_item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  padding: 2px 6px;
  border-radius: 6px;
  background-color: #ffffff;
  border: 1px solid #d0d5dd;
  box-shadow: 0 1px 2px 0 #1018280d;
  margin-bottom: 6px;
}

#ai_file_body_left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}

#ai_file_body_left_bg {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 4px;
  padding: 6px 8px;
  border-radius: 8px;
  background: #eff8ff;
}

.highlight-resource-keyword {
  background: yellow;
}

.msg-ticket-text {
  font-size: 12px;
  line-height: 18px;
  font-weight: 400;
  color: #475467;
  cursor: pointer;
}

.msg-ticket-text:hover {
  color: #175cd3;
}
.model-select-icon {
  width: 16px;
  height: 16px;
  cursor: pointer;
}
.rag-icon {
  width: 20px;
  height: 20px;
}
/* 录音盒子样式 */
.recording-box {
  position: absolute;
  top: -40px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  z-index: 200;
}

/* 波纹样式 */
.wave {
  position: absolute;
  width: 40px;
  height: 40px;
  border: 2px solid rgba(0, 123, 255, 0.7);
  border-radius: 50%;
  opacity: 0;
  animation: wave-animation 1.5s linear infinite;
}

/* 第二个波纹延迟动画 */
.wave:nth-child(2) {
  animation-delay: 0.5s;
}

/* 第三个波纹延迟动画 */
.wave:nth-child(3) {
  animation-delay: 1s;
}

/* 波纹动画关键帧 */
@keyframes wave-animation {
  0% {
    transform: scale(0.2);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}
@media (width < 768px) {
  .console-button-text {
    visibility: hidden;
    width: 0;
    height: 24px;
  }
  .msg-tips-text {
    font-size: 8px;
    line-height: 14px;
  }
  #console-input-buttons {
    top: -34px;
  }
  .console-button {
    gap: 0;
    padding: 2px 6px;
  }
  .rag-icon {
    width: 14px;
    height: 14px;
  }
  .console-button-text2 {
    font-size: 12px;
    line-height: 16px;
  }
  .model-select-icon {
    width: 12px;
    height: 12px;
  }
  .el-divider--vertical {
    margin: 0;
  }
  #input-tips {
    padding: 2px;
  }
  #console-input-box-inner-body {
    padding: 0;
  }
  #upload-box {
    position: fixed;
    bottom: 250px;
    left: 60px;
    max-width: 200px;
    z-index: 99;
  }
}
</style>
