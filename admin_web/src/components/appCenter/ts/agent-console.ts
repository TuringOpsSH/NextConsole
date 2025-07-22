import {nextTick, ref} from 'vue'
import {ElMessage} from "element-plus";

import {msg_item, msg_queue_item, reference_item, running_question_meta} from "@/types/next_console";
import {get_current_timestamp} from "@/utils/base";
import { search_messages, update_session} from "@/api/next_console";
import {addAppMessage} from "@/api/appCenterApi";
import {
  addAgentAppQa,
  AgentAppMsgFlow,
  CurrentAgent,
  CurrentAgentApp,
  CurrentAgentAppQas,
  CurrentAgentAppSession,
  CurrentAgentReference,
  getTargetAgentReference,
  QAWorkFlowMap,
  scrollToBottom, sessionAttachData
} from "@/components/appCenter/ts/agent-app";

import {user_info} from "@/components/user_center/user";
import {ElNotification} from "element-plus";
import {LLMInstance} from "@/types/config_center";

export const modelListRef = ref()
export const consoleInput = ref('')
export const consoleInputRef = ref()
export const consoleInputHeight = ref(130)
export const consoleInputInnerRef = ref()
export const userComposition = ref(false)
export const showSupDetailFlag = ref(false)
export const currentSupDetail =  ref<reference_item>()
export const isRecording = ref(false)
export const audioUrl = ref(null);
export const user_batch_size = ref(0)
export async function askAgentQuestion() {
  if (!consoleInput.value || consoleInput.value.trim() === '') {
    ElMessage.info(
      {
        message: "请输入有效问题！",
        duration: 2000
      }
    )
    return false
  }
  // 判断是否达到并发限制
  if (user_batch_size.value >= 3) {
    ElMessage.info(
      {
        message: "请等待当前问题处理完毕！",
        duration: 2000
      }
    )
    return false
  }
  // 用户输入预处理：将换行符替换为两个换行符
  let userMsgContent = consoleInput.value.replace(/\n/g, '\n\n')
  // 生成问答对占位
  let new_qa_item_idx = AgentAppMsgFlow.value.length
  let new_qa_item = <msg_queue_item>{
    qa_id: null,
    qa_status: null,
    qa_topic: null,
    qa_value: {
      question: [ <msg_item> {
        msg_content: userMsgContent,
        msg_role: "user",
        msg_parent_id: 0,
        create_time: get_current_timestamp(),
        msg_remark: 0,
        msg_version: 0,
        msg_id: 0,
        msg_del: 0,
        assistant_id: -12345,
        shop_assistant_id: null,
      }],
      answer: {}
    },
    qa_share_picked: 0,
    qa_progress_open: false,
    qa_workflow_open: false,
    show_button_question_area: false,
    show_button_answer_area: false,
    short_answer: null,
    qa_finished: false,
  }

  AgentAppMsgFlow.value.push(new_qa_item);

  let new_qa = await addAgentAppQa()
  if (!new_qa?.qa_id) {
    return
  }

  AgentAppMsgFlow.value[ new_qa_item_idx ].qa_id = new_qa.qa_id
  AgentAppMsgFlow.value[ new_qa_item_idx ].qa_status = new_qa.qa_status
  AgentAppMsgFlow.value[ new_qa_item_idx ].qa_topic = new_qa.qa_topic
  scrollToBottom()
  // 如果启动了rag，则打开工作流占位符
  if (CurrentAgentAppSession.value.session_search_engine_switch ||
    CurrentAgentAppSession.value.session_attachment_image_switch
    || CurrentAgentAppSession.value.session_local_resource_switch ||
    CurrentAgentAppSession.value.session_attachment_file_switch){
    QAWorkFlowMap.value[new_qa.qa_id] = [{
      qa_id: new_qa_item_idx,
      msg_id:  null,
      task_id: null,
      task_type:  null,
      task_instruction:null,
      task_params: null,
      task_result: null,
      task_create_time: null,
      task_begin_time:  null,
      task_update_time: null,
      task_end_time:  null,
      task_status: null,
    }]
  }


  // 保存问题
  let question_params = {
    session_id: CurrentAgentAppSession.value.id,
    qa_id: new_qa.qa_id,
    msg_content: userMsgContent,
    stream: false,
    session_source: CurrentAgentAppSession.value.session_source,
    msg_answer_flag: false
  }
  let data = await addAppMessage(question_params, null)
  if (data.error_status){
    return
  }
  let msg_parent_id = data.result.msg_id
  let msg_abort_controller = new AbortController()
  // 更新数据
  AgentAppMsgFlow.value[ new_qa_item_idx ].qa_value.question[0].msg_id = msg_parent_id
  AgentAppMsgFlow.value[ new_qa_item_idx ].qa_value.answer[msg_parent_id] = [
    <msg_item>{
      msg_content: "",
      msg_role: "assistant",
      msg_parent_id: 0,
      create_time: get_current_timestamp(),
      msg_remark: 0,
      msg_version: 0,
      msg_id: 0,
      msg_del: 0,
      assistant_id: CurrentAgent.value.id,
      shop_assistant_id: null
    }
  ]


  let target_question =  {
    qa_item_idx: new_qa_item_idx  ,
    begin_time: performance.now(),
    abort_controller:msg_abort_controller,
    end_time: null,
    status: 'running',
  }
  running_questions.value.push(target_question)

  // 开始启动
  consoleInput.value = null
  scrollToBottom()
  let params = {
    app_code: CurrentAgentApp.value.app_code,
    session_id: CurrentAgentAppSession.value.id,
    qa_id: CurrentAgentAppQas.value[0].qa_id,
    msg_content: userMsgContent,
    stream: true,
    session_source: CurrentAgentAppSession.value.session_source,
    msg_parent_id: msg_parent_id,
    session_attach_data: sessionAttachData.value
    // 是否开启query-agent
    // query_agent_open_flag: true
  }
  const startTime = performance.now();
  user_batch_size.value += 1
  try {

    let data = await add_app_messages(params, msg_abort_controller.signal)
    // 处理流式响应来更新消息
    const reader = data.body.getReader()
    let chunk = await reader.read()
    while (!chunk.done) {
      // 当第一个字符出现时，获取参考文献，关闭工作流展示区
      if (!AgentAppMsgFlow.value[
        new_qa_item_idx
        ].qa_value.answer[
        msg_parent_id][0].msg_content) {
        getTargetAgentReference(msg_parent_id)
        AgentAppMsgFlow.value[
          new_qa_item_idx
          ].qa_workflow_open = false
      }
      AgentAppMsgFlow.value[
        new_qa_item_idx
        ].qa_value.answer[
        msg_parent_id][0].msg_content += new TextDecoder('utf-8').decode(chunk.value)
      chunk = await reader.read()
      splitMarkdown(AgentAppMsgFlow.value[new_qa_item_idx])
      scrollToBottom()
    }
  }
  catch (e) {
    if (e.name == 'AbortError') {


    }

  }
  user_batch_size.value -= 1
  // 完成后更新回答结果的id
  let data2 = await search_messages(
    {
      "qa_id": [CurrentAgentAppQas.value[0].qa_id],
    }
  )
  if (!data2.error_status ) {
    try{
      AgentAppMsgFlow.value[
        new_qa_item_idx
        ].qa_value.answer[
        msg_parent_id
        ][0].msg_id = data2.result[0]?.qa_value.answer[msg_parent_id][0].msg_id
    }
    catch (e) {
      // console.log(e)
    }
  }
  add_copy_button_event()
  // 更新问题状态
  let idx = running_questions.value.indexOf(target_question)
  running_questions.value.splice(idx, 1)
  AgentAppMsgFlow.value[ new_qa_item_idx ].qa_finished = true
}

