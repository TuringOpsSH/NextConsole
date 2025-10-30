<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue';
import { genFileId, UploadRawFile, UploadUserFile } from 'element-plus';
import { onMounted, ref, watch, nextTick } from 'vue';
import { attachment_remove_from_session as attachmentRemoveFromSession } from '@/api/next-console';
import AttachmentPreview, { IAttachmentDetail } from './AttachmentPreview.vue';
import ResourceUploadManager from './ResourceUploadManager.vue';
const props = defineProps({
  sessionId: {
    type: Number,
    required: true,
    default: 0
  },
  file: {
    type: Object,
    required: true,
    default: () => ({})
  },
  accept: {
    type: String,
    required: false,
    default: '*'
  }
});
const uploadFileRef = ref(null);
const uploadFileList = ref<UploadUserFile[]>([]);
const resourceUploadManagerRef = ref(null);
const localSessionId = ref(0);
const currentFile = ref<IAttachmentDetail>({});
const currentSession = ref({
  id: localSessionId.value
});
const localAccept = ref('*');
const localAcceptDesc = ref('所有');
const localAcceptFormat = ref([]);
const emits = defineEmits(['update:file']);
async function handleExceed(files) {
  uploadFileRef.value.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  uploadFileRef.value!.handleStart(file);
  uploadFileRef.value?.submit();
}
async function handleRemoveAttachment(uploadFile: UploadFile, uploadFiles: UploadFiles) {
  await attachmentRemoveFromSession({
    session_id: localSessionId.value,
    resource_list: [currentFile.value.resource_id]
  });
  currentFile.value.resource_id = 0;
  await nextTick();
  emits('update:file', null);
}
async function handleUploadSuccess(data) {
  currentFile.value = data;
  emits('update:file', data);
}
function getFileIcon(format: string) {
  let icon_format_map = {
    // 文档类型
    doc: 'doc.svg',
    docx: 'docx.svg',
    xls: 'xls.svg',
    xlsx: 'xlsx.svg',
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
  const formatIcon = icon_format_map[format] || 'file_format_other.svg';
  return '/images/' + formatIcon;
}
watch(
  () => props.file,
  async newVal => {
    currentFile.value = newVal;
  },
  { immediate: true }
);
watch(
  () => props.sessionId,
  async newVal => {
    localSessionId.value = newVal;
    currentSession.value.id = newVal;
  },
  { immediate: true }
);
watch(
  () => props.accept,
  async newVal => {
    if (!newVal) {
      localAccept.value = '*';
      return;
    }
    if (typeof newVal === 'object') {
      if (newVal.includes('all')) {
        localAccept.value = '*';
        localAcceptDesc.value = '所有';
        return;
      }
      localAccept.value = '';
      localAcceptDesc.value = '';
      localAcceptFormat.value = [];
      for (const item of newVal) {
        localAccept.value += '.' + item + ',';
        localAcceptDesc.value += item + '/';
        localAcceptFormat.value.push(getFileIcon(item));
      }
      // 去除最后一个字符
      localAccept.value = localAccept.value.slice(0, -1);
      localAcceptDesc.value = localAcceptDesc.value.slice(0, -1);
      return;
    }
    localAccept.value = newVal;
  },
  { immediate: true }
);
</script>

<template>
  <el-upload
    ref="uploadFileRef"
    v-model:file-list="uploadFileList"
    action=""
    :limit="1"
    :show-file-list="false"
    :auto-upload="true"
    name="chunk_content"
    :on-exceed="handleExceed"
    :accept="localAccept"
    drag
    :before-upload="resourceUploadManagerRef?.prepareUploadFile"
    :http-request="resourceUploadManagerRef?.uploadFileContent"
    :on-success="resourceUploadManagerRef?.uploadFileSuccess"
    :on-remove="handleRemoveAttachment"
  >
    <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
    <div>
      <el-image v-for="format in localAcceptFormat" :src="format" />
    </div>
    <div class="el-upload__text">拖拽文件至此或者 <em>点击上传</em></div>
    <template #tip>
      <div class="el-upload__tip">可接受的文件类型：{{ localAcceptDesc }}</div>
    </template>
  </el-upload>
  <AttachmentPreview
    v-if="currentFile?.resource_id"
    :attachment-list="[currentFile]"
    @remove-attachment="args => handleRemoveAttachment(args)"
  />
  <div id="upload-box">
    <ResourceUploadManager
      ref="resourceUploadManagerRef"
      v-model:file-list="uploadFileList"
      v-model:current-session="currentSession"
      source="session-params"
      @upload-success="data => handleUploadSuccess(data)"
    />
  </div>
</template>

<style scoped>
#upload-box {
  position: fixed;
  bottom: 250px;
  right: 380px;
  max-width: 200px;
  z-index: 99;
}
</style>
