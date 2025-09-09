<script setup lang="ts">
import { onBeforeUnmount, reactive, ref, watch } from 'vue';
import VueJsonPretty from 'vue-json-pretty';
import WebOfficeSDK from '@/components/global/wps/web-office-sdk-solution-v2.0.7.es.js';
import { add_copy_button_event } from '@/components/next-console/messages-flow/message_flow';
import { useUserInfoStore } from '@/stores/userInfoStore';
import { ResourceItem } from '@/types/resource-type';
import 'vue-json-pretty/lib/styles.css';
import { clientFingerprint, getFingerPrint } from '@/components/global/web_socket';
import { resource_view_meta_get } from '@/api/resource-api';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';
import markdownItKatex from '@vscode/markdown-it-katex';
import markdownItMermaid from 'markdown-it-mermaid-plugin';
import MarkdownTasks from 'markdown-it-task-lists';
import * as pdfjsLib from 'pdfjs-dist';
import 'pdfjs-dist/web/pdf_viewer.css';
import 'pdfjs-dist/build/pdf.worker.min.mjs';
import PDFObject from 'pdfobject';
import { ElMessage } from 'element-plus';

const props = defineProps({
  resourceId: {
    type: Number,
    default: 0,
    required: true
  }
});
const userInfoStore = useUserInfoStore();
const currentViewResource = reactive<ResourceItem>(
  // @ts-ignore
  {
    sub_rag_file_cnt: 0,
    id: null,
    resource_parent_id: null,
    user_id: null,
    resource_name: null,
    resource_type: null,
    resource_desc: null,
    resource_icon: null,
    resource_format: null,
    resource_path: null,
    resource_size_in_MB: null,
    resource_status: null,
    rag_status: null,
    create_time: null,
    update_time: null,
    delete_time: null,
    show_buttons: null,
    resource_parent_name: null,
    resource_is_selected: null,
    sub_resource_dir_cnt: null,
    sub_resource_file_cnt: null,
    resource_feature_code: '',
    resource_is_supported: false,
    resource_show_url: '',
    resource_source_url: '',
    resource_title: '',
    resource_source: 'resource_center',
    ref_text: null,
    rerank_score: null,
    view_config: {}
  }
);
const resourceViewerLoading = ref(false);
const WPSInstance = ref(null);
const wpsContainer = ref<HTMLDivElement | null>(null);
let mdAnswer = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str, lang) {
    let language = lang ? lang : 'plaintext';
    let languageText = '<span style="">' + language + '</span>';
    let copyButton =
      '<img src="/images/copy.svg" alt="复制" class="answer-code-copy" style="width: 20px;height: 20px;cursor: pointer"/>';
    let header =
      '<div style="display: flex;justify-content: space-between;border-bottom: 1px solid #D0D5DD;padding: 8px">' +
      languageText +
      copyButton +
      '</div>';

    if (hljs.getLanguage(language)) {
      try {
        return (
          '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative;' +
          'border-bottom: 1px solid #D0D5DD;padding: 16px">' +
          header +
          '<code class="hljs-code" >' +
          '<br>' +
          hljs.highlight(str, { language: language, ignoreIllegals: true }).value +
          '<br>' +
          '</code></pre>'
        );
      } catch (__) {}
    }

    return (
      '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative;' +
      'border-bottom: 1px solid #D0D5DD;padding: 16px">' +
      header +
      '<code class="hljs-code" >' +
      '<br>' +
      hljs.highlight(str, { language: 'plaintext', ignoreIllegals: true }).value +
      '<br>' +
      '</code></pre>'
    );
  }
});
const defaultTableRule =
  mdAnswer.renderer.rules.table_open ||
  function (tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
  };
