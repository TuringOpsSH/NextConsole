<script setup lang="ts">
import {ResourceItem} from "@/types/resource_type";
import {reactive, ref, watch} from 'vue';
import {resource_parse_get} from "@/api/resource_api";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js";
import markdownItKatex from "@vscode/markdown-it-katex";
import markdownItMermaid from "markdown-it-mermaid-plugin";
import MarkdownTasks from "markdown-it-task-lists";

const props = defineProps({
  resourceId: {
    type: Number,
    default: 0,
    required: true
  },
})
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
async function initResourceParser() {
  resourceViewerLoading.value = true;
  try {
    const res = await resource_parse_get({
      resource_id: currentViewResource.id,
    });
    if (!res.error_message) {
      Object.assign(currentViewResource, res.result);
    } else {
      console.error(res.error_message);
    }
  } catch (error) {
    console.error('Error fetching resource metadata:', error);
    console.error('获取资源元数据失败，请稍后重试。');
  } finally {
    resourceViewerLoading.value = false;
  }
}
function renderMarkdown() {
  if (!currentViewResource.resource_content) {
    return '<div class="std-middle-box"><div class="view-area">暂无内容</div></div>';
  }
  return mdAnswer.render(currentViewResource.resource_content);
}
watch(
    () => props.resourceId,
    async (newResourceID) => {
      currentViewResource.id = newResourceID;
    },
    {
      immediate: true,
      deep: true
    }
);
defineExpose({
  initResourceParser
});
</script>

<template>
  <el-scrollbar>
    <div v-loading="resourceViewerLoading" element-loading-text="加载中" style="height: 100%">
      <div v-html="renderMarkdown()" />
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
}
</style>