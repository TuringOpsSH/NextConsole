<script setup lang="ts">
import {ArrowRight} from '@element-plus/icons-vue';
import {onBeforeUnmount, reactive, ref, watch} from 'vue';
import {show_resource_list} from '@/components/resource/resource_list/resource_list';
import {currentPathTree,} from '@/components/resource/resource_view/resource_viewer';
import WebOfficeSDK from '@/components/global/wps/web-office-sdk-solution-v2.0.7.es.js';
import {add_copy_button_event, md_answer} from '@/components/next_console/messages_flow/message_flow';
import Resource_view_tree from '@/components/resource/resource_tree/resource_view_tree.vue';
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import {getToken} from "@/utils/auth";
import {clientFingerprint, getFingerPrint} from "@/components/global/web_socket/web_socket";
import {get_resource_object_path, resource_view_meta_get} from "@/api/resource_api";
import {user_info} from "@/components/user_center/user";
import {ResourceItem} from "@/types/resource_type";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js";
import markdownItKatex from "@vscode/markdown-it-katex";
import markdownItMermaid from "markdown-it-mermaid-plugin";
import MarkdownTasks from "markdown-it-task-lists";
import * as pdfjsLib from 'pdfjs-dist';
import 'pdfjs-dist/web/pdf_viewer.css';
import 'pdfjs-dist/build/pdf.worker.min.mjs';

