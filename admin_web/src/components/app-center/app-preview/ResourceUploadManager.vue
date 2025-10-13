<script setup lang="ts">
import { enc } from 'crypto-js';
import sha256 from 'crypto-js/sha256';
import {
  ElNotification,
  UploadFile,
  UploadFiles,
  UploadRawFile,
  UploadRequestOptions,
  UploadUserFile
} from 'element-plus';
import { ref, watch } from 'vue';
import {
  attachment_base_init as attachmentBaseInit,
  attachment_add_into_session as attachmentAddIntoSession
} from '@/api/next-console';
import {
  update_upload_task as updateUploadTask,
  add_upload_task as addUploadTask,
  upload_resource_object as uploadResourceObject
} from '@/api/resource-api';
interface IResourceUploadItem {
  id: number | null;
  resource_parent_id: number | null;
  resource_id: number | null;
  resource_name: string | null;
  resource_size_in_mb: number | null;
  resource_type: string | null;
  resource_format: string | null;
  content_max_idx: number | null;
  content_finish_idx: number | null;
  resource_md5: string | null;
  task_icon: string | null;
  task_source: string | null;
  task_status: string | null;
  create_time: string | null;
  update_time: string | null;
  raw_file: UploadRawFile | null;
  task_error_msg?: string | null;
  uid?: number;
}
const props = defineProps({
  currentSession: {
    type: Object || Number,
    required: false,
    default: () => ({})
  },
  fileList: {
    type: Array as () => UploadUserFile[],
    required: true
  },
  source: {
    type: String,
    required: false,
    default: 'files'
  }
});
const emit = defineEmits([
  'upload-success',
  'upload-finished',
]);
const localCurrentSession = ref({
  id: null
});
const uploadFileList = ref([]);
const showUploadManageBox = ref(false);
const uploadFileTaskList = ref<IResourceUploadItem[]>([]);
const uploadManagerStatus = ref('pending');
const uploadSize = ref(1);
const finishTimeSizeMap = ref({});
const showCloseConfirmFlag = ref(false);
const showUploadFileDetail = ref(true);
const localSource = ref('files');
function cleanUploadManager() {
  uploadFileList.value = [];
  // 更新后端上传任务状态
  for (let i = 0; i < uploadFileTaskList.value.length; i++) {
    if (
      uploadFileTaskList.value[i].task_status !== 'success' &&
      uploadFileTaskList.value[i].task_status !== 'error' &&
      uploadFileTaskList.value[i].task_status !== 'abort' &&
      uploadFileTaskList.value[i].id
    ) {
      let params = {
        task_id: uploadFileTaskList.value[i].id,
        task_status: 'abort'
      };
      updateUploadTask(params);
    }
  }

  uploadFileTaskList.value = [];
  uploadManagerStatus.value = 'pending';
  showUploadManageBox.value = false;
  showCloseConfirmFlag.value = false;
}
function closeUploadManager(notice: boolean = true) {
  // 关闭上传管理器
  // 检查任务状态，如果有任务正在上传，提示用户是否关闭
  if (notice) {
    for (let i = 0; i < uploadFileTaskList.value.length; i++) {
      if (
        uploadFileTaskList.value[i].task_status !== 'success' &&
        uploadFileTaskList.value[i].task_error_msg !== '空'
      ) {
        showCloseConfirmFlag.value = true;
        return false;
      }
    }
  }
  showUploadManageBox.value = false;
  cleanUploadManager();
}
function getSuccessUploadTask() {
  // 获取已经上传成功的文件数量
  let count = 0;
  for (let i = 0; i < uploadFileTaskList.value.length; i++) {
    if (uploadFileTaskList.value[i].task_status === 'success') {
      count++;
    }
  }
  return count;
}
function getSuccessUploadSize() {
  // 获取已经上传成功的文件大小
  let size = 0;
  for (let i = 0; i < uploadFileTaskList.value.length; i++) {
    if (uploadFileTaskList.value[i].task_status === 'success') {
      size += uploadFileTaskList.value[i].resource_size_in_mb;
    }
  }
  return parseFloat(size.toFixed(4));
}
function getUploadSpeed() {
  // 获取上传速度: 3s内上传的文件大小
  let currentTime = Date.now();
  let lastTime = currentTime - 3000;
  let finishUploadSizeIn3s = 0;
  for (let key in finishTimeSizeMap.value) {
    if (parseInt(key) > lastTime) {
      finishUploadSizeIn3s += finishTimeSizeMap.value[key];
    }
  }
  return parseFloat((finishUploadSizeIn3s / 1024 / 1024 / 3).toFixed(2));
}
async function pauseAllUploadTask() {
  // 暂停所有上传任务
  for (let i = 0; i < uploadFileTaskList.value.length; i++) {
    if (uploadFileTaskList.value[i].task_status !== 'uploading') {
      continue;
    }
    uploadFileTaskList.value[i].task_status = 'pause';
    uploadFileTaskList.value[i].content_finish_idx -= 1;
    // 更新后端上传任务状态
    let params = {
      task_id: uploadFileTaskList.value[i].id,
      task_status: 'pause'
    };
    updateUploadTask(params);
  }
  uploadManagerStatus.value = 'pause';
}
async function continueAllUploadTask() {
  // 继续所有上传任务
  for (let i = 0; i < uploadFileTaskList.value.length; i++) {
    if (uploadFileTaskList.value[i].task_status === 'pause') {
      // 更新后端上传任务状态
      let params = {
        task_id: uploadFileTaskList.value[i].id,
        task_status: 'uploading'
      };
      await updateUploadTask(params);

      uploadFileTaskList.value[i].task_status = 'uploading';
      uploadFileContent(<UploadRequestOptions>{
        file: uploadFileTaskList.value[i].raw_file,
        data: {},
        headers: {}
      });
    }
  }
  uploadManagerStatus.value = 'uploading';
}
async function calculateMD5(file: UploadRawFile): Promise<string> {
  // 计算文件的MD5值
  try {
    const arrayBuffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle?.digest('SHA-256', arrayBuffer);
    if (!hashBuffer) {
      return;
    }
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  } catch (e) {
    return;
  }
}
async function calculateSHA256(file: UploadRawFile): Promise<string> {
  // 计算文件的SHA256值
  const arrayBuffer = await file.arrayBuffer();
  const wordArray = enc.Latin1.parse(
    Array.from(new Uint8Array(arrayBuffer))
      .map(byte => String.fromCharCode(byte))
      .join('')
  );
  return sha256(wordArray).toString(enc.Hex);
}
function getUploadTaskProgress(item: IResourceUploadItem, output: string = 'number') {
  // 获取上传任务进度,以MB为单位或者以比例返回
  if (item.content_finish_idx === -1) {
    return 0;
  }
  if (output === 'number') {
    if (item.task_status === 'success') {
      return parseFloat(item.resource_size_in_mb.toFixed(4));
    }
    return item.content_finish_idx * uploadSize.value;
  }
  let progress = Math.floor(((item.content_finish_idx * uploadSize.value) / item.resource_size_in_mb) * 100);
  return parseFloat(progress.toFixed(4));
}
async function initUploadTask(targetUploadTask: IResourceUploadItem) {
  let res = await addUploadTask({
    resource_parent_id: targetUploadTask.resource_parent_id,
    resource_name: targetUploadTask.resource_name,
    resource_size: targetUploadTask.resource_size_in_mb,
    resource_type: targetUploadTask.resource_type,
    resource_format: targetUploadTask.resource_format,
    task_source: targetUploadTask.task_source,
    content_max_idx: targetUploadTask.content_max_idx,
    resource_md5: targetUploadTask.resource_md5
  });
  if (!res.error_status && !res.error_message) {
    // 4. 更新上传任务列表
    targetUploadTask.id = res.result.id;
    uploadManagerStatus.value = 'uploading';
    targetUploadTask.resource_name = res.result.resource_name;
    targetUploadTask.resource_type = res.result.resource_type;
    targetUploadTask.resource_format = res.result.resource_format;
    targetUploadTask.task_icon = res.result.task_icon;
    targetUploadTask.task_status = res.result.task_status;
  } else {
    targetUploadTask.task_status = 'error';
    targetUploadTask.task_error_msg = '空';
    return false;
  }
}
async function execUploadTask(targetUploadTask: IResourceUploadItem) {
  let contentSize = 1024 * 1024 * uploadSize.value;
  let content = null;
  let chunkMD5 = '';
  // 从已经上传的位置开始上传，默认为-1
  let res = null;
  try {
    let beginIdx = targetUploadTask.content_finish_idx + 1;
    for (let i = beginIdx; i <= targetUploadTask.content_max_idx; i++) {
      if (targetUploadTask.task_status === 'pause') {
        return false;
      }
      let startIdx = i * contentSize;
      let endIdx = (i + 1) * contentSize;
      if (endIdx > targetUploadTask.raw_file.size) {
        endIdx = targetUploadTask.raw_file.size;
      }
      content = targetUploadTask.raw_file.slice(startIdx, endIdx);
      try {
        chunkMD5 = await calculateMD5(content);
        if (!chunkMD5) {
          chunkMD5 = await calculateSHA256(content);
        }
      } catch (e) {
        chunkMD5 = await calculateSHA256(content);
      }
      let uploadContentForm = new FormData();
      uploadContentForm.append('chunk_task_id', targetUploadTask.id.toString());
      uploadContentForm.append('chunk_index', i.toString());
      uploadContentForm.append('chunk_content', content);
      uploadContentForm.append('chunk_MD5', chunkMD5);
      uploadContentForm.append('chunk_size', content.size);
      res = await uploadResourceObject(uploadContentForm);
      if (!res.error_status) {
        // 上传成功，更新位置
        targetUploadTask.content_finish_idx = i;
        let finishTime = Date.now();
        if (!finishTimeSizeMap.value[finishTime]) {
          finishTimeSizeMap.value[finishTime] = 0;
        }
        finishTimeSizeMap.value[finishTime] += endIdx - startIdx;
      } else {
        targetUploadTask.task_status = 'error';
        return false;
      }
    }
    return res;
  } catch (e) {
    targetUploadTask.task_status = 'error';
    ElNotification.error({
      title: '系统通知',
      message: '上传文件内容失败' + e,
      duration: 5000
    });
    return false;
  }
}
async function uploadFileContent(options: UploadRequestOptions) {
  // 分块上传文件内容
  let { file, data, headers } = options;
  let targetUploadTask = uploadFileTaskList.value.find(item => item.raw_file.uid === file.uid);
  if (!targetUploadTask) {
    return false;
  }
  if (!targetUploadTask.id) {
    // 3. 生成上传任务
    await initUploadTask(targetUploadTask);
  }
  targetUploadTask.task_status = 'uploading';
  // 循环上传文件内容
  const execRes = await execUploadTask(targetUploadTask);
  if (!execRes) {
    return false;
  }
  // 上传成功，更新状态
  targetUploadTask.task_status = 'success';
  // 更新后端上传任务状态
  let params = {
    task_id: targetUploadTask.id,
    task_status: 'success'
  };
  updateUploadTask(params);
  let failFlag = false;
  for (let i = 0; i < uploadFileTaskList.value.length; i++) {
    if (uploadFileTaskList.value[i].task_status !== 'success') {
      failFlag = true;
      break;
    }
  }
  if (!failFlag) {
    uploadManagerStatus.value = 'success';
  }
  return execRes;
}
async function pauseUploadTask(item: IResourceUploadItem) {
  // 暂停上传任务,修改任务状态为pause
  item.task_status = 'pause';
  item.content_finish_idx -= 1;
  let params = {
    task_id: item.id,
    task_status: 'pause'
  };
  updateUploadTask(params);
  // 更新管理器状态：如果所有任务都暂停了，那么管理器状态也为pause
  let allPause = true;
  for (let i = 0; i < uploadFileTaskList.value.length; i++) {
    if (uploadFileTaskList.value[i].task_status !== 'pause') {
      allPause = false;
      break;
    }
  }
  if (allPause) {
    uploadManagerStatus.value = 'pause';
  }
}
async function removeUploadTask(item: IResourceUploadItem) {
  // 删除上传任务
  let index = uploadFileTaskList.value.findIndex(value => value.id === item.id);
  uploadFileTaskList.value.splice(index, 1);
  // 更新后端上传任务状态
  let params = {
    task_id: item.id,
    task_status: 'abort'
  };
  updateUploadTask(params);
}
async function retryUploadTask(item: IResourceUploadItem) {
  // 重试上传任务
  if (item.task_status === 'error') {
    // 更新后端上传任务状态
    let params = {
      task_id: item.id,
      task_status: 'pending'
    };
    await updateUploadTask(params);
    item.task_status = 'pending';
    item.content_finish_idx = -1;
    await uploadFileContent(<UploadRequestOptions>{
      file: item.raw_file,
      data: {},
      headers: {}
    });
    // 更新管理器状态
    uploadManagerStatus.value = 'uploading';
  } else {
    ElNotification.error({
      title: '系统通知',
      message: '任务状态不是错误状态，无法重试',
      duration: 5000
    });
  }
}
async function continueUploadTask(item: IResourceUploadItem) {
  // 更新后端上传任务状态
  let params = {
    task_id: item.id,
    task_status: 'uploading'
  };
  await updateUploadTask(params);
  // 继续上传任务,修改任务状态为uploading，然后继续上传
  item.task_status = 'uploading';
  uploadFileContent(<UploadRequestOptions>{
    file: item.raw_file,
    data: {},
    headers: {}
  });
  // 更新管理器状态
  uploadManagerStatus.value = 'uploading';
}
function getTaskIcon(resourceType: string, resourceFormat: string) {
  // 获取任务图标
  let iconBaseUrl = '/images/';
  let iconUrl = 'other.svg';
  let iconFormatMap = {
    // 文档类型
    doc: 'doc.svg',
    docx: 'doc.svg',
    xls: 'xls.svg',
    xlsx: 'xls.svg',
    csv: 'csv.svg',
    ppt: 'ppt.svg',
    pptx: 'pptx.svg',
    pdf: 'pdf.svg',
    txt: 'txt.svg',
    // 图片类型
    jpeg: 'jpeg.svg',
    jpg: 'jpg.svg',
    png: 'png.svg',
    gif: 'gif.svg',
    bmp: 'bmp.svg',
    webp: 'webp.svg',
    svg: 'svg.svg',
    // 视频类型
    mp4: 'mp4.svg',
    avi: 'avi.svg',
    mkv: 'mkv.svg',
    flv: 'flv.svg',
    mov: 'mov.svg',
    wmv: 'wmv.svg',
    webm: 'webm.svg',
    mpg: 'mpg.svg',
    '3gp': '3gp.svg',
    mpeg: 'mpeg.svg',
    // 音频类型
    mp3: 'mp3.svg',
    wav: 'wav.svg',
    wma: 'wma.svg',
    flac: 'flac.svg',
    aac: 'aac.svg',
    ogg: 'ogg.svg',
    m4a: 'm4a.svg',
    amr: 'amr.svg',
    aiff: 'aiff.svg',
    aif: 'aif.svg',
    ra: 'ra.svg',
    // 代码
    css: 'css.svg',
    js: 'js.svg',
    json: 'json.svg',
    xml: 'xml.svg',
    java: 'java.svg',
    cpp: 'cpp.svg',
    c: 'c.svg',
    py: 'py.svg',
    php: 'php.svg',
    go: 'go.svg',
    h: 'h.svg',
    hpp: 'hpp.svg',
    rb: 'rb.svg',
    cs: 'cs.svg',
    sh: 'sh.svg',
    bat: 'bat.svg',
    swift: 'swift.svg',
    kt: 'kt.svg',
    ts: 'ts.svg',
    pl: 'pl.svg',
    lua: 'lua.svg',
    r: 'r.svg',
    scala: 'scala.svg',
    sql: 'sql.svg',
    vb: 'vb.svg',
    vbs: 'vbs.svg',
    yaml: 'yaml.svg',
    yml: 'yml.svg',
    md: 'md.svg',
    ps1: 'ps1.svg',
    ini: 'ini.svg',
    conf: 'conf.svg',
    properties: 'properties.svg',
    cmd: 'cmd.svg',
    vue: 'vue.svg',
    jsx: 'jsx.svg',
    perl: 'perl.svg',
    db2: 'db2.svg',
    rs: 'rs.svg',
    mm: 'mm.svg',
    m: 'm.svg',
    plsql: 'plsql.svg',
    hs: 'hs.svg',
    hsc: 'hsc.svg',
    Dockerfile: 'Dockerfile.svg',
    dart: 'dart.svg',
    pm: 'pm.svg',
    bash: 'bash.svg',
    svelte: 'svelte.svg',

    // 压缩包
    zip: 'zip.svg',
    rar: 'rar.svg',
    '7z': '7z.svg',
    gz: 'gz.svg',
    tar: 'tar.svg',
    // 网页
    html: 'html.svg',
    htm: 'htm.svg.svg',
    // 二进制程序
    exe: 'exe.svg',
    apk: 'apk.svg',
    ipa: 'ipa.svg',
    deb: 'deb.svg',
    rpm: 'rpm.svg',
    dmg: 'dmg.svg',
    msi: 'msi.svg',
    bin: 'bin.svg',
    iso: 'iso.svg'
  };
  if (iconFormatMap[resourceFormat]) {
    iconUrl = iconFormatMap[resourceFormat];
    return iconBaseUrl + iconUrl;
  }
  let iconTypeMap = {};
  if (iconTypeMap[resourceType]) {
    return iconTypeMap[resourceType];
  }
  return iconBaseUrl + iconUrl;
}
async function prepareUploadFile(uploadFile: UploadRawFile) {
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
  let contentMaxIdx = Math.floor(resourceSize / uploadSize.value);
  // 前端临时可视化文件类型和格式
  let resourceType = '';
  let resourceFormat = '';
  if (uploadFile.name.indexOf('.') > -1) {
    resourceFormat = uploadFile.name.split('.').pop().toLowerCase();
  }
  resourceType = uploadFile.type;
  let taskIcon = getTaskIcon(resourceType, resourceFormat);
  // 3. 初始化会话资源文件夹并获取到资源文件夹id
  showUploadManageBox.value = true;
  let resourceParentId = null;
  if (localCurrentSession.value?.id) {
    let initRes = await attachmentBaseInit({
      session_id: localCurrentSession.value.id
    });
    if (initRes.error_status) {
      return false;
    }
    resourceParentId = initRes.result.id;
  }
  uploadFileTaskList.value.push({
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
  let resourceId = response.result?.resource_id;
  if (!resourceId) {
    return;
  }
  if (!localCurrentSession.value?.id) {
    return;
  }
  let params = {
    session_id: localCurrentSession.value.id,
    resource_id: resourceId,
    attachment_source: localSource.value,
  };
  attachmentAddIntoSession(params);
  // 判断是否全部任务完成，完成则关闭上传管理框
  let finishFlag = true;
  for (let i = 0; i < uploadFileTaskList.value.length; i++) {
    if (
      uploadFileTaskList.value[i].task_status == 'pending' ||
      uploadFileTaskList.value[i].task_status == 'uploading'
    ) {
      finishFlag = false;
      break;
    }
  }
  emit('upload-success', {
    resource_id: resourceId,
    resource_name: response.result?.resource_name,
    resource_icon: response.result?.task_icon,
    resource_size: response.result?.resource_size_in_mb
  });
  if (finishFlag) {
    closeUploadManager();
    emit('upload-finished');
  }
}
watch(
  () => props.fileList,
  newFileList => {
    if (newFileList.length > 0) {
      uploadFileList.value = newFileList;
    }
  },
  { immediate: true }
);
watch(
  () => props.currentSession,
  newSession => {
    localCurrentSession.value.id = newSession?.id;
  },
  { immediate: true , deep: true}
);
watch(
  () => props.source,
  newSource => {
    localSource.value = newSource;
  },
  { immediate: true }
);
defineExpose({
  closeUploadManager,
  cleanUploadManager,
  getTaskIcon,
  calculateMD5,
  calculateSHA256,
  prepareUploadFile,
  uploadFileContent,
  uploadFileSuccess
});

</script>

<template>
  <div v-show="showUploadManageBox" id="upload_manager">
    <div id="upload_header">
      <div id="upload_header_left">
        <div id="upload_status_icon">
          <el-image src="/images/upload_blue.svg" style="width: 20px; height: 20px" />
        </div>
        <div v-show="uploadManagerStatus == 'uploading'" id="upload_status_text">
          <el-text>上传中 {{ getSuccessUploadTask() }}/{{ uploadFileTaskList.length }}</el-text>
        </div>
        <div v-show="uploadManagerStatus == 'pending'" id="upload_status_text">
          <el-text>上传中 0/{{ uploadFileTaskList.length }}</el-text>
        </div>
        <div v-show="uploadManagerStatus == 'pause'" id="upload_status_text">
          <el-text type="warning">全部暂停</el-text>
        </div>
        <div v-show="uploadManagerStatus == 'success'" id="upload_status_text">
          <el-text type="success">全部上传成功</el-text>
        </div>
      </div>
      <div id="upload_header_right">
        <div class="upload_button" @click="showUploadFileDetail = !showUploadFileDetail">
          <el-image
            v-show="showUploadFileDetail"
            src="/images/triangle_down_blue.svg"
            style="width: 20px; height: 20px"
          />
          <el-image
            v-show="!showUploadFileDetail"
            src="/images/triangle_right_grey.svg"
            style="width: 20px; height: 20px"
          />
        </div>
        <div class="upload_button" @click="closeUploadManager()">
          <el-image src="/images/close_grey.svg" style="width: 20px; height: 20px" />
        </div>
      </div>
    </div>
    <div v-show="showUploadFileDetail" id="upload_status">
      <div id="upload_status_left">
        <el-text v-show="uploadManagerStatus == 'pause'">
          已上传 {{ getSuccessUploadTask() }}/{{ uploadFileTaskList.length }} 个任务
        </el-text>
        <el-text v-show="uploadManagerStatus == 'success'">
          已上传 {{ getSuccessUploadTask() }} 个任务, 共 {{ getSuccessUploadSize() }}MB
        </el-text>
        <el-text v-show="uploadManagerStatus == 'uploading'">速度： {{ getUploadSpeed() }} MB/s</el-text>
      </div>
      <div id="upload_status_right">
        <div v-show="uploadManagerStatus == 'uploading'" class="upload_button" @click="pauseAllUploadTask()">
          <el-text>全部暂停</el-text>
        </div>
        <div v-show="uploadManagerStatus == 'pause'" class="upload_button" @click="continueAllUploadTask()">
          <el-text>全部继续</el-text>
        </div>
      </div>
    </div>
    <el-scrollbar wrap-style="width : 100%" view-style="width : 100%" style="width: 100%">
      <div v-show="showUploadFileDetail" id="upload_queue">
        <div v-for="item in uploadFileTaskList" :key="item.id" class="upload-task-item">
          <div class="upload-task-left">
            <div class="upload-task-icon">
              <img :src="item?.task_icon" alt="" class="resource-icon" />
            </div>
            <div class="upload-task-meta">
              <div class="upload-task-name">
                <el-text truncated style="max-width: 300px">{{ item?.resource_name }}</el-text>
              </div>
              <div class="upload-task-progress-box">
                <el-text class="upload-task-progress-text">
                  {{ getUploadTaskProgress(item) }} MB / {{ parseFloat(item.resource_size_in_mb.toFixed(4)) }}MB
                </el-text>
              </div>
            </div>
          </div>
          <div class="upload-task-right">
            <div v-show="item.task_status == 'uploading'" class="upload-task-right-button-area">
              <el-progress :percentage="getUploadTaskProgress(item, 'progress')" type="circle" :width="40" />
              <div class="upload-button" @click="pauseUploadTask(item)">
                <el-image src="/images/pause_blue.svg" class="upload-button-icon" />
              </div>
            </div>
            <div v-show="item.task_status == 'success'" class="upload-task-right-button-area">
              <el-image src="/images/success_grey.svg" class="upload-button-icon" />
            </div>
            <div
              v-show="item.task_status != 'uploading' && item.task_status != 'success'"
              class="upload-task-right-button-area"
            >
              <el-tooltip v-if="item.task_status == 'error'" content="文件为空，无法上传">
                <el-image src="/images/notice_error_small.svg" class="upload-button-icon" />
              </el-tooltip>
              <div v-show="item.task_status != 'success'" class="upload-button" @click="removeUploadTask(item)">
                <el-image src="/images/close_grey.svg" class="upload-button-icon" />
              </div>
              <div v-show="item.task_status == 'error'" class="upload-button" @click="retryUploadTask(item)">
                <el-image src="/images/retry_grey.svg" class="upload-button-icon" />
              </div>
              <div v-show="item.task_status == 'pause'" class="upload-button" @click="continueUploadTask(item)">
                <el-image src="/images/continue.svg" class="upload-button-icon" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-scrollbar>
  </div>

  <el-dialog v-model="showCloseConfirmFlag" style="max-width: 400px" top="40vh" :close-on-click-modal="false">
    <div id="upload_close_confirm_box">
      <div>
        <el-text id="close_confirm_text">仍有任务未完成，确认关闭上传管理器？</el-text>
      </div>
      <div id="upload_close_confirm_button_box">
        <el-button style="width: 120px" @click="showCloseConfirmFlag = false">取消</el-button>
        <el-button style="width: 120px" type="primary" @click="cleanUploadManager()">确认</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
#upload_manager {
  display: flex;
  max-width: 900px;
  min-width: 500px;
  max-height: 500px;
  width: calc(100% - 20px);
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  border: 1px solid #ebeef5;
  border-radius: 5px;
  margin: 10px;
  padding: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 999;
  background-color: white;
}
#upload_header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: calc(100% - 20px);
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
}
#upload_header_left {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  padding: 10px;
  gap: 10px;
}
#upload_header_right {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  padding: 10px;
}
.upload_button {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
#upload_status {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: calc(100% - 20px);
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
  background-color: #f0f0f0;
}
#upload_status_left {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}
#upload_status_right {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}
#upload_queue {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  width: calc(100% - 20px);
  padding: 10px;
  gap: 10px;
  max-height: 300px;
}
.upload-task-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
  width: calc(100% - 20px);
}
.upload-task-left {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}
#upload_close_confirm_box {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 10px;
  padding: 10px;
  width: calc(100% - 20px);
}
#upload_close_confirm_button_box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 10px;
  width: calc(100% - 20px);
}
#close_confirm_text {
  color: #101828;
  text-align: center;

  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 24px;
}
.upload-task-progress-text {
  font-weight: 300;
  font-size: 12px;
  line-height: 14px;
  color: #606266;
}
.upload-task-icon {
  width: 24px;
  height: 24px;
}
.upload-button {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.upload-button-icon {
  width: 16px;
  height: 16px;
}
.upload-task-right-button-area {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}
.upload-task-meta {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 2px;
}
.upload-task-name {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
.upload-task-progress-box {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
.resource-icon {
  width: 22px;
  height: 22px;
  margin-right: 4px;
}
@media (width < 768px) {
  #upload_manager {
    width: 300px;
    min-width: 200px;
  }
}
</style>