export async function stop_agent_question(target_question: running_question_meta | null = null){
  // 如果没有传入参数，则停止最新的问题
  if (!target_question){
    if (running_questions.value.length === 0){
      ElMessage({
        message: '没有正在运行的问题',
        type: 'warning'
      })
      return
    }
    target_question = running_questions.value[0]
  }

  // 将传入的消息队列中的所有问题停止
  target_question.abort_controller.abort()
  target_question.end_time = performance.now()
  // 从运行队列中删除
  let idx = running_questions.value.indexOf(target_question)
  running_questions.value.splice(idx, 1)
  ElMessage({
    message: '问题已停止',
    type: 'success'
  })
  AgentAppMsgFlow.value[ target_question.qa_item_idx ].qa_finished = true

  AgentAppMsgFlow.value[ target_question.qa_item_idx ].qa_value.answer[
    AgentAppMsgFlow.value[ target_question.qa_item_idx ].qa_value.question[0].msg_id
    ][0].msg_is_cut_off = true

}

export async function handleInputChange(val:string){
  // 更新高度
  setTimeout(()=>{
    consoleInputHeight.value = Math.max(130, consoleInputRef.value.clientHeight + 70)

  }, 10)

}
export async function handleKeyDown(event) {
  // 正确识别用户提交行为与换行行为
  if (event.key === 'Enter' && !userComposition.value) {
    if (event.ctrlKey|| event.shiftKey) {
      const start = event.target.selectionStart;
      const end = event.target.selectionEnd;
      if (!consoleInput.value) {
        return false
      }
      consoleInput.value = consoleInput.value.slice(0, start) + '\n' + consoleInput.value.slice(end);
      nextTick().then(() => {
        event.target.selectionStart = start + 1;
        event.target.selectionEnd = start + 1;
      });
    }
    else {
      askAgentQuestion()
    }
  }

}
export async function showSupDetail(item: msg_queue_item, event){
  if (event.target.tagName.toLowerCase() === 'sup'||
    (event.target.tagName.toLowerCase() === 'a' && event.target.parentElement.tagName.toLowerCase() === 'sup')) {
    showSupDetailFlag.value = true
    const targetRect = event.target.getBoundingClientRect();
    const mouseX = event.clientX;
    const mouseY = event.clientY;
    tooltipStyle.value = {
      position: 'absolute',
      top: `${window.scrollY + mouseY}px`, // 鼠标的Y轴位置
      left: `${window.scrollX + mouseX}px`, // 鼠标的X轴位置
    };
    let question_id = item.qa_value.question[0].msg_id
    let reference_list = CurrentAgentReference.value?.[question_id]// 获取 <sup> 的内容
    if (reference_list?.length){
      currentSupDetail.value = null
      for (let i = 0; i <= reference_list.length; i++) {
        if (i == event.target.textContent) {

          currentSupDetail.value = reference_list[i-1]
        }
      }
    }
  }
  else {
    showSupDetailFlag.value = false
  }
}