const props = defineProps({
  resource_id: {
    type: String,
    default: '',
    required: false
  }
});
const currentWebPageMode = ref('preview');
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
const WPSInstance = ref(null);
const resourceViewerLoading = ref(false);
const wpsContainer = ref<HTMLDivElement | null>(null);
const tableHTML = ref('');
const currentMarkdownMode = ref('preview');
let mdAnswer = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str, lang) {
    let language = lang ? lang : 'plaintext';
    let languageText = '<span style="">' + language + '</span>';
    let copyButton =
        '<img src="images/copy.svg" alt="复制" class="answer-code-copy" style="width: 20px;height: 20px;cursor: pointer"/>';
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
const nodeEnv = import.meta.env.VITE_APP_NODE_ENV
function viewCodeResourceToMd() {
  let code = currentViewResource.resource_content;
  if (!code) {
    return '';
  }
  code = '```' + currentViewResource.resource_format + '\n' + code + '\n```';
  // 渲染
  return md_answer.render(code);

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
async function getParentResourceList() {
  if (!currentViewResource.id) {
    currentPathTree.value = [];
    return;
  }
  if (currentViewResource.user_id === user_info.value.user_id) {
    currentPathTree.value.push(
        // @ts-ignore
        {
          id: null,
          resource_name: '我的资源',
          resource_type: 'folder',
          resource_status: '正常',
          resource_type_cn: '文件夹'
        }
    );
  } else {
    currentPathTree.value.push(
        // @ts-ignore
        {
          id: null,
          resource_name: '共享资源',
          resource_type: 'folder',
          resource_status: '正常',
          resource_type_cn: '文件夹'
        }
    );
  }

  let params = {
    resource_id: currentViewResource.id
  };
  let res = await get_resource_object_path(params);
  if (!res.error_status) {
    currentPathTree.value = res.result.data;
  }
}

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


async function initResourceViewer() {
  getParentResourceList()
  resourceViewerLoading.value = true;
  await getCurrentResourceObject();
  resourceViewerLoading.value = false;
  console.log(currentViewResource.view_config?.engine)
  if (currentViewResource.view_config?.engine == "wps") {
    await initWpsDoc();
  } else if (currentViewResource.view_config?.engine == "vue-office") {

  } else if (currentViewResource.view_config?.engine == "markdown") {
    add_copy_button_event();
  } else if (currentViewResource.view_config?.engine == "json") {

  } else if (currentViewResource.view_config?.engine == "excel") {
    await initExcelViewer()
  } else if (currentViewResource.view_config?.engine == "text") {

  } else if (currentViewResource.view_config?.engine == "webpage") {

  } else if (currentViewResource.view_config?.engine == "embed-pdf" && nodeEnv == 'private') {
    // 初始化PDF查看器
    await initPdfViewer();
  } else if (currentViewResource.view_config?.engine == "video") {

  } else if (currentViewResource.view_config?.engine == "audio") {

  } else {
    console.warn('当前文件类型不支持在线预览');
  }
}

async function initWpsDoc() {

  // 启用wps 进行渲染
  let token = getToken();

  // @ts-ignore
  WPSInstance.value = WebOfficeSDK.init({
    officeType: getWpsType(),
    appId: currentViewResource.view_config?.wps_config?.wps_app_id,
    fileId: currentViewResource.id,
    mount: document.querySelector('#WPS_APP'),
    token: token
  });
  await WPSInstance.value.ready();
  WPSInstance.value.iframe.style.width='100vw';

}
async function initPdfViewer() {
  try {
    const loadingTask = pdfjsLib.getDocument(currentViewResource.resource_show_url);
    const pdf = await loadingTask.promise;
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

      // 将每个 canvas 元素添加一个间隔样式，便于区分不同页面
      canvas.style.marginBottom = '20px';

      // 将 canvas 添加到容器中
      pdfContainer.value.appendChild(canvas);

      // 渲染页面
      const renderContext = {
        canvasContext: context,
        viewport: viewport
      };
      await page.render(renderContext).promise;
    }
  } catch (error) {
    console.error('Error rendering PDF:', error);
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
const handleMouseEnter = (event, index) => {
  const target = event.target;
  currentPathTree.value[index].isOverflow = target.scrollWidth > target.clientWidth;
};
function renderMarkdown() {
  return mdAnswer.render(currentViewResource.resource_content);
}
onBeforeUnmount(() => {
  WPSInstance.value?.destroy();
});
watch(
    () => props.resource_id,
    async (newResourceID) => {
      currentViewResource.id = parseInt(newResourceID);
      await initResourceViewer();
    },
    {
      immediate: true,
      deep: true
    }
);
</script>

<template>
  <el-container class="resource-viewer-container">
    <el-header style="padding: 0 !important">
      <div id="resource_header_area">
        <div id="resource_header">
          <div id="resource_path">
            <el-breadcrumb
              :separator-icon="ArrowRight"
              style="display: flex; flex-direction: row; align-items: center; justify-content: flex-start"
            >
              <el-breadcrumb-item
                v-for="(item, index) in currentPathTree"
                :key="item.id"
                @click="show_resource_list(item)"
              >
                <el-tooltip :content="item.resource_name" effect="light" :disabled="!item.isOverflow">
                  <el-text
                    truncated
                    class="resource-sub-path"
                    :class="{
                      'resource-sub-path-last': index == currentPathTree?.length - 1
                    }"
                    @mouseenter="handleMouseEnter($event, index)"
                  >
                    {{ item?.resource_name }}
                  </el-text>
                </el-tooltip>
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
        </div>
      </div>
    </el-header>
    <el-main style="padding: 0 !important">
      <div id="resource_view_main" v-loading="resourceViewerLoading" element-loading-text="加载中">
        <el-scrollbar style="width: 100%">
          <div v-if="currentViewResource?.view_config?.support">
            <div v-if="currentViewResource?.view_config?.engine == 'markdown'" class="view-area"
                 style="align-items: flex-start">
              <el-tabs v-model="currentMarkdownMode" style="width: 100%">
                <el-tab-pane name="preview" label="预览" >
                  <div v-html="renderMarkdown()" style="width: 100%" />
                </el-tab-pane>
                <el-tab-pane name="code" label="源码">
                  <div v-html="viewCodeResourceToMd()" style="width: 100%" />
                </el-tab-pane>
              </el-tabs>
            </div>
            <div v-else-if="currentViewResource?.view_config?.engine == 'json'" class="view-area"
                 style="justify-content: flex-start; align-items: flex-start">
              <vue-json-pretty
                  :data="currentViewResource.view_config.data"
                  :showLength="true"
                  :showLineNumber="true"
                  :showIcon="true"
                  :showSelectController="true"
              />
            </div>
            <div v-else-if="currentViewResource?.view_config?.engine == 'text'" class="view-area"
                 style="justify-content: flex-start;align-items: flex-start">
              <div class="text-area">
                <el-text size="large"> {{ currentViewResource.resource_content }}</el-text>
              </div>
            </div>
            <div v-else-if="currentViewResource?.view_config?.engine == 'element'" class="view-area">
              <div class="std-middle-box" style="align-items: flex-start">
                <el-image :src="currentViewResource.resource_show_url" />
              </div>
            </div>
            <div v-else-if="currentViewResource?.view_config?.engine == 'video'" class="view-area">
              <div style="width: 100%; height: 100%" class="std-middle-box">
                <video controls width="600">
                  <source :src="currentViewResource.resource_show_url" type="video/mp4" />
                  <source :src="currentViewResource.resource_show_url" type="video/webm" />
                  <source :src="currentViewResource.resource_show_url" type="video/ogg" />
                  Your browser does not support the video tag.
                </video>
              </div>
            </div>
            <div v-else-if="currentViewResource?.view_config?.engine == 'audio'" class="view-area">
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
              <el-tabs v-model="currentWebPageMode" style="width: 100%">
                <el-tab-pane name="preview" label="预览">
                  <div style="padding: 16px" class="std-middle-box" v-if="currentViewResource.resource_source_url">
                    <iframe
                        :src="currentViewResource.resource_source_url"
                        style="width: 100%; height: calc(100vh - 200px); border: none"
                    ></iframe>
                  </div>
                  <div style="padding: 16px" class="std-middle-box" v-else>
                    <iframe
                        :srcdoc="currentViewResource.resource_content"
                        style="width: 100%; height: calc(100vh - 200px); border: none"
                    ></iframe>
                  </div>
                </el-tab-pane>
                <el-tab-pane name="code" label="源码">
                  <div style="padding: 16px" class="std-middle-box">
                    <div v-html="viewCodeResourceToMd()" style="width: 100%" />
                  </div>
                </el-tab-pane>
              </el-tabs>
            </div>
            <div v-else-if="currentViewResource?.view_config?.engine == 'wps'" class="view-area">
              <div id="WPS_APP" ref="wpsContainer" />
            </div>
            <div v-else-if="currentViewResource?.view_config?.engine == 'embed-pdf'" class="view-area"
                 style="justify-content: flex-start">
              <embed :src="currentViewResource?.resource_show_url" type="application/pdf"
                     width="100%" height="100%" style="border: none" v-if="nodeEnv !='private'">
              <div v-else ref="pdfContainer" style="width: 100%; height: 100%;" />
            </div>
            <div v-else-if="currentViewResource?.view_config?.engine == 'excel'" class="view-area"
                 style="justify-content: flex-start">
              <div style="padding: 16px" class="std-middle-box" v-if="currentViewResource.resource_show_url">
                <iframe id="excel-iframe"
                    style="width: 100%; height: calc(100vh - 200px); border: none"
                ></iframe>
              </div>
            </div>
          </div>
          <div v-else-if="resourceViewerLoading">
            <el-result icon="info" title="文件加载中" />
          </div>
          <div v-else class="view-area">
            <el-result
              v-show="!resourceViewerLoading"
              icon="info"
              title="此文件暂不支持在线查看"
              sub-title="Sorry, This file does not currently support online viewing"
            />
          </div>
        </el-scrollbar>
      </div>
    </el-main>
    <el-footer height="48px" style="padding: 0 !important; background-color: #f9fafb"> </el-footer>
  </el-container>
  <resource_view_tree />
</template>

<style scoped lang="scss">
#resource_header_area {
  display: flex;
  flex-direction: column;
  width: 100%;

  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
#resource_header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  height: 24px;
}
#resource_path {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 16px;
  width: calc(100% - 32px);
}
.resource-sub-path {
  cursor: pointer;
  font-size: 14px;
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.resource-sub-path:hover {
  color: #8ec5fc;
}
.resource-sub-path-last {
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  color: #101828;
}
#resource_view_main {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 108px);
  flex: 1;
}
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
  justify-content: center;
  align-items: center;
  padding: 16px;
  height: calc(100vh - 140px);
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
.excel-table td, .excel-table th {
  border: 1px solid #ddd;
  padding: 8px;
}
.excel-table th {
  background-color: #f2f2f2;
}
@media (width < 768px) {
  .resource-sub-path {
    cursor: pointer;
    font-size: 12px;
  }
  .resource-sub-path-last {
    font-weight: 600;
    font-size: 12px;
    line-height: 14px;
    color: #101828;
    cursor: default;
  }
}
</style>
