<script setup lang="ts">
import {Microphone, VideoPause} from '@element-plus/icons-vue';
import {ElMessage, ElNotification, type UploadUserFile} from 'element-plus';
import {v4 as uuidv4} from 'uuid';
import {nextTick, onMounted, reactive, ref, watch} from 'vue';
import {
  add_messages2 as addMessages,
  attachment_add_resources_into_session as attachmentAddResourcesIntoSession,
  attachment_remove_from_session as attachmentRemoveFromSession,
  attachment_search_in_session as attachmentSearchInSession
} from '@/api/next_console';
import AttachmentPreview from './AttachmentPreview.vue';
import ResourceUploadManager from './ResourceUploadManager.vue';
import ResourcesSearch from './ResourcesSearch.vue';
import {running_question_meta as IRunningQuestionMeta, session_item as ISessionItem} from '@/types/next_console';
import {getInfo} from '@/utils/auth';

const userInputRef = ref();
const consoleInputRef = ref();
const userInput = ref('');
const userComposition = ref(false);
const userBatchSize = ref(0);
const runningQuestions = ref<IRunningQuestionMeta[]>([]);
const currentSession = reactive<ISessionItem>({});
const userInfo = ref();
const emit = defineEmits([
  'begin-answer',
  'update-answer',
  'finish-answer',
  'stop-answer',
  'turn-on-msg-choose-model',
  'height-change',
  'create-session'
]);
const props = defineProps({
  session: {
    type: Object,
    default: {},
    required: false
  },
  height: {
    type: String,
    default: '130px'
  },
  streaming: {
    type: Boolean,
    default: true
  },
  socket: {
    type: Object,
    default: null
  }
});
const consoleHeight = ref('180px');
const isRecording = ref(false);
interface IResourceItem {
  id?: number;
  resource_parent_id?: number;
  user_id?: number;
  resource_name?: string;
  resource_type?: string;
  resource_type_cn?: string | null;
  resource_title?: string;
  resource_desc?: string;
  resource_icon?: string;
  resource_format?: string;
  resource_size_in_MB?: number;
  resource_path?: string | null;
  resource_status?: string;
  resource_source?: string | null;
  resource_source_url?: string | null;
  resource_show_url?: string | null;
  resource_download_url?: string | null;
  resource_feature_code?: string | null;
  rag_status?: string | null;
  resource_language?: string | null;
  create_time?: string;
  update_time?: string;
  delete_time?: string | null;
  show_buttons?: boolean | null;
  resource_is_selected?: boolean | null;
  resource_parent_name?: string | null;
  sub_resource_dir_cnt?: number | null;
  sub_resource_file_cnt?: number | null;
  sub_rag_file_cnt?: number | null;
  resource_is_supported?: boolean | null;
  resource_view_support?: boolean | null;
  resource_content?: string | null;
  ref_text?: string | null;
  rerank_score?: number | null;
  resource_tags?: ResourceTag[] | null;
  author_info?: Users | null;
  access_list?: string[];
  [property: string]: any;
}
let audioContext;
let mediaStreamSource;
let scriptProcessor;
let audioBuffer;
let recordingTimeout;
let audioData = [];
const currentMsgAttachment = ref([]);
const sessionResourcesList = ref<IResourceItem[]>([]);
const resourcesSearchRef = ref(null);
const resourceSearchDialogShow = ref(false);
const uploadFileList = ref<UploadUserFile[]>([]);
const resourceUploadManagerRef = ref(null);
const attachmentButtonRef = ref(null);
function askQuestionPreCheck() {
  // 判断是否达到并发限制
  if (userBatchSize.value >= 1) {
    ElNotification.warning({
      title: '系统消息',
      message: '请等待当前问题处理完毕！',
      duration: 2000
    });
    return false;
  }
  // 判断是否为空
  if (!userInput.value || userInput.value.trim() === '') {
    ElNotification.warning({
      title: '系统消息',
      message: '请输入有效问题！',
      duration: 2000
    });
    return false;
  }
  // 判断会话情况
  if (!currentSession.session_code) {
    ElMessage.info('会话状态异常，请刷新页面重试！');
    return false;
  }
  return true;
}
async function askQuestion() {
  // 判断是否达到并发限制
  if (!askQuestionPreCheck()) {
    return;
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
    userQaID: targetQuestion.qa_item_idx,
    attachments: currentMsgAttachment.value.map(item => item.resource_id)
  });
  // 开始启动
  userInput.value = null;
  let params = {
    session_code: currentSession.session_code,
    messages: [
      {
        role: 'user',
        content: userMsgContent
      }
    ],
    app_code: currentSession.session_source,
    stream: props.streaming,
    attachments: []
  };
  if (currentMsgAttachment.value.length > 0) {
    params['attachments'] = currentMsgAttachment.value.map(item => item.resource_id);
    // 清空当前消息附件
    currentMsgAttachment.value = [];
  }
  userBatchSize.value += 1;
  let qaId = null;
  try {
    if (params.stream) {
      let data = await addMessages(params, msgAbortController.signal);
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
    } else {
      let data = await addMessages(params, null);
      emit('update-answer', {
        data: data,
        userQaID: targetQuestion.qa_item_idx
      });
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
async function stopQuestion(targetQuestion: IRunningQuestionMeta | null = null) {
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
      });
    } else {
      await askQuestion();
    }
  }
}
async function handleInputChange() {
  // 更新高度
  setTimeout(() => {
    const newHeight = Math.min(180, consoleInputRef.value.clientHeight + 130);
    emit('height-change', { newHeight: newHeight });
  }, 10);
}
async function clickRecommendQuestion(data) {
  userInput.value = data.question;
  userInputRef.value.focus();
  askQuestion();
}
const concatUint8Arrays = (...arrays) => {
  const totalLength = arrays.reduce((acc, arr) => acc + arr.length, 0);
  const result = new Uint8Array(totalLength);
  let offset = 0;
  for (const arr of arrays) {
    result.set(arr, offset);
    offset += arr.length;
  }
  return result;
};
async function resampleAudio(buffer, sourceRate, targetRate) {
  const offlineContext = new OfflineAudioContext(1, (buffer.length * targetRate) / sourceRate, targetRate);
  const source = offlineContext.createBufferSource();
  source.buffer = buffer;
  source.connect(offlineContext.destination);
  source.start();
  return await offlineContext.startRendering();
}
function sendAudioData() {
  if (audioBuffer.length >= 1280) {
    // 切割 1280B 的数据
    const chunk = audioBuffer.subarray(0, 1280);
    audioBuffer = audioBuffer.subarray(1280);
    // 发送数据到 WebSocket
    props.socket.emit('audio_message', {
      user_id: userInfo.value.user_id,
      data: chunk
    });
    // 存储数据块
    audioData.push(chunk);
  }

  // 持续发送，直到录音结束
  if (isRecording.value) {
    requestAnimationFrame(sendAudioData);
  }
}
async function startRecording(src) {
  // event.preventDefault();
  isRecording.value = true;
  try {
    // 创建音频上下文
    audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();

    // 获取音频输入
    const stream = await navigator.mediaDevices.getUserMedia({ audio: { sampleRate: { ideal: 16000 } } });

    // 打印实际采样率
    console.log('实际使用的采样率:', audioContext.sampleRate);

    // 创建 ScriptProcessorNode
    scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);

    // 连接节点
    mediaStreamSource = audioContext.createMediaStreamSource(stream);
    mediaStreamSource.connect(scriptProcessor);
    scriptProcessor.connect(audioContext.destination);

    // 缓存音频数据
    audioBuffer = new Uint8Array();

    // 处理音频数据
    scriptProcessor.onaudioprocess = async event => {
      const inputBuffer = event.inputBuffer;
      const actualSampleRate = audioContext.sampleRate;

      let processedBuffer = inputBuffer;
      if (actualSampleRate !== 16000) {
        processedBuffer = await resampleAudio(inputBuffer, actualSampleRate, 16000);
      }

      const inputData = processedBuffer.getChannelData(0);

      // 将浮点数转换为 16 位有符号整数
      const int16Data = new Int16Array(inputData.length);
      for (let i = 0; i < inputData.length; i++) {
        int16Data[i] = Math.round(inputData[i] * 32767);
      }
      const uint8Data = new Uint8Array(int16Data.buffer);
      audioBuffer = concatUint8Arrays(audioBuffer, uint8Data);
    };
    // 启动定时发送数据
    requestAnimationFrame(sendAudioData);
    // 设置 59 秒的录音时长限制
    recordingTimeout = setTimeout(() => {
      if (isRecording.value) {
        stopRecording('a');
      }
    }, 59 * 1000);
  } catch (error) {
    console.error('无法访问麦克风', error);
    ElNotification({
      title: '无法访问麦克风',
      message: '请检查是否有麦克风设备与相关权限',
      type: 'warning'
    });
  }
}
async function stopRecording(src) {
  // event.preventDefault();
  if (isRecording.value) {
    isRecording.value = false;
    try {
      scriptProcessor.disconnect();
      mediaStreamSource.disconnect();
      audioContext.close();
    } catch (e) {
      console.error('关闭音频上下文时出错', e);
      return;
    }

    // 清除定时器
    clearTimeout(recordingTimeout);
    if (audioBuffer.length > 0) {
      // 发送剩余数据到 WebSocket
      props.socket.emit('audio_message', {
        user_id: userInfo.value.user_id,
        data: audioBuffer,
        lastFrame: true
      });
      // 存储剩余数据块
      audioData.push(audioBuffer);
    }

    props.socket.emit('audio_message_stop', {
      user_id: userInfo.value.user_id
    });
    audioData = [];
    audioBuffer = new Uint8Array();
    console.log('录音结束');
    if (consoleInputRef.value) {
      askQuestion();
    }
  }
}
function updateQuestion(data: string) {
  userInput.value += data;
}
function handleUploadSuccess(data: any) {
  currentMsgAttachment.value.push(data);
  attachmentButtonRef.value?.hide();
}
async function handleRemoveAttachment(data: any) {
  const idx = currentMsgAttachment.value.findIndex(item => item.resource_id === data.resource_id);
  if (idx !== -1) {
    currentMsgAttachment.value.splice(idx, 1);
  }
  await attachmentRemoveFromSession({
    session_id: currentSession.id,
    resource_list: [data.resource_id]
  });
  await nextTick();
}
async function commitAddChooseResources() {
  resourceSearchDialogShow.value = false;
  sessionResourcesList.value = resourcesSearchRef.value?.getSelectedResources();
  let params = {
    session_id: currentSession.id,
    resource_list: []
  };
  if (sessionResourcesList.value) {
    for (let resource of sessionResourcesList.value) {
      params.resource_list.push(resource.id);
      currentMsgAttachment.value.push({
        resource_id: resource.id,
        resource_name: resource.resource_name,
        resource_icon: 'images/' + resource.resource_icon,
        resource_size: resource.resource_size_in_MB
      });
    }
    await attachmentAddResourcesIntoSession(params);
  }
  resourceSearchDialogShow.value = false;
  await nextTick();
}
async function initSessionAttachment() {
  if (!currentSession.id) {
    return;
  }
  const res = await attachmentSearchInSession({
    session_id: currentSession.id,
    msg_id: 0,
    attachment_sources: ['files']
  })
  if (!res.error_status) {
    currentMsgAttachment.value = res.result.map(item => ({
      resource_id: item.id,
      resource_name: item.resource_name,
      resource_icon: item.resource_icon?.includes("images/") || item.resource_icon?.includes("http") ? item.resource_icon : 'images/' + item.resource_icon,
      resource_size: item.resource_size_in_MB
    }));
  }
}
onMounted(async () => {
  if (window.innerWidth >= 768) {
    userInputRef.value.focus();
  }
  consoleHeight.value = props.height;
});
watch(
  () => props.session,
  async newVal => {
    if (newVal && newVal != currentSession) {
      Object.assign(currentSession, newVal);
      userInfo.value = await getInfo();
      await initSessionAttachment();
    }
  },
  { immediate: true, deep: true }
);
watch(
  () => props.height,
  newVal => {
    consoleHeight.value = newVal;
  }
);
defineExpose({
  clickRecommendQuestion,
  askQuestion,
  updateQuestion
});
</script>