mdAnswer.renderer.rules.table_open = function (tokens, idx, options, env, self) {
  tokens[idx].attrPush(['class', 'custom-table']);
  return defaultTableRule(tokens, idx, options, env, self);
};
mdAnswer.use(markdownItKatex, {
  throwOnError: false,
  errorColor: ' #cc0000',
  strict: false // 允许非标准语法
});
mdAnswer.use(markdownItMermaid);
const customTableStyle = `
    <style>
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
    }
    .custom-table th, .custom-table td {
        border: 1px solid #D0D5DD;
        padding: 8px;
        text-align: left;
    }
    .custom-table th {
        background-color: #f2f2f2;
    }
    </style>
`;
document.head.insertAdjacentHTML('beforeend', customTableStyle);
mdAnswer.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx];
  const src = token.attrGet('src');
  const alt = token.content;
  const title = token.attrGet('title');
  const isLast = env.is_last;
  const imgHtml = `<img src="${src}" alt="${alt}" title="${title}" style="max-width: 100%">`;

  if (isLast) {
    return ` <div style="text-align: center;">${src}</div> `;
  }

  return ` <div style="text-align: center;">${imgHtml}</div> `;
};
// 自定义链接样式
mdAnswer.renderer.rules.link_open = function (tokens, idx, options, env, self) {
  const aIndex = tokens[idx].attrIndex('target');

  if (aIndex < 0) {
    tokens[idx].attrPush(['target', '_blank']); // 添加 target="_blank"
  } else {
    tokens[idx].attrs[aIndex][1] = '_blank';
  }
  return self.renderToken(tokens, idx, options);
};
// 自定义引用样式
mdAnswer.renderer.rules.blockquote_open = function (tokens, idx, options, env, self) {
  tokens[idx].attrSet('class', 'my-custom-quote');
  return self.renderToken(tokens, idx, options);
};
// 任务列表
mdAnswer.use(MarkdownTasks);
const pdfContainer = ref(null);
const nodeEnv = import.meta.env.VITE_APP_NODE_ENV;
async function getCurrentResourceObject() {
  if (!clientFingerprint.value) {
    await getFingerPrint();
  }
  let params = {
    resource_id: currentViewResource.id,
    clientFingerprint: clientFingerprint.value
  };
  resourceViewerLoading.value = true;
  let res = await resource_view_meta_get(params);
  if (!res.error_status) {
    Object.assign(currentViewResource, res.result);
  }
  resourceViewerLoading.value = false;
}
function getWpsType() {
  if (!currentViewResource.resource_format) {
    return '';
  }
  if (
    [
      'doc',
      'dot',
      'wps',
      'wpt',
      'docx',
      'dotx',
      'docm',
      'dotm',
      'rtf',
      'txt',
      'xml',
      'mhtml',
      'mht',
      'html',
      'htm',
      'uof',
      'uot3'
    ].includes(currentViewResource.resource_format)
  ) {
    return WebOfficeSDK.OfficeType.Writer;
  }
  if (
    ['xls', 'xlt', 'et', 'ett', 'xlsx', 'xltx', 'xlsm', 'xltm', 'csv'].includes(currentViewResource.resource_format)
  ) {
    return WebOfficeSDK.OfficeType.Spreadsheet;
  }
  if (
    ['ppt', 'pptx', 'pptm', 'ppsx', 'ppsm', 'pps', 'potx', 'potm', 'dpt', 'dps', 'pot'].includes(
      currentViewResource.resource_format
    )
  ) {
    return WebOfficeSDK.OfficeType.Presentation;
  }
  if (['pdf', 'ofd'].includes(currentViewResource.resource_format)) {
    return WebOfficeSDK.OfficeType.Pdf;
  }
  if (currentViewResource.resource_format == 'otl') {
    return WebOfficeSDK.OfficeType.Otl;
  }
  if (currentViewResource.resource_format == 'dbt') {
    return WebOfficeSDK.OfficeType.Dbt;
  }
  return WebOfficeSDK.OfficeType.Writer;
}
async function initWpsDoc() {
  // 启用wps 进行渲染
  // @ts-ignore
  WPSInstance.value = WebOfficeSDK.init({
    officeType: getWpsType(),
    appId: currentViewResource.view_config?.wps_config?.wps_app_id,
    fileId: currentViewResource.id,
    mount: document.querySelector('#WPS_APP'),
    token: userInfoStore.token
  });
  await WPSInstance.value.ready();
  WPSInstance.value.iframe.style.width = '100vw';
}
async function initPdfViewer() {
  try {
    const pdf = await pdfjsLib.getDocument(currentViewResource.resource_show_url).promise;
    // 获取 PDF 的总页数
    const numPages = pdf.numPages;
    // 遍历每一页
    for (let pageNum = 1; pageNum <= numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const scale = 1.5;
      const viewport = page.getViewport({ scale: scale });

      // 创建一个 canvas 元素用于渲染 PDF 页面
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      canvas.height = viewport.height;
      canvas.width = viewport.width;
      canvas.style.marginBottom = '20px';
      pdfContainer.value.appendChild(canvas);
      // 渲染页面
      const renderContext = {
        canvasContext: context,
        viewport: viewport
      };
      await page.render(renderContext).promise;
    }
  } catch (error) {
    console.log(error, 'PDF加载失败', '尝试使用其他方式加载');
    try {
      const pdfOptions = {
        // 可选配置
        pdfOpenParams: {
          view: 'FitV', // 适合宽度查看
          page: 1, // 默认打开第一页
          zoom: 100 // 100%缩放
        }
      };
      pdfContainer.value.innerHTML = '';
      const success = PDFObject.embed(currentViewResource.resource_show_url, pdfContainer.value, pdfOptions);
      if (!success) {
        ElMessage.info('您的浏览器不支持 PDF 预览，请下载查看');
      }
    } catch (error) {
      console.error('PDF加载失败', error);
    }
  }
}
async function initExcelViewer() {
  if (!currentViewResource.resource_show_url) {
    return;
  }
  if (nodeEnv == 'private') {
    const response = await fetch(currentViewResource.resource_show_url);
    const blob = await response.blob();
    document.getElementById('excel-iframe').src = URL.createObjectURL(blob);
  } else {
    document.getElementById('excel-iframe').src = currentViewResource.resource_show_url;
  }
}
async function initResourceViewer() {
  await getCurrentResourceObject();
  if (currentViewResource.view_config?.engine == 'wps') {
    await initWpsDoc();
  } else if (currentViewResource.view_config?.engine == 'vue-office') {
  } else if (currentViewResource.view_config?.engine == 'markdown') {
    add_copy_button_event();
  } else if (currentViewResource.view_config?.engine == 'json') {
  } else if (currentViewResource.view_config?.engine == 'excel') {
    await initExcelViewer();
  } else if (currentViewResource.view_config?.engine == 'text') {
  } else if (currentViewResource.view_config?.engine == 'webpage') {
  } else if (currentViewResource.view_config?.engine == 'embed-pdf' && nodeEnv == 'private') {
    // 初始化PDF查看器
    await initPdfViewer();
  } else if (currentViewResource.view_config?.engine == 'video') {
  } else if (currentViewResource.view_config?.engine == 'audio') {
  } else {
    console.warn('当前文件类型不支持在线预览');
  }
}
function renderMarkdown() {
  return mdAnswer.render(currentViewResource.resource_content || '');
}
watch(
  () => props.resourceId,
  async newResourceID => {
    currentViewResource.id = newResourceID;
  },
  {
    immediate: true,
    deep: true
  }
);