let audioContext;
let mediaStreamSource;
let scriptProcessor;
let audioBuffer ;
let recordingTimeout;
let audioData = [];

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
// 重采样音频数据
async function resampleAudio(buffer, sourceRate, targetRate) {
  const offlineContext = new OfflineAudioContext(1, buffer.length * targetRate / sourceRate, targetRate);
  const source = offlineContext.createBufferSource();
  source.buffer = buffer;
  source.connect(offlineContext.destination);
  source.start();
  return await offlineContext.startRendering();
}
// 定时器：每 40ms 切割并发送数据
const sendAudioData = () => {
  if (audioBuffer.length >= 1280) {
    // 切割 1280B 的数据
    const chunk = audioBuffer.subarray(0, 1280);
    audioBuffer = audioBuffer.subarray(1280);
    // 发送数据到 WebSocket
    socket.value.emit("whzy_audio_message", {
      user_id: user_info.value.user_id,
      data: chunk
    });
    // 存储数据块
    audioData.push(chunk);
  }

  // 持续发送，直到录音结束
  if (isRecording.value) {
    requestAnimationFrame(sendAudioData);
  }
};

export async function startRecording(source:number) {
  // event.preventDefault();

  console.log('开始录音', source)
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
    scriptProcessor.onaudioprocess = async (event) => {
      const inputBuffer = event.inputBuffer;
      const actualSampleRate = audioContext.sampleRate;

      let processedBuffer = inputBuffer;
      if (actualSampleRate!== 16000) {
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

    isRecording.value = true;

    // 启动定时发送数据
    requestAnimationFrame(sendAudioData);
    // 设置 59 秒的录音时长限制
    recordingTimeout = setTimeout(() => {
      if (isRecording) {
        stopRecording();
      }
    }, 59 * 1000);
  } catch (error) {
    console.error("无法访问麦克风:", error);
    ElNotification({
      title: "无法访问麦克风",
      message: "请检查是否有麦克风设备与相关权限",
      type: "warning",
    });
  }
}


export async function stopRecording(source:number) {
  // event.preventDefault();
  console.log(source)
  if (isRecording.value) {
    isRecording.value = false;
    scriptProcessor?.disconnect();
    mediaStreamSource?.disconnect();
    audioContext?.close();
    // 清除定时器
    clearTimeout(recordingTimeout);
    if (audioBuffer.length > 0) {
      // 发送剩余数据到 WebSocket
      socket.value.emit("whzy_audio_message", {
        user_id: user_info.value.user_id,
        data: audioBuffer,
        LastFrame: true
      });
      // 存储剩余数据块
      audioData.push(audioBuffer);
    }

    socket.value.emit("whzy_audio_message_stop", {
      user_id: user_info.value.user_id
    });
    // 合并所有数据块
    // const fullAudioData = concatUint8Arrays(...audioData);
    // 将录音数据转换为 Blob 对象
    // const audioBlob = createWavBlob(fullAudioData);

    // 生成 URL
    // audioUrl.value = URL.createObjectURL(audioBlob);
    // console.log(audioUrl.value, audioBlob.size);
    // 清空存储的数据块数组和音频缓冲区
    audioData = [];
    audioBuffer = new Uint8Array();
    console.log("录音结束");

  }
}

export async function  switchLlmInstance(item:LLMInstance){
  // 切换llm_instance
  // welcome界面
  if (!CurrentAgentAppSession.value.id){
    console.log('item', item.llm_code, CurrentAgentAppSession.value.session_llm_code)
    CurrentAgentAppSession.value.session_llm_code = item.llm_code
    modelListRef.value?.hide()
    ElMessage.success("切换成功!")
    // // console.log('item', item.llm_code, current_session.session_llm_code)
    return
  }
  let params = {
    session_id : CurrentAgentAppSession.value.id,
    session_llm_code: item.llm_code,
  }
  let data = await update_session(params)
  if (!data.error_status){
    CurrentAgentAppSession.value.session_llm_code = item.llm_code
    modelListRef.value?.hide()
    ElMessage.success("切换成功!")
  }
}
export function getSessionLlmName(){
  let current_llm_name = '火山引擎/DeepSeek-V3'
  if (CurrentAgentAppSession.value.session_llm_code){
    for (let i = 0; i < llm_instance_queue.value.length; i++) {
      if (llm_instance_queue.value[i].llm_code === CurrentAgentAppSession.value.session_llm_code){
        current_llm_name = llm_instance_queue.value[i].llm_desc
        if (window.innerWidth < 768){
          current_llm_name = llm_instance_queue.value[i].llm_type
        }
        break
      }
    }
  }
  return current_llm_name
}
export function get_running_progress(target_question: running_question_meta){


  try{
    let msg_parent_id = msg_flow.value[target_question.qa_item_idx].qa_value.question[0].msg_id
    return msg_flow.value[target_question.qa_item_idx].qa_value.answer[msg_parent_id][0].msg_content?.length
  } catch (e) {
    console.error(e)
    return 0
  }

}