<template>
  <div id="console-input" :style="{ height: consoleHeight }">
    <div id="console-input-box" ref="consoleInputRef">
      <div id="console-input-box-inner">
        <div id="console-input-box-inner-head">
          <AttachmentPreview
            :attachment-list="currentMsgAttachment"
            @remove-attachment="args => handleRemoveAttachment(args)"
          />
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
              :autosize="{ minRows: 2, maxRows: 6 }"
              @keydown.enter.prevent
              @keydown="handleKeyDown"
              @compositionend="userComposition = false"
              @compositionstart="userComposition = true"
              @input="handleInputChange"
            />
          </div>
        </div>
        <div id="console-input-box-inner-foot">
          <div class="std-middle-box">
            <el-popover ref="attachmentButtonRef" trigger="click">
              <template #reference>
                <el-image src="images/paperclip.svg" class="footer-icon" />
              </template>
              <div>
                <div class="std-middle-box">
                  <el-button text @click="resourceSearchDialogShow = true">From AI资源库</el-button>
                </div>
                <div class="std-middle-box">
                  <el-upload
                    ref="uploadFileRef"
                    v-model:file-list="uploadFileList"
                    action=""
                    :show-file-list="false"
                    :auto-upload="true"
                    multiple
                    name="chunk_content"
                    accept="*"
                    :before-upload="resourceUploadManagerRef?.prepareUploadFile"
                    :http-request="resourceUploadManagerRef?.uploadFileContent"
                    :on-success="resourceUploadManagerRef?.uploadFileSuccess"
                  >
                    <el-button text>From 本地文件</el-button>
                  </el-upload>
                  <div id="upload-box">
                    <ResourceUploadManager
                      ref="resourceUploadManagerRef"
                      v-model:file-list="uploadFileList"
                      v-model:current-session="currentSession"
                      @upload-success="data => handleUploadSuccess(data)"
                    />
                  </div>
                </div>
              </div>
            </el-popover>
          </div>
          <div class="std-middle-box">
            <div class="std-middle-box">
              <div
                class="input-button"
                @mousedown.prevent="startRecording(1)"
                @mouseup="stopRecording(2)"
                @touchstart.prevent="startRecording(3)"
                @touchend="stopRecording(4)"
              >
                <div v-show="isRecording" class="recording-box">
                  <div class="wave"></div>
                  <div class="wave"></div>
                  <div class="wave"></div>
                </div>
                <el-tooltip content="语音输入" placement="top">
                  <el-icon class="input-icon">
                    <Microphone v-show="!isRecording" class="input-icon" />
                    <VideoPause v-show="isRecording" class="input-icon" style="color: #c45656" />
                  </el-icon>
                </el-tooltip>
              </div>
            </div>
            <div class="std-middle-box">
              <div
                v-show="userBatchSize == 1"
                class="input-button"
                style="background-color: red"
                @click="stopQuestion()"
              >
                <el-image src="images/pause_white.svg" class="input-icon" />
              </div>
              <el-popover rigger="hover" width="300px">
                <template #reference>
                  <el-badge v-show="userBatchSize > 1" :value="userBatchSize">
                    <div class="input-button" style="background-color: red">
                      <el-image src="images/pause_white.svg" class="input-icon" />
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
                    <el-image src="images/close_red.svg" @click="stopQuestion(running_question)" />
                  </div>
                </div>
              </el-popover>
              <div v-show="!userBatchSize" class="input-button" @click="askQuestion()">
                <el-image src="images/send_blue.svg" class="input-icon" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="input-tips">
      <div class="std-middle-box">
        <el-text class="msg-tips-text"> 以上内容均由AI生成式模型生成，仅供参考 </el-text>
      </div>
    </div>
  </div>
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
#console-input-box-inner-foot {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 12px 16px;
  width: calc(100% - 32px);
}
.footer-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
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

#upload-box {
  position: fixed;
  bottom: 250px;
  right: 380px;
  max-width: 200px;
  z-index: 99;
}
#console-input-box-inner-head {
  width: calc(100% - 30px);
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