onBeforeUnmount(() => {
  WPSInstance.value?.destroy();
});
defineExpose({
  initResourceViewer
});
</script>

<template>
  <el-scrollbar>
    <div v-loading="resourceViewerLoading" element-loading-text="加载中" style="height: 100%">
      <div v-if="currentViewResource?.view_config?.engine == 'markdown'" class="view-area">
        <div v-html="renderMarkdown()" />
      </div>
      <div v-else-if="currentViewResource?.view_config?.engine == 'json'" class="view-area">
        <VueJsonPretty
          :data="currentViewResource.view_config.data"
          :show-length="true"
          :show-line-number="true"
          :show-icon="true"
          :show-select-controller="true"
        />
      </div>
      <div v-else-if="currentViewResource?.view_config?.engine == 'text'" class="view-area">
        <div class="text-area">
          <el-text size="large"> {{ currentViewResource.resource_content }}</el-text>
        </div>
      </div>
      <div
        v-else-if="currentViewResource?.view_config?.engine == 'element'"
        class="view-area"
        style="align-items: center; justify-content: center"
      >
        <div class="std-middle-box">
          <el-image :src="currentViewResource.resource_show_url" />
        </div>
      </div>
      <div
        v-else-if="currentViewResource?.view_config?.engine == 'video'"
        class="view-area"
        style="align-items: center; justify-content: center"
      >
        <div style="width: 100%; height: 100%" class="std-middle-box">
          <video controls width="600">
            <source :src="currentViewResource.resource_show_url" type="video/mp4" />
            <source :src="currentViewResource.resource_show_url" type="video/webm" />
            <source :src="currentViewResource.resource_show_url" type="video/ogg" />
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
      <div
        v-else-if="currentViewResource?.view_config?.engine == 'audio'"
        class="view-area"
        style="align-items: center; justify-content: center"
      >
        <div style="width: 100%; height: 100%" class="std-middle-box">
          <audio controls>
            <source :src="currentViewResource.resource_show_url" type="audio/mpeg" />
            <source :src="currentViewResource.resource_show_url" type="audio/ogg" />
            <source :src="currentViewResource.resource_show_url" type="audio/wav" />
            <source :src="currentViewResource.resource_show_url" type="audio/mp4" />
            <source :src="currentViewResource.resource_show_url" type="audio/x-m4a" />
            Your browser does not support the video tag.
          </audio>
        </div>
      </div>
      <div v-else-if="currentViewResource?.view_config?.engine == 'webpage'" class="view-area">
        <div v-if="currentViewResource.resource_source_url" style="padding: 16px" class="std-middle-box">
          <iframe
            :src="currentViewResource.resource_source_url"
            style="width: 100%; height: calc(100vh - 200px); border: none"
          />
        </div>
        <div v-else style="padding: 16px" class="std-middle-box">
          <iframe
            :srcdoc="currentViewResource.resource_content"
            style="width: 100%; height: calc(100vh - 200px); border: none"
          />
        </div>
      </div>
      <div v-else-if="currentViewResource?.view_config?.engine == 'wps'" class="view-area">
        <div id="WPS_APP" ref="wpsContainer" />
      </div>
      <div
        v-else-if="currentViewResource?.view_config?.engine == 'embed-pdf'"
        class="view-area"
        style="height: calc(100vh - 120px)"
      >
        <embed
          v-if="nodeEnv != 'private'"
          :src="currentViewResource?.resource_show_url"
          type="application/pdf"
          width="100%"
          height="100%"
          style="border: none"
        />
        <div v-else ref="pdfContainer" style="width: 100%; height: 100%" />
      </div>
      <div
        v-else-if="currentViewResource?.view_config?.engine == 'excel'"
        class="view-area"
        style="justify-content: flex-start"
      >
        <div v-if="currentViewResource.resource_show_url" class="std-middle-box">
          <iframe id="excel-iframe" style="width: 100%; height: calc(100vh - 200px); border: none" />
        </div>
      </div>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}
.view-area {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  height: 100%;
}
#WPS_APP {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 140px);
  width: 100%;
}
#WPS_APP iframe {
  width: 100% !important;
  height: 100% !important;
  border: none;
}
.text-area {
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  background-color: #ffffff;
  word-break: break-word;
  &:hover {
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
}
/* 增强表格样式 */
.excel-table table {
  border-collapse: collapse;
  width: 100%;
}
.excel-table td,
.excel-table th {
  border: 1px solid #ddd;
  padding: 8px;
}
.excel-table th {
  background-color: #f2f2f2;
}
</style>
